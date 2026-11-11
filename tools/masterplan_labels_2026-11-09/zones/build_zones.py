# Zone explanation images, 9 styles, over today's plan (09:00 file + roads v2).
# Facts only from OSM (bergama_osm.osm -> _src/roads/feat.json), survey labels, building counts from the plan.
import json, math, sys, os
R = '/mnt/project-files/planting_masterplan_2026-11-08/masterplan_labels_2026-11-08/'
sys.path.insert(0, R + '_src/roads'); import tfm
import numpy as np
from PIL import Image
D = R + '_src/zones/'
Z = json.load(open(D + os.environ.get('ZONES', 'zones.json')))
F = json.load(open(R + '_src/roads/feat.json'))
FONT = "Arial, Helvetica, sans-serif"
ORDER = ['YN', 'DN', '2', '3', '4', '5', '6']
INFO = {
 'YN': dict(t='Upper Neighbourhood', s='Yukarı Mahalle', c='#E3A12F', ic='house', w='upper',
   b=['62 buildings in our plan: dense hillside houses', 'Near quarters: Ulucami, Selçuk (OSM)', 'Street: Kale Çeşme Sokak (OSM)'],
   u='Residents walking down to the west park'),
 'DN': dict(t='Lower Neighbourhood', s='Aşağı Mahalle', c='#D8692E', ic='house', w='lower',
   b=['86 buildings in our plan', 'Health: 3 Nolu Aile Sağlığı Merkezi, Benek Eczanesi (OSM)', 'Streets: Telli Dede Sokak, 2. Çukurbağ Caddesi (OSM)'],
   u='Residents reaching the south bank walk'),
 '2': dict(t='Cultural Heritage', s='Ulu Cami quarter', c='#B8323C', ic='dome', w='heritage',
   b=['Bergama Ulu Cami, Parmaklı Mescidi (OSM, historic)', 'Ulucami Köprüsü crosses the Selinos (OSM)', 'Streets: Cami Kebir Caddesi, Ulu Cami Yokuşu Sokak (OSM)'],
   u='Worshippers and visitors on the heritage walk'),
 '3': dict(t='Bazaar', s='Çarşı: historic market', c='#7A4BA0', ic='shop', w='market',
   b=['OSM: 6 restaurants, 6 cafés, 6 antiques, 3 bakeries, 3 carpet', 'Tahtakale Ucuzluk Pazarı, Halı Dokuma Atölyesi (OSM)', 'Yabets Sinagogu, Halk Kütüphanesi, Yıldız Garajı (OSM)', 'Tabak Köprüsü joins both banks (OSM)'],
   u='Shoppers, traders and bus arrivals'),
 '4': dict(t='Archaeological Site', s='Arkeolojik sit: Kızıl Avlu (OSM boundary)', c='#2F8F4E', ic='column', w='ancient',
   b=['Kızıl Avlu temple and South Rotunda (OSM)', 'Kurtuluş Cami inside the site boundary (OSM)', 'Visitor ticket shop and toilets (OSM)'],
   u='Visitors: gates, then our proposed link to the walk'),
 '5': dict(t='Settled Housing', s='Yerleşik konut', c='#2C6FC4', ic='house', w='housing',
   b=['33 buildings in our plan', 'Streets: Onur, Özgür, Pelin, Barış Sokak (OSM)', 'Güler Market, Sancak Market; 7 car dealers (OSM)'],
   u='Residents on the south bank walk'),
 '6': dict(t='Industrial Area', s='Sanayi: Bergama 2. Sanayi Sitesi', c='#4B5058', ic='factory', w='industry',
   b=['Bergama 2. Sanayi Sitesi (OSM landuse=industrial)', '2. Sanayi Caddesi with 1. to 9. Sokak (OSM)', 'Fevzipaşa quarter; 15 buildings in our plan'],
   u='Workers next to the east park'),
}
NOTE = ('Facts: OpenStreetMap (bergama_osm.osm) and building counts from our plan file. Zone shapes follow the plan buildings inside your marked areas; '
        'the archaeological site uses the OSM Kızıl Avlu boundary. "Users" lines are our reading of the land use, not data.')
_c = NOTE.rfind(' ', 0, 150); N1, N2 = NOTE[:_c], NOTE[_c+1:]
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')

# ---------- geometry ----------
def chaikin(p, n=3):
    for _ in range(n):
        q = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            q += [(.75*a[0]+.25*b[0], .75*a[1]+.25*b[1]), (.25*a[0]+.75*b[0], .25*a[1]+.75*b[1])]
        p = q
    return p
RING = {k: chaikin([tuple(a) for a in Z[k]['plan']]) for k in ORDER}
def pth(p): return 'M' + ' L'.join('%.1f,%.1f' % a for a in p) + ' Z'
def cen(k):
    p = RING[k]; return (sum(a[0] for a in p)/len(p), sum(a[1] for a in p)/len(p))
