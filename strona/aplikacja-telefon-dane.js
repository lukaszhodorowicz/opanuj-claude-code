/* Symulator aplikacji Claude, dane telefonu z Remote Control: napisy ze zrzutów Łukasza z 27.10.2026 (materialy/zrzuty-lukasza/ w pamięci projektu: lista sesji IMG_1056, IMG_1057 i IMG_1058, otwarta rozmowa IMG_1059) i opisy dla czytnika ekranu. Napisy są zapisane jak JSON (cudzysłowy przy kluczach): tests/test_napisy_telefonu.py czyta je stąd i sprawdza w dane/napisy-interfejsu.yaml (gdzie: telefon). Dane konta (nazwa urządzenia, tytuł sesji, folder) to pola scenariusza `aplikacja.telefon` i `aplikacja.folder`, a nazwy innych sesji i godziny to szare paski. Wygląd: strona/aplikacja-telefon-widok.js, gra: strona/aplikacja-telefon.js. */

/* Napisy telefonu. „Opus 5.5” i „Extra” to model i poziom z konta autora zrzutu IMG_1059; w symulatorze stoją na stałe, bo scenariusz nie ma pola z modelem (umowa symulatora). */
PK.NAPISY_TELEFONU = {"tytul": "Code", "urzadzenia": "Devices", "sesje": "Sessions", "nowa": "New session", "teraz": "now", "podpowiedz": "Reply to Claude or hold to talk", "model": "Opus 5.5", "wysilek": "Extra"};

/* Opisy tylko dla czytnika ekranu (aria-label) i podpis pod ramką: tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_TELEFONU = {
  ramka: "Telefon z aplikacją Claude: lista sesji i rozmowa",
  podpis: "Aplikacja Claude na telefonie",
  wstecz: "Wróć do listy sesji",
  sesja: "Otwórz sesję z komputera",
  przycisk: "Przycisk telefonu (w ćwiczeniu bez skutku)",
  praca: "Claude pracuje",
};

/* Ikony kreskowe telefonu i paska stanu; żadna nie niesie napisu. Laptop, chmura, lupa, plus i kropki to ikony okna (PK.IKONY_APLIKACJI, PK.IKONY_EKRANU), bo zrzuty telefonu rysują je tak samo. */
PK.IKONY_TELEFONU = (() => {
  const s = (d, w) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 1.7}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const A = PK.IKONY_APLIKACJI;
  return {
    menu: s('<path d="M5 8h14M5 12h9.5M5 16h12"/>'),
    zegar: s('<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>'),
    suwaki: s('<path d="M6 4v4.5M6 13.5V20M12 4v8.5M12 17.5V20M18 4v2.5M18 11.5V20"/><circle cx="6" cy="11" r="2.2"/><circle cx="12" cy="15" r="2.2"/><circle cx="18" cy="9" r="2.2"/>'),
    mikrofon: s('<rect x="9" y="4" width="6" height="10.5" rx="3"/><path d="M6 11.5a6 6 0 0 0 12 0M12 17.5V20"/>'),
    wyslij: s('<path d="M12 18V6M6.5 11.5 12 6l5.5 5.5"/>', 2.2),
    plus: A.plus,
    laptop: A.laptop,
    szukaj: A.szukaj,
    kropki: A.kropki,
    wstecz: A.wstecz,
    chmura: PK.IKONY_EKRANU.chmura,
    /* pasek stanu: sygnał, Wi-Fi i bateria bez prawdziwych danych */
    sygnal: '<svg viewBox="0 0 18 12" fill="currentColor" aria-hidden="true"><rect x="0" y="8" width="3" height="4" rx=".8"/><rect x="5" y="5.5" width="3" height="6.5" rx=".8"/><rect x="10" y="3" width="3" height="9" rx=".8"/><rect x="15" y="0" width="3" height="12" rx=".8"/></svg>',
    wifi: '<svg viewBox="0 0 18 13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M1.5 4.8a10 10 0 0 1 15 0M4.2 7.8a6 6 0 0 1 9.6 0M7 10.8a2.2 2.2 0 0 1 4 0"/></svg>',
    bateria: '<svg viewBox="0 0 26 12" fill="none" aria-hidden="true"><rect x=".7" y=".7" width="21.6" height="10.6" rx="3.4" stroke="currentColor" stroke-width="1.2" opacity=".6"/><rect x="2.3" y="2.3" width="6.5" height="7.4" rx="2" fill="#e6b422"/><path d="M24 4v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" opacity=".6"/></svg>',
  };
})();
