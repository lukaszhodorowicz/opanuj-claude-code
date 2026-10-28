/* Symulator aplikacji Claude, drogi etapów: polecenia dróg nad oknem, dalsze etapy wybranej drogi pod nimi i podgląd folderu po końcu drogi w tekście lekcji (ćwiczenie z listą etapy złożoną z dróg; grę prowadzi strona/aplikacja-tryby.js). */

/* Lista dróg ćwiczenia (pozycje `etapy` z własną listą `etapy`) albo null, gdy `etapy` to zwykłe etapy. */
PK.drogiEtapow = (cw) => {
  const e = cw.etapy;
  return Array.isArray(e) &&
    e.length &&
    e.every((d) => d && Array.isArray(d.etapy))
    ? e
    : null;
};

/* Polecenia dróg nad oknem; klik w polecenie zeruje okno i gra drogę od pierwszego etapu. */
PK.poleceniaDrog = (drogi) =>
  drogi.map((d, i) => PK.polecenieEtapu(d, i, "d")).join("");

/* Rysuje pod poleceniami dróg dalsze etapy drogi `i`, od drugiego (pierwszy gra się po kliknięciu drogi; i < 0 czyści); zwraca etapy tej drogi albo []. */
PK.ustawDroge = (sek, drogi, i) => {
  let dalej = sek.querySelector(".polecenia-etapy");
  if (!dalej) {
    dalej = document.createElement("div");
    dalej.className = "polecenia polecenia-etapy";
    sek.querySelector(".polecenia").after(dalej);
  }
  const droga = drogi[i];
  dalej.hidden = !droga || droga.etapy.length < 2;
  dalej.innerHTML = dalej.hidden
    ? ""
    : `<p class="polecenia-naglowek">Dalej w drodze „${PK.esc(droga.etykieta)}”</p>` +
      droga.etapy.map((e, j) => (j ? PK.polecenieEtapu(e, j, "e") : "")).join("");
  return droga ? droga.etapy : [];
};

/* Polecenia dróg po kolei: w czasie gry (`trwa`: gra się etap albo droga czeka na dalsze etapy) żadne nie jest aktywne; poza grą aktywna jest tylko pierwsza nieukończona droga, a po ukończeniu wszystkich każda (powtórka); `wyslane` mają ukończone i bieżąca. */
PK.stanDrog = (sek, ukonczone, biezaca, trwa) => {
  const przyciski = [...sek.querySelectorAll(".polecenie[data-d]")];
  const pierwsza = przyciski.findIndex((_, j) => !ukonczone.has(j));
  przyciski.forEach((b, j) => {
    b.disabled = trwa || (pierwsza >= 0 && j !== pierwsza);
    b.classList.toggle("wyslane", ukonczone.has(j) || j === biezaca);
  });
};

/* Podglądy `<!-- podglad: <ćwiczenie> <id drogi> -->` w tekście lekcji: stan folderu pod oknem po końcu drogi (karta zgody liczy się dopiero po zatwierdzeniu, krok czyta nic nie zmienia). */
PK.podgladyDrog = (cw, drogi, nazwa, start) => {
  if (!start.length) return;
  document.querySelectorAll(`.podglad[data-cw="${cw.id}"]`).forEach((el) => {
    const droga = drogi.find((d) => d.id === el.dataset.t);
    if (!droga) return;
    const folder = PK.folderEtapow(
      PK.folderAplikacji.pokaz(el, { nazwa, pliki: start }),
    );
    let karta = null; /* karta zgody, która czeka na zatwierdzenie */
    droga.etapy.forEach((e) => {
      if (e.klik === "zatwierdz" && karta) folder.oznacz([karta]);
      if (e.klik === "zatwierdz") karta = null;
      (e.kroki || []).forEach((k) => {
        if (k.typ === "zgoda") karta = { plik: k.plik, linijki: k.linijki };
        else if (k.typ === "zmiana") folder.oznacz(k.pliki);
        else if (k.typ === "folder" && k.akcja !== "czyta") folder.krok(k);
      });
    });
    /* stan końcowy stoi od razu: bez wpadania nowych kart */
    el.querySelectorAll(".apl-pojawia").forEach((k) =>
      k.classList.remove("apl-pojawia"),
    );
  });
};
