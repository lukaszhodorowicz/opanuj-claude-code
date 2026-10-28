/* Symulator aplikacji Claude, okno Settings nad całym oknem symulatora (wspólne dla katalogu konektorów, strona/aplikacja-katalog.js, i przeglądarki wtyczek, strona/aplikacja-wtyczki.js): nagłówek „Settings” z wyszarzonym X, lewa kolumna z napisami ze zrzutów (dane w strona/aplikacja-ustawienia-dane.js, a w wariantach kont A i B w strona/aplikacja-ustawienia-konta.js, wybór polem `aplikacja.konto_ustawien`), nagłówek strony z zakładkami i przyciskami, miejsce na zawartość strony; ikony kreskowe bez marek. */

/* Ikony rysowane kreską, bez marek: żadna nie niesie napisu ani logo (ikony konektorów to znaki funkcji, nie logo firm). */
PK.IKONY_KATALOGU = (() => {
  const s = (d) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    /* kafelki konektorów */
    "Google Drive": s('<path d="M7 18.5a4 4 0 0 1-.6-7.9A5.5 5.5 0 0 1 17 9.4a4.6 4.6 0 0 1 .5 9.1z"/>'),
    Gmail: s('<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m4.5 7.5 7.5 6 7.5-6"/>'),
    "Google Calendar": s('<rect x="4" y="5.5" width="16" height="14.5" rx="2.5"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>'),
    "Microsoft 365": s('<rect x="4.5" y="4.5" width="6.5" height="6.5" rx="1.2"/><rect x="13" y="4.5" width="6.5" height="6.5" rx="1.2"/><rect x="4.5" y="13" width="6.5" height="6.5" rx="1.2"/><rect x="13" y="13" width="6.5" height="6.5" rx="1.2"/>'),
    Slack: s('<path d="M12 4.5c-4.4 0-7.5 2.9-7.5 6.6 0 2 1 3.8 2.6 5l-.6 3.4 3.6-1.9c.6.1 1.2.2 1.9.2 4.4 0 7.5-2.9 7.5-6.7S16.4 4.5 12 4.5z"/>'),
    Notion: s('<path d="M7 3.5h8l3.5 3.5v13.5H7z"/><path d="M15 3.5V7h3.5M10 12h5M10 15.5h5"/>'),
    Canva: s('<path d="M4.5 19.5l3-1 10.8-10.8-2-2L5.5 16.5z"/><path d="m14.5 6.5 2 2"/>'),
    "Atlassian MCP": s('<path d="M12 4.5 20 19.5H4z"/>'),
    "Google Sheets": s('<rect x="4.5" y="4.5" width="15" height="15" rx="2.5"/><path d="M4.5 10h15M4.5 14.5h15M10 4.5v15"/>'),
    Figma: s('<rect x="5" y="5" width="6.5" height="6.5" rx="1.5"/><rect x="12.5" y="5" width="6.5" height="6.5" rx="3.2"/><rect x="5" y="12.5" width="6.5" height="6.5" rx="3.2"/>'),
    "Google Docs": s('<path d="M7 3.5h7l4.5 4.5v12.5H7z"/><path d="M14 3.5V8h4.5M10 12.5h5.5M10 16h5.5"/>'),
    Supabase: s('<ellipse cx="12" cy="7" rx="6.5" ry="2.8"/><path d="M5.5 7v10c0 1.5 2.9 2.8 6.5 2.8s6.5-1.3 6.5-2.8V7M5.5 12c0 1.5 2.9 2.8 6.5 2.8s6.5-1.3 6.5-2.8"/>'),
    /* kafelki wtyczek */
    lista: s('<path d="m5 7 1.6 1.6L9.5 5.5M5 14.5l1.6 1.6 2.9-3.1M12.5 7.5h6.5M12.5 15h6.5"/>'),
    wykres: s('<path d="M7 19.5v-7M12 19.5v-12M17 19.5v-9"/>'),
    bank: s('<path d="M4.5 9.5 12 4.5l7.5 5zM6.5 10v7M10 10v7M14 10v7M17.5 10v7M4.5 19.5h15"/>'),
    dokument: s('<path d="M7 3.5h10a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H8a2 2 0 0 1-2-2V4.5"/><path d="M9.5 9h5M9.5 12.5h5"/>'),
    /* okno i lewa kolumna */
    kloda: s('<rect x="5.5" y="10.5" width="13" height="9.5" rx="2.2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>'),
    x: s('<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>'),
    plus: s('<path d="M12 5v14M5 12h14"/>'),
    dalej: s('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    rozwin: s('<path d="m7 10 5 5 5-5"/>'),
    filtr: s('<path d="M5 7h14M8 12h8M10.5 17h3"/>'),
    sortuj: s('<path d="M8 19V5M5 8l3-3 3 3M16 5v14M13 16l3 3 3-3"/>'),
    zweryfikowany: s('<circle cx="12" cy="12" r="8"/><path d="m8.7 12.2 2.3 2.3 4.3-4.6"/>'),
    ogolne: s('<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.3M12 18.2v2.3M3.5 12h2.3M18.2 12h2.3M6 6l1.6 1.6M16.4 16.4 18 18M18 6l-1.6 1.6M7.6 16.4 6 18"/>'),
    konto: s('<circle cx="12" cy="8.5" r="3.2"/><path d="M5.5 19.5c.8-3.4 3.4-5 6.5-5s5.7 1.6 6.5 5"/>'),
    prywatnosc: s('<path d="M12 4 5.5 6.5v5c0 4 2.7 6.9 6.5 8.5 3.8-1.6 6.5-4.5 6.5-8.5v-5z"/><circle cx="12" cy="11" r="1.6"/>'),
    uzycie: s('<circle cx="12" cy="12" r="8"/><path d="M12 12V8.5"/>'),
    mozliwosci: s('<rect x="3.5" y="7.5" width="17" height="12" rx="2.5"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5"/>'),
    pamiec: s('<path d="M9.5 5a3 3 0 0 0-3 3 3 3 0 0 0-1.5 5.2A3 3 0 0 0 9.5 19H12V5zM14.5 5a3 3 0 0 1 3 3 3 3 0 0 1 1.5 5.2 3 3 0 0 1-4.5 5.8H12V5z"/>'),
    paleta: s('<path d="M12 4.5a7.5 7.5 0 1 0 0 15c1.2 0 1.8-.8 1.4-1.8-.4-1 .2-2 1.3-2H17a2.5 2.5 0 0 0 2.5-2.5C19.5 8 16.2 4.5 12 4.5z"/><circle cx="8.5" cy="11" r=".8"/><circle cx="11" cy="8" r=".8"/><circle cx="15" cy="8.7" r=".8"/>'),
    kod: s('<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>'),
    system: s('<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M9 19.5h6M12 16v3.5"/>'),
    narzedzie: s('<path d="M14.5 6.5a4 4 0 0 0 4.8 5.2L12 19a2.1 2.1 0 0 1-3-3l7.3-7.3z"/>'),
    klocki: s('<rect x="4" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="12" y="12" width="6.5" height="6.5" rx="1.2"/><rect x="4" y="4.5" width="6.5" height="6.5" rx="1.2"/><path d="m15.5 4.5 3.5 3.5-3.5 3.5L12 8z"/>'),
    wtyczka: s('<path d="M9 4v4M15 4v4M7 8h10v3.5a5 5 0 0 1-10 0z"/><path d="M12 16.5V20"/>'),
    zwoj: s('<path d="M7.5 4.5h9.5a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H8.5a2 2 0 0 1-2-2V6.5"/><path d="M9.5 9h6M9.5 12.5h6"/>'),
  };
})();
/* Ikony lewej kolumny w kolejności PK.USTAWIENIA_KOLUMNA. */
PK.IKONY_KOLUMNY = ["ogolne", "konto", "prywatnosc", "uzycie", "mozliwosci", "pamiec", "paleta", "kod", "system", "wtyczka", "narzedzie", "zwoj", "klocki", "wtyczka"];

