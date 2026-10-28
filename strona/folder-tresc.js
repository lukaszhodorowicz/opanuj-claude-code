/* Zmiana treści pliku w podglądzie folderu: akcje `edytuj` i `przywroc` oraz znacznik na karcie („zmieniona treść” z liczbami linijek albo „przywrócony”). */
(() => {
  const zwykly = PK.Folder;

  /* Ten sam folder co PK.Folder, z pamięcią zmian treści: plik → {dodane, usuniete} i zbiór przywróconych. */
  PK.Folder = function (el, pliki, opcje = {}) {
    const f = zwykly(el, pliki, opcje);
    const { esc } = PK;
    const wFolderze = (p) =>
      [f.luzem, ...Object.values(f.foldery)].some((w) => w.includes(p));
    const jest = (p) => wFolderze(p) && !f.usuniete.has(p);
    f.edycje = {};
    f.przywrocone = new Set();

    f.klasyTresci = (p) =>
      f.edycje[p] ? " edytowany" : f.przywrocone.has(p) ? " przywrocony" : "";
    f.znacznik = (p) => {
      const e = f.edycje[p];
      if (!e) {
        return f.przywrocone.has(p)
          ? '<span class="karta-przywrocony">przywrócony</span>'
          : "";
      }
      return (
        '<span class="karta-edytowany">zmieniona treść</span>' +
        '<span class="karta-liczby" title="' +
        esc("linijki dodane: " + e.dodane + ", usunięte: " + e.usuniete) +
        '"><b class="plus">+' +
        e.dodane +
        '</b><b class="minus">−' +
        e.usuniete +
        "</b></span>"
      );
    };

    /* Liczby mówią o stanie względem początku ćwiczenia: kolejna edycja je zastępuje, nie dodaje. */
    f.edytuj = (p, dodane, usuniete) => {
      if (!jest(p)) return;
      f.edycje[p] = {
        dodane: Number(dodane) || 0,
        usuniete: Number(usuniete) || 0,
      };
      f.przywrocone.delete(p);
      f.swiezeKarty.add(p);
      f.zmian++;
      f.rysuj();
    };
    /* Cofnięcie całej zmiany: liczby znikają, zostaje „przywrócony”. Bez wcześniejszej edycji nic się nie dzieje. */
    f.przywroc = (p) => {
      if (!jest(p) || !f.edycje[p]) return;
      delete f.edycje[p];
      f.przywrocone.add(p);
      f.swiezeKarty.add(p);
      f.zmian++;
      f.rysuj();
    };

    const reset = f.reset;
    f.reset = () => {
      f.edycje = {};
      f.przywrocone = new Set();
      reset();
    };
    /* Po zmianie nazwy znacznik idzie z kartą pod nową nazwę. */
    const zmien = f.zmien;
    f.zmien = (p, n) => {
      if (wFolderze(p)) {
        if (f.edycje[p]) f.edycje[n] = f.edycje[p];
        delete f.edycje[p];
        if (f.przywrocone.delete(p)) f.przywrocone.add(n);
      }
      zmien(p, n);
    };
    const zastosuj = f.zastosuj;
    f.zastosuj = (k) =>
      k.akcja === "edytuj"
        ? f.edytuj(k.nazwa, k.dodane, k.usuniete)
        : zastosuj(k);
    return f;
  };
})();
