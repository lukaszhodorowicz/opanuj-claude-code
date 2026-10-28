/* Symulator aplikacji Claude, tryby: przełącznik trybu w rzędzie pod polem wiadomości, menu trybów otwierane jego kliknięciem i etapy ćwiczenia z kartą zgody, ze zmianą bez karty albo ze zmianą w folderze i z kartą planu (rodzaj aplikacja z listą etapy albo z drogami etapów; części: strona/aplikacja-tryby-drogi.js, aplikacja-tryby-zmiany.js, aplikacja-plan.js). */

/* Napisy pozycji menu w kolejności listy trybów ze zrzutu Łukasza 27.10.2026 (plik 04-41-10: Auto, Manual, Accept edits, Plan; Bypass permissions dopiero po włączeniu na koncie, strona/aplikacja-tryby-menu.js); test sprawdza je w dane/napisy-interfejsu.yaml. */
PK.TRYBY_APLIKACJI = ["Auto", "Manual", "Accept edits", "Plan"];

/* Polecenie nad oknem: przycisk z ikoną, etykietą i opisem; `atr` to atrybut z numerem (e: etap, d: droga). */
PK.polecenieEtapu = (e, i, atr) =>
  `<button class="polecenie" data-${atr}="${i}"><span class="polecenie-ikona"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg></span>` +
  `<span class="polecenie-tekst"><b>${PK.esc(e.etykieta || "")}</b>${e.opis ? `<small>${PK.esc(e.opis)}</small>` : ""}</span></button>`;

