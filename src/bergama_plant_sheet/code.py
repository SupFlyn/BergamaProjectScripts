# -*- coding: utf-8 -*-
# CURRENT VERSION: bergama_plant_sheet_v1.py = v1 (1 Nov 2026, round 5 S4: the D4 approval sheet)
"""BERGAMA PLANT SHEET v1 (round 5, session S4, 1 Nov 2026; BRIEF D4, G-R5-6, G-R5-4.4, D10; PLAN §9 "D4 STOP").
ONE A0 portrait sheet for Aras to approve before any booklet page uses the new plants and people:
  * every species x state (general, spring, summer, autumn, winter) of the plant module v3 (common/plants.py): the
    section at 1:250, the plan at 1:1,000, and for shrubs, flowers and reeds a detail at 1:50 (1:100 above 2.5 m);
    under each cell the image source (asset_png = Data/plants/, cutout = Data/cutouts/, hires = assets_hires.json,
    placeholder = no image yet: a labelled dashed box, never a stand-in drawing);
  * the crops (cotton, maize, tomato) per state; their size is not sourced, so they are shown in a 1.00 m box;
  * the people (common/figures.py, set "library_dark") in every pose the pages use, at 1:50, each on what it touches
    (step, water, rail, bank, branch, stall), with its source (asset_library / drawn_A1_style); the three depth
    layers; the plan-view people.
Colours: every plant colour is still "pending research/plant_colours.md" (FLAG in the log); the sheet says so.
Writes Downloads/Bergama/output/Bergama_plant_sheet/Bergama_plant_sheet.pdf; log in Downloads/Bergama/logs/.
Runs as delivered in a Grasshopper Python 3 component (press a Button wired to any input named run) or plain
Python 3. Needs Data/ from the run kit: figures_A1.json, cutouts/, assets_hires.json; Data/plants/ when the asset
project has delivered it (until then the placeholders show what is missing).
"""
import os
import json
import math
import time
import zlib

VERSION = "v1"
GH_LABEL = "PlantSheet"
OUT_FOLDER = "Bergama_plant_sheet"
OUT_PDF_NAME = "Bergama_plant_sheet.pdf"
LOG_NAME = "bergama_plant_sheet_log.txt"

#@include ../common/bergama_paths.py
OUT_DIR = bg_output(OUT_FOLDER)
LOG_DIR = bg_logs()

#@include ../common/hex_rgb.py
#@include ../common/pdf_fonts.py
_ENC_EXTRA = _PF_EXTRA
#@include ../common/pdf_str.py
#@include ../common/_f.py
#@include ../common/font_metrics.py
PT = FM_PT


def text_w(s, size, bold=False):
    """the real Arial width (font_metrics.fm_width) of s at size mm"""
    return fm_width(s, size / PT, bold)


#@include ../common/page_stream.py
#@include ../common/_text_ops.py
#@include ../common/write_pdf.py
#@include ../common/section_parts.py
#@include ../common/plants.py
#@include ../common/hires.py
#@include ../common/figures.py


class Page(object):
    def __init__(self, W, H):
        self.W, self.H, self.items = W, H, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, stripes=None, alpha=None):
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, cap=1):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, cap))

    def text(self, s, x, y, size, color, bold=False, align="L"):
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, None, None))


def put(pg, shapes):
    """house shapes onto the page (as water.py shp_put): poly, line, text, image"""
    for s_ in shapes or []:
        t = s_[0]
        if t == "poly":
            if len(s_[1]) >= 3:
                pg.poly([list(s_[1])], fill=s_[2] or None, stroke=s_[3] or None, lw=s_[4] or 0.1)
        elif t == "line":
            pg.line(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None)
        elif t == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=s_[6] if len(s_) > 6 else False,
                    align=s_[7] if len(s_) > 7 else "L")
        elif t == "image":
            pg.items.append(tuple(s_) + (None,) * (9 - len(s_)))


