# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_agriculture_alternatives_v9.py = v9 (1 Nov 2026, round 4; what changed: the NEW IN / VERSION notes below)
# bergama_agriculture_alternatives_v8.py (v8, 31 Oct: round 3, p18 + p19 merged on ONE booklet page) · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             the site board's plan 01 "What is there" at a round scale with the fields and orchards fed
#   3 SOURCES                       the numbered key of the [n] marks on pages 1-2
# T4a (revision 29 Oct, WO-T4a-4): D9 a: the plant ladder page (booklet p20) is gone with everything only it used (its
#   content lives on the water board's p17 and p14-15); pictograms and step markers from common/icons.py (02 §2); D13:
#   sources naming our own model run or method and status words never reach the printed key (cite).
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math, re

VERSION = "v9"  # v9 (round 4, S6b: booklet p19 rebuilt as story groups, real Arial text check, one trigger file); v8.3 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v8.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v8.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
# NEW IN v9 (round 4, 1 Nov, session S6b; P19.1, K4, G-R4-1/2/7/11; spec revision_2026-11-01_round4/handover/
#   S6b_p19_design_spec.md): booklet p19 "Where the clean water goes, and what it grows" is rebuilt as story groups,
#   each with ONE heading inside its first crop, the crops of a row sharing their top and bottom edges; every figure,
#   source and photo kept (K4), only the layout and the duplicate titles changed:
#   * ag1_stream 260 x 40 (group 2 "HOW MUCH WATER REACHES THE FARMS", was "THE STREAM COMES FIRST"); ag1_bars
#     194 x 72 (group 3 "HECTARES ONE STORAGE IRRIGATES, BY CROP"); ag1_context 194 x 72 (group 4 "WHY CROP CHOICE
#     IS THE LEVER": the reading's squares and 2.2-4.4 x on top, the four tiles under it); ag1_history 260 x 34 (group
#     5 "THE CROPS, THEN AND NOW"); ag1_crops 128 x 34 (the photos at the one booklet photo size). ag1_reading is no
#     crop any more (drawn inside ag1_context). Booklet captions of these crops are empty (the heading says it).
#   * G-R4-1: text widths from the real Arial (text_w = font_metrics.fm_width; common/text_w.py and the Helvetica
#     table gone); one TextPage per booklet crop (common/text_place.py): every text registered, the drawings no text
#     may touch (icons, bars, photos, squares) are keeps, a collision RAISES; log "overlap p19 <crop> checked n,
#     collisions 0" (lp_overlap_flag / ag_flags gone). ² and ³ are the embedded font's own glyphs (the raised 0.6 x
#     digit printed under 6 pt).
#   * G-R4-2: wrap and Page.para never leave a one-word last line. G-R4-7: the step chips' numbers through
#     common/marker.py mk_marker. G-R4-11: the timeline's "Red Hall" is Kızıl Avlu from the shared names table.
#   * Trigger: the script's own copies (common/chain_fire.py, gh_in_items.py, the globals scan) are replaced by
#     common/trigger.py trig_should_run (a press of the Button or a new done text on its own inputs); the log says
#     "trigger: <why>". results.json keys and the other crop ids are unchanged.
# NEW IN v8 (round 3, B4 · P18.1-P18.4, D8, G2, G3, G4, G17; spec revision_2026-10-31_round3/handover/B4_work/
#   spec_p18_merged.md): page 1's five booklet crops are drawn at 1:1 for ONE merged booklet page and carry "bk_w"
#   (the booklet keeps them 1:1): ag1_stream 260 x 40 mm (the to-farms headline folded in: ag1_headline is gone),
#   ag1_bars 227 x 66 (direct labels, no key row), ag1_context 161 x 66 (tiles 2 x 2), ag1_reading 128 x 31 (two
#   squares by area + the ratio), ag1_history 128 x 31 (no leader lines), ag1_crops 128 x 31. No strokes around tiles
#   or photos (G17). P18.2: the photos go in as plain images (common/plant_photos.py, A2) and the log says
#   "photos: n of m placed as images"; "FLAG overlap p18 <crop> n" per crop (label_place.py).
# NEW IN v7 (round 2, Aras 31 Oct 11:13: p18 + p19 on one page if legible, PG2 p18-19, M10): ag1_bars compact (rows
#   14 mm apart, bars 5 mm, grid 165 mm wide: about 239 x 98 mm, was 264 x 113); ag1_reading one strip 252 x 28 mm
#   (was 244 x 48): the two dry-year bars it repeated from ag1_bars are gone (a fact once), the ratio and the lever stay.
# Revision 30 Oct (T5, booklet p.19; M10, G4): every fact once in the booklet. Storage (p.10) is no longer printed
#   here (headline, store legend); the olive area is facts.py "8,705 ha", printed once (the olive bar row; the
#   cotton tile and the timeline no longer repeat the 2025 areas: "8,700" gone); the olive full-irrigation row prints
#   its normal-year need from facts.py (the dry-year need and 1.25 ha are p.18's); "what it replaces" (1.25 ha again,
#   and a note on an older board version) is gone with its crop ag1_replaces.
# NEW IN v5.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): p.19 "10,000 m³ = N ha olive" is computed live, the
# same way as the water board's p.18 (10,000 / gross m³ a ha of olive in a dry year, from water_balance_results.json);
# it was the fixed text "1.22 ha".
# v4 (MIRAQUA 28 Oct, booklet revision v4, pages 18-19; a feature change, so the next whole number):
#   * P18.1 / P19.3 / P19.4 / G11 / G12: every photo through common/plant_photos.py; corn printed as "Corn (Mısır)"
#     (data key "maize" and the Wikimedia file kept); an empty frame says "no photo: <reason>".
#   * P19.1 / G5 / F10: the kicker top left; page 3's top-right corner on the booklet grid (column 8, 4 rows 5.2 mm
#     apart, 7.5 pt): steps 1-5, NEXT -> D The heritage loop (title bold), the chain key; no big page numbers.
#   * P19.2: the ladder's people from common/figures.py at true scale (1.75 m), one colour, no stroke.
#   * G4 / F13: ladder labels placed by common/label_place.py clear of figures, lines, plants and each other;
#     "hub square: dry, step-free" and "wade the strip" now print.
#   * G13: flood heights in m with 2 decimals (values unchanged). Bank depth research 28 Oct §4.5: over the bank top
#     only at S4 (left); K4 before the DSİ walls.
#   * F5: [n] marks only for public online sources; internal pointers out of the printed source list.
#   * G1: page 2's group line removed; page 1's left column on the 14 mm margin.
# v3.1 (bugfix, Aras 27 Oct, booklet Prompt 8 "final check of every page"): plant and crop names "English (Turkish)"
#   from the shared table where pages 1 and 3 still had the English alone: page 3's season row OLIVE (ZEYTİN) HARVEST,
#   its labels (hub square: oriental plane (Doğu çınarı) shade; common reed (Kamış) gold; olive (Zeytin) harvest;
#   olive (Zeytin) trees on the fields) and page 1's "what it replaces" figure. Page 3: "stored winter water" and
#   "site edge: farmland outside" sit at the row's top edge, so they found no free place above it and were left out on
#   every run: they now go under their anchors. The h01 timeline quotes stay word for word. Page 1's "THE STREAM COMES
#   FIRST" block and the step chips: its 6.5 pt words are 7 pt, the smallest size on a booklet page.
# v3 (Aras 27 Oct 17:35, Prompt 6 "water, part 3"; the booklet's p.24-25):
#   * page 1, "THE STREAM COMES FIRST" between the headline and the bars (task 1: "show the defence ON the board"): the
#     priority 1 stream: summer strip -> 2 on-site planting -> 3 farms (the model has no draw of its own for the
#     planting: it lives on the strip's water, so it shares the strip's bar); the design store through a normal and the
#     1-in-5 dry water year as two stacked bars on one scale (strip, farms, left over; the store size dashed across
#     both), read live from the water balance v4 results (design.year_split, one daily run); and the double squeeze in
#     one line, computed: water left for the farms after the strip, the need per hectare and the hectares that water
#     serves, dry year against normal, then why deficit-irrigated olive is the lever. Without year_split (water balance
#     v3 or older) only the priority row is drawn (logged). The bars move down to make room: rows 16.5 mm apart (were
#     19.5), the reading box ends at the 14 mm margin.
#   * pages 1 and 3 say where they sit in the booklet: "C WATER · WHAT WE DO WITH IT" (was "AGRICULTURE ANALYSIS");
#     page 3, the last page of the water theme, closes it top right: what we do with the water in five steps and NEXT
#     D HISTORY AND HERITAGE (rule 7, task 3).
#   * m² and m³ are written as a raised small 2 or 3 (0.6 x the size, as wide as the glyph), which every PDF viewer
#     shows (task 2: "325,000-375,000 m" in some viewers).
# v2 (Aras 27 Oct, Prompt 5, rule 8: "Plant names: English first, Turkish in brackets, no Latin ... Every plant AND every
# crop in the booklet gets a photo of the plant itself ... openly licensed photos ... credited in the sources ... Same
# crop ratio and size for every photo"): every plant and crop name on pages 1 and 3 is "English (Turkish)" from the
# shared table (src/common/plant_photos.py), no Latin names on the pages. Page 3's step columns show each step's plants
# as photos (PHOTO_W x PHOTO_H mm, two side by side) with the name and the photo's [n] credit under each; the giant reed
# under REMOVE. Page 1 adds "THE CROPS" under the timeline: olive, cotton, corn, tomato as photos. The photos come
# from the shared cache Downloads/Bergama/cached/plant_photos/ (the water board shows the same photo of the same
# plant) and go into their frames with PyMuPDF after the PDF is written; a missing one is an empty frame saying "no
# photo", never an error; the log says how many were placed. Room on page 3: the chain sits 4 mm higher, the season rows
# are 50 mm (were 52; 4.5 mm stay above the tallest tree); the plants' reasons are left out under the photos when the
# column would not fit (logged). The Data file changes (STEPS: plant keys instead of botanical names): copy the new one.
# v1.7 (bugfix, Aras 27 Oct 16:05): page 3 crashed ("too many values to unpack": the sketch engine's items now
# carry a 4th value, the label group); the text under the component shows a newly pasted version at once, idle.
# v1.6 (Aras 27 Oct 11:07, booklet p24-26; revision_2026-10-27/PHASE2_SPEC.md): white pages (the beige paper goes); no
# source footers or credit lines on the pages: the [n] marks are numbered once for the sheet and their key is a 4th
# page "Sources" (the booklet's sources page reads it there). Page 1 adds "why the stored water goes to farms": a
# cotton / olive timeline in card h01's words and years, labels placed by measured width. Page 3 rebuilt for option A:
# the one-way chain upstream entry -> K4 -> K3 -> İstiklal -> K5 -> K6 -> downstream -> farmland outside the site,
# hubs and in-bed sub-hubs, programme and historic roots; the ladder drawn three times (high water, low water, olive
# harvest) with what people do on each step; the species under each step. Every label is placed by a collision check
# (Placer): a label with no free place is left out and named in the log.
# v1.5 (Aras 26 Oct 07:06, review of the deck, p.33-34): page 2's map is the site board's own plan 01 ("What is there",
# board v42+, cut from its sheet PDF with PyMuPDF and scaled by one factor, never redrawn) at the largest round scale
# that fits, with only the farms layer drawn on it (fields and orchards fed, their extent), the plan's own key, the
# figures beside it and a context line; v1.4's land cover drawing stays only as a flagged fallback. Page 3's ladder is
# drawn by the proposal sections' sketch engine (the p.23 upstream entry's language): hand ground, washes, winter
# water and summer strip, the faint design-flood reach, level marks, sketch plants and people, rain and sun marks.
# The "# r: pymupdf" line installs PyMuPDF in Rhino 8 on the first run (as the booklet).
# v1.4 (Aras 25 Oct 21:47-22:02, booklet stage 3): the booklet shows crops of this sheet (booklet/CROP_SPEC.md):
# blocks.json lists one crop per panel of the three pages and results.json keeps v1.3's keys; the v1.3 booklet redraws
# are gone. Caveat notes taken off the sheet (labels kept); "stream", never "river". Page 3's ladder drawn in the site
# board's section language (src/common/section_style.py): cut ground with sloped banks, the strip hatched, whole plants,
# one size across and up.
# v1.3 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/<folder>/booklet/: c7_hero.pdf (plant ladder +
# the water board's planting bands A-F), c8_b.pdf (hectares per crop bars), blocks.json (every word a label) and
# results.json (hectares per crop). The A3 sheet is unchanged.
# v1.2 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first): sentences become pictogram tiles, callouts and tags; method
# and source sentences become [n] marks with one numbered source key in each page's footer; layout and colours kept.
# Flood figures corrected to the surveyed sections (research/rain_river_levels/README.md, v1.1 correction and line 49).
# v1.1 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_agriculture_alternatives_log.txt (next to cached/ and output/), overwritten by each press.
# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))
# ---- plant photos, shared by the water board and the agriculture alternatives (Aras 27 Oct, Prompt 5: "every plant
# AND every crop in the booklet gets a photo of the plant itself. Use openly licensed photos (e.g. Wikimedia Commons)
# credited in the sources, never photos from shop or nursery sites. Same crop ratio and size for every photo").
# MIRAQUA round 28 Oct (G12): every photo is PINNED to one Wikimedia Commons file page (PLANTS), the whole plant or
# crop in its setting, the same file wherever the species shows. No lead image and no search at run time (they gave
# the museum cob and the African olive). Why cards printed "not loaded": Wikimedia answered a burst of 3-4 requests a
# plant with HTTP errors (most likely 429, too many requests) and the code kept asking. Now: ONE batched API call for
# all photos still to fetch, then one 500 px download at a time with a pause, Retry-After honoured once, and after a
# second refusal nothing more this press (remembered 10 min, so a quick second press does not trip it again). The
# user agent names the project and its repository (Wikimedia's user-agent policy).
# Fetched once on Aras's PC (the cloud cannot reach Wikimedia), kept in the cache folder and read from there on every
# later press. Any licence is accepted (D8, PHOTO_ANY_LICENCE); credits stay. A photo Aras puts into the cache folder
# himself (<key>.jpg with a <key>.json {"file", "credit"}) is used as it is. If the pinned files cannot be fetched,
# an older cached photo of the same plant stays (where its row allows), else the frame says why.
# Credit (Aras 28 Oct 11:38, fault table F15: "no Latin file names"): author, licence, Wikimedia Commons and the page-id
# link that opens exactly that file page; PHOTO_CREDIT_FILE = True adds the file name (brief G12) if that is chosen.
PHOTO_W, PHOTO_H = 28.0, 21.0        # mm on the A3 page, every photo in the booklet (4:3, cover-cropped, never stretched)
PHOTO_PX = 500                       # px wide fetched: a standard Wikimedia thumbnail step (about 450 dpi at PHOTO_W)
PHOTO_CREDIT_FILE = False            # True = the credit names the Commons file too (G12) besides the page-id link (F15)
PLANT_PHOTO_DIR = bg_cache("plant_photos")   # one folder for every script: the same plant shows the same photo
# Every plant and crop the booklet names: key -> (printed name "English (Turkish)", the Commons files to use in order
# (file page titles without "File:"; the first that is free and loads is used), keep_old = an older cached photo of
# this plant may stay when none of them loads). Names: English and Turkish as in research/water_data/04 §1 (species
# matrix), Aras's examples "Common reed (Kamış)", "Oriental plane (Doğu çınarı)"; Kofa = the rush genus Juncus
# (turkiyebitkileri.com, Juncaceae - Kofagiller, Juncus - Kofa). Files: revision_2026-10-28/checks/photos.md §2-3
# (whole plant in its setting; author and licence are read from each file page at the fetch and checked there).
PLANTS = {
    "reed": (u"Common reed (Kamış)", (u"Common Reed (Phragmites australis) (8131465127).jpg",
                                     u"Reed panicle at Brodalen 1.jpg"), True),
    "cattail": (u"Broadleaf cattail (Hasır otu)", (u"Bulrush (Typha latifolia) (8139113636).jpg",), True),
    "mint": (u"Water mint (Su nanesi)", (u"Mentha aquatica Meinerswijk.jpg", u"Mentha aquatica 02.jpg"), True),
    "iris": (u"Yellow flag iris (Sarı süsen)", (u"Yellow Iris, Gunnersbury Triangle.JPG",
                                                u"Iris pseudacorus (yellow flag iris) (Newark, Ohio, USA) 5 (27772297656).jpg"), True),
    "rush": (u"Sharp rush (Kofa)", (u"Juncus acutus2.jpg",), True),
    # H-B 30 Oct (M6, p16 gap): titles from the Commons search index (T1 sourcing §2 and a web search, 30 Oct); not
    # opened from here (Commons blocked in the cloud): UNVERIFIED until the first fetch on Aras's PC logs them.
    # Turkish name of Juncus effusus not verified: the genus name Kofa (as for the sharp rush) is used.
    "soft_rush": (u"Soft rush (Kofa)", (u"Pitrus (Juncus effusus) 07.JPG", u"Pitrus plant (Juncus effusus) (1).jpg",
                                       u"Pitrus (Juncus effusus) 05.JPG", u"JuncusEffusus.jpg"), True),
    "stone_pine": (u"Stone pine (Fıstık çamı)", (u"Stone Pine (Pinus pinea) - Rome, Italy 2024-03-04.jpg",
                                                 u"Pinus pinea.JPG"), True),
    "loosestrife": (u"Purple loosestrife (Aklar otu)", (u"Lythrum salicaria, field of purple loosestrife, Concord, Massachusetts.jpg",
                                                        u"Purple Loosestrife (Lythrum salicaria) - geograph.org.uk - 950598.jpg"), True),
    "tamarisk": (u"Tamarisk (Ilgın)", (u"A Tamarisk Tree in Israel (5759425470).jpg", u"Tamarix canariensis-Daimiel.jpg"), True),
    "willow": (u"White willow (Ak söğüt)", (u"A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi, Finland, 2018 September.jpg",
                                            u"Silberweide (Salix alba).JPG"), True),
    "chaste": (u"Chaste tree (Hayıt)", (u"Vitex-agnus-castus-habitus.jpg", u"Vitex-agnus-castus-habit.JPG"), True),
    "poplar": (u"White poplar (Ak kavak)", (u"Pioppo (populus alba).jpg", u"Daniel Fuchs.CC-BY-SA.Populus alba.jpg"), True),
    "ash": (u"Narrow-leaved ash (Dişbudak)", (u"Fraxinus angustifolia - Israel.JPG", u"Fraxinus-angustifolia.jpg"), True),
    "oleander": (u"Oleander (Zakkum)", (u"Oleander (Nerium oleander) habit.jpg", u"Nerium oleander (Adelfa).jpg"), True),
    "plane": (u"Oriental plane (Doğu çınarı)", (u"Oriental Plane tree - Platanus orientalis - Doğu Çınarı, Arslanköy 04.JPG",
                                                u"TRSTENO ORIENTAL PLANE TREE, CROATIA.jpg"), True),
    "lavender": (u"French lavender (Karabaş otu)", (u"Lavandula stoechas (cantueso).jpg", u"Lavandula stoechas 1.JPG"), True),
    "rosemary": (u"Rosemary (Biberiye)", (u"Large rosemary bush.jpg", u"Rosmarinus officinalis (Italy) 01.jpg"), True),
    "olive": (u"Olive (Zeytin)", (u"Olive trees on Thassos.JPG",), True),       # was the African wild olive (Cape Town)
    "cotton": (u"Cotton (Pamuk)", (u"CottonPlant.JPG",), True),
    "maize": (u"Corn (Mısır)", (u"Maize field, Balcalı 01.jpg", u"A Maize Crop with beautiful Corn.jpg"), False),  # G11, P18.1:
    "tomato": (u"Tomato (Domates)", (u"Solanum lycopersicum in Kaunas.jpg",), True),                       # never the cob
    "giant_reed": (u"Giant reed (Kargı)", (u"Poaceae plant at golden hour near the river in Laos.jpg",
                                           u"Arundo donax 2007.JPG"), True),
}


def plant_name(key):
    """The printed name of a plant: "English (Turkish)"."""
    return PLANTS[key][0]


def plant_photo_of(key, log, state):
    """(jpeg path or None, credit or None, why not) of a plant in PLANTS, from the shared folder."""
    name, files, keep_old = PLANTS[key]
    return plant_photo(key, name, files, keep_old, PLANT_PHOTO_DIR, log, state)


PHOTO_UA = ("MIRAQUA-booklet/3 (https://github.com/SupFlyn/BergamaProjectScripts; Bergama student project, "
            "Yasar University) Python-urllib")
PHOTO_TIMEOUT = 8.0                  # s per request; after one network failure the rest are not tried this press
PHOTO_PAUSE = 1.0                    # s between two downloads
PHOTO_HOLD = 600.0                   # s: after Wikimedia refused twice, no new request for this long (any press)


def jpeg_info(data):
    """(width, height, colour components) of JPEG bytes (baseline or progressive), else None."""
    import struct
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        m = data[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        n = struct.unpack(">H", data[i + 2:i + 4])[0]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (w, h, data[i + 9]) if data[i + 9] in (1, 3) else None
        i += 2 + n
    return None


def _photo_http(url, state):
    """the bytes at url; an HTTP 429/503 waits for its Retry-After (at most 30 s) and tries once more, a second
    refusal sets state["refused"] (nothing more is fetched this press). A pause before every request but the first."""
    import time
    import urllib.request
    import urllib.error
    for attempt in (0, 1):
        wait = PHOTO_PAUSE - (time.time() - state.get("last", 0.0))
        if wait > 0:
            time.sleep(wait)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": PHOTO_UA})
            with urllib.request.urlopen(req, timeout=PHOTO_TIMEOUT) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code not in (429, 503):
                raise
            if attempt:
                state["refused"] = u"Wikimedia refused (HTTP %d)" % ex.code
                _photo_hold(state["refused"])
                raise
            try:
                ra = float(ex.headers.get("Retry-After") or 5.0)
            except Exception:
                ra = 5.0
            time.sleep(min(30.0, max(1.0, ra)))
        finally:
            state["last"] = time.time()


def _photo_hold(why=None):
    """the refusal memo in the cache folder: written with why, else read: (why, seconds left) or None"""
    import time
    p = os.path.join(PLANT_PHOTO_DIR, "_refused.json")
    try:
        if why:
            os.makedirs(PLANT_PHOTO_DIR, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"why": why, "t": time.time()}, f)
            return None
        with open(p, "r", encoding="utf-8") as f:
            m = json.load(f)
        left = PHOTO_HOLD - (time.time() - float(m["t"]))
        return (m["why"], left) if left > 0 else None
    except Exception:
        return None


def _png_to_jpeg(src, dst):
    """A PNG turned into a JPEG on white by .NET System.Drawing (Rhino on Windows); False where that is missing."""
    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing as SD
        bmp = SD.Bitmap(src)
        out = SD.Bitmap(bmp.Width, bmp.Height)
        g = SD.Graphics.FromImage(out)
        g.Clear(SD.Color.White)
        g.DrawImage(bmp, 0, 0, bmp.Width, bmp.Height)
        g.Dispose()
        out.Save(dst, SD.Imaging.ImageFormat.Jpeg)
        bmp.Dispose()
        out.Dispose()
        return True
    except Exception:
        return False


PHOTO_ANY_LICENCE = True            # D8 (Aras, 30 Oct): licences are not regarded; every source is still credited


def photo_free(lic):
    """True for an open licence: CC BY / CC BY-SA (any version), CC0, public domain; always True while
    PHOTO_ANY_LICENCE (D8)."""
    if PHOTO_ANY_LICENCE:
        return True
    t = (lic or u"").lower()
    if not t or "non-free" in t or "fair use" in t or "-nc" in t or "-nd" in t or " nc" in t or " nd" in t:
        return False
    return t.startswith("cc by") or t.startswith("cc-by") or t.startswith("cc0") or "public domain" in t or \
        t.startswith("pd")


def _photo_meta(info):
    """(author, licence) from a Commons imageinfo record's extmetadata."""
    import re
    md = info.get("extmetadata", {}) or {}
    artist = re.sub(r"<[^>]+>", u"", md.get("Artist", {}).get("value", u"")).strip()
    return re.sub(r"\s+", u" ", artist), md.get("LicenseShortName", {}).get("value", u"").strip()


def _photo_infos(titles, state):
    """ONE Commons API call for up to 50 file titles: {title: imageinfo record + pageid} for the files that exist"""
    import urllib.parse
    out = {}
    for i in range(0, len(titles), 50):
        part = titles[i:i + 50]
        q = json.loads(_photo_http("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
                                   "&iiprop=url|mime|size|user|extmetadata&iiurlwidth={}&titles={}".format(
                                       PHOTO_PX, urllib.parse.quote(u"|".join(u"File:" + t for t in part))),
                                   state).decode("utf-8"))
        qq = q.get("query", {})
        norm = dict((n_.get("to"), n_.get("from")) for n_ in qq.get("normalized", []) or [])
        for pg_ in qq.get("pages", {}).values():
            ii = (pg_.get("imageinfo") or [None])[0]
            if "missing" in pg_ or not ii:
                continue
            t = pg_.get("title", u"")
            t = norm.get(t, t)
            ii["pageid"] = pg_.get("pageid")
            out[t.replace(u"File:", u"", 1)] = ii
    return out


def _photo_safe(s):
    """a name the sheets' fonts can print (WinAnsi + the Turkish letters): other letters lose their accents (Kaunas
    authors etc.), anything still unprintable leaves the name out"""
    import unicodedata
    tr = u"ĞğİıŞş"
    out = u""
    for ch in s or u"":
        try:
            ch.encode("cp1252")
            out += ch
        except Exception:
            if ch in tr:
                out += ch
            else:
                b = unicodedata.normalize("NFKD", ch)[0]
                out += b if ord(b) < 128 else u""
    out = u" ".join(out.split())
    return out if sum(c.isalpha() for c in out) >= 2 else u""


def photo_credit(name, m):
    """the printed credit of a photo record m {author, licence, pageid, title} (F15: no Latin file names)"""
    link = u"commons.wikimedia.org/?curid={}".format(m["pageid"]) if m.get("pageid") else u"Wikimedia Commons"
    cr = u"photo {}: {}, {}, Wikimedia Commons, {}".format(name, m.get("author") or u"author named on the file page",
                                                            m.get("licence") or u"licence on the file page", link)
    if PHOTO_CREDIT_FILE and m.get("title"):
        cr += u" (File:{})".format(m["title"])
    return cr


