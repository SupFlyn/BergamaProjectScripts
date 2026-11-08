# -*- coding: utf-8 -*-
"""Bergama Group 6: BOARD BUILDER = build_gh_chain v3 (8 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.

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
    a script taken out of board_order.txt: its component is unwired and renamed "REMOVED <name>", never deleted
Adding, removing or reordering scripts only changes the files in kit/: this builder never needs a new version for it.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run        Button: nothing happens until it is pressed
  input  force      Boolean Toggle, off by default: run_after AND force both on = every script run from the beginning
                    (whole chain + every left-column-only script; sticky 'bergama_force_run' = time, for the scripts'
                    own caches). Both toggles are added by the builder itself on the first press (Aras 15:25 UTC)
  input  run_after  Boolean Toggle, off by default: True = right after the update, run what changed:
                    the chain from the first updated chain script to its end (the later ones read its results, each
                    script once) and every updated left-column-only script (Aras 15:16 UTC)
  output log   the last run's report
  output done  "done HH:MM:SS.ss · N s" after a good run
board_order.txt: one line per script, "chain: <file prefix> = <name>" (in chain order) or "solo: <file prefix> = <name>"
(left column only); "= <name>" is optional (else the script's GH_LABEL); "#" starts a comment.
"""
import os, re, ast, json, time, hashlib, urllib.request, urllib.parse

# ---- SETTINGS ----
VERSION = "v3"
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
WIDGET_DX = 300.0                      # widgets sit this far left of their component
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
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120) as r:
        return r.read()


def blob_sha(path):
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
    data = http(url, "*/*", token)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)


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
        fetch(lst, lp, token)
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
    for r in sorted(todo):
        it, dst = todo[r], local_path(todo[r]["path"])
        if os.path.isfile(dst) and blob_sha(dst) == it["sha"]:
            same += 1
            continue
        fetch(it, dst, token)
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
    inputs = []
    for name, kind, v in ins:
        v = None if v is NO_VALUE else v
        inputs.append((name, kind or kind_of(v), v))
    for o in ("log", "done"):
        if o not in outs:
            outs.append(o)
    label = consts.get("GH_LABEL") if isinstance(consts.get("GH_LABEL"), str) else None
    return {"label": label, "version": consts.get("VERSION", ""), "inputs": inputs, "outputs": outs, "code": src}


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


def get_source(comp):
    for a in ("Text", "Source", "Code", "Script"):
        try:
            v = getattr(comp, a, None)
            if isinstance(v, str):
                return v
        except Exception:
            pass
    return None


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


def relayout(obj):
    obj.Attributes.ExpireLayout()
    obj.Attributes.PerformLayout()


def place(doc, obj, x, y):
    obj.CreateAttributes()
    obj.Attributes.Pivot = PT(float(x), float(y))
    doc.AddObject(obj, False)
    relayout(obj)
    return obj


def slider_spec(v):
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e9:
        v = int(v)                                            # 1000.0 -> whole-number slider at 1000
    if isinstance(v, int):
        lo, hi = (min(0, 2 * v), max(2 * v, 10)) if v else (0, 10)
        return lo, hi, 0
    s = repr(v)
    dec = min(3, max(1, len(s.split(".")[1]) if "." in s and "e" not in s else 2))
    lo, hi = (min(0.0, 2 * v), max(2 * v, 1.0)) if v else (0.0, 1.0)
    return lo, hi, dec


def make_widget(doc, name, kind, v, x, y):
    if kind == "toggle":
        w = GH_BooleanToggle()
        w.NickName = name
        w.Value = bool(v)
    elif kind == "slider":
        lo, hi, dec = slider_spec(v)
        w = GH_NumberSlider()
        w.NickName = name
        w.Slider.Type = GH.GUI.Base.GH_SliderAccuracy.Float if dec else GH.GUI.Base.GH_SliderAccuracy.Integer
        w.Slider.DecimalPlaces = dec
        w.Slider.Minimum = System.Decimal(lo)
        w.Slider.Maximum = System.Decimal(hi)
        w.Slider.Value = System.Decimal(float(v))
    else:
        w = GH_Panel()
        txt = "" if v is None or isinstance(v, (list, tuple, dict, set)) else str(v)
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


