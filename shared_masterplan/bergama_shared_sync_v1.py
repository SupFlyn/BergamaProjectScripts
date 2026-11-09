# -*- coding: utf-8 -*-
"""Bergama Group 6: SHARED SYNC v1 (8 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.

Aras 8 Nov 2026 10:24-10:47 UTC: three people (aras, begum, nil) edit the masterplan in Illustrator and in Rhino;
every run must use ONE latest combined file. One press does, in this order:
  1 your Rhino edits (anything you changed under layer 'masterplan' since the last bake) are written into your own
    file Data/shared/my_masterplan.svg (the file you open and save in Illustrator)
  2 that file is UPLOADED to GitHub: SupFlyn/BergamaProjectScripts, branch 'shared', shared/people/<you>/
  3 everything is DOWNLOADED from the cloud (all three people's files + the master); only these copies are read
  4 merge, group by group (each top group of the SVG = one layer in Rhino): a group changed by one person goes in;
    changed by two or more: the newest edit wins (each group keeps its own edit date and editor in
    shared/master/state.json), the other version is saved in shared/master/conflicts/ and the log prints a FLAG
  5 the master goes back to the cloud (shared/master/masterplan_latest.svg) in one commit; git keeps every version
    (the log lists the last 10); your own file becomes the master, so your next edit starts from the latest plan
  6 the master is copied to Data/assets/plan/masterplan_latest.svg: PlanToRhino v2 (wire this component's 'done' into
    its 'run') bakes it, then the planting analysis rebuilds from it
Planting areas: if the master has no planting_area_* groups yet, they are added (hidden) from
Data/assets/planting_areas_seed.svg (traced from the planting board v9, about +-3 m).

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run      Button: nothing happens until it is pressed
  output log      the last run's report
  output done     "done HH:MM:SS.ss · N s" after a good run: wire it into PlanToRhino v2's 'run'
One-time setup on each computer: a text file Downloads/Bergama/Data/shared_settings.txt with two lines
  token=<the GitHub token (fine-grained, this repo only, Contents read and write)>
  me=aras            (or begum / nil)
Never paste the token in a chat. Rule: save in Illustrator before you press the button.
"""
import os, time, json, re, hashlib, base64, copy, math

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "SharedSync"
OUT_FOLDER = "bergama_shared_sync"
LOG_NAME = "bergama_shared_sync_log.txt"
REPO = "SupFlyn/BergamaProjectScripts"            # the shared files live in this repo ...
BRANCH = "shared"                                 # ... on this branch (made from main on the first run)
BASE_BRANCH = "main"
CLOUD = "shared"                                  # folder in the repo: shared/people/<name>/, shared/master/
PEOPLE = ("aras", "begum", "nil")
SHARED_LOCAL = "shared"                           # Data/shared/ on this computer
ROOT_LAYER = "masterplan"                         # PlanToRhino's parent layer
SKIP_LAYERS = ("analysis_", "masterplan_conflicts")   # sub-layers that are outputs, never written back
HISTORY_N = 10
API = "https://api.github.com"

# ---- Bergama folders (template block, SCRIPT_STANDARD §9) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
LOG_DIR = bg_logs()
SH_DIR = os.path.join(DATA_DIR, SHARED_LOCAL)
MY_FILE = os.path.join(SH_DIR, "my_masterplan.svg")
CLOUD_COPY = os.path.join(SH_DIR, "cloud")
PLAN_DIR = os.path.join(DATA_DIR, "assets", "plan")
SEED_FILE = os.path.join(DATA_DIR, "assets", "planting_areas_seed.svg")
SETTINGS_FILE = os.path.join(DATA_DIR, "shared_settings.txt")
LOCAL_STATE = os.path.join(SH_DIR, "local_state.json")

# PlanToRhino v2 keys (must match bergama_plan_to_rhino_v2.py)
PTR_KEY = "bergama_plan_to_rhino"
STAMP = "bergama_plan_to_rhino"
UNIT_KEY = "bergama_unit"
SYNC_KEY = "bergama_shared_sync"
CAP = 0.716

SVG_NS = "http://www.w3.org/2000/svg"
XL_NS = "http://www.w3.org/1999/xlink"
SVGNS = "{%s}" % SVG_NS
XLINK = "{%s}href" % XL_NS
_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def now_iso(t=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() if t is None else t))


