<em>Przewodnik po Claude Code · Moduł 4: Skille: powtarzalne zadania na jedno polecenie · Lekcja 3 z 4</em>

# CLAUDE.md czy skill

Prowadzisz mały sklep internetowy z kosmetykami naturalnymi. Opisy produktów i posty piszesz razem z Claude. W jednym tygodniu dzieją się dwie rzeczy:

- Claude drugi raz napisał w opisie, że krem leczy.
- Trzeci raz wklejasz do rozmowy ten sam przepis na opis produktu: sześć kroków.

Oba sygnały mówią: zapisz to na stałe. Każdy prowadzi jednak w inne miejsce. Gdy Claude dwa razy źle zastosuje tę samą zasadę, dopisz ją do CLAUDE.md. <!-- fakt: wyzwalacz-claude-md-dwa-razy-ten-sam-blad --> Gdy trzeci raz wklejasz do rozmowy tę samą procedurę z kilku kroków, zapisz ją jako skill. <!-- fakt: skill-wyzwalacze-ten-sam-prompt-ta-sama-procedura -->

Plik CLAUDE.md znasz z lekcji 2 modułu 2 (CLAUDE.md: zasady firmy w jednym pliku). Skill to plik `SKILL.md` z instrukcjami. Claude używa go sam, gdy pasuje do zadania, albo gdy wpiszesz jego nazwę po ukośniku. <!-- fakt: skill-czym-jest -->

Oba pliki przechowują instrukcje dla Claude, ale wczytują się inaczej. CLAUDE.md wczytuje się automatycznie w każdej rozmowie, a skill na żądanie. <!-- fakt: claude-md-kazda-sesja-skill-na-zadanie --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> Na żądanie znaczy: gdy go wywołasz, czyli wpiszesz jego nazwę po ukośniku, albo gdy pasuje do zadania. <!-- fakt: skill-wczytuje-sie-gdy-wywolany-albo-pasuje --> <!-- fakt: skill-czym-jest -->

Dlatego miejsce zapisu ma znaczenie:

- Zasada zapisana w skillu wejdzie do rozmowy tylko razem ze skillem. <!-- fakt: skill-wczytuje-sie-gdy-wywolany-albo-pasuje --> Skill dotyczy jednego, konkretnego zadania, a CLAUDE.md całego projektu. <!-- fakt: claude-md-caly-projekt-skill-jedno-zadanie -->
- Przepis zapisany w CLAUDE.md zajmowałby miejsce w kontekście Claude w każdym zapytaniu, także przy postach. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy --> Kontekst to wszystko, co Claude ma przed sobą w rozmowie: historia rozmowy, treść plików, CLAUDE.md, wczytane skille i instrukcje systemowe. W trakcie pracy się zapełnia. <!-- fakt: claude-code-okno-kontekstu-co-trzyma-zapelnia-sie -->

CLAUDE.md i skille to rozszerzenia: dodatki, którymi dopasowujesz to, co Claude wie, i automatyzujesz pracę. <!-- fakt: rozszerzenia-zmieniaja-co-claude-wie --> Dokumentacja radzi zacząć od CLAUDE.md z zasadami projektu, a inne rozszerzenia dokładać wtedy, gdy pojawi się konkretny powód. <!-- fakt: rozszerzenia-zacznij-od-claude-md -->

Aplikacja na komputer i Claude Code w terminalu działają na tym samym silniku i mają wspólną pamięć projektu w plikach CLAUDE.md. <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> <!-- fakt: aplikacja-i-terminal-wspolne-claude-md -->

W ćwiczeniach pracujesz w folderze Opisy-produktow. Leżą w nim:

- CLAUDE.md z zasadami sklepu,
- przepis-na-opis.txt z Twoim przepisem,
- notatki o kremie i o serum.

W ćwiczeniu niżej zapiszesz zasadę i przepis, każde w swoim miejscu. Zobaczysz, że:

- zasada trafia do CLAUDE.md w głównym folderze,
- przepis trafia do pliku `SKILL.md` w folderze `.claude/skills/opis-produktu`.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Zasada w CLAUDE.md

<!-- podglad: cw1 zasada -->

1. O zapis w CLAUDE.md prosisz Claude wprost: „Dopisz do CLAUDE.md…”. <!-- fakt: claude-md-prosba-o-zapis -->
2. Przełącznik pod polem wiadomości pokazywał Accept edits (przyjmowanie zmian). <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci --> W tym trybie Claude tworzy i zmienia pliki w folderze bez pytania. <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
3. CLAUDE.md leży w głównym folderze. Wchodzi w całości do każdej rozmowy w tym folderze. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy -->

