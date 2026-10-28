/* Symulator aplikacji Claude, prezentacja w panelu Browser: edytor slajdów jak na zrzutach Łukasza z 26.10.2026 (nagłówek, nieklikane paski narzędzi, jeden slajd 16:9, pigułka „‹ 1 / 4 ›” z klikanymi strzałkami) i krótka animacja tworzenia z kursorem „Claude”. */

/* Napisy edytora slajdów. Źródło: zrzut Łukasza 26.10.2026 (edytor Claude Slides); test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: claude.ai). */
PK.NAPISY_SLAJDOW = {
  share: "Share",
  dodaj: "Add slide",
  powiekszenie: "31%",
  kursor: "Claude",
};

/* Ikony obrysowe 24×24 (kreska w kolorze tekstu), rysowane tu, bez zewnętrznych bibliotek. */
PK.IKONY_SLAJDOW = (() => {
  const s = (d, w = 1.7) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {
    rozwin: s('<path d="m7 10 5 5 5-5"/>', 1.8),
    klodka: s('<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/><circle cx="12" cy="15.5" r=".9" fill="currentColor"/>'),
    dymek: s('<path d="M12 4a8 8 0 1 1-4.3 14.75L4 20l1.25-3.75A8 8 0 0 1 12 4z"/>'),
    powieksz: s('<path d="M14 4h6v6M20 4l-6.5 6.5M10 20H4v-6M4 20l6.5-6.5"/>'),
    zamknij: s('<path d="M6 6l12 12M18 6 6 18"/>'),
    tekst: s('<path d="M6 5.5h12M12 5.5v13"/>'),
    obraz: s('<rect x="4" y="4" width="16" height="16" rx="3.5"/><circle cx="14.5" cy="9.5" r="2"/><path d="M4.5 16.5 9 12l5.5 6"/>'),
    tabela: s('<rect x="4" y="4.5" width="16" height="15" rx="2.5"/><path d="M4 9.5h16M4 14.5h16M9.5 9.5v10"/>'),
    ksztalty: s('<circle cx="9.5" cy="9.5" r="5.5"/><rect x="10.5" y="10.5" width="9.5" height="9.5" rx="2"/>'),
    pobierz: s('<path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M5 19.5h14"/>'),
    odtworz: s('<path d="M8 5.5v13l10-6.5z"/>'),
    widok: s('<rect x="6.5" y="3.5" width="11" height="17" rx="2.5"/><path d="M10 16h4"/>'),
    wstecz: s('<path d="M14.5 6 8.5 12l6 6"/>', 1.9),
    dalej: s('<path d="m9.5 6 6 6-6 6"/>', 1.9),
    ksiazka: s('<path d="M12 7c-2-1.6-4.6-2.1-8-1.6v12.8c3.4-.5 6 0 8 1.6 2-1.6 4.6-2.1 8-1.6V5.4c-3.4-.5-6 0-8 1.6zM12 7v12.8"/>'),
    pokaz: s('<rect x="4" y="4.5" width="16" height="10.5" rx="1"/><path d="M3 4.5h18M12 15v2.5M8.5 20l3.5-2.5 3.5 2.5"/>'),
    kursor:
      '<svg viewBox="0 0 22 22" aria-hidden="true"><path d="M3 2.5 19.5 9l-7.2 2.3-2.7 7.5z" fill="#8c601e" stroke="#efe8df" stroke-width="1.6" stroke-linejoin="round"/></svg>',
  };
})();

