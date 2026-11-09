# ---- 30_render (composer core, round 5 S1; G-R5-12): an exported drawing drawn on the booklet page at its scale -------
# The drawing's layers (in z order, then export order) become one small vector PDF of exactly the drawing's printed
# size (the common write_pdf: polygons with holes, lines, circles, see-through, images), which is then set on the page
# 1:1 with PyMuPDF show_pdf_page: geometry is scaled from drawing units to page mm, line widths and dashes stay PRINT
# sizes (never scaled, unlike xform), and the page box clips everything outside the extent. No text is drawn here:
# every text is a text item set by 40_set / 50_place (a "text" shape left in a layer is a WARNING and is skipped).
#   rd_drawing(P, D, T, frame=None) -> placed     draws D with transform T (20_scale BkT) on BkPage P; registers the
#                                                 drawing rect as a TextPage block + keep (kind "drawing", name = its
#                                                 id: only its own labels may sit on it) and its keep_areas as keeps;
#                                                 placed = dict(D, T, rect, den, id) also kept in P.placed
#                                                 frame = None | (colour, width_pt): a thin frame round the rect (insets)
#   rd_close()                                    closes the temporary PDFs (after the booklet is saved)
# Temporary files: Downloads/Bergama/cached/booklet/_render/<page>_<id>.pdf (overwritten each run).
# v31 (round 6 S9, G6-9 "every element its own group inside its kind group inside its drawing group"): each shape's
# "grp" ("<kind>/<element id>", common/item_export.py §2.8) is handed to write_pdf as pg.grp, a list parallel to
# pg.items (None = untagged), with pg.grp_root = the drawing id; write_pdf (S2) writes drawing > kind > element as
# nested groups. The drawing PDF is then set on the page as one Form XObject (show_pdf_page) = the drawing's group.
# Counts per page go to BK_GRP (log "groups <page> kinds=<n> elements=<n> untagged=<n>", 82_compose).
BK_K = 72.0 / 25.4          # pt per mm
RD_DOCS = []
BK_GRP = {}                 # page -> dict(kinds=set, elements=set, untagged=n)    (G6-9 log line)


class _RdPg(object):
    pass


def _rd_img_path(f):
    if not f:
        return f
    if os.path.isabs(f):
        return f
    for base in (os.path.join(BERGAMA_ROOT, "Data"), BERGAMA_ROOT):
        p = os.path.join(base, f)
        if os.path.isfile(p):
            return p
    return f


def rd_items(D, T, page=None, grp=None):
    """D's shapes as write_pdf page items in mm, y up from the drawing's lower-left corner; grp (a list) gets each
    item's "grp" tag (G6-9), parallel to the items"""
    e, k = T.e, T.k
    mm = 25.4 / 72.0

    def P(p):
        return ((float(p[0]) - e[0]) * k, (float(p[1]) - e[1]) * k)
    out, skipped = [], 0
    for L in sorted(D.get("layers") or [], key=lambda L: L.get("z", 0)):
        for s in L.get("shapes") or []:
            n0 = len(out)
            t = s.get("t") or s.get("type")         # Ix writes "t", the key-map module (S2) "type"
            if t == "poly":
                rings = [[P(p) for p in r] for r in s.get("rings") or [] if len(r) >= 3]
                if rings and (s.get("fill") or s.get("stroke")):
                    out.append(("poly", rings, s.get("fill"), s.get("stroke"), (s.get("width_pt") or 0.0) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, None, s.get("opacity")))
            elif t == "line":
                pts = [P(p) for p in s.get("pts") or []]
                if len(pts) >= 2 and s.get("stroke"):
                    out.append(("line", pts, s["stroke"], (s.get("width_pt") or 0.25) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, s.get("cap", 1)))
            elif t == "circle":
                cx, cy = P(s["c"])
                r = s["r_mm"] if s.get("r_mm") is not None else float(s.get("r") or 0.0) * k
                if r > 0 and (s.get("fill") or s.get("stroke")):
                    out.append(("circle", cx, cy, r, s.get("fill"), s.get("stroke"), (s.get("width_pt") or 0.0) * mm))
            elif t == "image":
                b = s.get("box") or [0, 0, 0, 0]
                x0, y0 = P(b[:2])
                x1, y1 = P(b[2:4])
                c = s.get("clip")
                clip = None
                if c:
                    cx0, cy0 = P(c[:2])
                    cx1, cy1 = P(c[2:4])
                    clip = (min(cx0, cx1), min(cy0, cy1), max(cx0, cx1), max(cy0, cy1))
                out.append(("image", min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0), _rd_img_path(s.get("file")),
                            s.get("opacity"), bool(s.get("flip")), clip))
            elif t == "text":
                skipped += 1
            if grp is not None and len(out) > n0:
                grp.append(wp_grp_of(s) if "wp_grp_of" in globals() else (s.get("grp") or L.get("grp")))
    if skipped:
        wn_warn(page or D.get("page"), "text", u"%s: %d text shape(s) inside its layers not drawn (texts are items: "
                u"Ix.layer turns them into labels)" % (D.get("id"), skipped))
    return out


