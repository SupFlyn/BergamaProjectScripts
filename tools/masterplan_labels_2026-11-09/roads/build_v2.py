# v2 (Aras 9 Nov 16:00): clean even-width roads, red dotted only near the south side of the Selinos (edges, no centre dash),
# Kizil Avlu circulation in dashed blue + link to our route. Units = his 09:00 file (viewBox 0 0 8372.233 10968.204).
import json, os, sys, math, html
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from tfm import to_plan
OUT = D + '/../../roads_v2/'; os.makedirs(OUT, exist_ok=True)
HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="295.354cm" height="386.934cm" viewBox="0 0 8372.233 10968.204">\n'
FT = 'font-family="Arial, ArialMT"'
K = 6000 / 7630; X0, Y0 = 200, 5240                      # mask frame of the 6000 px renders
ROAD = np.array(Image.open(D + '/b_roads_streets.png').convert('L')) < 128
SEL = np.array(Image.open(D + '/selinos_mask.png').convert('L')) < 128
H, W = ROAD.shape
F = {i: (k, t, p) for k, i, t, p in json.load(open(D + '/feat.json'))}
RES = {r['i']: r for r in json.load(open(D + '/osm_res.json'))}
PATH = {'footway', 'steps', 'pedestrian', 'path', 'track', 'cycleway'}
MAIN = {'trunk', 'primary', 'secondary'}
LOW = ['371130187', '1350426789', '371130159']            # lower-edge road: drawn on its real centre line
def pl(i): return [to_plan(*q) for q in F[i][2]]
def pts(P): return ' '.join('%.1f,%.1f' % tuple(q) for q in P)
def gid(s): return ''.join(c if c.isalnum() or c in '-_' else '_' for c in s.replace(' ', '_'))
def pix(x, y): return int((y - Y0) * K), int((x - X0) * K)
def onmask(M, x, y):
    r, c = pix(x, y); return 0 <= r < H and 0 <= c < W and M[r, c]
