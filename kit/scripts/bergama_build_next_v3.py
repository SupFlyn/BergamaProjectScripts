# -*- coding: utf-8 -*-
r"""Bergama: one-step AcBuild run with timings (build_next v3, 24 Nov 2026).
v3 (Aras 24 Nov 17:20 UTC: "use the letters like 2.01 is the latest edit according to my feedback ... edits in the night
it would go like 2.01a 2.01b and so on after 2.01z 2.01aa 2.01ab"): AcBuild names with a letter suffix
(bergama_acbuild_v2_09a.py) are found, ordered 2.09 < 2.09a < ... < 2.09z < 2.09aa, and build Bergama_AC_v2.09a.pln.
v2 (Aras 23 Nov 21:11 UTC "run this same script in both pc's ... do a speed comparison like time to build and open up 3D
window, saving and closing"): every step is timed and written to cached\bergama_archicad_site\speed_<PC>_<time>.json;
after the build: a timed save, a timed quit, a timed reopen of the built file, a timed 3D window, a timed quit.
  py -3 bergama_build_next_v2.py build --from Bergama_AC_v1.96.pln     a given source file (default: the newest)
  ... --acbuild bergama_acbuild_v2_02.py                                a given AcBuild version from main
(v1 text below)
Aras 23 Nov 20:41 UTC: "we do that launcher idea for your use just in case", "do the indexing and pointing to that so
you can run that". It does the know-how note's run recipe (library/_index/knowhow/archicad_acbuild.md) in one go:

  0. fetches the newest bergama_acbuild_v*.py from GitHub main into scripts\ (a different local copy of the same
     name is moved to scripts\_replaced\ first, never deleted)
  1. stops if Archicad is already running on this PC (one licence key: close Archicad on the OTHER PC yourself)
  2. moves the AutoSave-Archicad-30* folders and stale .lck files into archicad\_recovery_backup_<date>\ (moved,
     never deleted), so no hidden "Project Recovery" dialog blocks Tapir
  3. copies the newest archicad\Bergama_AC_v*.pln to Bergama_AC_v<AcBuild version>.pln (stops if that file exists)
  4. starts Archicad with the copy and waits until Tapir answers with that project open
  5. runs AcBuild (it saves the project itself at the end)
  6. counts the elements per type (read-only) and compares them with the last run
  7. quits Archicad (restart after every run)

  py -3 bergama_build_next_v1.py            the whole recipe
  py -3 bergama_build_next_v1.py check      only steps 1, 4 (newest Bergama_AC_v*.pln), 6, 7: reopen test + counts

Step lines go to logs\bergama_build_next_status.txt; its last line starts with DONE or ERROR.
Counts per run: cached\bergama_archicad_site\build_next_counts.json.
"""
import datetime, glob, hashlib, json, os, re, runpy, shutil, subprocess, sys, time, urllib.request

_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files", "scripts")) else _BG
SCRIPTS = os.path.join(ROOT, "scripts")
AC_DIR = os.path.join(ROOT, "archicad")
STATUS = os.path.join(ROOT, "logs", "bergama_build_next_status.txt")
COUNTS = os.path.join(ROOT, "cached", "bergama_archicad_site", "build_next_counts.json")
AUTOSAVE = os.path.join(os.path.expanduser("~"), "GRAPHISOFT")
GH_LIST = "https://api.github.com/repos/SupFlyn/BergamaProjectScripts/contents/kit/scripts?ref=main"
PORTS = range(19723, 19744)
OPEN_WAIT_MIN = 30          # minutes for Archicad to open the project (the v1.96 file is 868.5 MB)
QUIT_WAIT_MIN = 10
FROM = []                   # v2: --from source pln name
PIN = []                    # v2: --acbuild <bergama_acbuild_vX_YY.py> (default: the newest on main)
T = {}                      # v2: step -> seconds
MEM = {}                    # v2: step -> Archicad working set (GB) after it
TYPES = ("Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab", "Roof", "Mesh", "Zone",
         "CurtainWall", "Shell", "Skylight", "Morph", "Stair", "Railing", "Opening")


def say(t):
    line = u"%s  %s" % (time.strftime("%H:%M:%S"), t)
    print(line, flush=True)
    with open(STATUS, "a", encoding="utf-8") as f:
        f.write(line + u"\n")


def vkey(p):
    """v3: version order with letter suffixes: v2_09 < v2_09a < v2_09z < v2_09aa (also Bergama_AC_v2.09a.pln)"""
    m = re.search(r"v(\d+)[_.](\d+)([a-z]*)", os.path.basename(p))
    if not m:
        return [-1, -1, 0, u""]
    return [int(m.group(1)), int(m.group(2)), len(m.group(3)), m.group(3)]


def blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fetch_newest():
    """step 0: the newest AcBuild on GitHub main, in scripts\\ (Aras 17 Nov: every script comes from main)"""
    with urllib.request.urlopen(urllib.request.Request(GH_LIST, headers={"User-Agent": "bergama-build-next"}),
                                timeout=60) as f:
        items = json.loads(f.read().decode("utf-8"))
    ac = [i for i in items if re.match(r"bergama_acbuild_v\d+_\d+[a-z]*\.py$", i["name"])]
    if PIN:                                        # --acbuild <name>: that version from main, not the newest
        ac = [i for i in ac if i["name"] == PIN[0]]
        if not ac:
            raise RuntimeError(u"%s is not on GitHub main" % PIN[0])
    top = max(ac, key=lambda i: vkey(i["name"]))
    dst = os.path.join(SCRIPTS, top["name"])
    if os.path.isfile(dst):
        with open(dst, "rb") as f:
            if blob_sha(f.read()) == top["sha"]:
                say(u"AcBuild %s on this PC = GitHub main" % top["name"])
                return dst
        old = os.path.join(SCRIPTS, "_replaced", top["name"] + time.strftime(".%Y%m%d_%H%M%S"))
        os.makedirs(os.path.dirname(old), exist_ok=True)
        shutil.move(dst, old)
        say(u"FLAG local %s differed from main: moved to %s" % (top["name"], old))
    with urllib.request.urlopen(top["download_url"], timeout=300) as f:
        data = f.read()
    if blob_sha(data) != top["sha"]:
        raise RuntimeError(u"download of %s incomplete (checksum differs)" % top["name"])
    with open(dst, "wb") as f:
        f.write(data)
    say(u"AcBuild %s fetched from GitHub main" % top["name"])
    return dst


def timed(step, fn, *a):
    """v2: run one step, keep its seconds and Archicad's memory after it"""
    t0 = time.time()
    r = fn(*a)
    T[step] = round(time.time() - t0, 1)
    MEM[step] = ac_mem_gb()
    say(u"TIME %s: %.0f s%s" % (step, T[step], u"" if MEM[step] is None else u" (Archicad %.1f GB)" % MEM[step]))
    return r


def ac_mem_gb():
    """v2: Archicad's working set from tasklist (GB), None when not running"""
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Archicad.exe", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True).stdout
        kb = [int(re.sub(r"[^\d]", "", l.split('","')[-1]) or 0) for l in out.splitlines() if "archicad" in l.lower()]
        return round(sum(kb) / 1048576.0, 1) if kb else None
    except Exception:
        return None


def open_3d(url):
    """v2: open the 3D window and wait until Archicad answers again (3D built)"""
    tapir(url, "ChangeWindow", {"windowType": "3DModel"}, 7200.0)
    post(url, {"command": "API.IsAlive"}, 7200.0)


def save(url):
    tapir(url, "SaveProject", {}, 7200.0)


def archicad_running():
    out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout.lower()
    return u'"archicad.exe"' in out


def move_leftovers():
    """step 2: crash autosaves + stale locks aside (moved, never deleted)"""
    bk = os.path.join(AC_DIR, "_recovery_backup_" + time.strftime("%Y-%m-%d"))
    found = glob.glob(os.path.join(AUTOSAVE, "AutoSave-Archicad-30*")) + glob.glob(os.path.join(AC_DIR, "*.lck"))
    for p in found:
        os.makedirs(bk, exist_ok=True)
        dst = os.path.join(bk, os.path.basename(p))
        if os.path.exists(dst):
            dst += time.strftime(".%H%M%S")
        shutil.move(p, dst)
    say(u"leftovers moved to %s: %d" % (bk, len(found)) if found else u"no AutoSave folders or .lck files")


def newest_pln():
    fs = glob.glob(os.path.join(AC_DIR, "Bergama_AC_v*.pln"))
    if not fs:
        raise RuntimeError(u"no Bergama_AC_v*.pln in %s" % AC_DIR)
    return max(fs, key=vkey)


def post(url, body, timeout):
    req = urllib.request.Request(url, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.loads(f.read().decode("utf-8"))


def find_ac():
    for p in PORTS:
        try:
            if post("http://127.0.0.1:%d" % p, {"command": "API.IsAlive"}, 2.0).get("result", {}).get("isAlive"):
                return "http://127.0.0.1:%d" % p
        except Exception:
            continue
    return None


def tapir(url, name, params=None, timeout=600.0):
    p = {"addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": name}}
    if params is not None:
        p["addOnCommandParameters"] = params
    r = post(url, {"command": "API.ExecuteAddOnCommand", "parameters": p}, timeout)
    if not r.get("succeeded"):
        raise RuntimeError(u"%s failed: %s" % (name, json.dumps(r.get("error"))[:300]))
    out = (r.get("result") or {}).get("addOnCommandResponse") or {}
    if isinstance(out, dict) and out.get("error"):
        raise RuntimeError(u"%s: %s" % (name, json.dumps(out["error"])[:300]))
    return out


