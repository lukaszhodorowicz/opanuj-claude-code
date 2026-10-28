/* Symulator aplikacji Claude, pole wiadomości: tekst sam pojawia się w polu znak po znaku, jak pisze kursant, i znika po „wysłaniu”; używają go kroki drogi `pisz` (potem dymek w rozmowie), `komenda` (bez dymka) i `z_boku` (pole panelu pytania z boku). */

/* Wpisuje `tekst` w `pole` i czyści pole po wysłaniu. `przerwano()` mówi, że nowe polecenie albo „Od nowa” przerwało przebieg: wpisywanie kończy się wtedy bez czyszczenia (pole czyści ten, kto przerwał). Zwraca true, gdy tekst doszedł do końca i poszedł. Opcjonalne `zapisz(t)` zastępuje domyślne wpisanie `pole.textContent = t` (skill w polu dopisuje tekst po pasku skilla, strona/aplikacja-plus.js). */
PK.wpiszWPole = async (pole, tekst, przerwano, zapisz = (t) => (pole.textContent = t)) => {
  pole.classList.add("pisze");
  for (let i = 1; i <= tekst.length; i += 2) {
    zapisz(tekst.slice(0, i));
    await PK.czekaj(22);
    if (przerwano()) return false;
  }
  zapisz(tekst);
  await PK.czekaj(350);
  if (przerwano()) return false;
  pole.textContent = "";
  pole.classList.remove("pisze");
  return true;
};