def plant_photo(key, name, files, keep_old, photo_dir, log, state):
    """(jpeg path or None, credit or None, why not) for one plant or crop: key = file name in photo_dir, name = the
    printed name, files = its pinned Commons files in order, keep_old = an older cached photo may stay. Cache first
    (when it holds one of the pinned files, or Aras's own photo), then the web (see the header of this part)."""
    meta = os.path.join(photo_dir, key + ".json")
    old = None
    try:
        with open(meta, "r", encoding="utf-8") as f:
            m = json.load(f)
        p = os.path.join(photo_dir, m["file"])
        with open(p, "rb") as f:
            if jpeg_info(f.read(256 * 1024) + b"\x00" * 10):
                if not m.get("source") and not m.get("title"):
                    return p, m["credit"], None                       # Aras's own photo, as it is
                if m.get("title") in files and m.get("pageid"):
                    return p, photo_credit(name, m), None             # one of the pinned files, fetched before
                old = (p, m.get("credit"))                            # fetched by an older version
    except Exception:
        pass

    def fallback(why):
        if old and keep_old:
            log.append(u"photo {}: {}; the older cached photo stays".format(key, why))
            return old[0], old[1], None
        log.append(u"photo {}: {}; pinned file(s): {}".format(key, why, u"; ".join(
            u"commons.wikimedia.org/wiki/File:" + t.replace(u" ", u"_") for t in files)))
        return None, None, why
    if state.get("offline"):
        return fallback(u"offline")
    if "refused" not in state:
        h = _photo_hold()
        if h:
            state["refused"] = u"{}, press again in {:.0f} min".format(h[0], max(1.0, h[1] / 60.0))
    if state.get("refused"):
        return fallback(state["refused"])
    try:
        os.makedirs(photo_dir, exist_ok=True)
        if "infos" not in state:                                      # every photo still to fetch, in one call
            need = []
            for k_, row in PLANTS.items():
                try:
                    with open(os.path.join(photo_dir, k_ + ".json"), "r", encoding="utf-8") as f:
                        m_ = json.load(f)
                    if (m_.get("title") in row[1] and m_.get("pageid")) or not (m_.get("source") or m_.get("title")):
                        continue
                except Exception:
                    pass
                need += [t for t in row[1] if t not in need]
            state["infos"] = {}                                       # a failed call is not repeated this press
            state["infos"] = _photo_infos(need, state)
        ii, why = None, u"file not found on Commons"
        for t in files:
            c = state["infos"].get(t)
            if c is None:
                continue
            artist, lic = _photo_meta(c)
            if not photo_free(lic):
                why = u"licence not open ({})".format(lic or u"none")
                continue
            if c.get("mime") not in ("image/jpeg", "image/png"):
                why = u"not a photo file"
                continue
            ii = (t, c, artist, lic)
            break
        if ii is None:
            return fallback(why)
        t, c, artist, lic = ii
        data = _photo_http(c.get("thumburl") or c["url"], state)
        p = os.path.join(photo_dir, key + ".jpg")
        if jpeg_info(data):
            with open(p, "wb") as f:
                f.write(data)
        else:
            tmp = os.path.join(photo_dir, key + ".src")
            with open(tmp, "wb") as f:
                f.write(data)
            if not _png_to_jpeg(tmp, p):
                return fallback(u"not a JPEG")
        au = _photo_safe(artist) or _photo_safe(c.get("user", u""))
        if artist and au != " ".join(artist.split()):
            log.append(u"photo {}: author '{}' printed as '{}' (the sheets' fonts)".format(key, artist, au))
        m = {"file": os.path.basename(p), "title": t, "pageid": c.get("pageid"), "author": au, "licence": lic,
             "source": c.get("descriptionurl", u""), "size": [c.get("width"), c.get("height")]}
        m["credit"] = photo_credit(name, m)
        with open(meta, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False)
        log.append(u"photo {}: {} · page {} · {} · {} · {} x {} px".format(key, t, c.get("pageid"), au, lic,
                                                                          c.get("width"), c.get("height")))
        return p, m["credit"], None
    except Exception as ex:
        import socket
        import urllib.error
        if isinstance(ex, (urllib.error.URLError, socket.timeout, OSError)) and not isinstance(ex,
                                                                                              urllib.error.HTTPError):
            state["offline"] = True
        log.append(u"photo {}: {}: {}".format(key, type(ex).__name__, ex))
        if isinstance(ex, urllib.error.HTTPError):
            return fallback(state.get("refused") or u"Wikimedia error (HTTP {})".format(ex.code))
        return fallback(u"offline" if state.get("offline") else u"not loaded ({})".format(type(ex).__name__))


PHOTO_PLACED = [0, 0]                # this run: [placed as plain images, asked for] (fitz_add_photos; photo_flag_line)


def _photo_crop_pixmap(fitz, data, a):
    """the JPEG as a PyMuPDF Pixmap cut about its centre to the aspect a (w / h), never stretched"""
    src = fitz.Pixmap(data)
    if src.alpha:
        src = fitz.Pixmap(src, 0)
    iw, ih = src.width, src.height
    cw, ch = (int(round(ih * a)), ih) if iw / float(ih) > a else (iw, int(round(iw / a)))
    x0, y0 = (iw - cw) // 2, (ih - ch) // 2
    ir = fitz.IRect(x0, y0, x0 + cw, y0 + ch)
    dst = fitz.Pixmap(src.colorspace, ir, False)
    dst.copy(src, ir)
    dst.set_origin(0, 0)
    return dst


def fitz_add_photos(path, photos, page_h=297.0):
    """The photos put into a written PDF with PyMuPDF: photos = [(page index, x0, y0, x1, y1 mm, y up from the page
    foot, jpeg path)]; each JPEG fills its frame, cut to the frame's proportions about its centre (never stretched).
    Round 3 (A2, DATA-2): each photo goes in as a PLAIN image on the page (insert_image of the cut pixmap), no longer
    inside a Form XObject (show_pdf_page), which the booklet's crop copy dropped (p19 printed no photos). If the cut
    fails, the whole JPEG is inserted proportionally inside the frame (still a plain image). The file is saved in
    place. Returns how many were placed; PHOTO_PLACED / photo_flag_line() give the log line."""
    import fitz
    K = 72.0 / 25.4
    doc = fitz.open(path)
    n = 0
    for pi, x0, y0, x1, y1, p in photos:
        try:
            with open(p, "rb") as f:
                data = f.read()
            info = jpeg_info(data)
            if not info or x1 <= x0 or y1 <= y0:
                continue
            r = fitz.Rect(x0 * K, (page_h - y1) * K, x1 * K, (page_h - y0) * K)
            try:
                doc[pi].insert_image(r, pixmap=_photo_crop_pixmap(fitz, data, (x1 - x0) / (y1 - y0)),
                                     keep_proportion=False)
            except Exception:
                doc[pi].insert_image(r, stream=data, keep_proportion=True)
            n += 1
        except Exception:
            continue
    PHOTO_PLACED[0] += n
    PHOTO_PLACED[1] += len(photos)
    if n:
        t_ = path + ".tmp"
        doc.save(t_, garbage=3, deflate=True)
        doc.close()
        os.replace(t_, path)
    else:
        doc.close()
    return n


def photo_flag_line(reset=True):
    """the log line of this run's photos: "photos: n of m placed as images" (+ FLAG when some are missing)"""
    n, m = PHOTO_PLACED
    if reset:
        PHOTO_PLACED[0] = PHOTO_PLACED[1] = 0
    return u"photos: %d of %d placed as images%s" % (n, m, u" · FLAG %d missing" % (m - n) if n < m else u"")
# ---- the booklet's one icon set (02_SHARED_SYSTEMS §2, WO-T2b-1; M9 30 Oct: every icon has its legend name,
# ICO_LEGEND / ico_legend_entry): every symbol drawn on one 24-unit square grid,
# scaled to `size` page mm, with one stroke weight, one corner radius and one colour rule, so water, planting, plant,
# people and warning marks read as one family (quality bar: refs/R19, the crossed glass on page 18).
#   grid      24 x 24 units, origin at the icon centre, y up; drawing inside +-10 (2 units clear on every side)
#   stroke    ICO_LW_UNITS = 1.5 units = size / 16 page mm (0.375 at 6 mm, 1.25 at 20 mm); one weight per icon;
#             only the "not allowed" cross is heavier (1.5 x), on a paper casing
#   corners   boxes rounded at 1.5 units (one stroke); open lines end on whole or half grid units; gaps >= 2 units
#   colour    ink lines + at most two flat colours (c1, c2) from palette v1.4; c2 left None = c1 mixed 60 % to paper
#   text      none: numbers and labels are drawn by the caller (ico_step gives the anchor)
# Pure geometry: shapes in the house format of section_style.py, page mm, y up; the script's own put() draws them.
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)


# palette v1.4 (/mnt/project-files/palette/bergama_palette.py) and section_style.py SEC: hex without '#'
ICO_PAL = dict(
    ink="4A3F35",          # CORE ink
    paper="EFEDE6",        # CORE paper
    structure="B0AC9C",    # CORE structure
    water="91ADB4",        # CORE water
    water_deep="5D7F8D",   # CORE water_deep
    water_light="C1D3DB",  # CORE water_light
    green_mid="727A4E",    # CORE green_mid
    green_light="8C9969",  # CORE green_light
    olive="8E9A6C",        # section_style SEC olive
    reed="8E9466",         # section_style SEC reed
    agri="BDB57A",         # LAND_USE agri
    accent="8B3A3F",       # CORE accent (heritage, walking routes, warnings)
    market="BC6F45",       # LAND_USE commercial
    uv="8C7088",           # LAND_USE institutional (the violet of UV light)
    sun="F4C178",          # SCHEMES D5 education
    timber="AA8148",       # MASTERPLAN centre mid
    sewage="767167",       # MASTERPLAN service mid
)

ICO_GRID = 24.0
ICO_LW_UNITS = 1.5

# default (c1, c2) of every icon; None = c1 mixed toward paper
ICO_COL = {
    "water": ("water", None),
    "stream": ("water", "water_deep"),
    "stream_out": ("water", "agri"),
    "flow": ("water_deep", None),
    "depth": ("water", None),
    "high_water": ("water", "water_deep"),
    "rain": ("water_light", "water_deep"),
    "drought": ("agri", "sun"),
    "sun": ("sun", None),
    "shade": ("green_mid", "structure"),
    "reeds": ("water", "reed"),
    "plants": ("green_light", "green_mid"),
    "tree": ("green_mid", None),
    "olive": ("olive", None),
    "field": ("agri", None),
    "drip": ("water", None),
    "sewage": ("sewage", "structure"),
    "nutrients": ("water", "sewage"),
    "treatment": ("water", "structure"),
    "storage": ("water", "water_light"),
    "uv": ("water", "uv"),
    "glass": ("water", None),
    "not_drinkable": ("water", None),
    "chart": ("water_deep", "water"),
    "people": ("accent", None),
    "walk": ("accent", None),
    "bike": ("accent", None),
    "hub": ("accent", None),
    "market": ("market", None),
    "heritage": ("accent", None),
    "cafe": ("market", None),
    "seating": ("timber", None),
    "viewpoint": ("accent", None),
    "warning": ("accent", None),
    "key_area": ("accent", None),
    "key_line": ("accent", None),
    "key_dash": ("accent", None),
    "key_point": ("accent", None),
    # M9 (30 Oct): the plant-group functions of p.17 (G9) and the p.15 flood zone mark
    "flood_zone": ("water", "water_deep"),
    "wind": ("structure", None),
    "noise": ("structure", None),
    "corridor": ("green_mid", "green_light"),
}

ICO_NAMES = tuple(ICO_COL.keys())

# M9 (30 Oct): every icon's legend name (G1: no icon without its meaning). A page's legend row for an icon is
# ico_legend_entry(name) (or the Legend of label_place.py: lg.add(ico_legend_name(n), kind="icon", icon=n)).
ICO_LEGEND = {
    "water": u"Water", "stream": u"Selinos stream", "stream_out": u"Clean stream water to the fields",
    "flow": u"Flow direction", "depth": u"Water depth", "high_water": u"High water (flood level)",
    "rain": u"Rain", "drought": u"Dry season", "sun": u"Sun", "shade": u"Gives shade",
    "reeds": u"Reed basin (cleans water)", "plants": u"Planting", "tree": u"Tree", "olive": u"Olive grove",
    "field": u"Farmland", "drip": u"Drip irrigation", "sewage": u"Sewage outfall", "nutrients": u"Nutrients in the water",
    "treatment": u"Treatment works", "storage": u"Storage", "uv": u"UV disinfection", "glass": u"Drinking water",
    "not_drinkable": u"Not drinking water", "chart": u"Figures", "people": u"People", "walk": u"Walking",
    "bike": u"Cycling", "hub": u"Hub (meeting point)", "market": u"Market", "heritage": u"Heritage site",
    "cafe": u"Café", "seating": u"Seating", "viewpoint": u"Viewpoint", "warning": u"Warning",
    "key_area": u"Area", "key_line": u"Route", "key_dash": u"Path", "key_point": u"Place",
    "flood_zone": u"Flood zone", "wind": u"Cuts wind", "noise": u"Cuts street noise",
    "corridor": u"Ecological corridor",
}


def ico_legend_name(name):
    """M9: the legend name of icon `name` (every icon has one)"""
    if name not in ICO_LEGEND:
        raise ValueError("icons: %r has no legend name (ICO_LEGEND)" % (name,))
    return ICO_LEGEND[name]


def ico_legend_entry(name, label=None, **colours):
    """M9: the legend row of an icon: dict(label, kind="icon", icon=name, ...) for a page legend (label overrides the
    standard name only where the page means something narrower, e.g. "Kermes market")"""
    _ico_grid(name)                                                  # unknown names stop here
    return dict(colours, label=label or ico_legend_name(name), kind="icon", icon=name)


def ico_lw(size):
    """The one stroke weight (page mm) of an icon `size` mm square: 1.5 grid units = size / 16."""
    return size * ICO_LW_UNITS / ICO_GRID


def _ico_mix(a, b, t):
    """hex a -> hex b by t."""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def _ico_arc(x, y, rx, ry, a0, a1, n=16):
    """Points on an ellipse arc from a0 to a1 degrees (both included), grid units."""
    import math as _m
    return [(x + rx * _m.cos(_m.radians(a0 + (a1 - a0) * i / float(n))),
             y + ry * _m.sin(_m.radians(a0 + (a1 - a0) * i / float(n)))) for i in range(n + 1)]


def _ico_circ(x, y, r, n=32):
    return _ico_arc(x, y, r, r, 0.0, 360.0, n)[:-1]


def _ico_ell(x, y, rx, ry, n=32):
    return _ico_arc(x, y, rx, ry, 0.0, 360.0, n)[:-1]


def _ico_rrect(x0, y0, x1, y1, r=1.5):
    """A box with the set's rounded corners (r grid units, clipped to half the short side)."""
    r = max(0.0, min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0))
    if r <= 0.0:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return (_ico_arc(x1 - r, y0 + r, r, r, 270.0, 360.0, 4) + _ico_arc(x1 - r, y1 - r, r, r, 0.0, 90.0, 4)
            + _ico_arc(x0 + r, y1 - r, r, r, 90.0, 180.0, 4) + _ico_arc(x0 + r, y0 + r, r, r, 180.0, 270.0, 4))


def _ico_drop(x, yc, r, apex):
    """A water drop: round body r at (x, yc), point at (x, apex)."""
    import math as _m
    a = _m.degrees(_m.acos(r / float(apex - yc)))
    return [(x, apex)] + _ico_arc(x, yc, r, r, 90.0 + a, 450.0 - a, 24)


def _ico_leaf(b, t, w):
    """A pointed leaf from base b to tip t, w wide at its middle."""
    import math as _m
    dx, dy = t[0] - b[0], t[1] - b[1]
    L = _m.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    pts = []
    for s_ in (1, -1):
        rng = range(11) if s_ > 0 else range(10, -1, -1)
        for i in rng:
            s = i / 10.0
            o = s_ * w / 2.0 * _m.sin(_m.pi * s)
            pts.append((b[0] + dx * s + nx * o, b[1] + dy * s + ny * o))
    return pts[:-1]


def _ico_wave(x0, x1, y, amp, periods, n=24):
    import math as _m
    return [(x0 + (x1 - x0) * i / float(n), y + amp * _m.sin(2 * _m.pi * periods * i / float(n))) for i in range(n + 1)]


def _ico_union(ox, oy, circles, rect, n=72):
    """Outline of circles [(x, y, r)] united with a box (x0, y0, x1, y1) around (ox, oy), sampled by rays."""
    import math as _m
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n
        dx, dy = _m.cos(a), _m.sin(a)
        ts = []
        if abs(dx) > 1e-9:
            ts.append(((rect[2] if dx > 0 else rect[0]) - ox) / dx)
        if abs(dy) > 1e-9:
            ts.append(((rect[3] if dy > 0 else rect[1]) - oy) / dy)
        t = min(ts)
        for cx, cy, r in circles:
            px, py = ox - cx, oy - cy
            b = dx * px + dy * py
            disc = b * b - (px * px + py * py - r * r)
            if disc >= 0.0:
                t = max(t, -b + _m.sqrt(disc))
        out.append((ox + t * dx, oy + t * dy))
    return out


def _ico_arrowhead(x, y, ang, L=3.0, w=3.0):
    """A filled arrow tip at (x, y) pointing at ang degrees."""
    import math as _m
    a = _m.radians(ang)
    ux, uy = _m.cos(a), _m.sin(a)
    bx, by = x - ux * L, y - uy * L
    return [(x, y), (bx - uy * w / 2.0, by + ux * w / 2.0), (bx + uy * w / 2.0, by - ux * w / 2.0)]


def _ico_grid(name):
    """The icon in grid units with colour tokens: ("poly", ring, fill, stroke) / ("line", pts, colour)."""
    import math as _m
    P, L = "poly", "line"
    G = -8.0                                                         # the ground line of standing objects
    if name == "water":
        return [(P, _ico_drop(0.0, -3.0, 6.5, 10.0), "c1", "ink")]
    if name == "stream":
        top, bot = _ico_wave(-10.0, 10.0, 3.0, 1.2, 1.5), _ico_wave(-10.0, 10.0, -5.0, 1.2, 1.5)
        return [(P, top + bot[::-1], "c1", None), (L, top, "ink"), (L, bot, "ink"),
                (L, _ico_wave(-6.0, 6.0, -1.0, 1.0, 1.0, 16), "c2")]
    if name == "stream_out":                                         # page 18: the clean stream leaves past the fields
        return [(P, [(-10.0, 3.5), (2.0, 3.5), (2.0, 0.5), (10.0, 5.5), (2.0, 10.5), (2.0, 7.5), (-10.0, 7.5)],
                 "c1", "ink"),
                (P, [(-10.0, -9.0), (4.0, -9.0), (10.0, -2.0), (-4.0, -2.0)], "c2", "ink"),
                (L, [(-5.3, -9.0), (0.7, -2.0)], "ink"), (L, [(-0.7, -9.0), (5.3, -2.0)], "ink")]
    if name == "flow":
        return [(P, [(-10.0, -1.75), (2.0, -1.75), (2.0, -6.0), (10.0, 0.0), (2.0, 6.0), (2.0, 1.75), (-10.0, 1.75)],
                 "c1", "ink")]
    if name == "depth":                                              # a basin section with its water depth
        return [(P, [(-8.0, 1.0), (8.0, 1.0), (5.0, -8.0), (-5.0, -8.0)], "c1", None),
                (L, [(-11.0, 5.0), (-9.4, 5.0), (-5.0, -8.0), (5.0, -8.0), (9.4, 5.0), (11.0, 5.0)], "ink"),
                (L, [(0.0, -5.0), (0.0, -2.0)], "ink"), (P, _ico_arrowhead(0.0, -8.0, -90.0), "ink", None),
                (P, _ico_arrowhead(0.0, 1.0, 90.0), "ink", None)]
    if name == "high_water":
        surf = _ico_wave(-10.0, 10.0, -1.0, 0.9, 2.0)
        return [(P, surf + [(10.0, -9.0), (-10.0, -9.0)], "c1", None), (L, surf, "ink"),
                (P, [(-3.5, 6.0), (3.5, 6.0), (0.0, 0.0)], "c2", "ink"),
                (L, [(-2.5, -3.5), (2.5, -3.5)], "ink"), (L, [(-1.25, -6.0), (1.25, -6.0)], "ink"),
                (L, [(8.0, 0.5), (8.0, 6.5)], "ink"), (P, _ico_arrowhead(8.0, 10.0, 90.0, 3.5, 4.0), "ink", None)]
    if name == "rain":
        cloud = _ico_union(0.0, 0.0, [(-6.5, -0.5, 2.5), (6.5, -0.5, 2.5), (-3.0, 2.0, 3.5), (2.5, 3.0, 4.5)],
                           (-6.5, -3.0, 6.5, 2.0))
        return [(P, cloud, "c1", "ink")] + [(L, [(x, -5.5), (x - 1.5, -9.5)], "c2") for x in (-4.0, 0.5, 5.0)]
    if name == "drought":
        sh = [(P, _ico_rrect(-10.0, -9.0, 10.0, -3.0), "c1", "ink"),
              (L, [(-5.0, -3.0), (-3.8, -5.2), (-5.8, -7.0), (-4.8, -9.0)], "ink"),
              (L, [(3.5, -3.0), (2.4, -5.6), (4.4, -7.2), (3.6, -9.0)], "ink"),
              (P, _ico_circ(0.0, 4.5, 3.0), "c2", "ink")]
        return sh + [(L, _ico_arc(0.0, 4.5, 4.75, 4.75, a, a, 1)[:1] + _ico_arc(0.0, 4.5, 6.75, 6.75, a, a, 1)[:1],
                      "ink") for a in (0.0, 45.0, 90.0, 135.0, 180.0)]
    if name == "sun":
        sh = [(P, _ico_circ(0.0, 0.0, 4.5), "c1", "ink")]
        return sh + [(L, _ico_arc(0.0, 0.0, 6.5, 6.5, a, a, 1)[:1] + _ico_arc(0.0, 0.0, 9.5, 9.5, a, a, 1)[:1], "ink")
                     for a in range(0, 360, 45)]
    if name == "shade":                                              # a crown and the shadow it casts
        return [(P, _ico_ell(0.0, G - 0.5, 9.0, 1.75), "c2", None), (L, [(0.0, G), (0.0, -1.0)], "ink"),
                (P, _ico_ell(0.0, 3.5, 9.0, 5.0), "c1", "ink")]
    if name == "reeds":                                              # D2 a: common reed only in a lined, root-contained basin
        sh = [(P, [(-7.55, -3.0), (7.55, -3.0), (5.0, -9.0), (-5.0, -9.0)], "c1", None)]
        for x, h, s, ly in ((-4.0, 6.5, -1.0, -1.0), (0.0, 8.5, 1.0, 1.0), (4.0, 5.5, 1.0, -2.0)):
            sh += [(L, [(x, -6.0), (x, h - 2.0)], "c2"),
                   (P, _ico_leaf((x, ly), (x + 3.0 * s, ly + 3.5), 1.6), "c2", None),
                   (P, _ico_ell(x, h, 1.1, 2.4, 16), "c2", "ink")]
        return sh + [(L, [(-11.0, 0.5), (-8.8, 0.5), (-5.0, -9.0), (5.0, -9.0), (8.8, 0.5), (11.0, 0.5)], "ink")]
    if name == "plants":
        return [(P, _ico_leaf((-0.75, G), (-8.0, 2.0), 4.0), "c1", "ink"),
                (P, _ico_leaf((0.75, G), (8.0, 2.0), 4.0), "c1", "ink"),
                (P, _ico_leaf((0.0, G), (0.0, 8.0), 5.0), "c2", "ink"), (L, [(-10.0, G), (10.0, G)], "ink")]
    if name == "tree":
        return [(L, [(0.0, G - 1.0), (0.0, -3.0)], "ink"), (L, [(-5.0, G - 1.0), (5.0, G - 1.0)], "ink"),
                (P, _ico_circ(0.0, 3.0, 7.0), "c1", "ink")]
    if name == "olive":                                              # a forked trunk under a wide crown, three fruits
        return [(L, [(0.0, G - 1.0), (0.0, -5.0), (-3.0, -1.5)], "ink"), (L, [(0.0, -5.0), (3.0, -1.5)], "ink"),
                (L, [(-5.0, G - 1.0), (5.0, G - 1.0)], "ink"), (P, _ico_ell(0.0, 3.5, 9.5, 5.5), "c1", "ink"),
                (P, _ico_circ(-4.0, 3.0, 1.25, 12), "ink", None), (P, _ico_circ(1.0, 5.5, 1.25, 12), "ink", None),
                (P, _ico_circ(3.5, 1.5, 1.25, 12), "ink", None)]
    if name == "field":
        return [(P, [(-10.0, -6.0), (4.0, -6.0), (10.0, 6.0), (-4.0, 6.0)], "c1", "ink"),
                (L, [(-5.3, -6.0), (0.7, 6.0)], "ink"), (L, [(-0.7, -6.0), (5.3, 6.0)], "ink")]
    if name == "drip":
        sh = [(L, [(-10.0, 4.0), (10.0, 4.0)], "ink"), (L, [(-10.0, G), (10.0, G)], "ink")]
        for x in (-6.0, 0.0, 6.0):
            sh += [(P, _ico_rrect(x - 1.25, 2.75, x + 1.25, 5.25, 0.6), "ink", None),
                   (P, _ico_drop(x, -3.0, 1.75, 0.5), "c1", "ink")]
        return sh
    if name == "sewage":                                             # a pipe mouth and what falls from it
        return [(P, _ico_rrect(-10.0, 1.0, 4.0, 7.0, 0.0), "c2", "ink"),
                (P, _ico_rrect(3.5, -0.5, 6.0, 8.5), "c2", "ink"),
                (P, _ico_drop(8.0, -3.0, 2.0, 1.0), "c1", "ink"),
                (P, _ico_ell(5.0, -8.5, 5.0, 1.5), "c1", "ink")]
    if name == "nutrients":                                          # a drop with what it carries (NH4-N, P)
        return [(P, _ico_drop(0.0, -3.0, 6.5, 10.0), "c1", "ink"),
                (P, _ico_circ(-2.5, -4.5, 1.25, 12), "c2", None), (P, _ico_circ(2.0, -2.0, 1.25, 12), "c2", None),
                (P, _ico_circ(0.5, -6.5, 1.25, 12), "c2", None), (P, _ico_circ(-0.5, 1.5, 1.0, 12), "c2", None)]
    if name == "treatment":                                          # a sawtooth works hall and a round settling tank
        return [(L, [(-11.0, G), (11.0, G)], "ink"),
                (P, [(-10.0, G), (-2.0, G), (-2.0, 4.0), (-6.0, 1.5), (-6.0, 4.0), (-10.0, 1.5)], "c2", "ink"),
                (P, _ico_circ(5.5, -3.25, 4.75), "c1", "ink"), (P, _ico_circ(5.5, -3.25, 2.0, 16), None, "ink")]
    if name == "storage":                                            # a cylinder tank, filled to its level
        rx, ry, top, lev, bot = 7.0, 2.0, 5.0, -1.0, -7.0
        front = _ico_arc(0.0, bot, rx, ry, 180.0, 360.0)
        return [(P, [(-rx, top)] + front + [(rx, top)], "paper", None),
                (P, [(-rx, lev)] + front + [(rx, lev)] + _ico_arc(0.0, lev, rx, ry, 0.0, -180.0), "c1", None),
                (P, _ico_ell(0.0, lev, rx, ry), "c2", None),
                (L, [(-rx, top)] + front + [(rx, top)], "ink"),
                (P, _ico_ell(0.0, top, rx, ry), "paper", "ink")]
    if name == "uv":                                                 # a UV lamp over the water it disinfects
        sh = [(P, _ico_rrect(-10.0, -9.0, 10.0, -4.0, 0.0), "c1", None), (L, [(-10.0, -4.0), (10.0, -4.0)], "ink"),
              (P, _ico_rrect(-7.0, 2.0, 7.0, 5.5, 1.75), "c2", "ink")]
        sh += [(L, [(x, 0.0), (x * 1.25, -2.5)], "c2") for x in (-6.0, -3.0, 0.0, 3.0, 6.0)]
        return sh + [(L, [(x, 7.5), (x * 1.25, 10.0)], "c2") for x in (-4.5, 0.0, 4.5)]
    if name in ("glass", "not_drinkable"):
        return [(P, [(-5.5, 3.0), (5.5, 3.0), (4.5, -9.0), (-4.5, -9.0)], "c1", None),
                (L, [(-6.0, 9.0), (-4.5, -9.0), (4.5, -9.0), (6.0, 9.0)], "ink")]
    if name == "chart":
        return [(P, _ico_rrect(-7.0, -9.0, -3.0, 5.0, 0.0), "c1", None),
                (P, _ico_rrect(-1.0, -9.0, 3.0, -1.0, 0.0), "c2", None),
                (P, _ico_rrect(5.0, -9.0, 9.0, -5.0, 0.0), "c2", None),
                (L, [(-10.0, 9.0), (-10.0, -9.0), (10.0, -9.0)], "ink")]
    if name == "people":
        return [(P, _ico_circ(-4.0, 5.5, 2.5, 20), "ink", None), (P, _ico_rrect(-8.0, -9.0, 0.0, 2.0, 3.0), "c1", "ink"),
                (P, _ico_circ(5.0, 2.5, 2.0, 20), "ink", None), (P, _ico_rrect(2.0, -9.0, 8.0, -0.5, 2.5), "c2", "ink")]
    if name == "walk":
        return [(P, _ico_circ(1.0, 7.5, 2.25, 20), "c1", None),
                (L, [(0.5, 4.0), (-1.0, -2.0)], "c1"), (L, [(-1.0, -2.0), (-4.0, -5.0), (-5.0, -9.0)], "c1"),
                (L, [(-1.0, -2.0), (2.0, -5.5), (3.5, -9.0)], "c1"), (L, [(-4.5, -0.5), (-2.5, 2.5), (0.3, 3.2)], "c1"),
                (L, [(0.3, 3.2), (2.5, 0.5), (5.0, -0.5)], "c1")]
    if name == "bike":
        return [(P, _ico_circ(-6.0, -4.0, 4.0), None, "ink"), (P, _ico_circ(6.0, -4.0, 4.0), None, "ink"),
                (L, [(-6.0, -4.0), (-1.0, -4.0), (-3.0, 2.0), (-6.0, -4.0)], "c1"),
                (L, [(-3.0, 2.0), (4.0, 2.0), (-1.0, -4.0)], "c1"), (L, [(6.0, -4.0), (3.0, 5.0), (5.5, 5.0)], "c1"),
                (L, [(-5.0, 3.5), (-1.5, 3.5)], "c1")]
    if name == "hub":                                                # a meeting node: a disc in a ring, routes leaving it
        sh = [(P, _ico_circ(0.0, 0.0, 7.0), "c2", "ink"), (P, _ico_circ(0.0, 0.0, 3.5, 24), "c1", "ink")]
        return sh + [(L, _ico_arc(0.0, 0.0, 7.0, 7.0, a, a, 1)[:1] + _ico_arc(0.0, 0.0, 10.5, 10.5, a, a, 1)[:1], "ink")
                     for a in (45.0, 135.0, 225.0, 315.0)]
    if name == "market":                                             # a Kermes stall: striped awning, posts, counter
        sh = [(P, [(-10.0, 7.0), (0.0, 10.0), (10.0, 7.0)], "c1", "ink"),
              (L, [(-8.75, 3.0), (-8.75, G)], "ink"), (L, [(8.75, 3.0), (8.75, G)], "ink")]
        for i in range(4):
            x0 = -10.0 + 5.0 * i
            sh.append((P, [(x0, 7.0)] + _ico_arc(x0 + 2.5, 4.0, 2.5, 2.0, 180.0, 360.0, 8) + [(x0 + 5.0, 7.0)],
                       "c1" if i % 2 == 0 else "c2", "ink"))
        return sh + [(P, _ico_rrect(-10.0, G - 1.0, 10.0, -3.5), "c2", "ink")]
    if name == "heritage":                                           # a temple front
        sh = [(P, [(-10.0, 3.0), (10.0, 3.0), (0.0, 9.5)], "c1", "ink"), (P, _ico_rrect(-10.0, -9.0, 10.0, -6.0, 0.0), "c1", "ink")]
        return sh + [(P, _ico_rrect(x - 1.0, -6.0, x + 1.0, 3.0, 0.0), "c2", "ink") for x in (-6.5, -2.2, 2.2, 6.5)]
    if name == "cafe":
        steam = [(L, [(x + 0.8 * _m.sin(i * 1.05), 4.0 + i * 0.75) for i in range(8)], "ink") for x in (-3.0, 1.5)]
        return steam + [(L, _ico_arc(5.3, -2.0, 3.0, 3.0, -90.0, 90.0, 10), "ink"),
                        (P, [(-7.0, 2.0), (6.0, 2.0), (4.5, -6.5), (-5.5, -6.5)], "c1", "ink"),
                        (L, [(-9.0, -8.5), (8.0, -8.5)], "ink")]
    if name == "seating":                                            # a bench with a back
        return [(L, [(-10.0, G), (10.0, G)], "ink"), (L, [(-7.5, -1.5), (-7.5, G)], "ink"),
                (L, [(7.5, -1.5), (7.5, G)], "ink"), (L, [(-7.5, 0.5), (-7.5, 3.5)], "ink"),
                (L, [(7.5, 0.5), (7.5, 3.5)], "ink"),
                (P, _ico_rrect(-10.0, -2.0, 10.0, 0.5, 0.75), "c1", "ink"),
                (P, _ico_rrect(-10.0, 3.0, 10.0, 6.0, 0.75), "c1", "ink")]
    if name == "viewpoint":                                          # an eye
        return [(P, _ico_arc(0.0, -6.0, 11.66, 11.66, 30.96, 149.04, 16)
                 + _ico_arc(0.0, 6.0, 11.66, 11.66, 210.96, 329.04, 16), "paper", "ink"),
                (P, _ico_circ(0.0, 0.0, 3.75, 24), "c1", "ink"), (P, _ico_circ(0.0, 0.0, 1.25, 12), "ink", None)]
    if name == "warning":
        return [(P, [(-10.0, -8.0), (10.0, -8.0), (0.0, 9.32)], "c1", "c1"),
                (P, _ico_rrect(-1.0, -2.5, 1.0, 4.5, 1.0), "paper", None), (P, _ico_circ(0.0, -5.25, 1.25, 12), "paper", None)]
    if name == "key_area":
        return [(P, _ico_rrect(-9.0, -6.0, 9.0, 6.0), "c1", "ink")]
    if name == "key_line":
        return [(L, [(-10.0, 0.0), (10.0, 0.0)], "c1")]
    if name == "key_dash":
        return [(L, [(x, 0.0), (x + 4.0, 0.0)], "c1") for x in (-10.0, -2.0, 6.0)]
    if name == "key_point":
        return [(P, _ico_circ(0.0, 0.0, 4.5, 24), "c1", "ink")]
    if name == "flood_zone":                                         # a ground band under a raised wave line
        surf = _ico_wave(-10.0, 10.0, 2.0, 1.2, 2.0)
        return [(P, surf + [(10.0, -8.0), (-10.0, -8.0)], "c1", None), (L, surf, "ink"),
                (L, [(-10.0, -8.0), (10.0, -8.0)], "ink"),
                (L, _ico_wave(-7.0, 7.0, -3.0, 0.9, 1.5, 16), "c2"),
                (L, [(0.0, 5.5), (0.0, 9.5)], "ink"), (P, _ico_arrowhead(0.0, 10.5, 90.0, 3.0, 3.5), "ink", None)]
    if name == "wind":                                               # three gusts stopped by a crown
        sh = [(L, _ico_wave(-10.0, -1.0, y, 0.6, 1.0, 12), "ink") for y in (4.0, 0.0, -4.0)]
        return sh + [(P, _ico_ell(5.5, 1.0, 4.5, 7.0), "c1", "ink"), (L, [(5.5, -6.0), (5.5, -9.0)], "ink")]
    if name == "noise":                                              # sound arcs stopped by a crown
        sh = [(L, _ico_arc(-10.0, 0.0, r, r, -45.0, 45.0, 8), "ink") for r in (3.0, 6.0, 9.0)]
        return sh + [(P, _ico_ell(5.5, 1.0, 4.5, 7.0), "c1", "ink"), (L, [(5.5, -6.0), (5.5, -9.0)], "ink")]
    if name == "corridor":                                           # a green band linking two patches
        return [(P, _ico_circ(-6.5, 0.0, 3.5, 24), "c1", "ink"), (P, _ico_circ(6.5, 0.0, 3.5, 24), "c1", "ink"),
                (P, _ico_rrect(-6.5, -1.75, 6.5, 1.75, 0.0), "c2", None),
                (L, [(-3.4, 1.75), (3.4, 1.75)], "ink"), (L, [(-3.4, -1.75), (3.4, -1.75)], "ink")]
    raise ValueError("icons: unknown icon %r (see ICO_NAMES)" % (name,))


