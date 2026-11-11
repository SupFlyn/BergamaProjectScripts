# -*- coding: utf-8 -*-
"""Bergama Group 6: BOARD BUILDER = build_gh_chain v5.2 (12 Nov 2026; v5.2: a download that times out or breaks is tried 4 times (waits 2, 4, 8 s, 300 s read limit, 4 at a time); a file that still fails is a FLAG line and the old local copy is used, the press goes on; v5.1 round 9 closing: after a run_after + force press, a chain script whose own log was not written during the press (the chain stopped before it) is logged "not run" and not recorded, so the next run_after runs it (v5 counted it as ran and a later run_after skipped it); v5 round 9 G9-7: the round 8 S5 v3.5 functions restored (chain_secs = each chained script's time from its own log, fail_reason = the first ERROR line of its log on every FAILED line, a recorded 0 s counts as unknown, processor times under 0.5 s use the fallback), and the log's second line says whether Bergama_Altlik.3dm is the open Rhino model; v4: typed inputs from each script's GH_INPUTS (File Path, Line, Curve, Point, Number boxes, sliders over the script's own range, type hints, list access), inputs a script no longer has are taken off with their boxes, input boxes in a stair layout, Aras 17:30-17:37 UTC; v3.4 8 Nov: v3.4: the run_after pass is driven from Rhino idle, one script per step, and run_after + force presses the Chain Button so the whole chain runs, Aras 19:32 UTC; v3.3: everything from the cloud only). Rules: scripts/_template/SCRIPT_STANDARD.md.

Aras 8 Nov 2026 14:54-15:04 UTC. One press of the Button:
  1 DOWNLOAD from GitHub (SupFlyn/BergamaProjectScripts, branch main, folder kit/), one way only: first the checklist
    kit/scripts/needed_files.txt (every file the scripts need, Aras 15:13 UTC), then exactly the files on it:
      kit/scripts/<file>    -> Downloads/Bergama/scripts/<file>   (newest scripts + board_order.txt)
      kit/Data/<path>       -> Downloads/Bergama/Data/<path>      (Data files, assets, photos ...)
    only files that differ are downloaded; nothing is uploaded; local files not on the checklist are never touched;
    a checklist line missing in the cloud or on this PC is a FLAG line in the log
  2 READ every script named in board_order.txt (and any other script in kit/scripts/): its inputs, optional ones
    included, and their defaults are read from the script's own code (nothing about any script is written here)
  3 BUILD on THIS canvas (the Grasshopper file open now; nothing is saved):
      left column  every script on its own: own Button, every input wired to a widget at its default
      chain        the 'chain:' scripts in board_order.txt order, stair layout, one Button on the first, each 'done'
                   wired into the next 'run'; every input wired to a widget at its default too
    a component that is already there (found by its name) keeps its place: only its code is replaced
    widgets: a value you set is never reset; a widget still at the old default moves to a new default; an input
    that changed kind (number -> True/False ...) gets a new widget; a new input gets a widget at its default
    v4: a script with GH_INPUTS = {"name": "<type>[ list][ <min>..<max>][ = <default>]"} (types text, file, number,
    int, bool, line, curve, point) gets exactly those inputs, each with its type hint, access and a box of its type
    (text panel, File Path, Line, Curve, Point, Number / Integer box, slider over <min>..<max>, toggle); its other
    inputs are taken off together with the builder's boxes on them; a typed box holding your data is never swapped.
    Boxes sit in a stair beside their component (4 steps of 60 to the left, then back); boxes you moved stay put.
    a script taken out of board_order.txt: its component is unwired and renamed "REMOVED <name>", never deleted
Adding, removing or reordering scripts only changes the files in kit/: this builder never needs a new version for it.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run        Button: nothing happens until it is pressed
  input  force      Boolean Toggle, off by default: run_after AND force both on = every script run from the beginning:
                    the Chain Button is pressed (the whole chain runs through its done -> run wires), then every
                    left-column-only script. Both toggles are added by the builder itself on
                    the first press (Aras 15:25 UTC)
  input  run_after  Boolean Toggle, off by default: True = right after the update the builder runs, one at a time in
                    chain order, the left-column copies (their widgets) of only the scripts whose code, widgets or read files (kit/scripts/script_reads.txt)
                    changed since their last good run; its log lists every script as ran / skipped with the reason
                    and the check time (Aras 15:16-15:44 UTC); record in cached/bergama_build_gh_chain/runs.json
  output log   the last run's report
  output done  "done HH:MM:SS.ss · N s" after a good run
board_order.txt: one line per script, "chain: <file prefix> = <name>" (in chain order) or "solo: <file prefix> = <name>"
(left column only); "= <name>" is optional (else the script's GH_LABEL); "#" starts a comment.
"""
import os, re, ast, json, time, hashlib, urllib.request, urllib.parse, urllib.error

# ---- SETTINGS ----
VERSION = "v5.2"
GH_LABEL = "BoardBuilder"
REPO = "SupFlyn/BergamaProjectScripts"
BRANCH = "main"
KIT = "kit"
BASE = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
SCRIPTS_DIR = os.path.join(BASE, "scripts")
DATA_DIR = os.path.join(BASE, "Data")
CACHE_DIR = os.path.join(BASE, "cached", "bergama_build_gh_chain")
LOG_DIR = os.path.join(BASE, "logs")
LOG_NAME = "bergama_build_gh_chain_log.txt"
STATE = os.path.join(CACHE_DIR, "state.json")
ORDER_FILE = "board_order.txt"
NEEDED_FILE = "needed_files.txt"                  # the cloud checklist of every file the scripts need
SELF_PREFIX = "bergama_build_gh_chain"
SETTINGS_FILE = os.path.join(DATA_DIR, "shared_settings.txt")      # token= line used if present (repo is public)
# layout (canvas units, measured from this builder component)
SOLO_DX, CHAIN_DX = 420.0, 1500.0      # left column x / chain start x, right of the builder
TOP_DY = 160.0                         # first row below the builder
GAP_Y = 80.0                           # between solo components
STEP_X, STEP_Y = 800.0, 80.0           # chain stair step
WIDGET_DX = 300.0                      # widgets sit this far left of their component (where boxes are first made)
STAIR_N, STAIR_DX, STAIR_GAP = 4, 60.0, 30.0   # v4 input boxes: 4 steps of 60 to the left, 30 clear of the component
LOG_DX, LOG_W, LOG_H = 40.0, 240.0, 110.0


# ---------------------------------------------------------------- 1 download
def gh_token():
    try:
        for ln in open(SETTINGS_FILE, encoding="utf-8"):
            k, _, v = ln.partition("=")
            if k.strip().lower() == "token" and v.strip():
                return v.strip()
    except Exception:
        pass
    return None


def http(url, accept, token):
    hdr = {"Accept": accept, "User-Agent": "bergama-board-builder"}
    if token:
        hdr["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=300) as r:
        return r.read()


SHA_FILE = os.path.join(CACHE_DIR, "file_sha.json")
_SHA = {}                                         # {path: [size, mtime_ns, git sha]}: files re-read only when changed


def blob_sha(path):
    st = os.stat(path)
    c = _SHA.get(path)
    if c and c[0] == st.st_size and c[1] == st.st_mtime_ns:
        return c[2]
    h = _blob_sha(path)
    _SHA[path] = [st.st_size, st.st_mtime_ns, h]
    return h


def _blob_sha(path):
    with open(path, "rb") as f:
        b = f.read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def local_path(rel):
    """kit/scripts/x -> scripts/x, kit/Data/a/b -> Data/a/b, None for anything else"""
    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == KIT and parts[1] == "scripts" and len(parts) == 3:
        return os.path.join(SCRIPTS_DIR, parts[2])
    if len(parts) >= 3 and parts[0] == KIT and parts[1] == "Data":
        return os.path.join(DATA_DIR, *parts[2:])
    return None


_COMMIT = [BRANCH]


def fetch(it, dst, token):
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, _COMMIT[0], "/".join(
        urllib.parse.quote(p) for p in it["path"].split("/")))
    for n in range(4):                    # v5.2: a slow or broken download is tried again
        try:
            data = http(url, "*/*", token)
            break
        except Exception as e:
            if n == 3:
                return "%s (%s)" % (it["path"], e)
            time.sleep(2 ** (n + 1))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)
    return None


