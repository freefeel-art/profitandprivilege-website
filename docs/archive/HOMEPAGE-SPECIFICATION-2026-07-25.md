# Historical Homepage Specification — Profit and Privilege

> Implemented before archival on 2026-08-04. Status and content-count fields in
> this document are historical design evidence, not current operational state.

# Homepage Specification — Profit and Privilege

**Status:** Draft — awaiting approval
**Version:** 1.1 (revised after structural review)
**Date:** 2026-07-25
**Replaces:** `src/pages/index.astro` (current placeholder: "Website under active development")
**Scope:** Vaihe 1.1 strategisen katselmuksen kehityssuunnitelmasta

---

## 1. Etusivun tarkoitus

Etusivu on sivuston arvokkain sivu. Se on usein ensimmäinen kosketuspiste kävijään — olipa tämä tullut brändihaulla ("profit and privilege"), sosiaalisesta mediasta tai orgaanisesta hausta.

Etusivulla on neljä tehtävää:

1. **Kommunikoida välittömästi, mistä sivustossa on kyse** — kävijän pitää 3 sekunnissa ymmärtää, että tämä on tutkimuspohjainen affiliate-markkinoinnin ja online-tulon sivusto, ei toinen hype-sivu.
2. **Rakentaa luottamusta** — kävijä on todennäköisesti törmännyt kymmeniin "tienaa netissä" -sivuihin. Tämä erottuu metodologialla ja rehellisyydellä.
3. **Ohjata kävijä oikeaan sisältöön hänen tarpeensa mukaan** — aloittelija tarvitsee eri polun kuin OLSP:tä harkitseva tai AI-työkaluja etsivä.
4. **Toimia SEO-sisääntulopisteenä brändihauille** — "profit and privilege", "jarmo halonen", "olsp profit and privilege".

Etusivu **ei ole**:
- Myyntisivu. Se ei tyrkytä affiliate-linkkejä. CTA:t ovat sisäänheittoja sisältöön, eivät tuotteisiin.
- Blogiarkisto. Uusimmat artikkelit näkyvät, mutta etusivu ei ole `blog/index.astro`:n korvike.
- Dashboard. Se ei näytä pipeline-statistiikkaa tai admin-toimintoja.

---

## 2. Kohdeyleisö

| Segmentti | Tarve | Miten etusivu palvelee |
|-----------|-------|------------------------|
| **Aloittelijat** (online-tulo, ei kokemusta) | "Mistä aloitan? Voiko tällä oikeasti tienata?" | Ohjataan Online Income -pilariin, joka on merkitty aloituspisteeksi |
| **OLSP:tä harkitsevat** | "Onko OLSP Academy huijaus? Kannattaako liittyä?" | Ohjataan OLSP Ecosystem -pilariin |
| **Lead generation -ammattilaiset** | "Miten rakennan liidikoneiston?" | Ohjataan Lead Generation -pilariin |
| **Työkaluvertailijat** | "Mikä AI-työkalu on paras? Mikä SEO-työkalu?" | Ohjataan AI Tools -pilariin |
| **Palaavat lukijat** | "Mitä uutta on julkaistu?" | Latest articles -osio |
| **Brändihakijat** | "Onko tämä se Jarmo Halosen sivusto?" | Trust section + author-linkki |
| **Google** | "Mikä tämä sivusto on?" | Schema.org WebSite + Organization |

---

## 3. Käyttäjän kulku (User Journey)

### 3.1 Uusi kävijä ("onko tämä luotettava?")

```
Hero → "Mistä on kyse?" → skannaa pilarit → "Online Income → Best place to start" → sisältöön
```

### 3.2 Tavoitteellinen kävijä ("haluan tietää X:stä")

```
Hero → skannaa pilarit → klikkaa relevanttia pilaria → ohjautuu listing-sivulle → syvälle artikkeliin
```

### 3.3 Palaava kävijä ("mitä uutta?")

```
Hero → skrollaa suoraan Latest Articles -osioon → klikkaa uutta artikkelia
```

### 3.4 SEO-kävijä (brändihaku)

```
Google → etusivu → toteaa sivuston olevan aito → valitsee aiheen
```

---

## 4. Sivun rakenne ylhäältä alas

```
┌─────────────────────────────────────────────────────┐
│ 1. HERO SECTION                                     │
│    Sivuston nimi + arvolupaus (yksi tiivis lause)    │
│    Ei hero-kuvaa — typografinen hero                  │
├─────────────────────────────────────────────────────┤
│ 2. CONTENT PILLARS                                  │
│    5 korttia gridissä:                                │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│    │  OLSP    │ │ Lead Gen │ │★ Online  │           │
│    │Ecosystem │ │          │ │ Income   │           │
│    └──────────┘ └──────────┘ └──────────┘           │
│    ┌──────────┐ ┌──────────┐                        │
│    │Affiliate │ │ AI Tools │                        │
│    │ Traffic  │ │          │                        │
│    └──────────┘ └──────────┘                        │
│    ★ = "Best place to start" -merkintä aloittelijoille│
├─────────────────────────────────────────────────────┤
│ 3. LATEST ARTICLES                                  │
│    Lista 5-6 uusinta artikkelia (git-modifikaatio-   │
│    päivämäärän mukaan), jokaisessa:                   │
│    - Otsikko                                         │
│    - Tyyppibadge (Review / Blog / Roundup)            │
│    - Päivämäärä                                       │
│    - Linkit täysiin listauksiin                       │
├─────────────────────────────────────────────────────┤
│ 4. EDITORIAL TRUST                                  │
│    - Miksi tämä sivusto on erilainen                  │
│    - 3 tiivistä perustelua (1-2 virkettä kukin)        │
│    - GoldMasterQuote (brändisignatuuri)               │
│    - Kirjoittajalinkki                                │
├─────────────────────────────────────────────────────┤
│ 5. FOOTER                                           │
│    SiteFooter-komponentti sellaisenaan                │
└─────────────────────────────────────────────────────┘
```

