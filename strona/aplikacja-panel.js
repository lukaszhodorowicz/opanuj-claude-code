/* Symulator aplikacji Claude, karty panelu szczegółów sesji po prawej (zrzuty Łukasza 27.10.2026, pliki 04-06-00, 04-06-20, 04-42-00, 04-22-37): karta Environment (środowisko, folder, Remote Control z przełącznikiem), karta Connectors rozwinięta (konektory jako szare paski ze stanami Reconnect i Authenticate) i ich kolejność w panelu (Environment, Changes, Context, Connectors). Nazwy folderu i konektorów to dane konta (folder bierzemy z pola `aplikacja.folder`, konektory to szare paski). Wszystkie wiersze poza kartą Context są bez skutku, jak dotychczasowe karty panelu. */

/* Wiersz karty Environment: ikona, treść i opcjonalny element po prawej (gdy jest, treść zajmuje resztę wiersza). */
PK.wierszSrodowiska = (ikona, tresc, prawo = "") => `<li><span class="apl-sr-ikona">${ikona}</span><span class="apl-sr-tresc">${tresc}</span>${prawo}</li>`;

/* Przełącznik Remote Control: niebieski, gałka po prawej (włączony) albo szary, gałka po lewej (wyłączony: ten sam wiersz, przełącznik w drugą stronę, umowa symulatora). Nie reaguje na klik. */
PK.przelacznikZdalny = (wlaczony) =>
  `<span class="apl-przelacznik-zdalny${wlaczony ? " apl-zdalny-wl" : ""}" role="switch" aria-checked="${wlaczony}" aria-disabled="true" aria-label="${PK.esc(PK.NAPISY_EKRANU.panel.zdalne)}"><i></i></span>`;

/* Karta Environment: sesja lokalna to „This computer” z podkreślonym Save, folder i Remote Control (zrzuty 04-42-00, 04-06-00); gałęzi Gita ze zrzutu nie rysujemy (kursant bez Gita jej nie ma). Sesja w chmurze to „Default” z kołem zębatym i „Add repository…” bez Remote Control (zrzut 04-22-37). SSH nie ma zrzutu: pierwszy wiersz to szary pasek. Folder: nazwa z `aplikacja.folder`, po kropce szary pasek ścieżki; w ćwiczeniu z folderem każdej rozmowy folder zmienia się z rozmową, więc stoi tam szary pasek. */
PK.kartaSrodowiska = (apl) => {
  const P = PK.NAPISY_EKRANU.panel;
  const I = PK.IKONY_APLIKACJI;
  const E = PK.IKONY_EKRANU;
  const szary = (d) => `<span class="apl-szkic" style="width:${d}px"></span>`;
  const glowa = `<div class="apl-sr-glowa"><b>${PK.esc(P.srodowisko)}</b><span class="apl-sr-strzalka">${E.dol}</span></div>`;
  const zebatka = `<span class="apl-sr-prawo apl-sr-zebatka">${E.zebatka}</span>`;
  let wiersze;
  if (apl.srodowisko === "Cloud") {
    wiersze = PK.wierszSrodowiska(E.chmura, PK.esc(P.domyslne), zebatka) + PK.wierszSrodowiska(E.repo, `<span class="apl-sr-szary">${PK.esc(P.repozytorium)}</span>`);
  } else {
    const lokalne = apl.srodowisko === "Local";
    const folder = PK.folderyRozmow(apl) ? szary(70) : `<span class="apl-sr-nazwa">${PK.esc(apl.folder || "")}</span>`;
    wiersze =
      PK.wierszSrodowiska(I.laptop, lokalne ? PK.esc(P.komputer) : szary(80), lokalne ? `<span class="apl-sr-prawo apl-sr-zapisz">${PK.esc(P.zapisz)}</span>` : "") +
      PK.wierszSrodowiska(I.folder, `${folder}<span class="apl-sr-sciezka"> · </span>${szary(34)}`) +
      PK.wierszSrodowiska(E.kursor, PK.esc(P.zdalne), `<span class="apl-sr-prawo apl-sr-kropki">${I.kropki}</span>${PK.przelacznikZdalny(apl.remote_control !== false)}`);
  }
  return `<div class="apl-karta apl-karta-srodowisko">${glowa}<ul class="apl-sr-wiersze">${wiersze}</ul></div>`;
};

