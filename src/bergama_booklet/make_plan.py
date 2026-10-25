"""Write data/PLAN.py (built into the assembler) from the project's booklet/content/plan_merged.json and
sources_merged.json. usage: python3 src/bergama_booklet/make_plan.py [content folder]"""
import json, os, pprint, sys
HERE = os.path.dirname(os.path.abspath(__file__))
C = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/booklet/content"
KEEP = {"drawing": ("type", "asset", "caption", "scale_den", "legend", "focal"),
        "tiles": ("type", "heading", "tiles"), "text": ("type", "heading", "body", "bullets"),
        "images": ("type", "images", "caption"), "image": ("type", "image", "caption"), "stack": ("type", "blocks")}
TILE = ("keyword", "figure", "unit", "note", "icon_pdf")


def slim(b):
    t = b.get("type", "text")
    o = dict((k, b[k]) for k in KEEP.get(t, KEEP["text"]) if b.get(k) not in (None, "", []))
    o["type"] = t
    if t == "tiles":
        o["tiles"] = [dict((k, x[k]) for k in TILE if x.get(k) not in (None, "")) for x in b["tiles"]]
    if t == "stack":
        o["blocks"] = [slim(x) for x in b["blocks"]]
    return o


pages = json.load(open(os.path.join(C, "plan_merged.json"), encoding="utf-8"))
srcs = json.load(open(os.path.join(C, "sources_merged.json"), encoding="utf-8"))
plan = [{"id": p["id"], "part": p["part"], "template": p["template"], "title": p["title"],
         "statement": p.get("statement", ""), "frames": dict((k, slim(v)) for k, v in p["frames"].items())}
        for p in pages]
src = dict((k, {"text": v["text"], "url": v["url"]}) for k, v in srcs.items())
head = open(os.path.join(HERE, "data", "PLAN_HEAD.py"), encoding="utf-8").read()
with open(os.path.join(HERE, "data", "PLAN.py"), "w", encoding="utf-8") as f:
    f.write(head + "PLAN_SOURCES = " + pprint.pformat(src, width=118, sort_dicts=True) + "\n\nPLAN = " +
            pprint.pformat(plan, width=118, sort_dicts=False) + "\n")
print("PLAN.py: %d pages, %d sources" % (len(plan), len(src)))
