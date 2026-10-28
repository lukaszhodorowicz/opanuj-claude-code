<em>Przewodnik po Claude Code · Moduł 5: Claude w Twoich narzędziach · Lekcja 3 z 4</em>

# Claude czyta strony i wypełnia formularze za Twoją zgodą

Prowadzisz serwis rowerowy. Chcesz porównać swoje ceny przeglądów z cenami konkurencji i zapytać hurtownię o cennik części. Ceny konkurencji są na jej stronie. Hurtownia przyjmuje zapytania przez formularz na swojej stronie. Zwykle robisz to ręcznie: przepisujesz ceny ze strony do pliku, a dane firmy z pliku do formularza.

Tę pracę może zrobić Claude w panelu Browser (przeglądarka). Panel znasz z modułu 3: kliknięcie ścieżki pliku HTML w rozmowie otwiera ten plik w panelu. <!-- fakt: aplikacja-klik-sciezki-do-pdf-html-wideo-otwiera-panel-browser --> Panel Browser to przeglądarka z kartami, więc otworzysz w nim także dowolną inną stronę. <!-- fakt: aplikacja-browser-karty-dowolna-strona -->

Claude może czytać cudze strony i działać na nich. <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach --> Używa do tego tych samych narzędzi, którymi sprawdza Twoją własną stronę albo aplikację. <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach --> Te narzędzia klikają i wypełniają formularze. <!-- fakt: aplikacja-browser-narzedzia-klikaja-i-wypelniaja-formularze -->

Gdy Claude pierwszy raz ma coś zrobić na cudzej stronie, pokazuje kartę zgody i czeka na Twój wybór. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

W ćwiczeniu niżej poproś Claude dwa razy o ceny konkurencji. Zobaczysz, że zanim Claude otworzy cudzą stronę, pokazuje kartę zgody i czeka na Twój wybór. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone --> Po Allow once (zezwól raz) zapisuje ceny do pliku, a po Deny (odmów) na stronę nie wchodzi. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Allow once

<!-- podglad: cw1 zezwol-raz -->

1. Claude zapowiedział, że wejdzie na stronę konkurencji, Serwisu Rowerowego Zet. Zanim ją otworzył, pokazał kartę zgody i czekał. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone -->
2. Po Allow once strona otworzyła się w panelu Browser, a Claude ją przeczytał. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu --> <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach -->
3. Ceny zapisał w nowym pliku bez pytania, bo był włączony tryb Accept edits (przyjmowanie zmian). <!-- fakt: claude-code-tworzy-nowe-pliki --> <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania --> Kliknięcie ścieżki otworzyło plik. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

#### Deny

1. Karta pojawiła się w tym samym momencie: zanim Claude otworzył stronę. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone -->
2. Po Deny strona się nie otworzyła, a w folderze nie przybyło pliku z cenami. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->
3. Dokumentacja nie opisuje, co Claude mówi po odmowie. Jego słowa w ćwiczeniu to przykład.

<!-- /kolumny -->

Aplikacja pyta o zgodę już przy pierwszym wejściu na nową stronę. <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone --> Dopóki nie wybierzesz, Claude czeka. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

Przycisk Allow once zezwolił na to działanie. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu --> Sam przycisk niczego nie zapisał. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu --> Plik z cenami zapisał w folderze sam Claude, jak każdy inny wynik pracy. <!-- fakt: claude-code-tworzy-nowe-pliki --> <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania -->

Oprócz karty działają jeszcze dwa sprawdzenia, których ćwiczenie nie pokazuje. <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach --> Pokazuje je rysunek poniżej, a opisuje część „Dwa sprawdzenia oprócz karty”.

![Na cudzej stronie działają trzy sprawdzenia, a o karcie zgody decydujesz Ty. Każde działa w swoim momencie: lista dozwolonych domen przed wejściem na nową stronę, strażnik przy klikaniu i pisaniu oraz karta zgody przy pierwszym działaniu na stronie, nawet przy wejściu. Do działania w panelu Browser prowadzą tylko przyciski Allow once i Always allow.](obrazy/dwa-sprawdzenia-strony.png)
<!-- analogia: Pomyśl o ochronie biurowców. Gdy Twój pracownik pierwszy raz idzie do obcej firmy, recepcja dzwoni do Ciebie, a Ty mówisz: wpuść raz, wpuszczaj zawsze albo nie wpuszczaj. To karta zgody. W części trybów ochrona na bramce sprawdza jeszcze listę dozwolonych adresów. Po korytarzach chodzi ochroniarz i woła Cię, gdy pracownik robi coś podejrzanego. To strażnik. -->

## Karta zgody: trzy przyciski

Na cudzej stronie Claude czyta, klika i pisze. <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach --> <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> Przy pierwszym takim działaniu na stronie Claude czeka na Twój wybór na karcie zgody. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