PK.trybyAplikacji = function (cw, sek) {
  const { czekaj } = PK;
  const apl = cw.aplikacja || {};
  const drogi = PK.drogiEtapow && PK.drogiEtapow(cw); /* lista dróg albo null */
  let etapy = drogi ? [] : cw.etapy || []; /* przy drogach: etapy wybranej drogi */
  const okno = sek.querySelector(".apl-okno");
  const rozmowa = sek.querySelector(".apl-rozmowa");
  const pole = sek.querySelector(".apl-pole-tekst");
  const rzad = sek.querySelector(".apl-rzad");
  const licznik = sek.querySelector(".apl-licznik");
  const mow = PK.Nauczyciel(sek.querySelector(".nauczyciel"), []);
  const poczatek = rozmowa.innerHTML;

  /* licznik, widok zmian i podgląd folderu pod oknem: strona/aplikacja-tryby-zmiany.js */
  const zm = PK.zmianyEtapow(sek, cw, drogi);

  /* przełącznik trybu: ten sam napis co w oknie, ale klikalny; menu rysuje się nad nim */
  const przel = document.createElement("button");
  przel.type = "button";
  przel.className = "apl-chip apl-tryb apl-przelacznik";
  przel.setAttribute("aria-haspopup", "menu");
  sek.querySelector(".apl-tryb").replaceWith(przel);
  rzad.classList.add("apl-rzad-tryby");
  rzad.insertAdjacentHTML(
    "beforeend",
    PK.menuTrybow(apl.auto_dostepny !== false, apl.bypass_dostepny === true),
  );
  const menu = rzad.querySelector(".apl-menu-trybow");

  sek.querySelector(".polecenia").innerHTML = drogi
    ? PK.poleceniaDrog(drogi)
    : etapy.map((e, i) => PK.polecenieEtapu(e, i, "e")).join("");

  let zrobione = 0;
  let zajety = false;
  let gen = 0; /* „Od nowa” przerywa trwający etap */
  let karta = null; /* karta zgody, która czeka na decyzję */
  let biezaca = -1; /* numer wybranej drogi */
  let uspione = false; /* menu trybów zamknął pierścień zużycia, gdy etap czekał na jego pozycję: przełącznik otwiera je z powrotem */
  const ukonczone = new Set(); /* drogi doprowadzone do końca */

  /* menu przy przełączniku, ale nie poza rzędem pod polem wiadomości */
  const ulozMenu = () => {
    if (menu.hidden) return;
    const wolne = rzad.clientWidth - menu.offsetWidth;
    menu.style.left = Math.max(0, Math.min(przel.offsetLeft, wolne)) + "px";
  };
  /* po zmianie rozmiaru najpierw menu, potem znacznik (także ten pod pozycją menu) */
  const ulozWszystko = () => {
    ulozMenu();
    sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
  };
  window.addEventListener("resize", ulozWszystko);

  const elementEtapu = (e) => {
    if (!e || !e.klik) return null;
    if (e.klik === "zatwierdz")
      return karta && karta.querySelector(".apl-zgoda-tak");
    if (e.klik === "przelacznik") return przel;
    if (e.klik === "licznik") return licznik;
    if (e.klik === "tryb")
      return [...menu.querySelectorAll(".apl-menu-poz")].find(
        (b) => b.dataset.tryb === e.na,
      );
    return null;
  };
  /* karta planu, która czeka na decyzję, kończy etapy: znacznik stawia ona (strona/aplikacja-plan.js) */
  /* widok zmian otwarty wcześniej (klik w liczby w trakcie gry) odbiera etapowi „licznik” znacznik: nie ma już czego klikać */
  const ustawCel = (e = etapy[zrobione]) =>
    plan.czeka()
      ? plan.ustawCel()
      : e && e.klik === "licznik" && zm.otwarte()
        ? PK.celEtapu(sek, null, null, rzad)
        : uspione && e && e.klik === "tryb"
          ? PK.celEtapu(sek, { klik: "przelacznik" }, przel, rzad) /* menu zamknął pierścień: znacznik na przełączniku, który je otwiera z powrotem */
          : PK.celEtapu(sek, e, elementEtapu(e), rzad);
  /* Polecenia po kolei: aktywne tylko następne (numer `zrobione`), wysłane i dalsze mają disabled, w czasie gry etapu żadne; polecenia dróg w PK.stanDrog (tam też: w trakcie drogi nieaktywne). */
  const odswiez = () => {
    sek.querySelectorAll(".polecenie[data-e]").forEach((b) => {
      b.disabled = zajety || +b.dataset.e !== zrobione;
      b.classList.toggle("wyslane", +b.dataset.e < zrobione);
    });
    if (drogi) PK.stanDrog(sek, ukonczone, biezaca, zajety || zrobione < etapy.length || plan.czeka());
  };

  const dopisz = (html) => {
    rozmowa.insertAdjacentHTML("beforeend", html);
    return rozmowa.lastElementChild;
  };
  const plan = PK.planEtapow(sek, {
    dopisz,
    ustawTryb: (t) => (przel.textContent = t),
    graj: grajKroki,
  });

  function otworzMenu(otwarte) {
    menu.hidden = !otwarte;
    okno.classList.toggle("menu-otwarte", otwarte); /* krótka rozmowa rośnie, żeby lista mieściła się w oknie */
    przel.classList.toggle("otwarty", otwarte);
    przel.setAttribute("aria-expanded", String(otwarte));
    PK.zaznaczTryb(menu, otwarte ? przel.textContent : null); /* ✓ stoi tylko przy otwartym menu: zamknięte wygląda zawsze tak samo jak na starcie */
    ulozMenu();
    if (otwarte) {
      uspione = false;
      okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka (strona/aplikacja-pierscien.js) */
    }
  }
  /* Otwarcie okienka pierścienia zamyka menu trybów. Etap, który czeka na pozycję menu, nie może utknąć: znacznik przechodzi na przełącznik, a jego klik otwiera menu z powrotem i oddaje znacznik pozycji. */
  okno.addEventListener(PK.ZAMKNIJ_MENU, () => {
    if (menu.hidden) return;
    otworzMenu(false);
    uspione = true;
    if (!zajety) ustawCel();
  });

  function zatwierdz() {
    PK.zatwierdzZgode(karta);
    const zmiana = karta._zmiana;
    karta = null;
    zm.pokaz([zmiana]);
  }

  function otworzZmiany() {
    plan.zamknijPanel();
    zm.otworz();
    if (!zajety) ustawCel(); /* znacznik na licznikach znika po otwarciu widoku; w trakcie gry ustawi go koniecGry */
    /* układ się zmienił: znacznik i menu liczą położenie od nowa */
    sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
    ulozMenu();
  }

  async function kliknij(e, szybko, g) {
    const el = elementEtapu(e);
    if (el && !szybko) {
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (g !== gen) return;
    }
    if (e.klik === "zatwierdz" && karta) zatwierdz();
    else if (e.klik === "przelacznik") otworzMenu(true);
    else if (e.klik === "licznik") otworzZmiany();
    else if (e.klik === "tryb") {
      przel.textContent = e.na;
      otworzMenu(false);
    }
  }

  async function pisz(tekst, g) {
    pole.classList.add("pisze");
    for (let i = 1; i <= tekst.length; i += 2) {
      pole.textContent = tekst.slice(0, i);
      await czekaj(22);
      if (g !== gen) return;
    }
    pole.textContent = tekst;
    await czekaj(350);
    if (g !== gen) return;
    pole.textContent = "";
    pole.classList.remove("pisze");
    dopisz(PK.dymekAplikacji({ kto: "ty", tekst }));
  }

  async function krok(k, g, szybko, nast) {
    if (k.typ === "nauczyciel") return PK.krokNauczyciela(mow, k, nast, szybko);
    if (k.typ === "pisz")
      return szybko
        ? dopisz(PK.dymekAplikacji({ kto: "ty", tekst: k.tekst }))
        : pisz(k.tekst, g);
    if (k.typ === "claude")
      return dopisz(PK.dymekAplikacji({ kto: "claude", tekst: k.tekst }));
    if (k.typ === "mysli") {
      if (szybko) return;
      /* pauza bez napisu: dokumentacja aplikacji nie podaje wyglądu wskaźnika pracy */
      const el = dopisz(
        '<div class="apl-mysli" aria-hidden="true"><i></i><i></i><i></i></div>',
      );
      await czekaj(k.ms || 1200);
      return el.remove();
    }
    /* tryb Accept edits albo Auto: zmiana bez karty, w rozmowie nic nie przybywa, liczby stoją na karcie Changes */
    if (k.typ === "zmiana") return zm.pokaz(k.pliki);
    if (k.typ === "folder") return zm.krokFolderu(k);
    if (k.typ === "plan") return plan.pokaz(k);
    if (k.typ === "zgoda") {
      karta = dopisz(PK.kartaZgody(k));
      karta._zmiana = { plik: k.plik, linijki: k.linijki };
    }
  }

  /* Wykonuje etapy do numeru `cel` włącznie; wcześniejsze, jeszcze niezrobione, bez animacji. */
  async function idzDo(cel) {
    if (zajety || cel < zrobione || cel >= etapy.length) return;
    zajety = true;
    uspione = false;
    odswiez();
    const g = gen;
    PK.celPod(sek, null);
    while (zrobione <= cel) {
      const e = etapy[zrobione];
      const szybko = zrobione < cel;
      if (e.klik) await kliknij(e, szybko, g);
      if (g !== gen) return;
      for (const [j, k] of (e.kroki || []).entries()) {
        await krok(k, g, szybko, e.kroki[j + 1]);
        if (g !== gen) return;
      }
      zrobione++;
    }
    koniecGry();
  }

  /* Kroki przycisku karty planu: grają jak kroki etapu, po nich droga może się skończyć albo czekać na nową kartę. */
  async function grajKroki(kroki) {
    if (zajety) return;
    zajety = true;
    odswiez();
    const g = gen;
    PK.celPod(sek, null);
    for (const [j, k] of kroki.entries()) {
      await krok(k, g, false, kroki[j + 1]);
      if (g !== gen) return;
    }
    koniecGry();
  }

  function koniecGry() {
    if (drogi && zrobione >= etapy.length && !plan.czeka()) ukonczone.add(biezaca);
    zajety = false;
    odswiez();
    ustawCel();
  }

  function odNowa(calkiem /* „Od nowa” zdejmuje też ukończone drogi */) {
    if (calkiem) ukonczone.clear();
    gen++;
    zajety = false;
    uspione = false;
    zrobione = 0;
    karta = null;
    plan.zeruj();
    rozmowa.innerHTML = poczatek;
    pole.textContent = "";
    pole.classList.remove("pisze");
    przel.textContent = apl.tryb || "";
    biezaca = -1;
    if (drogi) etapy = PK.ustawDroge(sek, drogi, -1);
    otworzMenu(false);
    zm.zeruj();
    sek
      .querySelectorAll(".wlaczony, .wyslane")
      .forEach((e) => e.classList.remove("wlaczony", "wyslane"));
    mow(cw.nauczyciel_start, null, "polecenie"); /* nowa droga i „Od nowa”: mocny sygnał dymka */
    odswiez();
    ustawCel();
  }

  /* Polecenie drogi zeruje okno, ustawia tryb drogi i gra jej pierwszy etap; dalsze etapy drogi to polecenia pod nim. */
  function wybierzDroge(i) {
    odNowa();
    biezaca = i;
    etapy = PK.ustawDroge(sek, drogi, i);
    przel.textContent = drogi[i].tryb;
    idzDo(0);
  }

  sek.addEventListener("click", (ev) => {
    const b = ev.target.closest(".polecenie");
    if (b && b.dataset.d) wybierzDroge(+b.dataset.d);
    else if (b) idzDo(+b.dataset.e);
  });
  okno.addEventListener("click", (ev) => {
    if (uspione && przel.contains(ev.target)) {
      otworzMenu(true); /* zeruje `uspione` */
      return ustawCel();
    }
    const el = elementEtapu(etapy[zrobione]);
    if (el && el.contains(ev.target)) return idzDo(zrobione);
    /* licznik i przycisk Changes robią to samo: oba zaliczają etap z klik „licznik” */
    const zmienia = etapy[zrobione] && etapy[zrobione].klik === "licznik";
    if (zmienia && ev.target.closest(".apl-licznik, [data-pasek=changes]"))
      return idzDo(zrobione);
    /* licznik i przycisk Changes otwierają widok zmian dopiero po zmianie w plikach */
    if (zm.jest() && ev.target.closest(".apl-licznik, [data-pasek=changes]"))
      otworzZmiany();
  });
  sek.querySelector("[data-od-nowa]").addEventListener("click", () => odNowa(true));
  odNowa();
};