def short(iso):
    try:
        return time.strftime("%d %b %H:%M", time.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return iso or "?"


# =====================================================================================================  settings
def read_settings():
    if not os.path.isfile(SETTINGS_FILE):
        raise RuntimeError("no settings file: make %s with two lines: token=<GitHub token> and me=aras (or begum / nil)"
                           % SETTINGS_FILE)
    st = {}
    for line in open(SETTINGS_FILE, encoding="utf-8-sig"):
        if "=" in line:
            k, v = line.split("=", 1)
            st[k.strip().lower()] = v.strip()
    if not st.get("token"):
        raise RuntimeError("no 'token=' line in " + SETTINGS_FILE)
    me = (st.get("me") or "").lower()
    if me not in PEOPLE:
        raise RuntimeError("'me=' in %s must be one of %s (now: '%s')" % (SETTINGS_FILE, ", ".join(PEOPLE), me))
    return st["token"], me


# =====================================================================================================  GitHub
class Retry(Exception):
    pass


class GitHub(object):
    """the few GitHub REST calls the sync needs (standard library only)"""

    def __init__(self, token, repo=REPO, branch=BRANCH, opener=None):
        self.token, self.repo, self.branch = token, repo, branch
        self.opener = opener                     # tests pass a fake; None = urllib

    def call(self, method, path, body=None, accept="application/vnd.github+json", ok=(200, 201)):
        url = path if path.startswith("http") else API + path
        data = json.dumps(body).encode("utf-8") if body is not None else None
        hdr = {"Authorization": "Bearer " + self.token, "Accept": accept, "User-Agent": "bergama-shared-sync",
               "X-GitHub-Api-Version": "2022-11-28"}
        if data is not None:
            hdr["Content-Type"] = "application/json"
        if self.opener is not None:
            code, raw = self.opener(method, url, hdr, data)
        else:
            import urllib.request, urllib.error
            req = urllib.request.Request(url, data=data, headers=hdr, method=method)
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    code, raw = r.status, r.read()
            except urllib.error.HTTPError as e:
                code, raw = e.code, e.read()
        if code not in ok:
            msg = raw[:300].decode("utf-8", "replace")
            if code == 401:
                raise RuntimeError("GitHub refused the token (401): check token= in %s" % SETTINGS_FILE)
            if code == 403 and b"rate limit" in raw.lower():
                raise RuntimeError("GitHub rate limit reached: wait an hour and run again")
            raise RuntimeError("GitHub %s %s -> %d: %s" % (method, url.replace(API, ""), code, msg))
        return code, raw

    def j(self, method, path, body=None, ok=(200, 201)):
        code, raw = self.call(method, path, body, ok=ok)
        return code, (json.loads(raw.decode("utf-8")) if raw else None)

    def head(self):
        """the branch's last commit; the branch is made from main the first time"""
        code, d = self.j("GET", "/repos/%s/git/ref/heads/%s" % (self.repo, self.branch), ok=(200, 404))
        if code == 404:
            _, b = self.j("GET", "/repos/%s/git/ref/heads/%s" % (self.repo, BASE_BRANCH))
            self.j("POST", "/repos/%s/git/refs" % self.repo,
                   {"ref": "refs/heads/" + self.branch, "sha": b["object"]["sha"]})
            return b["object"]["sha"]
        return d["object"]["sha"]

    def tree(self, commit_sha):
        """{path: blob sha} for every file under CLOUD/ at this commit"""
        _, c = self.j("GET", "/repos/%s/git/commits/%s" % (self.repo, commit_sha))
        _, t = self.j("GET", "/repos/%s/git/trees/%s?recursive=1" % (self.repo, c["tree"]["sha"]))
        return dict((e["path"], e["sha"]) for e in t.get("tree", [])
                    if e.get("type") == "blob" and e["path"].startswith(CLOUD + "/")), c["tree"]["sha"]

    def blob(self, sha):
        _, raw = self.call("GET", "/repos/%s/git/blobs/%s" % (self.repo, sha), accept="application/vnd.github.raw")
        return raw

    def commit(self, parent, base_tree, files, message):
        """one commit with these files {path: bytes}; fails with Retry if somebody else committed meanwhile"""
        items, sent = [], {}
        for p, data in sorted(files.items()):
            h = git_sha(data)
            if h not in sent:                         # the same content (master = my file) is sent once
                _, b = self.j("POST", "/repos/%s/git/blobs" % self.repo,
                              {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
                sent[h] = b["sha"]
            items.append({"path": p, "mode": "100644", "type": "blob", "sha": sent[h]})
        _, t = self.j("POST", "/repos/%s/git/trees" % self.repo, {"base_tree": base_tree, "tree": items})
        _, c = self.j("POST", "/repos/%s/git/commits" % self.repo,
                      {"message": message, "tree": t["sha"], "parents": [parent]})
        code, d = self.j("PATCH", "/repos/%s/git/refs/heads/%s" % (self.repo, self.branch),
                         {"sha": c["sha"], "force": False}, ok=(200, 422))
        if code == 422:
            raise Retry()
        return c["sha"]

    def history(self, path, n=HISTORY_N):
        _, d = self.j("GET", "/repos/%s/commits?sha=%s&path=%s&per_page=%d" % (self.repo, self.branch, path, n))
        return [(x["commit"]["author"]["date"], x["commit"]["message"].split("\n")[0], x["sha"][:7]) for x in d or []]


def git_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# =====================================================================================================  SVG units
def register_ns(text):
    import xml.etree.ElementTree as ET
    for pfx, uri in re.findall(r'xmlns:([A-Za-z0-9_]+)="([^"]+)"', text[:5000]):
        try:
            ET.register_namespace(pfx, uri)
        except Exception:
            pass
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XL_NS)


def parse_svg(data):
    import xml.etree.ElementTree as ET
    text = data.decode("utf-8", "replace") if isinstance(data, bytes) else data
    register_ns(text)
    return ET.fromstring(text.encode("utf-8"))


def to_bytes(root):
    import xml.etree.ElementTree as ET
    raw = ET.tostring(root, encoding="utf-8")
    if raw.startswith(b"<?xml"):
        raw = raw.split(b"?>", 1)[1].lstrip()
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + raw


def local(tag):
    return tag.split("}", 1)[1] if isinstance(tag, str) and "}" in tag else (tag if isinstance(tag, str) else "")


def gid(el):
    return el.get("id") or el.get("data-name")


def ukey(name):
    """Illustrator adds _2, _3 ... to a repeated name: the group stays the same unit"""
    if re.match(r"^Layer_\d+$", name):
        return name
    return re.sub(r"(_\d+)+$", "", name) or name


def units_of(root):
    """the SVG's top groups, the same ones PlanToRhino turns into layers: [(key, element, parent)]"""
    out = []
    for ch in root:
        if local(ch.tag) != "g":
            continue
        nm = gid(ch)
        if nm and re.match(r"^Layer_\d+$", nm) and len([c for c in ch if local(c.tag) == "g"]) >= 2:
            for c in ch:
                if local(c.tag) == "g" and gid(c):
                    out.append((ukey(gid(c)), c, ch))
        elif nm:
            out.append((ukey(nm), ch, root))
    seen, res = set(), []
    for k, e, p in out:                           # a repeated key: the later copies get #2, #3
        k2, n = k, 1
        while k2 in seen:
            n += 1
            k2 = "%s#%d" % (k, n)
        seen.add(k2)
        res.append((k2, e, p))
    return res


def parse_css(text):
    out = {}
    text = re.sub(r"/\*.*?\*/", "", text or "", flags=re.S)
    for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", text):
        decl = {}
        for part in body.split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                decl[k.strip().lower()] = v.strip()
        for s_ in sel.split(","):
            s_ = s_.strip()
            if s_.startswith("."):
                out.setdefault(s_[1:], {}).update(decl)
    return out


class Doc(object):
    """one SVG file: root, css classes, ids, unit hashes"""

    def __init__(self, data, who=""):
        self.who = who
        self.root = parse_svg(data)
        self.css = {}
        for st in self.root.iter(SVGNS + "style"):
            self.css.update(parse_css(st.text or ""))
        self.ids = {}
        for el in self.root.iter():
            if el.get("id"):
                self.ids.setdefault(el.get("id"), el)
        self.units = units_of(self.root)
        self._dh = {}
        self.hash = dict((k, self.canon_hash(e)) for k, e, p in self.units)

    def style(self, el):
        st = {}
        for c in (el.get("class") or "").split():
            st.update(self.css.get(c, {}))
        for part in (el.get("style") or "").split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                st[k.strip().lower()] = v.strip()
        return st

    def def_hash(self, ref):
        if ref not in self._dh:
            self._dh[ref] = "?"
            el = self.ids.get(ref)
            self._dh[ref] = self.canon_hash(el) if el is not None else "missing:" + ref
        return self._dh[ref]

    def canon(self, el, out):
        tag = local(el.tag)
        out.append("<" + tag)
        att = {}
        for k, v in el.attrib.items():
            k2 = local(k) if "}" in k else k
            if k2 in ("id", "data-name", "class", "style"):
                continue
            att[k2] = v
        for k, v in self.style(el).items():
            att["s:" + k] = v
        for k in sorted(att):
            v = att[k]
            v = re.sub(r"url\(\s*#([^)]+)\)", lambda m: "url(" + self.def_hash(m.group(1).strip("'\" ")) + ")", v)
            if k == "href" and v.startswith("#"):
                v = "#" + self.def_hash(v[1:])
            v = _NUM.sub(lambda m: "%.1f" % float(m.group(0)), v) if k not in ("href",) or not v.startswith("data:") \
                else hashlib.sha1(v.encode("utf-8")).hexdigest()
            out.append(" %s=%s" % (k, v))
        out.append(">")
        if el.text and el.text.strip():
            out.append(el.text.strip())
        for c in el:
            self.canon(c, out)
            if c.tail and c.tail.strip():
                out.append(c.tail.strip())
        out.append("</%s>" % tag)

    def canon_hash(self, el):
        out = []
        self.canon(el, out)
        return hashlib.sha1("".join(out).encode("utf-8")).hexdigest()[:16]

    def unit(self, key):
        for k, e, p in self.units:
            if k == key:
                return e, p
        return None, None


REF_ATTRS = ("fill", "stroke", "clip-path", "mask", "filter", "marker-start", "marker-mid", "marker-end")


class Composer(object):
    """builds the master: the old master (or the first file) as the frame, units swapped in from other files"""

    def __init__(self, base):
        self.base = base
        self.root = base.root
        self.defs = None
        for ch in self.root:
            if local(ch.tag) == "defs":
                self.defs = ch
                break
        if self.defs is None:
            import xml.etree.ElementTree as ET
            self.defs = ET.Element(SVGNS + "defs")
            self.root.insert(0, self.defs)
        self.ids = dict((el.get("id"), el) for el in self.root.iter() if el.get("id"))
        self.def_h = {}

    def _mhash(self, ref):
        if ref not in self.def_h:
            el = self.ids.get(ref)
            self.def_h[ref] = self.base.canon_hash(el) if el is not None else None
        return self.def_h[ref]

    def bring_def(self, src, ref, who):
        """the def 'ref' of src present in the master (renamed if the master has a different one); returns its id"""
        el = src.ids.get(ref)
        if el is None:
            return ref
        h = src.def_hash(ref)
        if self._mhash(ref) == h:
            return ref
        new = ref
        if new in self.ids:
            new = "%s__%s" % (ref, who)
            n = 1
            while new in self.ids and self._mhash(new) != h:
                n += 1
                new = "%s__%s%d" % (ref, who, n)
            if new in self.ids:
                return new
        cp = self.localize(src, el, who)
        cp.set("id", new)
        self.defs.append(cp)
        self.ids[new] = cp
        self.def_h[new] = h
        return new

    def localize(self, src, el, who):
        """a deep copy whose styles are written on each element (no class), and whose references exist in the master"""
        cp = copy.deepcopy(el)
        for e in cp.iter():
            if e.get("class"):
                st = {}
                for c in e.get("class").split():
                    st.update(src.css.get(c, {}))
                for part in (e.get("style") or "").split(";"):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        st[k.strip().lower()] = v.strip()
                del e.attrib["class"]
                if st:
                    e.set("style", ";".join("%s:%s" % kv for kv in st.items()))
            for k in list(e.attrib):
                v = e.get(k)
                if "url(" in v:
                    e.set(k, re.sub(r"url\(\s*#([^)]+)\)",
                                    lambda m: "url(#%s)" % self.bring_def(src, m.group(1).strip("'\" "), who), v))
                if (k == XLINK or k == "href") and v.startswith("#"):
                    e.set(k, "#" + self.bring_def(src, v[1:], who))
        return cp

    def put(self, key, src, who, order_hint):
        """unit 'key' from src replaces the master's unit (same place), or is added"""
        el, parent = src.unit(key)
        new = self.localize(src, el, who) if src is not self.base else el
        old, op = Doc_unit(self.root, key)
        if old is not None:
            i = list(op).index(old)
            op.remove(old)
            op.insert(i, new)
            return
        par = self.find_parent(parent, src)
        kids = list(par)
        pos = len(kids)
        for k_after in order_hint:                 # keep the source's order: before the next unit the master has
            o2, p2 = Doc_unit(self.root, k_after)
            if o2 is not None and p2 is par:
                pos = kids.index(o2)
                break
        par.insert(pos, new)

    def find_parent(self, src_parent, src):
        nm = gid(src_parent) if src_parent is not None and src_parent is not src.root else None
        if nm:
            for ch in self.root:
                if local(ch.tag) == "g" and gid(ch) == nm:
                    return ch
        if src_parent is src.root:
            return self.root
        for ch in self.root:
            if local(ch.tag) == "g" and re.match(r"^Layer_\d+$", gid(ch) or ""):
                return ch
        return self.root

    def remove(self, key):
        old, op = Doc_unit(self.root, key)
        if old is not None:
            op.remove(old)


def Doc_unit(root, key):
    for k, e, p in units_of(root):
        if k == key:
            return e, p
    return None, None


def unit_svg(doc, key):
    """one unit alone as a small SVG (conflict copies)"""
    import xml.etree.ElementTree as ET
    r = ET.Element(SVGNS + "svg")
    for k in ("viewBox", "width", "height"):
        if doc.root.get(k):
            r.set(k, doc.root.get(k))
    tmp = Composer(Doc(to_bytes(r)))
    el, _ = doc.unit(key)
    if el is not None:
        tmp.root.append(tmp.localize(doc, el, doc.who or "x"))
    return to_bytes(tmp.root)


# =====================================================================================================  merge
def merge(master_data, state, people, me, now, seed_data=None):
    """master_data: bytes or None; state: dict; people: {name: (bytes, info)}; returns
    (master bytes, new state, conflicts [(key, who, bytes)], notes [str], changes [(key, who, at)])"""
    notes, conflicts, changes = [], [], []
    state = copy.deepcopy(state or {})
    seen = state.setdefault("seen", {})
    reg = state.setdefault("units", {})
    docs = dict((p, Doc(d, p)) for p, (d, info) in people.items() if d)
    if master_data:
        base = Doc(master_data, "master")
    elif me in docs:
        base = Doc(people[me][0], me)
        notes.append(u"first run: the master starts as %s's file" % me)
    elif docs:
        p0 = sorted(docs)[0]
        base = Doc(people[p0][0], p0)
    else:
        raise RuntimeError("nothing to merge: no file in the cloud and no Data/shared/my_masterplan.svg")
    if not master_data:
        for k in base.hash:
            reg[k] = {"hash": base.hash[k], "by": base.who, "at": people.get(base.who, (None, {}))[1].get("saved", now)}
    mh = dict(base.hash)
    comp = Composer(base)
    order = [k for k, e, p in base.units]
    for p in sorted(docs):
        for k, e, par in docs[p].units:
            if k not in order:
                order.append(k)
    # who changed what since their last merge
    cand, stale = {}, set()
    for p, d in docs.items():
        info = people[p][1] or {}
        sp = seen.get(p, {})
        for k in set(d.hash) | set(sp):
            h = d.hash.get(k)
            if h == sp.get(k) or h == mh.get(k):
                continue
            if h is None and k not in mh:
                continue
            at = (info.get("rhino_units") or {}).get(k) or info.get("saved") or now
            cand.setdefault(k, []).append((at, p, h))
            if sp.get(k) != mh.get(k) and k in mh:
                stale.add(k)                        # edited on an older copy: the master's newer version competes
    for k in order + [x for x in cand if x not in order]:
        if k not in cand:
            continue
        cs = list(cand[k])
        if k in stale:
            r0 = reg.get(k) or {}
            cs.append((r0.get("at") or "", "master (%s)" % r0.get("by", "?"), mh[k]))
        cs.sort(reverse=True)                       # newest edit date first
        at, who, h = cs[0]
        if who.startswith("master ("):
            pass                                    # the master's version is the newest: stays
        elif h is None:
            comp.remove(k)
            mh.pop(k, None)
            reg[k] = {"hash": None, "by": who, "at": at, "deleted": True}
            changes.append((k, who, at, "deleted"))
        else:
            hint = [x for x in order[order.index(k) + 1:]] if k in order else []
            comp.put(k, docs[who], who, hint)
            mh[k] = h
            reg[k] = {"hash": h, "by": who, "at": at}
            changes.append((k, who, at, "changed"))
        for at2, who2, h2 in cs[1:]:
            if h2 == h:
                continue
            notes.append(u"FLAG conflict: '%s' was edited by %s (%s) and %s (%s): %s's newer edit is in the master, "
                         u"%s's is saved in master/conflicts/" % (k, who, short(at), who2, short(at2), who, who2))
            if h2 is not None:
                if who2.startswith("master ("):
                    conflicts.append((k, who2[8:-1] + "_was_master", unit_svg(base, k)))
                else:
                    conflicts.append((k, who2, unit_svg(docs[who2], k)))
    # planting areas (hidden) from the seed, once
    if seed_data and not any(k.startswith("planting_area_") for k in mh):
        sd = Doc(seed_data, "seed")
        hint_keys = [k for k in order if k.lower().startswith(("trees", "planting", "people"))]
        for k, e, par in sd.units:
            if not k.startswith("planting_area_"):
                continue
            el = comp.localize(sd, e, "seed")
            el.set("style", (el.get("style") + ";" if el.get("style") else "") + "display:none")
            tgt = None
            for ch in comp.root:
                if local(ch.tag) == "g" and re.match(r"^Layer_\d+$", gid(ch) or "") and \
                        len([c for c in ch if local(c.tag) == "g"]) >= 2:
                    tgt = ch
                    break
            tgt = tgt if tgt is not None else comp.root
            pos = len(list(tgt))
            for hk in hint_keys:
                o2, p2 = Doc_unit(comp.root, hk)
                if o2 is not None and p2 is tgt:
                    pos = list(tgt).index(o2)
                    break
            tgt.insert(pos, el)
            changes.append((k, "seed", now, "added (hidden)"))
        notes.append(u"planting areas added from the seed (hidden; layers proposal_planting_<species>)")
    out = to_bytes(comp.root)
    final = Doc(out, "master")
    for k, h in final.hash.items():                 # the register follows the final hashes (renamed defs etc.)
        r = reg.setdefault(k, {"by": "?", "at": now})
        r["hash"] = h
    for p, d in docs.items():
        seen[p] = dict(d.hash)
    seen[me] = dict(final.hash)                     # my file becomes the master
    state["updated"] = now
    state["by"] = me
    return out, state, conflicts, notes, changes


# =====================================================================================================  Rhino -> SVG
def inv(m):
    a, b, c, d, e, f = m
    det = a * d - b * c
    return (d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det)


def mmul(a, b):
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def mpt(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def hexcol(c):
    return "#%02X%02X%02X" % (c.R, c.G, c.B)


def obj_sig(o):
    import Rhino
    try:
        if isinstance(o, Rhino.DocObjects.InstanceObject):
            x = o.InstanceXform
            return u"I%.3f,%.3f" % (x.M03, x.M13)
        g = o.Geometry
        if isinstance(g, Rhino.Geometry.TextEntity):
            p = g.Plane.Origin
            return u"T%.3f,%.3f" % (p.X, p.Y)
        c = g.GetBoundingBox(True).Center
        return u"%.3f,%.3f" % (c.X, c.Y)
    except Exception:
        return u"?"


def rhino_edits(doc, my, notes):
    """units of my file that were changed in Rhino since the last bake -> rebuilt from the Rhino objects.
    Returns (new my bytes or None, {unit: time})"""
    import Rhino
    import xml.etree.ElementTree as ET
    try:
        mx = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_matrix") or "null")
        ucount = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_unit_count") or "{}")
        lunit = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_layer_unit") or "{}")
    except Exception:
        mx = None
    if not mx:
        notes.append(u"Rhino edits: none read (the plan was not baked with PlanToRhino v2 in this file yet)")
        return None, {}
    Mi = inv(tuple(mx["M"]))
    s_m, u = float(mx["s_m"]), float(mx["u"]) or 1.0
    root_ix = doc.Layers.FindByFullPath(ROOT_LAYER, -1)
    if root_ix < 0:
        return None, {}
    es = Rhino.DocObjects.ObjectEnumeratorSettings()
    es.HiddenObjects = True
    es.LockedObjects = True
    by_unit, changed = {}, set()
    for o in doc.Objects.GetObjectList(es):
        lay = doc.Layers[o.Attributes.LayerIndex]
        fp = lay.FullPath
        if not fp.startswith(ROOT_LAYER + "::"):
            continue
        sub = fp[len(ROOT_LAYER) + 2:]
        if sub.startswith(SKIP_LAYERS):
            continue
        un = o.Attributes.GetUserString(UNIT_KEY) or lunit.get(fp) or sub.split("::")[-1]
        by_unit.setdefault(un, []).append(o)
        st = o.Attributes.GetUserString(STAMP)
        if not st or st != obj_sig(o):
            changed.add(un)
    for un, n in ucount.items():
        if len(by_unit.get(un, [])) != n:
            changed.add(un)
    if not changed:
        notes.append(u"Rhino edits: none")
        return None, {}
    d = Doc(my, "me")
    t = now_iso()
    done = {}
    syms = {}                                         # symbol id -> (x, y, w, h) of a <use> in my file
    for el in d.root.iter(SVGNS + "use"):
        ref = (el.get(XLINK) or el.get("href") or "").lstrip("#")
        if ref and ref not in syms:
            syms[ref] = tuple(float(el.get(k) or 0) for k in ("x", "y", "width", "height"))

    def P(pt):
        return mpt(Mi, (pt.X / u, pt.Y / u))

    def path_d(crv):
        out = []
        try:
            ok, pl = crv.TryGetPolyline()
        except Exception:
            ok = False
        if ok:
            Q = [P(p) for p in pl]
            out.append("M%.2f,%.2f" % Q[0] + "".join("L%.2f,%.2f" % q for q in Q[1:]))
            if crv.IsClosed:
                out.append("Z")
            return "".join(out)
        bz = None
        try:
            bz = Rhino.Geometry.BezierCurve.CreateCubicBeziers(crv, 0.01, 0.01)
        except Exception:
            bz = None
        if bz:
            p0 = P(bz[0].GetControlVertex3d(0))
            out.append("M%.2f,%.2f" % p0)
            for b in bz:
                q = [P(b.GetControlVertex3d(i)) for i in (1, 2, 3)]
                out.append("C%.2f,%.2f %.2f,%.2f %.2f,%.2f" % (q[0] + q[1] + q[2]))
        else:
            pl = crv.ToPolyline(0.01, 1.0, 0.0, 0.0).ToPolyline() if hasattr(crv, "ToPolyline") else None
            if pl is None:
                return ""
            Q = [P(p) for p in pl]
            out.append("M%.2f,%.2f" % Q[0] + "".join("L%.2f,%.2f" % q for q in Q[1:]))
        if crv.IsClosed:
            out.append("Z")
        return "".join(out)

    def colour(o):
        a = o.Attributes
        try:
            if a.ColorSource == Rhino.DocObjects.ObjectColorSource.ColorFromObject:
                return hexcol(a.ObjectColor)
        except Exception:
            pass
        return hexcol(doc.Layers[a.LayerIndex].Color)

    def element(o, n_skip):
        g = o.Geometry
        a = o.Attributes
        if isinstance(o, Rhino.DocObjects.InstanceObject):
            idf = o.InstanceDefinition
            desc = idf.Description or ""
            ref = desc.split("SVG symbol ", 1)[1].strip() if "SVG symbol " in desc else None
            x = o.InstanceXform
            xm = (x.M00 / u, x.M10 / u, x.M01 / u, x.M11 / u, x.M03 / u, x.M13 / u)
            if ref and ref in d.ids:
                m = mmul(Mi, mmul(xm, (1.0, 0.0, 0.0, -1.0, 0.0, 0.0)))
                sx, sy, sw, sh = syms.get(ref, (0.0, 0.0, 0.0, 0.0))
                vb = [float(v) for v in _NUM.findall(d.ids[ref].get("viewBox") or "")]
                if len(vb) == 4 and vb[2] > 0 and vb[3] > 0:
                    w_ = sw or vb[2]
                    h_ = sh or vb[3]
                    s = min(w_ / vb[2], h_ / vb[3])
                    V = (s, 0.0, 0.0, s, -vb[0] * s + (w_ - vb[2] * s) / 2.0, -vb[1] * s + (h_ - vb[3] * s) / 2.0)
                else:
                    V, w_, h_ = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0), sw, sh
                T = mmul(m, inv(mmul((1.0, 0.0, 0.0, 1.0, sx, sy), V)))
                e = ET.Element(SVGNS + "use")
                if a.Name:
                    e.set("id", a.Name)
                if sw or sh:
                    e.set("x", "%g" % sx)
                    e.set("y", "%g" % sy)
                    e.set("width", "%g" % w_)
                    e.set("height", "%g" % h_)
                e.set(XLINK, "#" + ref)
                e.set("transform", "matrix(%.6f %.6f %.6f %.6f %.3f %.3f)" % T)
                return [e]
            n_skip["blocks not from the plan (written as their pieces)"] = \
                n_skip.get("blocks not from the plan (written as their pieces)", 0) + 1
            out = []
            for so in idf.GetObjects():
                g2 = so.Geometry.Duplicate()
                g2.Transform(x)
                out += geom_el(g2, so.Attributes, colour(o), n_skip)
            return out
        return geom_el(g, a, colour(o), n_skip)

    def geom_el(g, a, col, n_skip):
        if isinstance(g, Rhino.Geometry.Hatch):
            ds = [path_d(c) for c in list(g.Get3dCurves(True)) + list(g.Get3dCurves(False))]
            e = ET.Element(SVGNS + "path")
            e.set("d", " ".join(x for x in ds if x))
            e.set("style", "fill:%s;fill-rule:evenodd;stroke:none" % col)
            return [e]
        if isinstance(g, Rhino.Geometry.TextEntity):
            p0 = g.Plane.Origin
            p1 = p0 + g.Plane.XAxis
            q0, q1 = P(p0), P(p1)
            ang = math.degrees(math.atan2(q1[1] - q0[1], q1[0] - q0[0]))
            size = g.TextHeight / (s_m * u * CAP)
            e = ET.Element(SVGNS + "text")
            e.set("x", "%.2f" % q0[0])
            e.set("y", "%.2f" % q0[1])
            try:
                fam = g.Font.FamilyName
                bold = g.Font.Bold
            except Exception:
                fam, bold = "Arial", False
            try:
                al = str(g.TextHorizontalAlignment)
            except Exception:
                al = "Left"
            anc = "middle" if "Center" in al else ("end" if "Right" in al else "start")
            e.set("style", "font-family:%s;font-size:%.2fpx;%sfill:%s;text-anchor:%s" %
                  (fam, size, "font-weight:bold;" if bold else "", col, anc))
            if abs(ang) > 0.05:
                e.set("transform", "rotate(%.3f %.2f %.2f)" % (ang, q0[0], q0[1]))
            e.text = g.PlainText if hasattr(g, "PlainText") else g.Text
            return [e]
        if isinstance(g, Rhino.Geometry.Curve):
            e = ET.Element(SVGNS + "path")
            e.set("d", path_d(g))
            try:
                lw = a.PlotWeight / s_m if a.PlotWeight > 0 else 1.0
            except Exception:
                lw = 1.0
            e.set("style", "fill:none;stroke:%s;stroke-width:%.3f" % (col, lw))
            return [e]
        k = type(g).__name__
        n_skip[k] = n_skip.get(k, 0) + 1
        return []

    n_skip = {}
    for un in sorted(changed):
        old, par = d.unit(ukey(un))
        g = ET.Element(SVGNS + "g")
        g.set("id", gid(old) if old is not None else re.sub(r"[^A-Za-z0-9_]+", "_", un))
        if old is not None:
            for k in ("style", "opacity", "display", "clip-path", "class"):
                if old.get(k) is not None:
                    g.set(k, old.get(k))
            for im in old.iter():                     # pictures stay as they were (Rhino does not write them back)
                if local(im.tag) == "image":
                    g.append(copy.deepcopy(im))
        objs = sorted(by_unit.get(un, []), key=lambda o: getattr(o.Attributes, "DisplayOrder", 0))
        sub = {}
        for o in objs:
            if isinstance(o.Geometry, Rhino.Geometry.PictureFrame) if hasattr(Rhino.Geometry, "PictureFrame") else False:
                continue
            els = element(o, n_skip)
            grps = list(o.Attributes.GetGroupList() or []) if o.Attributes.GroupCount else []
            tgt = g
            if grps:
                if grps[0] not in sub:
                    sub[grps[0]] = ET.SubElement(g, SVGNS + "g")
                tgt = sub[grps[0]]
            for e in els:
                tgt.append(e)
        if old is not None:
            i = list(par).index(old)
            par.remove(old)
            par.insert(i, g)
        else:
            lay1 = next((c for c in d.root if local(c.tag) == "g" and re.match(r"^Layer_\d+$", gid(c) or "")), d.root)
            lay1.append(g)
        done[ukey(un)] = t
    if n_skip:
        notes.append(u"Rhino edits: not written back: " + u", ".join(u"%s %d" % kv for kv in sorted(n_skip.items())))
    notes.append(u"Rhino edits written into your file: " + u", ".join(sorted(done)))
    return to_bytes(d.root), done


def stamp_layers(doc, reg, notes):
    """each Rhino layer under masterplan gets its group's edit date + editor (layer user text)"""
    try:
        lunit = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_layer_unit") or "{}")
    except Exception:
        lunit = {}
    n = 0
    for l in doc.Layers:
        if l.IsDeleted or not l.FullPath.startswith(ROOT_LAYER + "::"):
            continue
        un = lunit.get(l.FullPath)
        r = reg.get(ukey(un)) if un else None
        if not r:
            continue
        try:
            l.SetUserString("edited", r.get("at", ""))
            l.SetUserString("edited_by", r.get("by", ""))
            n += 1
        except Exception:
            pass
    return n


# =====================================================================================================  main
def read_local():
    try:
        return json.load(open(LOCAL_STATE, encoding="utf-8"))
    except Exception:
        return {}


def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


class LiveNotes(list):
    """the log written to disk after every step (Bergama.bat runs hidden: the file is the window)"""

    def __init__(self, head=u""):
        list.__init__(self)
        self.head = head

    def append(self, x):
        list.append(self, x)
        write_log(self.head + u"\n".join(self))

    def __iadd__(self, xs):
        for x in xs:
            self.append(x)
        return self


def main(gh=None, doc=None, me=None, notes=None):
    t0 = time.time()
    notes = notes if notes is not None else []
    notes.append(u"%s %s · %s" % (GH_LABEL, VERSION, time.strftime("%Y-%m-%d %H:%M")))
    if gh is None:
        token, me = read_settings()
        gh = GitHub(token)
    notes.append(u"you: %s · cloud: github.com/%s, branch %s, folder %s/" % (me, REPO, BRANCH, CLOUD))
    os.makedirs(CLOUD_COPY, exist_ok=True)
    loc = read_local()
    pme = "%s/people/%s/masterplan.svg" % (CLOUD, me)
    pinfo = "%s/people/%s/info.json" % (CLOUD, me)
    pm, ps = "%s/master/masterplan_latest.svg" % CLOUD, "%s/master/state.json" % CLOUD
    pplace = "%s/master/placing.json" % CLOUD
    placing = None
    if doc is not None:
        try:
            v = doc.Strings.GetValue(PTR_KEY, "v2_matrix")
            placing = v.encode("utf-8") if v else None
        except Exception:
            placing = None
    head = gh.head()
    files, base_tree = gh.tree(head)
    # 0 my file: the first time it comes from the cloud (master), else from the newest plan SVG
    if not os.path.isfile(MY_FILE):
        src = pm if pm in files else (pme if pme in files else None)
        if src:
            write_file(MY_FILE, gh.blob(files[src]))
            notes.append(u"your file made from the cloud copy %s" % src)
        else:
            try:
                fs = [os.path.join(PLAN_DIR, f) for f in os.listdir(PLAN_DIR) if f.lower().endswith(".svg")]
            except Exception:
                fs = []
            if not fs:
                raise RuntimeError("no plan to start from: put your plan SVG in %s or %s" % (PLAN_DIR, MY_FILE))
            newest = max(fs, key=os.path.getmtime)
            write_file(MY_FILE, open(newest, "rb").read())
            notes.append(u"your file made from %s" % newest)
    my = open(MY_FILE, "rb").read()
    saved = now_iso(os.path.getmtime(MY_FILE))
    # 1 Rhino edits into my file
    rhino_units = {}
    if doc is not None:
        new, rhino_units = rhino_edits(doc, my, notes)
        if new is not None:
            write_file(MY_FILE + ".before_rhino.svg", my)
            write_file(MY_FILE, new)
            my = new
    # 2 upload my file (only if it changed)
    if files.get(pme) != git_sha(my):
        info = {"saved": saved, "by": me, "rhino_units": rhino_units, "uploaded": now_iso()}
        try:
            head = gh.commit(head, base_tree, {pme: my, pinfo: json.dumps(info, indent=1).encode("utf-8")},
                             u"%s: upload (Illustrator file saved %s%s)" % (me, short(saved),
                                                                           ", Rhino edits: " + ", ".join(sorted(rhino_units)) if rhino_units else ""))
        except Retry:
            head = gh.head()
            files, base_tree = gh.tree(head)
            head = gh.commit(head, base_tree, {pme: my, pinfo: json.dumps(info, indent=1).encode("utf-8")},
                             u"%s: upload" % me)
        notes.append(u"1 uploaded your file (%.1f MB, saved %s)" % (len(my) / 1048576.0, short(saved)))
    else:
        notes.append(u"1 your file is unchanged since your last upload")
    # 3-5 download, merge, commit (again from the start if somebody committed meanwhile)
    for attempt in range(4):
        head = gh.head()
        files, base_tree = gh.tree(head)
        people, got = {}, []
        for p in PEOPLE:
            f = "%s/people/%s/masterplan.svg" % (CLOUD, p)
            if f not in files:
                continue
            cp = os.path.join(CLOUD_COPY, p + ".svg")
            data = open(cp, "rb").read() if os.path.isfile(cp) else None
            if data is None or git_sha(data) != files[f]:
                data = gh.blob(files[f])
                write_file(cp, data)
                got.append(p)
            fi = "%s/people/%s/info.json" % (CLOUD, p)
            info = json.loads(gh.blob(files[fi]).decode("utf-8")) if fi in files else {}
            people[p] = (data, info)
        master = None
        if pm in files:
            cp = os.path.join(CLOUD_COPY, "master.svg")
            master = open(cp, "rb").read() if os.path.isfile(cp) else None
            if master is None or git_sha(master) != files[pm]:
                master = gh.blob(files[pm])
                write_file(cp, master)
                got.append("master")
        state = json.loads(gh.blob(files[ps]).decode("utf-8")) if ps in files else {}
        notes.append(u"2 downloaded from the cloud: %s (the others were already here, same content)" %
                     (u", ".join(got) or u"nothing new"))
        seed = open(SEED_FILE, "rb").read() if os.path.isfile(SEED_FILE) else None
        if seed is None:
            notes.append(u"FLAG no %s: planting areas cannot be added" % SEED_FILE)
        now = now_iso()
        out, state2, conflicts, mnotes, changes = merge(master, state, people, me, now, seed)
        put = {}
        if placing and files.get(pplace) != git_sha(placing):
            put[pplace] = placing                     # survey placing for the AutoCAD DXF (from PlanToRhino v2)
        if master is None or git_sha(out) != git_sha(master):
            put[pm] = out
            put[pme] = out
            put[ps] = json.dumps(state2, indent=1, sort_keys=True).encode("utf-8")
            stamp_ = time.strftime("%Y%m%d_%H%M")
            for k, who, data in conflicts:
                put["%s/master/conflicts/%s_%s_%s.svg" % (CLOUD, re.sub(r"[^A-Za-z0-9_]+", "_", k), who, stamp_)] = data
            try:
                gh.commit(head, base_tree, put, u"%s: merge · %s" % (
                    me, u", ".join(u"%s by %s" % (k, w) for k, w, a, s in changes[:12]) or u"no layer changes"))
            except Retry:
                notes.append(u"somebody else uploaded at the same moment: merging again")
                continue
        elif put:
            try:
                gh.commit(head, base_tree, put, u"%s: survey placing" % me)
            except Retry:
                continue
        break
    else:
        raise RuntimeError("the cloud kept changing during 4 merges: run again")
    notes += mnotes
    if changes:
        notes.append(u"3 merged into the master:")
        for k, w, a, s in changes:
            notes.append(u"   %-40s %s by %s, edited %s" % (k, s, w, short(a)))
    else:
        notes.append(u"3 merged: no layer changed")
    # 6 local copies (conflicts too: Data/shared/conflicts/, the same files as in the cloud)
    for pth, data in put.items():
        if "/master/conflicts/" in pth:
            write_file(os.path.join(SH_DIR, "conflicts", pth.rsplit("/", 1)[1]), data)
    if conflicts:
        notes.append(u"conflict copies saved in the cloud (%s/master/conflicts/) and in %s" %
                     (CLOUD, os.path.join(SH_DIR, "conflicts")))
    write_file(os.path.join(CLOUD_COPY, "master.svg"), out)
    write_file(MY_FILE + ".prev.svg", my)
    write_file(MY_FILE, out)
    write_file(os.path.join(PLAN_DIR, "masterplan_latest.svg"), out)
    os.utime(os.path.join(PLAN_DIR, "masterplan_latest.svg"), None)
    loc.update(last_run=now_iso(), master_sha=git_sha(out))
    write_file(LOCAL_STATE, json.dumps(loc, indent=1).encode("utf-8"))
    notes.append(u"4 the master is in %s and your file %s is now the master (your previous file: .prev.svg); "
                 u"reopen it in Illustrator" % (os.path.join(PLAN_DIR, "masterplan_latest.svg"), MY_FILE))
    if doc is not None:
        try:
            doc.Strings.SetString(SYNC_KEY, "rebake_all", "1")    # PlanToRhino v2 bakes every layer fresh
            n = stamp_layers(doc, state2.get("units", {}), notes)
            notes.append(u"edit dates written on %d Rhino layers (layer user text 'edited', 'edited_by')" % n)
        except Exception as ex:
            notes.append(u"FLAG Rhino flags not set: %s" % ex)
    # layer register + history
    notes.append(u"layer edit dates (newest first):")
    reg = sorted(state2.get("units", {}).items(), key=lambda kv: kv[1].get("at", ""), reverse=True)
    for k, r in reg:
        if r.get("hash") is None and not r.get("deleted"):
            continue
        notes.append(u"   %-40s %s · %s%s" % (k, short(r.get("at", "")), r.get("by", "?"), u" (deleted)" if r.get("deleted") else u""))
    try:
        hist = gh.history(pm)
        notes.append(u"last %d versions of the master (restore one on github.com > branch shared > History):" % len(hist))
        for dt, msg, sha in hist:
            notes.append(u"   %s %s %s" % (sha, dt[:16].replace("T", " "), msg[:90]))
    except Exception as ex:
        notes.append(u"history not read: %s" % ex)
    notes.append(u"%.1f s" % (time.time() - t0))
    return u"\n".join(notes)


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


def done_text(ran, ok, secs):
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


# =====================================================================================================  DXF (AutoCAD)
mat_mul, mat_pt, ID = mmul, mpt, (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
DXF_TEMPLATE = """
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
BJTa+rAaSSJfOf8Bcdgxeg==
"""


def dxf_template():
    import zlib
    return zlib.decompress(base64.b64decode("".join(DXF_TEMPLATE.split()))).decode("utf-8")


def parse_transform(s):
    m = ID
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in _NUM.findall(args)]
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate":
            t = (1.0, 0.0, 0.0, 1.0, v[0], v[1] if len(v) > 1 else 0.0)
        elif name == "scale":
            t = (v[0], 0.0, 0.0, v[1] if len(v) > 1 else v[0], 0.0, 0.0)
        elif name == "rotate":
            a = math.radians(v[0])
            r = (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0.0, 0.0)
            t = mmul((1.0, 0.0, 0.0, 1.0, v[1], v[2]), mmul(r, (1.0, 0.0, 0.0, 1.0, -v[1], -v[2]))) if len(v) == 3 else r
        else:
            continue
        m = mmul(m, t)
    return m


def parse_color(v):
    if not v:
        return None
    v = v.strip().lower()
    if v in ("none", "transparent") or v.startswith("url("):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except Exception:
            return None
    if v.startswith("rgb"):
        n = [float(x) for x in _NUM.findall(v)[:3]]
        return tuple(int(round(max(0, min(255, x)))) for x in n) if len(n) == 3 else None
    return {"black": (0, 0, 0), "white": (255, 255, 255)}.get(v)


def first_num(v, dflt):
    m = _NUM.search(v or "")
    return float(m.group(0)) if m else dflt


def path_segs(d):
    """SVG path data -> [(closed, start, [('L', p) | ('C', c1, c2, p)])]: curves kept exact (cubic Beziers)"""
    toks = re.findall(r"[MmZzLlHhVvCcSsQqTtAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d or "")
    subs, cur, pos, start = [], None, (0.0, 0.0), (0.0, 0.0)
    i, cmd, lc, lq = 0, None, None, None

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                if cur is not None:
                    subs.append((True, start, cur))
                cur, pos, lc, lq = None, start, None, None
                continue
        elif cmd is None:
            i += 1
            continue
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = pos if rel else (0.0, 0.0)
        try:
            if c == "M":
                p = (num() + ox, num() + oy)
                if cur:
                    subs.append((False, start, cur))
                cur, pos, start, lc, lq = [], p, p, None, None
                cmd = "l" if rel else "L"
                continue
            if cur is None:
                cur, start = [], pos
            if c == "L":
                p = (num() + ox, num() + oy)
                cur.append(("L", p))
                pos, lc, lq = p, None, None
            elif c == "H":
                p = (num() + (pos[0] if rel else 0.0), pos[1])
                cur.append(("L", p))
                pos, lc, lq = p, None, None
            elif c == "V":
                p = (pos[0], num() + (pos[1] if rel else 0.0))
                cur.append(("L", p))
                pos, lc, lq = p, None, None
            elif c in "CS":
                if c == "C":
                    c1 = (num() + ox, num() + oy)
                else:
                    c1 = (2 * pos[0] - lc[0], 2 * pos[1] - lc[1]) if lc else pos
                c2 = (num() + ox, num() + oy)
                p = (num() + ox, num() + oy)
                cur.append(("C", c1, c2, p))
                pos, lc, lq = p, c2, None
            elif c in "QT":
                if c == "Q":
                    q = (num() + ox, num() + oy)
                else:
                    q = (2 * pos[0] - lq[0], 2 * pos[1] - lq[1]) if lq else pos
                p = (num() + ox, num() + oy)
                cur.append(("C", (pos[0] + 2 * (q[0] - pos[0]) / 3, pos[1] + 2 * (q[1] - pos[1]) / 3),
                            (p[0] + 2 * (q[0] - p[0]) / 3, p[1] + 2 * (q[1] - p[1]) / 3), p))
                pos, lc, lq = p, None, q
            elif c == "A":
                rx, ry, rot, fa, fs = num(), num(), num(), num(), num()
                p = (num() + ox, num() + oy)
                cur += arc_segs(pos, rx, ry, rot, fa, fs, p)
                pos, lc, lq = p, None, None
            else:
                i += 1
        except (IndexError, ValueError):
            break
    if cur:
        subs.append((False, start, cur))
    return subs


def arc_segs(p0, rx, ry, rot, fa, fs, p1):
    """SVG elliptical arc -> cubic Beziers (SVG spec F.6 end-point to centre conversion)"""
    rx, ry = abs(rx), abs(ry)
    if rx < 1e-12 or ry < 1e-12 or p0 == p1:
        return [("L", p1)]
    ph = math.radians(rot)
    cp, sp = math.cos(ph), math.sin(ph)
    dx, dy = (p0[0] - p1[0]) / 2.0, (p0[1] - p1[1]) / 2.0
    x1, y1 = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = x1 * x1 / (rx * rx) + y1 * y1 / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num_ = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    co = math.sqrt(max(0.0, num_ / (rx * rx * y1 * y1 + ry * ry * x1 * x1)))
    if bool(fa) == bool(fs):
        co = -co
    cx1, cy1 = co * rx * y1 / ry, -co * ry * x1 / rx
    cx, cy = cp * cx1 - sp * cy1 + (p0[0] + p1[0]) / 2.0, sp * cx1 + cp * cy1 + (p0[1] + p1[1]) / 2.0
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1.0, 0.0, (x1 - cx1) / rx, (y1 - cy1) / ry)
    dt = ang((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2) - 1e-9)))
    h = dt / n
    k = 4.0 / 3.0 * math.tan(h / 4.0)
    pt = lambda a: (cx + rx * math.cos(a) * cp - ry * math.sin(a) * sp, cy + rx * math.cos(a) * sp + ry * math.sin(a) * cp)
    dr = lambda a: (-rx * math.sin(a) * cp - ry * math.cos(a) * sp, -rx * math.sin(a) * sp + ry * math.cos(a) * cp)
    out = []
    for j in range(n):
        a0, a1 = t1 + j * h, t1 + (j + 1) * h
        q0, q1, d0, d1 = pt(a0), pt(a1), dr(a0), dr(a1)
        out.append(("C", (q0[0] + k * d0[0], q0[1] + k * d0[1]), (q1[0] - k * d1[0], q1[1] - k * d1[1]),
                    p1 if j == n - 1 else q1))
    return out


