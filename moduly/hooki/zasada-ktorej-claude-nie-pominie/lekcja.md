<em>Przewodnik po Claude Code · Moduł 7: Hooki: powiadomienia i pilnowanie Twoich zasad · Lekcja 2 z 3</em>

# Zasada, której Claude nie pominie

Piszesz teksty dla klienta, szkoły językowej z kilkoma oddziałami. Klient zakazuje w tych tekstach słów „promocja”, „rabat” i „okazja”. Wpisujesz ten zakaz do CLAUDE.md, a post piszesz z notatek sekretariatu, w których stoi „rabat 10%”.

CLAUDE.md wczytuje się na początku każdej rozmowy. <!-- fakt: claude-md-i-notatki-wczytane-na-start-rozmowy --> Claude czyta go i stara się stosować zasady, ale nie ma gwarancji, że zastosuje każdą. <!-- fakt: claude-md-bez-gwarancji-stosowania --> Dokumentacja nazywa taką zasadę prośbą, a nie gwarancją. Zasadę, która ma obowiązywać za każdym razem, radzi zapisać w hooku. <!-- fakt: claude-md-prosba-hook-egzekwowanie -->

Hook znasz z lekcji 1: Claude Code uruchamia go sam w ustalonej chwili, a nie wtedy, gdy model o nim pomyśli. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu --> W tej lekcji hook nie uruchamia polecenia. Wysyła Twoją zasadę i dane o zapisie pliku do modelu Claude, a model ocenia tekst. <!-- fakt: hook-prompt-osad-modelu --> Gdy model uzna, że tekst łamie zasadę, podaje powód. <!-- fakt: hook-prompt-odpowiedz-ok-i-powod -->

W tym hooku powód wraca do Claude, a Claude pracuje dalej. Tak działa dzięki ustawieniu `continueOnBlock`. <!-- fakt: hook-prompt-posttooluse-continueonblock --> Hook sprawdzi każdy plik zapisany narzędziem do zapisu albo edycji. <!-- fakt: hook-dopasowanie-edit-write --> Dokumentacja nie obiecuje jednak, że model złapie każde zakazane słowo. <!-- fakt: hook-prompt-osad-modelu -->

W ćwiczeniu niżej hook już leży w folderze z tekstami dla szkoły. Zleć post o naborze i nie wspominaj o zasadzie. Zobaczysz, że po zapisie Claude sam mówi o uwadze i oddaje post bez zakazanego słowa. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Post po sprawdzeniu

<!-- podglad: cw1 post -->

1. Claude zapisał post bez pytania, bo działa tryb Accept edits (przyjmowanie zmian). <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania -->
2. Zaraz po zapisie ruszył hook. <!-- fakt: zdarzenie-posttooluse-kiedy --> Wysłał zasadę i dane zapisu do modelu. <!-- fakt: hook-prompt-wysyla-zasade-i-dane-do-modelu -->
3. Model odmówił i podał powód: w tekście jest „rabat”. <!-- fakt: hook-prompt-odpowiedz-ok-i-powod -->
4. Powód wrócił do Claude, a Claude poprawił tekst. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

#### Bez Twojej prośby

1. O zasadzie nikt nie przypominał. Hook ruszył sam, w ustalonej chwili. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->
2. Claude czekał z dalszą pracą, aż hook skończy. <!-- fakt: hook-claude-czeka-na-hook -->
3. Hook leżał w pliku .claude/settings.json. Hooki z plików ustawień działają i w aplikacji, i w terminalu. <!-- fakt: aplikacja-hooki-z-ustawien-dzialaja -->

<!-- /kolumny -->

Domyślnie hook działa poza rozmową i nic do niej nie wczytuje. <!-- fakt: hook-dziala-poza-rozmowa --> Dlatego do Claude wraca tylko powód odmowy, i to dopiero dzięki ustawieniu `continueOnBlock`. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

## Prośba a sprawdzenie

### Po co jest sprawdzenie

Gdy post z „rabatem” trafi do klienta, który zakazał tego słowa, masz wstyd i poprawki. Taka zasada nie może zależeć od tego, czy Claude ją akurat zastosuje. Zasada w CLAUDE.md właśnie od tego zależy: Claude stara się ją stosować, ale bez gwarancji. <!-- fakt: claude-md-bez-gwarancji-stosowania -->

### Jak działa prośba, a jak sprawdzenie

Zasada w CLAUDE.md to prośba:

- CLAUDE.md wczytuje się na początku każdej rozmowy, <!-- fakt: claude-md-i-notatki-wczytane-na-start-rozmowy -->
- Claude traktuje go jako kontekst, a nie wymuszoną konfigurację. <!-- fakt: claude-md-kontekst-nie-wymuszenie -->

