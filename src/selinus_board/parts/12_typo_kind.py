TYPO_ORDER = ["traditional", "regular", "block", "selfbuilt", "large", "industrial", "sacred", "monument", "construction"]
TYPO_SHOP = ("commercial", "mixed")
TYPO_ROOF_C = C("A86A55")           # tile roofs (mixed toward the page in the drawings)
TYPO_FLAT_C = C("8E8A82")           # flat roofs, parapets, corrugated sheet
TYPO_TIMBER_C = C("6E4F3A")         # the old town's timber frame and brackets
TYPO_STONE_C = C("A99A86")          # stone courses
MINARET_K = 2.6                     # generic minaret: 2.6 x the hall's wall height ...
MINARET_H = (14.0, 32.0)            # ... kept within 14-32 m above its ground (not surveyed)
MINARET_W = 2.2                     # m: shaft width


def typo_kind(fabric, cat):
    """The silhouette a building takes: its fabric type, industry split from the civic halls."""
    if fabric == "large" and cat == "industrial":
        return "industrial"
    return fabric if fabric in TYPO else "regular"


def typo_tone(fabric, cat):
    """The wall material's colour of a building's type in the sections (v16.4)."""
    return TYPO[typo_kind(fabric, cat)]["tone"]


def minaret_h(wall_h):
    """Generic minaret height above its ground for a mosque hall whose walls are wall_h high (not surveyed)."""
    return max(MINARET_H[0], min(MINARET_H[1], MINARET_K * max(1.0, wall_h)))


def typo_rise(fabric, cat, w, wall_h=None, minaret=False):
    """How far the generic roof of a building of width w (m, along the cut) rises above its eaves; with a minaret (a
    mosque whose walls are wall_h high) how far the minaret's cap does."""
    t = TYPO[typo_kind(fabric, cat)]
    r = 0.0
    if t["roof"] in ("hip", "gable"):
        r = min(t["rise"], math.tan(math.radians(t["pitch"])) * (w / 2.0 + t["eaves"]))
    elif t["roof"] == "shed":
        r = min(t["rise"], math.tan(math.radians(t["pitch"])) * (w + 2.0 * t["eaves"]))
    elif t["roof"] == "saw":
        r = t["rise"] if w >= 8.0 else 0.0
    elif t["roof"] == "dome":
        r = min(0.42 * w, 9.0) * 1.15 + 1.5
    if minaret and wall_h is not None:
        r = max(r, minaret_h(wall_h) - wall_h + 3.5)
    return r


def has_minaret(u):
    """(True, (x, y) or None) when a mosque has a minaret: the survey's minaret symbol marks it (at its place), or its
    name says cami (a congregational mosque; a mescit may have none and is drawn without)."""
    if u.get("minaret"):
        return True, u.get("minaret_xy")
    nm = " " + (u.get("name") or "").lower() + " "
    if "cami" in nm and u.get("fabric") == "sacred":
        return True, None
    return False, None


def minaret_s(u, x0, y0, ux, uy, s0, s1):
    """Where along a section a mosque's minaret stands: the minaret symbol's place projected on the line (kept on the
    building), else the end of the building nearer the line's end (generic); None without a minaret."""
    ok, xy = has_minaret(u)
    if not ok:
        return None
    if xy is not None:
        s = (xy[0] - x0) * ux + (xy[1] - y0) * uy
        return max(s0 + 0.5 * MINARET_W, min(s1 - 0.5 * MINARET_W, s))
    return s1 - 0.5 * MINARET_W - 0.4


def _arch(sa, za, sb, zt, n=8):
    """A round-headed opening from sa to sb, sill za, crown zt: its outline."""
    r = 0.5 * (sb - sa)
    zs = zt - r
    pts = [(sa, za), (sb, za), (sb, zs)]
    for q in range(1, n):
        an = math.pi * q / n
        pts.append(((sa + sb) / 2.0 + r * math.cos(an), zs + r * math.sin(an)))
    pts.append((sa, zs))
    return pts