def shape_segs(tag, el):
    g = lambda k: first_num(el.get(k), 0.0)
    L = lambda P, cl: [(cl, P[0], [("L", p) for p in P[1:]])]
    if tag == "path":
        return path_segs(el.get("d"))
    if tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        return L([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], True) if w > 0 and h > 0 else []
    if tag in ("circle", "ellipse"):
        cx, cy = g("cx"), g("cy")
        rx = g("r") if tag == "circle" else g("rx")
        ry = g("r") if tag == "circle" else g("ry")
        if rx <= 0 or ry <= 0:
            return []
        k = 0.5522847498
        P = [(cx + rx, cy), (cx, cy + ry), (cx - rx, cy), (cx, cy - ry)]
        T = [(0, ry), (-rx, 0), (0, -ry), (rx, 0)]
        segs = []
        for j in range(4):
            a, b = P[j], P[(j + 1) % 4]
            ta, tb = T[j], T[(j + 1) % 4]
            segs.append(("C", (a[0] + k * ta[0], a[1] + k * ta[1]), (b[0] - k * tb[0], b[1] - k * tb[1]), b))
        return [(True, P[0], segs)]
    if tag == "line":
        return L([(g("x1"), g("y1")), (g("x2"), g("y2"))], False)
    if tag in ("polygon", "polyline"):
        v = [float(x) for x in _NUM.findall(el.get("points") or "")]
        P = list(zip(v[0::2], v[1::2]))
        return L(P, tag == "polygon") if len(P) >= 2 else []
    return []