def rad(k):
    c = cen(k); return max(math.hypot(a[0]-c[0], a[1]-c[1]) for a in RING[k])
def ellipse(k):
    p = np.array(RING[k]); c = p.mean(0); u, s, vt = np.linalg.svd(p - c)
    ang = math.degrees(math.atan2(vt[0][1], vt[0][0]))
    pr = (p - c) @ vt.T
    return c, abs(pr[:, 0]).max()*1.08, abs(pr[:, 1]).max()*1.08, ang
def inside(p, x, y):
    c = False; j = len(p) - 1
    for i in range(len(p)):
        xi, yi = p[i]; xj, yj = p[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/(yj-yi)+xi: c = not c
        j = i
    return c
def hull(pts):
    pts = sorted(set(pts))
    def cr(o, a, b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def edge_pt(k, tx, ty):
    c = cen(k); best = None
    for a in RING[k]:
        d = math.hypot(a[0]-tx, a[1]-ty)
        if best is None or d < best[0]: best = (d, a)
    return best[1]

# river centre line from the Selinos mask (6000 px frame x0=200,y0=5240,K=6000/7630)
M = np.array(Image.open(R + '_src/roads/selinos_mask.png').convert('L')) < 128
K = 6000/7630; RIV = []
for px in range(0, M.shape[1], 15):
    ys = np.nonzero(M[:, px])[0]
    if len(ys) > 20: RIV.append((200 + px/K, 5240 + ys.mean()/K))
def river_near(x, y): return min(RIV, key=lambda a: (a[0]-x)**2 + (a[1]-y)**2)
RN = {k: river_near(*cen(k)) for k in ORDER}

# ---------- OSM points per zone ----------
def cat(tg):
    a = tg.get('amenity', ''); s = tg.get('shop', '')
    if a == 'place_of_worship' or tg.get('building') in ('mosque', 'synagogue'): return 'worship'
    if a in ('hospital', 'pharmacy', 'clinic', 'doctors', 'veterinary'): return 'health'
    if tg.get('historic') or tg.get('building') in ('temple', 'ruins'): return 'historic'
    if a in ('restaurant', 'cafe', 'ice_cream', 'fast_food') or s in ('bakery', 'pastry'): return 'food'
    if a in ('bus_station', 'parking', 'fuel'): return 'transport'
    if a in ('library', 'toilets', 'drinking_water') or tg.get('tourism') or s == 'ticket': return 'service'
    if s: return 'shop'
    if tg.get('landuse') == 'industrial': return 'industry'
    return None
POI = {k: [] for k in ORDER}; NAMED = {}
for t, i, tg, co in F:
    lo = sum(c[0] for c in co)/len(co); la = sum(c[1] for c in co)/len(co)
    x, y = tfm.to_plan(lo, la)
    if tg.get('name'): NAMED.setdefault(tg['name'], (x, y))
    cc = cat(tg)
    if not cc: continue
    for k in ORDER:
        if inside(RING[k], x, y): POI[k].append((cc, x, y, tg.get('name')))
KEYPL = [('Bergama Ulu Cami', '2'), ('Parmaklı Mescidi', '2'), ('Ulucami Köprüsü', '2'), ('Tabak Köprüsü', '3'),
         ('Bergama Yabets Sinagogu', '3'), ('Tahtakale Ucuzluk Pazarı', '3'), ('Kızıl Avlu', '4'), ('South Rotunda', '4'),
         ('Eski Kışla Binası', '4'), ('Kurtuluş Cami', '4'), ('Benek Eczanesi', 'DN'), ('Güler Market', '5'),
         ('Bergama 2. Sanayi Sitesi', '6')]

# ---------- drawing helpers ----------
def T(x, y, s, size=30, fill='#222', w='normal', anchor='start', style='normal', extra=''):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" font-weight="%s" font-style="%s" fill="%s" text-anchor="%s" %s>%s</text>'
            % (x, y, FONT, size, w, style, fill, anchor, extra, esc(s)))
def icon(kind, cx, cy, s, col):
    g = '<g transform="translate(%.1f,%.1f) scale(%.3f)" fill="%s" stroke="none">' % (cx, cy, s/100, col)
    if kind == 'house': g += '<path d="M-40,-2 L0,-40 L40,-2 Z"/><rect x="-30" y="-4" width="60" height="40"/>'
    elif kind == 'dome': g += '<path d="M-30,10 A30,30 0 0 1 30,10 Z"/><rect x="-36" y="10" width="72" height="26"/><rect x="34" y="-42" width="8" height="78"/><path d="M33,-42 L38,-54 L43,-42 Z"/>'
    elif kind == 'shop': g += '<path d="M-42,-34 L42,-34 L48,-8 L-48,-8 Z"/><rect x="-36" y="-4" width="72" height="40"/>'
    elif kind == 'column': g += '<path d="M-44,-20 L0,-44 L44,-20 Z"/><rect x="-34" y="-16" width="12" height="44"/><rect x="-6" y="-16" width="12" height="44"/><rect x="22" y="-16" width="12" height="44"/><rect x="-46" y="30" width="92" height="10"/>'
    elif kind == 'factory': g += '<path d="M-44,38 L-44,-6 L-20,-22 L-20,-6 L4,-22 L4,-6 L28,-22 L28,38 Z"/><rect x="32" y="-44" width="12" height="82"/>'
    elif kind == 'leaf': g += '<path d="M-30,30 C-30,-20 10,-40 36,-36 C40,-6 20,34 -30,30 Z"/>'
    elif kind == 'walk': g += '<circle cx="4" cy="-34" r="10"/><path d="M-4,-20 L14,-20 L10,8 L22,38 L10,38 L0,14 L-12,38 L-24,38 L-8,4 Z"/>'
    elif kind == 'cross': g += '<rect x="-10" y="-36" width="20" height="72"/><rect x="-36" y="-10" width="72" height="20"/>'
    elif kind == 'bus': g += '<rect x="-38" y="-30" width="76" height="56" rx="8"/><circle cx="-22" cy="32" r="8"/><circle cx="22" cy="32" r="8"/>'
    elif kind == 'cup': g += '<path d="M-30,-20 L22,-20 L16,30 L-24,30 Z"/><path d="M22,-8 C40,-8 40,14 18,14" fill="none" stroke="%s" stroke-width="8"/>' % col
    return g + '</g>'
ICONS = {'YN': ['house', 'walk', 'leaf'], 'DN': ['house', 'cross', 'walk'], '2': ['dome', 'walk', 'column'],
         '3': ['shop', 'cup', 'bus'], '4': ['column', 'walk', 'leaf'], '5': ['house', 'shop', 'walk'], '6': ['factory', 'bus', 'leaf']}
def card(k, x, y, w=1180, box=True, under=False, head=False, num=None, size=1.0, users=True):
    I = INFO[k]; c = I['c']; o = []; lh = 38*size
    lines = I['b'] + (['Users: ' + I['u']] if users else [])
    h = 112*size + lh*len(lines) + 20
    if box: o.append('<rect x="%.1f" y="%.1f" width="%g" height="%.1f" fill="#fff" fill-opacity="0.94" stroke="%s" stroke-width="5" rx="10"/>' % (x, y, w, h, c))
    if head:
        o.append('<rect x="%.1f" y="%.1f" width="%g" height="%.1f" fill="%s" rx="10"/>' % (x, y, w, 70*size, c))
        o.append(T(x+24, y+50*size, (('%s  ' % num) if num else '') + I['t'], 44*size, '#fff', 'bold'))
        o.append(T(x+24, y+104*size, I['s'], 30*size, c, 'bold'))
    else:
        tx = x + 24
        if num is not None:
            o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x+50*size, y+48*size, 30*size, c))
            o.append(T(x+50*size, y+60*size, str(num), 34*size, '#fff', 'bold', 'middle')); tx = x + 96*size
        o.append(T(tx, y+60*size, I['t'], 48*size, c, 'bold'))
        if under: o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="%s"/>' % (tx, y+72*size, min(w-40, len(I['t'])*27*size), c))
        o.append(T(tx, y+104*size, I['s'], 30*size, '#555', 'bold'))
    yy = y + 112*size + 30*size
    for s in lines:
        u = s.startswith('Users:')
        o.append(T(x+40, yy, ('' if u else '• ') + s, 27*size, '#555' if u else '#222', 'normal', style='italic' if u else 'normal')); yy += lh
    return '\n'.join(o), (x, y, w, h)

