# the 3DSOLID records of a .dwg -> solids.pkl [(handle, record bytes)] for sab.py (needs the ezdwg package)
import pickle, sys
from ezdwg import raw
r = raw.read_object_records_by_type(sys.argv[1], [38])
pickle.dump([(x[0], bytes(x[-1])) for x in r], open(sys.argv[2], "wb"))
print(len(r), "solids")