/* Karta Connectors (zrzuty 04-06-20, 04-06-00 i 04-42-00): bez pola `aplikacja.konektory_do_polaczenia` rozwinięta (zrzut 04-06-20): trzy wiersze (kafelek bez litery, nazwa jako szary pasek, pomarańczowy stan Reconnect, Authenticate, Reconnect) i szary napis Show more, niczego nie otwiera ani nie zwija. Z polem (liczba N) zwinięta jak na zrzutach 04-06-00 i 04-42-00: nagłówek ze strzałką w prawo i napisem „N to reconnect” po prawej; klik nagłówka rozwija kartę do tych samych wierszy (strzałka w dół, napis znika, jak na zrzucie 04-06-20) i zwija z powrotem; „Od nowa” i nowe polecenie zwijają ją (PK.konektoryPanelu). Nazwy konektorów i litery w kafelkach to dane konta. */
PK.NAPIS_DO_POLACZENIA = " to reconnect"; /* fragment napisu składanego z liczbą konta: „13 to reconnect”; całość sprawdza wzór w dane/napisy-interfejsu.yaml */
PK.kartaKonektorow = (doPolaczenia) => {
  const P = PK.NAPISY_EKRANU.panel;
  const zwijana = Number.isInteger(doPolaczenia);
  const wiersz = (stan, d) => `<li><span class="apl-kon-kafel"></span><span class="apl-kon-nazwa"><span class="apl-szkic" style="width:${d}px"></span></span><span class="apl-kon-stan">${PK.esc(stan)}</span></li>`;
  const glowa = zwijana
    ? `<button type="button" class="apl-sr-glowa apl-kon-naglowek" aria-expanded="false"><b>${PK.esc(P.konektory)}</b><span class="apl-sr-strzalka">${PK.IKONY_EKRANU.prawo}</span><span class="apl-kon-liczba">${doPolaczenia}${PK.esc(PK.NAPIS_DO_POLACZENIA)}</span></button>`
    : `<div class="apl-sr-glowa"><b>${PK.esc(P.konektory)}</b><span class="apl-sr-strzalka">${PK.IKONY_EKRANU.dol}</span></div>`;
  const ukryte = zwijana ? " hidden" : "";
  return (
    `<div class="apl-karta apl-karta-konektory${zwijana ? " apl-kon-zwijana" : ""}">${glowa}` +
    `<ul class="apl-kon-wiersze"${ukryte}>${wiersz(P.ponownie, 44)}${wiersz(P.uwierzytelnij, 58)}${wiersz(P.ponownie, 36)}</ul>` +
    `<span class="apl-kon-wiecej"${ukryte}>${PK.esc(P.wiecej)}</span></div>`
  );
};

/* Klik nagłówka zwiniętej karty Connectors rozwija ją i zwija (kursant może to zrobić w każdej chwili, krok scenariusza nie jest potrzebny). Karta bez pola `konektory_do_polaczenia` nie ma przycisku i niczego tu nie robi. */
PK.konektoryPanelu = (sek) => {
  const karta = sek.querySelector(".apl-kon-zwijana");
  if (!karta) return;
  const naglowek = karta.querySelector(".apl-kon-naglowek");
  const ustaw = (otwarta) => {
    karta.classList.toggle("otwarta", otwarta);
    naglowek.setAttribute("aria-expanded", String(otwarta));
    karta.querySelectorAll(".apl-kon-wiersze, .apl-kon-wiecej").forEach((e) => (e.hidden = !otwarta));
  };
  naglowek.addEventListener("click", () => ustaw(!karta.classList.contains("otwarta")));
  sek.querySelectorAll("[data-od-nowa], .polecenie").forEach((b) => b.addEventListener("click", () => ustaw(false))); /* „Od nowa” i nowe polecenie przywracają stan zwinięty, jak karta Context */
};

/* Karty panelu od góry: Environment, karta Changes (tylko w ćwiczeniach z krokami i etapami, `kartaZmian` to jej HTML albo pusty napis), Context i Connectors. `proc` to procent karty Context z `aplikacja.kontekst` (drogi i etapy); bez niego (kroki, etapy bez pola) karta ma szary pasek w miejscu liczby i niczego nie otwiera. */
PK.kartyPanelu = (apl, kartaZmian, proc) =>
  PK.kartaSrodowiska(apl) + (kartaZmian || "") + PK.kartaKontekstu(proc === undefined ? null : proc, proc === undefined) + PK.kartaKonektorow(apl.konektory_do_polaczenia);
