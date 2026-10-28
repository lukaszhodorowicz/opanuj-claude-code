/* Symulator aplikacji Claude, dane okna Settings (przeglądarka wtyczek i katalog konektorów): napisy ze zrzutów Łukasza z 27.10.2026 (materialy/zrzuty-lukasza/ w pamięci projektu: wtyczki 03-59-16, konektory 04-43-33 i 04-23-08, lewa kolumna 04-45-04). Opisy ucięte krawędzią kafelka kończą się znakiem … tak jak na zrzucie; opis, którego zrzut nie pokazuje (kafelek ucięty krawędzią okna), jest null i rysuje się jako szary pasek. Kod okna jest w strona/aplikacja-ustawienia.js, treść kart w strona/aplikacja-wtyczki.js i strona/aplikacja-katalog.js. Stałe są zapisane jak JSON (cudzysłowy przy kluczach): tests/test_napisy_menu_plus.py czyta je stąd i sprawdza w dane/napisy-interfejsu.yaml (gdzie: aplikacja) oraz w narzedzia/scenariusz_katalog.py. */

/* Nagłówek okna, pole „Search”, lewa kolumna (tylko pozycje wspólne dla obu kont ze zrzutów; reszta kolumny jest u każdego inna), zakładki strony i przyciski. */
PK.USTAWIENIA = {"tytul": "Settings", "szukaj": "Search", "zakladki": ["Yours", "Discover"], "dodaj": "Add", "wszystkie": "Show all"};
PK.USTAWIENIA_KOLUMNA = [
  {"grupa": "Preferences", "pozycje": ["General", "Account", "Privacy", "Usage", "Capabilities", "Memory", "Design systems", "Claude Code"]},
  {"grupa": "This computer", "pozycje": ["System", "Extensions", "Developer"]},
  {"grupa": "Customize", "pozycje": ["Skills", "Connectors", "Plugins"]},
];

/* Przeglądarka wtyczek, zakładka Discover (zrzut 03-59-16): karta polecana i sekcja „New plugins”. Dwa ostatnie kafelki zrzutu są ucięte krawędzią okna, więc mają tylko nazwę. */
PK.WTYCZKI_POLECANA = {"od": "From Anthropic", "nazwa": "Data", "opis": "Query, chart and explain your data — SQL, spreadsheets and dashboards in one place.", "przycisk": "Add"};
PK.WTYCZKI_SEKCJA = "New plugins";
PK.WTYCZKI_KAFELKI = [
  {"nazwa": "Ando", "opis": "Team messaging for people and AI agents: read shared conversations, fin…", "zrodlo": "Anthropic Directory", "ikona": "lista"},
  {"nazwa": "Dataiku Headless", "opis": "Connect your agent to Dataiku: inspect projects, datasets, recipes, ML, and…", "zrodlo": "Anthropic Directory", "ikona": "wykres"},
  {"nazwa": "NetSuite SuiteSkills", "opis": "NetSuite skills for insights and workflows across your business.", "zrodlo": "Anthropic Directory", "ikona": "bank"},
  {"nazwa": "learn", "opis": "Use this skill when the user wants intellectual understanding — learning…", "zrodlo": "by Anthropic", "ikona": "dokument"},
  {"nazwa": "doc-coauthoring", "opis": null, "zrodlo": null, "ikona": "dokument"},
  {"nazwa": "web-artifacts-builder", "opis": null, "zrodlo": null, "ikona": "dokument"},
];

/* Katalog konektorów, zakładka Discover (zrzuty 04-43-33 i 04-23-08): „Top connectors” z liczbą i dwanaście kafelków w kolejności ze zrzutu; dwa ostatnie są ucięte krawędzią okna, więc mają tylko nazwę. */
PK.KONEKTORY_SEKCJA = {"nazwa": "Top connectors", "liczba": "7593"};
PK.KONEKTORY_KATALOG = [
  {"nazwa": "Google Drive", "opis": "Search, read, and upload files instantly", "autor": "by Google"},
  {"nazwa": "Gmail", "opis": "Draft replies, summarize threads, & search your inbox", "autor": "by Google"},
  {"nazwa": "Google Calendar", "opis": "Manage your schedule and coordinate meetings effortlessly", "autor": "by Google"},
  {"nazwa": "Microsoft 365", "opis": "Access your company's SharePoint, OneDrive, Outlook, and Teams directly…", "autor": "by Anthropic"},
  {"nazwa": "Slack", "opis": "Send messages, create canvases, and fetch Slack data", "autor": "by Slack"},
  {"nazwa": "Notion", "opis": "Connect your Notion workspace to search, update, and power workflows…", "autor": "by Notion"},
  {"nazwa": "Canva", "opis": "Search, create, autofill, and export Canva designs", "autor": "by Canva"},
  {"nazwa": "Atlassian MCP", "opis": "Search, read and update Jira, Confluence, Bitbucket, Loom and othe…", "autor": "by Atlassian"},
  {"nazwa": "Google Sheets", "opis": "Read, analyze, and update your spreadsheets", "autor": "by Google"},
  {"nazwa": "Figma", "opis": "Generate diagrams and better code from Figma context", "autor": "by Figma"},
  {"nazwa": "Google Docs", "opis": null, "autor": null},
  {"nazwa": "Supabase", "opis": null, "autor": null},
];
