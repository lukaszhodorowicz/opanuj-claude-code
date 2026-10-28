<em>Przewodnik po Claude Code · Moduł 7: Hooki: powiadomienia i pilnowanie Twoich zasad · Lekcja 3 z 3</em>

# Sprawdź, jakie hooki już u Ciebie działają

Prowadzisz małe biuro podróży. Pół roku temu do folderu biura trafiły hooki skopiowane z dokumentacji, a potem do Claude Code doszła wtyczka. Dziś przygotowujesz ofertę na Toskanię i nie pamiętasz, co uruchamia się bez Twojej prośby.

Hooki działają poza rozmową i domyślnie nic do niej nie wnoszą. <!-- fakt: hook-dziala-poza-rozmowa --> Gdy hook zadziała, Claude Code nic nie pokazuje w rozmowie. <!-- fakt: hook-sukces-nic-w-rozmowie --> A polecenie hooka działa z pełnymi uprawnieniami Twojego konta. Może zmienić, usunąć albo odczytać każdy plik, do którego ma dostęp Twoje konto. <!-- fakt: hook-pelne-uprawnienia-konta -->

Dlatego warto sprawdzić, jakie hooki działają w Twoim folderze. Hooki z plików ustawień działają i w aplikacji, i w terminalu. <!-- fakt: aplikacja-hooki-z-ustawien-dzialaja --> W aplikacji pytasz o nie Claude, a plik ustawień otwierasz kliknięciem jego ścieżki w odpowiedzi. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

W ćwiczeniu niżej zapytaj Claude o hooki w folderze biura. Zobaczysz, że w tym folderze hooki to wpisy w jednym pliku .claude/settings.json. <!-- fakt: hook-miejsce-folder-albo-komputer --> Claude przeczyta ten plik bez pytania o zgodę i opisze każdy hook: kiedy rusza i co robi. <!-- fakt: accept-edits-odczyty-bez-pytania -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

W tym folderze hooki są zapisane w jednym pliku, a Claude opisał je po polsku.

<!-- kolumny -->

#### Dwa hooki w jednym pliku

<!-- podglad: cw1 zapytaj -->

1. Claude przeczytał plik .claude/settings.json od razu, bo w trybie Accept edits (przyjmowanie zmian) odczyty idą bez pytania o zgodę. <!-- fakt: accept-edits-odczyty-bez-pytania -->
2. Oba hooki stoją w jednym bloku `hooks`, jeden obok drugiego. <!-- fakt: hook-blok-hooks-w-pliku-ustawien --> <!-- fakt: hook-nowe-zdarzenie-obok-istniejacych -->
3. Każdy wpis ma zdarzenie, dopasowanie i hook z poleceniem. <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->
4. Kliknięcie ścieżki otworzyło plik. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

#### Czego nie ma w folderze

1. Plik `~/.claude/settings.json` leży w folderze .claude w Twoim folderze domowym, poza folderem projektu. <!-- fakt: ustawienia-tylda-to-folder-domowy -->
2. Hooki wtyczki leżą w jej pliku `hooks/hooks.json`. <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona -->
3. Claude przeczytał tylko plik folderu biura. Hooki z tamtych miejsc działają razem z hookami folderu. <!-- fakt: hooki-z-roznych-plikow-sumuja-sie --> <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona -->

<!-- /kolumny -->

W ten sposób przeczytasz każdy wpis we własnym pliku:

- zdarzenie mówi, na co hook reaguje, <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->
- dopasowanie (`matcher`) zawęża, kiedy hook rusza, <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->
- pole `command` zawiera polecenie. <!-- fakt: hook-command-uruchamia-polecenie-powloki -->

Pierwszy wpis znasz z lekcji 1. Zdarzenie `Notification` (powiadomienie) z dopasowaniem `permission_prompt` zachodzi, gdy pytanie o zgodę czeka około sześciu sekund. <!-- fakt: hook-aplikacja-permission-prompt-po-szesciu-sekundach --> Wtedy hook uruchamia polecenie powiadomienia dla macOS. <!-- fakt: hook-powiadomienie-polecenie-systemu -->

Drugi wpis to hook dziennika poleceń:

- `PostToolUse` (po użyciu narzędzia) zachodzi po udanym użyciu narzędzia, <!-- fakt: zdarzenie-posttooluse-kiedy -->
- dopasowanie `Bash` pasuje tylko do narzędzia Bash, <!-- fakt: hook-dopasowanie-bash-tylko-narzedzie-bash -->
- Bash to narzędzie, którym Claude uruchamia polecenia powłoki, czyli polecenia takie jak w terminalu, <!-- fakt: narzedzie-bash-uruchamia-polecenia -->
- polecenie hooka dopisuje każde takie polecenie do pliku `~/.claude/command-log.txt`. Treść tego polecenia hook wyciąga programem `jq`. <!-- fakt: hook-przyklad-dziennik-polecen-bash -->

Ten hook to przykład z dokumentacji. <!-- fakt: hook-przyklad-dziennik-polecen-bash -->

## Skąd biorą się hooki i jak się sumują

### Po co wiedzieć, skąd jest hook

Hook nie musi leżeć w folderze, w którym pracujesz. Mógł przyjść z innego miejsca, na przykład z wtyczki. Instalacja wtyczki dodaje do Claude Code:

- jej skille,
- agentów,
- hooki,
- serwery MCP. <!-- fakt: wtyczka-dodaje-hooki -->

Żeby sprawdzić, co działa, musisz wiedzieć, gdzie szukać.

### Jak działają miejsca hooków

Hooki z Twoich ustawień i z ustawień projektu stoją w bloku `hooks` w pliku `settings.json`. Osobnego pliku z hookami nie ma, a własny plik `hooks/hooks.json` mają tylko wtyczki. <!-- fakt: hooki-tylko-w-settings-json -->

Miejsce hooka wyznacza, kiedy hook działa:

- `.claude/settings.json` w folderze projektu: tylko w tym projekcie, <!-- fakt: hook-miejsce-folder-albo-komputer -->
- `.claude/settings.local.json` (ustawienia lokalne): tylko dla Ciebie i tylko w tym projekcie, <!-- fakt: hook-miejsce-ustawienia-lokalne -->
- `~/.claude/settings.json`: we wszystkich Twoich projektach, <!-- fakt: hook-miejsce-folder-albo-komputer -->
- wtyczka: hooki z jej pliku `hooks/hooks.json` działają, gdy wtyczka jest włączona, <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona -->
- skill: od chwili, gdy ktoś uruchomi ten skill (Ty albo Claude), do końca sesji, <!-- fakt: hook-w-skillu-od-uruchomienia-do-konca-sesji -->
- subagent: tylko wtedy, gdy ten subagent działa. <!-- fakt: hook-w-subagencie-tylko-gdy-dziala -->

Znak `~` (tylda) to Twój folder domowy, jak w lekcji 1. <!-- fakt: ustawienia-tylda-to-folder-domowy --> Na Windowsie `~/.claude` to `%USERPROFILE%\.claude`. <!-- fakt: katalog-domowy-windows -->

Włączona wtyczka jest częścią każdej sesji, nie tylko tych, w których jej używasz. Jej hooki ruszają przy swoich zdarzeniach. <!-- fakt: wtyczka-wlaczona-hooki-w-kazdej-sesji --> Zainstalowane wtyczki leżą w folderze `~/.claude/plugins`. <!-- fakt: wtyczki-w-claude-plugins-nie-kasuj -->

Hooki z różnych plików ustawień sumują się, a nie zastępują jedne drugich. <!-- fakt: hooki-z-roznych-plikow-sumuja-sie --> Hooki włączonej wtyczki łączą się z hookami z Twoich ustawień i z ustawień projektu. <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona -->

Gdy zachodzi zdarzenie, wszystkie pasujące do niego hooki działają równolegle i każdy dochodzi do końca. <!-- fakt: hooki-jednego-zdarzenia-rownolegle-do-konca --> Odmowa jednego hooka nie zatrzymuje pozostałych. <!-- fakt: hooki-jednego-zdarzenia-rownolegle-do-konca -->

Ten sam hook zapisany w kilku plikach ustawień rusza raz. Kopia tego hooka we wtyczce albo w skillu działa osobno. <!-- fakt: hook-ten-sam-w-dwoch-plikach-rusza-raz -->

![Hooki ze wszystkich miejsc działają razem, każdy w swoim zasięgu. Hook w .claude/settings.json w folderze projektu działa tylko w tym projekcie. Hook w .claude/settings.local.json działa tylko dla Ciebie i tylko w tym projekcie. Hook w ~/.claude/settings.json działa we wszystkich Twoich projektach. Hook wtyczki działa, gdy wtyczka jest włączona. Hooki z tych miejsc sumują się. Hook skilla działa od uruchomienia skilla do końca sesji. Hook subagenta działa tylko wtedy, gdy pracuje ten subagent.](obrazy/skad-biora-sie-hooki.png)
<!-- analogia: Hooki działają jak regulaminy. Regulamin firmy obowiązuje we wszystkich jej biurach, regulamin jednego biura tylko w nim, a regulamin wycieczki tylko do jej końca. Wszystkie obowiązują naraz. -->