**Huomio:** Sivustolla ei ole navigaatiopalkkia eikä headeria. Tämä on tietoinen Gold Master -sääntö (§ 16.18: "Do not add a `<header>` or site-wide `<nav>`"). Etusivu kunnioittaa samaa periaatetta — sisältö on navigaatio.

---

## 5. Yksityiskohtainen osiokuvaus

### 5.1 Hero Section

Sivun ainoa `h1` on "Profit & Privilege". Tämä on brändinimi, ei SEO-otsikko. `<title>`-tagi on eri asia (ks. § 9).

**Rakenne:**
```html
<section id="hero">
  <h1>Profit &amp; Privilege</h1>
  <p class="tagline">Research-backed guides on affiliate marketing, lead generation, and online income — built from real community questions, not keyword tools. No hype, no shortcuts.</p>
</section>
```

**Perustelu:**
- Yksi lause kertoo kaiken olennaisen: MITÄ (guides on X, Y, Z), MITEN (built from real community questions), ja MIKÄ ON ERI (not keyword tools, no hype)
- Taglinen pituus on ~30 sanaa — lukijan huomio pysyy, toisin kuin kahdella erillisellä kappaleella
- "No hype, no shortcuts" on WHY.md:n lupaus tiivistettynä — erottautumislause, joka jää mieleen
- Ei hero-kuvaa: meillä ei ole hero-kuva-assettia. Typografinen hero on linjassa sivuston minimalistisen ilmeen kanssa

**CSS:**
- `h1` fonttikoko ~2.4rem (isompi kuin artikkeli-h1:n 1.9rem — etusivu on brändin kasvot)
- `tagline` `font-size: 1.05rem`, `color: var(--ink-light)`, `max-width: 580px`, `line-height: 1.6`
- Osio keskitetty (text-align: center), 4rem padding-top, 2rem padding-bottom

### 5.2 Content Pillars

Viisi pilarikorttia grid-asettelussa. Jokainen kortti on linkki kyseisen pilarin avainsisältöön. Yksi pilareista on merkitty aloituspisteeksi (`startHere: true`) — tämä korostetaan visuaalisesti kortissa.

**Pilarit ja niiden sisältö:**

| Pilari | Otsikko | Kuvaus | Linkki | Artikkelimäärä | Aloituspiste? |
|--------|---------|--------|--------|----------------|---------------|
| OLSP Ecosystem | OLSP Ecosystem | In-depth reviews of every OLSP product, from Academy to Solo Ads | `/reviews/` | 8 | — |
| Lead Generation | Lead Generation | What it is, how it works, and which tools actually deliver leads | `/blog/what-is-lead-generation/` | 11+ | — |
| Online Income for Beginners | Online Income for Beginners | Realistic methods for earning online — no experience required | `/blog/make-money-online-for-beginners/` | 8+ | ★ Best place to start |
| Affiliate Traffic & List Building | Traffic & List Building | Free traffic sources, email list building, and the tools that help | `/blog/best-free-traffic-sources-affiliate-marketing/` | 4 | — |
| AI Tools | AI Tools for Marketers | Independent reviews of AI writing, SEO, video, and chatbot tools | `/reviews/seo-writing-ai-review/` | 6 | — |

**Miten pilaridataa vaihdetaan myöhemmin:** Kaikki pilaritiedot ovat frontmatter-arrayna. Linkin vaihtaminen tarkoittaa `url`-kentän muuttamista. Aloituspisteen vaihtaminen tarkoittaa `startHere`-lipun siirtämistä toiseen objektiin. Pilarien lisääminen tai poistaminen tarkoittaa arrayn muokkaamista. Grid toimii 2–6 kortilla ilman CSS-muutoksia. Tämä on dokumentoitu toteutustiedostossa kommentilla.

**Kortin rakenne (normaali):**
```html
<a href="/reviews/" class="pillar-card">
  <h2>OLSP Ecosystem</h2>
  <p>In-depth reviews of every OLSP product, from Academy to Solo Ads</p>
  <span class="pillar-count">8 articles</span>
</a>
```

**Kortin rakenne (aloituspiste):**
```html
<a href="/blog/make-money-online-for-beginners/" class="pillar-card pillar-start">
  <span class="start-badge">★ Best place to start</span>
  <h2>Online Income for Beginners</h2>
  <p>Realistic methods for earning online — no experience required</p>
  <span class="pillar-count">8+ articles</span>
</a>
```

`pillar-start`-kortti eroaa visuaalisesti: `border-color: var(--accent)`, `background: var(--accent-soft)` oletuksena (ei vain hoverissa). `start-badge` on `font-size: 0.75rem`, `font-weight: 600`, `color: var(--accent)`, `margin-bottom: 0.5rem`. Tämä tekee aloituspisteen kortista visuaalisesti erottuvan ilman, että se huutaa.

**Perustelu pillar-korteille listan sijaan:**
Lista (kuten nykyiset `/blog/` ja `/reviews/` index-sivut) on helppo, mutta se ei auta kävijää, joka ei tiedä mitä etsii. Kortit visuaalisesti ryhmittelevät sisällön teemoittain. Etusivu on ensisijaisesti uusien kävijöiden kartta, ei arkisto.

