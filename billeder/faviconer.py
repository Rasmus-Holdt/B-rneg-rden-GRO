# -*- coding: utf-8 -*-
"""Bygger faneblads- og app-ikoner ud af Jeanettes sol.

Kør fra denne mappe:  python3 faviconer.py

Kilden er kilder/sol-canva.png – præcis den fil, Jeanette selv har lavet,
med gennemsigtig baggrund. Her sker der ikke andet end at Canva-rammen
skæres væk, at solen sættes på en kvadratisk flade, og at den skaleres til
de størrelser, browsere og telefoner beder om.

## To slags ikoner

**Fanebladet** får solen som den er: gennemsigtig baggrund, ingen plade
bagved. Det er den fil, Jeanette har sendt, i mindre udgaver.

**Hjemmeskærmen** (iPhone og Android) kan ikke gennemsigtighed. iOS lægger
et gennemsigtigt ikon på sort, Android på hvad brugerens tema nu er. Derfor
– og kun derfor – står solen dér på den samme cremefarve, som sidens kort
har. Det er ikke pynt, det er det platformene kræver.

## Hvorfor hver størrelse tegnes for sig

Solens stråler er tynde streger. Skalerer man ét stort ikon ned til 16 px,
forsvinder de i grød. Hver størrelse skaleres derfor direkte fra
originalen, og ved 16 og 32 px fylder solen næsten hele fladen, så selve
skiven bliver så stor som muligt.

## Filerne

    favicon-16/32/48/96.png   fanebladet – gennemsigtig
    favicon.ico               samme, i én fil til gamle browsere og bots,
                              der spørger efter /favicon.ico af vane
    apple-touch-icon.png      180 px, iPhone-hjemmeskærm – cremefarvet
    ikon-192/512.png          Android og "føj til hjemmeskærm" – cremefarvet
    ikon-maskable-512.png     Android beskærer selv til cirkel, se nedenfor
    logo-512.png              virksomhedslogoet i sidens strukturerede data.
                              Det er dét, Google kan vise ved siden af navnet.
"""
from PIL import Image
import os

_HER = os.path.dirname(os.path.abspath(__file__))
KILDER = os.path.join(_HER, '..', 'kilder', '')
ROD = os.path.join(_HER, '..', '')

CREME = (251, 243, 230, 255)     # --creme, samme som kortene på siden


def sol():
    """Jeanettes fil med Canva-rammen skåret væk."""
    im = Image.open(KILDER + 'sol-canva.png').convert('RGBA')
    return im.crop(im.getchannel('A').getbbox())


def luft(S):
    """Hvor stor en del af fladen solen fylder ved størrelsen S.

    Ved 16 og 32 px er der ikke pixels at spilde på luft, hvis strålerne
    skal kunne ses. Fra 48 px og op ser ikonet roligere ud med en kant."""
    return .98 if S <= 32 else .94 if S <= 96 else .86


