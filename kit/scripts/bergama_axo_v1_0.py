# -*- coding: utf-8 -*-
"""Bergama Axo: axonometric 3D Documents from the open Archicad model, ready to become diagrams.

Runs with the system Python (run_axo.bat), talks to Archicad through Tapir 2.0 on port 19723-19743.
Makes, in this order: AX-N1 .. AX-N6 (each node cropped), then AX-SITE-SW and AX-SITE-NE (whole model).
Per view the script sets up the 3D window (only the elements of that area, isometric, cut box, white
surfaces with black contours as the 3D Document defaults), then asks you, in Archicad's bubble and in this
console, to make the 3D Document by hand: Document > Documenting Tools > Create 3D Document... > Create
(Tapir 2.0 has no command for that step; Create3DDocuments arrives in 2.0.1). The script sees the new
document, places it in the View Map folder "BGA - axonometric" and goes on. No solid element operations.
A view whose 3D Document already exists is kept (delete it by hand to remake it). Saves the pln at the end.
Writes Downloads/Bergama/(Project Files/)logs/bergama_axo_log.txt.
"""
import json
import os
import sys
import time
import urllib.request

VERSION = "v1.0"   # v1.0 (Aras 20 Nov 09:11 "lets try to run that script on desktop"): first version, Tapir 2.0
NODE_MARGIN_M = 60.0          # m around each node's two section lines (ASSUMED, proposed 19 Nov)
PROJ = "Isometric"            # Archicad's predefined isometric
# Tapir: "an Isometric at azimuth 270 is the isometric from the south-east" -> predefined looks 45 deg further
VIEWS_SITE = [("AX-SITE-SW", "Site from the southwest", 180.0), ("AX-SITE-NE", "Site from the northeast", 0.0)]
NODE_AZ = 180.0               # node close-ups face like the southwest site view
VIEW_FOLDER = "BGA - axonometric"
WHITE = "BGA axo white"       # own surface: one flat white on everything
CONTOUR_PEN = 1               # pen 1 = black in Archicad's default pen sets (ASSUMED for his pen set)
WAIT_S = 900                  # how long the script waits for each hand-made 3D Document
TYPES_3D = ["Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab", "Roof", "Mesh", "Shell",
            "Morph", "Stair", "Railing", "CurtainWall", "Skylight"]

_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files")) else _BG
LOG = os.path.join(ROOT, "logs", "bergama_axo_log.txt")
LINES = []


def log(s):
    LINES.append(s)
    print(s)
    sys.stdout.flush()
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(u"\n".join(LINES) + u"\n")
    except Exception:
        pass


class AC(object):
    def __init__(self):
        self.url = None
        for p in range(19723, 19744):
            try:
                if self._post("http://127.0.0.1:%d" % p, {"command": "API.IsAlive"}, 2.0).get("result", {}).get("isAlive"):
                    self.url = "http://127.0.0.1:%d" % p
                    break
            except Exception:
                continue
        if not self.url:
            raise RuntimeError("no Archicad found on ports 19723-19743: open Bergama_AC.pln in Archicad, then run again")

    def _post(self, url, body, timeout=600.0):
        rq = urllib.request.Request(url, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
        with urllib.request.urlopen(rq, timeout=timeout) as f:
            return json.loads(f.read().decode("utf-8"))

    def api(self, cmd, params=None, timeout=600.0):
        b = {"command": cmd}
        if params is not None:
            b["parameters"] = params
        r = self._post(self.url, b, timeout)
        if not r.get("succeeded"):
            raise RuntimeError("%s failed: %s" % (cmd, json.dumps(r.get("error"))[:300]))
        return r.get("result") or {}

    def t(self, name, params=None, timeout=1800.0):
        p = {"addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": name}}
        if params is not None:
            p["addOnCommandParameters"] = params
        r = self.api("API.ExecuteAddOnCommand", p, timeout).get("addOnCommandResponse") or {}
        if isinstance(r, dict) and (r.get("error") or r.get("success") is False):
            raise RuntimeError("Tapir %s: %s" % (name, json.dumps(r.get("error") or r)[:300]))
        return r

    def has(self, name):
        try:
            return bool(self.api("API.IsAddOnCommandAvailable", {"addOnCommandId": {
                "commandNamespace": "TapirCommand", "commandName": name}}).get("available"))
        except Exception:
            return False


def walk(item):
    yield item
    for c in item.get("children") or []:
        yield from walk(c.get("navigatorItem") or c)