/* Edytor prezentacji z danych artefaktu {tytul, slajdy: [{nadtytul?, tytul, punkty}]}; pierwszy slajd tytułowy (punkty jako podtytuł), dalsze z listą punktów. */
PK.slajdyAplikacji = (dane) => {
  const { esc } = PK;
  const N = PK.NAPISY_SLAJDOW;
  const I = PK.IKONY_SLAJDOW;
  const slajdy = dane.slajdy || [];
  const el = (klasa, t) => `<p class="apl-sl-el ${klasa}">${esc(t)}</p>`;
  const slajd = (s, i) => {
    const tresc =
      i === 0
        ? (s.punkty || []).map((p) => el("apl-sl-pod", p)).join("")
        : `<ul class="apl-sl-el apl-sl-punkty">${(s.punkty || []).map((p) => `<li>${esc(p)}</li>`).join("")}</ul>`;
    return (
      `<div class="apl-sl-strona${i === 0 ? " apl-sl-tytulowy" : ""}" data-i="${i}"${i ? " hidden" : ""}>` +
      (s.nadtytul ? el("apl-sl-nad", s.nadtytul) : "") +
      el("apl-sl-h", s.tytul) +
      tresc +
      "</div>"
    );
  };
  const ik = (nazwa, klasa = "") => `<span class="apl-sl-ik${klasa ? " " + klasa : ""}">${I[nazwa]}</span>`;
  const kreska = '<i class="apl-sl-kreska"></i>';
  return (
    `<section class="apl-przegladarka apl-slajdy" data-nr="0">` +
    `<header class="apl-sl-glowa"><b class="apl-sl-tytul"><span>${esc(dane.tytul)}</span>${I.rozwin}</b>` +
    `<span class="apl-sl-prawa"><span class="apl-sl-share">${I.klodka}${esc(N.share)}</span>` +
    `<span class="apl-sl-ik apl-sl-para">${I.dymek}${I.rozwin}</span>${ik("powieksz", "apl-sl-zbedne apl-sl-rozwin")}${ik("zamknij")}</span></header>` +
    '<div class="apl-sl-narzedzia" aria-hidden="true">' +
    `<span class="apl-sl-grupa">${ik("tekst")}${ik("obraz")}${ik("tabela")}<span class="apl-sl-ik apl-sl-para">${I.ksztalty}${I.rozwin}</span></span>` +
    `<span class="apl-sl-grupa">${ik("pobierz")}${ik("odtworz")}${kreska}${ik("widok", "apl-sl-zbedne")}<i class="apl-sl-kreska apl-sl-zbedne"></i>` +
    `<span class="apl-sl-ik apl-sl-skala">${esc(N.powiekszenie)}${I.rozwin}</span></span>` +
    "</div>" +
    '<div class="apl-sl-scena"><div class="apl-sl-slajd">' +
    slajdy.map(slajd).join("") +
    `<span class="apl-sl-kursor" aria-hidden="true">${I.kursor}<span>${esc(N.kursor)}</span></span>` +
    "</div></div>" +
    '<div class="apl-sl-dol">' +
    `<span class="apl-sl-pigulka apl-sl-nawigacja"><button type="button" class="apl-sl-strzalka" data-krok="-1" aria-label="Poprzedni slajd" disabled>${I.wstecz}</button>` +
    `<span class="apl-sl-licznik">1 / ${slajdy.length}</span>` +
    `<button type="button" class="apl-sl-strzalka" data-krok="1" aria-label="Następny slajd"${slajdy.length < 2 ? " disabled" : ""}>${I.dalej}</button>` +
    `${kreska}${ik("ksiazka")}${ik("pokaz")}</span>` +
    `<span class="apl-sl-pigulka apl-sl-dodaj" aria-hidden="true">${esc(N.dodaj)}${kreska}${ik("pokaz")}</span>` +
    "</div></section>"
  );
};

/* Pokazuje slajd `nr` (przycięty do zakresu), ustawia licznik i wyłącza strzałkę na końcu. */
PK.slajdIdz = (ed, nr) => {
  const strony = ed.querySelectorAll(".apl-sl-strona");
  const n = Math.max(0, Math.min(strony.length - 1, nr));
  strony.forEach((s, i) => (s.hidden = i !== n));
  ed.dataset.nr = n;
  ed.querySelector(".apl-sl-licznik").textContent = `${n + 1} / ${strony.length}`;
  ed.querySelectorAll(".apl-sl-strzalka").forEach((b) => {
    b.disabled = +b.dataset.krok < 0 ? n === 0 : n === strony.length - 1;
  });
};

/* Strzałki pigułki działają wszędzie, gdzie stoi edytor (ćwiczenie i podgląd w tekście lekcji); znacznik „kliknij tutaj” na strzałce znika po kliknięciu. */
document.addEventListener("click", (e) => {
  const b = e.target.closest(".apl-sl-strzalka");
  if (!b || b.disabled) return;
  const ed = b.closest(".apl-slajdy");
  if (b.classList.contains("apl-cel")) PK.celAplikacji(b.closest("section.cwiczenie") || ed, null);
  PK.slajdIdz(ed, +ed.dataset.nr + +b.dataset.krok);
});

/* Animacja tworzenia pierwszego slajdu: pusty slajd z pigułką „Add slide”, kursor „Claude” idzie w róg, tło slajdu i napisy pojawiają się po kolei, potem pigułka z licznikiem. `trwa()` zwraca false, gdy ćwiczenie zaczęto od nowa. Czeka przez PK.czekaj (zrzuty mogą je zatrzymać). */
PK.slajdyTworz = async (ed, trwa) => {
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const kursor = ed.querySelector(".apl-sl-kursor");
  const slajd = ed.querySelector(".apl-sl-slajd");
  const idz = (x, y) => {
    kursor.style.left = x + "%";
    kursor.style.top = y + "%";
  };
  ed.classList.add("tworzy");
  idz(30, 42);
  await PK.czekaj(900);
  if (!trwa()) return;
  ed.classList.add("tlo");
  idz(4, 5);
  await PK.czekaj(700);
  for (const el of ed.querySelectorAll('.apl-sl-strona[data-i="0"] .apl-sl-el')) {
    if (!trwa()) return;
    const r = el.getBoundingClientRect();
    const s = slajd.getBoundingClientRect();
    idz(((r.left - s.left + Math.min(r.width, 40)) / s.width) * 100, ((r.bottom - s.top) / s.height) * 100);
    el.classList.add("widac");
    await PK.czekaj(650);
  }
  if (!trwa()) return;
  await PK.czekaj(500);
  if (trwa()) ed.classList.remove("tworzy", "tlo");
};