Zasada w hooku to sprawdzenie:

- Claude Code uruchamia hook w ustalonej chwili, a nie model z własnej decyzji, <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->
- uprawnienia i hooki pilnują granic bez względu na to, co zdecyduje Claude. <!-- fakt: hooki-egzekwuja-niezaleznie-od-claude -->

![Zasada w CLAUDE.md to prośba: Claude stara się ją stosować, ale bez gwarancji. Zasada w hooku to sprawdzenie po każdym zapisie narzędziem Edit albo Write. Model ocenia zapis na podstawie zasady i danych zapisu. Gdy zapis łamie zasadę, a ustawione jest continueOnBlock: true, powód wraca do Claude i Claude poprawia plik.](obrazy/prosba-czy-sprawdzenie.png)
<!-- wyjasnienie: obrazy/prosba-czy-sprawdzenie-wyjasnienie.png | Zasada w CLAUDE.md to prośba: Claude zwykle jej posłucha, a czasem nie. Zasada w hooku działa jak kłódka, która zatrzymuje złamanie zasady i odsyła Claude do poprawki. -->
<!-- analogia: Zasada w CLAUDE.md jest jak kartka z instrukcją przy taśmie produkcyjnej, a zasada w hooku jak kontroler na końcu taśmy. Kartkę pracownik czyta, ale może o niej zapomnieć. Kontroler ogląda każdą gotową sztukę i odsyła wadliwą do poprawki. -->

### Co Ci daje sprawdzenie

Hook z ćwiczenia rusza za każdym razem, gdy Claude zapisze plik narzędziem Edit albo Write. <!-- fakt: hook-dopasowanie-edit-write --> Nie musisz o nim przypominać. <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->

Dokumentacja radzi prosto: gdy coś ma się dziać za każdym razem, bez proszenia, napisz hook. <!-- fakt: hook-gdy-cos-ma-sie-dziac-zawsze -->

### Na co uważać

CLAUDE.md dalej jest potrzebny. Dokumentacja dzieli zasady tak: <!-- fakt: hooki-egzekwuja-niezaleznie-od-claude -->

- CLAUDE.md na „tak to u nas robimy”, na przykład ton i odbiorcę tekstów,
- uprawnienia i hooki na to, co nie może się zdarzyć nigdy.

Dokumentacja nazywa egzekwowaniem (wymuszeniem zasady) hook, który blokuje zmianę pliku, zanim do niej dojdzie. <!-- fakt: claude-md-prosba-hook-egzekwowanie --> Hook z tej lekcji działa inaczej. Rusza po zapisie, a ocenę wydaje model. <!-- fakt: zdarzenie-posttooluse-kiedy --> <!-- fakt: hook-prompt-osad-modelu --> Sprawdzenie odbędzie się więc przy każdym zapisie narzędziem Edit albo Write. <!-- fakt: hook-dopasowanie-edit-write --> Dokumentacja nie obiecuje jednak, że model złapie każde zakazane słowo. <!-- fakt: hook-prompt-osad-modelu -->

## Zasada zapisana zdaniem: hook typu prompt

### Po co jest hook typu prompt

Zasady z pracy często wymagają osądu. Słowo „rabat” ma odmiany: rabatu, rabatem, rabaty. Do decyzji, które wymagają osądu, a nie sztywnej reguły, dokumentacja wskazuje hook typu `prompt` (zasada zapisana zwykłym zdaniem dla modelu). <!-- fakt: hook-prompt-osad-modelu -->

### Jak działa hook typu prompt

Te szczegóły przydadzą Ci się, gdy będziesz czytać plik z hookiem.

Hook z lekcji 1 uruchamiał polecenie. Hook typu `prompt` działa inaczej: <!-- fakt: hook-prompt-wysyla-zasade-i-dane-do-modelu -->

1. Wysyła dane zdarzenia i Twoją zasadę do modelu Claude.
2. Model odpowiada decyzją.
3. Claude Code sam wykonuje tę decyzję.

Decyzja to pole `ok`. Wartość `true` pozwala na działanie. Przy `false`, czyli przy odmowie, model musi podać powód w polu `reason`. <!-- fakt: hook-prompt-odpowiedz-ok-i-powod --> Co dzieje się po odmowie, zależy od zdarzenia. <!-- fakt: hook-prompt-odpowiedz-ok-i-powod -->

Zasadę piszesz zwykłym zdaniem. Może to być reguła, co zablokować albo przepuścić. Może to być też warunek, który musi być spełniony. <!-- fakt: hook-prompt-zasada-zakaz-albo-warunek -->

