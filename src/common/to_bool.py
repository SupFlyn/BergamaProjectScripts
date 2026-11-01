# SUPERSEDED (round 4, S1, 1 Nov 2026): common/trigger.py is the one start-up file. Kept only while a script still
# includes this file (each page session moves its script to trig_should_run); the closing step deletes it.
def to_bool(v):
    if isinstance(v, (list, tuple)):
        return any(to_bool(x) for x in v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    return str(v).strip().lower() in ("true", "yes", "1", "on")
