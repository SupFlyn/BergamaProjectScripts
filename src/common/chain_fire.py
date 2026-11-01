def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring()      # noqa: F821
        except Exception:
            pass
        # 1 Nov (Aras 08:04: components ran after only pasting code and rewiring): the first solve with this wiring
        # (pasted, rewired or newly opened component) only notes what is on the wire; only a done text that
        # arrives after that fires the script.
        first = globals().get("_chain_first")
        if first is None:
            first = _scx.sticky.get(key + ":init") is None
            globals()["_chain_first"] = first
            _scx.sticky[key + ":init"] = True
        if not s.startswith("done "):
            return False
        if first or _scx.sticky.get(key) == s:
            _scx.sticky[key] = s
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def _chain_wiring():
    """The sources wired into this component (their ids, sorted): rewiring starts a new chain memory."""
    try:
        return ",".join(sorted(str(s_.InstanceGuid) for p_ in ghenv.Component.Params.Input       # noqa: F821
                               for s_ in p_.Sources))
    except Exception:
        return ""
