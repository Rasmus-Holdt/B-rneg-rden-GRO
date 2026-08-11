# -*- coding: utf-8 -*-
"""Solens form – ét sted, brugt af både byg.py og ikoner.py.

Solen tegnes i headeren, i sidehovederne, i footeren, i mudderpasset OG som
favicon. Lå tegningen to steder, ville de før eller siden komme til at se
forskellige ud efter en rettelse. Derfor står stregerne kun her.

Koordinatsystemet er 120×120. Alt andet skalerer ud fra det.
"""

GUL = '#f7c948'
KANT = '#e0a825'
BLAEK = '#33302a'
CREME = '#fbf3e6'

# Stråler, skive og ansigt. Stregerne er let buede, så den ser tegnet ud
# frem for konstrueret.
KROP = f'''  <g fill="none" stroke="{KANT}" stroke-width="7" stroke-linecap="round">
    <path d="M60 5 C61 12 60.5 16 60 20"/>
    <path d="M60 100 C60.5 105 60 110 60 116"/>
    <path d="M5 60 C12 59.5 16 60 20 60"/>
    <path d="M100 60 C106 60 111 59.5 116 60"/>
    <path d="M21 21 C25 26 28 28 31 31"/>
    <path d="M89 89 C92 92 95 95 99 99"/>
    <path d="M99 21 C95 25 92 28 89 31"/>
    <path d="M31 89 C28 92 25 95 21 99"/>
  </g>
  <path d="M60 22 C81 22 98 39 98 60 C98 81 81 98 60 98 C39 98 22 81 22 60 C22 39 39 22 60 22 Z"
        fill="{GUL}" stroke="{KANT}" stroke-width="5" stroke-linejoin="round"/>
  <ellipse cx="48" cy="54" rx="4" ry="5" fill="{BLAEK}"/>
  <ellipse cx="72" cy="54" rx="4" ry="5" fill="{BLAEK}"/>
  <path d="M47 70 Q60 80 73 70" fill="none" stroke="{BLAEK}"
        stroke-width="4" stroke-linecap="round"/>'''


def svg(cls=None, size=None, baggrund=False, luft=0.0):
    """Solen som færdig SVG.

    cls, size   sættes kun når den skal ind på siden
    baggrund    cremefarvet plade bagved (til iOS og Android-app-ikoner,
                som ikke selv lægger baggrund på)
    luft        andel tom kant hele vejen rundt (Android beskærer app-ikoner
                til cirkler, så solen skal trækkes ind)
    """
    attr = ''
    if cls is not None:
        attr += f' class="{cls}"'
    if size is not None:
        attr += f' width="{size}" height="{size}"'

    bg = f'<rect width="120" height="120" rx="22" fill="{CREME}"/>' if baggrund else ''

    krop = KROP
    if luft:
        s = 1 - 2 * luft
        krop = (f'<g transform="translate(60 60) scale({s}) translate(-60 -60)">'
                f'{KROP}</g>')

    return (f'<svg{attr} viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="Tegnet sol">{bg}\n{krop}\n</svg>')
