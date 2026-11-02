# ---- composer core: includes (round 5, S1, 1 Nov 2026; G-R5-12, PLAN §6 "schema + composer core") -------------------
# S10 puts ONE line "#@include parts/00_core.py" into code.py (after its imports and VERSION, PT globals) and removes
# code.py's own includes of the common files below (a file included twice is harmless, but keep one). Order matters:
# write_pdf needs the globals VERSION and PT (mm per pt) from code.py. warn.py before text_place.py (one warning list), pdf_fonts before font_metrics, grid before text_place.
import math, zlib
#@include ../../common/warn.py
#@include ../../common/bergama_paths.py
#@include ../../common/grid.py
#@include ../../common/pdf_fonts.py
_ENC_EXTRA = dict(_PF_EXTRA)          # pdf_str's six Turkish slots (the same table as the sheets')
#@include ../../common/font_metrics.py
#@include ../../common/text_place.py
#@include ../../common/trigger.py
#@include ../../common/hex_rgb.py
#@include ../../common/_f.py
#@include ../../common/pdf_str.py
#@include ../../common/page_stream.py
#@include ../../common/write_pdf.py
#@include 10_load.py
#@include 20_scale.py
#@include 30_render.py
#@include 40_set.py
#@include 50_place.py
#@include 60_layout.py
#@include 70_check.py
