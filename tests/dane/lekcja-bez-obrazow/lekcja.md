<em>Przewodnik po Claude Code · Moduł 1: Tryby pracy · Lekcja 3 z 4</em>

# Tryb planowania: najpierw plan, potem zmiany

Dwa ćwiczenia w symulatorze

Prosisz Claude o podwyżkę cen w cenniku dla klientów. Claude od razu zmienia plik. Podnosi też cenę pakietu, który obiecujesz klientom w promocji do końca roku. Pomyłkę widzisz dopiero w zmienionym pliku.

Dokumentacja Claude Code nazywa ten problem wprost. Gdy Claude od razu zabiera się do pisania kodu, może rozwiązać nie ten problem. <!-- fakt: plan-od-razu-do-kodu-zly-problem --> W cenniku wygląda to tak: prosisz o podwyżkę wszystkich cen, a chcesz podwyżki bez promocji.

Na to jest tryb Plan (planowanie). Oddziela badanie od wykonania. <!-- fakt: plan-od-razu-do-kodu-zly-problem --> W trybie Plan Claude czyta pliki i uruchamia polecenia, żeby zbadać folder. Potem proponuje plan. <!-- fakt: plan-aplikacja-opis --> Plików nie zmienia, dopóki nie zatwierdzisz planu. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia -->

Wyślij tę samą prośbę dwa razy: najpierw bez planu, potem z planem. Zobaczysz, że bez planu pomyłkę widać dopiero w zmienionym pliku, a z planem w planie, zanim plik się zmieni.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Bez planu

<!-- podglad: cw1 bez-planu -->

1. W trybie Accept edits (przyjmowanie zmian) Claude od razu zmienił cennik. <!-- fakt: aplikacja-accept-edits-auto-bez-czekania-na-zgode -->
2. Promocja poszła w górę: 990 zł zamiast 900 zł.
3. Pomyłkę widać dopiero w widoku zmian, po fakcie. <!-- fakt: aplikacja-widok-zmian-liczby-na-karcie-changes -->

#### Z planem

<!-- podglad: cw1 z-planem -->

1. W trybie Plan Claude przeczytał cennik i zaproponował plan. <!-- fakt: plan-aplikacja-opis -->
2. Plan pojawił się w rozmowie na karcie <em>Claude proposed a plan</em> (Claude proponuje plan). <!-- fakt: aplikacja-karta-planu-napisy -->
3. Cały plan z tytułem i sekcjami stoi w panelu Plan po prawej. <!-- fakt: aplikacja-panel-plan-wyglad -->
4. Promocję widać w planie, a plik jest jeszcze bez zmian. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia -->
5. Po kliknięciu <em>Accept and auto mode</em> przełącznik pokazał Auto, a Claude od razu zmienił plik. <!-- fakt: aplikacja-plan-accept-and-auto-mode-karta-znika-auto --> <!-- fakt: aplikacja-plan-accept-and-auto-mode-claude-buduje -->

<!-- /kolumny -->

W obu drogach Claude zrobił to samo: podniósł też promocję. Różnica leży w chwili, w której to widzisz. Bez planu widzisz gotową zmianę w pliku. Z planem widzisz zamiar, a plik czeka.

Plan chroni więc tylko wtedy, gdy go przeczytasz. Gdy w ćwiczeniu klikniesz <em>Accept and auto mode</em> bez czytania, promocja i tak pójdzie w górę.

### Jak działa tryb Plan

W trybie Plan Claude bada sprawę i proponuje zmiany, ale ich nie wprowadza. <!-- fakt: tryb-plan-nie-zmienia-plikow --> Czyta pliki i uruchamia polecenia, które pomagają zbadać folder. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia --> Zmiany w plikach są zablokowane, dopóki nie zatwierdzisz planu. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia -->

Plan widzisz w dwóch miejscach:

- w rozmowie: karta <em>Claude proposed a plan</em> z przyciskami do decyzji, <!-- fakt: aplikacja-karta-planu-napisy -->
- w panelu Plan po prawej: plan z tytułem i sekcjami. <!-- fakt: aplikacja-panel-plan-wyglad -->

Panel Plan to jeden z paneli zakładki Code, obok rozmowy, widoku zmian i terminala. <!-- fakt: aplikacja-panele-zakladki-code --> Pojawia się dopiero wtedy, gdy sesja ma plan do pokazania. <!-- fakt: aplikacja-panel-plan-w-menu -->

### Po co Ci plan

Dzięki planowi widzisz, co dokładnie Claude zamierza, zanim zmieni plik. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia --> Pomyłkę łapiesz w planie, a nie w cenniku, który już poszedł do klientów.

