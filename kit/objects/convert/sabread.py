# minimal reader of ACIS binary (SAB) data: records of tagged tokens
import struct


def records(d):
    """-> (header tokens, [ (type name, [tokens]) ]); a token is (kind, value)"""
    assert d[:15] == b"ACIS BinaryFile"
    i = 15
    ver, nrec, nent, flag = struct.unpack_from("<4i", d, i)
    i += 16
    toks = []
    out = []
    name = []
    hdr = None
    n = len(d)
    while i < n:
        t = d[i]
        i += 1
        if t == 0x04:
            toks.append(("i", struct.unpack_from("<i", d, i)[0])); i += 4
        elif t == 0x05:
            toks.append(("f", struct.unpack_from("<f", d, i)[0])); i += 4
        elif t == 0x06:
            toks.append(("d", struct.unpack_from("<d", d, i)[0])); i += 8
        elif t == 0x07:
            l = d[i]; toks.append(("s", d[i + 1:i + 1 + l].decode("latin1"))); i += 1 + l
        elif t == 0x08:
            l = struct.unpack_from("<H", d, i)[0]; toks.append(("s", d[i + 2:i + 2 + l].decode("latin1"))); i += 2 + l
        elif t == 0x09:
            l = struct.unpack_from("<I", d, i)[0]; toks.append(("s", d[i + 4:i + 4 + l].decode("latin1"))); i += 4 + l
        elif t == 0x0A:
            toks.append(("b", True))
        elif t == 0x0B:
            toks.append(("b", False))
        elif t == 0x0C:
            toks.append(("p", struct.unpack_from("<i", d, i)[0])); i += 4
        elif t in (0x0D, 0x0E):
            l = d[i]; s = d[i + 1:i + 1 + l].decode("latin1"); i += 1 + l
            if toks and name == [] and out is not None and hdr is not None and False:
                pass
            toks.append(("n" if t == 0x0D else "m", s))
        elif t == 0x0F:
            toks.append(("{", None))
        elif t == 0x10:
            toks.append(("}", None))
        elif t == 0x11:
            if hdr is None and not any(k in ("n", "m") for k, _v in toks[:1]):
                pass
            # the entity name = the leading run of m tokens and one n token
            j = 0
            nm = []
            while j < len(toks) and toks[j][0] == "m":
                nm.append(toks[j][1]); j += 1
            if j < len(toks) and toks[j][0] == "n":
                nm.append(toks[j][1]); j += 1
            out.append(("-".join(nm), toks[j:]))
            toks = []
        elif t == 0x12:
            l = struct.unpack_from("<I", d, i)[0]; toks.append(("s", d[i + 4:i + 4 + l].decode("latin1"))); i += 4 + l
        elif t in (0x13, 0x14):
            toks.append(("v", struct.unpack_from("<3d", d, i))); i += 24
        elif t == 0x15:
            toks.append(("e", struct.unpack_from("<i", d, i)[0])); i += 4
        elif t == 0x16:
            toks.append(("uv", struct.unpack_from("<2d", d, i))); i += 16
        else:
            raise ValueError("unknown tag 0x%02x at %d" % (t, i - 1))
    return (ver, nrec, nent, flag), out, toks