Danych zdarzenia nie musisz wklejać. Gdy w zasadzie nie ma znacznika `$ARGUMENTS` (miejsca na dane zdarzenia), Claude Code dokleja dane zdarzenia do zasady. <!-- fakt: hook-prompt-dane-doklejone-do-zasady --> Przy zapisie pliku dane zdarzenia to dane narzędzia: co narzędzie dostało i co zwróciło. <!-- fakt: hook-posttooluse-dostaje-dane-narzedzia -->

W pliku hook typu `prompt` ma takie pola: <!-- fakt: hook-prompt-pola-pliku -->

- `type`: wartość `prompt`,
- `prompt`: Twoja zasada,
- `model`: nieobowiązkowe, inny model do oceny,
- `timeout` (czas na odpowiedź): nieobowiązkowe, w sekundach, domyślnie 30,
- `continueOnBlock` (dosłownie: pracuj dalej po odmowie): nieobowiązkowe; na zdarzeniach, które je obsługują, między innymi `PostToolUse`, `true` oddaje Claude powód odmowy, a praca trwa dalej.

Typ `prompt` to jednorazowa ocena modelem i jeden z pięciu typów hooka. <!-- fakt: hook-piec-typow --> Obok `command` z lekcji 1 są jeszcze `http` i `mcp_tool` dla programistów oraz eksperymentalny `agent`. <!-- fakt: hook-piec-typow -->

### Co Ci daje hook typu prompt

Zasadę zapisujesz zwykłym zdaniem, takim jak w wytycznych klienta. <!-- fakt: hook-prompt-zasada-zakaz-albo-warunek --> Nie potrzebujesz skryptu, czyli osobnego programu, który trzeba napisać.

Druga droga to skrypt. Dokumentacja pokazuje taki hook dla chronionych plików: osobny skrypt porównuje ścieżkę pliku z listą wzorców i blokuje edycję. <!-- fakt: hook-przyklad-skrypt-blokuje-pliki --> To robota dla programisty.

### Na co uważać

- Ocenę wydaje model. To osąd, a nie sztywna reguła. <!-- fakt: hook-prompt-osad-modelu -->
- Hook typu `prompt` wybierasz, gdy do decyzji wystarczą same dane zdarzenia. <!-- fakt: hook-prompt-tylko-dane-zdarzenia --> Hook nie czyta CLAUDE.md ani innych plików folderu. <!-- fakt: hook-prompt-tylko-dane-zdarzenia -->
- Pliki czyta dopiero hook typu `agent`. Ten hook uruchamia subagenta (pomocnika Claude, poznasz go w module 9), który może czytać pliki, zanim zwróci decyzję. <!-- fakt: hook-agent-eksperymentalny-czyta-pliki --> To funkcja eksperymentalna, więc w tym kursie jej nie używamy.
- Claude czeka z dalszą pracą, aż hook skończy. <!-- fakt: hook-claude-czeka-na-hook --> Hook typu `prompt` ma na odpowiedź domyślnie 30 sekund. Ten czas zmienisz polem `timeout`. <!-- fakt: hook-prompt-czas-30-sekund -->
- Nie każde zdarzenie przyjmuje typ `prompt`. `PostToolUse` przyjmuje, a `Notification` z lekcji 1 nie. <!-- fakt: hook-prompt-zdarzenia-tak-nie -->
- Zasadę i dane hook wysyła domyślnie do modelu, którego Claude Code używa do funkcji działających w tle. <!-- fakt: hook-prompt-wysyla-zasade-i-dane-do-modelu -->

Teraz zobacz obie zasady obok siebie. Zobaczysz, że zasada w CLAUDE.md to prośba, którą Claude tym razem pominął. <!-- fakt: claude-md-bez-gwarancji-stosowania --> Tę samą zasadę Claude zapisze jako hook w pliku .claude/settings.json, a ten sam mail, napisany już z hookiem, wyjdzie bez „rabatu”. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Zasada w CLAUDE.md

<!-- podglad: cw2 claude-md -->

1. W folderze nie było hooka. Zasada stała tylko w CLAUDE.md, który wczytał się na początku rozmowy. <!-- fakt: claude-md-i-notatki-wczytane-na-start-rozmowy -->
2. Claude traktuje CLAUDE.md jako kontekst, a nie wymuszoną konfigurację. <!-- fakt: claude-md-kontekst-nie-wymuszenie -->
3. W mailu został „rabat”. Claude stara się stosować CLAUDE.md, ale bez gwarancji. <!-- fakt: claude-md-bez-gwarancji-stosowania -->

#### Zasada w hooku

<!-- podglad: cw2 hook -->

