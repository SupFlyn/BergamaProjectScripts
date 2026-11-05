

Rhino = _B19_RHINO                                   # b19_pre.py: given back after the make_board part was read

# ================================================================ B19 plan v1 (5 Nov 2026, Aras 19:51 + 20:47 + 20:59)
# A NEW standalone script: the masterplan's proposal (option A: zones, corridor, walks, hubs, trees; computed here by
# the masterplan's own code, read from the open file like the masterplan does) drawn in the drawing language of
# B19 "Greenikka" (Arkkitehdit MY, Viinikanlahti competition 2020, 3rd prize), general plan page 5
# -> library/examples/liked_2026-11-05/B19_SCRIPT_SPEC.md (targets 1-11), BRIEF.md (card).
# B19's own geometry (Tampere) is NOT copied: every drawing element of it is, on our proposal's geometry:
# dark slate water with a fine bank line, light ground over the whole project zone, white buildings with grey
# outlines, lawns and greens in light sage washes, trees as transparent sage crowns of mixed tones with a soft
# shadow, light grey paving, mauve movement lines, red facility marks, small black names beside their places,
# everything outside the project zone veiled whitish, the zone in a thin dark red line.
# Writes output/bergama_b19_plan/Bergama_B19_plan_v1.pdf (true size at 1:scale); rhino_bake = True bakes it on
# layer B19. It writes nothing another script reads (no masterplan_results.json, no booklet items).
VERSION = "bergama_b19_plan v1 (2026-11-05)"
SHORT = "v1"
GH_LABEL = "B19Plan"
SETTINGS = ("rhino_bake", "scale")
OUT_FOLDER = "bergama_b19_plan"
LOG_NAME = "bergama_b19_plan_log.txt"
BAKE_ROOT = "B19"
B19_SCALE = 2000.0           # default print scale (design spec, 5 Nov 21:0x; input `scale` overrides)
B19_NAME = "Bergama_B19_plan_v1.pdf"
B19_M = 15.0                 # mm paper margin (design value)
B19_HEAD = 20.0              # mm band under the plan: title, scale bar, north arrow (design value)
B19_A1 = (841.0, 594.0)      # ISO 216 A1, mm: the log says whether the sheet fits it
B19_VEIL = 0.6               # opacity of the whitish veil outside the project zone (design value)
B19_BORDER_MM = 0.35         # project zone line, mm (design value)
B19_NAME_MM = 2.12           # place names 6 pt (booklet minimum)
B19_ZONE_MM = 1.76           # zone names 5 pt
# Colours SAMPLED from B19 page 5 (B/liked-B/B19-masterplan/B19_board01_ark-kili_5-2020_Viinikanlahti_lowres_page05.png,
# 3308 x 2339 px), 5 Nov 2026: k-means 16 colours of the project area (water, white, greens, greys) and medians of
# hue-filtered pixels for salmon, dark red, sand and mauve. Values are the page's, not our palette (spec item 4).
B19_COL = dict(water="51626C", water_edge="4B5A64", deep="3D4340", lawn="B9C4B1", green="A7AF9E", tree="94988A",
               tree_dark="798274", shadow="616758", paving="D8D9D5", ground="E4E4E0", white="FBFBFA",
               line="C9CCC4", red="EA8477", border="692F28", sand="ECCCA8", mauve="9C6D70", ink="1E1E1E")
B19_HUE = {                  # masterplan legend key -> B19 colour (keys missing here keep the masterplan's hue)
    "bld": "white", "bld_edge": "tree", "her": "red", "her_edge": "border", "since": "ground", "street": "line",
    "bridge": "tree", "road_kept": "line", "eco": "lawn", "ring": "paving", "flood_plant": "green",
    "widen": "water", "widen_edge": "deep", "reed": "green", "reed_edge": "tree_dark", "arm": "water",
    "terrace": "tree_dark", "drytop": "lawn", "drytop_edge": "tree_dark", "spill": "water", "spill_edge": "deep",
    "store": "water_edge", "cch": "deep", "hidden": "water",
    "dg": "lawn", "dg_edge": "tree_dark", "dg_gather": "paving", "dg_row": "tree_dark",
    "walk": "mauve", "walk_bed": "mauve", "bike": "mauve", "foot": "mauve", "stones": "tree", "canopy": "tree_dark",
    "road_pedestrian": "mauve", "road_calmed": "mauve", "road_shared": "mauve", "road_relocated": "line",
    "road_later": "line", "street_cut": "mauve", "square": "paving", "square_edge": "tree", "market": "red",
    "walkhub": "red", "transit": "red", "gate": "red", "sub": "red", "seat": "red", "cafe": "red", "edu": "red",
    "view": "red", "deck": "red", "sight": "tree", "left": "ground"}
B19_NOT_IN_PROPOSAL = (u"harbour piers and marina boats", u"tram line", u"red public building footprints "
                       u"(our proposal adds no buildings)", u"beach sand")   # B19 elements with no match: not drawn

_b19_h0 = pl23_h


