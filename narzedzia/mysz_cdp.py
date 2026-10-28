"""Klient Chrome DevTools Protocol na bibliotece standardowej: uruchamia Chrome bez okna pod blokadą /tmp/przewodnik-chrome.lock, na wolnym porcie, wysyła prawdziwe zdarzenia myszy i robi zrzuty."""

import base64
import fcntl
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

from narzedzia.zrzuty import CHROME, flagi_chrome

BLOKADA = "/tmp/przewodnik-chrome.lock"  # ta sama blokada, której używa `flock` w poleceniach powłoki
LIMIT_STARTU = 20  # sekundy na plik DevToolsActivePort


def ramka(dane: bytes, maska: bytes | None = None) -> bytes:
    """Ramka tekstowa WebSocket (FIN, opcode 1) z maską klienta; maska losowa, gdy nie podano."""
    maska = maska if maska is not None else os.urandom(4)
    n = len(dane)
    naglowek = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack(">H", n) if n < 65536 else bytes([0x80 | 127]) + struct.pack(">Q", n))
    return naglowek + maska + bytes(b ^ maska[i % 4] for i, b in enumerate(dane))


def odczytaj_ramke(czytaj) -> tuple[int, bool, bytes]:
    """Jedna ramka od serwera: (opcode, czy ostatnia, dane); `czytaj(n)` zwraca dokładnie n bajtów."""
    b1, b2 = czytaj(2)
    n = b2 & 0x7F
    if n == 126:
        n = struct.unpack(">H", czytaj(2))[0]
    elif n == 127:
        n = struct.unpack(">Q", czytaj(8))[0]
    maska = czytaj(4) if b2 & 0x80 else None
    dane = czytaj(n)
    if maska:
        dane = bytes(b ^ maska[i % 4] for i, b in enumerate(dane))
    return b1 & 0x0F, bool(b1 & 0x80), dane


class Polaczenie:
    """Gniazdo WebSocket do jednej karty Chrome: wysyła polecenia protokołu i czeka na odpowiedź o tym samym numerze."""

    def __init__(self, port: int, sciezka: str):
        self.gniazdo = socket.create_connection(("127.0.0.1", port), timeout=30)
        klucz = base64.b64encode(os.urandom(16)).decode()
        self.gniazdo.sendall((f"GET {sciezka} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {klucz}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        odpowiedz = b""
        while b"\r\n\r\n" not in odpowiedz:
            odpowiedz += self._porcja(1)
        if b" 101 " not in odpowiedz.split(b"\r\n")[0]:
            raise RuntimeError(f"Chrome odrzucił połączenie DevTools: {odpowiedz[:80]!r}")
        self.numer = 0

    def _porcja(self, n: int) -> bytes:
        dane = self.gniazdo.recv(n)
        if not dane:
            raise ConnectionError("Chrome zamknął połączenie DevTools")
        return dane

    def _czytaj(self, n: int) -> bytes:
        dane = b""
        while len(dane) < n:
            dane += self._porcja(n - len(dane))
        return dane

    def _wiadomosc(self) -> dict:
        czesci = b""
        while True:
            opcode, ostatnia, dane = odczytaj_ramke(self._czytaj)
            if opcode == 0x8:
                raise ConnectionError("Chrome zamknął kartę")
            if opcode == 0x9:  # ping
                self.gniazdo.sendall(bytes([0x8A, 0x80]) + os.urandom(4))
                continue
            czesci += dane
            if ostatnia:
                return json.loads(czesci)

    def cmd(self, metoda: str, **parametry) -> dict:
        self.numer += 1
        self.gniazdo.sendall(ramka(json.dumps({"id": self.numer, "method": metoda, "params": parametry}).encode()))
        while True:
            m = self._wiadomosc()
            if m.get("id") == self.numer:
                if "error" in m:
                    raise RuntimeError(f"{metoda}: {m['error']}")
                return m.get("result", {})

    def zamknij(self) -> None:
        try:
            self.gniazdo.close()
        except OSError:
            pass


class Strona:
    """Karta Chrome o zadanym rozmiarze okna: wykonywanie JavaScriptu, prawdziwy klik myszą, zrzut."""

    def __init__(self, polaczenie: Polaczenie, szer: int, wys: int):
        self.p, self.szer, self.wys = polaczenie, szer, wys
        self.p.cmd("Emulation.setDeviceMetricsOverride", width=szer, height=wys, deviceScaleFactor=1, mobile=szer < 500)

    def otworz(self, url: str, czekaj: float = 1.5, limit: float = 40.0) -> None:
        """Otwiera stronę i czeka, aż skończy się wczytywać (readyState complete, do `limit` s), potem jeszcze `czekaj` s na skrypty strony."""
        self.p.cmd("Page.navigate", url=url)
        koniec = time.time() + limit
        time.sleep(0.5)
        while time.time() < koniec and self.ev("document.readyState") != "complete":
            time.sleep(0.3)
        time.sleep(czekaj)

    def ev(self, wyrazenie: str):
        """Wartość wyrażenia JavaScript (JSON); None przy błędzie wyrażenia."""
        wynik = self.p.cmd("Runtime.evaluate", expression=wyrazenie, returnByValue=True)
        return None if "exceptionDetails" in wynik else wynik.get("result", {}).get("value")

    def klik(self, x: float, y: float) -> None:
        for typ in ("mouseMoved", "mousePressed", "mouseReleased"):
            self.p.cmd("Input.dispatchMouseEvent", type=typ, x=x, y=y, button="left", clickCount=1)

    def zrzut(self, sciezka: Path) -> str:
        sciezka.parent.mkdir(parents=True, exist_ok=True)
        sciezka.write_bytes(base64.b64decode(self.p.cmd("Page.captureScreenshot", format="png")["data"]))
        return str(sciezka)


def zatrzymaj(proces: subprocess.Popen) -> None:
    """Zatrzymuje Chrome po PID (terminate, po 5 s kill), nigdy po nazwie procesu."""
    proces.terminate()
    try:
        proces.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proces.kill()
        proces.wait()


def _port(profil: str, proces: subprocess.Popen) -> int:
    plik = Path(profil) / "DevToolsActivePort"
    koniec = time.time() + LIMIT_STARTU
    while time.time() < koniec:
        if proces.poll() is not None:
            raise RuntimeError(f"Chrome zakończył się przed startem DevTools (kod {proces.returncode})")
        if plik.is_file() and plik.read_text().strip():
            return int(plik.read_text().split()[0])
        time.sleep(0.1)
    raise RuntimeError("Chrome nie podał portu DevTools w limicie czasu")


@contextmanager
def przegladarka(szer: int, wys: int):
    """Chrome bez okna na wolnym porcie (port 0) pod blokadą kursu; daje `Strona`, a na końcu zatrzymuje proces po PID i kasuje profil."""
    with open(BLOKADA, "a") as blokada:
        fcntl.flock(blokada, fcntl.LOCK_EX)
        profil = tempfile.mkdtemp(prefix="mysz-profil-")
        proces = subprocess.Popen(
            [CHROME, "--headless=new", *flagi_chrome(), "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=0", f"--window-size={szer},{wys}", f"--user-data-dir={profil}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        polaczenie = None
        try:
            port = _port(profil, proces)
            karty = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
            adres = next(k["webSocketDebuggerUrl"] for k in karty if k["type"] == "page")
            polaczenie = Polaczenie(port, "/" + adres.split("/", 3)[3])
            yield Strona(polaczenie, szer, wys)
        finally:
            if polaczenie:
                polaczenie.zamknij()
            zatrzymaj(proces)
            shutil.rmtree(profil, ignore_errors=True)
