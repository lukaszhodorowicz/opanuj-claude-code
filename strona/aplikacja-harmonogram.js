/* Symulator aplikacji Claude, zadanie według harmonogramu, działanie (ćwiczenie z drogami i polem `aplikacja.harmonogram`): pozycja Scheduled w pasku bocznym, strona Scheduled tasks, okno New scheduled task z sekcją Advanced settings i strona zadania; kroki `klik` z celami scheduled, new-task, advanced-settings, create i run-now (znacznik „kliknij tutaj”, czekanie na klik, skutek), wpis historii po Run now i komunikat po Create (część „Zadanie według harmonogramu” w dane/FORMAT-SCENARIUSZA.md). Wygląd: strona/aplikacja-harmonogram-widok.js, strona/styl-aplikacja-harmonogram.css. */

PK.CELE_HARMONOGRAMU = ["scheduled", "new-task", "advanced-settings", "create", "run-now"];
PK.KOMUNIKAT_HARMONOGRAMU_MS = 5000; /* komunikat „… created.” po Create znika po chwili, jak w aplikacji */

/* Element, za którym stoi rząd ze znacznikiem „kliknij tutaj” (pod nim): pozycja paska bocznego, rząd z przyciskiem New task, nagłówek sekcji Advanced settings, rząd z przyciskiem Run now; Create dostaje znacznik nad przyciskiem (PK.celAplikacji). */
Object.assign(PK.PO_CELU_KROKU, { scheduled: "li", "new-task": ".apl-harm-gora", "advanced-settings": ".apl-harm-zaaw-glowa", "run-now": ".apl-harm-zadanie-gora" });

