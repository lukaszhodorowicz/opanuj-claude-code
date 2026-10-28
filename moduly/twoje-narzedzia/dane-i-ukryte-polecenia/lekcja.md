<em>Przewodnik po Claude Code · Moduł 5: Claude w Twoich narzędziach · Lekcja 4 z 4</em>

# Dane klientów i polecenia ukryte w cudzych tekstach

Prowadzisz agencję marketingową dla małych firm. W folderze Agencja-nowi-klienci leżą:

- lista klientów z ich adresami e-mail,
- cennik agencji,
- zapytania od nowych firm.

Przy tej pracy Claude czyta dużo cudzych tekstów:

- zapytania od nieznanych firm,
- maile,
- strony internetowe innych firm.

Konektor poczty masz już podłączony, tak jak kalendarz w lekcji 1. Po podłączeniu konektora Claude może wysyłać wiadomości. <!-- fakt: aplikacja-konektor-czyta-kalendarz-wysyla-wiadomosci -->

Lista klientów to cudze dane, za które odpowiadasz. Dlatego zanim dasz Claude zapytanie od obcej firmy, warto znać odpowiedzi na dwa pytania:

1. Co z Twojej rozmowy z Claude wychodzi poza komputer, dokąd trafia i jak długo tam zostaje?
2. Czy obcy tekst może kazać Claude zrobić coś z listą Twoich klientów?

Odpowiedź na pierwsze pytanie: Claude Code działa na Twoim komputerze, ale żeby korzystać z modelu, wysyła dane przez sieć. <!-- fakt: dane-prompty-i-odpowiedzi-szyfrowane-w-drodze --> W aplikacji rozmowa z sesji na Twoim komputerze trafia domyślnie do API Anthropic. <!-- fakt: aplikacja-sesje-lokalne-wysylaja-rozmowe-do-dostawcy-modelu --> Jak długo tam zostaje, zależy od planu i od jednego ustawienia. <!-- fakt: dane-przechowywanie-konta-konsumenckie-5-lat-albo-30-dni --> Pokazuje to rysunek, a szczegóły są niżej.

![Rozmowa trafia domyślnie do Anthropic, a jak długo tam zostaje, zależy od planu i ustawienia. Na planach Pro i Max dane zostają 5 lat albo 30 dni zależnie od ustawienia ulepszania modeli, a na planach Team i Enterprise standardowo 30 dni. Na Twoim komputerze zostaje zapis rozmów zwykłym tekstem.](obrazy/dokad-idzie-rozmowa.png)
<!-- analogia: Rozmowa jest jak list, który jedzie w zaklejonej kopercie i trafia do archiwum. Na planach Pro i Max archiwum trzyma go 5 lat, gdy pozwolisz się na nim uczyć, a 30 dni, gdy nie pozwolisz. Na planach Team i Enterprise trzyma go standardowo 30 dni. -->

Odpowiedź na drugie pytanie brzmi: tak. Ktoś obcy może wstawić do swojego tekstu zdanie, które próbuje zmienić instrukcje Claude albo nimi pokierować. <!-- fakt: ukryte-polecenie-definicja --> Dokumentacja nazywa to prompt injection (wstrzyknięcie polecenia). <!-- fakt: ukryte-polecenie-definicja --> W tej lekcji mówimy prościej: ukryte polecenie. Ukryte, bo stoi w cudzym tekście, między zwykłymi zdaniami.

W ćwiczeniu niżej zobaczysz zapytanie od nowej firmy. Stoi w nim zdanie napisane do Claude i wymierzone w Twoją listę klientów. Raz Claude je zauważy, a raz da się złapać. Gdy da się złapać, przeczyta listę bez pytania, ale wysyłka zaczeka na Twoją zgodę. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Claude zauważa polecenie

<!-- podglad: cw1 zauwaza -->

1. Claude bez pytania przeczytał zapytanie, bo w trybie Manual (ręczny) bez pytania idą tylko odczyty. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
2. Claude przytoczył zdanie napisane do niego i go nie wykonał.
3. Streszczenie pokazał na karcie zgody. Do pliku trafiło dopiero po zatwierdzeniu. <!-- fakt: aplikacja-manual-podglad-i-przyciski --> <!-- fakt: tryb-manual-aplikacja-czeka-na-zatwierdzenie -->

#### Claude daje się złapać

<!-- podglad: cw1 daje-sie-zlapac -->