# card slots: top band (y 4720-5230) and bottom band (y 7570-8200)
SLOT = {'YN': (260, 4990), '2': (1560, 4990), '4': (2860, 4990), 'DN': (260, 7600), '3': (1560, 7600), '5': (2860, 7600), '6': (4160, 7600)}
VB = (200, 4960, 7630, 3190)
def bands():
    return ('<rect x="200" y="4960" width="7630" height="300" fill="#fff"/>'
            '<rect x="200" y="7560" width="7630" height="680" fill="#fff"/>')
def foot(title, sub, colours=True, x=5500, y=7620):
    o = [T(x, y+40, title, 56, '#222', 'bold'), T(x, y+88, sub, 28, '#555')]
    if colours:
        yy = y + 140
        for i, k in enumerate(ORDER):
            cx = x + (i % 2)*560; cy = yy + (i//2)*48
            o.append('<rect x="%g" y="%g" width="44" height="30" fill="%s" rx="4"/>' % (cx, cy-24, INFO[k]['c']))
            o.append(T(cx+58, cy, INFO[k]['t'], 28, '#222'))
    o.append(T(x, 8090, N1, 20, '#666')); o.append(T(x, 8116, N2, 20, '#666'))
    return '\n'.join(o)
def leader(bx, k, dash='0.1 12', col='#222', w=5, toward=None):
    x, y, bw, bh = bx; c = cen(k)
    ax = min(max(c[0], x+40), x+bw-40); ay = y+bh if c[1] > y+bh else y
    ex, ey = edge_pt(k, ax, ay)
    return ('<path d="M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%g" stroke-dasharray="%s" stroke-linecap="round"/>'
            '<circle cx="%.1f" cy="%.1f" r="10" fill="%s"/>' % (ax, ay, ex, ey, col, w, dash, ex, ey, col))
def veil(op): return '<rect x="200" y="5240" width="7630" height="2190" fill="#fff" fill-opacity="%g"/>' % op
def rn(i): return ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][i]