Dokumentacja radzi zaczynać w trybie Plan złożone zadania. Wtedy Claude najpierw rozpisuje, jak je zrobi, a dopiero potem zmienia pliki. <!-- fakt: plan-aplikacja-porada-po-zatwierdzeniu -->

### Na co uważać w trybie Plan

- **Plan wydłuża pracę.** Tryb Plan pomaga, ale dokłada pracy. <!-- fakt: plan-drobna-zmiana-bez-planu --> Przy małej, jasnej zmianie poproś Claude wprost. Więcej o tym na końcu lekcji.
- **Polecenia nie zawsze idą bez pytania.** Czytanie plików idzie bez pytania. <!-- fakt: tryb-plan-bez-pytania-odczyty-i-polecenia-klasyfikatora --> Gdy masz dostęp do trybu Auto, polecenia ocenia klasyfikator w tle. <!-- fakt: plan-polecenia-klasyfikator-albo-pytanie --> <!-- fakt: auto-aplikacja-opis-trybu --> Zatwierdzone się wykonują, a odrzucone są blokowane. <!-- fakt: plan-polecenia-klasyfikator-albo-pytanie --> Bez dostępu do trybu Auto Claude pyta Cię o zgodę na polecenia spoza wbudowanej listy poleceń tylko do odczytu. <!-- fakt: plan-polecenia-klasyfikator-albo-pytanie -->
- **Plan działa tylko w tej sesji.** W aplikacji wybór trybu Plan obowiązuje tylko w bieżącej sesji (rozmowie). <!-- fakt: plan-aplikacja-tylko-biezaca-sesja --> W nowej sesji wybierasz go znowu.

## Trzy wyjścia z planu

Plan sam niczego nie zmienia. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia --> Pod planem decydujesz, co dalej: poprawić go czy wykonać. A jeśli wykonać, to w jakim trybie.

<!-- rysunek: R4 Co się dzieje po każdym przycisku. Plik obrazy/wyjscia-z-planu.png -->

Decyzję podejmujesz jednym z trzech przycisków na karcie planu: <!-- fakt: aplikacja-karta-planu-napisy -->

- **Revise…** (popraw). Na karcie pojawia się pole <em>What should change? (optional)</em> (co zmienić? nieobowiązkowe). <!-- fakt: aplikacja-plan-revise-pole-poprawki --> Piszesz w nim, co zmienić w planie, i klikasz <em>Revise</em>. Claude poprawia plan. <!-- fakt: aplikacja-plan-revise-poprawia-plan --> Twoja poprawka staje w rozmowie jako wiadomość, a przełącznik dalej pokazuje Plan. <!-- fakt: aplikacja-plan-revise-dymek-tryb-plan --> Potem w rozmowie pojawia się nowa karta planu. <!-- fakt: aplikacja-plan-revise-nowa-karta --> Przycisk <em>Back</em> (wstecz) wraca do przycisków karty i niczego nie wysyła. <!-- fakt: aplikacja-plan-revise-back-wraca -->
- **Accept** (zatwierdź). Zatwierdzasz plan, ale każdą zmianę zatwierdzasz potem ręcznie. <!-- fakt: aplikacja-plan-accept-potem-zmiany-recznie --> Przełącznik pokazuje wtedy Manual (ręczny). <!-- fakt: aplikacja-plan-accept-potem-zmiany-recznie --> <!-- fakt: plan-zatwierdzenie-wychodzi-z-trybu-planowania --> W tym trybie Claude proponuje każdą zmianę i czeka na Twoją zgodę. <!-- fakt: tryb-manual-aplikacja-czeka-na-zatwierdzenie --> Widzisz podgląd zmiany i przyjmujesz ją albo odrzucasz, jak w lekcji 1. <!-- fakt: aplikacja-manual-podglad-i-przyciski --> W symulatorze ta droga kończy się na przełączniku Manual i odpowiedzi Claude.
- **Accept and auto mode** (zatwierdź i włącz tryb Auto). Karta znika, przełącznik pokazuje Auto, a panel Plan zostaje otwarty. <!-- fakt: aplikacja-plan-accept-and-auto-mode-karta-znika-auto --> Claude od razu zaczyna pracę. <!-- fakt: aplikacja-plan-accept-and-auto-mode-claude-buduje --> Zanim wykona polecenie albo sięgnie do sieci, klasyfikator w tle sprawdza, czy to zgadza się z Twoją prośbą. <!-- fakt: auto-aplikacja-opis-trybu --> Tryb Auto poznasz w lekcji 4.