1. Claude bez pytania przeczytał zapytanie i listę klientów. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
2. Chciał wysłać listę przez konektor poczty na adres podany w cudzym tekście.
3. Wysyłka czekała na Twoją zgodę, bo nie jest odczytem. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien -->

<!-- /kolumny -->

Prośba była za każdym razem ta sama. Dokumentacja nie mówi, czy Claude rozpozna ukryte polecenie, czy je wykona. Dlatego obie odpowiedzi w ćwiczeniu to tylko przykłady.

W pierwszej drodze liczby +1 -1 na karcie Changes (zmiany) pokazały, że w pliku streszczeń jedna linijka doszła, a jedna ubyła. <!-- fakt: aplikacja-widok-zmian-liczby-na-karcie-changes --> Tę zmianę przeczytasz na karcie zgody, zanim ją zatwierdzisz. <!-- fakt: aplikacja-manual-podglad-i-przyciski -->

Zwróć uwagę na drugą drogę. Tryb Manual nie zatrzymał odczytu listy klientów. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> Zapora stoi przed większością działań, które zmieniają pliki albo sięgają do sieci, na przykład przed wysyłką. <!-- fakt: tryb-manual-pyta-przed-akcjami -->

Wśród zabezpieczeń przed ukrytymi poleceniami dokumentacja wymienia system uprawnień. W trybie Manual działania wrażliwe wymagają Twojej wyraźnej zgody. <!-- fakt: manual-wrazliwe-dzialania-wymagaja-zgody --> Większość narzędzi, które wysyłają zapytania do sieci, domyślnie też czeka w tym trybie na zgodę. <!-- fakt: manual-zadania-sieciowe-wymagaja-zgody --> W rozmowie na Twoim komputerze aplikacja stosuje do narzędzi konektora zwykłe reguły uprawnień sesji. <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien --> Dla konektora poczty obowiązują więc te same zasady zgody co w całej rozmowie. <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien -->

Zasad uprawnień pilnuje program Claude Code, nie model. <!-- fakt: uprawnienia-egzekwuje-program-nie-model --> Model to sztuczna inteligencja, która pisze odpowiedzi. Program to Claude Code na Twoim komputerze. <!-- fakt: dane-prompty-i-odpowiedzi-szyfrowane-w-drodze --> W drugiej drodze model chciał wysłać listę, a program i tak zatrzymał wysyłkę przed Twoją zgodą. <!-- fakt: manual-zadania-sieciowe-wymagaja-zgody -->

W ćwiczeniu Claude pisze, że czeka na Twoją zgodę na wysyłkę. W prawdziwej aplikacji w tym miejscu program zapyta Cię o zgodę. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien --> W ćwiczeniu zamiast tego pytania widzisz odpowiedź Claude, bo dokumentacja nie opisuje, jak ono wygląda. Gdy adres podał cudzy tekst, a nie Ty, odmów.

## Polecenie ukryte w cudzym tekście

Przypomnienie: ukryte polecenie to zdanie, które ktoś obcy wstawia do swojego tekstu. <!-- fakt: ukryte-polecenie-definicja --> W ćwiczeniu takie zdanie kazało wysłać listę klientów na obcy adres.

### Skąd przychodzi cudzy tekst

Cudzy tekst trafia do Claude różnymi drogami:

- z pliku w folderze, na przykład z zapytania zapisanego z maila, <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
- z konektora, który pobiera treści z zewnątrz, na przykład z konektora poczty, <!-- fakt: konektor-tresci-z-zewnatrz-ryzyko-wstrzykniecia -->
- z cudzej strony, którą Claude czyta w aplikacji. <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach -->

Claude czyta cudzy tekst tak samo jak Twoje pliki. W trybach Manual i Accept edits (przyjmowanie zmian) odczyt pliku w folderze idzie bez pytania. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: accept-edits-odczyty-bez-pytania --> Dlatego zapory stoją dopiero przed tym, co Claude chce zrobić.

### Trzy zapory, zanim coś wyjdzie z komputera

**Zapora 1: tryb Manual.** W tym trybie Claude Code zatrzymuje się i pyta przed większością działań, które:

- zmieniają pliki,
- uruchamiają polecenia systemowe,
- sięgają do sieci. <!-- fakt: tryb-manual-pyta-przed-akcjami -->

