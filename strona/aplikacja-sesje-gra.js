/* Symulator aplikacji Claude, pasek boczny z rozmowami, działanie (ćwiczenie z drogami): kroki `klik` z celami nowa-rozmowa, sesja, menu-sesji, archive, group-and-sort, view-all i archived (znacznik „kliknij tutaj”, czekanie na klik, skutek), nowy wiersz po pierwszej prośbie w nowej rozmowie, nazwa z pola `nazwa_sesji`, tytuł w pasku tytułu, widok listy rozmów i „Od nowa”. Folder każdej rozmowy: klik `folder` (kontrolka w nowej rozmowie przed pierwszą prośbą), wiersz w grupie folderu, kontrolka znika po pierwszej prośbie (strona/aplikacja-sesje-foldery.js); karta wiadomości: pole `wiadomosc` kroku `claude` i klik `wiadomosc-od` (strona/aplikacja-sesje-wiadomosc.js). Wygląd: strona/aplikacja-sesje.js. */

PK.ZWINIECIE_WIERSZA_MS = 220; /* tyle trwa zwijanie zarchiwizowanego wiersza, zanim zniknie z listy */

/* Pasek boczny ćwiczenia `sek`. `srodowisko`: {poczatek (HTML rozmowy startowej), zamknijPanel() (zamyka otwarty plik, widok artefaktu i stronę w panelu obok rozmowy), folderZmieniony?(teczka) (folder otwartej rozmowy się zmienił: znacznik w podglądzie folderu), folder? () (folder otwartej rozmowy: pliki w podglądzie liczą się od niego), rozmowaOtwarta?(klucz, dane) (kursant otworzył inną rozmowę: karta Context pokazuje jej procent z pola `kontekst` wiersza), sesjaStartuje?() i kontekstUstawiony?(procent) (tylko `przewin`, podgląd: pierwsza prośba i krok `kontekst`)}. Zwraca {klik, prosba, odpowiedz, przewin, reset}; działa też w ćwiczeniu bez `aplikacja.sesje` (wtedy tylko `nowa-rozmowa` i wiersz po pierwszej prośbie).
   - klik(k, przerwano): gra krok `klik` z celem z PK.CELE_SESJI: znacznik, czekanie na klik w wyznaczony element (poza krokiem nic nie reaguje i kursor się nie zmienia), skutek;
   - prosba(): wołana po wysłaniu prośby kursanta; pierwsza prośba w nowej rozmowie dokłada na szczyt listy (przy folderze każdej rozmowy: na szczyt grupy jej folderu) podświetlony wiersz bez tekstu;
   - odpowiedz(k): wołana po odpowiedzi Claude; pole `nazwa_sesji` nadaje nazwę wskazanej rozmowie (widać ją po jej otwarciu), pole `wiadomosc` dopisuje kartę na końcu rozmowy odbiorcy;
   - przewin(kroki): te same skutki bez czekania i bez animacji, do podglądu końca drogi w tekście lekcji;
   - reset(): lista, tytuł i widok wracają do stanu startowego. */
