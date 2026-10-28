"""Przebieg sprawdzianu myszą na jednej stronie lekcji: ćwiczenia z poleceniami (polecenia, znaczniki „kliknij tutaj”, dymek i okno), odwracane karty i poziome przewijanie; każde sprawdzenie daje `Wynik`."""

import time
from pathlib import Path

from narzedzia.mysz_cdp import Strona
from narzedzia.mysz_raport import Wynik

CWICZENIA = '[...document.querySelectorAll(".cwiczenie")].filter(s=>s.querySelector(".polecenie"))'
CEL = '[...{S}.querySelectorAll(".apl-cel")].find(e=>e.getBoundingClientRect().width>0)'
# co leży pod punktem kliknięcia: dymek nauczyciela, nagłówek ćwiczenia, nagłówek strony albo logo to usterka (kursant kliknąłby w nie)
POD = '(x,y)=>{const e=document.elementFromPoint(x,y);if(!e)return "nic";const z=e.closest(".nauczyciel,.dymek,.cwiczenie > .naglowek,body > header,body > nav,.logo");return z?"ZLE:"+e.tagName+" w "+z.tagName+"."+String(z.className).slice(0,40):"ok"}'
PROSTOKAT = '(()=>{{const r={E}.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.top>=0&&r.bottom<=innerHeight]}})()'
WIDOK = (
    '(()=>{{const s={S};const d=s.querySelector(".nauczyciel").getBoundingClientRect(),o=s.querySelector(".apl-okno,.okna").getBoundingClientRect();'
    "const miesci=o.bottom-d.top<=innerHeight,wyzsze=o.height>innerHeight,ma_cel=!!{CEL};"
    "return [ma_cel?true:miesci?(d.top>=-16&&d.bottom<=innerHeight+1):(wyzsze?(o.top>=-1&&o.top<=30):(o.bottom<=innerHeight+13)),"
    "o.top<innerHeight&&o.bottom>0,Math.round(d.top),Math.round(o.top),Math.round(o.bottom)]}})()"
)
LIMIT_KROKOW = 200
CISZA_MAX = 40  # sekundy bez znacznika celu i bez wolnego polecenia, zanim uznamy, że ćwiczenie utknęło
UKLAD_STABILNY = 5  # kolejnych odczytów (po 0,4 s) bez zmiany położenia, zanim zmierzymy dymek i okno; okno rośnie z opóźnieniem ok. 1 s


def _stabilny_ekran(strona: Strona, s: str) -> None:
    ostatni, stabilnie = None, 0
    for _ in range(22):
        time.sleep(0.4)
        teraz = strona.ev(f'scrollY+"/"+Math.round({s}.querySelector(".nauczyciel").getBoundingClientRect().top)')
        stabilnie = stabilnie + 1 if teraz == ostatni else 0
        ostatni = teraz
        if stabilnie >= UKLAD_STABILNY:
            return


def _jedno_cwiczenie(strona: Strona, indeks: int, lekcja: str, katalog: Path) -> Wynik:
    s = f"({CWICZENIA})[{indeks}]"
    strona.ev(f'(()=>{{const e={s};scrollTo({{top:e.getBoundingClientRect().top+scrollY-20,behavior:"instant"}})}})()')
    time.sleep(0.6)
    id_cw = strona.ev(f"{s}.id") or f"cw{indeks + 1}"
    apl = bool(strona.ev(f'{s}.classList.contains("cwiczenie-apl")'))
    wynik = Wynik(lekcja, "ćwiczenie", id_cw, strona.szer, strona.wys)
    klikniete, cisza = set(), 0
    cel = CEL.format(S=s)

    def zrzut(opis: str) -> None:
        wynik.zrzuty.append(strona.zrzut(katalog / f"{lekcja}-{id_cw}-{strona.szer}-{opis}.png"))

    for _ in range(LIMIT_KROKOW):
        c = strona.ev(PROSTOKAT.format(E=cel)) if strona.ev(f"!!{cel}") else None
        if c:  # najpierw znacznik „kliknij tutaj”, jak robi kursant
            cisza = 0
            if not c[2] and klikniete:
                wynik.usterki.append(f"cel „kliknij tutaj” poza ekranem po {len(klikniete)} poleceniach")
            if not c[2]:
                strona.ev(f'{cel}.scrollIntoView({{block:"center",behavior:"instant"}})')
                time.sleep(0.4)
                c = strona.ev(PROSTOKAT.format(E=cel))
            pod = strona.ev(f"({POD})({c[0]},{c[1]})")
            if pod != "ok":
                wynik.usterki.append(f"pod kursorem na celu: {pod}")
            strona.klik(c[0], c[1])
            time.sleep(1.5)
            continue
        wolne = strona.ev(f'[...{s}.querySelectorAll(".polecenie")].map((b,i)=>(!b.disabled&&!b.classList.contains("wyslane"))?i:-1).filter(i=>i>=0)') or []
        wolne = [i for i in wolne if i not in klikniete]
        if not wolne:
            czeka = apl and strona.ev(f'[...{s}.querySelectorAll(".polecenie")].some(b=>b.disabled&&!b.classList.contains("wyslane"))')
            if not czeka:
                break
            cisza += 1
            if cisza > CISZA_MAX:
                wynik.usterki.append(f"utknęło: polecenia nieaktywne bez znacznika celu przez {CISZA_MAX} s")
                zrzut("zablokowane")
                break
            time.sleep(1)
            continue
        cisza = 0
        d = wolne[0]
        klikniete.add(d)
        b = f'{s}.querySelectorAll(".polecenie")[{d}]'
        r = strona.ev(PROSTOKAT.format(E=b))
        if not r[2]:
            strona.ev(f'{b}.scrollIntoView({{block:"center",behavior:"instant"}})')
            time.sleep(0.4)
            r = strona.ev(PROSTOKAT.format(E=b))
        pod = strona.ev(f"({POD})({r[0]},{r[1]})")
        if pod != "ok":
            wynik.usterki.append(f"pod kursorem na poleceniu {d}: {pod}")
        strona.klik(r[0], r[1])
        _stabilny_ekran(strona, s)
        v = strona.ev(WIDOK.format(S=s, CEL=cel))
        if v and not (v[0] and v[1]):
            wynik.usterki.append(f"po kliknięciu polecenia {d} dymek albo okno poza ekranem (dymek {v[2]}, okno {v[3]}..{v[4]}, ekran {strona.wys})")
        if len(klikniete) == 1:
            zrzut("po-kliknieciu")
        if not apl:
            time.sleep(6)  # gra terminala trwa kilka sekund i nie ma znaczników
    else:
        wynik.usterki.append(f"za dużo kroków ({LIMIT_KROKOW})")
    zrzut("koniec")
    return wynik