Działania wrażliwe wymagają Twojej wyraźnej zgody. <!-- fakt: manual-wrazliwe-dzialania-wymagaja-zgody --> Tę zaporę widać w drugiej drodze ćwiczenia 1.

**Zapora 2: strażnik w trybie Auto.** W trybie Auto (automatyczny) strażnik, czyli osobny model AI (klasyfikator), ocenia działania, zanim się wykonają. <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem --> Strażnik domyślnie blokuje między innymi:

- działania, które wyglądają na wywołane wrogą treścią przeczytaną przez Claude, <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem -->
- wysyłanie wrażliwych danych na zewnętrzne adresy. <!-- fakt: auto-blokuje-wysylanie-danych -->

Strażnik nie dostaje wyników narzędzi, czyli na przykład treści przeczytanego pliku albo strony. Dlatego wroga treść z pliku albo ze strony nie może nim sterować wprost. <!-- fakt: auto-klasyfikator-widzi-wiadomosci-nie-wyniki -->

Dokumentacja opisuje te zasady strażnika dla Claude Code. Aplikacja na komputer działa na tym samym silniku. <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> W aplikacji w trybie Auto, zanim Claude sięgnie do sieci, strażnik w tle sprawdza, czy to działanie zgadza się z Twoją prośbą. <!-- fakt: auto-aplikacja-opis-trybu --> Ćwiczenie tej zapory nie pokazuje. Zobaczysz ją na rysunku pod ćwiczeniem 2.

**Zapora 3: karta zgody na cudzej stronie.** Gdy Claude pierwszy raz działa na cudzej stronie, pojawia się karta zgody, a Claude czeka na Twój wybór. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> Tę zaporę przećwiczysz w ćwiczeniu 2.

### Co Cię chroni przed ukrytym poleceniem

W trybie Manual większość wysyłek domyślnie czeka na Twoją zgodę, a w trybie Auto ocenia je strażnik. <!-- fakt: manual-zadania-sieciowe-wymagaja-zgody --> <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem --> Nawet gdy Claude da się złapać, jak w drugiej drodze ćwiczenia 1, wysyłka w trybie Manual czeka na Twoją decyzję. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien -->

### Czego zapory nie załatwią

Te zabezpieczenia znacznie zmniejszają ryzyko, ale żaden system nie jest całkowicie odporny na wszystkie ataki. <!-- fakt: zadna-ochrona-nie-jest-pelna --> Dlatego:

- Tryb Auto zmniejsza liczbę pytań o zgodę, ale nie gwarantuje bezpieczeństwa. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->
- Tryb Bypass permissions (pomijanie uprawnień) nie chroni przed ukrytymi poleceniami. <!-- fakt: bypass-bez-ochrony-przed-wstrzyknieciem -->
- Za sprawdzenie proponowanych zmian i poleceń, zanim się na nie zgodzisz, odpowiadasz Ty. <!-- fakt: uzytkownik-przeglada-przed-zgoda --> Zgoda chroni Cię tylko wtedy, gdy czytasz, o co Claude prosi.

W drugim ćwiczeniu Claude czyta cudzą stronę w panelu Browser (przeglądarka), który znasz z lekcji 3. <!-- fakt: aplikacja-browser-karty-dowolna-strona --> Zobaczysz, że zdanie na stronie drukarni może kazać Claude zanieść Twoją listę klientów na inną stronę. Ta strona dostaje własną kartę zgody, także w trybie Accept edits. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona --> Przycisk Deny (odmów) zatrzymuje Claude, zanim cokolwiek z folderu tam trafi. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Drukarnia Kolor: Allow once

1. Zanim Claude wszedł na stronę drukarni, pojawiła się karta zgody, a Claude czekał. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone --> <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona -->
2. Tę stronę wskazała Twoja prośba, więc wybór Allow once (zezwól raz) był w porządku. Allow once zezwala na to jedno działanie i niczego nie zapisuje. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu -->
3. W opisie strony stało zdanie napisane do Claude. Claude bez pytania przeczytał też listę klientów, bo w trybie Accept edits odczyty nie czekają na zgodę. <!-- fakt: accept-edits-odczyty-bez-pytania -->

#### Rabaty-Druk: Deny

<!-- podglad: cw2 odmow -->

