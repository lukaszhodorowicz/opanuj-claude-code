/* Symulator aplikacji Claude, widok strony artefaktu w panelu Browser: nagłówek (tytuł, Share i puste kółko autora albo napis dla gościa) nad stroną oferty, przełącznik kursu „Tak widzisz Ty / Tak zobaczy klient” i podmiana strony w miejscu. */

/* Napisy interfejsu claude.ai, które rysuje ten plik; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: claude.ai). */
PK.NAPISY_CLAUDE_AI = {
  share: "Share",
  gosc: "Content is user-generated and unverified.",
};

/* Widok artefaktu: dane {tytul, strona?} albo {tytul, slajdy} (edytor prezentacji z strona/aplikacja-slajdy.js); nagłówek zawsze kolorowy (konwencja kursu, D-2026-10-26-54); widok "ty" (Share i puste kółko autora) albo "klient" (napis zamiast kółka, bez Share; z `objasnienie` pod nagłówkiem mała nota kursu po polsku, przy napisie gościa). Bez paska adresu i przycisków przeglądarki. */
PK.artefaktAplikacji = (dane, widok, objasnienie) => {
  if (dane.slajdy) return PK.slajdyAplikacji(dane); /* prezentacja: edytor slajdów, bez widoku klienta */
  const { esc } = PK;
  const N = PK.NAPISY_CLAUDE_AI;
  const prawa =
    widok === "klient"
      ? `<span class="apl-art-gosc">${esc(N.gosc)}</span>`
      : `<span class="apl-art-share">${esc(N.share)}</span><span class="apl-art-autor" aria-hidden="true"></span>`;
  return (
    `<section class="apl-przegladarka apl-artefakt" data-widok="${widok}">` +
    `<header class="apl-art-glowa"><b class="apl-art-tytul">${esc(dane.tytul)}</b><span class="apl-art-prawa">${prawa}</span></header>` +
    (widok === "klient" && objasnienie ? `<p class="apl-art-objasnienie">${esc(objasnienie)}</p>` : "") +
    (dane.strona ? PK.stronaOferty(dane.strona) : "") +
    "</section>"
  );
};

/* Podgląd w tekście lekcji: widok „ty” albo „klient” z podpisem kursu nad nim, bez przełącznika. */
PK.artefaktPodglad = (cw, dane, widok) => {
  const { esc } = PK;
  const wk = cw.widok_klienta || {};
  const klient = widok === "klient";
  const etykieta = klient ? wk.klient : wk.ty;
  const podpis = klient && wk.podpis ? `<p class="apl-art-podpis">${esc(wk.podpis)}</p>` : "";
  const kurs = etykieta ? `<div class="apl-art-kurs"><span class="apl-art-etykieta">${esc(etykieta)}</span>${podpis}</div>` : "";
  return kurs + PK.artefaktAplikacji(dane, klient ? "klient" : "ty", wk.objasnienie);
};

