/* Symulator aplikacji Claude, katalog konektorów: okno Settings → Connectors, zakładka Discover (strona/aplikacja-ustawienia.js; pozycja „Browse connectors” podmenu Connectors je otwiera), kafelki z napisami ze zrzutów Łukasza (strona/aplikacja-ustawienia-dane.js), karta logowania po kliknięciu kafelka i krok `katalog_zamknij`, który okno zamyka; kroki `klik` z celem `konektor` (część „Menu + i katalog konektorów” w dane/FORMAT-SCENARIUSZA.md). */

PK.CEL_KATALOGU_MS = 1600; /* domyślny czas karty logowania w kroku katalog_zamknij */
/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_KATALOGU = {
  okno: "Ustawienia, katalog konektorów (w ćwiczeniu działa tylko kafelek ze znacznikiem)",
  zamknij: "Zamknij okno (w ćwiczeniu bez skutku)",
  logowanie: "Logowanie do konektora (w ćwiczeniu bez napisów)",
};

/* Okno katalogu w ćwiczeniu z drogami, które mają kroki pozycja „Browse connectors”, `klik` z celem `konektor` albo `katalog_zamknij`; null, gdy żadna droga ich nie ma (reszta ćwiczeń zostaje bez zmian). Aktywne są kafelki z nazwami wskazanymi w krokach `konektor` (pole `nazwa`), reszta jest bez skutku. Zwraca {otwiera, dotyczy, otworz, krok, reset}. */
PK.katalogAplikacji = function (cw, sek, okno) {
  const { esc, czekaj, szkic } = PK;
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  const otwiera = (k) => k.typ === "klik" && k.cel === "pozycja" && k.na === "Browse connectors";
  const dotyczy = (k) => k.typ === "katalog_zamknij" || (k.typ === "klik" && k.cel === "konektor");
  if (!kroki.some((k) => otwiera(k) || dotyczy(k))) return null;
  const aktywne = new Set(kroki.filter((k) => k.typ === "klik" && k.cel === "konektor").map((k) => k.nazwa));
  const I = PK.IKONY_KATALOGU;
  const O = PK.OPISY_KATALOGU;

  /* kafelek: ikona, nazwa ze znaczkiem weryfikacji, opis i autor (szare paski, gdy zrzut ich nie pokazuje), przycisk + bez skutku */
  const kafelek = (t) => {
    const opis = t.opis ? `<span class="apl-kaf-opis">${esc(t.opis)}</span>` : szkic(88) + szkic(58);
    const autor = t.autor ? `<span class="apl-kaf-autor">${esc(t.autor)}</span>` : szkic(30);
    const atr = aktywne.has(t.nazwa) ? "" : ' aria-disabled="true"';
    return (
      `<li><button type="button" class="apl-kafelek" data-nazwa="${esc(t.nazwa)}"${atr}><span class="apl-kaf-ikona">${I[t.nazwa] || I.klocki}</span>` +
      `<span class="apl-kaf-tekst"><b>${esc(t.nazwa)}<span class="apl-kaf-znaczek">${I.zweryfikowany}</span></b>${opis}${autor}</span>` +
      `<span class="apl-kaf-plus" aria-hidden="true">${I.plus}</span></button></li>`
    );
  };
  const tresc = () => {
    const S = PK.KONEKTORY_SEKCJA;
    return (
      `<div class="apl-kat-sekcja"><h4>${esc(S.nazwa)}</h4><span class="apl-kat-liczba">${esc(S.liczba)}</span><span class="apl-kat-wszystkie">${esc(PK.USTAWIENIA.wszystkie)}${I.dalej}</span></div>` +
      `<ul class="apl-kat-siatka">${PK.KONEKTORY_KATALOG.map(kafelek).join("")}</ul>`
    );
  };

  const { tlo, zawartosc, pokaz } = PK.powlokaKatalogu(okno, { opis: O.okno, zamknij: O.zamknij, strona: "Connectors", tresc: tresc() });
  let czeka = null; /* {el, pusc}: kafelek, na którego kliknięcie czeka krok klik */

  /* Kursant klika tylko to, na co czeka krok (kafelki leżą poza rozmową, więc strażnik kliku z aplikacja.js ich nie widzi); inne kliknięcia niczego nie robią. */
  tlo.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target)) czeka.pusc(true);
  });

  /* Znacznik „kliknij tutaj” pod kafelkiem; strona katalogu (.apl-kat-strona, jedyny przewijany element okna) przewija się tak, żeby kafelek razem ze znacznikiem leżał w całości w jej widocznym fragmencie (z zapasem 12 px na obramowanie zakreślacza). */
  const ZAPAS = 12;
  const wskaz = (el) => {
    PK.celPod(sek, el, el);
    const tag = sek.querySelector(".apl-tag-rzad .apl-tag");
    const uloz = () => tag && tag._uloz && tag._uloz();
    uloz();
    const s = zawartosc.getBoundingClientRect();
    const g = el.getBoundingClientRect();
    const dol = tag ? tag.getBoundingClientRect().bottom : g.bottom;
    if (g.top < s.top + ZAPAS) zawartosc.scrollTop -= s.top + ZAPAS - g.top;
    else if (dol > s.bottom - ZAPAS) zawartosc.scrollTop += dol - s.bottom + ZAPAS;
    uloz();
  };

  const karta = (kafelekEl) =>
    `<div class="apl-kat-karta" role="img" aria-label="${esc(O.logowanie)}"><div class="apl-kat-para"><span class="apl-kaf-ikona">${kafelekEl.querySelector(".apl-kaf-ikona").innerHTML}</span><span class="apl-kat-kloda">${I.kloda}</span></div>${szkic(46, "apl-kat-puls")}${szkic(64, "apl-kat-puls")}${szkic(38, "apl-kat-puls")}</div>`;

  return {
    otwiera,
    dotyczy,
    /* Pozycja „Browse connectors” już zamknęła menu: pokazuje okno z kafelkami. */
    otworz() {
      zawartosc.innerHTML = tresc();
      pokaz(true);
    },
    /* Krok `konektor`: znacznik pod kafelkiem, czekanie na klik, potem karta logowania zamiast kafelków. Krok `katalog_zamknij`: karta zostaje `ms` (domyślnie 1600), potem okno znika i widać rozmowę sprzed menu. `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane. */
    async krok(k, zyje) {
      if (k.typ === "katalog_zamknij") {
        await czekaj(k.ms || PK.CEL_KATALOGU_MS);
        if (zyje()) pokaz(false);
        return;
      }
      const el = zawartosc.querySelector(`.apl-kafelek[data-nazwa="${k.nazwa}"]`);
      wskaz(el);
      const ok = await new Promise((pusc) => (czeka = { el, pusc }));
      czeka = null;
      if (!ok || !zyje()) return;
      PK.celPod(sek, null);
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (zyje()) zawartosc.innerHTML = karta(el);
    },
    /* „Od nowa” i nowe polecenie: okno zamknięte, kafelki z powrotem, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      pokaz(false);
      zawartosc.innerHTML = tresc();
    },
  };
};
