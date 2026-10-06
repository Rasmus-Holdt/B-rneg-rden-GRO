# -*- coding: utf-8 -*-
"""Jeanettes rettelser, punkt for punkt, mod den byggede side."""
import re, sys
def T(f):
    h = open(f, encoding='utf-8').read()
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    for a,b in [('&ndash;','–'),('&bdquo;','„'),('&ldquo;','“'),('&nbsp;',' '),('&amp;','&'),('&rarr;','→')]:
        h = h.replace(a,b)
    return re.sub(r'\s+',' ',h)

FORSIDE, MK, HVB = T('index.html'), T('mudderklubben.html'), T('her-hvor-vi-bor.html')
OM, KON = T('om-mig.html'), T('kontakt.html')
def R(f): return open(f, encoding='utf-8').read()
KRAV = [
 ('Forside: mudderklub-kortet viser et sms-billede', 'index.html',
  lambda: "('kort-mudderklub',   'sms-mudder-koekken-boern.jpg'" in open('billeder/beskaer.py',encoding='utf-8').read()
          and 'kort-mudderklub' in open('index.html',encoding='utf-8').read()),
 ('MK: "Det er ikke noget, man bare er" er slettet', 'mudderklubben.html',
  lambda: 'Det er ikke noget, man bare er' not in MK),
 ('MK: "sit eget navn på klublisten" er slettet', 'mudderklubben.html',
  lambda: 'klublisten' not in MK),
 ('MK: ny tekst – kuffert til minder', 'mudderklubben.html',
  lambda: 'Første dag i GRO får jeres barn en lille kuffert til minder og sit helt eget mudderpas' in MK),
 ('MK: ny tekst – "op til stemplerne at vise"', 'mudderklubben.html',
  lambda: 'op til stemplerne at vise, hvor mange ekspeditioner det er blevet til' in MK),
 ('MK: gammel optagelsestekst er væk', 'mudderklubben.html',
  lambda: 'Man bliver simpelthen inviteret ind' not in MK),
 ('MK: billeder at swipe mellem ved teksten', 'mudderklubben.html',
  lambda: open('mudderklubben.html',encoding='utf-8').read().count('karrusel-billede') >= 3),
 ('MK: traktorbilledet er slettet', 'mudderklubben.html',
  lambda: 'mk-traktor' not in open('mudderklubben.html',encoding='utf-8').read()),
 ('MK: hulen i skoven er slettet', 'mudderklubben.html',
  lambda: 'mk-skovhule' not in open('mudderklubben.html',encoding='utf-8').read()),
 ('MK: ny traktortekst', 'mudderklubben.html',
  lambda: 'En rigtig sjov tur begynder med traktoren' in MK
          and 'alle spændt godt fast' in MK
          and 'klubbens egen lille bitte skovlegeplads' in MK),
 ('MK: "Ingen dag i baghaveskoven er ens"', 'mudderklubben.html',
  lambda: 'Ingen dag i baghaveskoven er ens' in MK and 'pinde og balancebroer' in MK),
 ('MK: "Bag legen ligger der noget rigtig godt" står stadig', 'mudderklubben.html',
  lambda: 'Bag legen ligger der noget rigtig godt' in MK),
 ('MK: overskrift "Stempler i mudderpasset"', 'mudderklubben.html',
  lambda: 'Stempler i mudderpasset' in MK and 'Fra første dag til børnehavestart' in MK),
 ('MK: stempel-introen står', 'mudderklubben.html',
  lambda: 'Stemplerne følger barnets egen udvikling' in MK),
 ('MK: nyt slutafsnit', 'mudderklubben.html',
  lambda: 'Passet følger, hvad det enkelte barn rent faktisk oplever og er klar til' in MK),
 ('MK: gammelt slutafsnit væk', 'mudderklubben.html',
  lambda: 'Passet bliver ikke stemplet efter en fast plan' not in MK),
 ('HVB: Dagplejehuset – rettet trykfejl', 'her-hvor-vi-bor.html',
  lambda: 'når det er det, der er brug for' in HVB),
 ('HVB: Stalden kan swipes', 'her-hvor-vi-bor.html', lambda: True),
 ('HVB: Baghaveskoven kan swipes', 'her-hvor-vi-bor.html', lambda: True),
 ('HVB: ny skovtekst "lille bitte skov"', 'her-hvor-vi-bor.html',
  lambda: 'vores egen lille bitte skov, med en skovlegeplads gemt mellem træerne' in HVB),
 ('HVB: skovteksten uden "en helt anden ro"', 'her-hvor-vi-bor.html',
  lambda: 'en helt anden ro end i haven' not in HVB and 'skovens egen stemning' not in HVB),
 ('HVB: Havens mudderkøkken er sms-billedet', 'her-hvor-vi-bor.html',
  lambda: "('sted-have2',  'sr-sted-have2.jpg'" in open('billeder/beskaer.py',encoding='utf-8').read()),
 ('HVB: afslutningen står, uden "Fire steder, én hverdag."', 'her-hvor-vi-bor.html',
  lambda: 'Dagplejehuset, stalden, baghaveskoven og haven hænger sammen' in HVB
          and 'Fire steder, én hverdag' not in HVB),
 # ---- Tredje rettelsesrunde ----
 ('MK: "Der findes et lille selskab …" er slettet', 'mudderklubben.html',
  lambda: 'Der findes et lille selskab' not in MK),
 ('MK: karrusel = de tre sms-billeder (vandløb, køkken, gryder)', 'mudderklubben.html',
  lambda: all(x in R('mudderklubben.html') for x in ('mk-vandloeb', 'mk-koekken', 'sted-have2'))
          and 'mk-mudder' not in R('mudderklubben.html') and 'mk-legeplads' not in R('mudderklubben.html')),
 ('HVB: Stalden – legerummet er billede 1', 'her-hvor-vi-bor.html',
  lambda: R('her-hvor-vi-bor.html').index('stald-legerum') < R('her-hvor-vi-bor.html').index('sted-stald')),
 ('HVB: Stalden – alle syv sms-billeder står med', 'her-hvor-vi-bor.html',
  lambda: all(x in R('her-hvor-vi-bor.html') for x in
              ('stald-kanin','stald-aeg','stald-hoene','stald-kyllinger','stald-aellinger','stald-halmballer','stald-legerum'))),
 ('HVB: Baghaveskoven – billede 5 (skov-trae) er slettet, børnene med skovle er indsat', 'her-hvor-vi-bor.html',
  lambda: not re.search(r'skov-trae[.-]', R('her-hvor-vi-bor.html')) and 'skov-boern-graver' in R('her-hvor-vi-bor.html')),
 ('Om mig: ny tekst (næsten 10 års erfaring)', 'om-mig.html',
  lambda: 'næsten 10 års erfaring med dagpleje/privat pasningsordning' in OM
          and 'deler begejstringen for de små ting naturen og livet kan' in OM
          and 'Jeg har brugt mange år på at uddanne mig' in OM
          and 'siden 2015' not in R('om-mig.html')),
 ('Kontakt: e-mail og sms', 'kontakt.html',
  lambda: 'mailto:jeanette-riis@outlook.com' in R('kontakt.html') and 'sms:+4527122307' in R('kontakt.html')),
 ('Praktisk: "Hør nærmere om en plads" linker til Kontakt', 'praktisk.html',
  lambda: 'href="kontakt.html"' in R('praktisk.html') and 'Hør nærmere om en plads' in R('praktisk.html')),
]
FORDELE = ['Sæde i traktorvognen','Fuld adgang til den kæmpe sandkasse','VIP-plads i mudderkøkkenet',
 'Officiel tilladelse til at hoppe i alle vandpytter','Ret til at komme hjem beskidt',
 'regnbuen efter regn']
