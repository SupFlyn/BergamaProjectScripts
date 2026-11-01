# ---- silhouette.py (round 5 S4, 1 Nov 2026; G-R5-4.4, G-R5-6, N1, D4): one small raster engine, pure Python 3 ------
# Used by figures.py (solid dark bodies of the library people) and plants.py (toned plant images). Included by
# plants.py (#@include), so every script that draws plants or people has it. No Rhino, no PIL; numpy only if present.
#   sil_png_size(path) -> (w, h) | None             PNG / JPEG pixel size from the header only
#   sil_png_read(path) -> (w, h, rgb bytes, n colours 1|3, alpha bytes | None) | None   (8/16 bit, not interlaced)
#   sil_png_write(path, w, h, rgb, alpha)           RGBA (or RGB) 8 bit PNG, filter 0
#   sil_body(rings_m, px_m, close_m, key) -> [ring m]   the filled outline of a pen drawing: rings rasterised,
#                                                   closed (dilate + erode close_m), holes filled, traced, smoothed
#   sil_alpha_body(path, h_m, px_m, close_m, thr) -> ([ring m], w_m)   the same from a PNG's alpha (feet = bottom row)
#   sil_tone(src, dst, shade, mid, light, keep, paper, fade) -> (ok, how)   a plant image toned to its species
#                                                   colours (luminance -> shade/mid/light ramp, keep = share of the
#                                                   photo's own colour kept, then faded toward the paper by fade)
# Bitmaps are lists of Python ints, one per row (bit i = column i), row 0 at the bottom (y up).
import os as _sil_os
import zlib as _sil_zlib
import struct as _sil_st

SIL_LOG = []
_SIL_BODY = {}          # key -> rings (m), one run
_SIL_PNG = {}           # path -> decoded PNG, one run


