# Format scenariusza: przełącznik trybu, menu trybów, karta zgody, zmiana bez karty i podgląd folderu

Dodatek do `dane/FORMAT-SCENARIUSZA.md`, część „Symulator aplikacji Claude”. Ćwiczenie `rodzaj: "aplikacja"` może mieć listę `etapy` zamiast `kroki` albo `drogi` (nigdy razem). Etap to jedno polecenie nad oknem. Polecenia klika się po kolei (D-2026-10-25-16): aktywne jest tylko następne, wysłane i dalsze mają atrybut `disabled` i są wyszarzone, a w czasie gry etapu żadne nie jest aktywne. Kursant klika polecenie albo element okna ze znacznikiem „kliknij tutaj”; polecenie klika ten sam element za niego, a kliknięcie elementu okna prowadzi dalej tak samo jak polecenie. „Od nowa” wraca do stanu startowego (aktywne tylko pierwsze polecenie). Zamiast jednej listy etapów ćwiczenie może mieć kilka dróg (część „Drogi etapów” niżej). Wzory: `tests/dane/tryby-drogi.json` (dwie drogi: bez planu i z planem), `tests/dane/okno-zgody-tryby.json` (karta zgody w trybie Manual), `tests/dane/tryby-zmiana-bez-karty.json` (zmiana w trybie Accept edits) i `tests/dane/tryby-folder.json` (karta zgody, potem kroki `folder`). Walidator: `narzedzia/scenariusz_tryby.py` i `narzedzia/scenariusz_tryby_folder.py` (stan folderu i krok `folder`), silnik: `strona/aplikacja-tryby.js`, `strona/aplikacja-tryby-drogi.js` (drogi) i `strona/aplikacja-zgoda.js`, wygląd: `strona/styl-aplikacja-tryby.css`.

```json
{
  "id": "cw1",
  "rodzaj": "aplikacja",
  "tytul": "Zatwierdź zmianę, potem zmień tryb",
  "nauczyciel_start": "Kliknij pierwsze polecenie nad oknem.",
  "aplikacja": {
    "srodowisko": "Local",
    "folder": "Raporty-kopia",
    "tryb": "Manual"
  },
  "etapy": [
    {
      "etykieta": "Poproś o sumę",
      "kroki": [
        { "typ": "pisz", "tekst": "Wpisz sumę w raport.txt." },
        { "typ": "mysli" },
        { "typ": "claude", "tekst": "Proponuję zmianę w pliku raport.txt." },
        {
          "typ": "zgoda",
          "plik": "raport.txt",
          "linijki": [
            { "tekst": "Suma: do uzupełnienia", "zmiana": "usunieta" },
            { "tekst": "Suma: 100 zł", "zmiana": "dodana" }
          ]
        }
      ]
    },
    {
      "etykieta": "Zatwierdź zmianę",
      "klik": "zatwierdz",
      "kroki": [{ "typ": "nauczyciel", "tekst": "Zmiana trafiła do pliku." }]
    },
    { "etykieta": "Wybierz tryb w przełączniku", "klik": "przelacznik" },
    { "etykieta": "Wybierz Accept edits", "klik": "tryb", "na": "Accept edits" }
  ]
}
```

## Drogi etapów

Gdy ćwiczenie ma porównać dwa przebiegi w jednym oknie (np. pracę bez planu i z planem), pole `etapy` jest listą **dróg** zamiast listy etapów. Droga to pozycja z własną listą `etapy`; reszta pól etapów (kroki, `klik`, `na`, `fakt`) działa w niej tak samo jak dziś. Lista `etapy` jest albo samymi etapami, albo samymi drogami; nie ma osobnego pola `drogi_etapow`, bo `etapy` rozpoznają już silnik, walidator i `strona/aplikacja.js`. Wzór: `tests/dane/tryby-drogi.json`.

