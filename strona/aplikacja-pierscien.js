/* Symulator aplikacji Claude, pierścień zużycia abonamentu: pusty okrąg w rzędzie pod polem wiadomości (ostatni element rzędu, za przyciskiem wyboru modelu) i okienko nad nim, które otwiera klik: nagłówek „Plan usage limits” z „See all”, wiersze Session limit, Weekly · all models i Cloud session credits z podpisami (napisy ze zrzutu Łukasza 27.10.2026, plik 04-24-40; strona/aplikacja-ekran.js); nazwa planu, procenty, terminy i kwota to dane konta, więc szare paski, a paski postępu są puste. Pierścień jest aktywny w każdym ćwiczeniu aplikacji; krok `klik` z celem `pierscien` (ćwiczenie z drogami) czeka, aż okienko będzie otwarte. Wygląd: strona/styl-aplikacja-pierscien.css, zrzuty z sieci materialy/zrzuty-aplikacji/pierscien-zuzycia/pierscien-przy-wyborze-modelu-z-popover.png. */

/* Opis przycisku i okienka dla czytnika ekranu (ten sam): napis kursu po polsku, nie napis interfejsu (dokumentacja go nie podaje). */
PK.OPIS_PIERSCIENIA = "Zużycie abonamentu";

/* Zdarzenia na oknie aplikacji, którymi menu rzędu (model, tryby, +) i okienko pierścienia zamykają się wzajemnie: `apl-menu-otwarte` mówi, że któreś menu właśnie się otworzyło (okienko się zamyka); `apl-zamknij-menu` mówi, że otworzyło się okienko (każde menu się zamyka). */
PK.MENU_OTWARTE = "apl-menu-otwarte";
PK.ZAMKNIJ_MENU = "apl-zamknij-menu";

/* Przycisk w rzędzie: okrąg 14 px, kreska 2 px w kolorze ikon rzędu (currentColor), bez łuku i bez koloru ostrzeżenia. */
PK.przyciskPierscienia = () =>
  `<button type="button" class="apl-pierscien" aria-haspopup="true" aria-expanded="false" aria-label="${PK.esc(PK.OPIS_PIERSCIENIA)}">` +
  `<svg viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>`;

/* Okienko (zrzut 04-24-40): nagłówek „Plan usage limits · [plan]” z odnośnikiem „See all →”, pod nim trzy grupy: Session limit z podpisem i procentem, Weekly · all models z terminem odnowienia i procentem, Cloud session credits (ikona ?) z kwotą i terminem wygaśnięcia; pod każdym wierszem pusty pasek postępu. Plan, procenty, terminy i kwota to szare paski (dane konta), „See all” bez skutku. */
PK.okienkoZuzycia = () => {
  const R = PK.NAPISY_EKRANU.pierscien;
  const E = PK.IKONY_EKRANU;
  const pasek = (d) => `<span class="apl-szkic" style="width:${d}px"></span>`;
  const wiersz = (nazwa, podpis, wartosc = "", ikona = "") =>
    `<div class="apl-okienko-wiersz"><b>${PK.esc(nazwa)}</b>${ikona}<span class="apl-okienko-podpis">${podpis}</span>${wartosc}</div>`;
  const tor = `<span class="apl-okienko-tor"></span>`;
  return (
    `<div class="apl-okienko-zuzycia" role="group" aria-label="${PK.esc(PK.OPIS_PIERSCIENIA)}" hidden>` +
    `<div class="apl-okienko-glowa"><span class="apl-okienko-naglowek">${PK.esc(R.naglowek)} · ${pasek(34)}</span><span class="apl-okienko-wszystko">${PK.esc(R.wszystko)}${E.strzalka}</span></div>` +
    `<div class="apl-okienko-grupa">${wiersz(R.sesja, PK.esc(R.start), pasek(16))}${tor}</div>` +
    `<div class="apl-okienko-grupa">${wiersz(R.tydzien, `${PK.esc(R.odnowa)} ${pasek(46)}`, pasek(16))}${tor}</div>` +
    `<div class="apl-okienko-grupa">${wiersz(R.chmura, pasek(46), "", `<span class="apl-okienko-pytajnik">${E.pytajnik}</span>`)}${tor}<span class="apl-okienko-podpis">${PK.esc(R.wygasa)} ${pasek(70)}</span></div>` +
    `</div>`
  );
};

