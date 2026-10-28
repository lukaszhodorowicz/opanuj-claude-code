/* Symulator aplikacji Claude, drogi: klikalny przycisk + obok pola wiadomości z menu pozycji i podmenu Plugins i Connectors (napisy i układ ze zrzutów Łukasza, dane w strona/aplikacja-plus-dane.js), lista poleceń nad polem z nazwanymi wierszami (otwierana pozycją „Slash commands” albo znakiem /) i skill jako podświetlony pasek (z nazwą wiersza albo bez) w polu i w dymku kursanta; kroki `klik` z celami plus, pozycja i wiersz oraz krok `ukosnik` (część „Przycisk +, lista poleceń i skill w polu” w dane/FORMAT-SCENARIUSZA.md). */

PK.CELE_PLUSA = ["plus", "pozycja", "wiersz"];

/* Podświetlony pasek skilla: w polu wiadomości i w dymku kursanta. Z nazwą wiersza listy (`na`) niesie jego napis po ukośniku (jak polecenie wpisane w polu, zrzut 04-04-30), bez nazwy (stare kroki z bez_napisu) jest samym paskiem. */
PK.pasekSkilla = (na) =>
  typeof na === "string"
    ? `<span class="apl-pole-skill apl-pole-skill-nazwa">/${PK.esc(na)}</span>`
    : `<span class="apl-pole-skill" role="img" aria-label="${PK.esc(PK.OPISY_PLUSA.skill)}"></span>`;

/* Menu +: pozycje z ikoną, napisem, podpisem albo skrótem i strzałką (Connectors, Plugins), a obok podmenu. Wiersze zainstalowanych wtyczek i konektorów w podmenu to szare paski (lista jest u każdego inna). `aktywne` to napisy pozycji wskazanych krokami, `chmura` mówi o sesji w chmurze (zrzut 04-22-37). */
PK.htmlMenuPlus = function (aktywne, chmura) {
  const { esc, szkic } = PK;
  const lokalna = (p) => chmura && PK.POZYCJE_LOKALNE.includes(p);
  /* naprawdę szare w aplikacji (z podpisem): klasa `apl-poz-wylaczona` zostaje szara także na zrzucie bez znacznika (narzedzia/zrzuty.py) */
  const wylaczona = (p) => p === "Import GitHub issue" || lokalna(p);
  const poz = (p) => {
    const rodzic = !!PK.PODMENU_PLUS[p];
    const podpis = p === "Import GitHub issue" ? PK.PODPIS_GITHUB : lokalna(p) ? PK.PODPIS_LOKALNE : "";
    const atr = (aktywne.has(p) && !wylaczona(p) ? "" : ' aria-disabled="true"') + (rodzic ? ' aria-haspopup="menu" aria-expanded="false"' : "");
    return (
      `<li role="none"><button type="button" class="apl-menu-poz${wylaczona(p) ? " apl-poz-wylaczona" : ""}" role="menuitem" data-poz="${esc(p)}"${atr}>` +
      `<span class="apl-poz-ikona">${PK.IKONY_PLUS[p]}</span>` +
      `<span class="apl-poz-tekst"><span class="apl-poz-napis">${esc(p)}</span>${podpis ? `<span class="apl-poz-podpis">${esc(podpis)}</span>` : ""}</span>` +
      (PK.SKROT_PLUS[p] ? `<span class="apl-poz-skrot">${esc(PK.SKROT_PLUS[p])}</span>` : "") +
      (rodzic ? `<span class="apl-poz-strzalka">${PK.IKONY_APLIKACJI.dalej}</span>` : "") +
      `</button></li>`
    );
  };
  const szary = (proc, dodatek) => `<li role="none" aria-hidden="true"><span class="apl-menu-poz apl-poz-szary">${szkic(proc)}${dodatek}</span></li>`;
  const strzalka = `<span class="apl-poz-strzalka">${PK.IKONY_APLIKACJI.dalej}</span>`;
  const przelacznik = (wlaczony) => `<span class="apl-poz-przelacznik${wlaczony ? " wlaczony" : ""}"></span>`;
  const kreska = '<li role="separator" class="apl-menu-kreska"></li>';
  const podmenu = (nazwa) => {
    const [a, b] = PK.PODMENU_PLUS[nazwa];
    const wiersze = nazwa === "Plugins" ? [szary(58, strzalka), szary(44, strzalka), szary(66, strzalka), kreska, poz2(a), poz2(b)] : [poz2(a), poz2(b), kreska, szary(46, przelacznik(true)), szary(62, przelacznik(false))];
    return `<ul class="apl-menu-trybow apl-podmenu-plus" role="menu" data-podmenu="${esc(nazwa)}" aria-label="${esc(nazwa)}" hidden>${wiersze.join("")}</ul>`;
  };
  const poz2 = (p) =>
    `<li role="none"><button type="button" class="apl-menu-poz" role="menuitem" data-poz="${esc(p)}"${aktywne.has(p) ? "" : ' aria-disabled="true"'}><span class="apl-poz-ikona">${PK.IKONY_PLUS[p]}</span><span class="apl-poz-tekst"><span class="apl-poz-napis">${esc(p)}</span></span></button></li>`;
  const pozycje = PK.MENU_PLUS.filter((p) => !(chmura && p === "Import GitHub issue"));
  return `<div class="apl-plus-menu"><ul class="apl-menu-trybow apl-menu-plus" role="menu" hidden>${pozycje.map(poz).join("")}</ul>${Object.keys(PK.PODMENU_PLUS).map(podmenu).join("")}</div>`;
};

