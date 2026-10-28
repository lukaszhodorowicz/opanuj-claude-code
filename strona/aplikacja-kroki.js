/* Symulator aplikacji Claude, kroki: ćwiczenie z listą `kroki` (licznik zmian albo przycisk Changes otwiera widok zmian; linijki widoku niczego nie otwierają; polecenia klikają się po kolei), wskazanie „kliknij tutaj” i powrót „Od nowa”. */

/* Gra ćwiczenie z krokami w oknie `sek` (sekcja ćwiczenia z htmlAplikacji); wołana z PK.aplikacja (strona/aplikacja.js) po obsłużeniu etapów i dróg. */
PK.krokiAplikacji = function (cw, sek) {
  const { czekaj } = PK;
  const kroki = cw.kroki || [];
  const okno = sek.querySelector(".apl-okno");
  const widok = sek.querySelector(".apl-widok-zmian");
  const mow = PK.Nauczyciel(sek.querySelector(".nauczyciel"), []);
  let zrobione = 0;
  let zajety = false;

  const elementKroku = (k) => {
    if (!k) return null;
    if (k.klik === "licznik") return sek.querySelector(".apl-licznik");
    if (k.klik === "changes")
      return sek.querySelector('[data-pasek="changes"]');
    return null;
  };

  const ustawCel = () => PK.celAplikacji(sek, elementKroku(kroki[zrobione]));

  /* Polecenia klikają się po kolei: aktywne tylko następne, wysłane i dalsze mają `disabled`. */
  function ustawPolecenia() {
    sek.querySelectorAll(".polecenie").forEach((b) => {
      const k = +b.dataset.k;
      b.classList.toggle("wyslane", k < zrobione);
      b.disabled = k !== zrobione;
    });
  }

  function otworzZmiany() {
    widok.hidden = false;
    okno.classList.add("zmiany-otwarte");
    sek.querySelector('[data-pasek="changes"]').classList.add("wlaczony");
  }

  async function wykonaj(k, szybko) {
    const el = elementKroku(k);
    if (!szybko && el) {
      el.classList.add("wcisniety");
      await czekaj(220);
      el.classList.remove("wcisniety");
    }
    otworzZmiany();
  }

  /* Wykonuje kroki do numeru `cel` włącznie; wcześniejsze, jeszcze niezrobione, bez animacji. */
  async function idzDo(cel) {
    if (zajety || cel < zrobione) return;
    zajety = true;
    sek.querySelectorAll(".apl-tag").forEach((e) => e.remove());
    while (zrobione <= cel) {
      const k = kroki[zrobione];
      const szybko = zrobione < cel;
      await wykonaj(k, szybko);
      zrobione++;
      ustawPolecenia();
      if (!szybko) mow(k.nauczyciel);
    }
    ustawCel();
    zajety = false;
  }

  function odNowa() {
    if (zajety) return;
    zrobione = 0;
    widok.hidden = true;
    okno.classList.remove("zmiany-otwarte");
    sek
      .querySelectorAll(".wlaczony, .wyslane")
      .forEach((e) => e.classList.remove("wlaczony", "wyslane"));
    ustawPolecenia();
    mow(cw.nauczyciel_start, null, "polecenie");
    ustawCel();
  }

  sek
    .querySelectorAll(".polecenie")
    .forEach((b) => b.addEventListener("click", () => idzDo(+b.dataset.k)));
  okno.addEventListener("click", (e) => {
    const k = kroki[zrobione];
    const el = elementKroku(k);
    const zmiany = e.target.closest(".apl-licznik, [data-pasek=changes]");
    /* licznik i przycisk Changes robią to samo: oba zaliczają krok, który otwiera widok zmian */
    if ((el && el.contains(e.target)) || (zmiany && k)) idzDo(zrobione);
    else if (zmiany) otworzZmiany();
  });
  sek.querySelector("[data-od-nowa]").addEventListener("click", odNowa);
  ustawPolecenia();
  ustawCel();
};