1. Claude zapisał najpierw hook, a potem ten sam mail. Zaraz po zapisie maila ruszył hook. <!-- fakt: zdarzenie-posttooluse-kiedy -->
2. Model uznał, że „rabat” łamie zasadę. Powód wrócił do Claude, a Claude poprawił mail. <!-- fakt: hook-prompt-posttooluse-continueonblock -->
3. Hook działał w tej samej rozmowie, w której Claude go zapisał. <!-- fakt: ustawienia-przeladowanie-bez-restartu-hooki -->

<!-- /kolumny -->

W pliku .claude/settings.json hook ma cztery części:

1. `"PostToolUse"` (po użyciu narzędzia): zdarzenie. Zachodzi po udanym użyciu narzędzia. <!-- fakt: zdarzenie-posttooluse-kiedy -->
2. `"matcher": "Edit|Write"`: dopasowanie. Hook rusza tylko przy narzędziu Edit albo Write. <!-- fakt: hook-dopasowanie-edit-write -->
3. `"type": "prompt"` i `"prompt"`: zasada zapisana zdaniem, którą ocenia model. <!-- fakt: hook-prompt-pola-pliku -->
4. `"continueOnBlock": true`: powód odmowy wraca do Claude, a Claude pracuje dalej. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

Hook w pliku ma te same trzy poziomy co w lekcji 1: <!-- fakt: hook-trzy-poziomy-zdarzenie-dopasowanie-hook -->

- zdarzenie,
- dopasowanie,
- hook.

Folder .claude jest chroniony. <!-- fakt: sciezki-chronione-czym-sa --> Znaczy to, że przed zapisem w nim Claude pyta o Twoją zgodę, także w trybie Accept edits. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> Kliknięcie ścieżki otworzyło plik. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

Poproś Claude, a napisze hook za Ciebie. <!-- fakt: hook-prosba-do-claude-w-terminalu --> Dla programu w terminalu dokumentacja opisuje to wprost. <!-- fakt: hook-prosba-do-claude-w-terminalu --> Aplikacja na komputer działa na tym samym silniku co program w terminalu. <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Hooki z plików ustawień działają i w aplikacji, i w terminalu. <!-- fakt: aplikacja-hooki-z-ustawien-dzialaja --> Claude Code uruchamia w obu te same zdarzenia hooków. <!-- fakt: hooki-te-same-zdarzenia-takze-w-aplikacji -->

Plik leży w folderze .claude tego projektu, więc hook działa tylko w tym projekcie. Hook w `~/.claude/settings.json` (pliku na Twoim komputerze, poza folderem projektu) działałby we wszystkich Twoich projektach. <!-- fakt: hook-miejsce-folder-albo-komputer -->

## Po każdym zapisie: PostToolUse, Edit|Write i continueOnBlock

### Po co jest dopasowanie

Hook ma sprawdzać tekst zapisany w pliku, a nie każdy ruch Claude. Hook bez dopasowania rusza przy każdym wystąpieniu swojego zdarzenia. <!-- fakt: hook-bez-dopasowania-kazde-zdarzenie --> Hook na `PostToolUse` bez dopasowania ruszałby więc także po czytaniu notatek. <!-- fakt: hook-dopasowanie-edit-write -->

### Jak działa hook po zapisie

- `PostToolUse` zachodzi zaraz po udanym użyciu narzędzia. <!-- fakt: zdarzenie-posttooluse-kiedy -->
- Dopasowanie `Edit|Write` zawęża hook do dwóch narzędzi. Edit zamienia tekst w istniejącym pliku, a Write tworzy albo nadpisuje plik. <!-- fakt: narzedzie-write-cala-tresc-edit-fragment -->
- Przy innych narzędziach hook nie rusza, na przykład przy czytaniu pliku (Read) albo poleceniu (Bash). <!-- fakt: hook-dopasowanie-edit-write -->
- Hook dostaje dane narzędzia: co narzędzie dostało i co zwróciło. <!-- fakt: hook-posttooluse-dostaje-dane-narzedzia --> Przy zapisie nowego pliku to cała jego treść. <!-- fakt: narzedzie-write-cala-tresc-edit-fragment -->

Gdy model odmówi, a hook nie ma `continueOnBlock: true`, Claude kończy pracę nad Twoją wiadomością. Powód pojawia się w rozmowie jako ostrzeżenie. <!-- fakt: hook-prompt-posttooluse-continueonblock -->

Z `continueOnBlock: true` powód wraca do Claude, a Claude pracuje dalej. <!-- fakt: hook-prompt-posttooluse-continueonblock --> Gdy Claude poprawia plik narzędziem Edit, hook rusza znowu. <!-- fakt: hook-dopasowanie-edit-write -->

