/* Symulator aplikacji Claude, drogi: karta zgody na przepływ (krok `przeplyw`: nazwa i fazy, wiersz ostrzeżenia o zużyciu tokenów i trzy przyciski Once, Always, Deny) i klik `once`, po którym karta traci przyciski i ostrzeżenie, a przepływ dostaje wpis w pracy w tle (strona/aplikacja-w-tle.js). Z dokumentacji (fakt przeplyw-aplikacja-karta-zgody) pochodzą: istnienie karty, nazwa przepływu, lista faz, ostrzeżenie o zużyciu tokenów i trzy napisy przycisków (dokumentacja je tylko wymienia). Umowy symulatora, bez źródła: miejsce karty w rozmowie i ramka; kolejność przycisków Once, Always, Deny w rzędzie; ostrzeżenie jako znak ⚠ i szary pasek bez tekstu; tylko Once aktywny, Always i Deny wyszarzone bez skutku (D-2026-10-26-54); stan po Once to sama ramka z nazwą i fazami. */

/* Napisy interfejsu aplikacji, które rysuje ten plik, (kolejność w rzędzie to umowa symulatora); test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). Klucze to cele przycisków (cel kroku `klik` ma tylko once). */
PK.NAPISY_PRZEPLYWU = { once: "Once", always: "Always", deny: "Deny" };
PK.OPIS_OSTRZEZENIA_PRZEPLYWU = "Ostrzeżenie o zużyciu tokenów"; /* dla czytnika ekranu: dokumentacja podaje tylko, że karta ma ostrzeżenie, nie jego treść */

/* Znacznik „kliknij tutaj” stoi pod ramką karty, czyli pod rzędem przycisków, ze strzałką na Once (PK.celKroku). */
PK.PO_CELU_KROKU.once = ".apl-plik";
PK.SELEKTORY_PRZEPLYWU = { once: '.apl-zgoda-przeplyw [data-cel="once"]' };
PK.PRZYCISK_PRZEPLYWU = ".apl-zgoda-przeplyw .apl-plan-p";

PK.IKONA_OSTRZEZENIA =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17.2v.1"/></svg>';

/* Karta w rozmowie pod odpowiedzią Claude: w ramce w kolorach okna nazwa przepływu (dana scenariusza), fazy jako punkty, wiersz ostrzeżenia (znak i szary pasek bez tekstu) i rząd przycisków. Once jest główny i aktywny, Always i Deny wyszarzone (aria-disabled), klik w nie niczego nie robi. */
PK.kartaPrzeplywu = (k) => {
  const { esc } = PK;
  const przycisk = (c) =>
    `<button type="button" class="apl-plan-p${c === "once" ? " apl-plan-glowny" : ""}" data-cel="${c}"${c === "once" ? "" : ' aria-disabled="true"'}>${esc(PK.NAPISY_PRZEPLYWU[c])}</button>`;
  return (
    `<div class="apl-zgoda apl-zgoda-przeplyw"><section class="apl-plik"><div class="apl-przeplyw-tresc">` +
    `<b class="apl-przeplyw-nazwa">${esc(k.nazwa)}</b>` +
    `<ul class="apl-przeplyw-fazy">${k.fazy.map((f) => `<li>${esc(f)}</li>`).join("")}</ul>` +
    `<div class="apl-przeplyw-ostrz" role="img" aria-label="${esc(PK.OPIS_OSTRZEZENIA_PRZEPLYWU)}">${PK.IKONA_OSTRZEZENIA}${PK.szaryPasek(58)}</div></div>` +
    `<div class="apl-plan-przyciski">${Object.keys(PK.NAPISY_PRZEPLYWU).map(przycisk).join("")}</div></section></div>`
  );
};

/* Po Once karta zostaje w rozmowie jako sama ramka z nazwą i fazami: znikają wiersz ostrzeżenia i przyciski. */
PK.zatwierdzPrzeplyw = (karta) => {
  karta.classList.add("zatwierdzona");
  karta.querySelector(".apl-przeplyw-ostrz").remove();
  karta.querySelector(".apl-plan-przyciski").remove();
};

/* Nazwa przepływu z karty, na którą kliknięto Once: tytuł wpisu w panelu zadań w tle. */
PK.nazwaPrzeplywu = (karta) => karta.querySelector(".apl-przeplyw-nazwa").textContent;
