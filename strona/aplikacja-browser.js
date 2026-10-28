/* Symulator aplikacji Claude, drogi: kroki `klik` z celami `przegladarka` (przycisk Browser na pasku tytułu otwiera panel z pustą kartą „New tab”) i `przegladarka-menu` (przycisk „…” w panelu otwiera menu); wygląd panelu i menu: strona/aplikacja-browser-dane.js. Część „Menu panelu Browser, edytor prezentacji i Transcript view” w dane/FORMAT-SCENARIUSZA.md. */

PK.CELE_BROWSERA = ["przegladarka", "przegladarka-menu"];

/* Panel Browser w ćwiczeniu z drogami, które mają krok `klik` z celem `przegladarka` albo `przegladarka-menu`; null w pozostałych. Przycisk Browser na pasku tytułu jest zwykle bez skutku (strona/styl-aplikacja-przegladarka.css); aktywny jest tylko wtedy, gdy krok na niego czeka. Panel stoi w miejscu otwartego pliku (`widok`) i znika razem z nim (inny plik, strona, artefakt, nowe polecenie). Menu „…” zostaje otwarte do końca drogi, a jego pozycje nie mają skutku. Zwraca {dotyczy, klik, zamknij, reset}. */
PK.browserAplikacji = function (cw, sek, okno, widok) {
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  if (!kroki.some((k) => k.typ === "klik" && PK.CELE_BROWSERA.includes(k.cel))) return null;
  const przycisk = sek.querySelector('[data-pasek="browser"]');
  const pasek = sek.querySelector(".apl-pasek");
  let czeka = null; /* {el, pusc}: element, na którego kliknięcie czeka krok */

  const panel = () => widok.querySelector(".apl-pbr");
  const zdejmij = () => {
    przycisk.classList.remove("wlaczony");
    okno.classList.remove("browser-otwarty");
  };
  /* Zamknięcie panelu przez innego lokatora miejsca (plik, strona, artefakt, zmiana rozmowy): czyści tylko to, co należy do panelu Browser. */
  const zamknij = () => {
    if (panel()) {
      widok.hidden = true;
      widok.innerHTML = "";
      okno.classList.remove("plik-otwarty");
    }
    zdejmij(); /* ślad na pasku tytułu i w oknie znika także wtedy, gdy panel zamknął już ktoś inny */
  };
  const otworzPanel = () => {
    widok.innerHTML = PK.panelBrowsera();
    widok.hidden = false;
    okno.classList.add("plik-otwarty", "browser-otwarty"); /* okno ma tyle wysokości, żeby mieściło się w nim menu „…” */
    przycisk.classList.add("wlaczony");
  };
  const otworzMenu = () => {
    panel().insertAdjacentHTML("beforeend", PK.menuBrowsera());
    panel().querySelector(".apl-pbr-menu").setAttribute("aria-expanded", "true");
    panel().querySelector(".apl-pbr-menu").classList.add("wlaczony");
  };

  /* Kursant klika tylko to, na co czeka krok; panel i menu stoją poza rozmową, więc strażnik kliku z aplikacja.js ich nie widzi. */
  sek.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target) && !czeka.el.hasAttribute("aria-disabled")) czeka.pusc(true);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_BROWSERA.includes(k.cel),
    async klik(k, zyje) {
      const menu = k.cel === "przegladarka-menu";
      const el = menu ? panel().querySelector(".apl-pbr-menu") : przycisk;
      if (menu) PK.wlaczMenuB(el, true); /* przycisk „…” jest nieaktywny, dopóki krok na niego nie czeka; przycisk Browser z paska tytułu reaguje tylko dlatego, że czeka na niego krok */
      const ok = await PK.czekajNaKlikMenuB(sek, el, menu ? panel().querySelector(".apl-pbr-glowa") : pasek, (c) => (czeka = c), zyje);
      if (menu) PK.wlaczMenuB(el, false);
      if (!ok) return;
      if (menu) otworzMenu();
      else otworzPanel();
    },
    zamknij,
    /* „Od nowa” i nowe polecenie: krok, który czeka na klik, przerwany; panel czyści strona/aplikacja.js (widok), tu znika tylko jego ślad na pasku tytułu i w oknie. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      zdejmij();
      PK.celPod(sek, null);
    },
  };
};
