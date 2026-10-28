/* Symulator aplikacji Claude, drogi: karta zgody przeglądarki (krok `zgoda` z `witryna`: trzy przyciski z napisami Allow once, Always allow i Deny przy pierwszym działaniu Claude na cudzej stronie), krok `strona` (cudza strona w panelu Browser bez kliku w ścieżkę, podmiana w miejscu z błyskiem) i pamięć zgody (Allow once na jeden krok `strona`, Always allow do końca drogi). Wygląd przycisków: karta planu (.apl-plan-przyciski, strona/styl-aplikacja-plan.css). */

/* Napisy interfejsu aplikacji, które rysuje ten plik, w kolejności z dokumentacji (fakt aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu); test sprawdza je w dane/napisy-interfejsu.yaml (gdzie: aplikacja). Klucze to cele kroku `klik`. */
PK.NAPISY_ZGODY_STRONY = { allow_once: "Allow once", always_allow: "Always allow", deny: "Deny" };
PK.DECYZJE_STRONY = Object.keys(PK.NAPISY_ZGODY_STRONY);

/* Znacznik „kliknij tutaj” stoi pod ramką karty, ze strzałką na przycisku (jak przy ptaszku, PK.celKroku). */
PK.DECYZJE_STRONY.forEach((c) => (PK.PO_CELU_KROKU[c] = ".apl-plik"));

/* Selektory przycisków karty, do wskazania celu kroku `klik` (PK.SELEKTORY_ZGODY_STRONY) i do rozpoznania kliku (PK.PRZYCISK_ZGODY_STRONY). */
PK.SELEKTORY_ZGODY_STRONY = Object.fromEntries(PK.DECYZJE_STRONY.map((c) => [c, `.apl-zgoda-strona [data-cel="${c}"]`]));
PK.PRZYCISK_ZGODY_STRONY = ".apl-zgoda-strona .apl-plan-p";

/* Cel najbliższego kroku `klik` z jedną z trzech decyzji w liście kroków `dalej` (kroki po karcie); undefined, gdy go nie ma. */
PK.celZgodyStrony = (dalej) => {
  const krok = (dalej || []).find((k) => k.typ === "klik" && PK.DECYZJE_STRONY.includes(k.cel));
  return krok && krok.cel;
};

/* Karta w rozmowie pod odpowiedzią Claude: ta sama ramka co karta „folder chroniony”, w niej trzy przyciski tekstowe w wyglądzie przycisków karty planu. Aktywny jest tylko przycisk `aktywny` (cel najbliższego kliku drogi), pozostałe są wyszarzone (aria-disabled, klik niczego nie robi; D-2026-10-26-54). Karta nie pokazuje nazwy strony: nazywa ją odpowiedź Claude nad kartą. */
PK.kartaZgodyStrony = (aktywny) => {
  const przycisk = (c) =>
    `<button type="button" class="apl-plan-p" data-cel="${c}"${c === aktywny ? "" : ' aria-disabled="true"'}>${PK.esc(PK.NAPISY_ZGODY_STRONY[c])}</button>`;
  return `<div class="apl-zgoda apl-zgoda-strona"><section class="apl-plik"><div class="apl-plan-przyciski">${PK.DECYZJE_STRONY.map(przycisk).join("")}</div></section></div>`;
};

/* Cudza strona w panelu Browser i pamięć zgody: `widok` to miejsce na otwarty plik (.apl-widok-pliku), `okno` dostaje klasę plik-otwarty. Zwraca {karta, decyzja, krok, zamknij, otwarta, zapomnij, reset}.
   - karta(k, dalej): HTML karty dla kroku `zgoda` z `witryna` i zapamiętanie, o którą stronę pyta;
   - decyzja(cel, karta): skutek kliku (przyciski znikają, karta zostaje cienką ramką): Allow once zapisuje zgodę na jeden krok `strona`, Always allow na wszystkie do końca drogi, Deny żadnej;
   - krok(k): krok `strona`; bez zgody nic nie rysuje (walidator do tego nie dopuszcza); ta sama strona w panelu jest podmieniana w miejscu z błyskiem, inna otwiera się od nowa;
   - zamknij(): panel przestaje pokazywać stronę (krok `plik` albo pytanie z boku zajmuje jego miejsce);
   - otwarta(): nazwa strony widocznej w panelu (albo null); zapomnij(): to samo co zamknij bez dotykania panelu, gdy zajął go już widok artefaktu;
   - reset(): zamknij i czyszczenie pamięci zgody („Od nowa”, nowe polecenie). */
PK.stronaZewnetrzna = function (okno, widok) {
  const zawsze = new Set(); /* strony z Always allow */
  let raz = null; /* strona z Allow once: zgoda na najbliższy krok `strona` */
  let czeka = null; /* strona, o którą pyta karta stojąca w rozmowie */
  let otwarta = null; /* strona widoczna w panelu */
  const zamknij = () => {
    if (!otwarta) return;
    otwarta = null;
    widok.hidden = true;
    widok.innerHTML = "";
    okno.classList.remove("plik-otwarty");
  };
  return {
    karta(k, dalej) {
      czeka = k.witryna;
      return PK.kartaZgodyStrony(PK.celZgodyStrony(dalej));
    },
    decyzja(cel, karta) {
      if (cel === "allow_once") raz = czeka;
      if (cel === "always_allow") zawsze.add(czeka);
      czeka = null;
      karta.classList.add("zatwierdzona");
      karta.querySelector(".apl-plan-przyciski").remove();
    },
    krok(k) {
      const zgoda = zawsze.has(k.witryna) || raz === k.witryna;
      if (raz === k.witryna) raz = null; /* Allow once zużywa się na jednym kroku */
      if (!zgoda) return;
      const podmiana = otwarta === k.witryna && !!widok.querySelector(".apl-przegladarka");
      const t = document.createElement("template");
      t.innerHTML = PK.przegladarkaAplikacji(k.strona);
      const nowa = t.content.firstElementChild;
      if (podmiana) {
        nowa.querySelector(".apl-prz-strona").classList.add("apl-art-nowa"); /* podmiana w miejscu: nowa strona błyska jak w widoku artefaktu */
        widok.querySelector(".apl-przegladarka").replaceWith(nowa);
      } else {
        widok.innerHTML = "";
        widok.append(nowa);
      }
      widok.hidden = false;
      okno.classList.add("plik-otwarty");
      otwarta = k.witryna;
    },
    zamknij,
    otwarta: () => otwarta,
    zapomnij() {
      otwarta = null; /* panel zajął widok artefaktu: jego zawartość jest już inna, więc nie ma czego zamykać ani podmieniać */
    },
    reset() {
      zamknij();
      zawsze.clear();
      raz = null;
      czeka = null;
    },
  };
};