```json
{
  "id": "cw1",
  "rodzaj": "aplikacja",
  "tytul": "Bez planu i z planem",
  "nauczyciel_start": "Wybierz pierwszą drogę nad oknem.",
  "aplikacja": { "srodowisko": "Local", "folder": "Faktury-kopia", "tryb": "Accept edits" },
  "etapy": [
    {
      "id": "bez-planu",
      "etykieta": "Bez planu",
      "opis": "Accept edits: Claude od razu zmienia folder.",
      "tryb": "Accept edits",
      "etapy": [
        {
          "kroki": [
            { "typ": "pisz", "tekst": "Uporządkuj faktury w teczki." },
            { "typ": "mysli" },
            { "typ": "folder", "akcja": "utworz", "nazwa": "2026-09" },
            { "typ": "nauczyciel", "tekst": "Claude od razu zmienił folder." }
          ]
        }
      ]
    },
    {
      "id": "z-planem",
      "etykieta": "Z planem",
      "tryb": "Plan",
      "etapy": [
        {
          "kroki": [
            { "typ": "pisz", "tekst": "Uporządkuj faktury. Najpierw plan." },
            { "typ": "mysli" },
            { "typ": "folder", "akcja": "czyta", "pliki": ["skan_0012.pdf"] },
            { "typ": "claude", "tekst": "Plan: jedna teczka na miesiąc." }
          ]
        },
        { "etykieta": "Otwórz listę trybów", "klik": "przelacznik" },
        { "etykieta": "Wybierz Accept edits", "klik": "tryb", "na": "Accept edits" }
      ]
    }
  ]
}
```

(Ćwiczenie w przykładzie zakłada `folder_startowy` z plikami `skan_0012.pdf` i innymi fakturami.)

| Pole drogi | Co to                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------ |
| `id`       | litery, cyfry, `_` i `-`; niepowtarzalne w ćwiczeniu; po nim idzie znacznik podglądu w lekcji (wymagane)           |
| `etykieta` | napis polecenia drogi nad oknem (wymagany)                                                                          |
| `opis`     | krótkie zdanie pod etykietą                                                                                         |
| `tryb`     | tryb startowy drogi na przełączniku (`Manual`, `Accept edits`, `Plan`, `Auto`; wymagane)                            |
| `fakt`     | fakt, na którym stoi zachowanie drogi                                                                               |
| `etapy`    | etapy drogi, niepusta lista; pierwszy etap gra się po kliknięciu drogi, więc nie potrzebuje `etykiety`              |

- **Polecenia dróg** stoją nad oknem. Kliknięcie drogi zeruje okno, licznik i podgląd folderu („od nowa”), ustawia `tryb` drogi i gra jej pierwszy etap. Dalsze etapy drogi pojawiają się pod poleceniami dróg jako kolejne polecenia (pod podpisem „Dalej w drodze …”), klikane po kolei jak etapy zwykłego ćwiczenia; znaczniki „kliknij tutaj” dla klików `przelacznik`, `tryb`, `zatwierdz` i `licznik` działają jak dotąd.
- **Kolejność dróg:** na starcie aktywna jest tylko pierwsza droga. W czasie gry (etapu albo drogi, która czeka na dalsze etapy) żadna droga nie jest aktywna, a z poleceń etapów tylko następny. Po zakończeniu drogi (wszystkich jej etapów) aktywna jest tylko następna nieukończona droga; po ukończeniu wszystkich aktywne są wszystkie, do powtórki. „Od nowa” wraca do stanu startowego i zdejmuje ukończone drogi.
- **Walidator** sprawdza każdą drogę osobno, od jej stanu startowego (tryb drogi, `folder_startowy`, zamknięte menu, brak zmian i teczek) tymi samymi regułami co etapy: karta zgody tylko w Manual, zmiany folderu tylko w Accept edits albo Auto, najwyżej jedna zmiana z licznikiem na drogę itd. Dróg ma być co najmniej dwie; etap w drodze nie ma własnego pola `etapy`.
- **Podgląd w tekście lekcji:** linia `<!-- podglad: <ćwiczenie> <id drogi> -->` (np. w bloku `<!-- kolumny -->`) rysuje folder po końcu tej drogi: stan z `folder_startowy` z zastosowanymi krokami `folder` (oprócz `czyta`), znacznikami zmiany po zatwierdzonej karcie albo kroku `zmiana`, ten sam wygląd kart co pod oknem. Rysuje go `PK.podgladyDrog` w `strona/aplikacja-tryby-drogi.js`. Znacznik podglądu drogi w lekcji, której scenariusz nie ma `folder_startowy`, to błąd składania strony (`narzedzia/strona.py`); identyfikatory podglądu biorą się tylko z pozycji `etapy`, które same mają listę `etapy`.

