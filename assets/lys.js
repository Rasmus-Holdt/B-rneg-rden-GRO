/* Børnegården GRO – klik på et billede for at se det stort
   ------------------------------------------------------------------
   Uden JavaScript sker der ingenting: billederne står som før, og
   karrusellen kan stadig swipes. Med JavaScript bliver hvert foto til
   en knap, og et klik åbner det i fuld skærm.

   Der hentes ikke én eneste ekstra byte. Det store billede er præcis
   den fil, browseren allerede har hentet til pladsen på siden
   (img.currentSrc), så visningen åbner øjeblikkeligt.

   <dialog>.showModal() bruges med vilje: browseren står selv for at
   fange tastaturet inde i vinduet, lukke på Esc og gøre resten af
   siden utilgængelig for skærmlæsere. Det er langt mindre kode – og
   langt mere korrekt – end at bygge det i hånden.
*/
(function () {
  'use strict';

  var dialog = document.createElement('dialog');
  if (typeof dialog.showModal !== 'function') return;   // for gammel browser

  var VAELGERE = '.karrusel-billede, .galleri figure, .blok-billede, .kort > .portraet-plads';

  dialog.className = 'lys';
  dialog.innerHTML =
    '<div class="lys-ramme">' +
      '<img class="lys-foto" alt="">' +
    '</div>' +
    '<button class="lys-luk" type="button" aria-label="Luk billedet"></button>' +
    '<button class="lys-pil lys-forrige" type="button" aria-label="Forrige billede"></button>' +
    '<button class="lys-pil lys-naeste" type="button" aria-label="Næste billede"></button>' +
    '<span class="lys-tael" aria-hidden="true"></span>';
  document.body.appendChild(dialog);

  var foto    = dialog.querySelector('.lys-foto');
  var tael    = dialog.querySelector('.lys-tael');
  var roligt  = matchMedia('(prefers-reduced-motion: reduce)');
  var forrige = dialog.querySelector('.lys-forrige');
  var naeste  = dialog.querySelector('.lys-naeste');

  var gruppe = [];      // billederne man kan bladre mellem lige nu
  var nr = 0;
  var kom_fra = null;   // knappen der åbnede – fokus skal tilbage dertil

  // Billedet tones ud, skiftes og tones ind igen. Filen ligger allerede i
  // browserens cache – den er jo den samme, som staar paa siden – saa der er
  // ingen ventetid at daekke over. Overtoningen er der udelukkende, fordi et
  // haardt klip mellem to fotos er ubehageligt at kigge paa.
  var skifter = null;
  function vis(i, uden_overgang) {
    nr = Math.max(0, Math.min(gruppe.length - 1, i));
    var kilde = gruppe[nr];
    clearTimeout(skifter);
    function saet() {
      foto.src = kilde.currentSrc || kilde.src;
      foto.alt = kilde.alt || '';
      foto.classList.remove('lys-skifter');
    }
    if (uden_overgang || roligt.matches) { saet(); }
    else { foto.classList.add('lys-skifter'); skifter = setTimeout(saet, 150); }
    var flere = gruppe.length > 1;
    tael.textContent = flere ? (nr + 1) + ' / ' + gruppe.length : '';
    forrige.hidden = naeste.hidden = !flere;
    forrige.disabled = nr === 0;
    naeste.disabled  = nr === gruppe.length - 1;
  }

  function aaben(billeder, i, knap) {
    gruppe = billeder;
    kom_fra = knap || null;
    vis(i, true);              // foerste billede uden overtoning
    dialog.showModal();
  }

  // Lukningen skal ogsaa kunne naa at tone ud. Uden dette forsvinder
  // vinduet med et snit, og Esc foeles haardere end alt andet paa siden.
  function luk() {
    if (roligt.matches || dialog.classList.contains('lys-lukker')) {
      dialog.close(); return;
    }
    dialog.classList.add('lys-lukker');
    setTimeout(function () {
      dialog.classList.remove('lys-lukker');
      dialog.close();
    }, 170);
  }

  // Esc udloeser "cancel". Vi tager over, saa den ogsaa faar overgangen med.
  dialog.addEventListener('cancel', function (e) { e.preventDefault(); luk(); });

  forrige.addEventListener('click', function () { vis(nr - 1); });
  naeste.addEventListener('click',  function () { vis(nr + 1); });
  dialog.querySelector('.lys-luk').addEventListener('click', luk);

  // Klik uden for billedet lukker
  dialog.addEventListener('click', function (e) {
    if (e.target === dialog || e.target.classList.contains('lys-ramme')) luk();
  });

  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft')  { e.preventDefault(); vis(nr - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); vis(nr + 1); }
  });

  // Swipe på telefon
  var x0 = null;
  dialog.addEventListener('touchstart', function (e) {
    x0 = e.changedTouches[0].clientX;
  }, { passive: true });
  dialog.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    x0 = null;
    if (Math.abs(dx) > 45) vis(nr + (dx < 0 ? 1 : -1));
  }, { passive: true });

  dialog.addEventListener('close', function () {
    foto.removeAttribute('src');
    if (kom_fra && document.contains(kom_fra)) kom_fra.focus({ preventScroll: true });
    kom_fra = null;
  });

  // ---- Gør hvert foto til en knap ----------------------------------
  function saetOp() {
    document.querySelectorAll(VAELGERE).forEach(function (plads) {
      // Nogle steder ER pladsen selv <picture> – portraettet af Jeanette har
      // klassen siddende direkte paa elementet og ikke paa en kasse udenom.
      // Uden den her linje var det det eneste foto paa siden, man ikke kunne
      // klikke paa.
      var pic = plads.matches('picture') ? plads : plads.querySelector('picture');
      if (!pic || pic.parentElement.classList.contains('lys-knap')) return;
      if (pic.matches('.sol, .sol-hjoerne, .sol-pas, .logo-tegning')) return;

      var knap = document.createElement('button');
      knap.type = 'button';
      knap.className = 'lys-knap';
      // Knappen skydes ind MELLEM foraelderen og <picture>. Sidder der en
      // layoutklasse paa billedet, som en regel rammer med ">" – portraettet
      // paa Om mig gjorde – holder reglen op med at virke. Klassen faar
      // derfor lov at gaelde begge steder: knappen overtager pladsen i
      // layoutet, billedet fylder knappen ud.
      if (pic.className) knap.className += ' ' + pic.className;
      var img = pic.querySelector('img');
      knap.setAttribute('aria-label', 'Se billedet stort: ' + (img ? img.alt : ''));
      pic.parentNode.insertBefore(knap, pic);
      knap.appendChild(pic);

      knap.addEventListener('click', function () {
        // Bladr mellem billederne i samme karrusel eller samme galleri.
        //
        // Der spoerges paa KNAPPEN og ikke paa pladsen. Foerste dias i en
        // karrusel bliver fanget af .blok-billede (den staar foer
        // .karrusel-billede i dokumentet), og .blok-billede ligger UDEN OM
        // sporet – saa closest() derfra fandt ingenting, og billede 1 af 8
        // aabnede alene uden pile. Knappen sidder inde i sporet uanset hvad.
        var aeske = knap.closest('.karrusel-spor, .galleri');
        var billeder = aeske
          ? Array.prototype.slice.call(aeske.querySelectorAll('.lys-knap img'))
          : [img];
        aaben(billeder, billeder.indexOf(img), knap);
      });
    });
  }

  window.__groLys = saetOp;
  saetOp();
})();