/* Lista poleceń: nazwane wiersze ze zrzutu 03-58-20 (pierwszy podświetlony, dymek z opisem obok) i szary wiersz bez nazwy na końcu. Klikalne są tylko wiersze wskazane krokami `wiersz` (`na` albo `bez_napisu`), reszta jest tekstem bez skutku. */
PK.htmlListyPlus = function (aktywneNa, bezNapisu) {
  const { esc, szkic } = PK;
  const wiersz = (n, i) => {
    const klasa = "apl-wiersz" + (i === 0 ? " apl-wiersz-pierwszy" : "");
    if (!aktywneNa.has(n)) return `<li role="none"><span class="${klasa}" role="option" aria-selected="${i === 0}" aria-disabled="true" data-wiersz="${esc(n)}"><span class="apl-wiersz-nazwa">${esc(n)}</span></span></li>`;
    return `<li role="none"><button type="button" class="${klasa} apl-wiersz-wybrany" role="option" aria-selected="${i === 0}" data-wiersz="${esc(n)}"><span class="apl-wiersz-nazwa">${esc(n)}</span></button></li>`;
  };
  const ostatni = bezNapisu
    ? `<li role="none"><button type="button" class="apl-wiersz apl-wiersz-wybrany apl-wiersz-bez-nazwy" role="option" aria-selected="false" aria-label="${esc(PK.OPISY_PLUSA.wiersz)}">${szkic(50)}</button></li>`
    : `<li role="none"><span class="apl-wiersz apl-wiersz-pasek" aria-hidden="true">${szkic(50)}</span></li>`;
  const opis = PK.OPISY_WIERSZY[PK.WIERSZE_LISTY[0]];
  return `<div class="apl-lista-polecen" hidden><ul class="apl-lista-rzedy" role="listbox">${PK.WIERSZE_LISTY.map(wiersz).join("")}${ostatni}</ul><div class="apl-lista-dymek" role="tooltip">${esc(opis)}</div></div>`;
};

