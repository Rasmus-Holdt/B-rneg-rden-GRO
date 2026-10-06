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
from PIL import Image, ImageFilter
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
    # hero-gynge er ikke brugt paa nogen af de syv sider laengere (kun i
    # overgang-test.html, som skal slettes). Jeanette sendte samme foto igen
    # under "Baghaveskoven", saa motivet er flyttet derhen i 3/2.
    ('forside-vandloeb',  'sr-forside-vandloeb.jpg', (0.00, 0.00, 1.00, 1.00), 4/3, 540),
    ('forside-sandkasse', 'sr-forside-sandkasse.jpg', (0.00, 0.00, 1.00, 1.00), 4/3, 540),

    # ---- FORSIDE: tre genvejskort ----
    # Jeanettes rettelse: kortet skal vise et af sms-billederne. IMG_4353 var
    # kun 720x474 og blev beskaaret til 632 px; det nye er 720x694 og rammer
    # pladsen (720x540) praecist.
    # Jeanettes tredje rettelse: kortet skal vise et af de tre sms-billeder
    # under "Mudder Klubben". Det er nu børnene i mudderkøkkenet. x-grænserne
    # 1,5 % og 98,5 % skærer den lyserøde/grønne skærmbilledramme væk.
    ('kort-mudderklub',   'sms-mudder-koekken-boern.jpg', (0.015, 0.10, 0.985, 0.60), 4/3, 360),
    ('kort-vaerdier',     'IMG_3981.JPG',          (0.00, 0.06, 1.00, 0.92), 4/3, 360),
    ('kort-sted',         'FullSizeRender-8.jpeg', (0.02, 0.02, 0.98, 1.00), 4/3, 360),

    # ---- MUDDER KLUBBEN ----
    # Karrusellen ved introteksten er byttet ud med de tre billeder, Jeanette
    # sendte på sms under "Mudder Klubben": vandløbet, børnene i mudderkøkkenet
    # og bordet med gryder (sidstnævnte er motivet 'sted-have2', som også
    # står i Haven – samme fil, ingen ny).
    # mk-mudder og mk-legeplads er taget ud af siden.
    # Barnet står i 59-541 px af de 694; vinduet er lagt, så hele barnet er med.
    ('mk-vandloeb', 'sms-mudder-vandloeb.jpg',      (0.00, 0.085, 1.00, 0.78), 3/2, 540),
    # x 1,5-98,5 %: skærmbilledrammen (lyserød/grøn) er skåret væk.
    ('mk-koekken',  'sms-mudder-koekken-boern.jpg', (0.015, 0.14, 0.985, 0.571), 3/2, 540),
    ('mk-vandkanal','sr-mk-vandkanal.jpg',   (0.00, 0.00, 1.00, 1.00), 4/3, 350),
    # Et barn stod halvt uden for venstre kant. Beskaeringen begynder inde
    # bag det, saa der ikke staar en halv skikkelse i kanten.
    # Rettet beskaering: barnet nederst til hoejre var skaaret midt over.
    ('mk-skovsti',  'IMG_4825.JPG',          (0.00, 0.14, 1.00, 0.72), 4/3, 350),

    # ---- VÆRDIER ----
    ('vd-ro',     'sr-vd-ro.jpg',          (0.00, 0.00, 1.00, 1.00), 4/5, 540),
    ('vd-tillid', 'sr-vd-tillid.jpg',      (0.00, 0.00, 1.00, 1.00), 4/5, 540),
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
    # Baandet laa saa hoejt, at det skar tvaers gennem barnet, der hopper
    # oeverst i billedet – en moerk, halv skikkelse i overkanten. Sat ned,
    # saa det begynder under hende og rammer barnet paa gulvet helt.
    # Rettet beskaering: udsnittet laa midt imellem to boern og skar begge
    # over – benet paa barnet i gyngen foroven og foedderne paa barnet
    # forneden. Nu staar barnet paa traedehynderne helt i billedet.
    ('sted-hus',    'FullSizeRender-3.jpeg', (0.00, 0.42, 1.00, 0.858), 3/2, 540),
    # Rettet beskaering: barnet paa klatrevaeggen var skaaret over – hovedet
    # laa uden for billedet. Nu er hele barnet med, fra haender til bare foedder.
    ('sted-hus2',   'FullSizeRender-4.jpeg', (0.00, 0.15, 1.00, 0.55), 3/2, 540),
    # Rettet beskaering: hovedet paa barnet ved reolen var skaaret af.
    ('sted-hus3',   'FullSizeRender.jpeg',   (0.00, 0.20, 1.00, 0.64), 3/2, 540),
    # Haanden, der klapper grisen, blev skaaret over ved haandleddet og
    # laa som en loesrevet haand i overkanten. Beskaeringen begynder nu
    # under den; tilbage staar grisen i graesset, som alt-teksten siger.
    ('sted-stald',  'IMG_4250.JPG',          (0.00, 0.42, 1.00, 0.96), 3/2, 540),

    # Stalden, karrusel 2-8. Jeanettes egne billeder inde fra stalden, sendt
    # paa sms. De loeser det hul, der stod i README: der fandtes ikke ét
    # skarpt billede indefra. Alle er ca. 1170 px brede og kvadratiske, saa
    # 3/2-beskaeringen tager fra bunden og lader motivet staa i toppen.
    # Barnet og kaninen staar i den oeverste to tredjedele; nederste tredjedel
    # er tom halm og en rusten rive. Derfor skaeres den fra her.
    # Rettet beskaering: barn og kanin laa smaat i et billede fuldt af tom halm.
    ('stald-kanin',      'sr-stald-kanin.jpg',       (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    # Kyllingerne og varmelampen sidder nederst i billedet, koen oeverst.
    ('stald-kyllinger',  'sms-stald-kyllinger.jpg',  (0.00, 0.33, 1.00, 1.00), 3/2, 540),
    ('stald-halmballer', 'sms-stald-halmballer.jpg', (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    ('stald-legerum',    'sms-stald-legerum.png',    (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    ('stald-aellinger',  'sms-stald-aellinger.jpg',  (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    # Aeggene ligger nede i venstre hjoerne bag en ude-af-fokus arm. Beskaaret
    # ind paa reden, saa det er aeggene og ikke aermet, man ser.
    # Originalen er et uskarpt videobillede. Det, der fyldte mest, var et
    # aerme ude af fokus i hoejre side. Beskaaret ind paa reden, saa det er
    # aeggene, man ser. Det koster bredde – men flere pixels sloer hjaelper
    # ikke, og motivet er nu til at forstaa.
    # Rettet beskaering: aeggene laa nede i hjoernet, aermet fyldte resten.
    # Anden rettelse: aermet og den sorte jakke fyldte stadig naesten
    # halvdelen af billedet. Skaaret strammere ind, saa aeggene og haanden,
    # der raekker ud efter dem, fylder det meste – jakken er nu kun en
    # smal kant i hoejre side.
    # Tredje rettelse: "billede 3 og 4 virker zoomede". Det gjorde de, fordi
    # begge var skåret ind til 3/2 af et kvadratisk/stående foto. Nu vises hele
    # fotoet i fuld højde, og siderne fyldes med en sløret udgave af det selv
    # (tilstanden 'ramme'). Ingen skæring, ingen opskalering.
    ('stald-aeg',        'sms-stald-aeg.jpg',        (0.00, 0.00, 1.00, 1.00), 3/2, 540, 'ramme'),
    # Rettet beskaering: hoenen var skaaret af forneden.
    ('stald-hoene',      'sms-stald-hoene.jpg',      (0.00, 0.00, 1.00, 1.00), 3/2, 540, 'ramme'),

    ('sted-skov',   'sr-sted-skov.jpg',      (0.00, 0.00, 1.00, 1.00), 3/2, 540),

    # Baghaveskoven, karrusel 2-4.
    # En enkelt gummistoevle stak ind i venstre kant. Skaaret fra.
    ('skov-traedestubbe', 'sr-skov-traedestubbe.jpg',  (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    ('skov-daekgynge',    'sms-skov-daekgynge.jpg',    (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    # skov-trae er slettet efter Jeanettes rettelse. I stedet står de to børn
    # med skovler (samme foto som Værdier 3, som hun selv har bedt om).
    ('skov-boern-graver', 'FullSizeRender-1.jpeg',     (0.00, 0.44, 1.00, 0.985), 3/2, 540),
    ('skov-tovgynge',     'FullSizeRender-9.jpeg',     (0.00, 0.20, 1.00, 1.00), 3/2, 540),
    ('sted-have',   'IMG_4553.JPG',          (0.00, 0.22, 1.00, 0.96), 3/2, 540),
    # Jeanettes rettelse: mudderkoekkenet skal vaere sms-billedet. IMG_4819 er
    # kun 564x705 – derfor vis=282 og ikke 530, saa HTML'en ikke lover en
    # bredde, filen ikke har. Pladsen er den samme; billedet fylder den ud.
    # Haven har faaet karrusel ligesom Dagplejehuset, Stalden og
    # Baghaveskoven. Derfor 3/2 og vis=540 som de andre karruseldias, hvor
    # de foer laa i 4/3 til et galleri med to i bredden.
    ('sted-have2',  'sr-sted-have2.jpg',     (0.00, 0.00, 1.00, 1.00), 3/2, 540),
    ('sted-have3',  'IMG_4554.JPG',          (0.00, 0.04, 1.00, 0.96), 3/2, 540),

    # ---- PRAKTISK / OM MIG ----
    # 3/2 og ikke 4/5: teksten ved siden af er kun fire linjer, og et
    # stående billede gjorde blokken 641 px høj med 150 px tekst i.
    # Resten blev tom creme. Liggende format giver en blok på ca. 340 px,
    # hvor billede og tekst vejer nogenlunde det samme.
    # Barnet i hoejre kant blev skaaret midt over. Der er skaaret 14 % af
    # hoejre side, saa det er ude af billedet i stedet for halvt med.
    # Alt-teksten lover "barn i regntoej og gummistoevler" – og det barn
    # staar i hoejre side. Baandet er lagt om hende i stedet for om baalet,
    # saa billedet viser det, teksten siger.
    # Rettet beskaering: barnet til hoejre var skaaret af forneden.
    ('praktisk-regntoej', 'FullSizeRender-6.jpeg', (0.00, 0.42, 1.00, 1.00), 3/2, 540),
    # om-mig er taget ud. Siden "Om mig" bruger portraettet af Jeanette
    # (jeanette), og IMG_4826 blev ikke hentet af nogen af de syv sider –
    # jobbet lavede seks filer, ingen browser bad om. Originalen ligger
    # stadig i kilder/fotos, hvis den skal bruges igen.

    # Jeanettes egne to billeder, sendt på sms. De er de eneste med hendes
    # ansigt på, og det er dem, siden "Om mig" skal bære. Originalerne er
    # under 700 px brede – derfor de små vis-bredder her: bliver pladsen
    # bredere end originalen, står der et opskaleret, sløret billede.
    ('jeanette',       'jeanette-portraet.jpeg', (0.00, 0.00, 1.00, 1.00), 4/5, 300),
    ('jeanette-boern', 'jeanette-boern.jpeg',    (0.00, 0.00, 1.00, 1.00), 3/2, 342),
]


def ramme(im, ar):
    """Hele fotoet i fuld højde midt i et ar-format billede; siderne fyldes
    med en sløret, mørkere udgave af fotoet selv. Bruges, hvor en beskæring
    til 3/2 ville skære for meget af et stående eller kvadratisk foto væk."""
    W = im.width
    H = int(round(W / ar))
    s = max(W / im.width, H / im.height)
    bg = im.resize((int(round(im.width * s)), int(round(im.height * s))), Image.LANCZOS)
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(W * 0.025))
    bg = Image.eval(bg, lambda v: int(v * 0.88))
    f = min(W / im.width, H / im.height)
    fg = im.resize((int(round(im.width * f)), int(round(im.height * f))), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return bg


def beskaer(im, box, ar, tilstand=None):
    if tilstand == 'ramme':
        return ramme(im, ar)
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


def gem(im, sti, bredde, retina, skarp=True):
    """Skalerer til `bredde` og gemmer som AVIF, WebP og JPEG.

    Om efterskarpheden: Lanczos giver den reneste nedskalering, men enhver
    nedskalering blødgør kanterne en anelse – detaljer, der før lå i to
    pixels, skal nu deles om én. Et let unsharp mask bagefter henter præcis
    den kant tilbage. Det er ikke en effekt, og det tilføjer ikke noget, der
    ikke var der: radius 0,6 px rører kun selve kanten, og tærsklen på 3
    holder fingrene fra flader som himmel og sand, hvor den ellers ville
    trække kornet frem.

    Det betyder mest for de billeder, hvor Jeanettes original ikke rækker
    til dobbelt opløsning. Dem kan vi ikke give flere pixels – men vi kan
    sørge for, at de pixels, der er, står skarpt.
    """
    if im.width != bredde:
        h = int(round(bredde * im.height / im.width))
        im = im.resize((bredde, h), Image.LANCZOS)
    if skarp:
        im = im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=55, threshold=3))
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
def _maal(src, box, ar, vis, tilstand=None):
    with Image.open(SRC + src) as _im:
        w, h = _im.size
    if tilstand == 'ramme':
        box = (0, 0, 1, 1)
        h = int(round(w / ar))
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
    return par(vis * 2) + par(int(vis * 1.5)) + par(vis)


MAAL = {}
for _ud, _src, _box, _ar, _vis, *_t in JOBS:
    MAAL[_ud] = _maal(_src, _box, _ar, _vis, *_t)


if __name__ == '__main__':
    originaler = [j[1] for j in JOBS]
    # Jeanette har selv bedt om, at to fotos står to steder: børnene i
    # mudderkøkkenet (forsidekort + karrusel) og de to børn med skovler
    # (Værdier 3 + Baghaveskoven). Alt andet må stadig kun bruges én gang.
    TILLADT_DUBLET = {'sms-mudder-koekken-boern.jpg', 'FullSizeRender-1.jpeg'}
    dubletter = {x for x in originaler if originaler.count(x) > 1} - TILLADT_DUBLET
    assert not dubletter, f'Samme original bruges flere gange: {dubletter}'

    i_alt = {'jpg': 0, 'webp': 0, 'avif': 0}
    import sys
    kun = set(sys.argv[1:])
    for ud, src, box, ar, vis, *t in JOBS:
        if kun and ud not in kun:
            continue
        raa = beskaer(Image.open(SRC + src).convert('RGB'), box, ar, *t)
        if raa.width < vis * 2:
            print(f'  ! {ud}: originalen er kun {raa.width} px bred '
                  f'(ville gerne have {vis*2})')
        stor, q2 = gem(raa, OUT + ud, min(vis * 2, raa.width), retina=True)
        # Mellemtrinnet. Uden det maatte en helt almindelig telefon med
        # 2x-skaerm hente den stoerste fil: den bad om 780 px, og valget stod
        # mellem 540 og 1080. Nu er der 810, og den henter ca. en tredjedel
        # faerre bytes uden at et eneste billede bliver mindre skarpt.
        mellem, _ = gem(raa, OUT + ud + '-15x', min(int(vis * 1.5), raa.width), retina=True)
        lille, _ = gem(raa, OUT + ud + '-1x', min(vis, raa.width), retina=False)

        k = {}
        for e in i_alt:
            k[e] = (os.path.getsize(f'{OUT}{ud}.{e}')
                    + os.path.getsize(f'{OUT}{ud}-15x.{e}')
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
