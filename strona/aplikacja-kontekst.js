/* Symulator aplikacji Claude, karta Context w panelu szczegółów (ćwiczenie z drogami albo z etapami i polem `aplikacja.kontekst`; w etapach tylko procent i rozwinięcie po kliku, bez kroków i bez zmiany procentu): nagłówek z napisem Context, strzałką i procentem; po kliknięciu otwarta karta z wierszem „N% used” i licznikiem, paskiem zajętości i wierszami kategorii z nazwami ze zrzutu Łukasza 27.10.2026 (treść: strona/aplikacja-kontekst-tresc.js; liczby wynikają z procentu karty). Krok `kontekst` zmienia procent z krótkim mignięciem; po `klik` `nowa-rozmowa` panel znika, a po pierwszej prośbie wraca z kartą bez procentu (szary pasek w jego miejscu) do najbliższego kroku `kontekst`. Układ karty ze zrzutu z sieci: materialy/zrzuty-aplikacji/karta-context/karta-context-otwarta-panel-szczegolow.png. */

/* Jedyny napis tej karty; test sprawdza go w dane/napisy-interfejsu.yaml (gdzie: aplikacja). Procent to wzór z tej listy. */
PK.NAPISY_KONTEKSTU = { context: "Context" };

PK.MIGNIECIE_KONTEKSTU_MS = 700; /* tyle trwa krok `kontekst`: kursant widzi mignięcie, zanim ruszy dalej droga */

/* Wnętrze karty (nagłówek i ukryta treść) dla procentu `proc`; to samo wnętrze karta dostaje na starcie i po „Od nowa”, więc stan startowy jest zawsze taki sam. `proc` = null to karta nowej rozmowy przed pierwszą liczbą: szary pasek w miejscu procentu i pusty pasek zajętości (stan bez treści: żaden fakt nie podaje wartości przed pierwszym krokiem `kontekst`). */
PK.kontekstWnetrze = (proc, statyczna = false) => {
  const tag = statyczna ? "div" : "button"; /* karta statyczna nie ma przycisku: nagłówek, który niczego nie robi, nie łapie fokusu klawiatury */
  const atrybuty = statyczna ? "" : ' type="button" aria-expanded="false"';
  return (
    `<${tag} class="apl-kontekst-naglowek"${atrybuty}><b>${PK.esc(PK.NAPISY_KONTEKSTU.context)}</b>` +
    `<span class="apl-kontekst-strzalka">${PK.IKONY_EKRANU.prawo}</span><span class="apl-kontekst-proc">${proc === null ? '<span class="apl-szkic apl-kontekst-brak"></span>' : `${proc}%`}</span></${tag}>` +
    `<div class="apl-kontekst-tresc" hidden>${PK.kontekstTresc(proc)}</div>`
  );
};

/* `statyczna`: karta w ćwiczeniu bez `aplikacja.kontekst` (kroki, etapy): stoi w panelu jak na zrzucie, ale niczego nie otwiera (klasa `apl-karta-statyczna`, nagłówek jest `div`, nie przyciskiem). */
PK.kartaKontekstu = (proc, statyczna = false) => `<div class="apl-karta apl-karta-kontekst${statyczna ? " apl-karta-statyczna" : ""}">${PK.kontekstWnetrze(proc, statyczna)}</div>`;

/* Karta w ćwiczeniu `sek`: klik w nagłówek otwiera i zamyka kartę (kursant może to zrobić w każdej chwili). Zwraca {otworz, ustaw, nowaRozmowa, pokazPanel, reset} albo null, gdy ćwiczenie nie ma `aplikacja.kontekst`. `ustaw(proc)` zmienia procent i pasek, miga procentem i kończy się po mignięciu; `nowaRozmowa()` chowa panel szczegółów (nowa sesja jeszcze się nie zaczęła) i zamyka kartę bez procentu; `pokazPanel()` pokazuje panel z powrotem (sesja startuje po wysłaniu pierwszej prośby), karta zostaje bez procentu do kroku `kontekst`. */
PK.kontekstCwiczenia = function (cw, sek) {
  const start = (cw.aplikacja || {}).kontekst;
  const karta = sek.querySelector(".apl-karta-kontekst");
  const okno = sek.querySelector(".apl-okno");
  if (start === undefined || !karta) return null;
  let miga = null;
  let biezacy = start; /* procent na karcie (null: szary pasek bez liczby) */
  let klucz = "start"; /* rozmowa, której procent stoi na karcie: „start”, id wiersza aplikacja.sesje albo „nowa” */
  const zapisane = {}; /* ostatni procent rozmów, które kursant opuścił: powrót do rozmowy go przywraca */
  const pokaz = (proc) => { /* karta zamknięta z procentem `proc` (null: szary pasek) */
    clearTimeout(miga);
    biezacy = proc;
    karta.className = "apl-karta apl-karta-kontekst";
    karta.innerHTML = PK.kontekstWnetrze(proc);
  };
  const otworz = (tak) => {
    karta.classList.toggle("otwarta", tak);
    karta.querySelector(".apl-kontekst-naglowek").setAttribute("aria-expanded", String(tak));
    karta.querySelector(".apl-kontekst-tresc").hidden = !tak;
  };
  karta.addEventListener("click", (e) => {
    if (e.target.closest(".apl-kontekst-naglowek")) otworz(!karta.classList.contains("otwarta"));
  });
  return {
    otworz: () => otworz(true),
    ustawCicho: (proc) => pokaz(proc), /* podgląd w tekście lekcji: nowy procent bez mignięcia i bez czekania, karta zamknięta */
    ustaw(proc) {
      biezacy = proc;
      const el = karta.querySelector(".apl-kontekst-proc");
      el.textContent = `${proc}%`;
      karta.querySelector(".apl-kontekst-zajete").style.width = `${proc}%`;
      PK.kontekstLiczby(karta, proc);
      el.classList.remove("mignij");
      void el.offsetWidth;
      el.classList.add("mignij");
      clearTimeout(miga);
      miga = setTimeout(() => el.classList.remove("mignij"), PK.MIGNIECIE_KONTEKSTU_MS);
      return PK.czekaj(PK.MIGNIECIE_KONTEKSTU_MS);
    },
    nowaRozmowa() {
      zapisane[klucz] = biezacy;
      klucz = "nowa";
      pokaz(null);
      okno.classList.add("panel-ukryty");
    },
    /* Kursant otworzył inną rozmowę z paska bocznego (`klik` `sesja` albo `wiadomosc-od`): karta pokazuje procent tej rozmowy, zamknięta. Rozmowa, którą kursant już widział, wraca do swojego ostatniego procentu; rozmowa z wiersza `aplikacja.sesje` z polem `kontekst` startuje od niego, a bez pola ma szary pasek zamiast liczby (żaden fakt nie podaje jej procentu). `nowa` obsługuje nowaRozmowa. */
    rozmowa(nowy, procent) {
      if (nowy === "nowa" || nowy === klucz) return;
      zapisane[klucz] = biezacy;
      klucz = nowy;
      pokaz(nowy in zapisane ? zapisane[nowy] : typeof procent === "number" ? procent : null);
      okno.classList.remove("panel-ukryty"); /* rozmowa z listy już działa: jej panel szczegółów stoi (po `+ New` był schowany do pierwszej prośby) */
    },
    pokazPanel: () => okno.classList.remove("panel-ukryty"),
    reset() {
      klucz = "start";
      Object.keys(zapisane).forEach((k) => delete zapisane[k]);
      pokaz(start);
      okno.classList.remove("panel-ukryty");
    },
  };
};
