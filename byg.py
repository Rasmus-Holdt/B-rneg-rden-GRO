# -*- coding: utf-8 -*-
"""Bygger de statiske HTML-sider til Børnegården GRO.
Fælles header/footer ét sted, så alle sider er identiske i opsætning."""
import os, re

UD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

TLF_VIS = '27 12 23 07'
TLF = '27122307'
ADRESSE      = 'Vinderslevvej 45, Vinderslev, 8620 Kjellerup'
ADRESSE_KORT = 'Vinderslevvej 45, 8620 Kjellerup'
# Officiel adresse og koordinater slået op i DAWA (api.dataforsyningen.dk),
# adresse-id 0a3f50c5-363a-32b8-e044-0003ba298018:
#   Vinderslevvej 45, Vinderslev, 8620 Kjellerup · 56.25713 N, 9.43122 Ø
LAT = '56.25713'
LON = '9.43122'
KORT_SOEG = 'Vinderslevvej+45,+8620+Kjellerup'
INSTA = 'boernegaarden.gro'

# Ét sted at rette kortlinket. Søger på selve adressen frem for koordinater,
# fordi Google Maps så viser husnummeret i søgefeltet i stedet for to
# talrækker – det er nemmere at genkende for den, der klikker.
KORT_URL = f'https://www.google.com/maps/search/?api=1&amp;query={KORT_SOEG}'
RUTE_URL = f'https://www.google.com/maps/dir/?api=1&amp;destination={KORT_SOEG}'


def adresselink(tekst, klasse=''):
    """Adressen som klikbart kortlink.

    `target="_blank"` med vilje: kortet skal åbne ved siden af, ikke oven i
    siden. Bliver man sendt væk fra en side, man er ved at læse, kommer man
    sjældent tilbage.

    `rel="noopener"` er en sikkerhedsdetalje – uden den får den nye fane
    adgang til at sende vores side videre til en anden adresse.

    `title` fortæller, hvad der sker, inden man klikker. Uden den er det ikke
    tydeligt, at en adresse er et link og ikke bare tekst.
    """
    k = f' class="{klasse}"' if klasse else ''
    return (f'<a href="{KORT_URL}"{k} target="_blank" rel="noopener" '
            f'title="Åbn adressen i Google Maps">{tekst}</a>')
# Domænet står på Jeanettes egen plakat. Skal bekræftes – se indhold/02.
DOMAENE = 'https://www.boernegaardengro.dk'

SIDER = [
    ('index.html',           'Forside'),
    ('mudderklubben.html',   'Mudder&nbsp;Klubben'),
    ('vaerdier.html',        'Værdier'),
    ('her-hvor-vi-bor.html', 'Her hvor vi bor'),
    ('praktisk.html',        'Praktisk'),
    ('om-mig.html',          'Om mig'),
    ('kontakt.html',         'Kontakt'),
]

# --------------------------------------------------------------------------
# Solen og navnetrækket – begge tegnet af Jeanette selv i Canva.
#
# Her stod tidligere en sol tegnet i SVG. Jeanette havde sin egen, og hendes
# er bedre: den er tegnet med farveblyant, og den streg kan man ikke ramme
# med bézierkurver. Filerne klargøres i billeder/grafik.py.
#
# Hvorfor <picture> og ikke bare <img>: WebP-udgaven fylder 19 KB mod PNG'ens
# 30, og solen står i headeren på alle syv sider. Klassen sidder på <picture>
# og ikke på <img>, fordi det er <picture>, der er elementet i layoutet –
# billedet indeni fylder bare 100 % af den plads, CSS giver.
# --------------------------------------------------------------------------
import importlib.util as _iu2
_spec2 = _iu2.spec_from_file_location('_graf', os.path.join(UD, 'billeder', 'grafik.py'))
_graf = _iu2.module_from_spec(_spec2); _spec2.loader.exec_module(_graf)
GRAFIK = _graf.MAAL


def tegning(navn, cls, alt='', straks=False):
    b, h = GRAFIK[navn]
    # Tom alt + aria-hidden: solen er pynt. En skærmlæser skal ikke læse
    # "tegnet sol" op syv gange på en side, hvor den ikke betyder noget.
    a = f'alt="{alt}"' if alt else 'alt="" aria-hidden="true"'
    doven = '' if straks else ' loading="lazy"'
    hast = ' fetchpriority="high"' if straks else ''
    return (f'<picture class="{cls}">'
            f'<source type="image/webp" srcset="billeder/{navn}.webp">'
            f'<img src="billeder/{navn}.png" {a} width="{b}" height="{h}"'
            f'{doven}{hast} decoding="async"></picture>')


def sol(cls='sol', size=None):
    """`size` bruges ikke længere – størrelsen står i CSS, ét sted pr. plads.
    Beholdt i signaturen, så de mange kaldesteder ikke skal rettes."""
    return tegning('sol', cls or 'sol')

IKON = {
 'tlf':   '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'pin':   '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 'insta': '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.1" fill="currentColor" stroke="none"/>',
 'mail':  '<rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m3 6.5 9 6.5 9-6.5"/>',
 # Årstider: sol, snefnug og blad
 'sommer':'<circle cx="12" cy="12" r="4.6"/><path d="M12 1.8v2.8M12 19.4v2.8M1.8 12h2.8M19.4 12h2.8M4.8 4.8l2 2M17.2 17.2l2 2M19.2 4.8l-2 2M6.8 17.2l-2 2"/>',
 'vinter':'<path d="M12 2v20M3.3 7 20.7 17M20.7 7 3.3 17"/><path d="M9.4 4.2 12 6.8l2.6-2.6M9.4 19.8 12 17.2l2.6 2.6"/><path d="M4.7 10.5 5.4 7 8.9 7.7M19.3 13.5l-.7 3.5-3.5-.7M19.3 10.5l-.7-3.5-3.5.7M4.7 13.5l.7 3.5 3.5-.7"/>',
 'foraar':'<path d="M12 22v-8.4"/><path d="M12 13.6c0-4-3.2-7.2-7.2-7.2 0 4 3.2 7.2 7.2 7.2z"/><path d="M12 13.6c0-3.4 2.8-6.2 6.2-6.2 0 3.4-2.8 6.2-6.2 6.2z"/>',
 'venstre':'<path d="M15 4.5 7.5 12l7.5 7.5"/>',
 'hoejre': '<path d="M9 4.5 16.5 12 9 19.5"/>',
}

def ikon(navn, cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IKON[navn]}</svg>')


