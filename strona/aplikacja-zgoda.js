/* Symulator aplikacji Claude, karta zgody w trybie Manual: podgląd zmiany pliku (linijki usunięte i dodane) z przyciskami zatwierdzenia i odrzucenia bez napisów, stan po zatwierdzeniu i znacznik „kliknij tutaj” (PK.celAplikacji w odpowiedzi, PK.celPod pod klikanym elementem). */

/* Opisy przycisków tylko dla czytnika ekranu (aria-label, bez dymku): tekst kursu po polsku, nie napisy aplikacji (dokumentacja ich nie podaje). */
PK.OPISY_ZGODY = {
  tak: "Zatwierdź zmianę",
  nie: "Odrzuć zmianę (w tym ćwiczeniu nie działa)",
  tak_polecenie: "Zezwól na polecenie",
  nie_polecenie: "Odrzuć polecenie (w tym ćwiczeniu nie działa)",
};

/* Ikony przycisków zgody: ptaszek i krzyżyk, rysowane kreską, bez napisu. */
PK.IKONY_ZGODY = (() => {
  const s = (d) =>
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    d +
    "</svg>";
  return {
    tak: s('<path d="m5.5 12.5 4.2 4.2L18.5 7.5"/>'),
    nie: s('<path d="m7 7 10 10M17 7 7 17"/>'),
  };
})();

/* Linijki zmiany: bez znaku, „-” na czerwono, „+” na zielono; te same w karcie zgody i w widoku zmian. */
PK.linijkiZgody = (linijki) => {
  const { esc } = PK;
  const znak = (l) =>
    l.zmiana === "dodana" ? "+" : l.zmiana === "usunieta" ? "-" : "";
  const wiersz = (l) =>
    `<li class="apl-l ${esc(l.zmiana || "bez")}"><span class="apl-znak" aria-hidden="true">${znak(l)}</span><span class="apl-l-tekst">${esc(l.tekst)}</span></li>`;
  return `<ol class="apl-linijki">${(linijki || []).map(wiersz).join("")}</ol>`;
};

/* Plik ze zmianą: nagłówek z nazwą i linijki; w widoku zmian po zatwierdzeniu. */
PK.plikZgody = (plik, linijki) =>
  `<section class="apl-plik"><header>${PK.IKONY_APLIKACJI.plik}<b>${PK.esc(plik)}</b></header>${PK.linijkiZgody(linijki)}</section>`;

/* Karta zgody w rozmowie pod odpowiedzią Claude: podgląd zmiany i dwa przyciski, odrzucenie po lewej, zatwierdzenie po prawej. */
PK.kartaZgody = (k) => {
  const { esc } = PK;
  const O = PK.OPISY_ZGODY;
  const I = PK.IKONY_ZGODY;
  return (
    `<div class="apl-zgoda"><section class="apl-plik"><header>${PK.IKONY_APLIKACJI.plik}<b>${esc(k.plik)}</b></header>${PK.linijkiZgody(k.linijki)}` +
    `<div class="apl-zgoda-przyciski">` +
    `<button type="button" class="apl-zgoda-nie" aria-disabled="true" aria-label="${esc(O.nie)}">${I.nie}</button>` +
    `<button type="button" class="apl-zgoda-tak" aria-label="${esc(O.tak)}">${I.tak}</button>` +
    `</div></section></div>`
  );
};

/* Po zatwierdzeniu karta zostaje w rozmowie bez przycisków. */
PK.zatwierdzZgode = (karta) => {
  karta.classList.add("zatwierdzona");
  const przyciski = karta.querySelector(".apl-zgoda-przyciski");
  if (przyciski) przyciski.remove();
};

/* Znacznik „kliknij tutaj” w osobnym rzędzie zaraz za elementem `po`, ze strzałką w górę na środek `el`; el = null zdejmuje znacznik.
   Cel w rzędzie pod polem (`po` to `.apl-rzad`, np. środowisko, folder, tryb, przycisk modelu, pierścień): rząd na wąskim ekranie zawija się w wiersze, a rząd ze znacznikiem za całym rzędem stałby pod ostatnim wierszem, więc dla celu z wyższego wiersza znacznik staje w rzędzie, zaraz za ostatnim elementem wiersza celu (na całą szerokość rzędu, reszta rzędu zawija się pod nim). Rząd w jednym wierszu i cel z ostatniego wiersza mają znacznik za rzędem jak dotąd. Miejsce liczy się od nowa po zmianie rozmiaru okna (`_uloz`). */