def segs_map(m, sub):
    cl, st, segs = sub
    return (cl, mpt(m, st), [tuple([s[0]] + [mpt(m, p) for p in s[1:]]) for s in segs])


def segs_flat(sub, n=8):
    cl, p0, segs = sub
    P = [p0]
    for s in segs:
        if s[0] == "L":
            P.append(s[1])
        else:
            a, c1, c2, b = P[-1], s[1], s[2], s[3]
            for k in range(1, n + 1):
                t = k / float(n)
                u = 1 - t
                P.append((u * u * u * a[0] + 3 * t * u * u * c1[0] + 3 * t * t * u * c2[0] + t * t * t * b[0],
                          u * u * u * a[1] + 3 * t * u * u * c1[1] + 3 * t * t * u * c2[1] + t * t * t * b[1]))
    return P


def path_points(d):
    """SVG path data -> [(closed, [points])], curves flattened (8 pieces per curve)"""
    return [(s[0], segs_flat(s)) for s in path_segs(d)]


# ---- clipping (Illustrator clip groups) ----
def poly_orient(C):
    a = 0.0
    for i in range(len(C)):
        x0, y0 = C[i - 1]
        x1, y1 = C[i]
        a += x0 * y1 - x1 * y0
    return 1.0 if a > 0 else -1.0


