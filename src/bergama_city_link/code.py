# bergama_city_link_v1_6.py · Thread 4 of the 22 Oct batch: connection to the city (the riverside spine and what it adds)
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_city_link_analysis by itself and saves
# ONE all-vector A3 PDF there (two pages) plus city_link_results.json:
#   1 WHY SHOPS MEET THE RIVER ONLY WHERE IT IS HIDDEN   spine study today: two charts, seven reasons, who comes
#   2 THE RIVERSIDE SPINE                                 the spine as a strip along the stream (not a plan: the plan is
#                                                         the site board's plan 07), heritage anchors, seven functions,
#                                                         the flood rule and who each function serves
# city_link_results.json = the spine and the function sites in survey coordinates. The site board (selinus_board v34,
# plan 07) reads it for the movement potential with the spine, and the masterplan (Thread 5) draws it.
# Read live on every run: the water balance results (farm areas for the producers' market) and the site board's
# movement result (walking potential on the spine), each with a flagged fallback.
# Notes for Aras: batch_2026-10-22/thread4_city_link/NOTES.md (every figure with its source).
import os, time, json, zlib, math

VERSION = "v1.6"
# v1.6 (Aras 25 Oct 17:00, visual first; audit batch_2026-10-25_visual_first/VISUAL_AUDIT.md §3): reasons as pictogram tiles,
# who comes as a people bar chart (log scale, "no data" bar), chart figures as callouts, walking potential as bars, stops as
# pictogram + keywords, events as a Jul-Sep calendar strip, flood rules as pictograms, bank vote as paired bars, sources as
# [n] with one numbered key per page. Flood depths corrected to research/rain_river_levels/README.md v1.1 (line 49).
# v1.5 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_city_link_log.txt (next to cached/ and output/), overwritten by each press.
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_city_link_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# all files under Downloads/Bergama/ (Aras rule, 24 Oct)
BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA, "output", "Bergama_city_link_analysis")
OUT_PDF = "Bergama_city_link_A3.pdf"
OUT_JSON = "city_link_results.json"
WB_FILES = [os.path.join(BERGAMA, "output", "Bergama_water_balance_analysis", "water_balance_results.json"),
            os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]
MV_FILE = os.path.join(BERGAMA, "output", "selinus_board", "city_link_movement.json")     # written by selinus_board v34
WB_DEFAULT = dict(cropland_ha=34.9, orchard_ha=1.34, cropland_crops="cotton,tomato")      # results_default.json, 24 Oct 08:21

# ------------------------------------------------------------------ the spine and the function sites (survey m)
# Anchors are surveyed points (h01 §0 and §5, source s62): K4 Ulucami Önü (29846,32278), K3 Tabak Köprüsü (30037,32122),
# P04 Red Hall south rotunda "Müze" (30238.7,31931.2), K5 Üç Kemer (30294,31792). side_ref = a surveyed point on the bank
# the piece runs on (P05 Ulu Cami; P02 Red Hall); offset_m = distance from the stream centreline (schematic, for the
# movement network only; Thread 5 draws the real edge). Piece B runs over the covered reach (offset 0), where the main
# spine (Kınık Caddesi) crosses the stream.
SPINE = [
    dict(id="A", name="Ulu Cami to K3 bank walk", frm=[29846.0, 32278.0], to=[30037.0, 32122.0], side_ref=[29844.2, 32313.3], offset_m=15.0, side="auto", catch_m=250.0),
    dict(id="B", name="Junction over the covered reach", frm=[30037.0, 32122.0], to=[30238.7, 31931.2], side_ref=None, offset_m=0.0),
    dict(id="C", name="Red Hall to Üç Kemer bank walk", frm=[30238.7, 31931.2], to=[30294.0, 31792.0], side_ref=[30245.0, 31962.0], offset_m=15.0, side="auto", catch_m=250.0),
]
# the main spine (Bankalar Caddesi + Kınık Caddesi, OSM "secondary" ways of the same extract, converted with the h01 §0
# formula, +-10-30 m), from Bankalar's south end east past the junction; the masterplan (v11) draws it (Thread 5)
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]
# side="auto": the bank is picked by the data (Aras 24 Oct 09:08: where more people live and modern buildings
# concentrate). Per bank, within catch_m of the stream along the piece: people = floors of homes (a proxy; footprints
# not weighted), modern = buildings of 3+ floors. More of both wins; on a split, modern decides when people differ by
# under 10 %, else people. The site board v34 recomputes it live from its buildings (survey floors + inferred) and
# writes the vote to city_link_movement.json, which wins over the built-in vote below.
# Built-in vote: survey floor labels YAZI_KAT_ADEDI (2,894 labels, course DXF of 17 Oct), the same floors as the board's
# density drawings; stream = OSM Selinos line; chainage and bank on the K4-K3-K5 chord (calculated, about ±30 m).
BANK_VOTE = {
    "A": dict(NE=dict(buildings=327, people_floors=425, modern_3plus=3), SW=dict(buildings=326, people_floors=436, modern_3plus=16)),
    "B": dict(NE=dict(buildings=403, people_floors=592, modern_3plus=4), SW=dict(buildings=263, people_floors=437, modern_3plus=31)),
    "C": dict(NE=dict(buildings=56, people_floors=73, modern_3plus=1), SW=dict(buildings=187, people_floors=245, modern_3plus=4)),
}

def bank_of(v):
    """the vote rule: (bank, why)"""
    ne, sw = v["NE"], v["SW"]
    if ne["people_floors"] >= sw["people_floors"] and ne["modern_3plus"] >= sw["modern_3plus"]:
        return "NE", "more people and more modern buildings"
    if sw["people_floors"] >= ne["people_floors"] and sw["modern_3plus"] >= ne["modern_3plus"]:
        return "SW", "more people and more modern buildings"
    if abs(ne["people_floors"] - sw["people_floors"]) < 0.10 * max(ne["people_floors"], sw["people_floors"], 1):
        return ("NE" if ne["modern_3plus"] > sw["modern_3plus"] else "SW"), "people within 10 %, more modern buildings"
    return ("NE" if ne["people_floors"] > sw["people_floors"] else "SW"), "more people (banks split on modern buildings)"

# chainage along the stream from the frame's north-west end: bridges from h02 card (s62): K4 467, K3 709, K5 1,126,
# K6 1,767 m; other places projected onto the K4-K3-K5-K6 chord here (calculated, about ±30 m)
CH = dict(K4=467, K3=709, K5=1126, K6=1767, cross=781, cov0=709, cov1=949)
# v1.6: source texts printed once in each page's numbered key (cite() gives their [n])
SRC_WET = "Days wet: research/rain_river_levels/README.md §3 (mean of water years 2016-2021)"
SRC_FLOOD = ("Floods: DSİ Q100/Q500; depth by Manning on the surveyed cross-sections, "
             "research/rain_river_levels/README.md v1.1 correction of 24 Oct (supersedes §3 levels)")