# round 4 (S2, G-R4-6): plant icons take the species' own general colour from the plant module (plants.py pla_colours,
# S3) when it is there; the ICO_PAL greens stay only as the fallback until then
ICO_PLANT_KEY = dict(olive="olive", reeds="reed")     # species icons only; generic tree / planting icons keep ICO_PAL


def _ico_plant_colour(name):
    """the general (no-season) leaf colour of an icon's species from pla_colours(key, None), or None"""
    f, key = globals().get("pla_colours"), ICO_PLANT_KEY.get(name)
    if not callable(f) or not key:
        return None
    try:
        c = f(key, None)
    except Exception:
        return None
    if isinstance(c, dict):
        c = c.get("leaf") or c.get("fill") or c.get("main")
    elif isinstance(c, (list, tuple)):
        c = c[0] if c else None
    return c if isinstance(c, str) and len(c.lstrip("#")) == 6 else None


def _ico_colours(name, ink, accent, second):
    """Token -> hex for one icon: ink, c1 (accent overrides), c2 (second overrides; None = c1 mixed to paper)."""
    d1, d2 = ICO_COL[name]
    c1 = accent or _ico_plant_colour(name) or ICO_PAL[d1]
    c2 = second or (ICO_PAL[d2] if d2 else _ico_mix(c1, ICO_PAL["paper"], 0.6))
    return dict(ink=ink or ICO_PAL["ink"], c1=c1, c2=c2, paper=ICO_PAL["paper"])


def ico_cross(cx, cy, size, colour=None, casing=True):
    """The "not allowed / not drinkable" cross over an icon: corner to corner of the live area, 1.5 x the stroke,
    on a paper casing one stroke wider."""
    u, lw = size / ICO_GRID, ico_lw(size)
    a, b = [(cx - 9.5 * u, cy - 9.5 * u), (cx + 9.5 * u, cy + 9.5 * u)], [(cx - 9.5 * u, cy + 9.5 * u), (cx + 9.5 * u, cy - 9.5 * u)]
    sh = [("line", a, ICO_PAL["paper"], 2.5 * lw), ("line", b, ICO_PAL["paper"], 2.5 * lw)] if casing else []
    return sh + [("line", a, colour or ICO_PAL["accent"], 1.5 * lw), ("line", b, colour or ICO_PAL["accent"], 1.5 * lw)]


def ico_draw(name, cx, cy, size, ink=None, accent=None, second=None):
    """Icon `name` (ICO_NAMES) centred at (cx, cy), size mm square: shapes. accent recolours c1, second c2."""
    u, lw = size / ICO_GRID, ico_lw(size)
    grid = _ico_grid(name)                                           # unknown names stop here
    col = _ico_colours(name, ink, accent, second)
    out = []
    for s in grid:
        if s[0] == "poly":
            ring = [(cx + x * u, cy + y * u) for x, y in s[1]]
            out.append(("poly", ring, col.get(s[2]) if s[2] else None, col.get(s[3]) if s[3] else None, lw))
        else:
            out.append(("line", [(cx + x * u, cy + y * u) for x, y in s[1]], col.get(s[2], s[2]), lw))
    if name == "not_drinkable":
        out += ico_cross(cx, cy, size)
    return out


def ico_badge(name, cx, cy, size, frame="circle", fill=None, edge=None, ink=None, accent=None, second=None):
    """Icon `name` on a round ("circle") or rounded-square ("square") plate size mm across, for legends: the icon at
    0.72 of the plate; plate in paper unless fill, with an edge line (one stroke of the plate size) only if edge."""
    lw = ico_lw(size)
    if frame == "square":
        h = size / 2.0 - lw / 2.0
        r = size * 3.0 / ICO_GRID
        ring = [(cx + x, cy + y) for x, y in _ico_rrect(-h, -h, h, h, r)]
    else:
        ring = [(cx + x, cy + y) for x, y in _ico_circ(0.0, 0.0, size / 2.0 - lw / 2.0, 40)]
    plate = ("poly", ring, fill or ICO_PAL["paper"], edge, lw if edge else 0.0)
    return [plate] + ico_draw(name, cx, cy, size * 0.72, ink, accent, second)


def ico_step(cx, cy, size, style="solid", colour=None, ink=None):
    """A numbered flow-step marker (page 18, steps 1-7) size mm across: (shapes, (ax, ay), text_hex, cap_mm).
    The caller writes the number centred on (ax, ay) in text_hex at cap height cap_mm (0.42 x size)."""
    lw = ico_lw(size)
    c = colour or ICO_PAL["water_deep"]
    ring = [(cx + x, cy + y) for x, y in _ico_circ(0.0, 0.0, size / 2.0 - lw / 2.0, 40)]
    if style == "ring":
        return [("poly", ring, ICO_PAL["paper"], c, lw)], (cx, cy), (ink or ICO_PAL["ink"]), 0.42 * size
    return [("poly", ring, c, None, lw)], (cx, cy), ICO_PAL["paper"], 0.42 * size
# ---- M1 (revision 30 Oct 2026, H-A): ONE booklet grid and ONE set of type styles for every page ----------------------
# Page mm, A3 landscape 420 x 297, origin top-left, y DOWN (the booklet's own system). A script that draws y-up calls
# grid_flip(y) / grid_rect_up(r) for its coordinates. Every block of a page (map, section, legend, intro, key map, box)
# is placed by grid cells: a column span (c0, n) and baseline rows, never by hand-tuned mm.
#   columns   12 x 29 mm, gutters 4 mm, margins 14 mm left/right: 14 + 12 x 29 + 11 x 4 + 14 = 420
#   rows      baseline 4 mm from y = 12 (the top margin); title band 12..25, drawing area 30..273, footer from 276
#   crops     a crop the booklet shows at 1:1 is drawn GRID_W(n) wide (n whole columns), so its own sub-blocks fall on
#             the page grid when the booklet places it on a column line (grid_sub gives that sub-grid inside a crop)
# Type: GRID_TYPE (pt, bold, lead mm, colour role). Intro helper: "*word*" (or "**word**") marks the bold key words.
GRID_PAGE = (420.0, 297.0)
GRID_ML, GRID_MR, GRID_MT, GRID_MB = 14.0, 14.0, 12.0, 12.0
GRID_COLS, GRID_COL, GRID_GUT = 12, 29.0, 4.0
GRID_BASE = 4.0                                   # baseline step, from y = GRID_MT
GRID_TITLE_Y, GRID_RULE_Y = 22.0, 25.0            # title baseline, the rule under the title band
GRID_AREA = (GRID_ML, 30.0, GRID_PAGE[0] - GRID_MR, 273.0)   # where drawings go (x0, y0, x1, y1)
GRID_FOOT_RULE = 276.0
GRID_MIN_PT = 6.0                                 # no text below this size on any page (PLAN p18-19 rule)

# colour roles (palette v1.4 core): ink, second ink, accent, rule
GRID_INK = dict(ink="4A3F35", ink2="6B645B", accent="8B3A3F", rule="B0AC9C", paper="FFFFFF")
# style -> (size pt, bold, lead mm, colour role)
GRID_TYPE = dict(
    page_title=(24.0, True, 10.0, "ink"),         # the page's title (booklet header)
    kicker=(8.0, True, 3.6, "accent"),            # the theme line above the title
    intro=(9.5, False, 4.0, "ink"),               # 2-3 lines, key words bold (G4)
    heading=(10.0, True, 4.0, "ink"),             # a drawing's own heading ("Pedestrian flow")
    subheading=(8.0, True, 3.6, "ink2"),
    label=(7.0, False, 3.0, "ink"),               # labels on drawings
    label_small=(6.0, False, 2.6, "ink"),         # the smallest a label may get (crowded maps)
    legend=(7.0, False, 4.0, "ink"),              # legend entries (row pitch = lead)
    legend_title=(7.0, True, 4.0, "ink"),
    caption=(7.5, False, 3.2, "ink2"),            # under a drawing: what, scale
    value=(18.0, True, 7.0, "accent"),            # a box's one headline value (G4)
    note=(7.5, False, 3.2, "ink2"),               # the one line under a value
    pageno=(14.0, True, 6.0, "accent"),
)
GRID_PT = 25.4 / 72.0                             # mm per pt


def grid_style(name):
    """(size_pt, bold, lead_mm, hex) of a type style (GRID_TYPE)"""
    s, b, ld, role = GRID_TYPE[name]
    return s, b, ld, GRID_INK[role]


def grid_w(n):
    """width (mm) of n whole columns with their inner gutters"""
    n = max(1, int(n))
    return n * GRID_COL + (n - 1) * GRID_GUT


def grid_x(c):
    """left edge (mm) of column c (1-based; c = GRID_COLS + 1 gives the right margin line)"""
    return GRID_ML + (c - 1) * (GRID_COL + GRID_GUT)


def grid_x1(c):
    """right edge (mm) of column c"""
    return grid_x(c) + GRID_COL


def grid_span(c0, n):
    """(x, w) of the span of n columns from column c0"""
    if c0 < 1 or c0 + n - 1 > GRID_COLS:
        raise ValueError("grid span %d+%d is off the %d-column grid" % (c0, n, GRID_COLS))
    return grid_x(c0), grid_w(n)


def grid_cols_for(w, lo=1):
    """the fewest whole columns (>= lo) at least w mm wide (GRID_COLS when w is wider than the page)"""
    for n in range(max(1, lo), GRID_COLS + 1):
        if grid_w(n) >= w - 1e-6:
            return n
    return GRID_COLS


def grid_snap_y(y, up=True):
    """y (mm from the top) on the baseline grid: the next line at or below the point (up=True gives the line at or
    above it)"""
    import math as _m
    k = (y - GRID_MT) / GRID_BASE
    k = _m.floor(k + 1e-6) if up else _m.ceil(k - 1e-6)
    return GRID_MT + k * GRID_BASE


def grid_snap_h(h):
    """a height rounded UP to whole baseline steps"""
    import math as _m
    return GRID_BASE * _m.ceil(h / GRID_BASE - 1e-6)


def grid_rows(n):
    """the height of n baseline rows"""
    return n * GRID_BASE


def grid_cell(c0, n, y, h, snap=True):
    """the block rect (x0, y0, x1, y1) of n columns from c0, top y, height h; snap: top on the baseline (next line
    down) and the height to whole steps"""
    x, w = grid_span(c0, n)
    if snap:
        y, h = grid_snap_y(y, up=False), grid_snap_h(h)
    return (x, y, x + w, y + h)


def grid_stack(heights, c0, n, y0=None, gap=GRID_BASE):
    """blocks of the given heights stacked down one column span from y0 (default the drawing area's top), each on the
    baseline: [rect]; raises when the stack runs past the drawing area (no block may leave the page)"""
    y = GRID_AREA[1] if y0 is None else grid_snap_y(y0, up=False)
    out = []
    for h in heights:
        r = grid_cell(c0, n, y, h)
        out.append(r)
        y = r[3] + gap
    if out and out[-1][3] > GRID_AREA[3] + 1e-6:
        raise ValueError("grid stack runs %.1f mm past the drawing area" % (out[-1][3] - GRID_AREA[3]))
    return out


def grid_row(widths_cols, y, h, c0=1):
    """blocks side by side on one baseline row: widths_cols = [n columns each] from column c0: [rect]"""
    out, c = [], c0
    for n in widths_cols:
        out.append(grid_cell(c, n, y, h))
        c += n
    if c - 1 > GRID_COLS:
        raise ValueError("grid row needs %d columns, the grid has %d" % (c - 1, GRID_COLS))
    return out


def grid_sub(width_mm, n=None):
    """the sub-grid INSIDE a crop of width_mm (drawn to be shown at 1:1 on the page): [(x0, x1)] of its columns from
    the crop's left edge; n defaults to the whole page columns the width holds"""
    n = n or max(1, int(round((width_mm + GRID_GUT) / (GRID_COL + GRID_GUT))))
    col = (width_mm - (n - 1) * GRID_GUT) / float(n)
    return [(i * (col + GRID_GUT), i * (col + GRID_GUT) + col) for i in range(n)]


def grid_flip(y, page_h=None):
    """a top-down y (mm) as y-up (or back): page_h - y"""
    return (page_h or GRID_PAGE[1]) - y


def grid_rect_up(r, page_h=None):
    """a top-down rect (x0, y0, x1, y1) as a y-up rect (x0, y0, x1, y1) with y0 < y1"""
    H = page_h or GRID_PAGE[1]
    return (r[0], H - r[3], r[2], H - r[1])


def grid_page_counter(n, total=None):
    """the page number, bottom right: the current page only, "17" (round 3, G2 / U20: no "NN/total"; total is
    accepted and ignored so older callers keep working)"""
    return "%d" % int(n)


# ------------------------------------------------------------------------------------------- intro with bold runs
def grid_marked_runs(text):
    """marked text -> runs [(s, bold)]: "*word*" or "**words**" are bold key words, the rest regular. An unpaired
    star is printed as it is."""
    import re as _re
    out = []
    pos = 0
    for m in _re.finditer(r"\*\*(.+?)\*\*|\*(?!\s)([^*]+?)\*", text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False))
        out.append((m.group(1) if m.group(1) is not None else m.group(2), True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False))
    return [(s, b) for s, b in out if s]


def grid_plain(text):
    """marked text without its marks (for measuring or logging)"""
    return "".join(s for s, _ in grid_marked_runs(text))


def grid_wrap_runs(runs, width_mm, size_pt, measure):
    """runs wrapped to width_mm: lines of [(s, bold, x_offset_mm)]. measure(s, size_pt, bold) -> mm. Words keep their
    own weight; a bold run is never split from its following punctuation."""
    words = []                                    # [word, bold, space_before]
    sp_next = False
    for s, b in runs:
        for ch in s:
            if ch.isspace():
                sp_next = True
            elif words and not sp_next and words[-1][1] == b:
                words[-1][0] += ch
            else:
                words.append([ch, b, bool(words) and sp_next])
                sp_next = False
    lines, cur, x = [], [], 0.0
    for w, b, sp in words:
        gap = measure(" ", size_pt, False) if (sp and cur) else 0.0
        ww = measure(w, size_pt, b)
        if cur and x + gap + ww > width_mm + 1e-6 and sp:
            lines.append(cur)
            cur, x, gap = [], 0.0, 0.0
        if cur and not sp:                       # glued (e.g. "word," after a bold run): no space
            gap = 0.0
        cur.append((w, b, x + gap))
        x += gap + ww
    if cur:
        lines.append(cur)
    out = []                                      # merge neighbouring words of one weight into one run
    for ln in lines:
        m = []
        for w, b, xo in ln:
            if m and m[-1][1] == b:
                m[-1] = (m[-1][0] + (" " if xo > m[-1][3] + 1e-6 else "") + w, b, m[-1][2], xo + measure(w, size_pt, b))
            else:
                m.append((w, b, xo, xo + measure(w, size_pt, b)))
        out.append([(s, b, xo) for s, b, xo, _ in m])
    return out


def grid_intro(text, width_mm, measure, max_lines=3, style="intro", min_pt=8.0, log=None):
    """the page intro (G4: 2-3 lines, key words bold): marked text -> (lines, size_pt, lead_mm, hex). lines =
    [[(s, bold, x_offset_mm)]]. The size steps down by 0.5 pt (not below min_pt) until it fits max_lines; text that
    still does not fit keeps its lines and a WARNING goes to log (shorten it: the rule is 3 lines)."""
    size, _, lead, col = grid_style(style)
    runs = grid_marked_runs(text)
    s = size
    while True:
        lines = grid_wrap_runs(runs, width_mm, s, measure)
        if len(lines) <= max_lines or s - 0.5 < min_pt - 1e-6:
            break
        s -= 0.5
    if len(lines) > max_lines and log is not None:
        log.append(u"WARNING: intro longer than %d lines at %.1f pt (%d lines): %s" % (
            max_lines, s, len(lines), grid_plain(text)[:60]))
    return lines, s, lead * s / size, col


def grid_text_runs(lines, x, y, lead, y_down=True):
    """intro lines placed: [(s, x_mm, baseline_y_mm, bold)] from the first baseline (x, y); y_down=False for y-up
    pages (lines go to smaller y)"""
    out = []
    for i, ln in enumerate(lines):
        yy = y + i * lead if y_down else y - i * lead
        for s, b, xo in ln:
            out.append((s, x + xo, yy, b))
    return out
# ---- text_place.py (round 4, S1, 1 Nov 2026; G-R4-1, G-R4-2, PLAN §4.1): ONE text placer, a collision RAISES -------
# Replaces label_place.py (its lp_* names stay as shims there until the closing step, see label_place.py).
# Every printed letter of a page goes through ONE TextPage: it measures with the real font (font_metrics.py), keeps
# every box, draws everything in .emit(drawer) (no other text path), and .check() RAISES TextCollision when any two
# texts, a text and an obstacle, a text and the page edge / margins / footer zone, or two drawing blocks overlap.
# Needs, included before it: pdf_fonts.py, font_metrics.py, grid.py (GRID_MIN_PT, grid_marked_runs).
#
#   tp = TextPage(name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
#                 unit_mm=1.0, log=None)
#       name        the round 4 BOOKLET page id ("p13a", "p15"), used in every log line and error
#       bounds      (x0, y0, x1, y1) of the sheet / crop in page units; no text outside it (minus margins)
#       y_down      True when page y grows downward (the booklet grid), False for y-up sheets
#       min_pt      smallest PRINTED size (default GRID_MIN_PT = 6.0): pt x scale must reach it, else TextError
#       pad         clear gap (mm) every text keeps from other texts and obstacles
#       margins     (left, top, right, bottom) mm kept free inside bounds ("top" = the visual top)
#       footer_zone (x0, y0, x1, y1) page units where only role="footer" text may sit
#       scale       print factor of this sheet in the booklet (printed mm / sheet mm), for the min_pt test
#       unit_mm     mm per page unit (1.0 for mm sheets; the site board's board units differ)
#       log         a list for the log lines (default TP_LOG; tp_log_lines() empties it)
#   tp.keep(geom, kind="keep", name=None, line=None)   an obstacle no text may touch: a box (x0, y0, x1, y1), a closed
#                                                     area [(x, y) ...] or, with line=True (or kind in TP_LINE_KINDS),
#                                                     an open polyline (streets, banks, cut lines)
#   tp.block(box, name)                               a drawing block (map, section, key map, legend): blocks may touch,
#                                                     never overlap
#   tp.put(text, x, y, pt, bold=False, align="L", angle=0, name=None, role="label", colour=None, allow=(),
#          group=None, emit=True, **extra) -> box     one fixed text (title, caption, footer, scale figure, legend row);
#                                                     (x, y) = the baseline point at `align` (L / C / R; "MC" = the
#                                                     middle of the ink); angle degrees, counter-clockwise on the page;
#                                                     allow = names / kinds of keeps this text may sit on (a number
#                                                     on its own marker disc); emit=False registers text another
#                                                     writer draws (the booklet's crop text)
#   tp.para(text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
#           max_lines=None, min_last_words=2, allow=()) -> next baseline
#                                                     wraps with tp_wrap (real widths; "*word*" / "**word**" bold;
#                                                     "\n" breaks; last line >= 2 words, else 0.25 pt smaller once if
#                                                     that stays >= min_pt, else TextError); each run is placed at its
#                                                     measured x, so "Ulucami Önü" + " walking hub" keep their space
#   tp.place(text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
#            colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label") -> item dict
#                                                     a label beside its point: positions in reading order (E, NE, N,
#                                                     NW, W, SW, S, SE, C, or (dx, dy, align) in page units), then the
#                                                     shorter alts, then a NUMBER on the point + a row in side_list;
#                                                     never below min_pt, never dropped: no spot and no side_list
#                                                     raises TextCollision. rank orders nothing here (callers place
#                                                     rank 0 first); kept for the interface
#   tp.check(raise_=True, log=None) -> n_items        the collision test; logs "overlap <page> checked n, collisions k"
#                                                     and raises TextCollision(page, item, other) when k > 0
#   tp.emit(drawer) -> n                              drawer(item) for every text in order; item = dict(text, x, y,
#                                                     pt, size_mm, bold, align, angle, colour, role, name, extra)
#   tp.export() -> dict                               boxes in mm, y DOWN from the bounds' top-left (crop-local) for
#                                                     the booklet (BkBlocks.crop(..., text_boxes, keep))
#   TpSideList(name, row_mm=8.0)                      the numbered key rows of place(); .close(tp) numbers them in
#                                                     reading order (top row first, left to right); .rows() ->
#                                                     [(n, text)]; check() raises while a side list is open
#   tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True) -> [[(s, bold, x_mm)]]
#   tp_shapes(shapes, tp, name=None, allow=(), y_down=None) -> the other shapes
#                                                     registers the ("text", ...) shapes of the common modules
#                                                     (section_frame, water, basemap, figures, buildings, node, para,
#                                                     xform) in tp, which then draws them; returns the non-text shapes
#                                                     for the caller to draw as before
# Geometry helpers (moved here from label_place.py): tp_hit, tp_seg_box, tp_seg_cross, TpSegIndex, tp_reading_order.
TP_LOG = []
TP_PT = 25.4 / 72.0
TP_ROW_MM = 8.0                 # reading order: anchors within this many mm of height count as one row
TP_POSITIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
TP_LINE_KINDS = ("line", "edge", "street", "road", "cut", "stream", "bank", "contour", "leader")