# --------------------------------------------------------------------------
# Stempelikoner – ét pr. mærke i mudderpasset. Tegnede stregikoner i samme
# stil som telefon/adresse-ikonerne, ikke emojis. 26x26 viewBox.
# --------------------------------------------------------------------------
STEMPEL_IKON = {
 'haand':   '<path d="M9 13V5a1.6 1.6 0 0 1 3.2 0v7"/><path d="M12.2 12V3.8a1.6 1.6 0 0 1 3.2 0V12"/><path d="M15.4 12.4V5.6a1.6 1.6 0 0 1 3.2 0V15"/><path d="M9 13v-2.4a1.6 1.6 0 0 0-3.2 0v5.6c0 3.9 2.6 6.8 6.2 6.8h2.2c3.3 0 5.4-2.6 5.4-6.2V15"/>',
 'fod':     '<path d="M11.6 22.6c-2.8 0-4.6-2.2-4.6-5.4 0-3.6 2-6.6 4.8-6.6s4.8 3 4.8 6.6c0 3.2-1.8 5.4-4.6 5.4z"/><circle cx="5.6" cy="6.6" r="1.6"/><circle cx="10.2" cy="4.2" r="1.7"/><circle cx="15" cy="4.8" r="1.6"/><circle cx="18.8" cy="7.6" r="1.4"/>',
 'draabe':  '<path d="M13 2.5s7 7.7 7 11.9a7 7 0 0 1-14 0C6 10.2 13 2.5 13 2.5z"/>',
 'kanin':   '<ellipse cx="8" cy="7" rx="2.1" ry="5"/><ellipse cx="14.6" cy="6.6" rx="2.1" ry="5"/><path d="M4.6 18a6.6 6.6 0 0 1 13.2 0 4 4 0 0 1-4 4h-5.2a4 4 0 0 1-4-4z"/><circle cx="9.4" cy="17.4" r=".9" fill="currentColor" stroke="none"/><circle cx="13.4" cy="17.4" r=".9" fill="currentColor" stroke="none"/>',
 'aeg':     '<path d="M12.5 2.5c3.8 0 7 4.9 7 9.4a7 7 0 0 1-14 0c0-4.5 3.2-9.4 7-9.4z"/><path d="M9 13.5a3.5 3.5 0 0 0 3.5 3.5"/>',
 'brod':    '<path d="M3.5 10.5c0-3 2.6-4.6 5.4-4.6h7.2c2.8 0 5.4 1.6 5.4 4.6 0 1.7-1.4 2.4-2.6 2.4v6.6a2 2 0 0 1-2 2H8.1a2 2 0 0 1-2-2V12.9c-1.2 0-2.6-.7-2.6-2.4z"/><path d="M9.6 6v7M15 6v7"/>',
 'orm':     '<path d="M3 20v-1.5a3.6 3.6 0 0 1 7.2 0 3.6 3.6 0 0 0 7.2 0v-3.6a3.6 3.6 0 0 1 3.6-3.6"/><circle cx="20.8" cy="10.6" r="1" fill="currentColor" stroke="none"/>',
 'plask':   '<path d="M12.5 3.5s5.4 6 5.4 9.4a5.4 5.4 0 0 1-10.8 0c0-3.4 5.4-9.4 5.4-9.4z"/><path d="M2.5 20h19"/><path d="M4.5 16.5 3 14.5M20.5 16.5 22 14.5"/>',
 'gulerod': '<path d="M13.6 9.4 6.2 20.4a1.4 1.4 0 0 1-2.3-.1 1.4 1.4 0 0 1 0-1.4L14.6 8.6z"/><path d="M14.6 8.6c1.6-1.6 4.2-1.8 5.9-.6-1 1.8-3.4 2.6-5.3 2"/><path d="M14.6 8.6c-1-2 .1-4.6 2-5.6 1 1.8.6 4.3-.9 5.6"/>',
 'blad':    '<path d="M4.5 20.5C4.5 11 10.8 4.5 21 4.5c0 10.2-6.5 16-16.5 16z"/><path d="M4.5 20.5 15 10"/>',
 'traktor': '<circle cx="8" cy="16.5" r="5"/><circle cx="18.5" cy="18" r="3.4"/><path d="M8 10.5V7h5.4l1.8 5.4h3.3"/><path d="M13.4 12.4H8"/>',
 'spand':   '<path d="M4.5 8.5h16l-1.8 12.2a1.6 1.6 0 0 1-1.6 1.3H7.9a1.6 1.6 0 0 1-1.6-1.3z"/><path d="M7 8.5a5.5 5.5 0 0 1 11 0"/><path d="M3 8.5h19"/>',
 'gryde':   '<path d="M3.5 10.5h17v7a4 4 0 0 1-4 4h-9a4 4 0 0 1-4-4z"/><path d="M20.5 12.5h1.8a1.6 1.6 0 0 1 0 3.2h-1.8M3.5 12.5H1.7a1.6 1.6 0 0 0 0 3.2h1.8"/><path d="M9 6.5c0-1.4 1-1.6 1-3M14 6.5c0-1.4 1-1.6 1-3"/>',
 'regnbue': '<path d="M2.5 20a10 10 0 0 1 20 0"/><path d="M6 20a6.5 6.5 0 0 1 13 0"/><path d="M9.5 20a3 3 0 0 1 6 0"/>',
 'gren':    '<path d="M12.5 22V6"/><path d="M12.5 12 7 7.5M12.5 15l5.5-4.5M12.5 8 8.5 3.5"/>',
 'gris':    '<path d="M3.5 12.5a9 9 0 0 1 18 0v3.6a5.4 5.4 0 0 1-5.4 5.4H8.9a5.4 5.4 0 0 1-5.4-5.4z"/><ellipse cx="12.5" cy="16" rx="3.6" ry="2.8"/><circle cx="11.2" cy="16" r=".8" fill="currentColor" stroke="none"/><circle cx="13.8" cy="16" r=".8" fill="currentColor" stroke="none"/><path d="M5.5 6 3 3.2M19.5 6 22 3.2"/>',
 'stoevle': '<path d="M7 2.5h5.5v10.8c0 1.6.8 3 2.2 3.8l3.4 2a3.4 3.4 0 0 1 1.6 2.9v.5H7z"/><path d="M7 15h5.6"/>',
 'spire':   '<path d="M12.5 21.5v-8"/><path d="M12.5 13.5C12.5 9.6 9.4 6.5 5.5 6.5c0 3.9 3.1 7 7 7z"/><path d="M12.5 13.5c0-3.3 2.7-6 6-6 0 3.3-2.7 6-6 6z"/><path d="M4.5 21.5h16"/>',
 'jakke':   '<path d="M9 2.5 12.5 6 16 2.5l4.5 2.3a2 2 0 0 1 1.1 1.8v4.9h-3v10a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1v-10h-3V6.6a2 2 0 0 1 1.1-1.8z"/><path d="M12.5 6v16"/>',
 'medalje': '<circle cx="12.5" cy="16" r="6"/><path d="M8.5 10.6 5.5 2.5h5l2.4 5.4M16.5 10.6l3-8.1h-5l-2.4 5.4"/><path d="M12.5 13.6v4.8M10.6 15.4h3.8"/>',
}


# --------------------------------------------------------------------------
# Billeder: WebP med JPEG-fallback, i to opløsninger.
# Browseren vælger selv format og størrelse, så en telefon uden retina-skærm
# ikke henter et billede i dobbelt opløsning. width/height står altid på,
# så pladsen er reserveret inden billedet er hentet – ingen layouthop.
# --------------------------------------------------------------------------
import importlib.util as _iu
_spec = _iu.spec_from_file_location('_besk', os.path.join(UD, 'billeder', 'beskaer.py'))
_besk = _iu.module_from_spec(_spec); _spec.loader.exec_module(_besk)
MAAL = _besk.MAAL

# Hvor bred pladsen er ved forskellige skærmbredder
SIZES = {
    # Pladserne er regnet efter det, de faktisk fylder, ikke gættet.
    # Genvejskortene: 900 px spalte minus to mellemrum på 24, delt med tre
    # = 284 px. Under 900 er de to i bredden, under 620 én.
    'genvej':         '(max-width: 620px) 88vw, (max-width: 900px) 34vw, 284px',
    # Forsidens to billeder: samme spalte, to i bredden = 438 px.
    'forside-foto':   '(max-width: 620px) 88vw, (max-width: 940px) 46vw, 438px',
    'blok':           '(max-width: 900px) 100vw, 530px',
    'galleri3':       '(max-width: 620px) 92vw, (max-width: 900px) 45vw, 340px',
    'galleri2':       '(max-width: 620px) 92vw, 45vw',
    # Jeanettes portræt fra sms. Pladsen er bevidst lille: originalen er
    # under 700 px bred, og vises den bredere, bliver den synligt uskarp.
    # Hellere et lille, skarpt billede end et stort, grødet.
    #
    # 76vw er målt, ikke gættet: på en 390 px skærm er der 15 px rullebjælke,
    # 2x20 px luft i .wrap og 2x26 px polstring i kortet tilbage at trække
    # fra – der er 283 px til billedet, altså 73 % af skærmbredden. Stod der
    # 62vw som før, regnede browseren med en mindre plads end den faktiske
    # og hentede en for lille fil, som så blev strukket op.
    'portraet':       '(max-width: 620px) 76vw, 300px',
}


def billede(navn, alt, plads, straks=False, cls=''):
    """Bygger et <picture> med tre spor: AVIF, WebP og JPEG.

    Browseren tager det første format, den kan læse. AVIF er ca. halv
    størrelse af WebP på disse fotos, så næsten alle besøgende henter
    det mindste. JPEG bliver kun brugt af meget gamle browsere.

    `straks=True` bruges kun til det billede, der står øverst på siden.
    Alle andre får loading="lazy", så de først hentes, når man ruller
    ned til dem.
    """
    b2, h2, b1, h1 = MAAL[navn]
    doven = '' if straks else ' loading="lazy"'
    hast = ' fetchpriority="high"' if straks else ''
    sizes = SIZES[plads]
    # Klassen sidder på <picture>, ikke på <img>: det er <picture>, der er
    # elementet i layoutet, og det er den, der skal kunne flyde eller
    # centreres. Sætter man klassen på <img>, kan CSS ikke få fat i den
    # kasse, billedet faktisk optager.
    k = f' class="{cls}"' if cls else ''
    return (
        f'<picture{k}>'
        f'<source type="image/avif" sizes="{sizes}" '
        f'srcset="billeder/{navn}-1x.avif {b1}w, billeder/{navn}.avif {b2}w">'
        f'<source type="image/webp" sizes="{sizes}" '
        f'srcset="billeder/{navn}-1x.webp {b1}w, billeder/{navn}.webp {b2}w">'
        f'<img src="billeder/{navn}.jpg" sizes="{sizes}" '
        f'srcset="billeder/{navn}-1x.jpg {b1}w, billeder/{navn}.jpg {b2}w" '
        f'alt="{alt}" width="{b2}" height="{h2}"{doven}{hast} decoding="async">'
        f'</picture>')


