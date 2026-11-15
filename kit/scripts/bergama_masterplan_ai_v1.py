# -*- coding: utf-8 -*-
"""Bergama Group 6: MASTERPLAN AI v1 (15 Nov 2026): Aras's newest masterplan SVG made Illustrator-ready and handed to
every script as Data/assets/plan/master.svg.

Aras 15 Nov 16:15 UTC: "here is the newest and latest masterplan svg use it and replace it where needed. Dont forget to
turn that svg that can be readable by illustrator with a script or something and supply that version into the
scripts"; "also place our dashed line for working area" + 16:20 "this is for masterplan aswell"; 16:20 "reduce these
trees and bushes opacity to %70"; 16:21 "produce one more alternative to that change those trees and bushes with ones
that looks similar to our these trees you can use our asset library".

Reads   Data/assets/plan/masterplan.svg (his file as delivered; if missing, joins Data/assets/plan/parts/
        masterplan.svg.part* and checks their md5 against masterplan.svg.md5), the Basemap cache (site_alan + the
        calisma working-area rings), the newest MasterplanBase script (its SVG reader and placing, nothing copied),
        Data/bergama_access_heritage.json (key "study": the working-area colour and width every map uses),
        Data/bergama_b19_plan_data.py TREE_EMBED (his painted tree set, traced; for version B only).
Writes  Data/assets/plan/master_A.svg  his planting, trees + bushes at 70 % opacity
        Data/assets/plan/master_B.svg  the same, trees + bushes swapped for flat round symbols of his painted set
                                       recoloured to his reference (sage, grey-blue, mauve, pink, orange)
        Data/assets/plan/master.svg    = A (input planting_b False) or B (True): what every script reads
        Data/assets/plan/archive/master_<date>.svg  the master.svg that was there before (once; never deleted)
Both A and B: the C2PA <metadata> block dropped (Illustrator does not need it), any rgba()/hsla() colour turned into
#RRGGBB + opacity (Illustrator reads rgba as black, 11 Nov), and our working-area dashed line added as the TOPMOST
layer "working_area" (Aras 14:45 UTC: the working-area dash is the topmost line of every drawing). Nothing else of
his file changes: his layer ids and names, groups, pictures and colours stay as they are.
"""
import os, re, json, math, time, glob, shutil, hashlib

VERSION = "v1"
GH_LABEL = "MasterplanAI"
OUT_FOLDER = "bergama_masterplan_ai"
LOG_NAME = "bergama_masterplan_ai_log.txt"
GH_INPUTS = {"planting_b": "bool", "rebuild": "bool"}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
PLAN_DIR = os.path.join(BERGAMA_ROOT, "Data", "assets", "plan")
IN_SVG = "masterplan.svg"
OUT_SVG, OUT_A, OUT_B = "master.svg", "master_A.svg", "master_B.svg"
STAMP_FILE = "master_ai_stamp.json"
MARK = u"MasterplanAI"                          # in a comment at the top of every file this script writes
SVG_NS, XL_NS = "http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink"
PLACE_GROUP = "ev-yol"                         # his existing roads + buildings: their box = site_alan (MasterplanBase)
BASEMAP_CACHE = os.path.join("cached", "bergama_basemap", "basemap_layers.json")
STYLE_JSON = os.path.join("Data", "bergama_access_heritage.json")
WORK_ID, WORK_NAME = "working_area", "working area"
WORK_DASH_MM = (2.4, 0.8)                      # pages_common pc_study's dash on every map
PT_MM = 25.4 / 72.0                            # his SVG unit = 1 pt (width in cm / viewBox width)
SOFT_IDS = ("agaclar", "assets")               # his trees (agaclar, with PLANTING_v13_1) and bushes (assets)
SOFT_OPACITY = "0.7"                           # Aras 16:20 UTC "reduce these trees and bushes opacity to %70"
PLANTING_ID = "PLANTING_v13_1"                 # its own .81 is dropped so the trees read 70 %, not 57 %
# ---- version B: his painted set (library/tree_assets_2026-11-06/contact_sheet.png), picked by look against his
# reference (16:21 UTC): flat round crowns, faint inner rings or rays; colours sampled from his reference picture
B_SPECIES = {"plane": ("S004", "919B90"), "stone_pine": ("S003", "919B90"), "ash": ("S005", "DCAE81"),
             "willow": ("S006", "8DA1AC"), "olive": ("S021", "8DA1AC"), "tamarisk": ("S063", "CAA6B9"),
             "rosemary": ("S062", "AE8E9B")}
