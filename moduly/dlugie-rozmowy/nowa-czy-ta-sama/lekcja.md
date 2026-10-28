<em>Przewodnik po Claude Code · Moduł 6: Długie rozmowy i limity abonamentu · Lekcja 2 z 4</em>

# Nowa rozmowa czy dalej ta sama

Prowadzisz firmę sprzątającą biura i galerie handlowe. Wczoraj w rozmowie z Claude padło ustalenie: Galeria Pasaż dostaje 8% rabatu za umowę na rok. Dziś chcesz dokończyć ofertę. Zaczynasz nową rozmowę czy wracasz do wczorajszej?

Od tego wyboru zależy, co Claude wie, gdy zaczyna pracę. W zakładce Code każda rozmowa, w aplikacji nazywana sesją, ma własną historię i folder projektu, niezależne od innych rozmów. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja --> Pasek boczny wymienia Twoje rozmowy. <!-- fakt: aplikacja-pasek-boczny-lista-sesji -->

- Nową rozmowę zaczyna przycisk + New (nowa rozmowa) w pasku bocznym. <!-- fakt: aplikacja-nowa-sesja-new-albo-cmd-n -->
- Do starej rozmowy wracasz, gdy klikniesz ją w pasku bocznym. <!-- fakt: aplikacja-powrot-do-sesji-klik-w-pasku-bocznym -->

Obie drogi mają swoją cenę. Gdy przechodzisz do innej pracy, stara rozmowa wypiera pliki potrzebne dalej i kosztuje tokeny przy każdej wiadomości. <!-- fakt: stara-rozmowa-wypiera-pliki-i-kosztuje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Nowa rozmowa zaczyna się za to bez historii poprzednich rozmów. <!-- fakt: sesje-niezalezne-zasady-w-claude-md --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Co znaczy „wypiera” i „tokeny”? Kontekst, czyli miejsce, jakie ma rozmowa, zapełnia się w trakcie pracy. <!-- fakt: claude-code-okno-kontekstu-co-trzyma-zapelnia-sie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Znasz to z lekcji 1. Stara historia zajmuje w nim miejsce, którego potem brakuje na pliki. <!-- fakt: stara-rozmowa-wypiera-pliki-i-kosztuje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Im więcej kontekstu Claude przetwarza, tym więcej tokenów zużywasz. <!-- fakt: koszty-rosna-z-rozmiarem-kontekstu --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Tokeny i zużycie abonamentu wyjaśni lekcja 4.

W ćwiczeniu niżej poprosisz o tę samą ofertę dwa razy: najpierw w nowej rozmowie, potem we wczorajszej. Patrz, czy rabat trafi do oferty.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Nowa rozmowa

<!-- podglad: cw1 nowa -->

1. Nowa rozmowa zaczęła się bez historii innych rozmów. <!-- fakt: sesje-niezalezne-zasady-w-claude-md --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. Rozmowa miała folder Oferty-sprzatanie, więc Claude przeczytał leżące w nim trzy pliki. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja -->
3. Rabatu nie było ani w plikach, ani w tej rozmowie. Claude zapytał więc, jaki rabat wpisać.

#### Stara rozmowa

<!-- podglad: cw1 stara -->

1. Wczorajsza rozmowa otworzyła się po kliknięciu w pasku bocznym. <!-- fakt: aplikacja-powrot-do-sesji-klik-w-pasku-bocznym -->
2. Ustalenie o rabacie było w historii tej rozmowy. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja -->
3. Claude wpisał rabat do oferty: 7 728 zł zamiast 8 400 zł miesięcznie.

<!-- /kolumny -->

## Co rozmowy mają wspólne, a co każda ma osobno

![Rozmowy w tym samym folderze mają osobną historię, ale wspólne pliki i CLAUDE.md. Wczorajsza rozmowa ma w historii ustalenie o rabacie, nowa zaczyna się bez historii innych rozmów. Każda ma własny kontekst i własne zmiany. Wspólne są pliki w folderze Oferty-sprzatanie i CLAUDE.md.](obrazy/co-dziela-rozmowy.png)
<!-- analogia: Dwie rozmowy są jak dwaj pracownicy na zmianach w tym samym biurze. Każdy ma własny notes, ale szafa z dokumentami, czyli folder, i regulamin, czyli CLAUDE.md, są wspólne. -->

Każda rozmowa ma osobno: <!-- fakt: aplikacja-sesja-niezalezna-rozmowa -->