1. Claude chciał wejść na stronę Rabaty-Druk, którą wskazało zdanie z opisu drukarni.
2. Nowa strona dostała własną kartę zgody, choć był włączony tryb Accept edits. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona -->
3. Po Deny Claude nie wszedł na tę stronę. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> Ceny zapisał w nowym pliku bez pytania. <!-- fakt: claude-code-tworzy-nowe-pliki --> <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania -->

<!-- /kolumny -->

Każda strona potrzebuje osobnej zgody, także subdomeny. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> Dlatego zgoda dla drukarni nie objęła strony Rabaty-Druk, choć prowadziło do niej zdanie z opisu drukarni. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> Subdomena to adres z dodatkowym członem przed nazwą strony, na przykład `sklep.kolor.example`.

Na cudzych stronach strażnik sprawdza też działania, które coś na stronie robią, na przykład klikanie i pisanie. Robi to w każdym trybie uprawnień. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> Gdy oflaguje (oznaczy jako ryzykowne) takie działanie, dostajesz pytanie o zgodę bez względu na tryb. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> To pytanie pojawia się nawet w trybie Bypass permissions, który poza wyjątkami nie pyta o zgodę. <!-- fakt: aplikacja-bypass-pyta-przy-dzialaniu-na-cudzych-stronach -->

Słowa Claude po odmowie to też przykład.

Rysunek zbiera trzy zapory na jednej drodze ukrytego polecenia. Ćwiczenia pokazały zaporę Manual i kartę zgody na cudzej stronie, a rysunek dokłada strażnika w trybie Auto.

![Przed ukrytym poleceniem stoją trzy zapory, ale żadna nie daje pewności. Cudzy tekst z pliku, maila albo strony zawiera zdanie napisane do Claude. Zanim coś wyjdzie z komputera, stoją trzy zapory: w trybie Manual Twoja zgoda, w trybie Auto strażnik, a na cudzej stronie osobna karta zgody przy pierwszym działaniu. W trybie Manual i na cudzej stronie na końcu decydujesz Ty, a w trybie Auto strażnik.](obrazy/trzy-zapory.png)
<!-- wyjasnienie: obrazy/trzy-zapory-wyjasnienie.png | Claude czyta zapytanie z ukrytym zdaniem bez pytania, a zapora stoi przed wysyłką: w Manual odmawiasz Ty, w Auto blokuje strażnik. -->

## Co z rozmowy wychodzi z komputera i jak długo zostaje

Rysunek na początku lekcji pokazuje, dokąd trafia rozmowa i jak długo tam zostaje. Tu są szczegóły, także o tym, czego rysunek nie pokazuje: o metrykach, raportach błędów, ankiecie i Remote Control.

### Co wychodzi z komputera

- Claude Code wysyła przez sieć wszystkie Twoje prompty (prośby do Claude) i wszystkie odpowiedzi modelu. W drodze są szyfrowane. <!-- fakt: dane-prompty-i-odpowiedzi-szyfrowane-w-drodze --> Szyfrowanie zamienia dane w kod, którego bez klucza nie da się przeczytać.
- W aplikacji sesja na Twoim komputerze wysyła rozmowę i kontekst do dostawcy modelu, domyślnie do API Anthropic. <!-- fakt: aplikacja-sesje-lokalne-wysylaja-rozmowe-do-dostawcy-modelu --> API Anthropic to wejście, przez które programy łączą się z modelami Anthropic.
- U tego dostawcy dane zapisane na serwerach chroni szyfrowanie dysków. <!-- fakt: dane-api-anthropic-szyfrowanie-dyskow -->

### Jak długo zostaje u Anthropic

Claude Code wymaga płatnego planu:

- Pro,
- Max,
- Team,
- Enterprise. <!-- fakt: plan-platny -->

Od planu zależy, co dzieje się z Twoimi danymi.

Na planach Pro i Max:

- To Ty wybierasz, czy Twoje dane posłużą do ulepszania przyszłych modeli Claude. <!-- fakt: dane-trening-konta-konsumenckie-za-zgoda -->
- Gdy ustawienie ulepszania modeli jest włączone, Anthropic trenuje (uczy) nowe modele na Twoich danych, także z Claude Code. <!-- fakt: dane-trening-konta-konsumenckie-za-zgoda -->
- Przy włączonym ustawieniu dane zostają 5 lat. <!-- fakt: dane-przechowywanie-konta-konsumenckie-5-lat-albo-30-dni -->
- Przy wyłączonym zostają 30 dni. <!-- fakt: dane-przechowywanie-konta-konsumenckie-5-lat-albo-30-dni -->