**Grid-asettelu:**
- Desktop (≥ 900px): `grid-template-columns: repeat(3, 1fr)` — 3 + 2 korttia kahdella rivillä
- Tabletti (600–899px): `grid-template-columns: repeat(2, 1fr)`
- Mobiili (≤ 599px): `grid-template-columns: 1fr`
- `gap: 1.25rem`

**Kortin CSS:**
- `border: 1px solid var(--line)`, `border-radius: var(--radius)`, `padding: 1.3rem`
- `background: var(--bg-soft)` (sama kuin verdict-box)
- `text-decoration: none`, `color: var(--ink)` — koko kortti on `<a>`, hoverissa `box-shadow` tai `border-color: var(--accent)`
- `pillar-card h2`: `font-size: 1.1rem`, `margin: 0 0 0.4rem`, `color: var(--accent)` — pilarin nimi aksenttivärillä
- `pillar-card p`: `font-size: 0.9rem`, `color: var(--ink-light)`, `margin: 0 0 0.6rem`
- `pillar-count`: `font-size: 0.78rem`, `color: var(--ink-light)`, `letter-spacing: 0.04em`, `text-transform: uppercase`
- Hover: `border-color: var(--accent)`, `background: var(--accent-soft)` (hienovarainen, ei rajua)

**Perustelu:**
- 5 korttia on sopiva määrä — ei liikaa kognitiivista kuormaa
- 3+2 -grid on visuaalisesti miellyttävämpi kuin 2+2+1 tai 5 rivissä
- Kokonaiset kortit linkkeinä maksimoivat klikkausalueen (Fitts's Law)
- Artikkelimäärä kertoo kävijälle, että kyseessä on kattava sivusto, ei pintaraapaisu

### 5.3 Latest Articles

Lista 5–6 uusimmasta artikkelista, sorteerattu `git log` -muokkauspäivämäärän mukaan (laskeva). Data tulee `src/data/production-home.js`:n `getPublishedArticles()`-funktiosta.

**Miksi 5–6 eikä kaikki?**
- Etusivu ei ole arkisto. `blog/index.astro` ja `reviews/index.astro` hoitavat täydelliset listat.
- 5–6 on tarpeeksi, jotta palaava kävijä näkee uusimman sisällön, mutta ei niin paljon, että etusivu muuttuu loputtomaksi scrolliksi.
- Parillisempi kuin 6–8 — tiiviimpi etusivu latautuu nopeammin ja pitää fokuksen.

**Rakenne:**
```html
<section id="latest">
  <h2 class="section-title">Latest Articles</h2>
  <ol class="latest-list">
    <li class="latest-item">
      <span class="latest-type">Review</span>
      <a href="/reviews/semrush-review/">Semrush Review: An Independent, Research-Based Analysis</a>
      <time datetime="2026-07-12">July 12, 2026</time>
    </li>
    <!-- ... -->
  </ol>
  <p class="browse-all">
    <a href="/blog/">Browse all articles →</a> &nbsp;·&nbsp; <a href="/reviews/">All reviews →</a>
  </p>
</section>
```

**CSS:**
- `latest-list`: `list-style: none`, `padding: 0`, `margin: 0`
- `latest-item`: `display: flex`, `align-items: baseline`, `gap: 0.8rem`, `padding: 0.55rem 0`, `border-bottom: 1px solid var(--line)`, `flex-wrap: wrap`
- `latest-type`: `flex-shrink: 0`, `font-size: 0.72rem`, `font-weight: 600`, `text-transform: uppercase`, `letter-spacing: 0.05em`, `color: var(--ink-light)`, `background: var(--bg-soft)`, `border: 1px solid var(--line)`, `border-radius: 4px`, `padding: 0.15rem 0.45rem` — pieni tyyppibadge, ei huomiota varastava
- `latest-item a`: `flex: 1`, `font-size: 0.92rem`, `color: var(--accent)`, `text-decoration: none`, `min-width: 200px`
- `latest-item a:hover`: `text-decoration: underline`
- `latest-item time`: `flex-shrink: 0`, `font-size: 0.78rem`, `color: var(--ink-light)`
- `browse-all`: `margin-top: 1rem`, `font-size: 0.88rem`

**Perustelu flex-asettelulle:**
- Kolme elementtiä (tyyppi, otsikko, päiväys) vaakasuorassa rivissä on nopea silmäillä
- Type-badge auttaa erottamaan review't, blogit ja roundupit toisistaan
- Date kertoo tuoreuden — palaava kävijä näkee heti, onko uutta
- Päiväys perustuu git-modifikaatioon, ei manuaaliseen date-kenttään — tämä on aina ajantasalla

**Data-lähde:**
`getPublishedArticles()` palauttaa `{ title, type, url, lastModified }[]` — täsmälleen tarvittavat kentät. Funktio on jo olemassa ja testattu tuotannossa.

### 5.4 Editorial Trust

Tämä osio korvaa sen luottamuksen, jonka artikkelisivuilla tuottavat Methodology-komponentti ja AuthorBox. Kolme lyhyttä perustelua yhdessä rivissä — ytimekäs, ei pitkää tekstiä.

**Rakenne:**
```html
<section id="trust">
  <h2 class="section-title">Why Trust This Site</h2>
  <div class="trust-grid">
    <div class="trust-item">
      <h3>Research, Not Assumptions</h3>
      <p>Every claim is verified. Vendor claims, self-reported figures, and confirmed facts are clearly distinguished.</p>
    </div>
    <div class="trust-item">
      <h3>Community-Driven Topics</h3>
      <p>We start where real people discuss their problems — Reddit, Quora, forums — not in a keyword tool.</p>
    </div>
    <div class="trust-item">
      <h3>Independent & Honest</h3>
      <p>We earn affiliate commissions, but editorial decisions are never driven by them. We tell you what's wrong, not just what's right.</p>
    </div>
  </div>

  <!-- GoldMasterQuote: brändisignatuuri -->
  <a href="https://olspacademy.com/megalive/1006001" class="goldmaster-quote" target="_blank" rel="noopener noreferrer">&ldquo;Brand New Live Training &mdash; Limited Spaces&rdquo;</a>

  <p class="author-link">
    All articles are written by <a href="/authors/jarmo-halonen/">Jarmo Halonen</a>, founder of Profit and Privilege.
  </p>
</section>
```

**Perustelu:**
- Kolme lyhyttä kohtaa kolmessa kortissa on helposti silmäiltävissä — ei pitkää tekstiä
- Sisältö tulee WHY.md:stä: "Research Before Opinion", "Community First", "Independent & Honest"
- GoldMasterQuote on brändin signatuurielementti — sen läsnäolo etusivulla yhdistää etusivun visuaalisesti artikkeleihin
- GoldMasterQuote käyttää `rel="noopener noreferrer"` (ei `sponsored`) — tämä on editoriaalinen luottamussignaali, ei mainos
- Author-linkki ohjaa kirjoittajaprofiiliin — siellä on täysi CV ja kuvaus

**CSS:**
- `trust-grid`: `display: grid`, `grid-template-columns: repeat(3, 1fr)`, `gap: 1.25rem`
- `trust-item`: `padding: 1.2rem`, `border: 1px solid var(--line)`, `border-radius: var(--radius)`, `background: var(--bg)`
- `trust-item h3`: `font-size: 0.95rem`, `color: var(--accent)`, `margin: 0 0 0.4rem`
- `trust-item p`: `font-size: 0.85rem`, `color: var(--ink-light)`, `margin: 0`, `line-height: 1.55`
- `goldmaster-quote`: kopioidaan OlspLayoutin CSS — `display: block`, `text-align: center`, `margin: 3rem 0`, `font-size: 1.15rem`, `font-weight: 600`, `font-style: italic`, `line-height: 1.6`, `color: var(--ink)`, `text-decoration: none`
- `author-link`: `text-align: center`, `font-size: 0.9rem`, `color: var(--ink-light)`

**Mobiili:** Trust-grid tiivistyy kahteen ja sitten yhteen sarakkeeseen.

### 5.5 Footer

`<SiteFooter />`-komponentti sellaisenaan — ei muutoksia. Komponentti importataan suoraan `src/components/olsp-standard/SiteFooter.astro`:sta.

**Huomio BLOG-MASTER-SPEC.md § 8a:n väliaikaisesta footer-linkistä:** Blogiartikkeleissa SiteFooter-linkki on tilapäisesti vaihdettu affiliate-osoitteeseen, kunnes etusivu on valmis. Etusivun valmistuttua footeriin palautetaan alkuperäinen linkki (`https://olsp.profitandprivilege.com`). Tämä tehdään erillisenä työnä (Vaihe 1.3 `publish.cjs`:n URL-korjauksen yhteydessä). Etusivun footer käyttää jo valmista `SiteFooter.astro`-komponenttia.

---

## 6. Mitä nykyistä sisältöä hyödynnetään

### 6.1 Data-lähteet

| Lähde | Kuvaus | Käyttö etusivulla |
|-------|--------|-------------------|
| `src/data/production-home.js` — `getPublishedArticles()` | Palauttaa kaikki julkaistut artikkelit otsikolla, tyypillä, URL:llä ja päivämäärällä | Latest Articles -osion datana |
| `docs/CONTENT-REGISTRY.md` | Manuaalinen rekisteri artikkeleista ja pilareista | Pillar-korttien artikkelimäärien lähde (kovakoodattu) |
| `docs/WHY.md` | Toimituksellinen manifesti | Trust-osion copy-tekstin pohja |
| `src/components/olsp-standard/GoldMasterQuote.astro` | Brändisignatuurilainaus | Trust-osiossa sellaisenaan (import) |
| `src/components/olsp-standard/SiteFooter.astro` | Brand-footer | Footerissa sellaisenaan (import) |

**Huomio:** `getPublishedArticles()` palauttaa tiedot `.astro`-tiedostoista lukemalla `const pageTitle` -muuttujan, `title=""`-attribuutin tai `<h1>`-sisällön. Tämä toimii luotettavasti, koska artikkelien tuotantostandardi takaa näiden olemassaolon.

### 6.2 Kovakoodattu sisältö

| Sisältö | Lähde / Perustelu |
|---------|-------------------|
| Hero-tagline | WHY.md:n hengessä kirjoitettu — ei kopioitu suoraan |
| Pillar-kuvaukset | CONTENT-REGISTRY:n pilarikuvausten pohjalta |
| Pillar-linkkikohteet | Editoriaalinen valinta — ks. § 5.2 taulukko |
| Trust-osion tekstit | WHY.md:n avainkohdista |
| Artikkelimäärät | CONTENT-REGISTRY:stä tarkistettuna |

### 6.3 Miten 44 julkaistua artikkelia tuodaan näkyville

Kolmella tavalla:

1. **Pillar-kortit** (5 kpl): jokainen kortti ohjaa pilarin sisältöön. Kortissa näkyy artikkelimäärä ("8 articles"), mikä viestii syvyydestä. Yksi kortti on merkitty aloituspisteeksi uusille kävijöille.
2. **Latest Articles** (5–6 kpl): kronologinen lista uusimmasta sisällöstä.
3. **Trust-osio**: viestii sisällön laadusta ja metodologiasta — epäsuorasti esittelee koko sivuston laajuuden.

Nämä kolme mekanismia yhdessä varmistavat, että:
- Selailija löytää nopeasti oikean pilarin
- Uusi kävijä saa ohjatun aloituspolun
- Palaava kävijä näkee uusimman sisällön

Artikkeleita **ei** listata kerralla kaikkia — se on listing-sivujen (`/blog/`, `/reviews/`) tehtävä.

---

## 7. CTA-strategia

### 7.1 Ensisijaiset CTA:t (sisäänheitto sisältöön)

Nämä eivät ole perinteisiä "osta nyt" -painikkeita, vaan navigaatioelementtejä, jotka ohjaavat kävijän ongelmansa äärelle:

| CTA | Tyyppi | Kohde |
|-----|--------|-------|
| Pillar-kortit (5 kpl) | Navigaatio | Listing-sivut / avainartikkelit |
| "Browse all articles" -linkit | Navigaatio | `/blog/` ja `/reviews/` |

Huomioarvo: `target="_blank"` tai `rel`-attribuutteja **ei** käytetä — kaikki nämä ovat sisäisiä linkkejä, jotka avautuvat samassa ikkunassa.

### 7.2 Toissijainen CTA (brändisignatuuri)

GoldMasterQuote on ainoa ulkoinen linkki etusivulla. Se käyttää `target="_blank" rel="noopener noreferrer"` (ei `sponsored`). Se ei ole myynti-CTA — se on osa sivuston editoriaalista identiteettiä, aivan kuten artikkeleissakin.

### 7.3 Mitä etusivulla EI ole

- Ei "Join Now" / "Sign Up" -painikkeita (nämä kuuluvat tuotesivuille, eivät etusivulle)
- Ei pop-up -modaaleja
- Ei sähköpostikeräyslomaketta (tämä tulee Vaiheessa 4.1 — erillinen suunnitelma)
- Ei affiliate-linkkejä (ainoa affiliate-linkki on GoldMasterQuote, ja sekin on merkitty `noopener noreferrer` eikä `sponsored`)

**Perustelu:** Etusivun tehtävä on rakentaa luottamusta ja ohjata sisältöön. Affiliate-konversio tapahtuu artikkeleissa, joissa tuote on ansaittu kontekstilla.

---

## 8. Sisäisen linkityksen strategia

### 8.1 Linkit etusivulta ulos

| Linkki | Tyyppi | Perustelu |
|--------|--------|-----------|
| 5 × pillar-kortit | Sisäinen | Pääasiallinen navigaatio |
| 5–6 × latest articles | Sisäinen | Tuorein sisältö |
| 1 × GoldMasterQuote | Ulkoinen (affiliate, `noopener noreferrer`) | Brändisignatuuri |
| 1 × author-linkki | Sisäinen | `/authors/jarmo-halonen/` |
| 1 × "Browse all articles" | Sisäinen | `/blog/` |
| 1 × "All reviews" | Sisäinen | `/reviews/` |
| 1 × SiteFooter-linkki | Sisäinen | `/` (tai väliaikainen affiliate-URL) |

Yhteensä ~16 linkkiä, joista vain 1 on ulkoinen. Etusivu on vahva sisäisen linkityksen solmukohta.

### 8.2 Linkit etusivulle (CONTENT-REGISTRY-päivitys)

Nykyisellään CONTENT-REGISTRY:ssä etusivulla ei ole lainkaan inbound-linkkejä (kenttä tyhjä). Etusivun valmistuttua:
- SiteFooter linkittää etusivulle jokaiselta sivulta (kun väliaikainen affiliate-linkki palautetaan)
- Etusivu lisätään sisäisen linkityksen solmukohdaksi Internal Link Map -kaavioon

Tämä päivitetään CONTENT-REGISTRY.md:hen Vaiheessa 1.1.

### 8.3 Sisäinen linkkirakenne etusivun kautta

```
etusivu
  ├── OLSP Ecosystem → /reviews/
  │   ├── OLSP Academy review
  │   ├── OLSP Community Builders
  │   ├── OLSP Live Profit Builders
  │   ├── OLSP MineeMe
  │   ├── OLSP Solo Ads
  │   ├── Megalink Traffic Rotator
  │   ├── OLSP Academy Complete Guide
  │   └── Is OLSP Academy an MLM?
  ├── Lead Generation → /blog/what-is-lead-generation/
  │   └── 11+ artikkelia
  ├── Online Income → /blog/make-money-online-for-beginners/
  │   └── 8+ artikkelia
  ├── Traffic & List Building → /blog/best-free-traffic-sources-affiliate-marketing/
  │   └── 4 artikkelia
  └── AI Tools → /reviews/seo-writing-ai-review/
      └── 6 artikkelia
```

---

## 9. SEO-huomiot

### 9.1 Title-tagi

```
Profit & Privilege — Independent Research on Affiliate Marketing & Online Income
```

**Perustelu:**
- Brändinimi ensin (brändihaut)
- Avainsanat "affiliate marketing" ja "online income" kuvaavat sivuston ydinaiheita
- "Independent Research" erottautuu ja houkuttelee klikkaamaan SERP:ssä
- Pituus ~80 merkkiä — mahtuu hyvin hakutuloksiin

### 9.2 Meta Description

```
Independent, research-backed reviews and guides on affiliate marketing, lead generation, and online income. Every article puts evidence before opinion — no hype, no shortcuts.
```

**Perustelu:**
- ~155 merkkiä — optimaalinen pituus
- Sisältää avainsanat: "reviews", "affiliate marketing", "lead generation", "online income"
- "No hype, no shortcuts" — erottautumislupaus, joka viestii laatua

### 9.3 Canonical URL

```
https://olsp.profitandprivilege.com/
```

Trailing slash — kuten kaikki sivuston URL:t.

### 9.4 Schema.org

Etusivulle lisätään kaksi skeematyyppiä:

1. **`WebSite`** — hakutoiminnallisuudella (vaikka sivustolla ei ole omaa hakua, SearchAction on standardi):
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "name": "Profit and Privilege",
      "url": "https://olsp.profitandprivilege.com",
      "description": "Independent, research-backed reviews and guides on affiliate marketing, lead generation, and online income.",
      "author": {
        "@type": "Person",
        "name": "Jarmo Halonen",
        "url": "https://olsp.profitandprivilege.com/authors/jarmo-halonen"
      }
    },
    {
      "@type": "Organization",
      "name": "Profit and Privilege",
      "url": "https://olsp.profitandprivilege.com"
    }
  ]
}
```

**Perustelu:**
- `WebSite` + `Organization` on standardi yhdistelmä brändisivuston etusivulle
- Ei `Article`- tai `Review`-skeemaa — etusivu ei ole artikkeli
- Google käyttää WebSite-skeemaa sivuston brändäyksen ymmärtämiseen

### 9.5 Open Graph / Twitter Cards

```html
<meta property="og:title" content="Profit & Privilege — Independent Research on Affiliate Marketing & Online Income" />
<meta property="og:description" content="Research-backed reviews and guides on affiliate marketing, lead generation, and online income." />
<meta property="og:url" content="https://olsp.profitandprivilege.com/" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Profit and Privilege" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Profit & Privilege — Independent Research on Affiliate Marketing & Online Income" />
<meta name="twitter:description" content="Research-backed reviews and guides on affiliate marketing, lead generation, and online income." />
```

**Huomio:** `og:type` on `website` (ei `article`). `og:image` jätetään pois — meillä ei ole hero-kuvaa, eikä ole järkevää keksiä sellaista pelkästään OG-tagia varten. Favicon hoitaa visuaalisen tunnisteen sosiaalisissa jaoissa.

### 9.6 Robots

```html
<meta name="robots" content="index, follow" />
```

Sama kuin kaikilla muillakin sivuilla.

---

## 10. Mobiilikäytettävyys

### 10.1 Breakpointit

Käytetään Gold Masterin 900px breakpointin lisäksi 600px välibreakpointtia pilarigridille:

| Breakpoint | Pilarigrid | Trust-grid | Hero-fontti |
|------------|-----------|------------|-------------|
| ≥ 900px | 3 kolumnia | 3 kolumnia | h1: 2.4rem |
| 600–899px | 2 kolumnia | 2 kolumnia | h1: 2rem |
| ≤ 599px | 1 kolumni | 1 kolumni | h1: 1.8rem |

### 10.2 Latest Articles mobiilissa

Flex-asettelu tiivistyy:
- `flex-wrap: wrap` mahdollistaa type-badgen, otsikon ja päivämäärän rivittymisen
- Mobiilissa otsikko saa koko rivin ja badge + päiväys jäävät ylä-/alariville

### 10.3 Kosketuskohteet

- Pillar-kortit: koko kortti on `<a>` — helppo napauttaa (min 44×44px kosketuspinta-ala)
- Latest-article -linkit: normaali tekstilinkki, riittävä rivikorkeus (1.65)
- Ei hover-riippuvaisia interaktioita (mobiilissa hover ei toimi)

### 10.4 Sivulataus

- Ei kuvia (paitsi favicon) — nopea lataus
- CSS on minimaalinen (~200-300 riviä inline-tyylejä)
- JS ei ole lainkaan (etusivu ei tarvitse scroll-spytä, TOC-togglea tai quiz-logiikkaa)
- Staattinen HTML, build-aikainen datanhaku — ei runtime-riippuvuuksia

**Core Web Vitals -odotus:** LCP < 1.5s, CLS = 0, INP = n/a (ei interaktiivisia elementtejä käyttäjän syötteisiin).

---

## 11. Mitä uusia komponentteja tarvitaan

### 11.1 Uudet komponentit: ei yhtään

Etusivu kirjoitetaan itsekantavana `.astro`-tiedostona, joka ei vaadi uusia jaettavia komponentteja. Kaikki tarvittava rakenne (pillar-kortit, latest-listaus, trust-osio) on etusivulle spesifistä eikä toistu muualla.

**Perustelu:**
- Gold Master -komponentit (13 kpl) on suunniteltu **artikkeleita** varten, ei infrastruktuurisivuja varten
- Etusivun rakenne ei toistu missään muualla — komponentin tekeminen yhdestä käyttökerrasta on ennenaikaista abstrahointia
- `production-home.js` tarjoaa jo datafunktion — uutta komponenttia ei tarvita datan hakemiseen

### 11.2 Mahdolliset tulevaisuuden komponentit

Jos myöhemmin luodaan pilarisivuja (Vaihe 4.2), pillar-korttien rakenne voidaan silloin eriyttää komponentiksi. Tämä on kuitenkin Vaiheen 4 asia, ei Vaiheen 1.

---

## 12. Mitä olemassa olevia komponentteja hyödynnetään sellaisenaan

| Komponentti | Tiedosto | Käyttö | Muutokset? |
|-------------|----------|--------|------------|
| **SiteFooter** | `src/components/olsp-standard/SiteFooter.astro` | Footer-osio | Ei muutoksia — import sellaisenaan |
| **GoldMasterQuote** | `src/components/olsp-standard/GoldMasterQuote.astro` | Trust-osio | Ei muutoksia — import sellaisenaan |
| **production-home.js** | `src/data/production-home.js` | Latest Articles -data | Ei muutoksia — `getPublishedArticles()` sellaisenaan |

**Mitä EI hyödynnetä:**

| Komponentti | Syy |
|-------------|-----|
| **OlspLayout** | Sisältää TOC-sivupalkin, mobiili-TOC:n, quiz-funktion — kaikki tarpeettomia etusivulla. Layout on suunniteltu pitkille artikkeleille. |
| **Layout.astro** (vanha) | Käyttää vanhaa kultaista design-järjestelmää (`--accent: #b8862b`), joka on ristiriidassa Gold Masterin sinisen kanssa. |
| **AuthorBox** | Liian suuri etusivulle — pelkkä linkki kirjoittajaprofiiliin riittää. |
| **HeroTag** | Artikkeleiden kategorianappi — ei relevantti etusivulla. |
| **VerdictBox, Methodology, Callout, ProductCta, FaqItem, PillList, ScoreBar, QuizBox** | Artikkelispesifejä komponentteja — eivät kuulu etusivulle. |

