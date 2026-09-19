# -*- coding: utf-8 -*-
"""Share-card images: public/og/<slug>.jpg (packshot on white) and public/og.jpg (storefront). Run after tools/katalog.py."""
import json, pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'public/og'; OUT.mkdir(parents=True, exist_ok=True)
KIRMIZI = (212, 43, 30)
W, H = 1200, 630
for u in json.loads((ROOT / 'src/content/urunler.json').read_text()):
    src = Image.open(ROOT / 'src/assets/urunler' / u['gorsel']).convert('RGBA')
    bg = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    src.thumbnail((760, 530))
    bg.alpha_composite(src, ((W - src.width) // 2, (H - 14 - src.height) // 2))
    bar = Image.new('RGBA', (W, 14), KIRMIZI + (255,)); bg.alpha_composite(bar, (0, H - 14))
    bg.convert('RGB').save(OUT / (u['slug'] + '.jpg'), quality=82, optimize=True)
foto = Image.open(ROOT / 'src/assets/dukkan/vitrin.jpg').convert('RGB')
r = max(W / foto.width, H / foto.height); foto = foto.resize((round(foto.width * r), round(foto.height * r)))
x = (foto.width - W) // 2; y = max(0, (foto.height - H) // 2 - 60)
foto.crop((x, y, x + W, y + H)).save(ROOT / 'public/og.jpg', quality=82, optimize=True)
print('og hazır:', len(list(OUT.glob('*.jpg'))))
