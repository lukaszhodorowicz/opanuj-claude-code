/* Podgląd folderu w ćwiczeniu aplikacji z krokami albo drogami: stan startowy ze scenariusza i zmiany wyprowadzone z kroków drogi (czytane pliki z prośby i odpowiedzi albo z pól `czyta_na_start` i `czyta`, nowy plik z pola `plik` odpowiedzi). */

/* Nazwy z listy `pliki`, które padają w tekście jako osobne słowo (także po @); „cennik.txt” nie trafia w „stary-cennik.txt” ani w „Podfolder/cennik.txt”. */
PK.wymienionePliki = (tekst, pliki) =>
  (pliki || []).filter((p) => {
    const nazwa = p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    /* bez lookbehind (Safari przed 16.4 go nie zna): znak przed nazwą łapie grupa (^|…) */
    return new RegExp(
      `(^|[^\\p{L}\\p{N}_./-])${nazwa}(?![\\p{L}\\p{N}_-]|\\.[\\p{L}\\p{N}])`,
      "u",
    ).test(tekst || "");
  });

/* Rysuje podgląd pod oknem `.apl-okno` ćwiczenia; bez `folder_startowy` w scenariuszu zwraca null; pliki startowe to `folder_startowy` i `aplikacja.folder_startowy_dodatkowe` ćwiczenia.
   Ścieżki: pola widoczne dla kursanta (`claude.plik`, nazwy w tekstach, `nowe_pliki`) liczą się od folderu rozmowy (`aplikacja.folder`), a `czyta_na_start` i `czyta` od korzenia podglądu (`folder_glowny`). Przy folderze każdej rozmowy (`aplikacja.sesje[].folder`) folder rozmowy zmienia się w drodze (uchwyt `zrodlo` podaje folder otwartej rozmowy), a `nowe_pliki` to ścieżki od korzenia. */
PK.folderCwiczenia = function (cw, sek) {
  const zrodlo = document.getElementById("scenariusz");
  const scen = zrodlo ? JSON.parse(zrodlo.textContent) : {};
  const wspolne = scen.folder_startowy || [];
  const glowny = scen.folder_glowny || "";
  const okno = sek.querySelector(".apl-okno");
  if (!wspolne.length || !okno) return null;
  const apl = cw.aplikacja || {};
  /* `folder_startowy_dodatkowe`: pliki, które tylko w tym ćwiczeniu leżą w folderze od startu (zwykłe karty, bez znacznika „nowy”) */
  const start = [...wspolne, ...(apl.folder_startowy_dodatkowe || [])];
  /* korzeń podglądu: `folder_glowny` (rozmowa w korzeniu albo w jednej z teczek) albo, jak dotąd, sam folder rozmowy */
  const przedrostekStartowy = glowny && apl.folder !== glowny ? apl.folder + "/" : "";
  const wieleFolderow = PK.folderyRozmow(apl);
  const odTeczki = (teczka) => (glowny && teczka !== glowny ? teczka + "/" : "");
  let zrodloFolderu = null; /* funkcja podająca folder otwartej rozmowy (folder każdej rozmowy) */
  const przedrostek = () => (zrodloFolderu ? odTeczki(zrodloFolderu()) : przedrostekStartowy);
  const odKorzenia = (nazwa) => przedrostek() + nazwa;
  const nowe = (cw.nowe_pliki || []).map((n) => (wieleFolderow ? n : odKorzenia(n)));
  const wszystkie = [...start, ...nowe];
  /* które ścieżki (od korzenia) wymienia tekst; kursant i Claude nazywają pliki od folderu rozmowy, więc pliki spoza niego nie padają z nazwy */
  const wymienione = (tekst, sciezki, pre = przedrostek()) =>
    PK.wymienionePliki(
      tekst,
      sciezki.filter((p) => p.startsWith(pre)).map((p) => p.slice(pre.length)),
    ).map((n) => pre + n);
  const el = document.createElement("div");
  okno.after(el);
  const podglad = PK.folderAplikacji.pokaz(el, {
    nazwa: glowny || apl.folder,
    pliki: start,
    /* znacznik folderu rozmowy tylko z `folder_glowny`: "" = korzeń, nazwa = teczka */
    rozmowa: glowny ? (przedrostekStartowy ? apl.folder : "") : undefined,
    /* nowy plik, o którym mówi rozmowa ze scenariusza, Claude utworzył już przed ćwiczeniem */
    nowe: wymienione(
      (apl.rozmowa || []).map((w) => w.tekst).join("\n"),
      nowe,
      przedrostekStartowy,
    ),
    zmienione: (apl.zmiany || []).map((z) => ({
      plik: odKorzenia(z.plik),
      ...PK.licznikZmian([z]),
    })),
  });

  /* czy plik już leży w folderze: startowy albo dołożony wcześniej (stan podglądu, nie lista ze scenariusza) */
  const wFolderze = (p) =>
    [podglad.folder.luzem, ...Object.values(podglad.folder.foldery)].some((w) =>
      w.includes(p),
    );

  /* Krok drogi, zanim zagra: pierwszy krok drogi podświetla `czyta_na_start`; `mysli` podświetla ścieżki z pola `czyta` albo, bez niego, pliki z prośby przed nim i z odpowiedzi po nim; `claude` z polem `plik` dokłada kartę nowego pliku albo, gdy plik już leży w folderze, daje mu znacznik zmiany bez liczb (z `bez_zmiany: true` nie daje: Claude plik tylko wymienia). */
  function krok(k, kroki) {
    const i = kroki.indexOf(k);
    if (i === 0 && apl.czyta_na_start)
      podglad.zmiana({
        akcja: "czyta",
        pliki: apl.czyta_na_start,
        poczatek: true,
      });
    if (k.typ === "mysli") {
      const prosba = kroki
        .slice(0, i)
        .reverse()
        .find((x) => x.typ === "pisz");
      const dalej = kroki.slice(i + 1);
      const koniec = dalej.findIndex((x) => x.typ === "pisz");
      const odp = (koniec < 0 ? dalej : dalej.slice(0, koniec)).find(
        (x) => x.typ === "claude",
      );
      const tekst = `${(prosba && prosba.tekst) || ""}\n${(odp && odp.tekst) || ""}`;
      podglad.zmiana({
        akcja: "czyta",
        pliki: k.czyta || wymienione(tekst, wszystkie),
        zastap: !!k.czyta,
      });
    }
    if (k.typ === "claude" && k.plik) {
      const p = odKorzenia(k.plik);
      if (wFolderze(p)) {
        if (k.bez_zmiany !== true)
          podglad.zmiana({ akcja: "zmieniony", plik: p });
      } else if (nowe.includes(p)) podglad.zmiana({ akcja: "nowy", plik: p });
    }
  }

  return {
    krok,
    reset: () => podglad.zmiana({ akcja: "od-nowa" }),
    /* znacznik folderu rozmowy przechodzi na teczkę (albo na korzeń, gdy to `folder_glowny`) otwartej rozmowy */
    rozmowa: (teczka) => glowny && podglad.zmiana({ akcja: "rozmowa", teczka: teczka === glowny ? "" : teczka }),
    zrodlo: (fn) => (zrodloFolderu = fn),
  };
};
