# -*- coding: utf-8 -*-
"""Bergama Group 6: UE5 RENDER v1 (18 Nov 2026): eye-level perspective renders in Unreal Engine 5.8 from the Archicad model.

What Aras asked (18 Nov 2026, 10:05-10:09 UTC): "getting perspective renders from UE5 and model from archicad"; four
reference images (dusk, warm lit glazing, dark still water, tall grass in front), "a lesser purple version of this",
"hyper realistic renders", "use all the good stuff like raytracing and all max it out". Render PC: the laptop
(RTX 4060 laptop GPU, 96 GB RAM).

Run in the Unreal Editor 5.8 (Aras: 5.8.4) of the Bergama UE project: Tools > Execute Python Script... > this file.
  1. imports Downloads/Bergama/cached/bergama_ue5/Bergama_site.udatasmith (Archicad 29 + Datasmith exporter) or, when
     there is none, Bergama_site.fbx (Archicad 30 3D window > Save As FBX; v1.2)
     into the level /Game/Bergama/Bergama_Persp; a re-import happens only when the .udatasmith file changed;
  2. builds the light rig: sun + sky atmosphere + real-time sky light + height fog at blue hour (sun SUN_ELEV_DEG below
     the horizon on DATE in the evening, NOAA solar position), white balance pulled warm / away from magenta (less
     purple), warm 2700 K lights inside every node building (cached/bergama_perspectives/buildings.json);
     the water surfaces (material name holds "water") get a dark, mirror-still water material;
  3. one cine camera per V view of the slides (cached/bergama_perspectives/views_*.json, read live): eye EYE_M above
     the model's ground (traced), moved forward to a clear spot like Perspectives v1.6, lens so a node building
     fills about 70 % of the frame (24-50 mm), image PX_W wide in the proportions of the view's box;
  4. renders every view with Movie Render Queue: the Path Tracer (hardware ray tracing, SPP samples, denoised) when
     the project has ray tracing on, else Lumen (FLAG) -> output/bergama_ue5/<page>_<view>.png, also copied over the
     Rhino interim pictures cached/bergama_perspectives/<page>_<view>.png when REPLACE_INTERIM (the slide scripts then
     place the renders).
Coordinates: Archicad model = survey m minus AcBuild's origin (cached/bergama_archicad_site/acbuild.json, read live),
heights absolute; UE cm. The Y sign of the Datasmith import is tested on the model bounds (logged).
Reads  cached/bergama_ue5/Bergama_site.udatasmith, cached/bergama_archicad_site/acbuild.json,
       cached/bergama_perspectives/views_*.json + buildings.json
Writes output/bergama_ue5/<page>_<view>.png, cached/bergama_ue5/import.json, logs/bergama_ue5_log.txt,
       (REPLACE_INTERIM) cached/bergama_perspectives/<page>_<view>.png
Works when: the log lists one "render" line per view, ends with "done" and 0 FLAG lines.
"""
import os, json, math, glob, time, shutil, datetime, urllib.request
import unreal

VERSION = "v1.5"   # v1.5 (Aras 11:04 UTC: the whole-site 3D window takes too long to export): several FBX files (one per Marquee area around the views, all in Archicad project coordinates) picked together and imported into one level; v1.4 (Aras 10:36 UTC "really really high quality really really detailed really really good textures"): every Archicad surface class gets a scanned 4K PBR set (colour, normal, roughness, AO) from Poly Haven (picked live through its API by keywords, most downloaded first; cached), mapped world-aligned at the scan's real size; v1.3 (Aras 10:19 UTC "a bat file to pick the fbx file and auto start"): run_ue5_render.bat writes the picked FBX path to cached/bergama_ue5/fbx_path.txt (the FBX stays where Archicad saved it, beside its textures) and opens UE with this script; v1.2 (Aras 10:16 UTC: the Datasmith exporter page sends him to Twinmotion; its builds cover Archicad 23-29 only, none for AC30 yet): Bergama_site.fbx (Archicad 30 FBX export) imported through Interchange when no .udatasmith is there; v1.1 (Aras 18 Nov 10:15 UTC "unreal engine 5.8.4"): texts say UE 5.8; the Datasmith exporter must be the 5.8 one; v1 (Aras 18 Nov 10:05-10:09 UTC): first UE5 renders from the Archicad model, blue hour, path tracer
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
UDS = os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "Bergama_site.udatasmith")
FBX = os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "Bergama_site.fbx")   # v1.2: Archicad 30 route
FBX_PICK = os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "fbx_path.txt")   # v1.3: written by run_ue5_render.bat
FBXS = []                    # v1.5: every FBX the launcher picked (one per line; several = one per area)
if os.path.isfile(FBX_PICK):
    with open(FBX_PICK, encoding="utf-8-sig") as _f:
        FBXS = [l.strip().strip('"') for l in _f if l.strip()]
