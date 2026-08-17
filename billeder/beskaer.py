# -*- coding: utf-8 -*-
"""Beskærer og optimerer Jeanettes originalfotos.

Kør fra denne mappe:  python3 beskaer.py

Hvert billede har en fast beskæring sat efter motivet og et fast sideforhold,
så CSS aldrig skal gætte. Ingen original bruges to steder – hvert af de 25
motiver på siden er forskelligt.

For hvert motiv laves seks filer:

    navn.avif      dobbelt opløsning, AVIF    ← det de fleste henter i dag
    navn.webp      dobbelt opløsning, WebP    ← browsere fra ca. 2016-2023
    navn.jpg       dobbelt opløsning, JPEG    ← fallback til gamle browsere
    navn-1x.avif   normal opløsning, AVIF     ← skærme uden retina
    navn-1x.webp   normal opløsning, WebP
    navn-1x.jpg    normal opløsning, JPEG

`vis` er den bredde, billedet faktisk fylder på skærmen i CSS-pixels. Alt
skaleres ud fra den, så vi ikke sender et 1160 px billede til en plads,
der er 275 px bred. Det var den største enkeltbesparelse.

Om kvaliteten: 2x-filen bliver vist i halv størrelse på skærmen. Derfor må
den komprimeres hårdere end 1x-filen uden at nogen kan se det – detaljerne
bliver alligevel klemt sammen af skærmen. Det er derfor tallene nedenfor er
forskellige for de to opløsninger.
"""
from PIL import Image
import os

# Absolutte stier ud fra filens egen placering. byg.py importerer MAAL herfra
# og kører fra roden, ikke fra billeder/ – med relative stier ledte den efter
# Jeanettes fotos ét niveau for højt oppe.
_HER = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HER, '..', 'kilder', 'fotos', '')   # udpakket zip fra Jeanette
OUT = os.path.join(_HER, '')

# 2x = retina. Vises i halv størrelse, tåler hårdere komprimering.
JPEG_KVALITET_2X = 78
WEBP_KVALITET_2X = 66
AVIF_KVALITET_2X = 50

# 1x = vises pixel for pixel. Skal være pænere.
JPEG_KVALITET_1X = 84
WEBP_KVALITET_1X = 76
AVIF_KVALITET_1X = 62

# Loft over, hvor meget én enkelt fil må fylde.
#
# Hvorfor: nogle af Jeanettes fotos er meget "kornede" – regnvejr, vådt græs,
# løv. Korn er tilfældig støj, og støj er det dyreste, der findes at
# komprimere. Med fast kvalitet blev regntøjs-billedet på praktisk-siden
# 240 KB, mens et roligt motiv i samme størrelse landede på 50 KB. Det ene
# billede kostede altså mere end resten af siden tilsammen.
#
# Derfor: koder vi filen, og er den for stor, koder vi igen med lavere
# kvalitet indtil den passer. Kornet forsvinder først – og det er alligevel
# usynligt, når billedet vises i halv størrelse på en telefon.
LOFT_2X_KB = 120
LOFT_1X_KB = 70

