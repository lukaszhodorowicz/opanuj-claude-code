/* Symulator aplikacji Claude, karta planu: krok `plan` w ćwiczeniu z etapami rysuje w rozmowie kartę „Claude proposed a plan” z przyciskami (Reject, Revise…, Accept, Accept and auto mode, ▾), pole poprawki po „Revise…” i panel Plan otwierany odnośnikiem „Open plan” (D-2026-10-26-54; grę prowadzi strona/aplikacja-tryby.js). */

/* Napisy z klatek filmów (najnowszy wygląd: plan-11, 12.10.2026; skutki przycisków: plan-skutek-*), adresy i sekundy w dane/napisy-interfejsu.yaml. */
PK.NAPISY_PLANU = {
  proponuje: "Proposing plan",
  zaproponowal: "Proposed plan",
  karta: "Claude proposed a plan",
  otworz: "Open plan",
  reject: "Reject",
  revise: "Revise…",
  esc: "Esc",
  accept: "Accept",
  skrot_accept: "⇧⌘⏎",
  auto: "Accept and auto mode",
  skrot_auto: "⌘⏎",
  panel: "Plan",
  podpowiedz: "Select any text to leave a comment for Claude",
  co_zmienic: "What should change? (optional)",
  wroc: "Back",
  wyslij: "Revise",
  enter: "Enter",
};

PK.IKONY_PLANU = (() => {
  const s = (d) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    dalej: s('<path d="m9.5 6 6 6-6 6"/>'),
    rozwin: s('<path d="m7 10 5 5 5-5"/>'),
    folder: s('<path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>'),
    oderwij: s('<rect x="8" y="8" width="11.5" height="11.5" rx="2"/><path d="M15.5 8V6a1.5 1.5 0 0 0-1.5-1.5H6A1.5 1.5 0 0 0 4.5 6v8A1.5 1.5 0 0 0 6 15.5h2"/>'),
    powieksz: s('<path d="M14 4h6v6M20 4l-6.5 6.5M10 20H4v-6M4 20l6.5-6.5"/>'),
    zamknij: s('<path d="M6 6l12 12M18 6 6 18"/>'),
    dymek: s('<path d="M5 5.5h14a1.5 1.5 0 0 1 1.5 1.5v8.5A1.5 1.5 0 0 1 19 17h-8l-4.5 3.5V17H5a1.5 1.5 0 0 1-1.5-1.5V7A1.5 1.5 0 0 1 5 5.5z"/>'),
  };
})();

/* Tryb przełącznika po kliknięciu (ZRODLA.md, część „Skutki przycisków”): revise zostawia Plan. */
PK.TRYB_PO_PLANIE = { accept: "Manual", auto: "Auto", revise: "Plan" };

/* Nagłówek karty: napis i odnośnik „Open plan” po prawej. */
PK.glowaPlanu = () =>
  `<div class="apl-plan-glowa"><b>${PK.esc(PK.NAPISY_PLANU.karta)}</b><button type="button" class="apl-plan-otworz">${PK.esc(PK.NAPISY_PLANU.otworz)}</button></div>`;

/* Wnętrze karty z przyciskami: aktywne tylko te, które mają klucz w `przyciski` kroku; Reject i ▾ zawsze nieaktywne (brak źródła skutku). */
PK.kartaPlanu = (k) => {
  const { esc } = PK;
  const N = PK.NAPISY_PLANU;
  const jest = (a) => !!(k.przyciski && k.przyciski[a]);
  const p = (akcja, t, klawisz, klasa = "", aktywny = jest(akcja)) =>
    `<button type="button" class="apl-plan-p${klasa}" data-akcja="${akcja}"${aktywny ? "" : " disabled"}>${esc(t)}${klawisz ? `<kbd>${esc(klawisz)}</kbd>` : ""}</button>`;
  return (
    PK.glowaPlanu() +
    '<div class="apl-plan-przyciski">' +
    `<span class="apl-plan-grupa">${p("reject", N.reject, "", "", false)}${p("revise", N.revise, N.esc)}</span>` +
    `<span class="apl-plan-grupa">${p("accept", N.accept, N.skrot_accept)}` +
    `<span class="apl-plan-para">${p("auto", N.auto, N.skrot_auto, " apl-plan-glowny")}` +
    `<button type="button" class="apl-plan-p apl-plan-glowny apl-plan-strzalka" data-akcja="rozwin" disabled aria-label="Więcej opcji (w tym ćwiczeniu nie działa)">${PK.IKONY_PLANU.rozwin}</button></span></span>` +
    "</div>"
  );
};

