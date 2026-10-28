<em>Przewodnik po Claude Code · Moduł 2: Claude zna Twoją firmę · Lekcja 1 z 4</em>

# Dobre zlecenie: cel, materiały i oczekiwany wynik

Piszesz do Claude „Zrób raport z kampanii” i dostajesz plik z samymi liczbami. Nie ma w nim wniosku ani rekomendacji. Musisz go przerobić albo dopisywać kolejne prośby.

W aplikacji Claude wpisujesz, co Claude ma zrobić, i wysyłasz to klawiszem <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie --> Claude czyta wtedy pliki z folderu, w którym pracujesz, i wprowadza zmiany zależnie od trybu uprawnień. <!-- fakt: aplikacja-claude-czyta-pliki-zmienia-i-uruchamia-wedlug-trybu --> Tryb uprawnień to ustawienie, które mówi, czy Claude będzie czekać na Twoją zgodę. <!-- fakt: aplikacja-tryb-pod-polem-mowi-czy-claude-czeka-na-zgode --> W ćwiczeniach jest włączony tryb Accept edits (akceptuj zmiany): Claude sam tworzy i zmienia pliki w folderze roboczym bez pytania. <!-- fakt: accept-edits-edycje-w-folderze-bez-pytania --> <!-- fakt: aplikacja-auto-i-accept-edits-stosuja-zmiany --> Trybów uczy moduł 1.

Ty opisujesz, czego chcesz, a Claude sam ustala, jak to zrobić. <!-- fakt: zlecenie-opisujesz-co-chcesz-claude-ustala-jak --> <!-- fakt: aplikacja-ten-sam-silnik-co-w-terminalu --> Ta samodzielność ma granice, które warto znać. <!-- fakt: zlecenie-samodzielnosc-claude-ma-granice --> Claude potrafi się domyślić, o co Ci chodzi, ale nie czyta w myślach. <!-- fakt: zlecenie-claude-nie-czyta-w-myslach --> W prośbie „Zrób raport z kampanii” nie ma słowa o tym, dla kogo jest raport i do czego posłuży.

Dlatego ta lekcja uczy pisać zlecenie złożone z trzech części i sprawdzianu:

- **cel**: co ma powstać i po co,
- **materiały**: pliki, z których Claude ma korzystać,
- **oczekiwany wynik**: format, długość albo odbiorca,
- **sprawdzian**: prośba, żeby Claude sprawdził swoją pracę i pokazał dowód.

W ćwiczeniach prowadzisz reklamy dla klientki, która ma sklep internetowy z roślinami. Klientka do 3 listopada zdecyduje o budżecie na listopad. W folderze Kampania-listopad leżą trzy pliki:

- wyniki-kampanii.csv: wyniki reklam z października,
- raport-wrzesien.txt: raport z września, którego układ klientka zna,
- notatki-ze-spotkania.txt: ustalenia ze spotkania z klientką.

Zleć ten sam raport najpierw jednym zdaniem, potem pełnym zleceniem, i porównaj oba raporty oraz odpowiedzi Claude.

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Jedno zdanie

<!-- podglad: cw1 zdanie -->

1. Raport to same liczby i skróty branżowe, bez wniosku.
2. Prośba nie mówiła, po co jest raport, dla kogo ani w jakim formacie.
3. Liczby są z właściwego pliku: Claude sam znalazł plik z wynikami. <!-- fakt: zlecenie-nie-trzeba-wskazywac-ktore-pliki-czytac -->

#### Pełne zlecenie

<!-- podglad: cw1 zlecenie -->

1. Raport kończy się rekomendacją i terminem decyzji klientki.
2. Układ pochodzi z raportu z września, liczby z pliku z wynikami, a termin z notatek.
3. Tym razem Claude porównał sumy wydatków i pokazał obie liczby. <!-- fakt: zlecenie-popros-o-sprawdzenie-w-tej-samej-prosbie -->

<!-- /kolumny -->

Każda część zlecenia zostawiła ślad w raporcie albo w odpowiedzi Claude. Dokumentacja Claude Code robi to samo w tabeli: obok ogólnej prośby stawia prośbę z kryteriami sprawdzenia. <!-- fakt: zlecenie-tabela-prosba-ogolna-obok-prosby-z-kryterium --> Przykład w tej tabeli dotyczy programowania. Raport z reklam to nasz przykład.

