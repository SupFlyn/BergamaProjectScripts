# SUPERSEDED (round 4, S1, 1 Nov 2026): common/trigger.py is the one start-up file. Kept only while a script still
# includes this file (each page session moves its script to trig_should_run); the closing step deletes it.
def _gh_in_items():
    """(name, value) of this component's own inputs only. 1 Nov (Aras 08:24): a setting written in the script
    (PHOTO_ANY_LICENCE = True in agriculture) was taken for a pressed Button, so the script started as soon as it was
    pasted; Rhino 8 also keeps old globals between solves. All globals only if the inputs cannot be read."""
    g_ = globals()
    try:
        return [(n_, g_.get(n_)) for n_ in (str(p_.NickName or p_.Name) for p_ in ghenv.Component.Params.Input)  # noqa: F821
                if n_ in g_]
    except Exception:
        return list(g_.items())