# (udfil, original, beskæring (x0,y0,x1,y1) som andele, sideforhold b/h, vis-bredde i px)
JOBS = [
    # ---- FORSIDE ----
    # De to billeder sad før i en polaroid-klynge ved siden af teksten og
    # fyldte 200 px. Da forsiden blev lagt om til ét bredt tekststykke,
    # rykkede de ned under teksten i en dobbeltspalte og fylder nu det
    # dobbelte. Derfor 540 i stedet for 200 – og 4/3 i stedet for kvadrat,
    # så beskæringen sker her og ikke med object-fit i browseren.
    ('hero-gynge',        'FullSizeRender-9.jpeg', (0.00, 0.26, 1.00, 1.00), 4/5, 360),
    ('forside-vandloeb',  'IMG_4849.JPG',          (0.05, 0.22, 0.78, 0.78), 4/3, 540),
    ('forside-sandkasse', 'IMG_3944.JPG',          (0.00, 0.02, 1.00, 1.00), 4/3, 540),

    # ---- FORSIDE: tre genvejskort ----
    ('kort-mudderklub',   'IMG_4353.JPG',          (0.00, 0.00, 1.00, 1.00), 4/3, 360),
    ('kort-vaerdier',     'IMG_3981.JPG',          (0.00, 0.06, 1.00, 0.92), 4/3, 360),
    ('kort-sted',         'FullSizeRender-8.jpeg', (0.02, 0.02, 0.98, 1.00), 4/3, 360),

    # ---- MUDDER KLUBBEN ----
    ('mk-mudder',   'FullSizeRender-2.jpeg', (0.00, 0.06, 1.00, 1.00), 3/2, 540),
    ('mk-traktor',  'FullSizeRender-7.jpeg', (0.00, 0.16, 1.00, 0.94), 3/2, 540),
    ('mk-skovhule', 'IMG_4829.JPG',          (0.00, 0.02, 1.00, 0.98), 4/5, 540),
    ('mk-legeplads','FullSizeRender-5.jpeg', (0.00, 0.10, 1.00, 0.80), 4/3, 350),
    ('mk-vandkanal','IMG_3948.JPG',          (0.00, 0.02, 1.00, 0.98), 4/3, 350),
    ('mk-skovsti',  'IMG_4825.JPG',          (0.00, 0.04, 1.00, 0.96), 4/3, 350),

    # ---- VÆRDIER ----
    ('vd-ro',     'IMG_4118.JPG',          (0.03, 0.09, 0.97, 0.97), 4/5, 540),
    ('vd-tillid', 'IMG_4821.JPG',          (0.00, 0.04, 1.00, 0.98), 4/5, 540),
    ('vd-vildt',  'FullSizeRender-1.jpeg', (0.00, 0.04, 1.00, 0.98), 4/5, 540),

    # ---- HER HVOR VI BOR ----
    # Alle fire steder i 3/2 og ikke 4/5. Teksten til hvert sted er tre-fire
    # linjer, og et stående billede gjorde blokkene 641 px høje med under en
    # tredjedel tekst i. Resten stod som tom creme, fire gange i træk.
    # Liggende format giver blokke på ca. 340 px, hvor billede og tekst vejer
    # det samme – og siden blev 1.200 px kortere at rulle igennem.
    # Beskæringen tager 40 % fra toppen og 60 % fra bunden af det, der skal
    # væk (se funktionen beskaer), så ansigter og motiv i den øverste
    # halvdel bliver stående.
    ('sted-hus',    'FullSizeRender-3.jpeg', (0.00, 0.10, 1.00, 0.94), 3/2, 540),
    ('sted-hus2',   'FullSizeRender-4.jpeg', (0.00, 0.08, 1.00, 0.72), 3/2, 540),
    ('sted-hus3',   'FullSizeRender.jpeg',   (0.00, 0.08, 1.00, 0.96), 3/2, 540),
    ('sted-stald',  'IMG_4250.JPG',          (0.00, 0.22, 1.00, 1.00), 3/2, 540),
    ('sted-skov',   'IMG_4239.JPG',          (0.06, 0.02, 0.94, 1.00), 3/2, 540),
    ('sted-have',   'IMG_4553.JPG',          (0.00, 0.22, 1.00, 0.96), 3/2, 540),
    ('sted-have2',  'IMG_5020.JPG',          (0.00, 0.02, 1.00, 0.88), 4/3, 530),
    ('sted-have3',  'IMG_4554.JPG',          (0.00, 0.04, 1.00, 0.96), 4/3, 530),

    # ---- PRAKTISK / OM MIG ----
    # 3/2 og ikke 4/5: teksten ved siden af er kun fire linjer, og et
    # stående billede gjorde blokken 641 px høj med 150 px tekst i.
    # Resten blev tom creme. Liggende format giver en blok på ca. 340 px,
    # hvor billede og tekst vejer nogenlunde det samme.
    ('praktisk-regntoej', 'FullSizeRender-6.jpeg', (0.00, 0.10, 1.00, 1.00), 3/2, 540),
    ('om-mig',            'IMG_4826.JPG',          (0.00, 0.02, 1.00, 0.98), 4/5, 540),

    # Jeanettes egne to billeder, sendt på sms. De er de eneste med hendes
    # ansigt på, og det er dem, siden "Om mig" skal bære. Originalerne er
    # under 700 px brede – derfor de små vis-bredder her: bliver pladsen
    # bredere end originalen, står der et opskaleret, sløret billede.
    ('jeanette',       'jeanette-portraet.jpeg', (0.00, 0.00, 1.00, 1.00), 4/5, 300),
    ('jeanette-boern', 'jeanette-boern.jpeg',    (0.00, 0.00, 1.00, 1.00), 3/2, 342),
]


def beskaer(im, box, ar):
    w, h = im.size
    x0, y0, x1, y1 = [int(round(v * (w if i % 2 == 0 else h)))
                      for i, v in enumerate(box)]
    im = im.crop((x0, y0, x1, y1))
    cw, ch = im.size
    nu = cw / ch
    if nu > ar:                      # for bred – tag fra siderne
        nw = int(round(ch * ar))
        o = (cw - nw) // 2
        im = im.crop((o, 0, o + nw, ch))
    elif nu < ar:                    # for høj – tag mest fra bunden
        nh = int(round(cw / ar))
        o = int((ch - nh) * 0.40)
        im = im.crop((0, o, cw, o + nh))
    return im


def gem_med_loft(ren, sti, fmt, kvalitet, loft_kb, gulv, **ekstra):
    """Gemmer filen. Er den større end loftet, prøves lavere kvalitet.

    `gulv` er den laveste kvalitet, vi vil gå ned til. Bliver filen stadig
    for stor dér, beholder vi den – bedre et lidt tungt billede end et grimt.
    """
    q = kvalitet
    while True:
        ren.save(sti, fmt, quality=q, **ekstra)
        kb = os.path.getsize(sti) / 1024
        if kb <= loft_kb or q <= gulv:
            return kb, q
        q -= 6


