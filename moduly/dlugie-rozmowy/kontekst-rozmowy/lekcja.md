<em>Przewodnik po Claude Code · Moduł 6: Długie rozmowy i limity abonamentu · Lekcja 1 z 4</em>

# Kontekst: ile jeszcze zmieści rozmowa

Ujednolicasz zapis nazwy produktu w e-booku klienta. Claude czyta dla Ciebie dziesięć długich rozdziałów, a rozmowa rośnie z każdym z nich. <!-- fakt: kontekst-kazdy-przeczytany-plik-dodaje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Wszystko, co Claude czyta i pisze w rozmowie, zajmuje miejsce. To miejsce jest ograniczone i nazywa się kontekstem. Kontekst mieści wszystko, co Claude wie o rozmowie, między innymi:

- Twoje polecenia,
- pliki, które czyta,
- jego odpowiedzi. <!-- fakt: kontekst-okno-miesci-wszystko-o-sesji --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

W zakładce Code każda rozmowa to sesja z własną historią. <!-- fakt: aplikacja-kazda-rozmowa-to-sesja -->

W trakcie pracy kontekst się zapełnia. <!-- fakt: claude-code-okno-kontekstu-co-trzyma-zapelnia-sie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Gdy miejsca brakuje, Claude streszcza rozmowę. Szczegółowe polecenia z początku rozmowy mogą wtedy zniknąć. <!-- fakt: claude-code-przy-limicie-kontekstu-streszcza-rozmowe --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Dlatego warto wiedzieć, ile miejsca zajęła rozmowa.

W bieżącym układzie aplikacji karta Context (kontekst) w panelu obok rozmowy pokazuje to w procentach. <!-- fakt: aplikacja-panel-szczegolow-sesji-karty-obok-czatu --> <!-- fakt: aplikacja-karta-context-procent-w-naglowku -->

W ćwiczeniu niżej Claude przeczyta dziesięć rozdziałów i zapisze listę poprawek. Patrz na procent na karcie Context: najpierw rośnie, a po poleceniu /compact (streść rozmowę) spada. Potem zobaczysz, że Claude dalej pracuje nad tą samą listą.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Na karcie Context

1. Procent urósł, gdy Claude przeczytał rozdziały, bo każdy przeczytany plik dokłada się do kontekstu. <!-- fakt: kontekst-kazdy-przeczytany-plik-dodaje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. Otwarta karta dzieli zajęte miejsce na kategorie. <!-- fakt: aplikacja-karta-context-procent-w-naglowku -->
3. Po poleceniu /compact procent spadł, bo streszczenie zwolniło miejsce. <!-- fakt: aplikacja-compact-skraca-rozmowe-wczesniej --> Liczby w ćwiczeniu są przykładowe.

#### W rozmowie

<!-- podglad: cw1 czytaj-i-streszczaj -->

1. Dymki w ćwiczeniu zostały bez zmian. Polecenie /compact zmieniło to, co Claude ma w kontekście: zastąpiło w nim rozmowę streszczeniem. <!-- fakt: compact-zastepuje-rozmowe-streszczeniem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. Streszczenie zachowuje Twoje prośby, więc Claude dalej pracował nad listą poprawek. <!-- fakt: claude-code-przy-limicie-kontekstu-streszcza-rozmowe --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
3. Listę poprawek Claude zapisał tuż przed streszczeniem. Po streszczeniu Claude Code czyta ponownie do pięciu ostatnio zmienianych plików z tej rozmowy (Claude je czytał albo zmieniał). <!-- fakt: po-streszczeniu-do-pieciu-plikow --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Dlatego lista poprawek wróciła do kontekstu. <!-- fakt: po-streszczeniu-do-pieciu-plikow --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

<!-- /kolumny -->

## Co zajmuje miejsce w rozmowie