SRC_RULES = ("Flood rules: city link research §0 Q6 / Part G: Taşkın ve Rüsubat Kontrolü Yön. Art. 17(1), 4(1)(n), 6(2); "
             "Planlı Alanlar İmar Yön. Art. 5(10)")
SRC_SHOPS = ("Shops: OSM shop=* and cafe/restaurant/fast food/bar/pub/ice cream (extract of 28 Jul 2026), counted by distance "
             "to the OSM Selinos line between the frame's NW end and K6 (calculated; OSM misses some shops, so the counts are "
             "low, not high)")
SRC_CH = "Chainage from the frame's NW end; bridges h02 card (s62); covered reach K3 to the end of the survey gap (h02 E01)"
SRC_HIST = "History: h01, h02 (sources s13 s28 s32 s36 s40 s42 s43 s59 s110)"
SRC_WHO = "Who comes: library/research/city_link_2026-10-24/city_link_research_v1.md §0; no data = no source anywhere"
SRC_STRIP = ("Strip diagram, not to scale across the river; chainage along the stream to scale (bridges s62; other places "
             "from h01 §5 survey coordinates, calculated, ±30 m)")
SRC_TABAK = ("h02 calls Tabaklar Hamamı 'opposite Ulu Cami on the right bank' (s32), but both survey points lie on the "
             "north-east bank [U]")
SRC_PLAN07 = ("The plan of the spine is on the site board's plan 07 (movement before and after), read from "
              "city_link_results.json")
SRC_T5 = "Exact edge, decks and stall sizes: Thread 5 masterplan"
# who: L locals, T tourists, S students; grows: W water, E river edge, A agriculture, H heritage
FUNCS = [
    dict(n=1, name="Bank bazaar", where="Tabaklar Hamamı", ch=522, bank="NE", xy=[29890.4, 32243.6], who="LT", grows="HE",
         icon="stall", kw=("Ottoman bazaar on this bank: Pabuççular Arastası", "stalls bring it back"), src="h02 s32"),
    dict(n=2, name="Parchment and leather workshops", where="Tannery quarter at K3", ch=737, bank="both", xy=[30062.0, 32106.0], who="TSL", grows="H",
         icon="hide", kw=("tanning named the stream · last master died 2026", "teach and sell the craft"), src="h02 s44 s45"),
    dict(n=3, name="Junction square", where="Kınık Caddesi over the covered stream", ch=781, bank="over", xy=[30058.0, 32047.0], who="LTS", grows="WEH",
         icon="slot", kw=("the one place the main road meets the river", "a slot: view down to the water strip"), src=None),
    dict(n=4, name="Red Hall water terrace", where="Red Hall, Roman tunnels' outlet", ch=962, bank="NE", xy=[30238.7, 31931.2], who="TL", grows="HW",
         icon="arch", kw=("Red Hall reopens: target 2026", "its visitors step out onto the river"), src="h02 s41"),
    dict(n=5, name="Producers' market", where="Üç Kemer bridge, Wednesdays", ch=1126, bank="spine", xy=[30294.0, 31792.0], who="LT", grows="A",
         icon="olive", kw=("food from fields on our stored water · olive oil", "Wednesdays · town producers' market: Saturdays"), src="h02 s25"),
    dict(n=6, name="Study terraces", where="Spine bank between K4 and K3", ch=620, bank="spine", xy=[29941.0, 32200.0], who="SL", grows="EW",
         icon="bench", kw=("shaded seats by the water strip", "for students · out of the street noise"), src=None),
    dict(n=7, name="Clean-water classroom", where="Reed basins, upstream entry", ch=200, bank="bed", xy=None, stage="entry", who="SL", grows="W",
         icon="reed", kw=("the cleaning basins as a lesson", "how the river works"), src=None),
]
EVENTS = dict(n=8, name="Summer bed events", where="Dry bed beside the 4 m water strip", who="LT", grows="WE",
              icon="calendar", kw=("open-air events · Jul-Sep", "bed 3 cm or less · cleared by October"), src=SRC_WET)
# v1.6: kw = 2 keyword lines (were one "why" sentence); src = the source number in the page key; icon = the stop's pictogram
HERITAGE = [  # (chainage, bank, label, source) from h01 §5 (survey coordinates projected, calculated)
    (380, "NE", "Roman complex", "P12"), (444, "NE", "Ulu Cami 1398", "P05"), (522, "NE", "Tabaklar Hamamı", "P07"),
    (737, "NE", "Tannery quarter", "E07"), (752, "SW", "İstiklal Meydanı", "P16"), (887, "SW", "Yabets synagogue", "P14"),
    (962, "NE", "Red Hall (Kızıl Avlu)", "P02"), (1376, "NE", "Harap Camii", "P18")]

# ------------------------------------------------------------------ computed here from OSM (extract of 28 Jul 2026)
# shops = OSM shop=* or amenity cafe/restaurant/fast_food/bar/pub/ice_cream (points and buildings); stream = the OSM
# Selinos lines between the frame's NW end and K6, covered pieces = tunnel/culvert tags; chainage as CH above
SHOPS_PER_100M = [(300, 2), (400, 3), (500, 1), (600, 2), (700, 17), (800, 14), (900, 6), (1000, 3), (1100, 2),
                  (1200, 0), (1300, 0), (1400, 1), (1500, 5), (1600, 1)]           # shops within 60 m of the stream