def download(log):
    """the cloud checklist kit/scripts/needed_files.txt first, then exactly the files on it"""
    token = gh_token()
    try:                                  # pinned to the branch's newest commit (a branch link can serve old copies)
        _COMMIT[0] = json.loads(http("https://api.github.com/repos/%s/commits/%s" % (REPO, BRANCH),
                                     "application/vnd.github+json", token).decode("utf-8"))["sha"]
        tree = json.loads(http("https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (REPO, _COMMIT[0]),
                               "application/vnd.github+json", token).decode("utf-8"))
    except Exception as e:
        log.append("FLAG no download (offline or GitHub refused: %s): the local files are used as they are" % e)
        return None
    cloud = {it["path"][len(KIT) + 1:]: it for it in tree.get("tree", [])
             if it.get("type") == "blob" and it["path"].startswith(KIT + "/") and local_path(it["path"])}
    lst = cloud.get("scripts/" + NEEDED_FILE)
    if lst is None:
        log.append("FLAG no %s in the cloud: nothing downloaded" % NEEDED_FILE)
        return None
    lp = local_path(lst["path"])
    if not (os.path.isfile(lp) and blob_sha(lp) == lst["sha"]):
        bad = fetch(lst, lp, token)
        if bad:
            log.append("FLAG download failed 4 times, the local copy is used: " + bad)
            if not os.path.isfile(lp):
                return None
    cc = cloud.get("scripts/" + CACHE_LIST)              # the speed-cache folder list: always taken, not a checklist line
    if cc is not None:
        cp = local_path(cc["path"])
        if not (os.path.isfile(cp) and blob_sha(cp) == cc["sha"]):
            bad = fetch(cc, cp, token)
            if bad:
                log.append("FLAG download failed 4 times, the local copy is used: " + bad)
    need = []
    for ln in open(lp, encoding="utf-8"):
        ln = ln.split("#", 1)[0].strip().replace("\\", "/")
        if ln:
            need.append(ln)
    got, same, missing, todo = 0, 0, [], {}
    for n in need:
        hits = [r for r in cloud if (r.startswith(n) if n.endswith("/") else r == n)]
        if not hits:
            missing.append(n)
        for r in hits:
            todo[r] = cloud[r]
    get = []
    for r in sorted(todo):
        it, dst = todo[r], local_path(todo[r]["path"])
        if os.path.isfile(dst) and blob_sha(dst) == it["sha"]:
            same += 1
        else:
            get.append((r, it, dst))
    if get:                                       # several at once (waiting on the network, not the PC)
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(4) as ex:
            res = list(ex.map(lambda x: fetch(x[1], x[2], token), get))
        for (r, it, dst), bad in zip(get, res):
            if bad:
                log.append("FLAG download failed 4 times, the local copy is used: " + bad)
            else:
                got += 1
                log.append("  downloaded " + r)
    for n in missing:
        log.append("FLAG on the checklist but not in the cloud: " + n)
    for n in need:
        if not n.endswith("/") and not os.path.isfile(os.path.join(BASE, *n.split("/"))):
            log.append("FLAG still missing on this PC: " + n)
    if tree.get("truncated"):
        log.append("FLAG GitHub cut the file list short: some files may be missing")
    log.append("download (checklist %s, %d lines): %d new or changed, %d already current"
               % (NEEDED_FILE, len(need), got, same))
    return [r.split("/", 1)[1] for r in todo if r.startswith("scripts/")]


# ---------------------------------------------------------------- 2 read the scripts
def newest(prefix):
    best = None
    for f in os.listdir(SCRIPTS_DIR):
        m = re.match(re.escape(prefix) + r"_v(\d+)(?:_(\d+))?\.py$", f)
        if m:
            k = (int(m.group(1)), int(m.group(2) or 0))
            if best is None or k > best[0]:
                best = (k, f)
    return best[1] if best else None


def prefix_of(fname):
    m = re.match(r"(.+?)_v\d+(?:_\d+)?\.py$", fname)
    return m.group(1) if m else None


def read_order(cloud_scripts):
    """[(prefix, 'chain'|'solo', label)] from board_order.txt + any other script in kit/scripts/ as solo"""
    out, seen = [], set()
    p = os.path.join(SCRIPTS_DIR, ORDER_FILE)
    if os.path.isfile(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.split("#", 1)[0].strip()
            k, _, v = ln.partition(":")
            v, _, lab = v.partition("=")
            k, v, lab = k.strip().lower(), v.strip(), lab.strip()
            if k in ("chain", "solo") and v and v not in seen and v != SELF_PREFIX:
                out.append((v, k, lab))
                seen.add(v)
    for f in sorted(cloud_scripts or []):
        pf = prefix_of(f)
        if pf and pf not in seen and pf != SELF_PREFIX:
            out.append((pf, "solo", ""))
            seen.add(pf)
    return out


INPUT_CALLS = ("inp", "inp_num", "inp_bool", "inp_int", "inp_str", "inp_list", "trig_get")
NO_VALUE = object()


def module_consts(tree):
    c = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                c[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                if (isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id in
                        ("set", "tuple", "list", "frozenset") and n.value.args):
                    try:
                        c[n.targets[0].id] = list(ast.literal_eval(n.value.args[0]))
                    except Exception:
                        pass
    return c


def value_of(node, consts):
    try:
        return ast.literal_eval(node)
    except Exception:
        pass
    if isinstance(node, ast.Name) and node.id in consts:
        return consts[node.id]
    return NO_VALUE


def kind_of(v):
    if isinstance(v, bool):
        return "toggle"
    if isinstance(v, (int, float)):
        return "slider"
    return "panel"


# v4 (Aras 11 Nov 2026 17:30-17:37 UTC: inputs had the wrong types): a script may list its inputs in
# GH_INPUTS = {"name": "<type>[ list][ <min>..<max>][ = <default>]"}, types: text, file, number, int, bool, line, curve,
# point. Then the component has exactly these inputs (others are taken off with their boxes), each with its type hint
# and access, and each wired to the box of its type: text panel, File Path, Line, Curve, Point, Number / Integer
# (no default) or a slider over <min>..<max> (with a default), a toggle for bool.
HINT_OF = {"text": "str", "file": "str", "number": "float", "int": "int", "bool": "bool", "line": "Line",
           "curve": "Curve", "point": "Point3d"}
BOX_OF = {"text": "panel", "file": "file", "line": "line", "curve": "curve", "point": "point"}
TYPED_BOXES = ("number", "integer", "file", "line", "curve", "point")


def parse_spec(txt):
    """'number list 0..1 = 0.5' -> {type, list, range, default}; None when it can't be read"""
    m = re.match(r"\s*(\w+)(\s+list)?(?:\s+(-?[\d.]+)\s*\.\.\s*(-?[\d.]+))?(?:\s*=\s*(.*?))?\s*$", str(txt))
    if not m or m.group(1).lower() not in HINT_OF:
        return None
    d = NO_VALUE
    if m.group(5) is not None:
        try:
            d = ast.literal_eval(m.group(5))
        except Exception:
            d = m.group(5)
    rng = (float(m.group(3)), float(m.group(4))) if m.group(3) is not None else None
    return {"type": m.group(1).lower(), "list": bool(m.group(2)), "range": rng, "default": d}


def parse_script(path):
    """{'label', 'version', 'inputs': [(name, kind, default)], 'outputs': [...]}"""
    src = open(path, encoding="utf-8-sig").read()
    ins, outs, seen = [], [], set()

    def add(name, kind, default):
        if name and name.lower() not in seen and name.lower() != "run":
            seen.add(name.lower())
            ins.append([name, kind, default])

    tree = None
    try:
        tree = ast.parse(src)
    except Exception:
        pass
    consts = module_consts(tree) if tree else {}
    doc = (ast.get_docstring(tree) if tree else None) or src[:6000]
    for ln in doc.splitlines():                                 # "  input  name   description"
        m = re.match(r"\s*input\s{2,}(\w+)\s*(.*)$", ln)
        if m:
            d = m.group(2).lower()
            if "toggle" in d or "true/false" in d or "boolean" in d:
                add(m.group(1), "toggle", "on by default" in d or "default true" in d)
            else:
                add(m.group(1), None, NO_VALUE)
        m = re.match(r"\s*output\s{2,}(\w+)", ln)
        if m and m.group(1) not in outs:
            outs.append(m.group(1))
    calls = {}
    if tree:
        for n in ast.walk(tree):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in INPUT_CALLS and n.args
                    and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)):
                v = value_of(n.args[1], consts) if len(n.args) > 1 else None
                key = (n.lineno, n.col_offset)
                calls[key] = (n.args[0].value, v)
        for _, (name, v) in sorted(calls.items()):
            known = next((i for i in ins if i[0].lower() == name.lower()), None)
            if known and known[2] is NO_VALUE and v is not NO_VALUE:
                known[1], known[2] = None, v
            elif not known:
                add(name, None, v)
    else:
        for m in re.finditer(r"\b(?:%s)\(\s*[\"'](\w+)[\"']" % "|".join(INPUT_CALLS), src):
            add(m.group(1), None, NO_VALUE)
    for lst in ("SETTINGS", "KNOWN_INPUTS"):                    # names the script lists as its own inputs
        for name in consts.get(lst) or []:
            if isinstance(name, str):
                add(name, None, NO_VALUE)
    inputs, spec = [], {}
    decl = consts.get("GH_INPUTS")
    if isinstance(decl, dict) and decl:                         # v4: the script lists its inputs with their types
        found = dict((i[0].lower(), i) for i in ins)
        for name, txt in decl.items():
            sp = parse_spec(txt)
            if sp is None or str(name).lower() == "run":
                continue
            old = found.get(str(name).lower())
            v = sp["default"] if sp["default"] is not NO_VALUE else (old[2] if old else NO_VALUE)
            v = None if v is NO_VALUE else v
            if sp["type"] == "bool":
                kind, v = "toggle", bool(v)
            elif sp["type"] in ("number", "int"):
                kind = "slider" if isinstance(v, (int, float)) and not isinstance(v, bool) else \
                    ("number" if sp["type"] == "number" else "integer")
            else:
                kind = BOX_OF[sp["type"]]
            inputs.append((str(name), kind, v))
            spec[str(name)] = {"hint": HINT_OF[sp["type"]], "list": sp["list"], "range": sp["range"],
                               "int": sp["type"] == "int"}
    else:
        for name, kind, v in ins:
            v = None if v is NO_VALUE else v
            inputs.append((name, kind or kind_of(v), v))
    for o in ("log", "done"):
        if o not in outs:
            outs.append(o)
    label = consts.get("GH_LABEL") if isinstance(consts.get("GH_LABEL"), str) else None
    return {"label": label, "version": consts.get("VERSION", ""), "inputs": inputs, "outputs": outs, "code": src,
            "spec": spec, "declared": bool(spec)}


