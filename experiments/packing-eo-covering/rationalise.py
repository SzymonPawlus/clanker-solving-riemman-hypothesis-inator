"""Take a float power-diagram config, round sites/weights to rationals in the
(u,v) basis, and EXACTLY certify the largest a for which the partition of T_a
has all diameters <= 1.  Exactness decides; the float input is only a guess."""
import json, sys, math
from fractions import Fraction as F
from exact import q3, Q3, power_cells_exact, verify, diam2

SQ3 = math.sqrt(3.0)
D = 10**6

def to_uv(x, y):
    return F(round((x - y/SQ3)*D), D), F(round((2*y/SQ3)*D), D)

def main(src, dens=D):
    d = json.load(open(src))
    a0 = F(int(round(d["a"])))
    sites = [to_uv(x, y) for x, y in d["sites"]]
    ws = [F(round(w*dens), dens) for w in d["weights"]]
    sq = [(q3(u), q3(v)) for u, v in sites]
    cells = power_cells_exact(sq, ws, q3(a0))
    ne = sum(1 for c in cells if c)
    worst = max(diam2(c) for c in cells if c)
    # scale: config in T_{a0} has max diam^2 = worst; in T_a it is worst*(a/a0)^2
    # need worst*(a/a0)^2 <= 1  ->  a <= a0/sqrt(worst)
    amax = float(a0) / math.sqrt(worst.approx())
    print("%s: %d cells (%d nonempty)  max diam^2 = %s ~%.9f  -> a_max ~ %.6f"
          % (src, len(cells), ne, worst, worst.approx(), amax))
    # pick a rational a strictly below a_max and certify exactly
    a = F(int(amax*1000), 1000)
    r = a / a0
    sc = [(q3(u*r), q3(v*r)) for u, v in sites]
    wsc = [w*r*r for w in ws]
    cells2 = power_cells_exact(sc, wsc, q3(a))
    ok, w2 = verify([c for c in cells2 if c], q3(a), verbose=False)
    print("   EXACT at a = %s : cells=%d  max diam^2 = ~%.12f  PASS=%s"
          % (a, sum(1 for c in cells2 if c), w2.approx(), ok))
    return a, ok, cells2

if __name__ == "__main__":
    main(sys.argv[1])
