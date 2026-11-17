# -*- coding: utf-8 -*-
"""Bergama: AcBuild launcher v1 (17 Nov 2026, Aras 11:36-11:38 UTC "make this cmd window hide instantly", "if error
happens bring it foreground and show the error in bold red and show the log dir in the screen aswell").
Started windowless by run_acbuild.bat (pyw). Runs the newest scripts/bergama_acbuild_v*.py in plain Python (only
Archicad open), writes its log as usual, and only if the run ends in an ERROR (or crashes) pops a window to the front:
the error in bold red, the log folder path, and buttons to open the folder / the log. A clean run shows nothing.
"""
import glob, os, re, runpy, traceback

ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
LOG_DIR = os.path.join(ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "bergama_acbuild_site_log.txt")
PROGRESS = os.path.join(LOG_DIR, "bergama_acbuild_progress.txt")


def newest():
    fs = glob.glob(os.path.join(ROOT, "scripts", "bergama_acbuild_v*.py"))
    return max(fs, key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))]) if fs else None


def show_error(title, text):
    """the error window: always on top, brought to the front, error in bold red, log folder shown"""
    import tkinter as tk
    w = tk.Tk()
    w.title(u"AcBuild: ERROR")
    w.attributes("-topmost", True)
    w.configure(padx=18, pady=14)
    tk.Label(w, text=title, fg="#C00000", font=("Segoe UI", 16, "bold"), justify="left",
             wraplength=900).pack(anchor="w")
    tk.Label(w, text=text, fg="#C00000", font=("Consolas", 10, "bold"), justify="left",
             wraplength=900).pack(anchor="w", pady=(8, 10))
    tk.Label(w, text=u"Log folder: " + LOG_DIR, font=("Segoe UI", 11, "bold"), justify="left").pack(anchor="w")
    tk.Label(w, text=u"Full log: " + LOG_FILE + u"\nLast steps: " + PROGRESS, font=("Segoe UI", 10),
             justify="left").pack(anchor="w", pady=(2, 10))
    row = tk.Frame(w)
    row.pack(anchor="w")
    tk.Button(row, text=u"Open log folder", command=lambda: os.startfile(LOG_DIR)).pack(side="left", padx=(0, 8))
    tk.Button(row, text=u"Open log", command=lambda: os.startfile(LOG_FILE) if os.path.isfile(LOG_FILE)
              else os.startfile(LOG_DIR)).pack(side="left", padx=(0, 8))
    tk.Button(row, text=u"Close", command=w.destroy).pack(side="left")
    w.lift()
    w.focus_force()
    w.after(300, lambda: w.attributes("-topmost", True))
    w.mainloop()


def last_progress(n=6):
    try:
        with open(PROGRESS, encoding="utf-8") as f:
            return u"".join(f.readlines()[-n:])
    except Exception:
        return u""


def main():
    f = newest()
    if not f:
        show_error(u"No AcBuild script found", u"Nothing matches %s" % os.path.join(ROOT, "scripts",
                                                                                    "bergama_acbuild_v*.py"))
        return
    try:
        ns = runpy.run_path(f, run_name="bergama_launcher")   # load only; the run itself below
        res = ns["_run"]()
        try:
            ns["write_log"](res)
        except Exception:
            pass
    except BaseException as ex:                            # a crash outside AcBuild's own error handling
        res = u"ERROR: %s: %s\n%s" % (type(ex).__name__, ex, traceback.format_exc()[-1500:])
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            with open(LOG_FILE, "w", encoding="utf-8") as fh:
                fh.write(res)
        except Exception:
            pass
    res = u"%s" % res
    if res.startswith(u"ERROR"):
        head = res.splitlines()[0]
        show_error(u"%s stopped with an error" % os.path.basename(f),
                   head + u"\n\n" + u"\n".join(res.splitlines()[1:])[-1200:] +
                   (u"\n\nLast steps:\n" + last_progress() if last_progress() else u""))


if __name__ == "__main__":
    main()