![Z continueOnBlock: true Claude dostaje powód i może poprawić plik, zamiast kończyć pracę. Po ok: false bez continueOnBlock Claude kończy pracę nad Twoją wiadomością. Z continueOnBlock: true powód wraca do Claude. Claude poprawia plik, a hook sprawdza nowy zapis.](obrazy/poprawiaj-nie-przerywaj.png)

### Co Ci daje hook po zapisie

Powód odmowy trafia do Claude, zanim Claude skończy pracę nad Twoją wiadomością. <!-- fakt: hook-prompt-posttooluse-continueonblock --> Claude może więc poprawić tekst od razu, bez Twojej pracy.

### Na co uważać

- Hook nie cofa zapisu, bo narzędzie już się wykonało. <!-- fakt: hook-posttooluse-nie-cofa --> Dopóki Claude nie poprawi pliku, jest w nim zakazane słowo.
- Przy zmianie istniejącego pliku narzędzie Edit dostaje tekst do zamiany i nowy tekst. <!-- fakt: narzedzie-write-cala-tresc-edit-fragment --> Te dane dostaje też hook, razem z wynikiem narzędzia. <!-- fakt: hook-posttooluse-dostaje-dane-narzedzia -->
- Claude może zmieniać pliki także poleceniami powłoki, takimi jak w terminalu. <!-- fakt: claude-zmienia-pliki-tez-poleceniami --> Gdy plik przepisze polecenie albo program spoza Claude Code, hook `Edit|Write` nie rusza. <!-- fakt: hook-edit-write-pomija-zmiany-poleceniem -->
- Zdarzenie `FileChanged` (plik się zmienił) łapie zmianę wskazanego z nazwy pliku, bez względu na to, co ją zrobiło. <!-- fakt: zdarzenie-filechanged-kazda-zmiana --> Ono nie przyjmuje jednak typu `prompt`, więc hooka z zasadą zapisaną zdaniem na nim nie ustawisz. <!-- fakt: hook-prompt-zdarzenia-tak-nie -->
- Jest też zdarzenie `PreToolUse` (przed użyciem narzędzia), które może narzędzie zablokować. <!-- fakt: zdarzenie-pretooluse-kiedy --> W tej lekcji nie budujemy hooka na `PreToolUse`.

![Hook Edit|Write widzi tylko zapisy, które Claude robi tymi narzędziami. Przy Write hook dostaje całą treść pliku, a przy Edit tekst do zamiany i nowy tekst. Zmiany zrobionej poleceniem albo innym programem hook Edit|Write nie widzi. Hook rusza po zapisie i go nie cofa.](obrazy/co-widzi-hook.png)

## Kiedy zapisać zasadę w hooku, a kiedy nie

<!-- kolumny -->

#### Zapisz w hooku

1. Gdy złamanie zasady kosztuje Cię klienta albo poprawki i nie chcesz polegać na tym, że Claude ją zastosuje. <!-- fakt: claude-md-bez-gwarancji-stosowania --> <!-- fakt: hook-stala-reakcja-nie-wybor-modelu -->
2. Gdy zasadę da się ocenić w samym zapisanym tekście, na przykład zakaz kilku słów. <!-- fakt: hook-prompt-tylko-dane-zdarzenia -->
3. Gdy sprawdzenie ma zachodzić za każdym razem, bez przypominania. <!-- fakt: hook-gdy-cos-ma-sie-dziac-zawsze -->

#### Zostaw w CLAUDE.md

1. Gdy zasada należy do „tak to u nas robimy”, na przykład ton i forma zwracania się do klientów. <!-- fakt: hooki-egzekwuja-niezaleznie-od-claude -->
2. Gdy do oceny trzeba przeczytać inne pliki. Hook typu `prompt` ocenia tylko dane zdarzenia. <!-- fakt: hook-prompt-tylko-dane-zdarzenia -->
3. Gdy nie chcesz czekać na ocenę przy każdym zapisie. Claude czeka, aż hook skończy. <!-- fakt: hook-claude-czeka-na-hook -->

<!-- /kolumny -->

## Źródła

- [Automatyzacja z hookami](https://code.claude.com/docs/en/hooks-guide)
- [Hooki: opis szczegółowy](https://code.claude.com/docs/en/hooks)
- [Rozszerzanie Claude Code](https://code.claude.com/docs/en/features-overview)
- [Jak Claude pamięta Twój projekt](https://code.claude.com/docs/en/memory)
- [Gdy ustawienia nie działają](https://code.claude.com/docs/en/debug-your-config)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