<!-- rysunek: obrazy/zlecenie-cztery-czesci.png: „Cztery części zlecenia i ich ślad w raporcie”. Lewa strona: prośba z pełnego zlecenia rozbita na cztery bloki, jeden pod drugim, z etykietą na każdym: Cel (zdanie o decyzji klientki), Materiały (trzy nazwy po @), Oczekiwany wynik (jedna strona, bez skrótów, jedna rekomendacja), Sprawdzian i dowód (suma wydatków, pokaż obie liczby). Prawa strona: raport raport-pazdziernik.txt jako kartka z trzema częściami i odpowiedź Claude z dwiema sumami. Strzałki w limonce: Cel → rekomendacja i termin w „Co dalej”; Materiały → nagłówki z września, liczby z pliku, termin z notatek; Wynik → długość i brak skrótów (ramka wokół całej kartki); Sprawdzian → dwie sumy w odpowiedzi. Kolory kursu (granat, limonka), Plus Jakarta Sans, napisy po polsku, nic nie udaje interfejsu aplikacji, szerokość 1600 px, czytelne przy 390 px. -->

Niżej omawiamy każdą część po kolei:

- po co jest,
- jak działa,
- co dzięki niej zyskujesz,
- na co uważać.

## Cel: opisz wynik, nie kroki

**Po co.** Zdanie „Zrób raport z kampanii” mówi, co ma powstać, ale nie mówi, do czego raport posłuży. W prośbie nie było słowa o tym, że klientka ma na jego podstawie zdecydować o budżecie. Dlatego raport z prośby jednym zdaniem kończy się na liczbach.

**Jak działa.** Dokumentacja radzi opisać wynik, a nie kroki: powiedz, czego chcesz, i pozwól Claude znaleźć pliki. <!-- fakt: zlecenie-opisz-wynik-nie-kroki --> Nie piszesz więc „otwórz plik, policz sumy, zapisz”. Dokumentacja radzi też zlecać zadanie jak zdolnemu współpracownikowi: dajesz kontekst i kierunek, a szczegóły zostawiasz Claude. <!-- fakt: zlecenie-zlecaj-jak-zdolnemu-wspolpracownikowi -->

W tym kursie cel to dwie rzeczy: co ma powstać i po co. W ćwiczeniu brzmiał tak: raport z reklam za październik, na którego podstawie klientka zdecyduje, czy zwiększyć budżet na listopad.

**Co zyskujesz.** Im dokładniejsze zlecenie, tym mniej poprawek będziesz potrzebować. <!-- fakt: zlecenie-dokladniejsze-polecenia-mniej-poprawek --> Raport z pełnego zlecenia kończy się rekomendacją, bo cel mówił, do czego raport posłuży.

**Na co uważać.** „Opisz wynik, nie kroki” nie znaczy „nie wskazuj plików”.

- Nie musisz podawać, które pliki Claude ma przeczytać. Claude sam to ustala. <!-- fakt: zlecenie-nie-trzeba-wskazywac-ktore-pliki-czytac --> Tak było przy prośbie jednym zdaniem: Claude sam znalazł plik z wynikami.
- Gdy liczy się konkretny plik, wskaż go. Dokumentacja radzi wskazać konkretne pliki i przykładowe wzorce. <!-- fakt: zlecenie-claude-nie-czyta-w-myslach --> Jak to zrobić, piszemy w części o materiałach.
- Zlecenie nie musi być idealne. Praca z Claude Code to rozmowa: zaczynasz od tego, czego chcesz, a potem doprecyzowujesz. <!-- fakt: zlecenie-claude-code-to-rozmowa-poprawiasz-zamiast-zaczynac-od-nowa --> Pokazuje to drugie ćwiczenie.

## Materiały: dane, wzór i źródło ustaleń

**Po co.** Gdy piszesz z pamięci „układ jak ostatnio” albo „wydaliśmy około czterech tysięcy”, Claude dostaje tylko Twój opis. Poprzedni raport trafi do rozmowy, gdy go wskażesz <!-- fakt: aplikacja-at-dodaje-plik-do-rozmowy --> albo gdy Claude sam go znajdzie. <!-- fakt: zlecenie-nie-trzeba-wskazywac-ktore-pliki-czytac -->