Karta ma trzy przyciski: <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

- **Allow once** (zezwól raz) zezwala na to działanie i niczego nie zapisuje. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu -->
- **Always allow** (zezwalaj zawsze) zapisuje zgodę dla tej strony na Twoim komputerze. <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony --> Później aplikacja pomija pytanie o zgodę dla tej strony. <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone -->
- **Deny** (odmów) odmawia zgody. W ćwiczeniu Claude po Deny nie wszedł na stronę. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

### Dwa sprawdzenia oprócz karty

Na cudzych stronach działają jeszcze dwa sprawdzenia: <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach -->

1. **Lista dozwolonych domen,** czyli adresów stron. Zanim Claude przejdzie na nową stronę, działa sprawdzenie tej listy. Tak jest w trybach innych niż Auto i Bypass permissions (pomijanie uprawnień). <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona --> W ćwiczeniach był włączony tryb Accept edits, a w nim to sprawdzenie działa. <!-- fakt: aplikacja-browser-lista-domen-przed-nowa-strona -->
2. **Strażnik.** W każdym trybie sprawdza działania Claude, które coś zmieniają na cudzej stronie, takie jak klikanie i pisanie. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> Strażnika znasz z modułu 1. To ten sam, który w trybie Auto sprawdza w tle działania Claude. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> <!-- fakt: auto-aplikacja-opis-trybu -->

Gdy strażnik oflaguje działanie (oznaczy je jako ryzykowne), dostajesz pytanie o zgodę bez względu na tryb. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie --> Pytanie dostaniesz nawet w trybie Bypass permissions, który poza kilkoma wyjątkami o nic nie pyta. <!-- fakt: aplikacja-bypass-pyta-przy-dzialaniu-na-cudzych-stronach -->

### Co zyskujesz i gdzie są granice

Dzięki karcie decydujesz o każdej cudzej stronie osobno. Na przykład: <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony -->

- stronę konkurencji przepuszczasz raz przyciskiem Allow once, <!-- fakt: aplikacja-browser-allow-once-bez-zapisu -->
- dla strony hurtowni wybierasz Always allow, który zapisuje zgodę, <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony -->
- nieznanej stronie odmawiasz zgody przyciskiem Deny. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

Pliki z Twojego folderu nie potrzebują karty zgody. <!-- fakt: aplikacja-browser-pliki-projektu-bez-zgody --> Dlatego stronę z modułu 3, zapisaną jako plik HTML w folderze, otwierasz w panelu bez pytania. <!-- fakt: aplikacja-browser-pliki-projektu-bez-zgody --> <!-- fakt: aplikacja-klik-sciezki-do-pdf-html-wideo-otwiera-panel-browser -->

Na co uważać:

- Każda strona potrzebuje osobnej zgody. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony --> Dotyczy to też subdomen, czyli adresów z dodatkowym członem przed nazwą strony, na przykład „sklep.” przed adresem hurtowni. <!-- fakt: aplikacja-browser-osobna-zgoda-dla-kazdej-strony -->
- Nawet na stronie z Twoją zgodą Claude bez Twojego udziału niczego nie kupi i nie założy konta. <!-- fakt: aplikacja-browser-bez-zakupow-kont-captcha --> Nie obejdzie też CAPTCHA, czyli zabezpieczenia, które sprawdza, czy ze strony korzysta człowiek, a nie program. <!-- fakt: aplikacja-browser-bez-zakupow-kont-captcha -->

W drugim ćwiczeniu Claude wypełni formularz zapytania na stronie Hurtowni Bike-Pro. Zobaczysz, że Claude wpisze dane w pola formularza. <!-- fakt: aplikacja-browser-narzedzia-klikaja-i-wypelniaja-formularze --> <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach --> Po Always allow kolejne wpisy na tej stronie przejdą bez nowej karty. <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Always allow

<!-- podglad: cw2 zawsze -->

1. Claude przeczytał plik dane-firmy.txt bez pytania, bo w trybie Accept edits odczyty nie wymagają zgody. <!-- fakt: accept-edits-odczyty-bez-pytania -->
2. Przed wejściem na stronę hurtowni pokazał kartę zgody. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone --> Always allow zapisał zgodę dla tej strony. <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony -->
3. Claude wpisał w pola formularza nazwę firmy, e-mail i prośbę o cennik. <!-- fakt: aplikacja-browser-narzedzia-klikaja-i-wypelniaja-formularze --> <!-- fakt: aplikacja-browser-claude-czyta-i-dziala-na-cudzych-stronach -->
4. Formularza nie wysłał, bo prośba brzmiała: „Nie wysyłaj, pokaż mi”.

#### Kolejne wpisy

