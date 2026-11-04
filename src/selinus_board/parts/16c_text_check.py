# ============================================================ v59 (round 4, G-R4-1) -> v60 (round 5): KEEP AREAS ONLY
# v60 (round 5, G-R5-12; Aras 22:46 "change approach"): the board's own text-collision check (sb_text_check,
# SbTextCollisions) is gone: every text leaves as an anchored item and the booklet sets and checks it (warnings, never
# stops). What stays: the drawing areas no other text may cover (sb_keep), exported as each drawing's keep areas
# (16d_items.py).
# v59 (round 4 closing, G-R4-1 keeps): the drawing areas no text may cover, registered while the pages draw (sb_keep):
# key maps, legends, section pictures, the stream at each cut, zoom insets, photos and map frames. Each holds the
# texts its own drawing set (its names, tags, numbers: items i0..i1 of the board) as allowed on it, so a place name on
# its map passes and a column text, caption or other block running over the drawing raises like text-text.
SB_KEEPS = []                                         # dict(lst, geom, kind, name, i0, i1, line); reset per layout


def sb_mark(B):
    """v59 (closing, G-R4-1): the index the next item of board B gets (the i0 of sb_keep); None on a dry run"""
    it = getattr(B, "items", None)
    return len(it) if isinstance(it, list) else None


def sb_keep(B, geom, name, kind="keep", i0=None, line=None):
    """v59 (closing, G-R4-1): one drawing area of board B no text may cover, for the page check: geom = a box (x0,
    y0, x1, y1) or a closed area [(x, y) ...] in board units (line=True: an open line). The texts B drew from item
    i0 (sb_mark taken before the drawing) up to this call are the drawing's own and may sit on it; i0 None = no text
    may (the stream at a cut). A dry run (no board items) registers nothing. Returns the keep's name."""
    it = getattr(B, "items", None)
    if not isinstance(it, list) or not geom:
        return None
    n = len(it)
    nm = u"%s#%d" % (name, len(SB_KEEPS))
    SB_KEEPS.append(dict(lst=it, geom=list(geom), kind=kind, name=nm, i0=n if i0 is None else int(i0), i1=n,
                         line=line))
    return nm


def _sb_keep_box(K):
    g = K["geom"]
    if len(g) == 4 and not hasattr(g[0], "__len__"):
        return tuple(g)
    return (min(p[0] for p in g), min(p[1] for p in g), max(p[0] for p in g), max(p[1] for p in g))
