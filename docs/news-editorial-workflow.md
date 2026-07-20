# Publikování aktuálních zpráv z Bulharska

## Cíl

Zprávy na Visit Bulharsko nejsou automatický překlad cizích médií. RSS zdroje používáme jen jako podklad pro vlastní český obsah.

Publikujeme pouze zprávy s jasným dopadem na české čtenáře:

- turistické lokality,
- pobřeží a letoviska,
- počasí a bezpečnost,
- letiště, lety a doprava,
- hranice, Schengen, víza a pravidla cestování,
- praktické změny pro návštěvníky Bulharska.

Nepublikujeme běžný politický šum, sport, burzu, obecné zahraniční zprávy ani články bez vazby na cestování.

## Workflow

1. `scripts/fetch_rss_news.py` stáhne titulky a krátké podklady z ověřených RSS zdrojů.
2. Skript vyfiltruje jen zprávy s cestovatelským dopadem.
3. Každá položka je pouze `draft` a obsahuje prompt pro AI přepis vlastními slovy.
4. AI z podkladu vytvoří vlastní český SEO článek.
5. Člověk článek schválí před publikací.
6. Až po schválení jde článek do webu a na GitHub.

## Povinné náležitosti každého článku

Článek není připravený k publikaci, pokud nemá:

- SEO titulek do cca 60 znaků,
- meta description do cca 155 znaků,
- čistý URL slug,
- H1,
- krátký excerpt pro homepage/kategorie,
- vlastní text článku, ideálně 500–800 slov,
- jasný praktický dopad pro cestovatele,
- minimálně 3 FAQ otázky a odpovědi,
- návrh realistického obrázku bez textu,
- SEO alt text obrázku,
- zdrojovou citaci a odkaz na původní zdroj.

## Pravidla přepisu

- Nekopírovat formulace zdroje.
- Nepřekládat větu po větě.
- Nepřebírat celé odstavce.
- Nevyrábět clickbait.
- Pokud zpráva nemá praktický dopad pro cestovatele, označit jako `skip`.
- Zdroj vždy uvést jako podklad, ne jako převzatý text.

## Doporučená struktura článku

```html
<p>Krátký úvod s hlavní informací a dopadem na českého čtenáře.</p>

<h2>Co se stalo</h2>
<p>Vlastní shrnutí situace.</p>

<h2>Koho se to týká</h2>
<p>Dopad na turisty, cestovatele, majitele apartmánů nebo lidi plánující cestu.</p>

<h2>Na co si dát pozor</h2>
<p>Praktické doporučení.</p>

<h2>FAQ</h2>
<h3>Otázka?</h3>
<p>Odpověď.</p>
```