# ---------------------------------------------------------------- 3 the canvas
import System
import Grasshopper as GH
from Grasshopper.Kernel import GH_ParameterSide, GH_ParamAccess
from Grasshopper.Kernel.Special import GH_NumberSlider, GH_BooleanToggle, GH_Panel, GH_ButtonObject
PT = System.Drawing.PointF


def py3_proxy():
    for p in GH.Instances.ComponentServer.ObjectProxies:
        if p.Desc.Name == "Python 3 Script" and not p.Obsolete:
            return p
    raise Exception("Python 3 Script component not found (is this Rhino 8?)")


def set_source(comp, code):
    for m in ("SetSource", "TrySetSource"):
        f = getattr(comp, m, None)
        if f:
            try:
                f(code)
                return m
            except Exception:
                pass
    for a in ("Text", "Source", "Code", "Script"):
        if hasattr(comp, a):
            try:
                setattr(comp, a, code)
                return a
            except Exception:
                pass
    names = [n for n in dir(comp) if re.search("source|text|script|code", n, re.I)]
    raise Exception("could not set the script text; members: " + ", ".join(names))


def pname(p):
    for a in ("VariableName", "NickName", "Name"):
        v = getattr(p, a, None)
        if v:
            return str(v)
    return ""


def find_param(lst, name):
    for p in lst:
        if pname(p).lower() == name.lower() or str(p.NickName).lower() == name.lower():
            return p
    return None


def add_param(comp, side, name, kind=None):
    lst = comp.Params.Input if side == GH_ParameterSide.Input else comp.Params.Output
    i = lst.Count
    p = comp.CreateParameter(side, i)
    p.Name = name
    p.NickName = name
    if hasattr(p, "VariableName"):
        try:
            p.VariableName = name
        except Exception:
            pass
    if side == GH_ParameterSide.Input:
        p.Optional = True
        if kind == "list":
            p.Access = GH_ParamAccess.list
        comp.Params.RegisterInputParam(p, i)
    else:
        comp.Params.RegisterOutputParam(p, i)
    return p


def set_hint(p, hint):
    """v4: the input's type hint (Rhino 8 script parameters; older Grasshopper hint classes as a fallback).
    True when it took; False = the input keeps "No Type Hint" (every Bergama script reads its inputs either way)."""
    th = getattr(p, "TypeHints", None)
    if th is not None:
        f = getattr(th, "Select", None)
        if f is not None:
            for h in (hint, hint.lower()):
                try:
                    if f(h) is not False:
                        return True
                except Exception:
                    pass
    try:
        import Grasshopper.Kernel.Parameters.Hints as H
        cls = {"str": "GH_StringHint_CS", "float": "GH_DoubleHint_CS", "int": "GH_IntegerHint_CS",
               "bool": "GH_BooleanHint_CS", "Line": "GH_LineHint", "Curve": "GH_CurveHint",
               "Point3d": "GH_Point3dHint"}[hint]
        if hasattr(p, "TypeHint"):
            p.TypeHint = getattr(H, cls)()
            return True
    except Exception:
        pass
    return False


def relayout(obj):
    obj.Attributes.ExpireLayout()
    obj.Attributes.PerformLayout()


def place(doc, obj, x, y):
    obj.CreateAttributes()
    obj.Attributes.Pivot = PT(float(x), float(y))
    doc.AddObject(obj, False)
    relayout(obj)
    return obj


def decimals(v):
    s = repr(float(v))
    return 0 if float(v).is_integer() else min(3, len(s.split(".")[1]) if "." in s and "e" not in s else 2)


def slider_spec(v, rng=None, whole=False):
    """(min, max, decimals) of the slider for default v; rng = the script's own (min, max) (v4)"""
    if rng:
        lo, hi = rng
        if whole:
            return int(lo), int(hi), 0
        dec = max(decimals(lo), decimals(hi), decimals(v))
        if dec == 0 and hi - lo <= 10:
            dec = 2 if hi - lo <= 1 else 1                       # a short range in tenths / hundredths
        return lo, hi, dec
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e9:
        v = int(v)                                            # 1000.0 -> whole-number slider at 1000
    if isinstance(v, int):
        lo, hi = (min(0, 2 * v), max(2 * v, 10)) if v else (0, 10)
        return lo, hi, 0
    s = repr(v)
    dec = min(3, max(1, len(s.split(".")[1]) if "." in s and "e" not in s else 2))
    lo, hi = (min(0.0, 2 * v), max(2 * v, 1.0)) if v else (0.0, 1.0)
    return lo, hi, dec


def box_class(kind):
    from Grasshopper.Kernel import Parameters as GP
    return {"number": GP.Param_Number, "integer": GP.Param_Integer, "file": GP.Param_FilePath,
            "line": GP.Param_Line, "curve": GP.Param_Curve, "point": GP.Param_Point}[kind]


def carry(kind, old):
    """v4: what a swapped box keeps from the panel or slider before it (a number or path you typed), else None"""
    if old is None or (isinstance(old, str) and not old.strip()):
        return None
    try:
        if kind in ("slider", "number"):
            return float(str(old).strip().replace(",", "."))
        if kind == "integer":
            return int(round(float(str(old).strip().replace(",", "."))))
        if kind in ("file", "panel"):
            return str(old).strip().strip('"').strip("'")
    except Exception:
        pass
    return None


def make_widget(doc, name, kind, v, x, y, sp=None, keep=None):
    sp = sp or {}
    if kind == "toggle":
        w = GH_BooleanToggle()
        w.NickName = name
        w.Value = bool(v)
    elif kind == "slider":
        lo, hi, dec = slider_spec(v, sp.get("range"), sp.get("int"))
        val = float(v)
        if keep is not None:
            val = keep
            lo, hi = min(lo, keep), max(hi, keep)
        w = GH_NumberSlider()
        w.NickName = name
        w.Slider.Type = GH.GUI.Base.GH_SliderAccuracy.Float if dec else GH.GUI.Base.GH_SliderAccuracy.Integer
        w.Slider.DecimalPlaces = dec
        w.Slider.Minimum = System.Decimal(lo)
        w.Slider.Maximum = System.Decimal(hi)
        w.Slider.Value = System.Decimal(float(val))
    elif kind in TYPED_BOXES:                                     # v4: an empty box of the input's own type
        w = box_class(kind)()
        w.NickName = name
        if keep is not None:
            from Grasshopper.Kernel import Types as GT
            goo = {"number": lambda k: GT.GH_Number(float(k)), "integer": lambda k: GT.GH_Integer(int(k)),
                   "file": lambda k: GT.GH_String(str(k))}.get(kind)
            if goo is not None:
                w.PersistentData.Append(goo(keep))
    else:
        w = GH_Panel()
        txt = "" if v is None or isinstance(v, (list, tuple, dict, set)) else str(v)
        if keep is not None:
            txt = keep
        w.NickName = name if txt else name + " (optional)"
        w.UserText = txt
        try:
            w.Properties.Multiline = True                         # the whole text is ONE item
        except Exception:
            pass
    place(doc, w, x, y)
    if kind == "panel":
        w.Attributes.Bounds = System.Drawing.RectangleF(float(x), float(y), 200.0, 20.0)
    return w