## Pola `aplikacja`

| Pole            | Co to                                                                                                 | Wymagane                               |
| --------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `srodowisko`    | jak w ćwiczeniu z krokami: `Local`, `Cloud` albo `SSH`                                                | tak, z listy `gdzie: aplikacja`        |
| `folder`        | sama nazwa folderu, bez `/` i `~`                                                                     | tak                                    |
| `tryb`          | tryb startowy na przełączniku: `Manual`, `Accept edits`, `Plan` albo `Auto`                           | tak, z listy `gdzie: aplikacja`        |
| `auto_dostepny` | `false` usuwa Auto z menu; wtedy tryb startowy i wybór Auto to błąd (fakt `aplikacja-dostepne-tryby`) | nie, domyślnie `true`                  |
| `bypass_dostepny` | `true` dodaje do listy trybów pozycję Bypass permissions (na końcu); domyślnie `false`: pozycja pojawia się dopiero po włączeniu na koncie (fakt `aplikacja-dostepne-tryby`); wybór tej pozycji nie jest krokiem scenariusza; pole w ćwiczeniu z krokami to błąd walidatora (`narzedzia/scenariusz_panel.py`), a w ćwiczeniu z drogami dozwolone tylko wtedy, gdy któraś droga ma krok `klik` z celem `tryb-menu` (lista trybów w drogach, `FORMAT-SCENARIUSZA.md`, część „Paczka 4A”) | nie, domyślnie `false` |
| `rozmowa`       | wiadomości na starcie, jak w ćwiczeniu z krokami                                                      | nie; pustą rozmowę zaczyna krok `pisz` |
| `kontekst`      | procent na karcie Context w panelu na starcie (liczba całkowita 0-100, napis „N%” ze wzoru listy napisów); karta ma w etapach tylko procent i rozwinięcie po kliku, kroków `kontekst`, `komenda` i `z_boku` etapy nie mają (`FORMAT-SCENARIUSZA.md`, część „Paczka 4C”) | nie, bez pola karta ma szary pasek |

W ćwiczeniu z drogami `tryb` to tryb okna przed wyborem drogi; po wyborze rządzi `tryb` drogi. Pól `zmiany` i `panel` nie ma: licznik liczy się z zatwierdzonej karty zgody albo z kroku `zmiana` i stoi na karcie Changes w panelu szczegółów, więc panel jest zawsze widoczny.

## Pola etapu

| Pole       | Co to                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------ |
| `etykieta` | napis polecenia nad oknem (wymagany)                                                       |
| `opis`     | krótkie zdanie pod etykietą: co polecenie zrobi                                            |
| `klik`     | element, który klika etap, zanim zagra swoje kroki: `zatwierdz`, `przelacznik`, `tryb` albo `licznik` |
| `na`       | przy `klik: "tryb"`: nazwa trybu z menu                                                    |
| `fakt`     | fakt, na którym stoi zachowanie po kliknięciu                                              |
| `kroki`    | lista kroków (niżej); etap bez `klik` musi mieć choć jeden krok                            |

## Zachowania i ich fakty