# ---------- the 9 styles ----------
def s1():  # ellipse outlines + dotted leaders + bold title + bullets
    o = [bands()]
    for k in ORDER:
        c, a, b, ang = ellipse(k)
        o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)" fill="none" stroke="%s" stroke-width="12"/>' % (c[0], c[1], a, b, ang, c[0], c[1], INFO[k]['c']))
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=False)
        o += [s, leader(bx, k)]
    o.append(foot('Zones around the project', 'Coloured ellipse = zone type; dotted leader to its description'))
    return o
def s2():  # walking radius circles + numbered nodes on the stream + side text column
    o = [bands(), veil(0.35)]
    r400 = 250*2.641
    o.append('<clipPath id="cp2"><rect x="200" y="5240" width="7630" height="2190"/></clipPath><g clip-path="url(#cp2)">')
    for k in ORDER:
        c = cen(k); o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="0.22" stroke="%s" stroke-opacity="0.6" stroke-width="4"/>' % (c[0], c[1], r400, INFO[k]['c'], INFO[k]['c']))
    o.append('</g>')
    o.append('<polyline points="%s" fill="none" stroke="#1F6FD1" stroke-width="8"/>' % ' '.join('%.1f,%.1f' % a for a in RIV))
    for i, k in enumerate(ORDER):
        c = cen(k); r = RN[k]
        o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#222" stroke-width="4" stroke-dasharray="14 10"/>' % (c[0], c[1], r[0], r[1]))
        o.append('<circle cx="%.1f" cy="%.1f" r="16" fill="%s" stroke="#fff" stroke-width="4"/>' % (c[0], c[1], INFO[k]['c']))
        o.append('<circle cx="%.1f" cy="%.1f" r="34" fill="#111"/>' % r + T(r[0], r[1]+13, str(i+1), 36, '#fff', 'bold', 'middle'))
    c = cen('4'); o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#111" stroke-width="3"/>' % (c[0], c[1]+r400*0.98, c[0]+260, c[1]+r400*0.98) + T(c[0]+270, c[1]+r400*0.98+10, '250 m', 30, '#111', 'bold'))
    o.append(T(260, 5040, 'DAILY LIFE', 64, '#111', 'bold') + '<rect x="260" y="5058" width="620" height="6" fill="#111"/>')
    o.append(T(260, 5100, 'Circle = 250 m around each zone centre (about 3 minutes on foot at 1.34 m/s).', 30, '#333'))
    o.append(T(260, 5140, 'Black number = where that zone meets the Selinos and our river park (nearest river point, dashed line).', 30, '#333'))
    o.append(T(260, 5180, 'Overlaps show where several daily routines share the same stretch of the river.', 30, '#333'))
    for i, k in enumerate(ORDER):
        x = 260 + (i % 4)*1340; y = 7610 + (i//4)*300
        o.append('<circle cx="%d" cy="%d" r="30" fill="#111"/>' % (x+30, y+30) + T(x+30, y+42, str(i+1), 32, '#fff', 'bold', 'middle'))
        o.append('<rect x="%d" y="%d" width="34" height="34" fill="%s" fill-opacity="0.6"/>' % (x+76, y+12, INFO[k]['c']))
        o.append(T(x+124, y+42, INFO[k]['t'], 38, '#111', 'bold'))
        o.append(T(x+20, y+90, INFO[k]['b'][0], 25, '#333')); o.append(T(x+20, y+124, INFO[k]['b'][1], 25, '#333'))
        o.append(T(x+20, y+158, 'Users: ' + INFO[k]['u'], 25, '#555', style='italic'))
    o.append(T(5600, 8090, N1, 20, '#666') + T(5600, 8116, N2, 20, '#666'))
    return o
def s3():  # flat colour fills + names written along the edge
    o = [bands(), veil(0.15)]
    for k in ORDER:
        o.append('<path d="%s" fill="%s" fill-opacity="0.62" stroke="%s" stroke-width="6"/>' % (pth(RING[k]), INFO[k]['c'], INFO[k]['c']))
    for k in ORDER:
        c, a, b, ang = ellipse(k)
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        if abs(ang) > 30 or k == '3': ang = 0
        th = math.radians(ang); nx, ny = -math.sin(th), math.cos(th)
        px, py = c[0] + nx*(b+40), c[1] + ny*(b+40)
        if py < c[1]: px, py = c[0] - nx*(b+40), c[1] - ny*(b+40)
        o.append('<g transform="translate(%.1f,%.1f) rotate(%.1f)">' % (px, py, ang) + T(0, 30, INFO[k]['t'], 78, INFO[k]['c'], 'bold', 'middle', 'italic',
                 'stroke="#fff" stroke-width="10" paint-order="stroke"') + '</g>')
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=False, size=0.95); o.append(s)
    o.append(foot('Character areas', 'Flat colour = one land use each; name written along the area edge'))
    return o