/* Wnętrze karty po „Revise…”: pole z szarą podpowiedzią (tekst poprawki wpisuje symulator), „Back” po lewej, „Revise” z „Enter” po prawej. */
PK.polePlanu = () => {
  const { esc } = PK;
  const N = PK.NAPISY_PLANU;
  return (
    PK.glowaPlanu() +
    `<div class="apl-plan-pole" data-podpowiedz="${esc(N.co_zmienic)}"></div>` +
    '<div class="apl-plan-przyciski">' +
    `<button type="button" class="apl-plan-p" data-akcja="wroc">${esc(N.wroc)}</button>` +
    `<button type="button" class="apl-plan-p apl-plan-glowny" data-akcja="wyslij" disabled>${esc(N.wyslij)}<kbd>${esc(N.enter)}</kbd></button>` +
    "</div>"
  );
};

/* Panel Plan: nagłówek z ikonami (działa tylko ✕), szara podpowiedź i plan jako dokument. */
PK.panelPlanu = (k) => {
  const { esc } = PK;
  const N = PK.NAPISY_PLANU;
  const I = PK.IKONY_PLANU;
  const sekcja = (s) =>
    `<h5>${esc(s.naglowek)}</h5><ul>${(s.punkty || []).map((t) => `<li>${esc(t)}</li>`).join("")}</ul>`;
  return (
    `<header class="apl-plan-panel-glowa"><b>${esc(N.panel)}</b><span class="apl-plan-ikony" aria-hidden="true">${I.folder}${I.oderwij}${I.powieksz}</span>` +
    `<button type="button" class="apl-plan-zamknij" aria-label="Zamknij panel">${I.zamknij}</button></header>` +
    `<p class="apl-plan-podp">${I.dymek}${esc(N.podpowiedz)}</p>` +
    `<div class="apl-plan-dok"><h4>${esc(k.tytul)}</h4>${(k.sekcje || []).map(sekcja).join("")}</div>`
  );
};