def gem(im, sti, bredde, retina):
    """Skalerer til `bredde` og gemmer som AVIF, WebP og JPEG."""
    if im.width != bredde:
        h = int(round(bredde * im.height / im.width))
        im = im.resize((bredde, h), Image.LANCZOS)
    ren = Image.new('RGB', im.size)      # nyt billede uden EXIF/GPS
    ren.paste(im)

    if retina:
        qj, qw, qa, loft = (JPEG_KVALITET_2X, WEBP_KVALITET_2X,
                            AVIF_KVALITET_2X, LOFT_2X_KB)
    else:
        qj, qw, qa, loft = (JPEG_KVALITET_1X, WEBP_KVALITET_1X,
                            AVIF_KVALITET_1X, LOFT_1X_KB)

    ren.save(sti + '.jpg', 'JPEG', quality=qj, optimize=True, progressive=True)

    # WebP får et rummeligere loft. Formatet er dårligere til korn end AVIF,
    # så tvinger man det ned på samme vægt, bliver billedet synligt udvasket.
    gem_med_loft(ren, sti + '.webp', 'WEBP', qw, loft * 1.6, 52, method=6)

    # speed=2 er langsomt at kode, men filen bliver mærkbart mindre. Det er
    # en engangsudgift her på maskinen; besøgende sparer hentetiden hver gang.
    _, brugt = gem_med_loft(ren, sti + '.avif', 'AVIF', qa, loft, 26,
                            speed=2, subsampling='4:2:0')
    return ren.size, brugt


# Bruges også af byg.py, så HTML'ens width/height altid matcher filerne.
#
# Her stod før bare `_vis * 2`. Det holdt kun, så længe originalen faktisk
# var dobbelt så bred som pladsen. Otte af Jeanettes billeder er mindre end
# det, og for dem skriver gem() en smallere fil (den skalerer aldrig OP),
# mens HTML'en blev ved med at love 1080 px. Browseren reserverede altså
# plads til et billede, der aldrig kom i den størrelse, og hele siden
# rykkede sig, når filen landede.
#
# Derfor regnes målene nu efter originalens virkelige størrelse. PIL læser
# kun filhovedet for at få .size, så det koster ingenting at slå op.
def _maal(src, box, ar, vis):
    with Image.open(SRC + src) as _im:
        w, h = _im.size
    x0, y0, x1, y1 = [int(round(v * (w if i % 2 == 0 else h)))
                      for i, v in enumerate(box)]
    cw, ch = x1 - x0, y1 - y0
    if cw / ch > ar:                       # for bred – der tages fra siderne
        cw = int(round(ch * ar))
    else:                                  # for høj – der tages fra bunden
        ch = int(round(cw / ar))
    def par(bredde):
        bredde = min(bredde, cw)
        return bredde, int(round(bredde * ch / cw))
    return par(vis * 2) + par(vis)


MAAL = {}
for _ud, _src, _box, _ar, _vis in JOBS:
    MAAL[_ud] = _maal(_src, _box, _ar, _vis)


if __name__ == '__main__':
    originaler = [j[1] for j in JOBS]
    dubletter = {x for x in originaler if originaler.count(x) > 1}
    assert not dubletter, f'Samme original bruges flere gange: {dubletter}'

    i_alt = {'jpg': 0, 'webp': 0, 'avif': 0}
    for ud, src, box, ar, vis in JOBS:
        raa = beskaer(Image.open(SRC + src).convert('RGB'), box, ar)
        if raa.width < vis * 2:
            print(f'  ! {ud}: originalen er kun {raa.width} px bred '
                  f'(ville gerne have {vis*2})')
        stor, q2 = gem(raa, OUT + ud, min(vis * 2, raa.width), retina=True)
        lille, _ = gem(raa, OUT + ud + '-1x', min(vis, raa.width), retina=False)

        k = {}
        for e in i_alt:
            k[e] = (os.path.getsize(f'{OUT}{ud}.{e}')
                    + os.path.getsize(f'{OUT}{ud}-1x.{e}')) / 1024
            i_alt[e] += k[e]
        skruet_ned = '  (korn: avif sat ned til q%d)' % q2 if q2 < AVIF_KVALITET_2X else ''
        print(f'{ud:20} {str(stor):>12} / {str(lille):>11}   '
              f'jpg {k["jpg"]:>5.0f} K   webp {k["webp"]:>5.0f} K   '
              f'avif {k["avif"]:>5.0f} K{skruet_ned}')

    print(f'\n{len(JOBS)} motiver')
    for e in ('jpg', 'webp', 'avif'):
        spar = 100 - 100 * i_alt[e] / i_alt['jpg']
        print(f'  {e.upper():5}-sporet ialt  {i_alt[e]/1024:5.2f} MB'
              + (f'   ({spar:.0f} % mindre end JPEG)' if e != 'jpg' else ''))
