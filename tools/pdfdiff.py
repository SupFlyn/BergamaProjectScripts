"""Show where two PDFs written by the Bergama scripts differ (content streams inflated, first differing lines).
usage: python3 tools/pdfdiff.py a.pdf b.pdf"""
import sys, re, zlib, difflib
def streams(p):
    b = open(p, "rb").read(); out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", b, re.S):
        s = m.group(1)
        try: s = zlib.decompress(s)
        except Exception: pass
        out.append(s.decode("latin-1"))
    return out
A, B = streams(sys.argv[1]), streams(sys.argv[2])
print("streams", len(A), len(B))
for i, (a, b) in enumerate(zip(A, B)):
    if a != b:
        d = list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0))
        print("stream %d: %d differing lines" % (i, sum(1 for x in d if x[:1] in "+-") - 2)); print("\n".join(d[2:12]))