def open_in_archicad(pln):
    """step 4: start Archicad 30 with the project and wait for Tapir with that project open"""
    exe = sorted(glob.glob(r"C:\Program Files\GRAPHISOFT\Archicad 30*\Archicad.exe"))
    if exe:
        subprocess.Popen([exe[-1], pln])
    else:
        os.startfile(pln)
    say(u"Archicad starting with %s (waiting up to %d min)" % (os.path.basename(pln), OPEN_WAIT_MIN))
    t_end = time.time() + 60 * OPEN_WAIT_MIN
    while time.time() < t_end:
        time.sleep(15)
        url = find_ac()
        if not url:
            continue
        try:
            info = tapir(url, "GetProjectInfo")
        except Exception:
            continue
        names = [re.sub(r"\.pln$", u"", os.path.basename(n or u"").lower())
                 for n in (pln, info.get("projectPath"), info.get("projectName"))]   # "v2.00": never splitext
        if names[0] in names[1:]:
            say(u"project open, Tapir answers at %s" % url)
            return url
    raise RuntimeError(u"Archicad did not answer with %s open within %d min (a hidden dialog such as Project "
                       u"Recovery or License Information may be waiting)" % (os.path.basename(pln), OPEN_WAIT_MIN))


def count(url, pln, label):
    """step 6: elements per type (read-only), compared with the last entry"""
    try:
        tapir(url, "ChangeWindow", {"windowType": "FloorPlan"})   # counts list the active window's database
    except Exception as ex:
        say(u"FLAG floor plan not activated (%s): counts may cover only the active window" % ex)
    c = {}
    for t in TYPES:
        try:
            c[t] = len(tapir(url, "GetElementsByType", {"elementType": t}, 1800.0).get("elements") or [])
        except Exception:
            pass                                   # a type this Archicad / Tapir does not know
    c = {k: v for k, v in c.items() if v}
    hist = []
    if os.path.isfile(COUNTS):
        with open(COUNTS, encoding="utf-8") as f:
            hist = json.load(f)
    prev = hist[-1]["counts"] if hist else {}
    rows = [u"%s %d%s" % (k, v, (u" (%+d)" % (v - prev[k])) if k in prev and prev[k] != v else u"")
            for k, v in sorted(c.items(), key=lambda kv: -kv[1])]
    mb = os.path.getsize(pln) / 1048576.0
    say(u"elements %d%s: %s" % (sum(c.values()), (u" (last: %d, %s)" % (sum(prev.values()), hist[-1]["file"]))
                                if prev else u"", u", ".join(rows)))
    say(u"file %s: %.1f MB" % (os.path.basename(pln), mb))
    hist.append({"when": datetime.datetime.now().isoformat(timespec="seconds"), "label": label,
                 "file": os.path.basename(pln), "mb": round(mb, 1), "counts": c})
    os.makedirs(os.path.dirname(COUNTS), exist_ok=True)
    with open(COUNTS, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=1)


def quit_archicad(url):
    """step 7: quit Archicad and wait until its process is gone"""
    try:
        tapir(url, "QuitArchicad", None, 120.0)
    except Exception:
        pass                                       # the connection may drop while Archicad quits
    t_end = time.time() + 60 * QUIT_WAIT_MIN
    while time.time() < t_end:
        time.sleep(10)
        if not archicad_running():
            say(u"Archicad closed")
            return
    raise RuntimeError(u"Archicad still running %d min after Quit (a dialog may be waiting)" % QUIT_WAIT_MIN)