def s4():  # natural/urban: white base, black icon circles, dotted arrows, big titles
    o = [bands(), veil(0.6), '<defs><marker id="ah4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#111"/></marker></defs>']
    for k in ORDER:
        o.append('<path d="%s" fill="none" stroke="#111" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>' % pth(RING[k]))
        c = cen(k); r = RN[k]
        o.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#111" stroke-width="6" stroke-dasharray="0.1 16" stroke-linecap="round" marker-end="url(#ah4)"/>'
                 % (c[0], c[1], (c[0]+r[0])/2 + 120, (c[1]+r[1])/2, r[0], r[1]))
        for j, ic in enumerate(ICONS[k]):
            x = c[0] - 110 + j*110; y = c[1] - 70
            o.append('<circle cx="%.1f" cy="%.1f" r="46" fill="#111"/>' % (x, y) + icon(ic, x, y, 56, '#fff'))
        o.append(T(c[0], c[1]+40, INFO[k]['w'], 72, '#111', 'bold', 'middle', extra='stroke="#fff" stroke-width="12" paint-order="stroke"'))
        o.append(T(c[0], c[1]+86, INFO[k]['t'], 40, '#111', 'normal', 'middle', 'italic', 'stroke="#fff" stroke-width="10" paint-order="stroke"'))
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=False, size=0.95); o.append(s)
    o.append(foot('Who lives, works and visits around the river', 'Icons = main uses (from OSM); dotted arrow = route from the zone to our river park', colours=False))
    return o
def s4b():  # style 4 v2 (Aras 17:40): no dotted outline, no arrows, icons + titles outside the zone
    o = [bands(), veil(0.6)]
    for k in ORDER:
        o.append('<path d="%s" fill="#111" fill-opacity="0.06" stroke="#111" stroke-width="4"/>' % pth(RING[k]))
    for k in ORDER:
        c = cen(k); ys = [a[1] for a in RING[k]]
        if c[1] < 6650:   # block above the zone
            ty = min(ys) - 70; iy = ty - 130
        else:             # block below the zone
            iy = max(ys) + 70; ty = iy + 130
        for j, ic in enumerate(ICONS[k]):
            x = c[0] - 110 + j*110
            o.append('<circle cx="%.1f" cy="%.1f" r="46" fill="#111"/>' % (x, iy) + icon(ic, x, iy, 56, '#fff'))
        o.append(T(c[0], ty, INFO[k]['w'], 72, '#111', 'bold', 'middle', extra='stroke="#fff" stroke-width="12" paint-order="stroke"'))
        o.append(T(c[0], ty+46, INFO[k]['t'], 40, '#111', 'normal', 'middle', 'italic', 'stroke="#fff" stroke-width="10" paint-order="stroke"'))
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=False, size=0.95); o.append(s)
    o.append(foot('Who lives, works and visits around the river', 'Thin line = zone; icons = main uses (from OSM), placed beside each zone', colours=False))
    return o
def s4c():  # style 4 v3 (Aras 17:44): no outlines, light veil, colour see-through fills, all text below the map
    o = ['<rect x="200" y="7540" width="7630" height="700" fill="#fff"/>', veil(0.2)]
    for k in ORDER:
        h = INFO[k]['c']; rgb = [int(h[i:i+2], 16) for i in (1, 3, 5)]; pc = '#%02x%02x%02x' % tuple(round(v + (255 - v)*0.45) for v in rgb)
        o.append('<path d="%s" fill="%s" fill-opacity="0.20" stroke="none"/>' % (pth(RING[k]), pc))  # pastel (45% toward white), 20%
    for k in ORDER:
        c = cen(k); ys = [a[1] for a in RING[k]]; col = INFO[k]['c']
        if c[1] < 6650 and k != '3': ty = min(ys) - 60; iy = ty - 105   # label above the zone
        else: iy = max(ys) + 55; ty = iy + 105                          # label below (Bazaar too, to clear the site label)
        lx = c[0]; anc = 'middle'
        if k in ('DN', '5'):   # beside the zone (east), clear of the plan legend row under them
            xs = [a[0] for a in RING[k]]; lx = max(xs) + 60; anc = 'start'; iy = c[1] + 40; ty = iy + 105
        for j, ic in enumerate(ICONS[k]):
            x = (lx - 110 + j*110) if anc == 'middle' else (lx + 46 + j*110)
            o.append('<circle cx="%.1f" cy="%.1f" r="46" fill="%s"/>' % (x, iy, col) + icon(ic, x, iy, 56, '#fff'))
        o.append(T(lx, ty+10, INFO[k]['t'], 52, col, 'bold', anc, extra='stroke="#fff" stroke-width="10" paint-order="stroke"'))
    for i, k in enumerate(ORDER):
        s, bx = card(k, 240 + i*1085, 7570, w=1060, box=False, size=0.85); o.append(s)
    o.append(T(260, 8010, 'Who lives, works and visits around the river', 46, '#222', 'bold'))
    o.append(T(260, 8052, 'Colour = zone type (see-through fill); icons = main uses from OSM, placed beside each zone.', 26, '#555'))
    o.append(T(260, 8090, N1, 20, '#666') + T(260, 8114, N2, 20, '#666'))
    return o