Hooki skilla i subagenta mają własny czas działania, opisany na rysunku. <!-- fakt: hook-w-skillu-od-uruchomienia-do-konca-sesji --> <!-- fakt: hook-w-subagencie-tylko-gdy-dziala --> Zasada „ten sam hook rusza raz” dotyczy tylko kilku plików ustawień, a kopia hooka w skillu działa osobno. <!-- fakt: hook-ten-sam-w-dwoch-plikach-rusza-raz -->

Aplikacja czyta te same pliki ustawień co program w terminalu. <!-- fakt: aplikacja-czyta-te-same-ustawienia-co-terminal -->

### Co Ci daje znajomość miejsc

Wiesz, gdzie szukać i o co zapytać Claude. Wiesz też, że hook z folderu biura nie wyłącza hooka z Twojego folderu domowego, bo hooki z obu plików się sumują. <!-- fakt: hooki-z-roznych-plikow-sumuja-sie -->

### Na co uważać

- Plik `~/.claude/settings.json` leży poza folderem biura, w Twoim folderze domowym. <!-- fakt: ustawienia-tylda-to-folder-domowy --> Claude w ćwiczeniu go nie przeczytał, więc nie opisał jego hooków.
- `~/.claude.json` to inny plik niż `~/.claude/settings.json`. Claude Code pomija hooki wpisane do `~/.claude.json`. <!-- fakt: hooki-tylko-w-settings-json -->
- Skille poznasz w module 4, a subagentów w module 9. Tu wystarczy Ci wiedzieć, kiedy działają ich hooki.

## Czy hook naprawdę rusza

### Po co to sprawdzać

Hook działa poza rozmową, więc Claude nie dostaje znaku, że hook ruszył. <!-- fakt: hook-dziala-poza-rozmowa --> Przy większości zdarzeń hook pilnujący zasad ze złą ścieżką do swojego skryptu przepuszcza wszystko. <!-- fakt: hook-blad-zwykle-nie-zatrzymuje-dzialania --> Nikt Ci o tym nie powie w rozmowie, a Ty liczysz na zasadę, której nikt nie pilnuje.

### Jak działa wynik hooka

Gdy hook zadziała, Claude Code nic nie pokazuje w rozmowie. Po skutku hooka sprawdzasz, czy ruszył. <!-- fakt: hook-sukces-nic-w-rozmowie --> Skutkiem hooka dziennika jest nowe polecenie dopisane do pliku `~/.claude/command-log.txt`. <!-- fakt: hook-przyklad-dziennik-polecen-bash -->

Hook kończy się na jeden z trzech sposobów: <!-- fakt: hook-trzy-wyniki-sukces-blokada-blad -->

- sukces: działanie idzie dalej, chyba że hook je zablokuje,
- błąd blokujący: na zdarzeniach, które mogą blokować, Claude Code zatrzymuje działanie,
- błąd nieblokujący, na przykład gdy hook się nie uruchomi: działanie zwykle idzie dalej. Dokumentacja opisuje wtedy notkę o błędzie hooka przy zdarzeniach takich jak `PreToolUse` (przed użyciem narzędzia).

![Błąd blokujący zatrzymuje działanie, a inny błąd hooka zwykle je przepuszcza. Gdy hook zadziała, w rozmowie nic nie widać. Wtedy sprawdzasz jego skutek. Błąd blokujący zatrzymuje działanie na zdarzeniach, które mogą blokować. Przy błędzie nieblokującym działanie zwykle idzie dalej. Przy zdarzeniach takich jak PreToolUse pojawia się wtedy notka o błędzie hooka. Hook ze złą ścieżką nie rusza wcale. Przy większości zdarzeń działanie i tak idzie dalej.](obrazy/zadzialal-czy-padl.png)

Przy większości zdarzeń hook, który padnie albo przekroczy limit czasu, nie zatrzymuje działania. <!-- fakt: hook-blad-zwykle-nie-zatrzymuje-dzialania --> Literówka w ścieżce w `settings.json` sprawia, że hook nigdy nie rusza. <!-- fakt: hook-literowka-w-sciezce-nie-rusza --> Hook, który się nie uruchomi, kończy się błędem nieblokującym. <!-- fakt: hook-trzy-wyniki-sukces-blokada-blad --> Dlatego dokumentacja radzi przy pierwszym uruchomieniu hooka pilnującego zasad wypatrywać notki o błędzie hooka. <!-- fakt: hook-literowka-w-sciezce-nie-rusza -->

