def load_palette(dirs, log):
    for d in dirs:
        for p in (os.path.join(d, "bergama_palette.py"), os.path.join(d, "palette", "bergama_palette.py")):
            if not os.path.isfile(p):
                continue
            try:
                m = _types.ModuleType("bergama_palette")
                exec(compile(open(p, encoding="utf-8").read(), p, "exec"), m.__dict__)
                for k in ("paper", "faint", "structure", "ink2", "ink"):
                    COL[k] = m.CORE.get(k, COL[k])
                for k, a in MP.items():
                    e = m.MASTERPLAN.get(k)
                    if e:
                        MP[k] = (e["light"], e["mid"], e["dark"])
                riv = m.MASTERPLAN.get("river")
                if riv:
                    COL["river"], COL["river_mid"], COL["river_dark"] = riv["light"], riv["mid"], riv["dark"]
                for k in ("aras_alan", "begum_alan", "nil_alan"):
                    COL[k] = m.STUDY_AREA.get(k, {}).get("line", COL[k])
                log.append(u"Palette read from " + p)
                return u"palette {} (version {})".format(os.path.basename(p), getattr(m, "VERSION", "?"))   # 25 Oct: no local path on the sheet
            except Exception as ex:
                log.append(u"WARNING: palette file {} not read ({}); embedded v1.4 colours used".format(p, ex))
    return u"embedded palette v1.4 colours"