1. Druga prośba: dopisać zdanie w polu Wiadomość.
2. Claude dopisał je bez nowej karty, bo zgoda dla tej strony jest zapisana. <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony --> <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone -->
3. Strażnik sprawdził także ten wpis. Tym razem niczego nie oflagował. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie -->

<!-- /kolumny -->

Po Always allow aplikacja pomija pytanie o zgodę dla tej strony. <!-- fakt: aplikacja-podglad-pyta-przy-pierwszym-wejsciu-na-nowa-strone --> Pytanie może jednak przyjść od strażnika. Gdy oflaguje działanie, zapyta Cię o zgodę bez względu na tryb. <!-- fakt: aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie -->

Zapisane dane firmy trafiły z pliku do formularza bez przepisywania. Formularz wysyłasz Ty, bo tak brzmiała prośba.

## Logowanie w panelu Browser

Część stron pokazuje dane dopiero po zalogowaniu. W panelu Browser zalogujesz się na stronie, także kontem Google. <!-- fakt: aplikacja-browser-logowanie-w-panelu --> Dzięki temu w panelu skorzystasz też ze strony, która wymaga konta. <!-- fakt: aplikacja-browser-logowanie-w-panelu -->

Panel ma czysty profil przeglądarki, osobny od Twojej zwykłej przeglądarki. <!-- fakt: aplikacja-browser-czysty-profil --> Czysty profil znaczy, że w panelu nie ma Twoich zapisanych logowań ani historii. <!-- fakt: aplikacja-browser-czysty-profil -->

Dokumentacja radzi używać panelu do stron, które nie potrzebują Twojej tożsamości. <!-- fakt: aplikacja-browser-do-stron-bez-twojej-tozsamosci --> Chodzi o strony, na których Claude nie musi działać w Twoim imieniu, jak cennik konkurencji. <!-- fakt: aplikacja-browser-do-stron-bez-twojej-tozsamosci --> <!-- fakt: aplikacja-browser-chrome-gdy-claude-ma-dzialac-jako-ty -->

## Panel Browser a rozszerzenie Claude in Chrome

Czasem Claude ma działać w Twoim imieniu, na przykład w Twoim Gmailu albo w Google Docs. <!-- fakt: chrome-mozliwosci-aplikacje-dane-formularze --> Dokumentacja każe wtedy użyć rozszerzenia Claude in Chrome zamiast panelu Browser. <!-- fakt: aplikacja-browser-chrome-gdy-claude-ma-dzialac-jako-ty --> Rozszerzenie to dodatek do przeglądarki.

Jak działa rozszerzenie:

- Dzieli stan logowania Twojej przeglądarki. Claude ma więc dostęp do każdej strony, na której Twoja przeglądarka jest już zalogowana. <!-- fakt: chrome-dzieli-logowanie-przegladarki -->
- Do zadań otwiera nowe karty. <!-- fakt: chrome-dzieli-logowanie-przegladarki -->
- Jego działania widzisz na bieżąco w oknie Chrome. <!-- fakt: chrome-widoczne-okno-i-pauza-przy-logowaniu -->
- Gdy Claude trafi na stronę logowania albo CAPTCHA, zatrzymuje się i prosi Cię o ręczne zalogowanie się albo rozwiązanie CAPTCHA. <!-- fakt: chrome-widoczne-okno-i-pauza-przy-logowaniu -->

Dzięki rozszerzeniu Claude: <!-- fakt: chrome-mozliwosci-aplikacje-dane-formularze -->

- bez konektorów pracuje w aplikacjach, do których Twoja przeglądarka jest już zalogowana, na przykład w Gmailu, Google Docs i Notion,
- wyciąga dane ze stron i zapisuje je na komputerze,
- wypełnia formularze i wpisuje dane za Ciebie.

Panel Browser korzysta z tego samego modelu bezpieczeństwa co rozszerzenie, czyli z tych samych zabezpieczeń. <!-- fakt: aplikacja-browser-ten-sam-model-bezpieczenstwa-co-chrome -->

Dokumentacja opisuje to rozszerzenie dla Claude Code w terminalu i w VS Code, programie do pisania kodu. <!-- fakt: chrome-rozszerzenie-z-terminala-i-vs-code --> Strona dokumentacji o rozszerzeniu nie opisuje używania go z aplikacji Claude na komputer.

Dla Ciebie w aplikacji znaczy to tyle: strony, na których Claude nie musi działać w Twoim imieniu, otwierasz w panelu Browser, a do pracy na Twoim koncie dokumentacja kieruje do rozszerzenia, opisanego dla terminala i VS Code. <!-- fakt: aplikacja-browser-do-stron-bez-twojej-tozsamosci --> <!-- fakt: aplikacja-browser-chrome-gdy-claude-ma-dzialac-jako-ty --> <!-- fakt: chrome-rozszerzenie-z-terminala-i-vs-code -->