def is_convex(C):
    if len(C) < 3:
        return False
    sg = 0
    n = len(C)
    for i in range(n):
        a, b, c = C[i - 2], C[i - 1], C[i]
        z = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if abs(z) < 1e-12:
            continue
        s = 1 if z > 0 else -1
        if sg and s != sg:
            return False
        sg = s
    return True


def inside_c(C, o, p):
    for i in range(len(C)):
        a, b = C[i - 1], C[i]
        if o * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) < -1e-9:
            return False
    return True


def clip_ring_c(P, C, o):
    """Sutherland-Hodgman: closed ring P cut by the convex polygon C (orientation o)"""
    out = list(P)
    for i in range(len(C)):
        if not out:
            break
        a, b = C[i - 1], C[i]
        side = lambda p: o * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
        src, out = out, []
        for j in range(len(src)):
            p, q = src[j - 1], src[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
                out.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def clip_line_c(P, C, o):
    """Cyrus-Beck: open polyline P cut by the convex polygon C -> list of pieces"""
    pieces, cur = [], []
    for j in range(1, len(P)):
        p, q = P[j - 1], P[j]
        t0, t1 = 0.0, 1.0
        ok = True
        for i in range(len(C)):
            a, b = C[i - 1], C[i]
            nx, ny = -o * (b[1] - a[1]), o * (b[0] - a[0])
            num_ = nx * (p[0] - a[0]) + ny * (p[1] - a[1])
            den = nx * (q[0] - p[0]) + ny * (q[1] - p[1])
            if abs(den) < 1e-15:
                if num_ < 0:
                    ok = False
                    break
                continue
            t = -num_ / den
            if den > 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if cur:
                pieces.append(cur)
                cur = []
            continue
        a_ = (p[0] + t0 * (q[0] - p[0]), p[1] + t0 * (q[1] - p[1]))
        b_ = (p[0] + t1 * (q[0] - p[0]), p[1] + t1 * (q[1] - p[1]))
        if not cur or t0 > 1e-9:
            if cur:
                pieces.append(cur)
            cur = [a_]
        cur.append(b_)
        if t1 < 1 - 1e-9:
            pieces.append(cur)
            cur = []
    if cur:
        pieces.append(cur)
    return [x for x in pieces if len(x) >= 2]


def in_rings(R, p):
    """even-odd point in polygon (all rings of a clip outline)"""
    x, y = p
    c = False
    for P in R:
        n = len(P)
        for i in range(n):
            (x0, y0), (x1, y1) = P[i - 1], P[i]
            if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                c = not c
    return c


class EdgeGrid(object):
    """the edges of a clip outline in grid cells, to cut lines against a non-convex clip quickly"""

    def __init__(self, R):
        self.E = [(P[i - 1], P[i]) for P in R for i in range(len(P))]
        xs = [p[0] for P in R for p in P]
        ys = [p[1] for P in R for p in P]
        self.x0, self.y0 = min(xs), min(ys)
        self.cs = max(max(xs) - self.x0, max(ys) - self.y0, 1e-9) / max(1.0, math.sqrt(len(self.E)))
        self.cells = {}
        for k, (a, b) in enumerate(self.E):
            for c in self.span(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])):
                self.cells.setdefault(c, []).append(k)

    def span(self, ax, ay, bx, by):
        i0, i1 = int((ax - self.x0) // self.cs), int((bx - self.x0) // self.cs)
        j0, j1 = int((ay - self.y0) // self.cs), int((by - self.y0) // self.cs)
        if (i1 - i0 + 1) * (j1 - j0 + 1) > 4096:
            return [None]
        return [(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)]

    def cuts(self, p, q):
        ks = set()
        for c in self.span(min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1])):
            ks.update(range(len(self.E)) if c is None else self.cells.get(c, ()))
        ts = []
        dx, dy = q[0] - p[0], q[1] - p[1]
        for k in ks:
            a, b = self.E[k]
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
            u = ((a[0] - p[0]) * dy - (a[1] - p[1]) * dx) / den
            if 0 < t < 1 and 0 <= u <= 1:
                ts.append(t)
        return sorted(ts)


def clip_line_r(P, R, grid):
    """open polyline P cut by any clip outline R (even-odd) -> list of pieces"""
    pieces, cur = [], []
    for j in range(1, len(P)):
        p, q = P[j - 1], P[j]
        ts = [0.0] + grid.cuts(p, q) + [1.0]
        for a_, b_ in zip(ts[:-1], ts[1:]):
            if b_ - a_ < 1e-12:
                continue
            m = (a_ + b_) / 2.0
            pa = (p[0] + a_ * (q[0] - p[0]), p[1] + a_ * (q[1] - p[1]))
            pb = (p[0] + b_ * (q[0] - p[0]), p[1] + b_ * (q[1] - p[1]))
            if in_rings(R, (p[0] + m * (q[0] - p[0]), p[1] + m * (q[1] - p[1]))):
                if not cur:
                    cur = [pa]
                cur.append(pb)
            elif cur:
                pieces.append(cur)
                cur = []
    if cur:
        pieces.append(cur)
    return [x for x in pieces if len(x) >= 2]


def trapezoids(R):
    """any clip outline (rings, even-odd) -> convex pieces: horizontal slabs between its corner heights"""
    E = [(P[i - 1], P[i]) for P in R for i in range(len(P)) if P[i - 1][1] != P[i][1]]
    ys = sorted(set(p[1] for P in R for p in P))
    out = []
    for y0, y1 in zip(ys[:-1], ys[1:]):
        ym = (y0 + y1) / 2.0
        xs = []
        for a, b in E:
            if (a[1] > ym) != (b[1] > ym):
                fx = lambda y: a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                xs.append((fx(ym), fx(y0), fx(y1)))
        xs.sort()
        for l, r in zip(xs[0::2], xs[1::2]):
            T = [(l[1], y0), (r[1], y0), (r[2], y1), (l[2], y1)]
            if abs(r[1] - l[1]) + abs(r[2] - l[2]) > 1e-9:
                out.append((T, min(l[1], l[2]), max(r[1], r[2]), y0, y1))
    return out


