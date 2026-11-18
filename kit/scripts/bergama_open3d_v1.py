# -*- coding: utf-8 -*-
"""Bergama: open the whole Archicad model in 3D step by step, one layer at a time (v1, 18 Nov 2026).
Aras 18 Nov 12:28-12:31 UTC "cant we install a plugin or something that would make archicad draw everything step by
step", "so can we make a script to do that to open 3D".

Run with run_open3d.bat while Archicad 30 (with Tapir) has Bergama_site.pln open on the floor plan.
1. hides every "BGA ..." layer (the hidden section grounds and SEO operators stay hidden),
2. opens the 3D window,
3. turns the BGA layers on again one by one, waiting for Archicad after each, and prints the time each took.
The console window shows each step; the same lines go to logs/bergama_open3d_log.txt.
EXPERIMENT: whether Archicad builds 3D faster this way than all at once is not tested on this model.
"""
import json, os, time, urllib.request

_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files", "scripts")) else _BG
LOG = os.path.join(ROOT, "logs", "bergama_open3d_log.txt")
KEEP_HIDDEN = (u"BGA Ground view ", u"BGA SEO operators")      # hidden by design: never turned on here
ORDER = (u"BGA Terrain", u"BGA River + water", u"BGA Streets", u"BGA Bridges (existing)", u"BGA Stairs",
         u"BGA Houses", u"BGA Buildings - structure", u"BGA Greenery")   # first these, then the other BGA layers


def say(t):
    line = u"%s  %s" % (time.strftime("%H:%M:%S"), t)
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + u"\n")
    except Exception:
        pass


def post(url, body, timeout):
    req = urllib.request.Request(url, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.loads(f.read().decode("utf-8"))


def find_ac():
    for p in range(19723, 19744):
        try:
            if post("http://127.0.0.1:%d" % p, {"command": "API.IsAlive"}, 2.0).get("result", {}).get("isAlive"):
                return "http://127.0.0.1:%d" % p
        except Exception:
            continue
    raise RuntimeError(u"no Archicad found on ports 19723-19743: open Archicad with Bergama_site.pln first")


def tapir(url, name, params=None, timeout=7200.0):
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


def set_hidden(url, names, hidden):
    tapir(url, "CreateLayers", {"layerDataArray": [{"name": n, "isHidden": hidden} for n in names],
                                "overwriteExisting": True})


def wait_idle(url):
    """returns once Archicad answers again (it answers only between its own jobs)"""
    post(url, {"command": "API.IsAlive"}, 7200.0)


def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    url = find_ac()
    say(u"Archicad found at %s" % url)
    at = tapir(url, "GetAttributesByType", {"attributeType": "Layer"}).get("attributes") or []
    bga = [a.get("name") for a in at if (a.get("name") or u"").startswith(u"BGA ")
           and not any((a.get("name") or u"").startswith(k) for k in KEEP_HIDDEN)]
    if not bga:
        raise RuntimeError(u"no BGA layers in this project: open Bergama_site.pln")
    steps = [n for n in ORDER if n in bga] + sorted(n for n in bga if n not in ORDER)
    say(u"%d BGA layers, turned on in this order: %s" % (len(steps), u", ".join(steps)))
    set_hidden(url, steps, True)
    say(u"all BGA layers hidden; opening the 3D window")
    t0 = time.time()
    tapir(url, "ChangeWindow", {"windowType": "3DModel"})
    wait_idle(url)
    say(u"3D window open (%.0f s)" % (time.time() - t0))
    for i, n in enumerate(steps, 1):
        t1 = time.time()
        set_hidden(url, [n], False)
        tapir(url, "ChangeWindow", {"windowType": "3DModel"})
        wait_idle(url)
        say(u"step %d/%d: %s on (%.0f s)" % (i, len(steps), n, time.time() - t1))
    say(u"done: the whole model is shown in 3D (%.0f s in all). You can close this window." % (time.time() - t0))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        say(u"ERROR: %s" % ex)
    input(u"\nPress Enter to close this window.")