/* Lewa kolumna okna: bez wariantu konta pozycje wspólne obu kont ze zrzutów (PK.USTAWIENIA_KOLUMNA, ikony w kolejności PK.IKONY_KOLUMNY), z wariantem „A” albo „B” pozycje jednego z dwóch kont (PK.USTAWIENIA_KONTA, ikony po nazwie pozycji, strona/aplikacja-ustawienia-konta.js). Zwraca [{grupa, pozycje: [{napis, ikona, zewnetrzna}]}]; `zewnetrzna` to pozycja z ukośną strzałką (link na zewnątrz). */
PK.kolumnaUstawien = (konto) => {
  const wariant = konto && PK.USTAWIENIA_KONTA && PK.USTAWIENIA_KONTA[konto];
  if (wariant)
    return wariant.map((g) => ({
      grupa: g.grupa,
      pozycje: g.pozycje.map((napis) => ({ napis, ikona: PK.IKONY_POZYCJI_USTAWIEN[napis], zewnetrzna: PK.USTAWIENIA_ZEWNETRZNE.includes(napis) })),
    }));
  let n = 0;
  return PK.USTAWIENIA_KOLUMNA.map((g) => ({ grupa: g.grupa, pozycje: g.pozycje.map((napis) => ({ napis, ikona: PK.IKONY_KOLUMNY[n++] })) }));
};

