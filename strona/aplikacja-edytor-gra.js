/* Symulator aplikacji Claude, drogi: krok `klik` z celem `edytor-rozwin` (ikona rozwinięcia w nagłówku edytora prezentacji w panelu Browser rozwija edytor na całe okno; wygląd okna: strona/aplikacja-edytor.js). Wymaga otwartej prezentacji (krok `artefakt` ze slajdami albo `aplikacja.artefakt_otwarty` ze slajdami). Część „Menu panelu Browser, edytor prezentacji i Transcript view” w dane/FORMAT-SCENARIUSZA.md. */

PK.CELE_EDYTORA = ["edytor-rozwin"];

/* Okno edytora w ćwiczeniu z drogami, które mają krok `klik` z celem `edytor-rozwin`; null w pozostałych. `artefakt` to wynik PK.artefaktCwiczenia (daje dane otwartej prezentacji). Ikona rozwinięcia reaguje tylko wtedy, gdy krok na nią czeka, a na wąskim ekranie (gdzie edytor w panelu chowa ją jako zbędną) krok ją pokazuje. Okno zostaje otwarte do końca drogi, do „Od nowa” i do nowego polecenia; jego elementy nie mają skutku. Zwraca {dotyczy, klik, reset}. */
PK.edytorAplikacji = function (cw, sek, okno, artefakt, widok) {
  const kroki = (cw.drogi || []).flatMap((d) => d.kroki || []);
  if (!kroki.some((k) => k.typ === "klik" && PK.CELE_EDYTORA.includes(k.cel))) return null;
  let czeka = null; /* {el, pusc}: ikona, na której kliknięcie czeka krok */
  let tlo = null; /* okno edytora nad oknem aplikacji */

  const zamknij = () => {
    if (tlo) tlo.remove();
    tlo = null;
    okno.classList.remove("edytor-otwarty");
  };
  const otworz = () => {
    okno.insertAdjacentHTML("beforeend", PK.edytorOkno(artefakt.dane()));
    tlo = okno.lastElementChild;
    okno.classList.add("edytor-otwarty");
  };

  /* Ikona leży w panelu, a nie w rozmowie, więc strażnik kliku z aplikacja.js jej nie widzi; inne kliknięcia niczego nie robią. */
  sek.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target)) czeka.pusc(true);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_EDYTORA.includes(k.cel),
    async klik(k, zyje) {
      const el = widok.querySelector(".apl-sl-rozwin");
      if (!el) return; /* walidator nie dopuszcza kroku bez otwartej prezentacji */
      el.classList.remove("apl-sl-zbedne"); /* wąski edytor chowa ikonę rozwinięcia; na czas kroku wraca */
      const ok = await PK.czekajNaKlikMenuB(sek, el, widok.querySelector(".apl-sl-glowa"), (c) => (czeka = c), zyje);
      if (ok) otworz();
    },
    /* „Od nowa” i nowe polecenie: okno zamknięte, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      zamknij();
      PK.celPod(sek, null);
    },
  };
};
