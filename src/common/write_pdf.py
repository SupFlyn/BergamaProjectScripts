def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    add.objs = objs                                       # G6-9: _wp_set_obj fills a reserved object later
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    xo_res = ""
    if getattr(pg, "grouped", False) or getattr(pg, "grp", None) is not None or any(it[0] == "grp" for it in pg.items):   # G6-9 (round 6): nested groups
        stream, xo = _wp_group_stream(pg, add, font, gs_res, title)
        xo_res = " /XObject << {} >>".format(" ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo)) if xo else ""
    elif any(it[0] == "image" for it in pg.items):        # D1 a (30 Oct): raster cutouts between the vector items
        stream, xo = _wp_image_stream(pg, add)
        xo_res = " /XObject << {} >>".format(" ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo)) if xo else ""
    else:
        stream = page_stream(pg)
    data = zlib.compress(stream, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>{} >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                font[0], font[1], gs_res, xo_res).encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))


# ---- images in the page (H-B, 30 Oct 2026; D1 a: layered raster collage) ------------------------------------------
# A page item ("image", x, y, w, h, path, alpha, flip, clip) puts a PNG (with or without alpha) or a JPEG at x, y
# (lower left, page mm, y up), w x h mm (the caller keeps the proportions), alpha 0-1 or None, flip True = mirrored,
# clip None or (x0, y0, x1, y1) mm. figures.py cut_image() makes these items; section_frame.py shp_put() puts them on
# a page (pg.items). The items are drawn in their place among the vector items (the order of pg.items = the layer
# order). Pages without an image item are written exactly as before. An unreadable image is skipped (WP_IMG_LOG).
# PNG: 8 or 16 bit, grey / grey+alpha / RGB / RGBA / palette (+tRNS), not interlaced; the alpha becomes an SMask.
WP_IMG_LOG = []


