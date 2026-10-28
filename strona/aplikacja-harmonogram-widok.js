/* Symulator aplikacji Claude, zadanie według harmonogramu, wygląd (ćwiczenie z drogami i polem `aplikacja.harmonogram`): pozycja Scheduled w pasku bocznym, strona Scheduled tasks (zrzut Łukasza 05-04-44), okno New scheduled task z polami z harmonogramu i sekcją Advanced settings z trzema zakładkami (05-04-51, 05-05-25, 05-05-38, 05-05-45, 05-05-56) i strona zadania z historią, instrukcją i uprawnieniami (05-06-07). Napisy: `PK.NAPISY_HARMONOGRAMU` (każdy ma wpis `gdzie: aplikacja` ze zrzutem w dane/napisy-interfejsu.yaml); cudze zadania, zakładki Yours i Templates, wpis historii i nazwa komputera to szare paski, bo zrzuty nie pokazują ich treści albo to dane konta. Grę kroków prowadzi strona/aplikacja-harmonogram.js. */

PK.NAPISY_HARMONOGRAMU = {
  pasek: "Scheduled",
  strona: "Scheduled tasks",
  nowe: "New task",
  puste: "No scheduled tasks yet.",
  okno: "New scheduled task",
  nazwa: "Name",
  tryb: "Auto",
  model: "Default model",
  ramka: "For this task, Claude will work and use connectors without pausing for approval.",
  wskazowki: "See safe use tips",
  wyzwalacz: "Trigger",
  harmonogram: "Schedule",
  zaawansowane: "Advanced settings",
  anuluj: "Cancel",
  utworz: "Create",
  zakladki: { general: "General", connectors: "Connectors", notifications: "Notifications" },
  ogolne: {
    tylkoTutaj: "Only on this computer",
    tylkoTutajOpis: "Only runs while your computer is on. Use this to run against a folder on this computer instead of a cloud environment.",
    wymagaj: "Require this computer",
    wymagajOpis: "Leave this off unless the task needs this computer’s folders or Claude in Chrome. When on, the task runs only while the computer is awake.",
    folder: "Local folder",
    folderOpis: "Claude can work in this folder while this computer is on and awake.",
    repozytorium: "Repository",
    repozytoriumOpis: "Picking a repository makes this a Claude Code task.",
    projekt: "Project",
    projektOpis: "A project in the cloud",
    brak: "None",
  },
  konektory: { brak: "No connectors connected", opis: "Add connectors in Settings to use them in your tasks.", dodaj: "Add connectors" },
  powiadomienia: {
    glowny: "Notify me when this task finishes",
    opis: "Claude will send you a one-line summary when each run completes — only when there’s something worth telling you for tasks that watch for a condition.",
    push: "Push notification",
    email: "Email",
    slack: "Slack",
  },
  zadanie: { uruchom: "Run now", aktywne: "Active", historia: "History", brak: "No runs yet", instrukcje: "Instructions", powtarza: "Repeats", uprawnienia: "Permissions", opisAuto: "Runs without asking." },
};

/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_HARMONOGRAMU = { zamknijOkno: "Zamknij okno (w ćwiczeniu bez skutku)", zamknijKomunikat: "Zamknij komunikat (w ćwiczeniu bez skutku)", okno: "Nowe zadanie według harmonogramu" };

PK.IKONY_HARMONOGRAMU = (() => {
  const s = (d, w) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 1.7}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    zegar: s('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/>'),
    stoper: s('<circle cx="12" cy="14" r="7"/><path d="M12 14V10M10 3.5h4M12 3.5V7M18.5 7l1.2-1.2"/>', 1.5),
    odtworz: s('<path d="M8 5.5v13l10.5-6.5z"/>'),
    auto: s('<path d="M5 6.5v11l7-5.5zM12 6.5v11l7-5.5z"/>', 1.6),
    projekt: s('<path d="M7 9.5h10M8.5 6.5h7M5.5 12.5h13v7h-13z"/>'),
    klocki: s('<rect x="4" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="12" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="4" y="4.5" width="6.5" height="6.5" rx="1.2"/><path d="m15.5 4.5 3.5 3.5-3.5 3.5L12 8z"/>'),
  };
})();