STAMP = os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "import.json")
ACB_JSON = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad_site", "acbuild.json")
PERSP_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_perspectives")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", "bergama_ue5")
LOG_FILE = os.path.join(BERGAMA_ROOT, "logs", "bergama_ue5_log.txt")
LEVEL = "/Game/Bergama/Bergama_Persp"
DS_DEST = "/Game/Bergama/Site"
SEQ_DIR = "/Game/Bergama/Seq"

# ---- view rules (same as Perspectives v1.6)
EYE_M = 1.6                  # m: eye height above the ground (standing person)
EYE_HIGH_M = 10.0            # m: eye height when no clear spot is found
CLEAR_M = 25.0               # m clear ahead of the eye
LENS_MM, LENS_MAX = 24.0, 50.0
PX_W = 3840                  # px: image width (height from the view's box proportions)
REPLACE_INTERIM = True       # copy the renders over the Rhino interim pictures the slide scripts place
# ---- look (drawing choices, from Aras's reference images 18 Nov; change here)
SITE_LAT, SITE_LON, TZ_H = 39.11952, 27.18381, 3.0   # Data/selinus_board_data.py line 1440; Turkey UTC+3
DATE = (2026, 6, 21)         # summer: the terraces dry
SUN_ELEV_DEG = -3.0          # blue hour, evening side (sun just below the horizon)
SUN_LUX = 120000.0           # physical sun (the sky brightness follows it)
WHITE_TEMP = 7200.0          # > 6500 = warmer picture (less blue / purple)
WHITE_TINT = 0.12            # pulls away from magenta
EXPOSURE_BIAS = -0.7         # darker, dusk mood
ROOM_LM, ROOM_K = 3000.0, 2700.0   # lumens and colour temperature of each room light (warm interior glow)
FOG_DENSITY = 0.02           # Aras 10:10 UTC "atmospheric looks": visible depth haze (UE default 0.02)
SPP = 512                   # path tracer samples per pixel
WARMUP = 64                  # frames before the shot (Lumen / exposure settle)

# ---- v1.4 textures: Archicad material name (lower case, contains) -> Poly Haven search words (all must match name/tags/
# categories; the most downloaded match wins). Drawing choices; edit here. First matching row wins.
TEX_RES = "4k"               # "8k" for close-ups (more VRAM: the laptop GPU has 8 GB)
TEX_MAP = [
    (("water", "foliage", "leaves", "reed", "glass", "glazing"), None),   # left alone (water: own material)
    (("roof tile", "rooftile"), ("roof",)),
    (("brick",), ("brick",)),
    (("rubble", "stonework", "historic", "bridge", "cut stone", "granite", "terrace stone"), ("stone", "wall")),
    (("river bed", "riverbed", "gravel"), ("gravel",)),
    (("quay", "pavement", "paving", "pavers", "stair"), ("paving",)),
    (("road", "asphalt"), ("asphalt",)),
    (("park", "grass"), ("grass",)),
    (("ground", "earth", "terrain", "soil"), ("ground",)),
    (("bark",), ("bark",)),
    (("timber", "wood", "pine"), ("wood", "planks")),
    (("plaster", "stucco", "lime", "our building white", "facet white"), ("plaster",)),
    (("concrete", "screed", "aac", "bims", " rc", "frame grey", "insulation"), ("concrete",)),
]
PH_API = "https://api.polyhaven.com"
TEX_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "textures")

LOG = []


def log(s):
    LOG.append(s)
    unreal.log(u"[Bergama UE5] " + s)


def flush():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(u"Bergama UE5 render %s  %s\n" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S")))
        f.write(u"\n".join(LOG) + u"\n")
        f.write(u"FLAG lines: %d\n" % sum(1 for l in LOG if l.startswith("FLAG")))


def sun_dir_enu(hour):
    """NOAA 'General Solar Position Calculations' (fractional-year form): unit vector toward the sun, (east, north, up)"""
    y, m, d = DATE
    n = datetime.date(y, m, d).timetuple().tm_yday
    g = 2 * math.pi / 365.0 * (n - 1 + (hour - TZ_H - 12) / 24.0)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g)
                    - 0.040849 * math.sin(2 * g))
    dec = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
           + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    tst = hour * 60.0 + eqt + 4.0 * SITE_LON - 60.0 * TZ_H
    ha = math.radians(tst / 4.0 - 180.0)
    la = math.radians(SITE_LAT)
    e = -math.cos(dec) * math.sin(ha)
    nn = math.sin(dec) * math.cos(la) - math.cos(dec) * math.cos(ha) * math.sin(la)
    u = math.sin(dec) * math.sin(la) + math.cos(dec) * math.cos(ha) * math.cos(la)
    return e, nn, u


