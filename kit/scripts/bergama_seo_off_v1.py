# -*- coding: utf-8 -*-
"""Bergama: TEST, remove every solid element operation link in the open Archicad model (v1, 18 Nov 2026).
Aras 18 Nov: whole-site 3D never opens after reopening, even with every BGA layer hidden and without the
section ground meshes (v1.65). This tests whether the ~29,000 solid links are the cause.

Run with run_seo_off.bat while Archicad 30 (with Tapir) has Bergama_site.pln open.
It lists all elements, reads their solid links, removes them, and prints the counts.
Undo: run run_acbuild.bat again; AcBuild re-creates every missing link.
Lines also go to logs/bergama_seo_off_log.txt.
"""
import json, os, time, urllib.request

_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files", "scripts")) else _BG
LOG = os.path.join(ROOT, "logs", "bergama_seo_off_log.txt")


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


def tapir(url, name, params=None, timeout=1800.0):
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


def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    url = find_ac()
    say(u"Archicad found at %s" % url)
    try:
        tapir(url, "ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
    except Exception:
        pass
    els = [e["elementId"]["guid"] for e in (tapir(url, "GetAllElements").get("elements") or [])
           if isinstance(e, dict) and e.get("elementId")]
    say(u"%d elements in the model; reading their solid links" % len(els))
    links = []
    for i in range(0, len(els), 500):
        part = els[i:i + 500]
        r = tapir(url, "GetSolidElementLinks", {"elements": [{"elementId": {"guid": g}} for g in part]})
        for g, e in zip(part, r.get("solidLinks") or []):
            for lk in ((e or {}).get("solidLinksWithTheGivenTarget") or []) if isinstance(e, dict) else []:
                op = (lk.get("operatorId") or {}).get("guid")
                if op:
                    links.append({"targetId": {"guid": g}, "operatorId": {"guid": op}})
        if (i // 500) % 20 == 0:
            say(u"  read %d of %d elements, %d links so far" % (min(i + 500, len(els)), len(els), len(links)))
    say(u"%d solid links found; removing them" % len(links))
    done = 0
    for i in range(0, len(links), 500):
        r = tapir(url, "RemoveSolidElementLinks", {"solidLinks": links[i:i + 500]})
        done += sum(1 for e in (r.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
        say(u"  removed %d of %d" % (done, len(links)))
    say(u"done: %d of %d solid links removed. Now press Ctrl+S, close Archicad, reopen Bergama_site.pln and "
        u"open 3D. Run run_acbuild.bat later to bring the links back." % (done, len(links)))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        say(u"ERROR: %s" % ex)
    input(u"\nPress Enter to close this window.")