### 12.1 Design-tokenit

Vaikka OlspLayoutia ei käytetä, sen CSS-tokenit kopioidaan etusivun `<style>`-blokkiin. Tämä varmistaa visuaalisen yhdenmukaisuuden artikkeleiden kanssa:

```css
:root {
  --ink: #1e293b;
  --ink-light: #475569;
  --bg: #ffffff;
  --bg-soft: #f8fafc;
  --line: #e2e8f0;
  --accent: #2563eb;
  --accent-soft: #eff6ff;
  --radius: 10px;
}
```

Perusresetit (`box-sizing`, body-fontti, linkkityylit) kopioidaan samoin.

---

## 13. Tekninen toteutussuunnitelma

### 13.1 Tiedostorakenne

```
src/pages/index.astro    ← Yksi itsekantava .astro-tiedosto
                            (korvaa nykyisen placeholderin)
```

Ei uusia tiedostoja. Etusivu ei tarvitse erillistä layoutia — OlspLayout on artikkeleille, `Layout.astro` on vanhentunut.

### 13.2 Frontmatter

```astro
---
export const prerender = true;

import SiteFooter from "../components/olsp-standard/SiteFooter.astro";
import GoldMasterQuote from "../components/olsp-standard/GoldMasterQuote.astro";
import { getPublishedArticles } from "../data/production-home.js";

const published = getPublishedArticles().slice(0, 6);

// Pillar data — muokkaa URL, description, count tai startHere muuttaaksesi etusivun sisältöä.
// startHere-flag merkitsee yhden kortin visuaalisesti aloituspisteeksi. Vaihda lippu toiseen
// objektiin, jos aloituspiste halutaan vaihtaa. Array tukee 2–6 korttia ilman CSS-muutoksia.
const pillars = [
  {
    name: "OLSP Ecosystem",
    description: "In-depth reviews of every OLSP product, from Academy to Solo Ads",
    url: "/reviews/",
    count: 8,
  },
  {
    name: "Lead Generation",
    description: "What it is, how it works, and which tools actually deliver leads",
    url: "/blog/what-is-lead-generation/",
    count: 11,
  },
  {
    name: "Online Income for Beginners",
    description: "Realistic methods for earning online — no experience required",
    url: "/blog/make-money-online-for-beginners/",
    count: 8,
    startHere: true,
  },
  {
    name: "Traffic & List Building",
    description: "Free traffic sources, email list building, and the tools that help",
    url: "/blog/best-free-traffic-sources-affiliate-marketing/",
    count: 4,
  },
  {
    name: "AI Tools for Marketers",
    description: "Independent reviews of AI writing, SEO, video, and chatbot tools",
    url: "/reviews/seo-writing-ai-review/",
    count: 6,
  },
];
---
```