/* Godzina „09:20” w zapisie ze strony zadania: „9:20 AM” (tak samo liczy narzedzia/scenariusz_harmonogram.py, godzina_12). */
PK.godzina12 = (pora) => {
  const g = parseInt(pora.slice(0, 2), 10);
  return `${g % 12 || 12}:${pora.slice(3)} ${g < 12 ? "AM" : "PM"}`;
};
PK.nastepnyBieg = (h) => `Next run: today at ${PK.godzina12(h.pora)}`;
PK.powtarzaSie = (h) => `${h.czestotliwosc} at ${PK.godzina12(h.pora)}`;
PK.komunikatUtworzenia = (h) => `“${h.nazwa}” created.`;

/* Pozycja paska bocznego (ikona zegara, napis Scheduled); wstawia ją po pozycji Customize. */
PK.pozycjaScheduled = () =>
  `<li class="apl-bok-harm"><span class="apl-bok-ikona">${PK.IKONY_HARMONOGRAMU.zegar}</span><span class="apl-bok-napis">${PK.esc(PK.NAPISY_HARMONOGRAMU.pasek)}</span></li>`;

/* Strona Scheduled tasks (zrzut 05-04-44): tytuł, zakładki jako szare paski, ikony szukania, filtra i sortowania bez skutku, przycisk New task ze strzałką, pusta lista z zegarem, napisem i drugim New task, pod spodem cudze zadania jako szare karty. */
PK.stronaScheduled = () => {
  const { esc, szkic } = PK;
  const N = PK.NAPISY_HARMONOGRAMU;
  const K = PK.IKONY_KATALOGU;
  const karta = (a, b, c) => `<li><span class="apl-harm-szablon-ikona"></span><span class="apl-harm-szablon-tekst">${szkic(a)}${szkic(b)}${szkic(c)}</span></li>`;
  return (
    `<div class="apl-harm-lista"><h3 class="apl-harm-tytul">${esc(N.strona)}</h3>` +
    `<div class="apl-harm-gora"><span class="apl-harm-zakladki"><span class="apl-harm-zakl wybrana">${szkic(100)}</span><span class="apl-harm-zakl">${szkic(100)}</span></span>` +
    `<span class="apl-harm-narzedzia"><span class="apl-harm-ikona-nar" aria-hidden="true">${PK.IKONY_APLIKACJI.szukaj}</span><span class="apl-harm-ikona-nar" aria-hidden="true">${K.filtr}</span><span class="apl-harm-ikona-nar" aria-hidden="true">${K.sortuj}</span>` +
    `<button type="button" class="apl-harm-nowe" data-poz="gora">${esc(N.nowe)}<span class="apl-harm-chevron">${K.rozwin}</span></button></span></div>` +
    `<div class="apl-harm-puste"><span class="apl-harm-stoper" aria-hidden="true">${PK.IKONY_HARMONOGRAMU.stoper}</span><p>${esc(N.puste)}</p><button type="button" class="apl-harm-nowe apl-harm-nowe-srodek" data-poz="srodek">${esc(N.nowe)}</button></div>` +
    `<ul class="apl-harm-szablony" aria-hidden="true">${karta(34, 86, 50)}${karta(30, 80, 62)}${karta(46, 84, 40)}${karta(32, 78, 56)}${karta(40, 82, 48)}${karta(36, 76, 60)}</ul></div>`
  );
};

/* Wiersz ustawienia z zakładki General: tytuł i podpis po lewej, kontrolka po prawej. */
const harmWiersz = (tytul, opis, kontrolka, nazwaKomputera) =>
  `<div class="apl-harm-ust"><div class="apl-harm-ust-tekst"><b>${PK.esc(tytul)}${nazwaKomputera ? `<span class="apl-harm-komputer">${PK.szkic(100)}</span>` : ""}</b><span>${PK.esc(opis)}</span></div>${kontrolka}</div>`;
const harmPrzelacznik = (wlaczony, opis) =>
  `<span class="apl-harm-przel${wlaczony ? " wl" : ""}" role="switch" aria-checked="${wlaczony}" aria-disabled="true" aria-label="${PK.esc(opis)}"><i></i></span>`;
const harmWybor = (ikona, napis, strzalka) =>
  `<span class="apl-harm-wybor">${ikona ? `<span class="apl-harm-wybor-ikona">${ikona}</span>` : ""}<span>${PK.esc(napis)}</span>${strzalka ? `<span class="apl-harm-chevron">${PK.IKONY_KATALOGU.rozwin}</span>` : ""}</span>`;