/* Szary pasek zamiast tekstu: szerokość w procentach, klasa dodatkowa. */
PK.szkic = (proc, klasa = "") => `<span class="apl-szkic ${klasa}" style="width:${proc}%"></span>`;

/* Okno Settings nad całym oknem symulatora: przyciemnione tło, nagłówek „Settings” z wyszarzonym X, lewa kolumna (wybrana pozycja `o.strona`), nagłówek strony (tytuł `o.strona`, zakładki Yours i Discover z wybraną drugą, pole Search, przyciski) i miejsce na zawartość. Wszystko poza zawartością jest bez skutku. Zwraca {tlo, zawartosc, pokaz}: `pokaz(true|false)` otwiera i zamyka okno (okno symulatora rośnie do stałej wysokości, klasa katalog-otwarty). Opcje: opis i zamknij (aria-label), strona (napis wybranej pozycji kolumny i tytuł strony), zakladka (numer wybranej zakładki: 0 Yours, 1 Discover, domyślnie 1), sortuj (przycisk sortowania obok filtra), tresc (HTML), klasa (dodatkowa klasa tła). Lewa kolumna zależy od atrybutu data-konto-ustawien okna symulatora (pole `aplikacja.konto_ustawien`). */
PK.powlokaKatalogu = function (okno, o) {
  const { esc } = PK;
  const U = PK.USTAWIENIA;
  const I = PK.IKONY_KATALOGU;
  const pozycja = (p) =>
    `<li class="apl-kat-wiersz${p.napis === o.strona ? " wybrany" : ""}${p.zewnetrzna ? " apl-kat-zewn" : ""}"><span class="apl-kat-ikona">${I[p.ikona]}</span><span class="apl-kat-napis">${esc(p.napis)}</span>${p.zewnetrzna ? `<span class="apl-kat-ikona-zewn">${I.zewnetrzny}</span>` : ""}</li>`;
  const grupa = (g) => `<li class="apl-kat-grupa" aria-hidden="true">${esc(g.grupa)}</li>${g.pozycje.map(pozycja).join("")}`;
  const wybrana = o.zakladka === undefined ? 1 : o.zakladka; /* domyślnie Discover (przeglądarka wtyczek, katalog konektorów); strona Connectors z listą „Yours” ma 0 */
  const zakladka = (z, i) => `<span class="apl-kat-zakladka${i === wybrana ? " wybrana" : ""}">${esc(z)}</span>`;
  const przycisk = (ikona) => `<span class="apl-kat-ikona-nar">${I[ikona]}</span>`;
  okno.insertAdjacentHTML(
    "beforeend",
    `<div class="apl-katalog-tlo${o.klasa ? " " + o.klasa : ""}" hidden><div class="apl-katalog" role="dialog" aria-label="${esc(o.opis)}">` +
      `<div class="apl-kat-gora"><span class="apl-kat-tytul">${esc(U.tytul)}</span><button type="button" class="apl-kat-x" aria-disabled="true" aria-label="${esc(o.zamknij)}">${I.x}</button></div>` +
      `<nav class="apl-kat-bok" aria-hidden="true"><div class="apl-kat-szukaj apl-kat-szukaj-bok">${PK.IKONY_APLIKACJI.szukaj}<span>${esc(U.szukaj)}</span></div><ul>${PK.kolumnaUstawien(okno.dataset.kontoUstawien).map(grupa).join("")}</ul></nav>` +
      `<div class="apl-kat-tresc"><div class="apl-kat-naglowek"><h3 class="apl-kat-h">${esc(o.strona)}</h3><div class="apl-kat-zakladki">${U.zakladki.map(zakladka).join("")}</div>` +
      `<div class="apl-kat-narzedzia"><div class="apl-kat-szukaj">${PK.IKONY_APLIKACJI.szukaj}<span>${esc(U.szukaj)}</span></div>${przycisk("filtr")}${o.sortuj ? przycisk("sortuj") : ""}<span class="apl-kat-dodaj">${I.plus}<span>${esc(U.dodaj)}</span>${I.rozwin}</span></div></div>` +
      `<div class="apl-kat-strona">${o.tresc}</div></div></div></div>`,
  );
  const tlo = okno.lastElementChild;
  const pokaz = (otwarte) => {
    tlo.hidden = !otwarte;
    okno.classList.toggle("katalog-otwarty", otwarte);
  };
  return { tlo, zawartosc: tlo.querySelector(".apl-kat-strona"), pokaz };
};
