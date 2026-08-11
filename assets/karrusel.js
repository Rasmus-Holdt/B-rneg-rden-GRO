/* Børnegården GRO – billedkarrusel
   ------------------------------------------------------------------
   Selve bevægelsen er ren CSS (scroll-snap), så swipe på telefon føles
   som i styresystemet og ikke som en efterligning. JavaScript bruges
   kun til to ting: at holde prikkerne i sync med hvad man kigger på,
   og at lade pilene rulle ét billede ad gangen.

   Uden JavaScript virker karrusellen stadig – den er så bare en
   vandret stribe billeder, man kan rulle i. Intet går i stykker.

   Opsætningen ligger i en funktion, fordi overgang.js skifter <main>
   ud i browsere uden View Transitions og skal kunne kalde den igen.
*/
(function () {
  'use strict';

  function saetOp() {
    document.querySelectorAll('.karrusel').forEach(function (karrusel) {
      if (karrusel.dataset.klar) return;          // allerede sat op
      var spor     = karrusel.querySelector('.karrusel-spor');
      var billeder = Array.prototype.slice.call(spor.children);
      var prikker  = karrusel.querySelector('.karrusel-prikker');
      var forrige  = karrusel.querySelector('.karrusel-forrige');
      var naeste   = karrusel.querySelector('.karrusel-naeste');
      var tael     = karrusel.querySelector('.karrusel-tael');
      if (billeder.length < 2) return;

      karrusel.dataset.klar = '1';
      karrusel.classList.add('karrusel-klar');
      var aktiv = 0;

      // ---- Prikker -------------------------------------------------
      billeder.forEach(function (_, i) {
        var knap = document.createElement('button');
        knap.type = 'button';
        knap.className = 'karrusel-prik';
        knap.setAttribute('aria-label', 'Vis billede ' + (i + 1) + ' af ' + billeder.length);
        knap.addEventListener('click', function () { gaaTil(i); });
        prikker.appendChild(knap);
      });
      var prikListe = Array.prototype.slice.call(prikker.children);

      function gaaTil(i) {
        i = Math.max(0, Math.min(billeder.length - 1, i));
        spor.scrollTo({ left: billeder[i].offsetLeft - spor.offsetLeft, behavior: 'smooth' });
      }

      function markér(i) {
        if (i === aktiv) return;
        aktiv = i;
        prikListe.forEach(function (p, n) {
          p.classList.toggle('er-aktiv', n === i);
          p.setAttribute('aria-current', n === i ? 'true' : 'false');
        });
        if (tael) tael.textContent = (i + 1) + ' / ' + billeder.length;
        if (forrige) forrige.disabled = i === 0;
        if (naeste)  naeste.disabled  = i === billeder.length - 1;
      }

      // ---- Hvilket billede fylder mest af sporet? -------------------
      if ('IntersectionObserver' in window) {
        var iagttager = new IntersectionObserver(function (poster) {
          poster.forEach(function (post) {
            if (post.isIntersecting && post.intersectionRatio > 0.55) {
              markér(billeder.indexOf(post.target));
            }
          });
        }, { root: spor, threshold: [0.55, 0.75] });
        billeder.forEach(function (b) { iagttager.observe(b); });
      } else {
        spor.addEventListener('scroll', function () {
          markér(Math.round(spor.scrollLeft / spor.clientWidth));
        }, { passive: true });
      }

      // ---- Pile ----------------------------------------------------
      if (forrige) forrige.addEventListener('click', function () { gaaTil(aktiv - 1); });
      if (naeste)  naeste.addEventListener('click',  function () { gaaTil(aktiv + 1); });

      // ---- Piletaster ----------------------------------------------
      spor.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft')  { e.preventDefault(); gaaTil(aktiv - 1); }
        if (e.key === 'ArrowRight') { e.preventDefault(); gaaTil(aktiv + 1); }
      });

      markér(0);
      prikListe[0].classList.add('er-aktiv');
      prikListe[0].setAttribute('aria-current', 'true');
      if (forrige) forrige.disabled = true;
      if (tael) tael.textContent = '1 / ' + billeder.length;
    });
  }

  window.__groKarrusel = saetOp;
  saetOp();
})();
