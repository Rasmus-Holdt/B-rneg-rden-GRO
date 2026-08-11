# Børnegården GRO – hjemmeside

Projektstatus: **v4 – bygget helt om.**

Kunde: Jeanette Riis, privat pasningsordning, Vinderslevvej 45, Vinderslev, 8620 Kjellerup.
Solgt via Handyhand.

## Sådan ser du siden

Åbn `index.html` i en browser. Rene statiske HTML-filer, intet build-trin nødvendigt
for at se den.

## Sådan retter du i teksten

Rediger **ikke** HTML-filerne direkte – de bliver overskrevet. Al tekst og struktur
står i `byg.py`. Ret der, og kør:

```
python3 byg.py
```

Så genskrives alle syv HTML-filer med den samme header, navigation og footer.
Det er også dét, der sikrer, at menuen er ens på alle sider.

## Sider

Fanerne følger den struktur, Jeanette selv skrev i sit tekstdokument:

| Fil | Fane |
|---|---|
| `index.html` | Forside |
| `mudderklubben.html` | Mudder Klubben – konceptet, medlemsfordele, mudderpasset |
| `vaerdier.html` | Værdier – de tre bærende principper |
| `her-hvor-vi-bor.html` | Her hvor vi bor – dagplejehuset, stalden, baghaveskoven, haven |
| `praktisk.html` | Praktisk – medbringe, det jeg sørger for, ledige pladser, økonomi |
| `om-mig.html` | Om mig – Jeanettes egen historie |
| `kontakt.html` | Kontakt – telefon, Instagram, adresse og kort |

## Design

Bygget tæt på Jeanettes egen Canva-skitse, efter aftale:

- **Brede, blege lodrette striber** som baggrund over hele siden. Ren
  CSS-gradient – ingen billedfil, ingen indlæsningstid
- **Den tegnede sol** går igen i header, sidehoveder, mudderpasset, footeren
  og som favicon. Den er tegnet i kode, ikke et billede, så den er skarp overalt
- **Cremefarvede papirkort** bærer al brødtekst. Det er dét, der gør, at lange
  afsnit stadig er til at læse oven på et stribet underlag – teksten står aldrig
  direkte på striberne
- **Skrifter:** Baloo 2 (runde overskrifter), Nunito (brødtekst, 18 px / 1,72 i
  linjeafstand), Caveat (håndskrevne accenter)

### Paletten

Holdt bevidst på tre farvefamilier, så intet trækker i hver sin retning:

| Rolle | Farve | Bruges til |
|---|---|---|
| Baggrund | Bleg himmelblå `#cfe0f0` / `#eaf2fa` | Striberne, intet andet |
| Flade | Varm creme `#fbf3e6` | Alle kort, header, footer |
| Tekst og struktur | Dyb petroleum `#12695a` | Overskrifter, links, sekundære knapper |
| Fremhævning | Solgul `#f7c948` og solvask `#fdf1d6` | Sollinjen i header, stempelfelter, "ledige pladser" |
| Handling | Rød `#d1503f` | Ring-knappen, aktiv fane, små versallabels |

Solgul er en lys nabo til cremen, så den lægger sig oveni i stedet for at
konkurrere. Rød er den eneste kolde-varme kontrast på siden og er derfor holdt
på det, der skal ses: ring, skriv, ledige pladser. Der er ingen grøn.

### Teknisk

- Responsivt: brydepunkter ved 1180, 900, 620 og 380 px.
  Verificeret i 1440, 768, 390 og 360 px bredde
- 8 KB JavaScript i alt: karrusel og overgangs-reserve. Ingen biblioteker
- `prefers-reduced-motion` og printstylesheet respekteres
- Alle billeder har alt-tekst, ét `<h1>` pr. side, "spring til indhold"-link,
  synlig tastaturmarkering
- Ingen døde links eller ankre, ingen ubrugte CSS-klasser eller -variabler
  (alt verificeret maskinelt)
- Skrifterne ligger på vores egen server i `assets/skrifter/`. Ingen data om
  besøgende sendes til Google, og browseren skal ikke først åbne en forbindelse
  til et fremmed domæne, før teksten kan sættes

### På telefon

Headeren er fastlåst i toppen, så den skal fylde lidt. Den er nede fra ca. 230 px
til **115 px**:

- Logo og ring-knap deler én række; undertitlen er skjult (den står i footeren)
- Ring-knappen viser kun nummeret, ikke "Ring til Jeanette"
- De syv faner fyldte tre rækker. Nu **én række, der kan svirpes til siden**,
  med en blød udtoning i højre kant som hint
- Alle klikflader er mindst 40 px høje. Verificeret på alle syv sider
- Ingen vandret rulning på nogen bredde. Verificeret element for element
- Hover-effekter er pakket i `@media (hover: hover)`, så de ikke hænger fast
  efter et tryk
- `-webkit-text-size-adjust: 100%` så iOS ikke selv skalerer teksten
- `scroll-padding-top` så spring-til-links lander under den faste header

## Ændringer fra v3

v3 blev afvist på billedbeskæring, for mange dekorative elementer og et samlet
indtryk, der var svært at overskue. v4 er bygget forfra:

- **7 faner efter Jeanettes egen struktur** i stedet for 5 sammenlagte. Hver fane
  har ét emne, så ingen side bliver en lang rulle
- **Hendes stil taget helt ind.** v3 var nedtonet og redaktionel; v4 bruger
  striberne, solen og farverne fra hendes Canva
- **25 billeder** mod v3's 12, alle med låst format pr. plads
- **Mudderpasset som et rigtigt pas** med 20 stempelfelter, hvert med sit eget
  tegnede ikon
- **Ledige pladser fremhævet** – det er hendes stærkeste salgsargument lige nu
- **Kort og tre store kontaktveje** i stedet for en formular
- **Fælles header/footer genereret fra `byg.py`**, så menuen ikke kan komme til
  at være forskellig fra side til side

## Sådan hænger siderne sammen

Alle syv sider åbner ens: et cremefarvet kort med solen kigrende ud over
øverste venstre hjørne. Det er den gennemgående gestus, der binder dem sammen.
Derefter veksler hver side mellem billede-plus-tekst-blokke (skiftevis venstre
og højre), gallerier med ens billedhøjde, og en fremhævet boks. Ingen side
består af den samme komponent to gange i træk.

### De 20 stempelikoner

Hvert mærke i mudderpasset har sit eget tegnede stregikon – hånd, fodaftryk,
kanin, æg, brød, regnorm, traktor, spand, gryde, regnbue, gren, gris,
gummistøvle, spire og så videre. De er tegnet i kode i samme stregstil som
telefon- og adresseikonerne, ikke emojis, så de er skarpe på alle skærme og
matcher resten af siden. Ikonringene skifter mellem petroleum, rød og solgul
og står let skævt, så de ligner rigtige stempler.

## Gentagelser der er ryddet op

Gennemgået systematisk og fjernet:

| Hvad | Før | Nu |
|---|---|---|
| Samme foto brugt to steder | 4 originaler gik igen (hyggekrogen tre gange) | 0 – `beskaer.py` fejler, hvis det sker igen |
| "Ring 27 12 23 07" på forsiden | 5 gange | 2 (den faste knap i headeren + én CTA) |
| Tagline "Gårdliv, nærvær og vild leg" | 3 gange på forsiden | 1 |
| "Ledige pladser"-boksen | Forside, Praktisk og Kontakt | Forside og Praktisk; på Kontakt kun én linje |
| To knapper til samme handling | Praktisk, Om mig, Kontakt | Én tydelig knap hvert sted |
| To forskellige "smalle" spaltebredder | 800 px og 880 px | Én bredde: 800 px |
| Farvede flader bag tekst | Grøn og orange | Ingen – alt står på samme creme, fremhævet felt får en sollinje i toppen |
| Gule skiver ved medlemsfordelene | 6 ens gule prikker | Hver fordel har sit eget tegnede ikon |

## Mapper

```
byg.py                              ← al tekst og sidestruktur. Ret her.
assets/style.css                    ← fælles stylesheet
assets/karrusel.js                  ← billedkarrusel (5 KB)
assets/overgang.js                  ← sideovergange i Firefox og ældre Safari (4 KB)
assets/skrifter/                    ← Nunito, Baloo 2 og Caveat (75 KB i alt)
assets/style.min.css                ← genereres af byg.py – ret ikke i den
_headers, .htaccess                 ← cache-regler til hosten
assets/ikoner.py                    ← genererer hele ikonsættet ud fra solen
favicon.* , ikon-*.png , logo-512   ← ikoner i roden (Google kigger her)
sitemap.xml, robots.txt,
site.webmanifest                    ← genereres af byg.py
billeder/                           ← 25 motiver × 6 filer (avif/webp/jpg i 1x og 2x)
  README.md                         ← hvad bruges hvor + advarsel om fotorettigheder
  beskaer.py                        ← beskærer og optimerer fra originalerne
indhold/00-fakta-og-kilder.md       ← hvert faktum og hvor det kommer fra
indhold/02-sporgsmaal-til-kunden.md ← det der mangler afklaring
kilder/                             ← Jeanettes to PDF'er + alle 39 originalfotos
```

