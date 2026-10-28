/* Symulator aplikacji Claude, folder każdej rozmowy (ćwiczenie z drogami i polem `sesje[].folder`): lista rozmów w pasku bocznym podzielona na grupy folderów z nagłówkiem nazwy teczki (ze strzałką i znakiem + ze zrzutów Łukasza 27.10.2026, bez skutku), kontrolka folderu w rzędzie pod polem (tylko w rozmowie bez pierwszej prośby) i nowy wiersz w grupie swojego folderu po pierwszej prośbie. Nazwy teczek to dane scenariusza, nie napisy interfejsu. Układ z zrzutu z sieci (materialy/zrzuty-aplikacji/pasek-boczny-sesje/, grupy z nagłówkami, gh102731 i rząd pod polem, gh102210). Grę kroków prowadzi strona/aplikacja-sesje-gra.js. */

/* Ćwiczenie ma folder każdej rozmowy: choć jeden wiersz `aplikacja.sesje` ma pole `folder` (walidator wymaga go wtedy w każdym). */
PK.folderyRozmow = (apl) => ((apl && apl.sesje) || []).some((s) => s.folder);

/* Nagłówek grupy (zrzuty Łukasza 27.10.2026, 03-58-01 i 04-22-37): nazwa teczki małym szarym tekstem, za nią strzałka w dół i po prawej znak +. Strzałka i + są tylko narysowane (żadne źródło nie opisuje ich skutku, w symulatorze bez klika, poza czytnikiem ekranu). */
PK.naglowekGrupyFolderu = (folder) =>
  `<div class="apl-grupa-folderu" data-folder="${PK.esc(folder)}"><span>${PK.esc(folder)}</span>` +
  `<i class="apl-grupa-strzalka" aria-hidden="true">${PK.IKONY_EKRANU.dol}</i><i class="apl-grupa-plus" aria-hidden="true">${PK.IKONY_APLIKACJI.plus}</i></div>`;

/* Wiersze listy w grupach: rozmowa startowa (otwarta, podświetlona) i wiersze `sesje`; grupy w kolejności, w jakiej folder pojawia się pierwszy raz na liście (umowa symulatora, żadne źródło nie opisuje kolejności grup), nad każdą nagłówek. Zwraca listę fragmentów HTML do wstawienia pod nagłówkiem listy. */
PK.wierszeGrupFolderow = (apl) => {
  const wiersze = [{ start: true, folder: apl.folder }, ...apl.sesje.map((s) => ({ id: s.id, folder: s.folder }))];
  const grupy = [];
  wiersze.forEach((w) => {
    let g = grupy.find((x) => x.folder === w.folder);
    if (!g) grupy.push((g = { folder: w.folder, wiersze: [] }));
    g.wiersze.push(w);
  });
  let nr = 0;
  return grupy.flatMap((g) => [
    PK.naglowekGrupyFolderu(g.folder),
    ...g.wiersze.map((w) => PK.wierszSesji({ otwarta: !!w.start, id: w.id, menu: true, proc: PK.SZEROKOSCI_WIERSZY[nr++ % PK.SZEROKOSCI_WIERSZY.length] })),
  ]);
};

/* Wiersz nowej rozmowy po pierwszej prośbie: na górze grupy swojego folderu; gdy takiej grupy nie ma, nowa grupa na górze listy (umowa symulatora, żadne źródło nie opisuje miejsca w grupie ani nowej grupy). Zwraca wstawiony wiersz. */
PK.wstawWierszFolderu = (lista, folder, htmlWiersza) => {
  const naglowek = [...lista.querySelectorAll(".apl-grupa-folderu")].find((e) => e.dataset.folder === folder);
  if (naglowek) {
    naglowek.insertAdjacentHTML("afterend", htmlWiersza);
    return naglowek.nextElementSibling;
  }
  lista.firstElementChild.insertAdjacentHTML("afterend", PK.naglowekGrupyFolderu(folder) + htmlWiersza);
  return lista.firstElementChild.nextElementSibling.nextElementSibling;
};

/* Po archiwizacji wiersza grupa bez wierszy traci nagłówek. */
PK.zdejmijPusteGrupy = (lista) =>
  lista.querySelectorAll(".apl-grupa-folderu").forEach((n) => {
    let e = n.nextElementSibling;
    while (e && e.classList.contains("apl-tag-rzad")) e = e.nextElementSibling;
    if (!e || !e.classList.contains("apl-wiersz")) n.remove();
  });

/* Kontrolka folderu w rzędzie pod polem: przycisk z ikoną folderu i nazwą teczki (zrzut gh102210). */
PK.kontrolkaFolderu = (ikona, folder) =>
  `<button type="button" class="apl-chip apl-chip-folder">${ikona}<span>${PK.esc(folder)}</span></button>`;

/* Znacznik „kliknij tutaj” pod rzędem pod polem (kontrolka folderu); mignięcie napisu po zmianie teczki. */
PK.MIGNIECIE_FOLDERU_MS = 700;
Object.assign(PK.PO_CELU_KROKU, { folder: ".apl-rzad" });
