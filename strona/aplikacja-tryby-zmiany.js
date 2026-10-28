/* Symulator aplikacji Claude, tryby: skutki etapów w plikach, czyli licznik +N -M na karcie Changes, widok zmian i podgląd folderu pod oknem ze znacznikami zmian (grę prowadzi strona/aplikacja-tryby.js). */

/* Skutek etapów na podgląd folderu: zatwierdzona karta i krok zmiana dają kartom znacznik zmiany z liczbami z linijek, krok folder zmienia sam folder (czyta i nowy idą przez zmiana(), reszta wprost przez PK.Folder). */
PK.folderEtapow = (podglad) => ({
  oznacz: (pliki) =>
    pliki.forEach((p) =>
      podglad.zmiana({ akcja: "zmieniony", plik: p.plik, ...PK.licznikZmian([p]) }),
    ),
  krok(k) {
    const f = podglad.folder;
    if (k.akcja === "czyta" || k.akcja === "nowy") podglad.zmiana(k);
    else if (k.akcja === "zmien") f.zmien(k.plik, k.nazwa);
    else if (k.akcja === "usun") f.usun(k.plik);
    else if (k.akcja === "utworz") f.utworz(k.nazwa);
    else if (k.akcja === "przenies") f.przenies(k.plik, k.do, k.uwaga);
  },
});

/* Zmiany w plikach jednego ćwiczenia z etapami (`drogi`: lista dróg albo null); zwraca {krokFolderu(k), pokaz(pliki), otworz(), otwarte(), jest(), zeruj()}. */
PK.zmianyEtapow = (sek, cw, drogi) => {
  const apl = cw.aplikacja || {};
  const okno = sek.querySelector(".apl-okno");
  const licznik = sek.querySelector(".apl-licznik");
  const widok = sek.querySelector(".apl-widok-zmian");
  const changes = sek.querySelector('[data-pasek="changes"]');

  /* Podgląd folderu pod oknem (D-2026-10-23-10, strona/aplikacja-folder.js): tylko gdy scenariusz ma folder_startowy. */
  const zrodlo = document.getElementById("scenariusz");
  const start = (zrodlo && JSON.parse(zrodlo.textContent).folder_startowy) || [];
  const kontener = document.createElement("div");
  if (start.length) okno.after(kontener);
  const podglad = start.length
    ? PK.folderAplikacji.pokaz(kontener, { nazwa: apl.folder, pliki: start })
    : null;
  const folder = podglad && PK.folderEtapow(podglad);
  if (drogi) PK.podgladyDrog(cw, drogi, apl.folder, start);

  let zmiany = null; /* zmiana w plikach (zatwierdzona karta albo krok zmiana): lista {plik, linijki} */
  return {
    krokFolderu: (k) => podglad && folder.krok(k),
    /* Licznik +N -M na karcie Changes i pliki w widoku zmian; ten sam skutek ma zatwierdzona karta i krok zmiana. */
    pokaz(pliki) {
      zmiany = pliki;
      const l = PK.licznikZmian(pliki);
      licznik.innerHTML = `<span class="apl-plus">+${l.dodane}</span> <span class="apl-minus">-${l.usuniete}</span>`;
      licznik.hidden = false;
      widok.innerHTML = pliki.map((p) => PK.plikZgody(p.plik, p.linijki)).join("");
      if (podglad) folder.oznacz(pliki);
    },
    otworz() {
      widok.hidden = false;
      okno.classList.add("zmiany-otwarte");
      changes.classList.add("wlaczony");
    },
    otwarte: () => !widok.hidden,
    jest: () => !!zmiany,
    zeruj() {
      zmiany = null;
      licznik.hidden = true;
      licznik.innerHTML = "";
      widok.hidden = true;
      widok.innerHTML = "";
      okno.classList.remove("zmiany-otwarte");
      if (podglad) podglad.zmiana({ akcja: "od-nowa" });
    },
  };
};