# ---- sheet layout (A0 portrait; sizes in mm; design values) -------------------------------------------------------------
SH_W, SH_H, SH_M = 841.0, 1189.0, 14.0
INK, INK2, RED = "3C4733", "8E8F8A", "8B2D2D"          # palette (Bergama COLOUR rule)
WATER, WATER_LINE, STEP = "A2B6B5", "5C7A86", "D5D3CE"  # PLAN §3 section materials
GROUND = "C2A383"                                        # PLAN §3 soil top layer
T_TITLE, T_HEAD, T_TEXT, T_SMALL = 16 * PT, 7 * PT, 5 * PT, 4.5 * PT
STATES = (None, "spring", "summer", "autumn", "winter")
K_SEC, K_PLAN = 4.0, 1.0                                 # 1:250 and 1:1,000: page mm per m
LABEL_W = 92.0
COL_W = (SH_W - 2 * SH_M - LABEL_W) / 5.0
SPECIES_ROWS = ("stone_pine", "ash", "plane", "willow", "olive", "tamarisk", "chaste", "rosemary", "lavender",
                "loosestrife", "soft_rush", "rush", "reed", "mint")
CROP_ROWS = ("cotton", "maize", "tomato")
CROP_BOX_M = 1.00                                        # crop size not sourced: shown in a 1.00 m box (labelled)
K_PEOPLE = 20.0                                          # 1:50


def _xspan(shapes):
    """(min x, max x) of house shapes, or None"""
    xs = []
    for s_ in shapes or []:
        if s_[0] in ("poly", "line"):
            xs += [q[0] for q in s_[1]]
        elif s_[0] == "image":
            xs += [s_[1], s_[1] + s_[3]]
        elif s_[0] == "text":
            xs.append(s_[2])
    return (min(xs), max(xs)) if xs else None


def _shift(shapes, dx):
    """house shapes moved by dx (page mm) along x"""
    out = []
    for s_ in shapes or []:
        if s_[0] in ("poly", "line"):
            out.append((s_[0], [(q[0] + dx, q[1]) for q in s_[1]]) + tuple(s_[2:]))
        elif s_[0] == "image":
            out.append((s_[0], s_[1] + dx) + tuple(s_[2:]))
        elif s_[0] == "text":
            out.append(s_[:2] + (s_[2] + dx,) + tuple(s_[3:]))
        else:
            out.append(s_)
    return out


def _at_left(shapes, left):
    """shapes moved so their left edge is at `left`; returns (shapes, right edge)"""
    sp = _xspan(shapes)
    if not sp:
        return shapes, left
    return _shift(shapes, left - sp[0]), left + sp[1] - sp[0]


def _src(key, state, view):
    return PLA_SRC.get((key, state or "general", view)) or "-"


def _sec_draw(key, x, g, k, state):
    """one species in section (reed and mint, which grow only in lined cells, through the image call itself)"""
    if key in ("reed", "mint"):
        sp = PLA_SPECIES[key]
        h, w = sp["h_m"], sp["crown_m"] or 1.0
        c0 = pla_colours(key, state)
        return _pla_img_draw(key, state, "side", x, g, h, w, k, c0, 0, False, 0, c0["bare"]) or \
            _pla_missing_draw(key, state, "side", x, g, h, w, k) or []
    return pla_section(key, x, g, k, season=state)