def bld_profile(fabric, cat, s0, s1, zb, base, top, floors, published=False, seed=0, ruin=False, minaret=None):
    """The generic drawing of one building between s0 and s1 (m along the section), from its lowest ground zb, its own
    ground base, to its eaves top (m): dict(body=[(s, z)...] outline (with the old town's jetty), roof=[(s, z)...] or
    None, roof_c, tone, slabs=[z], wins=[(sa, za, sb, zb)] window and door openings in elevation, arches=[outline],
    shop=(sa, za, sb, zb) or None, awning=[[(s, z)..]], lines=[[(s, z)..]] (eaves, coping, corrugation, coursing,
    scaffold), timber=[[(s, z)..]] (old town frame and brackets), bands=[[(s, z)..]] (concrete floor bands, filled),
    balconies=[(s_from, s_to, z)], minaret=dict or None, kind, x0/x1 (outer extent))."""
    kind = typo_kind(fabric, cat)
    t = TYPO[kind]
    w = s1 - s0
    floors = max(1, int(floors or 1))
    st = (top - base) / float(floors) if top > base else 3.0
    out = dict(kind=kind, body=[(s0, zb), (s1, zb), (s1, top), (s0, top)], roof=None, slabs=[], wins=[], arches=[],
               shop=None, awning=[], lines=[], timber=[], bands=[], balconies=[], minaret=None, tone=t["tone"],
               roof_c=t["roof_c"], x0=s0, x1=s1)
    if not published:
        out["slabs"] = [base + f * st for f in range(1, floors) if base + f * st > zb + 0.3]
    # ---- the old town's jetty: the upper floors stand out over the stone ground floor on brackets (generic)
    jet = 0.0
    if kind == "traditional" and floors >= 2 and w >= 4.0 and not published:
        jet = min(t["jetty"], 0.12 * w)
        z1 = base + st
        out["body"] = [(s0, zb), (s1, zb), (s1, z1), (s1 + jet, z1 + 0.15), (s1 + jet, top), (s0 - jet, top),
                       (s0 - jet, z1 + 0.15), (s0, z1)]
        for sx, sg in ((s0, -1.0), (s1, 1.0)):                     # brackets under the jetty
            out["timber"].append([(sx, z1 - 0.55), (sx + sg * jet, z1 + 0.15)])
        out["x0"], out["x1"] = s0 - jet, s1 + jet
    s0r, s1r = s0 - jet, s1 + jet                                   # the walls the roof sits on
    wr = s1r - s0r
    rise = typo_rise(fabric, cat, wr)
    e = min(t["eaves"], 0.25 * w)
    if t["roof"] == "hip" or t["roof"] == "gable":
        sm = (s0r + s1r) / 2.0
        half = wr / 2.0 + e
        flat = max(0.0, half - rise / max(1e-6, math.tan(math.radians(t["pitch"]))))     # a long hip: a ridge
        out["roof"] = [(s0r - e, top), (s1r + e, top), (sm + flat, top + rise), (sm - flat, top + rise)]
        out["lines"].append([(s0r - e, top - 0.18), (s0r - e, top), (s1r + e, top), (s1r + e, top - 0.18)])   # fascia
        if kind == "traditional" and rise > 0.6:                    # Turkish tile courses on the hipped roof
            for q in range(1, 4):
                f_ = q / 4.0
                za_ = top + rise * f_
                ds = (half - flat) * f_
                out["lines"].append([(s0r - e + ds, za_), (s1r + e - ds, za_)])
        out["x0"], out["x1"] = min(out["x0"], s0r - e), max(out["x1"], s1r + e)
    elif t["roof"] == "shed":
        lo_ = top
        hi_ = top + rise
        if seed % 2:                                      # which way the lean-to falls: alternates, not surveyed
            a_, b_ = (s0 - e, hi_), (s1 + e, lo_)
        else:
            a_, b_ = (s0 - e, lo_), (s1 + e, hi_)
        za0 = a_[1] + (b_[1] - a_[1]) * e / (w + 2.0 * e)
        zb0 = a_[1] + (b_[1] - a_[1]) * (w + e) / (w + 2.0 * e)
        out["roof"] = [(s0, top), (s1, top), (s1, zb0), b_, a_, (s0, za0)]       # the wall's wedge under the sheet
        n_ = max(2, int(w / 0.35))
        zz = []                                           # corrugation of the sheet, drawn as a fine zigzag on top
        for q in range(n_ + 1):
            f_ = q / float(n_)
            zz.append((a_[0] + (b_[0] - a_[0]) * f_, a_[1] + (b_[1] - a_[1]) * f_ + (0.06 if q % 2 else 0.0)))
        out["lines"].append(zz)
    elif t["roof"] == "saw" and rise > 0.0:
        n_ = max(1, int(round(w / 6.0)))
        tw_ = w / n_
        R = [(s0, top)]
        for q in range(n_):
            a_ = s0 + q * tw_
            R += [(a_, top + rise), (a_ + tw_, top)]
        out["roof"] = R + [(s1, top)]
    elif t["roof"] == "dome":
        r_ = min(0.42 * w, 9.0)
        sm = (s0 + s1) / 2.0
        dr = 0.15 * r_                                     # the drum under the dome
        dome = [(sm + r_ * math.cos(math.pi * q / 24.0), top + dr + r_ * math.sin(math.pi * q / 24.0)) for q in range(25)]
        out["roof"] = [(sm + r_, top), (sm + r_, top + dr)] + dome[1:-1] + [(sm - r_, top + dr), (sm - r_, top)]
        out["lines"].append([(sm - r_ - 0.2, top + dr), (sm + r_ + 0.2, top + dr)])       # the drum's cornice
        if r_ > 2.0:                                      # the finial (alem)
            out["lines"].append([(sm, top + dr + r_), (sm, top + dr + r_ + min(1.5, 0.25 * r_))])
        if r_ > 3.0:                                      # windows round the drum
            for q in (-2, -1, 0, 1, 2):
                c_ = sm + q * 0.36 * r_
                out["wins"].append((c_ - 0.25, top + 0.25 * dr, c_ + 0.25, top + 0.8 * dr))
    if t.get("parapet"):
        p_ = min(t["parapet"], 0.4 * st)
        out["lines"].append([(s0 - 0.1, top - p_), (s1 + 0.1, top - p_)])                      # parapet coping band
        out["lines"].append([(s0 - 0.1, top), (s1 + 0.1, top)])
    if kind == "monument":                                # stone and brick bands, a cornice; a ruin's broken top
        hh = top - zb
        q = 1
        while q * 1.2 < hh - 0.3:
            zq = zb + q * 1.2
            out["lines"].append([(s0, zq), (s1, zq)])
            out["lines"].append([(s0, zq + 0.18), (s1, zq + 0.18)])
            q += 1
        if ruin:
            rnd = random.Random(seed)
            n_ = max(3, int(w / 1.5))
            brk = [(s1, top)]
            for k in range(1, n_):
                brk.append((s1 - w * k / n_, top - rnd.uniform(0.3, min(3.0, 0.35 * hh))))
            brk.append((s0, top - rnd.uniform(0.0, 0.25 * hh)))
            out["body"] = [(s0, zb), (s1, zb)] + brk
        else:
            out["lines"].append([(s0 - 0.25, top - 0.35), (s1 + 0.25, top - 0.35), (s1 + 0.25, top), (s0 - 0.25, top)])
        if hh >= 6.0 and w >= 4.0:                        # round-arched openings
            n_ = max(1, int(w / 4.5))
            pw = w / n_
            ah = min(0.55 * hh, 6.0)
            for k in range(n_):
                c_ = s0 + pw * (k + 0.5)
                aw = min(2.4, 0.5 * pw)
                out["arches"].append(_arch(c_ - aw / 2.0, base + 0.8, c_ + aw / 2.0, base + 0.8 + ah))
    if kind == "construction":                            # scaffold: posts and diagonals
        n_ = max(1, int(w / 3.0))
        for q in range(n_):
            a_, b_ = s0 + w * q / n_, s0 + w * (q + 1) / n_
            out["lines"].append([(a_, zb), (b_, top)])
            out["lines"].append([(a_, top), (b_, zb)])
    if t.get("base") and kind == "traditional":           # the stone ground floor: courses
        zt_ = base + (st if (floors >= 2 and not published) else t["base"])
        q = 1
        while zb + q * 0.5 < zt_ - 0.15:
            out["lines"].append([(s0, zb + q * 0.5), (s1, zb + q * 0.5)])
            q += 1
    if kind == "regular" and not published:               # concrete floor bands (beam and slab edge)
        for f in range(1, floors + 1):
            zf = base + f * st
            if zf > zb + 0.3:
                out["bands"].append([(s0 - 0.05, zf - t["band"]), (s1 + 0.05, zf - t["band"]), (s1 + 0.05, zf),
                                     (s0 - 0.05, zf)])
        if floors >= 2 and w >= 5.0:                      # one cantilevered balcony per upper floor, on one side
            side = s1 if seed % 2 == 0 else s0
            sg = 1.0 if seed % 2 == 0 else -1.0
            for f in range(1, floors):
                out["balconies"].append((side, side + sg * t["balcony"], base + f * st))
    if kind == "block" and floors >= 2 and w >= 6.0:
        for f in range(1, floors):
            zf = base + f * st
            bw = t["balcony"]
            out["balconies"].append((s0, s0 - bw, zf))
            out["balconies"].append((s1, s1 + bw, zf))
    # windows (elevation): per floor, evenly spaced; the ground floor of a shop is a glazed front with an awning
    if t["win"] and w >= 2.0:
        ww, wh, sill, sp = t["win"]
        shop = cat in TYPO_SHOP and kind not in ("monument", "sacred", "construction")
        for f in range(floors if not published else 1):
            zf = base + f * st
            if zf + sill + wh > top - 0.2:
                continue
            if f == 0 and shop and w >= 3.0:
                za, zt_ = base + 0.15, base + min(2.8, st - 0.3)
                out["shop"] = (s0 + 0.35, za, s1 - 0.35, zt_)
                aw = min(1.4, 0.3 * w)
                out["awning"] = [[(s0, zt_ + 0.15), (s0 - aw, zt_ - 0.35)], [(s1, zt_ + 0.15), (s1 + aw, zt_ - 0.35)]]
                continue
            ext = jet if f >= 1 else 0.0                  # the jettied floors are wider
            a0_, a1_ = s0 - ext, s1 + ext
            n_ = max(1, int((a1_ - a0_ - 0.8) / sp))
            pitch_ = (a1_ - a0_) / n_
            for q in range(n_):
                c_ = a0_ + pitch_ * (q + 0.5)
                if f == 0 and q == n_ // 2 and kind in ("traditional", "regular", "selfbuilt") and w >= 4.0:
                    out["wins"].append((c_ - 0.5, zf + 0.05, c_ + 0.5, zf + min(2.1, st - 0.4)))     # the door
                    continue
                if kind == "sacred":
                    out["arches"].append(_arch(c_ - ww / 2.0, zf + sill, c_ + ww / 2.0, zf + sill + wh))
                    continue
                out["wins"].append((c_ - ww / 2.0, zf + sill, c_ + ww / 2.0, zf + sill + wh))
            if kind == "traditional" and f >= 1:          # the timber frame of the upper floor: posts and braces
                n2 = max(2, int((a1_ - a0_) / 1.25))
                for q in range(n2 + 1):
                    sx = a0_ + (a1_ - a0_) * q / n2
                    out["timber"].append([(sx, zf + 0.15), (sx, min(top, zf + st))])
                for q in range(0, n2, 2):
                    sa_, sb_ = a0_ + (a1_ - a0_) * q / n2, a0_ + (a1_ - a0_) * (q + 1) / n2
                    out["timber"].append([(sa_, zf + 0.15), (sb_, min(top, zf + st) - 0.1)])
    # ---- the minaret: shaft, balcony and conical cap at its place along the section (generic height)
    if minaret is not None and kind == "sacred":
        H = minaret_h(top - base)
        sm = minaret
        hw = 0.5 * MINARET_W
        zs = base + 0.82 * H                              # the balcony (serefe)
        ztop = base + H
        out["minaret"] = dict(shaft=[(sm - hw, zb), (sm + hw, zb), (sm + hw * 0.85, ztop), (sm - hw * 0.85, ztop)],
                              balcony=[(sm - hw - 0.6, zs), (sm + hw + 0.6, zs), (sm + hw + 0.6, zs + 0.9),
                                       (sm - hw - 0.6, zs + 0.9)],
                              cap=[(sm - hw * 0.95, ztop), (sm + hw * 0.95, ztop), (sm, ztop + 3.5)],
                              alem=[(sm, ztop + 3.5), (sm, ztop + 4.3)], s=sm, top=ztop + 4.3)
        out["x0"], out["x1"] = min(out["x0"], sm - hw - 0.6), max(out["x1"], sm + hw + 0.6)
    return out