def ikon(S, baggrund=None, del_af_hoejden=None):
    """Solen centreret på en kvadratisk flade på S x S pixels.

    `baggrund=None` giver gennemsigtig baggrund – det er fanebladets udgave.
    En farve fylder fladen ud, til de steder hvor gennemsigtighed ikke virker.
    Solen er lidt bredere end høj, så der skaleres efter højden; ellers ville
    den stikke ud til siderne i de størrelser, hvor der er mindst luft.
    """
    flade = Image.new('RGBA', (S, S), baggrund or (0, 0, 0, 0))
    m = sol()
    h = round(S * (del_af_hoejden or luft(S)))
    b = round(m.width * h / m.height)
    flade.alpha_composite(m.resize((b, h), Image.LANCZOS),
                          ((S - b) // 2, (S - h) // 2))
    return flade


def gem(im, sti):
    """Gemmer som PNG med fuld alfakanal.

    Her stod før en `quantize()`, der pressede filen ned i en tabel på 256
    farver. Det halverede vægten, men en farvetabel kan kun holde ét
    gennemsigtighedsniveau pr. farve, og solens kanter er bløde. Resultatet
    var trappetrin langs strålerne. En sol på 16 px fylder 1 KB som ægte
    RGBA – der er ingenting at spare.
    """
    im.save(sti, 'PNG', optimize=True)


def skriv_ico(sti, billeder):
    """Skriver en .ico med hver størrelse tegnet for sig.

    Pillow kan godt gemme .ico i flere størrelser, men skalerer dem alle ned
    fra ét billede, og så arver 16 px-udgaven den luft, der passer ved 48.
    Formatet er enkelt nok at skrive selv: et hoved, en indholdsfortegnelse
    og filerne bagefter – her lagt ind som PNG, hvilket alle browsere har
    forstået i femten år.
    """
    import struct, io
    dele = []
    for im in billeder:
        b = io.BytesIO()
        im.save(b, 'PNG', optimize=True)
        dele.append((im.width, b.getvalue()))

    hoved = struct.pack('<HHH', 0, 1, len(dele))     # 0, type 1 = ikon, antal
    forskyd = len(hoved) + 16 * len(dele)
    fortegnelse, krop = b'', b''
    for bredde, data in dele:
        fortegnelse += struct.pack(
            '<BBBBHHII',
            bredde if bredde < 256 else 0,           # 0 betyder 256
            bredde if bredde < 256 else 0,
            0, 0, 1, 32, len(data), forskyd)
        krop += data
        forskyd += len(data)
    with open(sti, 'wb') as f:
        f.write(hoved + fortegnelse + krop)


if __name__ == '__main__':
    # ---- fanebladet: Jeanettes sol, gennemsigtig ------------------------
    for s in (16, 32, 48, 96):
        gem(ikon(s), ROD + f'favicon-{s}.png')
    skriv_ico(ROD + 'favicon.ico', [ikon(s) for s in (16, 32, 48)])

    # favicon.svg er ikke linket fra siderne – tegningen er pixels, ikke
    # kurver, og en SVG med et billede pakket ind i sig er kun en dyrere PNG.
    # Filen skrives alligevel, så der aldrig ligger en forældet udgave
    # tilbage, hvis nogen henter adressen direkte.
    import base64
    _d = base64.b64encode(open(ROD + 'favicon-96.png', 'rb').read()).decode()
    open(ROD + 'favicon.svg', 'w', encoding='utf-8').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">'
        '<image width="96" height="96" href="data:image/png;base64,'
        + _d + '"/></svg>\n')

    # ---- hjemmeskærm: samme sol, men på creme ---------------------------
    # iOS og Android kan ikke gennemsigtige ikoner. Uden en flade bagved
    # lander solen på sort.
    gem(ikon(180, CREME), ROD + 'apple-touch-icon.png')
    gem(ikon(192, CREME), ROD + 'ikon-192.png')
    gem(ikon(512, CREME), ROD + 'ikon-512.png')

    # Maskable: Android klipper selv ikonet til den form, telefonen bruger –
    # cirkel, firkant med runde hjørner, dråbe. Kun de midterste 80 % er
    # sikre, så solen holder sig godt inden for midten.
    gem(ikon(512, CREME, del_af_hoejden=.62), ROD + 'ikon-maskable-512.png')

    # ---- Googles virksomhedslogo ----------------------------------------
    # Skal være kvadratisk og mindst 112 px, og vises på hvid baggrund i
    # søgeresultatet – derfor cremefladen her også.
    gem(ikon(512, CREME), ROD + 'logo-512.png')

    for f in ('favicon-16.png', 'favicon-32.png', 'favicon-48.png',
              'favicon-96.png', 'favicon.ico', 'apple-touch-icon.png',
              'ikon-192.png', 'ikon-512.png', 'ikon-maskable-512.png',
              'logo-512.png'):
        im = Image.open(ROD + f)
        print(f'{f:24} {im.format:4} {str(im.mode):5} '
              f'{os.path.getsize(ROD + f) / 1024:6.1f} KB')
