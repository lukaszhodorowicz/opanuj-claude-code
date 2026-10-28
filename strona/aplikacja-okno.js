/* Symulator aplikacji Claude, wygląd: składa HTML ćwiczenia (nagłówek, nauczyciel, polecenia, okno zakładki Code z widokiem zmian albo z miejscem na otwarty plik; pasek boczny z napisami ze zrzutów i kontem na dole, strona/aplikacja-ekran.js; panel szczegółów z kartami Environment, Context i Connectors, strona/aplikacja-panel.js; w rzędzie pod polem „This computer” i na końcu przycisk wyboru modelu i pierścień zużycia z okienkiem, strona/aplikacja-pierscien.js) ze scenariusza. */

/* Wiadomość w rozmowie; `plik` w odpowiedzi Claude staje się klikalną ścieżką (kropka albo przecinek zaraz po niej nie oddzielają się od niej przy zawinięciu linii), a `link` klikalnym linkiem (pierwsze wystąpienie w tekście). */
PK.dymekAplikacji = (w) => {
  const { esc } = PK;
  if (w.kto === "ty") return `<div class="apl-ty"><p>${w.skill ? `${PK.pasekSkilla(w.skill)} ` : ""}${esc(w.tekst)}</p></div>`; /* skill: podświetlony pasek bez tekstu przed tekstem (strona/aplikacja-plus.js) */
  let tekst = esc(w.tekst);
  if (w.plik) {
    const nazwa = esc(w.plik);
    const i = tekst.indexOf(nazwa);
    if (i >= 0) {
      const po = tekst.slice(i + nazwa.length);
      const znaki = po.match(/^[.,;:!?)”"…]+/)?.[0] || ""; /* znak po ścieżce: kropka nie ląduje sama na początku nowej linii */
      tekst = `${tekst.slice(0, i)}<button type="button" class="apl-sciezka">${nazwa}</button>${znaki ? `\u2060${znaki}` : ""}${po.slice(znaki.length)}`; /* U+2060 (łącznik słów) zabrania łamania linii przed znakiem; ścieżka zostawia dla znaku miejsce w linii (styl-aplikacja-zmiany.css) */
    }
  }
  if (w.link) {
    const adres = esc(w.link);
    const i = tekst.indexOf(adres);
    /* adres łamie się tylko po ukośniku (<wbr> nie dodaje znaku, więc zaznaczenie i kopiowanie dają cały adres) */
    if (i >= 0)
      tekst = `${tekst.slice(0, i)}<button type="button" class="apl-sciezka apl-link">${adres.replace(/(?<!:\/?)\//g, "/<wbr>")}</button>${tekst.slice(i + adres.length)}`;
  }
  const karta = w.karta && w.plik ? PK.kartaPliku(w.plik, w.karta.rozmiar) : ""; /* karta pliku (pole `karta_pliku` kroku claude, strona/aplikacja-plik-panel.js) stoi nad tekstem */
  return `<div class="apl-claude">${karta}<p>${tekst}</p></div>`;
};

PK.htmlAplikacji = function (cw, nr) {
  const { esc } = PK;
  const I = PK.IKONY_APLIKACJI;
  const N = PK.NAPISY_APLIKACJI;
  const apl = cw.aplikacja || {};
  const zmiany = apl.zmiany || [];
  const kroki = cw.kroki || [];
  const drogi = cw.drogi || [];
  /* drogi bez panelu szczegółów: licznika po prośbie kursanta nie podaje żaden fakt; panel zostaje tylko z kartą Context (`aplikacja.kontekst`), a karta Changes jest wtedy szarym paskiem bez licznika */
  const zSzyna = drogi.some((d) => (d.kroki || []).some((k) => k.typ === "klik" && k.cel === "ikona-tytulu")); /* pierwsza ikona paska tytułu (lista) z dymkiem „Show session rail” tylko w ćwiczeniu z krokiem klik ikona-tytulu (strona/aplikacja-plik-panel.js) */
  const wTle = PK.drogiZPracaWTle(drogi); /* droga z pracą w tle: ⋮ jest przyciskiem z menu (strona/aplikacja-w-tle.js), inaczej zostaje nieaktywny */
  const jestKontekst = drogi.length > 0 && apl.kontekst !== undefined;
  const kontekstEtapow = !!cw.etapy && apl.kontekst !== undefined; /* etapy zachowują kartę Changes, a karta Context pokazuje procent ze scenariusza i da się ją rozwinąć (strona/aplikacja.js) */
  const bezPanelu = (drogi.length > 0 && !jestKontekst) || apl.panel === "schowany";
  const szkic = (proc) =>
    `<span class="apl-szkic" style="width:${proc}%"></span>`;
  const licz = (z) => {
    const l = PK.licznikZmian(z);
    return `<span class="apl-plus">+${l.dodane}</span> <span class="apl-minus">-${l.usuniete}</span>`;
  };
  const przyciskPaska = (klucz, ikona) =>
    `<button type="button" class="apl-ikona" data-pasek="${klucz}" title="${esc(N[klucz])}" aria-label="${esc(N[klucz])}">${ikona}<span class="apl-dymek" aria-hidden="true">${esc(N[klucz])}</span></button>`;
  const B = PK.NAPISY_EKRANU.bok;
  const nowaSesja = `<li class="apl-bok-nowa">${esc(N.nowa)}</li>`;
  const znak = (l) =>
    l.zmiana === "dodana" ? "+" : l.zmiana === "usunieta" ? "-" : "";
  const linijka = (l) =>
    `<li class="apl-l ${esc(l.zmiana || "bez")}"><span class="apl-znak" aria-hidden="true">${znak(l)}</span><span class="apl-l-tekst">${esc(l.tekst)}</span></li>`;
  const plikZmian = (p, i) =>
    `<section class="apl-plik" data-p="${i}"><header>${I.plik}<b>${esc(p.plik)}</b></header>` +
    `<ol class="apl-linijki">${(p.linijki || []).map(linijka).join("")}</ol></section>`;
  const polecenie = (k, i, atr = "k") =>
    `<button class="polecenie" data-${atr}="${i}"><span class="polecenie-ikona"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg></span>` +
    `<span class="polecenie-tekst"><b>${esc(k.etykieta)}</b>${k.opis ? `<small>${esc(k.opis)}</small>` : ""}</span></button>`;

  const bok = `
    <aside class="apl-bok">
      <div class="apl-bok-gora">
        <span class="apl-swiatla"><i></i><i></i><i></i></span>
        <span class="apl-bok-strzalki">${I.bok}${I.wstecz}${I.dalej}</span>
        <span class="apl-zakladki"><span class="apl-zakladka">${I.czat}</span><span class="apl-zakladka wybrana" title="${esc(N.code)}" aria-label="${esc(N.code)}">${I.kod}</span></span>
      </div>
      <ul class="apl-bok-lista">${nowaSesja}${PK.pozycjaBokuZNapisem(I.szukaj, B.szukaj)}${PK.pozycjaBokuZNapisem(I.karty, B.artefakty)}${PK.pozycjaBokuZNapisem(I.dzwonek, B.dyzur)}${PK.pozycjaBokuZNapisem(I.teczka, B.dostosuj)}${PK.pozycjaBokuZNapisem(I.kropki, B.wiecej)}</ul>
      ${apl.sesje ? PK.sesjeBok(apl) : `<div class="apl-bok-sesje">${szkic(40)}<span class="apl-sesja">${szkic(78)}</span>${szkic(66)}</div>`}
      ${PK.kontoBoku()}
    </aside>`;
  const pasek = `
    <div class="apl-pasek">
      ${PK.tytulRozmowy(apl.nazwa)}
      <span class="apl-pasek-przyciski">${zSzyna ? PK.ikonaSzyny() : ""}${przyciskPaska("terminal", I.terminal)}${przyciskPaska("changes", I.zmiany)}${przyciskPaska("browser", I.przegladarka)}${przyciskPaska("files", I.plik)}${wTle ? PK.przyciskMenuPaska(I.kropkiPionowe) : `<span class="apl-ikona apl-bez">${I.kropkiPionowe}</span>`}</span>
    </div>`;
  const czat = `
    <div class="apl-czat">
      <div class="apl-rozmowa">${(apl.rozmowa || []).map((w) => PK.dymekAplikacji({ kto: w.kto, tekst: w.tekst })).join("")}</div>
      <div class="apl-pole"><span class="apl-pole-plus">${I.plus}</span><span class="apl-pole-tekst" ${PK.atrybutyPola()}></span><span class="apl-pole-wyslij">${I.wyslij}</span></div>
      <div class="apl-rzad">
        ${apl.srodowisko === "Local" ? `<span class="apl-chip apl-chip-komputer">${I.laptop}<span>${esc(PK.NAPISY_EKRANU.panel.komputer)}</span></span>` : `<span class="apl-chip" title="${esc(apl.srodowisko || "")}">${I.laptop}</span>`}
        ${PK.folderyRozmow(apl) ? PK.kontrolkaFolderu(I.folder, apl.folder || "") : `<span class="apl-chip">${I.folder}<span>${esc(apl.folder || "")}</span></span>`}
        <span class="apl-chip apl-tryb">${esc(apl.tryb || "")}</span>
        ${PK.przyciskModelu(apl)}${PK.przyciskPierscienia()}
        ${PK.okienkoZuzycia()}
      </div>
    </div>`;
  const kartaZmian = `<div class="apl-karta apl-karta-zmiany"><b>${esc(N.changes)}</b><button type="button" class="apl-licznik">${licz(zmiany)}</button></div>`;
  const kartyPanelu = `<div class="apl-panel">${PK.kartyPanelu(apl, jestKontekst ? "" : kartaZmian, jestKontekst || kontekstEtapow ? apl.kontekst : undefined)}</div>`;
  const panel = !drogi.length
    ? `${kartyPanelu}<div class="apl-widok-zmian" hidden>${zmiany.map(plikZmian).join("")}</div>`
    : (jestKontekst ? kartyPanelu : "") + '<div class="apl-widok-pliku" hidden></div>';

  return `
    <section class="cwiczenie cwiczenie-apl" id="${esc(cw.id)}">
      <div class="naglowek"><span class="etykieta">Ćwiczenie ${nr}</span><h3>${esc(cw.tytul)}</h3></div>
      ${cw.opis ? `<p class="opis">${esc(cw.opis)}</p>` : ""}
      ${PK.nauczycielHtml(cw.nauczyciel_start)}
      <div class="polecenia">${drogi.length ? drogi.map((d, i) => polecenie(d, i, "d")).join("") : kroki.map((k, i) => polecenie(k, i)).join("")}</div>
      <p class="apl-podpis">Aplikacja Claude na komputer, zakładka Code</p>
      <div class="apl-okno${bezPanelu ? " bez-panelu" : ""}${apl.sesje ? " apl-sesje" : ""}"${apl.konto_ustawien ? ` data-konto-ustawien="${esc(apl.konto_ustawien)}"` : ""}>${bok}<div class="apl-glowna">${pasek}<div class="apl-uklad">${czat}${panel}</div>${apl.sesje ? PK.widokListySesji() : ""}</div></div>
      <div class="przycisk-klaw"><button class="btn jasny" data-od-nowa>${esc(cw.przycisk || "Od nowa")}</button><small>Ćwiczenie zacznie się od początku.</small></div>
    </section>`;
};