**Jak działa.** W aplikacji wpisujesz @ i nazwę pliku, żeby dodać ten plik do kontekstu rozmowy. <!-- fakt: aplikacja-at-dodaje-plik-do-rozmowy --> Plik wskazany po @ Claude czyta, zanim odpowie. <!-- fakt: zlecenie-odwolanie-przez-at-claude-czyta-plik-przed-odpowiedzia --> Czyta więc źródło, a nie Twój opis. <!-- fakt: zlecenie-daj-material-zamiast-opisu -->

Zlecenie z ćwiczenia wskazuje trzy rodzaje materiału:

- **Dane.** Dokumentacja radzi dać Claude materiał zamiast jego opisu. <!-- fakt: zlecenie-daj-material-zamiast-opisu --> W ćwiczeniu to @wyniki-kampanii.csv.
- **Wzór.** Dokumentacja radzi wskazać istniejący plik albo wzorzec, do którego ma pasować nowy kod. <!-- fakt: zlecenie-wskaz-istniejacy-plik-jako-wzor --> <!-- fakt: zlecenie-wskaz-istniejace-wzorce-w-bazie-kodu --> My przenosimy tę radę na raport: wzorem układu jest @raport-wrzesien.txt.
- **Źródło ustaleń.** Dokumentacja radzi wskazać Claude źródło, w którym jest odpowiedź na pytanie. <!-- fakt: zlecenie-wskaz-zrodlo-ktore-odpowie-na-pytanie --> Odpowiedź na pytanie „czego chce klientka i do kiedy” jest w notatkach ze spotkania, czyli w @notatki-ze-spotkania.txt.

**Co zyskujesz.** Dokumentacja aplikacji mówi wprost: im więcej kontekstu ma Claude, tym lepsze wyniki. <!-- fakt: aplikacja-wiecej-kontekstu-lepszy-wynik --> Claude wziął do raportu coś z każdego z trzech plików, więc klientka dostaje znany układ i prawdziwe liczby.

**Na co uważać.**

- Nie musisz wskazywać wszystkiego. Dokumentacja radzi też powiedzieć Claude, żeby sam sięgnął po potrzebny kontekst, na przykład czytając pliki. <!-- fakt: zlecenie-claude-sam-siega-po-kontekst -->
- Dokumentacja radzi też dać Claude materiał wprost w prośbie, na przykład zrzut ekranu. <!-- fakt: zlecenie-daj-material-zamiast-opisu --> W aplikacji zrzut ekranu albo inny plik spoza folderu dołączasz przyciskiem + obok pola wiadomości albo przeciągając go do pola. <!-- fakt: aplikacja-plus-i-przeciaganie-dolaczaja-pliki --> Tego uczy lekcja „Nowy dokument z plików firmy” w module 0.

## Oczekiwany wynik i zakres

**Po co.** Klientka nie zna skrótów branżowych i nie przeczyta trzech stron. Raport ze skrótami, takimi jak CTR czy ROAS, musisz przed wysłaniem przetłumaczyć. W prośbie jednym zdaniem nie było też słowa o tym, za jaki okres ma być raport ani z jakich danych.

**Jak działa.** Dokumentacja radzi nazwać format, długość albo odbiorcę, żeby odpowiedź pasowała do tego, jak jej użyjesz. <!-- fakt: zlecenie-nazwij-format-dlugosc-odbiorce --> Radzi także zawęzić zadanie: napisać, którego pliku dotyczy i w jakiej sytuacji. <!-- fakt: zlecenie-zawez-zadanie --> Wspomnij o ograniczeniach, na przykład „bez skrótów branżowych”. <!-- fakt: zlecenie-claude-nie-czyta-w-myslach -->

Dokumentacja pisze, że najbardziej przydatne specyfikacje, czyli opisy zadania spisane przed pracą, mówią także, co zostaje poza zakresem. <!-- fakt: zlecenie-dobry-opis-zadania-mowi-co-poza-zakresem --> My przenosimy tę radę na zlecenie: przy raporcie dla klientki może to być zdanie „nie zmieniaj raportu z września”.

W zleceniu z ćwiczenia oczekiwany wynik i zakres to:

- raport za październik, z liczbami tylko z pliku z wynikami,
- jedna strona,
- bez skrótów branżowych,
- jedna rekomendacja,
- zapis w pliku raport-pazdziernik.txt.

Nazwę pliku dopisujemy z własnego zwyczaju, dokumentacja tego nie radzi. Dzięki niej wiesz, gdzie szukać raportu.

