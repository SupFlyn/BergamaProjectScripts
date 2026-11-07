"""Offline check of v9.1+: run the B19 script with the fake Rhino, then write the pieces exactly as Rhino is given them
(no see-through, fade flattened) through the script's own PDF writer. usage: flat_check.py <script> <fake_home> <out.pdf>"""
import os, sys
os.environ["BERGAMA_TEST_FLAT"] = "1"
out = sys.argv.pop(3)
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_gh.py")).read(), "run_gh.py", "exec"))
L = g["_B91_FLAT"]
sh = g["_B7_SHEET"]
pg = g["Page"](sh["W"], sh["H"])
pg.items = list(L)
print("pieces", len(L), "see-through left", sum(1 for it in L if it[0] == "poly" and it[7] is not None))
g["b8_write_pdf"](pg, out, "flat check")
