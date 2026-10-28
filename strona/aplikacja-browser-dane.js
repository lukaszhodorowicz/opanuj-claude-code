/* Symulator aplikacji Claude, panel Browser z pustą kartą „New tab” i menu „…” (zrzut Łukasza 27.10.2026, zrzut_2026-10-27_15-28-39.png; część „Menu panelu Browser, edytor prezentacji i Transcript view” w dane/FORMAT-SCENARIUSZA.md): napisy, ikony i HTML panelu oraz menu. Gra kroków `klik` z celami `przegladarka` i `przegladarka-menu`: strona/aplikacja-browser.js. */

/* Napisy panelu i menu; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */
PK.NAPISY_BROWSERA = {
  karta: "New tab",
  adres: "Type a URL",
  tytul: "Browse with Claude",
  opis: "Type a URL or ask Claude to open a site. Claude can read, click, and type.",
  podglad: "Preview your app instead?",
  wykryj: "Detect dev server",
  safari: "Open in Safari",
  kopiuj: "Copy URL",
  zrzut: "Save screenshot",
  html: "Open HTML file…",
  viewport: "Viewport",
  responsive: "Responsive",
  linki: "Open links in built-in browser",
  pliki: "Auto-open files Claude writes",
  weryfikuj: "Auto-verify changes",
  strony: "Manage allowed sites…",
  cookies: "Cookies",
  import: "Import cookies…",
  zachowaj: "Keep cookies",
  wspolne: "Shared",
  wyczysc: "Clear browsing data",
};
/* Polskie opisy tylko dla czytnika ekranu (aria-label): nie są napisami interfejsu. */
PK.OPISY_BROWSERA = { panel: "Panel Browser z pustą kartą", menu: "Menu panelu Browser (trzy kropki)" };

PK.IKONY_BROWSERA = (() => {
  const s = (d, w = 1.7) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    plus: s('<path d="M12 5v14M5 12h14"/>'),
    uklad: s('<rect x="4" y="4.5" width="16" height="15" rx="3"/><path d="M4 10.5h16"/>'),
    kropki: s('<circle cx="5.5" cy="12" r=".6"/><circle cx="12" cy="12" r=".6"/><circle cx="18.5" cy="12" r=".6"/>', 2.6),
    rozwin: s('<path d="M14 4h6v6M20 4l-6.5 6.5M10 20H4v-6M4 20l6.5-6.5"/>'),
    zamknij: s('<path d="M6 6l12 12M18 6 6 18"/>'),
    wstecz: s('<path d="M19 12H5M11 6l-6 6 6 6"/>'),
    dalej: s('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    odswiez: s('<path d="M19 12a7 7 0 1 1-2.2-5.1M19 4.5v4.6h-4.6"/>'),
    kursor: s('<path d="M6.5 4.5 18 10.5l-5 1.6L11 18z"/>', 1.5),
  };
})();

/* Menu „…” (zrzut 15-28-39), trzynaście wierszy w czterech grupach: Open in Safari, Copy URL, Save screenshot (szare przy pustej karcie), Open HTML file…; Viewport z wartością Responsive (szare); Open links in built-in browser (bez ptaszka), Auto-open files Claude writes (z ptaszkiem), Auto-verify changes, Manage allowed sites…; nagłówek Cookies (szary), Import cookies…, Keep cookies z wartością Shared i strzałką podmenu, Clear browsing data (czerwone). Wszystkie pozycje są bez skutku. */
PK.menuBrowsera = () => {
  const N = PK.NAPISY_BROWSERA;
  const poz = PK.pozycjaMenuB;
  const wiersze = [
    poz(N.safari, { szara: true }),
    poz(N.kopiuj, { szara: true }),
    poz(N.zrzut, { szara: true }),
    poz(N.html),
    PK.liniaMenuB,
    poz(N.viewport, { szara: true, wartosc: N.responsive }),
    PK.liniaMenuB,
    poz(N.linki),
    poz(N.pliki, { prawa: PK.ptaszekMenuB() }),
    poz(N.weryfikuj),
    poz(N.strony),
    PK.liniaMenuB,
    poz(N.cookies, { naglowek: true }),
    poz(N.import),
    poz(N.zachowaj, { wartosc: N.wspolne, prawa: PK.strzalkaMenuB() }),
    poz(N.wyczysc, { czerwona: true }),
  ];
  return `<ul class="apl-mb apl-pbr-lista" role="menu">${wiersze.join("")}</ul>`;
};

/* Panel Browser z pustą kartą: pasek kart (karta „New tab”, +; po prawej układ, „…”, rozwiń, zamknij), pasek adresu (wstecz, dalej, odśwież, pole „Type a URL”, kursor) i środek pustej karty. Ikony i pole adresu są bez skutku; „…” jest przyciskiem aktywnym tylko wtedy, gdy krok na niego czeka. */
PK.panelBrowsera = () => {
  const { esc } = PK;
  const N = PK.NAPISY_BROWSERA;
  const I = PK.IKONY_BROWSERA;
  const ik = (nazwa) => `<span class="apl-pbr-ik">${I[nazwa]}</span>`;
  return (
    `<section class="apl-pbr" aria-label="${esc(PK.OPISY_BROWSERA.panel)}">` +
    `<header class="apl-pbr-glowa"><span class="apl-pbr-karta">${esc(N.karta)}</span>${ik("plus")}` +
    `<span class="apl-pbr-prawa">${ik("uklad")}<button type="button" class="apl-pbr-ik apl-pbr-menu" aria-haspopup="menu" aria-expanded="false" aria-disabled="true" aria-label="${esc(PK.OPISY_BROWSERA.menu)}">${I.kropki}</button>${ik("rozwin")}${ik("zamknij")}</span></header>` +
    `<div class="apl-pbr-adres">${ik("wstecz")}${ik("dalej")}${ik("odswiez")}<span class="apl-pbr-pole">${esc(N.adres)}</span>${ik("kursor")}</div>` +
    `<div class="apl-pbr-pusto"><b>${esc(N.tytul)}</b><p>${esc(N.opis)}</p><p class="apl-pbr-podglad">${esc(N.podglad)} <span>${esc(N.wykryj)}</span></p></div>` +
    "</section>"
  );
};