#### Przepis w skillu

<!-- podglad: cw1 przepis -->

1. Skill projektu leży w pliku `.claude/skills/<nazwa>/SKILL.md`. <!-- fakt: skill-projektu-katalog -->
2. Zapis skilla w folderze `.claude` wymagał zgody, także w trybie Accept edits. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> Claude pyta, bo folder `.claude`, w którym leżą skille, należy do chronionych folderów. <!-- fakt: sciezki-chronione-czym-sa --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
3. Treść skilla wejdzie do rozmowy, gdy wywołasz skill albo gdy zadanie będzie pasować do jego opisu. <!-- fakt: skill-wczytuje-sie-gdy-wywolany-albo-pasuje --> <!-- fakt: claude-dopasowuje-zadanie-do-opisow-skilli -->

<!-- /kolumny -->

W pliku `SKILL.md` nie ma zasad sklepu. Nie muszą tam być: CLAUDE.md trzyma zawsze obecne zasady, a skille materiał wczytywany na żądanie. <!-- fakt: claude-md-zasady-stale-skill-material-na-zadanie --> Sprawdzisz to w ćwiczeniu 2.

## Kiedy zapisać w CLAUDE.md, a kiedy w skillu

<!-- kolumny -->

#### Do CLAUDE.md

- To, co Claude ma wiedzieć zawsze, także reguły „nigdy nie rób X”. <!-- fakt: do-claude-md-co-claude-ma-wiedziec-zawsze -->
- To, co dotyczy całego projektu, a nie jednego zadania. <!-- fakt: claude-md-caly-projekt-skill-jedno-zadanie -->
- Sygnał: Claude drugi raz źle zastosował tę samą zasadę. <!-- fakt: wyzwalacz-claude-md-dwa-razy-ten-sam-blad -->
- Przykład: „Nie obiecujemy efektów leczniczych.”

#### Do skilla

- Przepis pracy, który uruchamiasz poleceniem /nazwa. CLAUDE.md tego nie potrafi. <!-- fakt: skill-uruchamia-przepis-claude-md-nie -->
- Materiał, którego Claude potrzebuje tylko czasem, na przykład wytyczne stylu. <!-- fakt: do-skilla-material-czasem-albo-przepis -->
- To, co dotyczy jednego, konkretnego zadania. <!-- fakt: claude-md-caly-projekt-skill-jedno-zadanie -->
- Sygnał: trzeci raz wklejasz ten sam przepis. <!-- fakt: skill-wyzwalacze-ten-sam-prompt-ta-sama-procedura -->
- Przykład: sześć kroków opisu produktu.

<!-- /kolumny -->

Dokumentacja podaje przykłady z pracy programisty. <!-- fakt: do-claude-md-co-claude-ma-wiedziec-zawsze --> Przykłady ze sklepu wymyśliliśmy na potrzeby tej lekcji.

Dzięki temu podziałowi zasada sklepu jest w każdej rozmowie, także przy postach, i nie musisz jej wklejać. <!-- fakt: claude-md-kazda-sesja-skill-na-zadanie --> Przepis uruchamiasz jednym poleceniem. <!-- fakt: skill-uruchamia-przepis-claude-md-nie -->

### Gdy CLAUDE.md rośnie

Wpis w CLAUDE.md zamienił się z faktu w procedurę? To sygnał, żeby przenieść go do skilla. <!-- fakt: skill-tworz-gdy-wklejasz-te-same-instrukcje --> Na przykład krótka zasada „opis kończymy ceną” rozrosła się w sześć kroków pisania opisu.

Dokumentacja radzi trzymać CLAUDE.md poniżej 200 linii. Gdy plik rośnie, materiał pomocniczy przenieś do skilli. <!-- fakt: claude-md-do-200-linii-material-do-skilli --> Jak pisać krótkie i konkretne zasady, żeby plik zajmował mniej miejsca w kontekście, dowiesz się z lekcji 3 modułu 2. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy -->

### Gdy coś trzeba poprawić

Błąd, który się powtarza, popraw w CLAUDE.md, a nie jednorazowo w rozmowie. Przepis, który ciągle poprawiasz ręcznie, to skill do poprawki. <!-- fakt: powtarzany-blad-do-claude-md-przepis-do-poprawki-skilla -->

### Czego nie da ani CLAUDE.md, ani skill

