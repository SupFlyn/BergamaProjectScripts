# ---- 81_ids (round 5 S10; round 6 S9 v31, G6-2): ONE page numbering, group aliases, text clean-up, {src:key} numbers ---
# Round 6 (PLAN §2.1, G6-2): every content script exports the 22-page ids p01 ... p22 itself; the old 25 -> 23 map
# (BK_PAGE_IDS, BK_25_TO_23) is gone. An item exported for a page id outside p01-p22 = WARNING and is not shown.
BK_NPAGES = 22
# Group aliases ("folder/group" -> group): S8 asked agriculture's "stream comes first" block to join the water board's
# group p21_g2_figures (heading + both blocks); agriculture exports it as group "ag1_stream" (S9). Set here, once.
BK_GROUP_ALIAS = {"Bergama_agriculture_alternatives/ag1_stream": "p21_g2_figures"}
BK_SRC_RE = re.compile(r"(?:\s*\{src:([A-Za-z0-9_]+)\})+")
BK_SRC_ONE = re.compile(r"\{src:([A-Za-z0-9_]+)\}")
BK_SRC = dict(order=[], num={}, text={}, missing=set())
BK_FALSE_LABELS = (re.compile(r"\s*·\s*style a(?: \(cutouts\))?", re.I),      # P22 closing row: false crop label
                   re.compile(r"\s*·\s*1:[\d,]+\s*$"))                       # a scale tail the composer now prints


def bk_remap(log):
    """every loaded file: page ids checked (p01-p22, G6-2), group aliases, text clean-up; one log line per file"""
    for folder, d in BK_IX.items():
        bad = []
        for pid, its in (d.get("pages") or {}).items():
            if pid != "any" and (not re.match(r"^p\d\d$", u"%s" % pid) or not 1 <= int(pid[1:]) <= BK_NPAGES):
                bad.append(pid)
                wn_warn(pid, "page", u"%s exports %d items for page %s, not in the 22-page booklet (G6-2): not shown"
                        % (folder, len(its), pid))
            for it in its:
                it["page"] = pid
                g = BK_GROUP_ALIAS.get(u"%s/%s" % (folder, it.get("group")))
                if g:
                    it["group"] = g
                if it.get("kind") == "text":
                    bk_clean_text(it)
        log.append(u"pages %s: %s%s" % (folder, u" ".join(sorted(k for k in (d.get("pages") or {}))),
                                        (u"; not shown " + u" ".join(sorted(bad))) if bad else u""))


def bk_clean_text(it):
    s = u"%s" % it.get("string", u"")
    s = s.replace(u"**", u"*")                  # "**bold**" (water balance, city link) -> the setter's "*bold*"
    for rx in BK_FALSE_LABELS:
        s = rx.sub(u"", s)
    it["string"] = s


def bk_sources_collect():
    """every source row of every file: key -> text (first file wins; a different text for the same key = WARNING)"""
    for folder, d in sorted(BK_IX.items()):
        for k, v in (d.get("sources") or {}).items():
            t = (v or {}).get("text") or u""
            u_ = (v or {}).get("url")
            full = (u"%s, %s" % (t, u_)) if u_ and u_ not in t else t
            if k in BK_SRC["text"] and BK_SRC["text"][k] != full:
                wn_warn(None, "source", u"source key %s has two texts (%s kept)" % (k, folder))
                continue
            BK_SRC["text"].setdefault(k, full)


def bk_src_number(pids):
    """numbers every {src:key} in page order (texts in export order), then rewrites each mark run as "[1, 4]"; a key
    no file defines = WARNING and "[?]" """
    BK_SRC["order"][:] = []
    BK_SRC["num"].clear()
    for pid in pids:
        its = ix_page(pid)
        keys = []
        for it in its:
            for t_ in _bk_src_strings(it):
                keys += BK_SRC_ONE.findall(t_)
            keys += [k_ for k_ in it.get("src_keys") or () if isinstance(k_, str)]   # v31: a drawing's own sources
        keys += [it.get("key") for it in its if it.get("kind") == "source" and it.get("key")]   # page source rows
        for k in keys:
            if True:
                if k not in BK_SRC["num"]:
                    if k not in BK_SRC["text"]:
                        if k not in BK_SRC["missing"]:
                            wn_warn(pid, "source", u"mark {src:%s} has no source row in any items.json" % k)
                        BK_SRC["missing"].add(k)
                        continue
                    BK_SRC["order"].append(k)
                    BK_SRC["num"][k] = len(BK_SRC["order"])

    def rep(m):
        ks = BK_SRC_ONE.findall(m.group(0))
        ns = []
        for k in ks:
            n = BK_SRC["num"].get(k)
            v = u"%d" % n if n else u"?"
            if v not in ns:
                ns.append(v)
        return u" [%s]" % u", ".join(ns)
    n = 0
    for d in BK_IX.values():
        for its in d.get("pages", {}).values():
            for it in its:
                k = it.get("kind")
                if k == "text" and u"{src:" in (it.get("string") or u""):
                    it["string"] = BK_SRC_RE.sub(rep, it["string"]).lstrip()
                    it["short_forms"] = [BK_SRC_RE.sub(rep, t).lstrip() for t in it.get("short_forms") or []]
                    n += 1
                elif k == "legend":                  # v31 (G6-3): plain-string legend texts and titles carry marks too
                    for e in it.get("entries") or ():
                        if isinstance(e.get("text"), str) and u"{src:" in e["text"]:
                            e["text"] = BK_SRC_RE.sub(rep, e["text"]).lstrip()
                            n += 1
                    if isinstance(it.get("title"), str) and u"{src:" in it["title"]:
                        it["title"] = BK_SRC_RE.sub(rep, it["title"]).lstrip()
                        n += 1
                elif k == "list":
                    its_ = it.get("items") or []
                    for i_, t_ in enumerate(its_):
                        if isinstance(t_, str) and u"{src:" in t_:
                            its_[i_] = BK_SRC_RE.sub(rep, t_).lstrip()
                            n += 1
                elif k == "photo" and isinstance(it.get("caption"), str) and u"{src:" in it["caption"]:
                    it["caption"] = BK_SRC_RE.sub(rep, it["caption"]).lstrip()
                    n += 1
    return n


def _bk_src_strings(it):
    """the strings of an item that may carry {src:key} marks, in reading order (text, legend title + entries, list
    rows, photo caption)"""
    k = it.get("kind")
    if k == "text":
        return [it.get("string") or u""]
    out = []
    if k == "legend":
        if isinstance(it.get("title"), str):
            out.append(it["title"])
        out += [e.get("text") for e in it.get("entries") or () if isinstance(e.get("text"), str)]
    elif k == "list":
        out += [t for t in it.get("items") or () if isinstance(t, str)]
    elif k == "photo" and isinstance(it.get("caption"), str):
        out.append(it["caption"])
    return out