def bld_draw_cut(B, L, P, prof, fill, wall_c, ss, U, order=27, roof_c=None, pale=False, label=None, placed=None):
    """A cut building in vectors (v16.4): its interior in the tone of its type, the back wall seen through the cut with
    its windows, doors and arches, the generic roof of its type, the cut walls (heavier), a line at every floor slab,
    the old town's jetty and timber frame, the planned house's concrete floor bands and balcony, the shopfront and
    awning, the mosque's dome and minaret. P maps (s, z) to the page; ss = page units per metre (detail drops out when
    it would be too small to see). placed: the labels already on this section [(x0, x1, y)]; a label that would
    overlap one of them is left out."""
    body = [P(s, z) for s, z in prof["body"]]
    B.fill([body], fill, L, order)
    kind = prof["kind"]
    rc = roof_c
    if rc is None:
        rc = mix(prof["roof_c"], PAPER, 0.25)
    if prof["roof"]:
        R = [P(s, z) for s, z in prof["roof"]]
        if TYPO[kind]["roof"] == "shed":
            B.fill([R], fill, L, order)
        else:
            B.fill([R], rc, L, order)
        B.line(R + [R[0]], wall_c, L, order + 2, 0.1)
    small = ss * 1.0 <= 0.12 * U
    back = mix(fill, (255, 255, 255), 0.55)              # the far wall's openings, seen through the cut
    if not small:
        for a_, za, b_, zt_ in prof["wins"]:
            B.fill([[P(a_, za), P(b_, za), P(b_, zt_), P(a_, zt_)]], back, L, order + 1)
        for A_ in prof["arches"]:
            B.fill([[P(s, z) for s, z in A_]], back, L, order + 1)
    if prof["shop"] is not None and (prof["shop"][2] - prof["shop"][0]) * ss > 0.2 * U:
        a_, za, b_, zt_ = prof["shop"]
        B.fill([[P(a_, za), P(b_, za), P(b_, zt_), P(a_, zt_)]], mix(CAT["commercial"][1], (255, 255, 255), 0.35), L, order + 1)
    for Bd in prof["bands"]:
        B.fill([[P(s, z) for s, z in Bd]], mix(wall_c, fill, 0.55), L, order + 2)
    for z in prof["slabs"]:
        B.line([P(prof["body"][0][0], z), P(prof["body"][1][0], z)], wall_c, L, order + 2, 0.05)
    B.line(body + [body[0]], wall_c, L, order + 2, 0.18)            # the cut walls
    if not small:                                                    # window openings in the cut end walls
        s0, s1 = prof["body"][0][0], prof["body"][1][0]
        zs_ = sorted(set((round(za, 2), round(zt_, 2)) for (a_, za, b_, zt_) in prof["wins"]))
        for za, zt_ in zs_:
            for sx in (s0, s1):
                B.line([P(sx, za), P(sx, zt_)], (255, 255, 255), L, order + 3, 0.1)
    for ln in prof["lines"]:
        B.line([P(s, z) for s, z in ln], wall_c, L, order + 3, 0.05)
    if not small:
        for ln in prof["timber"]:
            B.line([P(s, z) for s, z in ln], mix(TYPO_TIMBER_C, fill, 0.15), L, order + 3, 0.06)
    for ln in prof["awning"]:
        B.line([P(s, z) for s, z in ln], mix(CAT["commercial"][1], INK, 0.3), L, order + 3, 0.12)
    for sa_, sb_, z in prof["balconies"]:                            # slab and rail
        B.line([P(sa_, z), P(sb_, z)], wall_c, L, order + 3, 0.12)
        B.line([P(sb_, z), P(sb_, z + 1.0), P(sa_, z + 1.0)], wall_c, L, order + 3, 0.04)
    mn = prof.get("minaret")
    if mn:
        for key in ("shaft", "balcony"):
            Q = [P(s, z) for s, z in mn[key]]
            B.fill([Q], fill, L, order + 1)
            B.line(Q + [Q[0]], wall_c, L, order + 2, 0.12)
        Q = [P(s, z) for s, z in mn["cap"]]
        B.fill([Q], rc, L, order + 1)
        B.line(Q + [Q[0]], wall_c, L, order + 2, 0.1)
        B.line([P(s, z) for s, z in mn["alem"]], wall_c, L, order + 2, 0.06)
    if label:
        top_ = max(z for s, z in (prof["roof"] or prof["body"]))
        sm = (prof["body"][0][0] + prof["body"][1][0]) / 2.0
        q = P(sm, top_)
        hw_ = 0.5 * tw(label, 0.17 * U) + 0.15 * U
        if placed is None or not any(x0_ < q[0] + hw_ and q[0] - hw_ < x1_ and abs(y_ - q[1]) < 0.3 * U
                                     for x0_, x1_, y_ in placed):
            B.text(label, q[0], q[1] + 0.12 * U, 0.17 * U, wall_c, L, order=order + 4, align="C")
            if placed is not None:
                placed.append((q[0] - hw_, q[0] + hw_, q[1]))


def bld_raster(art, prof, xp, yp, col, ecol, wcol, rcol, res, tcol=None):
    """A building beyond the cut in the picture (elevation): wall face in its type's tone, generic roof of its type,
    window openings and arches, the old town's timber frame, the planned house's floor bands and balconies, shopfront
    and awning, the mosque's minaret; detail below a pixel is left out."""
    body = [(xp(s), yp(z)) for s, z in prof["body"]]
    sa_fill(art, [body], col)
    if prof["roof"]:
        sa_fill(art, [[(xp(s), yp(z)) for s, z in prof["roof"]]], rcol)
        R = [(xp(s), yp(z)) for s, z in prof["roof"]]
        sa_stroke(art, R + [R[0]], 0.8, ecol, 0.9)
    if prof["shop"] is not None:
        a_, za, b_, zt_ = prof["shop"]
        sa_fill(art, [[(xp(a_), yp(za)), (xp(b_), yp(za)), (xp(b_), yp(zt_)), (xp(a_), yp(zt_))]], wcol, 0.9)
    for Bd in prof["bands"]:
        sa_fill(art, [[(xp(s), yp(z)) for s, z in Bd]], sa_mix(ecol, col, 0.55), 0.9)
    if 0.7 / res >= 1.2:                                   # windows only where they are at least ~1 px wide
        for a_, za, b_, zt_ in prof["wins"]:
            sa_fill(art, [[(xp(a_), yp(za)), (xp(b_), yp(za)), (xp(b_), yp(zt_)), (xp(a_), yp(zt_))]], wcol, 0.85)
        for A_ in prof["arches"]:
            sa_fill(art, [[(xp(s), yp(z)) for s, z in A_]], wcol, 0.85)
        for ln in prof["timber"]:
            sa_stroke(art, [(xp(s), yp(z)) for s, z in ln], 0.8, tcol or ecol, 0.75)
    for ln in prof["lines"]:
        sa_stroke(art, [(xp(s), yp(z)) for s, z in ln], 0.7, ecol, 0.8)
    for ln in prof["awning"]:
        sa_stroke(art, [(xp(s), yp(z)) for s, z in ln], 1.2, ecol, 0.9)
    for sa_, sb_, z in prof["balconies"]:
        sa_stroke(art, [(xp(sa_), yp(z)), (xp(sb_), yp(z))], 1.1, ecol, 0.85)
        sa_stroke(art, [(xp(sb_), yp(z)), (xp(sb_), yp(z + 1.0)), (xp(sa_), yp(z + 1.0))], 0.7, ecol, 0.7)
    sa_stroke(art, body + [body[0]], 1.0, ecol, 0.95)
    mn = prof.get("minaret")
    if mn:
        for key in ("shaft", "balcony"):
            Q = [(xp(s), yp(z)) for s, z in mn[key]]
            sa_fill(art, [Q], col)
            sa_stroke(art, Q + [Q[0]], 0.9, ecol, 0.9)
        Q = [(xp(s), yp(z)) for s, z in mn["cap"]]
        sa_fill(art, [Q], rcol)
        sa_stroke(art, Q + [Q[0]], 0.8, ecol, 0.9)
        sa_stroke(art, [(xp(s), yp(z)) for s, z in mn["alem"]], 0.8, ecol, 0.9)


def typo_label(fabric, cat, floors, mosque=False, name=""):
    """The short tag of a cut building: its fabric type (a mosque by name where the survey says so), a shop where it
    has one, its floors. v16.7: a building with its own name (label_name) is tagged with that name alone."""
    if name:
        return name
    k = typo_kind(fabric, cat)
    nm = {"traditional": "old town", "regular": "planned low-rise", "block": "apartment block", "selfbuilt": "small irregular",
          "large": "civic hall", "industrial": "industry", "sacred": "mosque" if mosque else "sacred",
          "monument": "monument", "construction": "in construction"}[k]
    if cat == "commercial" and k not in ("monument", "sacred"):
        nm += " · shop"
    elif cat == "mixed" and k not in ("monument", "sacred"):
        nm += " · shop + home"
    return "{} · {} fl".format(nm, int(floors or 1)) if k not in ("monument",) else nm


