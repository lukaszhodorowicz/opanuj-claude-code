/* Symulator aplikacji Claude, napisy pola wiadomości, nazw modeli i menu środowisk ze zrzutów Łukasza (paczka 4 część A, D-2026-10-27-51): tekst zastępczy pustego pola (nowa rozmowa „Describe a task or ask a question” ze zrzutów 03-58-01, 04-41-10; rozmowa po pierwszej wiadomości „Type / for commands” ze zrzutów 04-22-37, 04-25-37), podpowiedź pola w czasie pracy Claude z kwadratem stop (kadr zrzutu Łukasza z lekcji 0.1, bez znaków Return: to ikony), nazwy modeli z menu modelu (04-24-16) i napisy menu środowiska (kadr zrzutu Łukasza z lekcji 0.1). Każdy napis ma wpis `gdzie: aplikacja` z zrzutem w dane/napisy-interfejsu.yaml; sprawdza to tests/test_aplikacja_4a_napisy.py. */

PK.NAPISY_POLA = {
  nowa: "Describe a task or ask a question",
  rozmowa: "Type / for commands",
  /* podpowiedź w czasie pracy Claude: na kadrze strzałki klawisza Return są ikonami (nie znakami z czcionki), więc strona rysuje je ikoną SVG (strona/styl-aplikacja-pole.css), a napisem są tylko słowa i znak ⌘ z kadru: [ikona] to send, ⌘[ikona] to queue for later */
  praca: { wysylanie: "to send,", klawisz: "⌘", kolejka: "to queue for later" },
};

/* Nazwy modeli w kolejności menu ze zrzutu 04-24-16 (to modele z konta autora zrzutu; pole `aplikacja.model` bierze jedną z nich). */
PK.NAPISY_MODELI = ["Opus 5.5", "Fable 5.1", "Sonnet 5.5", "Haiku 5.5"];

/* Model domyślny na przycisku i w menu, gdy `aplikacja.model` pominięto: pierwszy wiersz menu ze zrzutu 04-24-16 (z haczykiem). */
PK.MODEL_DOMYSLNY = "Opus 5.5";

/* Domyślny poziom wysiłku na przycisku, gdy `aplikacja.wysilek` pominięto: ten sam co na większości zrzutów (03-58-01, 04-22-37, 04-24-16, 04-25-37). */
PK.WYSILEK_DOMYSLNY = "Medium";

/* Menu środowiska nad rzędem pod polem (kadr 2-rzad-pod-polem.png z lekcji 0.1; „Local”, „Cloud” i „This computer” mają też własne wpisy z dokumentacji i ze zrzutów 27.10.2026). */
PK.NAPISY_SRODOWISK = {
  szukaj: "Search environments…",
  lokalne: "Local",
  chmura: "Cloud",
  nowe: "New environment",
};

/* Atrybuty pola wiadomości: z nich CSS (strona/styl-aplikacja-pole.css) bierze tekst zastępczy pustego pola, zależnie od stanu rozmowy (pusta, z wiadomościami, Claude pracuje). */
PK.atrybutyPola = () => {
  const P = PK.NAPISY_POLA;
  return [["data-podp-nowa", P.nowa], ["data-podp-rozmowa", P.rozmowa], ["data-podp-praca-a", P.praca.wysylanie], ["data-podp-praca-b", P.praca.klawisz], ["data-podp-praca-c", P.praca.kolejka]].map(([k, v]) => `${k}="${PK.esc(v)}"`).join(" ");
};
