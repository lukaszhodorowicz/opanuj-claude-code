/* Symulator aplikacji Claude, napisy i ikony ze zrzutów Łukasza z 27.10.2026 (pasek boczny, panel szczegółów, rząd pod polem, menu ⋮; część B silnika, D-2026-10-27-51): stała `PK.NAPISY_EKRANU` (każdy jej napis ma wpis `gdzie: aplikacja` z zrzutem w dane/napisy-interfejsu.yaml; sprawdza to tests/test_napisy_ekranu_b.py), ikony, których nie ma w aplikacja-ikony.js, pozycje i konto paska bocznego. Dane konta (nazwy rozmów, folderów, konektorów, plan, liczby) to szare paski albo pola scenariusza, nigdy napisy. */

/* Napisy stałe, w grupach według miejsca na ekranie; napisy składane z danymi (np. „9% used”, „Resets …”) powstają w kodzie z fragmentów poniżej i mają w yaml wzór. */
PK.NAPISY_EKRANU = {
  bok: { szukaj: "Search", artefakty: "Artifacts", dyzur: "On-call", dostosuj: "Customize", wiecej: "More" },
  panel: {
    srodowisko: "Environment",
    komputer: "This computer",
    zapisz: "Save",
    zdalne: "Remote Control",
    domyslne: "Default",
    repozytorium: "Add repository…",
    konektory: "Connectors",
    ponownie: "Reconnect",
    uwierzytelnij: "Authenticate",
    wiecej: "Show more",
  },
  kontekst: {
    mcp: "MCP tools",
    narzedzia: "System tools",
    agenci: "Custom agents",
    prompt: "System prompt",
    pamiec: "Memory files",
    skille: "Skills",
    wiadomosci: "Messages",
    bufor: "Compact buffer",
    wolne: "Free space",
  },
  tryby: {
    naglowek: "Permissions · this session",
    Auto: "Claude handles permission decisions",
    Manual: "Always ask before making changes",
    "Accept edits": "Automatically accept all file edits",
    Plan: "Create a plan before making changes",
    "Bypass permissions": "Claude can modify or delete files without asking",
  },
  model: {
    wiecej: "More models",
    szybki: "Fast mode",
    wlacz: "Enable fast mode",
    kredyty: "Requires usage credits",
    kup: "Buy credits",
  },
  wysilek: {
    opis: "Higher effort means more thorough responses, but takes longer and uses your limits faster.",
    low: "Low",
    medium: "Medium",
    polecany: "Recommended",
    high: "High",
    extra: "Extra",
    max: "Max",
    ostrzezenie: "3.5× or more usage",
    ultracode: "Ultracode",
  },
  pierscien: {
    naglowek: "Plan usage limits",
    wszystko: "See all",
    sesja: "Session limit",
    start: "Starts when a message is sent",
    tydzien: "Weekly · all models",
    odnowa: "Resets",
    chmura: "Cloud session credits",
    wygasa: "Expires",
  },
  menu: { rozmowaBoczna: "Side chat", skrot: "⌘ ;" },
};
/* Fragmenty napisów składanych z liczbą konta; całość sprawdza wzór w yaml („9% used”, „90k / 1M”). */
PK.FRAGMENTY_EKRANU = { uzyte: "% used", okno: " / 1M" };

/* Ikony kreskowe i trójkąty ze zrzutów; żadna nie niesie napisu. */
PK.IKONY_EKRANU = (() => {
  const s = (d, w) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 1.7}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const trojkat = (d) => `<svg viewBox="0 0 10 10" fill="currentColor" aria-hidden="true"><path d="${d}"/></svg>`;
  return {
    kursor: s('<path d="M7 4.5v13l3.2-3.1 2.6 5.1 2.2-1.1-2.6-5 4.4-.3z"/>'),
    robak: s('<ellipse cx="12" cy="13.5" rx="4.2" ry="5.3"/><path d="M9.6 8.6a2.4 2.4 0 0 1 4.8 0M12 8.2v10.6M7.8 11.2H4.2M7.9 15.6 5 17.6M16.2 11.2h3.6M16.1 15.6l2.9 2M9.6 5.6 8.2 4M14.4 5.6 15.8 4"/>'),
    zebatka: s('<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.5 1.5M16.5 16.5 18 18M18 6l-1.5 1.5M7.5 16.5 6 18"/>'),
    chmura: s('<path d="M7 18h10a3.5 3.5 0 0 0 .6-6.95A5.5 5.5 0 0 0 7 10.5 3.8 3.8 0 0 0 7 18z"/>'),
    repo: s('<path d="M6 4.5h11a1.5 1.5 0 0 1 1.5 1.5v12H7.5A1.5 1.5 0 0 0 6 19.5z"/><path d="M6 19.5V4.5M9.5 8.5h5"/>'),
    pytajnik: s('<circle cx="12" cy="12" r="8"/><path d="M9.8 9.6a2.3 2.3 0 0 1 4.4.8c0 1.5-2.2 1.8-2.2 3.3M12 16.6v.1"/>'),
    ostrzezenie: s('<path d="M12 4.5 20 18.5H4z"/><path d="M12 10v4M12 16.4v.1"/>', 1.9),
    strzalka: s('<path d="M5 12h14M13.5 6.5 19 12l-5.5 5.5"/>'),
    dol: trojkat("M1.5 3h7L5 7.5z"),
    prawo: trojkat("M3 1.5v7L7.5 5z"),
  };
})();

/* Pozycja paska bocznego z ikoną i stałym napisem (zrzut 03-58-01: ikona, napis, bez skrótu). */
PK.pozycjaBokuZNapisem = (ikona, napis) =>
  `<li><span class="apl-bok-ikona">${ikona}</span><span class="apl-bok-napis">${PK.esc(napis)}</span></li>`;

/* Konto na dole paska bocznego (zrzut 03-58-01): kółko, nazwa konta jako szary pasek (dana konta), strzałka w dół i ikona robaka po prawej; bez skutku, więc poza czytnikiem ekranu. */
PK.kontoBoku = () =>
  `<div class="apl-bok-konto" aria-hidden="true"><span class="apl-konto-awatar"></span><span class="apl-szkic apl-konto-nazwa"></span>` +
  `<span class="apl-konto-strzalka">${PK.IKONY_EKRANU.dol}</span><span class="apl-konto-robak">${PK.IKONY_EKRANU.robak}</span></div>`;

/* Pigułka z napisem (Recommended, Buy credits, 3.5× or more usage); `ikona` rysuje się przed napisem. */
PK.pigulka = (napis, klasa, ikona = "") => `<span class="apl-pigulka ${klasa}">${ikona}<span>${PK.esc(napis)}</span></span>`;