def sil_png_size(path):
    """(w, h) in pixels of a PNG or JPEG, read from the header; None if unreadable"""
    try:
        with open(path, "rb") as f:
            d = f.read(65536)
    except Exception:
        return None
    if d[:8] == b"\x89PNG\r\n\x1a\n" and d[12:16] == b"IHDR":
        return _sil_st.unpack(">II", d[16:24])
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF:
                return None
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6]
            i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def sil_png_read(path):
    """(w, h, rgb bytes, n colours 1|3, alpha bytes or None) of a PNG (8 or 16 bit, grey/RGB/palette, +alpha,
    not interlaced), or None. Rows top to bottom as in the file. Kept in memory for the run."""
    if path in _SIL_PNG:
        return _SIL_PNG[path]
    try:
        with open(path, "rb") as f:
            d = f.read()
    except Exception:
        return None
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _sil_st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _sil_st.unpack(">IIBBBBB", c[:13])
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
    raw = _sil_zlib.decompress(b"".join(idat))
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
    if bd == 16:
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        r = (w, h, bytes(rgb), 3, alpha)
    elif ct == 0:
        r = (w, h, bytes(out), 1, None)
    elif ct == 4:
        r = (w, h, bytes(out[0::2]), 1, bytes(out[1::2]))
    elif ct == 2:
        r = (w, h, bytes(out), 3, None)
    else:
        rgb = bytearray(n * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
        r = (w, h, bytes(rgb), 3, bytes(out[3::4]))
    _SIL_PNG[path] = r
    return r


def sil_png_write(path, w, h, rgb, alpha=None):
    """writes an 8 bit RGB(A) PNG (rows top to bottom, filter 0); the folder is made"""
    if alpha is not None:
        px = bytearray(w * h * 4)
        px[0::4], px[1::4], px[2::4], px[3::4] = rgb[0::3], rgb[1::3], rgb[2::3], alpha
        bpp, ct = 4, 6
    else:
        px, bpp, ct = bytes(rgb), 3, 2
    stride = w * bpp
    raw = b"".join(b"\x00" + bytes(px[y * stride:(y + 1) * stride]) for y in range(h))

    def chunk(t, c):
        return _sil_st.pack(">I", len(c)) + t + c + _sil_st.pack(">I", _sil_zlib.crc32(t + c) & 0xffffffff)
    d = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _sil_st.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0)) +
         chunk(b"IDAT", _sil_zlib.compress(raw, 6)) + chunk(b"IEND", b""))
    _sil_os.makedirs(_sil_os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(d)


# ---- bitmaps (rows of ints) -------------------------------------------------------------------------------------------
def _sil_fill_ring(rows, ring, x0, y0, px, W):
    """ORs the inside of one closed ring (m) into rows (even-odd scanline at each row's centre)"""
    n = len(ring)
    if n < 3:
        return
    ys = [p[1] for p in ring]
    r0 = max(0, int((min(ys) - y0) / px) - 1)
    r1 = min(len(rows) - 1, int((max(ys) - y0) / px) + 1)
    full = (1 << W) - 1
    for r in range(r0, r1 + 1):
        yc = y0 + (r + 0.5) * px
        xs = []
        for i in range(n):
            ax, ay = ring[i]
            bx, by = ring[(i + 1) % n]
            if (ay <= yc < by) or (by <= yc < ay):
                xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
        xs.sort()
        m = 0
        for a, b in zip(xs[0::2], xs[1::2]):
            c0 = max(0, int(round((a - x0) / px)))
            c1 = min(W, int(round((b - x0) / px)))
            if c1 <= c0 and b - a > 0:                  # a sliver thinner than a pixel still marks one
                c0 = min(W - 1, max(0, int((0.5 * (a + b) - x0) / px)))
                c1 = c0 + 1
            if c1 > c0:
                m |= ((1 << (c1 - c0)) - 1) << c0
        rows[r] |= m & full


def _sil_dilate(rows, W, r):
    full = (1 << W) - 1
    hz = []
    for v in rows:
        a = v
        for i in range(1, r + 1):
            a |= (v << i) | (v >> i)
        hz.append(a & full)
    H = len(rows)
    out = []
    for y in range(H):
        a = 0
        for yy in range(max(0, y - r), min(H, y + r + 1)):
            a |= hz[yy]
        out.append(a)
    return out


def _sil_erode(rows, W, r):
    full = (1 << W) - 1
    inv = [(~v) & full for v in rows]
    # outside the grid counts as empty: pad so the border erodes (the grid has a margin > r, so this never bites)
    d = _sil_dilate(inv, W, r)
    return [(~v) & full for v in d]


def _sil_fill_holes(rows, W):
    """every empty region not connected to the grid border becomes filled"""
    full = (1 << W) - 1
    H = len(rows)
    emp = [(~v) & full for v in rows]
    edge = 1 | (1 << (W - 1))
    ext = [emp[y] if y in (0, H - 1) else (emp[y] & edge) for y in range(H)]
    changed = True
    while changed:
        changed = False
        for y in list(range(H)) + list(range(H - 1, -1, -1)):
            a = ext[y]
            b = a | (a << 1) | (a >> 1)
            if y > 0:
                b |= ext[y - 1]
            if y < H - 1:
                b |= ext[y + 1]
            b &= emp[y]
            while True:                                 # run along the row at once
                c = (b | (b << 1) | (b >> 1)) & emp[y]
                if c == b:
                    break
                b = c
            if b != a:
                ext[y] = b
                changed = True
    return [full & ~e for e in ext]


def _sil_bits(v):
    i = 0
    while v:
        if v & 1:
            yield i
        v >>= 1
        i += 1


def _sil_trace(rows, W):
    """outer outlines (lattice points, counter-clockwise) of the filled cells; holes must be filled before"""
    H = len(rows)
    full = (1 << W) - 1
    nxt = {}

    def add(a, b):
        nxt.setdefault(a, []).append(b)
    for y in range(H):
        v = rows[y]
        if not v:
            continue
        below = rows[y - 1] if y > 0 else 0
        above = rows[y + 1] if y < H - 1 else 0
        for x in _sil_bits(v & ~below & full):
            add((x, y), (x + 1, y))
        for x in _sil_bits(v & ~(v >> 1) & full):           # right neighbour empty
            add((x + 1, y), (x + 1, y + 1))
        for x in _sil_bits(v & ~above & full):
            add((x + 1, y + 1), (x, y + 1))
        for x in _sil_bits(v & ~(v << 1) & full):           # left neighbour empty
            add((x, y + 1), (x, y))
    loops = []
    while nxt:
        start = next(iter(nxt))
        loop, cur, prev_d = [start], start, None
        while True:
            outs = nxt.get(cur)
            if not outs:
                break
            if len(outs) > 1 and prev_d is not None:        # a pinch: turn right first (keeps the parts apart)
                def turn(b, _c=cur, _d=prev_d):
                    d = (b[0] - _c[0], b[1] - _c[1])
                    return _d[0] * d[1] - _d[1] * d[0]       # < 0 right, 0 straight, > 0 left
                outs.sort(key=turn)
            b = outs.pop(0)
            if not outs:
                del nxt[cur]
            prev_d = (b[0] - cur[0], b[1] - cur[1])
            cur = b
            if cur == start:
                break
            loop.append(cur)
        if len(loop) >= 4:
            loops.append(loop)
    return loops


def _sil_area(P):
    return 0.5 * sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def _sil_dp(P, tol):
    """Douglas-Peucker on a closed ring"""
    if len(P) < 5:
        return P
    i_far = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)

    def dp(Q):                                          # iterative (long staircases never hit the recursion limit)
        keep = [False] * len(Q)
        keep[0] = keep[-1] = True
        st = [(0, len(Q) - 1)]
        while st:
            i0, i1 = st.pop()
            if i1 - i0 < 2:
                continue
            (ax, ay), (bx, by) = Q[i0], Q[i1]
            L = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5 or 1e-9
            dm, im = -1.0, i0
            for i in range(i0 + 1, i1):
                d = abs((bx - ax) * (ay - Q[i][1]) - (ax - Q[i][0]) * (by - ay)) / L
                if d > dm:
                    dm, im = d, i
            if dm > tol:
                keep[im] = True
                st += [(i0, im), (im, i1)]
        return [q for q, k_ in zip(Q, keep) if k_]
    a = dp(P[:i_far + 1])
    b = dp(P[i_far:] + [P[0]])
    return a[:-1] + b[:-1]


