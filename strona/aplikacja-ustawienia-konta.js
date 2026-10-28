/* Symulator aplikacji Claude, lewa kolumna okna Settings w dwóch wariantach kont ze zrzutów Łukasza z 27.10.2026 (wybór polem `aplikacja.konto_ustawien`: "A" albo "B", dane/FORMAT-SCENARIUSZA.md, część „Okno Settings: wariant lewej kolumny”): konto A (paczka 1, zrzut 03-59-16) ma w grupie Preferences pozycję Cowork, konto B (paczki 2 i 3, zrzuty 04-26-45, 04-22-53 i 04-45-04) ma Billing, Reflect, Time and focus i Claude in Chrome zamiast Cowork oraz na końcu grupę Platform z linkiem API keys. Zrzut konta A kończy się na nagłówku „Customize” (kolumna ucięta krawędzią okna), więc jego pozycje Skills, Connectors i Plugins są przepisane z konta B, a grupy Platform dla konta A zrzut nie pokazuje (symulator jej nie rysuje). Kod okna: strona/aplikacja-ustawienia.js (PK.kolumnaUstawien, PK.powlokaKatalogu). Stałe są zapisane jak JSON (cudzysłowy przy kluczach): testy czytają je stąd i sprawdzają w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */

PK.USTAWIENIA_KONTA = {
  "A": [
    {"grupa": "Preferences", "pozycje": ["General", "Account", "Privacy", "Usage", "Capabilities", "Memory", "Design systems", "Claude Code", "Cowork"]},
    {"grupa": "This computer", "pozycje": ["System", "Extensions", "Developer"]},
    {"grupa": "Customize", "pozycje": ["Skills", "Connectors", "Plugins"]}
  ],
  "B": [
    {"grupa": "Preferences", "pozycje": ["General", "Account", "Privacy", "Billing", "Usage", "Capabilities", "Memory", "Design systems", "Reflect", "Time and focus", "Claude Code", "Claude in Chrome"]},
    {"grupa": "This computer", "pozycje": ["System", "Extensions", "Developer"]},
    {"grupa": "Customize", "pozycje": ["Skills", "Connectors", "Plugins"]},
    {"grupa": "Platform", "pozycje": ["API keys"]}
  ]
};

/* Pozycje z ukośną strzałką po prawej (link poza aplikację, zrzut 04-45-04). */
PK.USTAWIENIA_ZEWNETRZNE = ["API keys"];

/* Ikona każdej pozycji kolumny (klucze PK.IKONY_KATALOGU); ikony są kreskowe, bez marek. */
PK.IKONY_POZYCJI_USTAWIEN = {
  "General": "ogolne", "Account": "konto", "Privacy": "prywatnosc", "Billing": "karta", "Usage": "uzycie", "Capabilities": "mozliwosci", "Memory": "pamiec",
  "Design systems": "paleta", "Reflect": "refleksja", "Time and focus": "ksiezyc", "Claude Code": "kod", "Claude in Chrome": "kursor", "Cowork": "lista",
  "System": "system", "Extensions": "wtyczka", "Developer": "narzedzie", "Skills": "zwoj", "Connectors": "klocki", "Plugins": "wtyczka", "API keys": "klucz"
};

/* Ikony, których nie ma w strona/aplikacja-ustawienia.js: Billing, Reflect, Time and focus, API keys, ukośna strzałka linku, kursor (Claude in Chrome) i ptaszek stanu. */
(() => {
  const s = (d) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  Object.assign(PK.IKONY_KATALOGU, {
    karta: s('<rect x="4" y="6" width="16" height="12" rx="2.5"/><path d="M4 10.5h16M7.5 14.5h3"/>'),
    refleksja: s('<path d="M6.5 14.5a5.5 5.5 0 0 1 11 0M4 14.5h16M7 18.5h10"/>'),
    ksiezyc: s('<path d="M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z"/><path d="M17 4v3M15.5 5.5h3"/>'),
    kursor: s('<path d="M7 4.5v13l3.2-3.1 2.6 5.1 2.2-1.1-2.6-5 4.4-.3z"/>'),
    klucz: s('<circle cx="8.5" cy="15.5" r="3.5"/><path d="m11 13 7-7M15.5 8.5l2 2"/>'),
    zewnetrzny: s('<path d="M7 17 17 7M9 7h8v8"/>'),
    ptaszek: s('<path d="m5.5 12.5 4 4 9-9.5"/>'),
  });
})();