def docs3d(ac):
    tree = ac.t("GetNavigatorItemTree", {"navigatorMapId": "ProjectMap"})["navigatorItemTree"]
    return dict((i.get("name"), i) for i in walk(tree) if i.get("type") == "DocumentFrom3DItem")


def node_boxes(ac):
    """each node's box = its section lines (N<k>-A, N<k>-B in the model) + NODE_MARGIN_M"""
    els = ac.t("GetElementsByType", {"elementType": "SectElem"}).get("elements") or []
    if not els:
        return {}
    det = ac.t("GetSectionsAndElevationsDetails", {"elements": els}).get("detailsOfElements") or []
    bbs = ac.t("Get2DBoundingBoxes", {"elements": els}).get("boundingBoxes2D") or []
    out = {}
    for d, b in zip(det, bbs):
        nm = (d.get("name") or d.get("id") or u"").strip()
        bb = b.get("boundingBox2D")
        if not bb or len(nm) < 2 or nm[0] != "N" or not nm[1].isdigit():
            continue
        k = nm.split("-")[0].split(" ")[0]
        x0, y0, x1, y1 = out.get(k, (1e18, 1e18, -1e18, -1e18))
        out[k] = (min(x0, bb["xMin"]), min(y0, bb["yMin"]), max(x1, bb["xMax"]), max(y1, bb["yMax"]))
    m = NODE_MARGIN_M
    return dict((k, (v[0] - m, v[1] - m, v[2] + m, v[3] + m)) for k, v in out.items())


def elems_3d(ac):
    """every 3D element with its 3D box: [(element, box)]"""
    out = []
    for ty in TYPES_3D:
        try:
            els = ac.t("GetElementsByType", {"elementType": ty}).get("elements") or []
        except Exception:
            continue
        for i in range(0, len(els), 3000):
            ch = els[i:i + 3000]
            bbs = ac.t("Get3DBoundingBoxes", {"elements": ch}).get("boundingBoxes3D") or []
            out += [(e, b["boundingBox3D"]) for e, b in zip(ch, bbs) if b.get("boundingBox3D")]
    return out


def white_surface(ac):
    try:
        ac.t("CreateSurfaces", {"overwriteExisting": True, "surfaceDataArray": [dict(
            name=WHITE, materialType="Matte", surfaceColor={"red": 1.0, "green": 1.0, "blue": 1.0}, transparency=0,
            ambientReflection=80, diffuseReflection=80, specularReflection=0)]})
    except Exception as ex:
        log(u"FLAG white surface not made (%s)" % ex)
    for a in ac.t("GetAttributesByType", {"attributeType": "Surface"}).get("attributes") or []:
        if a.get("name") == WHITE:
            return int(a["index"]), a.get("attributeId")
    return None, None