- **Przełącznik trybu** stoi w rzędzie pod polem wiadomości i pokazuje nazwę bieżącego trybu (fakt `aplikacja-przelacznik-pod-polem-wiadomosci`).
- **`klik: "przelacznik"`** otwiera menu trybów kliknięciem przełącznika; menu stoi nad przełącznikiem (fakt `aplikacja-tryb-wybierasz-w-przelaczniku`). Na Macu menu otwiera też skrót Cmd+Shift+M (fakt `aplikacja-skrot-menu-trybu`); symulator go nie gra, lekcja podaje go zdaniem w tekście.
- **Menu** (zrzut Łukasza 27.10.2026, plik 04-41-10, sesja lokalna) ma nagłówek „Permissions · this session” i pozycje Auto, Manual, Accept edits, Plan w kolejności ze zrzutu, każda z podpisem pod nazwą; Auto tylko przy `auto_dostepny` różnym od `false` (fakt `aplikacja-dostepne-tryby`), Bypass permissions na końcu tylko przy `bypass_dostepny: true`. Bieżący tryb ma ✓. Napisy pozycji stoją w `PK.TRYBY_APLIKACJI` w `strona/aplikacja-tryby.js` (lista, kolejność jak `TRYBY_APLIKACJI` w walidatorze), menu buduje `strona/aplikacja-tryby-menu.js`, a test sprawdza napisy z listą napisów. Gdy rozmowa jest krótka (np. pusta na 390 px), rozmowa rośnie na czas otwartej listy (`min-height` przy klasie `menu-otwarte` okna), żeby lista mieściła się w oknie pod paskiem tytułu.
- **`klik: "tryb"`** wybiera pozycję `na`: menu się zamyka, a przełącznik pokazuje nazwę nowego trybu (fakty `aplikacja-tryb-wybierasz-w-przelaczniku` i `aplikacja-przelacznik-pod-polem-wiadomosci`). Działa tylko pozycja z etapu; pozostałe nic nie robią.
- **Krok `zgoda`** to karta zgody w rozmowie pod odpowiedzią Claude: nazwa pliku, podgląd zmiany (linijki usunięte i dodane) i dwa przyciski bez napisów, krzyżyk (odrzuć) i ptaszek (zatwierdź). Polski opis przycisku jest tylko dla czytnika ekranu (`aria-label`, bez dymku `title`; `PK.OPISY_ZGODY` w `strona/aplikacja-zgoda.js`), bo dokumentacja nie podaje napisów przycisków (fakty `aplikacja-manual-podglad-i-przyciski`, `aplikacja-manual-przyciski-zatwierdzania`). W ćwiczeniu z `drogi` (nie `etapy`) krok `zgoda` ma osobny wariant „folder chroniony”: ta sama karta bez nazwy pliku i bez podglądu linijek, tylko dla ścieżki w `.claude/` (opis: `dane/FORMAT-SCENARIUSZA.md`, część „Karta zgody w drodze”).
- **`klik: "zatwierdz"`** zatwierdza kartę: karta zostaje w rozmowie bez przycisków, zmiana trafia do pliku (fakt `tryb-manual-aplikacja-czeka-na-zatwierdzenie`). Na karcie Changes pojawiają się liczby `+N -M` z linijek karty. Kliknięcie liczb albo przycisku Changes na pasku tytułu otwiera widok zmian z tą samą zmianą (fakty `aplikacja-widok-zmian-liczby-na-karcie-changes`, `aplikacja-klikniecie-wskaznika-otwiera-widok-zmian`, `aplikacja-widok-zmian-przycisk-changes-na-pasku-tytulu`). Przed zatwierdzeniem karta Changes nie ma liczb.
- **Krok `zmiana`** to zmiana plików bez karty zgody, tylko w trybie Accept edits albo Auto (fakty `aplikacja-auto-i-accept-edits-stosuja-zmiany`, `accept-edits-edycje-w-folderze-bez-pytania`). W rozmowie nic nie przybywa: ani karty, ani podglądu. Liczby `+N -M` ze wszystkich plików kroku pojawiają się od razu na karcie Changes, a liczby albo przycisk Changes otwierają widok zmian z plikiem po pliku, tak samo jak po zatwierdzeniu karty (fakty `aplikacja-widok-zmian-liczby-na-karcie-changes`, `aplikacja-klikniecie-wskaznika-otwiera-widok-zmian`, `aplikacja-widok-zmian-przycisk-changes-na-pasku-tytulu`). Jeden krok może zmienić kilka plików naraz. W ćwiczeniu jest najwyżej jedna zmiana z licznikiem (karta zgody albo krok `zmiana`). „Od nowa” zdejmuje licznik i zamyka widok zmian.
- **Podgląd folderu pod oknem (D-2026-10-23-10)** stoi tuż za oknem, gdy scenariusz ma `folder_startowy` (bez tej listy podglądu nie ma). To ten sam podgląd co w ćwiczeniach z `kroki` i `drogami` (`strona/aplikacja-folder.js`, opis w `dane/FORMAT-SCENARIUSZA.md`): element kursu, nie interfejs aplikacji, więc bez faktu. Pokazuje nazwę folderu z `aplikacja.folder`, nazwy plików i ikony, bez licznika i bez słów. Zatwierdzenie karty zgody i krok `zmiana` dają kartom zmienionych plików znacznik zmiany z liczbami `+N -M` z ich linijek. Krok `folder` zmienia sam folder (niżej). „Od nowa” przywraca stan z `folder_startowy`.
- **`klik: "licznik"`** klika liczby `+N -M` na karcie Changes i otwiera widok zmian, jak w ćwiczeniu z `kroki`; liczby dostają znacznik „kliknij tutaj”, a kliknięcie przycisku Changes na pasku tytułu zalicza etap tak samo (fakty `aplikacja-klikniecie-wskaznika-otwiera-widok-zmian`, `aplikacja-widok-zmian-liczby-na-karcie-changes`).
- **Przycisk odrzucenia** jest na karcie, ale kliknięcie go nic nie robi (`aria-disabled`): dokumentacja nie opisuje skutku odrzucenia.

