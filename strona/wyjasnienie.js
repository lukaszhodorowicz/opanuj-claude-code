/* Odwracana karta „wyjaśnienie / schemat” w lekcji: klik w kartę albo w przycisk nad nią, Enter i spacja na karcie odwracają ją i podmieniają napis przycisku oraz aria-label. */
(function () {
  function podlacz(karta) {
    const wnetrze = karta.querySelector(".odwrot-w");
    const przycisk = karta.querySelector(".odwrot-przycisk");
    if (!wnetrze || !przycisk) return;
    const zmien = () => {
      const odwrocona = karta.classList.toggle("odwrocona");
      wnetrze.setAttribute("aria-pressed", odwrocona);
      wnetrze.setAttribute("aria-label", odwrocona ? "Wróć do wyjaśnienia" : "Odwróć kartę, żeby zobaczyć schemat");
    };
    wnetrze.addEventListener("click", zmien);
    przycisk.addEventListener("click", zmien);
    wnetrze.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        zmien();
      }
    });
  }

  function start() {
    document.querySelectorAll(".odwrot").forEach(podlacz);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