Gdy skutku nie widać, poproś Claude o naprawę i nazwij przyczynę, której ma szukać. Najczęstsze przyczyny według dokumentacji:

1. Literówka albo zła wielkość liter w dopasowaniu. Dopasowanie rozróżnia wielkość liter, a nazwy narzędzi zaczynają się wielką literą: Bash, Edit, Write, Read. Z literówką hook po cichu nie rusza. <!-- fakt: hook-dopasowanie-wielkosc-liter-literowka -->
2. Złe zdarzenie. `PreToolUse` zachodzi przed użyciem narzędzia, a `PostToolUse` po nim. <!-- fakt: hook-nie-rusza-sprawdz-zdarzenie -->
3. Hook w złym pliku. Hook tego projektu stoi w `.claude/settings.json`, a hook dla wszystkich Twoich projektów w `~/.claude/settings.json`. <!-- fakt: hook-miejsce-folder-albo-komputer --> Hook tylko dla Ciebie w tym projekcie stoi w `.claude/settings.local.json`. <!-- fakt: hook-miejsce-ustawienia-lokalne --> Claude Code pomija hook wpisany do `~/.claude.json`. <!-- fakt: hooki-tylko-w-settings-json -->
4. Claude Code nie wczytał zmiany. Gdy po kilku sekundach jej nie widać, uruchom sesję ponownie. <!-- fakt: ustawienia-zmiana-nie-dotarla-nowa-sesja -->
5. Przecinek po ostatnim elemencie albo komentarz `//`. Plik ustawień to ścisły JSON, więc taki znak to błąd składni. <!-- fakt: ustawienia-scisly-json-blad-na-starcie -->

Claude Code zgłasza plik z błędem składni jako Settings Error (błąd ustawień) przy następnym starcie. <!-- fakt: ustawienia-scisly-json-blad-na-starcie -->

Czasem błędny jest tylko pojedynczy wpis, na przykład nieznana nazwa zdarzenia hooka. Wtedy Claude Code pomija ten wpis i stosuje resztę pliku. <!-- fakt: ustawienia-settings-warning-pomija-zly-wpis --> Tak działa Settings Warning (ostrzeżenie o ustawieniach). <!-- fakt: ustawienia-settings-warning-pomija-zly-wpis -->

### Co Ci daje sprawdzenie skutku

Wiesz, że cisza w rozmowie nie znaczy, że hook działa. <!-- fakt: hook-sukces-nic-w-rozmowie --> Sprawdzasz skutek, a przy naprawie mówisz Claude, której przyczyny szukać.

### Na co uważać

Hook z poleceniem ma domyślnie limit czasu 600 sekund, czyli 10 minut. Po tym czasie Claude Code go przerywa, a przy większości zdarzeń taki hook nie podejmuje decyzji. <!-- fakt: hook-przekroczony-czas-bez-decyzji -->

Teraz pozbądź się hooka dziennika. W ćwiczeniu zobaczysz, że usunięcie hooka to usunięcie jego wpisu z pliku. <!-- fakt: hook-usun-wpis-z-pliku --> Zobaczysz też, że wyłączenie wszystkich hooków naraz zostawia ich wpisy w pliku. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania --> Obie zmiany w folderze .claude wymagają Twojej zgody. <!-- fakt: accept-edits-sciezki-chronione-pytaja -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

Usunięcie zostawiło w pliku jeden wpis, a wyłączenie zostawiło oba. Przed wyłączeniem folder wrócił do stanu sprzed usunięcia, więc oba hooki znowu były w pliku.

<!-- kolumny -->

#### Usunięty wpis

<!-- podglad: cw2 usun -->

1. Claude usunął z pliku wpis `PostToolUse`. Tak usuwasz hook zapisany w pliku ustawień. <!-- fakt: hook-usun-wpis-z-pliku -->
2. Wpis `Notification` został w pliku.
3. Folder .claude jest chroniony: przed zapisem w nim Claude pyta o zgodę, także w trybie Accept edits. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> <!-- fakt: sciezki-chronione-czym-sa -->

#### Wszystkie wyłączone

<!-- podglad: cw2 wylacz -->

