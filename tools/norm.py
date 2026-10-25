"""Print a file with run-specific bits normalised, for compare.sh: the run folder, mock ids, object addresses.
PDF content streams are inflated first, so paths written inside a PDF are normalised too.
usage: python3 tools/norm.py <file> <run folder>"""
import sys, re, zlib
f, run = sys.argv[1], sys.argv[2].encode()
b = open(f, "rb").read()
if f.endswith(".pdf"):
    def infl(m):
        try: return b"stream\n" + zlib.decompress(m.group(1)) + b"\nendstream"
        except Exception: return m.group(0)
    b = re.sub(rb"stream\r?\n(.*?)\r?\nendstream", infl, b, flags=re.S)
    b = re.sub(rb"/Length \d+", b"/Length N", b)
    b = re.sub(rb"\d{10} 00000 n", b"OFFSET 00000 n", b)
    b = re.sub(rb"startxref\s+\d+", b"startxref N", b)
b = b.replace(run, b"RUN")
b = re.sub(rb"id='\d+'", b"id=X", b); b = re.sub(rb"0x[0-9a-f]{6,}", b"0xX", b)
sys.stdout.buffer.write(b)
