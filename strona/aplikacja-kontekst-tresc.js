/* Symulator aplikacji Claude, treść otwartej karty Context (zrzut Łukasza 27.10.2026, plik 04-06-08): wiersz „N% used” z licznikiem „X / 1M”, pasek zajętości z kolorowymi odcinkami, wiersze kategorii (kolorowy znak, nazwa, tokeny, udział w oknie) i trzy wiersze ze strzałką bez skutku. Liczby wynikają z procentu karty (dana scenariusza, `aplikacja.kontekst` i krok `kontekst`): okno 1M jak na zrzucie, kategorie dzielą zajęte miejsce w proporcjach ze zrzutu (liczby całkowite, suma dokładnie równa zajętemu miejscu), bufor to 3k, a przy pełnym oknie mniej, i wolne miejsce to reszta, więc kategorie, bufor i wolne miejsce zawsze dają całe okno (100%) i wolne miejsce nie bywa ujemne. Bez procentu (karta nowej rozmowy przed pierwszą liczbą) liczby są szarymi paskami. */

/* Kategorie w kolejności ze zrzutu: [klucz napisu w PK.NAPISY_EKRANU.kontekst, numer koloru znaku, udział w zajętym miejscu wg zrzutu (17.8k, 16.9k, 14.9k, 12.1k, 12.1k, 9.9k, 7.8k)]. Wiersze „MCP server instru…”, „MCP tools (def…” i „System tools (de…” zrzut ucina, więc ich nie rysujemy. */
PK.KATEGORIE_KONTEKSTU = [["mcp", 1, 17.8], ["narzedzia", 2, 16.9], ["agenci", 3, 14.9], ["prompt", 4, 12.1], ["pamiec", 5, 12.1], ["skille", 5, 9.9], ["wiadomosci", 5, 7.8]];
PK.OKNO_KONTEKSTU = 1000000; /* tokenów: „1M” z nagłówka karty na zrzucie */
PK.BUFOR_KONTEKSTU = 3000; /* „Compact buffer 3k” ze zrzutu */
PK.STALE_WIERSZE_KONTEKSTU = ["mcp", "pamiec", "agenci"]; /* wiersze ze strzałką pod kategoriami (zrzut: MCP tools, Memory files, Custom agents); liczba po prawej to dana konta, więc szary pasek */

PK.tokenyKontekstu = (t) => `${+(t / 1000).toFixed(1)}k`;
PK.udzialKontekstu = (t) => `${((t / PK.OKNO_KONTEKSTU) * 100).toFixed(1)}%`;

/* Odcinki paska zajętości: udział kategorii w zajętym miejscu, w procentach szerokości odcinka `zajete`. */
PK.odcinkiKontekstu = () => {
  const suma = PK.KATEGORIE_KONTEKSTU.reduce((a, [, , u]) => a + u, 0);
  return PK.KATEGORIE_KONTEKSTU.map(([, k, u]) => `<i class="apl-kol-${k}" style="width:${((u / suma) * 100).toFixed(2)}%"></i>`).join("");
};

/* Nagłówek treści: „N% used” po lewej, „X / 1M” po prawej; bez procentu dwa szare paski. */
PK.sumyKontekstu = (proc) => {
  const F = PK.FRAGMENTY_EKRANU;
  if (proc === null) return '<span class="apl-szkic apl-kontekst-sz-duzy"></span><span class="apl-szkic apl-kontekst-sz"></span>';
  return `<b>${proc}${F.uzyte}</b><span>${PK.tokenyKontekstu(PK.podzialKontekstu(proc).zajete)}${F.okno}</span>`;
};