def s5():  # thin red line drawing, hatched numbered zones, place dots, numbered legend
    o = [bands(), veil(0.72), '<defs><pattern id="h5" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="16" stroke="#D2332E" stroke-width="2.5"/></pattern></defs>']
    for i, k in enumerate(ORDER):
        o.append('<path d="%s" fill="url(#h5)" stroke="#D2332E" stroke-width="3"/>' % pth(RING[k]))
        c = cen(k); o.append(T(c[0], c[1]+40, str(i+1), 110, '#D2332E', 'bold', 'middle', extra='stroke="#fff" stroke-width="10" paint-order="stroke"'))
    for nm, k in KEYPL:
        if nm in NAMED:
            x, y = NAMED[nm]
            o.append('<circle cx="%.1f" cy="%.1f" r="13" fill="#B01E1E"/>' % (x, y) + T(x+20, y-14, nm.upper(), 24, '#111', 'bold', extra='stroke="#fff" stroke-width="6" paint-order="stroke"'))
    for i, k in enumerate(ORDER):
        x = 260 + (i % 4)*1340; y = 7620 + (i//4)*300
        o.append(T(x, y+34, '%d.  %s' % (i+1, INFO[k]['t']), 36, '#D2332E', 'bold'))
        o.append(T(x+44, y+72, INFO[k]['s'], 25, '#333', 'bold'))
        for j, b in enumerate(INFO[k]['b'][:3]): o.append(T(x+44, y+106+j*32, b, 24, '#333'))
    o.append(T(260, 5050, 'ZONES ALONG THE SELINOS', 60, '#D2332E', 'bold'))
    o.append(T(260, 5100, 'Red hatch = zone we read in the critique; red dot = named place from OSM; numbers match the legend below.', 30, '#333'))
    o.append(T(5600, 8090, N1, 20, '#666') + T(5600, 8116, N2, 20, '#666'))
    return o
def s6():  # radial dashed ring arcs, icons, coloured label boxes, legend
    o = [bands(), veil(0.2)]
    for k in ORDER:
        c = cen(k); r = rad(k) + 50; col = INFO[k]['c']
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="70" stroke-dasharray="6 10" stroke-opacity="0.75" transform="rotate(-90 %.1f %.1f)" pathLength="1000" stroke-dashoffset="0"/>' % (c[0], c[1], r, col, c[0], c[1]))
        o.append('<path d="%s" fill="%s" fill-opacity="0.12" stroke="%s" stroke-width="4" stroke-dasharray="20 10"/>' % (pth(RING[k]), col, col))
        lw = len(INFO[k]['t'])*25 + 120
        o.append('<rect x="%.1f" y="%.1f" width="%d" height="74" fill="%s" rx="6"/>' % (c[0]-lw/2, c[1]-37, lw, col))
        o.append(icon(INFO[k]['ic'], c[0]-lw/2+44, c[1]+2, 50, '#fff') + T(c[0]-lw/2+84, c[1]+15, INFO[k]['t'], 42, '#fff', 'bold'))
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=True, head=True, size=0.95); o.append(s)
    o.append(foot('Zone hubs', 'Ring of dashes = reach of each zone; box colour = zone type'))
    return o
def s7():  # striped ring hubs ("odak") + big zone names + dark place tags
    o = [bands(), veil(0.25)]
    for k in ORDER:
        c = cen(k); r = rad(k) + 40; col = INFO[k]['c']
        for rr, sw, op in ((r, 60, 0.7), (r + 90, 36, 0.4)):
            o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%d" stroke-dasharray="3 7" stroke-opacity="%g"/>' % (c[0], c[1], rr, col, sw, op))
        o.append(T(c[0], (min(c[1]+r+190, 7400) if c[1] > 6700 else max(c[1]-r-150, 5330)), (INFO[k]['t'] + ' hub').upper(), 54, '#6b6b6b', 'bold', 'middle', extra='letter-spacing="4" stroke="#fff" stroke-width="10" paint-order="stroke"'))
    for nm, k in KEYPL:
        if nm in NAMED:
            x, y = NAMED[nm]; w = len(nm)*15 + 70; col = INFO[k]['c']
            o.append('<circle cx="%.1f" cy="%.1f" r="22" fill="%s" stroke="#fff" stroke-width="4"/>' % (x, y, col) + icon(INFO[k]['ic'], x, y, 28, '#fff'))
            o.append('<rect x="%.1f" y="%.1f" width="%d" height="40" fill="#2F3B35" rx="6"/>' % (x+28, y-20, w) + T(x+44, y+9, nm, 25, '#fff', 'bold'))
    for k in ORDER:
        s, bx = card(k, *SLOT[k], box=True, size=0.95); o.append(s)
    o.append(foot('Focus hubs (odak)', 'Striped rings = each zone as a focus; dark tag = key place (OSM)'))
    return o