def karrusel(billeder, navn):
    """billeder = liste af (fil, alt, bredde, hoejde). Første indlæses med det
    samme, resten dovent – ellers henter browseren tre billeder for at vise ét."""
    dias = []
    for i, (fil, alt) in enumerate(billeder):
        dias.append('        <div class="karrusel-billede">'
                    + billede(fil, alt, 'blok', straks=(i == 0)) + '</div>')
    return f'''<div class="karrusel">
      <div class="karrusel-spor" tabindex="0" role="group"
           aria-roledescription="billedkarrusel" aria-label="{navn}">
{chr(10).join(dias)}
      </div>
      <span class="karrusel-tael" aria-hidden="true"></span>
      <button class="karrusel-pil karrusel-forrige" type="button" aria-label="Forrige billede">{ikon('venstre')}</button>
      <button class="karrusel-pil karrusel-naeste" type="button" aria-label="Næste billede">{ikon('hoejre')}</button>
      <div class="karrusel-bund">
        <div class="karrusel-prikker" role="tablist" aria-label="Vælg billede"></div>
      </div>
    </div>'''


def stempel_ikon(navn):
    return (f'<svg viewBox="-1 -1 26 26" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{STEMPEL_IKON[navn]}</svg>')

# --------------------------------------------------------------------------
def header(aktiv):
    AKT = ' aria-current="page"'
    faner = '\n'.join(
        '      <li><a href="%s"%s>%s</a></li>' % (f, AKT if f == aktiv else '', t)
        for f, t in SIDER)
    return f'''<a class="spring-til" href="#indhold">Spring til indhold</a>
<header class="top">
  <div class="top-inder">
    <a class="logo" href="index.html">
      {sol('sol')}
      <span>
        {tegning('logo-gro-lille', 'logo-navn', alt='Børnegården GRO', straks=True)}
        <span class="logo-under">Privat pasningsordning &middot; 0&ndash;3 år</span>
      </span>
    </a>
    <a class="top-ring" href="tel:+45{TLF}">{ikon('tlf')}<span class="ring-lang">Ring til Jeanette &middot; </span>{TLF_VIS}</a>
  </div>
  <nav class="faner" aria-label="Hovedmenu">
    <ul>
{faner}
    </ul>
  </nav>
</header>'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h2>Børnegården GRO</h2>
        <p class="daempet">Privat pasningsordning for børn i alderen 0&ndash;3 år
        på en gård ved Vinderslev, med dyr, have og en lille skov bag huset.</p>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul class="footer-kontakt">
          <li>{ikon('tlf')}<a href="tel:+45{TLF}">{TLF_VIS}</a></li>
          <li>{ikon('pin')}{adresselink('Vinderslevvej 45<br>Vinderslev, 8620 Kjellerup')}</li>
          <li>{ikon('insta')}<a href="https://www.instagram.com/{INSTA}/" target="_blank" rel="noopener">{INSTA}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bund">
      <span>&copy; Børnegården GRO v/ Jeanette Riis</span>
      <span>{adresselink(ADRESSE)}</span>
    </div>
  </div>
</footer>'''

# --------------------------------------------------------------------------
# Strukturerede data. Det er dem, der gør at Google kan vise adresse,
# telefonnummer og kort direkte i søgeresultatet frem for bare en blå linje.
# --------------------------------------------------------------------------
def strukturerede_data(fil, title, desc):
    import json
    virksomhed = {
        "@type": "ChildCare",
        "@id": DOMAENE + "/#virksomhed",
        "name": "Børnegården GRO",
        "alternateName": "Børnegården GRO – privat pasningsordning",
        "description": ("Privat pasningsordning for børn i alderen 0-3 år på en gård "
                        "ved Vinderslev nord for Silkeborg. Dyr, have, egen lille skov "
                        "og en hverdag med gårdliv, nærvær og vild leg."),
        "url": DOMAENE + "/",
        "telephone": "+45" + TLF,
        "image": DOMAENE + "/billeder/" + DELEBILLEDE["index.html"] + ".jpg",
        # Google bruger "logo" til at vise ikonet ved siden af virksomheden.
        # Det skal være kvadratisk og mindst 112 px – vores er 512.
        "logo": {"@type": "ImageObject",
                 "url": DOMAENE + "/logo-512.png",
                 "width": 512, "height": 512},
        "priceRange": "3.213 kr./md. i egenbetaling",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Vinderslevvej 45",
            "addressLocality": "Vinderslev",
            "postalCode": "8620",
            "addressRegion": "Kjellerup",
            "addressCountry": "DK",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": float(LAT), "longitude": float(LON)},
        # Link til kortet. Google bruger det til at koble stedet sammen med
        # den rigtige adresse frem for at gætte ud fra teksten.
        "hasMap": f"https://www.google.com/maps/search/?api=1&query={LAT},{LON}",
        "areaServed": [
            {"@type": "Place", "name": "Vinderslev"},
            {"@type": "Place", "name": "Kjellerup"},
            {"@type": "Place", "name": "Silkeborg Kommune"},
        ],
        "sameAs": ["https://www.instagram.com/" + INSTA + "/"],
        "founder": {"@id": DOMAENE + "/#jeanette"},
        "employee": {"@id": DOMAENE + "/#jeanette"},
        "knowsLanguage": "da",
        "currenciesAccepted": "DKK",
        "audience": {"@type": "PeopleAudience",
                     "suggestedMinAge": 0, "suggestedMaxAge": 3},
        # Selve ydelsen. Uden dette ved Google kun at der ligger en
        # virksomhed – ikke hvad man kan købe, eller hvad det koster.
        "makesOffer": {
            "@type": "Offer",
            "name": "Fast pasningsplads, 0–3 år",
            "priceCurrency": "DKK",
            "price": "3213",
            "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "price": "3213",
                "priceCurrency": "DKK",
                "unitText": "måned",
                "description": ("Egenbetaling efter kommunalt tilskud på "
                                "8.027 kr. fra Silkeborg Kommune."),
            },
            "areaServed": {"@type": "Place", "name": "Silkeborg Kommune"},
        },
    }

    # Jeanette som selvstændig enhed. Det er hende, folk søger efter ved
    # navn, og det er hende, siden "Om mig" faktisk handler om.
    jeanette = {
        "@type": "Person",
        "@id": DOMAENE + "/#jeanette",
        "name": "Jeanette Riis",
        "jobTitle": "Privat børnepasser",
        "description": ("Driver Børnegården GRO i Vinderslev og har haft "
                        "privat pasningsordning siden 2015."),
        "url": DOMAENE + "/om-mig.html",
        "image": DOMAENE + "/billeder/jeanette.jpg",
        "worksFor": {"@id": DOMAENE + "/#virksomhed"},
        "telephone": "+45" + TLF,
    }
    side = {
        "@type": "AboutPage" if fil == "om-mig.html" else
                 "ContactPage" if fil == "kontakt.html" else "WebPage",
        "@id": DOMAENE + "/" + ("" if fil == "index.html" else fil),
        "url": DOMAENE + "/" + ("" if fil == "index.html" else fil),
        "name": title,
        "description": desc,
        "inLanguage": "da-DK",
        "isPartOf": {"@id": DOMAENE + "/#hjemmeside"},
        "about": {"@id": DOMAENE + "/#jeanette" if fil == "om-mig.html"
                  else DOMAENE + "/#virksomhed"},
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": DOMAENE + "/billeder/" + DELEBILLEDE.get(fil, "forside-vandloeb") + ".jpg",
        },
    }
    hjemmeside = {
        "@type": "WebSite",
        "@id": DOMAENE + "/#hjemmeside",
        "name": "Børnegården GRO",
        "url": DOMAENE + "/",
        "inLanguage": "da-DK",
        "publisher": {"@id": DOMAENE + "/#virksomhed"},
    }
    graf = [virksomhed, jeanette, hjemmeside, side]
    if fil != "index.html":
        titel_kort = dict(SIDER)[fil].replace("&nbsp;", " ")
        graf.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Forside", "item": DOMAENE + "/"},
                {"@type": "ListItem", "position": 2, "name": titel_kort,
                 "item": DOMAENE + "/" + fil},
            ],
        })
    data = {"@context": "https://schema.org", "@graph": graf}
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            + '</script>')


