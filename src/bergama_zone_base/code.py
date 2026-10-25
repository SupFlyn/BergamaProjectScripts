"""BERGAMA ZONE BASE v9 (2026-10-25): bakes Group 6's zone layout into the open Rhino file as an editable base.

NEW IN v9 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): bakes option A only (Option_A::INT_*); option B is no longer baked and the option input is
ignored. Option_B layers already in a file are left as they are (delete them by hand if you want). Nothing else
changed.

NEW IN v8 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_zone_base_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v7 (Aras 25 Oct 08:03-08:18): DEMETER'S GARDEN, Begum's idea alone (card i01), as zones DG 1 and DG 2 on
layer INT_ZONE_DG (tier D), where her drawing puts them: the south-west bank either side of K5 Uckemer bridge,
inside calisma_alan[1]. Outline = the open ground between the bed (WA 4 / WA 5) and the street edge less 1.5 m,
1.5 m clear of surveyed buildings and walls, 20 m clear of the K5 deck (DG 1 about 565 m2 upstream, DG 2 about
852 m2 downstream; placeholders, calculated from the survey DXF). Labels "DEMETER'S GARDEN" on each, and one very
small "idea: Begum" credit. Allowed as a public, educational garden with a cafe (Aras 08:07), so the 18 Oct "no
farmland inside the site" rule still holds for everything else. Everything else is as in v6.

NEW IN v6 (Aras 25 Oct 07:50-07:52: one file for everything, the larger survey "Bergama Müdahele Alanları (1)"): a
file with no study-area layers (aras_alan, begum_alan, nil_alan) is accepted when its survey (stream, buildings)
lies on the study areas recorded in STUDY_BBOX, i.e. it is the survey in survey coordinates; the base is baked
exactly as in v5. A file that HAS study-area layers must still have them where the course survey has them.
The working area is the whole calisma_alan, one shared area (Aras 25 Oct 08:05: no split by person). Every
proposal is baked whole when it lies in, crosses or comes within SNAP_M (15 m) of it (Aras 08:10-08:11: small
differences do not matter, lines that nearly match count as overlapping and the larger area is the true one); one
lying farther off is not baked and the log lists it. Labels are notes, baked as before.
calisma_alan is read from the open file (Bergama_Altlik.3dm; an open outline with ends under 5 m apart counts as
closed); with none there, the copy CALISMA_COPY below. The zones themselves are the same as in v5.

WHAT IT IS
  A Grasshopper Python 3 component. Wire a plain Button into an input named `run` (v8; bake / build / go / press also work);
  one press bakes the whole base, both presentations, into the open Rhino file:
    Option_A::INT_...   PanelReview1A: curved edges only where the project meets the water, straight elsewhere
    Option_B::INT_...   PanelReview1B: no organic forms, every edge straight or faceted
  These are the INT_ layers that bergama_masterplan reads, so after editing you press Build on the masterplan
  component and get one sheet per option.

  What is baked, per option (the revised draft of 17-18 Oct, mp2/draft2/make_draft_markup_v2.py, checked against
  CONCEPT_RECORD v2.3 sections 3.3-3.6, 5.2, 5.4):
    NEW IN v2 (Aras 2026-10-18 14:29): the water only runs downstream (Aras upstream, then Begum K4, K5, then Nil;
    the survey strip order). It is cleaned at Aras's end, so the whole river runs clean; Nil needs no treatment; no
    water flows back up.
    Aras   aras_alan      "Collect, clean and hold": WS 1 retention terraces (dry top) hold the runoff, WT 1
                          cleansing reed basins (v1's planted basins) take river water and the held runoff, WD 1
                          spillway gives the clean water back to the strip; GR 1 shaded walk
    Begum  begum_alan[0]  K4 "Amphibious heritage threshold": WA 1-2 bed (W), WA 3 flood terrace (F), GR 2 raised dry
                          top (D) on the cleared plot (2 INT_REMOVE_cleared buildings, gone in the 1 Oct photos)
           begum_alan[1]  K5: WA 4-5 bed, WA 6 flood terrace, GR 3 raised dry top
    Nil    nil_alan       "Give back": WP 1-2 floodable riverside planting fed by the clean river (v1's reed beds),
                          floodable boardwalk. No farmland and no farm channel inside the site (v3/v4, Aras 14:49 and
                          15:02: the farms are the existing ones on the slopes just outside the site)
    All    the continuous low-flow water strip (INT_WATER_strip, decision D8; labelled CLEAN WATER STRIP below Aras),
           wetland planting edges (INT_SURFACE_wetland), labels (INT_LABEL_notes)
    Arrows INT_LINK_water / INT_LINK_people / INT_LINK_flood: 11 per option, every one passes bergama_masterplan v6's
           link_check, and every water arrow points downstream.
           NEW IN v5 (Aras 15:03 "have the interaction arrows from the closest place possible always"): each arrow
           joins the two closest points of what it links (2.5 m inside each zone) along a line that crosses no third
           zone; a river end sits on open strip at or upstream of the zone it feeds, at or downstream of the zone it
           drains, so no arrow shows water running uphill. Every river end stays at least 1.5 m off any zone edge.
  Every size is a PLACEHOLDER, not a design size: each zone's user text `basis` says what it was sized on (open
  ground between surveyed obstacles, legibility). No storage volume, level or flow is drawn.

RULES IT KEEPS
  * It bakes only into a file whose study areas (aras_alan, begum_alan, nil_alan) sit where the course survey has
    them (within 5 cm): the base is in survey coordinates. Any other file: ERROR, nothing is baked.
  * The study-area curves are never touched.
  * YOUR EDITS ARE KEPT. Each baked object carries user text `base_hash` (its shape when baked). Pressing again
    deletes and re-bakes only the objects still exactly as baked; an object you moved, reshaped or recoloured
    stays, and its draft piece is not baked again. An object you deleted comes back on the next press (to stop
    that, set `option` to the other option or do not press again).
  * A and B are two designs for the same ground, so they lie in the same place on separate parent layers (the
    masterplan needs them there to read them). Switch a parent layer off to see one at a time; the masterplan bakes
    its two sheets side by side.

INPUTS (any case; only the button is needed)
  run      Button
  option   "both" (default), "A" or "B"

OUTPUT
  log: the log. It stays readable after the button is released, and is also written to
  Downloads/Bergama/output/bergama_zone_base/bergama_zone_base_log.txt.
"""

