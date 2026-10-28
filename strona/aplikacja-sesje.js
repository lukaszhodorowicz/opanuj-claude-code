/* Symulator aplikacji Claude, pasek boczny z rozmowami, wygląd (ćwiczenie z drogami i polem `aplikacja.sesje`): lista wierszy bez tekstu (szare paski, podświetlony pasek otwartej rozmowy), przycisk ⋮ przy wierszu i menu rozmowy z napisem Archive, nagłówek listy z ikoną i menu Group and sort z wierszem View all, tytuł rozmowy w pasku tytułu i widok listy rozmów z zakładką Archived. Układ ze zrzutów z sieci: materialy/zrzuty-aplikacji/pasek-boczny-sesje/ (dokumentacja aplikacji nie podaje, co pokazuje wiersz ani jak wygląda menu, więc wszystko poza czterema napisami to szare paski). Grę kroków prowadzi strona/aplikacja-sesje-gra.js. */

/* Jedyne napisy tego paska; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */
PK.NAPISY_SESJI = { archive: "Archive", grupa: "Group and sort", wszystkie: "View all", zarchiwizowane: "Archived" };

/* Polski opis przycisku ⋮ przy wierszu dla czytnika ekranu (bez dymka): dokumentacja nie podaje jego napisu. */
PK.OPIS_MENU_SESJI = "Menu rozmowy";

/* Cele kroku `klik` obsługiwane przez pasek boczny (w tym `folder`, kontrolka folderu nowej rozmowy, i `wiadomosc-od`, odnośnik karty wiadomości); cztery z nich (sesja, archive, archived, wiadomosc-od) kończą podgląd drogi w tekście lekcji (narzedzia/scenariusz_sesje.py). */
PK.CELE_SESJI = ["nowa-rozmowa", "sesja", "menu-sesji", "archive", "group-and-sort", "view-all", "archived", "folder", "wiadomosc-od"];
PK.CELE_PODGLADU_SESJI = ["sesja", "archive", "archived", "wiadomosc-od"];

/* Element, za którym stoi rząd ze znacznikiem „kliknij tutaj” (pod nim): wiersz, nagłówek listy, pozycja menu (rząd w menu), pasek zakładek, `+ New` (rząd w liście). */
Object.assign(PK.PO_CELU_KROKU, {
  "nowa-rozmowa": "li",
  sesja: ".apl-wiersz",
  "menu-sesji": ".apl-wiersz",
  archive: "li",
  "group-and-sort": ".apl-sesje-naglowek",
  "view-all": "li",
  archived: ".apl-sesje-zakladki",
});

PK.IKONY_SESJI = (() => {
  const s = (d, w) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 1.7}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    menu: s('<circle cx="12" cy="6" r=".6"/><circle cx="12" cy="12" r=".6"/><circle cx="12" cy="18" r=".6"/>', 2.6),
    suwaki: s('<path d="M8 4v5M8 14v6M16 4v9M16 18v2"/><circle cx="8" cy="11.5" r="2.3"/><circle cx="16" cy="15.5" r="2.3"/>'),
  };
})();

PK.SZEROKOSCI_WIERSZY = [78, 66, 58, 72, 62, 70]; /* szare paski kolejnych wierszy: pierwszy jak dawny szkic otwartej rozmowy */
PK.szaryPasek = (proc) => `<span class="apl-szkic" style="width:${proc}%"></span>`;
PK.szaraPozycja = (proc) => `<li role="none" class="apl-menu-szara">${PK.szaryPasek(proc)}</li>`;
PK.liniaMenu = '<li role="separator" class="apl-menu-linia"></li>';
PK.pozycjaMenu = (napis) =>
  `<li role="none"><button type="button" class="apl-menu-poz" role="menuitem">${PK.esc(napis)}</button></li>`;

/* Menu rozmowy (zrzut pasek-boczny-earlier-menu-sesji-z-archive.jpg): siedem pozycji w czterech grupach, tylko Archive z napisem i druga od dołu; reszta to szare paski bez skutku, bez skrótów klawiszowych. Menu powstaje przy otwarciu i znika przy zamknięciu (strona/aplikacja-sesje-gra.js), więc zamknięte wiersze nie niosą napisu Archive. */
PK.menuSesji = () =>
  `<ul class="apl-menu-sesji" role="menu">${[
    PK.szaraPozycja(46), PK.liniaMenu, PK.szaraPozycja(30), PK.szaraPozycja(40), PK.szaraPozycja(28), PK.liniaMenu,
    PK.szaraPozycja(54), PK.liniaMenu, PK.pozycjaMenu(PK.NAPISY_SESJI.archive), PK.szaraPozycja(36),
  ].join("")}</ul>`;