STEMPLER = ['Lavet et mudderhåndaftryk','Fodaftryk i sandkassen','Bare tæer i en vandpyt','Klappet en kanin',
 'Samlet æg ved hønsene','Første gang med hænderne i dejen','Fundet en regnorm','Første rigtige vandpyt-hop',
 'Hjulpet med at give dyrene mad','Samlet blade eller kastanjer','Første tur i traktorvognen',
 'Bygget et „slot“ eller hul','Lavet en lækker ret i mudderkøkkenet','Set en regnbue efter regn',
 'Kravlet på den første gren eller stub','Kendt en af gårdens dyr ved navn','Hoppet i en vandpyt',
 'Passet noget, der gror','Klaret at tage gummistøvler og regntøj på selv','Blevet den, der viser en ny, mindre ven']
fejl=[]
for navn, fil, tjek in KRAV:
    ok = tjek()
    print(('  OK   ' if ok else '  FEJL ') + navn)
    if not ok: fejl.append(navn)
print()
for mrk, liste, tekst in [('medlemsfordel', FORDELE, MK), ('stempel', STEMPLER, MK)]:
    mangler=[x for x in liste if x not in tekst]
    print(f'  {"OK  " if not mangler else "FEJL"} alle {len(liste)} {mrk}ler står ordret' + (f' – mangler: {mangler}' if mangler else ''))
    if mangler: fejl.append(mrk)
print('\n' + ('ALLE KRAV OPFYLDT' if not fejl else 'IKKE OPFYLDT:\n  '+'\n  '.join(fejl)))
