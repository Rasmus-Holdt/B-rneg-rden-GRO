/* Børnegården GRO – sideovergange i browsere uden View Transitions
   ------------------------------------------------------------------
   Chrome, Edge og Safari 18.2+ klarer overgangene helt selv med to linjer
   CSS (@view-transition). Denne fil gør INTET i de browsere.

   Firefox og ældre Safari kan det ikke. Her henter vi den nye side i
   baggrunden, skifter indholdet ud og animerer det – uden at bygge en
   "single page app". Adresselinjen, tilbage-knappen, bogmærker og
   søgemaskiner opfører sig præcis som før.

   Alt kan fejle uden konsekvens: sker der noget uventet, sender vi
   browseren afsted på almindelig vis med location.href. Værst tænkelige
   udfald er altså en helt normal sideindlæsning.
*/
(function () {
  'use strict';

  // Chrome/Edge/Safari 18.2+ klarer det selv – rør ikke ved noget
  if (CSS.supports('view-transition-name', 'none')) return;

  // Respektér "Reducér bevægelse"
  var roligt = matchMedia('(prefers-reduced-motion: reduce)');

  // fetch() virker ikke på file:// – så springer vi over og lader
  // browseren navigere normalt
  if (location.protocol === 'file:') return;

  // Skal svare til .side-gaar-ud i style.css. Ligger de to tal ikke på
  // samme værdi, ser man enten et tomt hul eller et brat klip.
  var UD_MS = 140;

  var laaser = false;
  var cache = Object.create(null);   // hentede sider, så et klik er øjeblikkeligt

  function erInternLink(a) {
    return a.origin === location.origin &&
           a.pathname !== location.pathname &&
           !a.hasAttribute('download') &&
           a.target !== '_blank';
  }

  function hent(url) {
    var nøgle = new URL(url, location.href).pathname;
    if (cache[nøgle]) return cache[nøgle];

    cache[nøgle] = fetch(url, { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var nyt = doc.querySelector('main');
        if (!nyt) throw new Error('ingen <main>');
        return { doc: doc, html: nyt.innerHTML, id: nyt.id };
      })
      .catch(function (fejl) {
        delete cache[nøgle];       // en fejl må ikke gemmes
        throw fejl;
      });
    return cache[nøgle];
  }

  // Erstat kun indholdet INDEN I <main>. Beholder man selve <main>-elementet,
  // beholder browseren også dets plads i layoutet, og siden hopper ikke.
  function skift(data, url, gemIHistorik) {
    var main = document.querySelector('main');

    main.classList.remove('side-gaar-ud', 'side-kommer-ind');
    main.innerHTML = data.html;

    var nyDoc = data.doc;
    document.title = nyDoc.title;

    // Beskrivelse og canonical skal følge med – ellers deler folk den
    // forkerte tekst, hvis de deler et link efter at have klikket rundt.
    ['meta[name="description"]', 'link[rel="canonical"]',
     'meta[property="og:title"]', 'meta[property="og:description"]',
     'meta[property="og:url"]'].forEach(function (vælger) {
      var gl = document.head.querySelector(vælger);
      var ny = nyDoc.head.querySelector(vælger);
      if (!gl || !ny) return;
      if (gl.hasAttribute('content')) gl.setAttribute('content', ny.getAttribute('content'));
      if (gl.hasAttribute('href'))    gl.setAttribute('href',    ny.getAttribute('href'));
    });

    // Den aktive fane skal flytte sig med
    var sti = new URL(url, location.href).pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav.faner a').forEach(function (a) {
      if (a.getAttribute('href') === sti) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    if (gemIHistorik) history.pushState({ gro: true }, '', url);

    // "instant" er vigtigt: html har scroll-behavior: smooth, og uden dette
    // ville siden rulle blødt op til toppen SAMTIDIG med at den toner ind.
    // De to bevægelser oveni hinanden var netop det, der så ud som et hak.
    try { window.scrollTo({ top: 0, behavior: 'instant' }); }
    catch (e) { window.scrollTo(0, 0); }

    // Karrusellen skal sættes op igen på det nye indhold
    if (window.__groKarrusel) window.__groKarrusel();

    // Skærmlæsere skal have besked om, at der er kommet en ny side
    main.setAttribute('tabindex', '-1');
    main.focus({ preventScroll: true });

    if (!roligt.matches) {
      main.classList.add('side-kommer-ind');
      main.addEventListener('animationend', function () {
        main.classList.remove('side-kommer-ind');
      }, { once: true });
    }
  }

  function navigér(url, gemIHistorik) {
    if (laaser) return;
    laaser = true;

    var main = document.querySelector('main');
    var ventetid = roligt.matches ? 0 : UD_MS;
    if (!roligt.matches) main.classList.add('side-gaar-ud');

    Promise.all([
      hent(url),
      new Promise(function (r) { setTimeout(r, ventetid); })
    ]).then(function (svar) {
      skift(svar[0], url, gemIHistorik);
      laaser = false;
    }).catch(function () {
      // Noget gik galt – lad browseren gøre det på den gammeldags måde
      location.href = url;
    });
  }

  // Peger man på en fane, hentes siden allerede dér. Klikket bliver så
  // øjeblikkeligt. Det svarer til det, Chrome gør med speculationrules.
  function forbered(e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (a && erInternLink(a)) hent(a.href).catch(function () {});
  }
  document.addEventListener('pointerenter', forbered, true);
  document.addEventListener('focusin', forbered);

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 ||
        e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || !erInternLink(a)) return;
    e.preventDefault();
    navigér(a.href, true);
  });

  window.addEventListener('popstate', function () {
    navigér(location.href, false);
  });
})();