class TextError(RuntimeError):
    pass


class TextCollision(TextError):
    def __init__(self, page, item, other, n=1, more=()):
        self.page, self.item, self.other, self.n, self.more = page, item, other, n, list(more)
        msg = u"text collision on %s: %s against %s" % (page, _tp_desc(item), _tp_desc(other))
        if n > 1:
            msg += u" (and %d more: %s)" % (n - 1, u"; ".join(u"%s / %s" % (_tp_desc(a), _tp_desc(b))
                                                               for a, b in self.more[:4]))
        RuntimeError.__init__(self, msg)


def _tp_desc(it):
    if it is None:
        return u"-"
    if isinstance(it, str):
        return it
    if isinstance(it, dict):
        if "text" in it:
            return u"text %r%s" % (it["text"][:40], (u" (%s)" % it["name"]) if it.get("name") else u"")
        return u"%s %s" % (it.get("kind", "obstacle"), it.get("name") or u"")
    return u"%r" % (it,)


def tp_log_lines():
    """this run's text log lines, oldest first; the list is emptied"""
    out = list(TP_LOG)
    del TP_LOG[:]
    return out


# ------------------------------------------------------------------------------------------------ geometry
def tp_hit(a, b, pad=0.0):
    """True when boxes a and b (x0, y0, x1, y1) come closer than pad"""
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def tp_seg_box(p, q, b):
    """True when the segment p-q passes through box b (Liang-Barsky)"""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - b[0]), (dx, b[2] - x0), (-dy, y0 - b[1]), (dy, b[3] - y0)):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def tp_seg_cross(p, q, r, s):
    """True when segments p-q and r-s cross (touching at a shared end point does not count)"""
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for a in (p, q):
        for b in (r, s):
            if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
                return False
    d1, d2, d3, d4 = orient(r, s, p), orient(r, s, q), orient(p, q, r), orient(p, q, s)
    return d1 * d2 < 0 and d3 * d4 < 0