MAL = '''<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="da_DK">
<meta property="og:site_name" content="Børnegården GRO">
<link rel="canonical" href="{DOMAENE}/{fil}">
<meta property="og:url" content="{DOMAENE}/{fil}">
<meta property="og:image" content="{DOMAENE}/billeder/{delebillede}.jpg">
<meta property="og:image:width" content="{delebillede_b}">
<meta property="og:image:height" content="{delebillede_h}">
<meta property="og:image:alt" content="{delebillede_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="geo.region" content="DK-82">
<meta name="geo.placename" content="Vinderslev, Kjellerup">
<!-- Skrifterne ligger på vores egen server. Ingen fremmed forbindelse skal
     åbnes først, og der sendes ingen besøgsdata til Google. De tre filer er
     variable og beskåret til danske tegn: 75 KB i alt mod ca. 207 KB før. -->
<link rel="preload" href="assets/skrifter/nunito.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/skrifter/fredoka.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.min.css">
<!-- Peger man på en fane, henter og optegner browseren siden på forhånd.
     Klikket bliver derefter øjeblikkeligt. "moderate" betyder: først når
     musen har hvilet ca. 200 ms, så der ikke hentes sider i blinde. -->
<script type="speculationrules">
{spekulation}
</script>
{preload}
<!-- Fanebladets ikon er Jeanettes tegnede sol, se billeder/faviconer.py.
     Fire PNG'er, én pr. størrelse browseren beder om. Hver er tegnet for sig
     med den luft, der passer til dén størrelse, i stedet for at blive
     skaleret ned fra én stor fil – ved 16 px er der ikke pixels at spilde.
     Google vil have et kvadratisk favicon i en størrelse deleligt med 48
     og tager gerne den største, der er erklæret; derfor står 96 med.
     favicon.ico er ikke erklæret her, men ligger stadig i roden: browsere
     og bots henter /favicon.ico af gammel vane, uanset hvad der står i
     HTML'en. Det samme gælder favicon.svg – tegningen er pixels, ikke
     kurver, og en SVG med et billede pakket ind i sig er kun en dyrere PNG. -->
<link rel="icon" href="favicon-16.png" type="image/png" sizes="16x16">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="favicon-48.png" type="image/png" sizes="48x48">
<link rel="icon" href="favicon-96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#fbf3e6">
<meta name="apple-mobile-web-app-title" content="GRO">
{jsonld}
</head>
<body>
{header}
<main id="indhold">
{indhold}
</main>
{footer}
<script src="assets/karrusel.js" defer></script>
<script src="assets/overgang.js" defer></script>
</body>
</html>
'''

# Det første billede på hver side. To ting sker med det:
#   1. Det forhåndshentes i <head>, så browseren ikke først skal læse hele
#      HTML'en for at opdage det. Det er sidens "største element", og det er
#      dét, Google måler sidens hastighed på.
#   2. Det får fetchpriority="high" og IKKE loading="lazy" – et dovent
#      førstebillede er den klassiske måde at ødelægge sin egen LCP-score på.
# Før stod kun forsiden og "her hvor vi bor" her; de fem øvrige sider ventede
# med deres topbillede til alt andet var hentet.
# Forsiden står ikke længere her. Dens største element er nu Jeanettes
# navnetræk øverst, ikke et foto, og det forhåndshentes for sig nedenfor –
# det er en PNG/WebP med gennemsigtig baggrund og hører ikke til i
# fotosporet med AVIF og srcset.
PRELOAD = {
    'mudderklubben.html':   'mk-mudder',
    'vaerdier.html':        'vd-ro',
    'her-hvor-vi-bor.html': 'sted-hus',
    'praktisk.html':        'praktisk-regntoej',
    'om-mig.html':          'jeanette',
}

# Hvilken pladsstørrelse (se SIZES) det forudhentede billede vises i.
# Forsiden står ikke længere her: dens topbillede er navnetrækket, som
# forhåndshentes for sig i skriv(). "Om mig" starter med portrættet af
# Jeanette, og det ligger i en smal flydende plads – ikke i den brede
# blok-plads, resten af siderne bruger.
PRELOAD_PLADS = {
    'om-mig.html': 'portraet',
}

# Billedet der vises, når nogen deler siden på Facebook eller i en sms.
# Uden dette fik alle syv sider forsidens gynge – også siden om økonomi.
DELEBILLEDE = {
    'index.html':           'forside-vandloeb',
    'mudderklubben.html':   'mk-mudder',
    'vaerdier.html':        'vd-ro',
    'her-hvor-vi-bor.html': 'sted-hus',
    'praktisk.html':        'praktisk-regntoej',
    'om-mig.html':          'jeanette-boern',
    'kontakt.html':         'sted-hus',
}

DELEBILLEDE_ALT = {
    'forside-vandloeb':  'Barn der graver ved vandløbet i haven hos Børnegården GRO',
    'mk-mudder':         'Børn der leger i mudderet i Mudder Klubben',
    'vd-ro':             'Barn der hviler i en rolig krog af haven',
    'sted-hus':          'Gården og huset, hvor Børnegården GRO holder til',
    'praktisk-regntoej': 'Barn i regntøj og gummistøvler klar til udeleg',
    'om-mig':            'Jeanette Riis, der driver Børnegården GRO',
    'jeanette-boern':    'Jeanette sammen med to børn ved døren til huset',
}


# Forudrendering: browseren henter og optegner siden allerede når musen
# hviler på en fane. Kun de syv rigtige sider – ikke test-filen.
SPEKULATION = _json_regler = (
    '{"prerender":[{"where":{"or":['
    + ','.join('{"href_matches":"' + f + '"}' for f, _ in SIDER)
    + ']},"eagerness":"moderate"}]}'
)


def skriv(fil, title, desc, indhold):
    navn = PRELOAD.get(fil)
    if navn:
        b2, h2, b1, h1 = MAAL[navn]
        # Kun AVIF forhåndshentes. Preloader man begge formater, henter
        # browseren dem begge to og dobbelt så mange bytes som nødvendigt.
        # Browsere uden AVIF ignorerer linjen og henter WebP som normalt.
        preload = (f'<link rel="preload" as="image" type="image/avif" '
                   f'imagesrcset="billeder/{navn}-1x.avif {b1}w, billeder/{navn}.avif {b2}w" '
                   f'imagesizes="{SIZES[PRELOAD_PLADS.get(fil, "blok")]}" '
                   f'fetchpriority="high">')
    elif fil == 'index.html':
        preload = ('<link rel="preload" as="image" type="image/webp" '
                   'href="billeder/logo-gro.webp" fetchpriority="high">')
    else:
        preload = ''

    del_navn = DELEBILLEDE.get(fil, 'forside-vandloeb')
    del_b, del_h, _, _ = MAAL[del_navn]

    html = MAL.format(title=title, desc=desc, header=header(fil),
                      footer=footer(), indhold=indhold, preload=preload,
                      jsonld=strukturerede_data(fil, title, desc),
                      spekulation=SPEKULATION,
                      delebillede=del_navn, delebillede_b=del_b,
                      delebillede_h=del_h,
                      delebillede_alt=DELEBILLEDE_ALT[del_navn],
                      fil='' if fil == 'index.html' else fil, DOMAENE=DOMAENE)
    with open(UD + fil, 'w', encoding='utf-8') as f:
        f.write(html)
    print('skrev', fil, len(html), 'tegn')

