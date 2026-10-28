/* Nauczyciel przy terminalu: postać z dymkiem, która mówi kilka słów i zaznacza okno, o którym mówi. */
PK.IKONA_NAUCZYCIELA =
  '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
  '<path fill-rule="evenodd" clip-rule="evenodd" d="M20.998 10.949H24v3.102h-3v3.028h-1.487V20H18v-2.921h-1.487V20H15v-2.921H9V20H7.488v-2.921H6V20H4.487v-2.921H3V14.05H0V10.95h3V5h17.998v5.949zM6 10.949h1.488V8.102H6v2.847zm10.51 0H18V8.102h-1.49v2.847z"/></svg>';

PK.nauczycielHtml = (tekst) =>
  '<div class="nauczyciel" aria-label="Nauczyciel"><div class="postac">' +
  PK.IKONA_NAUCZYCIELA +
  '</div><div class="dymek" role="status" aria-live="polite"><span class="o-oknie" hidden></span><p>' +
  PK.esc(tekst || "") +
  "</p></div></div>";

/* Sygnał zmiany tekstu: klasa `sygnal-polecenie` (mocny: nowe polecenie, nowa droga, „Od nowa”) albo `sygnal-krok` (słabszy: kolejny krok tej samej drogi); wygląd w strona/styl-dymek.css. Krok, który przyjdzie tuż po poleceniu (droga zaczyna od kroku nauczyciela), zmienia tylko tekst i nie przerywa mocnego sygnału. */
PK.OKNO_POLECENIA_MS = 400;

/* el: element .nauczyciel; okna: [{id, podpis, kol}] w kolejności na ekranie. Zwraca mow(tekst, idOkna, rodzaj), gdzie rodzaj „polecenie” daje mocny sygnał, każdy inny (domyślnie krok) słabszy. */
PK.Nauczyciel = function (el, okna) {
  const p = el.querySelector(".dymek p");
  const tag = el.querySelector(".o-oknie");
  let polecenieOd = -Infinity;
  return function mow(tekst, zrodlo, rodzaj) {
    const o = okna.length > 1 ? okna.find((x) => x.id === zrodlo) : null;
    p.textContent = tekst || "";
    tag.hidden = !o;
    tag.textContent = o ? o.podpis : "";
    okna.forEach((x) => x.kol && x.kol.classList.toggle("wskazane", x === o));
    const polecenie = rodzaj === "polecenie";
    const teraz = performance.now();
    if (!polecenie && teraz - polecenieOd < PK.OKNO_POLECENIA_MS) return;
    if (polecenie) polecenieOd = teraz;
    el.classList.remove("sygnal-polecenie", "sygnal-krok");
    void el.offsetWidth;
    el.classList.add(polecenie ? "sygnal-polecenie" : "sygnal-krok");
  };
};

/* Wypowiedź nauczyciela w kroku drogi albo etapu: po niej, gdy `nast` (następny krok) to znowu nauczyciel, silnik czeka tyle, ile kursant czyta tę wypowiedź (1,5 s + 45 ms na znak, od 2,5 do 9 s); przed innym krokiem i w szybkim odtwarzaniu nie czeka wcale, więc pojedyncza wypowiedź niczego nie opóźnia. */
PK.krokNauczyciela = (mow, k, nast, szybko) => {
  mow(k.tekst);
  if (szybko || !nast || nast.typ !== "nauczyciel") return;
  const ms = 1500 + 45 * (k.tekst || "").length;
  return PK.czekaj(Math.min(9000, Math.max(2500, ms)));
};
