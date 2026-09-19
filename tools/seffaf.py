# -*- coding: utf-8 -*-
"""Turns white-background JPG packshots into transparent PNGs (flood fill from the edges so
white areas inside the packaging survive). Rewrites urunler.json to point at the PNGs."""
import json, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / 'src/assets/urunler'
J = ROOT / 'src/content/urunler.json'
d = json.loads(J.read_text())
for u in d:
    src = IMG / u['gorsel']
    im0 = Image.open(src).convert('RGBA')
    c = im0.getpixel((0, 0))
    if c[3] < 250 or min(c[:3]) < 235: continue  # already transparent, or not a white background
    im = im0.convert('RGB')
    w, h = im.size
    pad = 2
    canvas = Image.new('RGB', (w + 2 * pad, h + 2 * pad), (255, 255, 255)); canvas.paste(im, (pad, pad))
    g = canvas.convert('L').point(lambda v: 255 if v >= 238 else 0)
    ImageDraw.floodfill(g, (0, 0), 128, thresh=0)
    mask = g.point(lambda v: 0 if v == 128 else 255).crop((pad, pad, pad + w, pad + h))
    out = im.convert('RGBA'); out.putalpha(mask)
    # trim to content
    bbox = mask.getbbox()
    if bbox: out = out.crop(bbox)
    dest = src.with_suffix('.png'); out.save(dest, optimize=True)
    if src != dest: src.unlink()
    u['gorsel'] = dest.name
    print('png', dest.name, out.size)
J.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
