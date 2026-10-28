/* Postęp kursu w przeglądarce (localStorage): lekcja otwarta albo przerobiona, przycisk pod lekcją, znaczniki i procent na stronie startowej. */
(function () {
  var KLUCZ = "opanuj-claude-code.postep.v1";
  var zapas = {}; // gdy przeglądarka nie pozwala zapisać, postęp żyje do zamknięcia karty

  function wczytaj() {
    try {
      var s = localStorage.getItem(KLUCZ);
      return s ? JSON.parse(s) || {} : {};
    } catch (e) {
      return zapas;
    }
  }
  function zapisz(stan) {
    zapas = stan;
    try {
      localStorage.setItem(KLUCZ, JSON.stringify(stan));
    } catch (e) {}
  }

  // strona lekcji: otwarcie liczy się jako „zaczęta”, przycisk przełącza „przerobiona”
  var nawigacja = document.querySelector("nav.nawigacja[data-lekcja]");
  if (nawigacja) {
    var adres = nawigacja.getAttribute("data-lekcja");
    var przycisk = nawigacja.querySelector("[data-postep-przycisk]");
    var stan = wczytaj();
    if (!stan[adres]) {
      stan[adres] = "zaczeta";
      zapisz(stan);
    }
    var pokaz = function () {
      var gotowa = wczytaj()[adres] === "przerobiona";
      przycisk.textContent = gotowa
        ? "Przerobiona ✓ (kliknij, żeby cofnąć)"
        : "Oznacz lekcję jako przerobioną";
      przycisk.classList.toggle("przerobiona", gotowa);
    };
    przycisk.addEventListener("click", function () {
      var s = wczytaj();
      s[adres] = s[adres] === "przerobiona" ? "zaczeta" : "przerobiona";
      zapisz(s);
      pokaz();
    });
    pokaz();
  }

  // strona startowa: znaczniki przy lekcjach i procent
  var spis = document.querySelectorAll("[data-postep-lekcja]");
  if (!spis.length) return;
  var odswiez = function () {
    var s = wczytaj();
    var przerobione = 0;
    spis.forEach(function (el) {
      var stanLekcji = s[el.getAttribute("data-postep-lekcja")] || "";
      el.setAttribute("data-stan", stanLekcji || "nowa");
      if (stanLekcji === "przerobiona") przerobione++;
    });
    var procent = Math.round((100 * przerobione) / spis.length);
    var pasek = document.querySelector("[data-postep-pasek]");
    var napis = document.querySelector("[data-postep-napis]");
    if (pasek) {
      // jeden klocek = 5%; pierwsza przerobiona lekcja zapala co najmniej jeden klocek
      var klocki = pasek.querySelectorAll(".postep-klocek");
      var pelne = przerobione ? Math.max(1, Math.round((procent / 100) * klocki.length)) : 0;
      klocki.forEach(function (k, i) {
        k.classList.toggle("pelny", i < pelne);
      });
    }
    if (napis) napis.textContent = procent + "%";
  };
  window.addEventListener("storage", function (e) {
    if (e.key === KLUCZ) odswiez();
  });
  odswiez();
})();
