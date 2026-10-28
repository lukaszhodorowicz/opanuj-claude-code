/* Symulator aplikacji Claude, edytor prezentacji rozwinięty na całe okno, jasny motyw (zrzut Łukasza 27.10.2026, zrzut_2026-10-27_15-31-46.png; część „Menu panelu Browser, edytor prezentacji i Transcript view” w dane/FORMAT-SCENARIUSZA.md): napisy, ikony i HTML okna z paskiem górnym (dom, tytuł, Translate, dymek, Chat, Share, zwiń), paskami narzędzi, slajdem i miniaturami. Okno otwiera krok `klik` z celem `edytor-rozwin` (strona/aplikacja-edytor-gra.js). Bez menu eksportu (zrzut go nie pokazuje) i bez paska adresu (zrzut go nie pokazuje; widok artefaktu w symulatorze też go nie ma). */

/* Napisy edytora; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: claude.ai). */
PK.NAPISY_EDYTORA = {
  tlumacz: "Translate",
  czat: "Chat",
  udostepnij: "Share",
  skala: "59%",
};
/* Polskie opisy tylko dla czytnika ekranu (aria-label): nie są napisami interfejsu. */
PK.OPISY_EDYTORA = {
  okno: "Edytor prezentacji rozwinięty na całe okno (w ćwiczeniu bez skutku, tylko do oglądania)",
  slajd: "Slajd",
  miniatura: "Miniatury slajdów",
};

PK.IKONY_EDYTORA = (() => {
  const s = (d, w = 1.7) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    dom: s('<path d="M4.5 11 12 4.5l7.5 6.5v8a1 1 0 0 1-1 1H15v-5.5H9V20H5.5a1 1 0 0 1-1-1z"/>'),
    zwin: s('<path d="M20 10h-6V4M14 10l6.5-6.5M4 14h6v6M10 14l-6.5 6.5"/>'), /* zwiń: groty w stronę środka, jak na zrzucie 15-31-46 */
    plus: s('<path d="M12 5v14M5 12h14"/>'),
    pojedynczy: s('<rect x="6" y="6" width="12" height="12" rx="2.5"/>'),
    siatka: s('<rect x="4.5" y="4.5" width="6" height="6" rx="1.5"/><rect x="13.5" y="4.5" width="6" height="6" rx="1.5"/><rect x="4.5" y="13.5" width="6" height="6" rx="1.5"/><rect x="13.5" y="13.5" width="6" height="6" rx="1.5"/>'),
    gwiazdka: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.8l1.5 5.6 4.9-3-3 4.9 5.6 1.5-5.6 1.5 3 4.9-4.9-3L12 21.2l-1.5-5.6-4.9 3 3-4.9-5.6-1.5 5.6-1.5-3-4.9 4.9 3z"/></svg>',
  };
})();

/* Jeden slajd 16:9 (pismo liczone od szerokości, więc miniatura jest tym samym slajdem w mniejszej skali): pierwszy slajd tytułowy (punkty jako podtytuł), dalsze z listą punktów. */
PK.slajdEdytora = (s, i) => {
  const { esc } = PK;
  const tresc = i === 0 ? (s.punkty || []).map((p) => `<p class="apl-ed-pod">${esc(p)}</p>`).join("") : `<ul class="apl-ed-punkty">${(s.punkty || []).map((p) => `<li>${esc(p)}</li>`).join("")}</ul>`;
  return `<div class="apl-ed-strona${i === 0 ? " apl-ed-tytulowy" : ""}">${s.nadtytul ? `<p class="apl-ed-nad">${esc(s.nadtytul)}</p>` : ""}<p class="apl-ed-h">${esc(s.tytul)}</p>${tresc}</div>`;
};

/* Okno edytora z danych artefaktu `{tytul, slajdy}` (to samo, co otwarty widok prezentacji w panelu Browser): jasny pasek górny (dom, tytuł ze strzałką, puste kółko autora, Translate, dymek ze strzałką, Chat z gwiazdką, Share z ikoną, zwiń), pływające paski narzędzi (T, obraz, tabela, kształty ze strzałką; pobierz, odtwórz, ramka, 59% ze strzałką), pierwszy slajd na scenie i pas dolny z + i książką, miniaturami slajdów (pierwsza wybrana, z numerem) i przełącznikiem widoku. Wszystko jest bez skutku. */
PK.edytorOkno = (dane) => {
  const { esc } = PK;
  const N = PK.NAPISY_EDYTORA;
  const O = PK.OPISY_EDYTORA;
  const I = PK.IKONY_EDYTORA;
  const S = PK.IKONY_SLAJDOW;
  const slajdy = dane.slajdy || [];
  const ik = (svg, klasa = "") => `<span class="apl-ed-ik${klasa ? " " + klasa : ""}">${svg}</span>`;
  const kreska = '<i class="apl-ed-kreska"></i>';
  const miniatura = (s, i) => `<div class="apl-ed-miniatura${i === 0 ? " wybrana" : ""}"><div class="apl-ed-slajd">${PK.slajdEdytora(s, i)}</div><span class="apl-ed-nr">${i + 1}</span></div>`;
  return (
    `<div class="apl-ed" role="dialog" aria-label="${esc(O.okno)}">` +
    `<header class="apl-ed-gora">${ik(I.dom)}<b class="apl-ed-tytul"><span>${esc(dane.tytul)}</span>${S.rozwin}</b>` +
    `<span class="apl-ed-prawa"><span class="apl-ed-autor apl-ed-zbedne" aria-hidden="true"></span><span class="apl-ed-przycisk apl-ed-zbedne">${esc(N.tlumacz)}</span>` +
    `<span class="apl-ed-przycisk apl-ed-para apl-ed-zbedne">${S.dymek}${S.rozwin}</span>` +
    `<span class="apl-ed-przycisk apl-ed-czat"><span class="apl-ed-gwiazdka">${I.gwiazdka}</span>${esc(N.czat)}</span>` +
    `<span class="apl-ed-przycisk">${S.klodka}${esc(N.udostepnij)}</span>${ik(I.zwin)}</span></header>` +
    '<div class="apl-ed-scena">' +
    `<div class="apl-ed-narzedzia apl-ed-lewe">${ik(S.tekst)}${ik(S.obraz)}${ik(S.tabela)}<span class="apl-ed-ik apl-ed-para apl-ed-zbedne">${S.ksztalty}${S.rozwin}</span></div>` +
    `<div class="apl-ed-narzedzia apl-ed-prawe">${ik(S.pobierz)}${ik(S.odtworz)}${ik(S.widok, "apl-ed-zbedne")}${kreska}<span class="apl-ed-ik apl-ed-skala">${esc(N.skala)}${S.rozwin}</span></div>` +
    `<div class="apl-ed-slajd apl-ed-glowny" role="img" aria-label="${esc(O.slajd)} 1">${slajdy.length ? PK.slajdEdytora(slajdy[0], 0) : ""}</div></div>` +
    `<div class="apl-ed-dol"><div class="apl-ed-dol-gora">${ik(I.plus)}${ik(S.ksiazka)}<span class="apl-ed-widok">${ik(I.pojedynczy, "wybrana")}${ik(I.siatka)}</span>${ik(S.rozwin, "apl-ed-mala")}</div>` +
    `<div class="apl-ed-miniatury" aria-label="${esc(O.miniatura)}">${slajdy.map(miniatura).join("")}</div></div></div>`
  );
};
