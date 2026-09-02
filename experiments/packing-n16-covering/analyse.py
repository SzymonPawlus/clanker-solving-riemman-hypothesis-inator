"""Where the waste sits, in the certified subdivision.  Reporting only."""
import json, math, sys
from fractions import Fraction as F
SQ3 = math.sqrt(3.0)
d = json.load(open(sys.argv[1]))
a = F(int(d["a"][0]), int(d["a"][1]))
faces = [[(F(u), F(v)) for u, v in f] for f in d["faces_uv"]]
af = float(a)
def cls(f):
    onv = sum(1 for (u, v) in f if v == 0)
    onu = sum(1 for (u, v) in f if u == 0)
    onw = sum(1 for (u, v) in f if u+v == a)
    corners = sum(1 for (u, v) in f if (u == 0 and v == 0) or (u == a and v == 0) or (u == 0 and v == a))
    nb = (onv >= 2) + (onu >= 2) + (onw >= 2)
    if corners: return "corner"
    return "edge" if nb else "interior"
tot = 0.0
rows = {}
for f in faces:
    s = F(0)
    for i in range(len(f)):
        x1, y1 = f[i]; x2, y2 = f[(i+1) % len(f)]
        s += x1*y2 - x2*y1
    A = float(s)*SQ3/4.0            # true plane area
    dm = F(0)
    for i in range(len(f)):
        for j in range(i+1, len(f)):
            du = f[i][0]-f[j][0]; dv = f[i][1]-f[j][1]
            q = du*du+du*dv+dv*dv
            if q > dm: dm = q
    rows.setdefault(cls(f), []).append((A, math.sqrt(float(dm)), len(f)))
    tot += A
print("a = %s = %.9f     area(T_a) = %.9f   (sum of faces %.9f)" % (a, af, SQ3/4*af*af, tot))
print("%-9s %3s  %-22s %-16s %s" % ("class", "n", "areas", "diameters", "sides"))
CEIL = {"corner": math.pi/6, "edge": 0.6095, "interior": 3*SQ3/8}
for k in ("corner", "edge", "interior"):
    v = rows.get(k, [])
    if not v: continue
    A = sorted(x[0] for x in v); D = sorted(x[1] for x in v)
    print("%-9s %3d  %.4f..%.4f (%.4f) %.4f..%.4f  %s   ceiling %.4f  waste %.4f"
          % (k, len(v), A[0], A[-1], sum(A), D[0], D[-1],
             sorted(x[2] for x in v), CEIL[k], len(v)*CEIL[k]-sum(A)))
tw = sum(len(rows.get(k, []))*CEIL[k] for k in CEIL) - tot
print("total headroom to the per-piece ceilings: %.4f  ->  a <= %.5f"
      % (tw, math.sqrt((tot+tw)*4/SQ3)))
