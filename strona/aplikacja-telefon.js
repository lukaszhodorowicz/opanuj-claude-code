/* Symulator aplikacji Claude, telefon z Remote Control, gra: ramka telefonu obok okna (na wąskim ekranie pod nim) z listą sesji, kroki `klik` z celami telefon-sesja i telefon-wstecz, krok `pisz` z polem `na_telefonie` i lustro rozmowy: rozmowa na telefonie to ta sama rozmowa co w oknie na komputerze (sedno Remote Control). Wygląd: strona/aplikacja-telefon-widok.js, napisy: strona/aplikacja-telefon-dane.js (część „Telefon i Remote Control” w dane/FORMAT-SCENARIUSZA.md). */

PK.CELE_TELEFONU = ["telefon-sesja", "telefon-wstecz"];

/* Telefon w ćwiczeniu z drogami, które ma pole `aplikacja.telefon`; null, gdy go nie ma (reszta ćwiczeń zostaje bez zmian). `okno` to `.apl-okno`, `rozmowa` to `.apl-rozmowa` okna: wszystko, co w niej stanie (prośba, odpowiedź Claude, wskaźnik pracy), pokazuje też telefon po otwarciu sesji. Zwraca {dotyczy, klik, pisz, reset}. */
PK.telefonAplikacji = function (cw, sek, okno, rozmowa) {
  const apl = cw.aplikacja || {};
  if (!apl.telefon) return null;
  const { czekaj } = PK;
  okno.after(Object.assign(document.createElement("div"), { innerHTML: PK.htmlTelefonu(apl) }).firstElementChild);
  sek.classList.add("ma-telefon");
  const tel = sek.querySelector(".apl-telefon");
  const ekrany = { lista: tel.querySelector('[data-ekran="lista"]'), rozmowa: tel.querySelector('[data-ekran="rozmowa"]') };
  const moja = tel.querySelector(".apl-tel-moja");
  const wstecz = tel.querySelector(".apl-tel-wstecz");
  const naglowek = tel.querySelector(".apl-tel-gora-rozmowy");
  const wiadomosci = tel.querySelector(".apl-tel-wiadomosci");
  const pole = tel.querySelector(".apl-tel-pole");
  const wpis = tel.querySelector(".apl-tel-wpis");
  const praca = tel.querySelector(".apl-tel-praca");
  let czeka = null; /* {el, pusc}: element, na którego kliknięcie czeka krok klik */
  [moja, wstecz].forEach((e) => e.setAttribute("aria-disabled", "true")); /* aktywne tylko wtedy, gdy krok na nie czeka */

  const pokaz = (nazwa) => {
    for (const [n, e] of Object.entries(ekrany)) e.hidden = n !== nazwa;
    wiadomosci.scrollTop = wiadomosci.scrollHeight;
  };
  const wlacz = (el, tak) => (tak ? el.removeAttribute("aria-disabled") : el.setAttribute("aria-disabled", "true"));

  /* Lustro: wiadomości okna (dymek kursanta i odpowiedź Claude) stają na telefonie, a trzy kropki pracy Claude uruchamiają kółko pracy w nagłówku. Zmiana w oknie, także „Od nowa” (rozmowa wraca do stanu startowego), przebudowuje telefon od początku. */
  const tresc = (e) => (e.querySelector("p") ? e.querySelector("p").textContent.replace(/⁠/g, "") : "");
  const lustro = () => {
    wiadomosci.innerHTML = [...rozmowa.children]
      .map((e) => (e.classList.contains("apl-ty") ? PK.dymekTelefonu("ty", tresc(e)) : e.classList.contains("apl-claude") ? PK.dymekTelefonu("claude", tresc(e)) : ""))
      .join("");
    praca.classList.toggle("pracuje", !!rozmowa.querySelector(".apl-mysli"));
    wiadomosci.scrollTop = wiadomosci.scrollHeight;
  };
  new MutationObserver(lustro).observe(rozmowa, { childList: true });
  lustro();

  /* Kursant klika tylko to, na co czeka krok; reszta telefonu jest bez skutku (kursor zwykły). */
  tel.addEventListener("click", (e) => {
    if (czeka && czeka.el.contains(e.target)) czeka.pusc(true);
  });

  return {
    dotyczy: (k) => k.typ === "klik" && PK.CELE_TELEFONU.includes(k.cel),
    /* Znacznik „kliknij tutaj” pod wierszem sesji (na liście) albo pod nagłówkiem rozmowy (strzałka wstecz), czekanie na klik i skutek: sesja otwiera rozmowę, strzałka wraca na listę. `zyje()` mówi, że ćwiczenie nie zostało w międzyczasie przerwane. */
    async klik(k, zyje) {
      const lista = k.cel === "telefon-sesja";
      const el = lista ? moja : wstecz;
      wlacz(el, true);
      PK.celPod(sek, el, lista ? el.closest("li") : naglowek);
      const ok = await new Promise((pusc) => (czeka = { el, pusc }));
      czeka = null;
      if (!ok || !zyje()) return;
      PK.celPod(sek, null);
      el.classList.add("wcisniety");
      await czekaj(200);
      el.classList.remove("wcisniety");
      if (!zyje()) return;
      wlacz(el, false);
      pokaz(lista ? "rozmowa" : "lista");
    },
    /* Wiadomość kursanta wpisana na telefonie (krok `pisz` z `na_telefonie`): tekst sam pojawia się w polu telefonu i znika po wysłaniu. Dymek w oknie dopisuje strona/aplikacja.js, a lustro pokazuje go na telefonie. Zwraca true, gdy tekst poszedł. */
    async pisz(tekst, przerwano) {
      if (ekrany.rozmowa.hidden) pokaz("rozmowa"); /* walidator do tego nie dopuszcza: pole musi być widoczne */
      pole.classList.add("pisze");
      const ok = await PK.wpiszWPole(wpis, tekst, przerwano);
      pole.classList.remove("pisze");
      return ok;
    },
    /* „Od nowa” i nowe polecenie: lista sesji, puste pole, krok, który czeka na klik, przerwany. */
    reset() {
      if (czeka) czeka.pusc(false);
      czeka = null;
      pokaz("lista");
      wlacz(moja, false);
      wlacz(wstecz, false);
      pole.classList.remove("pisze");
      wpis.classList.remove("pisze");
      wpis.textContent = "";
      lustro();
    },
  };
};