def widget_kind(w, name=None):
    """the builder's box kinds; a typed box (Number, Line ...) counts only when it carries the input's name"""
    if isinstance(w, GH_BooleanToggle):
        return "toggle"
    if isinstance(w, GH_NumberSlider):
        return "slider"
    if isinstance(w, GH_Panel):
        return "panel"
    for k in TYPED_BOXES:
        try:
            if type(w) == box_class(k) and (name is None or str(w.NickName).lower() == name.lower()):
                return k
        except Exception:
            pass
    return None


def box_data(w):
    try:
        return [str(g) for g in w.PersistentData.AllData(True)]
    except Exception:
        return []


def widget_value(w):
    k = widget_kind(w)
    if k == "toggle":
        return bool(w.Value)
    if k == "slider":
        return float(System.Decimal.ToDouble(w.Slider.Value))
    if k == "panel":
        return str(w.UserText or "")
    if k in TYPED_BOXES:
        return "|".join(box_data(w))
    return None


def same_default(a, b, kind):
    if kind == "slider":
        try:
            return abs(float(a) - float(b)) < 1e-9
        except Exception:
            return False
    if kind == "panel":
        a = "" if a is None or isinstance(a, (list, tuple, dict)) else str(a)
        b = "" if b is None or isinstance(b, (list, tuple, dict)) else str(b)
    return a == b


def set_widget_value(w, kind, v):
    if kind == "toggle":
        w.Value = bool(v)
    elif kind == "slider":
        lo, hi, _ = slider_spec(v)
        if System.Decimal(lo) < w.Slider.Minimum:
            w.Slider.Minimum = System.Decimal(lo)
        if System.Decimal(hi) > w.Slider.Maximum:
            w.Slider.Maximum = System.Decimal(hi)
        w.Slider.Value = System.Decimal(float(v))
    elif kind == "panel":
        w.UserText = "" if v is None or isinstance(v, (list, tuple, dict)) else str(v)
    w.ExpireSolution(False)


def slider_range(w, v, sp):
    """v4: a kept slider takes the script's own range and decimals; its value stays (inside the range)"""
    lo, hi, dec = slider_spec(v, sp.get("range"), sp.get("int"))
    val = float(System.Decimal.ToDouble(w.Slider.Value))
    lo, hi = min(lo, val), max(hi, val)
    acc = GH.GUI.Base.GH_SliderAccuracy.Float if dec else GH.GUI.Base.GH_SliderAccuracy.Integer
    if (w.Slider.Type, int(w.Slider.DecimalPlaces), float(System.Decimal.ToDouble(w.Slider.Minimum)),
            float(System.Decimal.ToDouble(w.Slider.Maximum))) == (acc, dec, float(lo), float(hi)):
        return False
    w.Slider.Type = acc
    w.Slider.DecimalPlaces = dec
    w.Slider.Minimum = System.Decimal(lo)
    w.Slider.Maximum = System.Decimal(hi)
    w.Slider.Value = System.Decimal(val)
    w.ExpireSolution(False)
    return True


def input_y(comp, p):
    relayout(comp)
    return float(p.Attributes.Pivot.Y) - 10.0


def drop_input(doc, comp, p):
    """v4: an input the script no longer has: off the component, with the builder's box if nothing else uses it"""
    for w in list(p.Sources):
        p.RemoveSource(w)
        if widget_kind(w, pname(p)) and w.Recipients.Count == 0:
            doc.RemoveObject(w, False)
    comp.Params.UnregisterInputParameter(p, True)


def fit_inputs(doc, comp, info, old_defaults, counts, fresh, hints, hint_fail):
    """inputs + widgets of one component; returns {input: default} as now applied. fresh = boxes made this press
    (the stair places them); hints = {input: hint} already set on this component (updated here)"""
    applied = {}
    x = float(comp.Attributes.Pivot.X) - WIDGET_DX
    spec = info.get("spec") or {}
    if info.get("declared"):
        want = set(n.lower() for n, _, _ in info["inputs"]) | {"run"}
        for p in list(comp.Params.Input):
            if pname(p).lower() not in want:
                drop_input(doc, comp, p)
                counts["inputs removed (the script no longer has them)"] += 1
        comp.Params.OnParametersChanged()
    for name, kind, v in info["inputs"]:
        applied[name] = v
        sp = spec.get(name) or {}
        p = find_param(comp.Params.Input, name)
        new_p = p is None
        if new_p:
            p = add_param(comp, GH_ParameterSide.Input,
                          name, "list" if isinstance(v, (list, tuple)) or sp.get("list") else None)
            comp.Params.OnParametersChanged()
            counts["inputs added"] += 1
        if sp:
            acc = GH_ParamAccess.list if sp["list"] else GH_ParamAccess.item
            if p.Access != acc:
                p.Access = acc
                counts["inputs set to list / item access"] += 1
            if new_p or hints.get(name) != sp["hint"]:
                if set_hint(p, sp["hint"]):
                    hints[name] = sp["hint"]
                    counts["type hints set"] += 1
                else:
                    hints.pop(name, None)
                    hint_fail.append("%s.%s (%s)" % (comp.NickName, name, sp["hint"]))
        w = p.Sources[0] if p.SourceCount else None
        wk = widget_kind(w, name) if w is not None else None
        if w is None:
            nw = make_widget(doc, name, kind, v, x, input_y(comp, p), sp)
            p.AddSource(nw)
            fresh.add(nw.InstanceGuid)
            counts["widgets added"] += 1
        elif wk is None:
            continue                                              # wired to something else: yours, left alone
        elif wk != kind:
            if wk in TYPED_BOXES and box_data(w):
                counts["boxes kept (they hold your data)"] += 1
                continue
            pv = w.Attributes.Pivot
            keep = carry(kind, widget_value(w)) if wk in ("panel", "slider") else None
            p.RemoveSource(w)
            if w.Recipients.Count == 0:
                doc.RemoveObject(w, False)
            nw = make_widget(doc, name, kind, v, pv.X, pv.Y, sp, keep)
            p.AddSource(nw)
            fresh.add(nw.InstanceGuid)
            counts["widgets swapped (input changed kind)"] += 1
        elif name in old_defaults and not same_default(old_defaults[name], v, kind) \
                and same_default(widget_value(w), old_defaults[name], kind):
            set_widget_value(w, kind, v)                          # never touched by you: follows the new default
            counts["widgets moved to a new default"] += 1
        else:
            if kind == "slider" and sp.get("range") and slider_range(w, v, sp):
                counts["slider ranges set from the script"] += 1
            counts["widgets kept as you set them"] += 1
    for o in info["outputs"]:
        if find_param(comp.Params.Output, o) is None:
            add_param(comp, GH_ParameterSide.Output, o)
    comp.VariableParameterMaintenance()
    comp.Params.OnParametersChanged()
    return applied


def stair(comp, fresh, old_xy, counts):
    """v4 (Aras 11 Nov 17:33 UTC "stair like layout to save space"): every box of the builder beside the component,
    level with its own input, STAIR_N steps of STAIR_DX to the left and back, each box one row high; a box that
    would touch one already placed steps further left. Moved: boxes made this press, boxes still where the builder
    put them last time, and the builder's older boxes still at their first place. Boxes you moved stay.
    Returns {input: [left, top]} of the boxes it placed."""
    relayout(comp)
    right = float(comp.Attributes.Bounds.Left) - STAIR_GAP
    placed, out, row = [], {}, 0
    for p in comp.Params.Input:
        name = pname(p)
        if name.lower() == "run":
            continue
        row += 1
        if p.SourceCount != 1:
            continue
        w = p.Sources[0]
        if not widget_kind(w, name) or w.Recipients.Count != 1:
            continue
        relayout(w)
        b = w.Attributes.Bounds
        rec = old_xy.get(name)
        if not (w.InstanceGuid in fresh or (rec and abs(b.Left - rec[0]) < 2 and abs(b.Top - rec[1]) < 2) or
                (rec is None and abs(w.Attributes.Pivot.X - (comp.Attributes.Pivot.X - WIDGET_DX)) < 2)):
            counts["boxes you moved, left where they are"] += 1
            continue
        pb = p.Attributes.Bounds
        top = float(pb.Top + pb.Height / 2.0 - b.Height / 2.0)
        col = (row - 1) % STAIR_N
        for k in range(24):
            left = right - (col + k) * STAIR_DX - b.Width
            r = System.Drawing.RectangleF(float(left), top, b.Width, b.Height)
            if not any(r.IntersectsWith(q) for q in placed):
                break
        w.Attributes.Pivot = PT(float(w.Attributes.Pivot.X + left - b.Left), float(w.Attributes.Pivot.Y + top - b.Top))
        if isinstance(w, GH_Panel):
            w.Attributes.Bounds = System.Drawing.RectangleF(float(left), top, b.Width, b.Height)
        relayout(w)
        nb = w.Attributes.Bounds
        placed.append(System.Drawing.RectangleF(nb.Left, nb.Top, nb.Width, nb.Height))
        out[name] = [float(nb.Left), float(nb.Top)]
        counts["boxes placed in the stair"] += 1
    return out