**Co zyskujesz.** Nie musisz tłumaczyć skrótów ani skracać raportu przed wysłaniem: klientka dostaje jedną stronę, zwykłe słowa i jedną rekomendację z terminem.

**Na co uważać.**

- Rada o formacie, długości albo odbiorcy mówi w dokumentacji o odpowiedzi Claude. Raport to nasz przykład.
- Gdy celem jest wydajność programu albo to, jaką część kodu sprawdzają testy, dokumentacja radzi podać miarę i próg. Wtedy jest jasne, kiedy praca jest skończona. <!-- fakt: zlecenie-podaj-miare-i-prog-gdy-cel-liczbowy --> Ta rada dotyczy programowania. W raporcie miarą jest długość, a progiem „jedna strona”.

## Sprawdzian: skąd Claude wie, że skończył

**Po co.** Claude kończy, gdy praca wygląda na skończoną. Bez sprawdzianu, który Claude może sam przeprowadzić, sprawdzasz wszystko Ty, a każdy błąd czeka, aż go zauważysz. <!-- fakt: zlecenie-bez-sprawdzianu-ty-jestes-petla-weryfikacji --> W raporcie dla klientki takim błędem może być zła suma wydatków.

**Jak działa.** Dokumentacja radzi, żeby w tej samej prośbie zlecić uruchomienie, test, porównanie albo sprawdzenie. Wtedy Claude pracuje dalej, zamiast skończyć po pierwszej próbie. <!-- fakt: zlecenie-popros-o-sprawdzenie-w-tej-samej-prosbie -->

Gdy sprawdzian ma tylko dwa wyniki, zdany albo niezdany, Claude sam wraca do pracy, zamiast czekać, aż Ty zauważysz błąd: <!-- fakt: zlecenie-sprawdzian-z-wynikiem-zamyka-petle -->

1. robi pracę,
2. przeprowadza sprawdzian,
3. czyta wynik,
4. poprawia, aż praca zda sprawdzian. <!-- fakt: zlecenie-sprawdzian-z-wynikiem-zamyka-petle -->

W ćwiczeniu sprawdzianem było porównanie sumy wydatków w raporcie z sumą w pliku z wynikami. To nasz przykład. Ćwiczenie pokazało to porównanie w dwóch krokach. Najpierw Claude napisał, że sprawdza sumę, a pod oknem znów zaświeciła się karta pliku z wynikami. Potem podał obie sumy.

W ćwiczeniu sumy zgodziły się od razu. Gdyby się nie zgodziły, Claude poprawiałby raport, aż się zgodzą. <!-- fakt: zlecenie-sprawdzian-z-wynikiem-zamyka-petle -->

<!-- rysunek: obrazy/sprawdzian-petla.png: „Bez sprawdzianu i ze sprawdzianem”. Dwa poziome przebiegi. Górny, „Bez sprawdzianu”: Claude pracuje → „wygląda na skończone” → koniec → Ty otwierasz pliki i sprawdzasz → błąd czeka, aż go zauważysz (szary). Dolny, „Ze sprawdzianem w zleceniu”: Claude pracuje → przeprowadza sprawdzian (porównuje dwie sumy) → czyta wynik → nie zgadza się: poprawia i sprawdza znów (pętla, strzałka wraca) → zgadza się: pokazuje dowód → koniec (limonka). Podpisy ze zdań dokumentacji o pętli sprawdzianu i o pracy, która „wygląda na skończoną”, bez wymyślonych napisów Claude. Kolory kursu (granat, limonka), Plus Jakarta Sans, napisy po polsku, nic nie udaje interfejsu aplikacji, szerokość 1600 px, czytelne przy 390 px. -->

**Co zyskujesz.** Według dokumentacji sprawdzian, który Claude może sam przeprowadzić, decyduje, czy musisz pilnować rozmowy, czy możesz od niej odejść. <!-- fakt: zlecenie-sprawdzian-roznica-miedzy-pilnowana-a-zostawiona-sesja --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> Sprawdzian dopisany do prośby działa od razu, przy każdym zadaniu. <!-- fakt: zlecenie-sprawdzian-w-prosbie-dziala-od-dzis -->

**Na co uważać.**

