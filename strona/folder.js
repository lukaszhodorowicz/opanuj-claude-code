/* Podgląd folderu pod terminalem: pliki jako karty z ikoną, które przesuwają się do folderów, zmieniają nazwę albo zostają przekreślone, z licznikiem zmian. */
PK.IKONA_FOLDERU =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
  '<path d="M3 7.5V18a1.5 1.5 0 0 0 1.5 1.5h15A1.5 1.5 0 0 0 21 18V9.5A1.5 1.5 0 0 0 19.5 8h-7.6L10 5.5H4.5A1.5 1.5 0 0 0 3 7z"/>' +
  "</svg>";
PK.IKONA_PLIKU =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
  '<path d="M7 2.5h7l4.5 4.5v13.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-17a1 1 0 0 1 1-1z"/><path d="M14 2.5V7h4.5"/>' +
  '<path d="M9 11h6M9 14h4"/></svg>';
PK.IKONA_OKA =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
  '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/></svg>';

/* Liczba zmian po polsku: 1 zmiana, 2-4 zmiany, 5 zmian. */
PK.zmiany = (n) => {
  if (!n) return "bez zmian";
  const j = n % 10;
  const d = n % 100;
  if (n === 1) return "1 zmiana";
  return n + (j >= 2 && j <= 4 && (d < 12 || d > 14) ? " zmiany" : " zmian");
};

/* Tyle milisekund po zmianie nazwy karta pokazuje starą nazwę („było: …”). */
PK.NA_CHWILE = 3200;