def pl23_h(key):
    """B19: the masterplan legend key's colour from B19_COL (else the masterplan's own hue)"""
    c_ = B19_HUE.get(key)
    return B19_COL[c_] if c_ else _b19_h0(key)


def ml_study_items(rings=None, D=None):
    """B19: the shared violet study line is not drawn; b19_page draws the zone in B19's thin dark red line"""
    return []


def icon(pg, kind, x, y, s):
    """B19: every facility gets the SAME mark (spec item 7, 11): a small red block with a dark red edge"""
    h = s * 0.32
    pg.poly([rect(x - h, y - h, x + h, y + h)], fill=B19_COL["red"], stroke=B19_COL["border"], lw=0.1)


def pl23_water_draw(pg, C, T, k, on, spacing):
    """B19: the stream as one dark slate surface with a fine dark bank line; islands left open"""
    rings = []
    for R, Hs in pl23_water_groups(C):
        Q = [T(p) for p in R]
        if not on(Q):
            continue
        QH = [[T(p) for p in H] for H in Hs if len(H) >= 3]
        pg.poly([Q] + QH, fill=B19_COL["water"], stroke=B19_COL["deep"], lw=0.15)
        rings.append(Q)
        rings += QH
    return rings


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0, distinct=True, style="b", month=None, season=None):
    """B19: a tree from above = a transparent sage crown (one of three tones by seed) over a soft shadow to the
    south-east; crown width = the species' sourced crown (plants.py PLA_SPECIES) unless crown_m is given"""
    cm = crown_m or (PLA_SPECIES.get(key) or {}).get("crown_m", 6.0)
    r = max(0.35, cm * k / 2.0)
    tone = (B19_COL["green"], B19_COL["tree"], B19_COL["tree_dark"])[seed % 3]
    ring_ = lambda ox, oy: [(cx + ox + r * math.cos(a * math.pi / 8.0), cy + oy + r * math.sin(a * math.pi / 8.0))
                            for a in range(16)]
    return [("poly", ring_(0.18 * r, -0.18 * r), B19_COL["shadow"], None, 0.0, 0.3),
            ("poly", ring_(0.0, 0.0), tone, B19_COL["tree_dark"], 0.08, 0.85)]


def b19_page(C, site, study, scale, warn):
    """The sheet: the plan of site_alan at 1:scale (true size) with the head band under it. Returns (Page, notes)."""
    k = 1000.0 / scale
    x0, y0, x1, y1 = bbox(site)
    dw, dh = (x1 - x0) * k, (y1 - y0) * k
    T = lambda p: ((p[0] - x0) * k, (p[1] - y0) * k)
    sub = Page(dw, dh)
    st = [[T(p) for p in R] for R in study if len(R) >= 3]
    with mpx_grp(sub, "ground", u"project ground"):     # spec item 8: no blank part inside the project zone
        sub.poly(st, fill=B19_COL["ground"])
    used, specs, icons = draw_corridor(sub, T, k, C, lambda p: True, dw, dh, [], [])
    with mpx_grp(sub, "ground", u"outside the project zone"):   # spec item 6: whitish outside
        sub.poly([rect(0.0, 0.0, dw, dh)] + st, fill="FFFFFF", alpha=B19_VEIL)
    with mpx_grp(sub, "annotations", u"project zone"):
        for Q in st:
            sub.line(Q + Q[:1], B19_COL["border"], B19_BORDER_MM)
    taken = [b for b, _ in icons]                        # spec item 7: names beside their places, never overlapping
    put, skipped = 0, []

    def place(s_, x, y, size, bold):
        w = text_w(s_, size, bold)
        for dx, dy in ((1.0, -size * 0.35), (-1.0 - w, -size * 0.35), (-w / 2.0, 1.2), (-w / 2.0, -1.2 - size)):
            b = (x + dx, y + dy, x + dx + w, y + dy + size)
            if b[0] < 0 or b[1] < 0 or b[2] > dw or b[3] > dh:
                continue
            if any(not (b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]) for o in taken):
                continue
            taken.append(b)
            sub.text(s_, b[0], b[1], size, B19_COL["ink"], bold=bold)
            return True
        return False
    for sp in specs:
        if sp.get("study"):
            if place(sp["text"], sp["xy"][0] + sp.get("r", 0.0), sp["xy"][1], B19_NAME_MM, True):
                put += 1
            else:
                skipped.append(sp["text"])
    ins = C.in_study
    for z in C.D.zones:
        nm = z.get("label") or u""
        q = z.get("q")
        if not nm or not q or not ins(q):
            continue
        x, y = T(q)
        if place(nm, x, y, B19_ZONE_MM, False):
            put += 1
        else:
            skipped.append(nm)
    W, H = dw + 2 * B19_M, dh + 2 * B19_M + B19_HEAD
    pg = Page(W, H)
    pg.poly([rect(0.0, 0.0, W, H)], fill="FFFFFF")
    blit(pg, sub, B19_M, B19_M + B19_HEAD)
    pg.text(u"MIRAQUA · MASTERPLAN", B19_M, B19_M + 8.0, 4.2, B19_COL["ink"], bold=True)
    pg.text(u"drawing language after Greenikka (Arkkitehdit MY, 2020), general plan", B19_M, B19_M + 3.0, 2.12,
            B19_COL["ink"])
    scale_bar(pg, B19_M + 130.0, B19_M + 3.0, scale, marks=(0.0, 50.0, 100.0, 200.0))
    nx, ny, h = W - B19_M - 4.0, B19_M + 2.0, 12.0       # north arrow: survey +y = north (assumed, as the survey)
    pg.poly([[(nx, ny + h), (nx - 2.6, ny + 0.45 * h), (nx, ny + 0.6 * h), (nx + 2.6, ny + 0.45 * h)]],
            fill=B19_COL["ink"])
    pg.line([(nx, ny), (nx, ny + 0.6 * h)], B19_COL["ink"], 0.25)
    pg.text(u"N", nx, ny + h + 1.0, 3.0, B19_COL["ink"], bold=True, align="C")
    fit = (W <= B19_A1[0] and H <= B19_A1[1]) or (W <= B19_A1[1] and H <= B19_A1[0])
    notes = [u"sheet {:.0f} x {:.0f} mm at 1:{:,.0f}: {}".format(W, H, scale, u"fits A1" if fit else
                                                                     u"LARGER than A1 (841 x 594)"),
             u"names placed {}, left out (no free room) {}{}".format(put, len(skipped), u": " + u"; ".join(skipped)
                                                                     if skipped else u""),
             u"legend keys drawn: " + u", ".join(sorted(used)),
             u"FLAG B19 elements with no match in our proposal, not drawn: " + u"; ".join(B19_NOT_IN_PROPOSAL),
             u"FLAG targets 8-11 (no gaps, designed edges, gradual water edge, one style) are not measured by the "
             u"script: check on the PDF"]
    if not fit:
        warn.append(u"B19 plan: sheet {:.0f} x {:.0f} mm is larger than A1 at 1:{:,.0f}".format(W, H, scale))
    if skipped:
        warn.append(u"B19 plan: {} name(s) left out for lack of free room: {}".format(len(skipped),
                                                                                      u"; ".join(skipped)))
    return pg, notes