/* Podział okna dla procentu `proc` (0-100): zajęte = proc × okno, kategorie dzielą zajęte w proporcjach ze zrzutu na liczby całkowite (metoda największych reszt, suma dokładnie równa zajętemu), bufor to 3k albo tyle, ile zostało po zajętym, wolne to reszta. Suma kategorii, bufora i wolnego miejsca to zawsze całe okno, wolne ≥ 0. Zwraca {zajete, kategorie (kolejność PK.KATEGORIE_KONTEKSTU), bufor, wolne}. */
PK.podzialKontekstu = (proc) => {
  const okno = PK.OKNO_KONTEKSTU;
  const zajete = Math.round((proc * okno) / 100);
  const suma = PK.KATEGORIE_KONTEKSTU.reduce((a, [, , u]) => a + u, 0);
  const surowe = PK.KATEGORIE_KONTEKSTU.map(([, , u]) => (zajete * u) / suma);
  const kategorie = surowe.map(Math.floor);
  const najwieksze = surowe.map((s, i) => [s - kategorie[i], i]).sort((a, b) => b[0] - a[0] || a[1] - b[1]);
  for (let r = zajete - kategorie.reduce((a, b) => a + b, 0), j = 0; r > 0; r--, j++) kategorie[najwieksze[j][1]]++;
  const bufor = Math.min(PK.BUFOR_KONTEKSTU, okno - zajete);
  return { zajete, kategorie, bufor, wolne: okno - zajete - bufor };
};

/* Wiersze kategorii z liczbami dla `proc` (albo szarymi paskami przy null): siedem kategorii, bufor i wolne miejsce. */
PK.wierszeKontekstu = (proc) => {
  const N = PK.NAPISY_EKRANU.kontekst;
  const liczby = (t) =>
    proc === null
      ? '<span class="apl-kontekst-liczba"><span class="apl-szkic"></span></span><span class="apl-kontekst-udzial"><span class="apl-szkic"></span></span>'
      : `<span class="apl-kontekst-liczba">${PK.tokenyKontekstu(t)}</span><span class="apl-kontekst-udzial">${PK.udzialKontekstu(t)}</span>`;
  const wiersz = (klucz, kolor, t) => `<li><i class="apl-kontekst-znak apl-kol-${kolor}"></i><span class="apl-kontekst-nazwa">${PK.esc(N[klucz])}</span>${liczby(t)}</li>`;
  const p = PK.podzialKontekstu(proc ?? 0);
  return (
    PK.KATEGORIE_KONTEKSTU.map(([klucz, kolor], i) => wiersz(klucz, kolor, p.kategorie[i])).join("") +
    wiersz("bufor", 6, p.bufor) +
    wiersz("wolne", 7, p.wolne)
  );
};

/* Trzy wiersze ze strzałką ›: nazwa i szary pasek zamiast liczby elementów; nie otwierają niczego (żadne źródło nie opisuje ich skutku). */
PK.staleWierszeKontekstu = () =>
  PK.STALE_WIERSZE_KONTEKSTU.map((k) => `<li><span class="apl-kontekst-wiecej">${PK.IKONY_APLIKACJI.dalej}</span><span class="apl-kontekst-nazwa">${PK.esc(PK.NAPISY_EKRANU.kontekst[k])}</span><span class="apl-kontekst-liczba"><span class="apl-szkic"></span></span></li>`).join("");

/* Cała treść karty: sumy, pasek zajętości (szerokość `proc`%), wiersze kategorii i wiersze ze strzałką. */
PK.kontekstTresc = (proc) =>
  `<div class="apl-kontekst-sumy">${PK.sumyKontekstu(proc)}</div>` +
  `<span class="apl-kontekst-pasek"><span class="apl-kontekst-zajete" style="width:${proc ?? 0}%">${PK.odcinkiKontekstu()}</span></span>` +
  `<ul class="apl-kontekst-wiersze">${PK.wierszeKontekstu(proc)}</ul>` +
  `<ul class="apl-kontekst-stale">${PK.staleWierszeKontekstu()}</ul>`;

/* Nowy procent w otwartej albo zamkniętej karcie `karta`: sumy i liczby w wierszach; pasek zajętości zmienia szerokość tym samym elementem (animacja szerokości zostaje). */
PK.kontekstLiczby = (karta, proc) => {
  karta.querySelector(".apl-kontekst-sumy").innerHTML = PK.sumyKontekstu(proc);
  karta.querySelector(".apl-kontekst-wiersze").innerHTML = PK.wierszeKontekstu(proc);
};