PK.celPod = (sek, el, po) => {
  PK.celAplikacji(sek, null);
  sek.querySelectorAll(".apl-tag-rzad").forEach((e) => e.remove());
  if (!el || !po) return;
  el.classList.add("apl-cel");
  const rzad = document.createElement(po.tagName === "LI" ? "li" : "div");
  rzad.className = "apl-tag-rzad";
  rzad.setAttribute("aria-hidden", "true");
  const tag = document.createElement("span");
  tag.className = "apl-tag apl-tag-pod";
  tag.textContent = "kliknij tutaj";
  rzad.appendChild(tag);
  const wRzedzie = po.classList.contains("apl-rzad") && po.contains(el);
  /* miejsce znacznika przy celu w rzędzie pod polem: pomiar bez znacznika, bo znacznik w rzędzie sam zawija resztę rzędu */
  const miejsce = () => {
    rzad.remove();
    const wiersze = [...po.children].filter((c) => !["absolute", "fixed"].includes(getComputedStyle(c).position) && getComputedStyle(c).display !== "none");
    const srodek = (e) => (e.getBoundingClientRect().top + e.getBoundingClientRect().bottom) / 2;
    const cel = wiersze.find((c) => c.contains(el));
    const wTymWierszu = cel ? wiersze.filter((c) => Math.abs(srodek(c) - srodek(cel)) < 10) : [];
    const ostatni = !cel || !wiersze.some((c) => srodek(c) > srodek(cel) + 10); /* nic nie stoi niżej: cel jest w ostatnim wierszu */
    (ostatni ? po : wTymWierszu[wTymWierszu.length - 1]).after(rzad);
  };
  if (!wRzedzie) po.after(rzad);
  /* etykieta stoi pod środkiem elementu, ale nie wychodzi poza rząd; strzałka zawsze wskazuje środek elementu */
  tag._uloz = () => {
    if (wRzedzie) miejsce();
    const r = el.getBoundingClientRect();
    const p = rzad.getBoundingClientRect();
    const pol = tag.offsetWidth / 2;
    const x = r.left - p.left + r.width / 2;
    const srodek = Math.max(pol, Math.min(p.width - pol, x));
    rzad.style.setProperty("--tag-x", srodek + "px");
    const strzalka = Math.max(10, Math.min(2 * pol - 10, x - srodek + pol));
    tag.style.setProperty("--strzalka", strzalka + "px");
  };
  tag._uloz();
};

/* Znacznik „kliknij tutaj” dla etapu `e` na elemencie `el`: licznik na karcie Changes ma znacznik jak w ćwiczeniu z krokami (strona/aplikacja.js), reszta stoi w rzędzie zaraz pod elementem: pod przyciskami karty, pod rzędem z przełącznikiem (`rzad`), pod pozycją menu. */
PK.celEtapu = (sek, e, el, rzad) => {
  if (e && e.klik === "licznik") {
    PK.celPod(sek, null);
    return PK.celAplikacji(sek, el);
  }
  const po =
    !el || !e
      ? null
      : e.klik === "zatwierdz"
        ? el.closest(".apl-plik")
        : e.klik === "przelacznik"
          ? rzad
          : el.parentElement;
  PK.celPod(sek, el, po);
};

/* Znacznik kursu „kliknij tutaj” na elemencie `el` (albo zdjęcie znacznika, gdy el = null). */
PK.celAplikacji = (sek, el) => {
  sek.querySelectorAll(".apl-cel").forEach((e) => e.classList.remove("apl-cel"));
  sek.querySelectorAll(".apl-tag").forEach((e) => e.remove());
  if (!el) return;
  const tag = document.createElement("span");
  tag.className = "apl-tag";
  tag.setAttribute("aria-hidden", "true");
  tag.textContent = "kliknij tutaj";
  el.classList.add("apl-cel");
  /* przy ścieżce (i linku) znacznik stoi pod odpowiedzią w osi ścieżki: nad ścieżką zasłoniłby tekst Claude, a pod samą ścieżką następną linijkę */
  const pod = el.classList.contains("apl-sciezka") || el.classList.contains("apl-art-wybor"); /* link ma obie klasy: apl-sciezka apl-link; przycisk przełącznika kursu (strona/aplikacja-artefakt.js) stoi w rzędzie z drugim przyciskiem, więc znacznik nad nim zasłoniłby sąsiada */
  tag.classList.toggle("apl-tag-pod", pod);
  if (!pod) return el.appendChild(tag);
  const kontener = el.closest(".apl-claude, .apl-art-kurs");
  kontener.appendChild(tag);
  /* środek ścieżki (przy zawinięciu: jej pierwszy kawałek) albo przycisku, ograniczony tak, by znacznik nie wyszedł poza odpowiedź (pole kursu); liczone od miejsca, w którym znacznik stoi bez przesunięcia (kontener może mieć wcięcie) */
  tag._uloz = () => {
    const r = el.getClientRects()[0];
    const p = kontener.getBoundingClientRect();
    const pol = tag.offsetWidth / 2;
    kontener.style.setProperty("--tag-x", "0px");
    const miejsce = tag.getBoundingClientRect(); /* przy left: 0 środek znacznika to jego miejsce w układzie */
    const start = miejsce.left + miejsce.width / 2;
    const x = r.left + r.width / 2 - start;
    kontener.style.setProperty("--tag-x", Math.max(p.left + pol - start, Math.min(p.right - pol - start, x)) + "px");
  };
  tag._uloz();
};
/* po zmianie rozmiaru okna znacznik przy ścieżce liczy pozycję od nowa */
window.addEventListener("resize", () => {
  document.querySelectorAll(".apl-tag-pod").forEach((t) => t._uloz && t._uloz());
});