BANDS = ["0-30", "30-60", "60-120", "120-250", "250-500"]                          # m from the stream
OPEN_BAND = [(30, 9), (168, 27), (401, 37), (689, 25), (769, 27)]                 # (buildings, shops) by the open stream
COVERED_BAND = [(24, 15), (11, 6), (30, 18), (85, 23), (135, 6)]                  # ... by the covered pieces
REASONS = [  # v1.6 tiles: (pictogram, keyword heading, big figure, keyword lines, source in the key)
    ("road", "MAIN ROAD MEETS THE STREAM", "1 crossing", ("Bankalar - Kınık Caddesi", "only where the stream runs covered"), "OSM, calculated"),
    ("front", "BUILDINGS WITHIN 30 M", "30 buildings", ("on 1.7 km of open stream", "almost no frontage for a shop"), "OSM, calculated"),
    ("bank", "BANK DISCONNECTED", "68 %", ("12 % enclosed by building backs", "2 % accessible"), "PR1 board p.2 (v18 bank analysis)"),
    ("deep", "BED BELOW THE BANKS", "1.1-6.7 m", ("walls", "no way down"), "Bed depth: survey, 22 cuts (library INDEX row 24)"),
    # v1.6 fix (VISUAL_AUDIT accuracy 1): was "0.4-1.4 m / Q500 rises over the banks; Q100 tops every bank too" (withdrawn);
    # now README v1.1 line 49: "on the surveyed sections Q100 2.0-3.0 m and Q500 2.3-3.3 m, flat end 1.4 / 1.5 m,
    # overtopping only at K4 and S4"
    ("flood", "Q100 OVER THE BED", "2.0-3.0 m", ("Q500 2.3-3.3 m · flat end 1.4 / 1.5 m", "over the banks only at K4 and S4"), SRC_FLOOD),
    ("sewage", "SEPTIC SEWAGE IN THE STREAM", "until 2024", ("odour", "flies"), "İZSU sewer, s59; E13"),
    ("arch", "RED HALL BUILT OVER THE RIVER", "AD 117-138", ("Ottoman bazaar still met it", "at Tabaklar Hamamı"), "h02 s13 s28; s32"),
]
WHO = [  # v1.6 bars: (pictogram, keyword heading, big figure, low, high, keyword lines, source); None = no data.
    # Research: library/research/city_link_2026-10-24/city_link_research_v1.md
    ("visitor", "VISITS · PERGAMON SITES 2023", "433,000", 433000, 433000, ("Minister: about 480,000", "mostly day trips"), "AA; research §0 Q2 [U]"),
    ("resident", "RESIDENTS · 7 MAHALLES 2025", "11,002", 11002, 11002, ("by the stream", "district 107,549"), "TÜİK ADNKS via republishers; §0 Q3"),
    ("student", "STUDENTS · EGE UNIV. MYO", "1,425", 1425, 1425, ("2024/25", "campus 3.5-3.7 km away"), "Ege MYO report 2025; §0 Q1"),
    ("student", "STUDENTS · DEÜ BERGAMA MYO", "400-500", 400, 500, ("2025", "campus 1.5-1.7 km away"), "press 01.08.2025; §0 Q1"),
    ("bed", "KYK STUDENT DORMITORY", "750 beds", 750, 750, ("on the Ege campus", "Efeler Cad. 7"), "two sources; §0 Q1 [V]"),
    ("walker", "PEDESTRIANS ON THE STREETS", None, None, None, ("no count exists", "needs an on-site count"), "none found; §0 Q8"),
]
FLOOD = [  # v1.6: (level, keyword lines on how often wet, [(rule pictogram, rule keywords)], source of the wet lines)
    ("Bed", ("dry or 3 cm Jul-Sep", "0.1 m on about 100 days"),
     [("nofix", "nothing fixed narrows the bed (17/1)"), ("calendar", "clearable stalls and events, Jul-Sep only")], SRC_WET),
    ("Terrace +1 m", ("0 days in an average year", "floods only"),
     [("stamp", "low stone seats only with DSİ approval"), ("stall", "stalls taken in on a warning")], SRC_WET),
    # v1.6 fix (VISUAL_AUDIT accuracy 1): was "Q100 2.6-3.0 m and Q500 2.9-3.5 m over the bed" (withdrawn); README v1.1
    # line 49 and its table (Q100 2.05-2.99 m, Q500 2.33-3.30 m on the five surveyed cuts; flat end 1.38 / 1.54 m)
    ("Bank top", ("Q100 2.0-3.0 m · Q500 2.3-3.3 m over the bed", "flat end 1.4 / 1.5 m · over the banks: K4, S4"),
     [("road", "6 m service road kept clear"), ("crest", "occupied floors at DSİ crest + 1.50 m (5/10)")], SRC_FLOOD),
]
# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

#@include ../common/rgb.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/text_w.py

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        self.path([P], fill, stroke, lw, closed, dash)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None):
        """several rings in one path; a fill uses even-odd, so holes stay open"""
        k = 72 / 25.4; o = ["q"]
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
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L"):
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        line, yy = "", y
        for word in s.split(" "):
            t = (line + " " + word).strip()
            if text_w(t, size, bold) > w and line:
                self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead; line = word
            else: line = t
        if line: self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        return yy

def write_pdf(pages, path):
    k = 72 / 25.4
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (5 + 2 * i) for i in range(n)), n),
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF,
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, 6 + 2 * i)).encode("latin-1")
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % (6 + 2 * i, len(content))).encode("latin-1") + content + b"\nendstream\nendobj\n"
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama city link) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
    with open(path, "wb") as f: f.write(out)


# ------------------------------------------------------------------ live numbers
def _load(paths):
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            return d, time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
        except Exception:
            pass
    return None, None