## Kroki etapu

| `typ`        | Pola                            | Co robi                                                                                            |
| ------------ | ------------------------------- | -------------------------------------------------------------------------------------------------- |
| `pisz`       | `tekst`, `fakt`?                | tekst sam pojawia się w polu wiadomości i idzie do rozmowy (fakt `aplikacja-enter-wysyla-zadanie`) |
| `mysli`      | `ms`? (1-10000, domyślnie 1200) | trzy kropki bez słów, jak w drogach                                                                |
| `claude`     | `tekst`, `fakt`?                | odpowiedź Claude, bez ikony                                                                        |
| `zgoda`      | `plik`, `linijki`, `fakt`?      | karta zgody; `linijki` jak w polu `zmiany` (`tekst`, `zmiana`: `dodana`/`usunieta`)                |
| `zmiana`     | `pliki`, `fakt`?                | zmiana bez karty (Accept edits, Auto); `pliki`: lista `{plik, linijki}`, linijki jak w karcie zgody |
| `folder`     | `akcja`, pola akcji, `fakt`?    | zmiana w folderze, która nie jest edycją treści; wymaga `folder_startowy` (akcje niżej)           |
| `nauczyciel` | `tekst`, `fakt`?                | zmienia komunikat nauczyciela                                                                      |

### Krok `folder`

| `akcja`    | Pola                                  | Co widać na kartach                                                             |
| ---------- | ------------------------------------- | ------------------------------------------------------------------------------- |
| `czyta`    | `pliki` (lista nazw)                  | karty z listy na chwilę unoszą się z obwódką i okiem                            |
| `nowy`     | `plik`                                | nowa karta wpada na blat                                                        |
| `zmien`    | `plik`, `nazwa` (nowa nazwa)          | karta zostaje na miejscu z nową nazwą, przez chwilę z napisem „było: …”; znacznik zmiany treści (ołówek z liczbami), jeśli plik go miał, idzie z kartą |
| `usun`     | `plik`                                | karta zostaje na miejscu, przekreślona                                          |
| `utworz`   | `nazwa` (teczki)                      | nowa pusta teczka nad plikami                                                   |
| `przenies` | `plik`, `do` (teczka), `uwaga`?       | karta przechodzi do teczki; `uwaga` to krótki napis na karcie, np. „zły folder” |

