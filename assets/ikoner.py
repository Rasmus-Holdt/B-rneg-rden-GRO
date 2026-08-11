# -*- coding: utf-8 -*-
"""Genererer hele ikonsættet ud fra solen.

Kør fra denne mappe:  python3 ikoner.py
Kræver:               pip install cairosvg pillow

Skal kun køres igen, hvis solen ændrer sig. Filerne er tjekket ind, så
byg.py kan køres uden cairosvg installeret.

**Tegningen hentes direkte fra `sol()` i byg.py.** Det er med vilje: favicon'en
skal være den samme sol som i headeren, ikke en efterligning. Ved at læse
funktionen ud af byg.py kan de to ikke komme til at afvige fra hinanden.

Hvorfor så mange filer:

  favicon.ico              Safari, ældre browsere, og dét Google leder efter
                           først. Indeholder 16, 32 og 48 px i én fil.
  favicon-48/96.png        Google viser kun favicons, hvis de er kvadratiske
                           og et multiplum af 48 px. Derfor lige præcis dem.
  favicon.svg              Skarp i alle størrelser i Chrome og Firefox.
  apple-touch-icon.png     180 px. iOS beskærer ikke, men lægger heller ikke
                           baggrund på, så den skal have cremen bagt ind.
  ikon-192/512.png         Til webmanifestet ("Føj til hjemmeskærm").
  ikon-maskable-512.png    Android beskærer app-ikoner til cirkler og
                           squircles. Denne har 20 % luft hele vejen rundt,
                           så solen aldrig bliver klippet.
  logo-512.png             Bruges som "logo" i de strukturerede data. Det er
                           det billede, Google kan vise ved siden af
                           virksomheden i søgeresultater.
"""
import io
import os
import re
import struct

import cairosvg
from PIL import Image

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)

CREME = '#fbf3e6'


def hent_solen_fra_byg():
    """Klipper `def sol(...)` ud af byg.py og kører den, så vi får præcis den
    samme tegning som headeren bruger – uden at kopiere den herover.

    byg.py kan ikke importeres direkte, fordi den bygger hele siden ved import."""
    kilde = open(os.path.join(ROD, 'byg.py'), encoding='utf-8').read()
    m = re.search(r'^def sol\(.*?\n(?=\n\S|\nIKON)', kilde, re.S | re.M)
    if not m:
        raise SystemExit('Kunne ikke finde sol() i byg.py – er den blevet omdøbt?')
    rum = {}
    exec(m.group(0), rum)
    return rum['sol']


sol = hent_solen_fra_byg()


def sol_svg(baggrund=False, luft=0.0):
    """Solen som selvstændig SVG-fil.

    `sol()` fra byg.py tegner i et 120x120-koordinatsystem. Vi genbruger det
    som det er – cairosvg kan rendere det i hvilken som helst pixelstørrelse.

    luft = andel tom kant hele vejen rundt (til maskable Android-ikoner)."""
    indre = sol('', 120)
    # fjern width/height/class, så vi selv styrer størrelsen
    indre = re.sub(r'\s(?:width|height|class)="[^"]*"', '', indre, count=3)
    indre = indre.replace('<svg ', '<svg ').replace(
        '<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1) \
        if 'xmlns' not in indre else indre

    krop = re.search(r'<svg[^>]*>(.*)</svg>', indre, re.S).group(1)
    bg = f'<rect width="120" height="120" rx="22" fill="{CREME}"/>' if baggrund else ''
    s = 1 - 2 * luft
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
            f'{bg}<g transform="translate(60 60) scale({s}) translate(-60 -60)">'
            f'{krop}</g></svg>')


def png(svg, px):
    data = cairosvg.svg2png(bytestring=svg.encode('utf-8'),
                            output_width=px, output_height=px)
    return Image.open(io.BytesIO(data)).convert('RGBA')


def skriv_ico(billeder, sti):
    """Pillows ICO-gemning skalerer ét billede til alle størrelser og kan ikke
    give hver størrelse sin egen data. Derfor bygges containeren her.

    En ICO-fil er: en header, en post pr. billede, og så billeddataene.
    Moderne Windows og browsere accepterer PNG-data i alle størrelser."""
    dele = []
    for b in billeder:
        buf = io.BytesIO()
        b.save(buf, 'PNG', optimize=True)
        dele.append((b.size[0], buf.getvalue()))

    header = struct.pack('<HHH', 0, 1, len(dele))    # reserveret, type=ikon, antal
    poster, data = b'', b''
    offset = len(header) + 16 * len(dele)
    for px, raa in dele:
        poster += struct.pack('<BBBBHHII',
                              px if px < 256 else 0,   # bredde (0 betyder 256)
                              px if px < 256 else 0,   # højde
                              0, 0,                     # palet, reserveret
                              1, 32,                    # farveplan, bits pr. pixel
                              len(raa), offset)
        data += raa
        offset += len(raa)
    with open(sti, 'wb') as f:
        f.write(header + poster + data)


def gem(billede, sti):
    billede.save(sti, 'PNG', optimize=True)
    print(f'  {os.path.relpath(sti, ROD):32} {billede.size[0]}×{billede.size[1]}'
          f'  {os.path.getsize(sti)/1024:.1f} KB')


if __name__ == '__main__':
    gennemsigtig = sol_svg()
    paa_creme = sol_svg(baggrund=True)
    maskable = sol_svg(baggrund=True, luft=0.20)

    print('Ikoner – samme tegning som solen i headeren, i alle størrelser:\n')

    with open(os.path.join(ROD, 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(gennemsigtig)
    print(f'  favicon.svg                      vektor'
          f'  {os.path.getsize(os.path.join(ROD, "favicon.svg"))/1024:.1f} KB')

    # Google viser kun favicons der er kvadratiske og et multiplum af 48
    for px in (48, 96):
        gem(png(gennemsigtig, px), os.path.join(ROD, f'favicon-{px}.png'))

    skriv_ico([png(gennemsigtig, px) for px in (16, 32, 48)],
              os.path.join(ROD, 'favicon.ico'))
    print(f'  favicon.ico                      16+32+48'
          f'  {os.path.getsize(os.path.join(ROD, "favicon.ico"))/1024:.1f} KB')

    # iOS lægger ikke selv baggrund på – cremen skal bages ind
    gem(png(paa_creme, 180), os.path.join(ROD, 'apple-touch-icon.png'))

    for px in (192, 512):
        gem(png(paa_creme, px), os.path.join(ROD, f'ikon-{px}.png'))
    gem(png(maskable, 512), os.path.join(ROD, 'ikon-maskable-512.png'))
    gem(png(paa_creme, 512), os.path.join(ROD, 'logo-512.png'))
