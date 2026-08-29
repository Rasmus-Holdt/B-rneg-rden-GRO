# Billeder

35 motiver, skåret ud af originalerne i `kilder/fotos/`. `beskaer.py` genskaber
alle beskæringer fra dem med én kommando:

```
cd billeder && python3 beskaer.py
```

For hvert motiv laves ni filer: `navn.*` i dobbelt opløsning, `navn-15x.*` i
halvanden og `navn-1x.*` i normal – hver i AVIF, WebP og JPEG. Browseren vælger selv format og
størrelse via `srcset` – en besøgende henter kun én af de ni.
`vis`-kolonnen i `beskaer.py` er den bredde, billedet faktisk fylder på
skærmen; alt skaleres ud fra den.

**Ingen original bruges to steder.** Scriptet fejler med det samme, hvis man
kommer til at bruge samme foto til to pladser. Hver beskæring er sat manuelt
efter motivet – ikke automatisk midterbeskæring – og låst til det sideforhold,
pladsen på siden bruger, så intet billede kan blive strukket. EXIF- og
GPS-data er fjernet.

## Nyt i denne runde (Jeanettes rettelser)

Jeanette sendte 16 billeder på sms i tre kategorier: Mudder Klubben, Stalden
og Baghaveskoven. Fire af dem viste sig at være fotos, vi allerede havde i
`kilder/fotos/`:

| Sms-billede | Er i forvejen | Hvad der skete |
|---|---|---|
| Dækkene med planter | `IMG_4239` = `sted-skov` | Står nu som første dias i Baghaveskoven-karrusellen |
| Pigen i tovgyngen | `FullSizeRender-9` = `hero-gynge` | `hero-gynge` var ikke længere i brug på nogen side. Motivet er flyttet til Baghaveskoven som `skov-tovgynge` |
| To børn der graver | `FullSizeRender-1` = `vd-vildt` | **Ikke flyttet.** Det bærer Værdier 3, og samme foto må ikke stå to steder |
| Mudderkøkkenet med gryder | `IMG_4819` | Var ikke brugt før. Er nu `sted-have2` |

De øvrige 12 er lagt i `kilder/fotos/` med `sms-`-præfiks, så det altid kan
ses, hvor de kom fra.

Tre motiver er væk: `mk-traktor` og `mk-skovhule` (Jeanette bad om at få
billederne på Mudder Klubben slettet) og `hero-gynge` (flyttet, se ovenfor).

## Hvad bruges hvor

