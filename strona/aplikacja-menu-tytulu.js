/* Symulator aplikacji Claude, drogi: menu sesji otwierane strzałką przy tytule rozmowy w pasku tytułu i jego podmenu „Transcript view” z pozycjami Normal i Verbose (zrzut Łukasza 27.10.2026, zrzut_2026-10-27_15-32-22.png; część „Menu panelu Browser, edytor prezentacji i Transcript view” w dane/FORMAT-SCENARIUSZA.md). Kroki `klik` z celami `strzalka-tytulu`, `transcript-view` i `widok-transkrypcji` (pole `na`); pozycji Thinking nie ma, bo aplikacja pokazuje ją dopiero po myśleniu Claude (fakt aplikacja-widok-thinking-dopiero-po-mysleniu). */

/* Napisy menu sesji; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */
PK.NAPISY_MENU_TYTULU = {
  otworz: "Open in",
  zmien: "Rename",
  skrot_zmien: "R",
  kopiuj: "Copy link",
  skrot_kopiuj: "C",
  widok: "Transcript view",
  chmura: "Edit cloud environment",
  archiwizuj: "Archive",
  skrot_archiwizuj: "A",
  usun: "Delete",
  skrot_usun: "D",
  normal: "Normal",
  verbose: "Verbose",
};
/* Polski opis strzałki dla czytnika ekranu (bez dymka): nie jest napisem interfejsu. */
PK.OPIS_STRZALKI_TYTULU = "Menu rozmowy (strzałka przy tytule)";
PK.CELE_TYTULU = ["strzalka-tytulu", "transcript-view", "widok-transkrypcji"];
PK.WIDOKI_TRANSKRYPCJI = ["Normal", "Verbose"]; /* bez Thinking: pojawia się dopiero po myśleniu Claude */

/* Podmenu widoku rozmowy: Normal i Verbose, ptaszek przy wybranej pozycji (na starcie Normal). */
PK.podmenuWidoku = (wybrany) => {
  const N = PK.NAPISY_MENU_TYTULU;
  const poz = (w) => PK.pozycjaMenuB(N[w.toLowerCase()], { dane: { widok: w }, prawa: w === wybrany ? PK.ptaszekMenuB() : "" });
  return `<ul class="apl-mb apl-mb-podmenu" role="menu">${PK.WIDOKI_TRANSKRYPCJI.map(poz).join("")}</ul>`;
};

/* Menu sesji (zrzut 15-32-22): Open in ›, kreska, Rename R, kreska, Copy link C, kreska, Transcript view › i (tylko w sesji w chmurze) Edit cloud environment, kreska, Archive A, Delete (czerwone) D. Pozycje nie mają skutku, poza tą, na którą czeka krok. */
PK.menuTytulu = (wChmurze) => {
  const N = PK.NAPISY_MENU_TYTULU;
  const poz = PK.pozycjaMenuB;
  const wiersze = [
    poz(N.otworz, { prawa: PK.strzalkaMenuB() }),
    PK.liniaMenuB,
    poz(N.zmien, { prawa: PK.skrotMenuB(N.skrot_zmien) }),
    PK.liniaMenuB,
    poz(N.kopiuj, { prawa: PK.skrotMenuB(N.skrot_kopiuj) }),
    PK.liniaMenuB,
    poz(N.widok, { prawa: PK.strzalkaMenuB(), dane: { poz: "widok" } }),
    wChmurze ? poz(N.chmura) : "",
    PK.liniaMenuB,
    poz(N.archiwizuj, { prawa: PK.skrotMenuB(N.skrot_archiwizuj) }),
    poz(N.usun, { czerwona: true, prawa: PK.skrotMenuB(N.skrot_usun) }),
  ];
  return `<ul class="apl-mb apl-mt" role="menu">${wiersze.join("")}</ul>`;
};

