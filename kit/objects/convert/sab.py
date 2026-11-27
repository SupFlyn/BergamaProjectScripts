import pickle, sys, collections
def shifted(b, k):
    if k == 0: return b
    n = int.from_bytes(b, "big")
    n = (n << k) & ((1 << (8 * len(b))) - 1)
    return n.to_bytes(len(b), "big")
END = b"End\x0e\x02of\x0e\x04ACIS\x0d\x04data"
def extract(b):
    for k in range(8):
        s = shifted(b, k)
        i = s.find(b"ACIS BinaryFile")
        if i >= 0:
            j = s.find(b"End\x0e\x02of\x0e\x04ACIS\x0d\x04data", i)
            return s[i:(j + len(END)) if j >= 0 else len(s)], k, j >= 0
    return None, None, False
if __name__ == "__main__":
    recs = pickle.load(open(sys.argv[1], "rb"))
    out = []
    c = collections.Counter()
    for h, b in recs:
        d, k, end = extract(b)
        c[(k, end)] += 1
        out.append((h, d))
    print(c)
    pickle.dump(out, open(sys.argv[2], "wb"))
    print(out[0][1][:120], out[0][1][-60:])