def evening_sun():
    """the evening minute the sun passes SUN_ELEV_DEG (survey y = north within 0.2 deg, pages_common line 83)"""
    t = 12.0
    while t < 24.0:
        if math.degrees(math.asin(sun_dir_enu(t)[2])) <= SUN_ELEV_DEG:
            return t, sun_dir_enu(t)
        t += 1.0 / 60
    raise RuntimeError(u"the sun never reaches %.1f deg on %s" % (SUN_ELEV_DEG, DATE))


EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAL = unreal.EditorAssetLibrary


def world():
    return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def actors(tag=None):
    a = EAS.get_all_level_actors()
    return [x for x in a if tag is None or tag in [str(t) for t in x.tags]]


def tag(a, t):
    a.tags = list(a.tags) + [unreal.Name(t)]


def spawn(cls, loc=(0, 0, 0), rot=None, t="BGA_rig"):
    a = EAS.spawn_actor_from_class(cls, unreal.Vector(*loc), rot or unreal.Rotator(0, 0, 0))
    tag(a, t)
    return a


def trace(a, b):
    """first hit point on the model between a and b (UE cm), None when nothing is hit"""
    h = unreal.SystemLibrary.line_trace_single(world(), unreal.Vector(*a), unreal.Vector(*b),
                                               unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [],
                                               unreal.DrawDebugTrace.NONE, True)
    if not h:
        return None
    for v in unreal.GameplayStatics.break_hit_result(h):
        if isinstance(v, unreal.Vector):
            return v
    return None


def open_level():
    if EAL.does_asset_exist(LEVEL):
        LES.load_level(LEVEL)
    else:
        LES.new_level(LEVEL)
        log(u"level %s made" % LEVEL)


def import_model():
    srcs = [f for f in FBXS if os.path.isfile(f)]          # v1.5: the picked FBX files win (several = one per area)
    if not srcs:                                          # v1.5: else every FBX in cached/bergama_ue5/fbx/
        srcs = sorted(glob.glob(os.path.join(BERGAMA_ROOT, "cached", "bergama_ue5", "fbx", "*.fbx")))
    if not srcs:
        srcs = [UDS] if os.path.isfile(UDS) else ([FBX] if os.path.isfile(FBX) else [])
    if not srcs:
        raise RuntimeError(u"no model file: run run_ue5_render.bat and pick the Archicad FBX file(s)")
    for f in FBXS:
        if not os.path.isfile(f):
            log(u"FLAG picked FBX not found: %s" % f)
    st = {"files": [[f, os.path.getmtime(f), os.path.getsize(f)] for f in srcs]}
    old = {}
    if os.path.isfile(STAMP):
        with open(STAMP, encoding="utf-8") as f:
            old = json.load(f)
    have = actors("BGA_ds")
    if have and old.get("files") == st["files"]:
        log(u"model: %d actors already imported, %d file(s) unchanged" % (len(have), len(srcs)))
        return have
    for a in have:
        EAS.destroy_actor(a)
    before = set(x.get_path_name() for x in actors())
    t0 = time.time()
    for src in srcs:
        if src == UDS:
            sc = unreal.DatasmithSceneElement.construct_datasmith_scene_from_file(UDS)
            if sc is None:
                raise RuntimeError(u"Datasmith could not read %s (is the Datasmith Importer plugin on?)" % UDS)
            try:
                op = sc.get_options(unreal.DatasmithImportOptions)
            except Exception:
                op = sc.get_options()
            op.base_options.scene_handling = unreal.DatasmithImportScene.CURRENT_LEVEL
            res = sc.import_scene(DS_DEST)
            sc.destroy_scene()
            if not res.import_succeed:
                raise RuntimeError(u"Datasmith import of %s failed" % UDS)
        else:                                             # FBX through Interchange, placed in the open level
            im = unreal.InterchangeManager.get_interchange_manager_scripted()
            sd = unreal.InterchangeManager.create_source_data(src)
            pa = unreal.ImportAssetParameters()
            pa.is_automated = True
            sub = "".join(ch if ch.isalnum() else "_" for ch in os.path.splitext(os.path.basename(src))[0])
            ok = im.import_scene(DS_DEST + "/" + sub, sd, pa)
            if ok is False:
                raise RuntimeError(u"FBX import of %s failed (Interchange)" % src)
            log(u"model part: %s imported" % src)
    new = [x for x in actors() if x.get_path_name() not in before]
    for a in new:
        tag(a, "BGA_ds")
    os.makedirs(os.path.dirname(STAMP), exist_ok=True)
    with open(STAMP, "w", encoding="utf-8") as f:
        json.dump(dict(st, version=VERSION, actors=len(new), when=time.strftime("%Y-%m-%d %H:%M:%S")), f)
    log(u"model: %d file(s) imported, %d actors, %.0f s" % (len(srcs), len(new), time.time() - t0))
    return new


