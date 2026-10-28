/* Symulator aplikacji Claude, wybór modelu i wysiłku (ćwiczenie z drogami i krokiem `klik` z celem `wybor-modelu`): menu nad rzędem pod polem wiadomości (cztery wiersze modeli z nazwami ze zrzutu, ✓ przy bieżącym, wiersz Effort z bieżącym poziomem, More models, część Fast mode), lista poziomów obok menu (Low, Medium, High, Extra, Max i nieaktywny Ultracode), ✓ przy wybranym poziomie i notka kursu. Napisy ze zrzutów Łukasza 27.10.2026 (04-24-16, 04-24-29; strona/aplikacja-ekran.js); nazwy modeli to modele z konta autora zrzutów, a bez pola `aplikacja.model` przycisk i menu pokazują model domyślny (PK.MODEL_DOMYSLNY, „Opus 5.5”). Kroki i skutki: dane/FORMAT-SCENARIUSZA.md. */

/* Początek opisu przycisku w rzędzie dla czytnika ekranu: po nim model i poziom („Wybór modelu i wysiłku: Opus 5.5 Medium”). */
PK.OPIS_WYBORU_MODELU = "Wybór modelu i wysiłku";
PK.CELE_MODELU = ["wybor-modelu", "effort", "poziom"];
PK.ZAMKNIECIE_MODELU_MS = 1500; /* po wyborze poziomu menu, lista i notka znikają po tym czasie */
PK.SZEROKOSC_MENU_MODELU = 280;
PK.SZEROKOSC_LISTY_WYSILKU = 285;
PK.SZEROKOSC_LISTY_WASKIEJ = 160; /* w wąskim oknie lista stoi w miejscu menu; wąska, bo po jej lewej stronie musi zmieścić się notka kursu, a napisy w niej zawijają się (klasa apl-menu-waska) */
PK.WASKIE_OKNO_MODELU = 560; /* węższy rząd pod polem: lista otwiera się w miejscu menu (telefon i wąskie okno) */
PK.NAJMNIEJ_MIEJSCA_MODELU = 220; /* poniżej tej szerokości menu i lista już się nie zwężają */
PK.SZEROKOSC_NOTKI = 180; /* największa szerokość notki; węższa, gdy obok listy jest mniej miejsca */

/* Poziomy wysiłku w kolejności listy (numer `poziom` kroku 1-5 liczy od góry). */
PK.POZIOMY_WYSILKU = [PK.NAPISY_EKRANU.wysilek.low, PK.NAPISY_EKRANU.wysilek.medium, PK.NAPISY_EKRANU.wysilek.high, PK.NAPISY_EKRANU.wysilek.extra, PK.NAPISY_EKRANU.wysilek.max];

/* Model i poziom wysiłku z pól `aplikacja.model` (domyślnie Opus 5.5) i `aplikacja.wysilek` (domyślnie Medium); `apl` może być pusty albo nieokreślony. */
PK.etykietaModelu = (apl) => ({ model: (apl && apl.model) || PK.MODEL_DOMYSLNY, poziom: (apl && apl.wysilek) || PK.WYSILEK_DOMYSLNY });

/* Przycisk wyboru modelu w rzędzie pod polem wiadomości: nieaktywny, dopóki ćwiczenie nie czeka na jego kliknięcie (PK.modelCwiczenia). Pokazuje „<model> <poziom>” (zrzuty 03-58-01, 04-24-16: nazwa jasna, poziom szary): model z `aplikacja.model` albo domyślny Opus 5.5, poziom z `aplikacja.wysilek` albo Medium. */
PK.przyciskModelu = (apl) => {
  const e = PK.etykietaModelu(apl);
  const opis = `${PK.OPIS_WYBORU_MODELU}: ${e.model} ${e.poziom}`;
  return `<button type="button" class="apl-chip apl-model" aria-disabled="true" aria-label="${PK.esc(opis)}"><span class="apl-model-nazwa">${PK.esc(e.model)}</span><span class="apl-model-poziom">${PK.esc(e.poziom)}</span></button>`;
};

