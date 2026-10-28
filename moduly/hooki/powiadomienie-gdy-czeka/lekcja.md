<em>Przewodnik po Claude Code · Moduł 7: Hooki: powiadomienia i pilnowanie Twoich zasad · Lekcja 1 z 3</em>

# Powiadomienie, gdy Claude czeka na zgodę albo skończył

Zlecasz Claude przegląd 60 opinii klientów i w tym czasie piszesz maile. Co chwilę zaglądasz jednak do okna aplikacji. Czy Claude już skończył? A może stoi i czeka na Twoją zgodę?

Na pierwsze pytanie odpowiada sama aplikacja. Gdy sesja w zakładce Code skończy zadanie, a Ty nie patrzysz akurat na tę sesję, aplikacja wysyła powiadomienie systemowe. <!-- fakt: aplikacja-powiadomienie-o-koncu-zadania --> Tego nie musisz ustawiać.

Na drugie pytanie odpowiada hook. Hook to polecenie, które ustawiasz sam, a Claude Code uruchamia je w określonych chwilach pracy. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu --> Jedna z tych chwil to zdarzenie Notification (powiadomienie). Claude Code wysyła je, gdy Claude czeka na Twoją odpowiedź albo zgodę. <!-- fakt: hook-notification-gdy-claude-czeka --> Hook reaguje na to zdarzenie zawsze, a nie wtedy, gdy model sam o tym pomyśli. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->

![Koniec zadania zgłasza sama aplikacja, a czekanie na zgodę zgłasza hook. Gdy Claude skończy zadanie, a Ty nie patrzysz na tę sesję, aplikacja sama wysyła powiadomienie. Gdy Claude czeka na zgodę, po około sześciu sekundach hook z pliku .claude/settings.json uruchamia Twoje polecenie.](obrazy/dwa-sygnaly.png)

W ćwiczeniu niżej hook już leży w folderze z opiniami. Poproś Claude, żeby napisał wnioski i spakował pliki dla zarządu. Zobaczysz, że gdy Claude czeka na Twoją zgodę, po około sześciu sekundach hook sam uruchamia swoje polecenie. <!-- fakt: hook-aplikacja-permission-prompt-po-szesciu-sekundach --> Praca rusza dopiero po kliknięciu ptaszka.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Pakowanie ze zgodą

<!-- podglad: cw1 czekaj -->

1. Pytanie o zgodę czekało około sześciu sekund. Wtedy hook z pliku .claude/settings.json uruchomił swoje polecenie. <!-- fakt: hook-aplikacja-permission-prompt-po-szesciu-sekundach -->
2. Hook uruchamia polecenie powłoki, czyli polecenie takie jak w terminalu. <!-- fakt: hook-command-uruchamia-polecenie-powloki --> Ćwiczenie nie rysuje skutku tego polecenia: zobaczysz go dopiero na swoim komputerze.
3. Żeby przygotować paczkę, Claude potrzebował polecenia zip, które pakuje pliki w archiwum. <!-- fakt: polecenie-zip-pakuje-pliki --> W aplikacji Accept edits sam przyjmuje zmiany plików i typowe polecenia na plikach. O inne polecenia, takie jak zip, pyta. <!-- fakt: accept-edits-aplikacja-pyta-o-inne-polecenia -->
4. Claude nie wspomniał o hooku, bo hook działa poza rozmową. <!-- fakt: hook-dziala-poza-rozmowa -->

#### Wnioski bez pytania

1. Claude przeczytał opinie i szablon, a potem zapisał wnioski w nowym pliku. <!-- fakt: claude-code-tworzy-nowe-pliki -->
2. Nie pytał o zgodę, bo był włączony tryb Accept edits (przyjmowanie zmian). W tym trybie Claude tworzy i zmienia pliki w folderze bez pytania. <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania -->

<!-- /kolumny -->

Hook leżał w folderze, zanim zaczęła się rozmowa. Hooki zapisane w plikach ustawień działają i w aplikacji, i w terminalu. <!-- fakt: aplikacja-hooki-z-ustawien-dzialaja -->

## Co to jest hook

### Po co jest hook