/* Menu sesji w ćwiczeniu z drogami, które mają krok `klik` z celem `strzalka-tytulu`, `transcript-view` albo `widok-transkrypcji`; null w pozostałych. Strzałka przy tytule w pasku tytułu jest przyciskiem aktywnym tylko wtedy, gdy krok na nią czeka. Menu zostaje otwarte po kroku (do „Od nowa” i nowego polecenia drogi); wybór pozycji podmenu przesuwa ptaszek, a menu się nie zamyka (umowa symulatora: żaden zrzut nie pokazuje, co dzieje się po wyborze). Pozycję „Edit cloud environment” rysuje tylko sesja `Cloud`. Zwraca {dotyczy, klik, reset}. */
PK.menuTytuluDrogi = function (cw, sek, okno) {
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  if (!kroki.some((k) => k.typ === "klik" && PK.CELE_TYTULU.includes(k.cel))) return null;
  const wChmurze = (cw.aplikacja || {}).srodowisko === "Cloud";
  const pasek = sek.querySelector(".apl-pasek");
  const przycisk = document.createElement("button");
  przycisk.type = "button";
  przycisk.className = "apl-ikona apl-tyt-strzalka";
  przycisk.setAttribute("aria-haspopup", "menu");
  przycisk.setAttribute("aria-expanded", "false");
  przycisk.setAttribute("aria-disabled", "true");
  przycisk.setAttribute("aria-label", PK.OPIS_STRZALKI_TYTULU);
  przycisk.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m7 10 5 5 5-5"/></svg>';
  pasek.firstElementChild.after(przycisk); /* pierwszy element paska to tytuł rozmowy (strona/aplikacja-sesje-gra.js podmienia go w miejscu) */
  pasek.classList.add("apl-pasek-menu");
  let menu = null;
  let widok = "Normal";
  let czeka = null; /* {el, pusc}: element, na którego kliknięcie czeka krok */

  const ulozMenu = () => {
    if (!menu) return;
    menu.style.left = Math.max(8, Math.min(przycisk.offsetLeft, pasek.clientWidth - menu.offsetWidth - 8)) + "px";
    sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
  };
  window.addEventListener("resize", ulozMenu);
  const pokazMenu = (tak) => {
    if (menu) menu.remove();
    menu = null;
    if (tak) {
      pasek.insertAdjacentHTML("beforeend", PK.menuTytulu(wChmurze));
      menu = pasek.lastElementChild;
      ulozMenu();
    }
    okno.classList.toggle("menu-tytulu-otwarte", tak); /* krótka rozmowa rośnie, żeby menu mieściło się w oknie */
    przycisk.classList.toggle("wlaczony", tak);
    przycisk.setAttribute("aria-expanded", String(tak));
  };
  const otworzPodmenu = () => {
    const wiersz = menu.querySelector('[data-poz="widok"]');
    wiersz.classList.add("otwarta");
    wiersz.closest("li").insertAdjacentHTML("beforeend", PK.podmenuWidoku(widok));
    ulozMenu();
  };
  const wybierz = (na) => {
    widok = na;
    menu.querySelector(".apl-mb-podmenu").outerHTML = PK.podmenuWidoku(widok);
  };

  /* Kursant klika tylko to, na co czeka krok (menu stoi poza rozmową); inne kliknięcia niczego nie robią. */
  sek.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target) && !czeka.el.hasAttribute("aria-disabled")) czeka.pusc(true);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_TYTULU.includes(k.cel),
    async klik(k, zyje) {
      const strzalka = k.cel === "strzalka-tytulu";
      const el = strzalka ? przycisk : k.cel === "transcript-view" ? menu.querySelector('[data-poz="widok"]') : menu.querySelector(`.apl-mb-podmenu [data-widok="${k.na}"]`);
      PK.wlaczMenuB(el, true);
      pasek.classList.toggle("apl-mt-czeka", !strzalka); /* przy menu czekającym na pozycję reszta pozycji jest przygaszona */
      const ok = await PK.czekajNaKlikMenuB(sek, el, strzalka ? pasek : el.closest("li"), (c) => (czeka = c), zyje);
      PK.wlaczMenuB(el, false);
      pasek.classList.remove("apl-mt-czeka");
      if (!ok) return;
      if (strzalka) pokazMenu(true);
      else if (k.cel === "transcript-view") otworzPodmenu();
      else wybierz(k.na);
    },
    /* „Od nowa” i nowe polecenie: menu zamknięte, widok wraca na Normal, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      widok = "Normal";
      pokazMenu(false);
      PK.wlaczMenuB(przycisk, false);
      pasek.classList.remove("apl-mt-czeka");
      PK.celPod(sek, null);
    },
  };
};
