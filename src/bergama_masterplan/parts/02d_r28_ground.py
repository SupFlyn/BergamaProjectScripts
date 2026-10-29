# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.23 the masterplan (v28: the open ground page is gone); the frame
# area (G10) (worker MP-plan). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, MP-plan). Both pages are crops drawn for the booklet panel (BK_W x BK_H = 392 x 238 mm) at 1:1:
#   * G7: the whole analysis frame (site_alan, 2,845 x 529 m) as ONE strip at 1:10,000 (284.5 x 52.9 mm; 1:5,000 would
#     need 569 mm), the water left to right, at the top-left; no halves, no "continues below".
#   * G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE on both, R28_STUDY_NAME in the legend; the strip's
#     edge is the analysis frame, named (R28_FRAME_NAME) only on p.21, where figures are counted over it.
#   * G10: ONE frame figure, the frame polygon's area; the grid counts only cells whose centre lies inside the frame
#     (pl28_frame_stats); every figure on p.21 and in r28_open_ground.json comes from that one count.
#   * P21.1: every open-ground category in its own R28_OPEN colour, the no-plant-cover hatch too; bars in the map's
#     colours.
#   * P23.1 / P23.2: the numbered markers in their R28_MARKERS group colour, placed by common/label_place.py (G4); the
#     list under the strip by group: coloured number, name, one short line. The reasons and source codes go to the
#     booklet's sources page (blocks.json and booklet/results.json "plan_sources"). The areas left as they are (no
#     intervention) get a grey letter on the plan and one line in the list (their two-line notes do not fit at
#     1:10,000).
PL28_TS, PL28_HEAD_TS = 2.65, 2.82   # booklet label 7.5 pt and kicker 8 pt (PLAN §2), mm
PL28_MARKS = (0.0, 100.0, 200.0, 500.0)   # the scale bar at 1:10,000, m (50 mm)
PL28_NI_R = 1.6                  # the letters of the areas left as they are, radius mm
PL28_HUB = {u"K4": u"K4 · Ulucami Önü", u"K3": u"K3 · Tabak", u"İstiklal": u"İstiklal Meydanı",
            u"Kızıl Avlu": u"Kızıl Avlu", u"K5": u"K5 · Üç Kemer", u"K6": u"K6"}   # list names (HUB_NAME, sentence case)
PL28_SRC_TAG = re.compile(u"\\s*\\((survey|satellite 2021|satellite check)\\)")   # source tags of the no-go reasons
PL28_SRC_NAME = {u"survey": u"survey (Bergama_Altlik.3dm)", u"satellite 2021": u"ESA WorldCover 2021",
                 u"satellite check": u"satellite check (OPEN_CHECK)"}


# v28 (revision 29 Oct, WO-T4b-1): ground_page (crop mp_max_area, the open ground page) is gone with p.22 (D1 a:
# merged into the site board's p.06), and with it r28_open_ground.json (no reader since site board v51).
