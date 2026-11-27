import numpy as np
from scipy.cluster.vq import kmeans2


def srgb(a):
    return np.asarray(a, float) / 255.0


def face_rgb(img, UV, F, flip_v=True):
    """mean texture colour of each triangle: its middle and three inner points"""
    im = np.asarray(img.convert("RGB"), float)
    h, w = im.shape[:2]
    out = np.zeros((len(F), 3))
    for wts in ((1 / 3, 1 / 3, 1 / 3), (0.6, 0.2, 0.2), (0.2, 0.6, 0.2), (0.2, 0.2, 0.6)):
        uv = UV[F[:, 0]] * wts[0] + UV[F[:, 1]] * wts[1] + UV[F[:, 2]] * wts[2]
        u = np.mod(uv[:, 0], 1.0)
        v = np.mod(uv[:, 1], 1.0)
        if flip_v:
            v = 1.0 - v
        x = np.clip((u * w).astype(int), 0, w - 1)
        y = np.clip((v * h).astype(int), 0, h - 1)
        out += im[y, x]
    return out / 4.0 / 255.0


def areas(V, F):
    return 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)


def palette(C, A, k, seed=1, merge=0.06):
    """k-means of face colours C weighted by area A -> (labels, colours); clusters closer than merge are one"""
    k = min(k, len(C))
    rng = np.random.default_rng(seed)
    p = A / A.sum()
    n = min(20000, max(len(C), 2000))                    # half by area, half by count: small parts keep their colour
    samp = np.vstack([C[rng.choice(len(C), size=n // 2, p=p)], C[rng.choice(len(C), size=n // 2)]])
    cen, _l = kmeans2(samp, k, minit="++", seed=seed)
    lab = np.argmin(((C[:, None, :] - cen[None, :, :]) ** 2).sum(2), axis=1)
    cols = []
    for j in range(k):
        m = lab == j
        cols.append((C[m] * A[m, None]).sum(0) / A[m].sum() if m.any() and A[m].sum() > 0 else cen[j])
    cols = np.array(cols)
    par = list(range(k))
    for i in range(k):
        for j in range(i):
            if np.linalg.norm(cols[i] - cols[par[j]]) < merge and par[i] == i:
                par[i] = par[j]
    lab = np.array([par[x] for x in lab])
    return lab, cols
