/* Symulator aplikacji Claude, dane menu + i listy „/”: napisy ze zrzutów Łukasza z 27.10.2026 (materialy/zrzuty-lukasza/ w pamięci projektu: menu 03-58-01, podmenu Plugins 03-58-57, podmenu Connectors i sesja w chmurze 04-22-37, lista 03-58-20) i ikony pozycji menu. Kod menu, podmenu i listy jest w strona/aplikacja-plus.js. Stałe z napisami są zapisane jak JSON (cudzysłowy przy kluczach): tests/test_napisy_menu_plus.py czyta je stąd i sprawdza w dane/napisy-interfejsu.yaml (gdzie: aplikacja) oraz w narzedzia/scenariusz_plus.py. */

/* Pozycje menu od góry. W sesji w chmurze „Import GitHub issue” znika, a „Add folder” i „Plugins” są wyszarzone (PK.POZYCJE_LOKALNE). */
PK.MENU_PLUS = ["Add files or photos", "Add folder", "Import GitHub issue", "Slash commands", "Connectors", "Plugins"];
/* Pozycje podmenu w kolejności ze zrzutów; podmenu otwiera klik w pozycję menu o tej nazwie. Wiersze zainstalowanych wtyczek i konektorów (u każdego inne) są szarymi paskami: nad kreską w Plugins, pod kreską w Connectors. */
PK.PODMENU_PLUS = {"Plugins": ["Manage plugins", "Browse plugins"], "Connectors": ["Browse connectors", "Manage connectors"]};
PK.SKROT_PLUS = {"Add files or photos": "⌘ U"};
PK.PODPIS_GITHUB = "This folder doesn’t have a GitHub remote";
PK.PODPIS_LOKALNE = "Only available in local sessions";
PK.POZYCJE_LOKALNE = ["Add folder", "Plugins"];

/* Wiersze listy „/” od góry (zrzut 03-58-20); czternasty wiersz zrzutu jest ucięty krawędzią listy, więc symulator rysuje go jako szary pasek bez nazwy (cel starych kroków `wiersz` z `bez_napisu: true`). Pierwszy wiersz jest podświetlony, a obok stoi dymek z jego opisem; opisów pozostałych wierszy zrzut nie pokazuje. */
PK.WIERSZE_LISTY = ["plugin", "model", "effort", "fast", "plan", "permissions", "skills", "workflows", "usage", "usage-credits", "config", "storage", "sandbox"];
PK.OPISY_WIERSZY = {"plugin": "Manage Claude Code plugins"};
PK.PODPOWIEDZ_POLA = "Type to filter";

/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_PLUSA = {
  wiersz: "Wiersz listy bez nazwy",
  skill: "Wybrany skill (w ćwiczeniu bez nazwy)",
};

/* Ikony pozycji menu rysowane kreską; żadna nie niesie napisu ani logo (ikona „Import GitHub issue” to neutralna gałąź w kółku, nie znak marki). */
PK.IKONY_PLUS = (() => {
  const s = (d) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const I = PK.IKONY_APLIKACJI;
  return {
    "Add files or photos": s('<path d="M20.4 11.1l-8.6 8.6a5 5 0 0 1-7.1-7.1l8.6-8.6a3.3 3.3 0 0 1 4.7 4.7l-8.6 8.6a1.7 1.7 0 0 1-2.3-2.3l7.9-7.9"/>'),
    "Add folder": I.folder,
    "Import GitHub issue": s('<circle cx="12" cy="12" r="8.5"/><circle cx="10" cy="9.3" r="1.3"/><circle cx="10" cy="14.7" r="1.3"/><circle cx="14.3" cy="11.2" r="1.3"/><path d="M10 10.6v2.8M13.3 11.9c-1.8.2-3.3.8-3.3 1.8"/>'),
    "Slash commands": s('<rect x="4.5" y="4.5" width="15" height="15" rx="3"/><path d="m14 8.3-4 7.4"/>'),
    Connectors: s('<rect x="4" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="12" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="4" y="4.5" width="6.5" height="6.5" rx="1.2"/><path d="m15.5 4.5 3.5 3.5-3.5 3.5L12 8z"/>'),
    Plugins: s('<path d="M9 4v4M15 4v4M7 8h10v3.5a5 5 0 0 1-10 0z"/><path d="M12 16.5V20"/>'),
    "Browse connectors": s('<rect x="4" y="5" width="4" height="14" rx="1"/><rect x="9.5" y="5" width="4" height="14" rx="1"/><path d="m15.6 6.4 3.3 12.4"/>'),
    "Manage connectors": I.teczka,
    "Manage plugins": I.teczka,
    "Browse plugins": I.plus,
  };
})();