def build_all(doc, warn):
    """Read the open file, compute the proposal (masterplan code, option A), draw and write the B19 sheet.
    Returns (folder, files, log lines, pages, scale) as main() expects."""
    folder = out_folder(doc)
    os.makedirs(folder, exist_ok=True)
    wn_reset()
    mpx_start()
    del MPX_PAGES[:]
    scale = inp_num("scale", B19_SCALE, warn)
    _SCALE[0] = scale
    if doc is not None:
        load_palette([DATA_DIR] + search_dirs(doc), warn)
    areas = read_areas(doc) if doc is not None else {}
    if len(areas) < 2:
        areas = calisma_from([ring(list(P)) for P in CALISMA_COPY])
        warn.append(u"no calisma_alan outlines in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) "
                    u"was used")
    site, site_found = read_site(doc)
    if not site_found:
        warn.append(u"no site_alan outline in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    V = View(areas, 0.0, 1000.0 / scale, frame=site)
    V.frame_P, V.study = list(site), [areas[k_] for k_ in sorted(areas)]
    bb = [bbox(A) for A in areas.values()] + [V.bb]
    R = (min(b[0] for b in bb) - RING_M - 5, min(b[1] for b in bb) - RING_M - 5,
         max(b[2] for b in bb) + RING_M + 5, max(b[3] for b in bb) + RING_M + 5)
    survey = read_survey(doc, R) if doc is not None else {}
    its = read_items(doc, "A") if doc is not None else []
    if not its:
        zb = zone_base_file(doc, warn)
        its = [i for i in zb[1] if i["layer"].startswith("Option_A::")]
        src = zb[0]
        if not its:
            its = [i for i in embedded_items() if i["layer"].startswith("Option_A::")]
            src = u"the copy of zone base v5 embedded in this script"
        warn.append(u"no Option_A::INT_ zones in the open file; {} was used".format(src))
    D = Design(its, areas, warn, "A")
    CL = city_layer("A", D, areas, survey, warn)
    spots = read_spots(doc, [V.bb]) if doc is not None else []
    t0 = time.time()
    C = Corridor(V, survey, CL, D, spots, warn)
    lines = [u"proposal computed (masterplan code, option A): zones {}, hubs {}, {:.1f} s".format(
        len(D.zones), len(C.hubs), time.time() - t0)]
    pg, notes = b19_page(C, site, C.study or V.study, scale, warn)
    lines += notes
    path = save(pg, folder, B19_NAME, u"MIRAQUA masterplan, B19 drawing language")
    lines.append(u"{}  {}".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S")))
    return folder, [path], lines, [("A", 1, pg)], scale


if Rhino is not None:
    try:
        _txt, _files = main()
    except Exception as _ex:
        _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
        gh_status(SHORT + " · ERROR")
        mem_set("ver", VERSION)
        mem_set("last", _txt)
        mem_set("status", SHORT + " · ERROR")
    log = _txt
    print(_txt)
    pdf = _files