def code_of(info):
    with open(info["path"], encoding="utf-8-sig") as f:
        return f.read()


def new_component(doc, proxy, nick, info, x, y):
    c = proxy.CreateInstance()
    c.NickName = nick
    while c.Params.Input.Count:
        c.Params.UnregisterInputParameter(c.Params.Input[0], True)
    while c.Params.Output.Count:
        c.Params.UnregisterOutputParameter(c.Params.Output[0], True)
    add_param(c, GH_ParameterSide.Input, "run")
    for o in info["outputs"]:
        add_param(c, GH_ParameterSide.Output, o)
    c.VariableParameterMaintenance()
    c.Params.OnParametersChanged()
    set_source(c, code_of(info))
    place(doc, c, x, y)
    pn = GH_Panel()
    pn.NickName = nick + " log"
    b = c.Attributes.Bounds
    place(doc, pn, b.Right + LOG_DX, b.Top)
    pn.Attributes.Bounds = System.Drawing.RectangleF(b.Right + LOG_DX, b.Top, LOG_W, LOG_H)
    pn.AddSource(find_param(c.Params.Output, "log"))
    return c


def comps_by_nick(doc):
    out = {}
    for o in doc.Objects:
        if isinstance(o, GH.Kernel.IGH_Component):
            out.setdefault(str(o.NickName), o)
    return out


def button_on(doc, comp, nick):
    p = find_param(comp.Params.Input, "run")
    for s in list(p.Sources):
        if isinstance(s, GH_ButtonObject):
            return s
    b = GH_ButtonObject()
    b.NickName = nick
    place(doc, b, comp.Attributes.Pivot.X - WIDGET_DX, input_y(comp, p))
    p.AddSource(b)
    return b


def build(doc, me, scripts, state, log):
    proxy = py3_proxy()
    counts = {k: 0 for k in ("components added", "code replaced", "code unchanged", "inputs added",
                             "widgets added", "widgets kept as you set them", "widgets moved to a new default",
                             "widgets swapped (input changed kind)", "inputs removed (the script no longer has them)",
                             "inputs set to list / item access", "type hints set", "slider ranges set from the script",
                             "boxes kept (they hold your data)", "boxes placed in the stair",
                             "boxes you moved, left where they are", "renamed REMOVED")}
    hints_all, xy_all, hint_fail, new_xy = state.get("hints", {}), state.get("box_xy", {}), [], {}
    have = comps_by_nick(doc)
    bx, by = float(me.Attributes.Pivot.X), float(me.Attributes.Pivot.Y)
    defaults = state.get("defaults", {})
    new_defaults, placed, changed = {}, [], []
    code_sha = state.get("code_sha", {})
    solo_y = by + TOP_DY
    for o in have.values():                                     # new solo components go below the lowest one
        if str(o.NickName).endswith(" solo"):
            solo_y = max(solo_y, float(o.Attributes.Bounds.Bottom) + GAP_Y)
    chain = [s for s in scripts if s["role"] == "chain"]
    cx, cy = bx + CHAIN_DX, by + TOP_DY
    last_chain = None
    for s in scripts:
        for nick in ([s["label"]] if s["role"] == "chain" else []) + [s["label"] + " solo"]:
            c = have.get(nick)
            if c is None:
                if nick.endswith(" solo"):
                    c = new_component(doc, proxy, nick, s, bx + SOLO_DX, solo_y)
                    hints_all.pop(nick, None)                       # a new component: nothing set on it yet
                    xy_all.pop(nick, None)
                else:
                    if last_chain is not None:
                        cx = float(last_chain.Attributes.Pivot.X) + STEP_X
                        cy = float(last_chain.Attributes.Pivot.Y) + STEP_Y
                    c = new_component(doc, proxy, nick, s, cx, cy)
                    hints_all.pop(nick, None)
                    xy_all.pop(nick, None)
                counts["components added"] += 1
                have[nick] = c
                changed.append(nick)
            else:
                if code_sha.get(nick) == s["sha"]:
                    counts["code unchanged"] += 1      # same checksum as the code put in last time
                else:
                    set_source(c, code_of(s))
                    c.ExpireSolution(False)
                    counts["code replaced"] += 1
                    changed.append(nick)
            fresh, hints = set(), hints_all.setdefault(nick, {})
            new_defaults[nick] = fit_inputs(doc, c, s, defaults.get(nick, {}), counts, fresh, hints, hint_fail)
            new_xy[nick] = stair(c, fresh, xy_all.get(nick, {}), counts)
            if nick.endswith(" solo"):
                button_on(doc, c, s["label"] + " Button")
                solo_y = max(solo_y, float(c.Attributes.Bounds.Bottom) + GAP_Y)
            else:
                last_chain = c
            placed.append(nick)
    # chain wiring: Button -> first run, every done -> next run (redone each press: the order may have changed)
    chain_comps = [have[s["label"]] for s in chain]
    for i, c in enumerate(chain_comps):
        p = find_param(c.Params.Input, "run")
        if i == 0:
            for src in list(p.Sources):
                if not isinstance(src, GH_ButtonObject):
                    p.RemoveSource(src)
            button_on(doc, c, "Chain Button")
        else:
            prev_done = find_param(chain_comps[i - 1].Params.Output, "done")
            if not (p.SourceCount == 1 and p.Sources[0] is prev_done):
                p.RemoveAllSources()
                p.AddSource(prev_done)
    for nick in state.get("placed", []):                        # taken out of board_order.txt
        if nick not in placed and nick in have:
            c = have[nick]
            p = find_param(c.Params.Input, "run")
            if p is not None:
                p.RemoveAllSources()
            c.NickName = "REMOVED " + nick
            counts["renamed REMOVED"] += 1
    state["defaults"], state["placed"] = new_defaults, placed
    state["hints"] = dict((n, h) for n, h in hints_all.items() if n in placed)
    state["box_xy"] = new_xy
    if hint_fail:
        log.append("FLAG type hint not set on %d inputs (they work without one): %s" % (len(hint_fail),
                                                                                     ", ".join(hint_fail[:12])))
    state["code_sha"] = {n: next(s["sha"] for s in scripts if n in (s["label"], s["label"] + " solo")) for n in placed}
    for k, v in counts.items():
        log.append("%-40s %d" % (k, v))
    log.append("components moved: 0 (existing components are never moved)")
    # what the scheduler runs: the LEFT-COLUMN copies (no done wires: one press = one script, nothing else starts),
    # chain scripts first in chain order, then the left-only ones
    queue = [{"label": sc_["label"], "comp": have[sc_["label"] + " solo"], "sha": sc_["sha"], "prefix": sc_["prefix"],
              "chain": have[sc_["label"]] if sc_ in chain else None}
             for sc_ in chain + [x for x in scripts if x["role"] == "solo"]]
    return queue


def own_toggles(doc, me, log):
    """the builder's own run_after and force inputs, each with a False toggle, added once"""
    for name in ("run_after", "force"):
        p = find_param(me.Params.Input, name)
        if p is None:
            p = add_param(me, GH_ParameterSide.Input, name)
            me.VariableParameterMaintenance()
            me.Params.OnParametersChanged()
            log.append("added the builder's own input " + name + " (toggle False)")
        if p.SourceCount == 0:
            p.AddSource(make_widget(doc, name, "toggle", False, me.Attributes.Pivot.X - WIDGET_DX, input_y(me, p)))


# ---------------------------------------------------------------- run_after: run only what needs it
# Aras 15:29-15:44 UTC: the builder decides, and presses the LEFT-COLUMN copies (their widgets count; the chain row
# stays for the manual Chain Button). A script runs when its code, its widgets or anything it reads changed
# since its last good run (or with run_after + force). One script per Grasshopper solution, in chain order; a script
# that wrote the same files as before wakes nothing after it. What each script reads: kit/scripts/script_reads.txt
# ("<file prefix>: <path under Downloads/Bergama>", folders end in "/", "<file prefix>: rhino" = reads Rhino layers).
RUNS = os.path.join(CACHE_DIR, "runs.json")
READS_FILE = "script_reads.txt"
HASH_GBPS = 0.5                                   # check-time estimate: GB hashed per second per core


