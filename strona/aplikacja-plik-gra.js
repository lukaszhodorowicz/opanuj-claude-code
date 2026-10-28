/* Symulator aplikacji Claude, drogi: kroki `klik` z celami plik-menu (menu „…” panelu otwartego pliku), plik-karta-menu (menu prawego kliku na karcie pliku w rozmowie), plik-karta-pozycja (pozycja tego menu, pole `pozycja`) i ikona-tytulu (dymek pierwszej ikony paska tytułu, pole `nr`); zrzuty Łukasza z 27.10.2026 (15-27-25, 15-27-51, 15-28-18). Menu i dymek nie mają skutku poza otwarciem i podświetleniem, zostają do końca drogi („Od nowa” i nowe polecenie je zamykają). Karta pliku przyjmuje klik i prawy klik, ikona klik i najechanie. Kod rysujący: strona/aplikacja-plik-panel.js, napisy: strona/aplikacja-plik-dane.js, kroki i skutki: dane/FORMAT-SCENARIUSZA.md. */

PK.CELE_PLIKU = ["plik-menu", "plik-karta-menu", "plik-karta-pozycja", "ikona-tytulu"];
/* Znacznik „kliknij tutaj”: pod paskiem panelu pliku, pod kartą pliku, pod pozycją menu karty i pod paskiem tytułu (ikona). */
Object.assign(PK.PO_CELU_KROKU, { "plik-menu": ".apl-pp-pasek", "plik-karta-menu": ".apl-kp", "plik-karta-pozycja": "li", "ikona-tytulu": ".apl-pasek" });

/* Zdarzenia, które zaliczają krok: karta pliku to klik albo prawy klik (zrzut pokazuje menu prawego kliku), ikona klik albo najechanie (dymek pojawia się po najechaniu), reszta tylko klik. */
PK.ZDARZENIA_PLIKU = { "plik-menu": ["click"], "plik-karta-menu": ["click", "contextmenu"], "plik-karta-pozycja": ["click"], "ikona-tytulu": ["click", "mouseover"] };