def water_material():
    p = "/Game/Bergama/M_BGA_Water"
    if EAL.does_asset_exist(p):
        return EAL.load_asset(p)
    m = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_BGA_Water", "/Game/Bergama", unreal.Material,
                                                               unreal.MaterialFactoryNew())
    ML = unreal.MaterialEditingLibrary
    for prop, val in ((unreal.MaterialProperty.MP_BASE_COLOR, (0.010, 0.016, 0.018)),
                      (unreal.MaterialProperty.MP_ROUGHNESS, 0.03), (unreal.MaterialProperty.MP_SPECULAR, 0.5),
                      (unreal.MaterialProperty.MP_METALLIC, 0.0)):
        if isinstance(val, tuple):
            n = ML.create_material_expression(m, unreal.MaterialExpressionConstant3Vector)
            n.constant = unreal.LinearColor(val[0], val[1], val[2], 1.0)
        else:
            n = ML.create_material_expression(m, unreal.MaterialExpressionConstant)
            n.r = val
        ML.connect_material_property(n, "", prop)
    ML.recompile_material(m)
    EAL.save_loaded_asset(m)
    return m


def set_water(ds):
    wm, n = water_material(), 0
    for a in ds:
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            for i, mi in enumerate(c.get_materials()):
                if mi and "water" in mi.get_name().lower():
                    c.set_material(i, wm)
                    n += 1
    log(u"water: %d material slots set to still dark water" % n) if n else log(
        u"FLAG water: no material named *water* in the import: river left as Archicad drew it")


def _get(url, dst=None):
    rq = urllib.request.Request(url, headers={"User-Agent": "BergamaStudentRender/1.4"})
    with urllib.request.urlopen(rq, timeout=120) as r:
        data = r.read()
    if dst:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst + ".part", "wb") as f:
            f.write(data)
        os.replace(dst + ".part", dst)
        return dst
    return json.loads(data.decode("utf-8"))


def ph_pick(words, cat):
    """the most downloaded Poly Haven texture whose name, tags and categories hold every word"""
    best = None
    for aid, a in cat.items():
        hay = (aid + " " + a.get("name", "") + " " + " ".join(a.get("tags", [])) + " " +
               " ".join(a.get("categories", []))).lower()
        if all(w in hay for w in words) and (best is None or a.get("download_count", 0) > best[1].get("download_count", 0)):
            best = (aid, a)
    return best


def ph_maps(aid):
    """download (once) colour, normal (GL), roughness, AO jpgs at TEX_RES -> {kind: local path}"""
    fl = _get(PH_API + "/files/" + aid)
    out = {}
    for kind, keys in (("col", ("Diffuse", "diff")), ("nor", ("nor_gl",)), ("rough", ("Rough", "rough")), ("ao", ("AO", "ao"))):
        for k in keys:
            e = (fl.get(k) or {}).get(TEX_RES) or (fl.get(k) or {}).get("2k")
            u = ((e or {}).get("jpg") or (e or {}).get("png") or {}).get("url")
            if u:
                dst = os.path.join(TEX_DIR, aid, "%s_%s%s" % (aid, kind, os.path.splitext(u)[1]))
                out[kind] = dst if os.path.isfile(dst) else _get(u, dst)
                break
    return out


def import_tex(path, dest, kind):
    t = unreal.AssetImportTask()
    t.filename, t.destination_path, t.automated, t.save, t.replace_existing = path, dest, True, True, True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    tex = EAL.load_asset(dest + "/" + os.path.splitext(os.path.basename(path))[0])
    if tex and kind != "col":
        tex.set_editor_property("srgb", False)
        if kind == "nor":
            tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        EAL.save_loaded_asset(tex)
    return tex