Możesz poprosić Claude w wiadomości: „daj mi znać, gdy czekasz”. Wtedy jednak wszystko zależy od tego, czy Claude sam zdecyduje się to zrobić. Hook od tego nie zależy: Claude Code uruchamia go zawsze w ustalonej chwili. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->

Dokumentacja radzi prosto: gdy coś ma się dziać za każdym razem, bez proszenia, napisz hook. <!-- fakt: hook-gdy-cos-ma-sie-dziac-zawsze -->

### Jak działa hook

Hook zapisujesz w pliku ustawień, w bloku `hooks`. <!-- fakt: hook-blok-hooks-w-pliku-ustawien --> Zapis ma trzy poziomy: <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->

1. zdarzenie, na które hook reaguje,
2. dopasowanie (`matcher`), które zawęża, kiedy hook rusza,
3. hook (wpis z typem i poleceniem), który się wtedy uruchamia.

W tej lekcji używasz tylko jednego zdarzenia: `Notification`. Rodzaje chwil i pięć zdarzeń niżej to mapa na później.

Zdarzenia zachodzą w trzech rodzajach chwil: <!-- fakt: hook-trzy-rytmy-zdarzen -->

- raz na sesję,
- raz na wiadomość,
- przy każdym użyciu narzędzia.

Narzędzia to wbudowane czynności Claude Code, na przykład: <!-- fakt: claude-code-tworzy-nowe-pliki -->

- czytanie plików,
- tworzenie nowych plików,
- zmiana plików.

Na początek wystarczy Ci pięć zdarzeń:

- `SessionStart`: sesja się zaczyna albo wznawia, <!-- fakt: zdarzenie-sessionstart-kiedy -->
- `PreToolUse`: Claude zaraz użyje narzędzia; hook może to zablokować, <!-- fakt: zdarzenie-pretooluse-kiedy -->
- `PostToolUse`: Claude użył narzędzia i się udało, <!-- fakt: zdarzenie-posttooluse-kiedy -->
- `Notification`: Claude Code wysyła powiadomienie, <!-- fakt: zdarzenie-notification-kiedy -->
- `Stop`: Claude kończy odpowiadać. <!-- fakt: zdarzenie-stop-kiedy -->

Te same zdarzenia zachodzą w terminalu, w aplikacji Claude na komputer i w sesjach w chmurze. <!-- fakt: hooki-te-same-zdarzenia-takze-w-aplikacji -->

### Co Ci daje hook

Hook reaguje tak samo za każdym razem. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu --> Dokumentacja podaje przykłady, do czego służą hooki: <!-- fakt: hook-zastosowania -->

- formatują pliki po zmianach,
- blokują polecenia, zanim się wykonają,
- wysyłają powiadomienie, gdy Claude potrzebuje Twojej odpowiedzi,
- dokładają informacje na starcie sesji.

Ta lekcja zajmuje się powiadomieniem. Hooki, które pilnują Twoich zasad, poznasz w lekcji 2.

### Czego hook nie robi

Hook działa poza rozmową i domyślnie nic do niej nie wnosi. <!-- fakt: hook-dziala-poza-rozmowa --> Dlatego Claude nie dostaje znaku, że hook ruszył. <!-- fakt: hook-dziala-poza-rozmowa -->

Hook typu `command`, czyli taki z poleceniem, nie uruchomi polecenia zaczynającego się od ukośnika (`/`). <!-- fakt: hook-command-bez-polecen-i-narzedzi --> Nie użyje też narzędzi Claude Code. <!-- fakt: hook-command-bez-polecen-i-narzedzi -->

Hook to inny sposób rozszerzania Claude Code niż skill, subagent i wtyczka. <!-- fakt: hook-inne-rozszerzenia-skille-subagenci-wtyczki --> Skille i wtyczki poznasz w module 4, a subagentów w module 9.

## Zdarzenie: Claude czeka na zgodę

### Po co jest to zdarzenie

Zlecasz pracę na kilka minut i robisz coś innego. W tym czasie Claude chce uruchomić polecenie i pyta o zgodę. <!-- fakt: accept-edits-aplikacja-pyta-o-inne-polecenia --> Ty o tym nie wiesz, więc zadanie stoi.

