import json
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parents[1]
site_path = root / 'src/data/site-data.json'
pub_path = root / 'data/published_news_sources.json'

with site_path.open('r', encoding='utf-8') as f:
    site = json.load(f)
with pub_path.open('r', encoding='utf-8') as f:
    published = json.load(f)

posts = site.get('posts', [])
existing_slugs = {p.get('slug') for p in posts}
existing_sources = {p.get('sourceUrl') for p in posts if p.get('sourceUrl')}
pub_list = published.setdefault('published', [])
if not isinstance(pub_list, list):
    pub_list = []
    published['published'] = pub_list
published_urls = set(pub_list)

category = {
    'id': 22,
    'name': 'Zpravodajství',
    'slug': 'zpravy-bulharsko',
    'link': 'https://visitbulharsko.cz/category/zpravy-bulharsko/'
}
max_id = max((int(p.get('id', 0)) for p in posts), default=3499)
now = '2026-07-21T00:00:00'

candidates = [
    {
        'sourceUrl': 'https://www.novinite.com/view_news.php?id=239724',
        'slug': 'bourky-v-bulharsku-21-cervence-2026',
        'title': 'Bulharsko má žluté varování před bouřkami v 14 regionech',
        'excerpt': 'Na úterý 21. července platí v části Bulharska žluté varování před bouřkami. Cestovatelé mají počítat hlavně s rizikem přeháněk ve východních oblastech a na horách.',
        'seoTitle': 'Bouřky v Bulharsku 21. července - Visit Bulharsko',
        'metaDescription': 'V Bulharsku platí žluté varování před bouřkami pro 14 regionů. Praktické dopady pro cesty k moři, do hor i po silnicích.',
        'content': '<p>Bulharsko vydalo na úterý 21. července žluté varování před bouřkami pro čtrnáct regionů ve střední a východní části země. Pro české cestovatele to neznamená zákaz cestování, ale důvod upravit denní plán, sledovat místní předpověď a počítat s tím, že počasí se může během odpoledne rychle změnit.</p>\n<h2>Co se stalo</h2>\n<p>Podle bulharských meteorologů začne den na řadě míst slunečně, později se ale mají tvořit přeháňky a bouřkové mraky. Nejvýraznější vývoj se očekává zejména ve východních regionech a v horských oblastech. Bouřky mohou být krátké, ale lokálně prudší: během letní dovolené to znamená hlavně riziko náhlého deště, horší viditelnosti, silnějšího větru a komplikací na silnicích.</p>\n<h2>Co to znamená pro cestovatele</h2>\n<p>Pokud míříte autem k Černému moři nebo se přesouváte mezi letovisky, nechte si časovou rezervu a vyhněte se jízdě v nejsilnějším dešti. Na pláži je rozumné opustit vodu při prvním hřmění a neschovávat se pod osamocené stromy nebo lehké slunečníky. V horách, například při výletech ve Staré planině nebo Rodopách, je lepší vyrazit brzy ráno a odpolední trasu zkrátit.</p>\n<p>U letů do Burgasu, Varny nebo Sofie může bouřkové počasí způsobit menší zpoždění, proto se před cestou na letiště vyplatí ověřit stav letu u dopravce.</p>\n<p><a href="https://www.novinite.com/view_news.php?id=239724" rel="nofollow noopener" target="_blank">Zdroj: Novinite / Sofia News Agency</a></p>'
    },
    {
        'sourceUrl': 'https://www.novinite.com/view_news.php?id=239714',
        'slug': 'bulharsko-vlna-veder-konec-cervence-2026',
        'title': 'Bulharsko čeká na konci července první vlna čtyřicítek',
        'excerpt': 'Předpovědi pro Bulharsko počítají po 25. červenci s nástupem velmi horkého počasí. U moře i ve vnitrozemí bude důležité plánovat aktivity mimo polední žár.',
        'seoTitle': 'Vlna veder v Bulharsku na konci července',
        'metaDescription': 'Bulharsko může na konci července zasáhnout vlna veder kolem 40 °C. Co to znamená pro pobyt u moře, ve městech i při cestách autem.',
        'content': '<p>Bulharsko se podle aktuálních výhledů chystá na nejteplejší období dosavadního roku. Po 25. až 26. červenci mohou teploty vystoupat k hranici 40 °C a místy i výše. Pro návštěvníky letovisek to znamená klasický letní režim s koupáním, ale také vyšší nároky na pitný režim, ochranu před sluncem a plánování přesunů.</p>\n<h2>Co se stalo</h2>\n<p>Meteorologické modely naznačují, že po nestabilnějším počasí přijde delší slunečná a velmi horká fáze. Největší zátěž obvykle dopadá na vnitrozemská města, jako jsou Plovdiv, Stará Zagora nebo Sofie, ale horko může být citelné i na pobřeží Černého moře. U moře ho částečně mírní vánek, přesto mohou být polední a odpolední hodiny pro děti, seniory a osoby se zdravotními potížemi náročné.</p>\n<h2>Co to znamená pro cestovatele</h2>\n<p>Prakticky: výlety do měst, klášterů nebo archeologických lokalit plánujte ideálně ráno. Mezi 12. a 16. hodinou je lepší zůstat ve stínu, klimatizovaném ubytování nebo u vody, ale s častými pauzami mimo přímé slunce. Při půjčení auta nenechávejte v zaparkovaném voze děti, zvířata ani elektroniku a počítejte s vyšší spotřebou klimatizace.</p>\n<p>Na plážích v Burgasu, Varně, Nesebaru, Primorsku nebo na Slunečném pobřeží sledujte také barvu vlajek a pokyny plavčíků. Vedro samo o sobě dovolenou neruší, ale podcenění hydratace a slunce může rychle pokazit celý pobyt.</p>\n<p><a href="https://www.novinite.com/view_news.php?id=239714" rel="nofollow noopener" target="_blank">Zdroj: Novinite / Sofia News Agency</a></p>'
    }
]

new_posts = []
new_urls = []
for c in candidates:
    if c['sourceUrl'] in published_urls or c['sourceUrl'] in existing_sources or c['slug'] in existing_slugs:
        continue
    max_id += 1
    new_posts.append({
        'id': max_id,
        'type': 'post',
        'slug': c['slug'],
        'path': f"/{c['slug']}/",
        'title': c['title'],
        'excerpt': c['excerpt'],
        'date': now,
        'modified': now,
        'categories': [category],
        'seo': {'title': c['seoTitle'], 'description': c['metaDescription']},
        'content': c['content'],
        'sourceUrl': c['sourceUrl']
    })
    new_urls.append(c['sourceUrl'])

if new_posts:
    site['posts'] = new_posts + posts
    for u in new_urls:
        if u not in pub_list:
            pub_list.append(u)
    with site_path.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(site, f, ensure_ascii=False, indent=2)
        f.write('\n')
    with pub_path.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(published, f, ensure_ascii=False, indent=2)
        f.write('\n')

print(json.dumps({'added': len(new_posts), 'slugs': [p['slug'] for p in new_posts], 'urls': new_urls}, ensure_ascii=False))