def read_lists():
    out = {}
    p = os.path.join(SCRIPTS_DIR, READS_FILE)
    if os.path.isfile(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.split("#", 1)[0].strip()
            k, _, v = ln.partition(":")
            k, v = k.strip(), v.strip().replace("\\", "/")
            if k and v:
                out.setdefault(k, []).append(v)
    return out


def _hash_file(path):
    h = hashlib.blake2b(digest_size=16)
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Prints(object):
    """file fingerprints: size + mtime first, the content hash only when those changed; several cores"""

    def __init__(self, cache):
        self.cache = cache                       # {abs path: [size, mtime_ns, hash]} kept in runs.json
        self.walked = {}                         # folder listings of this check (cleared after each run)

    def _stat(self, path):
        try:
            st = os.stat(path)
            return st.st_size, st.st_mtime_ns
        except OSError:
            return None

    def files_of(self, rel):
        """the absolute files behind one read entry (a folder = every file under it)"""
        ap = os.path.join(BASE, *rel.strip("/").split("/"))
        if rel in self.walked:
            return self.walked[rel]
        if rel.endswith("/"):
            out = []
            for root, dirs, files in os.walk(ap):
                dirs.sort()
                out += [os.path.join(root, f) for f in sorted(files)]
            self.walked[rel] = out
            return out
        return [ap]

    def to_hash(self, paths):
        """paths whose size or mtime differ from the cache, with their total bytes"""
        need, nbytes = [], 0
        for p in paths:
            st = self._stat(p)
            c = self.cache.get(p)
            if st and not (c and c[0] == st[0] and c[1] == st[1]):
                need.append(p)
                nbytes += st[0]
        return need, nbytes

    def hash_all(self, paths):
        need, _ = self.to_hash(paths)
        if need:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max(1, (os.cpu_count() or 2) - 1)) as ex:
                for p, h in zip(need, ex.map(_hash_file, need)):
                    st = self._stat(p)
                    if st:
                        self.cache[p] = [st[0], st[1], h]

    def of(self, rels):
        """{read entry: fingerprint} ("missing" when nothing is there)"""
        files = {r: self.files_of(r) for r in rels}
        self.hash_all([f for fl in files.values() for f in fl])
        out = {}
        for r, fl in files.items():
            hs = [(os.path.relpath(f, BASE), self.cache[f][2]) for f in fl if f in self.cache and self._stat(f)]
            out[r] = hashlib.blake2b(json.dumps(hs).encode("utf-8"), digest_size=16).hexdigest() if hs else "missing"
        return out


def rhino_print():
    """one checksum of the open Rhino model (every object's geometry + layer); None without Rhino. Recomputed only
    when Rhino reported an object or layer change since the last one (events counted in sticky, this session)."""
    try:
        import Rhino
        import scriptcontext as sc
        w = sc.sticky.get("bergama_rhino_watch")
        if w is None:
            w = {"n": 0, "at": None, "crc": None}

            def bump(sender, e):
                w["n"] += 1
            RD = Rhino.RhinoDoc                   # subscribed once per Rhino session
            RD.AddRhinoObject += bump
            RD.DeleteRhinoObject += bump
            RD.ReplaceRhinoObject += bump
            RD.UndeleteRhinoObject += bump
            RD.ModifyObjectAttributes += bump
            RD.LayerTableEvent += bump
            w["bump"] = bump
            sc.sticky["bergama_rhino_watch"] = w
        doc = Rhino.RhinoDoc.ActiveDoc
        key = [doc.RuntimeSerialNumber, w["n"]]
        if w["at"] == key and w["crc"]:
            return w["crc"]
        crc = 0
        for o in doc.Objects:
            crc = o.Geometry.DataCRC(crc)
            crc = (crc * 31 + o.Attributes.LayerIndex) & 0xFFFFFFFF
        w["at"], w["crc"] = key, "%08x" % crc
        return w["crc"]
    except Exception:
        return None


def widgets_of(comp):
    out = {}
    for p in comp.Params.Input:
        if p.SourceCount and widget_kind(p.Sources[0]):
            out[pname(p)] = widget_value(p.Sources[0])
    return out


def done_of(comp):
    """the text on the component's done output, None when it can't be read"""
    try:
        p = find_param(comp.Params.Output, "done")
        for g in p.VolatileData.AllData(True):
            return str(g.Value if hasattr(g, "Value") else g)
    except Exception:
        pass
    return None


def schedule(doc, fn, ms=5):
    doc.ScheduleSolution(ms, GH.Kernel.GH_Document.GH_ScheduleDelegate(fn))


def press(b, down):
    """a Button down (True) or up (False), then a Grasshopper solution right away; called from Rhino idle only,
    so no solution is running and the pressed scripts have finished when this returns"""
    b.ButtonDown = bool(down)
    b.ExpireSolution(True)


def on_idle(doc, fn):
    """fn(doc) once, the next time Rhino is idle and Grasshopper is not solving (v3.3 scheduled the next step from
    inside a scheduled step: real Grasshopper drops that, so the run pass never started, Aras 19:27 UTC)"""
    import Rhino
    st = {"done": False}

    def h(sender, e):
        if st["done"]:
            return
        try:
            if doc.SolutionState == GH.Kernel.GH_ProcessStep.Process:
                return                                       # a solution is running: next idle
        except Exception:
            pass
        st["done"] = True
        try:
            Rhino.RhinoApp.Idle -= h
        except Exception:
            pass
        fn(doc)
    Rhino.RhinoApp.Idle += h


def flush_log(log, note=""):
    try:
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write("\n".join(log) + ("\n" + note if note else ""))
    except Exception:
        pass


def proc_secs(c, fallback):
    """the component's processor time; under 0.5 s (a chained solve reads about 0) the fallback (v5, S5)"""
    try:
        s = float(c.ProcessorTime.TotalSeconds)
    except Exception:
        return fallback
    return s if s >= 0.5 else fallback


def script_log(it):
    """the script's own log: Downloads/Bergama/logs/<board_order prefix>_log.txt (v5, S5)"""
    return os.path.join(LOG_DIR, it["prefix"] + "_log.txt")


def log_mtime(it):
    """when the script's own log was last written (time.time() seconds), None when there is no log"""
    try:
        return os.path.getmtime(script_log(it))
    except OSError:
        return None


def chain_secs(items, t_start, total):
    """{label: seconds} after one Chain Button press (v5, S5 G6): a script's log time minus the end of the one
    before it (the first one: minus the press start), only for logs written after the press started; else its
    processor time, else the whole chain's time shared out"""
    out, prev = {}, t_start
    for it in items:
        m = log_mtime(it)
        if m is not None and m >= t_start:
            out[it["label"]] = max(0.0, m - prev)
            prev = m
        else:
            out[it["label"]] = proc_secs(it["chain"], total / max(1, len(items)))
    return out


def fail_reason(it, t_start, done_text):
    """why a script failed, for its FAILED line (v5, S5 G7): the first line of its own log that starts with ERROR
    (marked "(log from HH:MM)" when that log is older than this run), else the text it put on done; 150 chars"""
    m = log_mtime(it)
    if m is not None:
        try:
            with open(script_log(it), encoding="utf-8", errors="replace") as f:
                for ln in f:
                    ln = ln.strip()
                    if ln.startswith("ERROR"):
                        old = " (log from %s)" % time.strftime("%H:%M", time.localtime(m)) if m < t_start else ""
                        return ln[:150] + old
        except Exception:
            pass
    return (done_text or "no done text").replace("\r", " ").replace("\n", " ").strip()[:150]


_ABORT = [None]                                   # set by run_needed: ends the pass with an ERROR line


def guarded(fn):
    """a scheduled step: an error ends the pass with an ERROR line instead of a silent stop"""
    def g(d):
        try:
            fn(d)
        except Exception as e:
            import traceback
            if _ABORT[0]:
                _ABORT[0]("ERROR " + str(e) + "\n" + traceback.format_exc())
    return g