def sheet_plants(pg, top, log):
    """the species x state table; returns the y below it"""
    y = top
    x0 = SH_M + LABEL_W
    for i, s_ in enumerate(STATES):
        cx = x0 + i * COL_W
        pg.text((s_ or "general").capitalize(), cx + 4.0, y - 6.0, T_HEAD, INK, True)
        pg.text(u"section 1:250 · plan 1:1,000 · detail 1:50 (1:100 above 2.5 m)", cx + 4.0, y - 9.5, T_SMALL, INK2)
    pg.text(u"Species (sourced drawing height)", SH_M, y - 6.0, T_HEAD, INK, True)
    y -= 14.0
    for key in SPECIES_ROWS:
        sp = PLA_SPECIES[key]
        h = float(sp["h_m"])
        small = sp["layer"] != "tree"
        k2 = 20.0 if h <= 2.5 else 10.0
        row_h = max(h * K_SEC, h * k2 if small else 0.0) + 16.0
        g = y - row_h + 10.0                             # ground line of the row
        pg.text(sp["name"], SH_M, g + row_h - 14.0, T_TEXT, INK, True)
        pg.text(sp["latin"], SH_M, g + row_h - 16.5, T_SMALL, INK2)
        pg.text(u"h %.2f m%s" % (h, (u" · detail 1:%d" % (1000 / k2)) if small else u""), SH_M, g + row_h - 19.0,
                T_SMALL, INK2)
        if key in ("reed", "mint"):
            pg.text(u"lined cells only (no plan symbol)", SH_M, g + row_h - 21.5, T_SMALL, INK2)
        for i, s_ in enumerate(STATES):
            cx = x0 + i * COL_W
            pg.line([(cx + 2.0, g), (cx + COL_W - 4.0, g)], INK2, 0.15)
            shp, xr = _at_left(_sec_draw(key, 0.0, g, K_SEC, s_), cx + 4.0)   # true size, never squeezed
            put(pg, shp)
            lab = u"%s" % _src(key, s_, "side")
            if key not in ("reed", "mint"):
                shp, xr = _at_left(pla_plan(key, 0.0, g + 10.0, K_PLAN, season=s_), max(xr, cx + 10.0) + 6.0)
                put(pg, shp)
                lab += u" | plan %s" % _src(key, s_, "top")
            if small:
                shp, xr = _at_left(_sec_draw(key, 0.0, g, k2, s_), xr + 6.0)
                put(pg, shp)
            if xr > cx + COL_W:
                log.append(u"WARNING sheet %s %s runs %.0f mm into the next column" % (key, s_ or "general",
                                                                                   xr - cx - COL_W))
            pg.text(lab, cx + 2.0, g - 3.5, T_SMALL, INK2)
        y -= row_h
    for crop in CROP_ROWS:
        row_h = CROP_BOX_M * 20.0 + 16.0
        g = y - row_h + 10.0
        pg.text(PLA_CROPS[crop]["name"], SH_M, g + row_h - 14.0, T_TEXT, INK, True)
        pg.text(u"size not sourced: shown in a 1.00 m box at 1:50", SH_M, g + row_h - 16.5, T_SMALL, RED)
        for i, s_ in enumerate(STATES):
            cx = x0 + i * COL_W
            st = pla_crop_state(crop, s_)
            pg.line([(cx + 2.0, g), (cx + COL_W - 4.0, g)], INK2, 0.15)
            put(pg, _pla_crop_sec(crop, cx + 20.0, g, CROP_BOX_M, 0.6 * CROP_BOX_M, 20.0, i, False, st, s_))
            pg.text(u"%s · %s" % (st, _src(crop, s_, "side") if st not in ("bare", "harvested") else u"drawn"),
                    cx + 2.0, g - 3.5, T_SMALL, INK2)
        y -= row_h
    return y


# people scenes: (pose, params, width m); each scene shows what the figure touches
PEOPLE = (("stand", {}, 0.9), ("walk", {}, 1.0), ("watch", {}, 1.0), ("railing", {"rail_h": 1.10}, 1.4),
          ("sit_step", {"seat_h": 0.45}, 1.4), ("wade", {"depth_m": 0.40}, 1.4), ("fishing", {"water_dy": -0.80}, 3.6),
          ("touch", {"reach_y": -0.30}, 1.4), ("bike", {}, 2.0), ("adult_child", {}, 1.2), ("child_play", {}, 1.6),
          ("olive", {"branch_h": 1.90}, 1.2), ("running", {}, 1.2), ("lying", {}, 2.0), ("dog_walk", {}, 2.6),
          ("stall", {}, 3.0))