const harmPoleWyboru = (checked, napis) => `<span class="apl-harm-pole-wyboru"><i class="${checked ? "zazn" : ""}"></i><span>${PK.esc(napis)}</span></span>`;

/* Trzy zakładki sekcji Advanced settings: General (z folderem z harmonogramu w Local folder), Connectors i Notifications. */
PK.zakladkiZaawansowane = (h) => {
  const { esc } = PK;
  const N = PK.NAPISY_HARMONOGRAMU;
  const O = N.ogolne;
  const P = N.powiadomienia;
  const I = PK.IKONY_APLIKACJI;
  const zakl = (k, napis) => `<button type="button" class="apl-harm-zakl${k === "general" ? " wybrana" : ""}" data-z="${k}">${esc(napis)}</button>`;
  return (
    `<div class="apl-harm-zakladki apl-harm-zakl-zaaw" role="tablist">${Object.entries(N.zakladki).map(([k, n]) => zakl(k, n)).join("")}</div>` +
    `<div class="apl-harm-pane apl-harm-pane-general">${harmWiersz(O.tylkoTutaj, O.tylkoTutajOpis, harmPrzelacznik(false, O.tylkoTutaj))}` +
    `${harmWiersz(O.wymagaj, O.wymagajOpis, harmPrzelacznik(false, O.wymagaj), true)}` +
    `${harmWiersz(O.folder, O.folderOpis, harmWybor(I.folder, h.folder, false))}` +
    `${harmWiersz(O.repozytorium, O.repozytoriumOpis, harmWybor("", O.brak, true))}` +
    `${harmWiersz(O.projekt, O.projektOpis, harmWybor(PK.IKONY_HARMONOGRAMU.projekt, O.brak, true))}</div>` +
    `<div class="apl-harm-pane apl-harm-pane-connectors"><div class="apl-harm-konektory"><span class="apl-harm-konektory-ikona">${PK.IKONY_HARMONOGRAMU.klocki}</span><b>${esc(N.konektory.brak)}</b><span>${esc(N.konektory.opis)}</span><span class="apl-harm-dodaj-kon">${esc(N.konektory.dodaj)}</span></div></div>` +
    `<div class="apl-harm-pane apl-harm-pane-notifications">${harmWiersz(P.glowny, P.opis, harmPrzelacznik(true, P.glowny))}<div class="apl-harm-kanaly">${harmPoleWyboru(true, P.push)}${harmPoleWyboru(false, P.email)}${harmPoleWyboru(false, P.slack)}</div></div>`
  );
};

/* Okno New scheduled task nad stroną (zrzuty 05-04-51 do 05-05-56): pola z `h` (nazwa, polecenie, częstotliwość, pora), rząd Auto i Default model, ramka, rząd Trigger i zwinięta sekcja Advanced settings; Cancel i X bez skutku, Create zamyka okno. */
PK.oknoHarmonogramu = (h) => {
  const { esc } = PK;
  const N = PK.NAPISY_HARMONOGRAMU;
  const O = PK.OPISY_HARMONOGRAMU;
  const K = PK.IKONY_KATALOGU;
  const H = PK.IKONY_HARMONOGRAMU;
  const lista = (ikona, napis) => `<span class="apl-harm-p">${ikona || ""}<span>${esc(napis)}</span><span class="apl-harm-chevron">${K.rozwin}</span></span>`;
  return (
    `<div class="apl-harm-tlo"><div class="apl-harm-okno" role="dialog" aria-label="${esc(O.okno)}">` +
    `<div class="apl-harm-okno-gora"><span class="apl-harm-okno-tytul">${esc(N.okno)}</span><button type="button" class="apl-harm-x" aria-disabled="true" aria-label="${esc(O.zamknijOkno)}">${K.x}</button></div>` +
    `<div class="apl-harm-srodek"><span class="apl-harm-etykieta">${esc(N.nazwa)}</span><div class="apl-harm-pole-nazwy">${esc(h.nazwa)}</div>` +
    `<div class="apl-harm-polecenie"><div class="apl-harm-polecenie-tekst">${esc(h.polecenie)}</div>` +
    `<div class="apl-harm-rzad-modelu"><span class="apl-harm-tryb">${H.auto}<span>${esc(N.tryb)}</span><span class="apl-harm-chevron">${K.rozwin}</span></span><span class="apl-harm-model"><span>${esc(N.model)}</span><span class="apl-harm-chevron">${K.rozwin}</span></span></div></div>` +
    `<p class="apl-harm-ramka"><span>${esc(N.ramka)}</span> <span class="apl-harm-link" aria-disabled="true">${esc(N.wskazowki)}</span></p>` +
    `<div class="apl-harm-wyzwalacz"><b>${esc(N.wyzwalacz)}</b>${lista(H.zegar, N.harmonogram)}${lista("", h.czestotliwosc)}<span class="apl-harm-godzina">${esc(h.pora)}</span><span class="apl-harm-plus" aria-hidden="true">${K.plus}</span></div>` +
    `<div class="apl-harm-zaaw"><button type="button" class="apl-harm-zaaw-glowa" aria-expanded="false"><span>${esc(N.zaawansowane)}</span><span class="apl-harm-chevron">${K.rozwin}</span></button>` +
    `<div class="apl-harm-zaaw-tresc" data-zakl="general">${PK.zakladkiZaawansowane(h)}</div></div></div>` +
    `<div class="apl-harm-dol"><span class="apl-harm-anuluj" aria-disabled="true">${esc(N.anuluj)}</span><button type="button" class="apl-harm-utworz">${esc(N.utworz)}</button></div>` +
    `</div></div>`
  );
};