class TpSegIndex(object):
    """linework in buckets, so a box tests only the segments near it"""
    def __init__(self, polylines=(), segs=(), cell=10.0):
        self.cell, self.b = float(cell), {}
        for P in polylines:
            for a, c in zip(P, P[1:]):
                self.add(a, c)
        for a, c in segs:
            self.add(a, c)

    def add(self, a, c):
        k = self.cell
        for i in range(int(min(a[0], c[0]) // k), int(max(a[0], c[0]) // k) + 1):
            for j in range(int(min(a[1], c[1]) // k), int(max(a[1], c[1]) // k) + 1):
                self.b.setdefault((i, j), []).append((a, c))

    def near(self, box):
        k, seen, out = self.cell, set(), []
        for i in range(int(box[0] // k), int(box[2] // k) + 1):
            for j in range(int(box[1] // k), int(box[3] // k) + 1):
                for sg in self.b.get((i, j), ()):
                    if id(sg) not in seen:
                        seen.add(id(sg))
                        out.append(sg)
        return out

    def __iter__(self):
        seen = set()
        for lst in self.b.values():
            for sg in lst:
                if id(sg) not in seen:
                    seen.add(id(sg))
                    yield sg


def tp_reading_order(pts, y_down=False, row_mm=TP_ROW_MM):
    """the indexes of pts [(x, y)] in reading order: rows from the visual top down (rows row_mm high), left to right"""
    import math as _m
    if not pts:
        return []
    top = min(p[1] for p in pts) if y_down else max(p[1] for p in pts)
    row = (lambda p: int(_m.floor((p[1] - top) / row_mm))) if y_down else \
        (lambda p: int(_m.floor((top - p[1]) / row_mm)))
    return sorted(range(len(pts)), key=lambda i: (row(pts[i]), pts[i][0], i))


def _tp_in_poly(pt, P):
    x, y = pt
    inside = False
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1:
            inside = not inside
    return inside


def _tp_keep_hits(b, K, pad):
    """True when box b comes within pad of the obstacle K"""
    if not tp_hit(b, K["box"], pad):
        return False
    if K["pts"] is None:
        return True
    bb = (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
    for p, q in K["segs"].near(bb):
        if tp_seg_box(p, q, bb):
            return True
    if K["line"]:
        return False
    return _tp_in_poly(((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0), K["pts"]) or \
        _tp_in_poly(K["pts"][0], [(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])


# ------------------------------------------------------------------------------------------------ wrapping
def _tp_units(text, bold, bold_marks):
    """the text as word units (each a list of (s, bold) pieces glued without a space); None marks a forced break"""
    runs = grid_marked_runs(text) if (bold_marks and "grid_marked_runs" in globals()) else [(text, False)]
    units, cur = [], None
    for s, b in runs:
        b = bool(b or bold)
        for ch in s:
            if ch == "\n":
                if cur:
                    units.append(cur)
                units.append(None)
                cur = None
            elif ch.isspace():
                if cur:
                    units.append(cur)
                cur = None
            elif cur is not None and cur[-1][1] == b:
                cur[-1] = (cur[-1][0] + ch, b)
            elif cur is not None:
                cur.append((ch, b))
            else:
                cur = [(ch, b)]
    if cur:
        units.append(cur)
    return units


class TpWidow(TextError):
    pass


def tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True):
    """text wrapped to w_mm with real widths: lines of [(s, bold, x_offset_mm)] (neighbouring words of one weight
    merged into one run). "\\n" forces a break. A word wider than w_mm raises TextError. The last line of every
    wrapped paragraph holds at least min_last_words words (words are pulled down from the line before); when that
    cannot be done, TpWidow is raised (TextPage.para then tries 0.25 pt smaller)."""
    sp_w = fm_width(u" ", pt, False)

    def uw(u):
        return sum(fm_width(s, pt, b) for s, b in u)
    paras, cur = [], []
    for u in _tp_units(text, bold, bold_marks):
        if u is None:
            paras.append(cur)
            cur = []
        else:
            cur.append(u)
    paras.append(cur)
    out = []
    for words in paras:
        if not words:
            out.append([])
            continue
        lines, ln, x = [], [], 0.0
        for u in words:
            w = uw(u)
            if w > w_mm + 1e-6:
                raise TextError(u"the word %r (%.1f mm at %.1f pt) is wider than its column (%.1f mm)" % (
                    u"".join(s for s, _ in u), w, pt, w_mm))
            if ln and x + sp_w + w > w_mm + 1e-6:
                lines.append(ln)
                ln, x = [], 0.0
            x += (sp_w if ln else 0.0) + w
            ln.append(u)
        lines.append(ln)
        if len(lines) >= 2 and min_last_words > 1:
            while len(lines[-1]) < min_last_words:
                prev = lines[-2]
                if len(prev) <= 2:
                    raise TpWidow(u"last line %r would hold fewer than %d words" % (
                        u"".join(s for s, _ in lines[-1][0]), min_last_words))
                mv = prev.pop()
                lines[-1].insert(0, mv)
                if sum(uw(u) for u in lines[-1]) + sp_w * (len(lines[-1]) - 1) > w_mm + 1e-6:
                    raise TpWidow(u"last line cannot take one more word without passing the column width")
        for ln in lines:
            row, x = [], 0.0                       # row: [text, bold, x_offset]; one run per stretch of one weight
            for i, u in enumerate(ln):
                for j, (s, b) in enumerate(u):
                    gap = (i > 0 and j == 0)
                    if row and row[-1][1] == b:
                        row[-1][0] += (u" " if gap else u"") + s
                    else:
                        row.append([s, b, x + (sp_w if gap else 0.0)])
                    x += (sp_w if gap else 0.0) + fm_width(s, pt, b)
            out.append([(s, b, xo) for s, b, xo in row])
    return out


# ------------------------------------------------------------------------------------------------ the page
class TpSideList(object):
    """the numbered key of place(): rows numbered in reading order when closed"""
    def __init__(self, name, row_mm=TP_ROW_MM):
        self.name, self.row_mm, self.entries, self.closed = name, row_mm, [], False

    def add(self, anchor, text, item):
        if self.closed:
            raise TextError(u"side list %s is closed: place its labels before close()" % self.name)
        e = dict(anchor=tuple(anchor), text=text, item=item, n=None)
        self.entries.append(e)
        return e

    def close(self, tp):
        """numbers the entries in reading order and re-measures their number boxes"""
        order = tp_reading_order([e["anchor"] for e in self.entries], tp.y_down, self.row_mm / tp.unit_mm)
        for n, j in enumerate(order, 1):
            e = self.entries[j]
            e["n"] = n
            it = e["item"]
            it["text"] = u"%d" % n
            it["box"] = tp._box(it["text"], it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.closed = True
        return self.rows()

    def rows(self):
        return [(e["n"], e["text"]) for e in sorted(self.entries, key=lambda e: e["n"] or 0)]


class TextPage(object):
    def __init__(self, name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
                 unit_mm=1.0, log=None):
        if not bounds or len(bounds) != 4 or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
            raise TextError(u"TextPage %s: bounds must be (x0, y0, x1, y1)" % name)
        self.name, self.bounds, self.y_down = name, tuple(float(v) for v in bounds), bool(y_down)
        self.min_pt = float(GRID_MIN_PT if min_pt is None else min_pt)
        self.unit_mm, self.scale = float(unit_mm), float(scale)
        self.pad = pad / self.unit_mm
        m = [v / self.unit_mm for v in (margins or (0.0, 0.0, 0.0, 0.0))]
        b = self.bounds
        if self.y_down:
            self.inner = (b[0] + m[0], b[1] + m[1], b[2] - m[2], b[3] - m[3])
        else:
            self.inner = (b[0] + m[0], b[1] + m[3], b[2] - m[2], b[3] - m[1])
        self.footer_zone = tuple(footer_zone) if footer_zone else None
        self.log = log
        self.items, self.keeps, self.blocks, self.sides = [], [], [], []
        self._gid, self.checked = 0, False

    # -- measuring
    def _box(self, text, x, y, pt, bold=False, align="L", angle=0.0):
        b = fm_box(text, 0.0, 0.0, pt, bold, align, angle, self.y_down)
        u = self.unit_mm
        return (x + b[0] / u, y + b[1] / u, x + b[2] / u, y + b[3] / u)

    def _group(self):
        self._gid += 1
        return "g%d" % self._gid

    def _size_ok(self, text, pt):
        if pt * self.scale < self.min_pt - 1e-6:
            raise TextError(u"%s: %r would print at %.2f pt, below the %.1f pt minimum" % (
                self.name, text[:40], pt * self.scale, self.min_pt))

    # -- registering
    def keep(self, geom, kind="keep", name=None, line=None):
        """an obstacle no text may touch (see the module notes)"""
        g = list(geom)
        if len(g) == 4 and not hasattr(g[0], "__len__"):
            K = dict(kind=kind, name=name, box=tuple(float(v) for v in g), pts=None, line=False, segs=None)
        else:
            P = [tuple(p[:2]) for p in g]
            if len(P) < 2:
                return None
            is_line = (kind in TP_LINE_KINDS) if line is None else bool(line)
            xs, ys = [p[0] for p in P], [p[1] for p in P]
            segs = list(zip(P, P[1:])) + ([] if is_line else [(P[-1], P[0])])
            K = dict(kind=kind, name=name, box=(min(xs), min(ys), max(xs), max(ys)), pts=P, line=is_line,
                     segs=TpSegIndex(segs=segs, cell=max(5.0 / self.unit_mm, 1e-6)))
        self.keeps.append(K)
        return K

    def block(self, box, name):
        """a drawing block (blocks may touch, never overlap)"""
        B = dict(kind="block", name=name, box=tuple(float(v) for v in box))
        self.blocks.append(B)
        return B["box"]

    def put(self, text, x, y, pt, bold=False, align="L", angle=0.0, name=None, role="label", colour=None, allow=(),
            group=None, emit=True, **extra):
        """one fixed text; returns its box"""
        text = u"%s" % text
        if not text.strip():
            return None
        self._size_ok(text, pt)
        it = dict(text=text, x=float(x), y=float(y), pt=float(pt), size_mm=pt * TP_PT, bold=bool(bold),
                  align=align or "L", angle=float(angle or 0.0), colour=colour, role=role, name=name,
                  allow=tuple(allow or ()), group=group or self._group(), emit=bool(emit), extra=extra)
        it["box"] = self._box(text, it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.items.append(it)
        self.checked = False
        return it["box"]

    def para(self, text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
             max_lines=None, min_last_words=2, allow=()):
        """a wrapped paragraph from the first baseline (x, y), w and lead in page units; returns the next baseline"""
        u = self.unit_mm
        size = float(pt)
        try:
            lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
        except TpWidow:
            size = size - 0.25
            self._size_ok(text, size)
            lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
            lead = lead * size / float(pt)
        if max_lines is not None and len(lines) > max_lines:
            raise TextError(u"%s: %r needs %d lines, %d allowed: shorten it" % (self.name, text[:50], len(lines),
                                                                               max_lines))
        g = self._group()
        sg = 1.0 if self.y_down else -1.0
        yy = float(y)
        for ln in lines:
            for s, b, xo in ln:
                self.put(s, x + xo / u, yy, size, b, "L", 0.0, name, role, colour, allow, g)
            yy += sg * lead
        return yy

    def _at(self, code, text, anchor, pt, bold, d):
        """(x, y, align) of a compass position code round the anchor"""
        if not isinstance(code, str):
            dx, dy, al = code
            return anchor[0] + dx, anchor[1] + dy, al
        ix0, iy0, ix1, iy1 = fm_ink_box(text, pt, bold)
        u, sg = self.unit_mm, (-1.0 if self.y_down else 1.0)
        k = 0.7071 * d
        mid = -(iy0 + iy1) / 2.0
        tab = dict(E=(d, mid, "L"), W=(-d, mid, "R"), N=(0.0, d - iy0, "C"), S=(0.0, -d - iy1, "C"),
                   NE=(k, k - iy0, "L"), NW=(-k, k - iy0, "R"), SE=(k, -k - iy1, "L"), SW=(-k, -k - iy1, "R"),
                   C=(0.0, mid, "C"))
        dx, v, al = tab[code.upper()]
        return anchor[0] + dx / u, anchor[1] + sg * v / u, al

    def _free(self, b, allow=(), group=None):
        if not (self.inner[0] <= b[0] and b[2] <= self.inner[2] and self.inner[1] <= b[1] and b[3] <= self.inner[3]):
            return False
        if self.footer_zone and tp_hit(b, self.footer_zone, 0.0):
            return False
        for it in self.items:
            if it["group"] != group and tp_hit(b, it["box"], self.pad):
                return False
        for K in self.keeps:
            if K["name"] in allow or K["kind"] in allow:
                continue
            if _tp_keep_hits(b, K, self.pad):
                return False
        return True

    def place(self, text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
              colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label"):
        """a label beside its point (see the module notes); returns the registered item"""
        d = float(r) * self.unit_mm + gap
        for t in (text,) + tuple(alts or ()):
            t = u"%s" % t
            self._size_ok(t, pt)
            for code in positions:
                x, y, al = self._at(code, t, anchor, pt, bold, d)
                b = self._box(t, x, y, pt, bold, al, 0.0)
                if self._free(b, allow):
                    self.put(t, x, y, pt, bold, al, 0.0, name, role, colour, allow)
                    return self.items[-1]
        if side_list is None:
            raise TextCollision(self.name, dict(text=u"%s" % text, name=name), u"no free spot round its point and no "
                                u"side list to number it")
        x, y, al = self._at("C", u"0", anchor, pt, True, 0.0)
        self.put(u"0", x, y, pt, True, "C", 0.0, name, "number", colour, tuple(allow) + ("marker",))
        it = self.items[-1]
        if side_list not in self.sides:
            self.sides.append(side_list)
        side_list.add(anchor, u"%s" % text, it)
        return it

    # -- the test
    def check(self, raise_=True, log=None):
        """the collision test (see the module notes); returns the number of texts checked"""
        for sl in self.sides:
            if not sl.closed:
                raise TextError(u"%s: side list %s was never closed (its numbers are not set)" % (self.name, sl.name))
        hits = []
        I = self.items
        for i, a in enumerate(I):
            b = a["box"]
            if not (self.inner[0] - 1e-6 <= b[0] and b[2] <= self.inner[2] + 1e-6 and
                    self.inner[1] - 1e-6 <= b[1] and b[3] <= self.inner[3] + 1e-6):
                hits.append((a, u"the page edge or its margins"))
            if self.footer_zone and a["role"] != "footer" and tp_hit(b, self.footer_zone, 0.0):
                hits.append((a, u"the footer zone"))
            for c in I[i + 1:]:
                if c["group"] != a["group"] and tp_hit(b, c["box"], self.pad):
                    hits.append((a, c))
            for K in self.keeps:
                if K["name"] in a["allow"] or K["kind"] in a["allow"]:
                    continue
                if _tp_keep_hits(b, K, self.pad):
                    hits.append((a, K))
        B = self.blocks
        for i, a in enumerate(B):
            for c in B[i + 1:]:
                if tp_hit(a["box"], c["box"], -0.01 / self.unit_mm):
                    hits.append((a, c))
        line = u"overlap %s checked %d, collisions %d" % (self.name, len(I), len(hits))
        lg = log if log is not None else (self.log if self.log is not None else TP_LOG)
        lg.append(line)
        self.checked = True
        if hits and raise_:
            raise TextCollision(self.name, hits[0][0], hits[0][1], len(hits), hits[1:])
        return len(I)

    def emit(self, drawer):
        """draws every registered text through drawer(item); returns how many"""
        n = 0
        for it in self.items:
            if not it["emit"]:
                continue
            if it["role"] == "number" and it["text"] == u"0":
                raise TextError(u"%s: a numbered label was never given its number (close its side list)" % self.name)
            drawer(it)
            n += 1
        return n

    def export(self):
        """boxes in mm, y DOWN from the top-left of bounds (crop-local), for the booklet's assembled-page test"""
        if not self.checked:
            raise TextError(u"%s: export() before check()" % self.name)
        u, b = self.unit_mm, self.bounds

        def mm(r):
            if self.y_down:
                return ((r[0] - b[0]) * u, (r[1] - b[1]) * u, (r[2] - b[0]) * u, (r[3] - b[1]) * u)
            return ((r[0] - b[0]) * u, (b[3] - r[3]) * u, (r[2] - b[0]) * u, (b[3] - r[1]) * u)
        return dict(page=self.name, size_mm=((b[2] - b[0]) * u, (b[3] - b[1]) * u),
                    texts=[dict(box=mm(it["box"]), role=it["role"], name=it["name"], text=it["text"])
                           for it in self.items],
                    keep=[dict(box=mm(K["box"]), kind=K["kind"], name=K["name"]) for K in self.keeps],
                    blocks=[dict(box=mm(B["box"]), name=B["name"]) for B in self.blocks])


def tp_shapes(shapes, tp, name=None, allow=(), y_down=None):
    """registers the text shapes of a common module's shape list in tp (tp draws them in emit) and returns the other
    shapes. Text shape forms: ("text", s, x, y, size_mm, colour, bold, align[, mat, halo]) and
    ("text", s, (x, y), size_mm, colour, bold, align); align "MC" = (x, y) is the middle of the ink."""
    rest = []
    for s_ in shapes or ():
        if not s_ or s_[0] != "text":
            rest.append(s_)
            continue
        if isinstance(s_[2], (tuple, list)):
            x, y = s_[2][0], s_[2][1]
            tail = list(s_[3:])
        else:
            x, y = s_[2], s_[3]
            tail = list(s_[4:])
        size_mm = tail[0]
        col = tail[1] if len(tail) > 1 else None
        bold = tail[2] if len(tail) > 2 else False
        al = tail[3] if len(tail) > 3 else "L"
        extra = {}
        if len(tail) > 4 and tail[4] is not None:
            extra["mat"] = tail[4]
        if len(tail) > 5 and tail[5] is not None:
            extra["halo"] = tail[5]
        tp.put(s_[1], x, y, size_mm * tp.unit_mm / TP_PT, bold, al, 0.0, name, "shape", col, allow, **extra)
    return rest
# ---- marker.py (round 4, S1, 1 Nov 2026; G-R4-7, PLAN §4.4): ONE marker (circle + number / letter) everywhere --------
# The glyph sits on the centre of its VISIBLE ink box (font_metrics.fm_ink_box), so "g", "h", "1" and "12" are all
# centred (CHK3_7 §4.1: the old cap-height offsets pulled lowercase letters down and let tails hang out). The circle
# grows with the glyph: radius = half the ink box diagonal + MK_MARGIN_MM, so two digits get a larger circle (§4.2).
# The colour is the colour the named element is drawn in, from ONE table (mk_colour), never a page-wide accent (§4.3).
# Needs font_metrics.py (and pdf_fonts.py) included before it; text_place.py for mk_put.
#   mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
#             y_down=False) -> (shapes, box, r)
#       y_down  False (default) for the scripts' y-up sheets and the common modules' shape lists (section_frame,
#               figures); True on y-down pages (the booklet grid)
#       shapes  house format: ("poly", ring, fill, stroke, lw) then ("text", s, x, baseline_y, size_mm, colour, True,
#               "L"); box = the marker's outer box (rim included); r = the circle's radius (mm)
#       style   "solid": a disc in colour, a white rim, the glyph white or ink by contrast;
#               "ring": a paper disc, a coloured rim, the glyph in colour
#   mk_register(kind, table)          the element table a page draws with ({key: hex}), so marker = element colour
#   mk_colour(kind, key) -> hex       the registered colour; an unknown kind / key RAISES (no fallback colour)
#   mk_put(tp, shapes, name=None) -> the non-text shapes
#                                     registers the disc as a keep (kind "marker") and the glyph in the TextPage (it
#                                     may sit on its own disc only; give each marker its own name); the caller draws the returned disc shapes, the
#                                     TextPage draws the glyph
MK_MARGIN_MM = 0.45                    # clear ring round the glyph's ink box (G-R4-7 "keep a margin")
MK_PAPER = "FFFFFF"
MK_INK = "2C2219"                      # dark glyph on light discs (the north-arrow ink of PLAN §4.5)
MK_COLOURS = {}
MK_N = [0]                             # markers registered this run (unique keep names)


def _mk_lum(hx):
    """relative luminance (WCAG 2) of a hex colour"""
    h = str(hx).lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def _mk_contrast(a, b):
    la, lb = _mk_lum(a), _mk_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mk_text_colour(fill):
    """white or ink, whichever contrasts more with fill"""
    return MK_PAPER if _mk_contrast(fill, MK_PAPER) >= _mk_contrast(fill, MK_INK) else MK_INK


def mk_register(kind, table):
    """the colours a page draws its elements of one kind with ({key: hex}); markers of that kind read them"""
    MK_COLOURS.setdefault(kind, {}).update(dict((str(k), str(v).lstrip("#")) for k, v in table.items()))


def mk_colour(kind, key):
    """the colour the named element is drawn in"""
    try:
        return MK_COLOURS[kind][str(key)]
    except KeyError:
        raise KeyError(u"marker colour: no element colour registered for %s / %s (mk_register it from the table the "
                       u"element is drawn with)" % (kind, key))


def mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
              y_down=False):
    """one marker centred on (cx, cy) page mm (see the module notes)"""
    import math as _m
    s = u"%s" % s
    col = str(colour).lstrip("#")
    ix0, iy0, ix1, iy1 = fm_ink_box(s, size_pt, True)
    r = 0.5 * _m.hypot(ix1 - ix0, iy1 - iy0) + MK_MARGIN_MM
    if r_min is not None:
        r = max(r, float(r_min))
    ring = [(cx + r * _m.cos(2 * _m.pi * i / 48.0), cy + r * _m.sin(2 * _m.pi * i / 48.0)) for i in range(48)]
    if style == "ring":
        lw = max(rim_mm, 0.25)
        disc = ("poly", ring, MK_PAPER, col, lw)
        tc = text_col or col
        out_r = r + lw / 2.0
    else:
        disc = ("poly", ring, col, rim if rim_mm else None, rim_mm)
        tc = text_col or mk_text_colour(col)
        out_r = r + (rim_mm / 2.0 if rim_mm else 0.0)
    x = cx - (ix0 + ix1) / 2.0
    base = cy + (iy0 + iy1) / 2.0 if y_down else cy - (iy0 + iy1) / 2.0
    size_mm = size_pt * 25.4 / 72.0
    shapes = [disc, ("text", s, x, base, size_mm, tc, True, "L")]
    return shapes, (cx - out_r, cy - out_r, cx + out_r, cy + out_r), r


def mk_put(tp, shapes, name=None):
    """registers a marker in the TextPage tp: its disc as a keep, its glyph as a text that may sit on that disc;
    returns the disc shapes for the caller to draw (before tp.emit draws the glyph)"""
    disc = [s_ for s_ in shapes if s_ and s_[0] != "text"]
    MK_N[0] += 1
    nm = name or u"marker %d" % MK_N[0]
    for s_ in disc:
        if s_[0] == "poly":
            tp.keep(s_[1], "marker", nm)
    for s_ in shapes:
        if s_ and s_[0] == "text":
            tp.put(s_[1], s_[2], s_[3], s_[4] * tp.unit_mm / TP_PT, True, "L", 0.0, nm, "marker", s_[5], allow=(nm,))
    return disc
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_agriculture_alternatives_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_agriculture_alternatives_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_agriculture_alternatives_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'NAMES': '0972af4b119d556bb810b350fd8e70f4', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011', 'GEO': '8db5c86b0c11c98efb00cbe4dffb2aff'}.get(name):
        raise RuntimeError("Data file bergama_agriculture_alternatives_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_agriculture_alternatives_data.py:" + name, "exec"), globals())


bergama_data("NAMES")
# ---- Names (round 3, A2, 31 Oct 2026; G16 / D9): every printed bridge or place name comes from data/NAMES.py ---------
#   bridge_name(code, short=False)   "K3" -> "Tabak Köprüsü" (short: "Tabak", only where the full name is in the
#                                     same drawing's key or title); unknown code -> KeyError (never print a K-code)
#   bridges_in_order()               the codes upstream first: K1, K2, K4, K3, K5, K6 (lists, keys, rulers)
#   place_name(key)                  "bank_NE" -> "Kale side · north bank", "stream" -> "Selinos stream"
#   cut_end_labels(cid)              ("W3", "W3'") the cut id + prime at its ends (D6)
#   landmark_name(key, descr=None)   round 4 (S1, G-R4-11): "kizil_avlu" -> "Kızıl Avlu"; descr=True adds the table's
#                                     English descriptor ("Kızıl Avlu · Hadrian's temple"), descr="text" adds that text;
#                                     unknown key -> KeyError (never type a landmark name locally)
#   landmark_keys()                  the landmark keys in the table
# Needs data/NAMES.py included before it.


def bridge_name(code, short=False):
    """the one spelling of a bridge by its internal code (K1-K6, any case)"""
    row = NAMES["bridges"][str(code).strip().upper()]
    return row["short"] if short else row["name"]


def bridges_in_order():
    """the bridge codes in stream order, upstream first"""
    b = NAMES["bridges"]
    return sorted(b, key=lambda c: b[c]["order"])


def place_name(key):
    """the one spelling of a place (stream, banks, sides)"""
    return NAMES["places"][key]


def cut_end_labels(cid):
    """D6: the labels at a cut's two ends: the cut id and the id with a prime ("W3", "W3'")"""
    c = str(cid).strip()
    return c, c + u"'"


def landmark_name(key, descr=None):
    """the one (Turkish) spelling of a landmark, optionally followed by an English descriptor"""
    row = NAMES["landmarks"][str(key).strip().lower()]
    if descr is True:
        d = row.get("descr")
        if not d:
            raise KeyError(u"landmark %s has no descriptor in the names table" % key)
    else:
        d = descr or None
    return row["name"] + (u" · " + d if d else u"")


def landmark_keys():
    """the landmark keys in the names table"""
    return sorted(NAMES["landmarks"])
bergama_data("FACTS")
# ---- Shared facts reader (H-B 30 Oct 2026, M10). Include the data first:
#   #@include ../common/data/FACTS.py
#   #@include ../common/facts.py
# fact(key) = the value (float, or a (lo, hi) tuple for a range), unrounded; fact_text(key) = the printed form with
# the fact's fixed rounding and unit ("8,000 m³ per ha (1-in-5 dry year)"); None when a live file is missing (the
# page then prints nothing for it, never a typed copy). Live values come from Downloads/Bergama outputs on every run.
# The one page that prints a fact: fact_owner(key); a page that is not the owner should not print it (G4).
FACT_LOG = []
_FACT_CACHE = {}


def _fact_home(*p):
    import os as _o
    return _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", *p)


# results files other scripts write (new place first, then where older versions wrote them)
FACT_FILES = dict(water_balance=[
    ("cached", "Bergama_water_balance_analysis", "water_balance_results.json"),
    ("output", "Bergama_water_balance_analysis", "water_balance_results.json")])


def _fact_rows():
    rows = globals().get("FACTS")
    if rows is None:
        raise RuntimeError("FACTS data missing: include ../common/data/FACTS.py before ../common/facts.py")
    return rows


def fact_file(name):
    """the parsed results file of another script (dict) or None; read once per run"""
    import os as _o
    import json as _j
    if name in _FACT_CACHE:
        return _FACT_CACHE[name]
    data = None
    paths = [_fact_home(*p) for p in FACT_FILES.get(name, [])]
    if name == "water_balance":                    # the oldest place, before Downloads/Bergama (water board WB_FILES)
        paths.append(_o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis",
                                  "water_balance_results.json"))
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = _j.load(fh)
            FACT_LOG.append(u"Facts: %s read from %s" % (name, p))
            break
        except Exception:
            pass
    if data is None:
        FACT_LOG.append(u"Facts: %s results not found (run that script first); its facts are left out" % name)
    _FACT_CACHE[name] = data
    return data


def _fact_conv(row, v):
    c = row.get("conv")
    if v is None or c is None:
        return v
    if c == "drip_m3_ha":                          # net mm -> m³ per ha at the intake (1 mm on 1 ha = 10 m³)
        return v / fact("drip_efficiency") * 10.0
    if c == "ha_per_10000":
        return 10000.0 / v
    if c == "ratio":
        return float(v[0]) / float(v[1])
    if c == "da_sum_ha":                           # decares summed -> ha
        return sum(v) / 10.0
    raise ValueError("facts: unknown conv %r" % c)


def fact(key):
    """the value of a fact, unrounded (float, or (lo, hi)); None when a live source is missing"""
    rows = _fact_rows()
    if key not in rows:
        raise KeyError("no fact %r; known: %s" % (key, ", ".join(sorted(rows))))
    row = rows[key]
    k = row["kind"]
    if k == "static":
        return _fact_conv(row, row["value"])
    if k == "derived":
        return _fact_conv(row, fact(row["of"]))
    d = fact_file(row["file"])
    try:
        for p in row["path"]:
            d = d[p]
    except Exception:
        if d is not None:
            FACT_LOG.append(u"Facts: %s not in the %s results" % (key, row["file"]))
        return None
    if isinstance(d, (list, tuple)):
        return tuple(float(x) for x in d)
    return _fact_conv(row, float(d))


def fact_live(key):
    """True when the fact has a value now (static, or its live file was read)"""
    return fact(key) is not None


def fact_round(key, v):
    """v rounded as the fact prints it (round step, or nd decimals)"""
    row = _fact_rows()[key]
    if row.get("round"):
        st = float(row["round"])
        return int(round(v / st) * st)
    return round(v, row.get("nd", 0))


def fact_num(key, v=None):
    """the printed number only ("8,000", "1.25", "350,000-375,000"); None when missing"""
    v = fact(key) if v is None else v
    if v is None:
        return None
    row = _fact_rows()[key]
    nd = 0 if row.get("round") else row.get("nd", 0)

    def one(x):
        return ("{:,.%df}" % nd).format(fact_round(key, x))
    if isinstance(v, tuple):
        a, b = one(v[0]), one(v[1])
        return a if a == b else u"%s-%s" % (a, b)
    return one(v)


def fact_text(key, note=True):
    """number + unit (+ note): "8,000 m³ per ha (1-in-5 dry year)", "4.4 × its potential"; None when missing"""
    n = fact_num(key)
    if n is None:
        return None
    row = _fact_rows()[key]
    s = n + (u" " + row["unit"] if row.get("unit") else u"")
    if note and row.get("note"):
        s += u" " + row["note"]
    return s


def fact_ref(key):
    """(internal reference, public citation or None) of a fact"""
    row = _fact_rows()[key]
    return row.get("ref"), row.get("public")


def fact_owner(key):
    """the booklet page that prints the fact ("18"), None for a value that is never printed"""
    return _fact_rows()[key].get("printed_on")


def fact_prints_on(key, page):
    """True when page (a booklet page number) is the one that prints this fact (G4: once in the booklet)"""
    return str(_fact_rows()[key].get("printed_on")) == str(page)
LOG_DIR = bg_logs()                       # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_agriculture_alternatives_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v1 24 Oct: all files under Downloads/Bergama/ (Aras rule)
OUT_DIR = bg_output("Bergama_agriculture_alternatives")       # final PDFs only (27 Oct)
OUT_PDF = "Bergama_agriculture_alternatives_A3.pdf"
# built-in geometry and tables (survey coordinates, m): around2 extent, site frame, WorldCover classes clipped to the
# extent (outside / inside the site), Selinos and other streams, FAO-56 net irrigation per water year (C1), corridor cover
bergama_data("GEO")

# ------------------------------------------------------------------ live numbers from the water balance (Thread 2)
# The water balance script writes its results on every run; this script reads them, so storage and the share covered
# are never typed in here. Searched in this order; the first file found wins.
LIVE_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
              os.path.join(bg_output("Bergama_water_balance_analysis"), "water_balance_results.json"),  # v2.6 and older
              os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]   # old place, read fallback
# fallback: the cloud copy research/water_balance/water_balance_results_default.json (default lands, 24 Oct 08:23)
DEFAULT = json.loads('{"cutoff":{"orchard olive + cropland cotton":{"central":{"storage_m3":375000,"covered_pct_1in5_dry":99.2,"delivered_m3_per_year":336093}},"orchard olive + cropland tomato":{"central":{"storage_m3":350000,"covered_pct_1in5_dry":99.7,"delivered_m3_per_year":310094}}},"farm_demand_m3":{"orchard olive + cropland cotton":{"mean":339980,"median":348773,"wet5":315782,"dry5":356580,"dry10":382453,"min":278845,"max":393001,"dry5_year":2006},"orchard olive + cropland tomato":{"mean":311982,"median":319136,"wet5":288317,"dry5":334143,"dry10":343054,"min":251458,"max":362453,"dry5_year":2021}},"net_irrigation_mm":{"olive":{"mean":614.3,"median":619.5,"wet5":519.6,"dry5":720.1,"dry10":725.2,"min":415.2,"max":822.7},"cotton":{"mean":853.2,"median":875.6,"wet5":789.5,"dry5":891.8,"dry10":962.6,"min":703.1,"max":981.9},"maize":{"mean":722.7,"median":740.8,"wet5":675.4,"dry5":761.8,"dry10":816.2,"min":605.7,"max":835.7},"tomato":{"mean":781.0,"median":801.3,"wet5":719.7,"dry5":837.0,"dry10":860.8,"min":632.5,"max":903.1}},"lands":{"cropland_ha":34.9,"orchard_ha":1.34,"cropland_crops":"cotton,tomato"}}')
DEFAULT_NOTE = "water balance default-lands copy, 24 Oct"   # v1.4: the log says when it is used

def live():
    """storage, share covered and need per mix (cost cut-off, central case), farm areas, crops and net need per crop"""
    d, src = None, DEFAULT_NOTE
    for p in LIVE_FILES:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            src = "water balance results of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            d = None
    if d is None: d = DEFAULT
    mixes = [m for m in d["cutoff"] if m in d["farm_demand_m3"]]
    L = dict(storage_m3=[d["cutoff"][m]["central"]["storage_m3"] for m in mixes],
             farm_share_dry5_pct=[d["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in mixes],
             farm_need_dry5_m3=[d["farm_demand_m3"][m]["dry5"] for m in mixes],
             cropland_ha=d["lands"]["cropland_ha"], orchard_ha=d["lands"]["orchard_ha"],
             crops=[c.strip() for c in str(d["lands"].get("cropland_crops", "")).split(",") if c.strip()],
             net=d["net_irrigation_mm"])
    L["year_split"] = (d.get("design") or {}).get("year_split")      # v3: water balance v4 and newer
    L["design_mix"] = (d.get("design") or {}).get("mix", "")
    return L, src

def span(v):
    return (min(v), max(v)) if isinstance(v, (list, tuple)) else (v, v)

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
# v9 (round 4, G-R4-1): ² and ³ are the embedded Arial's own glyphs again (pdf_fonts.py since 28 Oct): the v3 raised
# 0.6 x digit printed at 4.2-4.5 pt, under the booklet's 6 pt minimum the text placer enforces; the unembedded
# Helvetica that lost them in some viewers is gone. (v3's SUP, SUP_K, SUP_UP and sup_runs deleted.)


def text_w(s, size, bold=False):
    """v9 (round 4, G-R4-1): the REAL Arial advance width (font_metrics.fm_width) of s at size pt, in mm; the
    Helvetica table (common/text_w.py) is gone (a missing font raises FontMissing, no estimate)"""
    return fm_width(s, size, bold)


# ---- G2/G3 (MIRAQUA round, 28 Oct 2026): Arial EMBEDDED in every sheet PDF -------------------------------------
# The sheets wrote the PDF standard fonts without embedding (Helvetica, Courier) with the Turkish letters in unused
# WinAnsi slots: the text was right (it copies and searches as İ ğ ş), but viewers without those glyphs drew nothing
# ("stiklal", "De irmen"). Now each font slot is Arial, embedded as a simple TrueType font with the SAME encoding
# (WinAnsi + the six Turkish letters in slots 129/141/143/144/157/158), so the strings, their measuring and the
# booklet's reading of the sheets stay as they were. Arial has Helvetica's widths, so nothing moves; text measured
# as Courier (the old monospace captions) comes out a little shorter. Text stays live for Illustrator.
# The font files are the system's (C:\Windows\Fonts\arial*.ttf, or the user's font folder): read and packed once per
# run. If a file is missing, that slot falls back to the old standard font and PDF_FONT_NOTE says so (for the log).
_PF_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PF_FILES = {"R": ("arial.ttf", "ArialMT", "Helvetica"), "B": ("arialbd.ttf", "Arial-BoldMT", "Helvetica-Bold"),
             "I": ("ariali.ttf", "Arial-ItalicMT", "Helvetica-Oblique"),
             "BI": ("arialbi.ttf", "Arial-BoldItalicMT", "Helvetica-BoldOblique")}
_PF_CACHE = {}
PDF_FONT_NOTE = []


def _pf_path(fn):
    import os as _o
    dirs = [_o.path.join(_o.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
            _o.path.join(_o.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
            "/Library/Fonts", "/System/Library/Fonts/Supplemental", "/usr/share/fonts/truetype/msttcorefonts"]
    for d in dirs:
        for nm in (fn, fn.capitalize(), fn.upper()):
            p = _o.path.join(d, nm)
            if _o.path.isfile(p):
                return p
    return None


def _pf_tables(data):
    """Round 4 (S1, 1 Nov 2026): the TrueType tables both the embedding (_pf_metrics) and the measuring
    (font_metrics.py) read, parsed once: upm, gid(char code) -> glyph id, adv (advance per glyph id), glyph_box(gid)
    -> (xMin, yMin, xMax, yMax) in font units or None (empty glyph), and the table offsets"""
    import struct as _s
    n = _s.unpack(">H", data[4:6])[0]
    tab = {}
    for i in range(n):
        tag, _c, off, ln = _s.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tab[tag.decode("latin-1")] = (off, ln)
    h = tab["head"][0]
    upm = _s.unpack(">H", data[h + 18:h + 20])[0]
    bbox = _s.unpack(">hhhh", data[h + 36:h + 44])
    hh = tab["hhea"][0]
    asc, desc = _s.unpack(">hh", data[hh + 4:hh + 8])
    nhm = _s.unpack(">H", data[hh + 34:hh + 36])[0]
    hm = tab["hmtx"][0]
    adv = [_s.unpack(">H", data[hm + 4 * i:hm + 4 * i + 2])[0] for i in range(nhm)]
    cm = tab["cmap"][0]
    sub = None
    for i in range(_s.unpack(">H", data[cm + 2:cm + 4])[0]):
        pid, eid, off = _s.unpack(">HHI", data[cm + 4 + 8 * i:cm + 12 + 8 * i])
        if pid == 3 and eid == 1:
            sub = cm + off
    seg = _s.unpack(">H", data[sub + 6:sub + 8])[0] // 2
    ends = _s.unpack(">%dH" % seg, data[sub + 14:sub + 14 + 2 * seg])
    p = sub + 16 + 2 * seg
    starts = _s.unpack(">%dH" % seg, data[p:p + 2 * seg])
    deltas = _s.unpack(">%dh" % seg, data[p + 2 * seg:p + 4 * seg])
    ro_at = p + 4 * seg
    ros = _s.unpack(">%dH" % seg, data[ro_at:ro_at + 2 * seg])

    def gid(u):
        for k in range(seg):
            if starts[k] <= u <= ends[k]:
                if ros[k] == 0:
                    return (u + deltas[k]) & 0xFFFF
                a = ro_at + 2 * k + ros[k] + 2 * (u - starts[k])
                g = _s.unpack(">H", data[a:a + 2])[0]
                return (g + deltas[k]) & 0xFFFF if g else 0
        return 0
    ng = _s.unpack(">H", data[tab["maxp"][0] + 4:tab["maxp"][0] + 6])[0] if "maxp" in tab else 0
    lfmt = _s.unpack(">h", data[h + 50:h + 52])[0]

    def glyph_box(g):
        if "loca" not in tab or "glyf" not in tab or not (0 <= g < ng):
            return None
        lo = tab["loca"][0]
        if lfmt == 0:
            a, b = (2 * v for v in _s.unpack(">HH", data[lo + 2 * g:lo + 2 * g + 4]))
        else:
            a, b = _s.unpack(">II", data[lo + 4 * g:lo + 4 * g + 8])
        if b <= a:
            return None
        o = tab["glyf"][0] + a
        return _s.unpack(">hhhh", data[o + 2:o + 10])
    return dict(tab=tab, upm=upm, bbox=bbox, asc=asc, desc=desc, adv=adv, nhm=nhm, gid=gid, glyph_box=glyph_box)


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
    import struct as _s
    T = _pf_tables(data)
    tab, upm, bbox, asc, desc, adv, nhm, gid = (T[k] for k in ("tab", "upm", "bbox", "asc", "desc", "adv", "nhm",
                                                               "gid"))
    inv = dict((v, k) for k, v in _PF_EXTRA.items())
    widths = []
    for code in range(32, 256):
        try:
            ch = inv.get(code) or bytes([code]).decode("cp1252")
        except Exception:
            ch = None
        g = gid(ord(ch)) if ch else 0
        widths.append(int(round(adv[min(g, nhm - 1)] * 1000.0 / upm)) if g else 0)
    cap, ital, weight = 0.716 * upm, 0.0, 400
    if "OS/2" in tab:
        o = tab["OS/2"][0]
        weight = _s.unpack(">H", data[o + 4:o + 6])[0]
        if _s.unpack(">H", data[o:o + 2])[0] >= 2:
            cap = _s.unpack(">h", data[o + 88:o + 90])[0]
    if "post" in tab:
        o = tab["post"][0]
        ital = _s.unpack(">i", data[o + 4:o + 8])[0] / 65536.0
    k = 1000.0 / upm
    return dict(widths=widths, bbox=[int(round(v * k)) for v in bbox], asc=int(round(asc * k)),
                desc=int(round(desc * k)), cap=int(round(cap * k)), ital=ital, bold=weight >= 600)


def _pf_style(st):
    """(compressed font file, its length, metrics, PostScript name) of one style, or None: read once per run"""
    if st not in _PF_CACHE:
        fn, ps, _std = _PF_FILES[st]
        p, got = _pf_path(fn), None
        if p:
            try:
                import zlib as _z
                with open(p, "rb") as fh:
                    raw = fh.read()
                got = (_z.compress(raw, 6), len(raw), _pf_metrics(raw), ps)
            except Exception as e:
                PDF_FONT_NOTE.append("font %s not read (%s): standard font used" % (fn, e))
        else:
            PDF_FONT_NOTE.append("font %s not found: standard font %s used (Turkish letters may not show)" % (fn, _std))
        _PF_CACHE[st] = got
    return _PF_CACHE[st]


def pdf_fonts(add, styles, content=None):
    """Font objects for a PDF writer: styles = one of "R", "B", "I", "BI" per font slot /F1, /F2 ... in order (a slot
    may repeat a style: the same objects are used). add(bytes) -> object number, as the writers' own add().
    content: the page content (str or bytes); when given, a slot it never uses gets the light standard-font object
    instead of an embedded file. Returns the object numbers, one per slot."""
    if isinstance(content, bytes):
        content = content.decode("latin-1")
    made, out = {}, []
    for i, st in enumerate(styles):
        used = content is None or ("/F%d " % (i + 1)) in content
        key = st if used else "std-" + st
        if key not in made:
            got = _pf_style(st) if used else None
            if got is None:
                made[key] = add(("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding << /Type /Encoding "
                                 "/BaseEncoding /WinAnsiEncoding %s >> >>" % (_PF_FILES[st][2], _PF_DIFF)).encode("latin-1"))
            else:
                data, n, m, ps = got
                ff = add(("<< /Length %d /Length1 %d /Filter /FlateDecode >>\nstream\n" % (len(data), n)).encode("latin-1")
                         + data + b"\nendstream")
                flags = 32 + (64 if "I" in st else 0)
                fd = add(("<< /Type /FontDescriptor /FontName /%s /Flags %d /FontBBox [%s] /ItalicAngle %s /Ascent %d "
                          "/Descent %d /CapHeight %d /StemV %d /FontFile2 %d 0 R >>" % (
                              ps, flags, " ".join(str(v) for v in m["bbox"]), ("%.1f" % m["ital"]), m["asc"], m["desc"],
                              m["cap"], 140 if m["bold"] else 80, ff)).encode("latin-1"))
                made[key] = add(("<< /Type /Font /Subtype /TrueType /BaseFont /%s /FirstChar 32 /LastChar 255 "
                                 "/Widths [%s] /FontDescriptor %d 0 R /Encoding << /Type /Encoding /BaseEncoding "
                                 "/WinAnsiEncoding %s >> >>" % (ps, " ".join(str(w) for w in m["widths"]), fd, _PF_DIFF)
                                 ).encode("latin-1"))
        out.append(made[key])
    return out
# ---- font_metrics.py (round 4, S1, 1 Nov 2026; G-R4-1, PLAN §4.1): REAL Arial widths and glyph boxes, one source -----
# Every width and text box in the scripts comes from here (the text placer text_place.py, the markers marker.py).
# It reads the same font files the sheets embed (pdf_fonts.py: arial.ttf / arialbd.ttf from the Windows font folder),
# so what is measured is what prints. A missing font RAISES FontMissing: there is no estimate fallback (CHK1_2 F2.1:
# the old Helvetica tables measured bold Ö as 600/1000 against Arial's 778, "walking hubthe busy hub").
# Needs pdf_fonts.py included before it (_pf_path, _pf_tables, _PF_FILES).
#   fm_load(bold=False, italic=False)          the font's tables (read once per run, cached)
#   fm_width(s, pt, bold=False)                -> mm   advance width of s at pt (no kerning: the sheets' PDF
#                                                      writers place glyphs by advance, so this is what prints)
#   fm_box(s, x, y, pt, bold=False, align="L", angle=0, y_down=True) -> (x0, y0, x1, y1) page mm
#                                              the box of s set with its baseline at (x, y): width = the advance
#                                              (or the ink if wider), height = the real ink of its glyphs (accents of
#                                              İ Ö Ü, the tails of ğ g y inside); angle in degrees, counter-clockwise
#                                              as seen on the page; align L / C / R at (x, y); "MC" = (x, y) is
#                                              the middle of the ink (the shape lists' middle-centre text)
#   fm_ink_box(s, pt, bold=True)               -> (x0, y0, x1, y1) mm, the visible glyph box with the pen at (0, 0)
#                                              on the baseline, y UP (for centring a glyph in a marker)
#   fm_asc_desc(pt, bold=False)                -> (ascender, descender) mm of the font (descender negative)
# Units: pt = font size in points (the em); 1 pt = 25.4 / 72 mm (FM_PT).
FM_PT = 25.4 / 72.0
_FM_CACHE = {}


class FontMissing(RuntimeError):
    pass


def fm_load(bold=False, italic=False):
    """the font tables for one style, read once per run; raises FontMissing when the font file is not there"""
    st = ("B" if bold else "") + ("I" if italic else "") or "R"
    if st not in _FM_CACHE:
        if "_pf_tables" not in globals():
            raise FontMissing("font_metrics needs common/pdf_fonts.py included before it")
        fn = _PF_FILES[st][0]
        p = _pf_path(fn)
        if not p:
            raise FontMissing("font %s not found (Windows font folder or the user's font folder): text cannot be "
                              "measured, so nothing is placed. Install Arial or copy %s there" % (fn, fn))
        with open(p, "rb") as fh:
            T = _pf_tables(fh.read())
        T["adv_c"], T["ink_c"] = {}, {}
        T["file"] = p
        _FM_CACHE[st] = T
    return _FM_CACHE[st]


def _fm_glyph(T, ch):
    """(advance, ink box or None) of one character in font units; raises when the font has no glyph for it"""
    a = T["adv_c"].get(ch)
    if a is None:
        g = T["gid"](ord(ch)) if ord(ch) <= 0xFFFF else 0
        if not g and ch not in u" ":
            raise ValueError(u"the font %s has no glyph for %r (U+%04X): use another character" % (
                T["file"], ch, ord(ch)))
        a = T["adv"][min(g, T["nhm"] - 1)]
        T["adv_c"][ch] = a
        T["ink_c"][ch] = T["glyph_box"](g) if g else None
    return a, T["ink_c"][ch]


def fm_width(s, pt, bold=False, italic=False):
    """advance width of s in mm at pt points"""
    T = fm_load(bold, italic)
    u = 0
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        u += _fm_glyph(T, ch)[0]
    return u * pt * FM_PT / float(T["upm"])


def fm_ink_box(s, pt, bold=True, italic=False):
    """the visible glyph box of s in mm, pen at (0, 0) on the baseline, y up: (x0, y0, x1, y1); an all-blank string
    gives its advance with zero height"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    x, box = 0, None
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        a, b = _fm_glyph(T, ch)
        if b:
            r = (x + b[0], b[1], x + b[2], b[3])
            box = r if box is None else (min(box[0], r[0]), min(box[1], r[1]), max(box[2], r[2]), max(box[3], r[3]))
        x += a
    if box is None:
        return (0.0, 0.0, x * k, 0.0)
    return (box[0] * k, box[1] * k, box[2] * k, box[3] * k)


def fm_asc_desc(pt, bold=False, italic=False):
    """the font's ascender and descender (hhea) in mm at pt; descender is negative"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    return T["asc"] * k, T["desc"] * k


def fm_box(s, x, y, pt, bold=False, align="L", angle=0.0, y_down=True, italic=False):
    """the page box (x0, y0, x1, y1) of s with its baseline at (x, y); see the module notes"""
    import math as _m
    w = fm_width(s, pt, bold, italic)
    ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold, italic)
    a0, a1 = min(0.0, ix0), max(w, ix1)
    dx = {"L": 0.0, "C": -w / 2.0, "R": -w}.get(str(align or "L")[:1].upper(), 0.0)
    dv = 0.0
    if str(align or "").upper() in ("MC", "CM"):          # middle centre: (x, y) is the middle of the ink
        dx, dv = -w / 2.0, -(iy0 + iy1) / 2.0
    # corners in text space (along the baseline u, up from it v), then onto the page
    corners = [(a0 + dx, iy0 + dv), (a1 + dx, iy0 + dv), (a1 + dx, iy1 + dv), (a0 + dx, iy1 + dv)]
    t = _m.radians(angle or 0.0)
    c, s_ = _m.cos(t), _m.sin(t)
    sg = -1.0 if y_down else 1.0          # page y of "up"
    P = [(x + u * c - v * s_, y + sg * (u * s_ + v * c)) for u, v in corners]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops, self.alphas = w, h, [], set()
        self.tp, self.tg = None, None    # v9 (G-R4-1): the open TextPage (one per booklet crop) and the text group
    def tgroup(self, start=True):
        """v9: start (or with False end) one text group: the lines of one word block may touch each other, never
        another text (TextPage pad)"""
        self.tg = ((self.tp._group() if self.tp is not None else "g") if start else None)
        return self.tg
    def keep(self, box, name, kind="drawing"):
        """v9: a drawing box (x0, y0, x1, y1, page mm y up) no text may touch, in the open TextPage"""
        if self.tp is not None:
            self.tp.keep(tuple(box), kind, name)
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None, alpha=None):
        self.path([P], fill, stroke, lw, closed, dash, alpha)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, alpha=None):
        """several rings in one path; a fill uses even-odd, so holes stay open. v1.5: alpha = opacity 0-1 (sketch washes)"""
        k = 72 / 25.4; o = ["q"]
        if alpha is not None and alpha < 0.995:
            a_ = max(1, int(round(alpha * 100))); self.alphas.add(a_); o.append("/GA%d gs" % a_)
        if fill: o.append(self._c(fill))
        if stroke: o.append(self._c(stroke, True)); o.append("%.3f w 1 J 1 j" % (lw * k))
        if dash: o.append("[%.2f %.2f] 0 d" % (dash[0] * k, dash[1] * k))
        for P in rings:
            o.append("%.2f %.2f m" % (P[0][0] * k, P[0][1] * k))
            o += ["%.2f %.2f l" % (x * k, y * k) for x, y in P[1:]]
            if closed: o.append("h")
        o.append("B*" if fill and stroke else ("f*" if fill else "S")); o.append("Q")
        self.ops.append(" ".join(o))
    def line(self, P, col, lw=0.25, dash=None): self.path([P], None, col, lw, False, dash)
    def circle(self, x, y, r, fill=None, stroke=None, lw=0.2):          # v1.2: for the pictograms
        self.poly([(x + r * math.cos(k * math.pi / 12), y + r * math.sin(k * math.pi / 12)) for k in range(24)], fill, stroke, lw, True)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", halo=None, allow=()):
        """one text, size in pt; v9: measured with the real Arial (text_w = fm_width) and, while a booklet crop's
        TextPage is open, registered in it (collisions raise at its check; allow = keep names / kinds it may sit on);
        ² / ³ are the font's own glyphs"""
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        if self.tp is not None and s.strip():
            self.tp.put(s, x, y, size, bold, "L", 0.0, group=self.tg, emit=False, allow=allow)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        if halo:                                   # v1.5: the sketches' text mask, a halo in the ground's colour
            self.ops.append("q %s %.2f w 1 j BT 2 Tr /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET Q" % (
                self._c(halo, True), size * 0.35, "F2" if bold else "F1", size, self._c(halo), x * k, y * k, b.decode("latin-1")))
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        """v9: wrapped by the no-widow wrap (G-R4-2), one text group (its lines may touch each other)"""
        g0 = self.tg
        self.tgroup()
        yy = y
        for ln in wrap(s, size, w, bold):
            self.text(ln, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        self.tg = g0
        return yy

def write_pdf(pages, path):
    k = 72 / 25.4
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (5 + 2 * i) for i in range(n)), n),
            "", ""]
    extra, first = [], 5 + 2 * n                          # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py):

    def add(b):                                           # font file + descriptor go after the pages
        extra.append(b.decode("latin-1"))
        return first + len(extra) - 1
    fid = pdf_fonts(add, ("R", "B"))
    objs[2], objs[3] = extra[fid[0] - first], extra[fid[1] - first]   # the font dicts themselves stay objects 3, 4
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        gs = "".join("/GA%d << /Type /ExtGState /ca %.2f /CA %.2f >> " % (a, a / 100.0, a / 100.0) for a in sorted(pg.alphas))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >>%s >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, (" /ExtGState << %s>>" % gs) if gs else "", 6 + 2 * i)).encode("latin-1")
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % (6 + 2 * i, len(content))).encode("latin-1") + content + b"\nendstream\nendobj\n"
    for j, o in enumerate(extra):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (first + j, o)).encode("latin-1")
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama agriculture alternatives) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
    with open(path, "wb") as f: f.write(out)

# ------------------------------------------------------------------ shared helpers
def fmt(v): return "{:,.0f}".format(v)
def fmt1(v): return "{:,.1f}".format(v)
def rnd(v, step=1000): return int(round(v / step) * step)
EFF = 0.90          # drip application efficiency, as the water balance (key figures "basis": "drip 90 %")

NET = {}            # net irrigation mm per crop from the water balance results (mean, dry5 = 1-in-5 dry year), set in build()

def gross_m3_ha(crop, year):
    if crop == "mix":                  # field crops weighted by their 2025 Bergama areas
        w = {c: TUIK_2025_DA[c] for c in ("cotton", "maize", "tomato") if c in NET}
        return sum(gross_m3_ha(c, year) * v for c, v in w.items()) / sum(w.values())
    return NET[crop]["mean" if year == "normal" else "dry5"] / EFF * 10.0     # 1 mm on 1 ha = 10 m3

SRC_KEY = []          # v1.6: sources printed as [n] on pages 1-3, numbered once for the sheet; the key is page 4
LOG_NOTES = []        # v1.6: what the layout left out (log)

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in the sheet's key (v1.6: page 4), as "[n]".
    v4 (MIRAQUA 28 Oct, F5): "" for a source that is not public online (F5_OFF): no mark, not in the key.
    v5 (T4a, D13): also "" for a source naming our own model run or method (F5_INTERNAL); status words cut (F5_STATUS)."""
    if not src or src in F5_OFF or any(t in src for t in F5_INTERNAL):
        return ""
    src = F5_STATUS.sub("", src).strip()
    if src not in SRC_KEY: SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)


def cited(s, *srcs):
    """v4 (F5): s with its [n] marks after one space, or s alone when none of its sources is public"""
    mk = "".join(cite(q) for q in srcs if q)
    return s + (" " + mk if mk else "")

def wrap(s, size, w, bold=False):
    """greedy wrap at real widths (size pt, w mm); v9 (G-R4-2): never a one-word last line: the last word of the
    line before moves down while that line keeps two words or more and the last line still fits"""
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    while len(out) >= 2 and len(out[-1].split()) < 2 and len(out[-2].split()) >= 3:
        a = out[-2].split()
        t = a[-1] + " " + out[-1]
        if text_w(t, size, bold) > w:
            break
        out[-2], out[-1] = " ".join(a[:-1]), t
    return out

# ------------------------------------------------------------------ v2 (Aras 27 Oct, Prompt 5): plant and crop photos
# The photos and the "English (Turkish)" names come from src/common/plant_photos.py (one cache folder for every script,
# every photo PHOTO_W x PHOTO_H mm). This PDF writer draws only the frame (thin, faint; "no photo" inside when there is
# none); the JPEGs go into the frames after write_pdf (put_photos, PyMuPDF). Each photo's credit is a [n] mark after its
# name, its key on the sources page.
PH_GAP = 2.0                         # mm between two photos side by side
PHOTO_GOT = {}                       # key -> (jpeg path or None, credit or None, why not), read once a press
PHOTO_LOG, PHOTO_STATE = [], {}      # plant_photos' own notes (web fetch) and its offline flag
PHOTO_FR = []                        # frames with a photo: (page index, x0, y0, x1, y1 mm y up, jpeg path)
PHOTO_N = [0]                        # frames drawn, with or without a photo


def photo_get(key):
    """v2: (jpeg path or None, credit or None, why not) of a plant in PLANTS, once a press; never raises"""
    if key not in PHOTO_GOT:
        try:
            PHOTO_GOT[key] = plant_photo_of(key, PHOTO_LOG, PHOTO_STATE)
        except Exception as ex:
            PHOTO_GOT[key] = (None, None, "%s: %s" % (type(ex).__name__, ex))
    return PHOTO_GOT[key]


def photo_mark(key):
    """v2: the [n] of a plant photo's credit (its key on the sources page); "" when there is no photo"""
    p, credit, _ = photo_get(key)
    return cite(credit) if p and credit else ""


def photo_frame(pg, pi, key, x, top, boxes=None):
    """v2: the frame of a plant's photo, PHOTO_W x PHOTO_H mm, its top-left at (x, top) on page index pi: the photo
    recorded for put_photos, or "no photo" inside the frame. boxes: the frame is added (overlap test).
    v4 (MIRAQUA 28 Oct, G12): an empty frame says why, as the water board's cards: "no photo: " + the loader's reason
    (common/plant_photos.py: offline, Wikimedia refused (HTTP 429) press again later, file not found, licence ...),
    7 pt (the booklet's smallest), top left in the frame. v8 (G17): no outline; an empty frame is a pale fill."""
    p, _cr, why = photo_get(key)
    PHOTO_N[0] += 1
    if p:
        PHOTO_FR.append((pi, x, top - PHOTO_H, x + PHOTO_W, top, p))
    else:
        pg.rect(x, top - PHOTO_H, PHOTO_W, PHOTO_H, fill=C["paper"])
        pg.para(u"no photo: " + (why or u"not loaded"), x + 1.5, top - 4.0, PHOTO_W - 3.0, 7, C["ink2"], lead=1.2)
    if boxes is not None and p:                  # an empty frame carries its own words: no drawing box then
        boxes.append((x, top - PHOTO_H, x + PHOTO_W, top))
    if p:                                        # v9 (G-R4-1): no text on a photo
        pg.keep((x, top - PHOTO_H, x + PHOTO_W, top), "photo " + key, "photo")


def name_lines(key, mark, size, w, bold=True):
    """v2: a plant's name under its photo: "English (Turkish) [n]" on one line when it fits in w, else the English name
    and "(Turkish) [n]" on two (each wrapped to w if it is longer still)"""
    t = plant_name(key) + ((" " + mark) if mark else "")
    if text_w(t, size, bold) <= w:
        return [t]
    en, _, tr = plant_name(key).partition(" (")
    if not tr:
        return wrap(t, size, w, bold)
    return wrap(en, size, w, bold) + wrap("(" + tr + ((" " + mark) if mark else ""), size, w, bold)


def name_lc(key):
    """v2: a plant's name in running text: "olive (Zeytin)" """
    s = plant_name(key)
    return s[:1].lower() + s[1:]


def name_caps(key):
    """v2: a plant's name in a capitals heading, the Turkish part with the dotted İ: "OLIVE (ZEYTİN)" """
    en, _, tr = plant_name(key).partition(" (")
    return en.upper() + ((" (" + tr.replace(u"i", u"İ").upper()) if tr else "")


def crop_word(key):
    """v4 (MIRAQUA 28 Oct, G11): a crop key as a short printed word, the English name of the shared table: "maize" ->
    "corn", "cotton" -> "cotton"; a key the table does not have stays as it is"""
    return plant_name(key).partition(" (")[0].lower() if key in PLANTS else key


def put_photos(path):
    """v2: the plant and crop photos into their frames on pages 1 and 3 (PyMuPDF, after write_pdf and put_base); a photo
    error never stops the sheet. Returns the log lines: how many were placed, and why each missing one is missing."""
    n, err = 0, ""
    try:
        if PHOTO_FR:
            n = fitz_add_photos(path, PHOTO_FR)
    except Exception as ex:
        err = " · FLAG not placed: %s: %s" % (type(ex).__name__, ex)
    if not err and n < len(PHOTO_FR):
        err = " · %d JPEG(s) could not be read" % (len(PHOTO_FR) - n)
    # v8 (P18.2, DATA-2): plant_photos.py's line "photos: n of m placed as images" (+ FLAG k missing); the booklet's
    # crop copy keeps plain images (A2), the photos went missing on p19 while they sat in Form XObjects
    out = ["%s · %d frame(s) drawn (cached/plant_photos)%s" % (photo_flag_line(), PHOTO_N[0], err)]
    out += ["  no photo: %s (%s)" % (plant_name(k), v[2] or "not loaded") for k, v in PHOTO_GOT.items() if not v[0]]
    out += ["  " + t for t in PHOTO_LOG]
    return "\n".join(out)

STAGE_TAG = u"C  WATER  ·  WHAT WE DO WITH IT"   # v3 (Prompt 6, rule 7): the booklet's theme and stage of pages 1 and 3


HEAD_Y = (285.0, 276.5, 269.5)       # v4 (MIRAQUA 28 Oct, P19.1): baselines of the kicker, the title and the subtitle


def header(pg, title, sub, hole=None, tag=None):
    """v4 (MIRAQUA 28 Oct, F10 decision 3, default remove; P19.1): the sheet's big page number before the title is
    gone (it read as a booklet page number); the booklet stage tag (pages 1 and 3) is the kicker over the title, top
    left, where the booklet's own pages carry theirs (8 pt, 12 mm from the top edge); title and subtitle on the 14 mm
    margin (were at 26 behind the number). G1: no "AGRICULTURE ANALYSIS · GROUP 6" line (page 2 had it)."""
    if hole:                                       # v1.5: a window left open for a plan placed under the page
        x0, y0, x1, y1 = hole
        pg.path([[(0, 0), (420, 0), (420, 297), (0, 297)], [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill=C["white"])
    else:                                          # v1.6 (Aras 27 Oct): white, the beige paper goes
        pg.rect(0, 0, 420, 297, fill=C["white"])
    if tag:                                        # v3: pages 1 and 3 name their booklet stage (accent, as its kicker)
        pg.text(tag, 14, HEAD_Y[0], 8, C["accent"], True)
    pg.text(title, 14, HEAD_Y[1], 22, C["ink"], True)
    pg.text(sub, 14, HEAD_Y[2], 11, C["ink2"])

# ------------------------------------------------------------------ pictograms and tiles
# v5 (T4a, 29 Oct, 02 §2): every pictogram comes from the shared icon set (common/icons.py); the script's own icon()
# with its 10 x 10 grid drawings is gone. AG_ICONS: tile key -> (icons.py name, crossed out).
AG_ICONS = {"nowater": ("drought", False), "cotton": ("field", False), "olive": ("olive", False),
            "drip": ("drip", False)}


def _ag_put(pg, shapes):
    """icons.py / marker.py house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) / ("text", s, x,
    baseline y, size mm, colour, bold, align), page mm y up, on this Page (v9: text for the markers' glyphs)"""
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly(sh[1], fill=sh[2], stroke=sh[3], lw=sh[4] or 0.2, closed=True)
        elif sh[0] == "text":
            pg.text(sh[1], sh[2], sh[3], sh[4] / 0.3528, sh[5], sh[6] if len(sh) > 6 else False,
                    sh[7] if len(sh) > 7 else "L")
        else:
            pg.line(sh[1], sh[2], sh[3])


def _ag_icon(pg, kind, x, y, sz):
    """the icon set's pictogram for a tile key in the square (x, y - sz)-(x + sz, y)"""
    name, crossed = AG_ICONS.get(kind, (kind, False))
    _ag_put(pg, ico_draw(name, x + sz / 2.0, y - sz / 2.0, sz))
    if crossed:
        _ag_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))

def tiles(pg, x, y, w, items, cols=1, s=1.0, boxes=None):
    """v1.2 (water board v1.6): facts as tiles: pictogram, keyword heading, the key figure large, short keyword lines and
    the source number. items = [(pictogram, heading, figure or None, [keyword lines], source or None)]. Returns the bottom y.
    v8 (G17): no frame and no fill: the tiles stand apart by whitespace on the grid; boxes gets each pictogram's square."""
    k = 0.3528
    fh, fb, ft = 8.5 * s, 15.0 * s, 7.0 * s
    ic, pad, g = 12.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, lines, ref in items:
        lines = list(lines or [])
        if ref: lines = lines[:-1] + [((lines[-1] + " ") if lines else "") + cite(ref)]
        L3 = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [], [q for ln in lines for q in wrap(ln, ft, txw)])
        hh = pad * 2 + (len(L3[0]) * fh * 1.25 + len(L3[1]) * fb * 1.15 + len(L3[2]) * ft * 1.3 + (fh * 0.3 if L3[1] else 0)) * k
        lay.append((kind, big, L3, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[3] for t in row)
        for c_, (kind, big, L3, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            _ag_icon(pg, kind, tx + pad, yy - pad, ic)
            if boxes is not None:
                boxes.append((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad))
            pg.keep((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad), "tile icon " + kind, "icon")   # v9
            pg.tgroup()                              # v9 (G-R4-1): the tile's lines are one word block
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L3[0]:
                ly -= fh * 1.25 * k; pg.text(ln, lx, ly + fh * 0.25 * k, fh, C["ink"], True)
            if L3[1]: ly -= fh * 0.3 * k
            for ln in L3[1]:
                ly -= fb * 1.15 * k
                pg.text(ln, lx, ly + fb * 0.2 * k, fb, C["accent"] if big in FLAGGED else C["green_deep"], True)
            for ln in L3[2]:
                ly -= ft * 1.3 * k; pg.text(ln, lx, ly + ft * 0.3 * k, ft, C["ink"])
            pg.tgroup(False)
        yy -= rh + g
    return yy + g

FLAGGED = ("NOT KNOWN", "not designed")         # big figures that say "no data": in the accent colour

def north(pg, x, y, ang_deg, r=7.0):
    a = math.radians(ang_deg)
    ux, uy = -math.sin(a), math.cos(a)
    px, py = -uy, ux
    tip = (x + ux * r, y + uy * r); bl = (x - ux * r * 0.6 + px * r * 0.45, y - uy * r * 0.6 + py * r * 0.45)
    br = (x - ux * r * 0.6 - px * r * 0.45, y - uy * r * 0.6 - py * r * 0.45)
    pg.poly([tip, bl, (x, y), br], fill=C["ink"], closed=True)
    pg.text("N", tip[0] + ux * 3.0, tip[1] + uy * 3.0 - 1.2, 8, C["ink"], True, "C")

# ------------------------------------------------------------------ page 1: what each cubic metre grows
# v4 (MIRAQUA 28 Oct, F5: public online sources only): the public sources keep their words, the project's own file
# pointers go from the printed key (kept here: NEWS research/water_data/03 §3; TUIK library/research/crops_2026-10-24
# §1.24-1.25; NET_REF research/water_balance/tables/C1). G11: corn, not maize, where printed (data keys stay "maize").
NEWS = "news: Ajans Bakırçay 19.03.2025"
TUIK = "TÜİK Bitkisel Üretim, Bergama 2025"
KAYA = "Kaya et al. 2017, Irrig. Drain. 66(5):820-827, Tables II, III, VI, pp.823-826 (deficit saving: Table II, S0.50 and S0.25 vs control)"
ITB = "İzmir Ticaret Borsası cotton report 2025, p.5"
NET_REF = ("net irrigation: FAO-56 (Allen et al. 1998), MGM/WMO 17742 normals, ERA5 1991-2025 scaled; per ha = FAO-56 "
           "daily soil balance net need (34 water years, Bergama climate) / 0.90 drip")
TAGEM = ("TAGEM/DSİ 2017 §12, Bergama station 17742 tables (net = ETc - 0.8 rain): cotton 829 mm, corn 765, "
         "tomato 606-825, olive 502-603")   # v5 (D13): was our check against our own figures
# v1.2: the context sentences as tiles (pictogram, heading, big figure, keyword lines, source)
# v2 (Aras 27 Oct, Prompt 5): the crops they name as "English (Turkish)"; figures and sources as they were
CONTEXT = [
    ("nowater", "DROUGHT 2025: NO WATER-HUNGRY CROPS", "7,500 ha",
     ["%s, %s, fodder · Bergama villages" % (name_lc("maize"), name_lc("cotton")),
      "no water for second crops · DSİ + Ministry"], NEWS),
    ("cotton", name_caps("cotton") + ": BERGAMA'S BIGGEST CROP", "37 %",
     ["of 26,800 ha field crops · 2025"], TUIK),
    ("olive", name_caps("olive") + " CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
]
DEFICIT = (1 - 350.0 / 622, 1 - 175.0 / 622)   # olive water saved: S0.50 and S0.25 against the control SC, Kaya et al. 2017 Table II
# Bergama district areas 2025, da (TÜİK MEDAS export, library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §1.25):
# the share of each crop the water balance models, used for the district mix row
TUIK_2025_DA = dict(cotton=99963, maize=24532 + 35491, tomato=13740 + 11268, olive=65978 + 21068)

COTTON_H = ("h01 §3 'Then vs now', cotton / textiles: \"Tersane cotton (16th c.); ginning 1861; Sümerbank (1954/60–2008)\" "
            "(s18, s106; library/research/selinos_bergama_history_context_v1.md line 111)")
OLIVE_H = ("h01 §2 + §5 P04: \"19th-c. olive-oil machinery in the Red Hall S rotunda\" (s25; "
           "selinos_bergama_history_context_v1.md lines 77, 139)")
# v1.6 (Aras 27 Oct, p24 + spec §3): the farm history behind the farms the water serves, as a timeline, in the
# card's own words and years (h01 §3 line 111, §2 line 77, §5 P04 line 139); today's areas from TÜİK 2025 (above)
HISTORY = [("cotton", "Tersane cotton (16th c.)", 1500, 1600, COTTON_H),
           ("cotton", "ginning 1861", 1861, None, COTTON_H),
           ("cotton", "Sümerbank (1954/60–2008)", 1954, 2008, COTTON_H),
           ("olive", u"19th-c. olive-oil machinery · %s S rotunda" % landmark_name("kizil_avlu"), 1800, 1900, OLIVE_H)]
# v9 (round 4, G-R4-11): the landmark's Turkish name from the shared names table (was "Red Hall"); OLIVE_H keeps the
# card's own words (a record, never printed: F5_OFF)


def history_line(pg, x, top, w, h):
    """a timeline 1500-2030 with the cotton (above) and olive (below) history, labels placed by measured width (no
    overlaps), inside the box x..x + w, top..top - h. v8 (round 3, G3): no leader lines (a label that takes a higher
    lane stands there alone, in its line's colour). v9 (round 4, P19.1): booklet p19 group 5's first block (crop
    ag1_history, AG_HIST_W x AG_HIST_H): the group's heading in the band on top, the line "Bergama's cotton and olive"
    under it, the timeline AG_HIST_YA under the top (cotton labels one lane above it, olive labels under the years);
    its old title "WHY THE STORED WATER GOES TO FARMS" is the group heading's job now. Returns its bottom y."""
    P = Placer()
    ag_heading(pg, "THE CROPS, THEN AND NOW", x, top)
    P.text(pg, "Bergama's %s and %s" % (name_lc("cotton"), name_lc("olive")), x, top - 9.0, 7, C["ink"])   # v2
    ya = top - AG_HIST_YA
    X = lambda yr: x + 2.0 + (w - 4.0) * (yr - 1500) / 530.0
    pg.line([(X(1500), ya), (X(2030), ya)], C["ink"], 0.3)
    for yr in range(1500, 2001, 100):
        pg.line([(X(yr), ya - 0.8), (X(yr), ya + 0.8)], C["ink"], 0.3)
        P.text(pg, str(yr), X(yr) - text_w(str(yr), 7) / 2.0, ya - 3.4, 7, C["ink2"])
    reg = (x, top - h + 0.5, x + w, top - 10.4)
    for lane, lab, a, b, ref in HISTORY:
        col, up = (C["accent"], True) if lane == "cotton" else (C["green_deep"], False)
        yb = ya + (1.0 if up else -1.0)
        if b:
            if lab.startswith("Sümerbank"):           # 1954 vs 1960 (card: conflicting dates): dashed until 1960
                pg.line([(X(1954), yb), (X(1960), yb)], col, 1.0, (0.6, 0.4))
                pg.line([(X(1960), yb), (X(2008), yb)], col, 1.0)
            else:
                pg.line([(X(a), yb), (X(b), yb)], col, 1.0)
        else:
            pg.circle(X(a), yb, 0.8, fill=col)
        if P.put(pg, cited(lab, ref), X((a + b) / 2.0 if b else a), yb + (0.6 if up else -0.6), 7, col, False, region=reg,
                 gap=1.2, up=up, lanes=3, leader=False) is None:
            raise TextError(u"p19 ag1_history: the label %r finds no free place on the timeline (shorten it)" % lab)
    return top - h


CROP_ROW = ("olive", "cotton", "maize", "tomato")   # v2 (Aras 27 Oct, Prompt 5): the crops page 1 compares


def crop_row(pg, x, top, w, boxes=None):
    """v2 (Aras 27 Oct, Prompt 5): "THE CROPS": page 1's crops as photos in one row (PHOTO_W x PHOTO_H each, the one
    photo size of the booklet, spread over w), the name "English (Turkish)" and the photo's credit [n] under each.
    v9 (round 4, P19.1): booklet p19 group 5's second block (crop ag1_crops, AG_CROPS_W x AG_CROPS_H) beside the
    timeline, which carries the group's heading: its heading band stays empty, the photos start on the shared content
    top AG_HEAD under the top; a name of two lines is one text group; the photos are keeps. boxes: the photo frames.
    Returns its bottom y."""
    n = len(CROP_ROW)
    gx = max(PH_GAP, (w - n * PHOTO_W) / (n - 1.0))
    pt = top - AG_HEAD
    low = pt - PHOTO_H
    for i, key in enumerate(CROP_ROW):
        px = x + i * (PHOTO_W + gx)
        photo_frame(pg, 0, key, px, pt, boxes)
        yy = pt - PHOTO_H - 2.6
        nl = name_lines(key, photo_mark(key), 6.5, PHOTO_W + gx - 1.0)
        pg.tgroup()
        for q in nl:
            pg.text(q, px, yy, 6.5, C["ink"], True)
            low = min(low, yy - 0.6); yy -= 2.5
        pg.tgroup(False)
    return low


# ------------------------------------------------------------------ v3 (Prompt 6): the stream comes first
AG_BAR_RP, AG_BAR_H, AG_BAR_O = 9.3, 3.8, 4.4   # v8: bars' largest row pitch, bar, dry bar offset, mm (v7 14, 5, 6)
# v9 (round 4, P19.1; spec revision_2026-11-01_round4/handover/S6b_p19_design_spec.md): booklet p19 is rebuilt as
# story groups, one heading each (GRID_TYPE heading, in a band AG_HEAD tall on top of every block, so the blocks of a
# booklet row share the content top). The crops' sizes, mm, drawn at 1:1 ("bk_w"; page columns in brackets):
#   row 2  ag1_stream 260 x 40 (8)  "HOW MUCH WATER REACHES THE FARMS"  | the water board's wb_decision (4)
#   row 3  ag1_bars   194 x 72 (6)  "HECTARES ONE STORAGE IRRIGATES, BY CROP" | ag1_context 194 x 72 (6) "WHY CROP CHOICE
#          IS THE LEVER": the reading (ag1_reading's squares and ratio, no crop of its own now) on top, the 4 tiles under
#   row 4  ag1_history 260 x 34 (8) "THE CROPS, THEN AND NOW" | ag1_crops 128 x 34 (4), the photos at the one booklet
#          photo size
# Each crop has ONE TextPage (common/text_place.py, real Arial widths): every text of the crop is registered, the
# drawings no text may touch are keeps, and a collision RAISES (log "overlap p19 <crop> checked n, collisions 0").
AG_HEAD = 6.0                        # v9: the group heading band, mm
AG_STREAM_W, AG_STREAM_H = grid_w(8), 40.0
AG_BARS_W, AG_BARS_H = grid_w(6), 72.0
AG_CTX_W, AG_CTX_H = grid_w(6), 72.0
AG_HIST_W, AG_HIST_H = grid_w(8), 34.0
AG_CROPS_W, AG_CROPS_H = grid_w(4), 34.0
AG_HIST_YA = 23.0                    # v9: the timeline's line under the block's top, mm
AG_READ_H = 18.0                     # v9: the reading's strip under the heading band in ag1_context, mm
AG_ST_LW = 76.0                      # ag1_stream: the left column (headline, key), mm
AG_ST_RW = 60.0                      # ag1_stream: room after the bars for the through-the-store lines, mm (v8 57)
AG_DBOX = {}                         # v8 (G3): crop id -> drawing boxes (page mm y up), page 1
PRIORITY =[(1, "stream: summer strip"), (2, "on-site planting, on the strip's water"), (3, "farms outside the site")]
AG_STEP_MM = 4.0                     # the flow-step marker's least size (marker.py), mm


def ag_heading(pg, text, x, top):
    """v9 (P19.1): a story group's ONE heading (GRID_TYPE heading: 10 pt bold, ink) in the block's heading band"""
    sz, _b, _ld, col = grid_style("heading")
    pg.text(text, x, top - 4.0, sz, col, True)


def ag_open(pg, cid, x0, top, W, H):
    """v9 (G-R4-1): the TextPage of booklet crop cid (x0..x0 + W, top - H..top, page mm y up): every text drawn until
    ag_close is registered in it"""
    pg.tp, pg.tg = TextPage(u"p19 " + cid, (x0, top - H, x0 + W, top), y_down=False), None
    AG_DBOX[cid] = AG_DBOX.get(cid, [])


def ag_close(pg, cid, x0, top, W, H):
    """v9: the crop's collision test (RAISES TextCollision on any hit; logs "overlap p19 <cid> checked n, collisions
    0"), then the crop itself (drawn at 1:1 for the booklet page)"""
    tp, pg.tp, pg.tg = pg.tp, None, None
    tp.check(True)
    ag_crop(cid, 0, x0, top - H, x0 + W, top, bk_w=W)


def chip(pg, x, y, n, label, size=7.5):
    """v3: a numbered step, the label after it (baseline y). Returns x after it. v9 (round 4, G-R4-7): the marker is
    the shared marker.py mk_marker (glyph centred on its ink box, 7 pt, at least AG_STEP_MM across, accent)."""
    s = AG_STEP_MM
    sh, _box, r = mk_marker(x + s / 2.0, y + 1.1, str(n), C["accent"], size_pt=7.0, r_min=s / 2.0)
    _ag_put(pg, sh)
    lx = x + s / 2.0 + r + 1.2
    pg.text(label, lx, y, size, C["ink"])
    return lx + text_w(label, size)


def step_arrow(pg, x, y):
    """v3: a small arrow, 4 mm long, at the mid-height of a label on baseline y. Returns x after it."""
    ym = y + 1.1
    pg.line([(x, ym), (x + 3.0, ym)], C["ink2"], 0.3)
    pg.poly([(x + 2.9, ym + 0.8), (x + 4.0, ym), (x + 2.9, ym - 0.8)], fill=C["ink2"], closed=True)
    return x + 4.0


def chips(pg, x, y, steps, size=7.5):
    """v3: numbered steps in one row, an arrow between two, from x on baseline y"""
    for i, (n, lab) in enumerate(steps):
        if i: x = step_arrow(pg, x + 1.5, y) + 1.5
        x = chip(pg, x, y, n, lab, size)
    return x


def squeeze(ys):
    """v3: the double squeeze, dry year against normal, from the water balance's year_split (one daily run of the
    design store): water left for the farms after the strip (carried in + filled - strip), the farms' need per hectare
    (the same fields both years, so their need) and the hectares that water serves = left / need per ha. Fractions."""
    n, d = ys["normal"], ys["dry5"]
    left = lambda q: q["carried_in_m3"] + q["filled_m3"] - q["strip_m3"]
    a = left(d) / max(left(n), 1.0) - 1.0
    b = d["farm_need_m3"] / max(n["farm_need_m3"], 1.0) - 1.0
    return a, b, (1.0 + a) / (1.0 + b) - 1.0


def pc(v):
    """v3: a change as a signed whole percent, "+11 %", "-2 %", "0 %" """
    return "0 %" if abs(v) < 0.005 else "%+.0f %%" % (100.0 * v)


def ag_stream_block(pg, L, src, x0, top, hl):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 1: "the board sends LESS water to farms in a 1-in-5 dry year than storage
    holds ... show the defence ON the board"): the priority as numbered steps; the design store through a normal and the
    1-in-5 dry water year, two stacked bars on one scale: strip (it also waters the bed planting: the model has no draw
    of its own for it), farms (light normal, deep dry, as the hectare bars), left over (carried on, or back to the
    stream after 365 days), the store size dashed across both; then the double squeeze. All from the water balance
    results (design.year_split); without them only the priority row.
    v8 (round 3, was stream_first; the merged booklet page): crop ag1_stream, AG_STREAM_W x AG_STREAM_H at 1:1 from
    (x0, top): the left column (AG_ST_LW) holds the title, the to-farms headline hl = (value, line) (was its own crop
    ag1_headline) and the bars' key; the right column the steps, the two bars and the squeeze.
    v9 (round 4, P19.1): booklet p19 group 2's first block: the group heading "HOW MUCH WATER REACHES THE FARMS"
    (was the title "THE STREAM COMES FIRST") on the steps' line; one TextPage for the crop (ag_open / ag_close: a
    collision raises); the outside values never run under the row labels or into the through-the-store lines."""
    W, H = AG_STREAM_W, AG_STREAM_H
    xl, xr = x0, x0 + AG_ST_LW + 5.0
    ag_open(pg, "ag1_stream", x0, top, W, H)
    ag_heading(pg, "HOW MUCH WATER REACHES THE FARMS", xl, top)
    pg.text(hl[0], xl, top - 11.5, 16, C["green_deep"], True)
    yk = top - 16.0
    pg.tgroup()                                    # the headline's line(s): one word block
    for ln in wrap(hl[1], 7.5, AG_ST_LW):
        pg.text(ln, xl, yk, 7.5, C["ink"])
        yk -= 3.3
    pg.tgroup(False)
    chips(pg, xr, top - 4.0, PRIORITY)
    ys = L.get("year_split")
    if not (ys and "normal" in ys and "dry5" in ys):
        LOG_NOTES.append("FLAG p1: the water balance results have no year_split (water balance v4 has not run): the "
                         "normal and dry-year bars and the squeeze line are left out")
        ag_close(pg, "ag1_stream", x0, top, W, H)
        return
    mix = L.get("design_mix") or "design mix"
    mix_t = " + ".join(name_lc(w.split()[-1]) if w.split() and w.split()[-1] in PLANTS else w for w in mix.split(" + "))
    SRC_Y = ("normal and 1-in-5 dry year: " + src + "; design store, " + mix_t + "; one daily run of the store over 34 "
             "water years: normal = the year of median farm need, dry = the 1-in-5 dry year of farm need; carried in + "
             "filled = strip + farms + left over; left for farms = carried in + filled - strip; hectares = left for farms "
             "/ need per hectare (calculated)")
    mk = cite(SRC_Y)
    V = float(ys.get("storage_m3") or 0.0)
    YRS = (("normal", "normal year", C["green_light"], C["ink"]), ("dry5", "1-in-5 dry year", C["green_deep"], C["white"]))
    tot = dict((k, ys[k]["carried_in_m3"] + ys[k]["filled_m3"]) for k, _, _, _ in YRS)
    xb = xr + 28.0                                 # v8: the bars' origin (their labels right-aligned before it)
    BW = x0 + W - 1.0 - AG_ST_RW - 4.0 - xb        # AG_ST_RW mm for the through-the-store lines after the bars
    BH, BP = 5.0, 9.5                              # v8: bar height, pitch (v3 6, 11)
    kx = BW / max(max(tot.values()), V, 1.0)
    v_t = lambda v: fmt(rnd(v, 1000 if v >= 10000 else 100))
    b1 = top - 10.0                                # the normal bar's top; the dry bar BP under it
    for j, (k, lab, fcol, fink) in enumerate(YRS):
        d = ys[k]
        bt = b1 - BP * j; bot = bt - BH
        segs = [(d["strip_m3"], C["water_deep"], C["white"]), (d["farms_m3"], fcol, fink),
                (max(0.0, tot[k] - d["strip_m3"] - d["farms_m3"]), C["faint"], C["ink"])]
        xs, out_x = xb, -1e9                       # out_x: where the last outside value ended (pushed right past it)
        for v, col, ink in segs:
            w_ = kx * v
            if w_ > 0.05:
                pg.rect(xs, bot, w_, BH, fill=col)
            t = v_t(v)
            if v >= 0.5:                           # v3.1: the block's small words 7 pt, the smallest size (were 6.5)
                tw_ = text_w(t, 7, True)
                if tw_ + 1.6 <= w_:                # inside, centred
                    pg.text(t, xs + w_ / 2.0, bot + 1.6, 7, ink, True, "C")
                else:                              # outside: over the normal bar, under the dry bar; v9: never left
                    # of the bars' origin (the row labels end 3 mm before it) nor into the through-the-store lines
                    tx = max(xs + w_ / 2.0 - tw_ / 2.0, out_x + 1.5, xb)
                    tx = min(tx, xb + BW + 3.0 - tw_)
                    pg.text(t, tx, bt + 0.9 if j == 0 else bot - 2.9, 7, C["ink"], True)
                    out_x = tx + tw_
            xs += w_
        pg.tgroup()                                # v9: the row's label and its water year: one word block
        pg.text(lab, xb - 3.0, bt - 2.2, 8, C["ink"], True, "R")
        pg.text("water year " + d["water_year"], xb - 3.0, bt - 5.3, 7, C["ink2"], align="R")
        pg.tgroup()                                # v9: the two lines after the bars: one word block
        pg.text("%s m³ through the store" % v_t(tot[k]), xb + BW + 4.0, bt - 2.2, 7.5, C["ink"], True)
        pg.text("stream's winter flow: %.0f %% of a median year" % d["winter_flow_pct_of_median"], xb + BW + 4.0,
                bt - 5.3, 7, C["ink2"])
        pg.tgroup(False)
    if V > 0:                                      # the store size, dashed across both bars
        xv = xb + kx * V
        pg.line([(xv, b1 - BP - BH - 0.8), (xv, b1 + 0.8)], C["ink"], 0.35, (1.0, 0.7))
    lg = yk - 1.1                                  # v8: the key in the left column, one row each
    for kind, cols, lab in (("fill", (C["water_deep"],), "strip, also waters the bed planting"),
                            ("fill", (C["green_light"], C["green_deep"]), "farms: normal · dry year"),
                            ("fill", (C["faint"],), "left: carried on, or back to the stream after a year"),
                            ("dash", (C["ink"],), ("store size " + mk).strip())):
        xx = xl
        for c_ in cols:
            if kind == "fill":
                pg.rect(xx, lg - 0.3, 3.5, 2.6, fill=c_); xx += 4.0
            else:
                pg.line([(xx + 1.7, lg - 0.6), (xx + 1.7, lg + 2.6)], c_, 0.35, (1.0, 0.7)); xx += 4.0
        pg.text(lab, xx + 0.8, lg, 7, C["ink"])           # v3.1: 7 pt (was 6.5)
        lg -= 3.6                                         # v9: 3.6 mm rows (was 3.4: the boxes kept 0.6 mm apart)
    a, b, c = squeeze(ys)
    pg.tgroup()                                    # v9: the squeeze and what it means: one word block
    pg.text("1-in-5 dry year vs normal year: left for farms after the strip %s · need per hectare %s · hectares %s %s" % (
        pc(a), pc(b), pc(c), mk), xr, top - 32.0, 7.5, C["accent"], True)
    if b > 0.0 and a <= 0.0:                       # what the run shows, said as it is (the log flags the other cases)
        t2 = "so the hectares fall faster than the volume: why deficit-irrigated %s is the lever" % name_lc("olive")
    elif b > 0.0 and c < 0.0:
        t2 = "the need per hectare outgrows the water left: why deficit-irrigated %s is the lever" % name_lc("olive")
    else:
        t2 = "the hectares hold in this dry year: the store covers it"
    pg.text(t2, xr, top - 35.6, 7.5, C["ink"])
    pg.tgroup(False)
    ag_close(pg, "ag1_stream", x0, top, W, H)
    if a > 0.0 or b <= 0.0:
        LOG_NOTES.append("MODEL p1: the dry year (%s) leaves the farms %s water after the strip and needs %s per hectare: "
                         "the squeeze is %s" % (ys["dry5"]["water_year"], pc(a), pc(b),
                                                "the need per hectare only" if b > 0.0 else "not there this time"))
    n_, d_ = ys["normal"], ys["dry5"]
    LOG_NOTES.append("p1 stream first (%s, store %s m3): normal %s / dry %s: in %s / %s m3 (filled %s / %s), strip %s / %s, "
                     "farms %s / %s of need %s / %s; left for farms %s, need per ha %s, hectares %s; winter flow %.0f / %.0f %% "
                     "of median" % (mix, fmt(V), n_["water_year"], d_["water_year"], fmt(tot["normal"]), fmt(tot["dry5"]),
                                    fmt(n_["filled_m3"]), fmt(d_["filled_m3"]), fmt(n_["strip_m3"]), fmt(d_["strip_m3"]),
                                    fmt(n_["farms_m3"]), fmt(d_["farms_m3"]), fmt(n_["farm_need_m3"]),
                                    fmt(d_["farm_need_m3"]), pc(a), pc(b), pc(c), n_["winter_flow_pct_of_median"],
                                    d_["winter_flow_pct_of_median"]))


def page_cubic(L, src):
    pg = Page(420, 297)
    header(pg, "WHAT EACH CUBIC METRE GROWS",
           "Same storage, different crops: hectares irrigated a season", tag=STAGE_TAG)
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, corn and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in; water balance crops: %s" % (", ".join(crop_word(c) for c in L["crops"]) or "not set"))
    # the to-farms headline (v8: drawn in ag1_stream's left column); T5 (30 Oct, M10): the storage figure is p.10's
    hl = ("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), "to farms · 1-in-5 dry year · %s %% of need · strip first %s" % (
        ("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi), cite(SRC1)))
    # bars: hectares served by W, per crop (v2, Prompt 5: the crop names "English (Turkish)")
    rows = [(plant_name("olive") + ", full irrigation", "olive", None), (plant_name("olive") + ", deficit irrigation", "olive", DEFICIT)] + \
           [(plant_name(c) if c in PLANTS else c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    vals = []
    for lab, crop, d in rows:
        for yr in ("normal", "dry"):
            g = gross_m3_ha(crop, yr)
            if d: lo, hi = w_lo / (g * (1 - d[0])), w_hi / (g * (1 - d[1]))
            else: lo, hi = w_lo / g, w_hi / g
            vals.append((lab, crop, yr, g, lo, hi, d))
    # v9 (round 4, P19.1): the sheet holds the five crops as booklet p19 shows them (rows 2-4 of the page; row 1 and
    # row 2's right block are the water board's), each at its booklet size (1:1, "bk_w"), at their p19 x positions:
    #   row 2  ag1_stream (14, top 262)
    #   row 3  ag1_bars (14, top 216) | ag1_context (212, top 216)
    #   row 4  ag1_history (14, top 138) | ag1_crops (278, top 138)
    AG_DBOX.clear()
    ag_stream_block(pg, L, src, 14.0, 262.0, (hl[0], hl[1].strip()))
    ag_bars_block(pg, 14.0, 216.0, rows, vals, fed, MIX)
    best = [q for q in vals if q[1] == "olive" and q[6] and q[2] == "dry"][0]     # v2: olive with deficit (not by its label)
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    ag_context_block(pg, 14.0 + AG_BARS_W + 4.0, 216.0, best, worst)
    ag_open(pg, "ag1_history", 14.0, 138.0, AG_HIST_W, AG_HIST_H)
    history_line(pg, 14.0, 138.0, AG_HIST_W, AG_HIST_H)       # v1.6: why the stored water goes to farms
    ag_close(pg, "ag1_history", 14.0, 138.0, AG_HIST_W, AG_HIST_H)
    cx = 14.0 + AG_HIST_W + 4.0
    ag_open(pg, "ag1_crops", cx, 138.0, AG_CROPS_W, AG_CROPS_H)
    crop_row(pg, cx, 138.0, AG_CROPS_W, AG_DBOX["ag1_crops"])   # v2 (Prompt 5): the crops as photos
    ag_close(pg, "ag1_crops", cx, 138.0, AG_CROPS_W, AG_CROPS_H)
    return pg


def ag_bars_block(pg, x0, top, rows, vals, fed, MIX):
    """page 1's main chart: hectares the storage irrigates per crop, a light (normal year) and a deep (1-in-5 dry
    year) bar each, the open end = the range (storage span; olive deficit saving 44-72 %), the values at the bar ends,
    "farms we feed" dashed. v8 (round 3, A3_3's bars with direct labels): crop ag1_bars, AG_BARS_W x AG_BARS_H at 1:1
    from (x0, top); no key row: the first row's values say "normal year" / "1-in-5 dry year", the open end is said on
    the top line; each row's name, need and Bergama area right-aligned before its bars.
    v9 (round 4, P19.1): booklet p19 group 3 (6 page columns, AG_BARS_W x AG_BARS_H): the group heading "HECTARES ONE
    STORAGE IRRIGATES, BY CROP" in the band on top, the top line under it; one TextPage (a collision raises); a row's
    three label lines are one word block, a value and its direct label too; the bars are keeps."""
    W, H = AG_BARS_W, AG_BARS_H
    BH, BO = AG_BAR_H, AG_BAR_O
    n = len(rows)
    ag_open(pg, "ag1_bars", x0, top, W, H)
    ag_heading(pg, "HECTARES ONE STORAGE IRRIGATES, BY CROP", x0, top)
    y0 = top - AG_HEAD - 6.0                         # the first row's top; the top line (farms we feed) above it
    RP = min(AG_BAR_RP, (y0 - (top - H + 4.5) - BO - BH) / max(n - 1, 1))
    yb_ = y0 - (n - 1) * RP - BO - BH                # the last row's dry bar bottom (= the grid's foot)
    texts = []                                       # per row: (name, need line, area line or None)
    for i, (lab, crop, d) in enumerate(rows):
        area = fact_num("olive_area_ha") if crop == "olive" else (fmt(TUIK_2025_DA[crop] / 10.0) if crop in TUIK_2025_DA else None)
        area_t = "Bergama 2025: %s ha %s" % (area, cite(TUIK)) if area and not (crop == "olive" and d) else None
        g_n, g_d = gross_m3_ha(crop, "normal"), gross_m3_ha(crop, "dry")
        if d: g_n, g_d = g_n * (1 - d[1]), g_d * (1 - d[0])
        mk = cite(NET_REF) + (cite(TAGEM) if i == 0 else "") + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
        if crop == "olive" and not d:                 # T5 (M10): facts.py; the 1-in-5 dry-year need prints on p.18
            need_t = fact_text("olive_need_normal_m3_ha")
            need_t = "%s %s" % (need_t, mk) if need_t else None
        else:
            need_t = "%s-%s m³ per ha a season %s" % (fmt(rnd(min(g_n, g_d), 10)), fmt(rnd(max(g_n, g_d), 10)), mk)
        texts.append((lab, need_t, area_t))
    lw = max([text_w(t[0], 7.5, True) for t in texts] + [text_w(q, 6.5) for t in texts for q in t[1:] if q])
    xb = x0 + lw + 3.0                               # the bars' origin
    vmax = max(v[5] for v in vals) * 1.08
    DIRECT = {"normal": "  normal year (mean of 34)", "dry": "  1-in-5 dry year"}   # the first row's direct labels

    def vtext(v, first):
        t = "%s-%s ha" % (fmt(v[4]), fmt(v[5])) if fmt(v[4]) != fmt(v[5]) else "%s ha" % fmt(v[4])
        return t, (DIRECT[v[2]] if first else "")
    avail = x0 + W - 1.0 - xb                        # the grid as wide as the longest bar + its words allow
    gw = min((avail - 1.5 - text_w(t, 7.5, True) - text_w(e, 7)) / (v[5] / vmax)
             for v in vals for t, e in [vtext(v, v[0] == rows[0][0])])
    step = 25 if vmax < 160 else (50 if vmax < 400 else 100)
    for t in range(0, int(vmax) + 1, step):
        xx = xb + gw * t / vmax
        pg.line([(xx, yb_), (xx, y0 + 0.5)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, yb_ - 3.5, 7, C["ink2"], align="C")
    xf = xb + gw * fed / vmax
    pg.line([(xf, yb_), (xf, y0 + 2.0)], C["accent"], 0.5, (1.5, 1.0))
    ff = "farms we feed: %s ha" % fmt1(fed)
    pg.text(ff, xf + 1.2, top - AG_HEAD - 3.5, 7.5, C["accent"], True)
    rng = "open bar end: range (storage span; deficit 44-72 % saving)"
    pg.text(rng, x0 + W - 1.0, top - AG_HEAD - 3.5, 7, C["ink2"], align="R")
    boxes = AG_DBOX.setdefault("ag1_bars", [])
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * RP
        name, need_t, area_t = texts[i]
        pg.tgroup()                                  # v9: the row's name, need and area: one word block
        pg.text(name, xb - 3.0, yy - 2.8, 7.5, C["ink"], True, "R")
        if need_t:
            pg.text(need_t, xb - 3.0, yy - 5.5, 6.5, C["ink2"], align="R")
        if area_t:
            pg.text(area_t, xb - 3.0, yy - 8.0, 6.5, C["accent"], align="R")
        pg.tgroup(False)
        for j, yr in enumerate(("normal", "dry")):
            v = [q for q in vals if q[0] == lab and q[2] == yr][0]
            by = yy - j * BO
            col = C["green_light"] if yr == "normal" else C["green_deep"]
            pg.rect(xb, by - BH, gw * v[4] / vmax, BH, fill=col)
            if v[5] > v[4] * 1.01:
                pg.rect(xb + gw * v[4] / vmax, by - BH, gw * (v[5] - v[4]) / vmax, BH, fill=None, stroke=col, lw=0.35)
            boxes.append((xb, by - BH, xb + gw * v[5] / vmax, by))
            pg.keep((xb, by - BH, xb + gw * v[5] / vmax, by), "bar %d %s" % (i, yr))
            t, e = vtext(v, i == 0)
            tx = xb + gw * v[5] / vmax + 1.5
            pg.tgroup()                              # v9: the value and its direct label: one word block
            pg.text(t, tx, by - BH + 0.9, 7.5, C["ink"], True)
            if e:
                pg.text(e, tx + text_w(t, 7.5, True), by - BH + 0.9, 7, C["ink2"])
            pg.tgroup(False)
    ag_close(pg, "ag1_bars", x0, top, W, H)


def ag_context_block(pg, x0, top, best, worst):
    """v9 (round 4, P19.1): booklet p19 group 4 "WHY CROP CHOICE IS THE LEVER" (crop ag1_context, AG_CTX_W x
    AG_CTX_H at 1:1 from (x0, top), 6 page columns, one TextPage): the lever first, then why.
      the reading (v1.2 THE READING; v8 its own crop ag1_reading, now the strip AG_READ_H under the heading band): the
        land one storage irrigates in the 1-in-5 dry year as squares by area: the thirstiest field crop = 1 (deep),
        deficit-irrigated olive = the ratio (deep up to its low end, open up to its high end, as the bars' open ends);
        beside them the ratio with what it compares (one word block), then the lever (one word block)
      the four context tiles 2 x 2 under it (v1.2 tiles at 0.9, no frames; each tile one word block, icons keeps)"""
    W, H = AG_CTX_W, AG_CTX_H
    ag_open(pg, "ag1_context", x0, top, W, H)
    ag_heading(pg, "WHY CROP CHOICE IS THE LEVER", x0, top)
    # the reading
    lo, hi = best[4] / worst[4], best[5] / worst[5]
    rt = "%.1f-%.1f x" % (lo, hi)
    st = top - AG_HEAD                               # the strip's top
    gy = st - AG_READ_H + 0.5                        # the squares stand on one line
    a = min(11.0, (AG_READ_H - 1.5) / math.sqrt(max(hi, 1.0)))   # 1 unit of land (a drawing size, not printed)
    xs = x0
    s_lo, s_hi = a * math.sqrt(max(lo, 0.0)), a * math.sqrt(max(hi, 0.0))
    xo = xs + a + 3.0
    pg.rect(xs, gy, a, a, fill=C["green_deep"])
    pg.rect(xo, gy, s_hi, s_hi, stroke=C["green_deep"], lw=0.35)
    pg.rect(xo, gy, s_lo, s_lo, fill=C["green_deep"])
    pg.keep((xs, gy, xs + a, gy + a), "reading square " + worst[1], "reading")
    pg.keep((xo, gy, xo + max(s_hi, s_lo), gy + max(s_hi, s_lo)), "reading square " + best[1], "reading")
    for cx_, side, key in ((xs, a, worst[1]), (xo, s_lo, best[1])):      # the crop's word in its deep square
        w_ = crop_word(key)
        sz = 6.5 if text_w(w_, 6.5, True) + 1.0 <= side else 6.0
        if text_w(w_, sz, True) + 1.0 <= side:
            pg.text(w_, cx_ + side / 2.0, gy + side / 2.0 - 0.8, sz, C["white"], True, "C", allow=("reading",))
        else:
            LOG_NOTES.append("FLAG p1 ag1_context: '%s' does not fit its %.1f mm square; the line beside the squares "
                             "names both crops" % (w_, side))
    tx = xo + max(s_hi, s_lo) + 5.0
    cwa = 60.0                                       # the ratio's column; the lever's column after it
    wname = plant_name(worst[1]) if worst[1] in PLANTS else worst[1].capitalize()
    pg.tgroup()                                      # the ratio, what it means and what it compares: one word block
    pg.text(rt, tx, st - 6.0, 18, C["accent"], True)
    pg.text("as much land, same storage", tx, st - 9.6, 7, C["ink"])
    yy = st - 12.6
    for ln in wrap("%s against %s, 1-in-5 dry year" % (best[0], wname), 6.5, cwa):
        pg.text(ln, tx, yy, 6.5, C["ink2"])
        yy -= 2.7
    pg.tgroup(False)
    lx = tx + cwa + 4.0
    pg.tgroup()                                      # the lever: one word block
    yy = st - 3.0
    for ln, b in [(q, True) for q in wrap("lever: crop + irrigation method, more than storage", 7, x0 + W - lx, True)] + \
                 [(q, False) for q in wrap("same water: more farmland · same farms: less storage", 7, x0 + W - lx)]:
        pg.text(ln, lx, yy, 7, C["ink"], b)
        yy -= 3.2
    pg.tgroup(False)
    # the four tiles 2 x 2 (v8: tiles at 0.9, no frames)
    AG_DBOX["ag1_context"] = []
    tiles(pg, x0, st - AG_READ_H - 1.5, W, CONTEXT, cols=2, s=0.9, boxes=AG_DBOX["ag1_context"])
    ag_close(pg, "ag1_context", x0, top, W, H)


# ------------------------------------------------------------------ page 2: the farms we feed, on the site board's plan 01
# v1.5 (Aras 26 Oct 07:06, deck p.33): "build this map from the 'What is there' plan (p.02): same base, same palette and
# legend". The base is the site board's own plan 01, cut from its sheet PDF and scaled by one factor (never redrawn,
# never stretched; Aras 25 Oct 22:07); this page draws only the farms layer on it. The board (v42+) writes the plan's
# georeference into output/selinus_board/booklet/blocks.json. Without it (or without PyMuPDF) the page falls back to
# v1.4's land cover drawing in the same window, flagged on the page and in the log.
CLS = [("farmland", "Fields (cropland)", C["field"]), ("orchard", "Orchards", C["orchard"]),
       ("trees", "Tree cover", C["tree"]), ("shrub", "Shrubland", C["shrub"]), ("grass", "Grassland", C["grass"])]
BOARD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "selinus_board")
ROUND_DENS = (5000, 10000, 20000, 25000, 50000)    # Aras 26 Oct 06:35: round scales only, the largest that fits
FARM_WIN = (13.0, 20.0, 373.0, 262.0)              # the map window, page mm (x0, y0, x1, y1), y up
FARM_COL = 377.0                                   # the key column, x from here to 406
BASE = {}                                          # the plan 01 cut put under page 2 after write_pdf (put_base)
BASE_OFF = [False]                                 # True: draw the fallback (the base could not be placed)


def plan01_geo():
    """(plan dict, note) of the site board's plan 01: its sheet PDF, crop rect (mm from the sheet's top-left) and the
    survey -> sheet similarity a * w + b (complex, sheet mm with y up, from the four frame corners); (None, why) when
    it is missing."""
    if BASE_OFF[0]:
        return None, "the site board's plan could not be placed under the farms (see the log)"
    try:
        import fitz                                 # PyMuPDF (the "# r:" line at the top installs it in Rhino 8)
    except Exception:
        return None, "PyMuPDF missing: Rhino installs it from the '# r: pymupdf' line on the first run (needs internet)"
    try:
        with open(bg_first([os.path.join(bg_booklet("selinus_board"), "blocks.json"),        # board v44+
                            os.path.join(BOARD_DIR, "booklet", "blocks.json")]), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None, "site board output not found (cached/booklet/selinus_board/blocks.json): run the site board first"
    blk = next((v for k, v in sorted(d.get("blocks", {}).items()) if k.lower().endswith("_plan01") and v.get("geo")), None)
    if not blk:
        return None, "the site board output has no plan 01 georeference: run the site board v42 or later"
    nm, pdf = os.path.basename(blk.get("pdf", "")), None
    for dd, _, names in sorted(os.walk(BOARD_DIR)):
        if nm in names:
            pdf = os.path.join(dd, nm)
            break
    if not pdf:
        return None, "the site board sheet %s is not in %s" % (nm, BOARD_DIR)
    r = [float(v) for v in blk["rect_mm"]]
    W = [complex(g[0], g[1]) for g in blk["geo"]["points"]]
    Z = [complex(r[0] + g[2], -(r[1] + g[3])) for g in blk["geo"]["points"]]
    wm, zm = sum(W) / len(W), sum(Z) / len(Z)
    a = sum((z - zm) * (w - wm).conjugate() for w, z in zip(W, Z)) / sum(abs(w - wm) ** 2 for w in W)
    err = max(abs(a * (w - wm) + zm - z) for w, z in zip(W, Z))
    return (dict(pdf=pdf, page=int(blk.get("page", 0)), rect=r, a=a, b=zm - a * wm, err=err, legend=blk.get("legend") or []),
            "site board plan 01 of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(pdf))))


def key_sample(pg, kind, col, x, y):
    """a legend sample 4 x 2.4 mm, its top-left at (x, y): fill, line, dash, dot or outline"""
    if kind == "fill": pg.rect(x, y - 2.4, 4.0, 2.4, fill=col)
    elif kind == "dot": pg.circle(x + 2.0, y - 1.2, 0.8, fill=col)
    elif kind == "dash": pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.4, (1.0, 0.6))
    elif kind == "outline": pg.rect(x + 0.2, y - 2.2, 3.6, 2.0, stroke=col, lw=0.35)
    elif kind == "outline2": pg.rect(x + 0.3, y - 2.1, 3.4, 1.8, stroke=col, lw=0.7)
    else: pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.5)


def page_farms(L, src):
    pg = Page(420, 297)
    BASE.clear()
    G, gnote = plan01_geo()
    fed = [(key, poly) for key in ("farmland", "orchard") for side in ("out", "in") for poly in GEO["lc"][key][side]]
    F = GEO["frame"]
    rotu = G["a"] / abs(G["a"]) if G else complex(math.cos(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])),
                                                  math.sin(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])))
    Q = [complex(p[0], p[1]) * rotu for _, poly in fed for ring in poly for p in ring]   # the plan's own turn
    bx0, bx1 = min(q.real for q in Q), max(q.real for q in Q)
    by0, by1 = min(q.imag for q in Q), max(q.imag for q in Q)
    wx0, wy0, wx1, wy1 = FARM_WIN
    den = next((d_ for d_ in ROUND_DENS if (bx1 - bx0) * 1000.0 / d_ + 4.0 <= wx1 - wx0 and
                (by1 - by0) * 1000.0 / d_ + 4.0 <= wy1 - wy0), ROUND_DENS[-1])
    m = 1000.0 / den                              # page mm per metre
    c = rotu * m
    t = complex((wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0) - complex((bx0 + bx1) / 2.0, (by0 + by1) / 2.0) * m

    def T(p):
        z = complex(p[0], p[1]) * c + t
        return (z.real, z.imag)
    hole = (wx0, wy0, wx1, wy1)
    if G:                                          # the window on the board's sheet, cut to plan 01's own crop
        kk = abs(G["a"]) / m

        def S(x, y):
            z = kk * (complex(x, y) - t) + G["b"]
            return z.real, -z.imag
        (sx0, sy1), (sx1, sy0) = S(wx0, wy0), S(wx1, wy1)
        r = G["rect"]
        cx0, cy0, cx1, cy1 = max(sx0, r[0]), max(sy0, r[1]), min(sx1, r[2]), min(sy1, r[3])
        if cx1 - cx0 > 20.0 * kk and cy1 - cy0 > 20.0 * kk:
            hole = (wx0 + (cx0 - sx0) / kk, wy0 + (sy1 - cy1) / kk, wx1 - (sx1 - cx1) / kk, wy1 - (cy0 - sy0) / kk)
            BASE.update(pdf=G["pdf"], page=G["page"], clip=(cx0, cy0, cx1, cy1), rect=hole, err=G["err"], den=den)
        else:
            G, gnote = None, "the farms lie outside the site board's plan 01"
    BASE["note"] = gnote
    header(pg, "THE FARMS WE FEED", "Fields and orchards the stored water serves, on the site plan \"What is there\"",
           hole=hole if G else None)
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0)"                # v4 (F5): read from Data/landcover
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    # v4 (MIRAQUA 28 Oct, F5): no [n] for what is not public online: the orchards (course survey symbols
    # SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH), the extent (around2.pdf registered to the survey) and the base (the site
    # board's own plan 01, cut and scaled, not redrawn) are said on the page without a mark
    # context line (review global rule 4): what it shows, why it is here, what to take from it; v4: 0.7 mm lower, under
    # the subtitle's new baseline (header)
    pg.text(cited("The site plan \"What is there\" with the fields and orchards our stored water serves outlined: the "
                  "farms read off the same base, colours and key as the site", None if G else WC),
            14, 264.8, 8.5, C["ink"])
    hx0, hy0, hx1, hy1 = hole
    if not G:                                      # fallback: v1.4's land cover drawing in the window, flagged
        A = GEO["around2"]
        pg.rect(wx0, wy0, wx1 - wx0, wy1 - wy0, fill=C["paper"])
        pg.path([[T(p) for p in A]], fill="E8E5DA")
        pg.path([[T(p) for p in GEO["frame"]]], fill="E8E5DA")
        for side in ("out", "in"):
            for key, lab, col in CLS[::-1]:
                for poly in GEO["lc"][key][side]:
                    pg.path([[T(p) for p in r] for r in poly], fill=col if (side == "out" or key in ("farmland", "orchard")) else "D9D6C8")
        for ln in GEO["streams"]: pg.line([T(p) for p in ln], C["water"], 0.5)
        for ln in GEO["selinos"]: pg.line([T(p) for p in ln], C["water_deep"], 1.1)
        pg.text("FLAG: " + gnote + " · land cover drawn from WorldCover instead", wx0 + 2, wy0 + 2, 7, C["accent"], True)
    # the farms layer: the extent, the fields and orchards we feed as outlines over the plan's own colours
    pg.poly([T(p) for p in GEO["around2"]], stroke=C["ink"], lw=0.35, closed=True, dash=(2.0, 1.2))
    for key, poly in fed:
        pg.path([[T(p) for p in r] for r in poly], stroke=C["accent"] if key == "farmland" else C["accent_deep"],
                lw=0.35 if key == "farmland" else 0.7)
    pg.rect(hx0, hy0, hx1 - hx0, hy1 - hy0, stroke=C["ink"], lw=0.25)
    # key column: north, scale, the farms layer with its figures, then plan 01's own key
    x, y = FARM_COL, 262.0
    north(pg, x + 6.0, y - 9.0, math.degrees(math.atan2(rotu.imag, rotu.real)), 5.0)
    bar = max(v for v in (50, 100, 200, 250, 500, 1000) if v * m <= 27.0)
    pg.rect(x, y - 21.0, bar * m / 2.0, 1.2, fill=C["ink"])
    pg.rect(x + bar * m / 2.0, y - 21.0, bar * m / 2.0, 1.2, stroke=C["ink"], lw=0.25)
    pg.text("0", x, y - 24.0, 6, C["ink"], align="C")
    pg.text("%d m" % bar, x + bar * m, y - 24.0, 6, C["ink"], align="R")
    pg.text("1:{:,} at A3".format(den), x, y - 27.5, 6.5, C["ink"], True)
    y -= 34.0
    fed_c, fed_o = L["cropland_ha"], L["orchard_ha"]
    o_lo = min(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    o_hi = max(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    cc = [c_ for c_ in L["crops"] if c_ in NET] or [c_ for c_ in NET if c_ != "olive"]
    c_lo = min(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    c_hi = max(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    f_in, f_out = GEO["area_ha"]["farmland"][1], GEO["area_ha"]["farmland"][0]
    pg.text("WE FEED", x, y, 8, C["accent"], True)
    y -= 3.0
    rows = [("outline", C["accent"], "fields " + cite(SRC2), "%s ha" % fmt1(fed_c),
             ["%s-%s m³ a season %s" % (fmt(rnd(fed_c * c_lo)), fmt(rnd(fed_c * c_hi)), cite(NEED2)),
              "as " + " / ".join(crop_word(c_) for c_ in cc) + " " + cite(TUIK),   # v4 (G11): corn, not maize
              "inside the site %s ha · outside %s ha %s" % (fmt1(f_in), fmt1(f_out), cite(WC))]),
            ("outline2", C["accent_deep"], "orchards", "%s ha" % fmt1(fed_o),             # v4 (F5): survey, no mark
             ["%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))), "as olive"]),
            ("dash", C["ink"], "the extent they lie in", "%s ha" % fmt(L.get("extent_ha", 455.0)), [])]
    for kind, col, lab, big, lines in rows:
        key_sample(pg, kind, col, x, y)
        pg.text(lab, x + 5.5, y - 2.1, 6.5, C["ink"], True)
        y -= 7.0
        pg.text(big, x, y, 12, C["green_deep"], True)
        y -= 3.4
        for ln in lines:
            y = pg.para(ln, x, y, 29.0, 6, C["ink2"], lead=1.2)
        y -= 2.0
    pg.line([(x, y + 0.5), (406.0, y + 0.5)], C["faint"], 0.3)
    y -= 4.0
    if G:
        pg.text("THE SITE PLAN'S KEY", x, y, 7, C["ink"], True)
        y -= 2.5
        for it in G["legend"]:
            key_sample(pg, it.get("kind", "fill"), it.get("colour", "B0AC9C"), x, y)
            y = min(pg.para(it.get("label", ""), x + 5.5, y - 2.0, 23.5, 5.5, C["ink"], lead=1.15) + 0.3, y - 3.4)
    else:
        for key, lab, col in CLS:
            key_sample(pg, "fill", col, x, y)
            pg.text(lab, x + 5.5, y - 2.0, 5.5, C["ink"]); y -= 3.6
    ag_crop("ag2_plan", 1, 13.0, min(y, wy0) - 1.0, 407.0, 267.6, den)   # v4: under the subtitle (269.5 now)
    return pg


def put_base(path):
    """v1.5: the site board's plan 01 under page 2's farms layer, as the booklet places sheets (PyMuPDF
    show_pdf_page): the window cut from its sheet, one scale factor both ways. Returns a log line."""
    if not BASE.get("pdf"):
        return "farms map: FLAG fallback drawing, " + BASE.get("note", "")
    import fitz
    K = 72 / 25.4
    hx0, hy0, hx1, hy1 = BASE["rect"]
    cx0, cy0, cx1, cy1 = BASE["clip"]
    doc, src = fitz.open(path), fitz.open(BASE["pdf"])
    doc[1].show_pdf_page(fitz.Rect(hx0 * K, (297.0 - hy1) * K, hx1 * K, (297.0 - hy0) * K), src, BASE["page"],
                         clip=fitz.Rect(cx0 * K, cy0 * K, cx1 * K, cy1 * K), overlay=False)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); src.close()
    os.replace(tmp, path)
    return "farms map on %s at 1:{:,} (georeference fit {:.2f} mm)".format(BASE["den"], BASE["err"]) % BASE["note"]

# ------------------------------------------------------------------ sources that are not public (F5, D13)
# v4 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38 "remove non-public citations"): the project's own record or internal
# research cards are not public online: cite() gives them no [n] and they leave the key; their words stay on the page
# as our own design statement. Facts now without a public source (reported): Tersane cotton (16th c.), ginning 1861,
# Sümerbank (1954/60-2008), the 19th-c. olive-oil machinery in the Kızıl Avlu S rotunda.
# v5 (T4a, 29 Oct, D13): also every source that names our own model run or method (F5_INTERNAL, by its words), and no
# status word (calculated, assumed ...) is ever printed in a source (F5_STATUS); page 3 (the plant ladder) is gone (D9 a).
F5_OFF = (COTTON_H, OLIVE_H)
F5_INTERNAL = ("water balance results", "default-lands copy", "farm areas from", "Bergama mix = ", "our arithmetic")
F5_STATUS = re.compile(r"\s*\((?:calculated|assumed|estimated|interpolated|indicative|design value)\)|"
                       r"\s*\b(?:calculated|assumed|estimated|interpolated|indicative)\b", re.I)


class Placer:
    """v1.6 (spec §2: no text on another text): every label's box is measured with text_w and kept; a new label takes
    the first free place over its anchor, lane by lane upwards (or downwards), left-, centre- or right-aligned on the
    anchor, inside its region; lifted labels get a hair leader down to the anchor. No free place: the label is left
    out and named in the log (never drawn over another). v8: put(leader=False) for no leaders (G3)."""
    def __init__(self):
        self.boxes, self.dropped = [], []

    def free(self, b):
        return all(b[2] <= q[0] or b[0] >= q[2] or b[3] <= q[1] or b[1] >= q[3] for q in self.boxes)

    def box(self, s, x, y, size, bold):
        h = size * 0.3528
        return (x - 0.5, y - 0.28 * h - 0.4, x + text_w(s, size, bold) + 0.5, y + 0.8 * h + 0.4)

    def text(self, pg, s, x, y, size, col, bold=False, halo=None):
        """a fixed label (titles, columns): drawn and blocked"""
        self.boxes.append(self.box(s, x, y, size, bold))
        pg.text(s, x, y, size, col, bold, halo=halo)

    def put(self, pg, s, ax, ay, size, col, bold=False, region=None, gap=1.4, up=True, lanes=9, halo="FFFFFF",
            lead_col=None, stick=False, leader=True):
        """v8 (round 3, G3): leader=False draws no hair leader (a lifted label stands in its lane alone)"""
        w, lane = text_w(s, size, bold), size * 0.3528 * 1.45
        for k in range(lanes):
            y = ay + (gap + k * lane if up else -gap - size * 0.3528 - k * lane)
            for x in (ax - 0.6, ax - w / 2.0, ax - w + 0.6):
                b = self.box(s, x, y, size, bold)
                if region and (b[0] < region[0] or b[2] > region[2] or b[1] < region[1] or b[3] > region[3]):
                    continue
                if not self.free(b):
                    continue
                end = b[1] + 0.3 if up else b[3] - 0.3
                seg = (ax - 0.25, min(ay, end), ax + 0.25, max(ay, end))
                lead = (bool(k) or stick) and leader
                if lead and not self.free(seg):
                    continue                           # the leader would cross another label
                self.boxes.append(b)
                if lead:
                    pg.line([(ax, ay), (ax, end)], lead_col or C["ink2"], 0.15)
                    self.boxes.append(seg)
                pg.text(s, x, y, size, col, bold, halo=halo)
                return x, y
        self.dropped.append(s)
        return None


# ------------------------------------------------------------------ v1.6: the sources page (Aras 27 Oct: no source footers)
def page_sources():
    """the sheet's one numbered source key, on its own page: the [n] marks on pages 1-3 refer to it, and the
    booklet's sources page reads it from here ("Sources by number:", as the old page footers)."""
    pg = Page(420, 297)
    pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text("SOURCES", 14, 279, 22, C["ink"], True)
    pg.text("Numbered as the [n] marks on pages 1-2", 14, 271.5, 11, C["ink2"])
    key = "Sources by number: " + "  ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY))
    pg.para(key, 14, 260, 392, 8, C["ink"], lead=1.35)
    return pg

# ------------------------------------------------------------------ v1.4: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own drawings. Each page function records its panels' rects
# (from the same numbers it lays them out with) in AG_CROPS; booklet_export writes them to blocks.json, with
# booklet/results.json (hectares per crop, same keys as v1.3). The v1.3 booklet redraws are gone.
# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(bg_first([os.path.join(bg_booklet(""), "booklet_slots.json"),        # 27 Oct: cached/booklet/
                            os.path.join(bg_output("bergama_booklet"), "booklet_slots.json")]), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes cached/booklet/<folder>/blocks.json (27 Oct, Aras: output/ holds
    final PDFs only; was output/<folder>/booklet/). out_dir = the script's output folder; its name is the folder key."""
    def __init__(self, out_dir, script, version):
        self.dir = bg_booklet(os.path.basename(os.path.normpath(out_dir)))
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop,
#                                      bk_w or None)
# v8: ag1_headline gone (the to-farms headline is part of ag1_stream)
# v9 (round 4, P19.1): the p19 crops carry their group heading inside, so their booklet captions are empty;
# ag1_reading is drawn inside ag1_context and is no crop of its own any more
AG_CAPTIONS = {"ag1_bars": "", "ag1_context": "", "ag1_crops": "", "ag1_stream": "", "ag1_history": "",
               "ag2_plan": "The farms we feed, on the site plan"}   # v5 (D9 a): ag3_* gone with the ladder page


def ag_crop(cid, page, x0, y0, x1, y1, den=None, legend=None, drop=None, bk_w=None):
    """a panel of page `page` (0-2), given as the page's own y-up mm (x0, y0)-(x1, y1). v8: bk_w = the width (mm) it is
    drawn for on the booklet page (the booklet then prints it at that size, 1:1)"""
    AG_CROPS.append((cid, page, (round(x0, 2), round(297.0 - y1, 2), round(x1, 2), round(297.0 - y0, 2)), den,
                     legend or [], drop or [], bk_w))


def ha_results(L):
    """hectares the storage irrigates per crop (page 1's bars): normal year and 1-in-5 dry year, lo-hi over the storage
    span (and the deficit saving range for olive), plus the dry-year ratio olive deficit / cotton."""
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0
    rows = [("olive_deficit", "olive", DEFICIT), ("olive_full", "olive", None)] + \
           [(c, c, None) for c in ("maize", "tomato", "cotton") if c in NET]
    out = {}
    for key, crop, dfc in rows:
        if crop not in NET: continue
        out[key] = {}
        for yr, yk in (("normal", "normal"), ("dry", "dry5")):
            g = gross_m3_ha(crop, yr)
            lo, hi = (w_lo / (g * (1 - dfc[0])), w_hi / (g * (1 - dfc[1]))) if dfc else (w_lo / g, w_hi / g)
            out[key][yk] = {"lo": round(lo, 1), "hi": round(hi, 1), "m3_per_ha": round(g, 0)}
    R = {"ha_per_crop": out, "to_farms_dry5_m3": [round(w_lo), round(w_hi)],
         "farms_fed_ha": round(L["cropland_ha"] + L["orchard_ha"], 2)}
    if "olive_deficit" in out and "cotton" in out:
        a, b = out["olive_deficit"]["dry5"], out["cotton"]["dry5"]
        R["ratio_olive_deficit_vs_cotton_dry5"] = {"lo": round(a["lo"] / b["lo"], 2), "hi": round(a["hi"] / b["hi"], 2)}
    ys = L.get("year_split")
    if ys and "normal" in ys and "dry5" in ys:      # v3 (Prompt 6): page 1's double squeeze, dry year against normal
        a_, b_, c_ = squeeze(ys)
        R["stream_first"] = {"water_years": [ys["normal"]["water_year"], ys["dry5"]["water_year"]],
                             "left_for_farms_change_pct": round(100.0 * a_, 1), "need_per_ha_change_pct": round(100.0 * b_, 1),
                             "hectares_change_pct": round(100.0 * c_, 1)}
    return R


def booklet_export(L):
    """blocks.json: one crop per panel of the A3 sheet; results.json: hectares per crop. Returns a log line."""
    bk = BkBlocks(OUT_DIR, "AgriCulture", VERSION)
    for cid, page, r, den, legend, drop, bk_w in AG_CROPS:
        bk.crop(cid, OUT_PDF, r, caption=AG_CAPTIONS.get(cid, ""), scale_den=den, legend=legend, page=page, drop=drop)
        if bk_w:                                   # v8: drawn for the booklet page at 1:1 (as city link, site board)
            bk.d["blocks"][cid]["bk_w"] = round(bk_w, 3)
    bk.save()
    R = ha_results(L)
    R.update(script="AgriCulture", version=VERSION)
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    return "booklet: %d crops, results.json" % len(AG_CROPS)

# ------------------------------------------------------------------ build and run
def build(path):
    BASE_OFF[0] = False
    L, src = live()
    NET.clear(); NET.update(L["net"])
    PHOTO_GOT.clear(); PHOTO_STATE.clear(); del PHOTO_LOG[:]   # v2: the plant photos, read once a press
    for _ in range(2):
        del AG_CROPS[:], SRC_KEY[:], LOG_NOTES[:], PHOTO_FR[:]      # v1.6: one source numbering for the whole sheet
        PHOTO_N[0] = 0
        tp_log_lines()                             # v9: a second pass logs its own "overlap p19 ..." lines only
        pages = [page_cubic(L, src), page_farms(L, src)]       # v5 (D9 a): the plant ladder page is gone
        write_pdf(pages + [page_sources()], path)
        try:                                       # v1.5: the site board's plan 01 under the farms layer
            return src, put_base(path) + "\n" + put_photos(path)   # v2: then the photos (never raises)
        except PermissionError:
            raise
        except Exception as ex:                    # never an empty window: once more with the fallback drawing
            BASE_OFF[0] = True
            err = "farms map: FLAG the site plan could not be placed (%s: %s), fallback drawing" % (type(ex).__name__, ex)
    return src, err + "\n" + put_photos(path)

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        src, base = build(path)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    try:                                           # v1.3: the A3 booklet frames; an error here never breaks the sheet
        bk = booklet_export(live()[0])
    except Exception as ex:
        bk = "booklet ERROR (sheet saved): %s: %s" % (type(ex).__name__, ex)
    bk = "\n".join([bk] + bg_tidy_output("Bergama_agriculture_alternatives"))   # 27 Oct: output/ = PDFs only
    flag = "".join("\n" + t for t in LOG_NOTES + tp_log_lines())   # v9 (G-R4-1): "overlap p19 <crop> checked n, collisions 0"
    flag += "\nFLAG: water balance results file not found in Downloads; its default-lands copy was used" if src == DEFAULT_NOTE else ""
    return "%s  %s\ntrigger: %s\nfigures: %s%s\n%s\nagriculture alternatives %s, %.1f s\n%s" % (
        OUT_PDF, time.strftime("%H:%M:%S"), TRIG_WHY[0], src, flag, base, VERSION, time.time() - t0, bk)

# ---- trigger.py (round 4, S1, 1 Nov 2026; BRIEF §6, round 3 open row 13): ONE start-up / trigger file ----------------
# Replaces common/chain_fire.py, gh_in_items.py, _gh_inputs.py, to_bool.py and the scripts' own copies of chain_fire,
# upstream_done, button_state, find_button, _button_value and BUTTON_WORDS (each page session removes its copy and
# calls trig_should_run; the closing step deletes the four old files once nothing includes them).
#
# WHAT STARTS A COMPONENT (the same for all nine scripts; RUN_GUIDE quotes this):
#   1. A press of its Button: the input named run (or bake / build / go / press / button / start, any case), else the
#      input a Button is wired into. Only the press starts it (the rising edge: False -> True); holding the Button
#      or re-solving while it is True does not start it again.
#   2. A NEW "done ..." text arriving on any of its own inputs from the script before it in the chain (one-click
#      chain). The first solve after the component is pasted, opened or rewired only NOTES the text already on the
#      wire, so pasting code or rewiring never starts a run (Aras 1 Nov 08:04); when the wire brings nothing, the done
#      text the upstream component left in Rhino's memory is read (Null on the wire).
#   Nothing else starts it: settings written in the script (PHOTO_ANY_LICENCE = True ...) and old globals that
#   Rhino 8 keeps between solves are never read as a press (Aras 1 Nov 08:24); only the component's own inputs are.
#
#   trig_inputs() -> {name: value}         the component's own inputs only (VariableName / NickName / Name), never
#                                          the script's globals; {} outside Grasshopper
#   trig_get(name, default=None)           one own input by name in any case; a list gives its first non-None item
#   to_bool(v, default=False)              True / "true" / "yes" / "1" / "on" / non-zero; a list = any item true
#   upstream_done(name) -> str | None      the "done ..." text the component wired into input `name` left in memory
#   chain_fire(v, key, name=None) -> bool  a NEW done text on v (a list gives its first "done ..." item) fires once;
#                                          the first solve per component + wiring only notes it
#   trig_button(settings=()) -> name|None  the Button input (see 1. above); never a name in settings (inputs that
#                                          carry options, e.g. the masterplan's SETTINGS), never one starting with "_"
#   trig_should_run(key="chain_seen", settings=()) -> (run, why, button)
#                                          run: bool; why: "button <name>" | "chain <input>" | None; button: its name
#                                          or None. Each script logs "trigger: <why>" in its run log.
TRIGGER_BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button", "start")


def trig_inputs():
    """{name: value} of this component's own inputs (globals holding them), nothing else"""
    g_ = globals()
    out = {}
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821 (Grasshopper)
            for a_ in ("VariableName", "NickName", "Name"):
                n_ = getattr(p_, a_, None)
                if n_ and str(n_) in g_:
                    out[str(n_)] = g_[str(n_)]
                    break
    except Exception:
        return {}
    return out


def trig_get(name, default=None):
    """an own input by name, any case; a list gives its first non-None item; empty text = default"""
    for k_, v_ in trig_inputs().items():
        if k_.lower() == str(name).lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None), None)
            return default if v_ is None or (isinstance(v_, str) and not v_.strip()) else v_
    return default


