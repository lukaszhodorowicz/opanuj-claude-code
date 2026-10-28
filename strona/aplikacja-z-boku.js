/* Symulator aplikacji Claude, pytanie z boku (`/btw`): panel obok rozmowy w miejscu otwartego pliku (nagłówek z szarym paskiem bez napisu i ikoną ✕, dymek kursanta po prawej, odpowiedź Claude po lewej, pole na dole bez tekstu zastępczego), krok `z_boku` (pytanie wpisane w pole panelu i odpowiedź) i zamknięcie krzyżykiem; rozmowa główna się nie zmienia. Układ ze zrzutów z sieci: materialy/zrzuty-aplikacji/pytanie-z-boku/. */

/* Polski opis krzyżyka dla czytnika ekranu (bez dymka title): dokumentacja nie podaje napisu przycisku. */
PK.OPIS_ZAMKNIECIA_Z_BOKU = "Zamknij pytanie z boku";
PK.PAUZA_ODPOWIEDZI_Z_BOKU_MS = 900; /* trzy kropki w panelu, zanim pojawi się odpowiedź */

PK.panelZBoku = () =>
  `<section class="apl-zboku"><header class="apl-zboku-glowa"><span class="apl-szkic apl-zboku-tytul"></span>` +
  `<button type="button" class="apl-zboku-zamknij" aria-label="${PK.esc(PK.OPIS_ZAMKNIECIA_Z_BOKU)}">${PK.IKONY_ZGODY.nie}</button></header>` +
  `<div class="apl-zboku-rozmowa"></div>` +
  `<div class="apl-pole apl-zboku-pole"><span class="apl-pole-tekst"></span><span class="apl-pole-wyslij">${PK.IKONY_APLIKACJI.wyslij}</span></div></section>`;

/* Panel w miejscu otwartego pliku: `widok` to `.apl-widok-pliku` okna `okno`. Zwraca {otworz, zamknij, pytanie}; krzyżyk zamyka panel o każdej porze. `pytanie(k, przerwano)` gra krok `z_boku`: pytanie wpisuje się w pole panelu i staje dymkiem po prawej, potem trzy kropki i odpowiedź po lewej. */
PK.zBokuCwiczenia = function (okno, widok) {
  const zamknij = () => {
    widok.hidden = true;
    widok.innerHTML = "";
    okno.classList.remove("plik-otwarty");
  };
  widok.addEventListener("click", (e) => {
    if (e.target.closest(".apl-zboku-zamknij")) zamknij();
  });
  return {
    otworz() {
      widok.innerHTML = PK.panelZBoku();
      widok.hidden = false;
      okno.classList.add("plik-otwarty");
    },
    zamknij,
    async pytanie(k, przerwano) {
      const panel = widok.querySelector(".apl-zboku");
      if (!panel) return; /* kursant zamknął panel krzyżykiem, zanim krok się zaczął */
      const rozmowa = panel.querySelector(".apl-zboku-rozmowa");
      if (!(await PK.wpiszWPole(panel.querySelector(".apl-pole-tekst"), k.pytanie, przerwano))) return;
      rozmowa.insertAdjacentHTML("beforeend", PK.dymekAplikacji({ kto: "ty", tekst: k.pytanie }));
      rozmowa.insertAdjacentHTML("beforeend", '<div class="apl-mysli" aria-hidden="true"><i></i><i></i><i></i></div>');
      await PK.czekaj(PK.PAUZA_ODPOWIEDZI_Z_BOKU_MS);
      if (przerwano()) return;
      rozmowa.querySelector(".apl-mysli").remove();
      rozmowa.insertAdjacentHTML("beforeend", PK.dymekAplikacji({ kto: "claude", tekst: k.odpowiedz }));
    },
  };
};
