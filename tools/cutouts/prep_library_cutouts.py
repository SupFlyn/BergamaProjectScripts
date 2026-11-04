# prepares library PNGs as style a cutouts: trim to alpha, people interiors white, 600 px tall, RGBA non-interlaced
import sys, json, os
from PIL import Image
from collections import deque
LIB = '/mnt/project-files/revision_2026-10-30/asset_library/library'
OUT = sys.argv[1]   # usage: python3 -I tools/cutouts/prep_library_cutouts.py <cutouts folder>
TREE_SRC = 'Pinterest board of nilduygu (tree / grass cutouts)'
NEW = [  # key, asset, folder, file, h_m, kind, facing
 ('plane','CS_007','veg-tree-bl-round','plane_3.png',15.0,'tree',1),
 ('plane','CS_011','veg-tree-bl-round','plane_4.png',15.0,'tree',1),
 ('plane','CS_012','veg-tree-bl-round','plane_5.png',15.0,'tree',1),
 ('plane','CS_014','veg-tree-bl-round','plane_6.png',15.0,'tree',1),
 ('ash','CS_004','veg-tree-bl-oval','ash_2.png',20.0,'tree',1),
 ('ash','CS_006','veg-tree-bl-oval','ash_3.png',20.0,'tree',1),
 ('ash','CS_021','veg-tree-bl-irr','ash_4.png',20.0,'tree',1),
 ('stone_pine','CS_016','veg-tree-bl-umb','stone_pine_2.png',27.5,'tree',1),
 ('stone_pine','CS_017','veg-tree-bl-umb','stone_pine_3.png',27.5,'tree',1),
 ('olive','CS_025','veg-tree-bl-irr','olive_2.png',11.5,'tree',1),
 ('tamarisk','CS_022','veg-tree-bl-irr','tamarisk_2.png',9.5,'tree',1),
 ('tamarisk','CS_024','veg-tree-bl-irr','tamarisk_3.png',9.5,'tree',1),
 ('person_stand','PB_324','ppl-stand','stand_4.png',1.75,'person',1),
 ('person_adult_child','PB_303','ppl-group','adult_child_1.png',1.75,'person',1),
 ('person_sit_step','PB_327','ppl-sit','sit_step_2.png',1.3,'person',1),
 ('person_sit_step','PB_292','ppl-sit','sit_step_3.png',1.3,'person',1),
]
def white_inside(im):
    a = im.split()[3]; w, h = im.size; px = a.load()
    seen = bytearray(w * h); q = deque()
    for x in range(w):
        for y in (0, h - 1): q.append((x, y))
    for y in range(h):
        for x in (0, w - 1): q.append((x, y))
    while q:
        x, y = q.popleft(); i = y * w + x
        if seen[i] or px[x, y] > 40: continue
        seen[i] = 1
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    bg = Image.new('RGBA', im.size, (255, 255, 255, 0)); bp = bg.load()
    for y in range(h):
        for x in range(w):
            if not seen[y * w + x]: bp[x, y] = (255, 255, 255, 255)
    return Image.alpha_composite(bg, im)
js = json.load(open(os.path.join(OUT, 'cutouts.json'), encoding='utf-8'))
cut = js['cutouts']
for key, aid, fol, fn, h_m, kind, fac in NEW:
    im = Image.open(os.path.join(LIB, fol, '_unclustered', aid + '.png')).convert('RGBA')
    im = im.crop(im.split()[3].getbbox())
    if kind == 'person': im = white_inside(im)
    s = 600.0 / im.size[1]; im = im.convert('RGBa').resize((max(1, round(im.size[0] * s)), 600), Image.LANCZOS).convert('RGBA')
    im.save(os.path.join(OUT, fn), interlace=False)
    e = {'file': fn, 'h_m': h_m, 'kind': kind, 'asset_id': aid}
    if fac < 0: e['facing'] = -1
    if kind == 'tree': e['source'] = TREE_SRC
    old = cut.get(key); old = [] if old is None else (old if isinstance(old, list) else [old])
    old = [o for o in old if o.get('asset_id') != aid]
    cut[key] = old + [e]
json.dump(js, open(os.path.join(OUT, 'cutouts.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('cutouts:', len(cut), 'keys,', sum(len(v) if isinstance(v, list) else 1 for v in cut.values()), 'entries')