/* Menu (zrzut 04-24-16): cztery wiersze modeli (nazwy ze zrzutu, ✓ przy wybranym modelu: z `aplikacja.model` albo domyślnym Opus 5.5, cyfra skrótu 2, 3, 4 przy pozostałych), kreska, wiersz Effort (napis, bieżący poziom jako tekst, strzałka), kreska, More models ze strzałką, kreska, część Fast mode (nagłówek, Enable fast mode z podpisem i pigułka Buy credits). Bez nagłówka; wiersze poza Effort są nieaktywne. Cyfry „1” zrzut nie pokazuje (model pierwszy stoi tam zawsze wybrany), więc niewybrany pierwszy model dostaje w jej miejscu szary pasek. */
PK.menuModelu = (apl) => {
  const { esc } = PK;
  const M = PK.NAPISY_EKRANU.model;
  const e = PK.etykietaModelu(apl);
  const szary = (d) => `<span class="apl-szkic" style="width:${d}px"></span>`;
  const strzalka = `<span class="apl-menu-strzalka" aria-hidden="true">${PK.IKONY_APLIKACJI.dalej}</span>`;
  const ptak = `<span class="apl-ptak" aria-hidden="true">${PK.IKONY_ZGODY.tak}</span>`;
  const nazwany = (n, i) => {
    const prawa = n === e.model ? ptak : i === 0 ? szary(8) : `<span class="apl-menu-skrot">${i + 1}</span>`;
    return `<li role="none"><span class="apl-menu-poz apl-menu-szary apl-menu-model${n === e.model ? " wybrany" : ""}"><span class="apl-menu-nazwa">${esc(n)}</span>${prawa}</span></li>`;
  };
  const modele = PK.NAPISY_MODELI.map(nazwany);
  const poziom = `<span class="apl-menu-poziom">${esc(e.poziom)}</span>`;
  const kreska = `<li role="separator" class="apl-menu-kreska"></li>`;
  return (
    `<ul class="apl-menu-modelu" role="menu" hidden>` +
    modele.join("") +
    kreska +
    `<li role="none"><button type="button" class="apl-menu-poz apl-menu-effort" role="menuitem" aria-haspopup="menu" aria-disabled="true"><span>${esc(PK.NAPISY_APLIKACJI.effort)}</span><span class="apl-menu-reszta">${poziom}${strzalka}</span></button></li>` +
    kreska +
    `<li role="none" aria-hidden="true"><span class="apl-menu-poz apl-menu-szary"><span>${esc(M.wiecej)}</span>${strzalka}</span></li>` +
    kreska +
    `<li role="none" aria-hidden="true" class="apl-menu-sekcja">${esc(M.szybki)}</li>` +
    `<li role="none" aria-hidden="true"><span class="apl-menu-poz apl-menu-szary apl-menu-szybki"><span class="apl-menu-dwie"><span>${esc(M.wlacz)}</span><small>${esc(M.kredyty)}</small></span>${PK.pigulka(M.kup, "apl-pig-kup")}</span></li>` +
    `</ul>`
  );
};

/* Lista poziomów (zrzut 04-24-29): zdanie u góry, pięć wierszy poziomów w kolejności ze zrzutu (numer od góry w data-poziom: Low 1, Medium 2 z pigułką Recommended, High 3, Extra 4, Max 5 z pigułką ostrzeżenia), szósty wiersz Ultracode bez skutku (ustawienie, nie poziom), notka kursu przy klikniętym wierszu. */
PK.listaWysilku = () => {
  const { esc } = PK;
  const W = PK.NAPISY_EKRANU.wysilek;
  const ptak = `<span class="apl-ptak" aria-hidden="true">${PK.IKONY_ZGODY.tak}</span>`;
  const poziomy = [
    [W.low, ""],
    [W.medium, PK.pigulka(W.polecany, "apl-pig-polecany")],
    [W.high, ""],
    [W.extra, ""],
    [W.max, PK.pigulka(W.ostrzezenie, "apl-pig-ostrzezenie", PK.IKONY_EKRANU.ostrzezenie)],
  ];
  const wiersze = poziomy
    .map(
      ([nazwa, pigulka], i) =>
        `<li role="none"><button type="button" class="apl-menu-poz apl-poziom" role="menuitemradio" aria-checked="false" aria-disabled="true" data-poziom="${i + 1}"><span class="apl-poziom-nazwa">${esc(nazwa)}</span>${pigulka}${ptak}</button></li>`,
    )
    .join("");
  return (
    `<div class="apl-menu-wysilku" role="menu" hidden>` +
    `<p class="apl-wysilek-opis">${esc(W.opis)}</p>` +
    `<ul>${wiersze}<li role="none" aria-hidden="true"><span class="apl-menu-poz apl-menu-szary apl-ultracode">${esc(W.ultracode)}</span></li></ul>` +
    `<span class="apl-model-notka" hidden></span></div>`
  );
};

/* Rzędy ze znacznikiem „kliknij tutaj” (PK.celKroku): pod rzędem z przyciskiem, pod wierszem Effort, pod wybranym wierszem poziomu. */
Object.assign(PK.PO_CELU_KROKU, { "wybor-modelu": ".apl-rzad", effort: "li", poziom: "li" });