/* Menu Group and sort (zrzut pasek-boczny-biezacy-menu-grupowania-view-all-ko.png): cztery szare wiersze bez skutku i ostatni wiersz View all. */
PK.menuGrupy = () =>
  `<ul class="apl-menu-grupy" role="menu">${[
    PK.szaraPozycja(56), PK.szaraPozycja(40), PK.liniaMenu, PK.szaraPozycja(52), PK.liniaMenu, PK.szaraPozycja(60), PK.pozycjaMenu(PK.NAPISY_SESJI.wszystkie),
  ].join("")}</ul>`;

/* Wiersz listy: szary pasek (otwarta: podświetlony pasek, id: wiersz do kliknięcia w kroku `sesja`); z `menu` także przycisk ⋮ (widoczny po najechaniu), który otwiera menu rozmowy. */
PK.wierszSesji = ({ proc, id, otwarta, menu }) =>
  `<span class="apl-wiersz${otwarta ? " apl-sesja" : ""}"${id ? ` data-sesja="${PK.esc(id)}"` : ""}>${PK.szaryPasek(proc)}` +
  (menu ? `<button type="button" class="apl-wiersz-menu" aria-haspopup="menu" aria-label="${PK.esc(PK.OPIS_MENU_SESJI)}">${PK.IKONY_SESJI.menu}</button>` : "") +
  "</span>";

/* Lista pod `+ New`: nagłówek (szary pasek, po najechaniu ikona z dymkiem Group and sort i menu), wiersz otwartej rozmowy i wiersze z `aplikacja.sesje` w podanej kolejności. */
PK.sesjeBok = (apl) => {
  const N = PK.NAPISY_SESJI;
  const wiersze = [{ otwarta: true }, ...apl.sesje.map((s) => ({ id: s.id }))];
  const naglowek =
    `<div class="apl-sesje-naglowek"><span class="apl-szkic"></span>` +
    `<button type="button" class="apl-ikona apl-grupa" aria-haspopup="menu" aria-label="${PK.esc(N.grupa)}">${PK.IKONY_SESJI.suwaki}<span class="apl-dymek" aria-hidden="true">${PK.esc(N.grupa)}</span></button></div>`;
  const rzad = PK.folderyRozmow(apl)
    ? PK.wierszeGrupFolderow(apl) /* folder każdej rozmowy: wiersze w grupach z nagłówkiem teczki (strona/aplikacja-sesje-foldery.js) */
    : wiersze.map((w, i) => PK.wierszSesji({ ...w, menu: true, proc: PK.SZEROKOSCI_WIERSZY[i % PK.SZEROKOSCI_WIERSZY.length] }));
  return `<div class="apl-bok-sesje apl-sesje-lista">${naglowek}${rzad.join("")}</div>`;
};

/* Tytuł rozmowy w pasku tytułu: nazwa nadana przez kursanta albo (bez nazwy) szary pasek, jak dotąd. Tytuł nie jest klikalny: dokumentacja nie opisuje skutku kliknięcia. */
PK.tytulRozmowy = (nazwa) =>
  nazwa ? `<span class="apl-tytul">${PK.esc(nazwa)}</span>` : '<span class="apl-szkic apl-szkic-tytul"></span>';

/* Widok listy rozmów po View all (zrzut pasek-boczny-biezacy-strona-sesji-archived.png): nagłówek jako szary pasek, dwie zakładki (pierwsza bez tekstu, wybrana; druga Archived), pod nimi wiersze wstawiane przez PK.wierszeListy. Bez przycisku „New session” i ikony szukania. */
PK.widokListySesji = () =>
  `<section class="apl-sesje-widok" hidden><div class="apl-sesje-tytul">${PK.szaryPasek(22)}</div>` +
  `<div class="apl-sesje-zakladki" role="tablist"><span class="apl-sesje-zakl wybrana" role="tab" aria-selected="true"><span class="apl-szkic"></span></span>` +
  `<button type="button" class="apl-sesje-zakl" role="tab" aria-selected="false" data-zakladka="archived">${PK.esc(PK.NAPISY_SESJI.zarchiwizowane)}</button></div>` +
  '<ul class="apl-sesje-wiersze"></ul></section>';

/* `n` szarych wierszy listy: pasek po lewej, krótki pasek po prawej; wiersze niczego nie otwierają (dokumentacja nie mówi, co robi kliknięcie rozmowy z tej listy). */
PK.wierszeListy = (n) =>
  Array.from({ length: n }, (_, i) => `<li>${PK.szaryPasek([46, 38, 52, 34, 44][i % 5])}<span class="apl-szkic apl-sesje-czas"></span></li>`).join("");

/* Dymki rozmowy z listy `{kto, tekst}`: te same co w oknie startowym ćwiczenia. */
PK.dymkiRozmowy = (lista) => (lista || []).map((w) => PK.dymekAplikacji({ kto: w.kto, tekst: w.tekst })).join("");