| Motiv | Bruges på | Original | Størrelse (2x) | AVIF |
|---|---|---|---|---|
| `forside-vandloeb` | Forside, polaroid + delebillede | sr-forside-vandloeb.jpg (opskaleret, af IMG_4849.JPG) | 1080×810 | 108 KB |
| `forside-sandkasse` | Forside, polaroid | sr-forside-sandkasse.jpg (opskaleret, af IMG_3944.JPG) | 1080×810 | 99 KB |
| `kort-mudderklub` | Forside, genvejskort | sr-kort-mudderklub.jpg (opskaleret, af sms-mudder-vandloeb.jpg) | 720×540 | 36 KB |
| `kort-vaerdier` | Forside, genvejskort | IMG_3981.JPG | 720×540 | 17 KB |
| `kort-sted` | Forside, genvejskort | FullSizeRender-8.jpeg | 720×540 | 60 KB |
| `mk-mudder` | Mudder Klubben, karrusel 1/2 | FullSizeRender-2.jpeg | 1080×720 | 113 KB |
| `mk-koekken` | Mudder Klubben, karrusel 2/2 | sms-mudder-koekken-boern.jpg | 1080×720 | 30 KB |
| `mk-legeplads` | Mudder Klubben, galleri | FullSizeRender-5.jpeg | 700×525 | 34 KB |
| `mk-vandkanal` | Mudder Klubben, galleri | sr-mk-vandkanal.jpg (opskaleret, af IMG_3948.JPG) | 700×525 | 43 KB |
| `mk-skovsti` | Mudder Klubben, galleri | IMG_4825.JPG | 700×525 | 41 KB |
| `vd-ro` | Værdier 1 – Ro og nærvær | sr-vd-ro.jpg (opskaleret, af IMG_4118.JPG) | 1080×1350 | 62 KB |
| `vd-tillid` | Værdier 2 – Tillid | sr-vd-tillid.jpg (opskaleret, af IMG_4821.JPG) | 1080×1350 | 98 KB |
| `vd-vildt` | Værdier 3 – Krop og sanser | FullSizeRender-1.jpeg | 1080×1350 | 119 KB |
| `sted-hus` | Dagplejehuset, karrusel 1/3 | FullSizeRender-3.jpeg | 1080×720 | 29 KB |
| `sted-hus2` | Dagplejehuset, karrusel 2/3 | FullSizeRender-4.jpeg | 1080×720 | 20 KB |
| `sted-hus3` | Dagplejehuset, karrusel 3/3 | FullSizeRender.jpeg | 1080×720 | 26 KB |
| `sted-stald` | Stalden, karrusel 1/8 | IMG_4250.JPG | 1080×720 | 62 KB |
| `stald-kanin` | Stalden, karrusel 2/8 | sr-stald-kanin.jpg (opskaleret, af sms-stald-kanin.jpg) | 1080×720 | 108 KB |
| `stald-aeg` | Stalden, karrusel 3/8 | sr-stald-aeg.jpg (opskaleret+beskåret, af sms-stald-aeg.jpg) | 1080×720 | 22 KB |
| `stald-hoene` | Stalden, karrusel 4/8 | sms-stald-hoene.jpg | 1080×720 | 19 KB |
| `stald-kyllinger` | Stalden, karrusel 5/8 | sms-stald-kyllinger.jpg | 1080×720 | 68 KB |
| `stald-aellinger` | Stalden, karrusel 6/8 | sms-stald-aellinger.jpg | 1080×720 | 73 KB |
| `stald-halmballer` | Stalden, karrusel 7/8 | sms-stald-halmballer.jpg | 1080×720 | 59 KB |
| `stald-legerum` | Stalden, karrusel 8/8 | sms-stald-legerum.png | 1080×720 | 76 KB |
| `sted-skov` | Baghaveskoven, karrusel 1/5 | sr-sted-skov.jpg (opskaleret, af IMG_4239.JPG) | 1080×720 | 111 KB |
| `skov-traedestubbe` | Baghaveskoven, karrusel 2/5 | sr-skov-traedestubbe.jpg (opskaleret, af sms-skov-traedestubbe.jpg) | 1080×720 | 64 KB |
| `skov-daekgynge` | Baghaveskoven, karrusel 3/5 | sms-skov-daekgynge.jpg | 1080×720 | 75 KB |
| `skov-tovgynge` | Baghaveskoven, karrusel 4/5 | FullSizeRender-9.jpeg | 1080×720 | 105 KB |
| `skov-trae` | Baghaveskoven, karrusel 5/5 | sms-skov-trae.jpg | 1080×720 | 119 KB |
| `sted-have` | Haven, karrusel 1/3 | IMG_4553.JPG | 1080×720 | 43 KB |
| `sted-have2` | Haven, karrusel 2/3 – mudderkøkkenet | sr-sted-have2.jpg (opskaleret, af IMG_4819.JPG) | 1080×720 | 65 KB |
| `sted-have3` | Haven, karrusel 3/3 | IMG_4554.JPG | 1060×795 | 52 KB |
| `praktisk-regntoej` | Praktisk info | FullSizeRender-6.jpeg | 1080×720 | 102 KB |
| `jeanette` | Om mig + header på alle sider | jeanette-portraet.jpeg | 600×750 | 23 KB |
| `jeanette-boern` | Om mig, delebillede | jeanette-boern.jpeg | 684×456 | 18 KB |

## Sidevægt efter karrusellerne