def image_px_size(raw):
    """(width, height) in pixels of PNG / JPEG / GIF bytes, else None"""
    import struct
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", raw[16:24])
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", raw[6:10])
    if raw[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            mk = raw[i + 1]
            if mk in (0xD8, 0x01) or 0xD0 <= mk <= 0xD7:
                i += 2
                continue
            ln = struct.unpack(">H", raw[i + 2:i + 4])[0]
            if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                return (w, h)
            i += 2 + ln
    return None


class DXF(object):
    """an AutoCAD 2010 DXF (AC1024) built on a blank file made with ezdxf (embedded above): handles of the
    template: layer table 1, linetype table 2, block record table 9, *Model_Space 17, plot style 13, material 21,
    ACAD_IMAGE_DICT 30"""

    def __init__(self):
        self.tpl = dxf_template()
        self.h = 0x400
        self.layers, self.ents, self.blocks, self.ltypes, self.imgdefs = [], [], [], [], []
        self.lay_seen, self.lt_seen = set(), {}

    def hd(self):
        self.h += 1
        return "%X" % self.h

    def layer(self, name, off=False):
        name = re.sub(r"[<>/\\\":;?*|=`,]", "_", name)[:200]
        if name not in self.lay_seen:
            self.lay_seen.add(name)
            self.layers.append("0\nLAYER\n5\n%s\n330\n1\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n2\n%s\n70\n0\n"
                               "62\n%d\n6\nContinuous\n370\n-3\n390\n13\n347\n21" % (self.hd(), name, -7 if off else 7))
        return name

    def ltype(self, pattern):
        """a dash pattern (drawing units, dash, gap, dash, ...) -> linetype name"""
        pat = [round(abs(x), 4) for x in pattern if abs(x) > 1e-9]
        if len(pat) % 2:
            pat = pat * 2
        if len(pat) < 2:
            return None
        key = tuple(pat)
        if key not in self.lt_seen:
            nm = "BERGAMA_DASH_%d" % (len(self.lt_seen) + 1)
            self.lt_seen[key] = nm
            el = "".join("\n49\n%.4f\n74\n0" % (x if j % 2 == 0 else -x) for j, x in enumerate(pat))
            self.ltypes.append("0\nLTYPE\n5\n%s\n330\n2\n100\nAcDbSymbolTableRecord\n100\nAcDbLinetypeTableRecord\n2\n%s\n"
                               "70\n0\n3\n%s\n72\n65\n73\n%d\n40\n%.4f%s" %
                               (self.hd(), nm, " ".join("%.2f" % x for x in pat), len(pat), sum(pat), el))
        return self.lt_seen[key]

    def head(self, kind, owner, lay, c, op=None, lt=None):
        s = "0\n%s\n5\n%s\n330\n%s\n100\nAcDbEntity\n8\n%s" % (kind, self.hd(), owner, lay)
        if lt:
            s += "\n6\n" + lt
        if c is not None:
            s += "\n420\n%d" % (c[0] * 65536 + c[1] * 256 + c[2])
        if op is not None and op < 0.999:
            s += "\n440\n%d" % (0x02000000 | max(0, min(255, int(round(op * 255)))))
        return s

    def poly(self, out, owner, lay, P, closed_, c, op=None, lt=None):
        if len(P) < 2:
            return
        s = [self.head("LWPOLYLINE", owner, lay, c, op, lt) + "\n100\nAcDbPolyline\n90\n%d\n70\n%d" %
             (len(P), 1 if closed_ else 0)]
        s += ["10\n%.4f\n20\n%.4f" % p for p in P]
        out.append("\n".join(s))

    def spline(self, out, owner, lay, sub, c, op=None, lt=None):
        """one SVG subpath (lines + cubic Beziers) as one exact degree-3 SPLINE"""
        cl, p0, segs = sub
        if cl and segs and (abs(segs[-1][-1][0] - p0[0]) > 1e-9 or abs(segs[-1][-1][1] - p0[1]) > 1e-9):
            segs = segs + [("L", p0)]
        cp = [p0]
        for s in segs:
            a = cp[-1]
            if s[0] == "L":
                b = s[1]
                cp += [(a[0] + (b[0] - a[0]) / 3.0, a[1] + (b[1] - a[1]) / 3.0),
                       (a[0] + 2 * (b[0] - a[0]) / 3.0, a[1] + 2 * (b[1] - a[1]) / 3.0), b]
            else:
                cp += [s[1], s[2], s[3]]
        n = len(segs)
        if n < 1:
            return
        kn = [0] * 4 + [k for k in range(1, n) for _ in range(3)] + [n] * 4
        s = [self.head("SPLINE", owner, lay, c, op, lt) + "\n100\nAcDbSpline\n210\n0.0\n220\n0.0\n230\n1.0\n70\n%d\n71\n3\n"
             "72\n%d\n73\n%d\n74\n0\n42\n0.0000000001\n43\n0.0000000001" % (8 + (1 if cl else 0), len(kn), len(cp))]
        s += ["40\n%d" % k for k in kn]
        s += ["10\n%.4f\n20\n%.4f\n30\n0.0" % p for p in cp]
        out.append("\n".join(s))

    def hatch(self, out, owner, lay, loops, c, op=None):
        """loops: point lists (polyline boundary) or subpaths (closed, start, segs) kept as line + spline edges"""
        body = []
        for L in loops:
            if isinstance(L, tuple):
                cl, p0, segs = L
                if not segs:
                    continue
                if abs(segs[-1][-1][0] - p0[0]) > 1e-9 or abs(segs[-1][-1][1] - p0[1]) > 1e-9:
                    segs = segs + [("L", p0)]
                e = ["92\n1\n93\n%d" % len(segs)]
                a = p0
                for s in segs:
                    if s[0] == "L":
                        e.append("72\n1\n10\n%.4f\n20\n%.4f\n11\n%.4f\n21\n%.4f" % (a[0], a[1], s[1][0], s[1][1]))
                    else:
                        e.append("72\n4\n94\n3\n73\n0\n74\n0\n95\n8\n96\n4\n40\n0\n40\n0\n40\n0\n40\n0\n40\n1\n40\n1\n40\n1\n"
                                 "40\n1\n" + "\n".join("10\n%.4f\n20\n%.4f" % p for p in (a, s[1], s[2], s[3])) + "\n97\n0")
                    a = s[-1]
                e.append("97\n0")
                body.append("\n".join(e))
            elif len(L) >= 3:
                body.append("\n".join(["92\n3\n72\n0\n73\n1\n93\n%d" % len(L)] + ["10\n%.4f\n20\n%.4f" % p for p in L] +
                                      ["97\n0"]))
        if not body:
            return
        out.append("\n".join([self.head("HATCH", owner, lay, c, op) + "\n100\nAcDbHatch\n10\n0.0\n20\n0.0\n30\n0.0\n210\n0.0\n"
                              "220\n0.0\n230\n1.0\n2\nSOLID\n70\n1\n71\n0\n91\n%d" % len(body)] + body + ["75\n0\n76\n1\n98\n0"]))

    def text(self, out, owner, lay, p, h, txt, rot, c, align, op=None):
        txt = txt.replace("\n", " ")
        al = {"middle": 1, "end": 2}.get(align, 0)
        s = (self.head("TEXT", owner, lay, c, op) + "\n100\nAcDbText\n10\n%.4f\n20\n%.4f\n30\n0.0\n40\n%.4f\n"
             "1\n%s\n50\n%.4f\n72\n%d" % (p[0], p[1], h, txt, rot, al))
        if al:
            s += "\n11\n%.4f\n21\n%.4f\n31\n0.0" % p
        s += "\n100\nAcDbText\n73\n0"
        out.append(s)

    def insert(self, out, owner, lay, name, m):
        sx = math.hypot(m[0], m[1])
        rot = math.degrees(math.atan2(m[1], m[0]))
        sy = (m[0] * m[3] - m[1] * m[2]) / sx if sx else 1.0
        out.append(self.head("INSERT", owner, lay, None) + "\n100\nAcDbBlockReference\n2\n%s\n10\n%.4f\n20\n%.4f\n"
                   "30\n0.0\n41\n%.6f\n42\n%.6f\n43\n1.0\n50\n%.4f" % (name, m[4], m[5], sx, sy, rot))

    def imagedef(self, fname, w, h):
        dh = self.hd()
        self.imgdefs.append([dh, fname, w, h, []])
        return len(self.imgdefs) - 1

    def image(self, out, owner, lay, di, ins, u, v, clip_px=None, op=None):
        idf = self.imgdefs[di]
        eh, rh = self.hd(), self.hd()
        idf[4].append((rh, eh))
        w, h = idf[2], idf[3]
        if clip_px and len(clip_px) >= 3:
            cp = list(clip_px) + ([clip_px[0]] if clip_px[0] != clip_px[-1] else [])
            clip = "71\n2\n91\n%d\n" % len(cp) + "\n".join("14\n%.4f\n24\n%.4f" % p for p in cp)
            fl, st = 7, 1
        else:
            clip = "71\n1\n91\n2\n14\n-0.5\n24\n-0.5\n14\n%.1f\n24\n%.1f" % (w - 0.5, h - 0.5)
            fl, st = 3, 0
        s = ("0\nIMAGE\n5\n%s\n330\n%s\n100\nAcDbEntity\n8\n%s%s\n100\nAcDbRasterImage\n90\n0\n10\n%.4f\n20\n%.4f\n30\n0.0\n"
             "11\n%.8f\n21\n%.8f\n31\n0.0\n12\n%.8f\n22\n%.8f\n32\n0.0\n13\n%d\n23\n%d\n340\n%s\n70\n%d\n280\n%d\n281\n50\n"
             "282\n50\n283\n%d\n360\n%s\n%s\n290\n0" %
             (eh, owner, lay, "", ins[0], ins[1], u[0], u[1], v[0], v[1], w, h, idf[0], fl, st,
              0 if op is None else int(round((1 - op) * 100)), rh, clip))
        self.h = max(self.h, int(eh, 16))
        out.append(s)

    def block(self, name):
        rec, beg, end = self.hd(), self.hd(), self.hd()
        ents = []
        self.blocks.append((name, rec, beg, end, ents))
        return rec, ents

    def text_out(self):
        t = self.tpl
        recs = "".join("\n0\nBLOCK_RECORD\n5\n%s\n330\n9\n100\nAcDbSymbolTableRecord\n100\nAcDbBlockTableRecord\n2\n%s\n340\n0"
                       % (rec, nm) for nm, rec, b, e, en in self.blocks)
        blks = "".join("\n0\nBLOCK\n5\n%s\n330\n%s\n100\nAcDbEntity\n8\n0\n100\nAcDbBlockBegin\n2\n%s\n70\n0\n10\n0.0\n20\n0.0\n"
                       "30\n0.0\n3\n%s\n1\n%s%s\n0\nENDBLK\n5\n%s\n330\n%s\n100\nAcDbEntity\n8\n0\n100\nAcDbBlockEnd"
                       % (b, rec, nm, nm, "", ("\n" + "\n".join(en)) if en else "", e, rec) for nm, rec, b, e, en in self.blocks)
        objs = []
        for dh, fname, w, h, reacts in self.imgdefs:
            objs.append("0\nIMAGEDEF\n5\n%s\n102\n{ACAD_REACTORS\n330\n30\n%s102\n}\n330\n30\n100\nAcDbRasterImageDef\n90\n0\n"
                        "1\n%s\n10\n%d\n20\n%d\n11\n%.6f\n21\n%.6f\n280\n1\n281\n0" %
                        (dh, "".join("330\n%s\n" % rh for rh, eh in reacts), fname, w, h, 1.0 / w, 1.0 / h))
            for rh, eh in reacts:
                objs.append("0\nIMAGEDEF_REACTOR\n5\n%s\n330\n%s\n100\nAcDbRasterImageDefReactor\n90\n2\n330\n%s" % (rh, eh, eh))
        norm = [x.strip() for x in t.split("\n")]

        def find(seq, start=0):
            for i in range(start, len(norm) - len(seq)):
                if norm[i:i + len(seq)] == seq:
                    return i
            raise RuntimeError("DXF template: %s not found" % seq)
        if self.imgdefs:                              # name the image definitions in ACAD_IMAGE_DICT (handle 30)
            i = find(["0", "DICTIONARY", "5", "30"])
            j = i + 2
            while norm[j] != "0":
                j += 2
            norm[j:j] = sum((["3", "BERGAMA_IMG_%d" % (k + 1), "350", dh] for k, (dh, f, w, h, r) in
                             enumerate(self.imgdefs)), [])
        lt0 = find(["0", "TABLE", "2", "LTYPE"])
        lt1 = find(["0", "ENDTAB"], lt0)
        i = find(["0", "TABLE", "2", "LAYER"])
        j = find(["0", "ENDTAB"], i)
        k = find(["0", "TABLE", "2", "BLOCK_RECORD"])
        k2 = find(["0", "ENDTAB"], k)
        b0 = find(["2", "BLOCKS"])
        b1 = find(["0", "ENDSEC"], b0)
        e0 = find(["2", "ENTITIES"])
        e1 = find(["0", "ENDSEC"], e0)
        o0 = find(["2", "OBJECTS"])
        o1 = find(["0", "ENDSEC"], o0)
        cuts = sorted([(lt1, "\n".join(self.ltypes)), (j, "\n".join(self.layers)), (k2, recs.strip("\n")),
                       (b1, blks.strip("\n")), (e1, "\n".join(self.ents)), (o1, "\n".join(objs))])
        parts, last = [], 0
        for pos, txt in cuts:
            parts.append("\n".join(norm[last:pos]))
            if txt:
                parts.append(txt)
            last = pos
        parts.append("\n".join(norm[last:]))
        out = "\n".join(p for p in parts if p)
        out = re.sub(r"(\$HANDSEED\n5\n)\w+", lambda m: m.group(1) + "%X" % (self.h + 1), out)
        return out + ("\n" if not out.endswith("\n") else "")


SYM_CLIP_TOL = 0.03          # DXF: a clip that cuts off less than 3 % of a symbol's size leaves the symbol whole (a block)


def svg_to_dxf(data, placing, notes, img_dir=None):
    """the master SVG -> DXF (AutoCAD 2010): one layer per plan layer (top group), symbols -> blocks, fills -> solid
    hatches, curves -> exact splines, transparency, dash patterns -> linetypes, pictures -> linked files in img_dir,
    clip groups -> shapes cut to the clip outline"""
    import base64 as _b64, hashlib as _hl
    d = Doc(data, "master")
    if placing:
        M = tuple(placing["M"])
        notes.append(u"DXF in survey metres (placing from PlanToRhino v2)")
    else:
        M = (1.0, 0.0, 0.0, -1.0, 0.0, 0.0)
        notes.append(u"FLAG DXF in plan SVG units (no survey placing yet: run SharedSync once from Rhino after PlanToRhino v2)")
    X = DXF()
    MS = "17"                                         # the template's *Model_Space
    n_skip, n = {}, {"splines": 0, "clipped": 0, "transparent": 0, "dashed": 0, "pictures": 0, "blocks kept": 0, "hidden": 0}
    blocks, imgs = {}, {}

    def skip(k):
        n_skip[k] = n_skip.get(k, 0) + 1

    def num_(v, dflt=1.0):
        try:
            return float(str(v).strip().rstrip("%")) / (100.0 if str(v).strip().endswith("%") else 1.0)
        except Exception:
            return dflt

    def style_of(el, parent):
        st = dict((k, v) for k, v in parent.items() if k not in ("display", "opacity", "transform", "clip-path"))
        for k in ("fill", "stroke", "stroke-width", "font-size", "font-weight", "text-anchor", "display", "visibility", "opacity",
                  "fill-opacity", "stroke-opacity", "stroke-dasharray", "clip-path"):
            if el.get(k) is not None:
                st[k] = el.get(k)
        st.update(d.style(el))
        st["_op"] = parent.get("_op", 1.0) * num_(st.pop("opacity", 1.0))
        return st

    def clip_of(ch, mm, s2, clip):
        """the clip outline of this element in output coordinates, joined with the clip already active:
        {"R": rings, "P": the outline if convex, "o": its turning sense, "empty": nothing visible}"""
        v = s2.get("clip-path") or ""
        m_ = re.search(r"url\(\s*['\"]?#([^)'\"]+)", v)
        if not m_:
            return clip
        cp = d.ids.get(m_.group(1))
        if cp is None:
            return clip
        R = []
        for e in cp:
            tg = local(e.tag)
            if tg in ("path", "rect", "circle", "ellipse", "polygon", "polyline"):
                me = mmul(mm, parse_transform(e.get("transform")))
                for sub in shape_segs(tg, e):
                    P = segs_flat(segs_map(me, sub), 4)
                    if len(P) > 2 and P[0] == P[-1]:
                        P = P[:-1]
                    if len(P) >= 3:
                        R.append(P)
            elif tg == "use":
                skip("clip outlines made of a symbol (not applied)")
            if R:
                break
        if not R:
            return clip
        P = R[0] if len(R) == 1 and is_convex(R[0]) else None
        if clip is not None:
            if clip["empty"]:
                return clip
            if P is not None and clip["P"] is not None:
                P = clip_ring_c(P, clip["P"], clip["o"])
                if len(P) < 3:
                    return {"R": [], "P": None, "o": 1.0, "empty": True}
                R = [P]
            else:
                skip("clip inside a clip (inner outline used)")
        return {"R": R, "P": P, "o": poly_orient(P) if P else 1.0, "empty": False}

    def all_in(P, clip, tol=0.0):
        if clip["P"] is not None:
            C, o = clip["P"], clip["o"]
            for i in range(len(C)):
                a, b = C[i - 1], C[i]
                ln = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
                if any(o * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) / ln < -tol - 1e-9 for p in P):
                    return False
            return True
        if "grid" not in clip:
            clip["grid"] = EdgeGrid(clip["R"])
        if not all(in_rings(clip["R"], p) for p in P):
            return False
        return not any(clip["grid"].cuts(P[i - 1], P[i]) for i in range(1, len(P)))

    def traps_of(clip):
        if "traps" not in clip:
            clip["traps"] = trapezoids(clip["R"])
        return clip["traps"]

    boxes = {}

    def sym_box(ref, tgt):
        """the corners of a symbol's drawing (its own units), for the 'wholly inside the clip' test"""
        if ref not in boxes:
            pts = []
            for e in tgt.iter():
                tg = local(e.tag)
                if tg in ("path", "rect", "circle", "ellipse", "polygon", "polyline", "line"):
                    for sub in shape_segs(tg, e):
                        pts += segs_flat(sub, 2)
            if not pts:
                vb = [float(x) for x in _NUM.findall(tgt.get("viewBox") or "")] or [0, 0, 0, 0]
                pts = [(vb[0], vb[1]), (vb[0] + vb[2], vb[1] + vb[3])]
            x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
            x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
            boxes[ref] = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        return boxes[ref]

    def dash_of(s2, sc):
        v = (s2.get("stroke-dasharray") or "").strip()
        if not v or v == "none":
            return None
        pat = [float(x) * sc for x in _NUM.findall(v)]
        lt = X.ltype(pat) if pat and sum(pat) > 0 else None
        if lt:
            n["dashed"] += 1
        return lt

    def picture(ch, mm, s2, clip, out, owner, lay):
        href = ch.get(XLINK) or ch.get("href") or ""
        m_ = re.match(r"data:image/(png|jpe?g|gif);base64,(.*)$", href.strip(), re.S)
        if not m_ or not img_dir:
            skip("pictures (not embedded / no picture folder)")
            return
        raw = _b64.b64decode("".join(m_.group(2).split()))
        sz = image_px_size(raw)
        if not sz or not sz[0] or not sz[1]:
            skip("pictures (unknown format)")
            return
        key = _hl.sha1(raw).hexdigest()[:12]
        if key not in imgs:
            ext = "jpg" if m_.group(1).startswith("j") else m_.group(1)
            fn = "img_%s.%s" % (key, ext)
            os.makedirs(img_dir, exist_ok=True)
            with open(os.path.join(img_dir, fn), "wb") as fh:
                fh.write(raw)
            imgs[key] = X.imagedef(".\\%s\\%s" % (os.path.basename(img_dir), fn), sz[0], sz[1])
        W, H = sz
        x, y = first_num(ch.get("x"), 0.0), first_num(ch.get("y"), 0.0)
        w, h = first_num(ch.get("width"), W), first_num(ch.get("height"), H)
        ins = mpt(mm, (x, y + h))
        pu, pv = mpt(mm, (x + w / W, y + h)), mpt(mm, (x, y + h - h / H))
        clip_px = None
        if clip is not None:
            corners = [mpt(mm, q) for q in ((x, y), (x + w, y), (x + w, y + h), (x, y + h))]
            if clip["empty"]:
                return
            if not all_in(corners, clip):
                if len(clip["R"]) > 1:
                    skip("pictures clipped by an outline with holes (outer ring used)")
                mi = inv(mm)
                clip_px = [((q[0] - x) / w * W - 0.5, (q[1] - y) / h * H - 0.5) for q in (mpt(mi, c) for c in clip["R"][0])]
                n["clipped"] += 1
        op = s2.get("_op", 1.0)
        X.image(out, owner, lay, imgs[key], ins, (pu[0] - ins[0], pu[1] - ins[1]), (pv[0] - ins[0], pv[1] - ins[1]),
                clip_px, op if op < 0.999 else None)
        n["pictures"] += 1

    def shape(tg, ch, mm, s2, clip, out, owner, lay):
        subs = [segs_map(mm, s) for s in shape_segs(tg, ch)]
        if not subs:
            return
        fill = parse_color(s2.get("fill", "#000000"))
        stroke = parse_color(s2.get("stroke"))
        if tg in ("line", "polyline"):
            fill = None
        op = s2.get("_op", 1.0)
        fop = op * num_(s2.get("fill-opacity", 1.0))
        sop = op * num_(s2.get("stroke-opacity", 1.0))
        cut = False
        if clip is not None:
            if clip["empty"]:
                return
            if not all_in([p for s in subs for p in segs_flat(s, 4)], clip):
                cut = True
                n["clipped"] += 1
        curved = any(sg[0] == "C" for s in subs for sg in s[2])
        if fill is not None:
            if not cut:
                X.hatch(out, owner, lay, subs if curved else [segs_flat(s) for s in subs], fill, fop)
            elif clip["P"] is not None:
                loops = [clip_ring_c(segs_flat(s), clip["P"], clip["o"]) for s in subs]
                X.hatch(out, owner, lay, [L for L in loops if len(L) >= 3], fill, fop)
            else:
                flat = [segs_flat(s) for s in subs]
                fx0, fx1 = min(p[0] for F in flat for p in F), max(p[0] for F in flat for p in F)
                fy0, fy1 = min(p[1] for F in flat for p in F), max(p[1] for F in flat for p in F)
                loops = []
                for T, tx0, tx1, ty0, ty1 in traps_of(clip):
                    if tx1 < fx0 or tx0 > fx1 or ty1 < fy0 or ty0 > fy1:
                        continue
                    o = poly_orient(T)
                    loops += [L for L in (clip_ring_c(F, T, o) for F in flat) if len(L) >= 3]
                X.hatch(out, owner, lay, loops, fill, fop)
            if fop < 0.999:
                n["transparent"] += 1
        if stroke is not None:
            sc = math.sqrt(abs(mm[0] * mm[3] - mm[1] * mm[2]))
            lt = dash_of(s2, sc)
            if sop < 0.999:
                n["transparent"] += 1
            for s in subs:
                if cut:
                    P = segs_flat(s)
                    if s[0]:
                        P = P + [P[0]]
                    if clip["P"] is not None:
                        pieces = clip_line_c(P, clip["P"], clip["o"])
                    else:
                        if "grid" not in clip:
                            clip["grid"] = EdgeGrid(clip["R"])
                        pieces = clip_line_r(P, clip["R"], clip["grid"])
                    for piece in pieces:
                        X.poly(out, owner, lay, piece, False, stroke, sop, lt)
                elif any(sg[0] == "C" for sg in s[2]):
                    X.spline(out, owner, lay, s, stroke, sop, lt)
                    n["splines"] += 1
                else:
                    X.poly(out, owner, lay, segs_flat(s), s[0], stroke, sop, lt)

    def walk(el, m, st, out, owner, lay, sym_mode=False, clip=None):
        for ch in el:
            tg = local(ch.tag)
            if tg in ("defs", "symbol", "clipPath", "mask", "metadata", "style", "title", "linearGradient", "radialGradient"):
                continue
            s2 = style_of(ch, st)
            if ch not in unit_els and ((s2.get("display") or "").strip() == "none" or
                                       (s2.get("visibility") or "").strip() in ("hidden", "collapse")):
                n["hidden"] += 1                        # hidden in Illustrator: not drawn (as in the SVG)
                continue
            mm = mmul(m, parse_transform(ch.get("transform")))
            ck = clip_of(ch, mm, s2, clip)
            if tg == "g":
                walk(ch, mm, s2, out, owner, lay, sym_mode, ck)
            elif tg in ("path", "rect", "circle", "ellipse", "polygon", "polyline", "line"):
                shape(tg, ch, mm, s2, ck, out, owner, lay)
            elif tg == "text":
                if ck is not None and ck["empty"]:
                    continue
                txt = re.sub(r"\s+", " ", "".join(ch.itertext())).strip()
                if txt:
                    x0 = first_num(ch.get("x"), 0.0)
                    y0 = first_num(ch.get("y"), 0.0)
                    ts = next((t for t in ch if local(t.tag) == "tspan"), None)
                    if ts is not None:
                        x0, y0 = first_num(ts.get("x"), x0), first_num(ts.get("y"), y0)
                    p = mpt(mm, (x0, y0))
                    q = mpt(mm, (x0 + 1.0, y0))
                    sc = math.sqrt(abs(mm[0] * mm[3] - mm[1] * mm[2]))
                    op = s2.get("_op", 1.0) * num_(s2.get("fill-opacity", 1.0))
                    X.text(out, owner, lay, p, first_num(s2.get("font-size"), 16.0) * sc * CAP, txt,
                           math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])), parse_color(s2.get("fill")) or (0, 0, 0),
                           (s2.get("text-anchor") or "start").strip(), op if op < 0.999 else None)
            elif tg == "use":
                ref = (ch.get(XLINK) or ch.get("href") or "").lstrip("#")
                tgt = d.ids.get(ref)
                if tgt is None:
                    continue
                mu = mmul(mm, (1.0, 0.0, 0.0, 1.0, first_num(ch.get("x"), 0.0), first_num(ch.get("y"), 0.0)))
                if local(tgt.tag) == "symbol":
                    vb = [float(x) for x in _NUM.findall(tgt.get("viewBox") or "")]
                    if len(vb) == 4 and vb[2] > 0 and vb[3] > 0:
                        w, h = first_num(ch.get("width"), vb[2]), first_num(ch.get("height"), vb[3])
                        s = min(w / vb[2], h / vb[3])
                        mu = mmul(mu, (s, 0.0, 0.0, s, -vb[0] * s + (w - vb[2] * s) / 2.0, -vb[1] * s + (h - vb[3] * s) / 2.0))
                    bx = [mpt(mu, q) for q in sym_box(ref, tgt)]
                    tol = SYM_CLIP_TOL * max(math.hypot(bx[2][0] - bx[0][0], bx[2][1] - bx[0][1]), 1e-9)
                    if ck is not None and not ck["empty"] and all_in(bx, ck, tol):
                        ck = None                   # the clip cuts (almost) nothing off this symbol: kept as a block
                        n["blocks kept"] += 1
                    if sym_mode or ck is not None or s2.get("_op", 1.0) < 0.999:
                        walk(tgt, mu, s2, out, owner, lay, True, ck)   # clipped / see-through: drawn as its pieces
                        continue
                    if ref not in blocks:
                        nm = re.sub(r"[^A-Za-z0-9_]+", "_", ref)
                        rec, ents = X.block(nm)
                        blocks[ref] = nm
                        walk(tgt, ID, {"fill": "#000000"}, ents, rec, "0", True)
                    X.insert(out, owner, lay, blocks[ref], mmul(M, mu))
                else:
                    walk([tgt], mu, s2, out, owner, lay, sym_mode, ck)
            elif tg == "image":
                picture(ch, mm, s2, ck, out, owner, lay)
    n_lay = 0
    unit_els = set(el for key, el, par in d.units)     # a hidden plan layer is still written, as a layer turned off
    for key, el, par in d.units:
        st = style_of(el, {"fill": "#000000"})
        hidden = (st.get("display") or "").strip() == "none"
        lay = X.layer(key, hidden)
        n_lay += 1
        m0 = parse_transform(par.get("transform")) if par is not d.root else ID
        walk([el], mmul(M, m0), {"fill": "#000000"}, X.ents, MS, lay)
    if n_skip:
        notes.append(u"DXF: drawn differently: " + u", ".join(u"%s %d" % kv for kv in n_skip.items()))
    notes.append(u"DXF: %d layers, %d entities, %d blocks, %d linetypes; %d splines, %d clipped, %d see-through, %d dashed, "
                 u"%d pictures (%d files in %s); %d clipped symbols kept whole as blocks (clip cuts off < %d%% of their size)" %
                 (n_lay, len(X.ents), len(blocks), len(X.ltypes), n["splines"], n["clipped"], n["transparent"], n["dashed"],
                  n["pictures"], len(imgs), os.path.basename(img_dir or "-"), n["blocks kept"], round(SYM_CLIP_TOL * 100)))
    notes.append(u"DXF: %d hidden groups / shapes left out (hidden in the SVG too)" % n["hidden"])
    return X.text_out()


