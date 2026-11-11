# Snap Aras's marked zones to the map: plan buildings (bldg.json) inside each marked area, closed into one shape;
# zone 4 = OSM Kızıl Avlu archaeological site boundary (w220480903).
import json, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
R = '/mnt/project-files/planting_masterplan_2026-11-08/masterplan_labels_2026-11-08/'
sys.path.insert(0, R + '_src/roads'); import tfm
D = R + '_src/zones/'
Z = json.load(open(D + 'zones.json')); B = json.load(open(D + 'bldg.json')); F = json.load(open(R + '_src/roads/feat.json'))
S = 4.0; X0, Y0, W, H = 200, 5240, 1908, 560
def topx(p): return [((x-X0)/S, (y-Y0)/S) for x, y in p]
def inside(p, x, y):
    c = False; j = len(p)-1
    for i in range(len(p)):
        xi, yi = p[i]; xj, yj = p[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/(yj-yi)+xi: c = not c
        j = i
    return c
def grow(im, r):
    for _ in range(r): im = im.filter(ImageFilter.MaxFilter(3))
    return im
def shrink(im, r):
    for _ in range(r): im = im.filter(ImageFilter.MinFilter(3))
    return im
def trace(m):  # Moore boundary of largest blob (m bool array)
    from collections import deque
    lab = np.zeros(m.shape, int); best = (0, 0); n = 0
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]: continue
        n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; c = 0
        while q:
            y, x = q.popleft(); c += 1
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy, xx = y+dy, x+dx
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; q.append((yy, xx))
        if c > best[0]: best = (c, n)
    b = lab == best[1]
    ys, xs = np.nonzero(b); i = np.argmin(ys*10000+xs); sy, sx = ys[i], xs[i]
    nb = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    pts = [(sx, sy)]; cy, cx = sy, sx; d = 6
    for _ in range(200000):
        for k in range(8):
            dd = (d + k) % 8; yy, xx = cy+nb[dd][0], cx+nb[dd][1]
            if 0 <= yy < b.shape[0] and 0 <= xx < b.shape[1] and b[yy, xx]:
                cy, cx = yy, xx; d = (dd + 5) % 8; break
        if (cy, cx) == (sy, sx): break
        pts.append((cx, cy))
    return pts[::3]
out = {}
for k, v in Z.items():
    if k == '4':
        for t, i, tg, co in F:
            if i == '220480903': ring = [tfm.to_plan(*c) for c in co]
        out[k] = dict(v, plan=[list(map(float, a)) for a in ring], src='OSM w220480903 Kızıl Avlu archaeological site'); continue
    zr = v['plan']
    zm = Image.new('L', (W, H), 0); ImageDraw.Draw(zm).polygon(topx(zr), fill=255); zm = grow(zm, 6)
    zmA = np.array(zm) > 0
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); nb = 0
    for x, y, a in B:
        px, py = (x-X0)/S, (y-Y0)/S
        if 0 <= px < W and 0 <= py < H and zmA[int(py), int(px)]:
            r = max(10, math.sqrt(a)/S*1.2); d.ellipse((px-r, py-r, px+r, py+r), fill=255); nb += 1
    for t, i, tg, co in F:  # OSM shops, amenities, historic places inside the marked area also count
        if not (tg.get('shop') or tg.get('amenity') or tg.get('historic')): continue
        x, y = tfm.to_plan(sum(c[0] for c in co)/len(co), sum(c[1] for c in co)/len(co)); px, py = (x-X0)/S, (y-Y0)/S
        if 0 <= px < W and 0 <= py < H and zmA[int(py), int(px)]: d.ellipse((px-10, py-10, px+10, py+10), fill=255)
    g = 24 if k == '2' else 14
    m = shrink(grow(m, g), g - 4)
    mm = (np.array(m) > 0) & zmA
    pts = trace(mm)
    out[k] = dict(v, plan=[[X0+px*S, Y0+py*S] for px, py in pts], src='plan buildings inside marked area (%d)' % nb)
    print(k, nb, len(pts))
json.dump(out, open(D + 'zones_v2.json', 'w'), ensure_ascii=False)
