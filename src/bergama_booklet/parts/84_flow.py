# ---- 84_flow (v35, 5 Nov 2026; Aras 12:32 "pages should be able to move drawings when needed", "drawings change hell
# a lot"; decision 09:45 "Both": an editable layout table + an automatic grid shift where a drawing no longer fits).
# 1. LAYOUT TABLE  ~/Downloads/Bergama/Data/booklet_layout.csv (written from parts/80_plan.py on the first run; then
#    YOURS: edit it in Excel, save as CSV, press the Button). One row per frame:
#      page_order;page;block;x_mm;y_mm;w_mm;h_mm;scale;size;on
#    page_order = where the page sits in the booklet (sort key; the cover stays first, Sources last);
#    block = the frame key (80_plan); x, y, w, h = the frame on the A3 sheet in mm (origin top left);
#    scale = 1:n of its true-scale drawings (n only; "id=n;id=n" for a frame holding several, written as id=n|id=n);
#    size = the factor of a diagram / chart (1 = the size its script exports); on = 0 leaves the frame's items out.
#    A row whose page / block the plan does not know = WARNING (ignored). Numbers: whole mm, "." or "," both read.
# 2. FLOW  every frame starts at its table place; each frame is MEASURED at its table scale (drawing + level column +
#    scale band + its notes); a frame too small GROWS (down / right from its top-left corner); a frame that then sits
#    on one placed before it (reading order) is SHIFTED below it or beside it, whichever moves it less and stays on
#    the page; if neither stays on the page it takes the first free place on a 2 mm grid; if there is none it stays
#    below the last one = WARNING "<page> <block> page full ... (scale kept)". The SCALE NEVER CHANGES (no factor, no
#    ladder). Frames marked over=True (a legend or list inside a map) move with the frame they sit on.
#    Log: "flow <page> <block> moved dx,dy grown dw,dh" for every frame that moved or grew; "frame ... (flow)".
BK_TABLE = os.path.join(BERGAMA_ROOT, "Data", "booklet_layout.csv")
BK_TABLE_COLS = ["page_order", "page", "block", "x_mm", "y_mm", "w_mm", "h_mm", "scale", "size", "on"]
BK_FLOW_SNAP = 2.0          # mm: the grid a moved frame snaps to
BK_FLOW_GAP = 4.0           # mm between frames (= the grid gutter)


def _bk_fkey(f):
    ids = f.get("ids")
    return f.get("key") or (ids if isinstance(ids, str) else list(ids)[0])


def _bk_num(s):
    s = (u"%s" % s).strip().replace(u",", u".")
    return float(s) if s else None