def sa_render(S, sc, s0, s1, zlo, zhi, res, style, leaf=1.0, season="", ground=None, people=True, bld_col=None,
              max_px=6000):
    """The soft picture of a section between s0 and s1 (m along the line) and zlo..zhi (m a.s.l.): the ground beyond in
    bands, buildings beyond (faded with distance), crowns at their measured size and leaf state, bridges, scale
    figures on the cut. ground: the cut's ground [(s, z)] (figures stand on it). Returns (SArt, res)."""
    W = int(math.ceil((s1 - s0) / res))
    if W > max_px:
        res = (s1 - s0) / max_px
        W = max_px
    H = max(2, int(math.ceil((zhi - zlo) / res)))
    bg = _sa_c(style["bg"])
    art = SArt(W, H, bg)
    fade_to = _sa_c(style["fade_to"])

    def xp(s):
        return (s - s0) / res

    def yp(z):
        return (zhi - z) / res
    items = []
    for d, ss_, zs in sc["bands"]:
        items.append((d, 0, ("band", ss_, zs)))
    for bo in sc["bld"]:
        if bo["s1"] < s0 or bo["s0"] > s1:
            continue
        items.append((bo["d"], 1, ("bld", bo)))
    for t in sc["trees"]:
        if t["s"] + t["r"] < s0 or t["s"] - t["r"] > s1:
            continue
        items.append((t["d"], 2, ("tree", t)))
    for br in sc["bridges"]:
        items.append((br["d"], 1, ("bridge", br)))
    items.sort(key=lambda it: (-it[0], it[1]))
    gcol, gedge = _sa_c(style["ground"]), _sa_c(style["ground_edge"])
    for d, _, it in items:
        kind = it[0]
        if kind == "band":
            _, ss_, zs = it
            f = sa_fade(d, SA_BANDS[-1], 0.35, 0.86)
            col = sa_mix(gcol, fade_to, f)
            ecol = sa_mix(gedge, fade_to, f)
            # one polygon per run of known heights
            ok = np.isfinite(zs)
            k = 0
            n = len(ss_)
            while k < n:
                if not ok[k]:
                    k += 1
                    continue
                k0 = k
                while k < n and ok[k]:
                    k += 1
                if k - k0 < 2:
                    continue
                top = [(xp(ss_[q]), yp(zs[q])) for q in range(k0, k)]
                sa_fill(art, [top + [(top[-1][0], H + 2), (top[0][0], H + 2)]], col)
                sa_stroke(art, top, 1.0, ecol, 0.8)
        elif kind == "bld":
            bo = it[1]
            f = sa_fade(d, SA_DEPTH_B, 0.12, 0.82)
            base = _sa_c(bld_col(bo) if bld_col else mix(typo_tone(bo.get("fabric", "regular"), bo.get("cat", "residential")),
                                                         (255, 255, 255), style.get("tone_mix", 0.5)))
            col = sa_mix(base, fade_to, f)
            ecol = sa_mix(_sa_c(style["bld_edge"]), fade_to, f)
            scol = sa_mix(_sa_c(style["storey"]), fade_to, f)
            # v16.3: the building's type as a silhouette (generic roof, windows, shopfront), not a plain box
            prof = bld_profile(bo.get("fabric", "regular"), bo.get("cat", "residential"), bo["s0"], bo["s1"], bo["zb"],
                               bo["base"], bo["zt"], bo["floors"], bo["fsrc"] == "published",
                               seed=int(abs(bo["s0"] * 7.0 + bo["d"] * 3.0)), ruin=bo.get("ruin", False),
                               minaret=bo.get("minaret"))
            wcol = sa_mix(ecol, col, 0.45)
            rbase = _sa_c(mix(prof["roof_c"], (255, 255, 255), style.get("roof_mix", 0.45)))
            rcol = col if TYPO[prof["kind"]]["roof"] == "shed" else sa_mix(rbase, fade_to, f)
            tcol = sa_mix(_sa_c(mix(TYPO_TIMBER_C, (255, 255, 255), 0.3)), fade_to, f)
            bld_raster(art, prof, xp, yp, col, ecol, wcol, rcol, res, tcol=tcol)
        elif kind == "bridge":
            br = it[1]
            f = sa_fade(d, SA_DEPTH_B, 0.15, 0.8)
            col = sa_mix(_sa_c(style["bridge"]), fade_to, f)
            xa, xb = xp(br["s0"]), xp(br["s1"])
            sa_fill(art, [[(xa, yp(br["z"] + 0.15)), (xb, yp(br["z"] + 0.15)), (xb, yp(br["z"] - 0.6)), (xa, yp(br["z"] - 0.6))]],
                 col)
            sa_stroke(art, [(xa, yp(br["z"] + 1.1)), (xb, yp(br["z"] + 1.1))], 0.8, col, 0.8)
        else:
            t = it[1]
            f = sa_fade(d, SA_DEPTH_T, style.get("tree_fade0", 0.06), 0.82)
            lf = leaf if t["kind"] == "tree" else 1.0
            sp = sa_tree(t["kind"], xp(t["s"]), yp(t["zg"]), yp(t["zg"] + t["lo"]), yp(t["zg"] + t["hi"]),
                             t["r"] / res, t["seed"], leaf=lf, season=season)
            if sp is not None:
                wash = style.get("tree_wash", 0.0)
                sp.onto(art, alpha=style["tree_alpha"] * (1.0 - 0.45 * f), toward=fade_to, fade=min(0.92, wash + f))
    if people and ground is not None:
        gs = [p[0] for p in ground]

        def g_at(s):
            k = max(0, min(len(ground) - 1, _bisect_right(gs, s) - 1))
            k1 = min(len(ground) - 1, k + 1)
            (sa_, za), (sb_, zb) = ground[k], ground[k1]
            return za if sb_ <= sa_ else za + (zb - za) * (s - sa_) / (sb_ - sa_)
        pcol = _sa_c(style["people"])
        for s, kind, scale, flip in sa_people(sc, g_at, int(abs(sc["a"][0] * 13 + sc["a"][1] * 7)) % 99991):
            if not (s0 <= s <= s1):
                continue
            P, (hx, hy, hr) = sa_figure(kind, s, g_at(s), scale, flip, 1.0 / res, xp, yp)
            sa_fill(art, [P], pcol, 0.82)
            sa_blob(art, hx, hy, max(0.5, hr), pcol, 0.82, soft=0.6)
    return art, res


#@include ../../common/_sa_c.py


# ============================================================ TECHNICAL SECTIONS · the seven analyses cut vertically
# Every technical analysis can also be cut along lines of its own (inputs sound_sections, heat_sections, shade_sections,
# solar_sections, wind_sections, air_sections, felt_sections). A section shows the analysis in the vertical plane of its
# line at true scale, from the ground and the stream bed up above the roofs, with the cut buildings (the same prisms the
# analyses use), the cut tree crowns, the terrain and the water; one sheet per line with four strips: the four seasons
# (sound: Lden and the day, evening and night levels), on the colour scales of the plan sheets. The plan models are
# evaluated at every height of the plane:
#   sound   NoiseModel (the plan's model, receivers every 1 m up each column)
#   heat    Landsat surface temperature along the ground and the roofs under the line
#   shade   hours out of the sun on the key day, 15-minute steps, exact 3D shadows of every building prism (absolute
#           heights), tree crown and the terrain horizon at every point of the plane
#   solar   kWh/m2 over the season on the ground (the plan's ground model), the cut roofs and the cut facades (the plan's
#           roof and facade model)
#   wind    the plan's wind at 1.5 m brought to every height with the log law, and the windbreak shelter of the
#           buildings and crowns upwind taken from their height above that point
#   air     dry bulb with the standard lapse rate at every height
#   felt    UTCI at every point of the plane: air, local wind, sun or shade and the sky that point sees
# Everything is kept between runs (selinus_cache): the line's geometry, every field, and the sky seen from the line
# (shared by the felt temperature and solar sections of the same line), the wind shelter (shared by wind and felt).
TSEC_DEF = [("sound_sections", "T1", "SOUND"), ("heat_sections", "T2", "SURFACE HEAT"), ("shade_sections", "T3", "SHADE"),
            ("solar_sections", "T4", "SOLAR RADIATION"), ("wind_sections", "T5", "WIND"),
            ("air_sections", "T6", "AIR TEMPERATURE"), ("felt_sections", "T7", "FELT TEMPERATURE")]
TSEC_DS = 0.5            # m between the columns of the sky, wind, air and felt fields (plus one outside every cut wall;
#                          v16.6: 1.0 -> 0.5)
TSEC_DZ = 0.5            # m between their heights
TSEC_DS_SHADE = 0.25     # v16.6: m between the columns of the shade field (v16.5: 1.0, as the other fields)
TSEC_DZ_SHADE = 0.25     # v16.6: m between its heights (v16.5: 0.5)
TSEC_DS_SOLAR = 0.25     # v16.6: m between the solar points on the ground and on the cut roofs (v16.5: ground every
#                          1.0 m plus one 0.25 m outside every cut wall, roofs every 1.5 m)
TSEC_DZ_SOLAR = 0.5      # v16.6: m: the cut facades in bands of at most this height (v16.5: 1.5)
TSEC_DS_SOUND = 2.5      # m between sound columns (plus one outside every cut wall)
TSEC_DZ_SOUND = 1.0      # m between the sound receivers of a column
TSEC_HEAD = 8.0          # m of air shown above the highest cut roof, crown or ground
TSEC_FETCH = 300.0       # m searched upwind for shelter, as on the plan
TSEC_LN10 = math.log(10.0 / 0.1)
TSEC_LN15 = math.log(1.5 / 0.1)


