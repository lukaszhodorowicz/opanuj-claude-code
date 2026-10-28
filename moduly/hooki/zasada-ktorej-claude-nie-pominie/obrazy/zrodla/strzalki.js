/* Rysuje granatowe strzałki z łamanych linii na nakładce SVG rysunku, liczone z położenia elementów po wczytaniu fontów. */
(function () {
  const NS = "http://www.w3.org/2000/svg";

  // Punkt na krawędzi elementu: strona "g" (góra), "d" (dół), "l" (lewo), "p" (prawo); u = przesunięcie 0..1 wzdłuż krawędzi.
  function punkt(kontener, el, strona, u) {
    const k = kontener.getBoundingClientRect();
    const r = document.querySelector(el).getBoundingClientRect();
    const t = u === undefined ? 0.5 : u;
    const x0 = r.left - k.left, y0 = r.top - k.top;
    if (strona === "g") return [x0 + r.width * t, y0];
    if (strona === "d") return [x0 + r.width * t, y0 + r.height];
    if (strona === "l") return [x0, y0 + r.height * t];
    return [x0 + r.width, y0 + r.height * t];
  }

  function linia(svg, punkty, grot) {
    const d = punkty.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
    const sciezka = document.createElementNS(NS, "path");
    sciezka.setAttribute("d", d);
    svg.appendChild(sciezka);
    if (!grot) return;
    const [a, b] = punkty.slice(-2);
    const kat = Math.atan2(b[1] - a[1], b[0] - a[0]);
    const dl = 11, roz = 0.78;
    const g = document.createElementNS(NS, "path");
    const l = [b[0] - dl * Math.cos(kat - roz), b[1] - dl * Math.sin(kat - roz)];
    const p = [b[0] - dl * Math.cos(kat + roz), b[1] - dl * Math.sin(kat + roz)];
    g.setAttribute("d", `M${l[0]} ${l[1]} L${b[0]} ${b[1]} L${p[0]} ${p[1]}`);
    svg.appendChild(g);
  }

  // plan: funkcja (p) => lista odcinków [{punkty: [[x,y],...], grot: true}]
  window.rysujStrzalki = function (kontenerSel, plan) {
    const kontener = document.querySelector(kontenerSel);
    const start = () => {
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "nakladka");
      svg.setAttribute("aria-hidden", "true");
      kontener.appendChild(svg);
      const p = (el, strona, u) => punkt(kontener, el, strona, u);
      plan(p).forEach((o) => linia(svg, o.punkty, o.grot !== false));
    };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(start);
  };
})();