Na planach Team i Enterprise:

- Anthropic nie trenuje modeli na kodzie ani na promptach wysłanych do Claude Code. Wyjątek: gdy firma sama zgodzi się udostępnić dane. <!-- fakt: dane-konta-firmowe-bez-treningu -->
- Standardowo dane zostają 30 dni. <!-- fakt: dane-konta-firmowe-30-dni -->

### Co zostaje na Twoim komputerze

Claude Code zapisuje przebieg rozmów na Twoim komputerze zwykłym tekstem, bez szyfrowania, domyślnie na 30 dni. Dzięki temu da się wrócić do rozmowy. <!-- fakt: dane-zapis-rozmow-na-komputerze-30-dni --> Zapis rozmów z aplikacji Claude na komputer też leży zwykłym tekstem, ale domyślnie nie znika po 30 dniach. <!-- fakt: dane-zapis-rozmow-na-komputerze-30-dni --> <!-- fakt: aplikacja-zapis-rozmow-bez-limitu-30-dni -->

### Metryki i raporty błędów

Osobno od rozmowy Claude Code wysyła dwa rodzaje danych o samym programie: metryki i raporty błędów.

**Metryki** to:

- opóźnienia,
- niezawodność,
- sposób używania.

Trafiają do Anthropic i do zewnętrznej usługi zapisu logów. Nigdy nie zawierają Twojego kodu, promptów ani ścieżek plików. <!-- fakt: dane-metryki-bez-tresci -->

**Raporty błędów** samego Claude Code trafiają do zewnętrznej usługi śledzenia błędów. Zanim cokolwiek opuści komputer, Claude Code usuwa z nich:

- znane wzorce sekretów,
- ścieżki plików,
- adresy e-mail,
- inne dane osobowe. <!-- fakt: dane-raporty-bledow-bez-danych-osobowych -->

Raporty błędów są włączone tylko wtedy, gdy spełnionych jest kilka warunków naraz. Jeden z nich: logujesz się kontem z planem Pro albo Max. <!-- fakt: dane-raporty-bledow-wlaczone-pro-max -->

### Ankieta i polecenie /feedback

Ankieta po ocenie rozmowy w Claude Code wysyła przebieg rozmowy z treścią plików tylko po odpowiedzi „Yes”; Anthropic trzyma go do 6 miesięcy. <!-- fakt: dane-ankieta-tak-wysyla-przebieg-rozmowy --> Polecenie /feedback w Claude Code wysyła do Anthropic kopię historii rozmowy razem z kodem, a Anthropic trzyma ją 5 lat. <!-- fakt: dane-feedback-wysyla-historie-z-kodem-5-lat -->

### Remote Control

Gdy Remote Control (zdalne sterowanie) połączy rozmowę z aplikacji, zobaczysz ją też na innych urządzeniach. <!-- fakt: aplikacja-remote-control-rozmowa-na-innych-urzadzeniach --> Dopóki jest połączona, jej przebieg jest też przechowywany na serwerach Anthropic. <!-- fakt: remote-control-zapis-rozmowy-na-serwerach-anthropic --> Remote Control poznasz w module 8.

### Co możesz ustawić

Ustawienia prywatności zmienisz w każdej chwili na stronie claude.ai/settings/data-privacy-controls. <!-- fakt: dane-ustawienia-prywatnosci-w-kazdej-chwili --> Wśród zabezpieczeń danych Anthropic wymienia też ograniczony czas przechowywania informacji wrażliwych i ograniczony dostęp do danych sesji. <!-- fakt: dane-ograniczony-czas-i-dostep -->

### Czego ta lekcja nie obejmuje

- Ta lekcja nie zastępuje regulaminu. Pełne zasady opisują Polityka prywatności Anthropic oraz Warunki dla konsumentów (Pro, Max) albo Warunki handlowe (Team, Enterprise). <!-- fakt: dane-pelne-zasady-w-regulaminach -->
- Dokumentacja Claude Code nie opisuje, co z rozmowy dostaje dostawca konektora (na przykład firma, która obsługuje Twoją pocztę) ani jak długo to przechowuje.

## Zanim podłączysz konektor albo dasz Claude cudzy tekst