### 13.3 Template-rakenne

```astro
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- meta, title, description, canonical, OG, Twitter, JSON-LD -->
</head>
<body>

<main>
  <!-- 1. Hero -->
  <section id="hero">...</section>

  <!-- 2. Content Pillars (one with startHere badge) -->
  <section id="pillars">...</section>

  <!-- 3. Latest Articles -->
  <section id="latest">...</section>

  <!-- 4. Editorial Trust -->
  <section id="trust">...</section>

  <!-- 5. Footer -->
  <SiteFooter />
</main>

</body>
</html>
```

### 13.4 Riippuvuudet

- **`production-home.js`** — `getPublishedArticles()` hakee git-lokin kautta muokkauspäivämäärät. Tämä vaatii, että `git` on saatavilla build-ympäristössä (Cloudflare Pagesissa on).
- **`SiteFooter.astro`** — staattinen komponentti, ei riippuvuuksia
- **`GoldMasterQuote.astro`** — staattinen komponentti, ei riippuvuuksia

Ei uusia npm-paketteja, ei uusia konfiguraatiotiedostoja, ei muutoksia `astro.config.mjs`:ään.

### 13.5 Mitä poistuu

Nykyinen `src/pages/index.astro` (10 riviä) korvataan kokonaan. Vanha `Layout.astro` jää ennalleen — sitä käyttää yhä `production.astro` (joka korjataan erikseen Vaiheessa 1.2).

