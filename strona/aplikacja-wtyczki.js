/* Symulator aplikacji Claude, przeglądarka wtyczek: okno Settings → Plugins, zakładka Discover (strona/aplikacja-ustawienia.js; pozycja „Browse plugins” podmenu Plugins je otwiera) z kartą polecaną i kafelkami „New plugins”, napisy ze zrzutów Łukasza (strona/aplikacja-ustawienia-dane.js); okno nie reaguje na kliknięcia, droga kończy się otwartą przeglądarką (część „Menu + i przeglądarka wtyczek” w dane/FORMAT-SCENARIUSZA.md). */

/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_WTYCZEK = {
  okno: "Ustawienia, przeglądarka wtyczek (w ćwiczeniu bez skutku na kliknięcia)",
  zamknij: "Zamknij okno (w ćwiczeniu bez skutku)",
  karta: "Karta wtyczki (w ćwiczeniu bez skutku)",
  rysunek: "Rysunek karty polecanej",
};

/* Przeglądarka wtyczek w ćwiczeniu z drogami, które mają krok `klik` z celem `pozycja` i `na: "Browse plugins"`; null, gdy żadna droga go nie ma (reszta ćwiczeń zostaje bez zmian). Okno zostaje otwarte do końca drogi (bez kroku zamykającego); „Od nowa” i nowe polecenie je zamykają. Zwraca {otwiera, otworz, reset}. */
PK.wtyczkiAplikacji = function (cw, sek, okno) {
  const { esc, szkic } = PK;
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const otwiera = (k) => k.typ === "klik" && k.cel === "pozycja" && k.na === "Browse plugins";
  if (!kroki.some(otwiera)) return null;
  const I = PK.IKONY_KATALOGU;
  const O = PK.OPISY_WTYCZEK;

  /* karta polecana: napis „From Anthropic”, nazwa, opis, przycisk Add i prosty rysunek tabeli (rysunku ze zrzutu nie kopiujemy) */
  const polecana = () => {
    const P = PK.WTYCZKI_POLECANA;
    return (
      `<div class="apl-wt-polecana"><div class="apl-wt-polecana-tekst"><span class="apl-wt-od">${esc(P.od)}</span><b class="apl-wt-polecana-nazwa">${esc(P.nazwa)}</b><span class="apl-wt-polecana-opis">${esc(P.opis)}</span><span class="apl-wt-przycisk">${esc(P.przycisk)}</span></div>` +
      `<svg class="apl-wt-rysunek" viewBox="0 0 120 90" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="${esc(O.rysunek)}"><rect x="8" y="8" width="84" height="64" rx="4"/><path d="M8 29h84M8 50h84M36 8v64M64 8v64"/><circle cx="82" cy="62" r="19" fill="#2c5f55"/><path d="m71 66 8-8 6 5 8-9"/></svg></div>`
    );
  };
  /* kafelek: ikona, nazwa, opis i źródło (szare paski, gdy zrzut ich nie pokazuje), przycisk + bez skutku; cały kafelek bez skutku */
  const karta = (t) => {
    const opis = t.opis ? `<span class="apl-kaf-opis">${esc(t.opis)}</span>` : szkic(88) + szkic(58);
    const zrodlo = t.zrodlo ? `<span class="apl-kaf-autor">${esc(t.zrodlo)}</span>` : szkic(36);
    return (
      `<li><div class="apl-kafelek apl-wt-karta" role="group" aria-disabled="true" aria-label="${esc(O.karta)}"><span class="apl-kaf-ikona">${I[t.ikona]}</span>` +
      `<span class="apl-kaf-tekst"><b>${esc(t.nazwa)}</b>${opis}${zrodlo}</span><span class="apl-kaf-plus" aria-hidden="true">${I.plus}</span></div></li>`
    );
  };
  const tresc = () =>
    polecana() +
    `<div class="apl-kat-sekcja"><h4>${esc(PK.WTYCZKI_SEKCJA)}</h4><span class="apl-kat-wszystkie">${esc(PK.USTAWIENIA.wszystkie)}${I.dalej}</span></div>` +
    `<ul class="apl-kat-siatka apl-wt-siatka">${PK.WTYCZKI_KAFELKI.map(karta).join("")}</ul>`;

  const { zawartosc, pokaz } = PK.powlokaKatalogu(okno, { opis: O.okno, zamknij: O.zamknij, strona: "Plugins", sortuj: true, tresc: tresc(), klasa: "apl-wt-tlo" });

  return {
    otwiera,
    /* Pozycja „Browse plugins” już zamknęła menu: pokazuje okno z kartami. */
    otworz() {
      zawartosc.innerHTML = tresc();
      pokaz(true);
    },
    /* „Od nowa” i nowe polecenie: okno zamknięte. */
    reset() {
      pokaz(false);
    },
  };
};