- historię, czyli wszystkie wiadomości i ustalenia, <!-- fakt: aplikacja-kazda-rozmowa-to-sesja -->
- kontekst, czyli miejsce, jakie rozmowa ma na wiadomości, pliki i wyniki (o nim była lekcja 1), <!-- fakt: aplikacja-sesja-wlasny-kontekst-i-zmiany -->
- zmiany w plikach, które Claude zrobił w tej rozmowie. <!-- fakt: aplikacja-sesja-wlasny-kontekst-i-zmiany -->

Rozmowy w tym samym folderze mają wspólne:

- pliki w tym folderze. Każda rozmowa pracuje w folderze, który dla niej wybierasz. Gdy wybierzesz ten sam folder, Claude czyta w niej te same pliki. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja --> <!-- fakt: aplikacja-kontrolka-folderu-obok-selektora -->
- plik CLAUDE.md z Twoimi zasadami. Wczytuje się, zanim cokolwiek napiszesz, więc działa w każdej rozmowie. <!-- fakt: kontekst-na-start-claude-md-mcp-skille --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Nowa rozmowa zaczyna się z czystym kontekstem, bez historii poprzednich rozmów. Zasady, które mają działać zawsze, zapisz więc w CLAUDE.md. <!-- fakt: sesje-niezalezne-zasady-w-claude-md --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Plik CLAUDE.md znasz z modułu 2.

## Jak zacząć nową rozmowę i wrócić do starej

### Nowa rozmowa

Nowa rozmowa przydaje się w dwóch sytuacjach.

- Przechodzisz do innej pracy. Stara rozmowa wypiera wtedy pliki potrzebne do nowego zadania. <!-- fakt: stara-rozmowa-wypiera-pliki-i-kosztuje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Nieaktualny kontekst marnuje też tokeny przy każdej kolejnej wiadomości. <!-- fakt: niezwiazana-praca-nazwij-i-zacznij-od-nowa --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
- Poprawiasz Claude w tej samej sprawie więcej niż dwa razy. Rozmowa jest wtedy zaśmiecona nieudanymi próbami. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Jak zacząć:

1. Kliknij + New w pasku bocznym. Możesz też nacisnąć <kbd>Cmd</kbd>+<kbd>N</kbd> na macOS albo <kbd>Ctrl</kbd>+<kbd>N</kbd> na Windows. <!-- fakt: aplikacja-nowa-sesja-new-albo-cmd-n -->
2. Sprawdź folder w rzędzie pod polem wiadomości. Folder wybierasz przed pierwszą wiadomością. <!-- fakt: aplikacja-rzad-pod-polem-srodowisko-folder-tryb-model --> <!-- fakt: aplikacja-kontrolka-folderu-obok-selektora -->
3. Wpisz zadanie i naciśnij <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie -->

Jeśli pod polem wiadomości nie ma przycisku wyboru środowiska, masz wcześniejszy układ aplikacji. <!-- fakt: aplikacja-wczesniejszy-uklad-brak-selektora --> Ten układ znasz z lekcji 1. W nim folder wybierasz nad polem wiadomości. <!-- fakt: aplikacja-wczesniejszy-uklad-srodowisko-i-folder-nad-polem -->

Nowa rozmowa z lepszym poleceniem prawie zawsze wypada lepiej niż długa rozmowa z nagromadzonymi poprawkami. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Do nowego polecenia dopisz to, czego nauczyły Cię poprawki. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem --> Stara rozmowa nie zajmuje miejsca w nowej, bo nowa zaczyna się z czystym kontekstem. <!-- fakt: sesje-niezalezne-zasady-w-claude-md --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Ustalenie z innej rozmowy wpisz w polecenie albo wróć do tamtej rozmowy. Claude w innej rozmowie może na Twoją prośbę zajrzeć do pozostałych rozmów; tego uczy moduł 9. <!-- fakt: aplikacja-claude-wypisuje-inne-sesje -->

### Powrót do starej rozmowy

Wczorajsze ustalenie o rabacie nie trafiło do żadnego pliku. Jest tylko w historii tamtej rozmowy. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja -->

Claude Code zapisuje rozmowę na komputerze w trakcie pracy. Dzięki temu możesz wrócić tam, gdzie rozmowa się skończyła. <!-- fakt: sesja-zapisana-rozmowa-zwiazana-z-folderem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Jak wrócić:

- Kliknij rozmowę w pasku bocznym. <!-- fakt: aplikacja-powrot-do-sesji-klik-w-pasku-bocznym -->
- Albo naciskaj <kbd>Ctrl</kbd>+<kbd>Tab</kbd> i <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Tab</kbd>. Te skróty przełączają po kolei między rozmowami z paska bocznego. <!-- fakt: aplikacja-ctrl-tab-przelacza-sesje -->