def run_needed(doc, me, queue, force, log, finish):
    """the scheduler: decide, run one script, record, go on; the log gets ran / skipped + reason + times"""
    try:
        runs = json.load(open(RUNS, encoding="utf-8"))
    except Exception:
        runs = {}
    rec, prints = runs.setdefault("scripts", {}), Prints(runs.setdefault("files", {}))
    reads = read_lists()
    if not reads:
        log.append("FLAG no %s yet: every script counts as changed" % READS_FILE)
    rh = {"now": None}
    if any("rhino" in v for v in reads.values()):
        t = time.time()
        rh["now"] = rhino_print()
        log.append("Rhino model checksum: %.1f s" % (time.time() - t))
    can_press = hasattr(GH_ButtonObject(), "ButtonDown")

    def abort(msg):
        log.append(msg)
        finish()
    _ABORT[0] = abort
    tally = {"ran": 0, "skipped": 0, "failed": 0, "not run": 0}
    log.append("run_after%s: one script at a time" % (" + force (everything)" if force else ""))

    def decide(it):
        """(run?, reason, check seconds)"""
        t = time.time()
        r = rec.get(it["label"])
        lst = [x for x in reads.get(it["prefix"], []) if x != "rhino"]
        if force:
            return True, "force", 0.0
        if not r:
            return True, "never run by the builder", 0.0
        if r.get("sha") != it["sha"]:
            return True, "code updated", 0.0
        it["w"] = widgets_of(it["comp"])
        if r.get("widgets") != it["w"]:
            return True, "widget changed", 0.0
        if it["prefix"] not in reads:
            return True, "no read list for this script", 0.0
        files = [f for x in lst for f in prints.files_of(x)]
        _, nbytes = prints.to_hash(files)
        est = nbytes / (HASH_GBPS * 1e9 * max(1, (os.cpu_count() or 2) - 1))
        if est > 1.0 and (r.get("secs") or 1e9) < est:     # v5: a recorded 0 s (old chain records) = unknown
            return True, "a run (%.0f s) is quicker than checking (%.0f s)" % (r["secs"], est), 0.0
        now = prints.of(lst)
        old = r.get("reads", {})
        diff = [x for x in lst if now.get(x) != old.get(x)]
        if "rhino" in reads.get(it["prefix"], []) and rh["now"] and r.get("rhino") != rh["now"]:
            diff.append("Rhino model")
        dt = time.time() - t
        if diff:
            return True, "changed: " + ", ".join(diff[:4]) + (" +%d more" % (len(diff) - 4) if len(diff) > 4 else ""), dt
        return False, "nothing it reads changed", dt

    def record(it, secs):
        lst = [x for x in reads.get(it["prefix"], []) if x != "rhino"]
        prints.walked.clear()                    # the run may have written into read folders
        rec[it["label"]] = {"sha": it["sha"], "widgets": it.get("w") or widgets_of(it["comp"]), "reads": prints.of(lst),
                            "secs": round(secs, 1), "time": time.strftime("%Y-%m-%d %H:%M:%S")}

    def step(i):
        def go(d):
            k = i
            while k < len(queue):
                it = queue[k]
                need, why, dt = decide(it)
                if need:
                    break
                tally["skipped"] += 1
                log.append("  skipped %-18s %s (check %.2f s)" % (it["label"], why, dt))
                k += 1
            if k >= len(queue):
                return end(d)
            it = queue[k]
            if not can_press:
                log.append("  FLAG %-18s needs a run (%s): press its Button yourself (this Grasshopper cannot)"
                           % (it["label"], why))
                return on_idle(d, guarded(step(k + 1)))
            c = it["comp"]
            tb = button_on(d, c, it["label"] + " Button")
            flush_log(log, "running %s ..." % it["label"])
            t = time.time()
            press(tb, True)                          # the script runs inside this call
            secs = time.time() - t
            dn = done_of(c)
            press(tb, False)
            if dn is not None and not dn.startswith("done"):
                tally["failed"] += 1
                log.append("  FAILED  %-18s %s (check %.2f s, %.0f s): not recorded, runs again next time: %s"
                           % (it["label"], why, dt, secs, fail_reason(it, t, dn)))
            else:
                tally["ran"] += 1
                record(it, secs)
                log.append("  ran     %-18s %s (check %.2f s, run %.0f s)" % (it["label"], why, dt, secs))
            flush_log(log)
            on_idle(d, guarded(step(k + 1)))
        return go

    def chain_all(d):
        """run_after + force: press the Chain Button once; the whole chain runs through its done -> run wires"""
        items = [it for it in queue if it.get("chain")]
        if not items or not can_press:
            return step(0)(d)
        tb = button_on(d, items[0]["chain"], "Chain Button")
        flush_log(log, "running the whole chain (Chain Button) ...")
        t = time.time()
        press(tb, True)
        total = time.time() - t
        press(tb, False)
        cs = chain_secs(items, t, total)              # v5: each script's time from its own log
        for it in items:
            dn = done_of(it["chain"])
            secs = cs[it["label"]]
            if dn is not None and not dn.startswith("done"):
                tally["failed"] += 1
                log.append("  FAILED  %-18s force, chain (%.0f s): not recorded, runs again next time: %s"
                           % (it["label"], secs, fail_reason(it, t, dn)))
            elif (log_mtime(it) or 0) < t:          # v5.1: its own log was not written during this press
                tally["not run"] += 1
                log.append("  not run %-18s force, chain: chain stopped before it (no log written during this "
                           "press): not recorded, runs again next time" % it["label"])
            else:
                tally["ran"] += 1
                record(it, secs)
                log.append("  ran     %-18s force, chain (run %.0f s)" % (it["label"], secs))
        log.append("  whole chain: %.0f s" % total)
        flush_log(log)
        on_idle(d, guarded(step(len(items))))

    def end(d):
        if rh["now"]:
            rh["now"] = rhino_print()            # after this pass's own bakes: only YOUR later edits count
            for it in queue:
                if "rhino" in reads.get(it["prefix"], []) and it["label"] in rec:
                    rec[it["label"]]["rhino"] = rh["now"]
        try:
            with open(RUNS, "w", encoding="utf-8") as f:
                json.dump(runs, f, indent=1)
        except Exception as e:
            log.append("FLAG run record not saved: %s" % e)
        log.append("run_after: %d ran, %d skipped, %d failed, %d not run" % (tally["ran"], tally["skipped"],
                                                                         tally["failed"], tally["not run"]))
        finish()

    guarded(chain_all if force else step(0))(doc)


# ---------------------------------------------------------------- speed caches in the cloud
# Aras 15:45 UTC: the scripts' speed caches backed up in the cloud so a cold PC starts warm. Folders (under
# Downloads/Bergama) listed in kit/scripts/cloud_cache.txt; stored as assets of the GitHub Release "bergama-cache"
# (one asset per file: name = short path hash + file name, label = "<content hash>|<path under Downloads/Bergama>"). Before the build: assets missing here are
# downloaded. At the end of the press: new or changed files uploaded, assets whose file is gone here deleted.
CACHE_LIST = "cloud_cache.txt"
CACHE_TAG = "bergama-cache"
CACHE_HASHES = os.path.join(CACHE_DIR, "cache_hashes.json")


def asset_name(rel):
    base = re.sub(r"[^A-Za-z0-9._-]", "_", rel.split("/")[-1])[-80:]
    return hashlib.blake2b(rel.encode("utf-8"), digest_size=5).hexdigest() + "_" + base


def label_parts(a):
    """(content hash, path) from an asset's label"""
    h, _, rel = (a.get("label") or "").partition("|")
    return h, rel


def cache_folders():
    p = os.path.join(SCRIPTS_DIR, CACHE_LIST)
    out = []
    if os.path.isfile(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.split("#", 1)[0].strip().replace("\\", "/").strip("/")
            if ln:
                out.append(ln)
    return out


def api(method, url, token, body=None, ctype="application/json"):
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "bergama-board-builder"}
    if token:
        hdr["Authorization"] = "Bearer " + token
    data = None
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        hdr["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=hdr, method=method)
    with urllib.request.urlopen(req, timeout=600) as r:
        raw = r.read()
    return json.loads(raw.decode("utf-8")) if raw else None


def cache_release(token, make):
    base = "https://api.github.com/repos/%s/releases" % REPO
    try:
        return api("GET", base + "/tags/" + CACHE_TAG, token)
    except urllib.error.HTTPError as e:
        if e.code != 404 or not make:
            raise
    return api("POST", base, token, {"tag_name": CACHE_TAG, "name": "Bergama speed caches (made by the board builder)",
                                     "body": "Machine-made: the scripts' speed caches. Do not edit by hand.",
                                     "target_commitish": BRANCH})


def cache_assets(rel, token):
    out, page = {}, 1
    while True:
        lst = api("GET", "https://api.github.com/repos/%s/releases/%d/assets?per_page=100&page=%d"
                  % (REPO, rel["id"], page), token)
        for a in lst or []:
            out[a["name"]] = a
        if not lst or len(lst) < 100:
            return out
        page += 1


def cache_local():
    """{path under Downloads/Bergama: abs path} of every file in the listed cache folders"""
    out = {}
    for fo in cache_folders():
        top = os.path.join(BASE, *fo.split("/"))
        for root, dirs, files in os.walk(top):
            for f in files:
                if f.endswith(".part"):
                    continue
                ap = os.path.join(root, f)
                out[os.path.relpath(ap, BASE).replace(os.sep, "/")] = ap
    return out


_CACHE_OK = [False]                               # cache_down saw the cloud this press: only then may cache_up delete


def cache_down(log):
    """assets this PC lacks -> downloaded (before anything runs)"""
    _CACHE_OK[0] = False
    if not cache_folders():
        return
    try:
        rel = cache_release(gh_token(), False)
    except Exception as e:
        if getattr(e, "code", None) == 404:
            _CACHE_OK[0] = True
        log.append("cache: no cloud copy yet (%s)" % getattr(e, "code", e))
        return
    have = cache_local()
    assets = cache_assets(rel, gh_token())
    get = [a for a in assets.values() if label_parts(a)[1] and label_parts(a)[1] not in have
           and label_parts(a)[1].split("/")[0] in ("cached", "output")]
    if get:
        from concurrent.futures import ThreadPoolExecutor

        def one(a):
            dst = os.path.join(BASE, *label_parts(a)[1].split("/"))
            data = http(a["browser_download_url"], "application/octet-stream", None)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst + ".part", "wb") as f:
                f.write(data)
            os.replace(dst + ".part", dst)
            return len(data)
        with ThreadPoolExecutor(8) as ex:
            mb = sum(ex.map(one, get)) / 1e6
        log.append("cache: %d downloaded (%.0f MB) from the cloud" % (len(get), mb))
    else:
        log.append("cache: nothing to download (%d files in the cloud)" % len(assets))
    _CACHE_OK[0] = True