Zasada zapisana w CLAUDE.md albo w skillu to prośba, nie gwarancja. <!-- fakt: claude-md-i-skill-prosba-nie-gwarancja --> Gdy coś ma się dziać za każdym razem, bez proszenia, dokumentacja radzi napisać hook. <!-- fakt: hook-gdy-cos-ma-sie-dziac-zawsze --> Hook Claude Code uruchamia w określonej chwili pracy, a skill wczytuje do kontekstu, żeby Claude go zastosował. <!-- fakt: hook-uruchamia-claude-code-przy-zdarzeniu --> Hooki poznasz w module 7.

## Zasady sklepu i przepis w jednej rozmowie

W notatkach o serum stoi linia: „Producent pisze: leczy przebarwienia.” W CLAUDE.md jest już zasada z ćwiczenia 1, a w folderze skill opis-produktu.

W ćwiczeniu niżej otwierasz nową rozmowę w tym samym folderze. Zobaczysz, że:

- CLAUDE.md wchodzi od pierwszej prośby i zostaje do końca rozmowy, <!-- fakt: claude-md-czytany-na-start-sesji --> <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy -->
- skill nie wchodzi przy prośbie o tytuły posta, bo ta prośba nie pasuje do jego opisu, <!-- fakt: skill-wczytuje-sie-gdy-wywolany-albo-pasuje --> <!-- fakt: claude-dopasowuje-zadanie-do-opisow-skilli -->
- polecenie /opis-produktu uruchamia skill, <!-- fakt: skill-uruchomienie-ukosnik -->
- opis serum trzyma się naraz przepisu ze skilla i zasad z CLAUDE.md.

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Prośba o tytuły

1. Na początku każdej rozmowy Claude czyta CLAUDE.md. <!-- fakt: claude-md-czytany-na-start-sesji --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> Dlatego najpierw zaświeciła karta CLAUDE.md.
2. Skill nie wszedł. Wchodzi, gdy go wywołasz albo gdy pasuje do zadania, a prośba o tytuły posta do jego opisu nie pasuje. <!-- fakt: skill-wczytuje-sie-gdy-wywolany-albo-pasuje --> <!-- fakt: claude-dopasowuje-zadanie-do-opisow-skilli -->
3. Gdy zadanie pasuje do opisu, Claude sam sięga po skill. <!-- fakt: aplikacja-skille-claude-laduje-sam-albo-wskazujesz --> <!-- fakt: claude-dopasowuje-zadanie-do-opisow-skilli -->
4. U siebie rozmowę zaczynasz, gdy wpiszesz zadanie i naciśniesz <kbd>Enter</kbd>. <!-- fakt: aplikacja-wpisz-zadanie-i-nacisnij-enter-zeby-zaczac -->

#### Polecenie /opis-produktu

<!-- podglad: cw2 razem -->

1. Nazwa skilla z ukośnikiem na początku wiadomości uruchomiła go od razu. <!-- fakt: skill-uruchomienie-ukosnik -->
2. Karta CLAUDE.md nie zaświeciła drugi raz. CLAUDE.md wszedł na starcie rozmowy i jest w każdym zapytaniu. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy -->
3. Opis powstał według sześciu kroków ze skilla, mówi na Ty i nie obiecuje leczenia.

<!-- /kolumny -->

Dzięki temu skill zawiera sam przepis. Zasad sklepu nie powtarzasz w każdym skillu, bo CLAUDE.md i tak jest w rozmowie. <!-- fakt: claude-md-zasady-stale-skill-material-na-zadanie -->

Tym razem Claude zastosował i przepis, i zasady. Następnym razem może być inaczej, bo zasada w CLAUDE.md i w skillu to prośba, nie gwarancja. <!-- fakt: claude-md-i-skill-prosba-nie-gwarancja -->

Świecące karty są tylko w ćwiczeniu. W aplikacji polecenie /context wpisane w polu wiadomości wypisuje w rozmowie podział jej kontekstu na kategorie. <!-- fakt: aplikacja-context-wypisuje-podzial-okna-kontekstu --> Więcej o nim w module 6.

## Co Claude wczytuje i ile miejsca to zajmuje

Koszt w tej części to miejsce, które CLAUDE.md i skille zajmują w kontekście. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy --> Ćwiczenie 2 pokazało chwilę, w której Claude wczytuje CLAUDE.md i skill. Rysunek niżej pokazuje, co jest w rozmowie od początku do końca.