import os
import json
import time
import zlib
import base64
import hashlib
import tempfile
import datetime
import types as _types

import Rhino
import Rhino.Geometry as rg
import System
import System.Drawing
import scriptcontext as sc

VERSION = "bergama_zone_base v9 (2026-10-25)"
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here

BASE_MD5 = "cdfe4fe55413b71ba9d80dd092ff1112"  # the decompressed base data (701,976 bytes of JSON, survey coordinates)
# The base: mp2/draft2/draft_markup.json (Option_A / Option_B, 14 zones each) + 11 typed arrows per option, JSON,
# zlib + base64. Generated by prep_auto_v5.py; v7 appends 10 Demeter's Garden items (2 zones + 3 labels per option).
# Do not edit by hand.
#@include data/BASE_DATA.py
SHORT = "v9"
BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button")
TAG = "bergama_zone_base"                          # user text key on every baked object (value = VERSION)
STUDY_BBOX = {                                     # the course survey's study areas (survey = file coordinates, m)
    "aras_alan": [(29610.0960, 32247.0612, 29880.6932, 32794.2334)],
    "begum_alan": [(29792.1139, 32108.0060, 30053.4176, 32398.0733), (30138.0721, 31405.2525, 30555.8868, 31924.6365)],
    "nil_alan": [(30389.6859, 30542.0263, 31415.5004, 31450.8529)],
}
BBOX_TOL = 0.05
LAYER_COLOURS = {                                  # the masterplan palette's tones for the starter layers (sRGB hex)
    "INT_ZONE_WS": "5D7F8D", "INT_ZONE_WD": "4E7A88", "INT_ZONE_WT": "6F8F6A", "INT_ZONE_WA": "7FA2A6",
    "INT_ZONE_WI": "A79A5A", "INT_ZONE_GR": "7E9A62", "INT_ZONE_DG": "89986A", "INT_WATER_strip": "32525F", "INT_SURFACE_wetland": "6F8F6A",
    "INT_REMOVE_cleared": "6E6A66", "INT_ROAD_path": "8C7B66", "INT_LABEL_notes": "3A3536",
    "INT_LINK_water": "32525F", "INT_LINK_people": "8C1C32", "INT_LINK_flood": "5D7F8D"}