- Sprawdzianem może być wszystko, co daje wynik, który Claude odczyta w rozmowie. <!-- fakt: zlecenie-sprawdzian-to-sygnal-czytelny-w-rozmowie --> Porównanie dwóch sum daje taki wynik: zgadza się albo nie. Sprawdzian nie musi dotyczyć liczb. Przy ofercie dla klienta może brzmieć: „sprawdź, czy w ofercie jest cena i termin, i wypisz je”. To nasz przykład.
- Jeden sprawdzian to nie gwarancja. Zgodna suma wydatków nie mówi, czy rekomendacja jest trafna.
- Dokumentacja radzi zawsze mieć sposób na sprawdzenie pracy: czego nie możesz sprawdzić, tego nie oddawaj. <!-- fakt: zlecenie-czego-nie-sprawdzisz-nie-wypuszczaj --> W pracy z klientką znaczy to: czego nie sprawdzisz, tego nie wysyłaj.
- Sprawdzian w prośbie działa w tej jednej wiadomości, w której o niego prosisz. Żeby długa praca bez Ciebie skończyła się poprawnie, dokumentacja wskazuje inne narzędzia. <!-- fakt: zlecenie-sprawdzian-w-prosbie-dziala-od-dzis --> Pracę aż do spełnienia warunku poznasz w module 8.

## Dowód zamiast „gotowe”

**Po co.** Samo „Zapisałem raport” nie mówi, czy liczby się zgadzają. Żeby to wiedzieć, musisz otworzyć oba pliki i samodzielnie policzyć sumy.

**Jak działa.** Dokumentacja radzi, żeby Claude pokazał dowód sukcesu, a nie tylko o nim zapewniał. <!-- fakt: zlecenie-popros-o-dowod-zamiast-zapewnienia --> O dowód prosisz w tym samym zleceniu. W ćwiczeniu to końcówka prośby: „i pokaż obie liczby”. Tym razem Claude odpowiedział: „Suma wydatków w raporcie to 4 000 zł, w pliku z wynikami też 4 000 zł. Zgadza się.”

**Co zyskujesz.** Dowód przejrzysz szybciej, niż samodzielnie powtórzysz sprawdzenie. <!-- fakt: zlecenie-dowod-szybszy-niz-powtorne-sprawdzanie --> Dowód przydaje się też w rozmowach, których nie pilnujesz. <!-- fakt: zlecenie-dowod-szybszy-niz-powtorne-sprawdzanie -->

**Na co uważać.**

- Dowodem jest to, o co poprosisz. Prośba jednym zdaniem nie wspominała o dowodzie i odpowiedź Claude mówiła tylko, że zapisał raport i że są w nim liczby z pliku wyników.
- Dowód pokazuje tylko to, co Claude sprawdził.

## Jak napisać zlecenie w aplikacji Claude

1. W polu wiadomości napisz cel: co ma powstać i po co.
2. Wskaż materiały: wpisz @ i nazwę każdego pliku. <!-- fakt: aplikacja-at-dodaje-plik-do-rozmowy -->
3. Opisz oczekiwany wynik: format, długość albo odbiorcę. <!-- fakt: zlecenie-nazwij-format-dlugosc-odbiorce -->
4. Dopisz sprawdzian i poproś o dowód. <!-- fakt: zlecenie-popros-o-sprawdzenie-w-tej-samej-prosbie --> <!-- fakt: zlecenie-popros-o-dowod-zamiast-zapewnienia -->
5. Naciśnij <kbd>Enter</kbd>. <!-- fakt: aplikacja-enter-wysyla-zadanie -->
6. Gdy Claude skończy, kliknij ścieżkę pliku w jego odpowiedzi, żeby otworzyć plik. <!-- fakt: aplikacja-klik-sciezki-w-rozmowie-otwiera-plik -->

Zlecenie z ćwiczenia, do przerobienia na własne zadanie:

```
Zrób raport z reklam za październik dla klientki.
Cel: klientka ma na jego podstawie zdecydować, czy zwiększyć budżet na listopad.
Materiały: dane z @wyniki-kampanii.csv, układ jak w @raport-wrzesien.txt, ustalenia z @notatki-ze-spotkania.txt.
Wynik: jedna strona, bez skrótów branżowych, jedna rekomendacja. Zapisz jako raport-pazdziernik.txt.
Na koniec sprawdź, czy suma wydatków w raporcie zgadza się z sumą w pliku z wynikami, i pokaż obie liczby.
```