## Mangler før den kan gå live

- [ ] **Slet `overgang-test.html`** – den er kun til fejlfinding
- [ ] **Rettigheder til fire fotos** – se advarslen i `billeder/README.md`
- [ ] **Bekræft domænet** www.BoernegaardenGRO.dk
- [ ] **Bekræft postnummer-visningen.** Adressen er slået op i DAWA og er
      officielt "Vinderslevvej 45, Vinderslev, 8620 Kjellerup". Jeanettes eget
      materiale skriver kun "Vinderslevvej 45, 8620 Kjellerup" – supplerende
      bynavn Vinderslev er tilføjet, fordi det gør den nemmere at finde
- [ ] **Et billede af Jeanette selv.** Der er ingen i materialet. Om mig-siden er
      hendes personlige tekst uden hendes ansigt, og det er dét, der ville løfte
      tilliden mest af alt
- [ ] **Et skarpt billede inde fra stalden.** Det eneste, der findes, er 240×242 px

## Kontaktsiden

Der er **ingen kontaktformular**. Siden viser i stedet tre store klikfelter:
ring, skriv på Instagram, kom forbi. På telefon er hvert felt et fuldt kort man
kan ramme med tommelfingeren, og telefonnummeret åbner direkte i opkald.

Det sparer også en tredjepartstjeneste (formularer på statiske sider kræver
Formspree eller lignende), en cookiebanner-diskussion og et sted hvor
henvendelser kan gå tabt uden at nogen opdager det.

## Årstiderne på Praktisk

"Efter sæson" har sit eget felt i fuld bredde med tre tegnede ikoner – sol,
snefnug og spire – i hver sin tone. Det er tegnede stregikoner i samme sprog som
resten af siden, ikke emojis: de er skarpe på alle skærme, kan farves med CSS,
og de bryder ikke stilen. Tonerne sidder kun i den lille ikoncirkel, aldrig som
flade bag tekst.

## Sideovergange

> **Ser du dem ikke?** Åbn `overgang-test.html`. Den tjekker de fire ting, der
> skal være opfyldt, og siger hvad der mangler. To hyppige årsager:
> **"Reducér bevægelse"** er slået til i systemindstillingerne (så dæmper siden
> med vilje alle animationer), eller siden ligger **kun på disken** – reserven
> til Firefox og ældre Safari kræver en rigtig server. Slet
> `overgang-test.html` inden siden går live.


Klikker man en fane, bliver headeren stående helt stille, mens indholdet under
den glider ud og det nye toner ind nedefra. Det er dét, der får de syv sider til
at føles som ét sted frem for syv løsrevne dokumenter.

Det er bygget med **View Transitions** (`@view-transition { navigation: auto }`),
som er ren CSS – ingen JavaScript, ingen framework, ingen "single page
app"-konstruktion med de problemer det giver for tilbage-knappen og SEO.
Headeren og footeren har hver sit `view-transition-name`, så browseren ved, at
de er de samme elementer på tværs af sider og ikke skal animeres.

Fire detaljer gør forskellen fra "en fade" til noget der føles dyrt:

1. **Den røde streg under den aktive fane glider** hen til den nye fane i stedet
   for at forsvinde ét sted og dukke op et andet. Stregen har sit eget
   `view-transition-name`, så browseren forstår, at det er den samme streg
2. **Hele skiftet tager 0,3 sekund.** Man har allerede besluttet sig for at
   skifte side; alt over et halvt sekund føles ikke elegant, det føles som at
   vente
3. **Et lille overlap – men aldrig et tomt hul.** Den gamle side toner ud på
   0,14 s, den nye begynder efter 0,06 s. Øjeblikket hvor hverken den gamle
   eller den nye side er synlig, er præcis dét, øjet opfatter som et hak
4. **Solen i logoet har sit eget navn**, så den ikke blinker et enkelt billede
   under skiftet. Den er det faste holdepunkt

### Hvad hakket kom af

