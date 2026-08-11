# Billeder

25 billeder, skåret ud af de 39 originaler i Jeanettes iCloud-zip.
Originalerne ligger i `kilder/fotos/`, og `beskaer.py` genskaber alle beskæringer
fra dem med én kommando:

```
cd billeder && python3 beskaer.py
```

For hvert motiv laves fire filer: `navn.webp` og `navn.jpg` i dobbelt opløsning,
og `navn-1x.webp` / `navn-1x.jpg` i normal. Browseren vælger selv format og
størrelse via `srcset` – en besøgende henter kun én af de fire.
`vis`-kolonnen i `beskaer.py` er den bredde, billedet faktisk fylder på skærmen;
alt skaleres ud fra den. Det var den største enkeltbesparelse: polaroiderne på
forsiden var 851 px brede til en plads på 280 px.

**Ingen original bruges to steder.** Scriptet fejler med det samme, hvis man
kommer til at bruge samme foto til to pladser. Hver beskæring er sat manuelt
efter motivet – ikke automatisk midterbeskæring – og låst til det sideforhold,
pladsen på siden bruger, så intet billede kan blive strukket. EXIF- og GPS-data
er fjernet.

## Hvad bruges hvor

| Motiv | Bruges på | Original | Størrelse (2x) | WebP |
|---|---|---|---|---|
| `hero-gynge` | Forside, stort polaroid | FullSizeRender-9.jpeg | 720×900 | 203 KB |
| `forside-vandloeb` | Forside, polaroid | IMG_4849.JPG | 400×400 | 40 KB |
| `forside-sandkasse` | Forside, polaroid | IMG_3944.JPG | 400×400 | 52 KB |
| `kort-mudderklub` | Forside, genvejskort | IMG_4353.JPG | 720×540 | 93 KB |
| `kort-vaerdier` | Forside, genvejskort | IMG_3981.JPG | 720×540 | 24 KB |
| `kort-sted` | Forside, genvejskort | FullSizeRender-8.jpeg | 720×540 | 103 KB |
| `mk-mudder` | Mudder Klubben, intro | FullSizeRender-2.jpeg | 1080×720 | 196 KB |
| `mk-traktor` | Mudder Klubben, traktoren | FullSizeRender-7.jpeg | 1080×720 | 170 KB |
| `mk-skovhule` | Mudder Klubben, skovlegepladsen | IMG_4829.JPG | 1080×1350 | 243 KB |
| `mk-legeplads` | Mudder Klubben, galleri | FullSizeRender-5.jpeg | 700×525 | 57 KB |
| `mk-vandkanal` | Mudder Klubben, galleri | IMG_3948.JPG | 700×525 | 48 KB |
| `mk-skovsti` | Mudder Klubben, galleri | IMG_4825.JPG | 700×525 | 63 KB |
| `vd-ro` | Værdier 1 – Ro og nærvær | IMG_4118.JPG | 1080×1350 | 72 KB |
| `vd-tillid` | Værdier 2 – Tillid | IMG_4821.JPG | 1080×1350 | 113 KB |
| `vd-vildt` | Værdier 3 – Krop og sanser | FullSizeRender-1.jpeg | 1080×1350 | 334 KB |
| `sted-hus` | Dagplejehuset, karrusel 1/3 | FullSizeRender-3.jpeg | 1080×1350 | 70 KB |
| `sted-hus2` | Dagplejehuset, karrusel 2/3 | FullSizeRender-4.jpeg | 1080×1350 | 36 KB |
| `sted-hus3` | Dagplejehuset, karrusel 3/3 | FullSizeRender.jpeg | 1080×1350 | 67 KB |
| `sted-stald` | Her hvor vi bor, Stalden | IMG_4250.JPG | 1080×1350 | 125 KB |
| `sted-skov` | Her hvor vi bor, Baghaveskoven | IMG_4239.JPG | 1080×720 | 189 KB |
| `sted-have` | Her hvor vi bor, Haven | IMG_4553.JPG | 1080×1350 | 144 KB |
| `sted-have2` | Haven, galleri | IMG_5020.JPG | 1060×795 | 50 KB |
| `sted-have3` | Haven, galleri | IMG_4554.JPG | 1060×795 | 85 KB |
| `praktisk-regntoej` | Praktisk info | FullSizeRender-6.jpeg | 1080×1350 | 420 KB |
| `om-mig` | Om mig | IMG_4826.JPG | 1080×1350 | 129 KB |

Tabellen viser den store WebP-udgave. En besøgende på telefon får `-1x`-filerne
og henter typisk 150–370 KB billeder pr. side. Alt under første skærmfuld
indlæses med `loading="lazy"`; det øverste billede på forsiden og på Her hvor vi
bor forhåndsindlæses.

Nogle originaler er mindre end den ønskede dobbelte opløsning. `beskaer.py`
skriver en advarsel, når det sker, og opskalerer aldrig – den bruger bare
originalens egen bredde.

## Beskæringer der fjerner skærmbillede-elementer

Flere af originalerne er skærmbilleder med UI oven på motivet. Beskæringen er
sat, så det er væk:

| Fil | Hvad der er beskåret væk |
|---|---|
| `vd-ro.jpg` (IMG_4118) | Tilbage-pil øverst til venstre, "..."-menu øverst til højre, hvide bånd top og bund |
| `sted-have2.jpg` (IMG_5020) | Skærmbillede-ikon nederst til højre |
| `sted-stald.jpg` (IMG_4250) | "1/4"-billedtæller øverst til højre |
| `vd-tillid.jpg` (IMG_4821) | Beskåret ind på de to børn |

## ⚠️ Fotos der sandsynligvis ikke er Jeanettes egne

Skal afklares med hende, inden siden går live. Ca. 15 af de 39 filer i zip'en
ligner gemte inspirationsbilleder frem for billeder fra hendes egen gård:

- **IMG_4822** – synligt vandmærke fra en engelsk blog (`stompinginthemud.blogspot.co.uk`). **Ikke brugt.**
- **IMG_4824** – Google Lens-ikon henover, tydeligt et skærmbillede. **Ikke brugt.**
- **IMG_4823, IMG_4827, IMG_4828, IMG_4830, IMG_4831, IMG_4832, IMG_4833, IMG_4848**
  – skovbørnehave-motiver med andre børn, andet terræn og anden billedstil end
  resten. Ingen af dem er i hendes egen Canva-plakat. **Ikke brugt.**

**Fire usikre billeder er i brug** efter aftale, og kan skiftes ud på fem minutter:

| Plads på siden | Fil | Original |
|---|---|---|
| Mudder Klubben, skovlegepladsen | `mk-skovhule.jpg` | IMG_4829 |
| Mudder Klubben, galleri | `mk-skovsti.jpg` | IMG_4825 |
| Værdier 2 – Tillid | `vd-tillid.jpg` | IMG_4821 |
| Om mig | `om-mig.jpg` | IMG_4826 |

**Sikkert hendes egne** (går igen i hendes egen Canva-plakat eller viser tydeligt
samme skur, sandkasse, bålplads og legestue): FullSizeRender og FullSizeRender-1
til -10, IMG_3944, IMG_3948, IMG_3981, IMG_4118, IMG_4239, IMG_4250, IMG_4353,
IMG_4354, IMG_4553, IMG_4554, IMG_4849.

## Ikke brugt

De resterende 14 originaler er ikke brugt – for lav opløsning (IMG_4838, det
eneste billede inde fra en stald, er kun 240×242 px), uklart motiv, eller fordi
der allerede var et stærkere billede til den plads.