/* Przycisk +, menu, podmenu i lista w ćwiczeniu z drogami, które mają kroki plus, pozycja, wiersz albo ukosnik; null, gdy żadna droga ich nie ma (reszta ćwiczeń zostaje bez zmian). Aktywne są pozycje menu i podmenu wskazane w krokach `pozycja` (pole `na`) i wiersze wskazane w krokach `wiersz`, reszta jest wyszarzona albo bez skutku. Sześć pozycji menu rysuje się zawsze, także w nowej sesji (zrzut 03-58-01); w sesji w chmurze (`aplikacja.srodowisko` Cloud) wygląd jak na zrzucie 04-22-37. Zwraca {dotyczy, klik, ukosnik, skill, wpisz, zeruj, reset}. */
PK.plusAplikacji = function (cw, sek, okno) {
  const { czekaj } = PK;
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const dotyczy = (k) => k.typ === "ukosnik" || (k.typ === "klik" && PK.CELE_PLUSA.includes(k.cel));
  if (!kroki.some(dotyczy)) return null;
  const klikane = (cel) => kroki.filter((k) => k.typ === "klik" && k.cel === cel);
  const aktywne = new Set(klikane("pozycja").map((k) => k.na));
  const aktywneNa = new Set(klikane("wiersz").map((k) => k.na).filter((n) => typeof n === "string"));
  const bezNapisu = klikane("wiersz").some((k) => typeof k.na !== "string");

  const poleWiadomosci = sek.querySelector(".apl-pole");
  const tekst = sek.querySelector(".apl-pole-tekst");
  const plus = document.createElement("button");
  plus.type = "button";
  plus.className = "apl-plus-przycisk";
  plus.setAttribute("aria-label", "+");
  plus.setAttribute("aria-haspopup", "menu");
  plus.setAttribute("aria-expanded", "false");
  plus.innerHTML = PK.IKONY_APLIKACJI.plus;
  sek.querySelector(".apl-pole-plus").replaceWith(plus);
  poleWiadomosci.classList.add("apl-pole-menu");
  poleWiadomosci.insertAdjacentHTML("beforeend", PK.htmlMenuPlus(aktywne, (cw.aplikacja || {}).srodowisko === "Cloud") + PK.htmlListyPlus(aktywneNa, bezNapisu));
  const menu = poleWiadomosci.querySelector(".apl-menu-plus");
  const podmenu = [...poleWiadomosci.querySelectorAll(".apl-podmenu-plus")];
  const lista = poleWiadomosci.querySelector(".apl-lista-polecen");
  const rzedy = lista.querySelector(".apl-lista-rzedy");
  rzedy.addEventListener("scroll", () => lista.classList.toggle("przewinieta", rzedy.scrollTop > 4)); /* dymek opisuje pierwszy wiersz: po przewinięciu znika */
  let czeka = null; /* {el, pusc}: element, na którego kliknięcie czeka krok klik */
  let zSkillem = false; /* false, true (skill bez nazwy) albo nazwa wiersza listy */
  let otwartePodmenu = null; /* „Plugins”, „Connectors” albo null */

  let uspione = null; /* {menu, podmenu, lista}: co było otwarte, gdy zamknął to pierścień zużycia (strona/aplikacja-pierscien.js) */
  const pokazPodmenu = (nazwa) => {
    otwartePodmenu = nazwa || null;
    podmenu.forEach((u) => (u.hidden = u.dataset.podmenu !== otwartePodmenu));
    menu.querySelectorAll("[aria-haspopup]").forEach((b) => {
      const otwarte = b.dataset.poz === otwartePodmenu;
      b.setAttribute("aria-expanded", String(otwarte));
      b.classList.toggle("otwarty", otwarte);
    });
    okno.classList.toggle("podmenu-otwarte", !!otwartePodmenu);
  };
  const pokazMenu = (otwarte) => {
    menu.hidden = !otwarte;
    if (!otwarte) pokazPodmenu(null); /* podmenu stoi obok menu: znika razem z nim */
    plus.classList.toggle("otwarty", otwarte);
    plus.setAttribute("aria-expanded", String(otwarte));
    okno.classList.toggle("plus-otwarte", otwarte);
    if (otwarte) {
      uspione = null;
      okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka (strona/aplikacja-pierscien.js) */
    }
  };
  /* Pole wiadomości przy otwartej liście: znak / i podpowiedź „Type to filter” (zrzut 03-58-20). */
  const poleListy = (otwarta) => {
    tekst.classList.remove("pisze");
    tekst.classList.toggle("z-lista", otwarta);
    if (otwarta) tekst.innerHTML = `<span class="apl-pole-uk">/</span><span class="apl-pole-podp">${PK.esc(PK.PODPOWIEDZ_POLA)}</span>`;
    else if (!zSkillem) tekst.innerHTML = ""; /* skill w polu (po kliku w wiersz) zostaje */
  };
  const pokazListe = (otwarta) => {
    lista.hidden = !otwarta;
    okno.classList.toggle("lista-otwarta", otwarta);
    poleListy(otwarta);
    if (otwarta) {
      uspione = null;
      okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE));
    }
  };
  /* Otwarcie okienka pierścienia zamyka menu, podmenu i listę. Krok, który czeka na element zamkniętego menu albo listy, nie może utknąć: znacznik przechodzi na przycisk +, a jego klik otwiera z powrotem to, co było otwarte (menu z podmenu albo listę), i oddaje znacznik elementowi kroku. */
  okno.addEventListener(PK.ZAMKNIJ_MENU, () => {
    const otwarte = { menu: !menu.hidden, podmenu: otwartePodmenu, lista: !lista.hidden };
    if (!otwarte.menu && !otwarte.lista) return;
    pokazMenu(false);
    pokazListe(false);
    uspione = otwarte;
    if (czeka) PK.celPod(sek, plus, poleWiadomosci);
  });
  const element = (k) =>
    k.cel === "plus"
      ? plus
      : k.cel === "pozycja"
        ? poleWiadomosci.querySelector(`[data-poz="${k.na}"]`)
        : typeof k.na === "string"
          ? lista.querySelector(`[data-wiersz="${k.na}"]`)
          : lista.querySelector(".apl-wiersz-bez-nazwy");
  /* Wiersz poza widocznym fragmentem listy przewija się na miejsce (z zapasem na znacznik pod nim); dymek przy pierwszym wierszu zależy od przewinięcia. */
  const przewin = (el) => {
    const r = el.getBoundingClientRect();
    const c = rzedy.getBoundingClientRect();
    if (r.bottom + 44 > c.bottom) rzedy.scrollTop += r.bottom + 44 - c.bottom;
    else if (r.top < c.top) rzedy.scrollTop -= c.top - r.top;
    lista.classList.toggle("przewinieta", rzedy.scrollTop > 4);
  };

  /* Kursant klika tylko to, na co czeka krok (menu i lista są poza rozmową, więc strażnik kliku z aplikacja.js ich nie widzi); inne kliknięcia niczego nie robią. */
  poleWiadomosci.addEventListener("click", (e) => {
    if (uspione && plus.contains(e.target)) {
      const bylo = uspione; /* pokazMenu i pokazListe zerują `uspione` */
      pokazMenu(bylo.menu);
      pokazPodmenu(bylo.podmenu);
      pokazListe(bylo.lista);
      if (czeka) PK.celPod(sek, czeka.el, czeka.po); /* znacznik wraca na element, na który czeka krok */
      return;
    }
    if (czeka && czeka.el.contains(e.target)) czeka.pusc(true);
  });

  return {
    dotyczy,
    skill: () => zSkillem,
    /* Znacznik „kliknij tutaj” w rzędzie zaraz pod elementem (pod polem przy +, pod pozycją menu albo podmenu i pod wierszem listy), czekanie na klik i skutek: + otwiera menu; „Plugins” i „Connectors” otwierają podmenu obok menu (menu zostaje); „Slash commands” zamyka menu i otwiera listę; pozycja podmenu i inna aktywna pozycja zamykają menu (Browse connectors i Browse plugins otwierają potem okno, strona/aplikacja.js); wiersz trafia do pola jako podświetlony pasek (z nazwą wiersza albo bez). `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane. */
    async klik(k, zyje) {
      const el = element(k);
      const po = k.cel === "plus" ? poleWiadomosci : el.parentElement;
      if (uspione && k.cel !== "plus") PK.celPod(sek, plus, poleWiadomosci); /* menu zamknął pierścień: znacznik stoi na przycisku +, który je otwiera z powrotem */
      else {
        PK.celPod(sek, el, po);
        if (k.cel === "wiersz") przewin(el);
      }
      const ok = await new Promise((pusc) => (czeka = { el, po, pusc }));
      czeka = null;
      uspione = null;
      if (!ok || !zyje()) return;
      PK.celPod(sek, null);
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (!zyje()) return;
      if (k.cel === "plus") pokazMenu(true);
      else if (k.cel === "pozycja") {
        if (PK.PODMENU_PLUS[k.na]) pokazPodmenu(k.na);
        else {
          pokazMenu(false);
          pokazListe(k.na === "Slash commands");
        }
      } else {
        zSkillem = typeof k.na === "string" ? k.na : true;
        pokazListe(false);
        tekst.classList.add("z-skillem");
        tekst.innerHTML = `${PK.pasekSkilla(zSkillem)}<span class="apl-pole-zadanie"></span>`;
      }
    },
    /* Krok ukosnik: w polu pojawia się znak /, po chwili otwiera się ta sama lista co po pozycji menu. */
    async ukosnik(zyje) {
      tekst.classList.add("pisze");
      tekst.textContent = "/";
      await czekaj(450);
      if (zyje()) pokazListe(true);
    },
    /* Tekst z kroku pisz po skillu w polu: dopisuje się po pasku. */
    wpisz: (t) => {
      const zadanie = tekst.querySelector(".apl-pole-zadanie");
      if (zadanie) zadanie.textContent = " " + t;
    },
    /* Po wysłaniu wiadomości pole jest puste, skilla w nim nie ma. */
    zeruj() {
      zSkillem = false;
      tekst.classList.remove("z-skillem");
    },
    /* „Od nowa” i nowe polecenie: menu, podmenu i lista zamknięte, pole puste, krok, który czeka na klik, przerwany. */
    reset() {
      uspione = null;
      if (czeka) czeka.pusc(false);
      czeka = null;
      this.zeruj();
      pokazMenu(false);
      pokazListe(false);
      rzedy.scrollTop = 0;
      lista.classList.remove("przewinieta");
      tekst.classList.remove("pisze", "z-lista");
      tekst.textContent = "";
    },
  };
};
