/* Symulator aplikacji Claude, wygląd telefonu z Remote Control (nowy wygląd kursu, nie kopia zdjęcia, D-2026-10-27-52): zaokrąglona ramka, pasek stanu bez prawdziwych danych, ekran „Code” z urządzeniem i listą sesji (zrzuty IMG_1056-IMG_1058) i ekran otwartej rozmowy z polem „Reply to Claude or hold to talk” (IMG_1059). Napisy i opisy: strona/aplikacja-telefon-dane.js, gra: strona/aplikacja-telefon.js. */

/* Ramka telefonu z oboma ekranami; `apl` to obiekt `aplikacja` ćwiczenia (`telefon.urzadzenie`, `telefon.sesja`, `folder`). Ekran listy stoi na starcie, ekran rozmowy ma `hidden`. */
PK.htmlTelefonu = (apl) => {
  const { esc } = PK;
  const N = PK.NAPISY_TELEFONU;
  const O = PK.OPISY_TELEFONU;
  const I = PK.IKONY_TELEFONU;
  const T = apl.telefon || {};
  const przycisk = (ikona, klasa = "") => `<span class="apl-tel-przycisk ${klasa}" aria-hidden="true">${ikona}</span>`;
  const pasek = (d, klasa = "") => `<span class="apl-szkic ${klasa}" style="width:${d}%"></span>`;

  const stan = `<div class="apl-tel-stan" aria-hidden="true"><span class="apl-szkic apl-tel-czas"></span><span class="apl-tel-wyspa"></span><span class="apl-tel-stan-ikony">${I.sygnal}${I.wifi}${I.bateria}</span></div>`;

  /* wiersz sesji z komputera (zrzut IMG_1057): pierścień, tytuł ze scenariusza i podpis „now” z zieloną ikoną laptopa; na liście stoi pierwszy */
  const moja =
    `<li><button type="button" class="apl-tel-sesja apl-tel-moja" aria-label="${esc(O.sesja)}: ${esc(T.sesja || "")}"><span class="apl-tel-kolo"></span>` +
    `<span class="apl-tel-opis"><b>${esc(T.sesja || "")}</b><small>${esc(N.teraz)}<span class="apl-tel-zielona">${I.laptop}</span></small></span></button></li>`;
  /* pozostałe sesje (zrzuty IMG_1056-IMG_1058): pierścień, dwa szare paski, ikona chmury i niebieska kropka; tytuły i godziny to dane konta */
  const inna = (a, b) =>
    `<li class="apl-tel-inna" aria-hidden="true"><span class="apl-tel-kolo"></span><span class="apl-tel-opis">${pasek(a, "apl-tel-pasek-tytul")}<small>${pasek(b)}<span class="apl-tel-chmura">${I.chmura}</span></small></span><i class="apl-tel-kropka"></i></li>`;
  const lista =
    `<section class="apl-tel-ekran-lista" data-ekran="lista">` +
    `<header class="apl-tel-gora">${przycisk(I.menu)}<b class="apl-tel-tytul">${esc(N.tytul)}</b>${przycisk(I.zegar + I.suwaki, "apl-tel-dwa")}</header>` +
    `<div class="apl-tel-tresc">` +
    `<div class="apl-tel-grupa"><span>${esc(N.urzadzenia)}</span><span class="apl-tel-plus" aria-hidden="true">${I.plus}</span></div>` +
    `<span class="apl-tel-urzadzenie"><span class="apl-tel-ikona-ur">${I.laptop}<i class="apl-tel-zielona-kropka"></i></span><span class="apl-tel-nazwa-ur">${esc(T.urzadzenie || "")}</span></span>` +
    `<div class="apl-tel-grupa"><span>${esc(N.sesje)}</span></div>` +
    `<ul class="apl-tel-sesje">${moja}${inna(70, 56)}${inna(58, 48)}${inna(64, 52)}${inna(76, 44)}${inna(54, 50)}${inna(68, 58)}</ul>` +
    `</div>` +
    `<div class="apl-tel-dol">${przycisk(I.szukaj, "apl-tel-okragly")}<span class="apl-tel-nowa">${I.plus}<span>${esc(N.nowa)}</span></span></div>` +
    `</section>`;

  /* ekran rozmowy: wiadomości wstawia lustro rozmowy z okna (strona/aplikacja-telefon.js); pole z podpowiedzią i rząd z plusem, modelem, mikrofonem i strzałką wysyłania */
  const rozmowa =
    `<section class="apl-tel-ekran-rozmowa" data-ekran="rozmowa" hidden>` +
    `<header class="apl-tel-gora apl-tel-gora-rozmowy"><button type="button" class="apl-tel-przycisk apl-tel-wstecz" aria-label="${esc(O.wstecz)}">${I.wstecz}</button>` +
    `<div class="apl-tel-tytuly"><b>${esc(T.sesja || "")}</b><small>${esc(apl.folder || "")}</small></div>` +
    `${przycisk('<i class="apl-tel-kolko"></i>', "apl-tel-praca")}${przycisk(I.kropki)}</header>` +
    `<div class="apl-tel-wiadomosci"></div>` +
    `<div class="apl-tel-pole"><div class="apl-tel-wiersz-pola"><span class="apl-tel-wpis"></span><span class="apl-tel-podpowiedz">${esc(N.podpowiedz)}</span></div>` +
    `<div class="apl-tel-pole-dol">${przycisk(I.plus, "apl-tel-okragly")}<span class="apl-tel-model">${esc(N.model)} <span>${esc(N.wysilek)}</span></span><span class="apl-tel-rozpor"></span>` +
    `${przycisk(I.mikrofon, "apl-tel-okragly")}${przycisk(I.wyslij, "apl-tel-okragly apl-tel-wyslij")}</div></div>` +
    `</section>`;

  return (
    `<div class="apl-telefon" role="group" aria-label="${esc(O.ramka)}"><div class="apl-tel-ramka"><div class="apl-tel-szklo">${stan}${lista}${rozmowa}</div></div>` +
    `<p class="apl-tel-podpis">${esc(O.podpis)}</p></div>`
  );
};

/* Dymek wiadomości na telefonie: kursant w ciemnym dymku po prawej, Claude zwykłym tekstem (zrzut IMG_1059). Tekst to ten sam tekst co w oknie na komputerze; ścieżka pliku jest zwykłym tekstem, bo telefon niczego nie otwiera. */
PK.dymekTelefonu = (kto, tekst) => `<div class="apl-tel-${kto === "ty" ? "ty" : "claude"}"><p>${PK.esc(tekst)}</p></div>`;