# =====================================================================================================  Windows: Bergama.bat
def notify(title, msg):
    """a small Windows notification (PowerShell, built into Windows); nothing if it fails"""
    try:
        import subprocess
        ps = ("Add-Type -AssemblyName System.Windows.Forms; $n = New-Object System.Windows.Forms.NotifyIcon; "
              "$n.Icon = [System.Drawing.SystemIcons]::Information; $n.Visible = $true; "
              "$n.ShowBalloonTip(8000, '%s', '%s', 'Info'); Start-Sleep -Seconds 9; $n.Dispose()" %
              (title.replace("'", "''")[:60], msg.replace("'", "''")[:240]))
        subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
                         creationflags=0x08000000)
    except Exception:
        pass


def show_error(text):
    """the hidden run shows itself again: a console window with the error in bold red (stays open)"""
    try:
        import subprocess, tempfile
        f = os.path.join(tempfile.gettempdir(), "bergama_error.txt")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(text)
        ps = ("$e=[char]27; Write-Host ($e+'[1;31m'+'BERGAMA SYNC ERROR'+$e+'[0m'); "
              "Get-Content -Encoding UTF8 '%s' | ForEach-Object { Write-Host ($e+'[1;31m'+$_+$e+'[0m') }; "
              "Write-Host ''; Write-Host 'Full log: %s'; Read-Host 'Press Enter to close'" %
              (f.replace("'", "''"), os.path.join(LOG_DIR, LOG_NAME).replace("'", "''")))
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps], creationflags=0x00000010)   # new console
    except Exception:
        pass