---

## 14. Hyväksymiskriteerit

Ennen kuin etusivu katsotaan valmiiksi, seuraavien ehtojen on täytyttävä:

- [ ] `astro build` menee läpi puhtaasti (ei virheitä, ei varoituksia)
- [ ] `astro dev` palauttaa HTTP 200 osoitteesta `/`
- [ ] Etusivun HTML sisältää kaikki viisi osiota (hero, pillars, latest, trust + footer)
- [ ] Pilarikortit linkittävät oikeille sivuille
- [ ] Online Income -pilariin on merkitty `startHere` ja se erottuu visuaalisesti muista korteista
- [ ] Latest Articles -lista sisältää 5–6 artikkelia ja jokaisella on toimiva linkki
- [ ] GoldMasterQuote ja SiteFooter renderöityvät oikein komponenteista
- [ ] Design-tokenit vastaavat Gold Master -spesifikaatiota (sininen aksentti, valkoinen tausta)
- [ ] Mobiilissa pilarigrid tiivistyy responsiivisesti
- [ ] `<title>` ja `<meta name="description">` sisältävät tarkoituksenmukaiset avainsanat
- [ ] JSON-LD sisältää `WebSite`- ja `Organization` -skeemat
- [ ] Open Graph / Twitter Card -tagit ovat paikallaan
- [ ] Sivustolla ei ole `<header>`- tai `<nav>`-elementtejä
- [ ] Sisäiset linkit eivät käytä `target="_blank"`-attribuuttia
- [ ] GoldMasterQuote käyttää `rel="noopener noreferrer"` (ei `sponsored`)

