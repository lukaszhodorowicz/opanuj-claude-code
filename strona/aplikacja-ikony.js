/* Symulator aplikacji Claude, część stała: napisy interfejsu, ikony kreskowe i licznik linijek „+N -M”. */

/* Jedyne napisy interfejsu aplikacji, które rysuje ten plik; test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). */
PK.NAPISY_APLIKACJI = {
  code: "Code",
  changes: "Changes",
  terminal: "Terminal",
  browser: "Browser",
  files: "Files",
  nowa: "+ New",
  effort: "Effort",
};

/* Ikony rysowane kreską; żadna nie niesie napisu. */
PK.IKONY_APLIKACJI = (() => {
  const s = (d, w) =>
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' +
    (w || 1.7) +
    '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    d +
    "</svg>";
  return {
    bok: s(
      '<rect x="3.5" y="5" width="17" height="14" rx="3"/><path d="M9 5v14"/>',
    ),
    wstecz: s('<path d="M14.5 6 8.5 12l6 6"/>'),
    dalej: s('<path d="m9.5 6 6 6-6 6"/>'),
    czat: s(
      '<path d="M12 4.5c-4.4 0-7.5 2.9-7.5 6.6 0 2 1 3.8 2.6 5l-.6 3.4 3.6-1.9c.6.1 1.2.2 1.9.2 4.4 0 7.5-2.9 7.5-6.7S16.4 4.5 12 4.5z"/>',
    ),
    kod: s('<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>'),
    plus: s('<path d="M12 5v14M5 12h14"/>'),
    szukaj: s('<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>'),
    karty: s(
      '<rect x="4" y="8" width="10" height="12" rx="2"/><path d="M9 8V6a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-4"/>',
    ),
    dzwonek: s(
      '<path d="M6.5 16.5V11a5.5 5.5 0 0 1 11 0v5.5l1.5 1.5H5z"/><path d="M10 20.5h4"/>',
    ),
    teczka: s(
      '<rect x="3.5" y="7.5" width="17" height="12" rx="2.5"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5"/>',
    ),
    kropki: s(
      '<circle cx="6" cy="12" r=".6"/><circle cx="12" cy="12" r=".6"/><circle cx="18" cy="12" r=".6"/>',
      2.6,
    ),
    /* ⋮ na pasku tytułu rozmowy: trzy kropki pionowo (dokumentacja i zrzut gh99530); poziome kropki `kropki` zostają w pasku bocznym */
    kropkiPionowe: s(
      '<circle cx="12" cy="6" r=".6"/><circle cx="12" cy="12" r=".6"/><circle cx="12" cy="18" r=".6"/>',
      2.6,
    ),
    terminal: s(
      '<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><path d="m7.5 10 2.5 2-2.5 2M12.5 15h4"/>',
    ),
    zmiany: s(
      '<path d="M7 3.5h10A1.5 1.5 0 0 1 18.5 5v14a1.5 1.5 0 0 1-1.5 1.5H7A1.5 1.5 0 0 1 5.5 19V5A1.5 1.5 0 0 1 7 3.5z"/><path d="M12 7.5v5M9.5 10h5M9.5 16h5"/>',
    ),
    przegladarka: s(
      '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.2 2.3 3.2 5 3.2 8s-1 5.7-3.2 8c-2.2-2.3-3.2-5-3.2-8s1-5.7 3.2-8z"/>',
    ),
    plik: s('<path d="M7 3.5h7l4.5 4.5v12.5H7z"/><path d="M14 3.5V8h4.5"/>'),
    laptop: s(
      '<rect x="5" y="5.5" width="14" height="10" rx="1.5"/><path d="M3 18.5h18"/>',
    ),
    folder: s(
      '<path d="M3.5 7a1.5 1.5 0 0 1 1.5-1.5h4.2l2 2.2H19a1.5 1.5 0 0 1 1.5 1.5v8.3A1.5 1.5 0 0 1 19 19H5a1.5 1.5 0 0 1-1.5-1.5z"/>',
    ),
    wyslij: s('<path d="M12 18V6M6.5 11.5 12 6l5.5 5.5"/>', 2.1),
  };
})();

/* Liczby linijek ze wszystkich plików zmiany: {dodane, usuniete, tekst: "+N -M"}. */
PK.licznikZmian = (zmiany) => {
  let dodane = 0;
  let usuniete = 0;
  (zmiany || []).forEach((p) =>
    (p.linijki || []).forEach((l) => {
      if (l.zmiana === "dodana") dodane++;
      if (l.zmiana === "usunieta") usuniete++;
    }),
  );
  return { dodane, usuniete, tekst: "+" + dodane + " -" + usuniete };
};