def find_exe(patterns):
    import glob
    for pat in patterns:
        hits = sorted(glob.glob(pat), reverse=True)    # the newest version first
        if hits:
            return hits[0]
    return None


def running(image):
    import subprocess
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq %s" % image, "/NH"], capture_output=True, text=True,
                             creationflags=0x08000000).stdout
        return image.lower() in out.lower()
    except Exception:
        return False


def cli(app):
    """Bergama.bat: sync, open the file in the chosen app (Illustrator: sync again once Illustrator is closed)"""
    import subprocess
    log = []

    def run_sync(tag):
        head = u"\n\n".join(log) + u"\n\n==== %s %s\n" % (tag, now_iso())
        live = LiveNotes(head)
        try:
            txt = main(notes=live)
            ok = True
        except Exception as ex:
            import traceback
            txt = u"\n".join(live) + u"\nERROR: %s: %s\n%s" % (type(ex).__name__, ex, traceback.format_exc()[-800:])
            ok = False
            write_log(head + txt)
            show_error(u"%s: %s\n\n(step reached: %s)" % (type(ex).__name__, ex, live[-1] if live else "start"))
        log.append(u"==== %s %s\n%s" % (tag, now_iso(), txt))
        write_log(u"\n\n".join(log))
        flags = [l for l in txt.split("\n") if "FLAG" in l]
        notify("Bergama sync " + ("done" if ok else "ERROR"),
               (u"%d conflict / flag lines - see logs" % len(flags)) if flags else
               (u"master is up to date" if ok else txt.split("\n")[0]))
        return ok
    pf = [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]
    if not run_sync("sync before opening"):
        return
    st = {}
    try:
        for line in open(SETTINGS_FILE, encoding="utf-8-sig"):
            if "=" in line:
                k, v = line.split("=", 1)
                st[k.strip().lower()] = v.strip()
    except Exception:
        pass
    if app == "rhino":
        exe = st.get("rhino_exe") or find_exe([os.path.join(p, "Rhino 8", "System", "Rhino.exe") for p in pf] +
                                              [os.path.join(p, "Rhino 7", "System", "Rhino.exe") for p in pf])
        f = st.get("rhino_file")
        if not f:
            cands = []
            for dp, dn, fn in os.walk(BERGAMA_ROOT):
                if dp.count(os.sep) - BERGAMA_ROOT.count(os.sep) > 2:
                    dn[:] = []
                    continue
                cands += [os.path.join(dp, x) for x in fn if x.lower().endswith(".3dm")]
            f = max(cands, key=os.path.getmtime) if cands else None
        if not exe:
            notify("Bergama", "Rhino not found: add rhino_exe=<path to Rhino.exe> to " + SETTINGS_FILE)
            return
        subprocess.Popen([exe] + ([f] if f else []))
        log.append(u"opened Rhino: %s %s" % (exe, f or "(no .3dm found: add rhino_file=<path> to the settings file)"))
    elif app == "illustrator":
        exe = st.get("illustrator_exe") or find_exe([os.path.join(p, "Adobe", "Adobe Illustrator*", "Support Files", "Contents",
                                                                  "Windows", "Illustrator.exe") for p in pf])
        if not exe:
            notify("Bergama", "Illustrator not found: add illustrator_exe=<path> to " + SETTINGS_FILE)
            return
        t0 = os.path.getmtime(MY_FILE)
        subprocess.Popen([exe, MY_FILE])
        log.append(u"opened Illustrator: %s" % MY_FILE)
        write_log(u"\n\n".join(log))
        time.sleep(20)
        while running("Illustrator.exe"):
            time.sleep(10)
        if os.path.getmtime(MY_FILE) != t0:
            run_sync("sync after Illustrator closed")
        else:
            log.append(u"Illustrator closed, your file was not saved: nothing to upload")
    elif app == "autocad":
        cp = os.path.join(CLOUD_COPY, "master.svg")
        placing = None
        try:
            token, me = read_settings()
            gh = GitHub(token)
            files, _ = gh.tree(gh.head())
            pp = "%s/master/placing.json" % CLOUD
            placing = json.loads(gh.blob(files[pp]).decode("utf-8")) if pp in files else None
        except Exception:
            placing = None
        notes = []
        dxf = svg_to_dxf(open(cp, "rb").read(), placing, notes, os.path.join(SH_DIR, "masterplan_latest_images"))
        out = os.path.join(SH_DIR, "masterplan_latest.dxf")
        write_file(out, dxf.encode("utf-8"))
        log.append(u"DXF written: %s\n%s" % (out, u"\n".join(notes)))
        exe = st.get("autocad_exe") or find_exe([os.path.join(p, "Autodesk", "AutoCAD*", "acad.exe") for p in pf])
        if not exe:
            notify("Bergama", "AutoCAD not found: add autocad_exe=<path to acad.exe> to " + SETTINGS_FILE)
        else:
            subprocess.Popen([exe, out])
            log.append(u"opened AutoCAD: %s" % out)
    write_log(u"\n\n".join(log))


if __name__ == "__main__" and "ghenv" not in globals():
    import sys as _sys
    _app = (_sys.argv[1] if len(_sys.argv) > 1 else "").lower()
    if _app in ("rhino", "illustrator", "autocad"):
        try:
            cli(_app)
        except Exception as _ex:
            import traceback as _tb
            write_log(u"ERROR while opening %s: %s: %s\n%s" % (_app, type(_ex).__name__, _ex, _tb.format_exc()[-800:]))
            show_error(u"opening %s: %s: %s" % (_app, type(_ex).__name__, _ex))
    else:
        print(main())


# ---- Grasshopper wiring (template) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = globals().get("run") is True or (isinstance(globals().get("run"), list) and True in globals().get("run"))
    if _pressed:
        _t0 = time.time()
        try:
            import Rhino as _Rh
            _res = main(doc=_Rh.RhinoDoc.ActiveDoc)
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button: upload your edits, download all, merge, then PlanToRhino bakes "
                                      "the master. Settings: " + SETTINGS_FILE)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