PARENT = {"A": "Option_A", "B": "Option_B"}


# ---------------------------------------------------------------- Grasshopper inputs, memory, status
#@include ../common/_gh_inputs.py


_GH_IN = _gh_inputs()
_T_START = time.time()


#@include ../common/chain_fire.py


#@include ../common/done_text.py



def gin(name, default=None):
    """An input by name in any case (bake = Bake = BAKE)."""
    for k_, v_ in _GH_IN.items():
        if k_.lower() == name.lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None), None)
            return default if v_ is None or (isinstance(v_, str) and not v_.strip()) else v_
    return default


def to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    return str(v).strip().lower() in ("true", "yes", "1", "on")


def find_button():
    for k_ in _GH_IN:
        if "".join(c for c in k_.lower() if c.isalpha()) in BUTTON_WORDS:
            return k_
    try:
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    return str(p_.NickName or p_.Name)
    except Exception:
        pass
    return None


# 25 Oct (Aras 09:55): remembered for this Rhino session only (sticky); no temp state file. The one copy on disk is
# the log in Downloads/Bergama/logs/, read back only if the session lost the last log.
#@include ../common/_key.py


def mem_get(k, default=None):
    kk = _key(k)
    try:
        if kk in sc.sticky:
            return sc.sticky[kk]
    except Exception:
        pass
    if k == "last":
        try:
            with open(os.path.join(LOG_DIR, "bergama_zone_base_log.txt"), encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return default


#@include ../common/mem_set.py


GH_LABEL = "ZoneBase"                                # Aras 25 Oct 09:44: name under the component


#@include ../common/gh_status.py


#@include ../common/gh_message.py


# ---------------------------------------------------------------- the base
def base_items():
    raw = zlib.decompress(base64.b64decode("".join(BASE_DATA)))
    if hashlib.md5(raw).hexdigest() != BASE_MD5:
        raise ValueError("the embedded base data is damaged (md5 differs): copy the script again")
    return json.loads(raw.decode("utf-8"))


def shape_hash(g):
    """A short hash of an object's shape (curve vertices or a text dot's point and text), rounded to 1 mm."""
    pts = []
    try:
        if isinstance(g, rg.TextDot):
            pts = [(g.Point.X, g.Point.Y), g.Text]
        else:
            res = g.TryGetPolyline()
            pl = res[1] if isinstance(res, tuple) and res[0] else None
            pts = [(p.X, p.Y) for p in pl] if pl is not None else [
                (g.PointAtStart.X, g.PointAtStart.Y), (g.PointAtEnd.X, g.PointAtEnd.Y), round(g.GetLength(), 3)]
    except Exception:
        pts = [str(g)]
    s_ = ";".join("{:.3f},{:.3f}".format(*p) if isinstance(p, tuple) else str(p) for p in pts)
    return hashlib.md5(s_.encode("utf-8")).hexdigest()[:16]


CALISMA_COPY = [                                   # v6: calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25: closed, ends snapped onto site_alan), survey m
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
CALISMA_LAYER = "calisma_alan"
CLOSE_GAP = 5.0                                   # v6: m, an open outline closer than this counts as closed
SNAP_M = 15.0                                     # v6: m, a proposal this close to calisma_alan counts as on it
SURVEY_PROBE = ("HIDRO_DERE_SULU", "SEV_UST", "BINA_MESKEN")   # v6: survey layers that cross the study areas
STUDY_NOTE = []                                                   # v6: what study_check accepted, for the log


def survey_on_study_areas(doc):
    """v6: True when objects on the SURVEY_PROBE layers overlap every recorded study area (survey coordinates)."""
    boxes = [b for bs in STUDY_BBOX.values() for b in bs]
    hit = [False] * len(boxes)
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name not in SURVEY_PROBE:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            bb = o.Geometry.GetBoundingBox(True)
            for k, b in enumerate(boxes):
                if not hit[k] and bb.Max.X >= b[0] and bb.Min.X <= b[2] and bb.Max.Y >= b[1] and bb.Min.Y <= b[3]:
                    hit[k] = True
            if all(hit):
                return True
    return all(hit)


def study_check(doc):
    """'' when the open file's study areas sit where the course survey has them (or, v6, the file has none and its
    survey lies on the recorded study areas), else why not."""
    del STUDY_NOTE[:]
    have = {}
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name not in STUDY_BBOX:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            bb = o.Geometry.GetBoundingBox(True)
            have.setdefault(lay.Name, []).append((bb.Min.X, bb.Min.Y, bb.Max.X, bb.Max.Y))
    if not have:                                                  # v6: e.g. the larger survey, no study layers
        if survey_on_study_areas(doc):
            STUDY_NOTE.append("No study-area layers in this file: its survey lies on the recorded study areas "
                              "(STUDY_BBOX), so it is the survey in survey coordinates; the base was baked there.")
            return ""
        return "no study-area layers, and no survey ({}) on the recorded study areas".format(", ".join(SURVEY_PROBE))
    for nm, boxes in STUDY_BBOX.items():
        got = list(have.get(nm, []))
        if len(got) < len(boxes):
            return "layer {} holds {} curve(s), the course survey has {}".format(nm, len(got), len(boxes))
        for b in boxes:
            j = next((k for k, q in enumerate(got) if max(abs(q[i] - b[i]) for i in range(4)) <= BBOX_TOL), None)
            if j is None:
                return "a study area on {} is not where the course survey has it (more than {} m off)".format(
                    nm, BBOX_TOL)
            got.pop(j)
    return ""


def ensure_layer(doc, path):
    idx = doc.Layers.FindByFullPath(path, -1)
    if idx >= 0:
        return idx
    parent, _, name = path.rpartition("::")
    lay = Rhino.DocObjects.Layer()
    lay.Name = name
    if parent:
        lay.ParentLayerId = doc.Layers[ensure_layer(doc, parent)].Id
    h = LAYER_COLOURS.get(name)
    if h:
        lay.Color = System.Drawing.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return doc.Layers.Add(lay)


def calisma_areas(doc, tol, log):
    """v6: the closed working-area outlines: calisma_alan of the open file, else CALISMA_COPY."""
    out = []
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name.lower() != CALISMA_LAYER:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            c = o.Geometry
            if not isinstance(c, rg.Curve):
                continue
            if not c.IsClosed:
                if c.PointAtStart.DistanceTo(c.PointAtEnd) > CLOSE_GAP:
                    log.append("calisma_alan: an open curve ({:.1f} m between its ends) was skipped".format(
                        c.PointAtStart.DistanceTo(c.PointAtEnd)))
                    continue
                res = c.TryGetPolyline()
                pl_ = res[1] if isinstance(res, tuple) and res[0] else None
                if pl_ is not None:
                    pl_.Add(pl_[0])
                    c = rg.PolylineCurve(pl_)
                else:
                    c = c.DuplicateCurve()
                    if not c.MakeClosed(CLOSE_GAP):
                        log.append("calisma_alan: a curve could not be closed and was skipped")
                        continue
            out.append(c)
    if out:
        log.append("Working area: {} calisma_alan outline(s) of this file, worked as one area".format(len(out)))
        return out
    log.append("Working area: no calisma_alan in this file; the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    return [rg.PolylineCurve([rg.Point3d(x, y, 0.0) for x, y in P + [P[0]]]) for P in CALISMA_COPY]


def near_work(g, areas, tol):
    """v6: True when curve g lies in, crosses or comes within SNAP_M of the working area (Aras 08:11: lines that
    nearly match are taken as overlapping, the larger area is the true one, so nothing is cut)."""
    pl = rg.Plane.WorldXY
    for A in areas:
        if A.Contains(g.PointAtStart, pl, tol) != rg.PointContainment.Outside:
            return True
        res = g.ClosestPoints(A)
        if res and res[0] and res[1].DistanceTo(res[2]) <= SNAP_M:
            return True
    return False


def bake(doc, which, log):
    """Bake the base for options `which` (('A', 'B') by default). Returns the number of objects baked."""
    items = base_items()
    tol = doc.ModelAbsoluteTolerance or 0.001
    areas = calisma_areas(doc, tol, log)
    n_all = 0
    for o_ in which:
        parent = PARENT[o_]
        t_ = time.time()
        # earlier bake of this script under this parent: untouched objects go, edited ones stay
        kept_ids, gone = set(), 0
        for o in list(doc.Objects):
            try:
                lp = doc.Layers[o.Attributes.LayerIndex].FullPath
            except Exception:
                continue
            if not lp.startswith(parent + "::") or o.Attributes.GetUserString(TAG) is None:
                continue
            if o.Attributes.GetUserString("base_hash") == shape_hash(o.Geometry):
                doc.Objects.Delete(o, True)
                gone += 1
            else:
                kept_ids.add(o.Attributes.GetUserString("base_id"))
        groups, dropped = {}, []
        for k_, it in enumerate(i for i in items if i["layer"].startswith(parent + "::")):
            bid = "{}-{}".format(o_, k_)
            if bid in kept_ids and (it["kind"] != "LABEL" or not it.get("lead") or bid + "-lead" in kept_ids):
                continue
            lay = it["layer"]
            att = Rhino.DocObjects.ObjectAttributes()
            att.LayerIndex = ensure_layer(doc, lay)
            att.Name = it.get("name") or ""
            for mk, mv in (it.get("meta") or {}).items():
                att.SetUserString(mk, str(mv))
            att.SetUserString(TAG, VERSION)
            att.SetUserString("base_id", bid)
            gids = []
            if it["kind"] == "LABEL":
                if it.get("pt") and bid not in kept_ids:
                    g = rg.TextDot(it.get("text") or it.get("name") or "", rg.Point3d(it["pt"][0], it["pt"][1], 0.0))
                    if it.get("font"):                       # v7: the very small "idea: Begum" credit
                        g.FontHeight = int(it["font"])
                    att.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddTextDot(g, att))
                if it.get("lead") and bid + "-lead" not in kept_ids:
                    g = rg.PolylineCurve([rg.Point3d(p[0], p[1], 0.0) for p in it["lead"]])
                    a2 = att.Duplicate()
                    a2.SetUserString("base_id", bid + "-lead")
                    a2.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddCurve(g, a2))
            else:
                P = [rg.Point3d(p[0], p[1], 0.0) for p in it["P"]]
                if it.get("closed") and P[0].DistanceTo(P[-1]) > tol:
                    P.append(P[0])
                g0 = rg.PolylineCurve(P)
                if not near_work(g0, areas, tol):            # v6: nothing is cut; only what lies far off is left out
                    dropped.append((it.get("meta") or {}).get("id") or it.get("name") or bid)
                    continue
                for g in [g0]:
                    a2 = att.Duplicate()
                    a2.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddCurve(g, a2))
            ok = sum(1 for g_ in gids if g_ != System.Guid.Empty)
            who = "calisma_alan"                         # v6: one shared working area, no split by person
            grp = groups.setdefault(who, {})
            nm = {"ZONE": "zones", "WATER": "strip pieces", "SURFACE": "wetland edges", "REMOVE": "cleared buildings",
                  "ROAD": "paths", "LINK": "arrows", "LABEL": "labels"}[it["kind"]]
            grp[nm] = grp.get(nm, 0) + ok
            n_all += ok
        dt = time.time() - t_
        log.append("{}: {:.1f} s{}{}".format(parent, dt, "; {} untouched objects of the last press replaced".format(
            gone) if gone else "", "; {} of your edited objects kept as they are".format(len(kept_ids))
            if kept_ids else ""))
        for who in sorted(groups):
            log.append("  {}  {}".format(who, ", ".join("{} {}".format(v, k) for k, v in sorted(groups[who].items()))))
        if dropped:
            log.append("  more than {:.0f} m outside calisma_alan, not baked: ".format(SNAP_M) + ", ".join(dropped))
    doc.Views.Redraw()
    return n_all