Wracasz do rozmowy razem z jej historią, więc ustalenia masz pod ręką. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja --> Domyślnie Claude Code przechowuje zapis rozmowy bez względu na to, jak jest stary. Dotyczy to rozmowy zaczętej w aplikacji albo ostatnio w niej prowadzonej. <!-- fakt: aplikacja-zapis-rozmowy-bez-limitu-wieku -->

Na co uważać:

- Stara rozmowa ma dalej swój kontekst. <!-- fakt: aplikacja-sesja-wlasny-kontekst-i-zmiany --> Ile miejsca w nim zostało, sprawdzisz tak jak w lekcji 1: w bieżącym układzie na karcie Context. <!-- fakt: aplikacja-karta-context-procent-w-naglowku -->
- Po przerwie dłuższej niż czas przechowywania pamięci podręcznej (cache) pierwsza wiadomość przetwarza od nowa cały kontekst rozmowy. <!-- fakt: pierwsza-wiadomosc-po-przerwie-caly-kontekst --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Co to znaczy dla abonamentu, wyjaśni lekcja 4.

Z czasem lista rozmów w pasku bocznym się wydłuża. <!-- fakt: aplikacja-pasek-boczny-lista-sesji --> W ćwiczeniu niżej nadasz nazwę wczorajszej rozmowie i odłożysz do archiwum starą rozmowę o hotelu Mewa. Po nadaniu nazwy patrz na tytuł rozmowy w pasku tytułu. <!-- fakt: aplikacja-zmiana-nazwy-klik-tytulu --> Przy archiwum patrz na listę rozmów w pasku bocznym. Rozmowa o hotelu Mewa zniknie z niej, a znajdziesz ją w zakładce Archived. <!-- fakt: aplikacja-archiwizacja-z-menu-w-pasku-bocznym --> <!-- fakt: aplikacja-zarchiwizowane-group-and-sort-view-all -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Nazwa

<!-- podglad: cw2 nazwa -->

1. Claude zmienił na Twoją prośbę nazwę wczorajszej rozmowy. <!-- fakt: aplikacja-popros-claude-o-nazwe-lub-archiwum -->
2. Prośba była w dzisiejszej rozmowie. Nową nazwę dostała wczorajsza. <!-- fakt: aplikacja-popros-claude-o-nazwe-lub-archiwum -->
3. Nazwę widać w pasku tytułu, gdy otworzysz tamtą rozmowę. <!-- fakt: aplikacja-zmiana-nazwy-klik-tytulu -->

#### Archiwum

<!-- podglad: cw2 archiwum -->

1. Menu rozmowy w pasku bocznym ma pozycję Archive (archiwizuj). <!-- fakt: aplikacja-archiwizacja-z-menu-w-pasku-bocznym -->
2. Po kliknięciu Archive rozmowa przeszła do zarchiwizowanych i zniknęła z listy. <!-- fakt: aplikacja-archiwizacja-z-menu-w-pasku-bocznym -->
3. Czeka w zakładce Archived (zarchiwizowane). <!-- fakt: aplikacja-zarchiwizowane-group-and-sort-view-all -->

<!-- /kolumny -->

## Nazwa i archiwum: jak to działa

### Nazwa rozmowy

Przy kilku zadaniach naraz nadawaj rozmowom opisowe nazwy. <!-- fakt: sesje-opisowe-nazwy-zeby-odnalezc --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Jak nadać nazwę:

- Otwórz rozmowę i kliknij jej tytuł w pasku tytułu. <!-- fakt: aplikacja-zmiana-nazwy-klik-tytulu -->
- Albo poproś Claude w innej rozmowie, żeby zmienił jej nazwę. <!-- fakt: aplikacja-popros-claude-o-nazwe-lub-archiwum --> Claude zmieni wtedy nazwę tamtej rozmowy, nie tej, w której piszesz. <!-- fakt: aplikacja-claude-widzi-sesje-aplikacji-bez-biezacej -->

Dzięki nazwie pasek tytułu od razu mówi, o czym jest otwarta rozmowa. <!-- fakt: aplikacja-zmiana-nazwy-klik-tytulu -->

Nazwa może mieć najwyżej 200 znaków. Dłuższą Claude Code przytnie. Niewidoczne znaki w nazwie zamieni na spacje. <!-- fakt: nazwa-sesji-do-200-znakow -->

### Archiwum

