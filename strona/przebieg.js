/* Odtwarzanie kroków przebiegu ze scenariusza w oknie terminala (pisanie, kolejka, narzędzia i ich późniejsze wyniki, menu z gałęziami, folder, pasek trybu). */
/* Typ następnego kroku z pominięciem wypowiedzi nauczyciela, bo ta nie przerywa pracy w terminalu. */
PK.nastepnyTyp = function (kroki, i) {
  for (let j = i + 1; j < kroki.length; j++)
    if (!kroki[j] || kroki[j].typ !== "nauczyciel")
      return kroki[j] ? kroki[j].typ : null;
  return null;
};
/* ctx: {t: terminal, f: folder, g: numer pokolenia terminala, n: funkcja ustawiająca tekst nauczyciela}. */
PK.graj = async function graj(ctx, kroki) {
  const { t, f, g, n } = ctx;
  const lista = kroki || [];
  for (let i = 0; i < lista.length; i++) {
    const k = lista[i];
    if (g !== t.gen) return;
    /* wskaźnik pracy świeci bez przerwy między „mysli” a „kolejka” stojącymi obok siebie */
    const dalej = PK.nastepnyTyp(lista, i);
    switch (k.typ) {
      case "pisz":
        if (!(await t.pisz(k.tekst, g))) return;
        break;
      case "kolejka":
        if (
          !(await t.kolejka(
            k.tekst,
            g,
            dalej === "mysli" || dalej === "kolejka",
          ))
        )
          return;
        break;
      case "mysli":
        if (!(await t.kreci(k.ms, g, dalej === "kolejka"))) return;
        break;
      case "claude":
        t.claude(k.tekst);
        break;
      case "narzedzie":
        t.narzedzie(k.nazwa, k.arg, k.wynik, k.zmiana);
        if (k.nazwa === "Read") f.czytaj(k.arg);
        break;
      case "wynik":
        t.wynik(k.wynik);
        break;
      case "folder":
        f.zastosuj(k);
        break;
      case "tryb":
        t.ustawTryb(k.na, true);
        break;
      case "nauczyciel":
        n(k.tekst);
        break;
      case "czekaj":
        await PK.czekaj(k.ms);
        break;
      case "menu": {
        const wybor = await new Promise((ok) => t.menu(k, ok));
        if (g !== t.gen) return;
        await graj(ctx, k.opcje[wybor].dalej);
        return; /* dalszą część przebiegu niesie wybrana gałąź */
      }
    }
  }
};