Żeby Claude Code pracował z Chrome, potrzebujesz: <!-- fakt: chrome-wymagania-przegladarka-sklep-plan -->

- przeglądarki Chrome, Edge albo innej opartej na Chromium,
- rozszerzenia Claude in Chrome ze sklepu Chrome Web Store,
- planu Pro, Max, Team albo Enterprise wykupionego bezpośrednio w Anthropic.

## Jak to zrobić u siebie

1. Otwórz panel Browser skrótem Cmd+Shift+B na Macu albo Ctrl+Shift+B w Windows. <!-- fakt: aplikacja-browser-otwierasz-skrotem-albo-przyciskiem --> Możesz też kliknąć przycisk Browser na pasku tytułu rozmowy. Jego nazwę zobaczysz po najechaniu myszą. <!-- fakt: aplikacja-browser-otwierasz-skrotem-albo-przyciskiem --> <!-- fakt: aplikacja-panel-plikow-files-na-pasku-tytulu -->
2. Napisz, z jakiej strony Claude ma wziąć dane i co ma z nimi zrobić. Wyślij prośbę klawiszem <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie -->
3. Gdy pojawi się karta zgody, wybierz Allow once, Always allow albo Deny. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

Warto też wiedzieć:

- Gdy pierwszy raz klikniesz w rozmowie odnośnik do cudzej strony, okno zapyta, czy odnośniki mają się otwierać w panelu Browser, czy w Twojej domyślnej przeglądarce. <!-- fakt: aplikacja-browser-okno-wyboru-przy-pierwszym-odnosniku --> Wybór zmienisz pozycją Open links in built-in browser (otwieraj odnośniki we wbudowanej przeglądarce) w menu ⋮ panelu. <!-- fakt: aplikacja-browser-okno-wyboru-przy-pierwszym-odnosniku -->
- Zgodę Always allow cofniesz w Settings (ustawieniach aplikacji). <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony -->
- Zapisane dane panelu wyczyścisz pozycją Clear browsing data (wyczyść dane przeglądania) w menu ⋮ panelu. <!-- fakt: aplikacja-browser-czyszczenie-danych -->
- Żeby całkiem wyłączyć panel, otwórz Settings > Claude Code i wyłącz Browser tools (narzędzia przeglądarki). <!-- fakt: aplikacja-browser-wylaczenie-browser-tools -->
- W sesji SSH, czyli przy pracy na innym komputerze przez sieć, Claude nie ma narzędzi panelu Browser. <!-- fakt: aplikacja-ssh-bez-narzedzi-panelu-browser -->
- Jeśli Twoje konto należy do organizacji, panel stosuje te same listy dozwolonych i zablokowanych stron co rozszerzenie. Te listy ustawia administrator organizacji. <!-- fakt: aplikacja-browser-organizacja-listy-stron-i-wylaczenie-narzedzi --> Administrator może też wyłączyć narzędzia Claude na cudzych stronach. Wtedy nadal je odwiedzasz, ale Claude ich nie czyta i nic na nich nie robi. <!-- fakt: aplikacja-browser-organizacja-listy-stron-i-wylaczenie-narzedzi -->

## Kiedy pozwalać Claude działać na cudzej stronie, a kiedy nie

<!-- kolumny -->

#### Pozwól

- Gdy strona nie wymaga Twojej tożsamości, na przykład cennik konkurencji. Claude nie musi tam działać w Twoim imieniu. <!-- fakt: aplikacja-browser-do-stron-bez-twojej-tozsamosci -->
- Gdy co tydzień bierzesz dane z tej samej strony. Wybierz Always allow: ten przycisk zapisuje zgodę dla tej strony. <!-- fakt: aplikacja-browser-always-allow-zapisuje-dla-strony -->
- Gdy potrzebujesz strony tylko raz albo jej nie znasz. Wybierz Allow once. Ta zgoda niczego nie zapisuje. <!-- fakt: aplikacja-browser-allow-once-bez-zapisu -->

#### Odmów albo wybierz inną drogę

- Gdy Claude ma działać w Twoim imieniu, na Twoim koncie. Dokumentacja kieruje wtedy do rozszerzenia Claude in Chrome. <!-- fakt: aplikacja-browser-chrome-gdy-claude-ma-dzialac-jako-ty -->
- Gdy zadanie to zakup albo założenie konta. Tego Claude bez Twojego udziału i tak nie zrobi. <!-- fakt: aplikacja-browser-bez-zakupow-kont-captcha -->
- Gdy strona budzi Twoje wątpliwości albo do zadania jej nie potrzebujesz. Wybierz Deny. <!-- fakt: aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu -->

<!-- /kolumny -->

## Źródła

- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Claude Code w przeglądarce Chrome](https://code.claude.com/docs/en/chrome)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