/* Strony harmonogramu w ćwiczeniu `sek` z oknem `okno` (z htmlAplikacji); null bez `aplikacja.harmonogram` (reszta ćwiczeń zostaje bez zmian). Zwraca {dotyczy, klik, reset}. Okno ma atrybut `data-harm`: „lista” (strona Scheduled tasks), „okno” (New scheduled task nad nią) albo „zadanie” (strona zadania); bez niego widać rozmowę. */
PK.harmonogramAplikacji = function (cw, sek, okno) {
  const { czekaj, esc } = PK;
  const h = cw.aplikacja && cw.aplikacja.harmonogram;
  if (!h) return null;
  const dotyczy = (k) => k.typ === "klik" && PK.CELE_HARMONOGRAMU.includes(k.cel);
  const bok = okno.querySelector(".apl-bok-lista");
  const glowna = okno.querySelector(".apl-glowna");
  const dostosuj = [...bok.children].find((li) => li.textContent.trim() === PK.NAPISY_EKRANU.bok.dostosuj);
  (dostosuj || bok.lastElementChild).insertAdjacentHTML("afterend", PK.pozycjaScheduled());
  glowna.insertAdjacentHTML("beforeend", `<section class="apl-harm">${PK.stronaScheduled()}${PK.stronaZadania(h)}</section>`);
  okno.insertAdjacentHTML("beforeend", PK.oknoHarmonogramu(h));
  const pozycja = bok.querySelector(".apl-bok-harm");
  const strona = glowna.querySelector(".apl-harm");
  const tlo = okno.querySelector(".apl-harm-tlo");
  const srodek = tlo.querySelector(".apl-harm-srodek");
  const naglowekZaaw = tlo.querySelector(".apl-harm-zaaw-glowa");
  const tresc = tlo.querySelector(".apl-harm-zaaw-tresc");
  const historia = strona.querySelector(".apl-harm-hist-tresc");
  const komunikat = strona.querySelector(".apl-harm-komunikat");
  let czeka = null; /* {els, pusc}: elementy, których kliknięcie kończy czekający krok */
  let rozwiniete = false;
  let zegar = null;

  const pokaz = (widok) => {
    if (widok) okno.dataset.harm = widok;
    else delete okno.dataset.harm;
    okno.classList.toggle("harm-otwarte", !!widok);
  };
  const rozwin = (tak) => {
    rozwiniete = tak;
    naglowekZaaw.setAttribute("aria-expanded", String(tak));
    tlo.querySelector(".apl-harm-zaaw").classList.toggle("rozwinieta", tak);
  };
  const zakladka = (z) => {
    tresc.dataset.zakl = z;
    tresc.querySelectorAll("[data-z]").forEach((b) => b.classList.toggle("wybrana", b.dataset.z === z));
  };
  /* element(y) kroku: pierwszy dostaje znacznik; New task ma dwa przyciski (u góry i pod pustą listą), kliknięcie któregokolwiek kończy krok */
  const elementy = (cel) =>
    ({
      scheduled: [pozycja],
      "new-task": [...strona.querySelectorAll(".apl-harm-nowe")],
      "advanced-settings": [naglowekZaaw],
      create: [tlo.querySelector(".apl-harm-utworz")],
      "run-now": [strona.querySelector(".apl-harm-uruchom")],
    })[cel];
  /* środek okna przewija się tak, by element razem ze znacznikiem leżał w jego widocznym fragmencie (z zapasem na obramowanie zakreślacza) */
  const widocznyWOknie = (el) => {
    if (!el.closest(".apl-harm-srodek")) return;
    const rzad = sek.querySelector(".apl-tag-rzad");
    const s = srodek.getBoundingClientRect();
    const g = el.getBoundingClientRect();
    const dol = rzad ? rzad.getBoundingClientRect().bottom : g.bottom;
    if (g.top < s.top + 12) srodek.scrollTop -= s.top + 12 - g.top;
    else if (dol > s.bottom - 12) srodek.scrollTop += dol - s.bottom + 12;
  };
  /* drugi przycisk New task też kończy krok: dostaje „rękę” (klasa apl-cel-obok), znacznik stoi tylko na pierwszym */
  const obok = (els, tak) => els.slice(1).forEach((e) => e.classList.toggle("apl-cel-obok", tak));
  const skutek = (cel) => {
    if (cel === "scheduled") pokaz("lista");
    else if (cel === "new-task") pokaz("okno");
    else if (cel === "advanced-settings") {
      rozwin(true);
      srodek.scrollTop += naglowekZaaw.getBoundingClientRect().top - srodek.getBoundingClientRect().top - 8; /* sekcja rozwija się w dół: nagłówek idzie na górę widocznego fragmentu */
    } else if (cel === "create") {
      pokaz("zadanie");
      komunikat.hidden = false;
      clearTimeout(zegar);
      zegar = setTimeout(() => (komunikat.hidden = true), PK.KOMUNIKAT_HARMONOGRAMU_MS);
    } else historia.innerHTML = PK.wpisHistorii(); /* run-now: jeden wpis przebiegu */
  };

  /* Kursant klika tylko to, na co czeka krok (okno i strony leżą poza rozmową, więc strażnik kliku z aplikacja.js ich nie widzi); inne kliknięcia niczego nie robią. Zakładki sekcji Advanced settings i jej nagłówek działają zawsze (nie mają kroku). */
  sek.addEventListener("click", (e) => {
    const z = e.target.closest("[data-z]");
    if (z && tlo.contains(z)) zakladka(z.dataset.z);
    if (e.target.closest(".apl-harm-zaaw-glowa")) rozwin(!rozwiniete);
    if (czeka && czeka.els.some((x) => x.contains(e.target))) czeka.pusc(true);
  });
  zakladka("general");

  return {
    dotyczy,
    /* Znacznik „kliknij tutaj”, czekanie na klik i skutek. Krok advanced-settings nie czeka, gdy kursant już rozwinął sekcję. `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane. */
    async klik(k, zyje) {
      if (k.cel === "advanced-settings" && rozwiniete) return;
      const els = elementy(k.cel);
      PK.celKroku(sek, k.cel, els[0]);
      obok(els, true);
      widocznyWOknie(els[0]);
      const ok = await new Promise((pusc) => (czeka = { els, pusc }));
      czeka = null;
      if (!ok || !zyje()) return;
      PK.celKroku(sek, k.cel, null);
      obok(els, false);
      els[0].classList.add("wcisniety");
      await czekaj(200);
      els[0].classList.remove("wcisniety");
      if (zyje()) skutek(k.cel);
    },
    /* „Od nowa” i nowe polecenie: strony i okno zamknięte (widać rozmowę), sekcja zwinięta z zakładką General, historia pusta, komunikat schowany, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      clearTimeout(zegar);
      komunikat.hidden = true;
      pokaz(null);
      rozwin(false);
      zakladka("general");
      srodek.scrollTop = 0;
      historia.innerHTML = `<p>${esc(PK.NAPISY_HARMONOGRAMU.zadanie.brak)}</p>`;
      PK.celPod(sek, null);
      sek.querySelectorAll(".apl-cel-obok").forEach((e) => e.classList.remove("apl-cel-obok"));
    },
  };
};