Zadaj ogólne pytanie o plik z wynikami. Potem w następnej wiadomości doprecyzuj, co ma powstać, i zobacz, jak z odpowiedzi Claude robi się notatka.

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Ogólne pytanie

1. Pytanie miało jedno zdanie i jeden plik po @.
2. Claude odpowiedział trzema spostrzeżeniami, o które nie trzeba było pytać wprost. <!-- fakt: zlecenie-otwarte-pytanie-o-plik-wydobywa-nieznane -->
3. Ta odpowiedź to przegląd dla Ciebie. Do klientki się nie nadaje.

#### Doprecyzowanie

<!-- podglad: cw2 rozpoznaj -->

1. Druga wiadomość mówiła, co ma powstać: notatka z trzema punktami.
2. Claude zapisał ją w nowym pliku w tej samej rozmowie.
3. Nie trzeba było zaczynać od nowa. <!-- fakt: zlecenie-claude-code-to-rozmowa-poprawiasz-zamiast-zaczynac-od-nowa -->

<!-- /kolumny -->

## Kiedy rozpisywać zlecenie, a kiedy nie

**Po co.** Nie każde zadanie potrzebuje celu, materiałów, wyniku i sprawdzianu. Gdy dopiero rozglądasz się w wynikach, nie wiesz jeszcze, czego chcesz, więc nie masz czego wpisać jako cel ani oczekiwany wynik.

**Jak działa.** Ogólne prośby mogą się przydać, gdy rozpoznajesz temat i stać Cię na poprawianie po drodze. <!-- fakt: zlecenie-niejasna-prosba-przy-rozpoznawaniu-tematu --> Otwarte pytanie, na przykład „co byś poprawił w tym pliku?”, może wydobyć rzeczy, o które nie przyszłoby Ci do głowy zapytać. <!-- fakt: zlecenie-otwarte-pytanie-o-plik-wydobywa-nieznane --> Gdy pierwsza próba nie wyjdzie, poprawiasz ją w tej samej rozmowie. <!-- fakt: zlecenie-claude-code-to-rozmowa-poprawiasz-zamiast-zaczynac-od-nowa -->

**Co zyskujesz.** Czasem ogólna prośba to najlepszy wybór, na przykład gdy chcesz zobaczyć, jak Claude rozumie problem, zanim go zawęzisz. <!-- fakt: zlecenie-ogolna-prosba-bywa-wlasciwa --> W drugim ćwiczeniu od pytania do gotowej notatki wystarczyły dwie krótkie wiadomości.

<!-- kolumny -->

#### Rozpisz zlecenie

1. Gdy wynik trafi do klientki.
2. Gdy liczby w wyniku mają się zgadzać z plikiem.
3. Gdy nie chcesz pilnować, czy wynik się zgadza. <!-- fakt: zlecenie-sprawdzian-roznica-miedzy-pilnowana-a-zostawiona-sesja -->

#### Zapytaj ogólnie

1. Gdy rozpoznajesz temat i stać Cię na poprawianie po drodze. <!-- fakt: zlecenie-niejasna-prosba-przy-rozpoznawaniu-tematu -->
2. Gdy chcesz zobaczyć, jak Claude rozumie problem, zanim go zawęzisz. <!-- fakt: zlecenie-ogolna-prosba-bywa-wlasciwa -->

<!-- /kolumny -->

**Na co uważać.** Ogólna prośba daje przegląd dla Ciebie, tak jak notatka z drugiego ćwiczenia. Raport dla klientki i tak wymaga pełnego zlecenia: z celem, materiałami, wynikiem i sprawdzianem.

### Kiedy zacząć od nowa

Czasem poprawki nie pomagają. Gdy Claude sobie nie radzi, dokumentacja zachęca, żeby się zastanowić, dlaczego. Podsuwa trzy pytania: <!-- fakt: zlecenie-gdy-claude-sobie-nie-radzi-zapytaj-dlaczego -->

- czy w rozmowie jest za dużo zbędnych rzeczy,
- czy zlecenie jest zbyt ogólne,
- czy zadanie jest za duże na jeden raz.

Odpowiedź na te pytania podpowiada, co zmienić. Gdy zlecenie jest zbyt ogólne, dopisz cel, materiały i oczekiwany wynik. Gdy zadanie jest za duże, zleć je w częściach. To nasze przykłady. Co zrobić z rozmową pełną nieudanych prób, piszemy niżej.