Overgangen var oprindeligt 0,68 sekund med et tomt hul på midten, og fire ting
trak i hver sin retning på samme tid. Alle fire er væk nu:

| Årsag | Hvad man så | Rettelse |
|---|---|---|
| To animationer oveni hinanden | Topkortet blev flyttet af både sideovergangen og sin egen entré-animation | Entré-animationen på `.hero-kort`/`.sidehoved` er fjernet – nu er der én bevægelse |
| Rullebjælken forsvandt | Gik man fra en lang til en kort side, sprang alt indhold 15 px til højre midt i skiftet | `scrollbar-gutter: stable` på `html` – pladsen reserveres altid |
| Skriften landede midt i overgangen | Teksten skiftede udseende og ombrød på ny, netop mens siden tonede ind | Skrifterne ligger lokalt og forudhentes, så de er der inden første optegning |
| Blød rulning + hop til toppen | I Firefox rullede siden blødt op **samtidig med** at den tonede ind | `scrollTo({behavior:'instant'})` i `overgang.js` |

### I browsere der ikke kan det selv

Firefox og Safari før 18.2 understøtter ikke View Transitions. Der tager
`assets/overgang.js` (3 KB) over: den henter den nye side i baggrunden, skifter
`<main>` ud og animerer med de samme keyframes. Resultatet er visuelt identisk.

Det er **ikke** en single page app. Adresselinjen, tilbage-knappen, bogmærker og
søgemaskiner opfører sig præcis som før – scriptet flytter kun indhold og bruger
`history.pushState`. Verificeret: titel, URL og aktiv fane følger med, tilbage-
knappen virker, og karrusellen sættes op igen på det nye indhold.

Alt kan fejle uden konsekvens. Går noget galt, sendes browseren afsted med
`location.href`, og værst tænkelige udfald er en helt almindelig sideindlæsning.
På `file://` slår scriptet fra af sig selv, fordi `fetch()` ikke er tilladt der.

**Reducér bevægelse** håndteres nu ordentligt. Før slog det hele blokken fra med
`animation: none !important`, og så sad man tilbage med hårde spring. Nu fjernes
kun forskydning og skalering – de bløde krydsfader bliver, bare kortere. Det er
bevægelsen, der giver svimmelhed, ikke at billedet ændrer sig.

Derudover toner kortene blidt op, når man ruller ned til dem. Også ren CSS
(`animation-timeline: view()`), så der er ingen JavaScript der kan fejle og
efterlade indhold usynligt – i browsere uden understøttelse står alting bare
synligt fra start. Begge dele slås fra ved `prefers-reduced-motion`.

## Billedkarrusel

Dagplejehuset har tre billeder samlet i én karrusel ved siden af teksten, som et
Instagram-opslag. Selve bevægelsen er **ren CSS scroll-snap**, ikke JavaScript –
derfor føles swipe på telefon som i styresystemet frem for som en efterligning,
og den er flydende selv på en gammel telefon.

`assets/karrusel.js` (4 KB, ingen biblioteker) gør kun to ting: holder prikkerne
i sync med hvad man kigger på, og lader pilene rulle ét billede ad gangen.
Slår man JavaScript fra, bliver karrusellen bare en vandret stribe billeder man
kan rulle i – intet går i stykker. Pilene vises kun når der er en mus,
prikkerne har 34 px klikfelt, og piletasterne virker.

## Hastighed

### Forudrendering – det største greb

```html
<script type="speculationrules">
{"prerender":[{"where":{"or":[...]},"eagerness":"moderate"}]}
</script>
```

Hviler musen på en fane, henter **og optegner** browseren siden på forhånd.
Klikket bliver derefter øjeblikkeligt – ikke "hurtigt", men uden ventetid
overhovedet. `moderate` betyder, at det først sker efter ca. 200 ms med musen
på linket, så der ikke hentes sider i blinde.

### Skrifterne ligger på vores egen server

Før hentedes tre skriftfamilier i otte vægte fra Google Fonts: 207 KB fra et
fremmed domæne, som browseren først skulle slå op og lave en ny sikker
forbindelse til, før teksten kunne sættes. Og hvert eneste besøg blev
registreret hos Google – på en side om andres børn.

Nu ligger de i `assets/skrifter/` som **tre variable skriftfiler**, beskåret til
de tegn dansk og de nærmeste europæiske sprog bruger:

| Fil | Vægte | Størrelse |
|---|---|---|
| `nunito.woff2` | 200–1000 | 23 KB |
| `baloo2.woff2` | 400–800 | 21 KB |
| `caveat.woff2` | 400–700 | 29 KB |