def tsec_lines(S):
    """The lines of every technical section input, trimmed to the frame (the analyses stop at it). Computed once per
    bake; skipped and trimmed lines are reported by their number in their input."""
    memo = env_memo(S)
    r = memo.get(("tsec_lines", repr(TSEC)))
    if r is not None:
        return r
    out = {}
    trimmed = []
    for key, num, title in TSEC_DEF:
        lst = []
        tr = []
        for k, (a, b) in enumerate(TSEC.get(key) or []):
            runs = S.F.clip_line([a, b])
            if not runs:
                LOG.append("{} line {} lies outside the frame and was skipped.".format(key, k + 1))
                continue
            p, q = tuple(runs[0][0]), tuple(runs[0][-1])
            if math.hypot(q[0] - p[0], q[1] - p[1]) < 10.0:
                LOG.append("{} line {} is shorter than 10 m inside the frame and was skipped.".format(key, k + 1))
                continue
            if math.hypot(p[0] - a[0], p[1] - a[1]) + math.hypot(q[0] - b[0], q[1] - b[1]) > 1.0:
                tr.append(str(k + 1))
            lst.append((k, p, q))                         # k: the line's place in its input (its number)
        if tr:
            trimmed.append("{} {}".format(key, ", ".join(tr)))
        out[key] = lst
    if trimmed:
        LOG.append("Technical section lines trimmed to the frame: " + "; ".join(trimmed) + ".")
    memo[("tsec_lines", repr(TSEC))] = out
    return out


def line_poly_cross(P, ox, oy, ux, uy):
    """Where the infinite line o + s u crosses polygon P: [(s, outward normal of the crossed edge)], sorted. Each
    vertex belongs to one side only, so the crossings pair up into the inside intervals."""
    out = []
    P = ccw(P)                                           # outward normals need a counter-clockwise ring
    n = len(P)
    for q in range(n):
        ax, ay = P[q]
        bx, by = P[(q + 1) % n]
        sa = ux * (ay - oy) - uy * (ax - ox)
        sb = ux * (by - oy) - uy * (bx - ox)
        if (sa > 0) != (sb > 0):
            ex, ey = bx - ax, by - ay
            le = math.hypot(ex, ey)
            out.append((((ax - ox) * ey - (ay - oy) * ex) / (ux * ey - uy * ex), (ey / le, -ex / le)))
    out.sort()
    return out


def tsec_geom_make(S, a, b):
    """Ground (stream bed carved as on the land-use sections), water, cut buildings and cut crowns along one line."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    step = 0.5
    smp = []
    for k in range(int(L / step) + 1):
        s = k * step
        px, py = x0 + ux * s, y0 + uy * s
        z_ = S.z_at(px, py)
        smp.append([s, classify_point(S, px, py)[0] == "water", z_, z_])
    if smp[-1][0] < L - 1e-6:
        z_ = S.z_at(x1, y1)
        smp.append([L, classify_point(S, x1, y1)[0] == "water", z_, z_])
    water = []
    k = 0
    while k < len(smp):
        if not smp[k][1]:
            k += 1
            continue
        k0 = k
        while k < len(smp) and smp[k][1]:
            k += 1
        za = smp[max(0, k0 - 2)][2]
        zb = smp[min(len(smp) - 1, k)][2]
        bank = min(za, zb)
        bed = min(r[2] for r in smp[k0:k])
        if bank - bed < 1.0:
            sm = (smp[k0][0] + smp[k - 1][0]) / 2.0
            dd_ = bed_depth(S, x0 + ux * sm, y0 + uy * sm)
            if dd_ is not None:
                bed = bank - dd_
        for r in smp[k0:k]:
            r[2] = bed
        sm_ = (smp[k0][0] + smp[k - 1][0]) / 2.0
        water.append((smp[k0][0], min(L, smp[k - 1][0] + step), bed, water_level(S, x0 + ux * sm_, y0 + uy * sm_, bed, bank)[0]))
    ground = [(r[0], r[2]) for r in smp]
    terrain = [(r[0], r[3]) for r in smp]                # before the stream bed was carved
    bl, gB, trees = S.env["solids"]
    bidx = S.env["bindex"]
    box = (min(x0, x1) - 1.0, min(y0, y1) - 1.0, max(x0, x1) + 1.0, max(y0, y1) + 1.0)
    cut = []
    for bo in gB.query(box):
        cr = line_poly_cross(bo["P"], x0, y0, ux, uy)
        u = bo.get("u") or {}
        for q in range(0, len(cr) - 1, 2):
            (s0, n0), (s1, n1) = cr[q], cr[q + 1]
            s0, s1 = max(0.0, s0), min(L, s1)
            if s1 - s0 > 0.02:
                cut.append((s0, s1, bo["base"], bo["top"], bidx[id(bo)], u.get("fabric", "regular"),
                            u.get("cat", "residential"), bool(u.get("annex")), n0, n1))
    cut.sort()
    crowns = []
    for ti, t in enumerate(trees):
        r = t["r"]
        if not (box[0] - r <= t["x"] <= box[2] + r and box[1] - r <= t["y"] <= box[3] + r):
            continue
        d = -(t["x"] - x0) * uy + (t["y"] - y0) * ux
        if abs(d) >= r:
            continue
        sc_ = (t["x"] - x0) * ux + (t["y"] - y0) * uy
        hw = math.sqrt(r * r - d * d)
        if sc_ + hw <= 0.0 or sc_ - hw >= L:
            continue
        crowns.append((sc_, hw, t["base"] + t["lo"], t["base"] + t["hi"], t["kind"], ti))
    zg = [z for s, z in ground]
    tops = [c[3] + typo_rise(c[5], c[6], c[1] - c[0], c[3] - c[2],
                             c[5] == "sacred" and has_minaret(bl[c[4]].get("u") or {})[0]) + 1.0 for c in cut] + \
        [c[3] for c in crowns]
    zlo = math.floor(min(zg)) - 1.0
    zhi = math.ceil(max([max(zg)] + tops)) + TSEC_HEAD
    return dict(a=tuple(a), b=tuple(b), L=L, ux=ux, uy=uy, ground=ground, terrain=terrain, water=water, cut=cut,
                crowns=crowns, zlo=zlo, zhi=zhi)


def tsec_geom(S, a, b):
    """The geometry of one line, kept between runs (the same line in several inputs is built once)."""
    memo = env_memo(S)
    mk = ("tsec_geom", a, b)
    G = memo.get(mk)
    if G is not None:
        return G
    pr = site_prints(S)
    C = getattr(S, "chan", None) or {}
    key = fp("sec_geom", MV["sec_geom"], S.env["keys"]["solids"], pr["terrain"], pr["water"], pr["bld"], CH_DEPTH,
             water_key(S), TSEC_HEAD, a, b, C.get("ch"), C.get("d"))
    ST = S.store
    G = ST.get("sec_geom", key)
    if G is None:
        G = ST.put("sec_geom", key, tsec_geom_make(S, a, b))
    G = dict(G, key=key)
    memo[mk] = G
    return G


def tsec_zg(G, s, key="ground"):
    """Ground (or stream bed) height at s, linear between the 0.5 m samples (key="terrain": before the carving)."""
    g = G[key]
    k = int(s / 0.5)
    if k <= 0:
        k = 0
    if k >= len(g) - 1:
        return g[-1][1]
    s0, z0 = g[k]
    s1, z1 = g[k + 1]
    return z0 + (z1 - z0) * ((s - s0) / (s1 - s0) if s1 > s0 else 0.0)


def tsec_cols(S, G, ds):
    """Columns of a field: every ds along the line and one 0.25 m (half a column if less) outside every cut wall.
    Each column: (s, x, y, ground, surface (ground or water level), roof of the cut building it stands in or None,
    roof of the cut building whose wall it faces or None, terrain before the stream bed was carved)."""
    memo = env_memo(S)
    mk = ("tsec_cols", G["key"], ds)
    r = memo.get(mk)
    if r is not None:
        return r
    L = G["L"]
    cut = G["cut"]

    def inside(s):
        for c in cut:
            if c[0] <= s <= c[1]:
                return c
        return None
    vals = [((i + 0.5) * ds, False) for i in range(int(L / ds))]
    walls = {}
    wo = min(0.25, 0.5 * ds)                              # v16.6: half a column at most (0.25 m as before for 0.5 m+)
    for c in cut:
        for s in (c[0] - wo, c[1] + wo):
            if 0.0 < s < L and inside(s) is None:
                vals.append((s, True))
                walls[s] = max(walls.get(s, -1e30), c[3])
    vals.sort()
    keep = []
    for s, isw in vals:                                   # columns closer than 5 cm: one kept, a wall's own first
        if keep and s - keep[-1][0] < 0.05:
            if isw and not keep[-1][1]:
                keep[-1] = (s, True)
            continue
        keep.append((s, isw))
    vals = [s for s, isw in keep]
    out = []
    for s in vals:
        zg = tsec_zg(G, s)
        zs = zg
        for w0, w1, bed, lvl in G["water"]:
            if w0 <= s <= w1:
                zs = max(zg, lvl)
        c = inside(s)
        out.append((s, G["a"][0] + G["ux"] * s, G["a"][1] + G["uy"] * s, zg, zs, c[3] if c else None, walls.get(s),
                    tsec_zg(G, s, "terrain")))
    memo[mk] = out
    return out


def tsec_k0(c, zlo, dz, hmin):
    """First height index of a column in open air: hmin above the ground or water, above the roof inside a building."""
    lim = c[4] + hmin if c[5] is None else max(c[4] + hmin, c[5] + 1e-6)
    return max(0, int(math.ceil((lim - zlo) / dz - 0.5)))


def tsec_nz(G, dz):
    return int(math.ceil((G["zhi"] - G["zlo"]) / dz))


def casters_frame(S, reach=ENV_REACH):
    """The casters of the frame (walls, crowns, horizons), built once per bake and shared by every section line."""
    memo = env_memo(S)
    C = memo.get(("casters16", reach))
    if C is None:
        C = memo[("casters16", reach)] = Casters16(S, S.env["E"], S.env["solids"], S.F, reach)
    return C


def slope_normals(S, X, Y, h=6.0):
    """The plan's ground normal at points (slope over 6 m, capped at 35 degrees): world x, y and up."""
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    zx = (z_np(S, X + h, Y) - z_np(S, X - h, Y)) / (2.0 * h)
    zy = (z_np(S, X, Y + h) - z_np(S, X, Y - h)) / (2.0 * h)
    sl = np.hypot(zx, zy)
    f = np.where(sl > 0.7, 0.7 / np.where(sl > 0, sl, 1.0), 1.0)
    zx, zy = zx * f, zy * f
    n_ = np.sqrt(zx * zx + zy * zy + 1.0)
    return -zx / n_, -zy / n_, 1.0 / n_