B_BUSH = (("S063", "CAA6B9"), ("S065", "919B90"), ("S062", "AE8E9B"))   # loose plants, in turn
B_PLANT_M = (0.5, 15.0)                        # m: a group this size (its box's long side) is one plant
B_SHADE = (0.32, 0.30)                         # the darkest band mixed this far to black, the lightest to white


# ================================================================ helpers
def md5_of(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def input_svg(log):
    p = os.path.join(PLAN_DIR, IN_SVG)
    parts = sorted(glob.glob(os.path.join(PLAN_DIR, "parts", IN_SVG + ".part*")))
    if not os.path.isfile(p) and parts:
        tmp = p + ".joining"
        with open(tmp, "wb") as out:
            for q in parts:
                with open(q, "rb") as f:
                    shutil.copyfileobj(f, out)
        want = os.path.join(PLAN_DIR, "parts", IN_SVG + ".md5")
        got = md5_of(tmp)
        if os.path.isfile(want) and open(want).read().split()[0].strip() != got:
            os.remove(tmp)
            raise RuntimeError(u"the %d parts in %s join to md5 %s, not the one in %s: copy the parts again"
                               % (len(parts), os.path.dirname(want), got, want))
        os.replace(tmp, p)
        log.append(u"joined %d parts into %s (md5 %s)" % (len(parts), p, got))
    if not os.path.isfile(p):
        raise RuntimeError(u"his newest masterplan is missing: copy masterplan.svg into %s, then press again" % PLAN_DIR)
    return p


def mb_lib(log):
    """the newest MasterplanBase script's code above its main: read_svg, world_matrix, site_alan, path helpers"""
    ps = glob.glob(os.path.join(BERGAMA_ROOT, "scripts", "bergama_masterplanbase_v*.py"))
    if not ps:
        raise RuntimeError(u"no bergama_masterplanbase_v*.py in %s\\scripts: run Bergama.bat once" % BERGAMA_ROOT)
    p = max(ps, key=lambda q: [int(x) for x in re.findall(r"\d+", os.path.basename(q))])
    code = open(p, encoding="utf-8").read()
    ns = {"__name__": "bergama_masterplanbase_lib"}
    exec(compile(code[:code.index("\n# ================================================================ main\n")], p, "exec"), ns)
    ns["BERGAMA_ROOT"] = BERGAMA_ROOT
    log.append(u"MasterplanBase code from %s" % os.path.basename(p))
    return ns


def group_span(txt, gid, start=0):
    """(i0, i1) of <g id="gid" ...> ... </g> in txt (nested <g> counted), or None"""
    m = re.search(r'<g\b[^>]*\bid="%s"' % re.escape(gid), txt[start:]) if start else \
        re.search(r'<g\b[^>]*\bid="%s"' % re.escape(gid), txt)
    if not m:
        return None
    i0 = m.start() + start
    depth, pos = 0, i0
    tag = re.compile(r"<g\b[^>]*?(/?)>|</g>")
    while True:
        t = tag.search(txt, pos)
        if t is None:
            return None
        if t.group(0) == "</g>":
            depth -= 1
        elif t.group(1) != "/":
            depth += 1
        pos = t.end()
        if depth == 0:
            return i0, pos


def set_attr(open_tag, name, value):
    """an opening tag with attribute name set (value None = removed)"""
    s = re.sub(r'\s%s="[^"]*"' % re.escape(name), "", open_tag)
    if value is None:
        return s
    return re.sub(r"(/?>)$", u' %s="%s"\\1' % (name, value), s, count=1)


def rgba_fix(txt, log):
    """fill/stroke="rgba(r,g,b,a)" or hsla -> #RRGGBB + fill-/stroke-opacity (Illustrator reads rgba as black)"""
    n = [0]

    def hsl(h, s, l):
        import colorsys
        r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
        return r * 255, g * 255, b * 255

    def rep(m):
        n[0] += 1
        k, fn, v = m.group(1), m.group(2), [x.strip() for x in m.group(3).split(",")]
        num = lambda x: float(x.rstrip("%")) / (100.0 if x.endswith("%") else 1.0)
        a = num(v[3]) if len(v) > 3 else 1.0
        if fn == "rgba":
            r, g, b = [num(x) * (255.0 if x.endswith("%") else 1.0) for x in v[:3]]
        else:
            r, g, b = hsl(float(v[0]), num(v[1]), num(v[2]))
        return u'%s="#%02x%02x%02x" %s-opacity="%.3f"' % (k, int(round(r)), int(round(g)), int(round(b)), k, a)
    txt = re.sub(r'\b(fill|stroke)="\s*(rgba|hsla)\(([^)]*)\)\s*"', rep, txt)
    if "rgba(" in txt or "hsla(" in txt or "var(" in txt:
        log.append(u"FLAG rgba / hsla / var() left in a style or class: Illustrator may draw those black")
    log.append(u"rgba / hsla colours turned into hex + opacity: %d" % n[0])
    return txt


# ================================================================ the working-area layer
def working_layer(txt, ns, log):
    """our dashed working-area line in his SVG units, as the group string, and the units per m"""
    sp = group_span(txt, PLACE_GROUP)
    if sp is None:
        raise RuntimeError(u"no group %s in his SVG: it places the plan (MasterplanBase), so no working area" % PLACE_GROUP)
    tmp = os.path.join(PLAN_DIR, "_ev_yol_tmp.svg")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(u'<svg xmlns="%s" xmlns:xlink="%s">%s</svg>' % (SVG_NS, XL_NS, txt[sp[0]:sp[1]]))
    try:
        _l, _t, box = ns["read_svg"](tmp, [])
    finally:
        os.remove(tmp)
    if box[0] > box[2]:
        raise RuntimeError(u"group %s has no drawing in it" % PLACE_GROUP)
    W, upm = ns["world_matrix"](ns["site_alan"](log), (box[0], box[1], box[2] - box[0], box[3] - box[1]), log)
    a, b, c, d, e, f_ = W
    det = a * d - b * c
    inv = lambda q: ((d * (q[0] - e) - c * (q[1] - f_)) / det, (-b * (q[0] - e) + a * (q[1] - f_)) / det)
    with open(os.path.join(BERGAMA_ROOT, BASEMAP_CACHE), encoding="utf-8") as f:
        cal = json.load(f).get("calisma") or []
    if not cal:
        log.append(u"FLAG no calisma ring in the Basemap cache: no working-area line (press Basemap once)")
        return u"", upm
    col, w_mm = "4C2528", 0.3
    try:
        with open(os.path.join(BERGAMA_ROOT, STYLE_JSON), encoding="utf-8") as f:
            col, w_mm = json.load(f)["key"]["study"][:2]
    except Exception as ex:
        log.append(u"FLAG working-area style not read (%s): 4C2528 0.3 mm used" % ex)
    rows = []
    for R in cal:
        P = [inv(q[:2]) for q in R]
        rows.append(u'<polygon points="%s" fill="none" stroke="#%s" stroke-width="%.3f" stroke-dasharray="%.3f %.3f" '
                    u'stroke-linecap="butt" stroke-linejoin="round"/>' % (
                        u" ".join(u"%.3f %.3f" % p for p in P), col.lstrip("#"), w_mm / PT_MM,
                        WORK_DASH_MM[0] / PT_MM, WORK_DASH_MM[1] / PT_MM))
    log.append(u"working area: %d ring(s), #%s %.2f mm, dash %.1f / %.1f mm, on top of every layer"
               % (len(rows), col.lstrip("#"), w_mm, WORK_DASH_MM[0], WORK_DASH_MM[1]))
    return u'<g id="%s" data-name="%s">%s</g>' % (WORK_ID, WORK_NAME, u"".join(rows)), upm


# ================================================================ version B: his painted set, recoloured
def tree_set(log):
    import zlib, base64
    p = os.path.join(BERGAMA_ROOT, "Data", "bergama_b19_plan_data.py")
    L = open(p, encoding="utf-8").read().split("\n")
    i = next(i for i, l in enumerate(L) if l.startswith("TREE_EMBED = ("))
    j = next(j for j in range(i + 1, len(L)) if L[j].startswith(")"))
    J = json.loads(zlib.decompress(base64.b64decode("".join(l.strip().strip(",").strip('"') for l in L[i + 1:j])))
                   .decode("utf-8"))
    by = dict((s["id"], s) for s in J["symbols"])
    log.append(u"painted set: %d symbols from %s" % (len(by), os.path.basename(p)))
    return by


def hexrgb(h):
    h = h.lstrip("#")
    return [int(h[k:k + 2], 16) for k in (0, 2, 4)]


def recolour(sym, base):
    """[(hex, rings unit -1..1 y up)]: band tones ranked by lightness -> a ramp of base (dark shade .. light tint)"""
    bands = [(bd["fill"], bd["rings"]) for bd in sym["bands"]]
    lum = lambda h: sum(c * w for c, w in zip(hexrgb(h), (0.299, 0.587, 0.114)))
    order = sorted(range(len(bands)), key=lambda k: lum(bands[k][0]))
    rank = dict((k, r / float(max(1, len(bands) - 1))) for r, k in enumerate(order))
    B = hexrgb(base)
    out = []
    for k, (h, rings) in enumerate(bands):
        t = rank[k]
        if t < 0.5:
            m, tgt = B_SHADE[0] * (1 - 2 * t), 0
        else:
            m, tgt = B_SHADE[1] * (2 * t - 1), 255
        out.append(("%02x%02x%02x" % tuple(int(round(c + (tgt - c) * m)) for c in B), rings))
    return out


def sym_paths(bands, X):
    """band paths; X(u, v) -> svg point"""
    s = []
    for h, rings in bands:
        d = u"".join(u"M" + u"L".join(u"%.3f,%.3f" % X(p[0], p[1]) for p in R) + u"Z" for R in rings if len(R) >= 3)
        if d:
            s.append(u'<path d="%s" fill="#%s" fill-rule="evenodd"/>' % (d, h))
    return u"".join(s)


def swap_symbols(txt, by, log):
    """his <symbol id="sym_<species>_3"> contents -> the picked symbol, same viewBox (every <use> keeps its place)"""
    n = 0
    for sp, (sid, col) in B_SPECIES.items():
        m = re.search(r'(<symbol\b[^>]*\bid="sym_%s_3"[^>]*>)(.*?)(</symbol>)' % re.escape(sp), txt, re.S)
        if not m or sid not in by:
            log.append(u"FLAG B: no symbol sym_%s_3 in his file or no %s in the set" % (sp, sid))
            continue
        vb = [float(x) for x in re.findall(r'viewBox="([^"]*)"', m.group(1))[0].replace(",", " ").split()]
        x0, y0, w, h = vb
        r = min(w, h) / 2.0
        cx, cy = x0 + w / 2.0, y0 + h / 2.0
        body = sym_paths(recolour(by[sid], col), lambda u, v: (cx + u * r, cy - v * r))
        txt = txt[:m.start()] + m.group(1) + u"<g>" + body + u"</g>" + m.group(3) + txt[m.end():]
        n += 1
        log.append(u"B: %s trees -> %s, #%s" % (sp, sid, col))
    log.append(u"B: %d of %d species symbols swapped" % (n, len(B_SPECIES)))
    return txt


def swap_plants(txt, gid, by, ns, upm, log, skip=()):
    """every plant-sized group inside his layer gid -> the next B_BUSH symbol, centred on its box, crown = box"""
    import xml.etree.ElementTree as ET
    sp = group_span(txt, gid)
    if sp is None:
        log.append(u"FLAG B: no layer %s in his file" % gid)
        return txt
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XL_NS)
    root = ET.fromstring(u'<svg xmlns="%s" xmlns:xlink="%s">%s</svg>' % (SVG_NS, XL_NS, txt[sp[0]:sp[1]]))
    lay = root[0]
    syms = [(recolour(by[s], c)) for s, c in B_BUSH if s in by]
    lo, hi = B_PLANT_M[0] * upm, B_PLANT_M[1] * upm
    cnt = {"plants": 0, "kept": 0}
    loc = lambda t: t.split("}", 1)[-1]

    def box_of(el, m):
        bx = [1e18, 1e18, -1e18, -1e18]
        mm = ns["mat_mul"](m, ns["parse_transform"](el.get("transform")))
        t = loc(el.tag)
        if t in ("g", "a"):
            for ch in el:
                b2 = box_of(ch, mm)
                bx = [min(bx[0], b2[0]), min(bx[1], b2[1]), max(bx[2], b2[2]), max(bx[3], b2[3])]
        elif t in ("path", "rect", "circle", "ellipse", "line", "polygon", "polyline"):
            subs = ns["path_segments"](el.get("d")) if t == "path" else ns["shape_subpaths"](t, el)
            for _c, s in subs:
                for p in ns["flat"](mm, s, upm):
                    bx = [min(bx[0], p[0]), min(bx[1], p[1]), max(bx[2], p[0]), max(bx[3], p[1])]
        return bx

    def walk(el, m):
        mm = ns["mat_mul"](m, ns["parse_transform"](el.get("transform")))
        for k, ch in enumerate(list(el)):
            if loc(ch.tag) != "g" or ch.get("id") in skip:
                cnt["kept"] += loc(ch.tag) != "g"
                continue
            bx = box_of(ch, mm)
            L = max(bx[2] - bx[0], bx[3] - bx[1])
            if bx[0] > bx[2]:
                continue
            if L <= hi:
                if L < lo:
                    continue
                cx, cy, r = (bx[0] + bx[2]) / 2.0, (bx[1] + bx[3]) / 2.0, L / 2.0
                # the box is in this layer's units; the new group sits in the parent's frame (inverse of mm)
                a, b, c, d, e, f_ = mm
                det = a * d - b * c
                inv = lambda q: ((d * (q[0] - e) - c * (q[1] - f_)) / det, (-b * (q[0] - e) + a * (q[1] - f_)) / det)
                bands = syms[cnt["plants"] % len(syms)]
                g = ET.Element("{%s}g" % SVG_NS, {"data-name": "plant B"})
                g.extend(ET.fromstring(u'<g xmlns="%s">%s</g>' % (SVG_NS, sym_paths(
                    bands, lambda u, v: inv((cx + u * r, cy - v * r))))))
                el.remove(ch)
                el.insert(k, g)
                cnt["plants"] += 1
            else:
                walk(ch, mm)
    walk(lay, (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    s = ET.tostring(lay, encoding="unicode")
    log.append(u"B: %s: %d plants swapped (%.1f-%.1f m groups), %d loose shapes kept as drawn" % (
        gid, cnt["plants"], B_PLANT_M[0], B_PLANT_M[1], cnt["kept"]))
    return txt[:sp[0]] + s + txt[sp[1]:]


# ================================================================ main
def build():
    t0 = time.time()
    log = []
    src = input_svg(log)
    pick_b = bool(globals().get("planting_b"))
    stamp = {"md5": md5_of(src), "version": VERSION, "b": pick_b,
             "basemap": int(os.path.getmtime(os.path.join(BERGAMA_ROOT, BASEMAP_CACHE)))}
    sp_ = os.path.join(PLAN_DIR, STAMP_FILE)
    out = os.path.join(PLAN_DIR, OUT_SVG)
    if os.path.isfile(sp_) and os.path.isfile(out) and not globals().get("rebuild"):
        try:
            if json.load(open(sp_, encoding="utf-8")) == stamp:
                return u"master.svg is up to date (his %s, md5 %s, planting %s): nothing written\n%s %s, 0 FLAG " \
                       u"line(s), %.1f s" % (IN_SVG, stamp["md5"], "B" if pick_b else "A", GH_LABEL, VERSION,
                                             time.time() - t0)
        except Exception:
            pass
    log.append(u"his masterplan: %s (%.1f MB, md5 %s)" % (src, os.path.getsize(src) / 1e6, stamp["md5"]))
    ns = mb_lib(log)
    with open(src, encoding="utf-8") as f:
        txt = f.read()
    n0 = len(txt)
    txt = re.sub(r"<metadata\b.*?</metadata>", u"", txt, flags=re.S)
    txt = re.sub(r'\s+xmlns:c2pa="[^"]*"', u"", txt)
    log.append(u"C2PA metadata dropped: %.1f KB" % ((n0 - len(txt)) / 1e3))
    txt = rgba_fix(txt, log)
    for gid in SOFT_IDS:                              # trees + bushes at 70 %
        m = re.search(r'<g\b[^>]*\bid="%s"[^>]*>' % gid, txt)
        if not m:
            log.append(u"FLAG no layer %s: its opacity not set" % gid)
            continue
        txt = txt[:m.start()] + set_attr(m.group(0), "opacity", SOFT_OPACITY) + txt[m.end():]
    m = re.search(r'<g\b[^>]*\bid="%s"[^>]*>' % PLANTING_ID, txt)
    if m:
        txt = txt[:m.start()] + set_attr(m.group(0), "opacity", None) + txt[m.end():]
    log.append(u"opacity %s on %s (%s's own opacity dropped so the trees read 70 %%)" % (
        SOFT_OPACITY, u" + ".join(SOFT_IDS), PLANTING_ID))
    work, upm = working_layer(txt, ns, log)
    if re.search(r'<g\b[^>]*\bid="%s"' % WORK_ID, txt):
        log.append(u"FLAG his file already has a %s layer: ours added after it" % WORK_ID)
    j = txt.rindex(u"</svg>")
    txt = txt[:j] + work + txt[j:]
    i = txt.index(u"<svg")
    txt = txt[:i] + u"<!-- %s %s, %s: from %s md5 %s -->\n" % (MARK, VERSION, time.strftime("%Y-%m-%d %H:%M"), IN_SVG,
                                                              stamp["md5"]) + txt[i:]
    files = {"A": txt}
    try:
        by = tree_set(log)
        tb = swap_symbols(txt, by, log)
        tb = swap_plants(tb, "agaclar", by, ns, upm, log, skip=(PLANTING_ID,))
        tb = swap_plants(tb, "assets", by, ns, upm, log)
        files["B"] = tb
    except Exception as ex:
        log.append(u"FLAG version B not made (%s: %s): master_B.svg not written" % (type(ex).__name__, ex))
    del txt
    # archive the master.svg that was there (never deleted)
    if os.path.isfile(out):
        with open(out, encoding="utf-8", errors="ignore") as f:
            head = f.read(4096)
        if MARK not in head:
            arc = os.path.join(PLAN_DIR, "archive")
            os.makedirs(arc, exist_ok=True)
            dst = os.path.join(arc, u"master_%s.svg" % time.strftime("%Y-%m-%d_%H%M", time.localtime(os.path.getmtime(out))))
            if not os.path.isfile(dst):
                shutil.copy2(out, dst)
            log.append(u"old master.svg archived: %s (md5 %s)" % (dst, md5_of(dst)))
    for k, name in (("A", OUT_A), ("B", OUT_B)):
        if k in files:
            p = os.path.join(PLAN_DIR, name)
            with open(p + ".tmp", "w", encoding="utf-8") as f:
                f.write(files[k])
            os.replace(p + ".tmp", p)
            log.append(u"%s: %s (%.1f MB)" % (k, p, os.path.getsize(p) / 1e6))
    use = "B" if pick_b and "B" in files else "A"
    if pick_b and use == "A":
        log.append(u"FLAG planting B asked but not made: master.svg = A")
    shutil.copyfile(os.path.join(PLAN_DIR, OUT_A if use == "A" else OUT_B), out + ".tmp")
    os.replace(out + ".tmp", out)
    log.append(u"master.svg = version %s (%s); every script reads it from %s" % (
        use, "his planting at 70 %" if use == "A" else "painted round symbols, recoloured", PLAN_DIR))
    with open(sp_, "w", encoding="utf-8") as f:
        json.dump(stamp, f)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


main = build


# ---- Grasshopper wiring (same in every script) ----
def chain_fire(v, key):
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done", "planting_b")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