# ==========================================================================
# FORSIDE
# ==========================================================================
# Forsiden er skrevet om efter Jeanettes rettelser i august:
#   * Navnetrækket fra Canva står som overskrift i stedet for sat tekst.
#   * "Gårdliv, nærvær og vild leg" er flyttet fra toppen ned som slutlinje.
#   * Al brødtekst er samlet i ét bredt stykke. Før var den delt i to kort
#     med en billedklynge imellem, og teksten blev læst i to omgange.
#   * Teksten er hendes egen, ord for ord. De fire afsnit, der før stod her
#     med henvisninger videre til de andre sider, er taget ud – de var
#     skrevet af mig, ikke af hende. Vejen videre går nu gennem de tre
#     genvejskort nederst i stedet.
#   * Ledige pladser er væk herfra og står kun under "Praktisk".
forside = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero-kort hero-bred">
      {sol('sol-hjoerne')}
      <h1>{tegning('logo-gro', 'logo-tegning', alt='Børnegården GRO', straks=True)}</h1>
      <p class="forord">Der findes en barndom, de fleste af os drømmer om til vores børn.</p>
      <p>En barndom med jord under neglene, dufte af nybagt brød, dyr der skal fodres,
         og dage der har plads til både ro og vild leg. Den slags minder, man selv
         ligger og smiler af mange år senere.</p>
      <p><strong>Det er den barndom, Børnegården GRO er bygget op omkring.</strong></p>
      <p>Her fodrer børnene dyrene om morgenen og hjælper til med rigtige opgaver
         &ndash; det giver dem en følelse af at høre til og kunne noget. Der er tid til
         bare at være: rolige stunder, nærvær og hygge, uden at der konstant skal ske
         noget. Og der er plads til, at børn får lov at være børn &ndash; hoppe i
         vandpytter, grave i den kæmpe sandkasse og mudre løs i mudderkøkkenet, indtil
         de kommer hjem glade og lidt beskidte.</p>
      <p class="under">Gårdliv, nærvær og vild leg,<br>flettet sammen til én hverdag.</p>
      <div class="knapper">
        <a class="knap knap-primaer" href="tel:+45{TLF}">{ikon('tlf')} Ring {TLF_VIS}</a>
        <a class="knap knap-sekundaer" href="her-hvor-vi-bor.html">Se stedet</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="galleri to forside-spalte">
      <figure>{billede('forside-vandloeb', 'Barn der graver ved vandløbet i haven', 'forside-foto')}</figure>
      <figure>{billede('forside-sandkasse', 'Barn der leger i den kæmpe sandkasse omkring træet', 'forside-foto')}</figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="genveje forside-spalte">
      <a class="genvej" href="mudderklubben.html">
        {billede('kort-mudderklub', 'Børn der graver og bygger i sandet', 'genvej')}
        <div class="genvej-tekst">
          <h2>Mudder Klubben</h2>
          <p>Mudderpas, traktorture til baghaveskoven og officiel tilladelse til at hoppe i alle vandpytter.</p>
          <span class="pil">Se klubben &rarr;</span>
        </div>
      </a>
      <a class="genvej" href="vaerdier.html">
        {billede('kort-vaerdier', 'Barn der hviler i den grønne hyggekrog', 'genvej')}
        <div class="genvej-tekst">
          <h2>Værdier</h2>
          <p>Ro og nærvær, tillid og selvstændighed, krop og sanser. Tre ben, der bærer hinanden.</p>
          <span class="pil">Læs mere &rarr;</span>
        </div>
      </a>
      <a class="genvej" href="her-hvor-vi-bor.html">
        {billede('kort-sted', 'Børn samlet omkring bålpladsen i haven', 'genvej')}
        <div class="genvej-tekst">
          <h2>Her hvor vi bor</h2>
          <p>Dagplejehuset, stalden, baghaveskoven og haven &ndash; fire steder, én hverdag.</p>
          <span class="pil">Se stedet &rarr;</span>
        </div>
      </a>
    </div>
  </div>
