"""Exact verification of separated-point certificates and of the covering-number floor.

Reads the float hypotheses produced by shrink.py, snaps them to rationals, repairs them by an
exact rational local search, and certifies:   N*(a) >= n   for the certified (a, n).

EVERY DECISION IN THIS FILE IS EXACT RATIONAL ARITHMETIC.  Floats are used only to *propose*.
"""
import json, math, os, sys
from fractions import Fraction as F
from exactlib import in_triangle, d2, check_separated

SQ3 = math.sqrt(3.0)
HERE = os.path.dirname(os.path.abspath(__file__))

def to_tri_rational(pts_xy, den):
    out = []
    for (x, y) in pts_xy:
        v = 2.0 * y / SQ3
        u = x - y / SQ3
        out.append((F(round(u * den), den), F(round(v * den), den)))
    return out

def clamp_exact(p, a):
    u, v = p
    if u < 0: u = F(0)
    if v < 0: v = F(0)
    if u + v > a:
        # push back along the (-1,-1) direction, exactly
        e = (u + v - a)
        u -= e / 2; v -= e / 2
        if u < 0: v += u; u = F(0)
        if v < 0: u += v; v = F(0)
    return (u, v)

def exact_repair(pts, a, den, rounds=400):
    """Exact rational local search: move offending points on the (1/den) lattice of T_a."""
    n = len(pts)
    pts = [clamp_exact(p, a) for p in pts]
    step = F(1, den)
    moves = [(F(0), F(0))]
    for k in (1, 2, 3, 5, 8):
        s = step * k
        moves += [(s, F(0)), (-s, F(0)), (F(0), s), (F(0), -s), (s, -s), (-s, s), (s, s), (-s, -s)]
    for r in range(rounds):
        improved = False
        for i in range(n):
            cur = pts[i]
            best = cur
            bestscore = None
            for (du, dv) in moves:
                cand = clamp_exact((cur[0] + du, cur[1] + dv), a)
                if not in_triangle(cand, a):
                    continue
                # score: (number of violated pairs, -min squared distance)
                viol = 0; mn = None
                for j in range(n):
                    if j == i: continue
                    dd = d2(cand, pts[j])
                    if dd < 1: viol += 1
                    if mn is None or dd < mn: mn = dd
                sc = (viol, -mn)
                if bestscore is None or sc < bestscore:
                    bestscore = sc; best = cand
            if best != cur:
                pts[i] = best; improved = True
        ok, bad = check_separated(pts, a)
        if ok:
            return pts, True
        if not improved:
            break
    return pts, False

def certify(n, a_frac, pts_xy, dens=(2000, 10000, 50000)):
    for den in dens:
        pts = to_tri_rational(pts_xy, den)
        ok, bad = check_separated(pts, a_frac)
        if ok:
            return pts, den, "direct"
        pts2, ok2 = exact_repair(pts, a_frac, den)
        if ok2:
            return pts2, den, "repaired"
    return None, None, None

if __name__ == '__main__':
    targets = sys.argv[1:] or ['22', '23', '24', '25', '26']
    report = []
    for t in targets:
        n = int(t)
        import glob
        cands = sorted(glob.glob(os.path.join(HERE, 'out', f'shrink_n{n}*.json')))
        cands = [json.load(open(p)) for p in cands]
        cands = [c for c in cands if c.get('n') == n and c.get('pts')]
        if not cands:
            print(f"n={n}: no hypothesis file"); continue
        data = min(cands, key=lambda c: c['a'])
        af = data['a']
        # NO rescaling: the float config already has min pairwise distance ~1.002 >= 1 inside
        # T_af, so it certifies n points at separation 1 in T_af directly, with 0.002 of margin
        # to absorb the rounding to rationals.
        a_frac = F(math.ceil(af * 1000000) + 2, 1000000)
        pts_xy = data['pts']
        if a_frac >= 6:
            print(f"n={n}: hypothesis a={float(a_frac):.6f} is NOT < 6 -- gives no floor below 6")
            report.append({"n": n, "a": str(a_frac), "certified": False,
                           "reason": "a >= 6"})
            continue
        pts, den, how = certify(n, a_frac, pts_xy, dens=(1000000,))
        if pts is None:
            print(f"n={n}: FAILED to certify at a={float(a_frac):.6f}")
            report.append({"n": n, "a": str(a_frac), "certified": False})
        else:
            ok, bad = check_separated(pts, a_frac)
            assert ok
            mn = min(d2(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n))
            print(f"n={n}: CERTIFIED  a = {a_frac} = {float(a_frac):.7f} < 6 "
                  f"[{how}, den={den}]  min squared distance = {float(mn):.9f} >= 1")
            report.append({"n": n, "a": str(a_frac), "certified": True, "den": den,
                           "min_d2": str(mn),
                           "pts": [[str(p[0]), str(p[1])] for p in pts]})
    with open(os.path.join(HERE, 'out', 'certificates.json'), 'w') as f:
        json.dump(report, f, indent=1)
    print("\nFLOOR:  N*(a) >= n for every a >= (the certified a), in particular for a in [a_cert, 6).")
