"""Exit 0 when two PDFs show the same thing: same page count, same text, same pixels at 50 dpi (PyMuPDF).
For PDFs whose bytes differ between identical runs (PyMuPDF writes its own ids). usage: pdfsame.py a.pdf b.pdf"""
import sys, warnings
warnings.simplefilter("ignore")
try:
    import pymupdf as fitz
except ImportError:
    import fitz
a, b = fitz.open(sys.argv[1]), fitz.open(sys.argv[2])
if len(a) != len(b): print("pages %d vs %d" % (len(a), len(b))); sys.exit(1)
for i, (p, q) in enumerate(zip(a, b)):
    if p.get_text() != q.get_text(): print("page %d: text differs" % (i + 1)); sys.exit(1)
    if p.get_pixmap(dpi=50).samples != q.get_pixmap(dpi=50).samples: print("page %d: drawing differs" % (i + 1)); sys.exit(1)
sys.exit(0)