/* Menu w ćwiczeniu `sek` z drogami: dokłada menu i listę do rzędu pod polem tylko wtedy, gdy któraś droga ma krok `klik` `wybor-modelu`; w innych ćwiczeniach przycisk zostaje nieaktywny (kursor zwykły, bez podświetlenia, bez skutku). Zwraca {zapowiedz, znacznik, po, reset} albo null.
   `zapowiedz(k)` uaktywnia element, który czeka na klik (przycisk, wiersz Effort albo wiersz poziomu z kroku); `znacznik(k, el)` stawia znacznik „kliknij tutaj” na `el`, a gdy menu zamknął pierścień zużycia, na przycisku modelu (jego klik otwiera menu z powrotem); `po(k, przerwano)` pokazuje skutek kliknięcia; `reset()` zamyka wszystko i zdejmuje ✓ i notkę („Od nowa” i nowe polecenie drogi). */
PK.modelCwiczenia = function (cw, sek) {
  const uzywa = (cw.drogi || []).some((d) => (d.kroki || []).some((k) => k.typ === "klik" && k.cel === "wybor-modelu"));
  const okno = sek.querySelector(".apl-okno");
  const rzad = sek.querySelector(".apl-rzad");
  const przycisk = rzad && rzad.querySelector(".apl-model");
  if (!uzywa || !przycisk) return null;
  const apl = cw.aplikacja || {};
  const e = PK.etykietaModelu(apl); /* model (domyślnie Opus 5.5) i poziom (domyślnie Medium) na starcie ćwiczenia */
  rzad.insertAdjacentHTML("beforeend", PK.menuModelu(apl) + PK.listaWysilku());
  const menu = rzad.querySelector(".apl-menu-modelu");
  const lista = rzad.querySelector(".apl-menu-wysilku");
  const notka = lista.querySelector(".apl-model-notka");
  const effort = menu.querySelector(".apl-menu-effort");
  let poziom = e.poziom; /* poziom wysiłku na przycisku: z `aplikacja.wysilek` albo Medium, po wyborze w menu wybrany poziom do „Od nowa” albo nowego polecenia */
  const POZIOMY = PK.POZIOMY_WYSILKU;
  /* przycisk, wiersz Effort i opis dla czytnika ekranu pokazują bieżący poziom; ✓ na liście stoi przy nim (zrzut 04-24-29) */
  const odswiezPoziom = () => {
    przycisk.setAttribute("aria-label", `${PK.OPIS_WYBORU_MODELU}: ${e.model} ${poziom}`);
    przycisk.querySelector(".apl-model-poziom").textContent = poziom;
    effort.querySelector(".apl-menu-poziom").textContent = poziom;
  };
  const zaznaczPoziom = (nr) =>
    lista.querySelectorAll(".apl-poziom").forEach((b, i) => {
      b.classList.toggle("wybrany", i + 1 === nr);
      b.setAttribute("aria-checked", String(i + 1 === nr));
    });
  let menuOtwarte = false;
  let listaOtwarta = false;
  let czeka = null; /* krok klik, który czeka na element menu (po `zapowiedz`, do `po`) */
  let uspione = null; /* {lista}: menu zamknął pierścień zużycia, gdy krok czekał na jego element; przycisk modelu otwiera je z powrotem */
  let konczy = false; /* poziom wybrany: ✓ i notka stoją, menu zaraz samo się zamknie */

  const element = (k) =>
    k.cel === "wybor-modelu" ? przycisk : k.cel === "effort" ? effort : lista.querySelector(`.apl-poziom[data-poziom="${k.poziom}"]`);
  const wlacz = (el, tak) => (tak ? el.removeAttribute("aria-disabled") : el.setAttribute("aria-disabled", "true"));

  /* menu stoi nad przyciskiem (jego prawa krawędź na prawej krawędzi przycisku, w obrębie rzędu); przycisk jest przy prawym końcu rzędu, więc lista poziomów otwiera się z lewej strony menu, a w wąskim oknie w miejscu menu; notka stoi po zewnętrznej stronie listy, ze strzałką do wiersza */
  const uloz = () => {
    const szer = rzad.clientWidth;
    const waski = szer < PK.WASKIE_OKNO_MODELU;
    const prawa = Math.min(szer, przycisk.offsetLeft + przycisk.offsetWidth);
    const miejsce = Math.max(prawa, PK.NAJMNIEJ_MIEJSCA_MODELU); /* wąski rząd: menu i lista nie szersze niż miejsce do prawej krawędzi przycisku, więc lista w miejscu menu kończy się na jego krawędzi */
    const sMenu = Math.min(PK.SZEROKOSC_MENU_MODELU, miejsce);
    const sLista = Math.min(waski ? PK.SZEROKOSC_LISTY_WASKIEJ : PK.SZEROKOSC_LISTY_WYSILKU, miejsce);
    menu.hidden = !menuOtwarte || (waski && listaOtwarta);
    lista.hidden = !listaOtwarta;
    lista.classList.toggle("apl-menu-waska", waski);
    const lMenu = Math.max(0, prawa - sMenu);
    const lLista = Math.max(0, waski ? prawa - sLista : lMenu - 8 - sLista);
    Object.assign(menu.style, { width: sMenu + "px", left: lMenu + "px" });
    Object.assign(lista.style, { width: sLista + "px", left: lLista + "px" });
    notka.style.maxWidth = Math.max(90, Math.min(PK.SZEROKOSC_NOTKI, lLista - 16)) + "px";
    okno.classList.toggle("menu-modelu-otwarte", menuOtwarte || listaOtwarta);
    przycisk.classList.toggle("otwarty", menuOtwarte);
    effort.classList.toggle("otwarty", listaOtwarta);
    /* znacznik pod elementem liczy położenie od nowa po zmianie układu */
    sek.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
  };
  window.addEventListener("resize", uloz);

  /* menu, lista i notka zamknięte; ✓ na liście stoi przy bieżącym poziomie (z `aplikacja.wysilek`, domyślnie Medium, albo po wyborze poziomu) */
  const zamknij = () => {
    menuOtwarte = listaOtwarta = false;
    uspione = null;
    konczy = false;
    notka.hidden = true;
    notka.textContent = "";
    zaznaczPoziom(POZIOMY.indexOf(poziom) + 1);
    [przycisk, effort, ...lista.querySelectorAll(".apl-poziom")].forEach((el) => wlacz(el, false));
    uloz();
  };
  /* „Od nowa” i nowe polecenie drogi: także poziom na przycisku wraca do startowego */
  const reset = () => {
    poziom = e.poziom;
    odswiezPoziom();
    zamknij();
  };

  /* Otwarcie okienka pierścienia zamyka menu i listę (strona/aplikacja-pierscien.js). Krok, który czeka na element zamkniętego menu, nie może utknąć: przycisk modelu zostaje aktywny, znacznik przechodzi na niego, a jego klik otwiera menu (i listę, jeśli była) z powrotem. Gdy poziom jest już wybrany, menu i tak zaraz znika (reset). */
  okno.addEventListener(PK.ZAMKNIJ_MENU, () => {
    if (!menuOtwarte && !listaOtwarta) return;
    if (konczy) return zamknij();
    uspione = { lista: listaOtwarta };
    menuOtwarte = listaOtwarta = false;
    wlacz(przycisk, true);
    uloz();
    if (czeka) PK.celKroku(sek, "wybor-modelu", przycisk);
  });
  przycisk.addEventListener("click", () => {
    if (!uspione || przycisk.hasAttribute("aria-disabled")) return;
    menuOtwarte = true;
    listaOtwarta = uspione.lista;
    uspione = null;
    wlacz(przycisk, false);
    uloz();
    okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka */
    if (czeka) PK.celKroku(sek, czeka.cel, element(czeka)); /* znacznik wraca na element, na który czeka krok */
  });

  return {
    zapowiedz(k) {
      if (!PK.CELE_MODELU.includes(k.cel)) return;
      czeka = k;
      wlacz(element(k), true);
    },
    znacznik: (k, el) => (uspione && k.cel !== "wybor-modelu" ? PK.celKroku(sek, "wybor-modelu", przycisk) : PK.celKroku(sek, k.cel, el)),
    async po(k, przerwano) {
      if (!PK.CELE_MODELU.includes(k.cel)) return;
      czeka = null;
      const el = element(k);
      wlacz(el, false);
      if (k.cel === "wybor-modelu") {
        zamknij(); /* nowe otwarcie zaczyna bez notki, ✓ stoi tylko przy bieżącym poziomie */
        menuOtwarte = true;
        uloz();
        return okno.dispatchEvent(new CustomEvent(PK.MENU_OTWARTE)); /* okienko pierścienia się zamyka */
      }
      if (k.cel === "effort") {
        listaOtwarta = true;
        return uloz();
      }
      konczy = true;
      poziom = POZIOMY[k.poziom - 1]; /* przycisk w rzędzie od razu pokazuje wybrany poziom */
      odswiezPoziom();
      zaznaczPoziom(k.poziom);
      notka.textContent = k.notka;
      notka.hidden = false;
      uloz();
      notka.style.top = el.offsetTop + el.offsetHeight / 2 + "px"; /* strzałka notki na środku klikniętego wiersza */
      await PK.czekaj(PK.ZAMKNIECIE_MODELU_MS);
      if (!przerwano()) zamknij();
    },
    reset,
  };
};