/* Menu i dymek tego okna w ćwiczeniu z drogami, które mają któryś z czterech celów; null w pozostałych. Zwraca {dotyczy, klik, reset}. */
PK.plikEkranyAplikacji = function (cw, sek, okno, widok) {
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  if (!kroki.some((k) => k.typ === "klik" && PK.CELE_PLIKU.includes(k.cel))) return null;
  const rozmowa = sek.querySelector(".apl-rozmowa");
  let czeka = null; /* {cel, el, pusc}: element, na którego kliknięcie czeka krok */
  let menuKarty = null; /* otwarte menu prawego kliku */

  const przyciskPanelu = () => widok.querySelector(".apl-pp-menu");
  const karta = () => [...rozmowa.querySelectorAll(".apl-kp")].pop();
  const ikona = () => sek.querySelector('[data-pasek="szyna"]');
  const pozycje = () => (menuKarty ? [...menuKarty.querySelectorAll(".apl-mp-poz")] : []);
  const element = (k) =>
    k.cel === "plik-menu" ? przyciskPanelu() : k.cel === "plik-karta-menu" ? karta() : k.cel === "plik-karta-pozycja" ? pozycje().find((b) => b.dataset.poz === k.pozycja) : ikona();
  const wylaczany = (k) => k.cel === "plik-menu" || k.cel === "plik-karta-pozycja"; /* przycisk „…” i pozycje menu są nieaktywne, dopóki krok na nie nie czeka */
  const wlacz = (el, tak) => (tak ? el.removeAttribute("aria-disabled") : el.setAttribute("aria-disabled", "true"));

  const zamknijMenuPanelu = () => {
    const menu = widok.querySelector(".apl-menu-pliku-panel");
    if (menu) menu.remove();
    okno.classList.remove("menu-pliku-otwarte");
    const b = przyciskPanelu();
    if (b) {
      b.classList.remove("otwarty");
      b.setAttribute("aria-expanded", "false");
    }
  };
  const zamknijMenuKarty = () => {
    if (menuKarty) menuKarty.remove();
    menuKarty = null;
  };
  /* Menu karty stoi przy karcie; gdy nie mieści się nad dołem okna, staje nad kartą. */
  const ulozMenuKarty = () => {
    if (!menuKarty) return;
    menuKarty.classList.remove("nad");
    menuKarty.classList.toggle("nad", menuKarty.getBoundingClientRect().bottom > okno.getBoundingClientRect().bottom - 4);
  };
  window.addEventListener("resize", ulozMenuKarty);

  const otworzMenuPanelu = (przycisk) => {
    zamknijMenuKarty();
    przycisk.parentElement.insertAdjacentHTML("beforeend", PK.menuPliku(PK.MENU_PLIKU, "apl-menu-pliku-panel"));
    przycisk.classList.add("otwarty");
    przycisk.setAttribute("aria-expanded", "true");
    okno.classList.add("menu-pliku-otwarte"); /* krótki panel (np. pod rozmową na telefonie) rośnie, żeby menu mieściło się w oknie */
    okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka (strona/aplikacja-pierscien.js) */
  };
  const otworzMenuKarty = (kp) => {
    zamknijMenuPanelu();
    zamknijMenuKarty();
    kp.insertAdjacentHTML("beforeend", PK.menuPliku(PK.MENU_KARTY_PLIKU, "apl-menu-karty"));
    menuKarty = kp.lastElementChild;
    ulozMenuKarty();
    okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE));
  };
  const skutek = (k, el) => {
    if (k.cel === "plik-menu") otworzMenuPanelu(el);
    else if (k.cel === "plik-karta-menu") otworzMenuKarty(el);
    else if (k.cel === "plik-karta-pozycja") {
      pozycje().forEach((b) => b.classList.toggle("apl-mp-wybrana", b === el)); /* podświetlenie jak najechanie, bez skutku */
    } else el.classList.add("apl-dymek-stale"); /* dymek zostaje widoczny do końca drogi */
  };

  /* Krok zalicza zdarzenie na elemencie, na który czeka; prawy klik na karcie nie pokazuje menu przeglądarki. */
  const zalicz = (e) => {
    if (!czeka || !czeka.el.contains(e.target) || !PK.ZDARZENIA_PLIKU[czeka.cel].includes(e.type)) return;
    if (e.type === "contextmenu") e.preventDefault();
    czeka.pusc(true);
  };
  ["click", "contextmenu", "mouseover"].forEach((z) => sek.addEventListener(z, zalicz));
  /* Okienko zużycia zamyka menu panelu i menu karty, ale nie menu karty, z którego krok czeka na pozycję (znacznik zostałby bez celu). */
  okno.addEventListener(PK.ZAMKNIJ_MENU, () => {
    zamknijMenuPanelu();
    if (!(czeka && czeka.cel === "plik-karta-pozycja")) zamknijMenuKarty();
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_PLIKU.includes(k.cel),
    async klik(k, zyje) {
      const el = element(k);
      if (!el) return; /* walidator nie dopuszcza kroku bez otwartego pliku, karty albo menu */
      if (wylaczany(k)) wlacz(el, true);
      PK.celKroku(sek, k.cel, el);
      const ok = await new Promise((pusc) => (czeka = { cel: k.cel, el, pusc }));
      czeka = null;
      if (wylaczany(k)) wlacz(el, false);
      if (!ok || !zyje()) return;
      PK.celKroku(sek, k.cel, null);
      el.classList.add("wcisniety");
      await PK.czekaj(200);
      el.classList.remove("wcisniety");
      if (zyje()) skutek(k, el);
    },
    /* „Od nowa” i nowe polecenie: menu zamknięte, dymek ukryty, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      zamknijMenuPanelu();
      zamknijMenuKarty();
      const i = ikona();
      if (i) i.classList.remove("apl-dymek-stale");
      PK.celPod(sek, null);
    },
  };
};