Konektor poczty wnosi do rozmowy maile od obcych ludzi. Zanim podłączysz konektor, sprawdź, czy ufasz jego dostawcy. Konektory, które pobierają treści z zewnątrz, mogą narazić Cię na ukryte polecenia. <!-- fakt: konektor-tresci-z-zewnatrz-ryzyko-wstrzykniecia -->

Dokumentacja radzi wybierać konektory od dostawców, którym ufasz. <!-- fakt: katalog-konektorow-przeglad-bez-audytu --> Anthropic sprawdza konektory według swoich kryteriów, zanim doda je do katalogu. Nie robi jednak audytu, czyli sprawdzenia, czy któryś z nich jest bezpieczny. <!-- fakt: katalog-konektorow-przeglad-bez-audytu --> Konektor z katalogu nie musi więc być bezpieczny.

Przy pracy z niesprawdzonymi treściami dokumentacja radzi między innymi: <!-- fakt: rady-praca-z-niesprawdzonymi-tresciami -->

- czytać polecenia, które proponuje Claude, zanim się na nie zgodzisz,
- nie przesyłać niesprawdzonych treści wprost do Claude,
- sprawdzać proponowane zmiany w ważnych plikach, tak jak streszczenie na karcie zgody w ćwiczeniu 1.

Słowo „wprost” w drugiej radzie znaczy: zanim tę treść przejrzysz.

## Jak to zrobić u siebie

1. Wejdź na stronę claude.ai/settings/data-privacy-controls i sprawdź ustawienie ulepszania modeli. Zmienisz je w każdej chwili. <!-- fakt: dane-ustawienia-prywatnosci-w-kazdej-chwili -->
2. Zanim dasz Claude cudze teksty, wybierz Manual w przełączniku trybu pod polem wiadomości. <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci --> Wtedy działania wrażliwe czekają na Twoją zgodę. <!-- fakt: manual-wrazliwe-dzialania-wymagaja-zgody -->
3. Gdy Claude prosi o zgodę, sprawdź proponowane zmiany i polecenia, zanim się na nie zgodzisz. <!-- fakt: uzytkownik-przeglada-przed-zgoda --> <!-- fakt: rady-praca-z-niesprawdzonymi-tresciami -->
4. Na karcie zgody przy cudzej stronie kliknij Deny, gdy tej strony nie wskazała Twoja prośba. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony -->
5. Podłączaj tylko taki konektor poczty, którego dostawcy ufasz. <!-- fakt: konektor-tresci-z-zewnatrz-ryzyko-wstrzykniecia --> <!-- fakt: katalog-konektorow-przeglad-bez-audytu -->

## Kiedy włączać tryb Manual przy cudzych treściach, a kiedy nie

<!-- kolumny -->

#### Włącz Manual

- Gdy Claude ma czytać zapytania i maile od obcych albo cudze strony, a w folderze leżą dane klientów. Wysyłka i większość innych zapytań do sieci czeka wtedy na Twoją zgodę. <!-- fakt: manual-zadania-sieciowe-wymagaja-zgody --> <!-- fakt: manual-wrazliwe-dzialania-wymagaja-zgody --> <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
- Gdy chcesz widzieć każdą zmianę pliku, zanim się zapisze. <!-- fakt: aplikacja-manual-podglad-i-przyciski -->
- Pamiętaj, że Manual nie zatrzyma odczytu plików w folderze. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->

#### Wystarczy inny tryb

- Gdy pracujesz na własnych plikach, bez cudzych tekstów. Accept edits przyspieszy pracę. <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania -->
- Na cudzych stronach karta zgody i strażnik działają także w trybie Accept edits. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona --> <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie -->
- Tryb Auto nie gwarantuje bezpieczeństwa, choć strażnik blokuje działania, które wyglądają na wywołane wrogą treścią. <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem --> <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->

<!-- /kolumny -->

Przy cudzych treściach nie włączaj trybu Bypass permissions. Ten tryb nie chroni przed ukrytymi poleceniami. <!-- fakt: bypass-bez-ochrony-przed-wstrzyknieciem -->

## Źródła

- [Wykorzystanie danych](https://code.claude.com/docs/en/data-usage)
- [Bezpieczeństwo](https://code.claude.com/docs/en/security)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Łączenie Claude Code z narzędziami przez MCP](https://code.claude.com/docs/en/mcp)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Konfiguracja uprawnień](https://code.claude.com/docs/en/permissions)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
