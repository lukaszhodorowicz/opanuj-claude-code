/* Symulator aplikacji Claude, działanie: wybiera sposób gry ćwiczenia (etapy z menu trybu, drogi do wyboru, kroki po kolei: strona/aplikacja-kroki.js). Drogi: prośba kursanta, odpowiedź ze ścieżką albo linkiem, klik otwiera plik albo widok artefaktu; karta Context, polecenia w polu wiadomości i pytanie z boku; pasek boczny z rozmowami (strona/aplikacja-sesje-gra.js); wskazanie „kliknij tutaj”, powrót „Od nowa” i podgląd końca drogi w tekście lekcji; krok klik z celem pierscien (strona/aplikacja-pierscien.js) i panel szczegółów po nowej rozmowie. */
PK.aplikacja = function (cw, host, nr) {
  host.innerHTML = PK.htmlAplikacji(cw, nr);
  const sek = host.firstElementChild;
  PK.konektoryPanelu(sek); /* klik nagłówka zwiniętej karty Connectors (pole `aplikacja.konektory_do_polaczenia`) rozwija ją i zwija, w każdym ćwiczeniu (strona/aplikacja-panel.js) */
  const pierscien = PK.pierscienCwiczenia(cw, sek); /* pierścień zużycia w rzędzie pod polem i jego okienko, w każdym ćwiczeniu (strona/aplikacja-pierscien.js); sam zamyka okienko przy „Od nowa” i nowym poleceniu drogi */
  /* podpięcie: menu trybu, karta zgody i podgląd folderu w etapach, strona/aplikacja-tryby.js */
  if (cw.etapy) {
    const kontekstEtapow = PK.kontekstCwiczenia(cw, sek); /* karta Context z `aplikacja.kontekst`: procent z rozwinięciem po kliku, bez kroków; null bez pola */
    if (kontekstEtapow) sek.querySelector("[data-od-nowa]").addEventListener("click", kontekstEtapow.reset); /* „Od nowa” zamyka rozwiniętą kartę */
    return PK.trybyAplikacji(cw, sek);
  }
  const folder = PK.folderCwiczenia(cw, sek); /* podgląd folderu pod oknem: strona/aplikacja-folder-cwiczenie.js */
  if (cw.drogi) return PK.drogiAplikacji(cw, sek, folder, pierscien);
  return PK.krokiAplikacji(cw, sek);
};