def rd_drawing(P, D, T, frame=None):
    import fitz as _fz
    pg = _RdPg()
    pg.W, pg.H = T.w, T.h
    did = u"%s" % D.get("id")
    pg.grp = []
    pg.items = rd_items(D, T, P.pid, pg.grp)
    pg.grp_root = did
    pg.page = P.pid                                 # write_pdf's per-page group counts (wp_groups_log, S2)
    st_ = BK_GRP.setdefault(P.pid, dict(kinds=set(), elements=set(), untagged=0))
    for g_ in pg.grp:
        if g_:
            st_["kinds"].add(u"%s" % g_.split(u"/")[0])
            st_["elements"].add(u"%s|%s" % (did, g_))
        else:
            st_["untagged"] += 1
    d_ = bg_booklet("_render")
    os.makedirs(d_, exist_ok=True)
    fn = os.path.join(d_, u"%s_%s.pdf" % (P.pid, "".join(c if c.isalnum() or c in "-_" else "_" for c in did)))
    placed = dict(D=D, T=T, rect=T.rect, den=T.den, id=did)
    if pg.items and pg.W > 0.01 and pg.H > 0.01:
        write_pdf(pg, fn, did)
        src = _fz.open(fn)
        RD_DOCS.append(src)
        r = T.rect
        P.page.show_pdf_page(_fz.Rect(r[0] * BK_K, r[1] * BK_K, r[2] * BK_K, r[3] * BK_K), src, 0)
        if "WP_IMG_LOG" in globals():
            for ln in WP_IMG_LOG:
                wn_warn(P.pid, "image", u"%s: %s" % (did, ln))
            del WP_IMG_LOG[:]
    else:
        wn_warn(P.pid, "drawing", u"%s has nothing to draw (no shapes or zero size)" % did)
    if frame:
        bk_rect(P, T.rect, None, frame[0], frame[1])
    P.tp.block(T.rect, did)
    P.tp.keep(T.rect, "drawing", did)
    for K_ in D.get("keep_areas") or []:
        if isinstance(K_, dict):
            pts, kk, nm = [T.pt(p[0], p[1]) for p in K_.get("pts") or []], K_.get("kind") or "keep", K_.get("name")
        else:                                   # a box [x0, y0, x1, y1] (the key-map module's form)
            e_ = T.e
            if (K_[2] - K_[0]) * (K_[3] - K_[1]) >= 0.95 * (e_[2] - e_[0]) * (e_[3] - e_[1]):
                continue                        # the whole frame: already the drawing's own keep (its labels may enter)
            a_, b_ = T.pt(K_[0], K_[3]), T.pt(K_[2], K_[1])
            pts, kk, nm = [a_, (b_[0], a_[1]), b_, (a_[0], b_[1])], "keep", None
        if len(pts) >= 3:
            P.tp.keep(pts, kk, u"%s:%s" % (did, nm or "keep"))
    P.placed.append(placed)
    P.ink.append(("drawing", T.rect, did))
    return placed


def bk_rect(P, r, fill=None, stroke=None, width_pt=0.5, dash=None):
    """a rectangle on the page (page mm, y down); colours hex"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_rect(_fz.Rect(r[0] * BK_K, r[1] * BK_K, r[2] * BK_K, r[3] * BK_K))
    sh.finish(color=hex_rgb(stroke) if stroke else None, fill=hex_rgb(fill) if fill else None,
              width=width_pt, dashes=("[%s] 0" % " ".join("%g" % d for d in dash)) if dash else None)
    sh.commit()


def bk_line(P, pts, stroke, width_pt=0.5, dash=None):
    """a polyline on the page (page mm, y down)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_polyline([_fz.Point(x * BK_K, y * BK_K) for x, y in pts])
    sh.finish(color=hex_rgb(stroke), width=width_pt, closePath=False,
              dashes=("[%s] 0" % " ".join("%g" % d for d in dash)) if dash else None)
    sh.commit()


def bk_poly(P, pts, fill=None, stroke=None, width_pt=0.5):
    """a closed polygon on the page (page mm, y down)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_polyline([_fz.Point(x * BK_K, y * BK_K) for x, y in pts])
    sh.finish(color=hex_rgb(stroke) if stroke else None, fill=hex_rgb(fill) if fill else None, width=width_pt,
              closePath=True)
    sh.commit()


def rd_close():
    for d in RD_DOCS:
        try:
            d.close()
        except Exception:
            pass
    del RD_DOCS[:]


# ---- v32.4 (p02 ran 10+ min in Aras's 4 Nov 21:49 run): PyMuPDF picks a fresh resource name for each drawing, photo
# and font it adds by listing EVERY xobject, image and font of the page, recursing into each drawing already placed
# (each one holds thousands of nested group xobjects, G6-9), with a list as its "seen" set: the time grows with the
# square of the drawing's groups. A new name only has to differ from the names in the page's OWN resource
# dictionaries, so the booklet's document lists those (shallow); the picture is the same. full=True (font
# subsetting at the end) still gets the original deep lists.
def _bk_res_shallow(doc, pno, key):
    try:
        x_ = doc[pno].xref
        t_, v_ = doc.xref_get_key(x_, "Resources/" + key)
        if t_ == "xref":
            v_ = doc.xref_object(int(v_.split()[0]), compressed=True)
        elif t_ != "dict":
            return []
        return [(int(m_.group(2)), m_.group(1)) for m_ in re.finditer(r"/([^\s/<>\[\]()]+)\s*(\d+)\s+\d+\s+R", v_)]
    except Exception:
        return []


def bk_shallow_res(doc):
    f0, i0, x0 = doc.get_page_fonts, doc.get_page_images, doc.get_page_xobjects

    def fonts(pno, full=False):
        if full:
            return f0(pno, full=True)
        return [(xr, u"", u"", u"", nm, u"") for xr, nm in _bk_res_shallow(doc, pno, "Font")]

    def images(pno, full=False):
        if full:
            return i0(pno, full=True)
        return []                                   # image names are in the XObject dictionary: listed below

    def xobjects(pno):
        return [(xr, nm, 0, None) for xr, nm in _bk_res_shallow(doc, pno, "XObject")]
    doc.get_page_fonts, doc.get_page_images, doc.get_page_xobjects = fonts, images, xobjects
    return doc