def build():
    try:
        acb = fetch_newest()
    except Exception as ex:                        # no internet: the newest copy already on this PC
        if PIN and u"not on GitHub main" in u"%s" % ex:
            raise
        acb = max(glob.glob(os.path.join(SCRIPTS, "bergama_acbuild_v*.py")), key=vkey)
        say(u"FLAG GitHub not reached (%s): using %s already on this PC" % (ex, os.path.basename(acb)))
    if archicad_running() or find_ac():
        raise RuntimeError(u"Archicad is already running on this PC: save and close it first")
    move_leftovers()
    src = os.path.join(AC_DIR, FROM[0]) if FROM else newest_pln()
    if not os.path.isfile(src):
        raise RuntimeError(u"source %s not found in %s" % (FROM[0], AC_DIR))
    ver = re.search(r"v(\d+)_(\d+)([a-z]*)", os.path.basename(acb))
    dst = os.path.join(AC_DIR, u"Bergama_AC_v%s.%s%s.pln" % ver.groups())
    if os.path.exists(dst):
        raise RuntimeError(u"%s already exists: this version was built before (rename or move it to rebuild)"
                           % os.path.basename(dst))
    timed(u"copy source", shutil.copy2, src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError(u"copy of %s incomplete" % os.path.basename(src))
    say(u"copied %s -> %s" % (os.path.basename(src), os.path.basename(dst)))
    url = timed(u"open project", open_in_archicad, dst)
    say(u"AcBuild %s running (live steps: logs\\bergama_acbuild_progress.txt)" % os.path.basename(acb))
    ns = runpy.run_path(acb, run_name="bergama_launcher")
    res = u"%s" % timed(u"build (AcBuild, incl. its own saves)", ns["_run"])
    try:
        ns["write_log"](res)
    except Exception:
        pass
    lines = [l for l in res.splitlines() if l.strip()]
    if res.startswith(u"ERROR"):
        raise RuntimeError(u"AcBuild stopped: %s (Archicad left open; full log logs\\bergama_acbuild_site_log.txt)"
                           % lines[0][:400])
    flags = [l for l in lines if l.startswith(u"FLAG")]
    say(u"AcBuild finished: %s; %d FLAG lines" % (lines[-1][:300] if lines else u"", len(flags)))
    for l in flags[:10]:
        say(u"  " + l[:300])
    if not any(l.startswith(u"Archicad project saved (end of the run") for l in lines):   # AcBuild's last save
        tapir(url, "SaveProject", {}, 3600.0)
        say(u"project saved by build_next")
    timed(u"save (whole model, after the build)", save, url)
    count(url, dst, u"build")
    timed(u"close (quit Archicad)", quit_archicad, url)
    url = timed(u"reopen built file", open_in_archicad, dst)
    timed(u"open 3D window (fresh start)", open_3d, url)
    timed(u"save (after reopen)", save, url)
    timed(u"close after 3D", quit_archicad, url)
    return dst


def check():
    if archicad_running() or find_ac():
        raise RuntimeError(u"Archicad is already running on this PC: save and close it first")
    move_leftovers()
    pln = newest_pln()
    t0 = time.time()
    url = open_in_archicad(pln)
    say(u"reopen took %.0f s" % (time.time() - t0))
    count(url, pln, u"check")
    quit_archicad(url)
    return pln


def main():
    os.makedirs(os.path.dirname(STATUS), exist_ok=True)
    args = sys.argv[1:]
    if u"--from" in args:
        FROM.append(args[args.index(u"--from") + 1])
    if u"--acbuild" in args:
        PIN.append(args[args.index(u"--acbuild") + 1])
    mode = (args[0] if args and not args[0].startswith(u"--") else u"build").lower()
    with open(STATUS, "w", encoding="utf-8") as f:
        f.write(u"%s  build_next v3 started (%s)\n" % (time.strftime("%H:%M:%S"), mode))
    t0 = time.time()
    try:
        pln = check() if mode == u"check" else build()
        say(u"DONE %s: %s in %.0f min" % (mode, os.path.basename(pln), (time.time() - t0) / 60.0))
    except Exception as ex:
        say(u"ERROR %s: %s" % (type(ex).__name__, ex))
        write_speed(mode, t0)
        sys.exit(1)
    write_speed(mode, t0)


def write_speed(mode, t0):
    """v2: the timings of this run, one file per PC and run"""
    try:
        import ctypes
        class MS(ctypes.Structure):
            _fields_ = [("l", ctypes.c_ulong), ("p", ctypes.c_ulong), ("tot", ctypes.c_ulonglong),
                        ("av", ctypes.c_ulonglong)] + [("x%d" % i, ctypes.c_ulonglong) for i in range(5)]
        m = MS()
        m.l = ctypes.sizeof(MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        ram = round(m.tot / 1073741824.0, 1)
    except Exception:
        ram = None
    pc = os.environ.get("COMPUTERNAME", u"PC")
    d = dict(pc=pc, ram_gb=ram, mode=mode, source=FROM[0] if FROM else u"newest", when=time.strftime("%Y-%m-%d %H:%M"),
             total_s=round(time.time() - t0, 1), seconds=T, archicad_gb_after=MEM)
    f = os.path.join(ROOT, "cached", "bergama_archicad_site", "speed_%s_%s.json" % (pc, time.strftime("%Y%m%d_%H%M")))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=1)
    say(u"timings saved: %s" % f)


if __name__ == "__main__":
    main()