### Jak działa zdarzenie

Hook z ćwiczenia reaguje na zdarzenie `Notification`. Claude Code wysyła je, gdy Claude czeka na Twoją odpowiedź albo zgodę. <!-- fakt: hook-notification-gdy-claude-czeka -->

Powiadomienia mają kilka typów. Dopasowanie wybiera, przy którym typie hook ruszy: <!-- fakt: hook-notification-pusty-matcher-wszystkie-typy -->

- puste dopasowanie: przy każdym typie powiadomienia, <!-- fakt: hook-notification-pusty-matcher-wszystkie-typy -->
- `permission_prompt` (pytanie o zgodę): gdy Claude potrzebuje Twojej zgody na użycie narzędzia, a pytanie czeka około sześciu sekund. <!-- fakt: hook-permission-prompt-czeka-szesc-sekund -->

W aplikacji Claude na komputer `permission_prompt` zachodzi około sześciu sekund po tym, jak Claude poprosi o zgodę. <!-- fakt: hook-aplikacja-permission-prompt-po-szesciu-sekundach --> Gdy w tym czasie piszesz, nie opóźniasz go. <!-- fakt: hook-aplikacja-permission-prompt-po-szesciu-sekundach -->

### Co Ci daje to zdarzenie

Wracasz do okna wtedy, gdy Claude naprawdę na Ciebie czeka. Hook rusza tylko wtedy, gdy pytanie o zgodę czeka na Twoją odpowiedź około sześciu sekund. <!-- fakt: hook-permission-prompt-czeka-szesc-sekund -->

### Na co uważać

Gdy odpowiesz na pytanie przed upływem tych około sześciu sekund, hook nie ruszy. <!-- fakt: hook-aplikacja-odpowiedz-szybciej-bez-powiadomienia --> W ćwiczeniu ptaszek był nieaktywny, dopóki ten czas nie minął.

![Hook z permission_prompt rusza dopiero, gdy pytanie o zgodę czeka około 6 sekund. Gdy odpowiesz na pytanie o zgodę przed upływem około sześciu sekund, hook nie rusza. Gdy pytanie czeka około sześciu sekund bez odpowiedzi, hook rusza. Pisanie w aplikacji nie przesuwa tej chwili.](obrazy/szesc-sekund.png)

Do powiadomienia wystarczy Ci `permission_prompt`. Inne zdarzenie, `PermissionRequest` (prośba o zgodę), daje sygnał już w chwili pytania. <!-- fakt: hook-permissionrequest-sygnal-od-razu --> Hook z `permission_prompt` rusza dopiero po około sześciu sekundach czekania. <!-- fakt: hook-permissionrequest-sygnal-od-razu -->

Hook z ćwiczenia ma dopasowanie `permission_prompt`, a nie puste, bo ma się odzywać tylko przy pytaniu o zgodę. <!-- fakt: hook-notification-pusty-matcher-wszystkie-typy --> Puste dopasowanie łapie też typ `idle_prompt` (bezczynność po odpowiedzi). Według dokumentacji zachodzi on około 60 sekund po tym, jak Claude skończył odpowiadać, jeśli od tego czasu nic nie piszesz. <!-- fakt: hook-idle-prompt-minuta-po-odpowiedzi -->

Gdy hook w aplikacji nie rusza, sprawdź wersję Claude Code. W aplikacji `permission_prompt` zachodzi dopiero od Claude Code w wersji 2.1.233. <!-- fakt: hook-aplikacja-permission-prompt-od-2-1-233 --> Wersję sprawdzisz tak: <!-- fakt: aplikacja-wersja-claude-code-status -->

1. W zakładce Code, w sesji lokalnej, wpisz `/status`.
2. Przeczytaj wiersz Claude Code.
3. Gdy wersja jest starsza niż 2.1.233, wybierz Claude > Check for Updates… (sprawdź aktualizacje) na Macu albo Help > Check for Updates… na Windowsie.
4. Zacznij nową sesję.

