#! python3
# -*- coding: utf-8 -*-
"""Bergama Group 6: SHARED SYNC v2 (8 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.

Aras 8 Nov 2026 (spec 12:36 UTC + answers 12:43-14:29 UTC): three people (aras, begum, nil) edit ONE masterplan, mostly
in Illustrator, some in Rhino. Every run gives everyone ONE combined latest file, built layer by layer from everyone's
newest edits. Bergama.bat runs this file (1 Rhino / 2 Illustrator); Rhino runs it too (Bergama.bat opens Rhino with it).
Run order (one sync):
  0 date stamp: each layer (top group of the SVG = one Rhino layer) of your file Data/shared/my_masterplan.svg that
    differs from the combined file this PC synced last gets the file's save time (on GitHub's clock) + your name
    (attributes data-edited / data-edited-by / data-edited-from on its group); unchanged layers keep their date
  1 your folder: download your cloud folder (your other PCs), merge your file into it layer by layer (newest date
    wins, the losing version to conflicts), upload the result as a new version
  2 download aras, begum, nil and latest
  3 merge: for each layer, the versions edited since the combined file was made compete; newest date wins; losers saved
    whole in conflicts (cloud + Data/shared/conflicts/); new layers added; a deleted layer goes only if the deletion is
    newer than every other edit of it
  4 upload the combined file to latest (and the conflicts)
  5 rebuild: the planting analysis SVG (Data/analysis/planting_analysis.svg); Rhino rebakes its layers when it opens
Cloud: GitHub repo SupFlyn/BergamaProjectScripts. Folders = Releases 'aras', 'begum', 'nil', 'latest', 'conflicts', 'images'
(files named by GitHub time; the 10 newest kept in each folder, conflicts never deleted); the register of layer dates is
state.json on branch 'shared'. All dates are GitHub's clock (UTC); the log shows them in this PC's time.
Speed: layer hashes cached between runs (Data/shared/hash_cache.json); downloads and uploads run in parallel; cloud
files are gzipped and their pictures are kept once in the folder 'images' (a 28 MB plan uploads as ~1.4 MB); a run with
nothing new here or in the cloud stops after one look at the register; the analysis is rebuilt only when its inputs
changed, after the app has opened.
Settings (setup.bat writes them): Downloads/Bergama/Data/shared_settings.txt: token=..., me=aras|begum|nil
Needs next to it in Downloads/Bergama: bergama_plan_to_rhino_v2_1.py, bergama_planting_analysis_v1.py.
"""
import os, time, json, re, hashlib, copy, math, calendar

# ---- SETTINGS ----
VERSION = "v2.1"   # 9 Nov 2026: loads PlanToRhino v2.1 (PTR_FILE)
GH_LABEL = "SharedSync"
OUT_FOLDER = "bergama_shared_sync"
LOG_NAME = "bergama_shared_sync_log.txt"
REPO = "SupFlyn/BergamaProjectScripts"            # the shared files live in this repo
BRANCH = "shared"                                 # the register state.json lives on this branch (made from main)
BASE_BRANCH = "main"
PEOPLE = ("aras", "begum", "nil")
FOLDERS = PEOPLE + ("latest", "conflicts", "images")   # one GitHub Release each (images: pictures, once each)
TAG_PREFIX = "bergama-"                           # release tags: bergama-aras, ... bergama-conflicts
KEEP_VERSIONS = 10
SHARED_LOCAL = "shared"                           # Data/shared/ on this computer
ROOT_LAYER = "masterplan"                         # PlanToRhino's parent layer
SKIP_LAYERS = ("analysis_", "masterplan_conflicts")   # sub-layers that are outputs, never written back
DATE_ATTR, BY_ATTR = "data-edited", "data-edited-by"
FROM_ATTR = "data-edited-from"                  # the date of the version the edit started from
API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"

# ---- Bergama folders (template block, SCRIPT_STANDARD §9) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
LOG_DIR = bg_logs()
SH_DIR = os.path.join(DATA_DIR, SHARED_LOCAL)
MY_FILE = os.path.join(SH_DIR, "my_masterplan.svg")      # the file you open and save in Illustrator
BASE_FILE = os.path.join(SH_DIR, "last_combined.svg")    # the combined file this PC synced last
CLOUD_COPY = os.path.join(SH_DIR, "cloud")
CONFLICT_DIR = os.path.join(SH_DIR, "conflicts")
PLAN_DIR = os.path.join(DATA_DIR, "assets", "plan")
PLAN_FILE = os.path.join(PLAN_DIR, "masterplan_latest.svg")
SEED_FILE = os.path.join(DATA_DIR, "assets", "planting_areas_seed.svg")
SETTINGS_FILE = os.path.join(DATA_DIR, "shared_settings.txt")
LOCAL_STATE = os.path.join(SH_DIR, "local_state.json")
HASH_CACHE = os.path.join(SH_DIR, "hash_cache.json")
PLACING_FILE = os.path.join(SH_DIR, "placing.json")
HERE = os.path.dirname(os.path.abspath(globals().get("__file__") or os.path.join(BERGAMA_ROOT, "x.py")))
PTR_FILE = "bergama_plan_to_rhino_v2_1.py"   # P5 9 Nov 2026: v2.1 (layer fix), was v2
PA_FILE = "bergama_planting_analysis_v1.py"

# PlanToRhino v2 keys (must match bergama_plan_to_rhino_v2_1.py)
PTR_KEY = "bergama_plan_to_rhino"
STAMP = "bergama_plan_to_rhino"
UNIT_KEY = "bergama_unit"
SYNC_KEY = "bergama_shared_sync"
CAP = 0.716                                       # Arial capital height / font size

SVG_NS = "http://www.w3.org/2000/svg"
XL_NS = "http://www.w3.org/1999/xlink"
SVGNS = "{%s}" % SVG_NS
XLINK = "{%s}href" % XL_NS
_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