def main():
    t0 = time.time()
    log(u"Bergama Axo %s  %s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S")))
    ac = AC()
    ver = ac.t("GetAddOnVersion").get("version")
    log(u"TAPIR OK %s (%s)" % (ver, ac.url))
    need = ["GetNavigatorItemTree", "ShowElementsIn3D", "Set3DProjectionSettings", "Set3DCutPlanes",
            "SetDocumentFrom3DDefaults", "GetElementsByType", "Get3DBoundingBoxes", "Get2DBoundingBoxes",
            "GetSectionsAndElevationsDetails", "CreateViewMapFolder", "CloneProjectMapItemToViewMap"]
    miss = [c for c in need if not ac.has(c)]
    if miss:
        raise RuntimeError(u"Tapir %s lacks %s: install Tapir 2.0.0" % (ver, u", ".join(miss)))

    boxes = node_boxes(ac)
    log(u"node boxes (section lines + %.0f m): %s" % (NODE_MARGIN_M, u"; ".join(
        u"%s %.0fx%.0f m" % (k, v[2] - v[0], v[3] - v[1]) for k, v in sorted(boxes.items())) or u"FLAG none found"))
    views = [(u"AX-" + k, u"Node %s" % k, NODE_AZ, boxes[k]) for k in sorted(boxes)]
    views += [(r, n, az, None) for r, n, az in VIEWS_SITE]

    have = docs3d(ac)
    there = lambda v: v[1] in have or any(i.get("uiId") == v[0] for i in have.values())
    todo = [v for v in views if not there(v)]
    for v in views:
        if there(v):
            log(u"%s: 3D Document already there, kept" % v[0])
    ELS = elems_3d(ac) if any(v[3] for v in todo) else []
    if ELS:
        log(u"3D elements read: %d" % len(ELS))

    mat, mat_id = white_surface(ac)
    defaults = dict(vect3DHatching=False, vectSunShadow=True, mustBeTransparent=False, intPlanConn="Online",
                    contureOff=False, boundaryDisplay="OverrideContours", boundaryPen=CONTOUR_PEN)
    if mat is not None:
        defaults.update(materialFrom3D=False, cMater=mat)
    else:
        log(u"FLAG no white surface: the 3D Documents keep the model surfaces")

    made = 0
    for ref, name, az, box in todo:
        if box:
            x0, y0, x1, y1 = box
            sel = [e for e, b in ELS if b["xMax"] >= x0 and b["xMin"] <= x1 and b["yMax"] >= y0 and b["yMin"] <= y1]
            if not sel:
                log(u"FLAG %s: no elements inside its box, skipped" % ref)
                continue
            ac.t("ShowElementsIn3D", {"elements": sel})
            planes = [dict(pa=1, pb=0, pc=0, pd=x1, cutPen=CONTOUR_PEN), dict(pa=-1, pb=0, pc=0, pd=-x0, cutPen=CONTOUR_PEN),
                      dict(pa=0, pb=1, pc=0, pd=y1, cutPen=CONTOUR_PEN), dict(pa=0, pb=-1, pc=0, pd=-y0, cutPen=CONTOUR_PEN)]
            if mat_id:
                for p in planes:
                    p["cutSurfaceId"] = mat_id
        else:
            sel = []
            ac.t("ShowElementsIn3D", {})
            planes = []
        try:
            ac.t("Set3DCutPlanes", {"cutPlanes": planes})
        except Exception as ex:
            log(u"FLAG %s: cut planes not set (%s)" % (ref, ex))
        ac.t("Set3DProjectionSettings", {"axonometry": {"projectionType": PROJ, "azimuth": az}})
        ac.t("SetDocumentFrom3DDefaults", dict(defaults, name=name, refId=ref))
        try:
            ac.t("RebuildView", {})
        except Exception:
            pass
        msg = (u"Bergama Axo: make the 3D Document now: Document > Documenting Tools > Create 3D Document... "
               u"> Create (name '%s', ID %s are filled in)" % (name, ref))
        log(u"%s: 3D window ready (%s elements, %s, azimuth %.0f). WAITING: %s" % (
            ref, len(sel) if box else u"all", PROJ, az, msg))
        try:
            ac.t("ShowNotificationBubble", {"message": msg, "timeoutMilliseconds": 60000})
        except Exception:
            pass
        got, t1 = None, time.time()
        while time.time() - t1 < WAIT_S:
            time.sleep(3)
            try:
                d = docs3d(ac)
            except Exception:
                continue
            got = next((i for n_, i in d.items() if n_ not in have and (n_ == name or i.get("uiId") == ref)), None)
            if got:
                break
        if not got:
            log(u"FLAG %s: no new 3D Document within %d min, stopped here" % (ref, WAIT_S // 60))
            break
        have[got.get("name")] = got
        made += 1
        log(u"%s: 3D Document made (%s)" % (ref, got.get("name")))

    if made:
        try:
            fid = None
            vm = ac.t("GetNavigatorItemTree", {"navigatorMapId": "PublicViewMap"})["navigatorItemTree"]
            fid = next((i["navigatorItemId"] for i in walk(vm) if i.get("type") == "FolderItem"
                        and i.get("name") == VIEW_FOLDER), None)
            if not fid:
                fid = ac.t("CreateViewMapFolder", {"folderName": VIEW_FOLDER})["navigatorItemId"]
            in_vm = set(i.get("name") for i in walk(vm) if i.get("type") == "DocumentFrom3DItem")
            add = [i for n_, i in have.items() if n_ not in in_vm and any(n_ == v[1] or i.get("uiId") == v[0] for v in views)]
            if add:
                ac.t("CloneProjectMapItemToViewMap", {"viewsData": [
                    dict(navigatorItemId=i["navigatorItemId"], parentNavigatorItemId=fid) for i in add]})
            log(u"View Map folder '%s': %d view(s) added" % (VIEW_FOLDER, len(add)))
        except Exception as ex:
            log(u"FLAG View Map not filled (%s): drag the 3D Documents into '%s' by hand" % (ex, VIEW_FOLDER))
        try:
            ac.t("SaveProject", {})
            log(u"pln saved")
        except Exception as ex:
            log(u"FLAG pln not saved (%s): press Ctrl+S in Archicad" % ex)
    n_ok = sum(1 for v in views if there(v))
    log(u"AXO DONE %d/%d  (%.1f min)" % (n_ok, len(views), (time.time() - t0) / 60.0))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        log(u"FAILED: %s" % ex)