Hooka na koniec zadania nie potrzebujesz. Aplikacja sama powiadamia, gdy sesja skończy zadanie, a Ty nie patrzysz na tę sesję. <!-- fakt: aplikacja-powiadomienie-o-koncu-zadania --> Zdarzenie `Stop` (koniec odpowiedzi) tu nie pomoże. Hook `Stop` rusza po każdej odpowiedzi Claude, a nie tylko po końcu zadania. <!-- fakt: hook-stop-po-kazdej-odpowiedzi -->

Teraz dodaj taki hook: poproś o niego Claude zwykłymi słowami. Zobaczysz, że z krótkiej prośby Claude robi plik .claude/settings.json w folderze. <!-- fakt: claude-code-tworzy-nowe-pliki --> Ten zapis wymaga Twojej zgody. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> W pliku przeczytasz, kiedy hook rusza i co uruchamia. <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Trzy rzeczy w pliku

<!-- podglad: cw2 dodaj-hook -->

1. `"Notification"`: zdarzenie, na które hook reaguje. <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->
2. `"matcher": "permission_prompt"`: dopasowanie. Hook rusza, gdy pytanie o zgodę czeka około sześciu sekund. <!-- fakt: hook-permission-prompt-czeka-szesc-sekund -->
3. `"type": "command"` i `"command"`: polecenie, które hook uruchamia. <!-- fakt: hook-command-uruchamia-polecenie-powloki -->

#### Zapis za Twoją zgodą

1. Prosisz zwykłymi słowami. Pliku nie piszesz sam. <!-- fakt: hook-prosba-do-claude-w-terminalu --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
2. Folder .claude jest chroniony, więc Claude zapytał o zgodę nawet w trybie Accept edits. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> <!-- fakt: sciezki-chronione-czym-sa -->
3. Po zgodzie w folderze Opinie-kluby pojawił się folder .claude z plikiem settings.json. <!-- fakt: claude-code-tworzy-nowe-pliki -->
4. Kliknięcie ścieżki w odpowiedzi Claude otworzyło plik. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

<!-- /kolumny -->

Dokumentacja podaje taką prośbę dla programu w terminalu: możesz poprosić Claude, żeby napisał hook za Ciebie, gdy opiszesz, czego chcesz. <!-- fakt: hook-prosba-do-claude-w-terminalu --> Aplikacja na komputer działa na tym samym silniku co program w terminalu. <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

W prośbie napisz, na jakim systemie pracujesz. W ćwiczeniu było to „Pracuję na Macu”. Dokumentacja ma osobne przykłady poleceń dla macOS, Linuxa i Windowsa. <!-- fakt: hook-powiadomienie-polecenie-systemu -->

## Polecenie, które hook uruchamia

### Po co jest polecenie

Zdarzenie i dopasowanie mówią, kiedy hook rusza. Potrzebujesz jeszcze polecenia, które coś zrobi na Twoim komputerze. <!-- fakt: hook-command-uruchamia-polecenie-powloki -->

### Jak działa polecenie

Hook typu `command` uruchamia polecenie powłoki, czyli polecenie takie jak w terminalu. Samo polecenie stoi w polu `command`. <!-- fakt: hook-command-uruchamia-polecenie-powloki -->

Dokumentacja ma gotowy hook powiadomienia dla macOS, Linuxa i Windowsa. Każdy używa polecenia powiadomień swojego systemu. <!-- fakt: hook-powiadomienie-polecenie-systemu --> Przykład dla macOS używa polecenia `osascript`. To ono stoi w pliku z ćwiczenia 2. <!-- fakt: hook-powiadomienie-polecenie-systemu -->

Hook `Notification` nie blokuje i nie zmienia powiadomienia. Służy do działań dodatkowych, na przykład do przekazania powiadomienia do innej usługi. <!-- fakt: hook-notification-nie-zmienia-rozmowy -->

### Co Ci daje gotowe polecenie

Nie piszesz polecenia sam. Prosisz Claude i podajesz swój system, a Claude zapisuje hook w pliku. <!-- fakt: hook-prosba-do-claude-w-terminalu --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->

### Na co uważać na Macu