def live():
    """farm lands from the water balance results; walking potential on the spine from the site board"""
    d, t = _load(WB_FILES)
    lands = (d or {}).get("lands") or WB_DEFAULT
    wb_src = ("water balance results of " + t) if d else "FLAG: water balance results not found; default lands of 24 Oct"
    mv, t2 = _load([MV_FILE])
    mv_src = ("site board movement of " + t2) if mv else "run the site board once to compute the walking potential"
    votes = dict((k, dict(v)) for k, v in BANK_VOTE.items())
    vote_src = "survey floor labels (built in, 24 Oct)"
    for v in (mv or {}).get("bank_votes") or []:
        if v.get("id") in votes:
            votes[v["id"]] = dict(NE=v["NE"], SW=v["SW"])
            vote_src = "site board buildings (" + mv_src + ")"
    sides = dict((pc["id"], bank_of(votes[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
    return dict(lands=lands, wb_src=wb_src, mv=mv, mv_src=mv_src, votes=votes, vote_src=vote_src, sides=sides)

#@include ../common/fmt.py

GROUP = dict(L=("Locals", "CC9A52"), T=("Tourists", "8B3A3F"), S=("Students", "5C7A86"))
GROWS = dict(W="water", E="river edge", A="agriculture", H="heritage")
GROW_C = dict(W=C["water_deep"], E=C["water"], A=C["green_mid"], H=C["accent"])   # v1.6 letter chips
SPINE_C = "BC6F45"

def header(pg, n, title, sub):
    pg.rect(0, 0, 420, 297, fill=C["ground"])
    pg.text(n, 14, 279, 22, C["accent"], True)
    pg.text(title, 26, 279, 22, C["ink"], True)
    pg.text(sub, 26, 271.5, 11, C["ink2"])
    pg.text("CONNECTION TO THE CITY · PAGE %s OF 2 · GROUP 6" % n, 406, 281, 7, C["ink2"], True, "R")

SRC_KEY = []                         # v1.6: sources printed as [n] on the page; the numbered key is in the footer


def cite(src):
    """v1.6 (water board v1.6 method): the number of a source in this page's footer key, as "[n]"."""
    if not src:
        return ""
    if src not in SRC_KEY:
        SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)


def footer(pg):
    """v1.6: ONE numbered source key per page (was a source paragraph); small text is fine here."""
    pg.para("Sources by number:  " + "   ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY)), 14, 13, 392, 5.5,
            C["ink2"])


def fit(pg, s, x, y, size, w, col, bold=False, align="L"):
    """v1.6: one line of keywords, shrunk (never below 4.5 pt) until it fits w mm"""
    while text_w(s, size, bold) > w and size > 4.5:
        size -= 0.25
    pg.text(s, x, y, size, col, bold, align)


def disc(pg, x, y, r, fill=None, stroke=None, lw=0.2):
    pg.poly([(x + r * math.cos(a * math.pi / 12), y + r * math.sin(a * math.pi / 12)) for a in range(24)],
            fill=fill, stroke=stroke, lw=lw, closed=True)


def icon(pg, kind, x, y, sz):
    """v1.6 (after water board v1.7 icon()): a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10
    grid. Graphic only."""
    u = sz / 10.0
    lw = 0.07 * sz
    ink, ink2, wat, wd, acc, st, pap = C["ink"], C["ink2"], C["water"], C["water_deep"], C["accent"], C["structure"], C["paper"]

    def P(pts):
        return [(x + a * u, y - sz + b * u) for a, b in pts]

    def R(a0, b0, a1, b1, fill=None, stroke=None):
        pg.poly(P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)]), fill=fill, stroke=stroke, lw=lw, closed=True)

    def D(a, b, r, fill=None, stroke=None):
        disc(pg, x + a * u, y - sz + b * u, r * u, fill, stroke, lw)

    def person(a, col):
        D(a, 8.0, 1.25, col)
        pg.poly(P([(a - 1.6, 0.6), (a - 1.6, 5.4), (a - 0.9, 6.4), (a + 0.9, 6.4), (a + 1.6, 5.4), (a + 1.6, 0.6)]),
                fill=col, closed=True)

    def X(a0, b0, a1, b1):
        pg.line(P([(a0, b0), (a1, b1)]), acc, lw * 1.4)
        pg.line(P([(a0, b1), (a1, b0)]), acc, lw * 1.4)

    if kind == "road":                                   # the road crosses the water once
        R(0, 3.6, 10, 6.4, wat)
        R(3.6, 0, 6.4, 10, ink2)
        for b in (0.8, 3.0, 5.2, 7.4):
            pg.line(P([(5, b), (5, b + 1.2)]), C["white"], lw * 0.6)
    elif kind == "front":                                # buildings turn their backs to the water
        R(0, 0.4, 10, 2.6, wat)
        for a in (0.4, 3.6, 6.8):
            R(a, 4.0, a + 2.8, 8.6, pap, ink)
        X(7.0, 0.2, 9.8, 3.2)
    elif kind == "bank":                                 # the bank cut off from the city
        R(0, 0.4, 4.2, 2.6, wat)
        R(4.2, 0.4, 5.4, 7.0, ink2)
        R(5.4, 5.8, 10, 7.0, st)
        X(6.2, 1.2, 9.4, 4.4)
    elif kind == "deep":                                 # the bed deep between walls
        pg.poly(P([(0, 9), (2.6, 9), (2.6, 1.2), (7.4, 1.2), (7.4, 9), (10, 9), (10, 0), (0, 0)]), fill=st, closed=True)
        R(2.6, 1.2, 7.4, 2.4, wat)
        pg.line(P([(5, 8.6), (5, 3.0)]), ink, lw)
        pg.poly(P([(4.2, 3.9), (5, 2.6), (5.8, 3.9)]), fill=ink, closed=True)
    elif kind == "flood":                                # a cut with two flood levels
        pg.poly(P([(0, 8), (2, 8), (3.4, 1.0), (6.6, 1.0), (8, 8), (10, 8), (10, 0), (0, 0)]), fill=st, closed=True)
        pg.poly(P([(2.3, 6.5), (3.4, 1.0), (6.6, 1.0), (7.7, 6.5)]), fill=wat, closed=True)
        pg.line(P([(1.2, 7.4), (8.8, 7.4)]), wd, lw, dash=(0.8 * u, 0.6 * u))
    elif kind == "sewage":                               # a pipe dripping into the water
        R(0, 0.4, 10, 2.6, wat)
        R(0, 6.0, 5.6, 8.2, ink2)
        R(5.0, 5.6, 6.0, 8.6, ink)
        D(6.6, 4.0, 0.65, "7A6448")
        D(7.4, 3.0, 0.5, "7A6448")
    elif kind == "arch":                                 # a Roman arch
        R(0.6, 0.4, 9.4, 1.2, ink2)
        pg.poly(P([(1.2, 1.2), (1.2, 7.0), (2.4, 8.8), (5, 9.6), (7.6, 8.8), (8.8, 7.0), (8.8, 1.2), (6.8, 1.2),
                   (6.8, 5.6), (5, 7.2), (3.2, 5.6), (3.2, 1.2)]), fill=acc, closed=True)
    elif kind in ("visitor", "resident", "student", "walker"):
        person(4.0, ink)
        if kind == "visitor":                            # a camera
            R(6.4, 4.0, 9.8, 6.4, ink2)
            D(8.1, 5.2, 0.7, C["white"])
        elif kind == "resident":                         # a house
            R(6.4, 0.6, 9.6, 3.8, pap, ink)
            pg.poly(P([(6.0, 3.6), (8.0, 5.8), (10.0, 3.6)]), fill=ink2, closed=True)
        elif kind == "student":                          # a cap
            pg.poly(P([(1.6, 9.2), (4.0, 10.0), (6.4, 9.2), (4.0, 8.4)]), fill=wd, closed=True)
            R(7.0, 1.0, 9.8, 4.6, pap, ink)
        else:                                            # no count
            pg.text("?", x + 8.0 * u, y - sz + 1.0 * u, 9.0 * u / 0.3528 * 0.8, acc, True, "C")
    elif kind == "bed":                                  # a bed
        R(0.6, 3.0, 9.4, 5.0, st)
        R(0.6, 5.0, 3.4, 6.8, pap, ink)
        R(0.6, 1.0, 1.4, 8.0, ink)
        R(8.6, 1.0, 9.4, 5.0, ink)
    elif kind == "stall":                                # a market stall
        pg.poly(P([(0.4, 6.0), (1.6, 9.0), (8.4, 9.0), (9.6, 6.0)]), fill=acc, closed=True)
        R(1.2, 0.4, 2.0, 6.0, ink)
        R(8.0, 0.4, 8.8, 6.0, ink)
        R(1.2, 3.0, 8.8, 4.0, ink2)
    elif kind == "hide":                                 # a stretched hide
        pg.poly(P([(2, 1), (1, 3), (2, 5), (1, 7), (2.4, 9.2), (5, 8.4), (7.6, 9.2), (9, 7), (8, 5), (9, 3), (8, 1),
                   (5, 1.8)]), fill="A0784F", closed=True)
    elif kind == "slot":                                 # a square with a slot onto the water below
        R(0, 4.0, 10, 9.0, st)
        R(3.0, 5.8, 7.0, 7.2, wat)
        R(0, 0.4, 10, 2.6, wat)
        pg.line(P([(5, 5.4), (5, 3.0)]), ink, lw)
    elif kind == "olive":                                # an olive tree
        R(4.5, 0.4, 5.5, 4.4, ink2)
        D(5.0, 6.2, 3.4, C["green_mid"])
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)):
            D(a, b, 0.5, ink)
    elif kind == "bench":                                # a shaded seat
        D(5.0, 7.6, 2.4, C["green_mid"])
        R(4.6, 3.4, 5.4, 5.4, ink2)
        R(1.0, 2.6, 9.0, 3.4, ink)
        R(1.6, 0.4, 2.4, 2.6, ink)
        R(7.6, 0.4, 8.4, 2.6, ink)
    elif kind == "reed":                                 # reeds in a basin
        R(0, 0, 10, 2.2, wat)
        for k_ in range(5):
            a = 1.6 + k_ * 1.7
            t = 6.6 + (k_ % 2) * 2.2
            pg.line(P([(a, 0.8), (a + 0.3, t)]), C["green_deep"], lw)
            R(a - 0.25, t - 1.8, a + 0.85, t + 0.2, C["field"])
    elif kind == "calendar":                             # a calendar page, Jul-Sep marked
        R(0.6, 0.6, 9.4, 8.6, pap, ink)
        R(0.6, 7.0, 9.4, 8.6, ink2)
        for i in range(12):
            a, b = 1.3 + (i % 4) * 2.0, 5.0 - (i // 4) * 2.0
            R(a, b, a + 1.4, b + 1.3, acc if i in (6, 7, 8) else C["faint"])
    elif kind == "nofix":                                # no post fixed in the bed
        R(0, 0.4, 10, 2.6, wat)
        R(4.4, 1.6, 5.6, 8.0, ink2)
        X(2.0, 2.0, 8.0, 8.6)
    elif kind == "stamp":                                # an approval stamp
        D(5.0, 5.0, 4.2, None, wd)
        pg.line(P([(2.8, 5.2), (4.4, 3.4), (7.4, 6.8)]), wd, lw * 1.4)
    elif kind == "crest":                                # occupied floors above the crest line
        R(2.4, 4.0, 7.6, 8.0, pap, ink)
        pg.poly(P([(2.0, 7.8), (5.0, 9.8), (8.0, 7.8)]), fill=ink2, closed=True)
        pg.line(P([(0, 2.6), (10, 2.6)]), wd, lw, dash=(0.8 * u, 0.6 * u))
        pg.line(P([(9.0, 2.8), (9.0, 3.8)]), ink, lw * 0.7)
    elif kind == "farm":                                 # a field fed by water
        pg.poly(P([(0, 0.6), (6.8, 0.6), (10, 5.4), (3.2, 5.4)]), fill=C["field"], closed=True)
        R(1.0, 7.0, 6.4, 8.6, wat)
        pg.line(P([(6.4, 7.8), (9.2, 7.8)]), wd, lw)
        pg.poly(P([(8.6, 8.6), (9.8, 7.8), (8.6, 7.0)]), fill=wd, closed=True)

def group_dots(pg, x, y, who, r=1.3):
    for i, k in enumerate("LTS"):
        cx = x + i * (2 * r + 1.0)
        ring = [(cx + r * math.cos(a * math.pi / 8), y + r * math.sin(a * math.pi / 8)) for a in range(16)]
        pg.poly(ring, fill=GROUP[k][1] if k in who else C["paper"], stroke=GROUP[k][1], lw=0.25, closed=True)

def roundel(pg, x, y, n, r=3.2, col=None):
    ring = [(x + r * math.cos(a * math.pi / 12), y + r * math.sin(a * math.pi / 12)) for a in range(24)]
    pg.poly(ring, fill=col or C["ink"], closed=True)
    pg.text(str(n), x, y - 1.25, 9, C["white"], True, "C")

# ------------------------------------------------------------------ page 1: why shops meet the river only where it is hidden
def page_why(L):
    pg = Page(420, 297)
    SRC_KEY[:] = []                               # v1.6: each page has its own numbered key
    header(pg, "1", "WHY SHOPS MEET THE RIVER ONLY WHERE IT IS HIDDEN",
           "spine study, today · shops follow the through road + fronts")   # v1.6 keywords (the open river has neither: tiles)
    # chart A: shops within 60 m of the stream, every 100 m of stream
    x0, y0, w, h = 22, 168, 180, 78
    pg.text("SHOPS WITHIN 60 M OF THE STREAM, EVERY 100 M OF STREAM " + cite(SRC_SHOPS) + " " + cite(SRC_CH), 14, 256, 9,
            C["ink"], True)
    c0, c1 = 300, 1700
    X = lambda c: x0 + (c - c0) / float(c1 - c0) * w
    vmax = 18.0
    cx0, cx1 = X(CH["cov0"]), X(CH["cov1"])
    pg.rect(cx0, y0, cx1 - cx0, h, fill=C["faint"])
    pg.text("stream covered", (cx0 + cx1) / 2, y0 + h - 4, 6.5, C["ink2"], True, "C")
    for c, n in SHOPS_PER_100M:
        bh = n / vmax * (h - 8)
        pg.rect(X(c) + 1.2, y0, X(c + 100) - X(c) - 2.4, max(bh, 0.3), fill=SPINE_C)
        if n:
            pg.text(str(n), (X(c) + X(c + 100)) / 2, y0 + bh + 1.2, 7, C["ink"], True, "C")
    pg.line([(x0, y0), (x0 + w, y0)], C["ink"], 0.35)
    for k in ("K4", "K3", "K5"):
        pg.line([(X(CH[k]), y0 - 3), (X(CH[k]), y0)], C["ink"], 0.35)
        pg.text(k, X(CH[k]), y0 - 6.5, 7, C["ink"], True, "C")
    xs = X(CH["cross"])
    pg.line([(xs, y0), (xs, y0 + h)], C["accent"], 0.9)
    pg.text("main road crosses", xs + 1.5, y0 + h - 9, 6.5, C["accent"], True)
    for c in range(c0, c1 + 1, 200):
        pg.text("%d m" % c, X(c), y0 - 11, 6, C["ink2"], False, "C")
    # v1.6: the figure as a callout on the chart, with a leader to the covered reach (was a sentence under the chart)
    qx, qy = X(1050), y0 + 58
    pg.text("31 of 57 (54 %)", qx, qy, 14, SPINE_C, True)
    pg.text("of the shops by the stream", qx, qy - 5.5, 7, C["ink"])
    pg.text("on the covered 200 m · main road crosses", qx, qy - 9, 7, C["ink"])
    pg.line([(qx - 1.5, qy + 1.5), (cx1, qy + 1.5)], SPINE_C, 0.35)
    disc(pg, cx1, qy + 1.5, 0.7, SPINE_C)
    # chart B: shops per 100 buildings by distance
    bx, by, bw, bh_ = 232, 168, 170, 78
    pg.text("SHOPS PER 100 BUILDINGS, BY DISTANCE FROM THE STREAM " + cite(SRC_SHOPS), 222, 256, 9, C["ink"], True)
    vmax = 65.0
    gw = bw / len(BANDS)
    for i, lab in enumerate(BANDS):
        for j, (rows, col, nm) in enumerate(((OPEN_BAND, C["water_deep"], "open"), (COVERED_BAND, C["structure"], "covered"))):
            nb, ns = rows[i]
            v = 100.0 * ns / nb if nb else 0.0
            hh = v / vmax * (bh_ - 8)
            xx = bx + i * gw + 3 + j * (gw - 6) / 2
            pg.rect(xx, by, (gw - 6) / 2 - 1, max(hh, 0.3), fill=col)
            pg.text("%.0f" % v, xx + (gw - 6) / 4 - 0.5, by + hh + 1.2, 7, C["ink"], True, "C")
            pg.text("n %d" % nb, xx + (gw - 6) / 4 - 0.5, by + 1.5, 5, C["white"] if hh > 6 else C["ink2"], False, "C")
        pg.text(lab + " m", bx + i * gw + gw / 2, by - 6.5, 7, C["ink"], True, "C")
    pg.line([(bx, by), (bx + bw, by)], C["ink"], 0.35)
    pg.rect(bx, by + bh_ - 3, 4, 3, fill=C["water_deep"]); pg.text("by the open stream", bx + 6, by + bh_ - 2.6, 7, C["ink"])
    pg.rect(bx + 50, by + bh_ - 3, 4, 3, fill=C["structure"]); pg.text("by the covered pieces", bx + 56, by + bh_ - 2.6, 7, C["ink"])
    pg.text("n = buildings", bx + 104, by + bh_ - 2.6, 7, C["ink2"])
    # v1.6: the figure tied by a leader to its bar (the open stream, 0-30 m); keywords instead of the sentence
    lx_ = bx + 3 + (gw - 6) / 4 - 0.5
    pg.line([(lx_, by - 15.5), (lx_, by - 0.5)], C["water_deep"], 0.35)
    pg.text("30 per 100", bx, by - 20, 14, C["water_deep"], True)
    pg.text("shops like the water · but only 30 buildings face it", bx + 30, by - 18.5, 7.5, C["ink"])
    # seven reasons: v1.6 pictogram tiles (icon, keyword heading, one big figure, keywords, [n]); were sentences
    pg.text("SEVEN REASONS THE RIVER EDGE HAS NO SPINE " + cite(SRC_HIST), 14, 128, 9, C["ink"], True)
    tw_ = 392 / 7.0
    for i, (ic, head, big, kws, src) in enumerate(REASONS):
        x = 14 + i * tw_
        pg.rect(x, 82, tw_ - 3, 41, fill=C["paper"])
        icon(pg, ic, x + 2.5, 120.5, 9)
        fit(pg, big, x + 13.5, 113, 13, tw_ - 18.5, C["accent"], True)
        fit(pg, head, x + 2.5, 105.5, 6.5, tw_ - 8, C["ink"], True)
        for j, k in enumerate(kws):
            fit(pg, k, x + 2.5, 100.5 - j * 3.6, 6.3, tw_ - 8, C["ink"])
        pg.text(cite(src), x + 2.5, 85, 6, C["ink2"], True)
    # who comes: v1.6 people pictograms with a bar each (log scale); no pedestrian count = an empty bar marked no data
    pg.text("WHO THE PROJECT BRINGS TO THE RIVER " + cite(SRC_WHO), 14, 72, 9, C["ink"], True)
    pg.text("bars: log scale, 1 to 1,000,000", 406, 72, 6, C["ink2"], False, "R")
    ww = 392 / 6.0
    bw_ = ww - 9.0
    lg = lambda v: bw_ * math.log10(max(v, 1)) / 6.0
    for i, (ic, head, big, lo, hi, kws, src) in enumerate(WHO):
        x = 14 + i * ww
        icon(pg, ic, x, 68, 9)
        pg.text(big or "no data", x + 11, 61, 14, C["ink"] if big else C["accent"], True)
        fit(pg, head, x, 54.5, 6.3, ww - 6, C["ink"], True)
        for j, k in enumerate(kws):
            fit(pg, k, x, 51 - j * 3.3, 6.2, ww - 6, C["ink"])
        if big:
            pg.rect(x, 40.5, lg(lo), 2.4, fill=SPINE_C)
            if hi > lo:                                   # a range: the upper part lighter
                pg.rect(x + lg(lo), 40.5, lg(hi) - lg(lo), 2.4, fill=C["structure"])
            ex = x + lg(hi)
        else:
            pg.poly([(x, 40.5), (x + bw_, 40.5), (x + bw_, 42.9), (x, 42.9)], stroke=C["accent"], lw=0.3, closed=True,
                    dash=(1.0, 0.8))
            pg.text("no data", x + bw_ / 2, 41.0, 5.5, C["accent"], True, "C")
            ex = x + bw_
        pg.text(cite(src), ex + 1.2, 40.9, 5.5, C["accent"] if not big else C["ink2"], True)
    # walking potential: v1.6 before/after bars (was a sentence); values live from the site board
    mv = L["mv"]
    pg.text("WALKING POTENTIAL", 14, 30, 7.5, C["ink"], True)
    if mv and mv.get("spine_walk_index") is not None:
        pg.text("computed, not a count " + cite(L["mv_src"]), 14, 26.4, 6, C["ink2"])
        pg.text("index 100 = busiest street piece today", 14, 23, 6, C["ink2"])
        rows = [("the spine", mv["spine_walk_index"], SPINE_C),
                ("streets within 40 m of the stream · today", mv.get("edge_walk_today", 0), C["structure"]),
                ("streets within 40 m of the stream · with the spine", mv.get("edge_walk_with", 0), C["water_deep"])]
        bx0 = 150.0
        sc = 150.0 / max([100.0] + [float(r[1] or 0) for r in rows])
        for j, (lab, v, col) in enumerate(rows):
            yy = 29.2 - j * 3.8
            pg.text(lab, bx0 - 2, yy + 0.3, 6, C["ink"], j == 0, "R")
            pg.rect(bx0, yy, max(float(v or 0) * sc, 0.3), 2.4, fill=col)
            pg.text("%.0f" % (v or 0), bx0 + float(v or 0) * sc + 1.2, yy + 0.3, 6.5, C["ink"], True)
        pg.line([(bx0 + 100 * sc, 20.6), (bx0 + 100 * sc, 32.4)], C["ink2"], 0.3, dash=(0.8, 0.8))
        pg.text("100", bx0 + 100 * sc, 33.0, 5.5, C["ink2"], False, "C")
    else:
        pg.text("no data yet · run the site board once " + cite(L["mv_src"]), 14, 26.4, 6.5, C["accent"], True)
    footer(pg)
    return pg

# ------------------------------------------------------------------ page 2: the riverside spine as a strip along the stream
def page_spine(L):
    pg = Page(420, 297)
    SRC_KEY[:] = []                               # v1.6: each page has its own numbered key
    header(pg, "2", "THE RIVERSIDE SPINE",
           "main road crossing to Ulu Cami and Üç Kemer · about 660 m")   # v1.6 keywords; bank and stop ties: drawn below
    c0, c1 = 150, 1800
    x0, w = 22, 384
    X = lambda c: x0 + (c - c0) / float(c1 - c0) * w
    ry0, ry1 = 182, 192                       # the river band
    ne0, sw1 = ry1, ry0                       # north-east bank above, south-west bank below
    pg.rect(x0, ry0, w, ry1 - ry0, fill=C["water"])
    cx0, cx1 = X(CH["cov0"]), X(CH["cov1"])
    pg.rect(cx0, ry0, cx1 - cx0, ry1 - ry0, fill=C["structure"])
    pg.text("covered", (cx0 + cx1) / 2, ry0 + 3.5, 6.5, C["white"], True, "C")
    pg.text("THE SELINOS, FLOWING  >", x0 + 2, ry0 + 3.5, 6.5, C["white"], True)
    pg.text("NORTH-EAST BANK", x0, 252, 7, C["ink2"], True)
    pg.text("SOUTH-WEST BANK", x0, 120, 7, C["ink2"], True)
    pg.text("strip diagram · across: not to scale · along: to scale " + cite(SRC_STRIP), x0 + w, 252, 6, C["ink2"], False, "R")
    # bridges
    for k in ("K4", "K3", "K5", "K6"):
        pg.rect(X(CH[k]) - 1.0, ry0 - 2, 2.0, ry1 - ry0 + 4, fill=C["ink"])
        pg.text(k, X(CH[k]), ry0 - 6.5, 7, C["ink"], True, "C")
    # the main spine, perpendicular
    xs = X(CH["cross"])
    pg.rect(xs - 2.2, 126, 4.4, 124, fill=C["accent"])
    pg.text("MAIN SPINE", xs + 4, 244, 8, C["accent"], True)
    pg.text("Bankalar - Kınık Caddesi", xs + 4, 239.5, 6.5, C["accent"])
    # walking route beyond the spine (Thread 5 details it), and the spine itself
    yb = lambda bank: ne0 + 6 if bank == "NE" else sw1 - 6      # the spine's line on its bank (picked by the data)
    ya, yc, ym = yb(L["sides"]["A"]), yb(L["sides"]["C"]), (ry0 + ry1) / 2.0
    pg.line([(X(c0), ya), (X(CH["K4"]), ya)], C["ink2"], 0.5, dash=(1.5, 1.5))
    pg.line([(X(CH["K5"]), yc), (X(c1), yc)], C["ink2"], 0.5, dash=(1.5, 1.5))
    pg.text("walking route continues upstream", X(c0) + 1, ya + (2 if ya > ry1 else -4), 6, C["ink2"])
    pg.text("walking route continues downstream", X(CH["K5"]) + 3, yc + (2 if yc > ry1 else -4), 6, C["ink2"])
    pg.line([(X(CH["K4"]), ya), (X(CH["K3"]), ya)], SPINE_C, 3.2)
    pg.line([(X(CH["K3"]), ya), (X(CH["cov0"]) + 4, ym), (X(CH["cov1"]) - 4, ym), (X(CH["cov1"]), yc)], SPINE_C, 3.2)
    pg.line([(X(CH["cov1"]), yc), (X(CH["K5"]), yc)], SPINE_C, 3.2)
    pg.text("RIVERSIDE SPINE · ABOUT 660 M " + cite(SRC_PLAN07), X(CH["K4"]) + 2, ya + (4.5 if ya > ry1 else -7.5), 8, SPINE_C, True)
    # heritage anchors
    for i, (c, bank, lab, src) in enumerate(HERITAGE):
        up = bank == "NE"
        y = (228 if i % 2 else 236) if up else (140 if i % 2 else 132)
        pg.line([(X(c), y + (-2 if up else 2)), (X(c), ne0 + 1 if up else sw1 - 1)], C["accent"], 0.25, dash=(0.8, 0.8))
        pg.poly([(X(c) - 1.6, y), (X(c), y + 2.4), (X(c) + 1.6, y), (X(c), y - 2.4)], fill=C["accent"], closed=True)
        pg.text(lab + (" " + cite(SRC_TABAK) if lab == "Tabaklar Hamamı" else ""), X(c), y + (4 if up else -6), 6.5,
                C["accent"], True, "C")
    # functions on their bank
    for f in FUNCS + [dict(EVENTS, ch=1040, bank="bed")]:
        c = f["ch"]
        bank = f["bank"]
        if bank == "spine":                         # on the bank the data picked for its piece
            bank = L["sides"]["A" if c < CH["K3"] else "C"]
        if bank == "NE":
            y = 214
        elif bank == "SW":
            y = 160
        elif f["bank"] == "both":
            y = 214
        elif f["bank"] == "over":
            y = 160
        else:
            y = (ry0 + ry1) / 2.0                  # in the bed
        if y > ry1 or y < ry0:
            pg.line([(X(c), y), (X(c), ry1 if y > ry1 else ry0)], C["ink"], 0.3)
        roundel(pg, X(c), y, f["n"])
        group_dots(pg, X(c) - 3.9, y - 6.5, f["who"], r=1.1)
    # legend for the dots
    lx = 300
    for i, k in enumerate("LTS"):
        pg.poly([(lx + i * 30 + 1.3 * math.cos(a * math.pi / 8), 133 + 1.3 * math.sin(a * math.pi / 8)) for a in range(16)],
                fill=GROUP[k][1], closed=True)
        pg.text(GROUP[k][0], lx + i * 30 + 3, 132, 7, C["ink"], True)
    # flood rule: three levels; v1.6 the rules as pictograms with keywords, wet lines as keywords
    pg.text("WHAT STANDS WHERE: THE FLOOD RULE " + cite(SRC_RULES), 14, 110, 9, C["ink"], True)
    for i, (lev, wet, rules, wsrc) in enumerate(FLOOD):
        y = 100 - i * 11
        pg.rect(14, y - 3, 3, 8, fill=(C["water"], C["water_light"], C["paper"])[i])
        pg.text(lev, 20, y + 1.5, 8, C["ink"], True)
        for j, k in enumerate(wet):
            fit(pg, k + (" " + cite(wsrc) if j == len(wet) - 1 else ""), 20, y - 1.8 - j * 2.8, 5.8, 52, C["ink2"])
        for j, (ic, k) in enumerate(rules):
            icon(pg, ic, 74, y + 4.6 - j * 4.6, 4.2)
            fit(pg, k, 80, y + 1.6 - j * 4.6, 6.8, 85, C["ink"])
    # functions table: v1.6 per stop a pictogram + 2 keyword lines + [n] (was one sentence)
    pg.text("EIGHT STOPS · WHO THEY SERVE AND WHAT THEY GROW FROM", 172, 110, 9, C["ink"], True)
    gx = 290
    for g_ in "WEAH":                            # v1.6: drawn legend of the letter chips
        pg.rect(gx, 109.6, 3.0, 2.6, fill=GROW_C[g_])
        pg.text(g_, gx + 1.5, 110.2, 5, C["white"], True, "C")
        pg.text(GROWS[g_], gx + 4.2, 110.1, 6.5, C["ink"])
        gx += 6.5 + text_w(GROWS[g_], 6.5)
    rows = FUNCS + [EVENTS]
    for i, f in enumerate(rows):
        y = 101 - i * 9.6
        roundel(pg, 175, y + 0.8, f["n"], r=2.6)
        pg.text(f["name"], 180, y + 1.5, 7.5, C["ink"], True)
        fit(pg, f["where"], 180, y - 2.2, 5.8, 62, C["ink2"])
        gx = 180 + min(text_w(f["where"], 5.8), 62) + 1.5     # v1.6: what it grows from as letter chips (legend above)
        for g_ in f["grows"]:
            pg.rect(gx, y - 2.7, 3.0, 2.6, fill=GROW_C[g_])
            pg.text(g_, gx + 1.5, y - 2.1, 5, C["white"], True, "C")
            gx += 3.4
        group_dots(pg, 262, y + 0.6, f["who"], r=1.1)
        icon(pg, f["icon"], 274.5, y + 4.4, 6.5)
        fit(pg, f["kw"][0], 283, y + 1.5, 6.5, 123, C["ink"], True)
        fit(pg, f["kw"][1] + (" " + cite(f["src"]) if f.get("src") else ""), 283, y - 1.9, 6.3, 123 if f is not EVENTS else 52,
            C["ink"])
        if f is EVENTS:                          # the Jul-Sep calendar strip; cleared by October
            for m, ch in enumerate("JFMAMJJASOND"):
                mx = 342 + m * 5.2
                on = m in (6, 7, 8)
                pg.rect(mx, y - 2.6, 4.8, 5.4, fill=C["accent"] if on else C["paper"],
                        stroke=C["ink"] if m == 9 else None, lw=0.3)
                pg.text(ch, mx + 2.4, y - 1.0, 5.5, C["white"] if on else C["ink2"], on, "C")
    # producers' market supply: v1.6 pictogram + live figures (was a sentence)
    ln = L["lands"]
    icon(pg, "farm", 14, 66, 7)
    pg.text("PRODUCERS' MARKET · FED BY THE STORED WATER " + cite(L["wb_src"]), 23, 63.4, 7, C["ink"], True)
    pg.text("%.1f ha fields (%s) · %.2f ha orchards" % (float(ln.get("cropland_ha", 0)), ln.get("cropland_crops", ""),
                                                        float(ln.get("orchard_ha", 0))), 23, 59.4, 8, SPINE_C, True)
    pg.text("not designed here: edge · decks · stall sizes " + cite(SRC_T5), 14, 54.2, 6.5, C["ink2"], True)
    pg.text("bed/bank structures: DSİ + Conservation Council approval " + cite("s14"), 14, 50.8, 6.5, C["ink2"])
    # which bank: v1.6 paired bars NE / SW per piece (people = home floors, modern = buildings of 3+ floors, within 250 m)
    yy = 45.4
    pg.text("WHICH BANK · THE DATA (within 250 m of the stream)", 14, yy, 8, C["ink"], True)
    pg.text("home floors", 20, yy - 3.8, 5.5, C["ink2"], True)
    pg.text("buildings of 3+ floors", 84, yy - 3.8, 5.5, C["ink2"], True)
    pg.text("bank", 122, yy - 3.8, 5.5, C["ink2"], True)
    fmax = max([1.0] + [float(L["votes"][pc["id"]][b]["people_floors"]) for pc in SPINE for b in ("NE", "SW")])
    mmax = max([1.0] + [float(L["votes"][pc["id"]][b]["modern_3plus"]) for pc in SPINE for b in ("NE", "SW")])
    yy -= 8.6
    for pc in SPINE:
        v = L["votes"][pc["id"]]
        bank, why = bank_of(v)
        auto = pc.get("side") == "auto"
        pg.text(pc["id"], 14, yy - 1.4, 8, SPINE_C if auto else C["ink"], True)
        for j, b in enumerate(("NE", "SW")):
            by_ = yy + 0.4 - j * 2.4
            col = SPINE_C if (auto and b == bank) else C["structure"]
            fw = 46.0 * float(v[b]["people_floors"]) / fmax
            mw = 24.0 * float(v[b]["modern_3plus"]) / mmax
            pg.rect(20, by_, max(fw, 0.3), 1.9, fill=col)
            pg.text("%s %s" % (b, fmt(v[b]["people_floors"])), 21 + fw, by_ + 0.3, 5, C["ink"])
            pg.rect(84, by_, max(mw, 0.3), 1.9, fill=col)
            pg.text("%s %d" % (b, v[b]["modern_3plus"]), 85 + mw, by_ + 0.3, 5, C["ink"])
        if auto:
            pg.text("-> " + {"NE": "north-east", "SW": "south-west"}[bank] + " bank", 122, yy + 0.6, 6.3, SPINE_C, True)
            fit(pg, why, 122, yy - 2.0, 5, 43, C["ink2"])
        else:
            pg.text("-> over the covered stream", 122, yy + 0.6, 6.3, C["ink"], True)
            pg.text("reaches both", 122, yy - 2.0, 5, C["ink2"])
        yy -= 5.6
    pg.text("floors: proxy for residents (no mahalle populations yet) " + cite(L["vote_src"]), 14, yy + 0.6, 5.5,
            C["ink2"])
    footer(pg)
    return pg

# ------------------------------------------------------------------ build and run
def results(L=None):
    return dict(spine_banks=(L or {}).get("sides"), bank_votes=(L or {}).get("votes"), bank_vote_source=(L or {}).get("vote_src"),
                script="bergama_city_link_v1_6.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                spine=SPINE, functions=[dict((k, f.get(k)) for k in ("n", "name", "where", "xy", "stage", "who", "grows", "ch", "bank"))
                                        for f in FUNCS + [EVENTS]],
                chainage=CH, main_spine=MAIN_SPINE,
                note="survey coordinates (m); spine offsets are schematic for the movement network")