def to_bool(v, default=False):
    if v is None:
        return default
    if isinstance(v, (list, tuple)):
        return any(to_bool(x) for x in v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if not s:
        return default
    return s in ("true", "yes", "1", "on")


def upstream_done(name):
    """the done text of the component wired into input `name`, read from Rhino's memory (sticky) when the wire brings
    Null. Keys: "done:<guid>", "lu_done:<guid>" or "...<guid>_done" (template scripts)."""
    try:
        import scriptcontext as _scx
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            if str(p_.NickName or p_.Name).lower() != str(name).lower():
                continue
            for src_ in p_.Sources:
                g = str(src_.Attributes.GetTopLevel.DocObject.InstanceGuid)
                for k_ in ("done:" + g, "lu_done:" + g):
                    v_ = _scx.sticky.get(k_)
                    if str(v_).startswith("done "):
                        return str(v_)
                for k_, v_ in list(_scx.sticky.items()):
                    if str(k_).endswith(g + "_done") and str(v_).startswith("done "):
                        return str(v_)
    except Exception:
        pass
    return None


def _chain_wiring():
    """the sources wired into this component (their ids, sorted): rewiring starts a new chain memory"""
    try:
        return ",".join(sorted(str(s_.Attributes.GetTopLevel.DocObject.InstanceGuid)          # noqa: F821
                               for p_ in ghenv.Component.Params.Input for s_ in p_.Sources))   # noqa: F821
    except Exception:
        return ""


def chain_fire(v, key, name=None):
    """True once for each NEW "done ..." text on v (see the module notes)"""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if str(x).startswith("done ")), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done ") and name:
        s = upstream_done(name) or ""
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring()      # noqa: F821
        except Exception:
            pass
        # the first solve with this wiring (pasted, rewired or newly opened component) only notes what is on the
        # wire; "first" is tied to this solve's token (_CHAIN_SOLVE, made anew each time the script body runs), not
        # to a global, because Rhino 8 keeps a script's globals between solves
        tok = globals().get("_CHAIN_SOLVE")
        if _scx.sticky.get(key + ":init") is None:
            _scx.sticky[key + ":init"] = tok
        first = _scx.sticky.get(key + ":init") is tok
        if not s.startswith("done "):
            return False
        if first or _scx.sticky.get(key) == s:
            _scx.sticky[key] = s
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def trig_button(settings=()):
    """the Button input's name, or None"""
    ins = trig_inputs()
    skip = set(str(n).lower() for n in settings or ())

    def ok(n):
        return n and not n.startswith("_") and n.lower() not in skip
    for k_ in ins:
        if ok(k_) and "".join(c for c in k_.lower() if c.isalpha()) in TRIGGER_BUTTON_WORDS:
            return k_
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            nm = str(p_.NickName or p_.Name)
            if not ok(nm):
                continue
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    return nm
    except Exception:
        pass
    return None