/* el: element podglądu (null = folder bez rysowania); pliki: lista startowa; opcje: {nazwa, statyczny, cele}. */
PK.Folder = function (el, pliki, opcje = {}) {
  const { esc } = PK;
  const ruch =
    !opcje.statyczny &&
    !(
      window.matchMedia &&
      matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  /* nazwa łamie się tylko po „-”, „_”, „.” i „/” (etykieta teczki `.claude/skills/x`): tam stoi <wbr>, a CSS nie łamie w środku fragmentu */
  const lamany = (s) => esc(s).replace(/([-_./])/g, "$1<wbr>");
  /* teczka karty `Podfolder/plik` albo `a/b/c/plik`: wszystko przed ostatnim `/`, jedna teczka z etykietą tej ścieżki (bez teczki w teczce) */
  const teczkaPliku = (p) => p.slice(0, p.lastIndexOf("/"));
  const cele = opcje.cele || {}; /* plik → napis celu ćwiczenia, np. „ma zostać” */
  const f = {
    luzem: [],
    foldery: {},
    uwagi: {},
    nowe: new Set(),
    swieze: new Set(),
    byly: {} /* nowa nazwa → {stara, do: czas końca napisu „było”} */,
    usuniete: new Set(),
    swiezeKarty: new Set() /* karty zmienione w tym rysowaniu: z animacją */,
    zmian: 0,
    /* Miejsca dla znacznika treści pliku (strona/folder-tresc.js): klasy karty i napis pod nazwą. */
    klasyTresci: () => "",
    znacznik: () => "",
    /* Napis „było: …” po zmianie nazwy: w podglądzie statycznym zawsze, na żywo przez PK.NA_CHWILE. */
    bylo(p) {
      const b = f.byly[p];
      if (!b || (!opcje.statyczny && Date.now() >= b.do)) return "";
      const roz = (x) => (x.lastIndexOf(".") > 0 ? x.slice(x.lastIndexOf(".")) : "");
      const stara =
        roz(b.stara) === roz(p) && roz(p)
          ? b.stara.slice(0, -roz(p).length)
          : b.stara;
      return (
        '<span class="karta-bylo" title="' +
        esc("było: " + b.stara) +
        '">było:<s>' +
        lamany(stara) +
        "</s></span>"
      );
    },
    karta(p) {
      /* `Podfolder/plik` (ćwiczenia aplikacji): tożsamość karty to pełna ścieżka, napis to sama nazwa pliku */
      const n = p.slice(p.lastIndexOf("/") + 1);
      const kropka = n.lastIndexOf(".");
      const rozsz = kropka > 0 ? n.slice(kropka + 1) : "";
      const baza = kropka > 0 ? n.slice(0, kropka) : n;
      const u = f.uwagi[p];
      const usuniety = f.usuniete.has(p);
      const cel = cele[p] || (f.byly[p] && cele[f.byly[p].stara]);
      return (
        '<div class="karta karta-' +
        esc(rozsz.toLowerCase() || "plik") +
        (f.nowe.has(p) ? " nowy" : "") +
        (u && !usuniety ? " uwaga" : "") +
        (f.byly[p] ? " zmieniony" : "") +
        (usuniety ? " usuniety" : f.klasyTresci(p)) +
        (ruch && f.swiezeKarty.has(p) ? " swiezo" : "") +
        '" data-plik="' +
        esc(p) +
        '" title="' +
        esc(p) +
        '"><span class="karta-ikona">' +
        PK.IKONA_PLIKU +
        (rozsz ? "<i>" + esc(rozsz.toUpperCase()) + "</i>" : "") +
        '</span><span class="karta-nazwa">' +
        lamany(baza) +
        "</span>" +
        f.bylo(p) +
        (usuniety
          ? '<span class="karta-usuniety">usunięty</span>'
          : (u
              ? '<span class="karta-uwaga">' + esc(u) + "</span>"
              : cel
                ? '<span class="karta-cel">' + esc(cel) + "</span>"
                : "") + f.znacznik(p)) +
        "</div>"
      );
    },
    teczka(nazwa, w) {
      return (
        '<div class="teczka' +
        (f.swieze.has(nazwa) ? " nowa" : "") +
        '" data-teczka="' +
        esc(nazwa) +
        '"><div class="teczka-glowa">' +
        PK.IKONA_FOLDERU +
        "<span>" +
        lamany(nazwa) +
        "</span><em>" +
        w.filter((x) => !f.usuniete.has(x)).length +
        '</em></div><div class="teczka-wnetrze">' +
        w.map(f.karta).join("") +
        "</div></div>"
      );
    },
    rysuj(przybyly) {
      if (!el) return;
      const przed = {};
      if (ruch)
        el.querySelectorAll(".karta").forEach((k) => {
          przed[k.dataset.plik] = k.getBoundingClientRect();
        });
      const teczki = Object.entries(f.foldery);
      el.classList.add("pulpit");
      el.innerHTML =
        '<div class="pulpit-glowa">' +
        PK.IKONA_FOLDERU +
        "<b>" +
        esc(opcje.nazwa || "Folder") +
        '</b><span class="licznik' +
        (f.zmian ? " sa" : "") +
        '">' +
        PK.zmiany(f.zmian) +
        "</span></div>" +
        (teczki.length
          ? '<div class="pulpit-teczki">' +
            teczki.map(([n, w]) => f.teczka(n, w)).join("") +
            "</div>"
          : "") +
        '<div class="pulpit-luzem">' +
        f.luzem.map(f.karta).join("") +
        "</div>";
      f.swieze.clear();
      f.swiezeKarty.clear();
      if (!ruch) return;
      el.querySelectorAll(".karta").forEach((k) => {
        const a = przed[k.dataset.plik];
        if (!a) return;
        const b = k.getBoundingClientRect();
        const dx = a.left - b.left;
        const dy = a.top - b.top;
        if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
        const s = b.width ? a.width / b.width : 1;
        const lot = k.dataset.plik === przybyly;
        if (lot) k.classList.add("w-locie");
        const anim = k.animate(
          [
            {
              transform:
                "translate(" + dx + "px," + dy + "px) scale(" + s + ")",
            },
            { transform: "none" },
          ],
          { duration: lot ? 750 : 450, easing: "cubic-bezier(.2,.75,.25,1)" },
        );
        anim.onfinish = () => k.classList.remove("w-locie");
      });
    },
    reset() {
      /* nazwa `Podfolder/plik` od startu leży w teczce `Podfolder` (`a/b/plik` w teczce `a/b`), reszta luzem */
      f.luzem = pliki.filter((p) => !p.includes("/"));
      f.foldery = {};
      pliki
        .filter((p) => p.includes("/"))
        .forEach((p) => {
          const t = teczkaPliku(p);
          (f.foldery[t] = f.foldery[t] || []).push(p);
        });
      f.uwagi = {};
      f.nowe = new Set();
      f.byly = {};
      f.usuniete = new Set();
      f.swiezeKarty = new Set();
      f.zmian = 0;
      f.rysuj();
    },
    utworz(n) {
      if (!f.foldery[n]) f.swieze.add(n);
      f.foldery[n] = f.foldery[n] || [];
      f.zmian++;
      f.rysuj();
    },
    przenies(p, n, uwaga) {
      if (!f.foldery[n]) f.swieze.add(n);
      f.foldery[n] = f.foldery[n] || [];
      f.luzem = f.luzem.filter((x) => x !== p);
      f.foldery[n].push(p);
      if (uwaga) f.uwagi[p] = uwaga;
      f.zmian++;
      f.rysuj(p);
    },
    nowy(p) {
      const t = p.includes("/") ? teczkaPliku(p) : "";
      if (t) (f.foldery[t] = f.foldery[t] || []).push(p);
      else f.luzem.push(p);
      f.nowe.add(p);
      f.zmian++;
      f.rysuj();
    },
    /* Zmiana nazwy: karta zostaje w tym samym miejscu, przez chwilę z napisem „było: …”. */
    zmien(p, n) {
      const lista = [f.luzem, ...Object.values(f.foldery)].find((w) =>
        w.includes(p),
      );
      if (!lista) return;
      lista[lista.indexOf(p)] = n;
      if (f.uwagi[p]) f.uwagi[n] = f.uwagi[p];
      delete f.uwagi[p];
      if (f.nowe.delete(p)) f.nowe.add(n);
      delete f.byly[p];
      const b = { stara: p, do: Date.now() + PK.NA_CHWILE };
      f.byly[n] = b;
      f.swiezeKarty.add(n);
      f.zmian++;
      f.rysuj();
      if (el && !opcje.statyczny)
        setTimeout(() => {
          if (f.byly[n] !== b) return;
          const k = [...el.querySelectorAll(".karta")].find(
            (x) => x.dataset.plik === n,
          );
          const napis = k && k.querySelector(".karta-bylo");
          if (!napis) return;
          if (!ruch) return napis.remove();
          napis.classList.add("gasnie");
          napis.addEventListener("animationend", () => napis.remove());
        }, PK.NA_CHWILE);
    },
    /* Skasowanie: karta zostaje na miejscu, wyszarzona i przekreślona, z napisem „usunięty”. */
    usun(n) {
      const jest =
        f.luzem.includes(n) ||
        Object.values(f.foldery).some((w) => w.includes(n));
      if (!jest || f.usuniete.has(n)) return;
      f.usuniete.add(n);
      f.swiezeKarty.add(n);
      f.zmian++;
      f.rysuj();
    },
    /* Claude czyta plik: karta na chwilę dostaje znak oka. */
    czytaj(p) {
      if (!el) return;
      const k = [...el.querySelectorAll(".karta")].find(
        (x) => x.dataset.plik === p,
      );
      if (!k) return;
      k.insertAdjacentHTML(
        "beforeend",
        '<span class="karta-oko">' + PK.IKONA_OKA + "czyta</span>",
      );
      k.classList.add("czyta");
      setTimeout(() => {
        k.classList.remove("czyta");
        const oko = k.querySelector(".karta-oko");
        if (oko) oko.remove();
      }, 2600);
    },
    /* Krok `folder` ze scenariusza. */
    zastosuj(k) {
      if (k.akcja === "przenies") f.przenies(k.plik, k.nazwa, k.uwaga);
      else if (k.akcja === "zmien") f.zmien(k.plik, k.nazwa);
      else if (f[k.akcja]) f[k.akcja](k.nazwa);
    },
  };
  f.reset();
  return f;
};

/* Kroki `folder` na ścieżce pierwszych odpowiedzi w menu: z nich podgląd stanu po przebiegu. */
PK.krokiFolderu = function (kroki, wynik = [], opcja = 0) {
  for (const k of kroki || []) {
    if (k.typ === "folder") wynik.push(k);
    if (k.typ === "menu" && k.opcje && k.opcje[0])
      return PK.krokiFolderu((k.opcje[opcja] || k.opcje[0]).dalej, wynik);
  }
  return wynik;
};