Zatwierdzenie planu kończy tryb Plan i przełącza sesję na tryb, który opisuje wybrany przycisk. <!-- fakt: plan-zatwierdzenie-wychodzi-z-trybu-planowania --> Poprawka trybu nie zmienia. <!-- fakt: aplikacja-plan-revise-dymek-tryb-plan -->

Dzięki temu sam decydujesz, jak Claude wykona plan:

- z Twoją zgodą przy każdej zmianie (Accept), <!-- fakt: aplikacja-plan-accept-potem-zmiany-recznie -->
- sam, pod okiem klasyfikatora (Accept and auto mode). <!-- fakt: auto-aplikacja-opis-trybu -->

Tryb Auto pojawia się w aplikacji tylko wtedy, gdy masz do niego dostęp. <!-- fakt: aplikacja-dostepne-tryby --> Dokumentacja aplikacji radzi też inną drogę: po zatwierdzeniu planu przełącz się na Accept edits albo Manual, żeby go wykonać. <!-- fakt: plan-aplikacja-porada-po-zatwierdzeniu -->

Teraz sam włącz tryb Plan w przełączniku i poproś o zmianę w cenniku. Zobaczysz, że Claude proponuje plan, a poprawka przyciskiem Revise… zatrzymuje usunięcie konsultacji, zanim plik się zmieni.

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Poprawka planu

1. Po wybraniu Plan z listy przełącznik pokazał Plan. <!-- fakt: aplikacja-tryb-wybierasz-w-przelaczniku -->
2. Claude przeczytał cennik i zaproponował plan. Plik się nie zmienił. <!-- fakt: plan-aplikacja-bez-zmian-w-plikach -->
3. Revise… otworzył pole na poprawkę. <!-- fakt: aplikacja-plan-revise-pole-poprawki -->
4. Poprawka poszła jako Twoja wiadomość, a tryb został Plan. <!-- fakt: aplikacja-plan-revise-dymek-tryb-plan -->
5. Claude napisał nowy plan: konsultacja zostaje. <!-- fakt: aplikacja-plan-revise-nowa-karta -->

#### Wykonanie planu

1. Po Accept przełącznik pokazał Manual. Zmianę w cenniku zatwierdzasz sam. <!-- fakt: aplikacja-plan-accept-potem-zmiany-recznie --> <!-- fakt: plan-zatwierdzenie-wychodzi-z-trybu-planowania -->
2. Po Accept and auto mode przełącznik pokazał Auto, a audyt od razu trafił do cennika. <!-- fakt: aplikacja-plan-accept-and-auto-mode-karta-znika-auto --> <!-- fakt: aplikacja-auto-i-accept-edits-stosuja-zmiany -->
3. Konsultacja została, bo poprawka zmieniła plan, zanim plik się zmienił. <!-- fakt: plan-edycje-zablokowane-do-zatwierdzenia -->

<!-- /kolumny -->

## Jak włączyć tryb Plan

### W aplikacji Claude na komputer

1. W zakładce Code kliknij przełącznik trybu pod polem wiadomości. <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci --> Otworzy się lista trybów. <!-- fakt: aplikacja-tryb-wybierasz-w-przelaczniku --> Listę otworzysz też skrótem <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd> na Macu <!-- fakt: aplikacja-skrot-menu-trybu --> albo <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd> na Windowsie. <!-- fakt: aplikacja-skrot-menu-trybu-windows -->
2. Kliknij Plan. <!-- fakt: aplikacja-dostepne-tryby -->
3. Napisz prośbę i naciśnij <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie --> Claude zbada folder i zaproponuje plan. <!-- fakt: plan-aplikacja-opis -->

Panel Plan nie ma przycisku na pasku tytułu rozmowy. Wybierzesz go z menu ⋮ obok przycisków tego paska, gdy sesja ma już plan. <!-- fakt: aplikacja-panel-plan-w-menu -->

Tryb zmienisz w każdej chwili, także w trakcie rozmowy. <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci --> Inne tryby aplikacja zapamiętuje dla folderu, a Plan obowiązuje tylko w bieżącej sesji. <!-- fakt: plan-aplikacja-tylko-biezaca-sesja --> W aplikacji <kbd>Shift</kbd> + <kbd>Tab</kbd> nie zmienia trybu. <!-- fakt: cykl-aplikacja-brak-shift-tab -->

### Jeśli pracujesz w terminalu

Claude Code działa też w terminalu. Tryb Plan włączasz tam i kończysz inaczej niż w aplikacji.