![Miejsce w rozmowie zajmują rzeczy wczytane na starcie i wszystko z bieżącej pracy. Pasek ma trzy części: miejsce zajęte od startu, miejsce, które przybywa w trakcie pracy (w tym przykładzie najwięcej zajmują przeczytane pliki), i wolne miejsce. Nad paskiem stoi karta Context z przykładową liczbą.](obrazy/co-zajmuje-miejsce.png)
<!-- wyjasnienie: obrazy/co-zajmuje-miejsce-wyjasnienie.png | Każdy przeczytany plik trafia do plecaka rozmowy obok CLAUDE.md i opisów skilli, a gdy miejsce się kończy, Claude streszcza rozmowę. -->
<!-- analogia: Miejsce w rozmowie działa jak plecak na wycieczkę. Część miejsca zajmują rzeczy spakowane z góry, na przykład CLAUDE.md i opisy skilli. Resztę zajmuje to, co zbierasz po drodze. Gdy plecak się zapełnia, Claude streszcza jego zawartość, żeby zrobić miejsce. -->

Część miejsca jest zajęta, zanim cokolwiek napiszesz. Na starcie do kontekstu wczytują się: <!-- fakt: kontekst-na-start-claude-md-mcp-skille --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

- plik CLAUDE.md z Twoimi zasadami dla Claude (poznasz go w module 2),
- nazwy narzędzi z konektorów (moduł 5), <!-- fakt: aplikacja-konektory-to-serwery-mcp -->
- opisy skilli (moduł 4).

W trakcie pracy dochodzą: <!-- fakt: kontekst-okno-miesci-wszystko-o-sesji --> <!-- fakt: claude-code-okno-kontekstu-co-trzyma-zapelnia-sie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

- Twoje polecenia,
- pliki, które Claude czyta,
- odpowiedzi Claude,
- wyniki poleceń, które Claude uruchamia.

Każdy przeczytany plik dokłada się do kontekstu osobno. <!-- fakt: kontekst-kazdy-przeczytany-plik-dodaje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Dlatego dziesięć długich rozdziałów tak podniosło procent.

Kontekst trzyma też instrukcje systemowe Claude. <!-- fakt: claude-code-okno-kontekstu-co-trzyma-zapelnia-sie -->

### Gdzie sprawdzić, ile miejsca zajęła rozmowa

Zajęte miejsce widzisz na karcie Context, zanim go zabraknie. <!-- fakt: aplikacja-karta-context-procent-w-naglowku --> Dzięki temu możesz streścić rozmowę wcześniej, zanim zrobi to Claude. <!-- fakt: aplikacja-compact-skraca-rozmowe-wczesniej -->

Aplikacja ma dwa układy zakładki Code: bieżący i wcześniejszy. <!-- fakt: aplikacja-karta-context-procent-w-naglowku --> <!-- fakt: aplikacja-wczesniejszy-uklad-pierscien-pokazuje-kontekst --> Jak rozpoznać wcześniejszy, przeczytasz niżej.

- W bieżącym układzie aplikacji procent pokazuje nagłówek karty Context w panelu obok rozmowy. <!-- fakt: aplikacja-karta-context-procent-w-naglowku --> Ten panel nazywa się panelem szczegółów sesji. <!-- fakt: aplikacja-panel-szczegolow-sesji-karty-obok-czatu -->
- Po otwarciu karta pokazuje, co zajmuje miejsce, z podziałem na kategorie. <!-- fakt: aplikacja-karta-context-procent-w-naglowku -->
- Podział na kategorie wypisze w rozmowie także polecenie /context wpisane w pole wiadomości. Działa w obu układach aplikacji. <!-- fakt: aplikacja-context-wypisuje-podzial-okna-kontekstu -->

### Gdy nie widzisz karty Context

