# step 2 of v2: his road shapes that the clean OSM roads do not cover (no map match) are kept as he drew them, same grey.
import json, os, copy
import numpy as np
from PIL import Image, ImageFilter
from lxml import etree
D = os.path.dirname(os.path.abspath(__file__)); K = 6000 / 7630
N = np.array(Image.open(D + '/n_roads.png').convert('L').point(lambda v: 255 if v < 128 else 0).filter(ImageFilter.MaxFilter(15))) > 0
H, W = N.shape
CL = {c['i']: c for c in json.load(open(D + '/his_cls.json'))}
LOWNAMES = {'Bergama - Kozak Yolu', 'Cami Kebir Caddesi'}
keep = []
for r in json.load(open(D + '/his_roads.json')):
    P = [(int((y - 5240) * K), int((x - 200) * K)) for x, y in r['pts']]
    P = [(a, b) for a, b in P if 0 <= a < H and 0 <= b < W]
    if not P: continue
    lost = np.mean([not N[a, b] for a, b in P])
    if lost > 0.5 and CL[r['i']]['name'] not in LOWNAMES and r['i'] != 437: keep.append(r['i'])   # 437 = his lower-edge road, replaced by its real line
P = etree.XMLParser(huge_tree=True); NS = 'http://www.w3.org/2000/svg'
his = etree.parse(D + '/../../inputs/B19_setB_layers2_0600.svg', P)
els = [e for e in his.xpath('//*[@id="roads_streets"]')[0].iter() if isinstance(e.tag, str) and e.tag.split('}')[1] in ('path', 'polygon', 'polyline', 'line', 'rect')]
out = []
for n in keep:
    e = copy.deepcopy(els[n])
    for a in ('clip-path', 'class', 'opacity'): e.attrib.pop(a, None)
    if e.get('fill') == 'none': e.set('stroke', '#E4E4E4')
    else:
        e.set('fill', '#E4E4E4'); e.attrib.pop('stroke', None)
    out.append(etree.tostring(e, encoding='unicode').replace(' xmlns="%s"' % NS, ''))
f = D + '/../../roads_v2/layer_8_roads_v2.svg'
s = open(f).read()
s = s.replace('</g>\n</svg>\n', '<g id="kept_as_you_drew_no_map_match">%s</g>\n</g>\n</svg>\n' % ''.join(out), 1) if 'kept_as_you_drew' not in s else s
open(f, 'w').write(s)
print('kept as drawn:', len(keep), keep)
