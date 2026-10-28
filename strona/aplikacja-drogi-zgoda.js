/* Symulator aplikacji Claude, drogi: karta zgody na zapis w folderze chronionym `.claude` albo na polecenie terminala (same ikony, bez nazwy pliku, bez treści polecenia i bez podglądu linijek) i znacznik „kliknij tutaj” kroku `klik` (ścieżka, link, ptaszek karty, nagłówek karty Context albo krzyżyk panelu pytania z boku). */

/* Karta w rozmowie pod odpowiedzią Claude: te same dwa przyciski co w ćwiczeniu z etapami (PK.IKONY_ZGODY, PK.OPISY_ZGODY), w tej samej ramce, ale bez nagłówka z nazwą pliku i bez linijek; krzyżyk wyszarzony, bez skutku. Krok z `polecenie` ma ten sam wygląd i własne opisy dla czytnika ekranu; krok z `odliczanie_ms` zaczyna z ptaszkiem nieaktywnym (aria-disabled), który zdejmuje dopiero PK.odliczanieZgody. */
PK.kartaZgodyChroniona = (k) => {
  const O = PK.OPISY_ZGODY;
  const I = PK.IKONY_ZGODY;
  const polecenie = !!(k && k.polecenie);
  const wstrzymany = k && k.odliczanie_ms ? ' aria-disabled="true"' : "";
  return (
    `<div class="apl-zgoda apl-zgoda-chroniona${polecenie ? " apl-zgoda-polecenie" : ""}"><section class="apl-plik"><div class="apl-zgoda-przyciski">` +
    `<button type="button" class="apl-zgoda-nie" aria-disabled="true" aria-label="${PK.esc(polecenie ? O.nie_polecenie : O.nie)}">${I.nie}</button>` +
    `<button type="button" class="apl-zgoda-tak"${wstrzymany} aria-label="${PK.esc(polecenie ? O.tak_polecenie : O.tak)}">${I.tak}</button>` +
    `</div></section></div>`
  );
};

/* Element, za którym stoi rząd ze znacznikiem „kliknij tutaj” (pod nim): karta zgody (ptaszek `zatwierdz`), karta Context (`context`) i nagłówek panelu pytania z boku (`zamknij-z-boku`); ścieżka i link dostają znacznik w odpowiedzi. */
PK.PO_CELU_KROKU = { zatwierdz: ".apl-plik", context: ".apl-karta", "zamknij-z-boku": ".apl-zboku-glowa" };

/* Znacznik „kliknij tutaj” kroku `klik` drogi na elemencie `el` (el = null zdejmuje wszystkie): ptaszek, nagłówek karty Context i krzyżyk panelu pytania z boku dostają rząd ze znacznikiem (PK.celPod), ścieżka i link znacznik w odpowiedzi (PK.celAplikacji). */
PK.celKroku = (sek, cel, el) =>
  PK.PO_CELU_KROKU[cel] || !el
    ? PK.celPod(sek, el, el && el.closest(PK.PO_CELU_KROKU[cel]))
    : PK.celAplikacji(sek, el);
