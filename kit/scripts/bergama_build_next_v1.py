# -*- coding: utf-8 -*-
r"""Bergama: one-step AcBuild run (build_next v1, 23 Nov 2026).
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
TYPES = ("Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab", "Roof", "Mesh", "Zone",
         "CurtainWall", "Shell", "Skylight", "Morph", "Stair", "Railing", "Opening")


def say(t):
    line = u"%s  %s" % (time.strftime("%H:%M:%S"), t)
    print(line, flush=True)
    with open(STATUS, "a", encoding="utf-8") as f:
        f.write(line + u"\n")


def vkey(p):
    return [int(x) for x in re.findall(r"\d+", os.path.basename(p))]


def blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fetch_newest():
    """step 0: the newest AcBuild on GitHub main, in scripts\\ (Aras 17 Nov: every script comes from main)"""
    with urllib.request.urlopen(urllib.request.Request(GH_LIST, headers={"User-Agent": "bergama-build-next"}),
                                timeout=60) as f:
        items = json.loads(f.read().decode("utf-8"))
    ac = [i for i in items if re.match(r"bergama_acbuild_v[\d_]+\.py$", i["name"])]
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
        acb = max(glob.glob(os.path.join(SCRIPTS, "bergama_acbuild_v*.py")), key=vkey)
        say(u"FLAG GitHub not reached (%s): using %s already on this PC" % (ex, os.path.basename(acb)))
    if archicad_running() or find_ac():
        raise RuntimeError(u"Archicad is already running on this PC: save and close it first")
    move_leftovers()
    src = newest_pln()
    ver = re.search(r"v(\d+)_(\d+)", os.path.basename(acb))
    dst = os.path.join(AC_DIR, u"Bergama_AC_v%s.%s.pln" % ver.groups())
    if os.path.exists(dst):
        raise RuntimeError(u"%s already exists: this version was built before (rename or move it to rebuild)"
                           % os.path.basename(dst))
    shutil.copy2(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError(u"copy of %s incomplete" % os.path.basename(src))
    say(u"copied %s -> %s" % (os.path.basename(src), os.path.basename(dst)))
    url = open_in_archicad(dst)
    say(u"AcBuild %s running (live steps: logs\\bergama_acbuild_progress.txt)" % os.path.basename(acb))
    ns = runpy.run_path(acb, run_name="bergama_launcher")
    res = u"%s" % ns["_run"]()
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
    count(url, dst, u"build")
    quit_archicad(url)
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
    mode = (sys.argv[1] if len(sys.argv) > 1 else u"build").lower()
    with open(STATUS, "w", encoding="utf-8") as f:
        f.write(u"%s  build_next v1 started (%s)\n" % (time.strftime("%H:%M:%S"), mode))
    t0 = time.time()
    try:
        pln = check() if mode == u"check" else build()
        say(u"DONE %s: %s in %.0f min" % (mode, os.path.basename(pln), (time.time() - t0) / 60.0))
    except Exception as ex:
        say(u"ERROR %s: %s" % (type(ex).__name__, ex))
        sys.exit(1)


if __name__ == "__main__":
    main()
