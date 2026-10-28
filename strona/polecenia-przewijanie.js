/* Zwarte polecenia nad oknem ćwiczenia: rozwija opis tylko przy poleceniu na teraz i po kliknięciu przewija stronę tak, by dymek nauczyciela, okno i znacznik „kliknij tutaj” były widać. */
(function () {
  const ruch = () => (matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth");

  /* Dymek u góry ekranu, gdy dymek i okno mieszczą się razem; inaczej dół okna przy dole ekranu, a okno wyższe od ekranu od swojej góry.
     Gdy znacznik celu nie mieści się w tym widoku (okno wyższe od ekranu), na środek ekranu idzie sam znacznik. */
  function pokaz(sek) {
    const dymek = sek.querySelector(".nauczyciel");
    const okno = sek.querySelector(".apl-okno, .okna");
    if (!dymek || !okno) return;
    const d = dymek.getBoundingClientRect();
    const o = okno.getBoundingClientRect();
    const gora = d.top + scrollY - 12;
    const dol = o.bottom + scrollY + 12;
    let y = dol - gora <= innerHeight ? gora : Math.min(dol - innerHeight, o.top + scrollY - 12);
    const cel = [...sek.querySelectorAll(".apl-cel")].find((e) => e.getBoundingClientRect().width > 0);
    if (cel) {
      const c = cel.getBoundingClientRect();
      const cGora = c.top + scrollY;
      const cDol = c.bottom + scrollY + 40; /* pod znacznikiem stoi jeszcze pigułka „kliknij tutaj” */
      if (cGora < y + 8 || cDol > y + innerHeight - 8) y = cGora - (innerHeight - (cDol - cGora)) / 2;
    }
    scrollTo({ top: Math.max(0, y), behavior: ruch() });
  }

  /* Po kliknięciu dymek, okno i rząd poleceń jeszcze się zmieniają (nowy tekst nauczyciela, nowy widok, nowy znacznik celu), więc przez 4 s od ostatniej
     zmiany każda zmiana powtarza przewinięcie. Ręczne przewijanie kursanta (kółko, przeciągnięcie palcem, klawisz) kończy śledzenie do następnego kliknięcia polecenia. */
  let reczne = false;
  ["wheel", "touchmove", "keydown"].forEach((z) => addEventListener(z, () => (reczne = true), { passive: true }));
  function odswiez(sek) {
    if (reczne || Date.now() > sek._do) return;
    const r = sek.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return; /* kursant odszedł do innego miejsca strony: nie ciągniemy go z powrotem */
    if (sek._powtorka) return; /* najwyżej jedno przewinięcie na 150 ms; samo opóźnianie nie działa, bo animacja w oknie zmienia je co kilkanaście ms */
    sek._powtorka = setTimeout(() => {
      sek._powtorka = 0;
      pokaz(sek);
    }, 150);
  }
  function sledz(sek) {
    sek._do = Date.now() + 4000;
    reczne = false;
    if (sek._obserwator) return;
    sek._obserwator = new ResizeObserver(() => odswiez(sek));
    sek.querySelectorAll(".nauczyciel, .apl-okno, .okna, .polecenia").forEach((el) => sek._obserwator.observe(el));
    const okno = sek.querySelector(".apl-okno, .okna");
    new MutationObserver(() => {
      if (Date.now() > sek._do) return;
      sek._do = Date.now() + 4000; /* gra trwa: nowe znaczniki celu pojawiają się w oknie jeden po drugim */
      odswiez(sek);
    }).observe(okno, { subtree: true, childList: true, attributes: true, attributeFilter: ["class"] });
  }

  /* `teraz`: jedyne wolne polecenie, a w pozostałych przypadkach ostatnio kliknięte. */
  function oznacz(sek) {
    const polecenia = [...sek.querySelectorAll(".polecenie")];
    const wolne = polecenia.filter((b) => !b.disabled);
    const cel = wolne.length === 1 ? wolne[0] : sek._ostatnie || null;
    polecenia.forEach((b) => b.classList.toggle("teraz", b === cel));
  }

  function start() {
    document.querySelectorAll(".cwiczenie").forEach(podlacz);
  }

  function podlacz(sek) {
    const rzad = sek.querySelector(".polecenia");
    if (!rzad) return;
    new MutationObserver(() => oznacz(sek)).observe(rzad, { subtree: true, attributes: true, attributeFilter: ["disabled"] });
    sek.querySelectorAll(".polecenie").forEach((b) =>
      b.addEventListener("click", () => {
        sek._ostatnie = b;
        oznacz(sek);
        sledz(sek);
        requestAnimationFrame(() => pokaz(sek));
      }),
    );
    const odNowa = sek.querySelector("[data-od-nowa]");
    if (odNowa) odNowa.addEventListener("click", () => { sek._ostatnie = null; oznacz(sek); });
    oznacz(sek);
  }

  /* Skrypt stoi przed silnik.js, który buduje ćwiczenia, więc czeka na koniec wczytywania strony. */
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