def tsec_plane(S, G, ds=None, dz=None):
    """The receivers of a line's plane: per column (every ds along the line and one outside every cut wall) the
    heights every dz from 0.25 m above the ground or water (above the roof inside a cut building) to the top, as
    point receivers with the ground's slope under them. Built once per line, spacing and bake (v16.6: the shade has
    its own, finer plane: TSEC_DS_SHADE, TSEC_DZ_SHADE)."""
    ds = TSEC_DS if ds is None else ds
    dz = TSEC_DZ if dz is None else dz
    memo = env_memo(S)
    mk = ("tsec_plane", G["key"], ds, dz)
    r = memo.get(mk)
    if r is not None:
        return r
    cols = tsec_cols(S, G, ds)
    zlo = G["zlo"]
    nz = tsec_nz(G, dz)
    k0 = np.array([tsec_k0(c, zlo, dz, 0.25) for c in cols], np.int64)
    cnt = np.maximum(nz - k0, 0)
    pid = np.repeat(np.arange(len(cols)), cnt)
    kz = np.repeat(k0, cnt) + (np.arange(int(cnt.sum())) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    Z = zlo + (kz + 0.5) * dz
    X = np.array([c[1] for c in cols])
    Y = np.array([c[2] for c in cols])
    terr = np.array([c[7] for c in cols])
    nwx, nwy, nzz = slope_normals(S, X, Y)
    hg = np.maximum(0.0, Z - terr[pid])                       # height above the ground: the slope's plane falls away
    hgl = np.maximum(0.25, Z - terr[pid])
    C = casters_frame(S)
    P = Points16(C, X, Y, pid, Z, nrm=(nwx[pid], nwy[pid], nzz[pid]), hg=hg, zair=Z - 2.0,
                 wf=np.log(hgl / 0.1) / TSEC_LN15)
    tab = hz_fall_table(S, C, X, Y, terr)
    if tab is not None:
        P.hzf = HzFall(tab, C.step, pid, hg)
    r = memo[mk] = dict(P=P, cols=cols, pid=pid, kz=kz, nz=nz, zlo=zlo, dz=dz, hgl=hgl)
    return r


def tsec_vals(pl, v):
    """Receiver values back to the columns of the plane (None below a column's first height)."""
    out = [[None] * pl["nz"] for _ in pl["cols"]]
    for p, k, x in zip(pl["pid"].tolist(), pl["kz"].tolist(), np.asarray(v, float).tolist()):
        out[p][k] = (None if x != x else x)
    return out


def tsec_shade(S, G):
    """Hours out of the sun at every point of the plane: the four key days and the mean day of the year, every minute
    the sun is up, through the exact 3D obstruction of every point (as on the plan, T3). v16.6: on its own plane every
    TSEC_DS_SHADE along the line and TSEC_DZ_SHADE in height (v16.5: 1.0 m x 0.5 m)."""
    keys = S.env["keys"]
    key = fp("sec_shade", MV["sec_field"], G["key"], keys["solids"], TSEC_DS_SHADE, TSEC_DZ_SHADE, SUN_BINS)
    res = S.store.get("sec_shade", key)
    if res is not None:
        return res
    pl = tsec_plane(S, G, TSEC_DS_SHADE, TSEC_DZ_SHADE)
    P = pl["P"]
    memo = env_memo(S)
    MS = memo.get("minute_sun")
    if MS is None:
        MS = memo["minute_sun"] = minute_sun(S.env["E"])
    SJ = ShadeJob(P, MS)
    sun_pass(P, casters_frame(S), [SJ])
    out = dict(zlo=pl["zlo"], dz=pl["dz"], nz=pl["nz"], s=[c[0] for c in pl["cols"]], days={})
    for k, sd in enumerate(SEASONS):
        out["days"][sd["key"]] = dict(SJ.days[k], vals=tsec_vals(pl, SJ.acc[2 + k] / 60.0))
    out["year"] = dict(daylight=SJ.year_daylight, vals=tsec_vals(pl, (SJ.acc[0] + SJ.acc[1]) / 60.0 / 365.0))
    return S.store.put("sec_shade", key, out)


def tsec_sky(S, G):
    """The sky view of every point of the plane (solid angle, crowns in and out of leaf), kept per line."""
    memo = env_memo(S)
    mk = ("tsec_sky", G["key"])
    r = memo.get(mk)
    if r is None:
        key = fp("sec_sky", MV["sec_field"], G["key"], S.env["keys"]["solids"], TSEC_DS, TSEC_DZ, SKY_BINS)
        r = S.store.get("sec_sky", key)
        if r is None:
            pl = tsec_plane(S, G)
            r = S.store.put("sec_sky", key, sky_pass(pl["P"], casters_frame(S))["svf"])
        memo[mk] = r
    return r


def tsec_shelter(S, G):
    """Share of the open-ground wind left at every point of the plane for every wind sector, crowns in and out of
    leaf: each building and crown upwind within the fetch (exact distance along the wind) counts with its height above
    that point's level (height above ground - 1.5 m) through the plan's windbreak wake curves; at 1.5 m above ground
    this is the plan's shelter. (sectors, leaf, receivers)"""
    memo = env_memo(S)
    mk = ("tsec_shelter", G["key"])
    r = memo.get(mk)
    if r is not None:
        return r
    pl = tsec_plane(S, G)
    P = pl["P"]
    Cw = casters_frame(S, TSEC_FETCH)
    R = TSEC_FETCH
    n = P.n
    ok_e = ((np.maximum(Cw.AX, Cw.BX) >= P.pu.min() - R) & (np.minimum(Cw.AX, Cw.BX) <= P.pu.max() + R) &
            (np.maximum(Cw.AY, Cw.BY) >= P.pv.min() - R) & (np.minimum(Cw.AY, Cw.BY) <= P.pv.max() + R))
    AX, AY, BX, BY, own, Hb = Cw.AX[ok_e], Cw.AY[ok_e], Cw.BX[ok_e], Cw.BY[ok_e], Cw.own[ok_e], Cw.HB[ok_e]
    ok_c = ((Cw.CU + Cw.CR >= P.pu.min() - R) & (Cw.CU - Cw.CR <= P.pu.max() + R) &
            (Cw.CV + Cw.CR >= P.pv.min() - R) & (Cw.CV - Cw.CR <= P.pv.max() + R))
    CU, CV, CR, CHR, CK = Cw.CU[ok_c], Cw.CV[ok_c], Cw.CR[ok_c], Cw.CHR[ok_c], Cw.CK[ok_c]
    cgrp = np.where(CK == 2, 2, 1)                        # 1 evergreen (pine, olive), 2 deciduous
    cc = pl["hgl"] - 1.5                                  # each receiver's level: height above the ground - 1.5 m
    out = np.ones((WIND_BINS, 2, n), np.float32)
    BIG = 1 << 40
    for k in range(WIND_BINS):
        d = Cw.dir_local(k * 360.0 / WIND_BINS)           # toward where the wind comes from
        dx, dy = d
        obs_p, obs_x, obs_h, obs_g = [], [], [], []
        if AX.size:
            aA, bA = AX * dx + AY * dy, -AX * dy + AY * dx
            aB, bB = BX * dx + BY * dy, -BX * dy + BY * dx
            okb = bA != bB
            e, p, bp = P._pairs(d, np.where(okb, np.minimum(bA, bB), np.inf), np.where(okb, np.maximum(bA, bB), -np.inf))
            if e.size:
                ap = P.pu[p] * dx + P.pv[p] * dy
                t = aA[e] + (bp[p] - bA[e]) * (aB[e] - aA[e]) / (bB[e] - bA[e]) - ap
                m = t > 0.0
                e, p, t = e[m], p[m], t[m]
                kb = p.astype(np.int64) * BIG + own[e]
                o = np.lexsort((t, kb))
                kb, t, e = kb[o], t[o], e[o]
                first = np.flatnonzero(np.r_[True, kb[1:] != kb[:-1]])
                cnt_ = np.diff(np.r_[first, kb.size])
                use = (cnt_ % 2 == 0) & (t[first] <= R)    # an odd count: the point stands in that building
                obs_p.append((kb[first] // BIG)[use])
                obs_x.append(t[first][use])
                obs_h.append(Hb[e[first]][use])
                obs_g.append(np.zeros(int(use.sum()), np.int64))
        if CU.size:
            ac, bc = CU * dx + CV * dy, -CU * dy + CV * dx
            e, p, bp = P._pairs(d, bc - CR, bc + CR)
            if e.size:
                perp = bp[p] - bc[e]
                m = np.abs(perp) < CR[e]
                e, p, perp = e[m], p[m], perp[m]
                hw = np.sqrt(CR[e] ** 2 - perp ** 2)
                along = ac[e] - (P.pu[p] * dx + P.pv[p] * dy)
                m = (along + hw > 0.0) & (along - hw <= R)
                e, p, along, hw = e[m], p[m], along[m], hw[m]
                obs_p.append(p)
                obs_x.append(np.maximum(0.0, along - hw))
                obs_h.append(CHR[e])
                obs_g.append(cgrp[e])
        if not obs_p:
            continue
        op, ox, oh, og = (np.concatenate(q) for q in (obs_p, obs_x, obs_h, obs_g))
        k0, cntr = P.r0[op], P.r1[op] - P.r0[op]
        tot = int(cntr.sum())
        if tot == 0:
            continue
        q = np.repeat(np.arange(op.size), cntr)
        r = np.repeat(k0, cntr) + (np.arange(tot) - np.repeat(np.cumsum(cntr) - cntr, cntr))
        he = oh[q] - cc[r]
        m = he > 0.0
        q, r, he = q[m], r[m], he[m]
        Q = np.full((3, n), np.inf)
        np.minimum.at(Q, (og[q], r), ox[q] / he)
        fB = wake_np(WAKE_SOLID, Q[0])
        fE = wake_np(WAKE_LEAFY, Q[1])
        base = np.minimum(fB, fE)
        out[k, 0] = np.minimum(base, wake_np(WAKE_LEAFY, Q[2]))
        out[k, 1] = np.minimum(base, wake_np(WAKE_BARE, Q[2]))
    memo[mk] = out
    return out


def tsec_comfort(S, G):
    """Per season, the means over the window hours at every point of the plane: felt temperature (UTCI) every hour
    with that point's sun or shade, sky view and wind; the wind at that height; the air temperature."""
    keys = S.env["keys"]
    key = fp("sec_comfort", MV["sec_field"], G["key"], keys["solids"], keys["comfort"], TSEC_DS, TSEC_DZ)
    res = S.store.get("sec_comfort", key)
    if res is not None:
        return res
    pl = tsec_plane(S, G)
    P = pl["P"]
    TT = S.env["TT"]
    win = window_mask(TT)
    svf = tsec_sky(S, G)
    shel = tsec_shelter(S, G)
    CJ = ComfortJob(P, TT, win, svf, shel)
    sun_pass(P, casters_frame(S), [CJ])
    CJ.finish()
    lnw = np.log(pl["hgl"] / 0.1) / TSEC_LN10             # the log law from 10 m to each height
    out = dict(zlo=pl["zlo"], dz=pl["dz"], nz=pl["nz"], s=[c[0] for c in pl["cols"]], seasons={})
    for si, sd in enumerate(SEASONS):
        hs = np.flatnonzero(win & (TT["si"] == si))
        N = max(1, hs.size)
        W = np.zeros((WIND_BINS, 2))
        np.add.at(W, (wind_bin(TT["wd10"][hs]), np.where(TT["leaf"][hs], 0, 1)), TT["ws10"][hs])
        wind = np.zeros(P.n)
        for kk, ll in zip(*np.nonzero(W)):
            wind += W[kk, ll] * shel[kk, ll]
        wind *= lnw / N
        sun_h = int(((TT["el"][hs] >= 2.0) & (TT["dni"][hs] > 0.0)).sum())
        out["seasons"][sd["key"]] = dict(
            hours=int(hs.size), utci=tsec_vals(pl, CJ.su[si] / N), sun=tsec_vals(pl, CJ.sT[si] / max(1, sun_h)),
            ta=tsec_vals(pl, float(TT["t2m"][hs].mean()) + CJ.dl), wind=tsec_vals(pl, wind),
            ta_mean=float(TT["t2m"][hs].mean()) if hs.size else None, u10_mean=float(TT["ws10"][hs].mean()) if hs.size else None,
            rh_mean=float(TT["rh"][hs].mean()) if hs.size else None)
    return S.store.put("sec_comfort", key, out)


def tsec_solar(S, G):
    """Mean kWh/m2 per day of each season on the ground under the line, on the cut roofs and on the cut facades: the
    plan's model (T4) at each of these points, every hour of the typical year, each with its own exact 3D
    obstruction, cosine-weighted sky and own plane.
    v16.6: the ground and the roofs evenly every TSEC_DS_SOLAR (0.25 m), each point standing for the strip of that
    width around it; the facades in bands of at most TSEC_DZ_SOLAR. v16.5 sampled the ground every 1.0 m plus one extra
    point 0.25 m outside every cut wall, and the roofs every 1.5 m: the extra wall-foot points (the darkest ground of
    an alley) stood for 0.25 m but were joined by straight lines to points 1 m away, so every cut wall drew a sharp V
    in the graph; the more buildings a section cuts, the more V's. Ground: (s0, s1, z, values)."""
    keys = S.env["keys"]
    key = fp("sec_solar", MV["sec_field"], G["key"], keys["solids"], TSEC_DS_SOLAR, TSEC_DZ_SOLAR, SUN_BINS, SKY_BINS)
    res = S.store.get("sec_solar", key)
    if res is not None:
        return res
    (x0, y0), ux, uy = G["a"], G["ux"], G["uy"]
    pts = []                                              # (kind, x, y, z, nx, ny, nz, info)
    cut = G["cut"]
    ds = TSEC_DS_SOLAR
    sp_ = sorted((c[0], c[1]) for c in cut)
    opn, a_ = [], 0.0                                     # the open stretches of the line, between the cut buildings
    for c0, c1 in sp_:
        if c0 > a_:
            opn.append((a_, min(c0, G["L"])))
        a_ = max(a_, c1)
    if a_ < G["L"]:
        opn.append((a_, G["L"]))
    gs = []
    for o0, o1 in opn:                                    # strips of at most ds, ending at the walls
        n = int(math.ceil((o1 - o0) / ds - 1e-9))
        for q in range(n):
            gs.append((o0 + (o1 - o0) * q / n, o0 + (o1 - o0) * (q + 1) / n))
    if gs:
        sm = np.array([0.5 * (p[0] + p[1]) for p in gs])
        gx, gy = x0 + ux * sm, y0 + uy * sm
        nwx, nwy, nzz = slope_normals(S, gx, gy)
        for q, (p0, p1) in enumerate(gs):
            s_ = float(sm[q])
            zg = tsec_zg(G, s_)
            zs = zg
            for w0, w1, bed, lvl in G["water"]:
                if w0 <= s_ <= w1:
                    zs = max(zg, lvl)
            pts.append(("g", float(gx[q]), float(gy[q]), zs + 0.05, nwx[q], nwy[q], nzz[q], (p0, p1, zs)))
    for ci, c in enumerate(cut):
        s0, s1, base, top, bi = c[:5]
        n = max(1, int(math.ceil((s1 - s0) / ds - 1e-9)))
        for q in range(n):
            a_, b_ = s0 + (s1 - s0) * q / n, s0 + (s1 - s0) * (q + 1) / n
            sm = (a_ + b_) / 2.0
            pts.append(("r", x0 + ux * sm, y0 + uy * sm, top + 0.05, 0.0, 0.0, 1.0, (a_, b_, top)))
        for s_w, nrm, outer in ((s0, c[8], s0 - 0.3), (s1, c[9], s1 + 0.3)):
            if not (0.0 < s_w < G["L"]):
                continue                                  # the wall is the end of the line, not a cut facade
            lo = tsec_zg(G, min(max(outer, 0.0), G["L"]))
            for c2 in cut:
                if c2 is not c and c2[0] - 0.3 <= outer <= c2[1] + 0.3:
                    lo = max(lo, c2[3])                   # a lower neighbour: only the wall above its roof is exposed
            if top - lo < 0.5:
                continue
            nb_ = max(1, min(120, int(math.ceil((top - lo) / TSEC_DZ_SOLAR - 1e-9))))
            px, py = x0 + ux * s_w + nrm[0] * 0.05, y0 + uy * s_w + nrm[1] * 0.05
            for q in range(nb_):
                z0, z1 = lo + (top - lo) * q / nb_, lo + (top - lo) * (q + 1) / nb_
                pts.append(("w", px, py, (z0 + z1) / 2.0, nrm[0], nrm[1], 0.0, (s_w, z0, z1, 1 if outer > s_w else -1, nrm)))
    out = dict(ground=[], roofs=[], walls=[])
    if not pts:
        return S.store.put("sec_solar", key, out)
    E = S.env["E"]
    C = casters_frame(S)
    n = len(pts)
    P = Points16(C, [p[1] for p in pts], [p[2] for p in pts], np.arange(n), [p[3] for p in pts],
                 nrm=(np.array([p[4] for p in pts]), np.array([p[5] for p in pts]), np.array([p[6] for p in pts])))
    PX, PY = np.array([p[1] for p in pts]), np.array([p[2] for p in pts])
    PG = z_np(S, PX, PY)
    tab = hz_fall_table(S, C, PX, PY, PG)
    if tab is not None:
        P.hzf = HzFall(tab, C.step, np.arange(n), np.array([p[3] for p in pts]) - PG)
    TT = S.env["TT"]
    sky = sky_pass(P, C, want_k=True)
    RJ = RadJob(P, TT, C.CP)
    sun_pass(P, C, [RJ])
    vals = rad_totals(P, TT, sky, RJ)
    for k, p in enumerate(pts):
        v = dict((sd["key"], float(vals[sd["key"]][k])) for sd in SEASONS)
        if p[0] == "g":
            out["ground"].append(p[7] + (v,))
        elif p[0] == "r":
            out["roofs"].append(p[7] + (v,))
        else:
            out["walls"].append(p[7] + (v,))
    return S.store.put("sec_solar", key, out)


def tsec_noise_key(S, G):
    return fp("sec_noise", MV["sec_field"], G["key"], S.env["keys"]["noise_raw"], TSEC_DS_SOUND, TSEC_DZ_SOUND)


def tsec_noise_prep(S, G):
    cols = tsec_cols(S, G, TSEC_DS_SOUND)
    zlo, dz = G["zlo"], TSEC_DZ_SOUND
    nz = tsec_nz(G, dz)
    k0s, tasks = [], []
    for c in cols:
        k0 = tsec_k0(c, zlo, dz, 0.5)
        zrs = [zlo + (kz + 0.5) * dz for kz in range(k0, nz)]
        k0s.append(k0)
        if zrs:
            tasks.append((c[1], c[2], c[4], zrs))
    return cols, k0s, tasks, zlo, dz, nz


def tsec_noise_start(S):
    """v17: the receivers of every sound section not in the store, all lines in one batch, handed to the worker
    processes before the plan sheets are drawn: they run while Rhino draws and computes the other analyses."""
    lines = tsec_lines(S).get("sound_sections") or []
    pre, tasks = {}, []
    job = dict()
    for k, a, b in lines:
        G = tsec_geom(S, a, b)
        key = tsec_noise_key(S, G)
        if key in pre or S.store.get("sec_noise", key) is not None:
            continue
        prep = tsec_noise_prep(S, G)
        pre[key] = dict(prep=prep, job=job, at=len(tasks))
        tasks += prep[2]
    if tasks:
        job["h"] = noise_par_start(noise_model(S), tasks, "multi", "sections")
    S.env["tsec_noise_pre"] = pre


def tsec_noise(S, G):
    """Road traffic noise at every receiver of the plane (the plan's model), day, evening, night and Lden; the plan's
    calibration offset is added on use."""
    key = tsec_noise_key(S, G)
    res = S.store.get("sec_noise", key)
    if res is None:
        pre = (S.env.get("tsec_noise_pre") or {}).pop(key, None)       # v17: started early with every other line
        cols, k0s, tasks, zlo, dz, nz = pre["prep"] if pre else tsec_noise_prep(S, G)
        vals = dict(day=[], evening=[], night=[], lden=[])
        if pre:
            job = pre["job"]
            if "out" not in job:
                job["out"] = noise_par_collect(job["h"])
            got = job["out"][pre["at"]:pre["at"] + len(tasks)]
        else:
            got = noise_par(noise_model(S), tasks, "multi", "section")      # v17: on every core
        rs_ = iter(got)
        for c, k0 in zip(cols, k0s):
            r = next(rs_) if k0 < nz else []
            for p, nm_ in enumerate(("day", "evening", "night", "lden")):
                vals[nm_].append([None] * k0 + [(q[p] if q else None) for q in r])
        res = S.store.put("sec_noise", key, dict(zlo=zlo, dz=dz, nz=nz, s=[c[0] for c in cols], vals=vals))
    off = S.env["noise"].get("offset", 0.0)
    if off:
        res = dict(res, vals=dict((k, [[(v + off if v is not None else None) for v in col] for col in cols_])
                                  for k, cols_ in res["vals"].items()))
    return res


def tsec_heat(S, G, season):
    """Landsat surface temperature along the line every metre, on the roof where it crosses a building, else on the
    ground or water (bilinear in the scene's 30 m grid, as the plan samples it)."""
    L_ = S.env["lst"].get(season)
    if not L_:
        return None
    out = []
    n = int(G["L"])
    for i in range(n):
        s = i + 0.5
        x, y = G["a"][0] + G["ux"] * s, G["a"][1] + G["uy"] * s
        top = None
        for c in G["cut"]:
            if c[0] <= s <= c[1]:
                top = c[3]
        z = top if top is not None else tsec_zg(G, s)
        out.append((s, z, lst_sample(L_, x, y), top is not None))
    return out


# ------------------------------------------------------------ technical sections: pictures, drawing, sheets


def bands_key(bands):
    return fp([(round(a, 6), round(b, 6), round(c, 6), round(d, 6), v) for a, b, c, d, v in bands])


def tsec_keyplan_png(S, d):
    """The key plan's base as one picture (buildings, water, open ground at 2 m), shared by every section sheet."""
    memo = env_memo(S)
    r = memo.get("tsec_keyplan")
    if r is not None:
        return r
    path = os.path.join(d, "key_plan.png")
    TB = tech_core(S, S.F, 2.0)
    w, h = TB["cv"].w, TB["cv"].h
    full = fp("keyplan", MV["render"], core_key(S, S.F, 2.0))
    e_ = maps_index(S, d).get("key_plan.png")
    try:
        if e_ and e_.get("key") == full and os.path.getsize(path) == e_.get("size"):
            memo["tsec_keyplan"] = path
            return path
    except Exception:
        pass
    bid, water = TB["bid"], TB["water"]
    pal = (bytes((244, 244, 246)), bytes((198, 198, 204)), bytes((168, 198, 222)))
    rows = []
    for py in range(h):
        o = py * w
        rows.append(b"".join(pal[1] if bid[i] else (pal[2] if water[i] else pal[0]) for i in range(o, o + w)))
    png_write(path, w, h, b"".join(rows))
    try:
        maps_index(S, d)[os.path.basename(path)] = dict(key=full, size=os.path.getsize(path), w=w, h=h)
        maps_index_save(S, d)
    except Exception:
        pass
    memo["tsec_keyplan"] = path
    return path


