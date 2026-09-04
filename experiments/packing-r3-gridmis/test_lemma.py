"""Independent randomised tests of the soundness-critical machinery.

1.  `test_containment`: the exact rational containment predicate in
    lattice.py is compared against a *separately written* float predicate
    (relaxed half-planes evaluated directly), on every candidate lattice point
    in a range, for several (d, g).  Points within 1e-9 of a boundary are
    skipped, since only there can the two legitimately disagree.

2.  `test_lemma`: the conclusion of Lemma 1 is exercised end to end.  Random
    point sets with pairwise distance >= 2 are generated inside T_d, each point
    is snapped to its nearest lattice point by brute-force float search, and we
    check that the snapped set (a) lies in V, (b) has n distinct elements, and
    (c) contains no edge of G.  A failure of any of these would mean the lemma
    or its implementation is wrong.

3.  `test_cover`: the covering-radius claim, by sampling points of T_d and
    checking the nearest lattice point is within r.

Run:  python3 test_lemma.py
"""
import math, random, sys
from fractions import Fraction as F

from gridmis.lattice import build_graph

R3 = math.sqrt(3.0)


def xy(g, a, j):
    return (float(g) * a / 2.0, float(g) * j * R3 / 2.0)


def test_containment(seed=1):
    bad = 0
    for (dstr, gstr) in [("4", "1/4"), ("13/2", "1/5"), ("83/10", "1/6"), ("7", "1/3")]:
        d, g = F(dstr), F(gstr)
        G = build_graph(d, g)
        r = float(G.r); df = float(d)
        inset = set(G.verts)
        amax = 2 * int((df + 2 * r) / float(g)) + 6
        jmax = int(df / float(g)) + 6
        for j in range(-4, jmax + 1):
            for a in range(-6, amax + 1):
                if (a - j) % 2:
                    continue
                x, y = xy(g, a, j)
                s = [y + r, (R3 * x - y) / 2.0 + r, (R3 * (df - x) - y) / 2.0 + r]
                if min(s) < 1e-9 and min(s) > -1e-9:
                    continue                      # boundary; float cannot decide
                want = min(s) > 0
                got = (a, j) in inset
                if want != got:
                    bad += 1
                    print("  MISMATCH", dstr, gstr, (a, j), s, want, got)
    print("test_containment: %d mismatches" % bad)
    return bad == 0


def test_cover(seed=2, samples=20000):
    rng = random.Random(seed)
    ok = True
    for (dstr, gstr) in [("4", "1/4"), ("83/10", "1/6")]:
        worst = 0.0
        d, g = F(dstr), F(gstr)
        G = build_graph(d, g)
        df, gf, r = float(d), float(g), float(G.r)
        for _ in range(samples):
            u, v = rng.random(), rng.random()
            if u + v > 1:
                u, v = 1 - u, 1 - v
            x = df * u + df / 2 * v
            y = df * R3 / 2 * v
            j = round(y * 2 / (gf * R3))
            best = 1e18
            for jj in (j - 1, j, j + 1):
                a0 = x * 2 / gf
                for aa in range(int(a0) - 3, int(a0) + 4):
                    if (aa - jj) % 2:
                        continue
                    px, py = xy(g, aa, jj)
                    best = min(best, math.hypot(x - px, y - py))
            worst = max(worst, best)
            if best > r + 1e-12:
                ok = False
        print("test_cover  d=%s g=%s: worst snap distance %.9f, r = %.9f" % (dstr, gstr, worst, r))
    print("test_cover:", "OK" if ok else "FAIL")
    return ok


def sample_packing(df, n, rng, tries=200000):
    """Random sequential adsorption: place as many points at separation >= 2 as
    fit in `tries` attempts, capped at n.  Returns the (possibly shorter) list;
    any list it returns is a genuine feasible configuration, which is all the
    lemma test needs."""
    pts = []
    for _ in range(tries):
        if len(pts) == n:
            break
        u, v = rng.random(), rng.random()
        if u + v > 1:
            u, v = 1 - u, 1 - v
        x = df * u + df / 2 * v
        y = df * R3 / 2 * v
        if all((x - px) ** 2 + (y - py) ** 2 >= 4.0 for px, py in pts):
            pts.append((x, y))
    return pts


def snap(g, x, y):
    gf = float(g)
    j0 = round(y * 2 / (gf * R3))
    best, bv = 1e18, None
    for jj in (j0 - 2, j0 - 1, j0, j0 + 1, j0 + 2):
        a0 = x * 2 / gf
        for aa in range(int(a0) - 4, int(a0) + 5):
            if (aa - jj) % 2:
                continue
            px, py = xy(g, aa, jj)
            dd = math.hypot(x - px, y - py)
            if dd < best:
                best, bv = dd, (aa, jj)
    return bv, best


def test_lemma(seed=3, trials=300):
    rng = random.Random(seed)
    fails = 0
    for (dstr, gstr, n) in [("4", "1/4", 6), ("13/2", "1/5", 9), ("83/10", "1/6", 12),
                            ("9", "1/8", 14)]:
        d, g = F(dstr), F(gstr)
        G = build_graph(d, g)
        idx = G.index
        df = float(d)
        got = 0
        for _ in range(trials):
            pts = sample_packing(df, n, rng, tries=3000)
            if pts is None or len(pts) < 3:
                continue
            n_here = len(pts)
            got += 1
            vs = []
            for (x, y) in pts:
                v, dist = snap(g, x, y)
                if dist > float(G.r) + 1e-12:
                    print("  COVER FAIL", dstr, gstr, dist, float(G.r)); fails += 1
                if v not in idx:
                    print("  BOUNDARY FAIL: snapped outside V", dstr, gstr, v); fails += 1
                vs.append(idx.get(v, -1))
            if len(set(vs)) != n_here:
                print("  DISTINCTNESS FAIL", dstr, gstr, vs); fails += 1
            for i in range(n_here):
                for k in range(i + 1, n_here):
                    if vs[i] >= 0 and vs[k] >= 0 and (G.adj[vs[i]] >> vs[k]) & 1:
                        print("  INDEPENDENCE FAIL", dstr, gstr); fails += 1
        print("test_lemma d=%s g=%s n<=%d: %d random feasible sets snapped, %d failures"
              % (dstr, gstr, n, got, fails))
    print("test_lemma:", "OK" if fails == 0 else "FAIL")
    return fails == 0


if __name__ == "__main__":
    ok = test_containment() and test_cover() and test_lemma()
    print("ALL TESTS", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