def trig_should_run(key="chain_seen", settings=()):
    """(run, why, button): does this solve start the script? (see the module notes)"""
    btn = trig_button(settings)
    ins = trig_inputs()
    try:
        import scriptcontext as _scx
        try:
            gk = str(ghenv.Component.InstanceGuid)                          # noqa: F821
        except Exception:
            gk = ""
        pk = "trig_prev:" + key + ":" + gk
        on = to_bool(trig_get(btn)) if btn else False
        prev = bool(_scx.sticky.get(pk, False))
        _scx.sticky[pk] = on
    except Exception:
        on, prev = (to_bool(trig_get(btn)) if btn else False), False
    if on and not prev:
        return True, u"button " + btn, btn
    # the chain: the button input first (the board family wires the done text there), then every other own input
    skip = set(str(x).lower() for x in settings or ())
    names = ([btn] if btn else []) + [n for n in ins if n != btn and not n.startswith("_") and n.lower() not in skip]
    fired = None
    for n in names:
        v = ins.get(n)
        if v is None or isinstance(v, (bool, int, float)) or (isinstance(v, (list, tuple)) and not any(
                isinstance(x, str) for x in v)):
            if n != btn:
                continue
        if chain_fire(v, key + ":" + n, n) and fired is None:
            fired = n
    if fired:
        return True, u"chain " + fired, btn
    return False, None, btn


_CHAIN_SOLVE = object()     # a new token every time the script body runs (one per solve)
TRIG_WHY = ["run outside Grasshopper"]   # v9 (round 4): what started this run, for the log ("trigger: <why>")


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    # v9 (round 4): the one trigger file (common/trigger.py): a press of the Button (its rising edge) or a NEW done
    # text from the script before in the chain; the script's own trigger copies are gone
    _pressed, _why, _btn = trig_should_run("bergama_agri_alt_log_chain")
    TRIG_WHY[0] = _why
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_agri_alt_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_agri_alt_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_agri_alt_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_agri_alt_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_agri_alt_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_agri_alt_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_agri_alt_log_ver" + _ik) != VERSION:   # v1.7 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                            # shows itself at once, idle, no old time or log
            _sc.sticky.pop("bergama_agri_alt_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_agri_alt_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_agri_alt_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "AgriCulture " + VERSION + " · " + _sc.sticky.get("bergama_agri_alt_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