def cache_up(log):
    """new or changed cache files -> uploaded; assets whose file is gone here -> deleted"""
    if not cache_folders():
        return
    token = gh_token()
    if not token:
        log.append("FLAG cache: no token in %s: the caches were not backed up" % SETTINGS_FILE)
        return
    try:
        rel = cache_release(token, True)
        assets = {label_parts(a)[1]: a for a in cache_assets(rel, token).values()}
        have = cache_local()
        try:
            hc = json.load(open(CACHE_HASHES, encoding="utf-8"))
        except Exception:
            hc = {}
        up, gone, mb = 0, 0, 0.0
        for rp, ap in sorted(have.items()):
            st = os.stat(ap)
            c = hc.get(ap)
            if c and c[0] == st.st_size and c[1] == st.st_mtime_ns:
                h = c[2]
            else:
                h = _hash_file(ap)
                hc[ap] = [st.st_size, st.st_mtime_ns, h]
            a = assets.get(rp)
            if a is not None and label_parts(a)[0] == h:
                continue
            if a is not None:
                api("DELETE", "https://api.github.com/repos/%s/releases/assets/%d" % (REPO, a["id"]), token)
            with open(ap, "rb") as f:
                data = f.read()
            api("POST", "https://uploads.github.com/repos/%s/releases/%d/assets?name=%s&label=%s"
                % (REPO, rel["id"], urllib.parse.quote(asset_name(rp)), urllib.parse.quote(h + "|" + rp)),
                token, data, "application/octet-stream")
            up += 1
            mb += len(data) / 1e6
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE_HASHES, "w", encoding="utf-8") as f:
            json.dump(hc, f)
        for rp, a in assets.items():
            if rp not in have and _CACHE_OK[0]:
                api("DELETE", "https://api.github.com/repos/%s/releases/assets/%d" % (REPO, a["id"]), token)
                gone += 1
        log.append("cache: %d uploaded (%.0f MB), %d removed from the cloud, %d files backed up"
                   % (up, mb, gone, len(have)))
    except Exception as e:
        log.append("FLAG cache backup failed (%s): the scripts are not affected" % e)


# ---------------------------------------------------------------- main
_T0 = [0.0]
MODEL_NAME = "Bergama_Altlik.3dm"     # Aras opens it in Rhino by hand before the press (RUN_GUIDE); never opened here


def model_line():
    """v5 (round 9 D2): is Bergama_Altlik.3dm the open Rhino model? Without it ZoneBase and MainBoard use their
    built-in copies of calisma_alan and site_alan"""
    names = []
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
        if doc is not None:
            names = [str(doc.Name or ""), os.path.basename(str(doc.Path or ""))]
    except Exception:
        pass
    want = os.path.splitext(MODEL_NAME)[0].lower()
    if any(os.path.splitext(n)[0].lower() == want for n in names if n):
        return "model %s open" % MODEL_NAME
    return "model fallback copy (%s not open)" % MODEL_NAME


def main(me, run_after=False, force=False):
    t0 = _T0[0] = time.time()
    log = ["%s %s" % (GH_LABEL, VERSION)]
    log.append(model_line())
    for d in (SCRIPTS_DIR, DATA_DIR, CACHE_DIR, LOG_DIR):
        os.makedirs(d, exist_ok=True)
    try:
        _SHA.clear()
        _SHA.update(json.load(open(SHA_FILE, encoding="utf-8")))
    except Exception:
        pass
    cloud = download(log)
    try:
        cache_down(log)
    except Exception as e:
        log.append("FLAG cache download failed (%s): the scripts make their caches themselves" % e)
    order = read_order(cloud)
    if not order:
        raise RuntimeError("no %s in %s and nothing downloaded: nothing to build" % (ORDER_FILE, SCRIPTS_DIR))
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        state = {}
    parsed = state.get("parsed", {})                   # checksum -> inputs read before: unchanged scripts not re-read
    scripts, labels, new_parsed = [], set(), {}
    for prefix, role, lab in order:
        f = newest(prefix)
        if not f:
            log.append("FLAG %s: no %s_v*.py in %s, skipped" % (prefix, prefix, SCRIPTS_DIR))
            continue
        path = os.path.join(SCRIPTS_DIR, f)
        sha = blob_sha(path)
        info = parsed.get(sha)
        if info is None:
            info = parse_script(path)
            info.pop("code", None)
        new_parsed[sha] = info
        info = dict(info, sha=sha, path=path, inputs=[tuple(i) for i in info["inputs"]])
        lab = lab or info["label"] or prefix
        if lab in labels:                                       # two scripts with one name: the file prefix tells them apart
            lab = prefix
        labels.add(lab)
        info.update(role=role, file=f, label=lab, prefix=prefix)
        scripts.append(info)
        log.append("  %-6s %-18s %-46s %d inputs" % (role, info["label"], f, len(info["inputs"])))
    state["parsed"] = new_parsed
    try:
        with open(SHA_FILE, "w", encoding="utf-8") as f:
            json.dump(_SHA, f)
    except Exception:
        pass
    doc = me.OnPingDocument()

    def edit(d):
        try:
            queue = build(d, me, scripts, state, log)
            own_toggles(d, me, log)
            with open(STATE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=1, default=str)
            if run_after:
                if force:                             # Aras 15:25 UTC: both on = every script from the beginning
                    import scriptcontext as sc
                    sc.sticky["bergama_force_run"] = time.time()
                fin = lambda: (cache_up(log), log.append("done in %.1f s" % (time.time() - t0)), _finish(me, log, True))

                def start(d2):
                    try:
                        run_needed(d2, me, queue, force, log, fin)
                    except Exception as e:
                        import traceback
                        log.append("ERROR " + str(e))
                        log.append(traceback.format_exc())
                        _finish(me, log, True)
                flush_log(log, "run_after: starts when Rhino is idle ...")
                on_idle(d, start)
                return
            cache_up(log)
            log.append("done in %.1f s" % (time.time() - t0))
        except Exception as e:
            import traceback
            log.append("ERROR " + str(e))
            log.append(traceback.format_exc())
        _finish(me, log)
    doc.ScheduleSolution(5, GH.Kernel.GH_Document.GH_ScheduleDelegate(edit))
    log.append("building on the canvas ...")
    return log


def _finish(me, log, from_idle=False):
    txt = "\n".join(log)
    try:
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(txt)
    except Exception:
        pass
    ok = not any(ln.startswith("ERROR") for ln in log)
    stk = "bergama_board_builder"
    import scriptcontext as sc
    sc.sticky[stk] = (txt, ("done %s.00 · %d s" % (time.strftime("%H:%M:%S"), round(time.time() - _T0[0])))
                           if ok else "ERROR")
    me.Message = "%s %s · %s" % (GH_LABEL, VERSION, time.strftime("%H:%M")) if ok else "ERROR"
    me.ExpireSolution(from_idle)                    # from Rhino idle no solution is running: start one


_me = ghenv.Component                                              # noqa: F821 (Grasshopper)
_pressed = bool(run) if "run" in globals() else False              # noqa: F821 (Grasshopper input)
import scriptcontext as _sc
_prev = _sc.sticky.get("bergama_board_builder_prev", False)
_sc.sticky["bergama_board_builder_prev"] = _pressed
if _pressed and not _prev:
    try:
        _fl = [globals().get(n) for n in ("run_after", "force")]
        _fl = [any(bool(x) for x in v) if isinstance(v, (list, tuple)) else bool(v) for v in _fl]
        _sc.sticky["bergama_board_builder"] = ("\n".join(main(_me, _fl[0], _fl[1])), "running")
    except Exception as _e:
        import traceback as _tb
        _sc.sticky["bergama_board_builder"] = ("ERROR " + str(_e) + "\n" + _tb.format_exc(), "ERROR")
        _me.Message = "ERROR"
log, done = _sc.sticky.get("bergama_board_builder", ("idle: press the Button", "idle"))
if not log.startswith("ERROR") and done == "idle":
    _me.Message = "%s %s · idle" % (GH_LABEL, VERSION)
print(log)