def master_material():
    """M_BGA_Scan: world-aligned colour, normal, roughness x AO from texture parameters, TileCM = real scan size"""
    p = "/Game/Bergama/M_BGA_Scan"
    if EAL.does_asset_exist(p):
        return EAL.load_asset(p)
    m = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_BGA_Scan", "/Game/Bergama", unreal.Material,
                                                               unreal.MaterialFactoryNew())
    ML = unreal.MaterialEditingLibrary
    size = ML.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -900, 0)
    size.parameter_name, size.default_value = "TileCM", 200.0
    wat = EAL.load_asset("/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedTexture")
    wan = EAL.load_asset("/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedNormal")

    def tex_param(name, y, normal=False, fn=wat):
        to = ML.create_material_expression(m, unreal.MaterialExpressionTextureObjectParameter, -600, y)
        to.parameter_name = name
        if normal:
            to.sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
        fc = ML.create_material_expression(m, unreal.MaterialExpressionMaterialFunctionCall, -300, y)
        fc.set_editor_property("material_function", fn)
        ML.connect_material_expressions(to, "", fc, "TextureObject")
        ML.connect_material_expressions(size, "", fc, "TextureSize")
        return fc
    col = tex_param("Col", -300)
    nor = tex_param("Nor", 0, True, wan)
    rgh = tex_param("Rough", 300)
    ao = tex_param("AO", 600)
    mul = ML.create_material_expression(m, unreal.MaterialExpressionMultiply, 0, 400)
    ML.connect_material_expressions(rgh, "XYZ Texture", mul, "A")
    ML.connect_material_expressions(ao, "XYZ Texture", mul, "B")
    ML.connect_material_property(col, "XYZ Texture", unreal.MaterialProperty.MP_BASE_COLOR)
    ML.connect_material_property(nor, "XYZ Texture", unreal.MaterialProperty.MP_NORMAL)
    ML.connect_material_property(mul, "", unreal.MaterialProperty.MP_ROUGHNESS)
    ML.connect_material_property(ao, "XYZ Texture", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    ML.recompile_material(m)
    EAL.save_loaded_asset(m)
    return m


def set_textures(ds):
    """v1.4: each Archicad surface class -> a scanned PBR material instance (Poly Haven, cached)"""
    try:
        cat = _get(PH_API + "/assets?t=textures")
    except Exception as ex:
        log(u"FLAG Poly Haven not reachable (%s): Archicad's own surfaces kept" % ex)
        return
    master = master_material()
    made, n, miss = {}, 0, set()
    for a in ds:
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            for i, mi in enumerate(c.get_materials()):
                if not mi:
                    continue
                nm = mi.get_name().lower().replace("_", " ")
                row = next((r for r in TEX_MAP if any(k in nm for k in r[0])), None)
                if row is None:
                    miss.add(mi.get_name())
                    continue
                if row[1] is None:
                    continue
                key = row[1]
                if key not in made:
                    made[key] = None
                    pick = ph_pick(key, cat)
                    if not pick:
                        log(u"FLAG no Poly Haven texture for %s: kept Archicad's" % u" + ".join(key))
                        continue
                    aid, info = pick
                    try:
                        maps = ph_maps(aid)
                        dest = "/Game/Bergama/Tex/" + aid
                        T = {k: import_tex(v, dest, k) for k, v in maps.items()}
                        inst = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                            "MI_" + aid, "/Game/Bergama/Tex", unreal.MaterialInstanceConstant,
                            unreal.MaterialInstanceConstantFactoryNew())
                        ML = unreal.MaterialEditingLibrary
                        ML.set_material_instance_parent(inst, master)
                        for k, pn in (("col", "Col"), ("nor", "Nor"), ("rough", "Rough"), ("ao", "AO")):
                            if T.get(k):
                                ML.set_material_instance_texture_parameter_value(inst, pn, T[k])
                        dim = info.get("dimensions") or [2000, 2000]          # mm (Poly Haven asset info)
                        ML.set_material_instance_scalar_parameter_value(inst, "TileCM", float(dim[0]) / 10.0)
                        EAL.save_loaded_asset(inst)
                        made[key] = inst
                        log(u"texture %s: Poly Haven '%s' (%s), %s, %.1f m tile, maps %s" % (
                            u" + ".join(key), info.get("name", aid), aid, TEX_RES, float(dim[0]) / 1000.0,
                            u", ".join(sorted(T))))
                    except Exception as ex:
                        log(u"FLAG texture %s (%s) failed: %s: %s" % (u" + ".join(key), aid, type(ex).__name__, ex))
                if made.get(key):
                    c.set_material(i, made[key])
                    n += 1
    log(u"textures: %d material slots given scanned PBR materials (%d sets)" % (n, sum(1 for v in made.values() if v)))
    if miss:
        log(u"FLAG materials with no texture row (kept as Archicad drew them): %s" % u", ".join(sorted(miss)[:40]))