**75 KB mod 207 KB**, ingen fremmed forbindelse, og Nunito og Baloo forudhentes
med `<link rel="preload">`, så de er der inden første optegning. En variabel
skriftfil dækker alle vægte i én fil – før var det otte separate hentninger.

Reserveskrifterne er stadig **metrisk justeret** med `size-adjust`,
`ascent-override` og `descent-override`, så de fylder præcis det samme som de
rigtige. Uden det hopper siden i det øjeblik skrifterne skifter – og med
sideovergangen kørende samtidig så det ud som et hak.

### Resten

| Greb | Effekt |
|---|---|
| **Rigtig størrelse** | Billederne blev skaleret efter hvor mange pixels de faktisk fylder. Polaroiderne på forsiden var 851 px til en plads på 280 px |
| **AVIF, WebP og JPEG** | Tre spor i samme `<picture>`. AVIF fylder ca. det halve af WebP på disse fotos, og næsten alle browsere kan det i dag. Gamle browsere falder automatisk tilbage |
| **Loft over den enkelte fil** | Nogle af fotoene er meget kornede (regnvejr, vådt græs). Korn er tilfældig støj og det dyreste, der findes at komprimere. `beskaer.py` koder om med lavere kvalitet, indtil filen er under 120 KB. Regntøjs-billedet gik fra 240 KB til 118 KB uden synlig forskel i den størrelse, det vises i |
| **To opløsninger** | `srcset` med 1x og 2x, så en skærm uden retina ikke henter det store billede |
| **`width` og `height` på alt** | Pladsen er reserveret inden billedet er hentet – siden hopper ikke |
| **`loading="lazy"`** | Alt under første skærmfuld hentes først når man ruller derned |
| **Preload af det første billede** | Alle seks sider med et topbillede forudhenter det i AVIF. Før gjaldt det kun to sider; de øvrige fem ventede med deres topbillede til alt andet var hentet |
| **Minificeret CSS** | 43 KB kilde → 26 KB udgivet. `style.css` er stadig den, man retter i; `byg.py` laver `style.min.css` |
| **Cache-regler** | `_headers` (Netlify/Cloudflare) og `.htaccess` (Apache). Billeder og skrifter gemmes et år, HTML tjekkes hver gang |

Målt over en rigtig server, alt inkluderet (HTML, CSS, JS, skrifter, billeder,
ikoner). "Alm. skærm" og "Retina" er AVIF-sporet, altså det de fleste får:

| Side | Alm. skærm | Retina | Retina, browser uden AVIF |
|---|---|---|---|
| Forside | 250 KB | 431 KB | 616 KB |
| Mudder Klubben | 344 KB | 553 KB | 844 KB |
| Værdier | 280 KB | 362 KB | 557 KB |
| Her hvor vi bor | 427 KB | 622 KB | 848 KB |
| Praktisk | 195 KB | 248 KB | 471 KB |
| Om mig | 190 KB | 201 KB | 248 KB |
| Kontakt | 126 KB | 126 KB | 126 KB |

Tallene dækker **hele** siden, også de billeder man først ser efter at have
rullet. Det, browseren henter før man ser noget, er 111 KB fælles (CSS, JS,
skrifter — gemmes et år, så det hentes kun ved første besøg) plus HTML og
topbilledet: mellem 126 og 254 KB afhængigt af siden.

Til sammenligning fyldte billedmappen alene 6,3 MB før dette projekt, og alle
hentede fuld opløsning uanset skærm. Der indlæses ingen biblioteker, trackere
eller analytics — 9 KB JavaScript i alt, skrevet i hånden.

Efter det første besøg falder tallene igen: CSS, JS, ikoner og alle billeder man
allerede har set, ligger i browserens cache.

## Ikoner

Solen findes som færdige filer i roden, genereret af `assets/ikoner.py`
(kræver `cairosvg`; skal kun køres igen hvis solen ændrer sig):

| Fil | Hvor den bruges |
|---|---|
| `favicon.ico` | Browserfaner og Safari. Indeholder 16, 32 og 48 px |
| `favicon.svg` | Chrome og Firefox – skarp i alle størrelser |
| `favicon-48.png`, `favicon-96.png` | **Google søgeresultater** |
| `apple-touch-icon.png` | Når nogen gemmer siden på hjemmeskærmen på iPhone |
| `ikon-192.png`, `ikon-512.png` | Webmanifestet |
| `ikon-maskable-512.png` | Android beskærer app-ikoner til cirkler; denne har 20 % luft |
| `logo-512.png` | `logo` i de strukturerede data |

