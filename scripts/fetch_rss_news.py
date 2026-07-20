import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, UTC
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / 'data' / 'feed_sources.json'
OUT = ROOT / 'src' / 'data' / 'feed-news.json'


def text(el, name):
    node = el.find(name)
    return unescape((node.text or '').strip()) if node is not None and node.text else ''


def strip_html(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    s = re.sub(r'\s+', ' ', s)
    s = unescape(s).strip()
    s = re.sub(r'The post .*? appeared first on Visit Bulharsko\s*\.?', '', s, flags=re.I).strip()
    return clean_markup(s)


def clean_markup(s):
    s = unescape(s or '')
    s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
    s = re.sub(r'__(.*?)__', r'\1', s)
    # Zpravodajský layout působí seriózněji bez emoji v titulcích z RSS.
    s = re.sub(r'[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def parse_date(s):
    if not s:
        return ''
    try:
        return parsedate_to_datetime(s).isoformat()
    except Exception:
        return s


def fetch_source(src):
    req = urllib.request.Request(src['url'], headers={'User-Agent': 'Hermes VisitBulharsko RSS importer'})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read(500_000)
    root = ET.fromstring(raw)
    items = []
    for item in root.findall('.//item')[:12]:
        title = clean_markup(text(item, 'title'))
        link = text(item, 'link')
        description = strip_html(text(item, 'description'))
        pub = parse_date(text(item, 'pubDate'))
        guid = text(item, 'guid') or link or title
        items.append({
            'source': src.get('name', ''),
            'sourceUrl': src.get('url', ''),
            'category': src.get('category', 'zpravy-bulharsko'),
            'title': title,
            'link': link,
            'excerpt': description[:220],
            'published': pub,
            'guid': guid,
        })
    return items


def main():
    sources = json.loads(SOURCES_FILE.read_text(encoding='utf-8'))
    all_items = []
    errors = []
    seen = set()
    for src in sources:
        try:
            for item in fetch_source(src):
                key = item['guid'] or item['link'] or item['title']
                if key in seen:
                    continue
                seen.add(key)
                all_items.append(item)
        except Exception as e:
            errors.append({'source': src.get('name'), 'url': src.get('url'), 'error': f'{type(e).__name__}: {e}'})
    all_items.sort(key=lambda x: x.get('published') or '', reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({'generatedAt': datetime.now(UTC).isoformat(), 'items': all_items[:24], 'errors': errors}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'items': len(all_items[:24]), 'errors': len(errors), 'out': str(OUT)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