def light_rig(ox, oy, sy, gz):
    for a in actors("BGA_rig"):
        EAS.destroy_actor(a)
    hr, (e, n, u) = evening_sun()
    v = unreal.Vector(-e, -n * sy, -u)                    # light travels from the sun toward the ground
    sun = spawn(unreal.DirectionalLight, (0, 0, gz * 100 + 5000), unreal.MathLibrary.make_rot_from_x(v))
    lc = sun.get_component_by_class(unreal.DirectionalLightComponent)
    lc.set_mobility(unreal.ComponentMobility.MOVABLE)
    lc.set_editor_property("atmosphere_sun_light", True)
    lc.set_editor_property("intensity", SUN_LUX)
    spawn(unreal.SkyAtmosphere)
    sk = spawn(unreal.SkyLight, (0, 0, gz * 100 + 5000))
    sc = sk.get_component_by_class(unreal.SkyLightComponent)
    sc.set_mobility(unreal.ComponentMobility.MOVABLE)
    sc.set_editor_property("real_time_capture", True)
    fg = spawn(unreal.ExponentialHeightFog, (0, 0, gz * 100))
    fc = fg.get_component_by_class(unreal.ExponentialHeightFogComponent)
    fc.set_editor_property("fog_density", FOG_DENSITY)
    fc.set_editor_property("volumetric_fog", True)          # atmospheric depth, light shafts through crowns
    try:
        lc.set_editor_property("enable_light_shaft_bloom", True)
    except Exception:
        pass
    pp = spawn(unreal.PostProcessVolume)
    pp.unbound = True
    s = pp.settings
    for k, val in (("white_temp", WHITE_TEMP), ("white_tint", WHITE_TINT), ("auto_exposure_bias", EXPOSURE_BIAS),
                   ("path_tracing_enable_denoiser", True), ("path_tracing_max_bounces", 32),
                   ("path_tracing_samples_per_pixel", SPP)):
        try:
            s.set_editor_property("override_" + k, True)
            s.set_editor_property(k, val)
        except Exception as ex:
            log(u"FLAG post process %s not set (%s)" % (k, ex))
    pp.settings = s
    log(u"sun: %s %02d:%02d local, %.1f deg below the horizon, azimuth %.0f deg from north; white %.0f K tint %+.2f, "
        u"exposure %+.1f" % ("%d-%02d-%02d" % DATE, int(hr), round(hr % 1 * 60), -SUN_ELEV_DEG,
                             math.degrees(math.atan2(e, n)) % 360, WHITE_TEMP, WHITE_TINT, EXPOSURE_BIAS))
    bj = os.path.join(PERSP_DIR, "buildings.json")
    if not os.path.isfile(bj):
        log(u"FLAG %s missing: no room lights" % bj)
        return {}
    with open(bj, encoding="utf-8") as f:
        B = json.load(f).get("buildings") or {}
    k = 0
    for nd, b in sorted(B.items()):
        if b.get("canopy") or not b.get("nf"):
            continue
        for i in range(int(b["nf"])):
            z = b["ground"] + b.get("plinth", 0) + i * b["storey"] + 0.75 * b["storey"]
            pl = spawn(unreal.PointLight, ((b["c"][0] - ox) * 100, (b["c"][1] - oy) * 100 * sy, z * 100))
            c = pl.get_component_by_class(unreal.PointLightComponent)
            c.set_mobility(unreal.ComponentMobility.MOVABLE)
            c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
            c.set_editor_property("intensity", ROOM_LM)
            c.set_editor_property("use_temperature", True)
            c.set_editor_property("temperature", ROOM_K)
            c.set_editor_property("attenuation_radius", 0.75 * max(b["L"], b["D"]) * 100)
            k += 1
    log(u"room lights: %d (%.0f lm, %.0f K) in %s" % (k, ROOM_LM, ROOM_K, u", ".join(sorted(B)) or u"none"))
    return B


def read_views():
    vs = []
    for fp in sorted(glob.glob(os.path.join(PERSP_DIR, "views_*.json"))):
        with open(fp, encoding="utf-8") as f:
            J = json.load(f)
        pg = J.get("page") or os.path.basename(fp)[6:-5]
        for vn, v in sorted((J.get("views") or {}).items()):
            if v.get("eye") and v.get("look") and v.get("box_mm"):
                vs.append((pg, vn, v))
            else:
                log(u"FLAG %s %s: no eye, look or box size: left out" % (pg, vn))
    if not vs:
        raise RuntimeError(u"no views_*.json in %s: press Slide04 and the node scripts first" % PERSP_DIR)
    return vs


