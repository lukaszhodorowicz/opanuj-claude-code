/* Symulator aplikacji Claude, praca w tle, wygląd: przycisk ⋮ i menu ⋮ z dwiema pozycjami ze zrzutu Łukasza 27.10.2026 (Side chat bez skutku i Background tasks z licznikiem prac), panel zadań w tle (nagłówek Background tasks, grupa Running, karty prac w tle z tytułem zadania, rodzajem Agent i szarymi paskami czasu, tokenów i użyć), panel subagenta (tytuł zadania, szare pole z zadaniem od Claude i wynik zwykłym tekstem), niebieski odnośnik „N running tasks” w rozmowie i szare wiersze po zakończeniu pracy. Układ i napisy ze zrzutów z sieci: materialy/zrzuty-aplikacji/panel-zadan-w-tle/ i subagent-w-rozmowie/. Przyciski bez skutku (×, ‹, kwadrat zatrzymania, View transcript) są narysowane i wyszarzone; grupy Finished nie rysujemy. Grę kroków prowadzi strona/aplikacja-w-tle.js. */

/* Napisy tego elementu; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). Odnośnik w rozmowie ma formę „N running tasks” (wzór z listy napisów: liczba od 2). */
PK.NAPISY_W_TLE = { zadania: "Background tasks", grupa: "Running", rodzaj: "Agent", transkrypt: "View transcript" };
PK.tekstLinkuWTle = (n) => `${n} running tasks`;

/* Polskie opisy dla czytnika ekranu (aria-label): dokumentacja nie podaje napisów tych elementów. */
PK.OPISY_W_TLE = {
  menu: "Menu paska tytułu",
  stop: "Zatrzymanie pracy (w ćwiczeniu bez skutku)",
  zamknij: "Zamknięcie panelu (w ćwiczeniu bez skutku)",
  wstecz: "Powrót (w ćwiczeniu bez skutku)",
  panel_subagenta: "Panel subagenta",
};
PK.CELE_W_TLE = ["menu-paska", "background-tasks", "wpis-w-tle"];
PK.RODZAJE_W_TLE = ["subagent", "przeplyw"];
/* Droga ćwiczenia ma pracę w tle: pole `w_tle` kroku `claude` albo kartę przepływu (jej Once dodaje wpis przepływu). */
PK.drogiZPracaWTle = (drogi) => (drogi || []).some((d) => (d.kroki || []).some((k) => k.w_tle || k.typ === "przeplyw"));

PK.IKONA_W_TLE =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5 16 7.5 12 11.5 8 7.5z"/><path d="M12 12.5 16 16.5 12 20.5 8 16.5z"/></svg>';
PK.IKONA_WSTECZ =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>';

/* Przycisk ⋮ w oknie drogi z pracą w tle: wygląda jak dotychczasowy nieaktywny przycisk (apl-bez, aria-disabled), dopóki strona/aplikacja-w-tle.js go nie włączy; menu powstaje dopiero po otwarciu. */
PK.przyciskMenuPaska = (ikona) =>
  `<span class="apl-menu-kropki"><button type="button" class="apl-ikona apl-bez" data-pasek="menu" aria-haspopup="menu" aria-expanded="false" aria-disabled="true" aria-label="${PK.esc(PK.OPISY_W_TLE.menu)}">${ikona}</button></span>`;

/* Menu ⋮ (zrzut Łukasza 27.10.2026, plik 04-25-37): dwie pozycje z ikoną: Side chat ze skrótem (nieaktywna, bez skutku) i Background tasks z licznikiem prac `liczba` (jedyna klikalna; napisy w strona/aplikacja-ekran.js). Dawne szare pozycje (zrzut gh99530) schodzą: zrzut Łukasza pokazuje tylko te dwie. */
PK.menuPaska = (liczba) => {
  const M = PK.NAPISY_EKRANU.menu;
  const boczna = `<li role="none"><span class="apl-menu-poz apl-menu-z-ikona apl-menu-nieaktywna" role="menuitem" aria-disabled="true">${PK.IKONY_APLIKACJI.czat}<span>${PK.esc(M.rozmowaBoczna)}</span><span class="apl-menu-skrot">${PK.esc(M.skrot)}</span></span></li>`;
  const wTle = `<li role="none"><button type="button" class="apl-menu-poz apl-menu-z-ikona" role="menuitem" data-poz="w-tle">${PK.IKONA_W_TLE}<span>${PK.esc(PK.NAPISY_W_TLE.zadania)}</span><span class="apl-menu-licznik">${liczba}</span></button></li>`;
  return `<ul class="apl-menu-paska" role="menu">${boczna}${wTle}</ul>`;
};

