/* Symulator aplikacji Claude, panel Browser: rysuje stronę oferty z pola `strona` kroku `plik` albo `strona` (szary pasek z jedną kartą bez napisu, pod nim jasna strona, z ramkami `pola` w kroku `strona`) i wybiera, czy otwarty plik to strona, czy linijki. */

/* Strona oferty (jasne tło, typografia kursu); wszystkie napisy idą ze scenariusza, strona nie dodaje własnych (ani nagłówków, ani przycisków, ani odnośników). Wspólny rysunek panelu Browser i widoku artefaktu. */
PK.stronaOferty = (s) => {
  const { esc } = PK;
  const punkt = (t) => `<li>${esc(t)}</li>`;
  const opinia = (t) => `<blockquote><p>${esc(t)}</p></blockquote>`;
  return (
    '<div class="apl-prz-strona">' +
    `<p class="apl-prz-tytul">${esc(s.tytul)}</p>` +
    `<p class="apl-prz-opis">${esc(s.opis)}</p>` +
    `<ul class="apl-prz-program">${(s.program || []).map(punkt).join("")}</ul>` +
    `<p class="apl-prz-cena">${esc(s.cena)}</p>` +
    `<div class="apl-prz-opinie">${(s.opinie || []).map(opinia).join("")}</div>` +
    `<p class="apl-prz-kontakt">${esc(s.kontakt)}</p>` +
    PK.polaStrony(s.pola) +
    "</div>"
  );
};

/* Ramki pól (tylko w kroku `strona`, pole `pola`): etykieta nad ramką, w ramce tekst `wartosc` (pusta wartość to pusta ramka). To div-y, nie pola formularza: nic nie da się w nich wpisać ani kliknąć, strona nie ma przycisku wysyłania. */
PK.polaStrony = (pola) => {
  if (!pola || !pola.length) return "";
  const { esc } = PK;
  const ramka = (p) => `<div class="apl-prz-pole"><span class="apl-prz-etykieta">${esc(p.etykieta)}</span><div class="apl-prz-ramka">${esc(p.wartosc)}</div></div>`;
  return `<div class="apl-prz-pola">${pola.map(ramka).join("")}</div>`;
};

/* Panel Browser ze stroną oferty: szary pasek z jedną kartą bez napisu, pod nim strona. */
PK.przegladarkaAplikacji = (s) =>
  '<section class="apl-przegladarka">' +
  '<div class="apl-prz-pasek" aria-hidden="true"><span class="apl-prz-karta"></span></div>' +
  PK.stronaOferty(s) +
  "</section>";

/* To, co pokazuje krok `plik` drogi (w oknie i w podglądzie w tekście lekcji): strona oferty, gdy krok ma pole `strona`, inaczej linijki pliku. */
PK.plikLubStrona = (k) =>
  k.strona ? PK.przegladarkaAplikacji(k.strona) : PK.plikAplikacji(k.nazwa, k.linijki);