Jeśli w jednej rozmowie poprawiasz to samo więcej niż dwa razy, rozmowa jest zaśmiecona nieudanymi próbami. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> Dokumentacja radzi wtedy zacząć od nowa z lepszym pierwszym zleceniem, w którym wykorzystasz wnioski z poprzednich prób. <!-- fakt: zlecenie-po-dwoch-nieudanych-poprawkach-lepsze-pierwsze-polecenie --> Nowa rozmowa z lepszym zleceniem prawie zawsze wypada lepiej niż długa rozmowa z poprawkami. <!-- fakt: zlecenie-po-dwoch-poprawkach-czysta-sesja-z-lepszym-poleceniem -->

<!-- rysunek: obrazy/nowa-rozmowa.png: „Długa rozmowa z poprawkami i nowa rozmowa”. Lewa strona: jedno zlecenie, pod nim stos szarych poprawek 1, 2 i 3, wszystkie zostają w historii rozmowy. Prawa strona: nowa rozmowa bez historii, w niej jedno pełne zlecenie (cel, materiały, wynik, sprawdzian i wnioski z poprzednich prób), a pod nim wynik (limonka). Podpisy ze zdań dokumentacji o rozmowie zaśmieconej nieudanymi próbami i o nowej rozmowie z lepszym zleceniem. Kolory kursu (granat, limonka), Plus Jakarta Sans, napisy po polsku, nic nie udaje interfejsu aplikacji, szerokość 1600 px, czytelne przy 390 px. -->

W aplikacji nową rozmowę otwierasz przyciskiem + New na pasku bocznym. <!-- fakt: aplikacja-nowa-rozmowa-plus-new-lub-cmd-n --> Nowa rozmowa ma własną historię, niezależną od poprzedniej. <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> Dlatego lepsze zlecenie piszesz w całości: cel, materiały, wynik i sprawdzian.

### Co dalej

Zwracaj uwagę na to, co działa. Gdy Claude da świetny wynik, dokumentacja radzi przyjrzeć się, jak było napisane zlecenie i jaki kontekst dostał Claude. <!-- fakt: zlecenie-zauwazaj-co-dziala -->

Zlecenie z ćwiczenia to jeden przykład, dobrych form jest więcej. Gdy nie wiesz, od czego zacząć, zajrzyj do biblioteki promptów w dokumentacji: to zbiór gotowych próśb do skopiowania. <!-- fakt: biblioteka-promptow-gdy-nie-wiesz-od-czego-zaczac --> Zaczynasz od nich i dopasowujesz je do swojej pracy. <!-- fakt: zlecenie-prompty-z-dokumentacji-to-punkty-wyjscia --> Możesz też zapytać samego Claude, jak z niego korzystać, a Claude wyjaśni. <!-- fakt: claude-code-uczy-jak-go-uzywac -->

Przykłady w radach dokumentacji o zleceniach dotyczą programowania. Te rzeczy ułożyliśmy sami:

- podział zlecenia na cel, materiały, wynik i sprawdzian,
- listę w kolumnie „Rozpisz zlecenie”,
- przykład raportu z reklam.

Gdy zlecenie się sprawdza, konwencje, których Claude się nauczył, na przykład układ raportu z września i zakaz skrótów branżowych, możesz zapisać w pliku CLAUDE.md. Wtedy każda rozmowa zacznie się od nich i Claude nie będzie się ich uczył od nowa. <!-- fakt: claude-md-zapisuje-konwencje-na-start-sesji --> <!-- fakt: aplikacja-rozmowa-to-sesja-z-wlasna-historia --> O tym pliku jest lekcja 2.

## Źródła

- [Biblioteka promptów](https://code.claude.com/docs/en/prompt-library)
- [Dobre praktyki pracy z Claude Code](https://code.claude.com/docs/en/best-practices)
- [Jak działa Claude Code](https://code.claude.com/docs/en/how-claude-code-works)
- [Aplikacja Claude na komputer](https://code.claude.com/docs/en/desktop)
- [Pierwsze kroki w aplikacji na komputer](https://code.claude.com/docs/en/desktop-quickstart)
- [Tryby uprawnień](https://code.claude.com/docs/en/permission-modes)

Sprawdzone 23–26.10.2026, Claude Code 2.1.309–2.1.310.