/* Widok artefaktu w ćwiczeniu z drogami: `widok` to miejsce na otwarty plik (.apl-widok-pliku), `okno` dostaje klasę plik-otwarty. Zwraca {krok, zamknij, reset}: krok `artefakt` otwiera widok albo, gdy jest otwarty, podmienia stronę w miejscu; reset zamyka go i otwiera od nowa, gdy ćwiczenie ma aplikacja.artefakt_otwarty. */
PK.artefaktCwiczenia = function (cw, okno, widok) {
  const { esc } = PK;
  const wk = cw.widok_klienta;
  const start = (cw.aplikacja || {}).artefakt_otwarty || null;
  let dane = null;
  let tryb = "ty";

  const wstaw = (html) => {
    const t = document.createElement("template");
    t.innerHTML = html;
    return t.content.firstElementChild;
  };
  const kurs = () => {
    if (!wk) return "";
    const wybor = (t) =>
      `<button type="button" class="apl-art-wybor${t === tryb ? " wybrany" : ""}" data-widok="${t}" aria-pressed="${t === tryb}">${esc(wk[t])}</button>`;
    return (
      '<div class="apl-art-kurs"><div class="apl-art-przelacznik" role="group">' +
      `${wybor("ty")}${wybor("klient")}</div>` +
      `<p class="apl-art-podpis"${tryb === "klient" ? "" : " hidden"}>${esc(wk.podpis)}</p></div>`
    );
  };
  const rysuj = (nowa) => {
    const el = wstaw(PK.artefaktAplikacji(dane, tryb, wk && wk.objasnienie));
    const strona = el.querySelector(".apl-prz-strona");
    if (nowa && strona) strona.classList.add("apl-art-nowa"); /* podmiana w miejscu: nowa strona błyska */
    return el;
  };

  let przebieg = 0; /* numer otwarcia: zamknięcie przerywa animację tworzenia slajdów */
  function otworz(d) {
    dane = d;
    tryb = "ty";
    przebieg++;
    widok.innerHTML = d.slajdy ? "" : kurs();
    widok.append(rysuj(false));
    widok.classList.add("apl-art-widok");
    widok.hidden = false;
    okno.classList.add("plik-otwarty");
  }
  const podmien = (d) => {
    dane = d;
    widok.querySelector(".apl-artefakt, .apl-slajdy").replaceWith(rysuj(true));
  };
  /* Prezentacja otwarta krokiem: animacja tworzenia, potem znacznik „kliknij tutaj” na strzałce „dalej”. */
  async function tworzSlajdy() {
    const nr = przebieg;
    const ed = widok.querySelector(".apl-slajdy");
    /* wąski ekran: edytor stoi pod rozmową, poza oknem; przewijamy na początku do strzałki „dalej” (slajd, znacznik i strzałka mają razem ok. 205 px), jak `wskazKlienta` */
    const strzalka = ed.querySelector('.apl-sl-strzalka[data-krok="1"]');
    if (strzalka) strzalka.scrollIntoView({ block: "center" });
    await PK.slajdyTworz(ed, () => nr === przebieg && ed.isConnected);
    if (nr !== przebieg || !ed.isConnected) return;
    const dalej = ed.querySelector('.apl-sl-strzalka[data-krok="1"]:not([disabled])');
    if (dalej) PK.celAplikacji(okno.parentElement, dalej);
  }
  function ustaw(t) {
    tryb = t;
    widok.querySelectorAll(".apl-art-wybor").forEach((b) => {
      b.classList.toggle("wybrany", b.dataset.widok === t);
      b.setAttribute("aria-pressed", b.dataset.widok === t);
    });
    const podpis = widok.querySelector(".apl-art-podpis");
    if (podpis) podpis.hidden = t !== "klient";
    widok.querySelector(".apl-artefakt").replaceWith(rysuj(false));
  }
  /* Znacznik „kliknij tutaj” (ten z PK.celAplikacji) na przycisku `klient`; gdy przełącznik wypada poza oknem przeglądarki (wąski ekran), przewija do niego stronę tak, jak przewija ją reszta kursu (łagodnie). */
  const wskazKlienta = () => {
    const sek = okno.parentElement;
    const przycisk = widok.querySelector('.apl-art-wybor[data-widok="klient"]');
    PK.celAplikacji(sek, przycisk);
    const dol = widok.querySelector(".apl-tag").getBoundingClientRect().bottom; /* znacznik stoi pod przyciskiem */
    if (przycisk.getBoundingClientRect().top >= 0 && dol <= window.innerHeight) return;
    przycisk.scrollIntoView({ block: "center" });
  };
  widok.addEventListener("click", (e) => {
    const b = e.target.closest(".apl-art-wybor");
    if (!b) return;
    if (b.dataset.widok === "klient" && b.classList.contains("apl-cel")) PK.celAplikacji(okno.parentElement, null);
    ustaw(b.dataset.widok);
  });

  return {
    dane: () => dane, /* dane otwartego widoku (tytul i strona albo slajdy); null, gdy nic nie jest otwarte (strona/aplikacja-edytor-gra.js rozwija z nich edytor prezentacji) */
    krok(k) {
      if (dane) return podmien(k);
      otworz(k);
      if (k.slajdy) return tworzSlajdy(); /* aplikacja.js czeka na koniec animacji */
      if (wk) wskazKlienta();
    },
    /* zamyka widok (krok `plik` zajmuje panel); kolejny krok `artefakt` otwiera go od nowa */
    zamknij() {
      przebieg++;
      dane = null;
      tryb = "ty";
      widok.hidden = true;
      widok.innerHTML = "";
      widok.classList.remove("apl-art-widok");
      okno.classList.remove("plik-otwarty");
    },
    reset() {
      this.zamknij();
      if (start) otworz(start);
    },
  };
};
