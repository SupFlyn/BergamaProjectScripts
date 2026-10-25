"""Offline check of the booklet on a chain run (no Rhino): python3 src/bergama_booklet/test_assemble.py <run dir> <out dir>
<run dir> = a tools/chain.sh output folder (its Downloads/Bergama/output/ holds the scripts' booklet assets).
Prints the assembler log: missing assets, labels that overlap or leave their frame, text left inside drawing PDFs,
type below 7 pt, text that does not fit, repeated text. For checking only: Aras builds the real booklet in Rhino."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
dist = os.path.join(HERE, "..", "..", "dist", open(os.path.join(HERE, "target.txt")).read().strip())
src = open(dist, encoding="utf-8").read().replace("else:\n    print(write_log(main()))", "else:\n    pass")
g = {"__name__": "booklet_test"}
exec(compile(src, dist, "exec"), g)
g["ASSET_ROOT"] = os.path.join(os.path.abspath(sys.argv[1]), "Downloads", "Bergama", "output")
g["OUT_DIR"] = os.path.abspath(sys.argv[2])
print(g["main"]())