def widget_kind(w):
    if isinstance(w, GH_BooleanToggle):
        return "toggle"
    if isinstance(w, GH_NumberSlider):
        return "slider"
    if isinstance(w, GH_Panel):
        return "panel"
    return None


def widget_value(w):
    k = widget_kind(w)
    if k == "toggle":
        return bool(w.Value)
    if k == "slider":
        return float(System.Decimal.ToDouble(w.Slider.Value))
    if k == "panel":
        return str(w.UserText or "")
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
    else:
        w.UserText = "" if v is None or isinstance(v, (list, tuple, dict)) else str(v)
    w.ExpireSolution(False)


def input_y(comp, p):
    relayout(comp)
    return float(p.Attributes.Pivot.Y) - 10.0


def fit_inputs(doc, comp, info, old_defaults, counts):
    """inputs + widgets of one component; returns {input: default} as now applied"""
    applied = {}
    x = float(comp.Attributes.Pivot.X) - WIDGET_DX
    for name, kind, v in info["inputs"]:
        applied[name] = v
        p = find_param(comp.Params.Input, name)
        if p is None:
            p = add_param(comp, GH_ParameterSide.Input,
                          name, "list" if isinstance(v, (list, tuple)) else None)
            comp.Params.OnParametersChanged()
            counts["inputs added"] += 1
        w = p.Sources[0] if p.SourceCount else None
        wk = widget_kind(w) if w is not None else None
        if w is None:
            p.AddSource(make_widget(doc, name, kind, v, x, input_y(comp, p)))
            counts["widgets added"] += 1
        elif wk is None:
            continue                                              # wired to something else: yours, left alone
        elif wk != kind:
            pv = w.Attributes.Pivot
            p.RemoveSource(w)
            if w.Recipients.Count == 0:
                doc.RemoveObject(w, False)
            p.AddSource(make_widget(doc, name, kind, v, pv.X, pv.Y))
            counts["widgets swapped (input changed kind)"] += 1
        elif name in old_defaults and not same_default(old_defaults[name], v, kind) \
                and same_default(widget_value(w), old_defaults[name], kind):
            set_widget_value(w, kind, v)                          # never touched by you: follows the new default
            counts["widgets moved to a new default"] += 1
        else:
            counts["widgets kept as you set them"] += 1
    for o in info["outputs"]:
        if find_param(comp.Params.Output, o) is None:
            add_param(comp, GH_ParameterSide.Output, o)
    comp.VariableParameterMaintenance()
    comp.Params.OnParametersChanged()
    return applied


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
    set_source(c, info["code"])
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
                             "widgets swapped (input changed kind)", "renamed REMOVED")}
    have = comps_by_nick(doc)
    bx, by = float(me.Attributes.Pivot.X), float(me.Attributes.Pivot.Y)
    defaults = state.get("defaults", {})
    new_defaults, placed, changed = {}, [], []
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
                else:
                    if last_chain is not None:
                        cx = float(last_chain.Attributes.Pivot.X) + STEP_X
                        cy = float(last_chain.Attributes.Pivot.Y) + STEP_Y
                    c = new_component(doc, proxy, nick, s, cx, cy)
                counts["components added"] += 1
                have[nick] = c
                changed.append(nick)
            else:
                if get_source(c) == s["code"]:
                    counts["code unchanged"] += 1
                else:
                    set_source(c, s["code"])
                    c.ExpireSolution(False)
                    counts["code replaced"] += 1
                    changed.append(nick)
            new_defaults[nick] = fit_inputs(doc, c, s, defaults.get(nick, {}), counts)
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
    for k, v in counts.items():
        log.append("%-40s %d" % (k, v))
    log.append("components moved: 0 (existing components are never moved)")
    k = next((i for i, s in enumerate(chain) if s["label"] in changed), None)
    solos = [have[s["label"] + " solo"] for s in scripts if s["role"] == "solo"]
    return {"chain": chain_comps[k:] if k is not None else [], "start": k,
            "solo": [c for c in solos if str(c.NickName) in changed],
            "all": {"chain": chain_comps, "start": 0 if chain_comps else None, "solo": solos}}


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


# ---------------------------------------------------------------- run_after: run what was updated
def press(b, down):
    """a Button pressed (True) or let go (False) by the script"""
    b.ButtonDown = down
    b.ExpireSolution(False)


