"""Where a script spends its time, from a PROFILE=<file> run: top functions by own time and by calls.
usage: python3 tools/hot.py <stats file> [script name filter]"""
import pstats, sys
st = pstats.Stats(sys.argv[1]); flt = sys.argv[2] if len(sys.argv) > 2 else ""
rows = [(v[2], v[3], v[1], k) for k, v in st.stats.items() if flt in k[0]]   # tottime, cumtime, calls
print("total %.1f s" % st.total_tt)
for tt, ct, n, k in sorted(rows, reverse=True, key=lambda r: r[1])[:30]:
    print("%7.2f cum %7.2f own %9d calls  %s:%d %s" % (ct, tt, n, k[0].split("/")[-1][:30], k[1], k[2]))
