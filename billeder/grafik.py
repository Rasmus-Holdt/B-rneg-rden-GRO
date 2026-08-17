# -*- coding: utf-8 -*-
"""Klargør Jeanettes to Canva-tegninger: navnetrækket og solen.

Kør fra denne mappe:  python3 grafik.py

Det er ikke fotos, men fladefarvet stregtegning med gennemsigtig baggrund.
Derfor er de behandlet for sig og ikke i beskaer.py:

  * De skal beholde alfakanalen. JPEG kan ikke det, så sporet er
    WebP med PNG som fallback – ikke AVIF/WebP/JPEG som fotosene.
  * Fladefarver komprimerer helt anderledes end fotos. Kvalitetstallene
    i beskaer.py ville give synlige kanter omkring de sorte streger.

Canva eksporterer med en stor gennemsigtig ramme udenom. Den bliver skåret
væk her, så CSS kan styre størrelsen præcist i stedet for at gætte, hvor
meget luft der ligger rundt om motivet.

Navnetrækket kommer kun ud af Canva i 466 px bredde. Det er for lidt til en
overskrift på en retinaskærm, så det skaleres 2x med Lanczos. Det tåler
motivet, fordi det er få flade farver med tykke sorte konturer – der er
ingen fine detaljer at miste. På et foto ville det have set udvasket ud.
"""
from PIL import Image
import os

# Absolutte stier ud fra filens egen placering. byg.py importerer MAAL
# herfra og kører fra roden, ikke fra billeder/ – med relative stier ledte
# den efter kilderne ét niveau for højt oppe.
_HER = os.path.dirname(os.path.abspath(__file__))
KILDER = os.path.join(_HER, '..', 'kilder', '')
UD = os.path.join(_HER, '')

# Solen bliver aldrig vist bredere end 92 px i CSS. På en retinaskærm er det
# 184 px, så alt over 200 px er bytes, ingen kommer til at se. Ubeskåret fra
# Canva fyldte den 26 KB på hver eneste sideindlæsning – nu under en tredjedel.
#
# Navnetrækket bruges to steder i vidt forskellig størrelse: som overskrift
# på forsiden (op til 466 px bredt) og i headeren på hver side (op til 218).
# Én fil til begge dele betød, at headeren hentede 34 KB for at vise noget,
# der fylder en fjerdedel. Headerens udgave er derfor Canvas egen opløsning
# uden opskalering – 466 px er præcis 2x af de 218, den vises i, så den er
# skarp på en retinaskærm og en tredjedel af vægten.
#
# (udfil, kildefil, opskalering, største bredde, alt-tekst)
JOBS = [
    ('logo-gro',       'logo-gro-canva.png', 2, 932, 'Navnetrækket, forsidens overskrift'),
    ('logo-gro-lille', 'logo-gro-canva.png', 1, 466, 'Navnetrækket, headeren'),
    ('sol',            'sol-canva.png',      1, 200, 'Jeanettes tegnede sol'),
]

# Bruges af byg.py, så width/height i HTML altid matcher de faktiske filer.
MAAL = {}


def klargoer(src, skala, maks):
    im = Image.open(KILDER + src).convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())      # Canva-rammen væk
    if skala != 1:
        im = im.resize((im.width * skala, im.height * skala), Image.LANCZOS)
    if im.width > maks:
        im = im.resize((maks, round(im.height * maks / im.width)), Image.LANCZOS)
    return im


for _ud, _src, _skala, _maks, _ in JOBS:
    _im = Image.open(KILDER + _src)
    _bb = _im.getchannel('A').getbbox()
    _b, _h = (_bb[2] - _bb[0]) * _skala, (_bb[3] - _bb[1]) * _skala
    if _b > _maks:
        _b, _h = _maks, round(_h * _maks / _b)
    MAAL[_ud] = (_b, _h)


if __name__ == '__main__':
    for ud, src, skala, maks, tekst in JOBS:
        im = klargoer(src, skala, maks)
        im.save(UD + ud + '.png', optimize=True)
        # method=6 er den langsomste og bedste indstilling. Filerne laves
        # én gang, så det er ligegyldigt at det tager et sekund ekstra.
        im.save(UD + ud + '.webp', quality=88, method=6)
        kb_p = os.path.getsize(UD + ud + '.png') / 1024
        kb_w = os.path.getsize(UD + ud + '.webp') / 1024
        print(f'{ud:10} {im.width:>4}x{im.height:<4}  '
              f'png {kb_p:5.1f} K   webp {kb_w:5.1f} K   {tekst}')