Panel szczegółów sesji pojawia się obok rozmowy, gdy jest na niego dość miejsca. <!-- fakt: aplikacja-panel-szczegolow-sesji-karty-obok-czatu --> Jeśli go nie widzisz, pokaż go przyciskiem na pasku tytułu rozmowy albo w menu ⋮ tego paska. <!-- fakt: aplikacja-panel-szczegolow-ukryj-i-pokaz --> Ten przycisk pokazała lekcja 2 modułu 0.

Panelu szczegółów nie ma we wcześniejszym układzie aplikacji. <!-- fakt: aplikacja-wczesniejszy-uklad-nie-ma-panelu-szczegolow --> Ten układ rozpoznasz po rzędzie pod polem wiadomości. W bieżącym układzie pierwszy przycisk w tym rzędzie to przycisk wyboru środowiska, czyli miejsca pracy Claude. <!-- fakt: aplikacja-rzad-pod-polem-srodowisko-folder-tryb-model --> <!-- fakt: aplikacja-selektor-srodowiska-pierwsza-kontrolka --> W ćwiczeniu wyżej ma ikonę laptopa. Jeśli pod polem wiadomości nie ma przycisku wyboru środowiska, masz wcześniejszy układ aplikacji. <!-- fakt: aplikacja-wczesniejszy-uklad-brak-selektora -->

We wcześniejszym układzie kliknij pierścień obok wyboru modelu. Okienko pokaże, ile miejsca zajmuje kontekst. <!-- fakt: aplikacja-wczesniejszy-uklad-pierscien-pokazuje-kontekst --> W bieżącym układzie ten pierścień pokazuje zużycie abonamentu, a we wcześniejszym także kontekst. <!-- fakt: aplikacja-pierscien-zuzycie-abonamentu --> <!-- fakt: aplikacja-wczesniejszy-uklad-pierscien-pokazuje-kontekst -->

### Czego procent nie mówi

- Procent nie mówi nic o innych rozmowach. Dotyczy tylko tej jednej. <!-- fakt: aplikacja-karta-context-procent-w-naglowku -->
- Procent nie mówi, ile zostało z abonamentu. Także ostrzeżenie o kontekście nie jest limitem zużycia. <!-- fakt: kontekst-ostrzezenie-to-nie-limit-zuzycia --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Zużycie abonamentu pokazuje w obu układach pierścień obok wyboru modelu. <!-- fakt: aplikacja-pierscien-zuzycie-abonamentu --> Uczy o nim lekcja 4 tego modułu.
- Kiedy Claude streści rozmowę sam, zależy od modelu i ustawień. <!-- fakt: kontekst-prog-streszczenia-zalezy-od-modelu --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

## Streszczenie: co zostaje, a co może zniknąć

Gdy kontekst się zapełni, Claude sam streszcza rozmowę i pracuje dalej. <!-- fakt: aplikacja-pelny-kontekst-claude-streszcza-i-pracuje-dalej --> Pełny kontekst nie kończy więc rozmowy. <!-- fakt: kontekst-pelne-okno-nie-konczy-sesji --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Polecenie /compact wpisane w pole wiadomości robi to wcześniej i zwalnia miejsce. <!-- fakt: aplikacja-compact-skraca-rozmowe-wczesniej --> Streszczenie zastępuje w kontekście dotychczasową rozmowę. <!-- fakt: compact-zastepuje-rozmowe-streszczeniem --> Dzięki temu historia rozmowy, już w skrócie, mieści się w kontekście. <!-- fakt: streszczenie-miesci-historie-w-oknie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Automatyczne streszczenie działa tak samo jak polecenie /compact. <!-- fakt: streszczenie-automatyczne-jak-compact --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Streszczenie zachowuje Twoje prośby. <!-- fakt: claude-code-przy-limicie-kontekstu-streszcza-rozmowe -->