/* Strona zadania (zrzut 05-06-07): okruszki, tytuł, Next run, Run now z przełącznikiem Active, historia (pusta albo z jednym wpisem jako szare paski), instrukcja, powtarzanie, uprawnienia Auto i komunikat o utworzeniu (ukrywa go gra po chwili). */
PK.stronaZadania = (h) => {
  const { esc, szkic } = PK;
  const N = PK.NAPISY_HARMONOGRAMU;
  const Z = N.zadanie;
  const O = PK.OPISY_HARMONOGRAMU;
  const H = PK.IKONY_HARMONOGRAMU;
  const sekcja = (naglowek, tresc) => `<h4>${esc(naglowek)}</h4>${tresc}`;
  return (
    `<div class="apl-harm-zadanie"><div class="apl-harm-okruszki"><span>${esc(N.strona)}</span><span class="apl-harm-ukosnik" aria-hidden="true"></span><span>${esc(h.nazwa)}</span><span class="apl-harm-chevron">${PK.IKONY_KATALOGU.rozwin}</span></div>` +
    `<div class="apl-harm-zadanie-gora"><div class="apl-harm-zadanie-opis"><h3>${esc(h.nazwa)}</h3><p>${esc(PK.nastepnyBieg(h))}</p></div>` +
    `<div class="apl-harm-akcje"><button type="button" class="apl-harm-uruchom">${H.odtworz}<span>${esc(Z.uruchom)}</span></button><span class="apl-harm-aktywne">${esc(Z.aktywne)}</span>` +
    `<span class="apl-harm-przel wl" role="switch" aria-checked="true" aria-disabled="true" aria-label="${esc(Z.aktywne)}"><i></i></span></div></div>` +
    `<div class="apl-harm-kolumny"><section class="apl-harm-historia">${sekcja(Z.historia, `<div class="apl-harm-hist-tresc"><p>${esc(Z.brak)}</p></div>`)}</section>` +
    `<section class="apl-harm-szczegoly">${sekcja(Z.instrukcje, `<p>${esc(h.polecenie)}</p>`)}${sekcja(Z.powtarza, `<p>${esc(PK.powtarzaSie(h))}</p>`)}` +
    `${sekcja(Z.uprawnienia, `<p class="apl-harm-uprawnienia"><b>${H.auto}<span>${esc(N.tryb)}</span></b><span>${esc(Z.opisAuto)}</span></p>`)}</section></div>` +
    `<div class="apl-harm-komunikat" hidden><span>${esc(PK.komunikatUtworzenia(h))}</span><button type="button" class="apl-harm-x" aria-disabled="true" aria-label="${esc(O.zamknijKomunikat)}">${PK.IKONY_KATALOGU.x}</button></div></div>`
  );
};
/* Wpis historii po Run now: dwa szare paski (zrzuty nie pokazują wpisu przebiegu, więc bez napisu). */
PK.wpisHistorii = () => `<div class="apl-harm-przebieg" aria-hidden="true">${PK.szkic(100)}${PK.szkic(100)}</div>`;