def _bk_table_write(path):
    rows = []
    for i, sp in enumerate(BK_PAGES, 1):
        if sp.get("kind") or not sp.get("frames"):
            continue
        for f in sp["frames"]:
            m = f["mm"]
            d = f.get("den")
            sc = u"|".join(u"%s=%d" % kv for kv in sorted(d.items())) if isinstance(d, dict) else (u"%d" % d if d else u"")
            rows.append([u"%d" % i, sp["pid"], _bk_fkey(f), u"%d" % round(m[0]), u"%d" % round(m[1]),
                         u"%d" % round(m[2] - m[0]), u"%d" % round(m[3] - m[1]), sc,
                         (u"%g" % f.get("f", 1.0)) if not d else u"", u"1"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        fh.write(u"sep=;\r\n")                      # Excel opens it in columns in any language setting
        fh.write(u";".join(BK_TABLE_COLS) + u"\r\n")
        for r in rows:
            fh.write(u";".join(r) + u"\r\n")
    return len(rows)


def _bk_table_read(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        raw = [ln.rstrip(u"\r\n") for ln in fh if ln.strip()]
    if raw and raw[0].lower().startswith(u"sep="):
        raw = raw[1:]
    if not raw:
        return []
    sep = u";" if raw[0].count(u";") >= raw[0].count(u",") else u","
    head = [h.strip().lower() for h in raw[0].split(sep)]
    out = []
    for ln in raw[1:]:
        cells = [c.strip().strip(u'"') for c in ln.split(sep)]
        out.append(dict(zip(head, cells + [u""] * (len(head) - len(cells)))))
    return out


def bk_table_apply(lines):
    """read (or first write) the layout table and apply it to BK_PAGES: page order, frame mm, scale, size, on/off"""
    if not os.path.isfile(BK_TABLE):
        n = _bk_table_write(BK_TABLE)
        lines.append(u"layout table written from the built-in plan: %d frames -> %s (edit it, press the Button)"
                     % (n, BK_TABLE))
        return
    try:
        rows = _bk_table_read(BK_TABLE)
    except Exception as ex:
        wn_warn(None, "table", u"layout table not read (%s: %s): the built-in plan is used" % (type(ex).__name__, ex))
        return
    bypid = dict((sp["pid"], sp) for sp in BK_PAGES if sp.get("pid"))
    order, used = {}, 0
    for r in rows:
        pid, key = r.get("page", u""), r.get("block", u"")
        sp = bypid.get(pid)
        if sp is None or sp.get("kind"):
            wn_warn(None, "table", u"layout table row %s / %s: no such content page (ignored)" % (pid, key))
            continue
        try:
            po = _bk_num(r.get("page_order", u""))
            if po is not None:
                order[pid] = min(order.get(pid, po), po)
            f = next((f for f in sp.get("frames") or [] if _bk_fkey(f) == key), None)
            if f is None:
                wn_warn(pid, "table", u"layout table block %r is not a frame of %s (ignored)" % (key, pid))
                continue
            x, y, w, h = [_bk_num(r.get(c, u"")) for c in ("x_mm", "y_mm", "w_mm", "h_mm")]
            if None not in (x, y, w, h) and w > 0 and h > 0:
                f["mm"] = (x, y, x + w, y + h)
            sc = (r.get("scale") or u"").strip()
            if u"=" in sc:
                f["den"] = dict((a.strip(), int(round(_bk_num(b)))) for a, b in
                                (p.split(u"=", 1) for p in sc.replace(u";", u"|").split(u"|") if u"=" in p))
            elif sc:
                f["den"] = int(round(_bk_num(sc.replace(u"1:", u""))))
            sz = _bk_num(r.get("size", u""))
            if sz:
                f["f"] = sz
            if (r.get("on") or u"1").strip() in (u"0", u"no", u"off"):
                sp["skip"] = list(sp.get("skip") or []) + [p for p in ([f["ids"]] if isinstance(f["ids"], str)
                                                                        else list(f["ids"]))]
                f["ids"], f["opt"] = (u"__off__%s" % key,), True
            used += 1
        except Exception as ex:
            wn_warn(pid, "table", u"layout table row %s / %s not read (%s: %s)" % (pid, key, type(ex).__name__, ex))
    if order:
        idx = dict((id(sp), i) for i, sp in enumerate(BK_PAGES))
        last = len(BK_PAGES) + 1000

        def key_(sp):
            if sp.get("kind") == "cover":
                return (-1e9, 0)
            if sp.get("kind") == "sources":
                return (1e9, 0)
            return (order.get(sp.get("pid"), idx[id(sp)] + 1), idx[id(sp)])
        BK_PAGES.sort(key=key_)
        _ = last
    lines.append(u"layout table %s: %d rows applied; page order %s" % (
        BK_TABLE, used, u" ".join(sp.get("pid", u"?") for sp in BK_PAGES)))


def _bk_ov(a, b, g=0.0):
    return a[0] < b[2] + g and b[0] < a[2] + g and a[1] < b[3] + g and b[1] < a[3] + g


def _bk_snap(v):
    return round(v / BK_FLOW_SNAP) * BK_FLOW_SNAP


def bk_flow(P, S, frames, pid, top):
    """v35: frames at their table place, grown to their measured size, shifted off each other (see the part notes);
    sets F["mm"], F["k"] = 1.0 (scale never changed)"""
    byk = dict((F["key"], F) for F in frames)
    for F in frames:
        F["_notes_in"] = []
        F["k"] = 1.0
    for F in frames:
        if F.get("note") in byk:
            for did, kk, it in F["items"]:
                if kk == "drawing":
                    byk[F["note"]]["_notes_in"] += list(S["att"].get(did, {}).get("side", []))
    live = [F for F in frames if F["items"] or F["_notes_in"] or F.get("key") == spec_side(frames)]
    if not live:
        return 1.0
    x0, x1, y1 = GRID_AREA[0], GRID_AREA[2], GRID_AREA[3]
    base = [F for F in live if not F.get("over")]
    base.sort(key=lambda F: (round(max(F["mm0"][1], top) / 6.0), F["mm0"][0]))
    placed = []
    for F in base:
        m0 = F["mm0"]
        w_, h_ = _bk_leaf(P, S, F, pid, 1.0)
        W, H = max(m0[2] - m0[0], w_), max(m0[3] - m0[1], h_)
        x, y = m0[0], max(m0[1], top)
        if x + W > x1 and W <= x1 - x0:
            x = x1 - W
        for _i in range(80):
            R = (x, y, x + W, y + H)
            hit = next((Q for Q in placed if _bk_ov(R, Q, BK_FLOW_GAP - 0.01)), None)
            if hit is None:
                break
            cand = []
            yd = _bk_snap(hit[3] + BK_FLOW_GAP + BK_FLOW_SNAP / 2.0)
            xr = _bk_snap(hit[2] + BK_FLOW_GAP + BK_FLOW_SNAP / 2.0)
            if yd + H <= y1 + 0.5:
                cand.append((abs(yd - y), x, yd))
            if xr + W <= x1 + 0.5:
                cand.append((abs(xr - x), xr, y))
            if cand:
                _d, x, y = min(cand)
                continue
            spot = None                                  # first free place on the grid, top to bottom, left to right
            yy = top
            while spot is None and yy + H <= y1 + 0.5:
                for xx in sorted(set([x0] + [_bk_snap(Q[2] + BK_FLOW_GAP + BK_FLOW_SNAP / 2.0) for Q in placed])):
                    if xx + W > x1 + 0.5:
                        continue
                    if not any(_bk_ov((xx, yy, xx + W, yy + H), Q, BK_FLOW_GAP - 0.01) for Q in placed):
                        spot = (xx, yy)
                        break
                yy += BK_FLOW_SNAP
            if spot:
                x, y = spot
            else:
                y = max(Q[3] for Q in placed) + BK_FLOW_GAP
                wn_warn(pid, u"%s page full" % F["key"], u"no free place for %.0f x %.0f mm: set below the last block, "
                        u"runs %.0f mm past the foot (scale kept; move or resize it in the layout table)"
                        % (W, H, y + H - y1))
            break
        F["mm"] = (x, y, x + W, y + H)
        placed.append(F["mm"])
        dx, dy, dw, dh = x - m0[0], y - m0[1], W - (m0[2] - m0[0]), H - (m0[3] - m0[1])
        if max(abs(dx), abs(dy), dw, dh) > 0.5:
            BK_PAGENO_LOG.append(u"flow %s %s moved %.0f,%.0f grown %.0f,%.0f" % (pid, F["key"], dx, dy, dw, dh))
        if y + H > y1 + 0.5 or x + W > x1 + 0.5:
            wn_warn(pid, u"%s edge" % F["key"], u"%.0f x %.0f mm runs past the drawing area (R %.0f, B %.0f mm; scale "
                    u"kept)" % (W, H, max(0.0, x + W - x1), max(0.0, y + H - y1)))
    for F in live:                                       # over frames ride on the frame they cover most
        if not F.get("over"):
            continue
        m0 = F["mm0"]

        def cov(Q):
            a, b = m0, Q["mm0"]
            return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
        host = max(base, key=cov) if base else None
        dx = dy = 0.0
        if host is not None and cov(host) > 0:
            dx, dy = host["mm"][0] - host["mm0"][0], host["mm"][1] - host["mm0"][1]
        w_, h_ = _bk_leaf(P, S, F, pid, 1.0)
        W, H = max(m0[2] - m0[0], w_), max(m0[3] - m0[1], h_)
        F["mm"] = (m0[0] + dx, m0[1] + dy, m0[0] + dx + W, m0[1] + dy + H)
    for F in live:
        m_ = F["mm"]
        BK_PAGENO_LOG.append(u"frame %s %s %.1f,%.1f,%.1f,%.1f (flow)" % (pid, F["key"], m_[0], m_[1], m_[2] - m_[0],
                                                                        m_[3] - m_[1]))
    return 1.0
