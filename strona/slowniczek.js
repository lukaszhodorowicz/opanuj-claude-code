/* Podpowiedzi pojęć ze słowniczka w tekście lekcji (elementy .pojecie wpisuje narzedzia/strona_slowniczek.py): mysz pokazuje po najechaniu, dotyk otwiera pierwszym dotknięciem i zamyka drugim, klik poza pojęciem i Esc zamykają, Tab otwiera, Enter i spacja przełączają. Jedna podpowiedź otwarta naraz; podpowiedź czyta czytnik ekranu przez aria-describedby. */
(() => {
  if (typeof document === "undefined") return;
  const MARGINES = 8;
  const ODSTEP = 6;
  let otwarte = null; /* .pojecie z otwartą podpowiedzią */
  let trzymane = false; /* otwarte dotykiem, klawiaturą albo spacją: najechanie myszą go nie zamyka */
  let wskaznik = ""; /* typ ostatniego wskaźnika (mouse, touch, pen); pusty po klawiaturze */

  const pojecie = (cel) => (cel && cel.closest ? cel.closest(".pojecie") : null);
  const slowo = (el) => el.querySelector(".pojecie-slowo");

  /* podpowiedź stoi na stałe względem okna, więc liczymy jej miejsce pod słowem (albo nad nim, gdy brak miejsca) i trzymamy w oknie */
  function ustaw(el) {
    const podp = el.querySelector(".pojecie-podp");
    const rzedy = slowo(el).getClientRects();
    if (!podp || !rzedy.length) return;
    const pierwszy = rzedy[0];
    const ostatni = rzedy[rzedy.length - 1];
    const szer = document.documentElement.clientWidth;
    const wys = document.documentElement.clientHeight;
    const w = podp.offsetWidth;
    const h = podp.offsetHeight;
    const lewo = Math.min(Math.max(MARGINES, ostatni.left), Math.max(MARGINES, szer - w - MARGINES));
    let gora = ostatni.bottom + ODSTEP;
    if (gora + h > wys - MARGINES && pierwszy.top - ODSTEP - h >= MARGINES) gora = pierwszy.top - ODSTEP - h;
    podp.style.left = Math.round(lewo) + "px";
    podp.style.top = Math.round(gora) + "px";
  }

  function zamknij(el) {
    if (!el) return;
    el.classList.remove("otwarta");
    const s = slowo(el);
    if (s) s.setAttribute("aria-expanded", "false");
    if (otwarte === el) {
      otwarte = null;
      trzymane = false;
    }
  }

  function otworz(el, na_stale) {
    if (otwarte && otwarte !== el) zamknij(otwarte);
    el.classList.add("otwarta");
    slowo(el).setAttribute("aria-expanded", "true");
    otwarte = el;
    trzymane = Boolean(na_stale);
    ustaw(el);
  }

  function przelacz(el) {
    if (el.classList.contains("otwarta")) zamknij(el);
    else otworz(el, true);
  }

  /* typ wskaźnika zapamiętujemy przy dotknięciu albo kliknięciu, a klawiatura go kasuje */
  document.addEventListener("pointerdown", (e) => { wskaznik = e.pointerType || ""; }, true);

  document.addEventListener("pointerover", (e) => {
    const el = pojecie(e.target);
    if (el && e.pointerType === "mouse" && !el.contains(e.relatedTarget)) otworz(el, false);
  });
  document.addEventListener("pointerout", (e) => {
    const el = pojecie(e.target);
    if (el && e.pointerType === "mouse" && !el.contains(e.relatedTarget) && !trzymane) zamknij(el);
  });

  /* Tab dochodzi do pojęcia i otwiera podpowiedź; dotknięcie i mysz otwierają inaczej (wyżej i niżej) */
  document.addEventListener("focusin", (e) => {
    const el = pojecie(e.target);
    if (el && wskaznik === "" && e.target.classList.contains("pojecie-slowo")) otworz(el, true);
  });
  document.addEventListener("focusout", (e) => {
    const el = pojecie(e.target);
    if (el && !el.contains(e.relatedTarget)) zamknij(el);
  });

  document.addEventListener("click", (e) => {
    const el = pojecie(e.target);
    if (!el) {
      if (otwarte) zamknij(otwarte);
      return;
    }
    if (e.target.closest(".pojecie-podp")) {
      zamknij(el); /* dotknięcie podpowiedzi zamyka ją */
      return;
    }
    if (wskaznik === "mouse") return; /* myszą otwiera i zamyka najechanie */
    przelacz(el);
  });

  document.addEventListener("keydown", (e) => {
    wskaznik = "";
    if (e.key === "Escape") {
      if (otwarte) zamknij(otwarte);
      return;
    }
    if ((e.key === "Enter" || e.key === " ") && e.target.classList && e.target.classList.contains("pojecie-slowo")) {
      e.preventDefault();
      przelacz(pojecie(e.target));
    }
  });

  const przelicz = () => { if (otwarte) ustaw(otwarte); };
  window.addEventListener("scroll", przelicz, { passive: true, capture: true });
  window.addEventListener("resize", przelicz);
})();
