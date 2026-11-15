# -*- coding: utf-8 -*-
"""Bergama Group 6: MASTER PRINT v1 (15 Nov 2026). Aras 20:45-20:50 UTC: "many of the things from masterplan is
missing", "river fill is failed ... we lost ground fills", "use one from open source browsers ... really good svg
reading engine", "yeah take chromium svg reader".

Prints his masterplan (Downloads/Bergama/Data/assets/plan/master.svg) ONCE to a vector PDF with the laptop's Chromium
(Microsoft Edge, or Chrome), so every picture, texture, pattern, gradient and clip of his file comes out as a browser
draws it. Pages (pages_common v3.36 pc_masterplan) then place that PDF cut to the working area. Run it again only
when master.svg changes. Runs OUTSIDE Rhino:  py -3 bergama_master_print_v1.py   (it may take many minutes)

Writes cached/bergama_masterplanbase/: master_print.pdf, master_print.stamp (master.svg size/time + viewBox),
master_print.svg + master_print_img/ (his embedded pictures as files, so the browser reads a smaller SVG).
"""
import os, re, sys, json, time, base64, subprocess

VERSION = "v1"
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
SVG = os.path.join(ROOT, "Data", "assets", "plan", "master.svg")
CDIR = os.path.join(ROOT, "cached", "bergama_masterplanbase")
BROWSERS = (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
TIMEOUT_S = 3600


def main():
    t0 = time.time()
    if not os.path.isfile(SVG):
        return "STOP: %s missing (run MasterplanAI first)" % SVG
    exe = next((b for b in BROWSERS if os.path.isfile(b)), None)
    if not exe:
        return "STOP: no Edge or Chrome found in %s" % ", ".join(BROWSERS)
    os.makedirs(CDIR, exist_ok=True)
    with open(SVG, "rb") as f:
        raw = f.read()
    m = re.search(rb'<svg\b[^>]*?\bviewBox="([^"]+)"', raw[:20000], re.S)
    if not m:
        return "STOP: master.svg has no viewBox"
    vb = [float(v) for v in re.split(r"[\s,]+", m.group(1).decode().strip())[:4]]
    stamp = "%d/%d" % (os.path.getsize(SVG), int(os.path.getmtime(SVG)))
    idir = os.path.join(CDIR, "master_print_img")
    os.makedirs(idir, exist_ok=True)
    n = [0]

    def out(mm):
        n[0] += 1
        fn = "i%03d.%s" % (n[0], "png" if mm.group(2) == b"png" else "jpg")
        with open(os.path.join(idir, fn), "wb") as g:
            g.write(base64.b64decode(re.sub(rb"\s+", b"", mm.group(3))))
        return mm.group(1) + b'"master_print_img/' + fn.encode() + b'"'
    mb0 = len(raw) / 1e6
    raw = re.sub(rb'((?:xlink:)?href=)"data:image/(png|jpeg|jpg);base64,([^"]*)"', out, raw)
    with open(os.path.join(CDIR, "master_print.svg"), "wb") as f:
        f.write(raw)
    print("pictures kept as files: %d (SVG %.0f MB -> %.0f MB)" % (n[0], mb0, len(raw) / 1e6), flush=True)
    raw = None
    html = os.path.join(CDIR, "master_print.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><style>@page{size:%.4fpx %.4fpx;margin:0}html,body{margin:0;padding:0}"
                "object{display:block;width:%.4fpx;height:%.4fpx}</style></head><body><object type=\"image/svg+xml\" "
                "data=\"master_print.svg\"></object></body></html>" % (vb[2], vb[3], vb[2], vb[3]))
    pdf = os.path.join(CDIR, "master_print.pdf")
    stp = os.path.join(CDIR, "master_print.stamp")
    for p in (pdf, stp):
        if os.path.isfile(p):
            os.remove(p)
    print("printing with %s (up to %d min) ..." % (os.path.basename(exe), TIMEOUT_S // 60), flush=True)
    try:
        subprocess.run([exe, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                        "--print-to-pdf=" + pdf, "file:///" + html.replace("\\", "/")],
                       capture_output=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/F", "/IM", os.path.basename(exe)], capture_output=True)
        return "FLAG: the browser did not finish in %d min; pages keep the vector masterplan" % (TIMEOUT_S // 60)
    if not os.path.isfile(pdf) or os.path.getsize(pdf) < 1000:
        return "FLAG: the browser wrote no PDF; pages keep the vector masterplan"
    note = ""
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        d = fitz.open(pdf)
        r = d[0].rect
        note = "; %d page(s), %.1f x %.1f pt (expected %.1f x %.1f)" % (d.page_count, r.width, r.height,
                                                                       vb[2] * 0.75, vb[3] * 0.75)
        if d.page_count != 1 or abs(r.width - vb[2] * 0.75) > 2 or abs(r.height - vb[3] * 0.75) > 2:
            return "FLAG: the printed page is not his artboard%s; pages keep the vector masterplan" % note
    except Exception as ex:
        note = "; not checked (%s)" % type(ex).__name__
    with open(stp, "w", encoding="utf-8") as f:
        json.dump({"stamp": stamp, "viewbox": vb, "browser": exe, "made": time.strftime("%Y-%m-%d %H:%M")}, f)
    return "MasterPrint %s: %s (%.1f MB) in %.0f s%s" % (VERSION, pdf, os.path.getsize(pdf) / 1e6, time.time() - t0,
                                                       note)


if __name__ == "__main__":
    print(main())