def s8():  # TOD: dotted yellow outlines, + x dot icons, legend, side key map I-VII with text
    o = [bands(), veil(0.3)]
    SYM = {'worship': ('#2E8B57', 'plus'), 'health': ('#1F6FD1', 'plus'), 'historic': ('#7A1E1E', 'dot'), 'food': ('#E07B00', 'dot'),
           'shop': ('#C0392B', 'x'), 'transport': ('#555', 'sq'), 'service': ('#8E44AD', 'x'), 'industry': ('#333', 'sq')}
    def sym(t, x, y):
        col, s = SYM[t]
        if s == 'plus': return '<path d="M%.1f,%.1f h28 M%.1f,%.1f v28" stroke="%s" stroke-width="8"/>' % (x-14, y, x, y-14, col)
        if s == 'x': return '<path d="M%.1f,%.1f l22,22 M%.1f,%.1f l-22,22" stroke="%s" stroke-width="7"/>' % (x-11, y-11, x+11, y-11, col)
        if s == 'sq': return '<rect x="%.1f" y="%.1f" width="20" height="20" fill="%s"/>' % (x-10, y-10, col)
        return '<circle cx="%.1f" cy="%.1f" r="11" fill="%s"/>' % (x, y, col)
    for i, k in enumerate(ORDER):
        o.append('<path d="%s" fill="#F4C430" fill-opacity="0.12" stroke="#E8B10E" stroke-width="12" stroke-dasharray="0.1 22" stroke-linecap="round"/>' % pth(RING[k]))
        c = cen(k); o.append(T(c[0], c[1]+30, rn(i), 80, '#C79200', 'bold', 'middle', extra='stroke="#fff" stroke-width="10" paint-order="stroke"'))
        for t, x, y, nm in POI[k]: o.append(sym(t, x, y))
    # legend
    lx, ly = 260, 7630
    o.append(T(lx, ly, 'LEGEND', 36, '#111', 'bold'))
    names = {'worship': 'Place of worship', 'health': 'Health', 'historic': 'Historic / archaeological', 'food': 'Restaurant, café, bakery',
             'shop': 'Shop', 'transport': 'Bus station, parking, fuel', 'service': 'Library, toilets, ticket, guest house', 'industry': 'Industrial site'}
    for j, (t, nm) in enumerate(names.items()):
        o.append(sym(t, lx+20, ly+50+j*42) + T(lx+56, ly+60+j*42, nm, 26, '#222'))
    o.append('<path d="M%d,%d h60" stroke="#E8B10E" stroke-width="12" stroke-dasharray="0.1 22" stroke-linecap="round"/>' % (lx+6, ly+400) + T(lx+86, ly+410, 'Character zone', 26, '#222'))
    # key map (scaled zones) + text
    kx, ky, ks = 1120, 7600, 0.085
    o.append('<g transform="translate(%g,%g) scale(%g) translate(-200,-5240)"><rect x="200" y="5240" width="7630" height="2190" fill="#f3f3f0"/>' % (kx, ky, ks) +
             '<polyline points="%s" fill="none" stroke="#9BB8D8" stroke-width="40"/>' % ' '.join('%.1f,%.1f' % a for a in RIV) +
             ''.join('<path d="%s" fill="#F4C430" stroke="#C79200" stroke-width="20"/>' % pth(RING[k]) for k in ORDER) +
             ''.join(T(cen(k)[0], cen(k)[1]+90, rn(i), 260, '#7a5a00', 'bold', 'middle') for i, k in enumerate(ORDER)) + '</g>')
    o.append(T(kx, ky-6, 'Key map', 24, '#555', 'bold'))
    for i, k in enumerate(ORDER):
        x = 1830 + (i % 4)*1280; y = 7620 + (i//4)*300
        o.append(T(x, y+30, '%s. %s' % (rn(i), INFO[k]['t']), 34, '#C79200', 'bold'))
        o.append(T(x, y+64, INFO[k]['s'], 24, '#333', 'bold'))
        for j, b in enumerate(INFO[k]['b'][:3]): o.append(T(x, y+96+j*30, b, 22, '#333'))
        o.append(T(x, y+186, 'Users: ' + INFO[k]['u'], 22, '#555', style='italic'))
    o.append(T(260, 5050, 'CHARACTER ZONES AROUND THE PROJECT', 60, '#111', 'bold'))
    o.append(T(260, 5100, 'Dotted yellow = zone; symbols = every OSM shop, amenity and historic place inside each zone.', 30, '#333'))
    o.append(T(5600, 8090, N1, 20, '#666') + T(5600, 8116, N2, 20, '#666'))
    return o
def s9():  # urban interface: yellow gradient fans from the river, letters, arrows, underlined titles
    o = [bands(), veil(0.25), '<defs><marker id="ah9" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#111"/></marker>']
    for k in ORDER:
        c = cen(k); r = RN[k]
        o[-1] += '<linearGradient id="g9%s" gradientUnits="userSpaceOnUse" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"><stop offset="0" stop-color="#F2B705" stop-opacity="0.85"/><stop offset="1" stop-color="#F2B705" stop-opacity="0.08"/></linearGradient>' % (k, r[0], r[1], c[0], c[1])
    o[-1] += '</defs>'
    o.append('<polyline points="%s" fill="none" stroke="#111" stroke-width="14"/>' % ' '.join('%.1f,%.1f' % a for a in RIV))
    for i, k in enumerate(ORDER):
        r = RN[k]; idx = RIV.index(r)
        span = [RIV[j] for j in range(max(0, idx-12), min(len(RIV), idx+13))]
        hp = hull(RING[k] + span)
        o.append('<path d="%s" fill="url(#g9%s)" stroke="none"/>' % (pth(hp), k))
        c = cen(k); L = 'abcdefg'[i]
        o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#111" stroke-width="5" marker-end="url(#ah9)"/>' % (r[0], r[1], c[0], c[1]))
        o.append('<circle cx="%.1f" cy="%.1f" r="38" fill="#fff" stroke="#111" stroke-width="5"/>' % (c[0], c[1]) + T(c[0], c[1]+15, L, 44, '#111', 'bold', 'middle'))
    for i, k in enumerate(ORDER):
        x, y = SLOT[k]; L = 'abcdefg'[i]
        o.append(T(x, y+56, '%s)  %s' % (L, INFO[k]['t'].lower()), 48, '#111', 'bold'))
        o.append('<rect x="%d" y="%d" width="%d" height="4" fill="#111"/>' % (x, y+70, len(INFO[k]['t'])*26 + 90))
        o.append(T(x, y+110, INFO[k]['s'], 28, '#555', 'bold'))
        for j, b in enumerate(INFO[k]['b'] + ['Users: ' + INFO[k]['u']]): o.append(T(x+14, y+150+j*36, b, 26, '#333', style='italic' if b.startswith('Users') else 'normal'))
    o.append(T(5500, 7660, 'URBAN INTERFACE', 60, '#111', 'bold'))
    o.append(T(5500, 7710, 'Black line = Selinos edge (our river park).', 28, '#333'))
    o.append(T(5500, 7750, 'Yellow fan = how each zone opens onto the river;', 28, '#333'))
    o.append(T(5500, 7790, 'arrow = from the river into the zone; letters match the text.', 28, '#333'))
    o.append(T(5500, 8090, N1, 20, '#666') + T(5500, 8116, N2, 20, '#666'))
    return o

STYLES = [('01_ellipses_bullets', s1), ('02_daily_life_circles', s2), ('03_flat_colour_areas', s3), ('04_icons_natural_urban', s4),
          ('04b_icons_natural_urban_v2', s4b), ('04c_icons_natural_urban_v3', s4c), ('05_red_hatch_numbered', s5), ('06_radial_rings_boxes', s6), ('07_striped_hubs', s7), ('08_character_zones_keymap', s8),
          ('09_urban_interface_fans', s9)]
if __name__ == '__main__':
    base = open(sys.argv[1], encoding='utf8').read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    only = sys.argv[3:]
    import re
    base = re.sub(r'viewBox="[^"]+"', 'viewBox="%g %g %g %g"' % VB, base, count=1)
    base = re.sub(r'width="[^"]+px" height="[^"]+px"', 'width="6000px" height="%dpx"' % round(6000*VB[3]/VB[2]), base, count=1)
    cut = base.rfind('</svg>')
    for name, fn in STYLES:
        if only and name[:2] not in only: continue
        b2 = base
        if name.startswith('04c'):
            b2 = re.sub(r'viewBox="[^"]+"', 'viewBox="200 5240 7630 2900"', b2, count=1)
            b2 = re.sub(r'width="6000px" height="[0-9]+px"', 'width="6000px" height="%dpx"' % round(6000*2900/7630), b2, count=1)
        g = '<g id="zones_%s">%s</g>' % (name, '\n'.join(fn()))
        open(out + '/zones_%s.svg' % name, 'w', encoding='utf8').write(b2[:cut] + g + b2[cut:])
        print(name, len(POI['3']))
