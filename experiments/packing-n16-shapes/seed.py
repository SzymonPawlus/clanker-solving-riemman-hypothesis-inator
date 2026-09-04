"""Build the triangulated-group seed from the record certificate, and refine corners."""
import json, os, math, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tri_group import Cover, sq, orient

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "..", "packing-n16-covering", "sub_s2_cert.json")


def load_record():
    d = json.load(open(REC))
    a = float(F(*[int(x) for x in d["a"]]))
    faces = [[(float(F(p[0])), float(F(p[1]))) for p in f] for f in d["faces_uv"]]
    return a, faces


def build_from_faces(a, faces):
    """Unique vertices + fan triangulation of each face; group = face index."""
    V = []
    idx = {}
    def vid(p):
        key = (round(p[0], 12), round(p[1], 12))
        if key not in idx:
            idx[key] = len(V)
            V.append([p[0], p[1]])
        return idx[key]
    tris, grp = [], []
    for gi, f in enumerate(faces):
        ids = [vid(p) for p in f]
        # ensure ccw
        s = 0.0
        for i in range(len(ids)):
            x1, y1 = V[ids[i]]; x2, y2 = V[ids[(i + 1) % len(ids)]]
            s += x1 * y2 - x2 * y1
        if s < 0:
            ids = ids[::-1]
        for i in range(1, len(ids) - 1):
            tris.append((ids[0], ids[i], ids[i + 1]))
            grp.append(gi)
    return V, tris, grp


def corner_of(a, p, tol=1e-9):
    for c in ((0.0, 0.0), (a, 0.0), (0.0, a)):
        if abs(p[0] - c[0]) < tol and abs(p[1] - c[1]) < tol:
            return c
    return None


def uv_to_xy(p):
    return (p[0] + 0.5 * p[1], (math.sqrt(3) / 2) * p[1])


def xy_to_uv(q):
    v = q[1] / (math.sqrt(3) / 2)
    return (q[0] - 0.5 * v, v)


def refine_corner_faces(a, faces, nchord=4):
    """Replace each corner face (a polygon containing a corner of T_a) by the
    inscribed `nchord`-chord sector polygon of the same circumradius, i.e. insert
    extra vertices on the arc.  Neighbouring faces keep their old outlines --
    the new vertices lie strictly inside them, so their convex hulls are
    unchanged; only the *tiling* has to be redone, which build_groups does."""
    out = []
    newpts = []
    for f in faces:
        ci = None
        for i, p in enumerate(f):
            if corner_of(a, p) is not None:
                ci = i
                break
        if ci is None:
            out.append(f)
            continue
        V = f[ci]
        rest = f[ci + 1:] + f[:ci]          # arc vertices in order
        Vxy = uv_to_xy(V)
        ang = []
        for p in rest:
            q = uv_to_xy(p)
            ang.append((math.atan2(q[1] - Vxy[1], q[0] - Vxy[0]),
                        math.hypot(q[0] - Vxy[0], q[1] - Vxy[1])))
        a0, a1 = ang[0][0], ang[-1][0]
        # unwrap
        while a1 - a0 > math.pi: a1 -= 2 * math.pi
        while a0 - a1 > math.pi: a0 -= 2 * math.pi
        r = min(t[1] for t in ang)
        arc = []
        for k in range(nchord + 1):
            th = a0 + (a1 - a0) * k / nchord
            q = (Vxy[0] + r * math.cos(th), Vxy[1] + r * math.sin(th))
            arc.append(xy_to_uv(q))
        out.append([V] + arc)
        newpts.append((V, arc))
    return out, newpts