def _wp_png(path):
    """(w, h, colour bytes, n colours 1|3, alpha bytes or None) of a PNG, or None"""
    import struct as _st
    with open(path, "rb") as f:
        d = f.read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _st.unpack(">IIBBBBB", c[:13])
        elif t == b"PLTE":
            plte = c
        elif t == b"tRNS":
            trns = c
        elif t == b"IDAT":
            idat.append(c)
        elif t == b"IEND":
            break
    if not hdr:
        return None
    w, h, bd, ct, _cm, _fm, il = hdr
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None or il or bd not in (8, 16) or (ct == 3 and bd != 8):
        return None
    bpp = ch * bd // 8
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        ft = raw[i]
        ln = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ft == 1:
            for x in range(bpp, stride):
                ln[x] = (ln[x] + ln[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                ln[x] = (ln[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                ln[x] = (ln[x] + (((ln[x - bpp] if x >= bpp else 0) + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = ln[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                ln[x] = (ln[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        out[y * stride:(y + 1) * stride] = ln
        prev = ln
    if bd == 16:                                          # keep the high byte of every sample
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        return w, h, bytes(rgb), 3, alpha
    if ct == 0:
        return w, h, bytes(out), 1, None
    if ct == 4:
        return w, h, bytes(out[0::2]), 1, bytes(out[1::2])
    if ct == 2:
        return w, h, bytes(out), 3, None
    rgb = bytearray(n * 3)
    rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
    alpha = bytes(out[3::4])
    return w, h, bytes(rgb), 3, (None if alpha.count(b"\xff") == n else alpha)


def _wp_jpeg(d):
    """(w, h, n colours) of a baseline / progressive JPEG, or None"""
    if d[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(d):
        if d[i] != 0xFF:
            return None
        m = d[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6], d[i + 9]
        i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def _wp_image_obj(path, add):
    """the XObject id of one image file (PNG with its SMask, or JPEG), or None"""
    try:
        with open(path, "rb") as f:
            head = f.read(4)
        if head == b"\x89PNG":
            r = _wp_png(path)
            if not r:
                WP_IMG_LOG.append(u"image %s: PNG type not supported (interlaced or < 8 bit)" % path)
                return None
            w, h, col, nc, alpha = r
            sm = ""
            if alpha is not None:
                a = zlib.compress(alpha, 6)
                sid = add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /DeviceGray "
                           "/BitsPerComponent 8 /Filter /FlateDecode /Length {} >>\nstream\n".format(w, h, len(a))
                           ).encode("latin-1") + a + b"\nendstream")
                sm = " /SMask {} 0 R".format(sid)
            c = zlib.compress(col, 6)
            return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8"
                        "{} /Filter /FlateDecode /Length {} >>\nstream\n".format(
                            w, h, "DeviceRGB" if nc == 3 else "DeviceGray", sm, len(c))).encode("latin-1") + c +
                       b"\nendstream")
        with open(path, "rb") as f:
            d = f.read()
        info = _wp_jpeg(d)
        if not info:
            WP_IMG_LOG.append(u"image %s: neither PNG nor JPEG" % path)
            return None
        w, h, nc = info
        return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                    "/Filter /DCTDecode /Length {} >>\nstream\n".format(
                        w, h, {1: "DeviceGray", 4: "DeviceCMYK"}.get(nc, "DeviceRGB"), len(d))).encode("latin-1") + d +
                   b"\nendstream")
    except Exception as ex:
        WP_IMG_LOG.append(u"image %s: %s" % (path, type(ex).__name__))
        return None


def _wp_image_stream(pg, add):
    """(content stream, [(name, id)]): runs of vector items through page_stream (each in q ... Q), the images
    between them in their order; one XObject per file"""
    names, xo = {}, []
    return _wp_run(pg.items, pg.W, pg.H, add, names, xo), xo


def _wp_run(items, W, H, add, names, xo):
    """the content stream of items in their order: vector runs through page_stream (each in q ... Q), images as
    XObjects (names: file -> name or None, shared by the whole PDF; xo collects [(name, id)]); "grp" markers skipped"""
    class _Run(object):
        pass
    parts, run = [], []

    def flush():
        if run:
            r = _Run()
            r.W, r.H, r.items = W, H, list(run)
            parts.append(b"q\n" + page_stream(r) + b"\nQ")
            del run[:]
    for it in items:
        if it[0] == "grp":
            continue
        if it[0] != "image":
            run.append(it)
            continue
        flush()
        x, y, w, h, p = it[1:6]
        alpha = it[6] if len(it) > 6 else None
        flip = it[7] if len(it) > 7 else False
        clip = it[8] if len(it) > 8 else None
        if p not in names:
            oid = _wp_image_obj(p, add)
            names[p] = None if oid is None else "Im%d" % (len(xo) + 1)
            if oid is not None:
                xo.append((names[p], oid))
        if names[p] is None or w <= 0 or h <= 0:
            continue
        ops = ["q 2.834646 0 0 2.834646 0 0 cm"]
        if alpha is not None and alpha < 0.975:
            ops.append("/A{:02d} gs".format(max(1, min(19, int(round(alpha * 20))))))
        if clip:
            ops.append("{} {} {} {} re W n".format(_f(clip[0]), _f(clip[1]), _f(clip[2] - clip[0]), _f(clip[3] - clip[1])))
        ops.append("{} 0 0 {} {} {} cm /{} Do Q".format(_f(-w if flip else w), _f(h), _f(x + w if flip else x), _f(y),
                                                       names[p]))
        parts.append(" ".join(ops).encode("latin-1"))
    flush()
    return b"\n".join(parts)


# ---- G6-9 nested groups (round 6, S2, 4 Nov 2026; Aras 17:50-17:51: "every tree its own group inside one Trees
# group ... apply this to everything") -------------------------------------------------------------------------------
# A page item ("grp", "<kind>/<element id>") opens a group for the items after it; ("grp", None) closes it (made by
# item_export.py ix_grp / ix_tag; page_stream and xform pass over them). When pg.items holds such markers, or the caller
# sets pg.grouped = True (the booklet's drawings, 30_render), write_pdf writes every element as its own Form XObject
# inside one Form XObject of its kind, in draw order. Illustrator opens a Form XObject as a group (UNVERIFIED here:
# never run; Aras checks "groups in Illustrator"), so a booklet drawing (itself one Form XObject via show_pdf_page)
# opens as Drawing > Trees > tree. Each group's name is also written as marked content (/G69 <</Name (...)>> BDC ...
# EMC) for readers that list it. Draw order is never changed: a kind that comes back after another kind starts a
# second group of that kind (counted as repeats in the log). Items under no open group go to kind "other" (one element
# per run) + one WARNING per drawing.
#   wp_grp_of(shape) -> "<kind>/<id>" or None   the group of an items.json shape dict (Ix stamps "grp" on every
#                                               shape at export, item_export.py)
#   wp_groups_log(page) -> "groups <page> kinds=n elements=n untagged=n"   one line per page (after its drawings)
# Two ways to tag, same result: markers in pg.items, or pg.grp = a list parallel to pg.items ("<kind>/<id>" or None
# each; the booklet's form, S9) with pg.grp_root = the drawing id (its name, marked content round the kinds).
# Stats key: pg.page if set, else the PDF title.
WP_GRP_STATS = {}           # page -> dict(kinds=set, elements=n, untagged=n, repeats=n, drawings=n)


def wp_grp_of(shape):
    return (shape.get("grp") or None) if isinstance(shape, dict) else None


def wp_groups_log(page):
    st = WP_GRP_STATS.get(page)
    if not st:
        return u"groups %s kinds=0 elements=0 untagged=0" % page
    return u"groups %s kinds=%d elements=%d untagged=%d%s" % (
        page, len(st["kinds"]), st["elements"], st["untagged"],
        u" repeats=%d" % st["repeats"] if st["repeats"] else u"")


def _wp_split_grp(g, n):
    g = u"%s" % g
    if "/" in g:
        k, e = g.split("/", 1)
        return (k.strip() or "other"), (e.strip() or u"%s %d" % (k, n))
    return g, u"%s %d" % (g, n)


def _wp_set_obj(add, oid, b):
    add.objs[oid - 1] = b


def _wp_group_stream(pg, add, font, gs_res, title=None):
    """(page content stream, [(name, id)] for the page's /XObject): kinds and elements as nested Form XObjects"""
    seq = pg.items
    pgrp = getattr(pg, "grp", None)
    if pgrp is not None:                                  # S9 form: pg.grp parallel to pg.items (str or None each)
        seq = []
        for i_, it in enumerate(pg.items):
            seq.append(("grp", pgrp[i_] if i_ < len(pgrp) else None))
            seq.append(it)
    runs, cur, buf, untagged = [], None, [], 0
    for it in seq:
        if it[0] == "grp":
            g = it[1] if len(it) > 1 and it[1] else None
            if g != cur:
                if buf:
                    runs.append((cur, buf))
                    buf = []
                cur = g
            continue
        buf.append(it)
        if cur is None:
            untagged += 1
    if buf:
        runs.append((cur, buf))
    kinds, n_other = [], 0                                # [[kind, [(element name, items)]]] consecutive by kind
    for g, its in runs:
        if g is None:
            n_other += 1
            k, e = "other", u"other %d" % n_other
        else:
            k, e = _wp_split_grp(g, len(runs))
        if kinds and kinds[-1][0] == k:
            kinds[-1][1].append((e, its))
        else:
            kinds.append([k, [(e, its)]])
    bbox = "[0 0 {} {}]".format(_f(pg.W / PT), _f(pg.H / PT))
    base_id = add(b"")
    names, img = {}, []

    def form(stream, res_id):
        data = zlib.compress(stream, 6)
        return add(("<< /Type /XObject /Subtype /Form /BBox {} /Resources {} 0 R /Length {} /Filter /FlateDecode >>"
                    "\nstream\n".format(bbox, res_id, len(data))).encode("latin-1") + data + b"\nendstream")

    def mc(name, xname):
        return b"/G69 << /Name " + pdf_str(name) + b" >> BDC /" + xname.encode("latin-1") + b" Do EMC"
    el_ids = []                                           # per kind: [(E name, id, element name)]
    n_el = 0
    for k, els in kinds:
        row = []
        for e, its in els:
            n_el += 1
            row.append(("E%d" % n_el, form(_wp_run(its, pg.W, pg.H, add, names, img), base_id), e))
        el_ids.append(row)
    base = "/Font << /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>".format(font[0], font[1], gs_res)
    img_res = " ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in img)
    objs_base = "<< {}{} >>".format(base, " /XObject << {} >>".format(img_res) if img_res else "")
    _wp_set_obj(add, base_id, objs_base.encode("latin-1"))
    page_xo, parts, seen = list(img), [], {}
    for i, (k, els) in enumerate(kinds):
        row = el_ids[i]
        res = add("<< {} /XObject << {} {} >> >>".format(base, img_res, " ".join(
            "/{} {} 0 R".format(n_, o_) for n_, o_, _e in row)).encode("latin-1"))
        kid = form(b"\n".join(mc(e, n_) for n_, _o, e in row), res)
        kn = "K%d" % (i + 1)
        page_xo.append((kn, kid))
        seen[k] = seen.get(k, 0) + 1
        parts.append(mc(k, kn))
    key = getattr(pg, "page", None) or (u"%s" % title if title else "page")
    st = WP_GRP_STATS.setdefault(key, dict(kinds=set(), elements=0, untagged=0, repeats=0, drawings=0))
    st["kinds"].update(seen)
    st["elements"] += n_el
    st["untagged"] += untagged
    st["repeats"] += sum(v - 1 for v in seen.values())
    st["drawings"] += 1
    if untagged:
        msg = u"%s: %d item(s) with no group went to kind \"other\" (G6-9: tag them with ix_grp at the point of " \
              u"drawing)" % (title or key, untagged)
        if "wn_warn" in globals():
            wn_warn(key, "groups", msg)                                                         # noqa: F821
        else:
            WP_IMG_LOG.append(msg)
    root = getattr(pg, "grp_root", None)
    if root:                                              # the drawing's own name round its kinds (no extra form:
        parts = [b"/G69 << /Name " + pdf_str(u"%s" % root) + b" >> BDC"] + parts + [b"EMC"]   # show_pdf_page's
    return b"\n".join(parts), page_xo                    # Form XObject is the drawing group)