def build(dir_):
    L = live()
    # 25 Oct 10:19 (no double runs): the site board and masterplan ran BEFORE this script and drew the spine from the
    # last city_link_results.json (or their built-in copy). The bank choice comes from survey building counts, so it
    # only changes when the survey changes; if it did change, say so (one more press of the chain fixes the drawings).
    try:
        with open(os.path.join(dir_, OUT_JSON), "r", encoding="utf-8") as f:
            prev, prev_src = json.load(f).get("spine_banks"), "the last run"
    except Exception:
        prev = dict((pc["id"], bank_of(BANK_VOTE[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
        prev_src = "the built-in copy"
    L["bank_note"] = ("" if prev == L["sides"] else
                      "\nWARNING: the spine bank changed from %s (%s -> %s): the site board and masterplan of this run drew "
                      "the old one; press the chain once more." % (prev_src, prev, L["sides"]))
    write_pdf([page_why(L), page_spine(L)], os.path.join(dir_, OUT_PDF))
    with open(os.path.join(dir_, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(results(L), f, ensure_ascii=False, indent=1)
    return L

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        L = build(OUT_DIR)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + os.path.join(OUT_DIR, OUT_PDF)
    t = time.strftime("%H:%M:%S")
    return "%s  %s\n%s  %s\nfigures: %s; %s\ncity link %s, %.1f s%s" % (OUT_PDF, t, OUT_JSON, t, L["wb_src"], L["mv_src"], VERSION, time.time() - t0, L.get("bank_note", ""))

#@include ../common/chain_fire.py


#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed = any(v is True for k, v in list(globals().items()) if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, "bergama_city_link_log_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_city_link_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_city_link_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_city_link_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_city_link_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_city_link_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
    done = _sc.sticky.get("bergama_city_link_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_city_link_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "CityLink " + VERSION + " · " + _sc.sticky.get("bergama_city_link_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