PK.sesjeCwiczenia = function (cw, sek, srodowisko) {
  const apl = cw.aplikacja || {};
  const okno = sek.querySelector(".apl-okno");
  const rozmowa = sek.querySelector(".apl-rozmowa");
  const widok = sek.querySelector(".apl-sesje-widok"); /* null bez aplikacja.sesje */
  const dane = Object.fromEntries((apl.sesje || []).map((s) => [s.id, s]));
  const lista = () => sek.querySelector(".apl-bok-sesje");
  const poczatekListy = lista().innerHTML;
  const tytul = () => sek.querySelector(".apl-pasek > :first-child");
  const e1 = PK.folderyRozmow(apl); /* folder każdej rozmowy (strona/aplikacja-sesje-foldery.js) */
  const kontrolka = sek.querySelector(".apl-chip-folder"); /* null poza e1 */
  const nowyStan = () => ({ otwarta: "start", pusta: false, nazwy: {}, html: {}, zarchiwizowane: [], menu: null, folderNowej: apl.folder });
  const klucz = (id) => (apl.id && id === apl.id ? "start" : id); /* id rozmowy startowej to klucz „start” */
  let st = nowyStan();
  let czeka = null; /* {el, pusc}: krok klik czeka na klik w `el` */

  const oznaczStart = () => {
    const w = lista().querySelector(".apl-sesja");
    if (!w) return;
    w.dataset.start = "1"; /* wiersz otwartej rozmowy ze startu (po zmianie rozmowy podświetlenie przechodzi gdzie indziej) */
    w.classList.add("apl-wiersz"); /* bez podświetlenia wiersz zachowuje odstępy */
  };
  oznaczStart();
  const wiersz = (klucz) => lista().querySelector(klucz === "start" ? "[data-start]" : `[data-sesja="${klucz}"]`);
  const wiersze = () => [...lista().children].slice(1).filter((e) => e.classList.contains("apl-wiersz") && !e.classList.contains("zwija"));
  const podswietl = (el) => {
    lista().querySelectorAll(".apl-sesja").forEach((e) => e.classList.remove("apl-sesja"));
    if (el) el.classList.add("apl-sesja");
  };
  const nazwaRozmowy = (klucz) => (klucz === "start" ? apl.nazwa : klucz === "nowa" ? undefined : st.nazwy[klucz] ?? (dane[klucz] || {}).nazwa);

  /* Folder otwartej rozmowy: start i wiersze mają własny, nowa rozmowa ten, który wybrał kursant (na początku folder rozmowy startowej). */
  const folderRozmowy = (k) => (k === "start" ? apl.folder : k === "nowa" ? st.folderNowej : (dane[k] || {}).folder);
  let miga = null;
  /* Folder każdej rozmowy: napis kontrolki, jej widoczność (jest tylko w rozmowie bez pierwszej prośby i bez odpowiedzi) i znacznik folderu rozmowy w podglądzie folderu; `mignij` daje krótkie mignięcie napisu. */
  function odswiezFolder(mignij) {
    if (!e1) return;
    const f = folderRozmowy(st.otwarta);
    kontrolka.querySelector("span").textContent = f;
    okno.classList.toggle("apl-bez-folderu", !!rozmowa.querySelector(".apl-ty, .apl-claude"));
    kontrolka.classList.remove("mignij");
    clearTimeout(miga);
    if (mignij) {
      void kontrolka.offsetWidth; /* animacja zaczyna się od nowa */
      kontrolka.classList.add("mignij");
      miga = setTimeout(() => kontrolka.classList.remove("mignij"), PK.MIGNIECIE_FOLDERU_MS);
    }
    if (srodowisko.folderZmieniony) srodowisko.folderZmieniony(f);
  }
  const htmlRozmowy = (k) => st.html[k] ?? (k === "start" ? srodowisko.poczatek : PK.dymkiRozmowy(dane[k].rozmowa));

  /* Otwiera rozmowę: `start`, id wiersza albo `nowa` (pusta, w folderze rozmowy startowej). Dymki opuszczanej rozmowy zostają w pamięci, więc to, co dopisały kroki (także karty wiadomości), wraca przy ponownym otwarciu. Panel obok rozmowy się zamyka. */
  function otworz(k) {
    st.html[st.otwarta] = rozmowa.innerHTML;
    srodowisko.zamknijPanel();
    st.otwarta = k;
    if (k === "nowa") st.folderNowej = apl.folder;
    rozmowa.innerHTML = k === "nowa" ? "" : htmlRozmowy(k);
    tytul().outerHTML = PK.tytulRozmowy(nazwaRozmowy(k));
    podswietl(k === "nowa" ? null : wiersz(k));
    odswiezFolder();
    if (srodowisko.rozmowaOtwarta) srodowisko.rozmowaOtwarta(k, dane[k]); /* karta Context pokazuje procent otwartej rozmowy (strona/aplikacja-kontekst.js) */
  }

  function prosba() {
    if (!st.pusta) return odswiezFolder(); /* rozmowa startowa (także pusta, z czyta_na_start) po pierwszej prośbie też traci kontrolkę folderu */
    st.pusta = false;
    const html = PK.wierszSesji({ proc: 60, otwarta: true, menu: !!widok });
    let nowy;
    if (e1) nowy = PK.wstawWierszFolderu(lista(), st.folderNowej, html); /* na górze grupy swojego folderu (albo nowa grupa na górze listy) */
    else {
      lista().firstElementChild.insertAdjacentHTML("afterend", html);
      nowy = lista().firstElementChild.nextElementSibling;
    }
    podswietl(nowy);
    odswiezFolder(); /* kontrolka folderu znika razem z pierwszą prośbą */
  }

  function odpowiedz(k) {
    const n = k.nazwa_sesji;
    if (n) {
      st.nazwy[n.sesja] = n.nazwa;
      if (st.otwarta === n.sesja) tytul().outerHTML = PK.tytulRozmowy(n.nazwa); /* walidator tego nie dopuszcza; tytuł nie rozjeżdża się z nazwą */
    }
    if (k.wiadomosc) {
      /* karta na końcu rozmowy odbiorcy; widać ją po jej otwarciu (odbiorca nie odpisuje i nie zaczyna pracy) */
      const odbiorca = klucz(k.wiadomosc.do);
      st.html[odbiorca] = htmlRozmowy(odbiorca) + PK.kartaWiadomosci({ od: st.otwarta, tytul: nazwaRozmowy(st.otwarta), tekst: k.wiadomosc.tekst });
    }
  }

  /* Otwarte menu wystaje pod listę (karta ma `position: absolute`): lista dostaje tyle wysokości, żeby karta razem ze znacznikiem w niej mieściła się w oknie; bez otwartego menu wysokość wraca do naturalnej. */
  function ulozListe() {
    const l = lista();
    const menu = l.querySelector(".apl-menu-sesji, .apl-menu-grupy");
    l.removeAttribute("style");
    if (menu) l.style.minHeight = `${Math.ceil(menu.getBoundingClientRect().bottom - l.getBoundingClientRect().top + 14)}px`;
  }
  window.addEventListener("resize", ulozListe);

  /* Menu rozmowy wiersza `id` (null zamyka): karta powstaje przy otwarciu i znika przy zamknięciu. */
  function menuRozmowy(id) {
    const w = id && wiersz(id);
    lista().querySelectorAll(".apl-menu-sesji").forEach((m) => m.remove());
    lista().querySelectorAll(".apl-wiersz.menu-otwarte").forEach((e) => e.classList.remove("menu-otwarte"));
    lista().classList.toggle("menu-otwarte", !!w);
    st.menu = w ? id : null;
    if (w) {
      w.classList.add("menu-otwarte");
      w.insertAdjacentHTML("beforeend", PK.menuSesji());
    }
    ulozListe();
  }

  /* Menu Group and sort przy nagłówku listy: powstaje przy otwarciu, znika przy zamknięciu. */
  function menuGrupy(tak) {
    const naglowek = lista().querySelector(".apl-sesje-naglowek");
    naglowek.querySelectorAll(".apl-menu-grupy").forEach((m) => m.remove());
    if (tak) naglowek.insertAdjacentHTML("beforeend", PK.menuGrupy());
    naglowek.classList.toggle("menu-otwarte", tak);
    lista().classList.toggle("menu-otwarte", tak);
    ulozListe();
  }

  /* Archiwizacja: wiersz zwija się i znika z listy (w podglądzie od razu). */
  async function archiwizuj(szybko) {
    const id = st.menu;
    const w = wiersz(id);
    menuRozmowy(null);
    st.zarchiwizowane.push(id);
    if (!szybko) {
      w.classList.add("zwija");
      await PK.czekaj(PK.ZWINIECIE_WIERSZA_MS);
    }
    w.remove();
    if (e1) PK.zdejmijPusteGrupy(lista());
  }

  /* Widok listy rozmów w miejscu rozmowy i pola wiadomości: „aktywne” (pierwsza zakładka, tyle wierszy, ile ma lista w pasku bocznym) albo „archived” (wiersze zarchiwizowanych rozmów tej drogi). */
  function pokazWidok(zakladka) {
    const n = zakladka === "archived" ? st.zarchiwizowane.length : wiersze().length;
    widok.querySelector(".apl-sesje-wiersze").innerHTML = PK.wierszeListy(n);
    widok.querySelector(".apl-sesje-zakl.wybrana").classList.remove("wybrana");
    const wybrana = widok.querySelector(zakladka === "archived" ? "[data-zakladka]" : ".apl-sesje-zakl");
    wybrana.classList.add("wybrana");
    widok.querySelectorAll(".apl-sesje-zakl").forEach((z) => z.setAttribute("aria-selected", String(z === wybrana)));
    widok.hidden = false;
    okno.classList.add("widok-listy");
  }

  /* Skutek kliku; `szybko` pomija zwijanie wiersza (podgląd w tekście lekcji). */
  async function zastosuj(k, szybko) {
    if (k.cel === "nowa-rozmowa") {
      otworz("nowa");
      st.pusta = true;
    } else if (k.cel === "sesja") otworz(klucz(k.sesja));
    else if (k.cel === "wiadomosc-od") otworz(ostatniaKarta().dataset.od); /* odnośnik karty otwiera rozmowę nadawcy, jak klik sesja */
    else if (k.cel === "folder") {
      st.folderNowej = k.folder;
      odswiezFolder(!szybko);
    }
    else if (k.cel === "menu-sesji") menuRozmowy(k.sesja);
    else if (k.cel === "archive") await archiwizuj(szybko);
    else if (k.cel === "group-and-sort") menuGrupy(true);
    else if (k.cel === "view-all") {
      menuGrupy(false);
      pokazWidok("aktywne");
    } else if (k.cel === "archived") pokazWidok("archived");
  }

  const ostatniaKarta = () => [...rozmowa.querySelectorAll(".apl-wiadomosc")].pop();

  /* Element, w który kursant ma kliknąć w kroku `k`. */
  function element(k) {
    const w = k.sesja && wiersz(klucz(k.sesja));
    if (k.cel === "folder") return kontrolka;
    if (k.cel === "wiadomosc-od") return ostatniaKarta().querySelector(".apl-wiad-wr");
    if (k.cel === "nowa-rozmowa") return sek.querySelector(".apl-bok-nowa");
    if (k.cel === "sesja") return w;
    if (k.cel === "menu-sesji") return w && w.querySelector(".apl-wiersz-menu");
    if (k.cel === "archive") return lista().querySelector(".apl-wiersz.menu-otwarte .apl-menu-poz"); /* klasa menu-otwarte stoi też na samej liście, więc sam selektor potomka złapałby View all */
    if (k.cel === "group-and-sort") return lista().querySelector(".apl-grupa");
    if (k.cel === "view-all") return lista().querySelector(".apl-menu-grupy .apl-menu-poz");
    return widok && widok.querySelector("[data-zakladka]");
  }

  sek.addEventListener("click", (e) => {
    if (!czeka || !czeka.el.contains(e.target)) return;
    const { pusc } = czeka;
    czeka = null;
    pusc();
  });

  odswiezFolder(); /* rozmowa startowa bez wiadomości ma kontrolkę folderu od początku */

  return {
    async klik(k, przerwano) {
      const el = element(k);
      if (!el) return; /* walidator nie dopuszcza celu bez elementu */
      PK.celKroku(sek, k.cel, el);
      ulozListe(); /* rząd ze znacznikiem w menu dodaje wysokości */
      await new Promise((pusc) => (czeka = { el, pusc }));
      if (przerwano()) return;
      PK.celKroku(sek, k.cel, null);
      el.classList.add("wcisniety");
      await PK.czekaj(200);
      el.classList.remove("wcisniety");
      if (przerwano()) return; /* „Od nowa” w czasie wciśnięcia przycisku: skutek nie dotyczy już nowego stanu */
      await zastosuj(k, false);
    },
    prosba,
    odpowiedz,
    folderOtwartej: () => folderRozmowy(st.otwarta),
    przewin(kroki) {
      kroki.forEach((k) => {
        if (k.typ === "pisz") {
          rozmowa.insertAdjacentHTML("beforeend", PK.dymekAplikacji({ kto: "ty", tekst: k.tekst }));
          prosba();
          if (srodowisko.sesjaStartuje) srodowisko.sesjaStartuje(); /* po prośbie panel szczegółów wraca, jak w grze (strona/aplikacja.js) */
        } else if (k.typ === "kontekst") {
          if (srodowisko.kontekstUstawiony) srodowisko.kontekstUstawiony(k.procent); /* procent ostatnio ustawiony w drodze, tak jak liczy walidator */
        } else if (k.typ === "claude") {
          rozmowa.insertAdjacentHTML("beforeend", PK.dymekAplikacji({ kto: "claude", tekst: k.tekst, plik: k.plik, link: k.link }));
          odpowiedz(k);
        } else if (k.typ === "klik" && PK.CELE_SESJI.includes(k.cel)) zastosuj(k, true);
      });
    },
    reset() {
      czeka = null;
      PK.celKroku(sek, "sesja", null); /* zdejmuje znacznik i rząd ze znacznikiem, także poza listą (zakładki widoku) */
      lista().innerHTML = poczatekListy;
      lista().classList.remove("menu-otwarte");
      ulozListe();
      oznaczStart();
      tytul().outerHTML = PK.tytulRozmowy(apl.nazwa);
      if (e1) {
        clearTimeout(miga);
        kontrolka.classList.remove("mignij");
      }
      if (widok) {
        widok.hidden = true;
        widok.querySelector(".apl-sesje-wiersze").innerHTML = "";
        widok.querySelectorAll(".apl-sesje-zakl").forEach((z) => {
          z.classList.toggle("wybrana", !z.dataset.zakladka);
          z.setAttribute("aria-selected", String(!z.dataset.zakladka));
        });
      }
      okno.classList.remove("widok-listy");
      st = nowyStan();
      odswiezFolder(); /* kontrolka i znacznik folderu wracają do rozmowy startowej */
    },
  };
};