def _sil_chaikin(P, n=2):
    for _ in range(n):
        Q = []
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        P = Q
    return P


def _sil_outline(rows, W, x0, y0, px, close_px, min_px=6):
    """closed, hole-filled, traced and smoothed outlines (m) of a bitmap"""
    if close_px > 0:
        rows = _sil_erode(_sil_dilate(rows, W, close_px), W, close_px)
    rows = _sil_fill_holes(rows, W)
    out = []
    for L in _sil_trace(rows, W):
        if abs(_sil_area(L)) < min_px:
            continue
        P = _sil_chaikin(_sil_dp([(float(a), float(b)) for a, b in L], 0.6), 2)
        out.append([(x0 + a * px, y0 + b * px) for a, b in P])
    return out


def sil_body(rings_m, px_m=0.01, close_m=0.05, key=None):
    """the solid outline(s) of a drawing made of closed rings (m, y up): rasterised at px_m, closed by close_m
    (gaps between pen strokes up to about 2 x close_m fill), inner holes filled, outer edge traced and smoothed.
    Returns [ring (m)]; [] for nothing. key: memo for the run."""
    if key is not None and key in _SIL_BODY:
        return _SIL_BODY[key]
    pts = [p for r in rings_m for p in r]
    if not pts:
        return []
    cp = max(0, int(round(close_m / px_m)))
    pad = (cp + 3) * px_m
    x0, y0 = min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad
    W = int((max(p[0] for p in pts) + pad - x0) / px_m) + 1
    H = int((max(p[1] for p in pts) + pad - y0) / px_m) + 1
    rows = [0] * H
    for r in rings_m:
        _sil_fill_ring(rows, r, x0, y0, px_m, W)
    out = _sil_outline(rows, W, x0, y0, px_m, cp)
    if key is not None:
        _SIL_BODY[key] = out
    return out


