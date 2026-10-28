/* Symulator aplikacji Claude, drogi: odliczanie przed ptaszkiem karty zgody (pole `odliczanie_ms` kroku `zgoda`): pigułka kursu „Claude czeka: N s” w miejscu znacznika „kliknij tutaj”, malejąca co sekundę, i ptaszek nieaktywny do końca czasu. Element kursu, nie wygląd aplikacji. */

/* Napis pigułki; ten sam wzór wypisuje narzedzia/tekst_pl.py (tekst_odliczania). */
PK.tekstOdliczania = (sekundy) => `Claude czeka: ${sekundy} s`;

/* Odliczanie `ms` pod kartą `karta` w ćwiczeniu `sek`: pigułka stoi w rzędzie pod ptaszkiem (jak znacznik PK.celPod, ale bez strzałki i bez zakreślacza), ptaszek zachowuje aria-disabled do końca czasu. Zwraca {gotowe, przerwij}: `gotowe` rozwiązuje się na true po upływie czasu (pigułka znika, ptaszek jest aktywny) albo na false po `przerwij()` (przerwanie tylko zatrzymuje licznik czasu; kartę razem z pigułką zdejmuje „Od nowa”). */
PK.odliczanieZgody = (sek, karta, ms) => {
  const tak = karta.querySelector(".apl-zgoda-tak");
  PK.celPod(sek, tak, karta.querySelector(".apl-plik"));
  tak.classList.remove("apl-cel"); /* ptaszek nie jest jeszcze do kliknięcia: bez zakreślacza */
  const tag = karta.querySelector(".apl-tag-rzad .apl-tag");
  tag.classList.add("apl-odliczanie");
  let zostalo = Math.ceil(ms / 1000);
  let licznik = null;
  let zakoncz = null;
  const gotowe = new Promise((r) => (zakoncz = r));
  const pokaz = () => {
    tag.textContent = PK.tekstOdliczania(zostalo);
    tag._uloz(); /* napis zmienia szerokość: środek pigułki liczy się od nowa */
  };
  /* pierwsza sekunda trwa tyle, ile zostaje po pełnych sekundach (przy 6000 ms równo 1 s), dalej co 1 s */
  const tyk = (opoznienie) => {
    licznik = setTimeout(() => {
      zostalo--;
      if (zostalo > 0) {
        pokaz();
        return tyk(1000);
      }
      tak.removeAttribute("aria-disabled");
      tag.closest(".apl-tag-rzad").remove();
      zakoncz(true);
    }, opoznienie);
  };
  pokaz();
  tyk(ms - (zostalo - 1) * 1000);
  return {
    gotowe,
    przerwij: () => {
      clearTimeout(licznik);
      zakoncz(false);
    },
  };
};
