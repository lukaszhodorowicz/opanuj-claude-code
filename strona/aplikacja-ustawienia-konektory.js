/* Symulator aplikacji Claude, okno Settings → Connectors, zakładka Yours (zrzut Łukasza 04-22-53 z 27.10.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_04-22-53.png w pamięci projektu): tabela podłączonych konektorów z kolumnami Connector, Type i Status; krok `klik` z celem `ustawienia-connectors` (wejście: konto na dole paska bocznego, umowa symulatora, jak dla `ustawienia-claude-code`; kod okna: strona/aplikacja-ustawienia-cc.js). Nazwy konektorów konta (blender, GitHub Integration, runpod, slack) i nazwy wtyczek w podpisie „Provided by the … plugin” to dane konta: szare paski. „Claude in Chrome” to konektor wbudowany w aplikację (znaczek Included), więc ma napis. Wszystko w oknie jest bez skutku. Stałe są zapisane jak JSON (cudzysłowy przy kluczach): testy czytają je stąd i sprawdzają w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */

/* Nagłówki tabeli i wiersze w kolejności ze zrzutu: `nazwa` null to szary pasek, `podpis` true to dopisek „Provided by the … plugin” pod nazwą, `znaczek` to pigułka przy typie, `stan` null to ptaszek. */
PK.KONEKTORY_TWOJE = {
  "naglowki": ["Connector", "Type", "Status"],
  "podpis": ["Provided by the", "plugin"],
  "wiersze": [
    {"nazwa": null, "podpis": false, "typ": "Desktop", "znaczek": "Local dev", "stan": null},
    {"nazwa": "Claude in Chrome", "podpis": false, "typ": "Desktop", "znaczek": "Included", "stan": null},
    {"nazwa": null, "podpis": false, "typ": "Web", "znaczek": null, "stan": null},
    {"nazwa": null, "podpis": true, "typ": "Web", "znaczek": "Plugin", "stan": "Connects in sessions"},
    {"nazwa": null, "podpis": true, "typ": "Web", "znaczek": "Plugin", "stan": "Connects in sessions"}
  ]
};

/* Opisy tylko dla czytnika ekranu (aria-label): tekst kursu po polsku, nie napisy aplikacji. */
PK.OPISY_USTAWIEN_KONEKTOROW = {
  okno: "Ustawienia, konektory, zakładka Yours (w ćwiczeniu bez skutku na kliknięcia)",
  tabela: "Lista podłączonych konektorów",
  stan: "Połączony",
};

/* Treść strony Connectors, zakładka Yours: tabela z nagłówkiem i wierszami (ikona konektora, nazwa albo szary pasek, typ z pigułką, stan). */
PK.trescKonektorowTwoich = () => {
  const { esc } = PK;
  const T = PK.KONEKTORY_TWOJE;
  const I = PK.IKONY_KATALOGU;
  const pasek = (d) => `<span class="apl-szkic apl-ukon-pasek" style="width:${d}px"></span>`;
  const nazwa = (w, i) => {
    const glowna = w.nazwa ? `<b>${esc(w.nazwa)}</b>` : `<b class="apl-ukon-dana">${pasek(60 + (i % 3) * 22)}</b>`;
    const podpis = w.podpis ? `<span class="apl-ukon-podpis">${esc(T.podpis[0])} ${pasek(38)} ${esc(T.podpis[1])}</span>` : "";
    return `<span class="apl-ukon-ikona">${I[w.nazwa === "Claude in Chrome" ? "kursor" : "klocki"]}</span><span class="apl-ukon-tekst">${glowna}${podpis}</span>`;
  };
  const typ = (w) => `<span class="apl-ukon-typ">${esc(w.typ)}</span>${w.znaczek ? `<span class="apl-ukon-znaczek">${esc(w.znaczek)}</span>` : ""}`;
  const stan = (w) => (w.stan ? `<span class="apl-ukon-stan-tekst">${esc(w.stan)}</span>` : `<span class="apl-ukon-ptaszek" role="img" aria-label="${esc(PK.OPISY_USTAWIEN_KONEKTOROW.stan)}">${I.ptaszek}</span>`);
  const wiersz = (w, i) => `<tr><td class="apl-ukon-nazwa">${nazwa(w, i)}</td><td class="apl-ukon-typ-kom">${typ(w)}</td><td class="apl-ukon-stan">${stan(w)}</td></tr>`;
  return (
    `<table class="apl-ukon-tabela" aria-label="${esc(PK.OPISY_USTAWIEN_KONEKTOROW.tabela)}"><thead><tr>${T.naglowki.map((n) => `<th scope="col">${esc(n)}</th>`).join("")}</tr></thead>` +
    `<tbody>${T.wiersze.map(wiersz).join("")}</tbody></table>`
  );
};
