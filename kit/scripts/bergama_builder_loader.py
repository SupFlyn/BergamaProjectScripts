# -*- coding: utf-8 -*-
"""Bergama Group 6: BOARD BUILDER LOADER (11 Nov 2026; Aras 18:41 UTC: "store that code on the cloud ... so i dont
update it ever"). Paste this file ONCE into the board builder component (Rhino 8 > Grasshopper > Python 3 Script), in
place of the builder code. It is never updated. On every press of the Button it takes the newest board builder
(kit/scripts/bergama_build_gh_chain_v<N>.py on GitHub main, saved to Downloads/Bergama/scripts/) and runs it inside
this component, so a new builder version reaches the board by itself. Offline: the newest builder already on this PC
runs. Inputs: run (Button), run_after and force (toggles, the builder adds them itself). Outputs: log, done.
"""
import os, re, json, hashlib, urllib.request
import scriptcontext as _ld_sc

_LD_NAME = "BuilderLoader v1"
_LD_REPO, _LD_BRANCH, _LD_FOLDER = "SupFlyn/BergamaProjectScripts", "main", "kit/scripts"
_LD_PREFIX = "bergama_build_gh_chain"
_LD_BASE = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
_LD_SCRIPTS = os.path.join(_LD_BASE, "scripts")
_LD_SETTINGS = os.path.join(_LD_BASE, "Data", "shared_settings.txt")      # token= line used if present (repo is public)


def _ld_token():
    try:
        for ln in open(_LD_SETTINGS, encoding="utf-8"):
            k, _, v = ln.partition("=")
            if k.strip().lower() == "token" and v.strip():
                return v.strip()
    except Exception:
        pass
    return None


def _ld_get(url, token):
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "bergama-board-builder"}
    if token:
        hdr["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60) as r:
        return r.read()


def _ld_key(name):
    """(major, minor) of a builder file name, None for any other file"""
    m = re.match(re.escape(_LD_PREFIX) + r"_v(\d+)(?:_(\d+))?\.py$", name or "")
    return (int(m.group(1)), int(m.group(2) or 0)) if m else None


def _ld_local():
    """the newest builder file on this PC, None when there is none"""
    try:
        names = [n for n in os.listdir(_LD_SCRIPTS) if _ld_key(n)]
    except OSError:
        return None
    return os.path.join(_LD_SCRIPTS, max(names, key=_ld_key)) if names else None


def _ld_fetch():
    """the newest builder on GitHub main -> Downloads/Bergama/scripts/ (only when it differs); returns a log line"""
    token = _ld_token()
    try:                                  # pinned to the branch's newest commit (a branch link can serve old copies)
        sha = json.loads(_ld_get("https://api.github.com/repos/%s/commits/%s" % (_LD_REPO, _LD_BRANCH),
                                 token).decode("utf-8"))["sha"]
        lst = json.loads(_ld_get("https://api.github.com/repos/%s/contents/%s?ref=%s" % (_LD_REPO, _LD_FOLDER, sha),
                                 token).decode("utf-8"))
        cands = [f for f in lst if f.get("type") == "file" and _ld_key(f.get("name"))]
        if not cands:
            return "FLAG loader: no %s_v*.py in the cloud: the builder on this PC runs" % _LD_PREFIX
        f = max(cands, key=lambda x: _ld_key(x["name"]))
        dst = os.path.join(_LD_SCRIPTS, f["name"])
        if os.path.isfile(dst):
            with open(dst, "rb") as fh:
                b = fh.read()
            if hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest() == f["sha"]:
                return "loader: %s is the newest builder (already on this PC)" % f["name"]
        data = _ld_get("https://raw.githubusercontent.com/%s/%s/%s/%s" % (_LD_REPO, sha, _LD_FOLDER, f["name"]), token)
        os.makedirs(_LD_SCRIPTS, exist_ok=True)
        with open(dst + ".part", "wb") as fh:
            fh.write(data)
        os.replace(dst + ".part", dst)
        return "loader: downloaded the newest builder %s" % f["name"]
    except Exception as e:
        return "FLAG loader: no download (offline or GitHub refused: %s): the builder on this PC runs" % e


# ---- every solve: on a new press fetch first, then run the newest builder here (it handles the press itself)
_ld_press = bool(run) if "run" in globals() else False                    # noqa: F821 (Grasshopper input)
_ld_prev = _ld_sc.sticky.get("bergama_builder_loader_prev", False)
_ld_sc.sticky["bergama_builder_loader_prev"] = _ld_press
if _ld_press and not _ld_prev:
    _ld_sc.sticky["bergama_builder_loader_note"] = _ld_fetch()
_ld_note = _ld_sc.sticky.get("bergama_builder_loader_note")
_ld_path = _ld_local()
if _ld_path is None:
    log = ((_ld_note + "\n") if _ld_note else "") + "no board builder on this PC yet: press the Button (needs internet once)"
    done = "idle"
    ghenv.Component.Message = _LD_NAME + " · press the Button"           # noqa: F821 (Grasshopper)
    print(log)
else:
    try:
        _ld_st = os.stat(_ld_path)
        _ld_k = [_ld_path, _ld_st.st_size, _ld_st.st_mtime_ns]
        _ld_c = _ld_sc.sticky.get("bergama_builder_loader_code")
        if not _ld_c or _ld_c[0] != _ld_k:                                 # read + compiled only when the file changed
            with open(_ld_path, encoding="utf-8") as _ld_f:
                _ld_c = (_ld_k, compile(_ld_f.read(), _ld_path, "exec"))
            _ld_sc.sticky["bergama_builder_loader_code"] = _ld_c
        exec(_ld_c[1], globals())                                          # sets log + done, like the pasted builder
        if _ld_note and isinstance(globals().get("log"), str):
            log = _ld_note + "\n" + log                                    # noqa: F821 (set by the builder)
    except Exception as _ld_e:
        import traceback as _ld_tb
        log = "ERROR loader: the builder %s did not run: %s\n%s" % (os.path.basename(_ld_path), _ld_e,
                                                                    _ld_tb.format_exc())
        done = "ERROR"
        ghenv.Component.Message = "ERROR"                                  # noqa: F821 (Grasshopper)
        print(log)
