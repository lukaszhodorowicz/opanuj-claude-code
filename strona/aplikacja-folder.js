/* Podgląd folderu pod oknem symulatora aplikacji: karty plików z silnika folderu lekcji terminalowych (PK.Folder) i cztery zmiany (czyta, nowy, zmieniony, od nowa); nie zna formatu scenariusza. */
PK.folderAplikacji = {
  /* kontener: pusty element pod oknem; stan: {nazwa (korzeń podglądu), pliki, nowe?: [nazwy już utworzone przez Claude], zmienione?: [{plik, dodane, usuniete}], rozmowa?: "" (korzeń) albo nazwa teczki, w której toczy się rozmowa}.
     Nazwa `Podfolder/plik` (w pliki, nowe, zmienione, czyta) to ścieżka od korzenia: teczka `Podfolder` od startu, karta o tożsamości pełnej ścieżki; `rozmowa` daje folderowi rozmowy wyróżnienie bez słów (klasa `rozmowa`).
     Zwraca uchwyt {zmiana(akcja), folder}; akcja: {akcja: "czyta", pliki, poczatek?: true (początek rozmowy), zastap?: true (gasi wcześniejsze podświetlenia z kroków)} | {akcja: "nowy", plik} | {akcja: "zmieniony", plik, dodane?, usuniete?} | {akcja: "rozmowa", teczka} (znacznik folderu rozmowy przechodzi na teczkę; "" = korzeń) | {akcja: "od-nowa"}.
     Zmieniony bez pól dodane i usuniete dostaje sam znaczek zmiany (ołówek w rogu i granatowa ramka), bez liczb +N −M. */
  pokaz(kontener, stan) {
    kontener.classList.add("apl-folder");
    const f = PK.Folder(kontener, stan.pliki || [], { nazwa: stan.nazwa });
    const jest = (p) =>
      [f.luzem, ...Object.values(f.foldery)].some((w) => w.includes(p)) &&
      !f.usuniete.has(p);
    const karta = (p) =>
      [...kontener.querySelectorAll(".karta")].find(
        (k) => k.dataset.plik === p,
      );

    /* znacznik folderu rozmowy: klasa na nagłówku korzenia albo na teczce, dokładana po każdym rysowaniu (rysuj składa element od nowa) */
    const rozmowaStartowa = stan.rozmowa;
    if (typeof stan.rozmowa === "string") {
      const rysuj = f.rysuj;
      const zaznacz = () => {
        const el = stan.rozmowa
          ? [...kontener.querySelectorAll(".teczka")].find(
              (t) => t.dataset.teczka === stan.rozmowa,
            )
          : kontener.querySelector(".pulpit-glowa");
        if (el) el.classList.add("rozmowa");
      };
      f.rysuj = (przybyly) => {
        rysuj(przybyly);
        zaznacz();
      };
    }

    /* znaczek zmiany w rogu karty: kółko z ołówkiem (bez napisu), widać go przy liczbach i bez nich */
    const OLOWEK =
      '<span class="karta-zmiana"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 0 1 3 3L8 19z"/><path d="M14.5 6.5l3 3"/></svg></span>';

    /* pliki ze znacznikiem zmiany bez liczb: PK.Folder.edytuj zawsze zapisuje liczby, więc ich napis zastępuje sam znaczek */
    const bezLiczb = new Set();
    const znacznik = f.znacznik;
    f.znacznik = (p) =>
      f.edycje[p]
        ? (bezLiczb.has(p)
            ? '<span class="karta-edytowany">zmieniona treść</span>'
            : znacznik(p)) + OLOWEK
        : znacznik(p);
    const edytuj = (p, dodane, usuniete) => {
      if (dodane === undefined && usuniete === undefined) bezLiczb.add(p);
      else bezLiczb.delete(p);
      f.edytuj(p, dodane, usuniete);
    };

    /* plik → chwila końca podświetlenia; gasi je `zgas` po 2,6 s */
    const CZYTA_MS = 2600;
    let czytane = {};
    /* pliki podświetlone na początku rozmowy (akcja z `poczatek: true`): kolejny krok z jawną listą ich nie gasi */
    let poczatkowe = new Set();

    /* obwódka i jedno oko na karcie; gdy karta już świeci, stare oko znika, więc oko nie dubluje się, a gaszenie liczy tylko `czytane` (PK.Folder.czytaj zostawiałby własny licznik 2,6 s) */
    function swiec(p) {
      const k = karta(p);
      if (!k) return;
      const oko = k.querySelector(".karta-oko");
      if (oko) oko.remove();
      k.insertAdjacentHTML(
        "beforeend",
        '<span class="karta-oko">' + PK.IKONA_OKA + "czyta</span>",
      );
      k.classList.add("czyta");
    }

    function zgas(p) {
      delete czytane[p];
      const k = karta(p);
      if (!k) return;
      k.classList.remove("czyta");
      const oko = k.querySelector(".karta-oko");
      if (oko) oko.remove();
    }

    /* nowa karta albo znacznik zmiany przerysowują folder: trwające podświetlenie wraca na swoje karty i gaśnie o pierwotnym czasie */
    function dalejCzyta() {
      const teraz = Date.now();
      Object.entries(czytane).forEach(([p, koniec]) => {
        if (koniec <= teraz || !jest(p)) return delete czytane[p];
        swiec(p);
        setTimeout(() => {
          if (czytane[p] === koniec) zgas(p);
        }, koniec - teraz);
      });
    }

    function odNowa() {
      stan.rozmowa = rozmowaStartowa;
      czytane = {};
      poczatkowe = new Set();
      bezLiczb.clear();
      f.reset();
      (stan.nowe || []).forEach((p) => !jest(p) && f.nowy(p));
      (stan.zmienione || []).forEach((z) =>
        edytuj(z.plik, z.dodane, z.usuniete),
      );
    }

    function zmiana(a) {
      if (!a) return;
      if (a.akcja === "od-nowa") return odNowa();
      if (a.akcja === "rozmowa") {
        if (typeof stan.rozmowa !== "string") return;
        stan.rozmowa = a.teczka;
        f.rysuj();
        return dalejCzyta();
      }
      /* czyta: karta na chwilę dostaje obwódkę i znak oka (`swiec`); pliki spoza folderu pomija */
      if (a.akcja === "czyta") {
        /* `zastap: true` (jawna lista `czyta` kroku): wcześniejsze podświetlenia z kroków gasną, bo kolejne kroki mają grać jeden po drugim; podświetlenia z `poczatek: true` zostają */
        if (a.zastap)
          Object.keys(czytane)
            .filter((p) => !poczatkowe.has(p))
            .forEach(zgas);
        const koniec = Date.now() + CZYTA_MS;
        return (a.pliki || []).filter(jest).forEach((p) => {
          if (a.poczatek) poczatkowe.add(p);
          else poczatkowe.delete(p);
          czytane[p] = koniec;
          swiec(p);
          setTimeout(() => {
            if (czytane[p] === koniec) zgas(p);
          }, CZYTA_MS);
        });
      }
      if (a.akcja === "nowy") {
        if (!a.plik || jest(a.plik)) return;
        f.nowy(a.plik);
        const k = karta(a.plik);
        if (k) k.classList.add("apl-pojawia");
        return dalejCzyta();
      }
      if (a.akcja === "zmieniony") {
        edytuj(a.plik, a.dodane, a.usuniete);
        dalejCzyta();
      }
    }

    odNowa();
    return { zmiana, folder: f };
  },
};
