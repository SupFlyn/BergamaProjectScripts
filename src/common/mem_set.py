def mem_set(k, v):
    try:
        sc.sticky[_key(k)] = v
    except Exception:
        pass