1. Na górze pliku stoi `"disableAllHooks": true` (wyłącz wszystkie hooki). To ustawienie chwilowo wyłącza wszystkie hooki bez usuwania ich wpisów. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania -->
2. Oba wpisy zostały w pliku.
3. Ten zapis też wymagał Twojej zgody. <!-- fakt: accept-edits-sciezki-chronione-pytaja -->

Po tym zapisie przestają działać hooki:

- z Twoich ustawień,
- z ustawień projektu,
- z ustawień lokalnych,
- z wtyczek. <!-- fakt: disableallhooks-zasieg-poza-ustawieniami-organizacji -->

<!-- /kolumny -->

Jednego hooka nie wyłączysz tak, żeby został w pliku. <!-- fakt: hook-nie-wylaczysz-pojedynczego --> Masz dwie drogi: usunąć jego wpis albo wyłączyć wszystkie hooki naraz.

W panelu plików aplikacji plik `.claude/settings.json` jest tylko do odczytu. <!-- fakt: aplikacja-reczna-edycja-pliku-w-panelu-files --> Dlatego zmianę w nim zlecasz Claude.

## Usuwanie i wyłączanie

### Po co usuwać hook

W folderze biura był hook, którego nie pamiętasz. Po każdym poleceniu terminala, które uruchamia Claude, dopisuje to polecenie do pliku w Twoim folderze domowym. <!-- fakt: hook-przyklad-dziennik-polecen-bash --> Chcesz się go pozbyć, a powiadomienie zostawić.

### Jak usuwasz i wyłączasz hooki

- Żeby usunąć hook z pliku ustawień, usuń jego wpis z tego pliku. <!-- fakt: hook-usun-wpis-z-pliku -->
- W aplikacji o usunięcie wpisu prosisz Claude. Claude ma narzędzia do zmiany plików. <!-- fakt: claude-code-tworzy-nowe-pliki -->
- Folder .claude projektu jest chroniony: przed zapisem w nim Claude pyta o zgodę, także w trybie Accept edits. <!-- fakt: accept-edits-sciezki-chronione-pytaja -->
- Folder `~/.claude` też jest chroniony. W trybach Manual (ręczny) i Accept edits Claude pyta o zgodę przed zapisem w nim, poza kilkoma wyjątkami. <!-- fakt: claude-domowy-chroniony-z-wyjatkami -->
- Zmiana w pliku ustawień, także w hookach, zwykle działa bez ponownego uruchamiania sesji. <!-- fakt: ustawienia-przeladowanie-bez-restartu-hooki -->
- `"disableAllHooks": true` chwilowo wyłącza wszystkie hooki bez usuwania ich wpisów. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania -->

Ustawienie `disableAllHooks` wyłącza hooki:

- z Twoich ustawień,
- z ustawień projektu,
- z ustawień lokalnych,
- z wtyczek. <!-- fakt: disableallhooks-zasieg-poza-ustawieniami-organizacji -->

Hooki wtyczki działają tylko wtedy, gdy wtyczka jest włączona. <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona --> Wtyczkę wyłączysz w aplikacji tak: <!-- fakt: aplikacja-manage-plugins -->

1. W sesji lokalnej (w aplikacji: This computer) kliknij **+** obok pola wiadomości. <!-- fakt: aplikacja-rzad-pod-polem-folder-z-nazwa-kadr -->
2. Wybierz **Plugins** (wtyczki).
3. Wybierz **Manage plugins** (zarządzaj wtyczkami). Tam włączysz, wyłączysz albo odinstalujesz wtyczkę.

### Co Ci daje usuwanie i wyłączanie

Usuwasz jeden hook, a wpisy pozostałych zostają w pliku. <!-- fakt: hook-usun-wpis-z-pliku --> Albo chwilowo wyłączasz wszystkie hooki i nie tracisz ich wpisów. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania -->

### Na co uważać

- `disableAllHooks` wyłącza też hooki, których potrzebujesz, na przykład powiadomienie z lekcji 1. Hooki ustawione przez organizację działają dalej. <!-- fakt: disableallhooks-zasieg-poza-ustawieniami-organizacji -->
- Polecenie `/goal` nie działa, gdy hooki są wyłączone. <!-- fakt: disableallhooks-goal-nie-dziala --> To polecenie poznasz w module 8.
- Nie usuwaj ręcznie pliku `~/.claude/settings.json` ani folderu `~/.claude/plugins`. Trzymają Twoje ustawienia i zainstalowane wtyczki. <!-- fakt: wtyczki-w-claude-plugins-nie-kasuj -->