/* Krzyżyk, strzałka wstecz i kwadrat zatrzymania: narysowane, wyszarzone, bez skutku (zrzuty nie pokazują skutku; D-2026-10-26-54). Panel zamyka krok `plik`, „Od nowa” albo nowe polecenie. */
const KRZYZYK_W_TLE = () => `<span class="apl-wtle-zamknij" aria-disabled="true" role="img" aria-label="${PK.esc(PK.OPISY_W_TLE.zamknij)}">${PK.IKONY_ZGODY.nie}</span>`;
const LICZBY_W_TLE = [[34, 22, 18], [28, 26, 20], [38, 18, 24]]; /* szare paski w wierszu tokenów, użyć narzędzi i nazwy narzędzia: liczby rosną w trakcie pracy, dokumentacja ich nie podaje */

/* Karta pracy w tle (zrzut gh74950): tytuł zadania (dana scenariusza), u subagenta wiersz z napisem Agent i szarym paskiem czasu, wiersz szarych pasków, wyszarzony odnośnik View transcript i wyszarzony kwadrat zatrzymania. Klika się tytuł subagenta (pokazuje jego wynik); przepływ nie ma w tym symulatorze rodzaju, odnośnika ani kwadratu (dokumentacja nie opisuje jego karty), a klik w niego nic nie robi. */
PK.wpisWTle = (w, i) => {
  const pasek = (p) => PK.szaryPasek(p);
  const liczby = LICZBY_W_TLE[i % LICZBY_W_TLE.length].map(pasek).join("");
  const tytul = PK.esc(w.tytul);
  if (w.rodzaj !== "subagent") return `<li><div class="apl-wtle-karta"><span class="apl-wtle-wpis" data-nr="${i + 1}">${tytul}</span><span class="apl-wtle-liczby">${liczby}</span></div></li>`;
  return (
    `<li><div class="apl-wtle-karta"><button type="button" class="apl-wtle-wpis" data-nr="${i + 1}">${tytul}</button>` +
    `<span class="apl-wtle-stop" aria-disabled="true" role="img" aria-label="${PK.esc(PK.OPISY_W_TLE.stop)}"></span>` +
    `<span class="apl-wtle-rodzaj"><b>${PK.esc(PK.NAPISY_W_TLE.rodzaj)}</b>${pasek(16)}</span>` +
    `<span class="apl-wtle-liczby">${liczby}</span>` +
    `<span class="apl-wtle-transkrypt" aria-disabled="true">${PK.esc(PK.NAPISY_W_TLE.transkrypt)}</span></div></li>`
  );
};

/* Panel zadań w tle: nagłówek z napisem Background tasks i wyszarzonym ×, grupa Running i karty prac w tle tej drogi. */
PK.panelZadanWTle = (wpisy) =>
  `<section class="apl-wtle" data-w-tle="zadania"><header class="apl-wtle-glowa"><b>${PK.esc(PK.NAPISY_W_TLE.zadania)}</b>${KRZYZYK_W_TLE()}</header>` +
  `<div class="apl-wtle-tresc"><span class="apl-wtle-grupa">${PK.esc(PK.NAPISY_W_TLE.grupa)}</span><ul class="apl-wtle-lista">${wpisy.map(PK.wpisWTle).join("")}</ul></div></section>`;

/* Panel subagenta (zrzut gh76602): w nagłówku wyszarzona strzałka ‹, tytuł zadania i wyszarzony ×; pod nim szare pole z treścią zadania (napisał je Claude) i wynik zwykłym tekstem, bez ikony, po akapicie na linijkę. */
PK.panelSubagenta = (w) =>
  `<section class="apl-wtle apl-wtle-subagent" data-w-tle="subagent" aria-label="${PK.esc(PK.OPISY_W_TLE.panel_subagenta)}">` +
  `<header class="apl-wtle-glowa"><span class="apl-wtle-wstecz" aria-disabled="true" role="img" aria-label="${PK.esc(PK.OPISY_W_TLE.wstecz)}">${PK.IKONA_WSTECZ}</span><b class="apl-wtle-tytul">${PK.esc(w.tytul)}</b>${KRZYZYK_W_TLE()}</header>` +
  `<div class="apl-wtle-zadanie"><p>${PK.esc(w.zadanie)}</p></div>` +
  `<div class="apl-wtle-wynik">${w.wynik.map((l) => `<p>${PK.esc(l)}</p>`).join("")}</div></section>`;

/* Niebieski napis pod odpowiedzią Claude (zrzuty gh74950, gh72965): liczba prac w tle w formie „N running tasks”. Nieaktywny: nie jest przyciskiem, nie reaguje na klik ani na najechanie (żadne źródło nie pokazuje, że klik w niego otwiera panel). */
PK.linkWTle = (n) => `<span class="apl-wtle-link">${PK.esc(PK.tekstLinkuWTle(n))}</span>`;

/* Szary, nieaktywny wiersz zwiniętej pracy subagenta w rozmowie (zrzut gh76602): tytuł zadania i znak ›, bez słowa Agent; skutek rozwinięcia nieopisany. */
PK.wierszKoncaWTle = (w) => `<div class="apl-wtle-wiersz" aria-disabled="true"><span>${PK.esc(w.tytul)}</span><i aria-hidden="true">›</i></div>`;
