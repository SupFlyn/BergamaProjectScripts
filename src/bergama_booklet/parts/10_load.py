# ---- 10_load (composer core, round 5 S1; G-R5-12, P04.7): read every content script's items.json -------------------
#   ix_load_all(need=(), root=None, log=None) -> {folder: export}
#         reads Downloads/Bergama/cached/booklet/<folder>/items.json for every folder; a folder in `need` without a
#         readable file = HARD STOP (missing data); any other unreadable file = WARNING. Validates (ix_validate),
#         indexes every item (ix_get), runs every text through the glyph check (P04.7: a character the font lacks is a
#         WARNING and becomes "–"), logs "items <folder> <script> <version> <run>: <kinds> (<this run | earlier>)"
#   ix_validate(d, folder) -> [problem]      schema, kinds, page keys, drawing refs, units (each a WARNING)
#   ix_get(id, folder=None) -> item | None   by id (ids clash across files: "folder/id" always works)
#   ix_page(pid) -> [item]                    every item exported for page pid, in file then export order
#   ix_texts(item_or_id) -> [item]            the text items of a drawing (anchor.drawing == its id), by priority
#   ix_text(id) -> str                        the string of a text id (a plain string passes through)
#   bk_font_files() -> (regular, bold)        the SAME Arial files font_metrics measures with (pdf_fonts _pf_path); a
#                                             missing file raises FontMissing (hard stop: fonts)
BK_IX = {}            # folder -> export dict
BK_ID = {}            # id and "folder/id" -> item


def bk_font_files():
    r, b = _pf_path(_PF_FILES["R"][0]), _pf_path(_PF_FILES["B"][0])
    if not r or not b:
        raise FontMissing("Arial (arial.ttf / arialbd.ttf) not found in the Windows or user font folder: the booklet "
                          "cannot measure or set text. Install Arial.")
    return r, b


def ix_validate(d, folder):
    bad = []
    if d.get("schema") != IX_SCHEMA_R:
        bad.append(u"schema %r, expected %r" % (d.get("schema"), IX_SCHEMA_R))
    pages = d.get("pages")
    if not isinstance(pages, dict):
        return bad + [u"no pages"]
    ids = set(it.get("id") for its in pages.values() for it in its if isinstance(it, dict))
    for pid, its in pages.items():
        for it in its:
            k = it.get("kind")
            if k not in IX_KINDS_R:
                bad.append(u"%s: item %s has unknown kind %r" % (pid, it.get("id"), k))
            if not it.get("id"):
                bad.append(u"%s: an item without id (%s)" % (pid, k))
            if k == "drawing":
                e = it.get("extent") or []
                if len(e) != 4 or e[2] <= e[0] or e[3] <= e[1]:
                    bad.append(u"%s: drawing %s extent %r" % (pid, it.get("id"), e))
                if it.get("units") not in ("m", "mm"):
                    bad.append(u"%s: drawing %s units %r" % (pid, it.get("id"), it.get("units")))
            for ref in ("drawing", "parent", "child"):
                r_ = it.get(ref)
                if r_ and r_ not in ids:
                    bad.append(u"%s: %s %s names %s %r, not in this file" % (pid, k, it.get("id"), ref, r_))
            a_ = it.get("anchor")
            if isinstance(a_, dict) and a_.get("drawing") and a_["drawing"] not in ids:
                bad.append(u"%s: text %s anchored to %r, not in this file" % (pid, it.get("id"), a_["drawing"]))
    return bad


IX_SCHEMA_R = "bergama-items/1"
IX_KINDS_R = ("drawing", "text", "legend", "list", "level_column", "inset", "keymap", "photo", "chart", "source")