</section>
'''

# ==========================================================================
# MUDDER KLUBBEN
# ==========================================================================
STEMPLER = [
 ('haand',   'Lavet et mudderhåndaftryk', ''),
 ('fod',     'Fodaftryk i sandkassen', ''),
 ('draabe',  'Bare tæer i en vandpyt', ''),
 ('kanin',   'Klappet en kanin', ''),
 ('aeg',     'Samlet æg ved hønsene', ''),
 ('brod',    'Første gang med hænderne i dejen', 'når der bages brød'),
 ('orm',     'Fundet en regnorm', ''),
 ('plask',   'Første rigtige vandpyt-hop', 'med begge fødder på én gang'),
 ('gulerod', 'Hjulpet med at give dyrene mad', ''),
 ('blad',    'Samlet blade eller kastanjer', ''),
 ('traktor', 'Første tur i traktorvognen', 'op til baghaveskoven'),
 ('spand',   'Bygget et &bdquo;slot&ldquo; eller hul', 'i sandkassen'),
 ('gryde',   'Lavet en lækker ret i mudderkøkkenet', ''),
 ('regnbue', 'Set en regnbue efter regn', ''),
 ('gren',    'Kravlet på den første gren eller stub', ''),
 ('gris',    'Kendt en af gårdens dyr ved navn', ''),
 ('stoevle', 'Hoppet i en vandpyt', ''),
 ('spire',   'Passet noget, der gror', ''),
 ('jakke',   'Klaret at tage gummistøvler og regntøj på selv', ''),
 ('medalje', 'Blevet den, der viser en ny, mindre ven mudderkøkkenet', ''),
]
stempel_html = '\n'.join(
    '        <li><span class="stempel-ikon">%s</span><span class="stempel-tekst">%s%s</span></li>'
    % (stempel_ikon(i), t, f'<span>{u}</span>' if u else '')
    for i, t, u in STEMPLER)

FORDELE = [
 ('traktor', 'Sæde i traktorvognen', ' (fastspændt og sikkert) på vej til klubbens egen ekspeditionsskov i baghaven'),
 ('spand',   'Fuld adgang til den kæmpe sandkasse', ''),
 ('gryde',   'VIP-plads i mudderkøkkenet', ', hvor der bages, røres og serveres retter, som ingen Michelin-kok nogensinde vil forstå'),
 ('plask',   'Officiel tilladelse til at hoppe i alle vandpytter', ''),
 ('haand',   'Ret til at komme hjem beskidt', ' &ndash; det er ikke et uheld, det er et bevis på en god dag'),
 ('regnbue', 'Æresmedlemskab af regnbuen efter regn', ', opdagelse af orme, biller og andre skattefund inkluderet'),
]
fordel_html = '\n'.join(
    '        <li><span class="fordel-ikon">%s</span><span class="fordel-tekst"><strong>%s</strong>%s</span></li>'
    % (stempel_ikon(i), a, b) for i, a, b in FORDELE)

# Skrevet om efter Jeanettes rettelser:
#   * Manchetten er sat i Caveat som på forsiden, ikke i almindelig grå tekst.
#   * Teksten kører nu som ét sammenhængende stykke – "ud i en smøre", som
#     hun skrev – med fed dér hvor hun har sat fed, og afsnitsmellemrum
#     dér hvor hun har lavet dem. Før var den brudt op i fire kort med
#     overskrifter, jeg selv havde fundet på.
#   * Afsnittene "Turen begynder med traktoren" og "Skovlegepladsen" er
#     slettet efter hendes ønske. Billederne fra dem (mk-traktor og
#     mk-skovhule) er flyttet ned i galleriet, så de ikke går tabt.
mudder = f'''
<div class="wrap">
  <div class="sidehoved">
    {sol('sol-hjoerne')}
    <p class="brodkrumme">Mudder Klubben</p>
    <h1>Velkommen til Mudder&nbsp;Klubben</h1>
    <p class="forord">Der findes et lille selskab i Børnegården GRO, som ikke alle børn
    kender til, før de selv bliver en del af det:</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="blok">
      <div class="blok-billede">{billede('mk-mudder', 'Barn i regntøj der graver i mudderet med legetøjsgravemaskine', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <p><strong>Mudder Klubben.</strong> Det er ikke noget, man bare er. Det er noget,
          man bliver optaget i &ndash; med sit eget mudderpas, sit eget navn på klublisten,
          og retten til alt det, der følger med.</p>
          <p><strong>Sådan bliver man medlem:</strong> Første dag i Børnegården GRO får jeres
          barn sit eget mudderpas &ndash; et lille, personligt hæfte, der stemples, første
          gang der graves, mudres eller opdages noget nyt. Det er ikke noget, man skal søge
          om eller kvalificere sig til. Man bliver simpelthen inviteret ind, den dag man
          starter &ndash; og så er det op til stemplerne at vise, hvor mange ekspeditioner
          det er blevet til.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kort">
      <h2>Medlemsfordele</h2>
      <p class="daempet">Som medlem af Mudder Klubben får jeres barn:</p>
      <ul class="fordele">
{fordel_html}
      </ul>
    </div>

    <div class="galleri to luft-over">
      <figure>{billede('mk-traktor', 'Barn på traktoren i haven', 'galleri2')}<figcaption>Traktoren holder klar med plads i vognen</figcaption></figure>
      <figure>{billede('mk-skovhule', 'Børn der sidder i en hule bygget af grene i skoven', 'galleri2')}<figcaption>Skjulesteder, kun medlemmer kender til</figcaption></figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kort fremhaevet smal">
      <p class="stor-tekst nulmargen"><strong>Bag legen ligger der noget rigtig godt:</strong>
      mudder og vand er nogle af de bedste redskaber, vi har til at styrke børns sanser,
      finmotorik og nysgerrighed. Men det behøver ikke at lyde kedeligt og fagligt for at
      virke &ndash; det skal bare føles som ren sjov. Og det gør det.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="pas">
      <div class="pas-hoved">
        {sol('sol-pas')}
        <div>
          <h2>Stempler i mudderpasset</h2>
          <p class="daempet nulmargen">Fra første dag til børnehavestart</p>
        </div>
        <span class="pas-maerke">20 stempler</span>
      </div>
      <p>Stemplerne følger barnets egen udvikling, så passet vokser sammen med barnet.
      De yngste får stempler for helt små, sanselige &bdquo;første gange&ldquo; &ndash; de ældste får
      stempler for mere selvstændige bedrifter. Det gør passet til en lille udviklingshistorie.</p>
      <ul class="stempler">
{stempel_html}
      </ul>
      <p class="luft-over"><strong>Passet bliver ikke stemplet efter en fast plan.</strong>
      Det følger, hvad det enkelte barn rent faktisk oplever og er klar til. Nogle stempler
      kommer tidligt, andre sent, og det er meningen. Det er barnets egen rejse, ikke en
      tjekliste, der skal nås.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="galleri">
      <figure>{billede('mk-legeplads', 'Sandkassen med køretøjer og dæk', 'galleri3')}<figcaption>Køretøjer, dæk og en kæmpe sandkasse</figcaption></figure>
      <figure>{billede('mk-vandkanal', 'Vandkanal gravet gennem sandet', 'galleri3')}<figcaption>Vand, jord og et spadestik</figcaption></figure>
      <figure>{billede('mk-skovsti', 'Børn på tur i skoven', 'galleri3')}<figcaption>Stier, der skal udforskes</figcaption></figure>
    </div>
  </div>
</section>
'''

# ==========================================================================
# VÆRDIER
# ==========================================================================
# Overskrift og manchet er skåret væk efter Jeanettes rettelse: "det står
# jo som jeg har bedt om, men jeg synes det lyder lidt dumt". Tilbage står
# fanens eget navn og de tre værdier, som taler for sig selv.
vaerdier = f'''
<div class="wrap">
  <div class="sidehoved sidehoved-lav">
    {sol('sol-titel')}
    <h1>Værdier</h1>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="blok">
      <div class="blok-billede">{billede('vd-ro', 'Rolig legekrog med sengehimmel og borde i barnehøjde', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <span class="vaerdi-nr">1</span>
          <h2>Ro og nærvær</h2>
          <p>Jeg har brugt tid på at fordybe mig i og erfare, hvordan man som voksen møder et
          barn med ægte ro &ndash; hvordan man er til stede, når et barn er ked af det, glad,
          vred eller bare skal have et kram, uden selv at være et andet sted i tankerne.</p>
          <p>Det betyder, at der ikke altid skal ske noget. At en stille stund med en billedbog
          i skødet er lige så værdifuld som en krea-dag. Og at børnene mærker en voksen, der er
          helt til stede &ndash; ikke en, der har travlt eller er distraheret.</p>
        </div>
      </div>
    </div>

    <div class="blok vendt">
      <div class="blok-billede">{billede('vd-tillid', 'To børn i regntøj der pumper vand op i en balje', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <span class="vaerdi-nr">2</span>
          <h2>Tillid og selvstændighed</h2>
          <p>Jeg arbejder ud fra en grundtanke om, at børn ikke skal underholdes hele tiden
          &ndash; de skal inviteres med i det rigtige liv. Når et barn hjælper med at fodre
          dyrene, ælte dej, dække bord eller bære en lille spand vand, er det en rigtig opgave
          med et rigtigt formål, og barnet mærker på egen krop, at det kan noget og betyder noget.</p>
          <p>Den samme tillid gælder følelser: børn må mærke det hele &ndash; vrede, skuffelse,
          glæde &ndash; uden at blive skyndet videre eller overdynget med ros. De skal opleve,
          at en voksen tror på, at de selv kan finde vej igennem det, med en rolig hånd at holde
          i, hvis det bliver svært.</p>
        </div>
      </div>
    </div>

    <div class="blok">
      <div class="blok-billede">{billede('vd-vildt', 'To børn der graver og undersøger jorden i skoven', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <span class="vaerdi-nr">3</span>
          <h2>Krop, sanser og det vilde</h2>
          <p>Al den ro og alt det ansvar skal have en modvægt, og den finder vi i Mudder Klubben.
          Her får kroppen og sanserne frit spil: jord under neglene, vand mellem tæerne,
          motorikopdagelser og eventyr i en kæmpe sandkasse og på traktorture til baghaveskoven.</p>
          <p>Det er ikke tilfældigt, at det fylder så meget. Bevægelse, motorik, sanseindtryk,
          kærlighed til dyr og fri leg i naturen er noget af det, der giver børn den bedste
          grobund &ndash; fysisk, følelsesmæssigt og socialt.</p>
          <p><a href="mudderklubben.html">Se Mudder Klubben &rarr;</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="citat">
      Ro, tillid og vild leg lyder som modsætninger.<br>
      Hos os er det de tre ben, der bærer hinanden &ndash; og hele grunden til,
      at hverdagen i GRO ser ud, som den gør.
    </div>
  </div>
</section>
'''

# ==========================================================================
# HER HVOR VI BOR
# ==========================================================================
# "Fire steder, én hverdag", indledningen og de fire ikoner er slettet efter
# Jeanettes rettelse – hun ville gå direkte til Dagplejehuset. Sætningen
# "Fire steder, én hverdag" står stadig som afslutning nederst, hvor hun
# selv har skrevet den.
sted = f'''
<div class="wrap">
  <div class="sidehoved sidehoved-lav">
    {sol('sol-titel')}
    <h1>Her hvor vi bor</h1>
  </div>
</div>

<section id="dagplejehuset">
  <div class="wrap">
    <div class="blok">
      <div class="blok-billede">{karrusel([
        ('sted-hus',  'Børn der leger på puder og trædesten i legestuen'),
        ('sted-hus2', 'Barn der klatrer på klatrevæggen i Tumleren'),
        ('sted-hus3', 'Legestuen med bogreol, tavle og plads til at lege'),
      ], 'Billeder fra dagplejehuset')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <h2>Dagplejehuset</h2>
          <p>Vi har ikke bare et hjørne eller et værelse med legetøj &ndash; vi har et helt hus,
          indrettet fra bunden til de 0&ndash;3-årige. Plads til at kravle og boltre sig i
          &bdquo;Tumleren&ldquo;, plads til at bygge, plads til at trække sig tilbage til en rolig
          stund, når det er der brug for.</p>
          <p>Et sted, hvor alting er i barnehøjde, fordi det er barnets hus lige så meget,
          som det er mit.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="stalden">
  <div class="wrap">
    <div class="blok vendt">
      <div class="blok-billede">{billede('sted-stald', 'Lille gris i græsset ved stalden', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <h2>Stalden</h2>
          <p>Gå gennem døren til stalden, og I møder både dyrene og en duft af hø. Her er højt
          til loftet, bogstaveligt talt &ndash; plads til at hoppe og svinge sig i høet, plads til
          at komme tæt på dyrene, og plads til de opgaver, der hører til: at give mad, samle æg,
          klappe dyrene eller bare stå og kigge.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="baghaveskoven">
  <div class="wrap">
    <div class="blok">
      <div class="blok-billede">{billede('sted-skov', 'Børn der klatrer på dæk mellem træerne i baghaveskoven', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <h2>Baghaveskoven</h2>
          <p>For enden af haven ligger vores egen lille skov, med en skovlegeplads gemt mellem
          træerne. Her er stier, der skal udforskes, grene der skal klatres i, og en helt anden
          ro end i haven &ndash; skovens egen stemning, kun et par minutters gåtur
          (eller traktortur) hjemmefra.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="haven">
  <div class="wrap">
    <div class="blok vendt">
      <div class="blok-billede">{billede('sted-have', 'Havens legeområde med sandkasse, dæk og redskaber', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <h2>Haven</h2>
          <p>Og så er der haven. En kæmpe have, hvor hver eneste del er tænkt til leg:
          mudderkøkkenet, den store sandkasse, kroge og gemmesteder, plads til at løbe,
          og plads til at bygge og til at grave.</p>
        </div>
      </div>
    </div>
    <div class="galleri to">
      <figure>{billede('sted-have2', 'Det lange mudderkøkken med gryder og skåle', 'galleri2')}<figcaption>Mudderkøkkenet, hvor der bages, røres og serveres</figcaption></figure>
      <figure>{billede('sted-have3', 'Havens legeområde med borde, baljer og redskaber', 'galleri2')}<figcaption>Kroge og gemmesteder over hele haven</figcaption></figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="citat">
      Fire steder, én hverdag. Dagplejehuset, stalden, baghaveskoven og haven hænger sammen
      som ét stort legelandskab &ndash; og det er her, jeres barns dage kommer til at udspille sig.
    </div>
  </div>
</section>
'''

# ==========================================================================
# PRAKTISK
# ==========================================================================
# Jeanette bad om at få tømt den øverste kasse for alt undtagen teksten
# "Praktisk info". Manchetten og de fire genvejsikoner er derfor væk.
praktisk = f'''
<div class="wrap">
  <div class="sidehoved sidehoved-lav">
    {sol('sol-titel')}
    <h1>Praktisk info</h1>
  </div>
</div>

<section id="medbringe">
  <div class="wrap">
    <div class="blok">
      <div class="blok-billede">{billede('praktisk-regntoej', 'Barn i regntøj og gummistøvler ude i haven', 'blok')}</div>
      <div class="blok-tekst">
        <div class="prose">
          <h2>Hvad skal I medbringe</h2>
          <p>Da vi bruger en stor del af dagen udenfor &ndash; i haven, stalden og skoven &ndash;
          er det rare tøj, der tåler jord, vand og lidt af hvert, der betyder mest.</p>
        </div>
      </div>
    </div>

    <div class="pakkeliste">
      <div class="kort flad">
        <h3>Fast, hele året</h3>
        <ul class="liste">
          <li>Gummistøvler (når barnet kan gå)</li>
          <li>Regntøj &ndash; jakke og bukser</li>
          <li>Skiftetøj &ndash; ekstra sæt, gerne to</li>
          <li>Sutteflaske, modermælkserstatning og sut, hvis jeres barn bruger det</li>
          <li>Navn i alt tøj og fodtøj</li>
        </ul>
      </div>
      <div class="kort flad">
        <h3>Til hvile og tryghed</h3>
        <ul class="liste">
          <li>Dyne</li>
          <li>Barnevogn &ndash; gerne en brugt &bdquo;altanvogn&ldquo;, som kan stå her året rundt, hvis I ønsker det</li>
          <li>Godkendt barnevognssele</li>
          <li>En bamse, hvis det er en fast del af hverdagen derhjemme</li>
        </ul>
      </div>
    </div>

    <div class="kort luft-over">
      <h3>Efter sæson</h3>
      <ul class="saesoner">
        <li class="saeson-sommer">
          <span class="saeson-ikon">{ikon('sommer')}</span>
          <span class="saeson-tekst"><strong>Sommer</strong>
          Solhat og solcreme, påsmurt hjemmefra om morgenen</span>
        </li>
        <li class="saeson-vinter">
          <span class="saeson-ikon">{ikon('vinter')}</span>
          <span class="saeson-tekst"><strong>Vinter</strong>
          Varm flyverdragt, hue, vanter (gerne et par ekstra) og varme sokker eller futter</span>
        </li>
        <li class="saeson-foraar">
          <span class="saeson-ikon">{ikon('foraar')}</span>
          <span class="saeson-tekst"><strong>Forår og efterår</strong>
          Todelt termotøj</span>
        </li>
      </ul>
    </div>
  </div>
</section>

<section id="soerger-for">
  <div class="wrap">
    <div class="kort fremhaevet">
      <h2>Det jeg sørger for</h2>
      <p>I mange kommunale dagplejer er der ting, forældrene selv skal huske og betale for
      &ndash; oftest bleer, nogle steder også solcreme og skumvaskeklude. Hos os er det
      inkluderet, så I skal bruge mindre tid på indkøb og pakning:</p>
      <ul class="liste">
        <li><strong>Bleer</strong> &ndash; har I specifikke mærker, medbringes bleer selv</li>
        <li><strong>Vådservietter og klude</strong></li>
        <li><strong>Solcreme</strong> &ndash; smør selv hjemmefra om morgenen, så eftersmører jeg i løbet af dagen</li>
      </ul>
    </div>
  </div>
</section>

<section id="pladser">
  <div class="wrap">
    <div class="pladser">
      <h2>Ledige pladser</h2>
      <p class="daempet">Sådan ser det ud lige nu:</p>
      <ul class="pladser-liste">
        <li><span class="pladser-tal">2</span><span class="pladser-hvornaar">ledige pladser</span>Vinter 2026/2027</li>
        <li><span class="pladser-tal">1</span><span class="pladser-hvornaar">ledig plads</span>Forår 2027</li>
      </ul>
      <div class="knapper midt">
        <a class="knap knap-primaer" href="kontakt.html">{ikon('mail')} Hør nærmere om en plads</a>
      </div>
    </div>
  </div>
</section>

<section id="oekonomi">
  <div class="wrap">
    <div class="kort">
      <h2>Økonomi</h2>
      <dl>
        <div class="beloeb"><dt>Egenbetaling pr. måned</dt><dd>3.213 kr.</dd></div>
        <div class="beloeb"><dt>Kommunens tilskud i 2026</dt><dd>8.027 kr.</dd></div>
        <div class="beloeb sum"><dt>Samlet betaling for pladsen pr. måned</dt><dd>11.250 kr.</dd></div>
      </dl>
      <div class="fakta luft-over">
        <p class="nulmargen">Egenbetalingen er det, I selv betaler. Kommunens tilskud udbetales
        oveni, og tilsammen udgør de to beløb den samlede betaling for pladsen.</p>
      </div>
    </div>
  </div>
</section>
'''

# ==========================================================================
# OM MIG
# ==========================================================================
# Skrevet helt om efter Jeanettes rettelser. Hun bad om fire ting:
#   * "Jeg hedder Jeanette" skulle ned i almindelig skriftstørrelse. Den
#     store overskrift er derfor væk; sætningen står nu som første linje i
#     teksten, hvor den hører hjemme.
#   * Alt skulle samles i én kasse uden del-overskrifter. De tre h3'er,
#     jeg havde sat ind for at bryde teksten op, er slettet.
#   * Hendes egen tekst, i normal størrelse.
#   * Hendes eget portræt fra sms i stedet for det motiv, der stod her før.
#     Det andet sms-billede, hende med de to børn, lå et stykke tid
#     midtstillet nederst i kassen. Originalen er kun 697 px bred, så
#     det måtte vises i 342 px for at være skarpt – halvdelen af
#     tekstspaltens bredde. Det kom til at ligne noget, der var klistret
#     på bagefter, og er taget ud igen. Filerne ligger stadig i billeder/,
#     hvis der kommer en større udgave fra fotografen.
#
# Siden skal stadig have en h1 – uden den ved hverken Google eller en
# skærmlæser, hvad siden hedder. Den står som fanens navn og er sat ned i
# størrelse med .h1-dis, så den ikke råber.
om_mig = f'''
<div class="wrap">
  <div class="sidehoved sidehoved-lav sidehoved-smal">
    {sol('sol-titel')}
    <h1 class="h1-dis">Om mig</h1>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="kort smal">
      {billede('jeanette', 'Jeanette Riis, der driver Børnegården GRO', 'portraet', straks=True, cls='portraet-plads')}
      <p>Jeg hedder Jeanette. Jeg er 39 år, har været mor i 17 år, og har haft privat
      pasningsordning siden 2015.</p>
      <p>De første 36 måneder af et barns liv kommer ikke igen. Det er i de år, hjernen
      udvikler sig hurtigere end på noget andet tidspunkt i livet, og det er i de år, et barn
      lægger grunden for tryghed, tillid og selvværd &ndash; ofte uden at vi voksne lægger
      mærke til, hvor meget der egentlig sker.</p>
      <p>Vi lever i en tid, hvor de fleste har travlt. Hvor en skærm nemt bliver den, der
      holder styr på et barn, mens de voksne når det hele. Jeg tror på noget andet: at et barn
      har mest gavn af en voksen, der er til stede &ndash; og af selv at være en del af det,
      der sker, i stedet for kun at kigge på.</p>
      <p>Derfor tager jeg børnene med, når der skal fodres dyr, bages brød eller ordnes ting
      i haven. Ikke fordi det er en aktivitet, men fordi et barn, der får lov at bidrage til
      noget rigtigt, mærker sig selv som en del af et fællesskab &ndash; og bygger en
      selvtillid, der sidder dybere end ros nogensinde kan give.</p>
      <p>Jeg har brugt mange timer på at forstå, hvordan et lille barns hjerne og følelser
      udvikler sig i de første leveår. Et lille barn kan endnu ikke berolige sig selv i en
      svær følelse &ndash; det låner roen fra den voksne, det er sammen med. Når jeg selv er
      rolig, smitter det: et barns gråd, vrede eller frustration kan finde et sted at lande,
      fordi der er en tryg voksen at læne sig op ad.</p>
      <p>Det er den viden, jeg tager med ind i mødet med de mindste, hver eneste dag. Men lige
      så vigtigt er det, I finder mig med gummistøvlerne på midt i det hele. Jeg hopper selv i
      vandpytterne, graver med i mudderet, og sætter mig på gyngen, hvis der er brug for et
      skub eller to. For mig er rigtig leg noget, man er en del af, ikke noget, man kun står
      ved siden af og kigger på.</p>
      <p>Den barndom, et barn får fra de er helt små, spiller ind igennem hele deres liv,
      derfor er den så vigtig.</p>
    </div>
  </div>
</section>
'''

# ==========================================================================
# KONTAKT
# ==========================================================================
# "Kontakt Jeanette" er slettet efter hendes rettelse; overskriften er nu
# bare fanens navn. Kassen "Kom forbi" hedder "Adresse", og kassen med
# ledige pladser er væk – de står under "Praktisk" og skal kun stå ét sted,
# så der ikke er to tal at holde opdateret, når noget bliver besat.
kontakt = f'''
<div class="wrap">
  <div class="sidehoved">
    {sol('sol-hjoerne')}
    <h1>Kontakt</h1>
    <p class="manchet">Ring eller skriv &ndash; og kom endelig forbi. Vil I se stedet, aftaler vi
    bare et tidspunkt. Det er altid nemmest at mærke et sted ved at stå i det.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <ul class="kontaktveje">
      <li>
        <a href="tel:+45{TLF}">
          <span class="kontaktvej-ikon">{ikon('tlf')}</span>
          <span class="kontaktvej-navn">Ring</span>
          <span class="kontaktvej-vaerdi">{TLF_VIS}</span>
          <span class="kontaktvej-note">Hverdage &ndash; læg gerne en besked</span>
        </a>
      </li>
      <li>
        <a href="https://www.instagram.com/{INSTA}/" target="_blank" rel="noopener">
          <span class="kontaktvej-ikon">{ikon('insta')}</span>
          <span class="kontaktvej-navn">Skriv</span>
          <span class="kontaktvej-vaerdi">{INSTA}</span>
          <span class="kontaktvej-note">Send en besked på Instagram</span>
        </a>
      </li>
      <li>
        <a href="{KORT_URL}" target="_blank" rel="noopener" title="Åbn adressen i Google Maps">
          <span class="kontaktvej-ikon">{ikon('pin')}</span>
          <span class="kontaktvej-navn">Adresse</span>
          <span class="kontaktvej-vaerdi">Vinderslevvej 45</span>
          <span class="kontaktvej-note">Vinderslev, 8620 Kjellerup</span>
        </a>
      </li>
    </ul>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kort kortkort">
      <div class="kort-boks">
        <iframe
          title="Kort over {ADRESSE}"
          src="https://www.openstreetmap.org/export/embed.html?bbox=9.4032%2C56.2491%2C9.4592%2C56.2651&amp;layer=mapnik&amp;marker={LAT}%2C{LON}"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <div class="kort-adresse">
        <p class="nulmargen"><strong>{adresselink(ADRESSE)}</strong></p>
        <a class="knap knap-blank" href="{RUTE_URL}" target="_blank" rel="noopener">{ikon('pin')} Få rutevejledning</a>
      </div>
    </div>
  </div>
</section>
'''

# ==========================================================================
skriv('index.html',
      # Navnet står forrest, fordi en browserfane er smal: har man fem faner
      # åbne, kan man kun se de første ca. 15 tegn, og dér skal der stå
      # hvem det er. Søgeordene står lige efter og er stadig med i de 60
      # tegn, Google viser – ingen af delene ofres.
      'Børnegården GRO | Pasningsordning i Vinderslev ved Kjellerup',
      'Privat pasningsordning for børn på 0-3 år i Vinderslev ved Kjellerup. Gård med dyr, egen skov og stor have. 2 ledige pladser vinter 2026/2027. Ring 27 12 23 07.',
      forside)
skriv('mudderklubben.html',
      'Børnegården GRO | Mudder Klubben, mudderpas og traktorture',
      'Mudderpas, traktorture til baghaveskoven, den kæmpe sandkasse og officiel tilladelse til at hoppe i alle vandpytter.',
      mudder)
skriv('vaerdier.html',
      'Børnegården GRO | Værdier: ro, nærvær og vild leg',
      'Ro og nærvær, tillid og selvstændighed, krop og sanser. De tre ting, der ligger bag alt, hvad vi laver i Børnegården GRO.',
      vaerdier)
skriv('her-hvor-vi-bor.html',
      'Børnegården GRO | Gården: hus, stald, skov og have',
      'Dagplejehuset, stalden, baghaveskoven og haven – fire steder, der hænger sammen som ét stort legelandskab.',
      sted)
skriv('praktisk.html',
      'Børnegården GRO | Priser og ledige pladser ved Kjellerup',
      'Egenbetaling 3.213 kr./md., kommunalt tilskud 8.027 kr. Se ledige pladser, pakkeliste og hvad der er inkluderet i Børnegården GRO ved Kjellerup.',
      praktisk)
skriv('om-mig.html',
      'Børnegården GRO | Om Jeanette Riis, dagplejer siden 2015',
      'Jeanette Riis har haft privat pasningsordning siden 2015. Om ro, nærvær og at være med i legen fremfor at kigge på.',
      om_mig)
skriv('kontakt.html',
      'Børnegården GRO | Kontakt og find vej i Vinderslev',
      'Ring til Jeanette på 27 12 23 07 eller kom forbi Vinderslevvej 45, Vinderslev, 8620 Kjellerup. Se kort og rutevejledning.',
      kontakt)

# --------------------------------------------------------------------------
# Minificeret CSS. style.css bliver ved med at være den, man retter i –
# style.min.css er den, siderne henter. Sparer ca. en fjerdedel af vægten,
# og gzip på serveren tager resten.
# --------------------------------------------------------------------------
def minificer_css(css):
    ud = re.sub(r'/\*.*?\*/', '', css, flags=re.S)        # kommentarer væk
    ud = re.sub(r'\s+', ' ', ud)                           # linjeskift og indryk
    ud = re.sub(r'\s*([{}:;,>~])\s*', r'\1', ud)           # luft om tegnsætning
    ud = re.sub(r';}', '}', ud)                            # sidste semikolon
    ud = re.sub(r'(\W)0\.(\d)', r'\1.\2', ud)             # 0.5s -> .5s
    return ud.strip()


_raa = open(UD + 'assets/style.css', encoding='utf-8').read()
_min = minificer_css(_raa)
with open(UD + 'assets/style.min.css', 'w', encoding='utf-8') as f:
    f.write('/* Genereret af byg.py – ret assets/style.css i stedet */\n' + _min)
print(f'skrev assets/style.min.css  {len(_raa)/1024:.0f} KB -> {len(_min)/1024:.0f} KB'
      f'  ({100 - 100*len(_min)/len(_raa):.0f} % mindre)')

# --------------------------------------------------------------------------
# sitemap.xml og robots.txt – så søgemaskiner ved hvad der findes
# --------------------------------------------------------------------------
import datetime
idag = datetime.date.today().isoformat()
# Forsiden vægtes højest, kontakt og praktisk derefter (dem folk søger efter)
VAEGT = {'index.html': '1.0', 'praktisk.html': '0.9', 'kontakt.html': '0.9'}
poster = '\n'.join(
    f'  <url>\n'
    f'    <loc>{DOMAENE}/{"" if f == "index.html" else f}</loc>\n'
    f'    <lastmod>{idag}</lastmod>\n'
    f'    <changefreq>monthly</changefreq>\n'
    f'    <priority>{VAEGT.get(f, "0.8")}</priority>\n'
    f'  </url>' for f, _ in SIDER)
with open(UD + 'sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + poster + '\n</urlset>\n')
print('skrev sitemap.xml')

import json as _json
manifest = {
    "name": "Børnegården GRO",
    "short_name": "GRO",
    "description": "Privat pasningsordning for børn i alderen 0-3 år "
                   "i Vinderslev ved Kjellerup.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#fbf3e6",
    "theme_color": "#fbf3e6",
    "lang": "da-DK",
    "icons": [
        {"src": "ikon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "ikon-512.png", "sizes": "512x512", "type": "image/png"},
        # Android beskærer app-ikoner til cirkler; "maskable" har luft omkring
        {"src": "ikon-maskable-512.png", "sizes": "512x512",
         "type": "image/png", "purpose": "maskable"},
    ],
}
with open(UD + 'site.webmanifest', 'w', encoding='utf-8') as f:
    _json.dump(manifest, f, ensure_ascii=False, indent=2)
print('skrev site.webmanifest')

with open(UD + 'robots.txt', 'w', encoding='utf-8') as f:
    f.write('User-agent: *\n'
            'Allow: /\n\n'
            '# Kildemateriale og arbejdsfiler skal ikke i søgeresultaterne.\n'
            '# Bemærk: favicon-filerne i roden må IKKE blokeres – Google\n'
            '# skal kunne hente dem for at vise ikonet i søgeresultatet.\n'
            'Disallow: /kilder/\n'
            'Disallow: /indhold/\n'
            'Disallow: /overgang-test.html\n\n'
            f'Sitemap: {DOMAENE}/sitemap.xml\n')
print('skrev robots.txt')
