# Depth-toned copies of the style a cutouts (R2-A 31 Oct 2026, Aras: nearer = stronger, farther = paler; never
# see-through). For every cutout: <name>_d1.png and <name>_d2.png, colours mixed toward the section paper by the
# FIG_DEPTH fade of layers 1 and 2 (common/figures.py), alpha unchanged (opaque bodies stay opaque); cutouts.json
# entries get "depth": {"1": file, "2": file}, read by figures.py cut_image().
# usage: python3 -I tools/cutouts/depth_tones.py <cutouts folder>
import sys, json, os
from PIL import Image
OUT = sys.argv[1]
PAPER = (0xF1, 0xED, 0xDF)            # section_parts SEC["paper"]
FADE = {"1": 0.40, "2": 0.62}         # figures.py FIG_DEPTH[layer][1]
js = json.load(open(os.path.join(OUT, 'cutouts.json'), encoding='utf-8'))
cut = js['cutouts']
done = {}
for key, v in cut.items():
    for e in (v if isinstance(v, list) else [v]):
        fn = e['file']
        if fn not in done:
            im = Image.open(os.path.join(OUT, fn)).convert('RGBA')
            r, g, b, a = im.split()
            files = {}
            for lay, f in FADE.items():
                ch = [c.point(lambda x, p=p, f=f: int(round(x + (p - x) * f))) for c, p in zip((r, g, b), PAPER)]
                out = fn[:-4] + '_d%s.png' % lay
                Image.merge('RGBA', ch + [a]).save(os.path.join(OUT, out), interlace=False)
                files[lay] = out
            done[fn] = files
        e['depth'] = done[fn]
json.dump(js, open(os.path.join(OUT, 'cutouts.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('toned copies:', 2 * len(done), 'files for', len(done), 'cutouts')