def _scene(pose, p, x, g, k):
    """the ground / step / water / rail / branch a figure touches, then the figure (feet at (x, g))"""
    sh = []
    if pose == "wade":                                   # wading strip: bed, water to depth_m, legs cut at the water
        d = p["depth_m"] * k
        sh.append(("poly", [(x - 0.6 * k, g), (x + 0.6 * k, g), (x + 0.6 * k, g + d), (x - 0.6 * k, g + d)], WATER, None, 0))
        sh.append(("line", [(x - 0.6 * k, g + d), (x + 0.6 * k, g + d)], WATER_LINE, 0.2))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose in ("fishing", "touch"):                     # bank edge, water below it
        wd = p.get("water_dy", p.get("reach_y", -0.3)) * k
        ex = x + (0.35 if pose == "fishing" else 0.45) * k
        bed = g + wd - 0.4 * k
        sh.append(("poly", [(ex, bed), (x + 3.4 * k, bed), (x + 3.4 * k, g + wd), (ex, g + wd)], WATER, None, 0))
        sh.append(("line", [(ex, g + wd), (x + 3.4 * k, g + wd)], WATER_LINE, 0.2))
        sh.append(("poly", [(x - 0.6 * k, bed), (ex, bed), (ex, g), (x - 0.6 * k, g)], STEP, INK2, 0.1))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "sit_step":                               # the step it sits on (nosing from fig_meta)
        an = fig_meta(pose, **p)
        nx, sy = x + an.get("seat_x", 0.15) * k, g + an.get("seat_y", p["seat_h"]) * k
        sh.append(("poly", [(nx - 0.55 * k, g), (nx, g), (nx, sy), (nx - 0.55 * k, sy)], STEP, INK2, 0.1))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "railing":
        an = fig_meta(pose, **p)
        rx, ry = x + an.get("rail_x", 0.4) * k, g + an.get("rail_y", p["rail_h"]) * k
        sh += fig_side(pose, x, g, k, pick=1, **p)
        sh += [("line", [(rx, g), (rx, ry)], INK2, 0.35), ("line", [(rx - 0.3 * k, ry), (rx + 0.3 * k, ry)], INK2, 0.5)]
        return sh
    if pose == "olive":
        an = fig_meta(pose, **p)
        hx = x + an.get("hand_x", 0.3) * k
        by = g + p["branch_h"] * k
        sh.append(("line", [(hx - 0.5 * k, by + 0.1 * k), (hx + 0.6 * k, by - 0.05 * k)], PLA_TRUNK, 0.6))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "stall":
        return fig_stall(x + 1.2 * k, g, k, facing=1)
    return fig_side(pose, x, g, k, pick=1, **p)


def sheet_people(pg, top, log):
    """the people panel: every pose at 1:50 on what it touches, the depth layers, the plan views; returns y"""
    k = K_PEOPLE
    pg.text(u"People · one set, one dark tone (A1 library first, then cutouts, then poses drawn in the A1 language) "
            u"· 1:50", SH_M, top - 6.0, T_HEAD, INK, True)
    g = top - 14.0 - 2.6 * k
    x = SH_M + 4.0
    for pose, p, wm in PEOPLE:
        if x + wm * k > SH_W - SH_M:
            g -= 3.2 * k
            x = SH_M + 4.0
        cx = x + 0.5 * k
        pg.line([(x - 2.0, g), (x + wm * k, g)], INK2, 0.15)
        put(pg, _scene(pose, p, cx, g, k))
        q = dict(p)
        src = _fig_side_dark(FIG_POSE_ALIAS.get(pose, pose) if pose != "stall" else "stall", 1, q)[0]
        pg.text(pose.replace("_", " "), x, g - 3.0, T_TEXT, INK, True)
        pg.text(src, x, g - 5.2, T_SMALL, INK2)
        x += wm * k + 8.0
    g -= 3.0 * k                                         # depth layers 0 / 1 / 2 (nearer stronger, farther paler)
    x = SH_M + 4.0
    pg.text(u"Depth layers 0 / 1 / 2 (opaque, paler and smaller behind)", x, g + 2.4 * k, T_TEXT, INK, True)
    for lay in (0, 1, 2):
        for j, pose in enumerate(("stand", "walk", "sit_step")):
            xx = x + (lay * 3 + j) * 0.9 * k
            put(pg, fig_side(pose, xx, g, k, layer=lay, pick=2 + j, seat_h=0.45) if pose == "sit_step" else
                fig_side(pose, xx, g, k, layer=lay, pick=2 + j))
    pg.line([(x - 2.0, g), (x + 8.2 * k, g)], INK2, 0.15)
    x2 = x + 9.5 * k                                     # plan views
    pg.text(u"Plan views (drawn A1 style)", x2, g + 2.4 * k, T_TEXT, INK, True)
    for j, pose in enumerate(("stand", "walk", "sit_step", "bike", "adult_child", "fishing", "dog_walk", "lying")):
        put(pg, fig_top(pose, x2 + 0.6 * k + j * 1.9 * k, g + 0.9 * k, k, pick=j))
        pg.text(pose.replace("_", " "), x2 + j * 1.9 * k, g - 3.0, T_SMALL, INK2)
    return g - 8.0