def run():
    btn = find_button()
    if btn is None:
        text = "No button found: wire a Button into an input named run. ({})".format(VERSION)
        gh_status(SHORT + " · no button")
        gh_message("warning", text)
        return text
    on = to_bool(gin(btn, False))
    pressed = (on and not mem_get("prev", False)) or chain_fire(gin(btn), "chain_seen")
    globals()["_ran_now"] = pressed
    mem_set("prev", on)
    if not pressed:
        last = mem_get("last", "")
        gh_status(mem_get("status", "") or SHORT + " · idle")
        return (last + "\n\n(This is the log of the last press. Press {} to bake again.)".format(btn)) if last else \
            "Idle. Press {} to bake the zone base into Option_A. ({})".format(btn, VERSION)
    t0 = time.time()
    gh_status(SHORT + " · baking")
    log, err = [], None
    doc = Rhino.RhinoDoc.ActiveDoc
    which = ("A",)                                     # v9: option A only, project-wide (Aras 25 Oct 16:43)
    # v5 24 Oct: all files under Downloads/Bergama/ (Aras rule); was beside the .3dm
    folder = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "bergama_zone_base")
    n = 0
    try:
        if doc is None:
            raise RuntimeError("no Rhino file is open")
        if doc.ModelUnitSystem != Rhino.UnitSystem.Meters:
            raise RuntimeError("the file is not in metres ({}): the base is in metres".format(doc.ModelUnitSystem))
        why = study_check(doc)
        if why:
            raise RuntimeError("this is not the Bergama survey in survey coordinates ({}). The base is in those "
                               "coordinates, so nothing was baked. Open Bergama_Altlik.3dm and press again".format(why))
        log.extend(STUDY_NOTE)
        n = bake(doc, which, log)
    except Exception as ex_:
        err = "ERROR: {}: {}".format(type(ex_).__name__, ex_)
    secs = time.time() - t0
    head = ["Run at {} | {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), VERSION),
            ("RESULT: " + err) if err else "RESULT: done in {:.0f} s: {} objects baked ({})".format(
                secs, n, " and ".join(PARENT[w] for w in which)),
            "DESTINATION: this Rhino file, layers {} (true place on the survey){}".format(
                " and ".join(PARENT[w] + "::INT_..." for w in which),
                "; log file in " + folder if folder else ""),
            "-" * 60]
    tail = ["", "Every size is a placeholder (user text 'basis' on each zone). Edit freely, then press Build on the "
                "masterplan component. Pressing here again keeps every object you changed."]
    text = "\n".join(head + log + ([] if err else tail))
    if folder:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            with open(os.path.join(LOG_DIR, "bergama_zone_base_log.txt"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass
    status = "{} · {}".format(SHORT, "ERROR" if err else time.strftime("%H:%M") + " · {:.0f} s".format(secs))
    mem_set("last", text)
    mem_set("status", status)
    gh_status(status)
    if err:
        gh_message("error", err)
    return text


try:
    _txt = run()
except Exception as _ex:
    _txt = "ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION)
    gh_status(SHORT + " · ERROR")
    mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
    mem_set("status", SHORT + " · ERROR")
log = _txt
print(_txt)                  # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
if globals().get("_ran_now"):
    mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