![Po streszczeniu CLAUDE.md i plan wracają z dysku, ale szczegóły z początku rozmowy mogą zniknąć. W kontekście zostają Twoje prośby w streszczeniu. Wracają CLAUDE.md z głównego folderu, plan, opisy skilli i do pięciu plików, które Claude czytał albo zmieniał.](obrazy/po-streszczeniu.png)
<!-- analogia: Streszczenie działa jak notatka po długim zebraniu. W notatce zostają najważniejsze ustalenia, a regulamin i plan leżą w szafie, więc nic im nie grozi. Drobne ustalenia z pierwszych minut zebrania mogą do notatki nie trafić. -->

Po streszczeniu część rzeczy wraca do kontekstu sama:

- plik CLAUDE.md z głównego folderu wraca z dysku, <!-- fakt: po-streszczeniu-claude-md-wraca-z-dysku --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
- plan, który Claude napisał w trybie planowania, wraca z dysku, <!-- fakt: po-streszczeniu-plan-wraca-z-dysku --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
- opisy skilli są budowane od nowa, <!-- fakt: po-streszczeniu-opisy-skilli-wracaja --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
- do pięciu ostatnio zmienianych plików z tej rozmowy (Claude je czytał albo zmieniał), które Claude Code czyta ponownie. Większy plik wraca jako sama ścieżka, bez treści. <!-- fakt: po-streszczeniu-do-pieciu-plikow --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

### Co zyskujesz

Polecenie /compact zwalnia miejsce, a Ty dalej prowadzisz tę samą rozmowę. <!-- fakt: compact-zwalnia-miejsce-w-tej-samej-rozmowie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Za poleceniem /compact możesz dopisać, na czym streszczenie ma się skupić. Na przykład: /compact zachowaj listę poprawek i termin oddania. Zrób to przed nowym, długim etapem pracy. W streszczeniu zostanie wtedy to, co wybierzesz, a nie to, co za ważne uzna automatyczne streszczenie. <!-- fakt: compact-z-poleceniem-co-zachowac --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

Na streszczenie wpłyniesz też, gdy dodasz do pliku CLAUDE.md część „Compact Instructions” (wskazówki do streszczenia). <!-- fakt: compact-instrukcje-w-claude-md-albo-z-naciskiem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Plik CLAUDE.md poznasz w module 2.

### Na co uważać

- Szczegółowe polecenia z początku rozmowy mogą w streszczeniu zniknąć. Zasady, które mają działać zawsze, zapisz w CLAUDE.md, a nie tylko w rozmowie. <!-- fakt: claude-code-przy-limicie-kontekstu-streszcza-rozmowe --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
- Polecenie /compact czyta całą rozmowę, którą streszcza. Streszczenie dużej rozmowy samo jest więc dużym zapytaniem. <!-- fakt: streszczenie-samo-jest-duzym-zadaniem --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> O tym, ile kosztuje duże zapytanie, mówi lekcja 4 tego modułu.

Czasem w środku pracy chcesz tylko coś sprawdzić, ale nie chcesz dokładać pytania do rozmowy. Służy do tego pytanie z boku: polecenie /btw otwiera osobny panel pytania z boku. <!-- fakt: aplikacja-btw-otwiera-boczna-rozmowe --> <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy --> W ćwiczeniu niżej zadasz takie pytanie. Po zamknięciu tego panelu zobaczysz, że w głównej rozmowie nie ma ani pytania, ani odpowiedzi.

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### W głównej rozmowie

<!-- podglad: cw2 z-boku -->

1. Nie ma w niej ani pytania, ani odpowiedzi. Nic z pytania z boku nie wróciło do głównej rozmowy. <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy -->
2. Po zamknięciu panelu pytania z boku rozmowa toczy się dalej od tego samego miejsca. <!-- fakt: aplikacja-pytanie-z-boku-zamknij-i-wracasz -->
3. Termin trafił do listy poprawek dopiero po zwykłej prośbie w głównej rozmowie.

#### W panelu pytania z boku