def make_seq(name, cam):
    p = SEQ_DIR + "/" + name
    if EAL.does_asset_exist(p):
        EAL.delete_asset(p)
    seq = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, SEQ_DIR, unreal.LevelSequence,
                                                                 unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(24, 1))
    seq.set_playback_start(0)
    seq.set_playback_end(1)
    b = seq.add_possessable(cam)
    try:
        tr = seq.add_track(unreal.MovieSceneCameraCutTrack)
    except Exception:
        tr = seq.add_master_track(unreal.MovieSceneCameraCutTrack)
    sec = tr.add_section()
    sec.set_range(0, 1)
    bid = None
    for f in (lambda: unreal.MovieSceneSequenceExtensions.get_portable_binding_id(seq, seq, b),
              lambda: seq.make_binding_id(b, unreal.MovieSceneObjectBindingSpace.LOCAL)):
        try:
            bid = f()
            break
        except Exception:
            pass
    sec.set_camera_binding_id(bid)
    EAL.save_loaded_asset(seq)
    return seq


def main():
    t0 = time.time()
    log(u"UE %s, Python script %s" % (unreal.SystemLibrary.get_engine_version(), VERSION))
    if not os.path.isfile(ACB_JSON):
        raise RuntimeError(u"%s missing: run AcBuild once" % ACB_JSON)
    with open(ACB_JSON, encoding="utf-8") as f:
        ox, oy = [float(q) for q in json.load(f)["origin"]]
    log(u"Archicad origin = survey (%.0f, %.0f) from %s" % (ox, oy, ACB_JSON))
    open_level()
    ds = import_model()
    views = read_views()
    c, ext = unreal.GameplayStatics.get_actor_array_bounds(world(), ds, False)
    lo, hi = c - ext, c + ext

    def inside(sy):
        return sum(1 for _, _, v in views if lo.x <= (v["eye"][0] - ox) * 100 <= hi.x
                   and lo.y <= (v["eye"][1] - oy) * 100 * sy <= hi.y)
    sy = -1.0 if inside(-1.0) >= inside(1.0) else 1.0      # Datasmith turns right-handed models: y usually flips
    log(u"model bounds x %.0f..%.0f m, y %.0f..%.0f m, z %.0f..%.0f m; Y sign %+.0f (%d of %d eyes inside)" % (
        lo.x / 100, hi.x / 100, lo.y / 100, hi.y / 100, lo.z / 100, hi.z / 100, sy, inside(sy), len(views)))
    if inside(sy) == 0:
        log(u"FLAG no view eye lies on the model: check the origin and the Datasmith export")
    set_water(ds)
    set_textures(ds)                                      # v1.4
    B = light_rig(ox, oy, sy, (lo.z + hi.z) / 200.0)

    U = lambda p, z: ((p[0] - ox) * 100, (p[1] - oy) * 100 * sy, z * 100)

    def ground(p):
        h = trace(U(p, hi.z / 100 + 50), U(p, lo.z / 100 - 50))
        return h.z / 100 if h else None

    def clear_eye(e, k):
        dd = math.hypot(k[0] - e[0], k[1] - e[1]) or 1.0
        nx, ny = (k[0] - e[0]) / dd, (k[1] - e[1]) / dd
        s = 0.0
        while s <= 0.6 * dd:
            p = (e[0] + nx * s, e[1] + ny * s)
            g = ground(p)
            if g is not None:
                z = g + EYE_M
                q = (p[0] + nx * CLEAR_M, p[1] + ny * CLEAR_M)
                if trace(U(p, z), U(q, z)) is None:
                    return p, z, (u"marked eye" if s == 0 else u"moved %.0f m forward to a clear spot" % s)
            s += 4.0
        g = ground(e)
        if g is None:
            return e, None, u"no ground under the eye"
        return e, g + EYE_HIGH_M, u"no clear spot at eye level: raised to %.0f m" % EYE_HIGH_M

    for a in actors("BGA_cam"):
        EAS.destroy_actor(a)
    jobs = []
    for pg, vn, v in views:
        e, k = tuple(v["eye"][:2]), tuple(v["look"][:2])
        e, ze, why = clear_eye(e, k)
        if ze is None:
            log(u"FLAG %s %s: the model has no ground under the eye (%.1f, %.1f): left out" % (pg, vn, e[0], e[1]))
            continue
        dist = math.hypot(k[0] - e[0], k[1] - e[1])
        if dist < 1.0:
            log(u"FLAG %s %s: eye and look points coincide: left out" % (pg, vn))
            continue
        lens = LENS_MM
        nd = v.get("node") or ("N6" if v.get("building") else None)
        if nd in B and B[nd].get("L"):
            lens = max(LENS_MM, min(LENS_MAX, 36.0 * dist / (B[nd]["L"] / 0.7)))
        bw, bh = float(v["box_mm"][0]), float(v["box_mm"][1])
        W, H = PX_W, int(round(PX_W * bh / bw))
        a, b_ = U(e, ze), U(k, ze)
        rot = unreal.MathLibrary.make_rot_from_x(unreal.Vector(b_[0] - a[0], b_[1] - a[1], 0.0))
        cam = spawn(unreal.CineCameraActor, a, rot, "BGA_cam")
        cam.set_actor_label(u"BGA_%s_%s" % (pg, vn))
        cc = cam.get_cine_camera_component()
        fb = cc.get_editor_property("filmback")
        fb.sensor_width, fb.sensor_height = 36.0, 36.0 * H / W
        cc.set_editor_property("filmback", fb)
        cc.set_editor_property("current_focal_length", lens)
        fs = cc.get_editor_property("focus_settings")
        fs.focus_method = unreal.CameraFocusMethod.DISABLE
        cc.set_editor_property("focus_settings", fs)
        jobs.append((u"%s_%s" % (pg, vn), cam, W, H))
        log(u"view %s %s (%s): eye %.1f, %.1f at %.1f m, looking %.0f m to %.1f, %.1f, %.0f mm lens, %d x %d px" % (
            pg, vn, why, e[0], e[1], ze, dist, k[0], k[1], lens, W, H))
    LES.save_current_level()
    rt = unreal.SystemLibrary.get_console_variable_int_value("r.RayTracing")
    path = rt == 1
    if not path:
        log(u"FLAG ray tracing is off in this project (Project Settings > Rendering > Support Hardware Ray Tracing "
            u"+ Path Tracing, restart): rendered with Lumen instead of the Path Tracer")
    MQ = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    q = MQ.get_queue()
    q.delete_all_jobs()
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, cam, W, H in jobs:
        seq = make_seq(name, cam)
        j = q.allocate_new_job(unreal.MoviePipelineExecutorJob)
        j.job_name = name
        j.sequence = unreal.SoftObjectPath(seq.get_path_name())
        j.map = unreal.SoftObjectPath(LEVEL + "." + LEVEL.split("/")[-1])
        cf = j.get_configuration()
        o = cf.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
        o.output_directory = unreal.DirectoryPath(OUT_DIR)
        o.file_name_format = "{sequence_name}.{frame_number}"
        o.output_resolution = unreal.IntPoint(W, H)
        o.override_existing_output = True
        cf.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPass_PathTracer if path
                                        else unreal.MoviePipelineDeferredPassBase)
        cf.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
        aa = cf.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
        aa.override_anti_aliasing = True
        aa.anti_aliasing_method = unreal.AntiAliasingMethod.AAM_NONE
        aa.spatial_sample_count = SPP if path else 1
        aa.temporal_sample_count = 1 if path else 16
        aa.engine_warm_up_count = WARMUP
        aa.render_warm_up_count = WARMUP
        cv = cf.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
        for k_, v_ in (("r.MotionBlurQuality", 0), ("r.DepthOfFieldQuality", 0), ("r.Lumen.Reflections.HardwareRayTracing", 1),
                       ("r.Lumen.HardwareRayTracing", 1), ("r.ScreenPercentage", 100)):
            cv.add_or_update_console_variable(k_, v_)
    log(u"queue: %d views, %s, %s samples, %.0f s to set up" % (
        len(jobs), "Path Tracer" if path else "Lumen", SPP if path else 16, time.time() - t0))
    flush()

    def done(ex_, ok):
        for name, cam, W, H in jobs:
            fs_ = sorted(glob.glob(os.path.join(OUT_DIR, name + ".*.png")), key=os.path.getmtime)
            if not fs_:
                log(u"FLAG %s: no picture written" % name)
                continue
            dst = os.path.join(OUT_DIR, name + ".png")
            shutil.move(fs_[-1], dst)
            log(u"render %s: %d x %d px -> %s" % (name, W, H, dst))
            if REPLACE_INTERIM:
                shutil.copy2(dst, os.path.join(PERSP_DIR, name + ".png"))
        log(u"done (%s): %.1f min" % ("ok" if ok else "FLAG the queue reported a failure", (time.time() - t0) / 60))
        flush()
    global _EXECUTOR
    _EXECUTOR = MQ.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
    _EXECUTOR.on_executor_finished_delegate.add_callable_unique(done)


_EXECUTOR = None
try:
    main()
except Exception as ex:
    log(u"FLAG stopped: %s: %s" % (type(ex).__name__, ex))
    flush()
    raise
