/* Symulator aplikacji Claude, lista trybów otwierana przełącznikiem w rzędzie pod polem (zrzut Łukasza 27.10.2026, plik 04-41-10, sesja lokalna): nagłówek „Permissions · this session”, pozycje w kolejności ze zrzutu (Auto, Manual, Accept edits, Plan, Bypass permissions) z podpisem pod nazwą i haczykiem przy bieżącym trybie; napisy w strona/aplikacja-ekran.js, wiersze wybiera klik w kroku `tryb`. */

/* Lista trybów: Auto tylko, gdy jest dostępny (`aplikacja.auto_dostepny`), Bypass permissions tylko po włączeniu na koncie (`aplikacja.bypass_dostepny: true`, fakt aplikacja-dostepne-tryby: „appears in the mode selector once enabled”). Haczyk stawia PK.zaznaczTryb przy otwarciu. */
PK.menuTrybow = (auto, bypass = false) => {
  const T = PK.NAPISY_EKRANU.tryby;
  const ptak = `<span class="apl-ptak" aria-hidden="true">${PK.IKONY_ZGODY.tak}</span>`;
  const pozycje = PK.TRYBY_APLIKACJI.filter((t) => auto || t !== "Auto").concat(bypass ? ["Bypass permissions"] : []);
  const wiersze = pozycje
    .map(
      (t) =>
        `<li role="none"><button type="button" class="apl-menu-poz apl-tryb-poz" role="menuitem" data-tryb="${PK.esc(t)}"><span class="apl-tryb-nazwa">${PK.esc(t)}</span>${ptak}<small>${PK.esc(T[t])}</small></button></li>`,
    )
    .join("");
  return `<ul class="apl-menu-trybow" role="menu" hidden><li role="presentation" class="apl-menu-naglowek">${PK.esc(T.naglowek)}</li>${wiersze}</ul>`;
};

/* Haczyk przy trybie `tryb` (napis przełącznika w chwili otwarcia menu); `null` zdejmuje go przy zamknięciu. */
PK.zaznaczTryb = (menu, tryb) =>
  menu.querySelectorAll(".apl-tryb-poz").forEach((b) => b.classList.toggle("wybrany", b.dataset.tryb === tryb));
