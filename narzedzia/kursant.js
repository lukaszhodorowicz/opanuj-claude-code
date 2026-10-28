/* Skrypt kursanta wstrzykiwany przez narzedzia/kursant.py do kopii złożonej lekcji: przeklikuje jedno ćwiczenie i oddaje dziennik kroków (element pre o id kursant-dziennik albo postMessage z ramki 390 px). */
(() => {
  const P = __PLAN__;
  const czekaj = (ms) => new Promise((r) => setTimeout(r, ms));
  const dz = { kroki: [] };
  const wyslij = () => {
    dz.bledy = window.__kursantBledy;
    if (parent !== window) return parent.postMessage({ kursant: dz }, "*");
    const pre = document.createElement("pre"); pre.id = "kursant-dziennik"; pre.textContent = JSON.stringify(dz); document.body.append(pre);
  };
  let sek = null;
  const hash = (s) => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h; };
  const widoczny = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; };
  const klikalny = (e) => !!e && !e.disabled && e.getAttribute("aria-disabled") !== "true" && getComputedStyle(e).pointerEvents !== "none" && widoczny(e);
  const polecenia = () => [...sek.querySelectorAll(".polecenie")];
  const napis = (e) => ((e.querySelector("b") || e).innerText || e.textContent || "").trim().slice(0, 120);
  /* tekst tuż przed ćwiczeniem to koniec poprzedniego bloku (tam stoi zdanie celu), tekst tuż po to początek następnego */
  const sasiad = (kier) => { const m = sek.closest(".miejsce-cwiczenia") || sek; const e = m[kier]; const s = e ? e.innerText.trim() : ""; return kier.startsWith("prev") ? s.slice(-1500) : s.slice(0, 1500); };
  function stan(krok, klik) {
    const dzieci = [...sek.children].filter((e) => !e.matches(".polecenia, .nauczyciel, .naglowek, .opis, .przycisk-klaw"));
    const tekst = dzieci.map((e) => e.innerText).join("\n").replace(/\s+/g, " ").trim();
    const ukryte = dzieci.reduce((n, e) => n + e.querySelectorAll("[hidden]").length, 0);
    const r = sek.getBoundingClientRect(), cel = sek.querySelector(".apl-cel"), tag = sek.querySelector(".apl-tag");
    const srodek = (e) => { const q = e.getBoundingClientRect(); return q.left + q.width / 2; };
    dz.kroki.push({
      krok, klik: klik || null, t: Math.round(performance.now()), y: Math.round(r.top + scrollY), wys: Math.round(r.height),
      polecenia: polecenia().map((b) => ({ tekst: napis(b), klikalny: klikalny(b), wyslane: b.classList.contains("wyslane") })),
      okno: hash(tekst + "|" + ukryte), okno_tekst: ([...sek.querySelectorAll(".apl-okno, .term")].map((e) => e.innerText).join(" | ") || tekst).replace(/\s+/g, " ").trim().slice(-800),
      nauczyciel: ((sek.querySelector(".nauczyciel") || {}).innerText || "").trim(),
      znacznik: cel ? { element: napis(cel), odchylenie: tag ? Math.round(Math.abs(srodek(tag) - srodek(cel))) : null } : null,
      w_bok: r.right > innerWidth + 1 || sek.scrollWidth > sek.clientWidth + 1,
      pola_do_wpisania: sek.querySelectorAll("input, textarea, [contenteditable=true]").length,
      folder: !!sek.querySelector(".pulpit, .folder"),
    });
  }
  async function spokoj() {
    let ostatnia = performance.now();
    const ob = new MutationObserver(() => (ostatnia = performance.now()));
    ob.observe(sek, { subtree: true, childList: true, characterData: true, attributes: true });
    const start = performance.now();
    /* 12 s ciszy (czas wirtualny): krok `mysli` trwa do 10 s, a wskaźnik pracy kręci się samym CSS, bez zmian na stronie */
    while (performance.now() - ostatnia < 12000 && performance.now() - start < 60000) await czekaj(200);
    ob.disconnect();
    document.getAnimations().forEach((a) => { try { a.finish(); } catch (e) {} });
  }
  const klik = (e) => { e.click(); return napis(e); };
  const odNowa = () => sek.querySelector("[data-od-nowa], [data-reset]");
  (async () => {
    await czekaj(300);
    sek = document.getElementById(P.cw);
    if (!sek) { dz.blad = "brak ćwiczenia " + P.cw; return wyslij(); }
    /* bez przewijania: kliknięcia działają poza ekranem, a przewinięcie (płynne w styl-strona.css) przesuwałoby kadr zrzutu */
    await spokoj();
    dz.tytul = napis(sek.querySelector(".naglowek h3") || sek);
    dz.typ = sek.classList.contains("cwiczenie-apl") ? "aplikacja" : "terminal";
    dz.tekst_przed = sasiad("previousElementSibling"); dz.tekst_po = sasiad("nextElementSibling");
    stan("start");
    const n = polecenia().length, od = odNowa() ? [["od-nowa", () => klik(odNowa())]] : [];
    const plan = !n ? [["koniec", null], ...od] : [
      ...(n > 1 ? [["poza-kolejnoscia", () => klik(polecenia()[n - 1])], ...od] : []),
      ...polecenia().map((_, i) => ["polecenie-" + (i + 1), () => klik(polecenia()[i])]), ...od,
      ["podwojny-klik", () => { const b = polecenia()[0]; b.click(); return klik(b); }], ...od];
    let nr = 0;
    const krok = async (nazwa, fn) => { if (P.stop !== null && nr >= P.stop) return false; nr++; const opis = fn(); await czekaj(50); await spokoj(); stan(nazwa, opis); return true; };
    /* kursant odpowiada w oknie wyboru (opcja 0, jak plan zrzutów), a za znacznikiem „kliknij tutaj” idzie, gdy `cel()` pozwala */
    async function dalej(cel) {
      const klikniete = new Set();
      for (let p = 0; p < 6; p++) {
        const o = sek.querySelector(".opcja:not([disabled])"), c = sek.querySelector(".apl-cel");
        const e = o || (c && cel() && !klikniete.has(c) ? c : null);
        if (!e) return true;
        klikniete.add(e);
        if (!(await krok(o ? "opcja" : "znacznik", () => klik(e)))) return false;
      }
      return true;
    }
    for (const [nazwa, fn] of plan) {
      const i = nazwa.startsWith("polecenie-") ? +nazwa.slice(10) - 1 : -1;
      if (i >= 0 && !(await dalej(() => !klikalny(polecenia()[i])))) return wyslij();
      if (fn && !(await krok(nazwa, fn))) return wyslij();
      /* po ostatnim poleceniu (albo od razu, gdy ćwiczenie gra samo) kursant idzie dalej, aż zobaczy efekt końcowy;
         w porównaniu dróg (polecenia z `data-d`) każda droga ma swój efekt, zapisany w `konce` */
      const droga = i >= 0 && polecenia()[i].dataset.d !== undefined && i < n - 1;
      if (droga || nazwa === (n ? "polecenie-" + n : "koniec")) {
        if (!(await dalej(() => true))) return wyslij();
        (dz.konce = dz.konce || []).push(dz.kroki.length - 1);
        if (!droga) dz.koniec = dz.kroki.length - 1;
      }
    }
    wyslij();
  })();
})();