def ix_load_all(need=(), root=None, log=None):
    import json as _j
    lg = WN_LOG if log is None else log          # the one warning list (warn.py): it reaches the log
    BK_IX.clear()
    BK_ID.clear()
    root = root or bg_booklet("")
    names = sorted(n for n in os.listdir(root) if os.path.isdir(os.path.join(root, n))) if os.path.isdir(root) else []
    for n in need:
        if n not in names:
            names.append(n)
    for folder in names:
        p = os.path.join(root, folder, "items.json")
        if not os.path.isfile(p):
            if folder in need:
                raise RuntimeError(u"items.json of %s missing (%s): run that script first" % (folder, p))
            continue
        try:
            with open(p, encoding="utf-8") as f:
                d = _j.load(f)
        except Exception as ex:
            if folder in need:
                raise RuntimeError(u"items.json of %s unreadable (%s: %s)" % (folder, type(ex).__name__, ex))
            wn_warn(None, "load", u"%s/items.json unreadable (%s): skipped" % (folder, type(ex).__name__), lg)
            continue
        for b_ in ix_validate(d, folder):
            wn_warn(None, "load", u"%s: %s" % (folder, b_), lg)
        d["_folder"], d["_path"] = folder, p
        fresh, note = bg_this_run(p)
        BK_IX[folder] = d
        n = {}
        for pid, its in (d.get("pages") or {}).items():
            for it in its:
                it["_folder"] = folder
                n[it.get("kind")] = n.get(it.get("kind"), 0) + 1
                iid = it.get("id")
                BK_ID[u"%s/%s" % (folder, iid)] = it
                if iid in BK_ID and BK_ID[iid] is not it:
                    BK_ID[iid] = None                     # clash: only "folder/id" finds it
                elif iid not in BK_ID:
                    BK_ID[iid] = it
                if it.get("kind") == "text":
                    _ix_glyphs(it, pid, lg)
        lg.append(u"items %s %s %s %s: %s (%s)" % (folder, d.get("script"), d.get("version"), d.get("run"),
                                                   u", ".join(u"%s %d" % kv for kv in sorted(n.items())), note))
        if d.get("warnings"):
            lg.append(u"  %s logged %d content warnings in its own log" % (folder, len(d["warnings"])))
    return BK_IX


def _ix_glyphs(it, pid, lg):
    """P04.7: every character of the text must be in the font it is set in; a missing one -> WARNING + "–\""""
    s = u"%s" % it.get("string", u"")
    s2, miss = fm_safe(s, bool(it.get("bold")))
    if miss:
        wn_warn(pid, "glyph", u"%s: %s not in the font, set as %r" % (
            it.get("id"), u", ".join(u"U+%04X %s" % (ord(c), c) for c in miss), s2[:60]), lg)
        it["string"] = s2
    alt = []
    for t in it.get("short_forms") or ():
        alt.append(fm_safe(t, bool(it.get("bold")))[0])
    if alt:
        it["short_forms"] = alt


def ix_get(iid, folder=None):
    if iid is None:
        return None
    if isinstance(iid, dict):
        return iid
    if folder:
        return BK_ID.get(u"%s/%s" % (folder, iid))
    return BK_ID.get(iid) or BK_ID.get(u"%s" % iid)


def ix_page(pid):
    out = []
    for folder in sorted(BK_IX):
        out.extend(BK_IX[folder].get("pages", {}).get(pid, []))
    return out


def ix_texts(drawing):
    D = ix_get(drawing)
    if D is None:
        return []
    out = []
    for its in BK_IX.get(D.get("_folder"), {}).get("pages", {}).values():
        for it in its:
            a_ = it.get("anchor")
            if it.get("kind") == "text" and isinstance(a_, dict) and a_.get("drawing") == D["id"]:
                out.append(it)
    return sorted(out, key=lambda t: t.get("priority", 5))


def ix_text(t, folder=None):
    if t is None:
        return u""
    it = ix_get(t, folder) if not isinstance(t, dict) else t
    if it is not None and it.get("kind") == "text":
        return it.get("string", u"")
    return u"%s" % t