1. Naciskaj <kbd>Shift</kbd> + <kbd>Tab</kbd>, aż pasek stanu pokaże <em>⏸ plan mode on</em> (tryb planowania włączony). <!-- fakt: plan-terminal-shift-tab-az-do-plan-mode-on --> <!-- fakt: pasek-napisy-trybow -->
2. Plan możesz też włączyć dla jednej wiadomości. Wpisz wtedy `/plan` przed prośbą. <!-- fakt: tryb-plan-wlaczenie-shift-tab-lub-plan -->

Gdy Claude napisze plan, wybierasz jedną z odpowiedzi:

- <em>Yes, and use auto mode</em> (tak, w trybie auto): zatwierdzasz plan, a Claude zaczyna pracę w trybie Auto. <!-- fakt: plan-opcja-yes-and-use-auto-mode --> Gdy tryb Auto nie jest dostępny w sesji, ta odpowiedź nazywa się <em>Yes, auto-accept edits</em>. <!-- fakt: plan-opcja-yes-auto-accept-edits -->
- <em>Yes, manually approve edits</em> (tak, zmiany zatwierdzę ręcznie): zatwierdzasz plan, ale każdą zmianę przeglądasz osobno. <!-- fakt: plan-opcja-yes-manually-approve-edits -->
- <em>No, keep planning</em> (nie, planuj dalej): zostajesz w trybie Plan i piszesz Claude, co zmienić. <!-- fakt: plan-opcja-no-keep-planning -->

Zatwierdzenie planu kończy tryb Plan i włącza tryb z wybranej odpowiedzi. Wtedy Claude zaczyna zmieniać pliki. <!-- fakt: plan-zatwierdzenie-wychodzi-z-trybu-planowania --> W trakcie pracy sprawdza ją z planem. <!-- fakt: plan-wyjscie-zatwierdzenie-albo-shift-tab -->

Plan poprawisz też sam. <kbd>Ctrl</kbd> + <kbd>G</kbd> otwiera go w Twoim domyślnym edytorze tekstu, zanim Claude przejdzie dalej. <!-- fakt: plan-ctrl-g-otwiera-plan-w-edytorze -->

Z trybu Plan wyjdziesz bez zatwierdzania, gdy znów naciśniesz <kbd>Shift</kbd> + <kbd>Tab</kbd>. <!-- fakt: tryb-plan-wyjscie-shift-tab -->

## Kiedy włączać tryb Plan, a kiedy nie

Dokumentacja zaleca pracę w fazach. Trzy pierwsze to badanie, plan i wykonanie. Czwarta to zapis zmian w repozytorium git. <!-- fakt: plan-cztery-fazy-pracy --> Tryb Plan pilnuje, żeby badanie i plan przyszły przed wykonaniem. <!-- fakt: plan-od-razu-do-kodu-zly-problem -->

<!-- kolumny -->

#### Włącz

- Gdy nie masz pewności, jak zadanie zrobić. <!-- fakt: plan-kiedy-najbardziej-przydatny -->
- Gdy zmiana obejmie wiele plików, na przykład cennik, oferty i umowy naraz. <!-- fakt: plan-kiedy-najbardziej-przydatny -->
- Gdy nie znasz plików, które mają się zmienić, na przykład folderu po poprzednim wykonawcy. <!-- fakt: plan-kiedy-najbardziej-przydatny -->

#### Nie musisz

- Gdy zmianę opiszesz jednym zdaniem. Wtedy pomiń plan. <!-- fakt: plan-kiedy-najbardziej-przydatny -->
- Gdy zakres jest jasny, a poprawka mała, na przykład literówka. Poproś Claude, żeby zrobił to od razu. <!-- fakt: plan-drobna-zmiana-bez-planu -->

<!-- /kolumny -->

Chodzi o opis zmiany, nie prośby. Prośba z ćwiczenia miała jedno zdanie, a zmiana objęła pięć linijek, w tym promocję, której nie chcesz ruszać.

## Źródła

- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Pierwsze kroki w aplikacji](https://code.claude.com/docs/en/desktop-quickstart)
- [Dobre praktyki](https://code.claude.com/docs/en/best-practices)

Dokumentacja nie opisuje karty planu w aplikacji. Jej wygląd i skutki przycisków wzięliśmy z nagrań aplikacji: [12.10.2026](https://www.youtube.com/watch?v=wnSIIVqS48A&t=650s), [18.07.2026](https://www.youtube.com/watch?v=ZW6d_2rwcdk&t=805s), [13.07.2026](https://www.youtube.com/watch?v=-YTot4fwNFY&t=313s) i [30.04.2026](https://www.youtube.com/watch?v=bqJzIWAEn40&t=1033s).

Sprawdzone 26.10.2026, Claude Code 2.1.310.
