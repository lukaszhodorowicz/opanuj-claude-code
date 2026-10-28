/* Silnik strony lekcji: czyta scenariusz, quiz i fiszki z JSON na stronie i buduje z nich ćwiczenia, podglądy folderu, quiz oraz fiszki. */
(() => {
  const { esc, czekaj } = PK;
  const wez = (id) => document.getElementById(id);
  const dane = (id) => {
    const e = wez(id);
    return e ? JSON.parse(e.textContent) : null;
  };
  const SCEN = dane("scenariusz") || { cwiczenia: [] };
  const FOLDER = SCEN.folder_startowy || [];
  const TYTUL_TERMINALA = SCEN.terminal_tytul || "claude";
  const NAZWA_FOLDERU = TYTUL_TERMINALA.replace(/^~\//, "");
  const IKONA_STARTU =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg>';

  const NAGLOWEK = (cw, nr) =>
    '<div class="naglowek"><span class="etykieta">Ćwiczenie ' +
    nr +
    "</span><h3>" +
    esc(cw.tytul) +
    "</h3></div>" +
    (cw.opis ? '<p class="opis">' + esc(cw.opis) + "</p>" : "");
  const sekcja = (host, cw, html) => {
    host.innerHTML =
      '<section class="cwiczenie" id="' +
      esc(cw.id) +
      '">' +
      html +
      "</section>";
    return host.firstElementChild;
  };

  /* ---------- porównanie i pojedynczy terminal z zadaniami ---------- */
  /* Układ zawsze ten sam: nauczyciel, polecenia, okna; w oknie terminal, pod nim folder, pod folderem legenda. */
  function zadaniowe(cw, host, nr) {
    const jedno = cw.rodzaj === "pojedynczy";
    const zadania = cw.zadania || [];
    const maFolder =
      !jedno ||
      zadania.some((z) =>
        JSON.stringify(z.przebiegi).includes('"typ":"folder"'),
      );
    const doKlikniecia = zadania.filter((z) => !z.start_od_razu);
    const okno = (ter) =>
      '<div class="okno" data-o="' +
      esc(ter.id) +
      '" data-tryb="' +
      esc(ter.tryb || "manual") +
      '">' +
      (jedno
        ? ""
        : '<p class="podpis-okna"><b>' +
          esc(ter.podpis) +
          "</b><span>" +
          esc(ter.dopisek || "") +
          "</span></p>") +
      '<div class="term" data-t="' +
      esc(ter.id) +
      '"></div>' +
      (maFolder ? '<div class="pulpit"></div>' : "") +
      '<div class="legenda" hidden></div></div>';
    const polecenie = (z) =>
      '<button class="polecenie" data-z="' +
      zadania.indexOf(z) +
      '"><span class="polecenie-ikona">' +
      IKONA_STARTU +
      '</span><span class="polecenie-tekst"><b>' +
      esc(z.etykieta) +
      "</b>" +
      (z.opis ? "<small>" + esc(z.opis) + "</small>" : "") +
      "</span></button>";
    const sek = sekcja(
      host,
      cw,
      NAGLOWEK(cw, nr) +
        PK.nauczycielHtml(cw.nauczyciel_start) +
        (doKlikniecia.length
          ? '<div class="polecenia">' +
            doKlikniecia.map(polecenie).join("") +
            "</div>"
          : "") +
        '<div class="okna' +
        (jedno ? "" : " dwa") +
        '">' +
        (cw.terminale || []).map(okno).join("") +
        "</div>" +
        (jedno
          ? '<div class="przycisk-klaw"><button class="btn jasny" data-od-nowa>' +
            esc(cw.przycisk || "Od nowa") +
            "</button><small>Ćwiczenie zacznie się od początku.</small></div>"
          : ""),
    );
    const kolumny = [...sek.querySelectorAll(".okno")];
    const mow = PK.Nauczyciel(
      sek.querySelector(".nauczyciel"),
      (cw.terminale || []).map((ter, i) => ({
        id: ter.id,
        podpis: ter.podpis,
        kol: kolumny[i],
      })),
    );
    const okienka = (cw.terminale || []).map((ter, i) => {
      const kol = kolumny[i];
      const el = kol.querySelector(".term");
      if (jedno) el.tabIndex = 0;
      return {
        id: ter.id,
        tryb: ter.tryb || "manual",
        t: PK.Terminal(el, {
          tryb: ter.tryb,
          tytul: TYTUL_TERMINALA,
          legenda: kol.querySelector(".legenda"),
        }),
        f: PK.Folder(kol.querySelector(".pulpit"), FOLDER, {
          nazwa: NAZWA_FOLDERU,
          cele: cw.cele,
        }),
      };
    });
    let ostatnie = null;

    async function uruchom(zad) {
      ostatnie = zad;
      sek
        .querySelectorAll(".polecenie")
        .forEach((b) =>
          b.classList.toggle("wyslane", +b.dataset.z === zadania.indexOf(zad)),
        );
      okienka.forEach((o) => {
        o.t.wyczysc();
        o.f.reset();
        o.t.ustawTryb(o.tryb);
        o.g = o.t.gen;
      });
      mow(
        jedno
          ? cw.nauczyciel_start
          : "Patrz, które okno zmienia pliki w folderze.",
        null,
        "polecenie", /* nowe polecenie albo „Od nowa”: mocny sygnał dymka */
      );
      const wyniki = await Promise.all(
        okienka.map((o) => o.t.pisz(zad.polecenie, o.g)),
      );
      if (wyniki.includes(false)) return;
      for (const o of okienka) {
        PK.graj(
          { t: o.t, f: o.f, g: o.g, n: (s) => mow(s, o.id) },
          (zad.przebiegi || {})[o.id],
        );
        await czekaj(200);
      }
    }

    sek
      .querySelectorAll(".polecenie")
      .forEach((b) =>
        b.addEventListener("click", () => uruchom(zadania[+b.dataset.z])),
      );
    const odNowa = sek.querySelector("[data-od-nowa]");
    if (odNowa)
      odNowa.addEventListener("click", () =>
        uruchom(ostatnie || zadania.find((z) => z.start_od_razu) || zadania[0]),
      );
    const start = zadania.find((z) => z.start_od_razu);
    if (start) uruchom(start);
    else if (location.hash === "#start" && !jedno && zadania[0])
      uruchom(zadania[0]);
  }

  /* ---------- przełącznik trybów klawiszami Shift + Tab ---------- */
  function przelacznik(cw, host, nr) {
    const cykl = cw.cykl || ["manual", "edycje", "plan"];
    const sek = sekcja(
      host,
      cw,
      NAGLOWEK(cw, nr) +
        PK.nauczycielHtml(cw.nauczyciel_start) +
        '<div class="term" tabindex="0" aria-label="Terminal do ćwiczenia: naciśnij Shift+Tab"></div>' +
        '<div class="przycisk-klaw"><button class="btn jasny" data-shift>⇧ Shift + Tab</button>' +
        '<button class="btn jasny" data-reset>Od nowa</button></div>',
    );
    const el = sek.querySelector(".term");
    const mow = PK.Nauczyciel(sek.querySelector(".nauczyciel"), []);
    const t = PK.Terminal(el, {
      tryb: cykl[0],
      niski: true,
      tytul: TYTUL_TERMINALA,
    });
    function start() {
      t.wyczysc();
      t.ustawTryb(cykl[0]);
      if (cw.tekst_startowy)
        t.dodaj('<span class="wynik">' + esc(cw.tekst_startowy) + "</span>");
      mow(cw.nauczyciel_start, null, "polecenie"); /* początek i „Od nowa”: mocny sygnał dymka */
    }
    function przelacz() {
      const nast = cykl[(cykl.indexOf(t.tryb) + 1) % cykl.length];
      t.ustawTryb(nast, true);
      mow((cw.komentarze || {})[nast] || ""); /* kolejny tryb: sygnał kroku */
    }
    el.addEventListener("keydown", (e) => {
      if (e.key === "Tab" && e.shiftKey) {
        e.preventDefault();
        przelacz();
      }
    });
    sek.querySelector("[data-shift]").addEventListener("click", przelacz);
    sek.querySelector("[data-reset]").addEventListener("click", start);
    start();
  }

  /* ---------- ćwiczenia w miejscach znaczników ---------- */
  (SCEN.cwiczenia || []).forEach((cw, i) => {
    const host = document.querySelector(
      '.miejsce-cwiczenia[data-id="' + cw.id + '"]',
    );
    if (!host) return;
    if (cw.rodzaj === "przelacznik") przelacznik(cw, host, i + 1);
    else if (cw.rodzaj === "aplikacja") PK.aplikacja(cw, host, i + 1);
    else zadaniowe(cw, host, i + 1);
  });

  /* ---------- podglądy folderu w tekście lekcji: stan po przebiegu ze scenariusza ---------- */
  document.querySelectorAll(".podglad[data-cw]").forEach((el) => {
    const cw = (SCEN.cwiczenia || []).find((c) => c.id === el.dataset.cw);
    const zad = cw && (cw.zadania || [])[0];
    const kroki = zad && (zad.przebiegi || {})[el.dataset.t];
    if (!kroki) return;
    const f = PK.Folder(el, FOLDER, { nazwa: NAZWA_FOLDERU, statyczny: true });
    PK.krokiFolderu(kroki, [], Number(el.dataset.opcja || 0)).forEach(f.zastosuj);
  });

  /* ---------- quiz ---------- */
  const quiz = (dane("quiz") || {}).pytania || dane("quiz") || [];
  const lista = Array.isArray(quiz) ? quiz : [];
  if (!lista.length && wez("sekcja-quiz")) wez("sekcja-quiz").hidden = true;
  let punkty = 0;
  let odpowiedzi = 0;
  lista.forEach((q, i) => {
    const box = document.createElement("div");
    box.className = "pytanie";
    box.innerHTML =
      '<div class="tresc">' + (i + 1) + ". " + esc(q.pytanie) + "</div>";
    const wyj = document.createElement("div");
    wyj.className = "wyjasnienie";
    wyj.textContent = q.wyjasnienie || "";
    const btns = q.odpowiedzi.map((o, j) => {
      const b = document.createElement("button");
      b.className = "odp";
      b.textContent = o;
      b.addEventListener("click", () => {
        btns.forEach((x) => (x.disabled = true));
        btns[q.poprawna].classList.add("dobra");
        if (j !== q.poprawna) b.classList.add("zla");
        else punkty++;
        odpowiedzi++;
        wyj.classList.add("widac");
        if (odpowiedzi === lista.length)
          wez("quiz-wynik").textContent =
            "Wynik: " +
            punkty +
            " z " +
            lista.length +
            (punkty === lista.length
              ? ". Komplet!"
              : ". Wróć do ćwiczeń przy pytaniach z błędem.");
      });
      box.appendChild(b);
      return b;
    });
    box.appendChild(wyj);
    wez("quiz-lista").appendChild(box);
  });

  /* ---------- fiszki ---------- */
  const fiszki = (dane("fiszki") || {}).fiszki || dane("fiszki") || [];
  const talia = Array.isArray(fiszki) ? fiszki : [];
  if (!talia.length && wez("sekcja-fiszki")) wez("sekcja-fiszki").hidden = true;
  talia.forEach((f) => {
    const b = document.createElement("button");
    b.className = "fiszka";
    b.innerHTML =
      '<div class="wnetrze"><div class="strona-f przod">' +
      esc(f.przod) +
      '</div><div class="strona-f tyl">' +
      esc(f.tyl) +
      "</div></div>";
    b.addEventListener("click", () => b.classList.toggle("odwrocona"));
    wez("fiszki-lista").appendChild(b);
  });
})();