/* Drogi: każde polecenie zaczyna od rozmowy ze scenariusza i gra kroki swojej drogi; klik w ścieżkę otwiera plik obok rozmowy, klik w link widok artefaktu (strona/aplikacja-artefakt.js). */
PK.drogiAplikacji = function (cw, sek, folder, pierscien) {
  const { czekaj } = PK;
  const drogi = cw.drogi || [];
  const okno = sek.querySelector(".apl-okno");
  const rozmowa = sek.querySelector(".apl-rozmowa");
  const pole = sek.querySelector(".apl-pole-tekst");
  const widok = sek.querySelector(".apl-widok-pliku");
  const mow = PK.Nauczyciel(sek.querySelector(".nauczyciel"), []);
  const poczatek = rozmowa.innerHTML;
  let gen = 0; /* numer przebiegu: nowe polecenie albo „Od nowa” przerywa poprzedni */
  const artefakt = PK.artefaktCwiczenia(cw, okno, widok);
  const plus = PK.plusAplikacji(cw, sek, okno); /* przycisk +, menu, lista poleceń i skill w polu (strona/aplikacja-plus.js); null, gdy żadna droga ich nie ma */
  const katalog = PK.katalogAplikacji(cw, sek, okno); /* okno katalogu konektorów (strona/aplikacja-katalog.js); null, gdy żadna droga nie ma kroków katalogu */
  const wtyczki = PK.wtyczkiAplikacji(cw, sek, okno); /* przeglądarka wtyczek (strona/aplikacja-wtyczki.js); null, gdy żadna droga nie ma pozycji „Browse plugins” */
  const kontekst = PK.kontekstCwiczenia(cw, sek); /* karta Context w panelu (strona/aplikacja-kontekst.js); null bez aplikacja.kontekst */
  const zBoku = PK.zBokuCwiczenia(okno, widok); /* panel pytania z boku w miejscu otwartego pliku (strona/aplikacja-z-boku.js) */
  const model = PK.modelCwiczenia(cw, sek); /* menu wyboru modelu i lista poziomów wysiłku w rzędzie pod polem (strona/aplikacja-model.js); null bez kroku klik „wybor-modelu” */
  const strona = PK.stronaZewnetrzna(okno, widok); /* cudza strona w panelu Browser i pamięć zgody przeglądarki (strona/aplikacja-drogi-strona.js) */
  const wTle = PK.wTleAplikacji(cw, sek, okno, widok, () => zamknijPanele()); /* menu ⋮, panel zadań w tle i panel subagenta w miejscu otwartego pliku (strona/aplikacja-w-tle.js); null, gdy żadna droga nie ma pola w_tle */
  const harm = PK.harmonogramAplikacji(cw, sek, okno); /* pozycja Scheduled w pasku bocznym, strona Scheduled tasks, okno New scheduled task i strona zadania (strona/aplikacja-harmonogram.js); null bez aplikacja.harmonogram */
  /* pasek boczny z rozmowami (strona/aplikacja-sesje-gra.js): zmiana rozmowy zamyka plik, widok artefaktu i stronę w panelu */
  const sesje = PK.sesjeCwiczenia(cw, sek, { poczatek, zamknijPanel: () => zamknijPanele(), folderZmieniony: (teczka) => folder && folder.rozmowa(teczka), rozmowaOtwarta: (klucz, dane) => kontekst && kontekst.rozmowa(klucz, dane && dane.kontekst) }); /* rozmowaOtwarta: karta Context pokazuje procent otwartej rozmowy (pole kontekst wiersza aplikacja.sesje; bez pola szary pasek) */ /* folder każdej rozmowy: znacznik folderu rozmowy w podglądzie przechodzi na teczkę otwartej rozmowy */
  if (folder) folder.zrodlo(() => sesje.folderOtwartej()); /* ścieżki widoczne dla kursanta liczą się od folderu otwartej rozmowy */
  const telefon = PK.telefonAplikacji(cw, sek, okno, rozmowa); /* telefon z Remote Control obok okna (strona/aplikacja-telefon.js); null bez aplikacja.telefon */
  const ustawienia = PK.ustawieniaCCAplikacji(cw, sek, okno); /* okno Settings → Claude Code (strona/aplikacja-ustawienia-cc.js); null, gdy żadna droga nie ma kroku klik ustawienia-claude-code ani komendy /config */
  const trybMenu = PK.trybMenuDrogi(cw, sek, okno); /* przełącznik trybu i lista trybów w drogach (strona/aplikacja-menu-rzedu.js); null bez kroku klik tryb-menu */
  const srodowiskoMenu = PK.srodowiskoMenuDrogi(cw, sek, okno); /* menu środowiska otwierane kontrolką „This computer” (strona/aplikacja-menu-rzedu.js); null bez kroku klik srodowisko-menu */
  const plikEkrany = PK.plikEkranyAplikacji(cw, sek, okno, widok); /* menu „…” panelu pliku, menu prawego kliku karty pliku i dymek ikony paska tytułu (strona/aplikacja-plik-gra.js); null bez kroku klik plik-menu, plik-karta-menu, plik-karta-pozycja ani ikona-tytulu */
  const przegl = PK.browserAplikacji(cw, sek, okno, widok); /* panel Browser z pustą kartą „New tab” i menu „…” (strona/aplikacja-browser.js); null bez kroku klik przegladarka albo przegladarka-menu */
  const menuTyt = PK.menuTytuluDrogi(cw, sek, okno); /* menu sesji ze strzałki przy tytule rozmowy i podmenu Transcript view (strona/aplikacja-menu-tytulu.js); null bez kroku klik strzalka-tytulu, transcript-view albo widok-transkrypcji */
  const edytor = PK.edytorAplikacji(cw, sek, okno, artefakt, widok); /* edytor prezentacji rozwinięty na całe okno (strona/aplikacja-edytor-gra.js); null bez kroku klik edytor-rozwin */
  const zamknijPanele = () => { artefakt.zamknij(); strona.zamknij(); if (przegl) przegl.zamknij(); }; /* panel obok rozmowy zajmuje jedno miejsce: nowy plik, strona, artefakt, panel zadań albo inna rozmowa zamyka to, co w nim stało */
  let klik = null; /* {cel, klikniete, pusc}: ścieżka albo link w ostatniej odpowiedzi, ptaszek karty zgody albo przycisk karty przeglądarki */
  let zagrane = 0; /* ile dróg zagrano po kolei od pierwszej */
  let gra = false; /* trwa przebieg drogi: żadne polecenie nie jest wtedy aktywne */
  let odliczanie = null; /* odliczanie przed ptaszkiem karty zgody (strona/aplikacja-drogi-odliczanie.js); „Od nowa” i nowe polecenie je przerywają */

  /* Po kolei: aktywna tylko następna droga; w czasie gry żadna; po zagraniu wszystkich każda, do powtórki. */
  function ustawPolecenia() {
    sek.querySelectorAll(".polecenie").forEach((b) => {
      b.disabled = gra || (zagrane < drogi.length && +b.dataset.d !== zagrane);
    });
  }

  function wyczysc(calkiem) { /* calkiem: „Od nowa” zdejmuje też `wyslane` z poleceń; nowa droga je zachowuje */
    gen++;
    if (odliczanie) odliczanie.przerwij();
    odliczanie = null;
    klik = null;
    rozmowa.innerHTML = poczatek;
    pole.textContent = "";
    pole.classList.remove("pisze");
    if (plus) plus.reset(); /* menu i lista zamknięte, skill z pola zdjęty, czekający krok przerwany */
    if (katalog) katalog.reset(); /* okno katalogu zamknięte, czekający krok przerwany */
    if (wtyczki) wtyczki.reset(); /* przeglądarka wtyczek zamknięta */
    if (harm) harm.reset(); /* strony harmonogramu i okno zamknięte (widać rozmowę), sekcja Advanced settings zwinięta, historia pusta, czekający krok przerwany */
    if (wTle) wTle.reset(); /* menu ⋮ zamknięte, wpisy usunięte, ⋮ znów nieaktywny, czekający krok przerwany */
    widok.hidden = true;
    widok.innerHTML = "";
    okno.classList.remove("plik-otwarty");
    artefakt.reset(); /* zamyka widok artefaktu; ćwiczenie z artefakt_otwarty otwiera go od nowa */
    strona.reset(); /* zamyka cudzą stronę i czyści pamięć zgody (Allow once, Always allow) */
    if (kontekst) kontekst.reset(); /* karta Context wraca do procentu ze startu, zamknięta */
    if (model) model.reset(); /* menu, lista poziomów i notka zamknięte, przycisk znów nieaktywny */
    sesje.reset(); /* lista rozmów, tytuł i widok listy wracają do stanu startowego */
    if (telefon) telefon.reset(); /* lista sesji na telefonie, puste pole, krok czekający na klik przerwany */
    if (ustawienia) ustawienia.reset(); /* okno Settings zamknięte, krok czekający na klik przerwany */
    if (trybMenu) trybMenu.reset(); /* lista trybów zamknięta, tryb ze startu, czekający krok przerwany */
    if (srodowiskoMenu) srodowiskoMenu.reset(); /* menu środowiska zamknięte, czekający krok przerwany */
    if (plikEkrany) plikEkrany.reset(); /* menu pliku i karty zamknięte, dymek ikony ukryty, czekający krok przerwany */
    if (przegl) przegl.reset(); /* ślad panelu Browser na pasku tytułu zdjęty, czekający krok przerwany (sam panel czyści widok wyżej) */
    if (menuTyt) menuTyt.reset(); /* menu sesji zamknięte, widok rozmowy znów Normal, czekający krok przerwany */
    if (edytor) edytor.reset(); /* okno edytora zamknięte, czekający krok przerwany */
    PK.celAplikacji(sek, null);
    if (calkiem) sek.querySelectorAll(".wyslane").forEach((e) => e.classList.remove("wyslane"));
    if (folder) folder.reset();
    gra = false;
    ustawPolecenia();
  }

  /* ostatnia ścieżka, ostatni link ptaszek karty zgody albo Once karty przepływu, które czekają (liczy się tylko z ostatniej odpowiedzi; po zatwierdzeniu karta nie ma przycisków), a także nagłówek karty Context i krzyżyk panelu pytania z boku (te dwa stoją poza rozmową) */
  const SELEKTORY = { link: ".apl-link", zatwierdz: ".apl-zgoda-tak", sciezka: ".apl-sciezka:not(.apl-link)", context: ".apl-kontekst-naglowek", "zamknij-z-boku": ".apl-zboku-zamknij", "wybor-modelu": ".apl-model:not([aria-disabled])", effort: ".apl-menu-effort:not([aria-disabled])", poziom: ".apl-poziom:not([aria-disabled])", ...PK.SELEKTORY_ZGODY_STRONY, ...PK.SELEKTORY_PRZEPLYWU }; /* przycisk modelu, wiersz Effort i wiersz poziomu są aktywne tylko wtedy, gdy krok na nie czeka (PK.modelCwiczenia.zapowiedz) */
  const ostatni = (cel) => {
    const lista = (cel === "context" || cel === "zamknij-z-boku" || PK.CELE_MODELU.includes(cel) ? okno : rozmowa).querySelectorAll(SELEKTORY[cel]);
    return lista[lista.length - 1];
  };
  const dopisz = (html) => {
    rozmowa.insertAdjacentHTML("beforeend", html);
    return rozmowa.lastElementChild;
  };

  /* Wiadomość kursanta: tekst sam pojawia się w polu (po podświetlonym skillu, gdy wybrany z listy), potem idzie do rozmowy razem ze skillem (Enter wysyła). */
  async function pisz(tekst, g, naTelefonie) {
    const skill = !naTelefonie && !!plus && plus.skill();
    /* z `na_telefonie` tekst pisze się w polu telefonu (strona/aplikacja-telefon.js), a dymek staje w oknie i, przez lustro rozmowy, na telefonie */
    const poszlo = naTelefonie ? telefon.pisz(tekst, () => g !== gen) : PK.wpiszWPole(pole, tekst, () => g !== gen, skill ? plus.wpisz : undefined);
    if (!(await poszlo)) return;
    if (plus && !naTelefonie) plus.zeruj();
    dopisz(PK.dymekAplikacji({ kto: "ty", tekst, skill }));
    sesje.prosba(); /* pierwsza prośba w nowej rozmowie dokłada wiersz do listy */
    if (kontekst) kontekst.pokazPanel(); /* sesja startuje po wysłaniu zadania: po `+ New` panel szczegółów wraca z pierwszą prośbą */
  }

  /* Polecenie w polu wiadomości (strona/aplikacja-pole.js): tekst pojawia się i znika po wysłaniu, bez dymka w rozmowie, bez listy podpowiedzi; `/btw` otwiera panel pytania z boku w miejscu otwartego pliku, `/config` okno Settings na stronie Claude Code. */
  async function komenda(tekst, g) {
    if (!(await PK.wpiszWPole(pole, tekst, () => g !== gen))) return;
    if (tekst === PK.KOMENDA_USTAWIEN_CC && ustawienia) return ustawienia.otworz();
    if (tekst !== "/btw") return;
    zamknijPanele(); /* panel zajmuje miejsce pliku: otwarty widok artefaktu, cudza strona i panel Browser się zamykają */
    zBoku.otworz();
  }

  async function krok(k, g, nast, dalej) {
    if (k.typ === "pisz") return pisz(k.tekst, g, !!k.na_telefonie && !!telefon);
    if (k.typ === "komenda") return komenda(k.tekst, g);
    if (k.typ === "kontekst") return kontekst && kontekst.ustaw(k.procent); /* nowy procent na karcie Context z krótkim mignięciem */
    if (k.typ === "z_boku") return zBoku.pytanie(k, () => g !== gen);
    if (k.typ === "nauczyciel") return PK.krokNauczyciela(mow, k, nast);
    if (k.typ === "claude") {
      if (k.plik || k.link) klik = null; /* nowa ścieżka albo link: klik w starą niczego z góry nie zalicza */
      if (k.w_tle_koniec && wTle) dopisz(wTle.wierszeKonca()); /* koniec pracy w tle: napis „N running tasks” znika, przed odpowiedzią szare wiersze z tytułami zadań */
      const dymek = dopisz(PK.dymekAplikacji({ kto: "claude", tekst: k.tekst, plik: k.plik, link: k.link, karta: k.karta_pliku }));
      if (k.w_tle && wTle) wTle.dodaj(k.w_tle, dymek); /* nowe prace w tle: ⋮ aktywny, karty w panelu zadań, nieaktywny napis „N running tasks” pod odpowiedzią */
      return sesje.odpowiedz(k); /* pole nazwa_sesji nadaje nazwę rozmowie z listy */
    }
    if (k.typ === "zgoda") {
      const karta = dopisz(k.witryna ? strona.karta(k, dalej) : PK.kartaZgodyChroniona(k)); /* z `witryna` karta przeglądarki z trzema przyciskami (strona/aplikacja-drogi-strona.js); inaczej tylko ikony, bez nazwy pliku, bez treści polecenia i bez linijek (strona/aplikacja-drogi-zgoda.js) */
      if (k.odliczanie_ms) await (odliczanie = PK.odliczanieZgody(sek, karta, k.odliczanie_ms)).gotowe; /* droga czeka, ptaszek jest do tej chwili nieaktywny */
      return;
    }
    if (k.typ === "przeplyw") return void dopisz(PK.kartaPrzeplywu(k)); /* karta zgody na przepływ pod odpowiedzią Claude, czeka na klik Once (strona/aplikacja-przeplyw.js) */
    if (k.typ === "mysli") {
      /* pauza bez napisu: dokumentacja aplikacji nie podaje wyglądu wskaźnika pracy */
      const el = dopisz('<div class="apl-mysli" aria-hidden="true"><i></i><i></i><i></i></div>');
      await czekaj(k.ms || 1200);
      return el.remove();
    }
    if (k.typ === "klik" && k.cel === "pierscien") return pierscien.krok(() => g === gen); /* czeka na otwarcie okienka zużycia; już otwarte się liczy */
    if (telefon && telefon.dotyczy(k)) return telefon.klik(k, () => g === gen); /* klik w wiersz sesji na telefonie albo w strzałkę wstecz */
    if (ustawienia && ustawienia.dotyczy(k)) return ustawienia.klik(k, () => g === gen); /* klik w konto na dole paska bocznego otwiera Settings → Claude Code */
    if (k.typ === "klik" && PK.CELE_SESJI.includes(k.cel)) {
      await sesje.klik(k, () => g !== gen);
      if (k.cel === "nowa-rozmowa" && kontekst && g === gen) kontekst.nowaRozmowa(); /* nowa sesja jeszcze się nie zaczęła: panel szczegółów znika, karta Context bez procentu */
      return;
    }
    if (przegl && przegl.dotyczy(k)) return przegl.klik(k, () => g === gen); /* klik w przycisk Browser na pasku tytułu albo w „…” panelu Browser */
    if (menuTyt && menuTyt.dotyczy(k)) return menuTyt.klik(k, () => g === gen); /* klik w strzałkę przy tytule, w Transcript view albo w pozycję podmenu */
    if (edytor && edytor.dotyczy(k)) return edytor.klik(k, () => g === gen); /* klik w ikonę rozwinięcia edytora prezentacji */
    if (trybMenu && trybMenu.dotyczy(k)) return trybMenu.klik(k, () => g === gen); /* klik w przełącznik trybu albo w pozycję listy trybów */
    if (srodowiskoMenu && srodowiskoMenu.dotyczy(k)) return srodowiskoMenu.klik(k, () => g === gen); /* klik w kontrolkę środowiska otwiera menu, które zostaje otwarte do końca drogi */
    if (plikEkrany && plikEkrany.dotyczy(k)) return plikEkrany.klik(k, () => g === gen); /* klik w „…” panelu pliku, w kartę pliku, w pozycję jej menu albo w pierwszą ikonę paska tytułu */
    if (harm && harm.dotyczy(k)) return harm.klik(k, () => g === gen); /* klik w Scheduled, New task, Advanced settings, Create albo Run now (strona/aplikacja-harmonogram.js) */
    if (wTle && wTle.dotyczy(k)) return wTle.klik(k, () => g === gen); /* klik w ⋮, w pozycję Background tasks, albo we wpis w panelu zadań (napis „N running tasks” jest nieaktywny, nie ma celu) */
    if (k.typ === "ukosnik") return plus.ukosnik(() => g === gen); /* znak / w polu i lista poleceń */
    if (plus && plus.dotyczy(k)) {
      await plus.klik(k, () => g === gen); /* klik w +, w pozycję menu albo w wiersz listy */
      if (katalog && katalog.otwiera(k) && g === gen) katalog.otworz(); /* pozycja „Browse connectors” zamknęła menu i otwiera katalog */
      if (wtyczki && wtyczki.otwiera(k) && g === gen) wtyczki.otworz(); /* pozycja „Browse plugins” zamknęła menu i otwiera przeglądarkę wtyczek */
      return;
    }
    if (katalog && katalog.dotyczy(k)) return katalog.krok(k, () => g === gen); /* klik w kafelek konektora albo zamknięcie okna katalogu */
    if (k.typ === "klik") {
      if (model) model.zapowiedz(k); /* uaktywnia przycisk modelu, wiersz Effort albo wiersz poziomu, zanim krok zacznie na niego czekać */
      const el = ostatni(k.cel);
      if (!el) return; /* bez ścieżki albo linku w odpowiedzi nie ma czego klikać (walidator do tego nie dopuszcza) */
      if (!klik || !klik.klikniete || klik.cel !== k.cel) {
        if (model) model.znacznik(k, el); /* gdy pierścień zamknął menu modelu, znacznik stoi na przycisku, który je otwiera */
        else PK.celKroku(sek, k.cel, el);
        await new Promise((pusc) => (klik = { cel: k.cel, klikniete: false, pusc }));
      }
      klik = null;
      if (g !== gen) return;
      PK.celKroku(sek, k.cel, null);
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (k.cel === "zatwierdz") PK.zatwierdzZgode(el.closest(".apl-zgoda")); /* karta zostaje w rozmowie bez przycisków */
      if (PK.DECYZJE_STRONY.includes(k.cel)) strona.decyzja(k.cel, el.closest(".apl-zgoda")); /* karta przeglądarki: przyciski znikają, zgoda w pamięci */
      if (k.cel === "once") {
        const karta = el.closest(".apl-zgoda");
        PK.zatwierdzPrzeplyw(karta); /* karta zostaje w rozmowie jako ramka z nazwą i fazami */
        const dymki = rozmowa.querySelectorAll(".apl-claude");
        if (wTle) wTle.dodaj([{ rodzaj: "przeplyw", tytul: PK.nazwaPrzeplywu(karta) }], dymki[dymki.length - 1]); /* wpis przepływu w pracy w tle: ⋮ aktywny, odnośnik przy dwóch pracach */
      }
      if (k.cel === "context" && kontekst) kontekst.otworz();
      if (k.cel === "zamknij-z-boku") zBoku.zamknij();
      if (model) await model.po(k, () => g !== gen); /* skutek kliku w menu wyboru modelu; po wyborze poziomu czeka na zamknięcie menu */
      return;
    }
    if (k.typ === "artefakt") {
      strona.zapomnij(); /* widok artefaktu zajmuje panel Browser: cudza strona znika z niego razem z jego zawartością */
      if (przegl) przegl.zamknij(); /* pusta karta Browser też ustępuje */
      return artefakt.krok(k); /* otwiera widok artefaktu albo podmienia jego stronę w miejscu */
    }
    if (k.typ === "strona") {
      if (przegl) przegl.zamknij();
      if (!strona.otwarta()) artefakt.zamknij(); /* cudza strona zajmuje panel Browser: otwarty widok artefaktu się zamyka (gdy panel już pokazuje cudzą stronę, artefaktu w nim nie ma, a zamknięcie wyczyściłoby panel przed podmianą) */
      return strona.krok(k); /* otwiera stronę bez kliku w ścieżkę albo podmienia ją w miejscu */
    }
    if (k.typ === "plik") {
      zamknijPanele(); /* plik zajmuje panel: otwarty widok artefaktu, cudza strona i panel Browser się zamykają */
      widok.innerHTML = PK.plikLubStrona(k);
      widok.hidden = false;
      okno.classList.add("plik-otwarty");
    }
  }

  const PAUZA_CZYTANIA_MS = 600; /* czas na zobaczenie plików z czyta_na_start przed pisaniem prośby */

  async function uruchom(i) {
    wyczysc();
    const g = gen;
    sek.querySelector(`.polecenie[data-d="${i}"]`).classList.add("wyslane");
    gra = true;
    ustawPolecenia();
    if (zagrane === 0 && i === 0) mow(cw.nauczyciel_start, null, "polecenie"); /* zdanie startowe stoi nad oknem tylko przed pierwszym poleceniem */
    else mow(sek.querySelector(".nauczyciel .dymek p").textContent, null, "polecenie"); /* kolejne polecenie nie powtarza zdania startowego, ale daje mocny sygnał dymka; tekst zmienia pierwszy krok nauczyciela drogi */
    const ks = drogi[i].kroki || [];
    for (const [j, k] of ks.entries()) {
      if (folder) folder.krok(k, drogi[i].kroki);
      if (j === 0 && k.typ === "pisz" && cw.aplikacja.czyta_na_start) {
        await czekaj(PAUZA_CZYTANIA_MS); /* kursant widzi podświetlone pliki przy pustym polu, zanim zacznie się pisanie */
        if (g !== gen) return;
      }
      await krok(k, g, ks[j + 1], ks.slice(j + 1));
      if (g !== gen) return;
    }
    gra = false;
    zagrane = Math.max(zagrane, i + 1);
    ustawPolecenia();
  }

  sek
    .querySelectorAll(".polecenie")
    .forEach((b) => b.addEventListener("click", () => uruchom(+b.dataset.d)));
  /* w fazie przechwytywania: krzyżyk panelu pytania z boku zamyka panel, więc cel trzeba rozpoznać, zanim zniknie z okna */
  okno.addEventListener("click", (e) => {
    if (e.target.closest('.apl-zgoda [aria-disabled="true"]')) return; /* ptaszek przed końcem odliczania i wyszarzone przyciski karty niczego nie zaliczają */
    /* liczy się tylko ścieżka albo link z ostatniej odpowiedzi, nagłówek karty Context, krzyżyk panelu, aktywny przycisk karty przeglądarki, przycisk modelu, wiersz Effort, wiersz poziomu i Once karty przepływu */
    const cel = Object.keys(SELEKTORY).find((c) => ostatni(c) && e.target.closest(`.apl-sciezka, .apl-link, .apl-zgoda-tak, .apl-kontekst-naglowek, .apl-zboku-zamknij, .apl-model, .apl-menu-effort, .apl-poziom, ${PK.PRZYCISK_ZGODY_STRONY}, ${PK.PRZYCISK_PRZEPLYWU}`) === ostatni(c));
    if (!cel) return;
    /* klik przed krokiem klik też się liczy: droga nie czeka potem drugi raz; klik w ścieżkę, gdy krok czeka na link (albo odwrotnie), nic nie zalicza */
    if (klik && klik.pusc) {
      if (klik.cel === cel) klik.pusc();
    } else klik = { cel, klikniete: true };
  }, true);
  sek.querySelector("[data-od-nowa]").addEventListener("click", () => {
    zagrane = 0;
    wyczysc(true);
    mow(cw.nauczyciel_start, null, "polecenie");
  });
  artefakt.reset(); /* ćwiczenie z artefakt_otwarty zaczyna z otwartym widokiem */
  ustawPolecenia();
  PK.podgladyDrogCwiczenia(cw, drogi); /* podgląd końca drogi w tekście lekcji: strona/aplikacja-drogi-podglad.js */
};