def sprawdz_cwiczenia(strona: Strona, url: str, lekcja: str, katalog: Path) -> list[Wynik]:
    """Przeklikuje prawdziwą myszą każde ćwiczenie z poleceniami na stronie; wynik na każde ćwiczenie."""
    strona.otworz(url)
    for _ in range(5):  # strona z ćwiczeniami może jeszcze budować okna po wczytaniu
        sekcje = strona.ev('document.querySelectorAll(".cwiczenie").length') or 0
        if sekcje:
            break
        time.sleep(1)
    if not sekcje:
        wynik = Wynik(lekcja, "ćwiczenie", "brak", strona.szer, strona.wys, ["na stronie nie ma żadnego ćwiczenia (strona się nie wczytała albo lekcja nie ma ćwiczeń)"])
        wynik.zrzuty.append(strona.zrzut(katalog / f"{lekcja}-brak-cwiczen-{strona.szer}.png"))
        return [wynik]
    ile = strona.ev(f"{CWICZENIA}.length") or 0
    return [_jedno_cwiczenie(strona, i, lekcja, katalog) for i in range(ile)]


POMIAR_KARTY = (
    '(()=>{{const k=document.querySelectorAll(".odwrot")[{I}],w=k.querySelector(".odwrot-w"),o=k.classList.contains("odwrocona");'
    'const f=k.querySelector((o?".odwrot-tyl":".odwrot-przod")+" img").getBoundingClientRect(),q=k.querySelector(".odwrot-przycisk").getBoundingClientRect();'
    'return {{odwrocona:o,etykieta:w.getAttribute("aria-label"),pas:Math.round(w.getBoundingClientRect().height-f.height),x:q.left+q.width/2,y:q.top+q.height/2}}}})()'
)


def sprawdz_karty(strona: Strona, url: str, lekcja: str, katalog: Path) -> list[Wynik]:
    """Każda odwracana karta: klik w przycisk odwraca, drugi klik wraca, etykieta się zmienia, a pod rysunkiem nie ma pustego pasa (przed, po odwróceniu i po powrocie)."""
    strona.otworz(url)
    ile = strona.ev('document.querySelectorAll(".odwrot").length') or 0
    wyniki = []
    for i in range(ile):
        wynik = Wynik(lekcja, "karta", f"karta{i + 1}", strona.szer, strona.wys)
        strona.ev(f'(()=>{{scrollTo({{top:document.querySelectorAll(".odwrot")[{i}].getBoundingClientRect().top+scrollY-120,behavior:"instant"}})}})()')
        time.sleep(0.8)
        stany = []
        for krok in ("start", "odwrocona", "wrot"):
            p = strona.ev(POMIAR_KARTY.format(I=i))
            stany.append(p)
            wynik.zrzuty.append(strona.zrzut(katalog / f"{lekcja}-karta{i + 1}-{strona.szer}-{krok}.png"))
            if krok != "wrot":
                strona.klik(p["x"], p["y"])
                time.sleep(1)
        start, odw, wrot = stany
        if start["odwrocona"] or not odw["odwrocona"] or wrot["odwrocona"]:
            wynik.usterki.append("klik w przycisk nie odwraca karty albo drugi klik nie wraca")
        if start["etykieta"] == odw["etykieta"]:
            wynik.usterki.append("etykieta karty nie zmienia się po odwróceniu")
        for nazwa, p in (("na starcie", start), ("po odwróceniu", odw), ("po powrocie", wrot)):
            if abs(p["pas"]) > 1:
                wynik.usterki.append(f"pusty pas {p['pas']} px pod rysunkiem {nazwa}")
        wyniki.append(wynik)
    return wyniki


def sprawdz_przewijanie(strona: Strona, url: str, lekcja: str, katalog: Path) -> Wynik:
    """Strona nie przewija się w poziomie: scrollWidth nie większy niż szerokość okna."""
    strona.otworz(url)
    sw, iw = strona.ev("document.documentElement.scrollWidth"), strona.ev("innerWidth")
    wynik = Wynik(lekcja, "przewijanie", "w poziomie", strona.szer, strona.wys)
    if sw is None or iw is None:
        wynik.usterki.append("nie udało się odczytać szerokości strony")
    elif sw > iw:
        wynik.usterki.append(f"strona przewija się w poziomie: scrollWidth {sw} > {iw}")
        wynik.zrzuty.append(strona.zrzut(katalog / f"{lekcja}-poziome-{strona.szer}.png"))
    return wynik
