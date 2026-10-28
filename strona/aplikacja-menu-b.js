/* Symulator aplikacji Claude, wspólne klocki menu ze zrzutów paczki 4 części B (menu „…” panelu Browser, menu sesji z paska tytułu, okno edytora prezentacji): pozycja menu, kreska, ptaszek i strzałka podmenu oraz czekanie na klik w element kroku `klik` ze znacznikiem „kliknij tutaj”. */

/* Ptaszek (niebieski) i strzałka podmenu: te same ikony co w reszcie symulatora. */
PK.ptaszekMenuB = () => `<span class="apl-mb-ptak" aria-hidden="true">${PK.IKONY_ZGODY.tak}</span>`;
PK.strzalkaMenuB = () => `<span class="apl-mb-strzalka" aria-hidden="true">${PK.IKONY_APLIKACJI.dalej}</span>`;
PK.liniaMenuB = '<li role="separator" class="apl-mb-linia"></li>';

/* Pozycja menu: napis po lewej, po prawej `prawa` (wartość, skrót, ptaszek albo strzałka podmenu). Pozycja nie ma skutku (aria-disabled), poza tą, na którą czeka krok (`klik()` ją odblokowuje). Opcje: `szara` (naprawdę szara w aplikacji: stoi szara także na zrzucie bez znacznika), `czerwona`, `dane` (atrybuty data-*), `wartosc` (szary napis po prawej), `naglowek` (szary napis bez ramki pozycji, nie jest klikalny). */
PK.pozycjaMenuB = (napis, o = {}) => {
  const { esc } = PK;
  if (o.naglowek) return `<li role="presentation" class="apl-mb-naglowek">${esc(napis)}</li>`;
  const klasy = ["apl-mb-poz", o.szara && "apl-poz-wylaczona", o.czerwona && "apl-mb-czerwona"].filter(Boolean).join(" ");
  const dane = Object.entries(o.dane || {}).map(([k, v]) => ` data-${k}="${esc(v)}"`).join("");
  const prawa = (o.wartosc ? `<span class="apl-mb-wartosc">${esc(o.wartosc)}</span>` : "") + (o.prawa || "");
  return `<li role="none"><button type="button" class="${klasy}" role="menuitem" aria-disabled="true"${dane}><span class="apl-mb-napis">${esc(napis)}</span>${prawa ? `<span class="apl-mb-prawa">${prawa}</span>` : ""}</button></li>`;
};

/* Skrót klawiszowy po prawej (szary). */
PK.skrotMenuB = (znak) => `<span class="apl-mb-skrot">${PK.esc(znak)}</span>`;

/* Czekanie na klik w `el`: znacznik „kliknij tutaj” w rzędzie za elementem `po` (PK.celPod), czekanie, wciśnięcie. `ustaw({el, pusc})` zapamiętuje czekający krok dla modułu (null po kliku), `zyje()` mówi, że ćwiczenie nie zostało przerwane („Od nowa”, nowe polecenie). Zwraca true, gdy kursant kliknął, false, gdy krok przerwano. */
PK.czekajNaKlikMenuB = async (sek, el, po, ustaw, zyje) => {
  PK.celPod(sek, el, po);
  const ok = await new Promise((pusc) => ustaw({ el, pusc }));
  ustaw(null);
  if (!ok || !zyje()) return false;
  PK.celPod(sek, null);
  el.classList.add("wcisniety");
  await PK.czekaj(200);
  el.classList.remove("wcisniety");
  return zyje();
};

/* Włącza (tak) albo wyłącza pozycję: wyłączona nie reaguje i nie ma kursora ręki. */
PK.wlaczMenuB = (el, tak) => {
  if (tak) el.removeAttribute("aria-disabled");
  else el.setAttribute("aria-disabled", "true");
};