Polecenie `osascript` pokazuje powiadomienia przez wbudowaną aplikację Script Editor. <!-- fakt: hook-macos-script-editor-bez-zgody-cisza --> Gdy Script Editor nie ma zgody na powiadomienia, polecenie nie działa i nic o tym nie mówi. macOS sam o tę zgodę nie zapyta. <!-- fakt: hook-macos-script-editor-bez-zgody-cisza -->

Dokumentacja podaje, jak to naprawić: jedno polecenie w programie Terminal i jedna zmiana w ustawieniach systemu. To jedyny krok w terminalu w tej lekcji. Polecenie testowe sprawia, że Script Editor pojawi się w ustawieniach powiadomień. <!-- fakt: hook-macos-naprawa-zgody-script-editor -->

1. Otwórz program Terminal, wklej polecenie testowe `osascript -e 'display notification "test"'` i naciśnij Enter. Na razie nic się nie pokaże.
2. Otwórz Ustawienia systemowe > Powiadomienia (System Settings > Notifications).
3. Znajdź na liście Script Editor i włącz zezwolenie na powiadomienia (Allow Notifications).
4. Uruchom polecenie testowe jeszcze raz i sprawdź, czy powiadomienie testowe się pojawia.

### Na co uważać na Windowsie

Przykład z dokumentacji dla Windowsa otwiera okno dialogowe, a nie powiadomienie w rogu ekranu. Dokumentacja ostrzega, że takie okno może się otworzyć za oknem terminala. <!-- fakt: hook-windows-okno-dialogowe-za-oknem -->

Gdy na Windowsie nie masz programu Git Bash, hook typu `command` domyślnie uruchamia polecenie w PowerShell. <!-- fakt: hook-windows-bez-git-bash-powershell -->

### Claude nie sprawdzi polecenia

Claude nie wie, czy polecenie hooka zadziałało, bo hook działa poza rozmową. <!-- fakt: hook-dziala-poza-rozmowa --> Gdy powiadomienie się nie pojawia, sprawdź ustawienia powiadomień swojego systemu.

## Gdzie leży hook i gdzie obowiązuje

### Po co wybierać miejsce

Hook dla jednego klienta nie powinien się odzywać przy pracy dla innego. Inny hook, na przykład powiadomienie o zgodzie, przyda Ci się przy każdej pracy. O tym decyduje plik, w którym hook leży. <!-- fakt: hook-miejsce-folder-albo-komputer -->

### Jak działa miejsce hooka

Miejsce hooka wyznacza, gdzie hook działa: <!-- fakt: hook-miejsce-folder-albo-komputer -->

- `.claude/settings.json` w folderze projektu: hook działa tylko w tym projekcie,
- `~/.claude/settings.json`: hook działa we wszystkich Twoich projektach.

Znak `~` (tylda) oznacza Twój folder domowy. `~/.claude` to folder .claude w folderze domowym, a samo `.claude` to folder w projekcie. <!-- fakt: ustawienia-tylda-to-folder-domowy --> Na Windowsie `~/.claude` to `%USERPROFILE%\.claude`, czyli folder .claude w Twoim folderze użytkownika. <!-- fakt: katalog-domowy-windows -->

![Hook z projektu działa tylko w nim, a hook z folderu domowego we wszystkich Twoich projektach. Hook w .claude/settings.json folderu Opinie-kluby działa tylko w tym projekcie. Hook w ~/.claude/settings.json działa we wszystkich Twoich projektach. Hooki z obu plików sumują się.](obrazy/gdzie-lezy-hook.png)

Aplikacja czyta te same pliki ustawień co program w terminalu. <!-- fakt: aplikacja-czyta-te-same-ustawienia-co-terminal -->

Zapis w folderze .claude jest chroniony. W trybach Manual (ręczny) i Accept edits wymaga Twojej zgody. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> Dokumentacja wyjaśnia, że to chroni ustawienia Claude przed przypadkowym zepsuciem. <!-- fakt: sciezki-chronione-czym-sa --> Folder `~/.claude` też jest chroniony: w tych trybach Claude zapyta o zgodę przed zapisem w nim, poza kilkoma wyjątkami. <!-- fakt: claude-domowy-chroniony-z-wyjatkami -->

