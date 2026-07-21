import os
import shutil
from pathlib import Path

src = Path(r'C:/Users/lukas/Desktop/Hermes/visitbulharsko-astro').resolve()
dst = Path(r'C:/Users/lukas/Desktop/Hermes/visit-bulharsko-github').resolve()

exclude_names = {'node_modules', 'dist', '.astro', '.git'}
exclude_rel = {
    Path('data/source'),
    Path('data/content'),
    Path('data/live-news-raw.json'),
    Path('data/property-feed-last.xml'),
}

def excluded(path: Path, base: Path) -> bool:
    try:
        rel = path.relative_to(base)
    except ValueError:
        return False
    parts = rel.parts
    if any(p in exclude_names for p in parts):
        return True
    for ex in exclude_rel:
        if rel == ex or ex in rel.parents:
            return True
    return False

# delete destination content except .git and excluded paths
for item in list(dst.iterdir()):
    if item.name == '.git':
        continue
    if excluded(item, dst):
        continue
    if item.is_dir():
        shutil.rmtree(item)
    else:
        item.unlink()

for dirpath, dirnames, filenames in os.walk(src):
    d = Path(dirpath)
    dirnames[:] = [name for name in dirnames if not excluded(d / name, src)]
    if excluded(d, src):
        continue
    rel_dir = d.relative_to(src)
    target_dir = dst / rel_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    for fn in filenames:
        s = d / fn
        if excluded(s, src):
            continue
        t = target_dir / fn
        shutil.copy2(s, t)

print('sync complete')