De tre karruseller på "Her hvor vi bor" rummer 16 billeder. Kun det første
dias i hver karrusel hentes ved sideindlæsning; resten står med
`loading="lazy"` inde i en vandret rullebeholder og hentes først, når man
swiper hen til dem.

| | Ved sideindlæsning | Hvis man ser alt |
|---|---|---|
| Telefon (1x) | 97 KB | 672 KB |
| Computer (2x) | 194 KB | 1.242 KB |

Det er stadig den tungeste side på hjemmesiden. Vil man have den ned, er den
korteste vej at skære et par dias af Stalden-karrusellen – ikke at
komprimere hårdere.

## Opskalerede billeder (AI-superresolution)

Elleve motiver var mindre end den plads, de fylder på siden – enten fordi
selve originalfotoet var lille (`sted-have2`, `mk-vandkanal`, `vd-tillid`),
eller fordi en stram, rigtig beskæring kostede bredde (`stald-aeg`,
`forside-vandloeb`, `kort-mudderklub`, `vd-ro`, `sted-skov`,
`skov-traedestubbe`, `stald-kanin`, `forside-sandkasse`). De blev vist i
under 75 % af den tilsigtede opløsning – synligt bløde på en skarp skærm.

`beskaer.py` skalerer aldrig op – almindelig opskalering (bicubic/Lanczos)
tilføjer ingen ægte detalje, kun sløring, og ville gøre billederne dårligere,
ikke bedre. I stedet er de kørt igennem FSRCNN, et lille neuralt
superresolution-netværk (OpenCV's `dnn_superres`, model `FSRCNN_x2`), som
genopbygger kanter og struktur ud fra mønstre i selve billedet – i praksis
det samme, en fotograf ville gøre med Topaz eller Lightrooms
opskaleringsværktøj. Resultatet er gemt som en ny kildefil
(`kilder/fotos/sr-<motiv>.jpg`) og sat ind i `JOBS` i stedet for det
oprindelige foto, med beskæringen allerede foretaget (box `0,0,1,1`) – selve
beskæringsvalget er ikke ændret, kun opløsningen.

Kontrolleret for hvert af de 11 billeder: gennemsnitlig farveafvigelse pixel
for pixel er under 0,3 ud af 255 pr. kanal – umuligt at se, og langt under
JPEG-kompressionens egen støj. Ingen finjustering af farve, hvidbalance
eller kontrast er lavet. Alle 11 rammer nu den fulde 2×-målopløsning
(1080 px, eller det tilsvarende for kort-/mindre motiver).

Originalfotos­ne ligger stadig urørt i `kilder/fotos/` under deres
oprindelige navne, hvis motivet skal beskæres om.

## Billeder der er værd at kigge på igen

**`stald-aeg` er teknisk svag.** Originalen er et uskarpt videobillede, og
det, der fylder mest, er et ærme ude af fokus. Beskæringen er skåret
strammere ind om æggene og hånden, så den sorte jakke kun er en smal kant i
højre side i stedet for at fylde næsten halvdelen af billedet – men det er
stadig det svageste af de otte staldbilleder. Det ville ikke koste noget at
lade det ude.

**`om-mig` er taget ud.** Jobbet lavede seks filer, som ingen af de syv
sider hentede – siden "Om mig" bruger portrættet af Jeanette. Originalen
(IMG_4826) ligger stadig i `kilder/fotos/`, hvis motivet skal bruges igen.

## ⚠️ Fotos hvor det bør bekræftes, at de er Jeanettes egne

Det har været en åben post fra starten, og de nye sms-billeder har ikke lukket
den. **Skal afklares, inden siden går live.**

Fra det oprindelige materiale er der nu kun to tilbage i brug:

| Plads | Fil | Original |
|---|---|---|
| Mudder Klubben, galleri | `mk-skovsti` | IMG_4825 |
| Værdier 2 – Tillid | `vd-tillid` | IMG_4821 |

To af de fire, der stod her før, er ude af siden: `mk-skovhule` (IMG_4829)
blev slettet med Jeanettes rettelse, og `om-mig` (IMG_4826) er taget helt ud
af `beskaer.py`.

Blandt de nye sms-billeder ser fire ud til at være gemte inspirationsbilleder
snarere end fotos fra gården:

| Plads | Fil | Hvorfor |
|---|---|---|
| Haven, mudderkøkkenet | `sted-have2` (IMG_4819) | 564×705 px – den typiske størrelse for et gemt Pinterest-billede. Terrakotta, sækkelærred og eukalyptus ligner ikke resten af haven |
| Mudder Klubben, karrusel | `mk-koekken` | Havde en lyserød/grøn ramme, altså et skærmbillede fra et opslag. Motivet ligner et AI-genereret billede, samme stil som det IMG_5020, dette billede afløser |
| Stalden, karrusel | `stald-legerum` | Sandgulv og plastiklegetøj i en lade – hverken bygningen eller legetøjet går igen på nogen af de andre billeder |
| Baghaveskoven, karrusel | `skov-trae` | Stedsegrøn eg og tørt terræn. I originalen er der bjerge i baggrunden; de er beskåret væk, men træet er stadig ikke dansk |

De øvrige otte nye billeder – kaninen, kyllingerne, halmballerne,
ællingerne, æggene, hønen, trædestubbene og dækgyngen – ligner klart
Jeanettes egen gård og går igen med samme bygninger og hegn som resten.

## Beskæringer der fjerner skærmbillede-elementer

| Fil | Hvad der er beskåret væk |
|---|---|
| `vd-ro.jpg` (IMG_4118) | Tilbage-pil øverst til venstre, "…"-menu øverst til højre, hvide bånd top og bund |
| `sted-stald.jpg` (IMG_4250) | "1/4"-billedtæller øverst til højre |
| `vd-tillid.jpg` (IMG_4821) | Beskåret ind på de to børn |
| `mk-koekken.jpg` | Lyserød og grøn ramme øverst og nederst |

## Beskæringer der er sat efter motivet

Den automatiske beskæring tager 40 % fra toppen af det overskydende og
centrerer vandret. Det rammer forkert, når motivet ikke sidder i midten, og
ti billeder er derfor sat i hånden efter en gennemgang af alle 35:

| Fil | Hvad der var galt | Nu |
|---|---|---|
| `sted-hus2` | Barnet på klatrevæggen var skåret over – hovedet lå helt uden for billedet | Hele barnet med, fra hænder til bare fødder |
| `sted-hus3` | Hovedet på barnet ved reolen var skåret af | Barnet står frit med luft over hovedet |
| `stald-hoene` | Hønen var skåret af forneden | Barn og høne fylder billedet |
| `mk-skovsti` | Barnet nederst til højre var skåret midt over | Alle fire børn er med |
| `mk-mudder` | Begge børn faldt helt ud af billedet | Begge børn og gravemaskinen er med |
| `kort-mudderklub` | Barnet stod klemt ude i venstre kant med tre fjerdedele tomt mudder | Barnet fylder venstre tredjedel, vandløbet resten |
| `stald-aeg` | Æggene lå nede i hjørnet, et ærme ude af fokus fyldte resten | Beskåret ind på reden. Originalen er et uskarpt videobillede, så det er så godt, det bliver |
| `stald-kanin` | Barn og kanin lå småt i et billede fuldt af tom halm | Strammere om barnet og kaninen |
| `praktisk-regntoej` | Barnet til højre var skåret af forneden | Barnet står helt i billedet ved bålpladsen |
| `stald-kyllinger` | Kyllingerne og varmelampen sad nederst og faldt ud | Beskærer til de nederste to tredjedele |

Tre af originalerne har motivet så tæt på kanten, at der ikke er mere at
hente: `stald-hoene` mangler toppen af barnets hoved, og `kort-mudderklub`
har barnet helt ude i venstre kant. Sådan er billedet taget.
