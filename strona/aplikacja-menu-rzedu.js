/* Symulator aplikacji Claude, drogi: menu w rzędzie pod polem wiadomości otwierane kliknięciem w kroku drogi (paczka 4 część A). Lista trybów (kroki `klik` z celami `tryb-menu` i `tryb`, pole `na`): przełącznik trybu staje się klikalny, lista ma nagłówek i pozycje ze zrzutu Łukasza 04-41-10 (strona/aplikacja-tryby-menu.js, to samo menu co w etapach), wybór pozycji zmienia napis przełącznika. Menu środowiska (krok `klik` z celem `srodowisko-menu`): kontrolka „This computer” otwiera menu z polem wyszukiwania, grupą Local, pozycją Cloud i New environment (kadr zrzutu Łukasza z lekcji 0.1); menu niczego nie zmienia i zostaje otwarte do końca drogi. Kroki i skutki: dane/FORMAT-SCENARIUSZA.md. */

PK.CELE_TRYBU = ["tryb-menu", "tryb"];
PK.CELE_SRODOWISKA = ["srodowisko-menu"];
/* Znacznik „kliknij tutaj”: pod rzędem z przełącznikiem i z kontrolką środowiska, pod pozycją listy trybów. */
Object.assign(PK.PO_CELU_KROKU, { "tryb-menu": ".apl-rzad", tryb: "li", "srodowisko-menu": ".apl-rzad" });

/* Menu środowiska (kadr 2-rzad-pod-polem.png): pole wyszukiwania z kursorem i tekstem zastępczym, kreska, nagłówek Local, This computer z laptopem i ✓, kreska, Cloud ze strzałką, kreska, New environment z plusem. Wszystkie pozycje są bez skutku. */
PK.menuSrodowisk = () => {
  const { esc } = PK;
  const S = PK.NAPISY_SRODOWISK;
  const I = PK.IKONY_APLIKACJI;
  const kreska = '<div class="apl-srod-kreska" role="separator"></div>';
  const poz = (ikona, napis, prawa = "") => `<div class="apl-srod-poz" role="menuitem" aria-disabled="true"><span class="apl-srod-ikona">${ikona}</span><span>${esc(napis)}</span>${prawa}</div>`;
  return (
    `<div class="apl-menu-srodowisk" role="menu" hidden>` +
    `<div class="apl-srod-szukaj"><span class="apl-srod-kursor"></span><span class="apl-srod-podp">${esc(S.szukaj)}</span></div>` +
    `<div class="apl-srod-naglowek">${esc(S.lokalne)}</div>` +
    poz(I.laptop, PK.NAPISY_EKRANU.panel.komputer, `<span class="apl-srod-ptak" aria-hidden="true">${PK.IKONY_ZGODY.tak}</span>`) +
    kreska +
    poz("", S.chmura, `<span class="apl-srod-strzalka" aria-hidden="true">${I.dalej}</span>`) +
    kreska +
    poz(I.plus, S.nowe) +
    `</div>`
  );
};

/* Wspólne czekanie na klik w element kroku: znacznik („start” to {cel, el}, gdy znacznik ma stać gdzie indziej niż na elemencie kroku), czekanie, wciśnięcie. Zwraca true, gdy kursant kliknął, false, gdy krok przerwano („Od nowa”, nowe polecenie). */
const czekajNaKlik = async (sek, k, el, ustaw, zyje, start = { cel: k.cel, el }) => {
  PK.celKroku(sek, start.cel, start.el);
  const ok = await new Promise((pusc) => ustaw({ k, el, pusc }));
  ustaw(null);
  if (!ok || !zyje()) return false;
  PK.celKroku(sek, k.cel, null);
  el.classList.add("wcisniety");
  await PK.czekaj(200);
  el.classList.remove("wcisniety");
  return zyje();
};