**Det er præcis den samme sol som i headeren.** `ikoner.py` klipper `sol()`
ud af `byg.py` og kører den, i stedet for at have en kopi af tegningen. Derfor
kan de to ikke komme til at afvige fra hinanden – retter man solen i headeren,
følger favicon'en med, næste gang scriptet kører.

Jeg havde først tegnet en særlig favicon-udgave med større øjne og fire stråler
i stedet for otte, fordi ansigtet bliver utydeligt ved 16 px. Men den blev sin
egen ting og lignede ikke længere sol'en på siden. Nu er der én tegning, og ved
16 px er den lidt grødet – til gengæld er det den rigtige sol. På en retina-skærm
vises 32 px-udgaven, og der er ansigtet skarpt.

**iOS lægger ikke selv baggrund på.** `apple-touch-icon.png` har cremen bagt
ind, ellers ville solen stå på sort på hjemmeskærmen. Pillow kan ikke gemme
flere størrelser i én ICO-fil, så containeren skrives manuelt i `skriv_ico()`.

### For at solen dukker op i Google

Google viser kun favicons, der opfylder alle fire krav – de er alle på plads:

1. Kvadratisk og et multiplum af 48 px (`favicon-48.png`, `favicon-96.png`)
2. Refereret med `<link rel="icon">` på forsiden
3. Ligger på samme domæne og er ikke blokeret i `robots.txt`
4. Siden er indekseret

Punkt 4 kræver, at siden faktisk er lagt op og indsendt i Google Search
Console. Der går typisk et par dage til nogle uger, før ikonet dukker op i
søgeresultatet – det er ikke noget, der kan fremskyndes fra koden.
`logo-512.png` i de strukturerede data er det, Google kan bruge ved siden af
virksomheden i et vidensfelt.

## SEO

- **Strukturerede data** (JSON-LD) på hver side: `ChildCare` med adresse,
  koordinater, telefon, åbent område (Vinderslev, Kjellerup, Silkeborg Kommune),
  aldersgruppe 0–3 og pris. Det er dem, der gør, at Google kan vise adresse og
  telefonnummer direkte i søgeresultatet frem for bare en blå linje
- **Brødkrumme-markup** på alle undersider
- **Canonical-link** på hver side
- **Titler med lokale søgeord** – "privat pasningsordning", "Vinderslev",
  "Kjellerup" – i stedet for bare virksomhedsnavnet. Det er sådan folk søger
- **Beskrivelser med det konkrete**: pris, antal ledige pladser, aldersgruppe
- **Logo i de strukturerede data**, så Google kan vise solen ved siden af
  virksomheden
- `sitemap.xml` med prioritet (forside højest, derefter Praktisk og Kontakt)
- `robots.txt` der holder `kilder/` og `indhold/` ude af søgeresultaterne
- Åbne graf-tags med billede, så et link på Facebook viser fotoet af pigen i
  gyngen frem for en tom hvid boks

**Vigtigt:** alle absolutte URL'er bruger `www.boernegaardengro.dk`. Bliver
domænet et andet, skal `DOMAENE` øverst i `byg.py` rettes, og `python3 byg.py`
køres igen. Så følger canonical, sitemap, JSON-LD og og:image automatisk med.

## Adresse og kort

Adressen er verificeret i DAWA, Danmarks officielle adresseregister
(`api.dataforsyningen.dk`), adresse-id `0a3f50c5-363a-32b8-e044-0003ba298018`:

> **Vinderslevvej 45, Vinderslev, 8620 Kjellerup** · 56,25713 N / 9,43122 Ø

Koordinaterne står i toppen af `byg.py` og bruges af kortudsnittet på
kontaktsiden. Rutevejlednings-knappen sender adressen som søgetekst til Google
Maps, så den ikke kan komme til at pege forkert.

## Princip

Al brødtekst på siden er Jeanettes egen, kun rettet for åbenlyse tastefejl
("boltresig" → "boltre sig", "Mororikopdagelser" → "motorikopdagelser", en sætning
der stod to gange i træk i Om mig). Der er ikke tilføjet eller opdigtet indhold.
Kontrolleret maskinelt: alle 59 nøglepassager fra hendes dokument står på siden.
