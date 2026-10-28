/* Symulator aplikacji Claude, karta wiadomości od innej rozmowy (pole `wiadomosc` kroku `claude`, klik `wiadomosc-od`): ramka w kolorach okna z nagłówkiem (tytuł rozmowy nadawcy i strzałka odnośnika po prawej, bez napisu) i tekstem wiadomości pod nim. Dokumentacja podaje tylko tytuł nadawcy i odnośnik do niego (fakt aplikacja-wiadomosc-karta-z-tytulem-nadawcy), więc ramka i miejsce na końcu rozmowy to umowa symulatora; żaden zrzut karty nie istnieje. Grę kroków prowadzi strona/aplikacja-sesje-gra.js. */

/* Polski opis strzałki dla czytnika ekranu (bez dymka): dokumentacja nie podaje napisu odnośnika. */
PK.OPIS_ODNOSNIKA_WIADOMOSCI = "Otwórz rozmowę, która wysłała wiadomość";

/* Karta: `od` to klucz rozmowy nadawcy (start albo id wiersza), `tytul` jej nazwa, `tekst` treść wiadomości (dane scenariusza). */
PK.kartaWiadomosci = ({ od, tytul, tekst }) =>
  `<div class="apl-wiadomosc" data-od="${PK.esc(od)}"><header><b>${PK.esc(tytul)}</b>` +
  `<button type="button" class="apl-wiad-wr" aria-label="${PK.esc(PK.OPIS_ODNOSNIKA_WIADOMOSCI)}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg></button></header>` +
  `<p>${PK.esc(tekst)}</p></div>`;

/* Znacznik pod kartą (rząd w rozmowie, strzałka na przycisk). */
Object.assign(PK.PO_CELU_KROKU, { "wiadomosc-od": ".apl-wiadomosc" });