/* Przełącznik trybu i lista trybów w ćwiczeniu z drogami, które mają krok `klik` z celem `tryb-menu` albo `tryb`; null, gdy żadna droga ich nie ma (przełącznik zostaje zwykłym napisem). Aktywny jest przełącznik albo pozycja listy, na którą czeka krok; reszta nie reaguje (pozycje są wyszarzone jak w menu +). Otwarcie okienka pierścienia zamyka listę, ale krok czekający na jej pozycję nie utyka: znacznik wraca na przełącznik, a jego klik otwiera listę z powrotem. Zwraca {dotyczy, klik, reset}. */
PK.trybMenuDrogi = function (cw, sek, okno) {
  const apl = cw.aplikacja || {};
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const rzad = sek.querySelector(".apl-rzad");
  const stary = rzad && rzad.querySelector(".apl-tryb");
  if (!stary || !kroki.some((k) => k.typ === "klik" && PK.CELE_TRYBU.includes(k.cel))) return null;
  const przel = document.createElement("button");
  przel.type = "button";
  przel.className = "apl-chip apl-tryb apl-przelacznik";
  przel.setAttribute("aria-haspopup", "menu");
  przel.setAttribute("aria-expanded", "false");
  przel.setAttribute("aria-disabled", "true");
  przel.textContent = apl.tryb || "";
  stary.replaceWith(przel);
  rzad.classList.add("apl-rzad-tryby");
  rzad.insertAdjacentHTML("beforeend", PK.menuTrybow(true, apl.bypass_dostepny === true));
  const menu = rzad.querySelector(".apl-menu-trybow");
  menu.querySelectorAll(".apl-tryb-poz").forEach((b) => b.setAttribute("aria-disabled", "true"));
  let czeka = null; /* {k, el, pusc}: element, na którego kliknięcie czeka krok */
  let uspione = false; /* listę zamknął pierścień zużycia: przełącznik otwiera ją z powrotem */

  const element = (k) => (k.cel === "tryb-menu" ? przel : [...menu.querySelectorAll(".apl-tryb-poz")].find((b) => b.dataset.tryb === k.na));
  const wlacz = (el, tak) => (tak ? el.removeAttribute("aria-disabled") : el.setAttribute("aria-disabled", "true"));
  const uloz = () => {
    if (menu.hidden) return;
    menu.style.left = Math.max(0, Math.min(przel.offsetLeft, rzad.clientWidth - menu.offsetWidth)) + "px";
    sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
  };
  window.addEventListener("resize", uloz);
  const otworz = (tak) => {
    menu.hidden = !tak;
    okno.classList.toggle("menu-otwarte", tak); /* krótka rozmowa rośnie, żeby lista mieściła się w oknie */
    przel.classList.toggle("otwarty", tak);
    przel.setAttribute("aria-expanded", String(tak));
    PK.zaznaczTryb(menu, tak ? przel.textContent : null);
    uloz();
    if (tak) {
      uspione = false;
      okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka */
    }
  };

  okno.addEventListener(PK.ZAMKNIJ_MENU, () => {
    if (menu.hidden) return;
    otworz(false);
    uspione = true;
    wlacz(przel, true);
    if (czeka) PK.celKroku(sek, "tryb-menu", przel);
  });
  rzad.addEventListener("click", (e) => {
    if (uspione && przel.contains(e.target) && !przel.hasAttribute("aria-disabled")) {
      otworz(true); /* zeruje `uspione` */
      wlacz(przel, !!czeka && czeka.el === przel);
      if (czeka) PK.celKroku(sek, czeka.k.cel, czeka.el); /* znacznik wraca na element, na który czeka krok */
      return;
    }
    if (czeka && czeka.el.contains(e.target) && !czeka.el.hasAttribute("aria-disabled")) czeka.pusc(true);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_TRYBU.includes(k.cel),
    async klik(k, zyje) {
      const el = element(k);
      wlacz(el, true);
      const start = uspione && k.cel === "tryb" ? { cel: "tryb-menu", el: przel } : undefined; /* lista zamknięta przez pierścień: znacznik stoi na przełączniku */
      const ok = await czekajNaKlik(sek, k, el, (c) => (czeka = c), zyje, start);
      wlacz(el, false);
      if (!ok) return;
      if (k.cel === "tryb-menu") otworz(true);
      else {
        przel.textContent = k.na;
        otworz(false);
      }
    },
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      uspione = false;
      przel.textContent = apl.tryb || "";
      wlacz(przel, false);
      menu.querySelectorAll(".apl-tryb-poz").forEach((b) => wlacz(b, false));
      otworz(false);
    },
  };
};

/* Menu środowiska w ćwiczeniu z drogami, które mają krok `klik` z celem `srodowisko-menu` (tylko `aplikacja.srodowisko` „Local”: kadr pokazuje menu sesji lokalnej); null w pozostałych. Kontrolka „This computer” staje się przyciskiem, aktywnym tylko wtedy, gdy krok na nią czeka. Menu zostaje otwarte po kroku (do „Od nowa”, nowego polecenia drogi, następnego kliknięcia w kontrolkę albo otwarcia okienka zużycia). Zwraca {dotyczy, klik, reset}. */
PK.srodowiskoMenuDrogi = function (cw, sek, okno) {
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const rzad = sek.querySelector(".apl-rzad");
  const chip = rzad && rzad.querySelector(".apl-chip-komputer");
  if (!chip || !kroki.some((k) => k.typ === "klik" && PK.CELE_SRODOWISKA.includes(k.cel))) return null;
  const przycisk = document.createElement("button");
  przycisk.type = "button";
  przycisk.className = `${chip.className} apl-srod-przycisk`;
  przycisk.setAttribute("aria-haspopup", "menu");
  przycisk.setAttribute("aria-expanded", "false");
  przycisk.setAttribute("aria-disabled", "true");
  przycisk.innerHTML = chip.innerHTML;
  chip.replaceWith(przycisk);
  rzad.classList.add("apl-rzad-tryby");
  rzad.insertAdjacentHTML("beforeend", PK.menuSrodowisk());
  const menu = rzad.querySelector(".apl-menu-srodowisk");
  let czeka = null;

  const otworz = (tak) => {
    menu.hidden = !tak;
    przycisk.classList.toggle("otwarty", tak);
    przycisk.setAttribute("aria-expanded", String(tak));
    okno.classList.toggle("menu-srodowisk-otwarte", tak);
    if (tak) okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko zużycia się zamyka */
  };
  okno.addEventListener(PK.ZAMKNIJ_MENU, () => otworz(false)); /* otwarcie okienka zużycia zamyka to menu */
  przycisk.addEventListener("click", () => {
    if (czeka && !przycisk.hasAttribute("aria-disabled")) czeka.pusc(true);
    else if (!przycisk.hasAttribute("aria-disabled")) otworz(menu.hidden);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_SRODOWISKA.includes(k.cel),
    async klik(k, zyje) {
      przycisk.removeAttribute("aria-disabled");
      const ok = await czekajNaKlik(sek, k, przycisk, (c) => (czeka = c), zyje);
      przycisk.setAttribute("aria-disabled", "true");
      if (ok) otworz(true);
    },
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      przycisk.setAttribute("aria-disabled", "true");
      otworz(false);
    },
  };
};