Zmiany w pliku ustawień, także w hookach, zwykle działają bez ponownego uruchamiania sesji. <!-- fakt: ustawienia-przeladowanie-bez-restartu-hooki --> Dotyczy to też pliku w folderze .claude, nawet gdy ten folder powstał w tej samej sesji. <!-- fakt: ustawienia-przeladowanie-bez-restartu-hooki -->

### Co Ci daje miejsce hooka

Hook z folderu jednego klienta nie włączy się w folderze innego klienta. <!-- fakt: hook-miejsce-folder-albo-komputer --> Hook, który ma działać we wszystkich Twoich projektach, zapisujesz raz w `~/.claude/settings.json`. <!-- fakt: hook-miejsce-folder-albo-komputer -->

### Na co uważać

W panelu plików aplikacji plik `.claude/settings.json` jest tylko do odczytu. <!-- fakt: aplikacja-reczna-edycja-pliku-w-panelu-files --> Dlatego o zmianę w tym pliku prosisz Claude.

Gdy plik ma już hooki, nowe zdarzenie dopisuje się obok nich. Nie zastępuje całego bloku. <!-- fakt: hook-nowe-zdarzenie-obok-istniejacych -->

Gdy zmiana w pliku ustawień nie działa po kilku sekundach, Claude Code mógł jej nie zauważyć. <!-- fakt: ustawienia-zmiana-nie-dotarla-nowa-sesja --> Wtedy uruchom sesję ponownie. <!-- fakt: ustawienia-zmiana-nie-dotarla-nowa-sesja -->

Sesje w chmurze nie czytają pliku `~/.claude/settings.json` z Twojego komputera. Hooki z tego pliku nie działają więc w sesjach w chmurze. <!-- fakt: hooki-chmura-nie-czyta-domowych-ustawien -->

Hooki z pliku w folderze projektu i z pliku w folderze domowym sumują się, a nie zastępują jedne drugich. <!-- fakt: hooki-z-roznych-plikow-sumuja-sie --> Jak przejrzeć i usunąć hooki, pokaże lekcja 3.

## Kiedy dodawać hook na pytanie o zgodę, a kiedy nie

<!-- kolumny -->

#### Dodaj hook

1. Gdy zlecasz długie zadanie z poleceniami, o które aplikacja pyta także w Accept edits, jak zip w ćwiczeniu 1. <!-- fakt: accept-edits-aplikacja-pyta-o-inne-polecenia -->
2. Gdy w tym czasie robisz coś innego i nie patrzysz na okno aplikacji.
3. W folderze klienta, gdy hook ma działać tylko tam. W `~/.claude/settings.json`, gdy ma działać we wszystkich Twoich projektach. <!-- fakt: hook-miejsce-folder-albo-komputer -->

#### Nie dodawaj hooka

1. Gdy patrzysz na okno aplikacji i odpowiadasz od razu. Gdy odpowiesz przed upływem około sześciu sekund, hook i tak nie ruszy. <!-- fakt: hook-aplikacja-odpowiedz-szybciej-bez-powiadomienia -->
2. Gdy chcesz wiedzieć tylko, że Claude skończył. O tym aplikacja powiadamia sama. <!-- fakt: aplikacja-powiadomienie-o-koncu-zadania -->
3. Gdy masz Claude Code w wersji starszej niż 2.1.233, bo wtedy w aplikacji `permission_prompt` nie zachodzi. <!-- fakt: hook-aplikacja-permission-prompt-od-2-1-233 --> Najpierw zaktualizuj aplikację. <!-- fakt: aplikacja-wersja-claude-code-status -->

<!-- /kolumny -->

## Źródła

- [Automatyzacja z hookami](https://code.claude.com/docs/en/hooks-guide)
- [Hooki: opis szczegółowy](https://code.claude.com/docs/en/hooks)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Pliki ustawień](https://code.claude.com/docs/en/settings)
- [Rozszerzanie Claude Code](https://code.claude.com/docs/en/features-overview)
- [Folder .claude](https://code.claude.com/docs/en/claude-directory)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)
- [Polecenie zip: opis](https://manpages.debian.org/unstable/zip/zip.1.en.html)

Sprawdzone 23–26.10.2026, Claude Code 2.1.309–2.1.310.
