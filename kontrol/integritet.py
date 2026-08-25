# -*- coding: utf-8 -*-
"""Alle billedreferencer paa alle syv sider mod filerne paa disken."""
import os, re, sys
from PIL import Image
sider=['index.html','mudderklubben.html','vaerdier.html','her-hvor-vi-bor.html',
       'praktisk.html','om-mig.html','kontakt.html']
fejl=[];par=0;srcs=0
for s in sider:
    h=open(s,encoding='utf-8').read()
    if h.count('<h1')!=1: fejl.append(f'{s}: {h.count("<h1")} h1')
    for img in re.findall(r'<img [^>]*>',h):
        if 'alt="' not in img: fejl.append(f'{s}: img uden alt')
    for m in re.finditer(r'<img src="billeder/([a-z0-9-]+)\.jpg"[^>]*width="(\d+)" height="(\d+)"',h):
        rw,rh=Image.open(f'billeder/{m.group(1)}.jpg').size; par+=1
        if (rw,rh)!=(int(m.group(2)),int(m.group(3))):
            fejl.append(f'{s}: {m.group(1)} lover {m.group(2)}x{m.group(3)}, filen er {rw}x{rh}')
    for m in re.finditer(r'billeder/([a-z0-9-]+?)(-15x|-1x)?\.(avif|webp|jpg) (\d+)w',h):
        sti=f'billeder/{m.group(1)}{m.group(2) or ""}.{m.group(3)}'; srcs+=1
        if not os.path.exists(sti): fejl.append(f'{s}: mangler {sti}'); continue
        if Image.open(sti).size[0]!=int(m.group(4)):
            fejl.append(f'{s}: {sti} srcset siger {m.group(4)}w, filen er {Image.open(sti).size[0]}w')
print(f'{par} width/height-par og {srcs} srcset-bredder kontrolleret mod filerne')
print('ALT OK' if not fejl else 'FEJL:\n  '+'\n  '.join(fejl[:20]))
