/* Okno terminala Claude Code w symulatorze: ekran, pasek trybu i menu z polską legendą opcji. */
const PK = {
  czekaj: (ms) => new Promise((r) => setTimeout(r, ms)),
  esc: (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;"),
  TRYBY: {
    manual: { tekst: "⏸ manual mode on", klasa: "manual" },
    edycje: { tekst: "⏵⏵ accept edits on", klasa: "edycje" },
    plan: { tekst: "⏸ plan mode on", klasa: "plan" },
    auto: { tekst: "⏵⏵ auto mode on", klasa: "auto" },
  },
  CZASOWNIKI: ["Pondering", "Thinking", "Reading", "Considering"],
};

PK.Terminal = function (el, opcje) {
  const { esc, czekaj } = PK;
  el.innerHTML =
    '<div class="term-gora"><span class="kropki"><b></b><b></b><b></b></span><span class="term-tytul">' +
    esc(opcje.tytul || "claude") +
    '</span><span style="width:45px"></span></div>' +
    '<div class="term-ekran' +
    (opcje.niski ? " niski" : "") +
    '"></div>' +
    '<div class="term-dol"><div class="wejscie">&gt; <span class="pisane"></span><span class="kursor">&nbsp;</span></div>' +
    '<div class="status"><span class="tryb"></span><span>? for shortcuts</span></div></div>';
  const ekran = el.querySelector(".term-ekran");
  const tryb = el.querySelector(".tryb");
  const pisane = el.querySelector(".pisane");
  let legenda = opcje.legenda || el.nextElementSibling;
  if (!legenda || !legenda.classList.contains("legenda")) {
    legenda = document.createElement("div");
    legenda.className = "legenda";
    el.insertAdjacentElement("afterend", legenda);
  }
  legenda.hidden = true;
  function wiersz(html, klasa) {
    const d = document.createElement("span");
    d.className = "l " + (klasa || "");
    d.innerHTML = html;
    return d;
  }

  const t = {
    el,
    gen: 0,
    tryb: "manual",
    wskaznik: null /* wiersz „✻ … (esc to interrupt)”, gdy Claude pracuje */,
    /* ostatnie wywołanie narzędzia: {koniec: wiersz, pod którym stanie następna linia wyniku, zmiana, maWynik} */
    narz: null,
    ustawTryb(k, mignij) {
      t.tryb = k;
      tryb.textContent = PK.TRYBY[k].tekst;
      tryb.className = "tryb " + PK.TRYBY[k].klasa;
      if (mignij) {
        void tryb.offsetWidth;
        tryb.classList.add("mignij");
      }
    },
    wyczysc() {
      t.gen++;
      t.wskaznik = null;
      t.narz = null;
      legenda.hidden = true;
      ekran.innerHTML = "";
      pisane.textContent = "";
    },
    /* nowy wiersz rozmowy; gdy Claude pracuje, staje nad wskaźnikiem pracy, który zostaje na dole */
    dodaj(html, klasa) {
      const d = wiersz(html, klasa);
      if (t.wskaznik && t.wskaznik.parentNode === ekran)
        ekran.insertBefore(d, t.wskaznik);
      else ekran.appendChild(d);
      ekran.scrollTop = ekran.scrollHeight;
      return d;
    },
    odstep() {
      t.dodaj("", "odstep");
    },
    /* znaki w polu „>” jak przy pisaniu; false, gdy w trakcie ćwiczenie ruszyło od nowa */
    async wpisz(tekst, g) {
      for (const z of tekst) {
        if (g !== t.gen) return false;
        pisane.textContent += z;
        await czekaj(18);
      }
      await czekaj(250);
      if (g !== t.gen) return false;
      pisane.textContent = "";
      return true;
    },
    async pisz(tekst, g) {
      if (!(await t.wpisz(tekst, g))) return false;
      t.dodaj("&gt; <b>" + esc(tekst) + "</b>", "ty");
      t.odstep();
      return true;
    },
    /* zapala wskaźnik pracy albo zostawia ten, który już świeci */
    pracuj() {
      if (!t.wskaznik) {
        const c =
          PK.CZASOWNIKI[Math.floor(Math.random() * PK.CZASOWNIKI.length)];
        t.wskaznik = t.dodaj(
          '<span class="kreci">✻ ' +
            c +
            '… <span class="szary">(esc to interrupt)</span></span>',
        );
      }
    },
    zgasPrace() {
      if (t.wskaznik) t.wskaznik.remove();
      t.wskaznik = null;
    },
    /* zostaw: wskaźnik nie gaśnie po czasie, bo następny krok (kolejka) dzieje się w trakcie tej samej pracy */
    async kreci(ms, g, zostaw) {
      t.pracuj();
      await czekaj(ms);
      if (g !== t.gen) return false;
      if (!zostaw) t.zgasPrace();
      return true;
    },
    /* wiadomość wysłana, gdy Claude pracuje: wskaźnik pracy świeci dalej, a wiadomość czeka w rozmowie na szaro */
    async kolejka(tekst, g, zostaw) {
      t.pracuj();
      if (!(await t.wpisz(tekst, g))) return false;
      t.dodaj("&gt; <b>" + esc(tekst) + "</b>", "ty kolejka");
      t.odstep();
      if (!zostaw) t.zgasPrace();
      return true;
    },
    claude(tekst) {
      /* Claude zaczyna odpowiadać, więc wiadomości z kolejki przestają być szare */
      ekran
        .querySelectorAll(".l.kolejka")
        .forEach((d) => d.classList.remove("kolejka"));
      t.dodaj('<span class="kula claude">⏺</span> ' + esc(tekst));
      t.odstep();
    },
    narzedzie(nazwa, arg, wyniki, zmiana) {
      const d = t.dodaj(
        '<span class="kula narzedzie">⏺</span> <span class="nazwa-narz">' +
          esc(nazwa) +
          "</span>(" +
          esc(arg) +
          ")",
      );
      t.narz = { koniec: d, zmiana, maWynik: false };
      t.wynik(wyniki);
      t.odstep();
    },
    /* linie „⎿” pod ostatnim wywołaniem narzędzia, także gdy niżej stoją już wiadomości z kolejki */
    wynik(linie) {
      const n = t.narz;
      if (!n || n.koniec.parentNode !== ekran) return;
      for (const w of linie || []) {
        const d = wiersz(
          (n.maWynik ? "     " : "  ⎿  ") +
            '<span class="wynik ' +
            (n.zmiana ? "zmiana" : "") +
            '">' +
            esc(w) +
            "</span>",
        );
        n.koniec.after(d);
        n.koniec = d;
        n.maWynik = true;
        ekran.scrollTop = ekran.scrollHeight;
      }
    },
    /* def: {tytul, tresc, pytanie, opcje:[{napis, pl, opis}], ramka}; zakoncz(i) po wyborze. */
    menu(def, zakoncz) {
      const opcje = def.opcje;
      let tresc = "";
      if (def.tresc) {
        const w = def.tresc.split("\n");
        const tekst =
          def.ramka === "plan"
            ? "<b>" + esc(w[0]) + "</b>\n" + esc(w.slice(1).join("\n"))
            : esc(def.tresc);
        tresc = '<span class="plan-tresc">' + tekst + "</span>";
      }
      const box = t.dodaj("", "");
      box.innerHTML =
        '<span class="ramka ' +
        (def.ramka || "") +
        '">' +
        (def.tytul ? '<span class="tytul">' + esc(def.tytul) + "</span>" : "") +
        tresc +
        '<span class="szare">' +
        esc(def.pytanie || "") +
        '</span><span class="opcje"></span><span class="podpowiedz-klaw">↑/↓ i Enter albo kliknij</span></span>';
      const kont = box.querySelector(".opcje");
      let wybrany = 0;
      const przyciski = opcje.map((o, i) => {
        const b = document.createElement("button");
        b.className = "opcja";
        b.innerHTML =
          '<span class="strzalka">' +
          (i === 0 ? "❯" : "&nbsp;") +
          "</span> " +
          (i + 1) +
          ". " +
          esc(o.napis);
        b.addEventListener("click", () => wybierz(i));
        b.addEventListener("mouseenter", () => {
          if (!b.disabled) zaznacz(i);
        });
        kont.appendChild(b);
        return b;
      });
      let wiersze = [];
      if (opcje.every((o) => o.opis)) {
        legenda.hidden = false;
        /* zawsze ten sam układ: numer, polska nazwa, pod nią napis z programu; opis tylko przy zaznaczonej opcji */
        legenda.innerHTML =
          '<div class="leg-tytul">Co znaczą te opcje</div>' +
          opcje
            .map(
              (o, i) =>
                '<div class="leg-wiersz"><span class="leg-nr">' +
                (i + 1) +
                '</span><span class="leg-nazwy"><span class="leg-pl">' +
                esc(o.pl || o.napis) +
                '</span><span class="leg-ang">' +
                esc(o.napis) +
                '</span></span><span class="leg-opis">' +
                esc(o.opis) +
                "</span></div>",
            )
            .join("");
        wiersze = [...legenda.querySelectorAll(".leg-wiersz")];
      } else {
        legenda.hidden = true;
      }
      function zaznacz(i) {
        wybrany = i;
        przyciski.forEach((b, j) => {
          b.classList.toggle("wybrana", j === i);
          b.querySelector(".strzalka").innerHTML = j === i ? "❯" : "&nbsp;";
        });
        wiersze.forEach((w, j) => w.classList.toggle("aktywny", j === i));
      }
      function klaw(e) {
        if (!document.body.contains(box))
          return el.removeEventListener("keydown", klaw);
        if (e.key === "ArrowDown") {
          e.preventDefault();
          zaznacz((wybrany + 1) % opcje.length);
        }
        if (e.key === "ArrowUp") {
          e.preventDefault();
          zaznacz((wybrany + opcje.length - 1) % opcje.length);
        }
        if (e.key === "Enter") {
          e.preventDefault();
          wybierz(wybrany);
        }
      }
      function wybierz(i) {
        przyciski.forEach((b) => (b.disabled = true));
        zaznacz(i);
        el.removeEventListener("keydown", klaw);
        if (wiersze.length) {
          legenda.querySelector(".leg-tytul").textContent = "Twój wybór";
          wiersze.forEach((w, j) => w.classList.toggle("wygaszony", j !== i));
        }
        zakoncz(i);
      }
      el.addEventListener("keydown", klaw);
      zaznacz(0);
      ekran.scrollTop = ekran.scrollHeight;
    },
  };
  t.ustawTryb(opcje.tryb || "manual");
  return t;
};