![Jedna rozmowa w folderze Opisy-produktow. Na osi czasu są trzy kolejne prośby, w środku polecenie /opis-produktu serum-notatki.txt. CLAUDE.md jest w każdym zapytaniu w całości. Opisy skilli też są w każdym zapytaniu. Treść skilla opis-produktu wchodzi dopiero od wywołania. Potem zostaje w rozmowie. Skill wchodzi, gdy go wywołasz albo gdy zadanie pasuje do jego opisu.](obrazy/zawsze-a-na-zadanie.png)
<!-- analogia: CLAUDE.md to regulamin przypięty na ścianie: wisi zawsze. Skill to segregator na półce: na grzbiecie widać tylko tytuł, otwierasz go, gdy jest potrzebny, a potem leży na biurku do końca dnia. -->

CLAUDE.md wczytuje się na starcie rozmowy w całości. Zajmuje miejsce w kontekście Claude w każdym zapytaniu. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia -->

Ze skilli na starcie wchodzą tylko opisy. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy --> Pełna treść skilla trafia do rozmowy dopiero wtedy, gdy skill zostaje uruchomiony. <!-- fakt: skill-laduje-sie-przy-uzyciu --> Treść uruchomionego skilla zostaje w rozmowie w kolejnych turach. <!-- fakt: skill-tresc-wchodzi-raz-i-zostaje --> Tura to jedna Twoja wiadomość razem z odpowiedzią Claude.

Dzięki temu długi materiał w skillu prawie nic nie kosztuje, dopóki go nie potrzebujesz. <!-- fakt: skill-tresc-tylko-przy-uzyciu-dlugi-material-tani --> Ten sam materiał w CLAUDE.md zajmowałby miejsce w każdym zapytaniu, także przy tytułach posta. <!-- fakt: koszt-claude-md-kazde-zapytanie-skill-opisy -->

Na co uważać:

- Każdy skill na liście skilli, czyli jego nazwa i opis, zajmuje miejsce w kontekście w każdej turze, nawet jeśli Claude nigdy go nie użyje. <!-- fakt: kazdy-skill-na-liscie-kosztuje-w-kazdej-turze --> <!-- fakt: skill-laduje-sie-przy-uzyciu --> Nie zakładaj więc skilli na zapas.
- Za dużo dodatków może dodać szum. Skille mogą wtedy nie uruchamiać się poprawnie, a Claude może gubić Twoje zasady. <!-- fakt: za-duzo-dodatkow-szum -->
- Gdy opisy skilli są mętne albo się pokrywają, Claude może wziąć zły skill albo pominąć ten, który by pomógł. <!-- fakt: claude-dopasowuje-zadanie-do-opisow-skilli -->

## U siebie w aplikacji

1. Otwórz rozmowę w folderze, w którym leży CLAUDE.md.
2. Zasadę dla całego projektu zapisz prośbą „Dopisz do CLAUDE.md…”. <!-- fakt: claude-md-prosba-o-zapis --> Wyślij ją klawiszem <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie -->
3. Przepis na jedno zadanie zapisz jako skill projektu, na przykład prośbą „Zapisz mój przepis z pliku … jako skill projektu o nazwie …”. W trybie Accept edits Claude poprosi o zgodę na zapis w folderze `.claude`: zatwierdź zapis. <!-- fakt: accept-edits-sciezki-chronione-pytaja --> <!-- fakt: sciezki-chronione-czym-sa --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu -->
4. Gdy folderu `.claude/skills` nie było na starcie rozmowy, nowy skill uruchom w nowej rozmowie w tym samym folderze. <!-- fakt: skill-nowy-folder-skilli-wymaga-przeladowania --> <!-- fakt: skill-projektu-z-folderu-sesji --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Wpisz jego nazwę z ukośnikiem na początku wiadomości. <!-- fakt: skill-uruchomienie-ukosnik -->
5. Przejrzyj CLAUDE.md. Wpisy, które z faktu zamieniły się w procedurę, przenieś do skilli. <!-- fakt: skill-tworz-gdy-wklejasz-te-same-instrukcje -->
6. Nie zakładaj skilli na zapas: każdy skill na liście zajmuje miejsce w każdej turze. <!-- fakt: kazdy-skill-na-liscie-kosztuje-w-kazdej-turze -->

## Źródła

- [Rozszerz Claude Code](https://code.claude.com/docs/en/features-overview)
- [Rozszerz Claude o skille](https://code.claude.com/docs/en/skills)
- [Jak Claude pamięta Twój projekt](https://code.claude.com/docs/en/memory)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)

Sprawdzone 26.10.2026, Claude Code 2.1.310.