/* Rząd ze znacznikiem „kliknij tutaj” stoi za całym rzędem pod polem (PK.celKroku), strzałka na środku pierścienia. */
PK.PO_CELU_KROKU.pierscien = ".apl-rzad";

/* Pierścień w ćwiczeniu `sek` (każdy rodzaj: kroki, etapy, drogi). Zwraca {krok, otwarte, reset}:
   - krok(zyje): gra krok `klik` z celem `pierscien`: gdy okienko jest już otwarte (wcześniejszy klik je zostawił), nie czeka; inaczej stawia znacznik i czeka na klik w pierścień. Okienko zostaje otwarte po kroku. `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane;
   - otwarte(): czy okienko jest otwarte;
   - reset(): okienko zamknięte, czekający krok porzucony.
   Okienko otwiera i zamyka klik w pierścień (w drugą stronę niż inne miejsca: klik gdzie indziej go nie zamyka, także w kartę Context). Zamykają je też „Od nowa”, nowe polecenie drogi i otwarcie menu modelu, trybów albo + (reguła symulatora). Odwrotnie, otwarcie okienka zamyka każde z tych menu, ale krok czekający na ich element nie utyka: menu same oddają znacznik swojemu przyciskowi, a klik w niego otwiera menu z powrotem (aplikacja-model.js, aplikacja-plus.js, aplikacja-tryby.js). */
PK.pierscienCwiczenia = function (cw, sek) {
  const okno = sek.querySelector(".apl-okno");
  const rzad = sek.querySelector(".apl-rzad");
  const przycisk = rzad.querySelector(".apl-pierscien");
  const okienko = rzad.querySelector(".apl-okienko-zuzycia");
  const zKrokiem = (cw.drogi || []).some((d) => (d.kroki || []).some((k) => k.typ === "klik" && k.cel === "pierscien"));
  if (zKrokiem) rzad.classList.add("apl-rzad-z-pierscieniem"); /* do 720 px pierścień i przycisk modelu zostają w rzędzie tylko w takim ćwiczeniu (styl-aplikacja-model.css) */
  let otwarte = false;
  let czeka = null; /* krok klik czeka na otwarcie okienka: funkcja wznawiająca */

  const ustaw = (tak) => {
    if (tak === otwarte) return;
    otwarte = tak;
    okienko.hidden = !tak;
    przycisk.classList.toggle("otwarty", tak);
    przycisk.setAttribute("aria-expanded", String(tak));
    okno.classList.toggle("okienko-zuzycia-otwarte", tak);
    if (!tak) return;
    okno.dispatchEvent(new CustomEvent(PK.ZAMKNIJ_MENU));
    if (czeka) czeka();
  };
  const reset = () => {
    czeka = null;
    ustaw(false);
  };

  przycisk.addEventListener("click", () => ustaw(!otwarte));
  okno.addEventListener(PK.MENU_OTWARTE, () => ustaw(false));
  /* w fazie przechwytywania: reset przed obsługą kliku przez resztę ćwiczenia, bo pierwszy krok drogi bywa klik w pierścień */
  sek.addEventListener("click", (e) => { if (e.target.closest("[data-od-nowa], .polecenie[data-d]")) reset(); }, true);

  return {
    otwarte: () => otwarte,
    reset,
    async krok(zyje) {
      if (otwarte) return;
      PK.celKroku(sek, "pierscien", przycisk);
      await new Promise((wznow) => (czeka = wznow));
      czeka = null;
      if (zyje()) PK.celKroku(sek, "pierscien", null);
    },
  };
};