def run_updated(doc, todo, log):
    """chain from the first updated chain script to its end (the later ones read its results) + every updated
    left-column-only script; each script once"""
    if not todo["chain"] and not todo["solo"]:
        log.append("run_after: nothing was updated, nothing run")
        return
    btns, undo = [], None
    if todo["chain"]:
        first = todo["chain"][0]
        p = find_param(first.Params.Input, "run")
        if todo["start"] == 0:
            btns.append(button_on(doc, first, "Chain Button"))
        else:                         # a Button on its run for this one press; the done wire is put back after
            saved = list(p.Sources)
            p.RemoveAllSources()
            tb = GH_ButtonObject()
            tb.NickName = "update run"
            place(doc, tb, first.Attributes.Pivot.X - WIDGET_DX, input_y(first, p) - 30.0)
            p.AddSource(tb)
            first.ExpireSolution(False)
            btns.append(tb)
            undo = (p, saved, tb)
    for c in todo["solo"]:
        btns.append(button_on(doc, c, str(c.NickName)[:-5] + " Button"))
    if not hasattr(btns[0], "ButtonDown"):
        log.append("FLAG run_after: this Grasshopper cannot press a Button from a script: press these yourself: " +
                   ", ".join(str(b.NickName) for b in btns))
        return

    def down(d):
        for b in btns:
            press(b, True)
        d.ScheduleSolution(5, GH.Kernel.GH_Document.GH_ScheduleDelegate(up))

    def up(d):
        for b in btns:
            press(b, False)
        if undo:
            p, saved, tb = undo
            p.RemoveAllSources()
            for src in saved:
                p.AddSource(src)
            d.RemoveObject(tb, False)
    doc.ScheduleSolution(5, GH.Kernel.GH_Document.GH_ScheduleDelegate(down))
    log.append("run_after: runs %s%s" % (
        ("chain from %s to the end (%d scripts)" % (todo["chain"][0].NickName, len(todo["chain"])))
        if todo["chain"] else "", (("; " if todo["chain"] else "") + "left column: " +
                                   ", ".join(str(c.NickName) for c in todo["solo"])) if todo["solo"] else ""))


# ---------------------------------------------------------------- main
_T0 = [0.0]


def main(me, run_after=False, force=False):
    t0 = _T0[0] = time.time()
    log = ["%s %s" % (GH_LABEL, VERSION)]
    for d in (SCRIPTS_DIR, DATA_DIR, CACHE_DIR, LOG_DIR):
        os.makedirs(d, exist_ok=True)
    cloud = download(log)
    order = read_order(cloud)
    if not order:
        raise RuntimeError("no %s in %s and nothing downloaded: nothing to build" % (ORDER_FILE, SCRIPTS_DIR))
    scripts = []
    labels = set()
    for prefix, role, lab in order:
        f = newest(prefix)
        if not f:
            log.append("FLAG %s: no %s_v*.py in %s, skipped" % (prefix, prefix, SCRIPTS_DIR))
            continue
        info = parse_script(os.path.join(SCRIPTS_DIR, f))
        lab = lab or info["label"] or prefix
        if lab in labels:                                       # two scripts with one name: the file prefix tells them apart
            lab = prefix
        labels.add(lab)
        info.update(role=role, file=f, label=lab)
        scripts.append(info)
        log.append("  %-6s %-18s %-46s %d inputs" % (role, info["label"], f, len(info["inputs"])))
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        state = {}
    doc = me.OnPingDocument()

    def edit(d):
        try:
            todo = build(d, me, scripts, state, log)
            own_toggles(d, me, log)
            if run_after and force:               # Aras 15:25 UTC: both on = every script run from the beginning
                import scriptcontext as sc
                sc.sticky["bergama_force_run"] = time.time()   # for the scripts' own caches: do the full work
                log.append("run_after + force: every script from the beginning")
                run_updated(d, todo["all"], log)
            elif run_after:
                run_updated(d, todo, log)
            with open(STATE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=1, default=str)
            log.append("done in %.1f s" % (time.time() - t0))
        except Exception as e:
            import traceback
            log.append("ERROR " + str(e))
            log.append(traceback.format_exc())
        _finish(me, log)
    doc.ScheduleSolution(5, GH.Kernel.GH_Document.GH_ScheduleDelegate(edit))
    log.append("building on the canvas ...")
    return log


def _finish(me, log):
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
    me.ExpireSolution(False)


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