`czyta` i `nowy` idą przez `zmiana()` podglądu, reszta przez metody `PK.Folder` (`zmien`, `usun`, `utworz`, `przenies`; `strona/folder.js`). W kroku nie ma innych pól niż te z tabeli (poza `typ` i `fakt`). Po każdej akcji innej niż `czyta` nauczyciel odzywa się najdalej dwa kroki później (`narzedzia/czytelnosc.py`).

## Błędy, które łapie walidator

- `etapy` razem z `kroki`, `drogi` albo `nowe_pliki`; pusta lista `etapy`; etap bez etykiety; etap bez `klik` i bez kroków.
- Drogi etapów: lista `etapy` miesza drogi i etapy; jedna droga; droga bez `id` (albo z id spoza liter, cyfr, `_` i `-`, albo powtórzonym), bez `etykiety`, z `trybem` spoza listy napisów albo Auto przy `auto_dostepny: false`, z polem spoza tabeli, bez etapów; etap w drodze z własnym polem `etapy`; menu otwarte na końcu drogi.
- (Dotyczy `etapy`; karta zgody w `drogi` ma własne reguły w `dane/FORMAT-SCENARIUSZA.md`.) Karta zgody poza trybem Manual, dla pliku spoza `folder_startowy` (karta pokazuje tylko edycję istniejącego pliku, nie tworzenie) albo druga w ćwiczeniu: żaden fakt nie podaje licznika po drugiej zmianie.
- Krok `zmiana` w trybie Manual albo Plan (Claude nie stosuje wtedy zmian sam); druga zmiana z licznikiem w ćwiczeniu (druga `zmiana`, `zmiana` po zatwierdzonej karcie zgody i karta zgody po `zmiana`: żaden fakt nie podaje licznika po kolejnej zmianie); plik spoza `folder_startowy` (zmiana nie tworzy plików); ten sam plik dwa razy w jednym kroku; pusta lista `pliki`, plik bez linijki zmiany; licznik spoza wzoru z listy napisów.
- Krok `folder` z akcją inną niż `czyta` w trybie Manual albo Plan (Claude nie zmienia wtedy plików sam; fakty `tryb-manual-aplikacja-czeka-na-zatwierdzenie`, `plan-aplikacja-opis`); `czyta` jest dozwolone w każdym trybie.
- Krok `folder` bez `folder_startowy`; akcja spoza listy; pole, które nie należy do akcji; nazwa pusta albo z `/`.
- Stan folderu po kolejnych krokach etapów: `czyta`, `zmien`, `usun` i `przenies` tylko na plik, który w tej chwili leży w folderze (nie na usunięty ani na plik pod starą nazwą); `nowy` i `zmien` na nazwę, której żadna karta jeszcze nie nosi (karta usuniętego pliku też ją zajmuje); `utworz` nowej teczki; `przenies` do teczki utworzonej wcześniej i tylko pliku luźnego (plik, który już leży w jakiejkolwiek teczce, nie przechodzi do innej: podgląd zdejmuje plik tylko z luźnych); ten sam plik dwa razy w liście `pliki`.
- Karta zgody albo krok `zmiana` dla pliku, którego w tej chwili nie ma w folderze (także po zmianie nazwy albo usunięciu).
- Krok inny niż `nauczyciel`, gdy karta czeka na decyzję (Claude czeka) albo gdy menu jest otwarte.
- `licznik` bez licznika na karcie Changes (przed zatwierdzoną kartą zgody i przed krokiem `zmiana`, albo gdy karta czeka) i przy otwartym menu trybu.
- `zatwierdz` bez czekającej karty; `przelacznik` przy otwartym menu albo gdy karta zgody czeka (brak faktu o zmianie trybu w tej chwili); `tryb` bez otwartego menu, z nazwą spoza listy napisów, z trybem już wybranym albo z Auto przy `auto_dostepny: false`; pole `na` przy innym kliku; menu otwarte na końcu ćwiczenia.
- Licznik `+N -M` z linijek karty spoza wzoru z listy napisów interfejsu.