## Cudze hooki

### Po co sprawdzać cudze hooki

Dostajesz folder od grafika albo instalujesz wtyczkę z katalogu wtyczek. Folder może mieć plik `.claude/settings.json` z hookami, które działają w tym projekcie. <!-- fakt: hook-miejsce-folder-albo-komputer --> Wtyczka dodaje do Claude Code między innymi swoje hooki. <!-- fakt: wtyczka-dodaje-hooki -->

### Jak działają cudze hooki

- Hook z poleceniem działa z pełnymi uprawnieniami Twojego konta, także wtedy, gdy napisał go ktoś inny. <!-- fakt: hook-pelne-uprawnienia-konta -->
- Włączona wtyczka jest częścią każdej sesji. Wszystko, co uruchamia, uruchamia jako Ty. <!-- fakt: wtyczka-wlaczona-hooki-w-kazdej-sesji -->
- Hook na zdarzeniu `PermissionRequest` (prośba o zgodę) rusza, gdy Claude Code ma Cię zapytać o zgodę. Może odpowiedzieć na to pytanie w Twoim imieniu. <!-- fakt: hook-permissionrequest-odpowiada-za-ciebie --> Z pustym dopasowaniem zatwierdzałby każde pytanie o zgodę, także na zapis plików i polecenia. <!-- fakt: hook-permissionrequest-odpowiada-za-ciebie -->

### Co Ci daje sprawdzenie

Dokumentacja radzi przejrzeć polecenia hooka, zanim go dodasz. <!-- fakt: hook-pelne-uprawnienia-konta --> Cudzy folder sprawdzisz tak jak w ćwiczeniu 1: zapytasz Claude o hooki i przeczytasz plik ustawień. Hook, któremu nie ufasz, usuniesz tak jak w ćwiczeniu 2.

### Na co uważać

- Hooki wtyczki leżą w jej pliku `hooks/hooks.json`. W pliku ustawień folderu ich nie znajdziesz. <!-- fakt: hooki-tylko-w-settings-json --> Wyłączasz je razem z wtyczką w Manage plugins. <!-- fakt: aplikacja-manage-plugins -->
- Ta lekcja nie uczy budowy hooka `PermissionRequest`. Gdy zobaczysz to zdarzenie w cudzym pliku, zapytaj Claude, na jakie pytania hook odpowiada za Ciebie.

## Kiedy usuwać hook, a kiedy nie

<!-- kolumny -->

#### Usuń albo wyłącz

1. Gdy nie wiesz, co hook robi, albo mu nie ufasz. Jego polecenie działa z pełnymi uprawnieniami Twojego konta. <!-- fakt: hook-pelne-uprawnienia-konta -->
2. Gdy hook przyszedł z wtyczki: wtedy wyłącz wtyczkę w Manage plugins. <!-- fakt: aplikacja-manage-plugins --> <!-- fakt: hook-wtyczka-dziala-gdy-wlaczona -->
3. Gdy chcesz na chwilę wyłączyć wszystkie hooki: `disableAllHooks` zostawia ich wpisy w pliku. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania -->

#### Zostaw

1. Gdy hook daje powiadomienie, którego potrzebujesz, jak hook z lekcji 1.
2. Gdy hook pilnuje Twojej zasady, jak hook z lekcji 2.
3. Gdy pozostałe hooki mają działać dalej. Wtedy usuń tylko wpis zbędnego hooka, <!-- fakt: hook-usun-wpis-z-pliku --> bo `disableAllHooks` wyłącza wszystkie. <!-- fakt: disableallhooks-wylacza-wszystkie-bez-usuwania -->

<!-- /kolumny -->

## Źródła

- [Automatyzacja z hookami](https://code.claude.com/docs/en/hooks-guide)
- [Hooki: opis szczegółowy](https://code.claude.com/docs/en/hooks)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Pliki ustawień](https://code.claude.com/docs/en/settings)
- [Wszystkie ustawienia](https://code.claude.com/docs/en/settings-reference)
- [Gdy ustawienia nie działają](https://code.claude.com/docs/en/debug-your-config)
- [Folder .claude](https://code.claude.com/docs/en/claude-directory)
- [Wtyczki: przegląd](https://code.claude.com/docs/en/plugins/overview)
- [Instalacja wtyczek](https://code.claude.com/docs/en/plugins/install)
- [Narzędzia Claude Code](https://code.claude.com/docs/en/tools-reference)
- [Rozszerzanie Claude Code](https://code.claude.com/docs/en/features-overview)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