/* Karta planu jednego ćwiczenia. `dopisz(html)` dokłada element do rozmowy, `ustawTryb(t)` zmienia napis przełącznika, `graj(kroki)` gra kroki przycisku. Zwraca {pokaz(k), czeka(), ustawCel(), zamknijPanel(), zeruj()}. */
PK.planEtapow = (sek, { dopisz, ustawTryb, graj }) => {
  const { esc, czekaj } = PK;
  const N = PK.NAPISY_PLANU;
  const okno = sek.querySelector(".apl-okno");
  let karta = null; /* karta, która czeka na decyzję */
  let wiersz = null; /* wiersz „Proposing plan” nad kartą */
  let plan = null; /* krok `plan` tej karty */
  let pole = false; /* karta pokazuje pole poprawki */
  let otwarty = false; /* kursant otworzył panel z planem tej karty */
  let panel = null;
  let gen = 0; /* „Od nowa” i „Back” przerywają wpisywanie poprawki */

  function otworzPanel(k) {
    if (!panel) {
      panel = document.createElement("section");
      panel.className = "apl-plan-panel";
      sek.querySelector(".apl-uklad").appendChild(panel);
    }
    panel.innerHTML = PK.panelPlanu(k);
    panel.hidden = false;
    okno.classList.add("plan-otwarty");
  }
  function zamknijPanel() {
    if (panel) {
      panel.hidden = true;
      panel.innerHTML = "";
    }
    okno.classList.remove("plan-otwarty");
  }
  const panelOtwarty = () => !!panel && !panel.hidden;

  /* Następny ruch: „Open plan”, dopóki panel nie był otwarty; potem jedyny aktywny przycisk (przy kilku żaden, mówi nauczyciel); w polu poprawki „Revise”. */
  function cel() {
    if (!karta) return null;
    if (pole) return karta.querySelector('[data-akcja="wyslij"]:not([disabled])');
    if (!otwarty) return karta.querySelector(".apl-plan-otworz");
    const aktywne = karta.querySelectorAll("[data-akcja]:not([disabled])");
    return aktywne.length === 1 ? aktywne[0] : null;
  }
  function ustawCel() {
    const el = cel();
    PK.celPod(sek, el, el && karta);
  }

  function rysuj() {
    karta.innerHTML = pole ? PK.polePlanu() : PK.kartaPlanu(plan);
    ustawCel();
  }

  async function wpisz(tekst) {
    const g = gen;
    const el = karta.querySelector(".apl-plan-pole");
    await czekaj(500);
    for (let i = 1; i <= tekst.length; i += 2) {
      if (g !== gen) return;
      el.textContent = tekst.slice(0, i);
      await czekaj(30);
    }
    if (g !== gen) return;
    el.textContent = tekst;
    karta.querySelector('[data-akcja="wyslij"]').disabled = false;
    ustawCel();
  }

  /* Accept, Accept and auto mode i wysłana poprawka: karta znika, wiersz nad nią mówi „Proposed plan”, przełącznik pokazuje tryb po kliknięciu, potem grają kroki przycisku. */
  function decyzja(klucz) {
    const p = plan.przyciski[klucz];
    karta.remove();
    karta = null;
    pole = false;
    gen++;
    wiersz.firstChild.textContent = N.zaproponowal;
    PK.celPod(sek, null);
    if (klucz === "revise") dopisz(PK.dymekAplikacji({ kto: "ty", tekst: p.poprawka }));
    ustawTryb(PK.TRYB_PO_PLANIE[klucz]);
    graj(p.kroki || []);
  }

  okno.addEventListener("click", (ev) => {
    if (ev.target.closest(".apl-plan-zamknij")) {
      zamknijPanel();
      /* okno się poszerzyło: znacznik liczy położenie od nowa (jak po otwarciu widoku zmian w aplikacja-tryby.js) */
      sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
      return;
    }
    if (!karta || !karta.contains(ev.target)) return;
    if (ev.target.closest(".apl-plan-otworz")) {
      otwarty = true;
      otworzPanel(plan);
      return ustawCel();
    }
    const b = ev.target.closest("button[data-akcja]");
    if (!b || b.disabled) return;
    const a = b.dataset.akcja;
    if (a === "revise") {
      pole = true;
      rysuj();
      wpisz(plan.przyciski.revise.poprawka);
    } else if (a === "wroc") {
      pole = false;
      gen++;
      rysuj();
    } else if (a === "wyslij") decyzja("revise");
    else if (a === "accept" || a === "auto") decyzja(a);
  });

  return {
    /* Krok `plan`: wiersz „Proposing plan” i karta; otwarty panel od razu pokazuje nowy plan. */
    pokaz(k) {
      wiersz = dopisz(`<p class="apl-plan-proponuje">${esc(N.proponuje)}${PK.IKONY_PLANU.dalej}</p>`);
      karta = dopisz('<div class="apl-plan-karta"></div>');
      plan = k;
      pole = otwarty = false;
      karta.innerHTML = PK.kartaPlanu(k);
      if (panelOtwarty()) otworzPanel(k);
      otwarty = panelOtwarty();
    },
    /* Karta czeka na decyzję, gdy ma choć jeden działający przycisk. */
    czeka: () =>
      !!karta && ["accept", "auto", "revise"].some((a) => plan.przyciski && plan.przyciski[a]),
    ustawCel,
    zamknijPanel,
    zeruj() {
      gen++;
      karta = wiersz = plan = null;
      pole = otwarty = false;
      zamknijPanel();
    },
  };
};