---

## 15. Riskit ja rajaukset

### 15.1 Tietoiset rajaukset (mitä EI tehdä tässä vaiheessa)

| Rajaus | Perustelu |
|--------|-----------|
| Ei hero-kuvaa | Meillä ei ole sopivaa assettia. Typografinen hero on brändin mukainen. |
| Ei navigaatiopalkkia | Gold Master -sääntö kieltää `<header>`/`<nav>`:n. Sisältö toimii navigaationa. |
| Ei sähköpostikeräystä | Kuuluu Vaiheeseen 4.1 — erillinen suunnitelma liidimagneetille. |
| Ei "popular" / "trending" -osiota | Ei analytiikkadataa suosion määrittämiseen. Pillar-kortit ja startHere-badge hoitavat ohjauksen. |
| Ei animaatioita | Staattinen sivu latautuu nopeammin ja on saavutettavampi. |
| Ei uusia komponentteja `olsp-standard/`:iin | Etusivun rakenne on uniikki — komponentti yhdelle sivulle on ennenaikaista abstrahointia. |
| Ei muutoksia artikkeleihin | Etusivu on itsenäinen sivu — artikkelit eivät muutu. |
| Ei footer-linkin korjausta | Kuuluu Vaiheeseen 1.3 yhdessä `publish.cjs`:n korjauksen kanssa. |

