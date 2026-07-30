# Visit Bulharsko – předlaunch audit

Datum: 2026-07-29
Cílová doména pro build: `https://visitbulharsko.cz`
Build command: `SITE_URL=https://visitbulharsko.cz BASE_PATH=/ npm run build`

## Executive summary

Web je po dnešních opravách technicky výrazně blíž k live spuštění. Původní audit našel kritický launch blocker: při Windows/Git Bash buildu se generovaly rozbité interní URL typu `/C:/Program Files/Git/...`. To by na produkční doméně rozbilo CSS, obrázky, canonicaly a interní odkazy. Opraveno lokálně.

Aktuální build:

- 138 statických stránek
- Astro check: 0 errors, 0 warnings, 0 hints
- broken Windows URL v HTML: 0
- robots.txt: OK
- sitemap.xml: OK
- canonicaly: míří na `https://visitbulharsko.cz/`
- homepage H1: OK
- články: Article + BreadcrumbList schema: OK
- homepage: WebSite + Organization schema: OK
- Twitter cards: OK
- OG image: absolutní URL na doméně: OK

## Co jsem lokálně opravil

Soubory:

- `astro.config.mjs`
- `src/utils/paths.ts`
- `src/layouts/BaseLayout.astro`
- `src/pages/index.astro`
- `src/pages/[slug]/index.astro`

Opravy:

1. Normalizace `BASE_PATH=/` pro Windows/Git Bash build, aby se z `/` nestalo `C:/Program Files/Git/`.
2. Canonical URL a asset URL se generují bezpečně pro cílovou doménu.
3. Doplněny Twitter meta tagy.
4. Doplněny OG url/type/site_name a absolutní OG image.
5. Homepage dostala jeden H1 přes `sr-only`.
6. Homepage dostala `WebSite` + `Organization` schema.
7. Články dostaly `Article` + `BreadcrumbList` schema.
8. Články používají `og:type=article`.

## Rychlost / výkon

Lokální statický server:

- `/`: HTTP 200, cca 51 kB HTML
- `/nemovitosti-bulharsko/`: HTTP 200, cca 35 kB HTML
- `/category/zpravy-bulharsko/`: HTTP 200, cca 110 kB HTML
- `/sitemap.xml`: HTTP 200, cca 12 kB
- `/robots.txt`: HTTP 200

Hlavní riziko rychlosti nejsou Astro šablony, ale assety:

- assetů celkem: 304
- assety celkem: cca 98.64 MB
- největší asset: `uploads/2025/01/Objevte-skvele-ceny-optimized.webp` – cca 6.8 MB
- další velké PNG/JPG obrázky: cca 1.5–2.8 MB za kus

Doporučení před/po live:

- nepouštět těžký GIF do kritických šablon,
- největší PNG/JPG převést na WebP/AVIF a ideálně max 250–350 kB,
- pro historické starší články optimalizovat postupně; pro launch hlavně homepage, hlavní kategorie a top články.

## SEO audit

Po opravách zmizelo:

- chybějící Twitter cards: původně 138 stránek, nyní 0
- chybějící Article schema u článků: původně 133, nyní 0 u běžných článků
- broken canonical/asset URLs: nyní 0
- homepage bez H1: opraveno

Zůstává jako nižší priorita:

- 81× krátká meta description
- 14× dlouhá meta description
- 12× dlouhý title
- několik stránek s více H1 / missing alt, hlavně `nemovitosti-bulharsko`, `o-nas`, `kontakt`
- jedna thin category page: `/category/cestovni-pruvodce/` cca 296 slov

Tohle nejsou launch blockery, ale stojí za následnou úpravu.

## AI SEO / LLM SEO audit

Silné stránky:

- strukturovaná data pro články po opravě: Article + BreadcrumbList
- homepage: WebSite + Organization
- jasná topical mapa: zprávy, destinace, historie, kultura, tipy, nemovitosti
- mnoho long-tail cestovatelských článků
- statický HTML obsah je dobře čitelný i bez JavaScriptu

Slabiny:

- část starších článků má generické / krátké popisy,
- některé URL obsahují emoji nebo cyrilici v procentech,
- starší články mohou působit jako AI/news šum bez jasného praktického dopadu,
- newsletter formuláře jsou zatím statické a nikam neukládají kontakty,
- chybí `llms.txt` / AI summary stránka pro lepší orientaci LLM crawlerů.

Doporučení pro AI SEO:

1. Přidat `/llms.txt` s přehledem webu, hlavních sekcí a top URL.
2. Přidat „O webu / redakční pravidla“ s jasným autorstvím a účelem webu.
3. U money stránek a top průvodců doplnit FAQ schema tam, kde dává smysl.
4. Sjednotit staré RSS/news články: ponechat jen ty s cestovatelským dopadem, slabé noindex/archivovat.

## Technická připravenost na přenos domény

Aktuální stav po opravě:

- build na `SITE_URL=https://visitbulharsko.cz BASE_PATH=/` funguje
- canonicaly míří na doménu, ne na GitHub Pages
- robots.txt ukazuje sitemap na doméně
- sitemap.xml generuje URL na doméně
- interní odkazy už nejsou rozbité Windows cestami

Checklist pro zítřejší live:

1. Zkopírovat opravené source soubory do GitHub clone.
2. Buildnout s `SITE_URL=https://visitbulharsko.cz BASE_PATH=/`.
3. Nasadit `dist/` do cílového hostingu / gh-pages režimu pro vlastní doménu.
4. Pokud GitHub Pages:
   - nastavit custom domain `visitbulharsko.cz`,
   - vytvořit/ověřit `CNAME` soubor v publish větvi,
   - DNS: apex A záznamy na GitHub Pages + případně www CNAME.
5. Po přepnutí ověřit:
   - `https://visitbulharsko.cz/`
   - `https://visitbulharsko.cz/sitemap.xml`
   - `https://visitbulharsko.cz/robots.txt`
   - top článek
   - kategorie
   - nemovitosti stránku
6. Přidat doménu do Google Search Console.
7. Odeslat sitemap.
8. Zkontrolovat indexability + canonicaly.

## Doporučené priority před live

P0 – před spuštěním:

- Přenést lokální opravy do GitHub clone a deploynout testovací build.
- Ověřit produkční doménový build proti doménovým canonicalům.
- Rozhodnout, jestli newsletter formulář zatím schovat / označit / napojit.

P1 – ideálně brzy po spuštění:

- Optimalizovat největší obrázky.
- Zkrátit/přepsat meta descriptions u hlavních stránek.
- Vyčistit podezřelé URL s emoji/cyrilicí.
- Doplnit `llms.txt`.

P2 – obsahově:

- Přidat nové aktuální zprávy z konce července.
- Vytvořit evergreen články pro nejhledanější cestovní dotazy.
- Slabé staré RSS články dát do archivu/noindex nebo přepracovat.
