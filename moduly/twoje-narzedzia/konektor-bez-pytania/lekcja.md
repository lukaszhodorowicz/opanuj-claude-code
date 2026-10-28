<em>Przewodnik po Claude Code · Moduł 5: Claude w Twoich narzędziach · Lekcja 2 z 4</em>

# Co konektor zrobi bez pytania

Prowadzisz firmę cateringową, która wozi lunche na spotkania w biurach. Konektor poczty masz już podłączony, tak jak kalendarz w lekcji 1.

Konektor nie tylko czyta. Po podłączeniu konektora Claude może czytać Twój kalendarz i wysyłać wiadomości. <!-- fakt: aplikacja-konektor-czyta-kalendarz-wysyla-wiadomosci --> W tej lekcji chodzi o wysyłanie wiadomości przez konektor poczty.

Prosisz więc Claude o dwie rzeczy naraz. Ma wpisać termin degustacji do pliku z zamówieniem klientki i wysłać jej wiadomość z tym terminem. Czy Claude najpierw Cię zapyta, czy wyśle wiadomość sam? Wiadomość do klientki zwykle chcesz przeczytać, zanim wyjdzie.

O tym, co Claude robi bez pytania, decyduje tryb uprawnień. <!-- fakt: tryb-uprawnien-ustala-co-bez-pytania --> Konektor ma narzędzia, czyli działania, które Claude może w nim wykonać, na przykład wysłać wiadomość. <!-- fakt: konektor-organizacja-ustawia-zasady-narzedzi --> <!-- fakt: aplikacja-konektor-czyta-kalendarz-wysyla-wiadomosci -->

Wysłanie wiadomości przez konektor nie jest ani odczytem, ani zmianą pliku. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: accept-edits-odczyty-bez-pytania --> Dlatego z trzech trybów niżej bez pytania przepuszcza je tylko tryb Auto. <!-- fakt: tryb-auto-bez-pytania-wszystko-z-kontrola-w-tle -->

Wyślij tę samą prośbę w trzech trybach. Zobaczysz, że Claude zatrzymuje się:

- w trybie Manual (ręczny) dwa razy: przy pliku i przy wiadomości, <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
- w trybie Accept edits (przyjmowanie zmian) raz: przy wiadomości, <!-- fakt: accept-edits-odczyty-bez-pytania -->
- w trybie Auto (automatyczny) wcale, bo wysyłkę ocenia strażnik (osobny model AI) zamiast Ciebie. <!-- fakt: auto-kolejnosc-reszta-do-klasyfikatora --> <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Manual

<!-- podglad: cw1 manual -->

1. Claude przeczytał zamówienie bez pytania, bo w tym trybie bez pytania idą tylko odczyty. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->
2. Zmianę pliku pokazał na karcie zgody i czekał, aż ją przyjmiesz. <!-- fakt: aplikacja-manual-podglad-i-przyciski -->
3. Przed wysłaniem wiadomości zatrzymał się drugi raz. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt -->

#### Accept edits

<!-- podglad: cw1 accept-edits -->

1. Claude przeczytał zamówienie i wpisał termin bez pytania. <!-- fakt: accept-edits-odczyty-bez-pytania -->
2. Liczby +1 -1 na karcie Changes (zmiany) pokazały zmianę w pliku. <!-- fakt: aplikacja-widok-zmian-liczby-na-karcie-changes -->
3. Zatrzymał się dopiero przed wysłaniem wiadomości. <!-- fakt: accept-edits-odczyty-bez-pytania -->

#### Auto

<!-- podglad: cw1 auto -->

1. Claude przeczytał i zmienił zamówienie bez oceny strażnika. <!-- fakt: auto-odczyty-i-zmiany-w-folderze-bez-klasyfikatora -->
2. Wysyłka trafiła do strażnika. <!-- fakt: auto-kolejnosc-reszta-do-klasyfikatora --> Strażnik sprawdza, czy działanie nie wykracza poza Twoją prośbę. <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem -->
3. Tym razem wysyłkę przepuścił, więc Claude o nic nie zapytał. <!-- fakt: auto-aplikacja-opis-trybu -->

<!-- /kolumny -->

Prośba za każdym razem była ta sama. Zmienił się tylko tryb, a z nim liczba zatrzymań: dwa, jedno, zero.