1. Polecenie /btw otworzyło pytanie z boku. <!-- fakt: aplikacja-btw-otwiera-boczna-rozmowe -->
2. Pytanie z boku może czytać wszystko z głównej rozmowy do tej chwili. <!-- fakt: aplikacja-btw-otwiera-boczna-rozmowe -->
3. Claude odpowiedział z tego, co już było w rozmowie. <!-- fakt: aplikacja-btw-otwiera-boczna-rozmowe -->

<!-- /kolumny -->

### Po co jest pytanie z boku

Pytanie z boku przydaje się w środku zadania. Pytaniem z boku coś sprawdzisz albo dopytasz o to, czego nie rozumiesz, a główna rozmowa nie zboczy z tematu. <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy --> Pytanie z boku korzysta z kontekstu rozmowy. <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy --> Ani pytanie, ani odpowiedź nie trafiają jednak do historii rozmowy. <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy -->

### Jak otworzyć pytanie z boku

Masz trzy sposoby: <!-- fakt: aplikacja-btw-otwiera-boczna-rozmowe -->

- wpisz /btw w polu wiadomości, tak jak w ćwiczeniu,
- na macOS naciśnij <kbd>Cmd</kbd>+<kbd>;</kbd>,
- na Windows naciśnij <kbd>Ctrl</kbd>+<kbd>;</kbd>.

Gdy skończysz, zamknij pytanie z boku i prowadź główną rozmowę dalej. <!-- fakt: aplikacja-pytanie-z-boku-zamknij-i-wracasz -->

### Czego pytanie z boku nie robi

- Aplikacja nie zapisuje pytań z boku na dysku. Po zamknięciu aplikacji do pytania nie wrócisz. <!-- fakt: aplikacja-pytanie-z-boku-nie-zapisuje-sie-na-dysku -->
- W tym kursie pracujesz w sesji lokalnej (This computer), a w niej pytanie z boku działa. <!-- fakt: aplikacja-pytanie-z-boku-nie-zapisuje-sie-na-dysku -->

## Kiedy streszczać rozmowę, a kiedy nie

<!-- kolumny -->

#### Streszczaj

1. Pracujesz dalej nad tym samym, a miejsca jest mało. Polecenie /compact zwolni miejsce w tej samej rozmowie. <!-- fakt: compact-zwalnia-miejsce-w-tej-samej-rozmowie --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. Zaczynasz długi nowy etap tej samej pracy. Dopisz za /compact, co ma zostać w streszczeniu. <!-- fakt: compact-z-poleceniem-co-zachowac --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

#### Nie streszczaj

1. Przechodzisz do innej pracy. Stara rozmowa wypiera wtedy z kontekstu pliki potrzebne do nowej pracy i kosztuje przy każdej wiadomości. <!-- fakt: stara-rozmowa-wypiera-pliki-i-kosztuje --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Zacznij nową rozmowę. Jak to zrobić, pokaże lekcja 2.
2. Zasada ma działać zawsze. Zapisz ją w CLAUDE.md, bo polecenia z początku rozmowy mogą zniknąć. <!-- fakt: claude-code-przy-limicie-kontekstu-streszcza-rozmowe --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
3. Chcesz o coś zapytać, ale tak, żeby pytanie nie zostało w rozmowie. Zadaj je z boku. <!-- fakt: aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy -->
4. Claude ma przejrzeć wiele dużych plików. Zleć to subagentowi, czyli pomocnikowi Claude: zbiera informacje we własnym, osobnym kontekście, więc duże czytanie plików nie trafia do Twojego kontekstu. <!-- fakt: subagent-zbiera-w-osobnym-oknie-kontekstu --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Subagentów uczy moduł 9.

<!-- /kolumny -->

## Źródła

- [Okno kontekstu](https://code.claude.com/docs/en/context-window)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Pierwsze kroki w aplikacji](https://code.claude.com/docs/en/desktop-quickstart)
- [Polecenia](https://code.claude.com/docs/en/commands)
- [Koszty i zużycie](https://code.claude.com/docs/en/costs)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
