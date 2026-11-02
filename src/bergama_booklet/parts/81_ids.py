# ---- 81_ids (round 5, S10, 2 Nov 2026): ONE page numbering, group aliases, text clean-up, {src:key} numbers -----------
# Page ids (S6/S8/S9 handovers: "S10 settles one numbering"): the booklet uses the 23-page ids of PLAN §4. Content
# scripts that export 25-page ids are listed in BK_PAGE_IDS and mapped here, once, right after loading (every item's
# "page" and the file's "pages" keys), so nothing else in the booklet knows the old numbers. A folder not listed counts
# as 23-page (a page id over p23 from it = WARNING). Change a line here when a script moves to 23-page ids.
BK_PAGE_IDS = {
    "selinus_board": 25,                       # S7: 16d_items SB_IX_PAGES (heritage loop "p22" = 23-page p20)
    "bergama_proposal_sections": 25,           # S9: "p13" (same in both)
    "Bergama_agriculture_alternatives": 25,    # S9: "p21" = 23-page p19
    "Bergama_city_link_analysis": 25,          # S9: "p08", "p10" (same in both)
    "Bergama_water_balance_analysis": 23,      # S5: "p11" (same in both)
    "bergama_water_board": 23,                 # S8: WBX_PAGE
    "bergama_masterplan": 23,                  # S6: MPX_PAGE
}
BK_25_TO_23 = {"p13": "p13", "p14": "p13", "p15": "p14", "p16": "p15", "p17": "p16", "p18": "p17", "p19": "p18",
               "p20": "p18", "p21": "p19", "p22": "p20", "p23": "p21", "p24": "p22", "p25": "p23"}   # D9, D7
# Group aliases ("folder/group" -> group): S8 asked agriculture's "stream comes first" block to join the water board's
# group p21_g2_figures (heading + both blocks); agriculture exports it as group "ag1_stream" (S9). Set here, once.
BK_GROUP_ALIAS = {"Bergama_agriculture_alternatives/ag1_stream": "p21_g2_figures"}
BK_SRC_RE = re.compile(r"(?:\s*\{src:([A-Za-z0-9_]+)\})+")
BK_SRC_ONE = re.compile(r"\{src:([A-Za-z0-9_]+)\}")
BK_SRC = dict(order=[], num={}, text={}, missing=set())
BK_FALSE_LABELS = (re.compile(r"\s*·\s*style a(?: \(cutouts\))?", re.I),      # P22 closing row: false crop label
                   re.compile(r"\s*·\s*1:[\d,]+\s*$"))                       # a scale tail the composer now prints


def bk_pid(folder, pid):
    if pid in (None, "any"):
        return "any"
    if BK_PAGE_IDS.get(folder, 23) == 25:
        return BK_25_TO_23.get(pid, pid)
    return pid


def bk_remap(log):
    """every loaded file to 23-page ids, group aliases, text clean-up; one log line per file"""
    for folder, d in BK_IX.items():
        new, moved = {}, []
        for pid, its in (d.get("pages") or {}).items():
            np_ = bk_pid(folder, pid)
            if np_ != pid:
                moved.append(u"%s->%s" % (pid, np_))
            if np_ not in ("any",) and (not re.match(r"^p\d\d$", np_) or int(np_[1:]) > 23):
                wn_warn(np_, "page", u"%s exports items for page %s, not in the 23-page booklet: not shown" % (
                    folder, pid))
            for it in its:
                it["page"] = np_
                g = BK_GROUP_ALIAS.get(u"%s/%s" % (folder, it.get("group")))
                if g:
                    it["group"] = g
                if it.get("kind") == "text":
                    bk_clean_text(it)
            new.setdefault(np_, []).extend(its)
        d["pages"] = new
        log.append(u"pages %s: %s-page ids%s" % (folder, BK_PAGE_IDS.get(folder, 23),
                                                 (u", mapped " + u" ".join(sorted(set(moved)))) if moved else u""))


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
            if it.get("kind") == "text":
                keys += BK_SRC_ONE.findall(it.get("string") or u"")
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
                if it.get("kind") == "text" and u"{src:" in (it.get("string") or u""):
                    it["string"] = BK_SRC_RE.sub(rep, it["string"]).lstrip()
                    it["short_forms"] = [BK_SRC_RE.sub(rep, t).lstrip() for t in it.get("short_forms") or []]
                    n += 1
    return n
