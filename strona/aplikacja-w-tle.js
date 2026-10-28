/* Symulator aplikacji Claude, praca w tle, gra: pole `w_tle` (lista prac) i `w_tle_koniec` kroku `claude`, kroki `klik` z celami menu-paska, background-tasks i wpis-w-tle, ⋮ nieaktywny do pierwszej pracy w tle, menu ⋮, panel zadań w tle i panel subagenta w miejscu otwartego pliku (jak panel pytania z boku), napis „N running tasks” pod odpowiedzią (przy co najmniej dwóch pracach; nieaktywny: bez skutku, bez ręki i bez podświetlenia) i szare wiersze po zakończeniu pracy (część „Praca w tle: menu ⋮, panel zadań i panel subagenta” w dane/FORMAT-SCENARIUSZA.md). Wygląd: strona/aplikacja-w-tle-widok.js. */

/* Praca w tle w ćwiczeniu z drogami, które mają pole `w_tle` albo kartę przepływu (krok `przeplyw`, klik Once dodaje wpis); null, gdy żadna droga go nie ma (reszta ćwiczeń zostaje bez zmian). `widok` to `.apl-widok-pliku` okna `okno`, `zamknijInne()` zamyka widok artefaktu i cudzą stronę, które panel wypiera. Zwraca {dotyczy, dodaj, wierszeKonca, klik, reset}. */
PK.wTleAplikacji = function (cw, sek, okno, widok, zamknijInne) {
  const { czekaj } = PK;
  const dotyczy = (k) => k.typ === "klik" && PK.CELE_W_TLE.includes(k.cel);
  if (!PK.drogiZPracaWTle(cw.drogi)) return null;
  const przycisk = sek.querySelector('[data-pasek="menu"]');
  const pasek = sek.querySelector(".apl-pasek");
  const opakowanie = przycisk.parentElement;
  let wpisy = []; /* prace w tle tej drogi, w kolejności kroków `claude` z `w_tle` */
  let menu = null;
  let czeka = null; /* {el, pusc}: element, na którego kliknięcie czeka krok klik */
  let skonczone = false; /* praca w tle skończyła się (krok z w_tle_koniec): nowa praca, którą zaczyna klik Once na karcie przepływu, zaczyna listę od nowa */

  const wlacz = (tak) => {
    przycisk.classList.toggle("apl-bez", !tak);
    if (tak) przycisk.removeAttribute("aria-disabled");
    else przycisk.setAttribute("aria-disabled", "true");
  };
  const pokazMenu = (otwarte) => {
    if (menu) menu.remove();
    menu = null;
    if (otwarte) {
      opakowanie.insertAdjacentHTML("beforeend", PK.menuPaska(wpisy.length));
      menu = opakowanie.querySelector(".apl-menu-paska");
    }
    przycisk.classList.toggle("wlaczony", otwarte);
    przycisk.setAttribute("aria-expanded", String(otwarte));
  };
  const pokazPanel = (html) => {
    zamknijInne();
    widok.innerHTML = html;
    widok.hidden = false;
    okno.classList.add("plik-otwarty");
  };
  const element = (k) =>
    k.cel === "menu-paska" ? przycisk : k.cel === "background-tasks" ? menu.querySelector('[data-poz="w-tle"]') : widok.querySelector(`button.apl-wtle-wpis[data-nr="${k.nr}"]`);
  const skutek = (k) => {
    if (k.cel === "menu-paska") pokazMenu(true);
    else if (k.cel === "wpis-w-tle") pokazPanel(PK.panelSubagenta(wpisy[k.nr - 1]));
    else {
      pokazMenu(false);
      pokazPanel(PK.panelZadanWTle(wpisy));
    }
  };

  /* Kursant klika tylko to, na co czeka krok (menu i panel stoją poza rozmową); inne kliknięcia niczego nie robią, także napis „N running tasks” pod odpowiedzią (nieaktywny). */
  sek.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target)) czeka.pusc(true);
  });

  return {
    dotyczy,
    /* Krok `claude` z `w_tle`: nowe prace w tle; ⋮ staje się aktywny, otwarty panel zadań dostaje karty, a pod odpowiedzią `dymek` (przy co najmniej dwóch pracach) staje nieaktywny napis z ich liczbą; napis z wcześniejszej odpowiedzi znika. */
    dodaj(lista, dymek) {
      if (skonczone) {
        skonczone = false;
        wpisy = [];
        pokazMenu(false);
        if (widok.querySelector("[data-w-tle]")) {
          widok.hidden = true; /* panel po zakończonej pracy nie ma stanu do pokazania (stan po zakończeniu nie ma źródła) */
          widok.innerHTML = "";
          okno.classList.remove("plik-otwarty");
        }
      }
      wpisy.push(...lista);
      wlacz(true);
      sek.querySelectorAll(".apl-wtle-link").forEach((l) => l.remove());
      if (wpisy.length >= 2) dymek.insertAdjacentHTML("beforeend", PK.linkWTle(wpisy.length));
      if (widok.querySelector('[data-w-tle="zadania"]')) widok.innerHTML = PK.panelZadanWTle(wpisy);
    },
    /* Krok `claude` z `w_tle_koniec`: napis „N running tasks” znika razem z końcem pracy w tle, a przed ostatnią odpowiedzią stoi szary wiersz z tytułem na każdego subagenta (HTML do wstawienia w rozmowę). */
    wierszeKonca() {
      skonczone = true;
      sek.querySelectorAll(".apl-wtle-link").forEach((l) => l.remove());
      return wpisy.filter((w) => w.rodzaj === "subagent").map(PK.wierszKoncaWTle).join("");
    },
    /* Znacznik „kliknij tutaj” pod paskiem tytułu (⋮), pod pozycją menu, pod kartą, czekanie na klik i skutek. */
    async klik(k, zyje) {
      const el = element(k);
      PK.celPod(sek, el, k.cel === "menu-paska" ? pasek : el.closest("li") || el.parentElement);
      const ok = await new Promise((pusc) => (czeka = { el, pusc }));
      czeka = null;
      if (!ok || !zyje()) return;
      PK.celPod(sek, null);
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (!zyje()) return;
      skutek(k);
    },
    /* „Od nowa” i nowe polecenie: menu zamknięte, wpisy usunięte, ⋮ znów nieaktywny, krok, który czeka na klik, przerwany (panel zamyka wyczyszczenie widoku w strona/aplikacja.js, napis i wiersze rozmowę startową). */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      skonczone = false;
      wpisy = [];
      pokazMenu(false);
      wlacz(false);
      PK.celPod(sek, null);
    },
  };
};
