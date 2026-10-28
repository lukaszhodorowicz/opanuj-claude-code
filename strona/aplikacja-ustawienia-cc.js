/* Symulator aplikacji Claude, okno Settings na stronie „Claude Code” z częścią „Remote Control” i przełącznikiem „Connect new sessions to Remote Control”: napisy ze zrzutów Łukasza z 27.10.2026 (zrzut_2026-10-27_04-44-01.png, zrzut_2026-10-27_04-07-11.png w materialy/zrzuty-lukasza/ w pamięci projektu), krok `klik` z celem `ustawienia-claude-code` (wejście: konto na dole paska bocznego, umowa symulatora) i stan przełącznika z pola `aplikacja.rc_nowe_sesje`. Obudowa okna: strona/aplikacja-ustawienia.js (PK.powlokaKatalogu). To samo wejście (konto na dole paska bocznego) otwiera też stronę Connectors, zakładka Yours, krokiem `klik` z celem `ustawienia-connectors` (strona/aplikacja-ustawienia-konektory.js). Napisy zapisane jak JSON: tests/test_napisy_telefonu.py czyta je stąd i sprawdza w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */

PK.KOMENDA_USTAWIEN_CC = "/config"; /* polecenie wpisane w polu wiadomości, które otwiera Settings > Claude Code (fakt aplikacja-config-otwiera-settings-claude-code) */

PK.USTAWIENIA_CC = {
  "wyglad": "Appearance",
  "widok": {"nazwa": "Default transcript view", "opis": "The view sessions open in. Picking a view from a session’s Transcript view menu changes only that session.", "pozycje": ["Normal", "Thinking", "Verbose"]},
  "zdalne": "Remote Control",
  "przelaczniki": [
    {"nazwa": "Connect new sessions to Remote Control", "opis": "Sessions you start on this computer connect to Remote Control automatically, so you can continue them from other devices."},
    {"nazwa": "Let your phone and claude.ai start sessions here", "opis": "While Claude is open, sessions you start from your phone or claude.ai run on this computer. They can read and edit files and run commands in the folders below, following your approval settings. This computer’s name and each folder’s name, path, Git branch, and repository URL are sent to Anthropic so your devices can list them."},
    {"nazwa": "Keep this computer awake for Remote Control", "opis": "Keeps this computer from going to sleep on its own. If it does go to sleep, it isn’t reachable until it wakes up."}
  ]
};

/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_USTAWIEN_CC = {
  okno: "Ustawienia programu: wygląd rozmów i zdalne sterowanie (w ćwiczeniu bez skutku, tylko przewijanie)",
  zamknij: "Zamknij okno (w ćwiczeniu bez skutku)",
  konto: "Konto: otwórz ustawienia",
  przelacznik: "Przełącznik (w ćwiczeniu bez skutku)",
};

/* Treść strony: sekcja Appearance z wyborem widoku rozmowy (Normal wybrane), sekcja Remote Control z trzema przełącznikami (pierwszy ze stanu `wlaczony`, pozostałe włączone jak na zrzucie) i szare paski w miejscu dalszych ustawień (reszta strony to ustawienia innych funkcji, których symulator nie rysuje). Wszystko poza przewijaniem jest bez skutku. */
PK.trescUstawienCC = (wlaczony) => {
  const { esc } = PK;
  const U = PK.USTAWIENIA_CC;
  const przelacznik = (wl) => `<span class="apl-ucc-przel${wl ? " apl-ucc-wl" : ""}" role="switch" aria-checked="${wl}" aria-disabled="true" aria-label="${esc(PK.OPISY_USTAWIEN_CC.przelacznik)}"><i></i></span>`;
  const wiersz = (nazwa, opis, prawo, klasa = "") =>
    `<div class="apl-ucc-wiersz${klasa}"><div class="apl-ucc-opis"><b>${esc(nazwa)}</b><span>${esc(opis)}</span></div>${prawo}</div>`;
  const widok = `<span class="apl-ucc-wybor" role="radiogroup" aria-label="${esc(U.widok.nazwa)}">${U.widok.pozycje.map((p, i) => `<span class="apl-ucc-poz${i === 0 ? " wybrana" : ""}" role="radio" aria-checked="${i === 0}">${esc(p)}</span>`).join("")}</span>`;
  const szare = [58, 72, 64].map((d) => `<div class="apl-ucc-wiersz apl-ucc-szary"><div class="apl-ucc-opis"><span class="apl-szkic" style="width:${d}%"></span><span class="apl-szkic" style="width:${d + 24 > 96 ? 96 : d + 24}%"></span></div><span class="apl-szkic apl-ucc-szary-prawo"></span></div>`).join("");
  return (
    `<h4 class="apl-ucc-h">${esc(U.wyglad)}</h4>${wiersz(U.widok.nazwa, U.widok.opis, widok, " apl-ucc-wiersz-wybor")}` +
    `<h4 class="apl-ucc-h">${esc(U.zdalne)}</h4>${U.przelaczniki.map((p, i) => wiersz(p.nazwa, p.opis, przelacznik(i === 0 ? wlaczony : true))).join("")}` +
    `<h4 class="apl-ucc-h apl-ucc-h-szary"><span class="apl-szkic" style="width:90px"></span></h4>${szare}`
  );
};

