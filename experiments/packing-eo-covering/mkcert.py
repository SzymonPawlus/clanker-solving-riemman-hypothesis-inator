"""Freeze a float power-diagram config into an EXACT rational certificate."""
import json, sys, math
from fractions import Fraction as F
from exact import q3, power_cells_exact, verify, diam2
SQ3 = math.sqrt(3.0); D = 10**6

def to_uv(x, y):
    return F(round((x - y/SQ3)*D), D), F(round((2*y/SQ3)*D), D)

def make(src, dst):
    d = json.load(open(src))
    a0 = F(int(round(d["a"])))
    sites = [to_uv(x, y) for x, y in d["sites"]]
    ws = [F(round(w*D), D) for w in d["weights"]]
    cells = power_cells_exact([(q3(u), q3(v)) for u, v in sites], ws, q3(a0))
    worst = max(diam2(c) for c in cells if c)
    amax = float(a0)/math.sqrt(worst.approx())
    a = F(int(amax*1000), 1000)
    r = a/a0
    json.dump({"n": len(sites), "a": [str(a.numerator), str(a.denominator)],
               "basis": "(u,v) in e1=(1,0), e2=(1/2,sqrt3/2); |u e1+v e2|^2 = u^2+uv+v^2",
               "sites": [[str((u*r)), str((v*r))] for u, v in sites],
               "weights": [str(w*r*r) for w in ws],
               "claim": "power-diagram cells of these sites/weights partition T_a into n convex sets of diameter <= 1"},
              open(dst, "w"), indent=0)
    print("wrote %s : n=%d a=%s" % (dst, len(sites), a))

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2])
