/* Symulator aplikacji Claude, drogi: podgląd końca drogi w tekście lekcji (znacznik `<!-- podglad: ćwiczenie droga -->`): otwarty plik, widok artefaktu albo cudza strona z ostatniego takiego kroku drogi, a gdy ostatni jest klik w pasku bocznym z rozmowami (sesja, archive, archived), okno z listą rozmów w stanie końca drogi (strona/aplikacja-sesje-gra.js). */

/* Ostatni krok `plik`, `artefakt`, `strona` albo klik `sesja`, `archive`, `archived` drogi: to, co pokazuje podgląd w tekście lekcji. */
PK.koniecDrogi = (droga) =>
  [...((droga && droga.kroki) || [])]
    .reverse()
    .find((k) => k.typ === "plik" || k.typ === "artefakt" || k.typ === "strona" || (k.typ === "klik" && PK.CELE_PODGLADU_SESJI.includes(k.cel)));

/* Okno aplikacji ćwiczenia `cw` po wszystkich krokach drogi, bez pola wiadomości i rzędu pod nim: lista rozmów z tytułem albo widok listy rozmów. Okno budują te same funkcje co ćwiczenie, w oderwanym od strony HTML-u. Panel szczegółów jest w podglądzie schowany (klasa panel-ukryty, ta sama co po `+ New`): podgląd stoi zwykle w jednej z dwóch kolumn lekcji, a przy `aplikacja.kontekst` panel zabierał rozmowie szerokość do kilku liter (D-2026-10-27-51, usterka U1); podgląd pokazuje pasek boczny i rozmowę, nie panel. */
PK.sesjePodglad = (cw, droga) => {
  const szablon = document.createElement("template");
  szablon.innerHTML = PK.htmlAplikacji(cw, 0);
  const sek = szablon.content.firstElementChild;
  const rozmowa = sek.querySelector(".apl-rozmowa");
  const kontekst = PK.kontekstCwiczenia(cw, sek); /* karta Context w panelu pokazuje procent rozmowy otwartej na końcu drogi (null bez aplikacja.kontekst) */
  /* te same wywołania co w grze (strona/aplikacja.js): nowa rozmowa zeruje kartę, otwarta rozmowa daje jej procent, pierwsza prośba pokazuje panel, krok `kontekst` ustawia procent (bez klików w kartę: podgląd pokazuje kartę zamkniętą) */
  const doKarty = kontekst && { rozmowaOtwarta: (klucz, dane) => (klucz === "nowa" ? kontekst.nowaRozmowa() : kontekst.rozmowa(klucz, dane && dane.kontekst)), sesjaStartuje: kontekst.pokazPanel, kontekstUstawiony: kontekst.ustawCicho };
  PK.sesjeCwiczenia(cw, sek, { poczatek: rozmowa.innerHTML, zamknijPanel() {}, ...doKarty }).przewin(droga.kroki);
  const okno = sek.querySelector(".apl-okno");
  okno.classList.add("panel-ukryty");
  okno.querySelectorAll(".apl-pole, .apl-rzad").forEach((e) => e.remove());
  return okno.outerHTML;
};

/* Wypełnia podglądy ćwiczenia `cw` (miejsca `.podglad` z `data-t` równym id drogi); droga bez takiego kroku (np. z odmową Deny) zostaje bez podglądu, a składanie lekcji tego nie dopuszcza (narzedzia/strona_podglad.py). */
PK.podgladyDrogCwiczenia = (cw, drogi) => {
  document.querySelectorAll(`.podglad[data-cw="${cw.id}"]`).forEach((el) => {
    const droga = drogi.find((d) => d.id === el.dataset.t);
    const koniec = PK.koniecDrogi(droga);
    if (!koniec) return;
    el.classList.add("apl-podglad");
    el.innerHTML =
      koniec.typ === "klik"
        ? PK.sesjePodglad(cw, droga)
        : koniec.typ === "artefakt"
          ? PK.artefaktPodglad(cw, koniec, el.dataset.widok)
          : PK.plikLubStrona(koniec); /* plik z linijkami, strona oferty (krok plik z `strona`) albo cudza strona (krok strona) */
  });
};