### 15.2 Riskit

| Riski | Todennäköisyys | Vaikutus | Lievennys |
|-------|---------------|----------|-----------|
| `getPublishedArticles()` epäonnistuu Cloudflare-buildissa | Matala | Latest Articles -osio tyhjä | `git` on saatavilla Cloudflare Pagesissa; funktio on jo testattu tuotannossa |
| Artikkelimäärät menevät vanhaksi | Keskitaso | Virheellinen tieto kävijälle | CONTENT-REGISTRY päivitetään jokaisen uuden artikkelin yhteydessä (standardi) |
| Uusi design ei tunnu yhtenäiseltä artikkeleiden kanssa | Matala | Visuaalinen epäjohdonmukaisuus | Samat CSS-tokenit, sama fontti, sama väripaletti — vain layout on eri |
| Etusivun SEO kannibalisoi artikkelien SEO:ta | Erittäin matala | Artikkelien sijoitus laskee | Etusivu kohdistuu brändihakuihin, ei avainsanoihin. Artikkelit kohdistuvat pitkän hännän avainsanoihin. |

---

## 16. Yhteenveto perusteluista

**Miksi tämä malli eikä jokin muu?**

1. **Ei OlspLayoutia** — TOC-sivupalkki on suunniteltu artikkelinavigaatioon. Etusivulla se veisi 280px turhaa tilaa ja hämmentäisi kävijää.

2. **Pilarikortit, ei listausta** — Uusi kävijä ei tiedä mitä etsiä. Kortit ryhmittelevät sisällön visuaalisesti teemoittain ja toimivat karttana.

3. **Pilarikortit ja startHere-badge, ei erillistä Featured-osiota** — Featured-nostojen intentio ("mistä aloitan?") on päällekkäinen pilarikorttien kanssa. Online Income -pilarikortti on merkitty aloituspisteeksi (`startHere`), mikä ohjaa uudet kävijät ilman ylimääräistä osiota. Pilaridata on helposti muokattavissa oleva array frontmatterissa.

4. **Vain yksi ulkoinen linkki** — GoldMasterQuote. Etusivun tehtävä on rakentaa luottamusta, ei myydä. Myynti tapahtuu artikkeleissa, joissa tuotteella on konteksti.

5. **Ei uusia komponentteja** — Kaikki etusivun tarvitsema on joko jo olemassa (SiteFooter, GoldMasterQuote, production-home.js) tai kirjoitetaan suoraan etusivulle. Tämä pitää muutoksen pienenä ja vähentää regressioriskiä.

6. **Build-aikainen datanhaku, ei runtime** — `getPublishedArticles()` ajetaan buildin aikana, ei selaimessa. Etusivu pysyy staattisena HTML:nä, kuten kaikki muutkin sivut.

---

> **Seuraava askel:** Tämän spesifikaation hyväksymisen jälkeen toteutetaan `src/pages/index.astro`. Tämän jälkeen Vaihe 1.2 (`production.astro`:n korjaus) ja Vaihe 1.3 (`publish.cjs`:n URL-korjaus ja footer-linkin palautus).