# ---- time: GitHub's clock (UTC) for every date; the log shows this PC's time ----
def iso_utc(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def epoch(iso):
    try:
        return calendar.timegm(time.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return None


def short(iso):
    """a GitHub (UTC) date shown in this PC's time"""
    t = epoch(iso or "")
    return time.strftime("%d %b %H:%M", time.localtime(t)) if t is not None else (iso or "?")


def tz_name():
    try:
        return time.strftime("%Z") or "PC time"
    except Exception:
        return "PC time"


def fname_time(iso):
    """2026-11-08T12:43:05Z -> 2026-11-08_124305 (file names in the cloud: GitHub time)"""
    return iso[:10] + "_" + iso[11:19].replace(":", "")


# =====================================================================================================  settings
def read_settings():
    if not os.path.isfile(SETTINGS_FILE):
        raise RuntimeError("no settings file %s: run setup.bat once on this PC" % SETTINGS_FILE)
    st = {}
    for line in open(SETTINGS_FILE, encoding="utf-8-sig"):
        if "=" in line:
            k, v = line.split("=", 1)
            st[k.strip().lower()] = v.strip()
    if not st.get("token"):
        raise RuntimeError("no 'token=' line in %s: run setup.bat again" % SETTINGS_FILE)
    me = (st.get("me") or "").lower()
    if me not in PEOPLE:
        raise RuntimeError("'me=' in %s must be one of %s (now: '%s'): run setup.bat again" %
                           (SETTINGS_FILE, ", ".join(PEOPLE), me))
    return st["token"], me, st


# =====================================================================================================  GitHub
class Retry(Exception):
    pass


class GitHub(object):
    """the few GitHub REST calls the sync needs (standard library only). Folders are Releases; the register is
    state.json on branch BRANCH. Every reply's Date header sets the clock: all dates are GitHub's time."""

    def __init__(self, token, repo=REPO, branch=BRANCH, opener=None):
        self.token, self.repo, self.branch = token, repo, branch
        self.opener = opener                     # tests pass a fake; None = urllib
        self.offset = None                       # GitHub clock - this PC's clock (s)
        self.rel = {}

    def _send(self, method, url, hdr, data):
        if self.opener is not None:
            return self.opener(method, url, hdr, data)
        import urllib.request, urllib.error

        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        op = urllib.request.build_opener(NoRedirect)
        req = urllib.request.Request(url, data=data, headers=hdr, method=method)
        try:
            with op.open(req, timeout=600) as r:
                return r.status, r.read(), dict(r.headers.items())
        except urllib.error.HTTPError as e:
            return e.code, e.read(), dict(e.headers.items()) if e.headers else {}

    def call(self, method, path, body=None, accept="application/vnd.github+json", ok=(200, 201), raw_body=None,
             ctype=None, auth=True):
        url = path if path.startswith("http") else API + path
        data = raw_body if raw_body is not None else (json.dumps(body).encode("utf-8") if body is not None else None)
        hdr = {"Accept": accept, "User-Agent": "bergama-shared-sync", "X-GitHub-Api-Version": "2022-11-28"}
        if auth:
            hdr["Authorization"] = "Bearer " + self.token
        if data is not None:
            hdr["Content-Type"] = ctype or "application/json"
        code, raw, heads = self._send(method, url, hdr, data)
        heads = dict((k.lower(), v) for k, v in (heads or {}).items())
        if heads.get("date"):
            try:
                import email.utils
                self.offset = email.utils.parsedate_to_datetime(heads["date"]).timestamp() - time.time()
            except Exception:
                pass
        if code in (301, 302, 303, 307, 308) and code not in ok:
            loc = heads.get("location")
            if not loc:
                raise RuntimeError("GitHub %s %s -> %d without a location" % (method, url.replace(API, ""), code))
            return self.call("GET", loc, accept=accept, ok=ok, auth=False)   # the file host: no token
        if code not in ok:
            msg = (raw or b"")[:300].decode("utf-8", "replace")
            if code == 401:
                raise RuntimeError("GitHub refused the token (401): run setup.bat again with a working token")
            if code == 403 and b"rate limit" in (raw or b"").lower():
                raise RuntimeError("GitHub rate limit reached: wait an hour and run again")
            raise RuntimeError("GitHub %s %s -> %d: %s" % (method, url.replace(API, ""), code, msg))
        return code, raw

    def j(self, method, path, body=None, ok=(200, 201)):
        code, raw = self.call(method, path, body, ok=ok)
        return code, (json.loads(raw.decode("utf-8")) if raw else None)

    def now(self):
        """GitHub's time now (UTC ISO)"""
        if self.offset is None:
            self.call("GET", "/repos/%s" % self.repo)
        return iso_utc(time.time() + (self.offset or 0.0))

    # ---- register (state.json on the branch) ----
    def head(self):
        code, d = self.j("GET", "/repos/%s/git/ref/heads/%s" % (self.repo, self.branch), ok=(200, 404))
        if code == 404:
            _, b = self.j("GET", "/repos/%s/git/ref/heads/%s" % (self.repo, BASE_BRANCH))
            self.j("POST", "/repos/%s/git/refs" % self.repo, {"ref": "refs/heads/" + self.branch, "sha": b["object"]["sha"]})
            return b["object"]["sha"]
        return d["object"]["sha"]

    def read_state(self, head):
        """(state dict, tree sha) at this commit"""
        _, c = self.j("GET", "/repos/%s/git/commits/%s" % (self.repo, head))
        _, t = self.j("GET", "/repos/%s/git/trees/%s" % (self.repo, c["tree"]["sha"]))
        for e in t.get("tree", []):
            if e.get("path") == "state.json" and e.get("type") == "blob":
                _, raw = self.call("GET", "/repos/%s/git/blobs/%s" % (self.repo, e["sha"]), accept="application/vnd.github.raw")
                return json.loads(raw.decode("utf-8")), c["tree"]["sha"]
        return {}, c["tree"]["sha"]

    def write_state(self, head, tree, state, message):
        """commit state.json; Retry if somebody else committed since 'head' (the merge is then done again)"""
        data = json.dumps(state, indent=1, sort_keys=True).encode("utf-8")
        import base64
        _, b = self.j("POST", "/repos/%s/git/blobs" % self.repo,
                      {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        _, t = self.j("POST", "/repos/%s/git/trees" % self.repo,
                      {"base_tree": tree, "tree": [{"path": "state.json", "mode": "100644", "type": "blob", "sha": b["sha"]}]})
        _, c = self.j("POST", "/repos/%s/git/commits" % self.repo, {"message": message, "tree": t["sha"], "parents": [head]})
        code, _ = self.j("PATCH", "/repos/%s/git/refs/heads/%s" % (self.repo, self.branch),
                         {"sha": c["sha"], "force": False}, ok=(200, 422))
        if code == 422:
            raise Retry()
        return c["sha"], t["sha"]

    # ---- folders (Releases) ----
    def release(self, folder):
        """the release of this folder (made the first time)"""
        if folder not in self.rel:
            tag = TAG_PREFIX + folder
            code, r = self.j("GET", "/repos/%s/releases/tags/%s" % (self.repo, tag), ok=(200, 404))
            if code == 404:
                self.head()                                  # the branch must exist for the tag
                _, r = self.j("POST", "/repos/%s/releases" % self.repo,
                              {"tag_name": tag, "target_commitish": self.branch, "name": "Bergama shared: " + folder,
                               "body": "Bergama shared masterplan folder '%s' (written by bergama_shared_sync). "
                                       "Do not edit by hand." % folder, "draft": False, "prerelease": True})
            self.rel[folder] = r
        return self.rel[folder]

    def assets(self, folder):
        """{name: (id, size)} of the files in this folder"""
        rid = self.release(folder)["id"]
        out, page = {}, 1
        while True:
            _, d = self.j("GET", "/repos/%s/releases/%d/assets?per_page=100&page=%d" % (self.repo, rid, page))
            for a in d or []:
                out[a["name"]] = (a["id"], a.get("size", 0))
            if not d or len(d) < 100:
                return out
            page += 1

    def upload(self, folder, name, data, exist_ok=False):
        """a new file in this folder; returns (asset id, name) (a taken name gets _2, _3 ...)"""
        rid = self.release(folder)["id"]
        ext = ".svg.gz" if name.endswith(".svg.gz") else os.path.splitext(name)[1]
        base = name[:len(name) - len(ext)]
        for n in range(1, 30):
            nm = name if n == 1 else "%s_%d%s" % (base, n, ext)
            code, raw = self.call("POST", "%s/repos/%s/releases/%d/assets?name=%s" % (UPLOADS, self.repo, rid, nm),
                                  raw_body=data, ctype="application/gzip" if nm.endswith(".gz") else "image/svg+xml",
                                  ok=(200, 201, 422))
            if code in (200, 201):
                return json.loads(raw.decode("utf-8"))["id"], nm
            if exist_ok:                                     # the same content is already there (named by content)
                return None, name
        raise RuntimeError("GitHub: could not upload %s to %s" % (name, folder))

    def download(self, asset_id):
        _, raw = self.call("GET", "/repos/%s/releases/assets/%d" % (self.repo, asset_id), accept="application/octet-stream")
        return raw

    def delete(self, asset_id):
        self.call("DELETE", "/repos/%s/releases/assets/%d" % (self.repo, asset_id), ok=(204, 404))


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


_FILE_MEMO = {}
_UNIT_CACHE = []
_CACHE_DIRTY = [False]
_DATE_RE = re.compile(br' data-edited(?:-by|-from)?="[^"]*"')


def unit_cache():
    """{text key: canonical hash} kept between runs in Data/shared/hash_cache.json"""
    if not _UNIT_CACHE:
        d = {}
        try:
            d = json.load(open(HASH_CACHE, encoding="utf-8"))
        except Exception:
            pass
        _UNIT_CACHE.append(d if isinstance(d, dict) else {})
    return _UNIT_CACHE[0]


def save_unit_cache(keep=6000):
    if not _CACHE_DIRTY[0] or not _UNIT_CACHE:
        return
    d = _UNIT_CACHE[0]
    if len(d) > keep:                                          # dicts keep insertion order: the oldest go first
        for k in list(d)[:len(d) - keep]:
            del d[k]
    try:
        os.makedirs(os.path.dirname(HASH_CACHE), exist_ok=True)
        tmp = HASH_CACHE + ".tmp"
        json.dump(d, open(tmp, "w", encoding="utf-8"))
        os.replace(tmp, HASH_CACHE)
        _CACHE_DIRTY[0] = False
    except Exception:
        pass


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
        self.hash = self.unit_hashes(data)

    def unit_hashes(self, data):
        """canonical hash per unit; a unit whose text is unchanged since an earlier run is not hashed again"""
        import xml.etree.ElementTree as ET
        fsha = hashlib.sha1(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()
        if fsha in _FILE_MEMO:
            got = _FILE_MEMO[fsha]
            if set(got) == set(k for k, e, p in self.units):
                return dict(got)
        cache = unit_cache()
        unit_ids = set(id(e) for k, e, p in self.units)
        fp = hashlib.sha1()
        for st in self.root.iter(SVGNS + "style"):
            fp.update((st.text or "").encode("utf-8"))
        for ch in self.root:                                   # defs, symbols ... (everything that is not a unit)
            if id(ch) not in unit_ids and not any(id(c) in unit_ids for c in ch):
                fp.update(ET.tostring(ch))
        fp = fp.hexdigest()
        out = {}
        for k, e, p in self.units:
            raw = _DATE_RE.sub(b"", ET.tostring(e))
            rk = hashlib.sha1(fp.encode("ascii") + raw).hexdigest()
            h = cache.get(rk)
            if h is None:
                h = self.canon_hash(e)
                cache[rk] = h
                _CACHE_DIRTY[0] = True
            out[k] = h
        _FILE_MEMO[fsha] = dict(out)
        return out

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
            if k2 in ("id", "data-name", "class", "style", DATE_ATTR, BY_ATTR, FROM_ATTR):
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


# =====================================================================================================  layer dates + merge
def doc_dates(d):
    """{layer: (date, editor)} read from the layers' own attributes"""
    out = {}
    for k, e, p in d.units:
        if e.get(DATE_ATTR):
            out[k] = (e.get(DATE_ATTR), e.get(BY_ATTR) or "?")
    return out


def set_date(el, at, by, frm=None):
    el.set(DATE_ATTR, at)
    el.set(BY_ATTR, by)
    if frm is not None:
        el.set(FROM_ATTR, frm)


def stamp(my_data, base_data, now, me, fallback=None, saved=None):
    """step 0: each layer of my file that differs from the combined file this PC synced last (base) gets GitHub's time
    and my name; an unchanged layer keeps the base's date. Returns (bytes, [stamped layers], {deleted layer: [date, me]})"""
    L = Doc(my_data, me)
    B = Doc(base_data, "base") if base_data else None
    bd = doc_dates(B) if B else {}
    for k, v in (fallback or {}).items():
        bd.setdefault(k, tuple(v))
    stamped = []
    for k, e, p in L.units:
        if B is not None and B.hash.get(k) == L.hash[k] and k in bd:
            be = B.unit(k)[0]                               # unchanged: the base's dates back (Illustrator drops them)
            set_date(e, bd[k][0], bd[k][1], be.get(FROM_ATTR) if be is not None else None)
        elif B is None and e.get(DATE_ATTR):
            pass                                        # no base on this PC yet: the file's own date stands
        else:
            frm = bd.get(k, ("", ""))[0]
            # the edit's time: when the file was saved (in GitHub time), if that is after the version it started from
            at = saved if saved and frm < saved <= now else now
            set_date(e, at, me, frm)                       # and remember which version the edit started from
            stamped.append(k)
    deleted = dict((k, [saved if saved and bd.get(k, ("", ""))[0] < saved <= now else now, me])
                   for k in (B.hash if B is not None else {}) if k not in L.hash)
    out = to_bytes(L.root)
    _INFO[hashlib.sha1(out).hexdigest()] = (dict(L.hash), doc_dates(L))   # only dates changed: same hashes
    return out, stamped, deleted


def merge_layers(frame_data, frame_label, base_dates, base_deleted, cands, now):
    """the layer-by-layer merge. frame: the file the result is built on (its layers stay unless replaced);
    base_dates {layer: date} / base_deleted {layer: date}: what the competing files are compared with;
    cands [(label, bytes, {layer: [date, by]} deletions)]. For each layer: the versions edited after the base compete,
    the newest date wins, every other version is a conflict (saved whole). Returns
    (bytes, rows [(layer, action, from, date, by)], conflicts [(layer, by, date, bytes, label)], deleted {layer: [date, by]})"""
    frame = Doc(frame_data, frame_label)
    comp = Composer(frame)
    fd = doc_dates(frame)
    docs = [(lab, Doc(data, lab), dels or {}) for lab, data, dels in cands if data]
    dd = dict((lab, doc_dates(d)) for lab, d, dels in docs)
    order = [k for k, e, p in frame.units]
    for lab, d, dels in docs:
        for k, e, p in d.units:
            if k not in order:
                order.append(k)
    for lab, d, dels in docs:
        for k in dels:
            if k not in order:
                order.append(k)
    rows, conflicts, deleted = [], [], {}
    for k in order:
        bd = max(base_dates.get(k) or "", base_deleted.get(k) or "")
        cs = []
        for lab, d, dels in docs:
            if k in d.hash:
                at, by = dd[lab].get(k, ("", "?"))
                newer_than_frame = k in frame.hash and d.hash[k] != frame.hash[k] and at > (fd.get(k, ("", "?"))[0] or "")
                if at > bd or newer_than_frame:
                    cs.append((at, lab, by, d))
            elif k in dels and (dels[k][0] or "") > bd and (k in frame.hash or any(k in x[1].hash for x in docs)):
                cs.append((dels[k][0], lab, dels[k][1], None))
        late = []          # edited after the version the frame's edit started from, but older than it: lost already
        if k in frame.hash:
            ffrom = frame.unit(k)[0].get(FROM_ATTR) or ""
            for lab, d, dels in docs:
                if k in d.hash and d.hash[k] != frame.hash[k]:
                    at, by = dd[lab].get(k, ("", "?"))
                    if ffrom and ffrom < at < (fd.get(k, ("", "?"))[0] or ""):
                        late.append((at, lab, by, d))
        uniq, seen = [], set()
        for c in sorted(cs, key=lambda c: (c[0], c[1]), reverse=True):   # newest first; the same content once
            key = (c[3].hash[k] if c[3] is not None else None, c[0])
            if key in seen:
                continue
            seen.add(key)
            uniq.append(c)
        win_h = uniq[0][3].hash[k] if uniq and uniq[0][3] is not None else (frame.hash.get(k) if not uniq else None)
        done_h = set([win_h])
        for at2, lab2, by2, d2 in late:
            if d2.hash[k] not in done_h:
                done_h.add(d2.hash[k])
                conflicts.append((k, by2, at2, unit_svg(d2, k), lab2))
        if not uniq:
            if k in frame.hash:
                at, by = fd.get(k, ("", "?"))
                rows.append((k, "kept", frame_label, at, by))
            continue
        at, lab, by, d = uniq[0]
        if d is None:
            if k in frame.hash:
                comp.remove(k)
            deleted[k] = [at, by]
            rows.append((k, "deleted", lab, at, by))
        else:
            if not (k in frame.hash and frame.hash[k] == d.hash[k]):
                hint = order[order.index(k) + 1:]
                comp.put(k, d, lab, hint)
            el, _ = Doc_unit(comp.root, k)
            if el is not None:
                set_date(el, at, by)
            rows.append((k, "changed" if k in frame.hash else "added", lab, at, by))
            frm = (d.unit(k)[0].get(FROM_ATTR) or "") if d.unit(k)[0] is not None else ""
            fat, fby = fd.get(k, ("", "?"))
            if k in frame.hash and frame.hash[k] != d.hash[k] and fat > frm and \
                    not any(c[3] is not None and c[3].hash[k] == frame.hash[k] for c in uniq[1:]):
                # the edit started from an older version than the one it replaces: that one is saved too
                conflicts.append((k, fby, fat, unit_svg(frame, k), frame_label))
        for at2, lab2, by2, d2 in uniq[1:]:
            if d2 is None or (d is not None and d2.hash[k] == d.hash[k]) or d2.hash[k] in done_h:
                continue
            done_h.add(d2.hash[k])
            conflicts.append((k, by2, at2, unit_svg(d2, k), lab2))
    out = to_bytes(comp.root)
    return out, rows, conflicts, deleted


_INFO = {}


def doc_info(data):
    """(unit hashes, unit dates) of a file, read once per run"""
    k = hashlib.sha1(data).hexdigest()
    if k not in _INFO:
        d = Doc(data, "x")
        _INFO[k] = (d.hash, doc_dates(d))
    return _INFO[k]


def unit_table(data):
    h, dates = doc_info(data)
    return dict((k, (h[k], dates.get(k, ("", ""))[0])) for k in h)


def add_seed(data, seed_data, now):
    """planting areas (hidden) from the seed, once, when the plan has no planting_area_* layers yet"""
    base = Doc(data, "latest")
    if any(k.startswith("planting_area_") for k in base.hash):
        return data, []
    sd = Doc(seed_data, "seed")
    comp = Composer(base)
    order = [k for k, e, p in base.units]
    hint_keys = [k for k in order if k.lower().startswith(("trees", "planting", "people"))]
    added = []
    for k, e, par in sd.units:
        if not k.startswith("planting_area_"):
            continue
        el = comp.localize(sd, e, "seed")
        el.set("style", (el.get("style") + ";" if el.get("style") else "") + "display:none")
        set_date(el, now, "seed")
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
        added.append(k)
    return to_bytes(comp.root), added


def fill_dates(data, now, by):
    """layers without a date (a plan from before v2) get one"""
    d = Doc(data, "x")
    n = 0
    for k, e, p in d.units:
        if not e.get(DATE_ATTR):
            set_date(e, now, by)
            n += 1
    return (to_bytes(d.root), n) if n else (data, 0)


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
    t = iso_utc(time.time())
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



def stamp_layers(doc, dates):
    """each Rhino layer under masterplan gets its layer's edit date (GitHub time + this PC's time) and editor"""
    try:
        lunit = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_layer_unit") or "{}")
    except Exception:
        lunit = {}
    n = 0
    for l in doc.Layers:
        if l.IsDeleted or not l.FullPath.startswith(ROOT_LAYER + "::"):
            continue
        un = lunit.get(l.FullPath)
        r = dates.get(ukey(un)) if un else None
        if not r:
            continue
        try:
            l.SetUserString("edited", r[0])
            l.SetUserString("edited_pc_time", short(r[0]) + " (" + tz_name() + ")")
            l.SetUserString("edited_by", r[1])
            n += 1
        except Exception:
            pass
    return n


# =====================================================================================================  local files + log
def read_local():
    try:
        return json.load(open(LOCAL_STATE, encoding="utf-8"))
    except Exception:
        return {}


def write_local(loc):
    write_file(LOCAL_STATE, json.dumps(loc, indent=1, sort_keys=True).encode("utf-8"))


def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import threading
    tmp = "%s.%d_%d.tmp" % (path, os.getpid(), threading.get_ident())   # two downloads may write the same picture
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


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


def safe(k):
    return re.sub(r"[^A-Za-z0-9_]+", "_", k).strip("_") or "layer"


def gzip_bytes(data):
    """the cloud keeps files gzipped (a 28 MB SVG becomes a few MB: much faster up and down)"""
    import gzip, io
    bio = io.BytesIO()
    with gzip.GzipFile(fileobj=bio, mode="wb", compresslevel=3, mtime=0) as g:
        g.write(data)
    return bio.getvalue()


def unzip(name, data):
    if data is not None and name.endswith(".gz"):
        import gzip
        return gzip.decompress(data)
    return data


_IMG_RE = re.compile(br"data:image/[^\"'\s)<>]{2000,}")


def plain(name):
    return name[:-3] if name.endswith(".gz") else name


class Cloud(object):
    """cached downloads: Data/shared/cloud/<folder>/<file> (only the current file of each folder is kept)"""

    def __init__(self, gh):
        import threading
        self.gh = gh
        self.ids = {}
        self.lock = threading.Lock()
        self.imgs = None
        self.conf = None

    # ---- pictures: kept once in the cloud folder 'images' (by content), not inside every version
    def image_list(self):
        with self.lock:
            if self.imgs is None:
                self.imgs = dict((nm, aid) for nm, (aid, sz) in self.gh.assets("images").items())
            return self.imgs

    def strip_images(self, data):
        """the pictures embedded in the SVG (data:...) are replaced by bergama-img:<sha1>; new ones are uploaded"""
        found = {}

        def sub(m):
            raw = m.group(0)
            h = hashlib.sha1(raw).hexdigest()
            found[h] = raw
            return b"bergama-img:" + h.encode("ascii")
        out = _IMG_RE.sub(sub, data)
        if found:
            have = self.image_list()
            new = [(h, raw) for h, raw in found.items() if "img_%s.gz" % h not in have]
            for h, raw in found.items():
                self.save_image(h, raw)

            def up(item):
                h, raw = item
                aid, nm = self.gh.upload("images", "img_%s.gz" % h, gzip_bytes(raw), exist_ok=True)
                with self.lock:
                    self.imgs[nm] = aid
            if new:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=min(6, len(new))) as ex:
                    list(ex.map(up, new))
        return out

    def save_image(self, h, raw):
        p = os.path.join(CLOUD_COPY, "images", h)
        if not os.path.isfile(p):
            write_file(p, raw)

    def restore_images(self, data):
        hs = sorted(set(m.decode("ascii") for m in re.findall(br"bergama-img:([0-9a-f]{40})", data)))
        if not hs:
            return data
        miss = [h for h in hs if not os.path.isfile(os.path.join(CLOUD_COPY, "images", h))]
        if miss:
            have = self.image_list()

            def down(h):
                aid = have.get("img_%s.gz" % h)
                if aid is None:
                    raise RuntimeError("picture %s is missing in the cloud folder 'images'" % h)
                self.save_image(h, unzip(".gz", self.gh.download(aid)))
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=min(6, len(miss))) as ex:
                list(ex.map(down, miss))
        pics = dict((h, open(os.path.join(CLOUD_COPY, "images", h), "rb").read()) for h in hs)
        return re.sub(br"bergama-img:([0-9a-f]{40})", lambda m: pics[m.group(1).decode("ascii")], data)

    def asset_id(self, folder, name):
        if (folder, name) not in self.ids:
            for nm, (aid, sz) in self.gh.assets(folder).items():
                self.ids[(folder, nm)] = aid
        return self.ids.get((folder, name))

    def has_conflict(self, name):
        """is this losing version already in the cloud folder 'conflicts' (listed once per run)"""
        with self.lock:
            if self.conf is None:
                self.conf = set(self.gh.assets("conflicts"))
        return (name + ".gz") in self.conf

    def forget(self, aids):
        for key in [kk for kk, v in self.ids.items() if v in aids]:
            del self.ids[key]
            if self.conf is not None and key[0] == "conflicts":
                self.conf.discard(key[1])

    def get(self, folder, name):
        if not name:
            return None, False
        p = os.path.join(CLOUD_COPY, folder, name)
        if os.path.isfile(p):
            return self.restore_images(unzip(name, open(p, "rb").read())), False
        aid = self.asset_id(folder, name)
        if aid is None:
            raise RuntimeError("the cloud register names %s/%s but the file is not there" % (folder, name))
        data = self.gh.download(aid)
        self.keep(folder, name, data)
        return self.restore_images(unzip(name, data)), True

    def get_many(self, pairs):
        """several downloads at the same time: [(folder, name)] -> [(data, new)]"""
        if len(pairs) < 2:
            return [self.get(f, n) for f, n in pairs]
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(pairs)) as ex:
            return list(ex.map(lambda fn: self.get(*fn), pairs))

    def put_many(self, items, sent):
        """several uploads at the same time: [(folder, name, data)] -> [name]"""
        if len(items) < 2:
            return [self.put(f, n, d, sent) for f, n, d in items]
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=min(6, len(items))) as ex:
            return list(ex.map(lambda it: self.put(it[0], it[1], it[2], sent), items))

    def keep(self, folder, name, data):
        d = os.path.join(CLOUD_COPY, folder)
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f != name:
                try:
                    os.remove(os.path.join(d, f))
                except Exception:
                    pass
        write_file(os.path.join(d, name), data)

    def put(self, folder, name, data, sent):
        if not name.endswith(".gz"):
            name += ".gz"
        data = gzip_bytes(self.strip_images(data))
        aid, nm = self.gh.upload(folder, name, data)
        self.ids[(folder, nm)] = aid
        if folder == "conflicts" and self.conf is not None:
            self.conf.add(nm)
        sent.append(aid)
        if folder != "conflicts":
            self.keep(folder, nm, data)
        return nm

    def trim(self, folder, current, notes):
        """the KEEP_VERSIONS newest files of a folder stay; older ones are deleted"""
        names = sorted(self.gh.assets(folder).items(), key=lambda kv: kv[0], reverse=True)
        gone = 0
        for i, (nm, (aid, sz)) in enumerate(names):
            if i >= KEEP_VERSIONS and nm != current:
                self.gh.delete(aid)
                gone += 1
        if gone:
            notes.append(u"   %s: %d old version(s) removed (the %d newest are kept)" % (folder, gone, KEEP_VERSIONS))
        return [nm for nm, v in names[:KEEP_VERSIONS]]


def snapshot(state):
    """what the register says about the files (who uploaded what, which layers were deleted)"""
    return hashlib.sha1(json.dumps([state.get("files") or {}, state.get("deleted") or {}],
                                   sort_keys=True).encode("utf-8")).hexdigest()


def newest_3dm():
    cands = []
    for dp, dn, fn in os.walk(BERGAMA_ROOT):
        if dp.count(os.sep) - BERGAMA_ROOT.count(os.sep) >= 2:
            dn[:] = []
        cands += [os.path.join(dp, x) for x in fn if x.lower().endswith(".3dm")]
    return max(cands, key=os.path.getmtime) if cands else None


def conflict_name(k, by, at):
    return "%s_%s_%s.svg" % (safe(k), safe(by), fname_time(at) if at else "nodate")


# =====================================================================================================  main (one sync)
def main(gh=None, me=None, notes=None, analysis=True):
    t0 = time.time()
    notes = notes if notes is not None else []
    notes.append(u"%s %s · times in this log: %s" % (GH_LABEL, VERSION, tz_name()))
    if gh is None:
        token, me, _st = read_settings()
        gh = GitHub(token)
    cloud = Cloud(gh)
    head = gh.head()                                      # its reply also gives GitHub's clock
    now = gh.now()
    notes.append(u"you: %s · %s · cloud: github.com/%s (folders = Releases; register on branch %s)" %
                 (me, short(now), REPO, BRANCH))
    loc = read_local()
    os.makedirs(SH_DIR, exist_ok=True)
    state, tree = gh.read_state(head)
    files = state.get("files", {})
    # ---- your file (the first time: the latest combined file, so nothing counts as your edit)
    if not os.path.isfile(MY_FILE):
        lat, _ = cloud.get("latest", files.get("latest"))
        if lat:
            write_file(MY_FILE, lat)
            write_file(BASE_FILE, lat)
            notes.append(u"your file made from the cloud's latest combined file")
        else:
            try:
                fs = [os.path.join(PLAN_DIR, f) for f in os.listdir(PLAN_DIR)
                      if f.lower().endswith(".svg") and os.path.join(PLAN_DIR, f) != PLAN_FILE]
            except Exception:
                fs = []
            if not fs and os.path.isfile(PLAN_FILE):
                fs = [PLAN_FILE]
            if not fs:
                raise RuntimeError("no plan to start from: put the plan SVG in %s" % PLAN_DIR)
            newest = max(fs, key=os.path.getmtime)
            write_file(MY_FILE, open(newest, "rb").read())
            notes.append(u"your file made from %s (the cloud is empty: this is the first run)" % newest)
    if not os.path.isfile(BASE_FILE) and files.get("latest"):
        # a file on this PC but no record of the last sync: which layers were edited here cannot be told, so the
        # file is set aside whole (nothing lost) and this PC starts from the latest combined file
        lat, _ = cloud.get("latest", files["latest"])
        old = os.path.join(CONFLICT_DIR, "my_masterplan_before_first_sync_%s.svg" % fname_time(now))
        write_file(old, open(MY_FILE, "rb").read())
        write_file(MY_FILE, lat)
        write_file(BASE_FILE, lat)
        notes.append(u"FLAG this PC had a masterplan file but no record of its last sync: it was set aside as %s and "
                     u"your file now starts from the latest combined file. Copy any layer you still need from it, "
                     u"save, and run again" % old)
    my = open(MY_FILE, "rb").read()
    base = open(BASE_FILE, "rb").read() if os.path.isfile(BASE_FILE) else None
    # ---- quick exit: nothing edited here and nothing new in the cloud since this PC's last sync
    try:
        placing0 = json.load(open(PLACING_FILE, encoding="utf-8")) if os.path.isfile(PLACING_FILE) else None
    except Exception:
        placing0 = None
    if base is not None and my == base and loc.get("snap") == snapshot(state) and os.path.isfile(PLAN_FILE) \
            and (not placing0 or placing0 == state.get("placing")):
        notes.append(u"0-4 nothing edited on this PC and nothing new in the cloud since your last sync: "
                     u"no download, no upload")
        if analysis:
            step5(state.get("placing") or placing0, notes)
        notes.append(u"%.1f s" % (time.time() - t0))
        return u"\n".join(notes), my
    # ---- 0 date stamp
    saved = iso_utc(os.path.getmtime(MY_FILE) + (gh.offset or 0.0))   # the PC's save time, on GitHub's clock
    my, stamped, my_del = stamp(my, base, now, me, (state.get("dates") or {}), saved)
    write_file(MY_FILE, my)
    notes.append(u"0 your edits since your last sync on this PC: %s%s" % (
        u", ".join(stamped) if stamped else u"none",
        (u"; deleted: " + u", ".join(sorted(my_del))) if my_del else u""))
    base_dates = dict((k, v[0]) for k, v in doc_info(base)[1].items()) if base else {}
    base_del = dict((k, v[0]) for k, v in (loc.get("base_deleted") or {}).items())
    conflicts_all, local_conf, done_conf = [], [], set()
    # ---- 1 your folder
    fresh = True                                          # the register just read is still current
    for attempt in range(5):
        if not fresh:
            head = gh.head()
            state, tree = gh.read_state(head)
        fresh = False
        files = state.setdefault("files", {})
        dels = state.setdefault("deleted", {})
        if attempt == 0:                                  # your folder and everything step 2 needs, at the same time
            cloud.get_many([(f, files.get(f)) for f in PEOPLE + ("latest",)])
        O, got = cloud.get(me, files.get(me))
        sent = []
        if O is None:
            mine, rows1, conf1, d1 = my, [], [], dict(my_del)
        else:
            mine, rows1, conf1, d1 = merge_layers(O, "your folder", base_dates, base_del,
                                                  [("this PC", my, my_del), ("your other PC", O, dels.get(me, {}))], now)
        conf1 = [c for c in conf1 if not cloud.has_conflict(conflict_name(c[0], c[1], c[2]))]   # saved before
        if O is not None and not conf1 and unit_table(mine) == unit_table(O):
            notes.append(u"1 your folder: already up to date")
            fresh = True
            break
        try:
            nm = cloud.put(me, "masterplan_%s.svg" % fname_time(now), mine, sent)
            cn = []
            for k, by, at, data, lab in conf1:
                cn.append(cloud.put("conflicts", conflict_name(k, by, at), data, sent))
                local_conf.append((plain(cn[-1]), data))
                done_conf.add(conflict_name(k, by, at))
            files[me] = nm
            md = dict(dels.get(me, {}))
            md.update(d1)
            md.update(my_del)
            dels[me] = dict((k, v) for k, v in md.items() if k not in doc_info(mine)[0])
            state["updated"], state["by"] = now, me
            head, tree = gh.write_state(head, tree, state,
                                        u"%s: upload %s%s" % (me, nm, (u" · conflicts: " + u", ".join(cn)) if cn else u""))
            fresh = True
        except Retry:
            for aid in sent:
                gh.delete(aid)
            cloud.forget(sent)
            notes.append(u"   somebody uploaded at the same moment: again")
            continue
        notes.append(u"1 your folder: uploaded %s (%.1f MB)%s" % (nm, len(mine) / 1048576.0,
                                                                (u", %d conflict(s)" % len(conf1)) if conf1 else u""))
        conflicts_all += conf1
        cloud.trim(me, nm, notes)
        break
    else:
        raise RuntimeError("the cloud kept changing during 5 uploads of your folder: run again")
    # ---- 2-4 download all, merge, upload latest
    seed = open(SEED_FILE, "rb").read() if os.path.isfile(SEED_FILE) else None
    placing = None
    if os.path.isfile(PLACING_FILE):
        try:
            placing = json.load(open(PLACING_FILE, encoding="utf-8"))
        except Exception:
            placing = None
    vers = None
    for attempt in range(5):
        if not fresh:
            head = gh.head()
            state, tree = gh.read_state(head)
        fresh = False
        files = state.setdefault("files", {})
        dels = state.setdefault("deleted", {})
        sent, got, people = [], [], []
        res = cloud.get_many([(p, files.get(p)) for p in PEOPLE + ("latest",)])
        for p, (data, new) in zip(PEOPLE, res):
            if data:
                people.append((p, data, dels.get(p, {})))
                if new:
                    got.append(p)
        latest, new = res[-1]
        if new:
            got.append("latest")
        notes.append(u"2 downloaded: %s (the rest was already on this PC)" % (u", ".join(got) or u"nothing new"))
        if latest is None:
            out = dict((p, d) for p, d, x in people).get(me) or my
            out, n0 = fill_dates(out, now, me)
            rows = [(k, "added", me, a, b) for k, (a, b) in doc_info(out)[1].items()]
            conf2, d2 = [], {}
            notes.append(u"3 first combined file: made from %s's folder" % me)
        else:
            ld = doc_info(latest)[1]
            out, rows, conf2, d2 = merge_layers(latest, "latest", dict((k, v[0]) for k, v in ld.items()),
                                                dict((k, v[0]) for k, v in dels.get("latest", {}).items()), people, now)
        added = []
        if seed:
            out, added = add_seed(out, seed, now)
        else:
            notes.append(u"FLAG no %s: planting areas cannot be added" % SEED_FILE)
        new_placing = bool(placing) and placing != state.get("placing")
        if new_placing:
            state["placing"] = placing
        changed = latest is None or unit_table(out) != unit_table(latest)
        conf2 = [c for c in conf2 if conflict_name(c[0], c[1], c[2]) not in done_conf      # saved in step 1
                 and not cloud.has_conflict(conflict_name(c[0], c[1], c[2]))]               # or before
        if not changed and not new_placing and not conf2:
            notes.append(u"3 merge: nothing changed")
            break
        try:
            ups = [("latest", "masterplan_%s.svg" % fname_time(now), out)] if changed else []
            ups += [("conflicts", conflict_name(k, by, at), data) for k, by, at, data, lab in conf2]
            names = cloud.put_many(ups, sent)
            if changed:
                files["latest"] = names.pop(0)
            cn = names
            for nm_, (k, by, at, data, lab) in zip(cn, conf2):
                local_conf.append((plain(nm_), data))
            ld_ = dict(dels.get("latest", {}))
            ld_.update(d2)
            dels["latest"] = dict((k, v) for k, v in ld_.items() if k not in doc_info(out)[0])
            state["dates"] = dict((k, list(v)) for k, v in doc_info(out)[1].items())
            state["updated"], state["by"] = now, me
            head, tree = gh.write_state(head, tree, state, u"%s: combined %s · %s" % (
                me, files.get("latest"), u", ".join(u"%s from %s" % (r[0], r[2]) for r in rows if r[1] != "kept")[:300]
                or u"no layer changes"))
        except Retry:
            for aid in sent:
                gh.delete(aid)
            cloud.forget(sent)
            notes.append(u"   somebody uploaded at the same moment: merging again")
            continue
        conflicts_all += conf2
        if changed:
            notes.append(u"4 uploaded the combined file to latest: %s" % files["latest"])
            vers = cloud.trim("latest", files["latest"], notes)
        break
    else:
        raise RuntimeError("the cloud kept changing during 5 merges: run again")
    # ---- merge report
    if latest is not None or rows:
        notes.append(u"merge report (per layer: kept from · edited (%s) · by):" % tz_name())
        for k, act, lab, at, by in sorted(rows, key=lambda r: (r[1] == "kept", r[0])):
            notes.append(u"   %-40s %-8s %-12s %s · %s" % (k, act, lab, short(at), by))
    for k in added:
        notes.append(u"   %-40s added (hidden, planting area from the seed)" % k)
    for k, by, at, data, lab in conflicts_all:
        notes.append(u"FLAG conflict: '%s' by %s (edited %s) lost to a newer edit: saved as %s in conflicts" %
                     (k, by, short(at), conflict_name(k, by, at)))
    for nm, data in local_conf:
        write_file(os.path.join(CONFLICT_DIR, nm), data)
    if local_conf:
        notes.append(u"conflict copies: cloud folder 'conflicts' and %s" % CONFLICT_DIR)
    # ---- local copies: your file = the combined file
    write_file(MY_FILE + ".prev.svg", my)
    write_file(MY_FILE, out)
    write_file(BASE_FILE, out)
    write_file(PLAN_FILE, out)
    loc.update(last_sync=now, base_deleted=dels.get("latest", {}), latest=files.get("latest"),
               placing=state.get("placing") or placing, snap=snapshot(state))
    write_local(loc)
    notes.append(u"your file %s is now the combined file (your previous file: my_masterplan.svg.prev.svg)" % MY_FILE)
    f3 = newest_3dm()
    if f3 and os.path.getmtime(f3) > (loc.get("rhino_hook_saved") or 0) + 120 and loc.get("rhino_hook_saved"):
        notes.append(u"FLAG %s was saved in Rhino without Bergama.bat: open Rhino with option 1 so those edits are "
                     u"picked up" % os.path.basename(f3))
    save_unit_cache()
    # ---- 5 rebuild the planting analysis from the combined file (Bergama.bat does it after the app has opened)
    if analysis:
        step5(state.get("placing") or placing, notes)
    # ---- versions
    try:
        vers = vers or sorted(gh.assets("latest"), reverse=True)[:KEEP_VERSIONS]
        notes.append(u"latest: the %d versions in the cloud (newest first):" % len(vers))
        for v in vers:
            m_ = re.search(r"(\d{4}-\d\d-\d\d)_(\d\d)(\d\d)(\d\d)", v)
            notes.append(u"   %s%s" % (v, (u"  (%s)" % short("%sT%s:%s:%sZ" % m_.groups())) if m_ else u""))
    except Exception as ex:
        notes.append(u"versions not listed: %s" % ex)
    notes.append(u"%.1f s" % (time.time() - t0))
    return u"\n".join(notes), out


# =====================================================================================================  5 planting analysis
def load_script(fname):
    """another Bergama script next to this one, loaded as a module (its Grasshopper part does not run)"""
    import importlib.util
    for d in (HERE, BERGAMA_ROOT):
        p = os.path.join(d, fname)
        if os.path.isfile(p):
            sp = importlib.util.spec_from_file_location(fname[:-3], p)
            m = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(m)
            return m
    raise RuntimeError("%s is missing in %s" % (fname, BERGAMA_ROOT))


def analysis_data(plan_file, placing, notes, PTR=None, PA=None):
    """what the planting analysis needs, read from the combined SVG (survey metres via PlanToRhino's placing)"""
    PTR = PTR or load_script(PTR_FILE)
    PA = PA or load_script(PA_FILE)
    M = tuple(placing["M"])
    Mi = PA.inv(M)
    plan = PTR.Plan(plan_file)
    d = Doc(open(plan_file, "rb").read(), "x")

    def ring(subs):
        out = []
        for cl, sg in subs:
            P = [sg[0]] + [seg[-1] for seg in sg[1:]]
            out.append([PA.mat_pt(M, p) for p in P])
        return out
    data = {"areas": {}, "water": [], "paths_fill": [], "paths_line": [], "roads": [], "heritage": [], "trees": []}
    sym_re = re.compile(r"sym_(" + "|".join(sorted(PA.TREES, key=len, reverse=True)) + r")\b")
    for it in plan.items:
        lay = PTR.layer_for(it["top"]) or ""
        if it["kind"] == "block":
            m_ = sym_re.search(it.get("sym") or "")
            if m_:
                vb = [float(x) for x in _NUM.findall((d.ids.get(it["sym"]).get("viewBox") if d.ids.get(it["sym"]) is not None
                                                      else "") or "")] or [0.0, 0.0, 0.0, 0.0]
                c = PA.mat_pt(it["m"], (vb[0] + vb[2] / 2.0, vb[1] + vb[3] / 2.0))   # the tree's centre
                data["trees"].append((m_.group(1),) + PA.mat_pt(M, c))
            continue
        if it["kind"] != "shape":
            continue
        rs = ring(it["subs"])
        f = it.get("fill")
        if lay.startswith("proposal_planting_") and f:
            data["areas"].setdefault(lay[len("proposal_planting_"):], []).append(PA.Region(rs))
        elif lay == "proposal_water" and f and f[2] > f[0] + 15 and f[2] >= f[1] - 25:
            data["water"].append(PA.Region(rs))
        elif lay == "proposal_paths":
            if f:
                data["paths_fill"].append(PA.Region(rs))
            else:
                data["paths_line"] += [r for r in rs if len(r) > 1]
        elif lay == "existing_roads" and f:
            r_ = PA.Region(rs)
            per = sum(math.hypot(r[i][0] - r[i - 1][0], r[i][1] - r[i - 1][1]) for r in r_.rings for i in range(len(r)))
            r_.width = 2.0 * r_.area / per if per else 0.0
            data["roads"].append(r_)
        elif lay == "existing_heritage" and f:
            data["heritage"].append(PA.Region(rs))
    missing = [k for k in PA.KEYS + ["meadow_lawn"] if k not in data["areas"]]
    if missing:
        notes.append(u"FLAG no planting area layer for: " + u", ".join(missing))
    data["to_svg"] = lambda p: PA.mat_pt(Mi, p)
    data["m_per_unit"] = math.sqrt(abs(M[0] * M[3] - M[1] * M[2]))
    a0, a1 = PA.mat_pt(Mi, (0.0, 0.0)), PA.mat_pt(Mi, (0.0, 100.0))
    L = math.hypot(a1[0] - a0[0], a1[1] - a0[1]) or 1.0
    data["north"] = ((a1[0] - a0[0]) / L, (a1[1] - a0[1]) / L)
    allp = [p for v in data["areas"].values() for r_ in v for r in r_.rings for p in r] or \
        [(t[1], t[2]) for t in data["trees"]] or [(0.0, 0.0)]
    data["plan_bb"] = (min(p[0] for p in allp), min(p[1] for p in allp), max(p[0] for p in allp), max(p[1] for p in allp))
    data["u"] = float(placing.get("u") or 1.0)
    notes.append(u"read for the analysis: %d area pieces, %d water, %d path fills + %d lines, %d roads, %d heritage, %d trees"
                 % (sum(len(v) for v in data["areas"].values()), len(data["water"]), len(data["paths_fill"]),
                    len(data["paths_line"]), len(data["roads"]), len(data["heritage"]), len(data["trees"])))
    return data, PA


def step5(placing, notes, doc=None):
    """the analysis is rebuilt only when the combined file, the placing or the two scripts changed"""
    try:
        h = hashlib.sha1(open(PLAN_FILE, "rb").read())
        h.update(json.dumps(placing, sort_keys=True).encode("utf-8"))
        for f in (PTR_FILE, PA_FILE):
            for d in (HERE, BERGAMA_ROOT):
                q = os.path.join(d, f)
                if os.path.isfile(q):
                    h.update(("%s %d %d" % (f, os.path.getsize(q), int(os.path.getmtime(q)))).encode("utf-8"))
                    break
        key = h.hexdigest()
        old = doc.Strings.GetValue(SYNC_KEY, "analysis_key") if doc is not None else read_local().get("analysis_key")
        if placing and old == key:
            notes.append(u"5 planting analysis: already up to date (nothing it uses has changed)")
            return
        rebuild_analysis(PLAN_FILE, placing, notes, doc=doc)
        if placing and doc is not None:
            doc.Strings.SetString(SYNC_KEY, "analysis_key", key)
        elif placing:
            loc = read_local()
            loc["analysis_key"] = key
            write_local(loc)
    except Exception as ex:
        notes.append(u"FLAG planting analysis not rebuilt: %s: %s" % (type(ex).__name__, ex))


def rebuild_analysis(plan_file, placing, notes, doc=None):
    if not placing:
        notes.append(u"5 planting analysis: waits for the plan's survey placing (open Rhino once with option 1)")
        return
    data, PA = analysis_data(plan_file, placing, notes)
    res = PA.main(doc=doc, data=data)
    keep = [l for l in res.split("\n") if "board SVG" in l or "FLAG" in l or "WARNING" in l]
    notes.append(u"5 planting analysis rebuilt from the combined file" + (u": " if keep else u"") + u" / ".join(keep))


# =====================================================================================================  Rhino (opened by Bergama.bat)
def rhino_session():
    """runs inside Rhino (Bergama.bat starts Rhino with this file): load the combined file into the layers, rebuild the
    planting analysis, and from now on write the layers you change into your shared file each time you save.
    Bergama.bat uploads them when Rhino closes. Nothing is installed in Rhino."""
    import Rhino
    import scriptcontext as sc
    notes = LiveNotes(u"")
    notes.append(u"%s %s in Rhino · times: %s" % (GH_LABEL, VERSION, tz_name()))

    def on_open(doc):
        try:
            if os.path.isfile(MY_FILE):                 # edits saved in this .3dm without Bergama.bat
                new, done = rhino_edits(doc, open(MY_FILE, "rb").read(), notes)
                if new is not None:
                    write_file(MY_FILE, new)
                    notes.append(u"FLAG Rhino edits that were not synced yet are now in your file (uploaded at the "
                                 u"next sync): " + u", ".join(sorted(done)))
            if not os.path.isfile(PLAN_FILE):
                notes.append(u"FLAG no combined file %s yet: run Bergama.bat first" % PLAN_FILE)
                return
            sha = git_sha(open(PLAN_FILE, "rb").read())
            if doc.Strings.GetValue(SYNC_KEY, "baked_sha") != sha:
                doc.Strings.SetString(SYNC_KEY, "rebake_all", "1")
                PTR = load_script(PTR_FILE)
                res = PTR.main(True, False)
                notes.append(u"combined file loaded into the Rhino layers (PlanToRhino v2): " +
                             u" / ".join(l for l in (res or u"").split("\n")[-3:] if l.strip()))
                doc.Strings.SetString(SYNC_KEY, "baked_sha", sha)
            else:
                notes.append(u"the Rhino layers already show the combined file")
            mx = doc.Strings.GetValue(PTR_KEY, "v2_matrix")
            if mx:
                write_file(PLACING_FILE, mx.encode("utf-8"))
            n = stamp_layers(doc, doc_dates(Doc(open(PLAN_FILE, "rb").read(), "x")))
            notes.append(u"edit dates on %d Rhino layers (layer user text edited / edited_pc_time / edited_by)" % n)
            if mx:
                step5(json.loads(mx), notes, doc=doc)
            doc.Views.Redraw()
        except Exception as ex:
            import traceback
            notes.append(u"ERROR %s: %s\n%s" % (type(ex).__name__, ex, traceback.format_exc()[-800:]))
            show_error(u"Rhino: %s: %s" % (type(ex).__name__, ex))

    def on_save(sender, e):
        try:
            if getattr(e, "ExportSelected", False):
                return
            doc = e.Document
            if not os.path.isfile(MY_FILE):
                return
            new, done = rhino_edits(doc, open(MY_FILE, "rb").read(), notes)
            if new is not None:
                write_file(MY_FILE, new)
                notes.append(u"saved in Rhino: your changed layers are in your file (uploaded when Rhino closes): " +
                             u", ".join(sorted(done)))
            loc = read_local()
            loc["rhino_hook_saved"] = time.time()
            write_local(loc)
        except Exception as ex:
            notes.append(u"ERROR on save %s: %s" % (type(ex).__name__, ex))
            show_error(u"Rhino save: %s: %s" % (type(ex).__name__, ex))

    old = sc.sticky.get("bergama_on_save")
    if old is not None:
        try:
            Rhino.RhinoDoc.EndSaveDocument -= old
        except Exception:
            pass
    Rhino.RhinoDoc.EndSaveDocument += on_save
    sc.sticky["bergama_on_save"] = on_save
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is not None and doc.Path:
        on_open(doc)
    else:                                               # the file is still opening: do it once it is open
        def once(sender, e):
            try:
                Rhino.RhinoDoc.EndOpenDocumentInitialViewUpdate -= sc.sticky.get("bergama_on_open")
            except Exception:
                pass
            on_open(e.Document)
        sc.sticky["bergama_on_open"] = once
        Rhino.RhinoDoc.EndOpenDocumentInitialViewUpdate += once


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


def short_path(p):
    """the Windows 8.3 form of a path (no spaces) so Rhino's command line reads it; the path itself elsewhere"""
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(1024)
        n = ctypes.windll.kernel32.GetShortPathNameW(p, buf, 1024)
        return buf.value if 0 < n < 1024 else p
    except Exception:
        return p


def cli(app):
    """Bergama.bat: sync, open the combined file in the chosen app, sync again when the app is closed"""
    import subprocess
    log = []
    notify("Bergama", "syncing the masterplan ... (%s opens when it is done)" % ("Rhino" if app == "rhino" else "Illustrator"))

    def run_sync(tag, analysis=True):
        head = u"\n\n".join(log) + u"\n\n==== %s · %s\n" % (tag, time.strftime("%d %b %H:%M (") + tz_name() + ")")
        live = LiveNotes(head)
        try:
            txt, _ = main(notes=live, analysis=analysis)
            ok = True
        except Exception as ex:
            import traceback
            txt = u"\n".join(live) + u"\nERROR: %s: %s\n%s" % (type(ex).__name__, ex, traceback.format_exc()[-800:])
            ok = False
            write_log(head + txt)
            show_error(u"%s: %s\n\n(step reached: %s)" % (type(ex).__name__, ex, live[-1] if live else "start"))
        log.append(u"==== %s\n%s" % (tag, txt))
        write_log(u"\n\n".join(log))
        flags = [l for l in txt.split("\n") if "FLAG" in l]
        if ok:
            notify("Bergama sync done", (u"%d conflict / flag line(s): see the log" % len(flags)) if flags
                   else u"the combined file is up to date")
        return ok
    pf = [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]
    if not run_sync("sync before opening", analysis=False):
        return
    try:
        _t, _m, st = read_settings()
    except Exception:
        st = {}
    t0 = os.path.getmtime(MY_FILE)
    if app == "rhino":
        exe = st.get("rhino_exe") or find_exe([os.path.join(p, "Rhino 8", "System", "Rhino.exe") for p in pf])
        f = st.get("rhino_file") or newest_3dm()
        if not exe:
            show_error("Rhino 8 not found: add a line rhino_exe=<path to Rhino.exe> to " + SETTINGS_FILE)
            return
        me_py = short_path(os.path.abspath(__file__))
        cmd = '"%s" /nosplash /runscript="_-RunPythonScript %s" %s' % (exe, me_py, ('"%s"' % f) if f else "")
        subprocess.Popen(cmd)
        log.append(u"opened Rhino: %s (Rhino loads the combined file and keeps your saves in your shared file)" % (f or "-"))
        image = "Rhino.exe"
    else:
        exe = st.get("illustrator_exe") or find_exe([os.path.join(p, "Adobe", "Adobe Illustrator*", "Support Files", "Contents",
                                                                  "Windows", "Illustrator.exe") for p in pf])
        if not exe:
            show_error("Illustrator not found: add a line illustrator_exe=<path to Illustrator.exe> to " + SETTINGS_FILE)
            return
        subprocess.Popen([exe, MY_FILE])
        log.append(u"opened Illustrator: %s (save as SVG, Decimal Places 7; close Illustrator to upload)" % MY_FILE)
        image = "Illustrator.exe"
    write_log(u"\n\n".join(log))
    if app != "rhino":                                     # Rhino rebuilds it itself when the file opens
        n5 = []
        step5(_placing(), n5)
        log.extend(n5)
        write_log(u"\n\n".join(log))
    time.sleep(20)
    while running(image):
        time.sleep(10)
    if os.path.getmtime(MY_FILE) != t0:
        run_sync("sync after %s closed" % ("Rhino" if app == "rhino" else "Illustrator"))
    else:
        log.append(u"%s closed without saving changes: nothing to upload" % ("Rhino" if app == "rhino" else "Illustrator"))
        write_log(u"\n\n".join(log))


def _placing():
    """the survey placing the last sync used (the cloud's, or this PC's own)"""
    return read_local().get("placing")


def _in_rhino():
    try:
        import Rhino   # noqa: F401
        return True
    except Exception:
        return False


if __name__ == "__main__" and "ghenv" not in globals():
    if _in_rhino():
        rhino_session()
    else:
        import sys as _sys
        _app = (_sys.argv[1] if len(_sys.argv) > 1 else "").lower()
        if _app in ("rhino", "illustrator"):
            try:
                cli(_app)
            except Exception as _ex:
                import traceback as _tb
                write_log(u"ERROR while opening %s: %s: %s\n%s" % (_app, type(_ex).__name__, _ex, _tb.format_exc()[-800:]))
                show_error(u"opening %s: %s: %s" % (_app, type(_ex).__name__, _ex))
        else:
            print(main()[0])
