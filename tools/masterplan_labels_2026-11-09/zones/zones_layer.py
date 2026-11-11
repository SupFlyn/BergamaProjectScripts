# Layer-only SVG of zones style 4 v5, same page/viewBox as his plan file B19_setB_layers2_0600.svg (drops in 1:1).
import os, sys
os.environ['ZONES'] = 'zones_v2.json'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_zones as b
o = b.s4c(); n = len(b.ORDER); NAME = {k: b.INFO[k]['t'].replace(' ', '_') for k in b.ORDER}
fills = o[2:2+n]; labels = o[2+n:2+n+4*n]; cards = o[2+5*n:2+6*n]; tail = o[2+6*n:]
assert len(tail) == 3, len(tail)
def g(i, body): return '<g id="%s">%s</g>' % (i, body)
L = [g('map_light_wash_white_20pc', o[1]),
     g('zone_fills', ''.join(g('fill_' + NAME[k], f) for k, f in zip(b.ORDER, fills))),
     g('zone_icons_and_titles', ''.join(g('label_' + NAME[k], ''.join(labels[4*i:4*i+4])) for i, k in enumerate(b.ORDER))),
     g('explanations_below_map', g('panel_white_background', o[0]) + ''.join(g('text_' + NAME[k], c) for k, c in zip(b.ORDER, cards))
       + g('key_title', tail[0] + tail[1]) + g('sources_note', tail[2]))]
svg = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="295.354cm" height="386.934cm" viewBox="0 0 8372.233 10968.204">\n'
       + g('layer_12_zones_v5', '\n'.join(L)) + '\n</svg>\n')
out = sys.argv[1]; open(out, 'w', encoding='utf8').write(svg); print(out, len(svg))
