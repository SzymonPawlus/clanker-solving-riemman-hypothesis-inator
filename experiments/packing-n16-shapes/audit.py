"""Audit the current record certificate (attacks/n16-covering, a = 89267/20000).

Read-only w.r.t. the other worker's tree: it only *loads* their JSON.
Everything computed here is exact rational arithmetic, re-derived in this file.
"""
import json, sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "packing-n16-covering", "sub_s2_cert.json")

d = json.load(open(SRC))
a = F(*[int(x) for x in d["a"]]) if isinstance(d["a"], list) else F(d["a"])
faces = [[(F(p[0]), F(p[1])) for p in f] for f in d["faces_uv"]]
S = F(d["max_sq_diam"])
print("a = %s = %.6f   faces = %d   max_sq_diam = %s = %.9f"
      % (a, float(a), len(faces), S, float(S)))

# --- independent re-verification of the certificate ------------------------------
T = geom.tri(a)
faces = [geom.ccw(f) for f in faces]
ok_conv = all(geom.is_convex_ccw(f) for f in faces)
ok_in = all(p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= a for f in faces for p in f)
mx = max(geom.diam2(f) for f in faces)
tot = sum(geom.area_uv(f) for f in faces)
print("all convex ccw: %s   all inside T_a: %s" % (ok_conv, ok_in))
print("max diam^2 recomputed: %s  (matches: %s)" % (mx, mx == S))
print("sum of uv-areas: %s   area_uv(T_a) = %s   equal: %s"
      % (tot, geom.area_uv(T), tot == geom.area_uv(T)))
rem = geom.cover_remainder(T, faces)
print("DIRECT coverage check (exact difference): leftover pieces = %d" % len(rem))

# --- where does the area go? -----------------------------------------------------
SQ3_2 = 0.8660254037844386          # sqrt3/2, for *reporting* only
HEX = 0.6495190528383289            # 3*sqrt3/8, area of the regular hexagon of diameter 1
SECTOR = 0.5235987755982988         # pi/6, area of the 60-degree sector of radius 1

def euclid_area(f):
    return float(geom.area_uv(f)) * SQ3_2

def corners_touched(f):
    c = 0
    for V in ((F(0), F(0)), (a, F(0)), (F(0), a)):
        if V in f:
            c += 1
    return c

def bdry_verts(f):
    return sum(1 for p in f if p[0] == 0 or p[1] == 0 or p[0] + p[1] == a)

print()
print(" i  |V| corner bdry     area   area/hex   diam^2   diam   at-max")
rows = []
for i, f in enumerate(faces):
    ar = euclid_area(f)
    d2 = geom.diam2(f)
    rows.append((i, len(f), corners_touched(f), bdry_verts(f), ar, ar / HEX, d2))
for (i, nv, co, bv, ar, eff, d2) in rows:
    print("%2d   %d    %d     %d   %8.5f   %6.2f%%  %8.6f  %.6f   %s"
          % (i, nv, co, bv, ar, 100 * eff, float(d2), float(d2) ** 0.5,
             "*" if d2 == mx else ""))

nmax = sum(1 for r in rows if r[6] == mx)
print("\nfaces attaining the max diameter: %d of %d" % (nmax, len(faces)))
tot_area = sum(r[4] for r in rows)
print("total area %.6f   15 * hexagon bound = %.6f   deficit = %.6f (%.2f%%)"
      % (tot_area, 15 * HEX, 15 * HEX - tot_area, 100 * (1 - tot_area / (15 * HEX))))

corner_rows = [r for r in rows if r[2] == 1]
edge_rows = [r for r in rows if r[2] == 0 and r[3] >= 2]
int_rows = [r for r in rows if r[2] == 0 and r[3] < 2]
for name, rs in (("corner", corner_rows), ("edge", edge_rows), ("interior", int_rows)):
    if rs:
        print("%-9s n=%2d  total area %8.5f   mean %7.5f   loss vs hex %7.5f"
              % (name, len(rs), sum(r[4] for r in rs), sum(r[4] for r in rs) / len(rs),
                 len(rs) * HEX - sum(r[4] for r in rs)))
print("\ncorner-piece area ceiling (pi/6 each): %.6f ; achieved %.6f ; headroom %.6f"
      % (3 * SECTOR, sum(r[4] for r in corner_rows), 3 * SECTOR - sum(r[4] for r in corner_rows)))