W ćwiczeniu wysyłka nie tworzy pliku, dlatego w podglądzie folderu widzisz tylko zmienione zamówienie.

W ćwiczeniu, w trybach Manual i Accept edits, Claude pisze, że potrzebuje Twojej zgody na wysyłkę. W prawdziwej aplikacji w tym miejscu program zapyta Cię o zgodę. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: accept-edits-odczyty-bez-pytania --> W ćwiczeniu zastępuje je odpowiedź Claude, bo dokumentacja nie opisuje, jak to pytanie wygląda.

![O wysyłkę przez konektor Claude pyta Ciebie, a w trybie Auto decyduje strażnik. Prośba o wpis w zamówieniu i wiadomość do klientki dzieli się na dwa działania: zmianę pliku i wysyłkę przez konektor. W kolumnach Manual, Accept edits i Auto widać, kto decyduje o każdym z nich. Pod spodem są dwa wyjątki: narzędzie, o które Claude pyta w każdym trybie, i narzędzie zablokowane przez organizację.](obrazy/kto-decyduje-konektor.png)

## Co tryb przepuszcza bez pytania

Bez pytania przechodzi to, co przepuszcza wybrany tryb:

- **Manual:** tylko odczyty. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> Przed większością działań, które zmieniają pliki, uruchamiają polecenia albo sięgają do sieci, Claude się zatrzymuje i pyta. <!-- fakt: tryb-manual-pyta-przed-akcjami --> Przy zmianie pliku widzisz jej podgląd i przyjmujesz ją albo odrzucasz. <!-- fakt: aplikacja-manual-podglad-i-przyciski -->
- **Accept edits:** odczyty, zmiany plików i typowe polecenia na plikach, na przykład kopiowanie i przenoszenie. <!-- fakt: accept-edits-odczyty-bez-pytania --> Claude sam tworzy i zmienia pliki w folderze, w którym pracujesz. <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania --> O inne polecenia aplikacja nadal pyta. <!-- fakt: accept-edits-aplikacja-pyta-o-inne-polecenia -->
- **Auto:** wszystko, a w tle działają kontrole bezpieczeństwa. <!-- fakt: tryb-auto-bez-pytania-wszystko-z-kontrola-w-tle --> Działania ocenia strażnik, czyli osobny model AI (klasyfikator), zanim się wykonają. <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem -->

Wysłania wiadomości nie ma na liście tego, co Manual i Accept edits przepuszczają bez pytania. <!-- fakt: tryb-manual-bez-pytania-tylko-odczyt --> <!-- fakt: accept-edits-odczyty-bez-pytania --> Dlatego w ćwiczeniu Claude w obu tych trybach zatrzymał się przed wysyłką.

Skoro wiesz, co przepuszcza każdy tryb, dobierz go do zadania:

- Manual, gdy chcesz sam zatwierdzać każdą zmianę, <!-- fakt: aplikacja-zatwierdzanie-kazdej-zmiany-to-manual -->
- Accept edits, gdy ufasz zmianom w plikach i chcesz pracować szybciej, <!-- fakt: accept-edits-aplikacja-kiedy-uzywac -->
- Auto do długich zadań, przy których pytania o zgodę Cię męczą. <!-- fakt: auto-do-dlugich-zadan -->

Na liście trybów może się też pojawić Bypass permissions (pomijanie uprawnień), ale dopiero po włączeniu. <!-- fakt: aplikacja-dostepne-tryby --> Ten tryb działa bez pytań o zgodę, z kilkoma wyjątkami. Jeden z nich poznasz niżej, w części „Narzędzie, które pyta w każdym trybie”. Dokumentacja każe go używać tylko w odizolowanych kontenerach albo maszynach wirtualnych. <!-- fakt: aplikacja-bypass-tylko-kontenery --> Na zwykłym komputerze z Twoimi plikami tego trybu nie włączaj.

## Co strażnik sprawdza przed wysyłką

W trybie Auto każde działanie Claude przechodzi przez te same kroki, zawsze w tej samej kolejności. <!-- fakt: auto-kolejnosc-najpierw-reguly --> Przy zadaniu z ćwiczenia liczą się dwa z nich:

1. Odczyty i zmiany plików w folderze, w którym pracujesz, przechodzą od razu, bez strażnika, poza dwoma wyjątkami. <!-- fakt: auto-kolejnosc-odczyty-i-edycje-w-folderze -->
2. Wszystko inne trafia do strażnika. <!-- fakt: auto-kolejnosc-reszta-do-klasyfikatora --> W ćwiczeniu to była wysyłka wiadomości.

Zanim Claude uruchomi polecenie albo sięgnie do sieci, strażnik w tle sprawdza, czy to działanie zgadza się z Twoją prośbą. <!-- fakt: auto-aplikacja-opis-trybu --> Domyślnie blokuje między innymi:

- wysyłanie wrażliwych danych na zewnętrzne adresy, <!-- fakt: auto-blokuje-wysylanie-danych -->
- wrażliwe szczegóły w treści wysyłanej do innych ludzi, gdy Twoja wiadomość nie pozwoliła na nie dla tego odbiorcy. <!-- fakt: auto-blokuje-wrazliwe-szczegoly-do-innych -->

Gdy strażnik zablokuje działanie, Claude dostaje powód. Zwykle to nazwa reguły, a nie pisemne wyjaśnienie. <!-- fakt: auto-claude-dostaje-powod-blokady -->

W ćwiczeniu strażnik przepuścił wiadomość z terminem degustacji. Przy innej treści wiadomości strażnik mógłby ją zatrzymać. <!-- fakt: auto-blokuje-wrazliwe-szczegoly-do-innych -->

Tryb Auto zmniejsza liczbę pytań o zgodę, ale nie gwarantuje bezpieczeństwa. Nie zastępuje Twojego przeglądu wrażliwych działań. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->

## Narzędzie, które pyta w każdym trybie

Czasem samo pytanie o zgodę jest celem. Dokumentacja podaje przykład: krok, w którym ktoś udziela zgody albo dostępu. Gdyby taki krok przeszedł sam, żaden człowiek by się na nic nie zgodził. <!-- fakt: mcp-narzedzie-wymagajace-zgody-po-co -->

Dlatego autor konektora (w dokumentacji: serwera MCP) może oznaczyć narzędzie tak, żeby każde jego użycie wymagało Twojej wyraźnej zgody. <!-- fakt: mcp-autor-oznacza-narzedzie-wymagajace-zgody --> Dokumentacja opisuje to dla Claude Code. Aplikacja na komputer działa na tym samym silniku. <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Takie narzędzie działa inaczej niż reszta:

- Claude Code pyta o zgodę przy każdym jego użyciu, także w trybach Accept edits i Auto. <!-- fakt: mcp-narzedzie-wymagajace-zgody-pyta-w-kazdym-trybie -->
- W pytaniu nie ma odpowiedzi „nie pytaj ponownie”. <!-- fakt: mcp-narzedzie-wymagajace-zgody-pyta-w-kazdym-trybie -->
- Żaden tryb nie przepuszcza go bez pytania, nawet Bypass permissions. <!-- fakt: zaden-tryb-nie-przepuszcza-narzedzi-wymagajacych-zgody -->
- W trybie Auto takie narzędzie nie trafia do strażnika. Pyta wprost Ciebie. <!-- fakt: auto-narzedzia-wymagajace-zgody-omijaja-klasyfikator -->

Dzięki temu zgoda na taki krok zawsze pochodzi od człowieka. Pozostałe narzędzia tego samego konektora działają według trybu, tak jak w ćwiczeniu. <!-- fakt: mcp-narzedzie-wymagajace-zgody-po-co -->

Dokumentacja nie mówi, które narzędzia konektorów z katalogu są tak oznaczone. Nie opisuje też, jak takie pytanie wygląda w aplikacji. Dlatego ćwiczenie go nie pokazuje.

## Co może zablokować organizacja

Ta część dotyczy Cię tylko wtedy, gdy Twoje konto Claude należy do organizacji. <!-- fakt: konektor-organizacja-ustawia-zasady-narzedzi -->

Organizacja może ustawić zasady dla każdego narzędzia konektora osobno. <!-- fakt: konektor-organizacja-ustawia-zasady-narzedzi --> Gdy zablokuje narzędzie, dzieje się tak:

1. Aplikacja zatrzymuje zablokowane narzędzia, zanim przekaże konektor do rozmowy. Robi tak w rozmowach na Twoim komputerze (w aplikacji: This computer, w dokumentacji: Local) i w rozmowach SSH. <!-- fakt: aplikacja-konektor-bez-zablokowanych-narzedzi --> <!-- fakt: aplikacja-rzad-pod-polem-folder-z-nazwa-kadr -->
2. Claude w ogóle ich nie widzi, bo nie ma ich na jego liście narzędzi. <!-- fakt: konektor-zablokowane-narzedzie-niewidoczne-dla-claude -->
3. Aplikacja pomija konektor, którego wszystkie narzędzia są zablokowane. <!-- fakt: aplikacja-i-czat-ta-sama-blokada-narzedzia -->

Aplikacja i czat na claude.ai stosują tę samą blokadę. Dzięki temu zablokowanego narzędzia Claude nie użyje ani w aplikacji, ani w czacie. <!-- fakt: aplikacja-i-czat-ta-sama-blokada-narzedzia -->

Dokumentacja nie podaje, po co organizacja blokuje narzędzia.

Organizacja może też wybrać dla narzędzia ustawienie ask (pytaj). To ustawienie nie dociera do rozmów, które aplikacja prowadzi na Twoim komputerze. Takie narzędzie podlega tam zwykłym regułom uprawnień zamiast pytania przy każdym użyciu. <!-- fakt: aplikacja-konektor-zwykle-reguly-uprawnien -->

## Kiedy włączać Auto przy konektorze, a kiedy nie

<!-- kolumny -->

#### Włącz

- Do długiego zadania, przy którym pytania o zgodę Cię męczą. <!-- fakt: auto-do-dlugich-zadan -->
- Gdy ufasz, że praca idzie w dobrą stronę. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->
- Gdy chcesz sam zatwierdzić tylko jeden krok, na przykład wysyłkę. Wpisz w prośbę taką granicę: „nie wysyłaj, zanim przeczytam”. Strażnik potraktuje to jak sygnał blokady. <!-- fakt: auto-granice-z-rozmowy -->

#### Wybierz Manual albo Accept edits

- Gdy chcesz sam zdecydować o wysłaniu wiadomości do klienta. W trybie Auto ocenia ją strażnik, nie Ty. <!-- fakt: auto-kolejnosc-reszta-do-klasyfikatora -->
- Gdy chcesz sam zatwierdzać każdą zmianę w plikach. Wtedy wybierz Manual. <!-- fakt: aplikacja-zatwierdzanie-kazdej-zmiany-to-manual -->
- Gdy działanie jest wrażliwe i chcesz je sprawdzić sam. Tryb Auto nie zastępuje takiego przeglądu. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->

<!-- /kolumny -->

Strażnik blokuje działanie, które pasuje do granicy, nawet gdy domyślne reguły by je przepuściły. <!-- fakt: auto-granice-z-rozmowy --> Granica obowiązuje, dopóki nie zdejmiesz jej kolejną wiadomością, i nie znika, gdy Claude sam uzna warunek za spełniony. <!-- fakt: auto-granica-trwa-do-zdjecia-wiadomoscia -->

Granica z prośby nie jest zapisaną regułą. Gdy długa rozmowa zostanie streszczona, wiadomość z granicą może zniknąć, a z nią granica. <!-- fakt: auto-granice-z-rozmowy -->

Aplikacja zapamiętuje dla folderu tryb wybrany w przełączniku (poza trybem Plan). <!-- fakt: aplikacja-tryb-wybierasz-w-przelaczniku --> Jeśli raz wybierzesz tryb Auto w folderze z zamówieniami, będzie włączony, gdy znów otworzysz ten folder. Przed zadaniem z wysyłką sprawdź więc, jaki tryb pokazuje przełącznik pod polem wiadomości. <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci -->

Za sprawdzenie tego, co Claude proponuje, zanim się na to zgodzisz, odpowiadasz Ty. <!-- fakt: uzytkownik-przeglada-przed-zgoda -->

## Źródła

- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Łączenie Claude Code z narzędziami przez MCP](https://code.claude.com/docs/en/mcp)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Bezpieczeństwo](https://code.claude.com/docs/en/security)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