Rozmowę, której już nie potrzebujesz, odłóż do archiwum: <!-- fakt: aplikacja-archiwizacja-z-menu-w-pasku-bocznym -->

1. Najedź na rozmowę w pasku bocznym.
2. Otwórz jej menu.
3. Wybierz Archive. Rozmowa przejdzie do zarchiwizowanych.

Możesz też poprosić Claude w innej rozmowie, żeby zarchiwizował tę rozmowę. <!-- fakt: aplikacja-popros-claude-o-nazwe-lub-archiwum --> <!-- fakt: aplikacja-claude-widzi-sesje-aplikacji-bez-biezacej --> Wtedy Claude najpierw pokaże kartę zgody. W trybach Auto i Bypass permissions (pomijanie uprawnień) może to zrobić bez niej. <!-- fakt: aplikacja-karta-zgody-przed-archiwizacja --> Tryby pracy i pytania o zgodę znasz z modułu 1.

Zarchiwizowana rozmowa zostaje w aplikacji. <!-- fakt: aplikacja-zarchiwizowane-group-and-sort-view-all --> Zarchiwizowane rozmowy znajdziesz w bieżącym układzie aplikacji tak: <!-- fakt: aplikacja-zarchiwizowane-group-and-sort-view-all -->

1. Najedź na nagłówek listy rozmów w pasku bocznym. Pojawi się ikona Group and sort (grupuj i sortuj).
2. Kliknij ją i wybierz ostatni wiersz menu: View all (pokaż wszystkie).
3. Otwórz zakładkę Archived.

Jeśli pod polem wiadomości nie ma przycisku wyboru środowiska, masz wcześniejszy układ aplikacji. <!-- fakt: aplikacja-wczesniejszy-uklad-brak-selektora --> W nim ikona Filter (filtr) jest widoczna bez najeżdżania. Kliknij ją, wybierz Status, a potem Archived. <!-- fakt: aplikacja-wczesniejszy-uklad-filter-status-archived -->

Dzięki archiwum lista w pasku bocznym pokazuje rozmowy, których potrzebujesz. <!-- fakt: aplikacja-pasek-boczny-lista-sesji --> Odłożona rozmowa czeka w zakładce Archived. <!-- fakt: aplikacja-zarchiwizowane-group-and-sort-view-all -->

## Kiedy zaczynać nową rozmowę, a kiedy nie

![Trzy drogi, gdy rozmowa urosła albo zmieniasz zadanie. Ta sama praca i brakuje miejsca: /compact w tej samej rozmowie. Inna praca albo trzecia poprawka: nowa rozmowa przyciskiem + New. Potrzebujesz ustaleń ze starej rozmowy: wróć do niej, kliknij ją w pasku bocznym. Zasada na stałe idzie do CLAUDE.md.](obrazy/rozmowa-rosnie-trzy-drogi.png)

<!-- kolumny -->

#### Zacznij nową

1. Przechodzisz do innej pracy. Stara rozmowa wypierałaby potrzebne pliki i kosztowała tokeny przy każdej wiadomości. <!-- fakt: stara-rozmowa-wypiera-pliki-i-kosztuje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. To samo poprawiasz więcej niż dwa razy. Zacznij od nowa z lepszym, dokładniejszym poleceniem. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

#### Zostań przy starej

1. Potrzebujesz ustaleń ze starej rozmowy. Wróć do niej: kliknij ją w pasku bocznym. <!-- fakt: aplikacja-powrot-do-sesji-klik-w-pasku-bocznym -->
2. Pracujesz dalej nad tym samym, a brakuje miejsca. Wpisz /compact: streszczenie zwolni miejsce, a Ty zostaniesz w tej samej rozmowie. <!-- fakt: compact-zwalnia-miejsce-w-tej-samej-rozmowie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> <!-- fakt: aplikacja-compact-skraca-rozmowe-wczesniej --> Streszczenie znasz z lekcji 1.

<!-- /kolumny -->

Zasadę, która ma działać w każdej rozmowie, zapisz w pliku CLAUDE.md. <!-- fakt: sesje-niezalezne-zasady-w-claude-md --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

## Źródła

- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Zarządzanie sesjami](https://code.claude.com/docs/en/sessions)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)
- [Okno kontekstu](https://code.claude.com/docs/en/context-window)
- [Dobre praktyki](https://code.claude.com/docs/en/best-practices)
- [Koszty i zużycie](https://code.claude.com/docs/en/costs)
- [Polecenia](https://code.claude.com/docs/en/commands)
- [Folder .claude](https://code.claude.com/docs/en/claude-directory)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