/* Okno Settings w ćwiczeniu z drogami, które mają krok `klik` z celem `ustawienia-claude-code` (strona Claude Code) albo `ustawienia-connectors` (strona Connectors, zakładka Yours, strona/aplikacja-ustawienia-konektory.js); null, gdy żadna droga go nie ma (reszta ćwiczeń zostaje bez zmian). Okno powstaje tylko dla celu użytego w drogach; lewa kolumna zależy od `aplikacja.konto_ustawien` (strona/aplikacja-ustawienia-konta.js). Wejściem jest konto na dole paska bocznego (kółko, nazwa, strzałka): żaden zrzut nie pokazuje drogi do Settings, więc to umowa symulatora; na wąskim ekranie wiersz konta, schowany razem z paskiem, wraca (klasa apl-ma-ustawienia okna). Zwraca {dotyczy, klik, otworz, reset}. */
PK.ustawieniaCCAplikacji = function (cw, sek, okno) {
  const O = PK.OPISY_USTAWIEN_CC;
  const wlaczony = (cw.aplikacja || {}).rc_nowe_sesje !== false; /* domyślnie jak na zrzucie: włączony */
  /* strona okna dla każdego celu kliku w konto */
  const STRONY = {
    "ustawienia-claude-code": { strona: "Claude Code", opis: O.okno, tresc: () => PK.trescUstawienCC(wlaczony), klasa: "apl-ustaw-cc" },
    "ustawienia-connectors": { strona: "Connectors", zakladka: 0, opis: PK.OPISY_USTAWIEN_KONEKTOROW.okno, tresc: () => PK.trescKonektorowTwoich(), klasa: "apl-ustaw-konektory" },
  };
  const dotyczy = (k) => k.typ === "klik" && Object.keys(STRONY).includes(k.cel);
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const uzyteKlikiem = Object.keys(STRONY).filter((cel) => kroki.some((k) => k.typ === "klik" && k.cel === cel));
  const zKomenda = kroki.some((k) => k.typ === "komenda" && k.tekst === PK.KOMENDA_USTAWIEN_CC); /* komenda /config otwiera tę samą stronę Claude Code bez kliku w konto */
  const uzyte = zKomenda && !uzyteKlikiem.includes("ustawienia-claude-code") ? [...uzyteKlikiem, "ustawienia-claude-code"] : uzyteKlikiem;
  if (!uzyte.length) return null;
  const { czekaj } = PK;
  const konto = sek.querySelector(".apl-bok-konto");
  if (uzyteKlikiem.length) {
    /* wiersz konta jest przyciskiem tylko wtedy, gdy któryś krok w niego klika; sama komenda /config nie zmienia paska bocznego */
    okno.classList.add("apl-ma-ustawienia");
    konto.removeAttribute("aria-hidden");
    konto.setAttribute("role", "button");
    konto.setAttribute("tabindex", "0");
    konto.setAttribute("aria-label", O.konto);
  }
  const okna = Object.fromEntries(uzyte.map((cel) => {
    const S = STRONY[cel];
    return [cel, PK.powlokaKatalogu(okno, { opis: S.opis, zamknij: O.zamknij, strona: S.strona, zakladka: S.zakladka, tresc: S.tresc(), klasa: S.klasa })];
  }));
  let czeka = null; /* {pusc}: krok klik czeka na klik w konto */

  /* Kursant klika tylko to, na co czeka krok; Enter i spacja na koncie działają jak klik. */
  konto.addEventListener("click", () => czeka && czeka.pusc(true));
  konto.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      konto.click();
    }
  });

  return {
    dotyczy,
    /* Znacznik „kliknij tutaj” nad kontem, czekanie na klik, potem okno Settings na stronie z celu kroku (przewijana zawartość, reszta bez skutku). `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane. */
    async klik(k, zyje) {
      PK.celAplikacji(sek, konto);
      const ok = await new Promise((pusc) => (czeka = { pusc }));
      czeka = null;
      if (!ok || !zyje()) return;
      PK.celAplikacji(sek, null);
      konto.classList.add("wcisniety");
      await czekaj(200);
      konto.classList.remove("wcisniety");
      if (zyje()) okna[k.cel].pokaz(true);
    },
    /* Komenda /config (krok `komenda`, strona/aplikacja.js) po wpisaniu i wysłaniu otwiera okno Settings na stronie Claude Code. */
    otworz() {
      okna["ustawienia-claude-code"].pokaz(true);
    },
    /* „Od nowa” i nowe polecenie: okno zamknięte, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      Object.values(okna).forEach((o) => {
        o.pokaz(false);
        o.zawartosc.scrollTop = 0;
      });
    },
  };
};
