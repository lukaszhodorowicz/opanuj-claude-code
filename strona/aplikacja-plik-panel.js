/* Symulator aplikacji Claude, wygląd panelu pliku obok rozmowy, karty pliku w rozmowie, menu pliku i pierwszej ikony paska tytułu według zrzutów Łukasza z 27.10.2026 (15-27-18, 15-27-25, 15-27-51, 15-28-18). Panel: pasek z kartą pliku (nazwa kursywą i ×) i ikonami (lupa, lista z kropkami, „…”, rozwiń, zamknij), podpis z nazwą pliku i numerowane linijki z podświetloną pierwszą. Wszystkie ikony poza „…” są bez skutku; „…” otwiera menu tylko w kroku `klik` z celem plik-menu (strona/aplikacja-plik-gra.js). Napisy: strona/aplikacja-plik-dane.js. */

/* Ikony kreskowe panelu; żadna nie niesie napisu. */
PK.IKONY_PLIKU = (() => {
  const s = (d, w) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 1.7}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const I = PK.IKONY_APLIKACJI;
  return {
    lupa: I.szukaj,
    lista: s('<circle cx="5.5" cy="7" r=".7"/><path d="M9.5 7H20"/><circle cx="5.5" cy="12" r=".7"/><path d="M9.5 12H20"/><circle cx="5.5" cy="17" r=".7"/><path d="M9.5 17H20"/>', 2),
    kropki: I.kropki,
    rozwin: s('<path d="M14 4.5h5.5V10M10 19.5H4.5V14M19.5 4.5l-6.5 6.5M4.5 19.5 11 13"/>'),
    zamknij: s('<path d="m6 6 12 12M18 6 6 18"/>', 1.8),
    szyna: s('<rect x="3.5" y="5" width="17" height="14" rx="3.5"/><circle cx="8" cy="10" r=".7"/><path d="M11.5 10h5"/><circle cx="8" cy="14" r=".7"/><path d="M11.5 14h5"/>', 1.6),
  };
})();

/* Opis dla czytnika ekranu przycisku „…” panelu pliku. */
PK.OPIS_MENU_PLIKU = "Menu panelu pliku";

/* Otwarty plik: pasek panelu, podpis z nazwą i numerowane linijki bez znaków zmian; ten sam wygląd w oknie i w podglądzie w tekście lekcji. Pierwsza linijka jest podświetlona jak w edytorze (kursor stoi w pierwszej linii). Numer linijki stoi w `.apl-znak`, tekst w `.apl-l-tekst`. */
PK.plikAplikacji = (nazwa, linijki) => {
  const { esc } = PK;
  const I = PK.IKONY_PLIKU;
  const ikona = (svg) => `<span class="apl-pp-ikona" aria-hidden="true">${svg}</span>`;
  const wiersz = (l, i) =>
    `<div class="apl-l bez${i === 0 ? " apl-l-biezaca" : ""}"><span class="apl-znak" aria-hidden="true">${i + 1}</span><span class="apl-l-tekst">${esc(l) || "&nbsp;"}</span></div>`;
  return (
    `<section class="apl-plik apl-plik-tresc">` +
    `<div class="apl-pp-pasek"><span class="apl-pp-karta"><i>${esc(nazwa)}</i><span class="apl-pp-x" aria-hidden="true">${I.zamknij}</span></span>` +
    `<span class="apl-pp-ikony">${ikona(I.lupa)}${ikona(I.lista)}<span class="apl-pp-menu-opak"><button type="button" class="apl-pp-ikona apl-pp-menu" aria-haspopup="menu" aria-expanded="false" aria-disabled="true" aria-label="${esc(PK.OPIS_MENU_PLIKU)}">${I.kropki}</button></span>${ikona(I.rozwin)}${ikona(I.zamknij)}</span></div>` +
    `<header><b>${esc(nazwa)}</b></header>` +
    `<div class="apl-linijki">${(linijki || []).map(wiersz).join("")}</div></section>`
  );
};

/* Karta pliku w rozmowie (zrzut 15-27-18): znaczek rodzaju (TXT), nazwa pliku (sama nazwa, bez teczek) i rozmiar „NB”. Rodzaj bierze się z rozszerzenia (walidator dopuszcza tylko .txt), rozmiar to liczba bajtów ze scenariusza. */
PK.kartaPliku = (plik, rozmiar) => {
  const { esc } = PK;
  const nazwa = plik.slice(plik.lastIndexOf("/") + 1);
  const rodzaj = PK.RODZAJ_KARTY_PLIKU[nazwa.slice(nazwa.lastIndexOf(".")).toLowerCase()] || "";
  return `<div class="apl-kp" role="group" aria-label="Karta pliku"><span class="apl-kp-rodzaj">${esc(rodzaj)}</span><span class="apl-kp-nazwa">${esc(nazwa)}</span><span class="apl-kp-rozmiar">${rozmiar}B</span></div>`;
};

/* Menu z grup pozycji (PK.MENU_PLIKU, PK.MENU_KARTY_PLIKU): pozycje to przyciski z napisem w `data-poz`, wszystkie nieaktywne (`aria-disabled`), dopóki krok nie czeka na jedną z nich. Pole wyboru (`ptak` jest prawdą albo fałszem) dostaje rolę menuitemcheckbox, niebieski ✓ stoi tylko przy zaznaczonych. */
PK.menuPliku = (grupy, klasa) => {
  const { esc } = PK;
  const poz = (p) => {
    const pole = typeof p.ptak === "boolean";
    const dodatki =
      (p.skrot ? `<span class="apl-mp-szary">${esc(p.skrot)}</span>` : "") +
      (p.wartosc ? `<span class="apl-mp-szary">${esc(p.wartosc)}</span>` : "") +
      (p.podmenu ? `<span class="apl-mp-str" aria-hidden="true">${PK.IKONY_APLIKACJI.dalej}</span>` : "") +
      (pole ? `<span class="apl-mp-ptak" aria-hidden="true">${p.ptak ? PK.IKONY_ZGODY.tak : ""}</span>` : "");
    return `<li role="none"><button type="button" class="apl-mp-poz" role="${pole ? "menuitemcheckbox" : "menuitem"}"${pole ? ` aria-checked="${p.ptak}"` : ""} aria-disabled="true" data-poz="${esc(p.napis)}"><span class="apl-mp-nazwa">${esc(p.napis)}</span>${dodatki}</button></li>`;
  };
  const kreska = '<li class="apl-mp-kreska" role="separator"></li>';
  return `<ul class="apl-menu-pliku ${klasa}" role="menu">${grupy.map((g) => g.map(poz).join("")).join(kreska)}</ul>`;
};

/* Pierwsza ikona paska tytułu (zrzut 15-28-18): lista w zaokrąglonym polu z dymkiem „Show session rail”. Powstaje tylko w ćwiczeniu z krokiem `klik` z celem ikona-tytulu (reszta ćwiczeń ma pasek jak dotąd). Przycisk nie otwiera niczego: dymek pokazuje najechanie albo krok. */
PK.ikonaSzyny = () => {
  const napis = PK.esc(PK.DYMKI_PASKA["1"]);
  return `<button type="button" class="apl-ikona apl-ikona-szyna" data-pasek="szyna" title="${napis}" aria-label="${napis}">${PK.IKONY_PLIKU.szyna}<span class="apl-dymek" aria-hidden="true">${napis}</span></button>`;
};