def dens(P, step=4.0):
    out = []
    for a, b in zip(P, P[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        out += [(a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n) for j in range(n)]
    return out + [P[-1]]
def dp(P, tol):                                             # Douglas-Peucker
    if len(P) < 3: return P
    a, b = np.array(P[0]), np.array(P[-1]); d = b - a; L = np.hypot(*d) or 1e-9
    dist = [abs(d[0] * (p[1] - a[1]) - d[1] * (p[0] - a[0])) / L for p in P[1:-1]]
    j = int(np.argmax(dist))
    if dist[j] > tol: return dp(P[:j + 2], tol)[:-1] + dp(P[j + 1:], tol)
    return [P[0], P[-1]]
def chaikin(P, n=2):
    for _ in range(n):
        if len(P) < 3: return P
        Q = [P[0]]
        for a, b in zip(P, P[1:]):
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        P = Q + [P[-1]]
    return P
def smooth(P): return chaikin(dp(P, 2.5), 2)
def width_at(x, y, nx, ny):                                 # his drawn road width across the line, from the mask
    w = 0
    for s in (1, -1):
        t = 0.0
        while t < 40 and onmask(ROAD, x + s * nx * t, y + s * ny * t): t += 0.6
        w += t
    return w
def runs(S, keep):                                          # split a sampled line into the runs where keep is True
    out, cur = [], []
    for p, k in zip(S, keep):
        if k: cur.append(p)
        elif cur:
            if len(cur) > 2: out.append(cur)
            cur = []
    if len(cur) > 2: out.append(cur)
    return out
def offset(P, d):
    out = []
    for j in range(len(P)):
        a = P[max(0, j - 1)]; b = P[min(len(P) - 1, j + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1e-9
        out.append((P[j][0] - ty / L * d, P[j][1] + tx / L * d))
    return out
EXT = (205, 7825, 5245, 7545)
def inext(p): return EXT[0] < p[0] < EXT[1] and EXT[2] < p[1] < EXT[3]
# ---------------- roads: OSM centre line where his road is, at his own measured width ----------------
roads = {}; widths = {}
for i, (k, t, p) in F.items():
    if k != 'w' or 'highway' not in t or t['highway'] in PATH or t.get('tunnel') == 'yes': continue
    if i not in RES: continue
    S = [q for q in dens(pl(i)) if inext(q)]
    if len(S) < 3: continue
    keep = [True] * len(S) if i in LOW else [any(onmask(ROAD, x + dx, y + dy) for dx in (-7, 0, 7) for dy in (-7, 0, 7)) for x, y in S]
    rr = runs(S, keep)
    if not rr: continue
    ws = []
    for r in rr:
        for j in range(1, len(r) - 1, 3):
            tx, ty = r[j + 1][0] - r[j - 1][0], r[j + 1][1] - r[j - 1][1]; L = math.hypot(tx, ty) or 1e-9
            w = width_at(r[j][0], r[j][1], -ty / L, tx / L)
            if 2 < w < 70: ws.append(w)
    roads[i] = rr; widths[i] = float(np.median(ws)) if len(ws) >= 3 else None
cls = lambda h: 'main_roads' if h in MAIN else 'streets'
med = {c: float(np.median([w for i, w in widths.items() if w and cls(F[i][1]['highway']) == c])) for c in ('main_roads', 'streets')}
for i in widths:
    if widths[i] is None or i in LOW: widths[i] = med[cls(F[i][1]['highway'])]
    widths[i] = round(min(max(widths[i], 6.0), 45.0), 1)
COL = '#E4E4E4'
o = [HEAD, '<g id="ROADS_around_the_site_v2">\n']
for c in ('main_roads', 'streets'):
    o.append('<g id="%s">' % c)
    byname = {}
    for i, rr in roads.items():
        if cls(F[i][1]['highway']) != c: continue
        nm = F[i][1].get('name') or 'unnamed'
        for r in rr:
            byname.setdefault(nm, []).append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>' % (pts(smooth(r)), COL, widths[i]))
    for nm in sorted(byname): o.append('<g id="%s_%s">%s</g>' % (c[:4], gid(nm), ''.join(byname[nm])))
    o.append('</g>\n')
o.append('</g>\n</svg>\n')
open(OUT + 'layer_8_roads_v2.svg', 'w').write(''.join(o))
# coverage check: how much of his road surface the clean roads cover
print('roads', len(roads), 'widths median', med)
# ---------------- red dotted: only near the south (lower) side of the Selinos ----------------
cols = np.where(SEL.any(0))[0]
ymid = {c: np.where(SEL[:, c])[0].mean() for c in cols}
def river_y(x):
    c = int((x - X0) * K)
    if c in ymid: return Y0 + ymid[c] / K
    near = cols[np.argmin(abs(cols - c))]
    return Y0 + ymid[near] / K if abs(near - c) < 60 * K else None
SOUTH = 300                                                  # units below the river centre (~114 m)
RED = '#C0392B'
o = [HEAD, '<g id="RED_DOTTED_south_of_the_Selinos">\n']
for i, (k, t, p) in F.items():
    if k != 'w' or 'highway' not in t or i in LOW or i in roads or t.get('tunnel') == 'yes': continue
    r = RES.get(i)
    if not r or r['cov'] >= 0.5 or r['near'] <= 0.7: continue
    S = [q for q in dens(pl(i)) if inext(q)]
    keep = []
    for x, y in S:
        ry = river_y(x); keep.append(ry is not None and 0 < y - ry < SOUTH)
    for rr in runs(S, keep):
        if len(rr) * 4 < 40: continue
        P = smooth(rr); h = t['highway']; nm = gid(t.get('name') or 'unnamed')
        if h in PATH:
            o.append('<g id="path_%s_%s"><polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="0.1 4.5" stroke-linecap="round"/></g>' % (i, nm, pts(P), RED))
        else:
            w = med[cls(h)] / 2
            o.append('<g id="road_%s_%s">' % (i, nm) + ''.join('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="0.1 4.5" stroke-linecap="round"/>' % (pts(offset(P, s * w)), RED) for s in (1, -1)) + '</g>')
o.append('</g>\n</svg>\n')
open(OUT + 'layer_11_red_dotted_south_selinos.svg', 'w').write(''.join(o))
print('red dotted groups', sum(1 for s in o if s.startswith('<g id="path') or s.startswith('<g id="road')))
# ---------------- Kizil Avlu circulation (OSM footways/paths/service inside + round the site wall) ----------------
wall = pl('220480903')
def inside(pt, ring):
    x, y = pt; c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
BLUE = '#1F6FD1'
inner = []
for i, (k, t, p) in F.items():
    if k != 'w' or t.get('highway') not in ('footway', 'path', 'pedestrian', 'steps', 'service') or t.get('tunnel') == 'yes': continue
    P = pl(i); S = dens(P)
    dw = [min(math.hypot(q[0] - a, q[1] - b) for a, b in dens(wall, 6)) for q in S[::3]]
    if np.mean([inside(q, wall) for q in S]) > 0.3 or np.mean([d < 25 for d in dw]) > 0.5: inner.append((i, P))
gates = [(i, t['barrier'], to_plan(*p[0])) for i, (k, t, p) in F.items() if k == 'n' and t.get('barrier') in ('gate', 'turnstile') and inside(to_plan(*p[0]), wall) or (k == 'n' and t.get('barrier') in ('gate', 'turnstile') and min(math.hypot(to_plan(*p[0])[0] - a, to_plan(*p[0])[1] - b) for a, b in wall) < 12)]
R = np.array([q for l in json.load(open(D + '/route.json')) for q in l])
turn = [g for g in gates if g[1] == 'turnstile'][0][2]
rot = pl('1222770549'); rx0 = min(a for a, b in rot); rcy = sum(b for a, b in rot) / len(rot)
end = R[np.argmin(np.hypot(*(R - [rot[0][0], rot[0][1] + 60]).T))]
link = [turn, (rx0 - 14, rcy), (float(end[0]), float(end[1]))]
o = [HEAD, '<g id="KIZIL_AVLU_circulation">\n']
o.append('<g id="paths_inside_the_site_existing_OSM">%s</g>\n' % ''.join('<polyline id="osm_%s" points="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="6 4" stroke-linecap="round" stroke-linejoin="round"/>' % (i, pts(P if P[0] == P[-1] else chaikin(dp(P, 1.2), 2)), BLUE) for i, P in inner))
o.append('<g id="gates_and_turnstile_OSM">%s</g>\n' % ''.join('<g id="%s_%s"><circle cx="%.1f" cy="%.1f" r="4.5" fill="#FFFFFF" stroke="%s" stroke-width="1.6"/></g>' % (b, i, x, y, BLUE) for i, b, (x, y) in gates))
o.append('<g id="Selinos_tunnel_under_the_courtyard_OSM"><polyline points="%s" fill="none" stroke="%s" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.8"/></g>\n' % (pts(pl('220481134')), BLUE))
o.append('<g id="proposed_link_to_our_route"><polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-dasharray="10 5" stroke-linecap="round" stroke-linejoin="round"/>' % (pts(chaikin(link, 3)), BLUE))
o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/></g>\n' % (end[0], end[1], BLUE))
# small key
kx, ky = 2560, 6175
o.append('<g id="key_Kizil_Avlu_circulation"><rect x="%g" y="%g" width="214" height="62" fill="#FFFFFF" fill-opacity="0.85" stroke="%s" stroke-width="1"/>' % (kx, ky, BLUE))
o.append('<text x="%g" y="%g" %s font-size="11" font-weight="bold" fill="%s">Kızıl Avlu circulation</text>' % (kx + 8, ky + 14, FT, BLUE))
o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.8" stroke-dasharray="6 4"/><text x="%g" y="%g" %s font-size="8.4" fill="#1E1E1E">existing paths inside (OpenStreetMap)</text>' % (kx + 8, ky + 27, kx + 34, ky + 27, BLUE, kx + 40, ky + 30, FT))
o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.2" stroke-dasharray="2 3"/><text x="%g" y="%g" %s font-size="8.4" fill="#1E1E1E">Selinos in its tunnel (OpenStreetMap)</text>' % (kx + 8, ky + 53, kx + 34, ky + 53, BLUE, kx + 40, ky + 56, FT))
o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2.6" stroke-dasharray="10 5"/><text x="%g" y="%g" %s font-size="8.4" fill="#1E1E1E">link to our riverside route (proposed)</text></g>\n' % (kx + 8, ky + 40, kx + 34, ky + 40, BLUE, kx + 40, ky + 43, FT))
o.append('</g>\n</svg>\n')
open(OUT + 'layer_10_kizil_avlu_circulation.svg', 'w').write(''.join(o))
print('kizil avlu paths', len(inner), 'gates', [(b, round(x), round(y)) for i, b, (x, y) in gates], 'link', [tuple(map(round, q)) for q in link], 'length m %.0f' % (sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(link, link[1:])) / 2.641))