def main(G):
    t0 = time.time()
    pla_missing("placeholder")                            # the sheet shows what is missing, never a stand-in
    pg = Page(SH_W, SH_H)
    pg.poly([[(0, 0), (SH_W, 0), (SH_W, SH_H), (0, SH_H)]], fill="FFFFFF")
    pg.text(u"Plants and people · sample sheet for approval (D4)", SH_M, SH_H - SH_M - 6.0, T_TITLE, INK, True)
    pg.text(u"Plant colours: pending research/plant_colours.md (every species). Image source under each cell: asset_png "
            u"= Data/plants, cutout = Data/cutouts (species by look), hires = PhyloPic silhouette, placeholder = no "
            u"image yet.", SH_M, SH_H - SH_M - 12.0, T_TEXT, RED)
    warn = []
    y = sheet_plants(pg, SH_H - SH_M - 26.0, warn)
    y = sheet_people(pg, y - 6.0, warn)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, OUT_PDF_NAME)
    try:
        write_pdf(pg, out, "Bergama plant sheet " + VERSION)
    except PermissionError:
        return "ERROR: The PDF is open in a viewer: close it and press the Button again (%s)" % out
    lines = [u"%s  %s" % (out, time.strftime("%H:%M:%S")), u"plant sheet %s, %.1f s" % (VERSION, time.time() - t0)]
    if y < 0:
        warn.append(u"WARNING sheet content runs %.0f mm below the page" % -y)
    lines = warn + lines
    lines += pla_log_lines()
    lines.append(fig_set_line())
    lines += fig_flag_lines()
    lines.append(u"FLAG fauna pending research (deferred; not on this sheet)")
    lines += FIG_LOG + SIL_LOG + HR_LOG + WP_IMG_LOG + PLA_LOG
    nw = sum(1 for ln in lines if ln.startswith(u"WARNING"))
    return u"%d warnings\n" % nw + u"\n".join(lines)


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


#@include ../common/trigger.py
#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try:
        _ik = ":" + str(ghenv.Component.InstanceGuid)
    except Exception:
        _ik = ""
    _pressed, _why, _btn = trig_should_run("bergama_plant_sheet_log_chain")
    if _pressed:
        _t0 = time.time()
        try:
            _res = main(globals()) + u"\ntrigger: " + (_why or u"-")
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_plant_sheet_log" + _ik] = write_log(_res)
        _ok = not _res.startswith("ERROR")
        _sc.sticky["bergama_plant_sheet_log_status" + _ik] = (time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0)
                                                              if _ok else "ERROR")
        _sc.sticky["bergama_plant_sheet_log_done" + _ik] = done_text(True, _ok, time.time() - _t0)
        _sc.sticky["bergama_plant_sheet_log_ver" + _ik] = VERSION
        try:
            if _ok and _res.split("\n", 1)[0] != "0 warnings":
                ghenv.Component.AddRuntimeMessage(ghenv.Component.RuntimeMessageLevel.Warning, _res.split("\n", 1)[0])
        except Exception:
            pass
    if _sc.sticky.get("bergama_plant_sheet_log_ver" + _ik) != VERSION:
        for _s in ("", "_status", "_done"):
            _sc.sticky.pop("bergama_plant_sheet_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_plant_sheet_log_done" + _ik, "idle")
    log = _sc.sticky.get("bergama_plant_sheet_log" + _ik, "Press the Button to draw the sheet into " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(
            "bergama_plant_sheet_log_status" + _ik, "idle")
    except Exception:
        pass
else:
    print(write_log(main(globals())))