def sil_alpha_body(path, h_m, px_m=0.01, close_m=0.02, thr=128):
    """([ring m], w_m): the solid outline of a cutout PNG from its alpha (alpha > thr), scaled so the image is h_m
    tall, feet = the bottom row at y 0, x centred. ([], 0) if unreadable or with no alpha."""
    key = ("alpha", path, round(h_m, 3), px_m, close_m, thr)
    if key in _SIL_BODY:
        return _SIL_BODY[key]
    r = sil_png_read(path)
    if not r or r[4] is None:
        SIL_LOG.append(u"silhouette: %s has no alpha" % _sil_os.path.basename(path))
        _SIL_BODY[key] = ([], 0.0)
        return _SIL_BODY[key]
    w, h, _rgb, _nc, al = r
    m_px = h_m / float(h)                                    # m per image pixel
    step = max(1, int(px_m / m_px))
    W, H = (w + step - 1) // step + 6, (h + step - 1) // step + 6
    rows = [0] * H
    for yy in range(0, h, step):
        ln = al[yy * w:(yy + 1) * w:step]
        v = 0
        for i, a in enumerate(ln):
            if a > thr:
                v |= 1 << (i + 3)
        rows[(h - 1 - yy) // step + 3] = v                   # image top row -> highest bitmap row
    px = m_px * step
    cp = max(0, int(round(close_m / px)))
    out = _sil_outline(rows, W, -(w * m_px) / 2.0 - 3 * px, -3 * px, px, cp)
    if out:                                                  # feet exactly on y 0
        y_min = min(p[1] for R in out for p in R)
        out = [[(a, b - y_min) for a, b in R] for R in out]
    _SIL_BODY[key] = (out, w * m_px)
    return _SIL_BODY[key]


# ---- the cutout library (Data/cutouts/cutouts.json; recovered from a936d62:src/common/figures.py:747-792, round 5) --------
# {"cutouts": {key: entry or [entries]}}, entry = {"file", "h_m" (true height of what the PNG shows, bottom edge =
# ground/feet), "kind", "facing" (-1 = looks left; default +1), "depth": {"1": file, "2": file}, ...}. Keys: plants =
# the plants.py species key ("olive"), people = "person_<pose>", "stall". Read once per run.
_SIL_CUT = {}


def sil_cut_dir():
    return _sil_os.path.join(_sil_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "cutouts")


def sil_cut_library():
    """{key: [entry, ...]} from cutouts.json (entries whose file exists), {} when the folder or file is missing"""
    import json as _j
    if "lib" in _SIL_CUT:
        return _SIL_CUT["lib"]
    lib = {}
    p = _sil_os.path.join(sil_cut_dir(), "cutouts.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            js = _j.load(fh)
        js = js.get("cutouts", js) if isinstance(js, dict) else {}
        for k_, v in js.items():
            vs = v if isinstance(v, list) else [v]
            ok = [e for e in vs if isinstance(e, dict) and e.get("file") and e.get("h_m") and
                  _sil_os.path.isfile(_sil_os.path.join(sil_cut_dir(), e["file"]))]
            if ok:
                lib[k_] = ok
        SIL_LOG.append(u"cutouts: %d keys from %s" % (len(lib), p))
    except Exception as ex:
        SIL_LOG.append(u"FLAG cutouts: %s not read (%s)" % (p, type(ex).__name__))
    _SIL_CUT["lib"] = lib
    return lib


# ---- toning (plants) ----------------------------------------------------------------------------------------------------
def _sil_hex(c):
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def sil_tone(src, dst, shade, mid, light, keep=0.25, paper="F1EDDF", fade=0.0):
    """writes dst: the PNG src toned to a species' colours. Each pixel's luminance (stretched between the 2nd and
    98th percentile of the opaque pixels) maps onto the ramp shade -> mid -> light; keep (0-1) of the photo's own
    colour is mixed back (flowers stay visible); then everything is mixed toward the paper by fade (depth). Alpha
    unchanged. With numpy: as above; without: the ramp from the green channel only (keep ignored).
    Returns (True, "numpy"|"lut") or (False, why)."""
    r = sil_png_read(src)
    if not r:
        return False, "unreadable PNG"
    w, h, rgb, nc, al = r
    S, M_, L_, P = _sil_hex(shade), _sil_hex(mid), _sil_hex(light), _sil_hex(paper)
    try:
        import numpy as _np
    except Exception:
        _np = None
    if _np is not None:
        a = _np.frombuffer(rgb, dtype=_np.uint8).reshape(-1, nc).astype(_np.float32)
        if nc == 1:
            a = _np.repeat(a, 3, axis=1)
        lum = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
        op = lum if al is None else lum[_np.frombuffer(al, dtype=_np.uint8) > 128]
        if op.size < 10:
            op = lum
        lo, hi = _np.percentile(op, 2), _np.percentile(op, 98)
        t = _np.clip((lum - lo) / max(1.0, hi - lo), 0.0, 1.0)[:, None]
        S_, M2, L2 = (_np.array(c, dtype=_np.float32)[None, :] for c in (S, M_, L_))
        duo = _np.where(t < 0.5, S_ + (M2 - S_) * (t / 0.5), M2 + (L2 - M2) * ((t - 0.5) / 0.5))
        out = duo * (1.0 - keep) + a * keep
        out = out + (_np.array(P, dtype=_np.float32)[None, :] - out) * fade
        sil_png_write(dst, w, h, _np.clip(out + 0.5, 0, 255).astype(_np.uint8).tobytes(), al)
        return True, "numpy"
    g = rgb[1::3] if nc == 3 else rgb
    gs = sorted(g[::97]) or [0, 255]
    lo, hi = gs[int(0.02 * (len(gs) - 1))], gs[int(0.98 * (len(gs) - 1))]
    lut = [bytearray(256) for _ in range(3)]
    for v in range(256):
        t = min(1.0, max(0.0, (v - lo) / float(max(1, hi - lo))))
        for c in range(3):
            x = S[c] + (M_[c] - S[c]) * t / 0.5 if t < 0.5 else M_[c] + (L_[c] - M_[c]) * (t - 0.5) / 0.5
            x = x + (P[c] - x) * fade
            lut[c][v] = int(max(0, min(255, round(x))))
    out = bytearray(w * h * 3)
    for c in range(3):
        out[c::3] = bytes(g).translate(bytes(lut[c]))
    sil_png_write(dst, w, h, bytes(out), al)
    return True, "lut"
