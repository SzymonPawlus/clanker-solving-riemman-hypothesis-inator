"""Independent exact checker.  Written from problems/.../RULES.md §2 + README.md.

CONSTRUCTION checker: a PASS certifies  s(n) <= s  and nothing else.  Optimality
is never touched.

Conventions (RULES.md §2, quoted, not reinterpreted):
  * point formulation: n points, pairwise distance >= 2, in the CLOSED equilateral
    triangle with A = (0,0), B = (d,0), C = (d/2, d*sqrt3/2), and d = s - 2*sqrt3.
  * `side_length` in a certificate always means s, never d.
  * all inequalities NON-STRICT.
  * no rigid motions are searched over: the placement above is the definition.

Containment, derived here rather than imported:
  AB is the segment y = 0 from (0,0) to (d,0); interior side is y >= 0.
  AC lies on y = sqrt3 * x;             interior side is y <= sqrt3 x.
  BC lies on y = sqrt3 * (d - x);       interior side is y <= sqrt3 (d-x).
  (Signs fixed by testing the centroid (d/2, d*sqrt3/6), which satisfies all three.)
  A point is in the closed triangle iff all three hold non-strictly.

Minimal enclosing side, in this FIXED placement:  d only appears in the BC
constraint, and  sqrt3(d-x) - y >= 0  <=>  d >= x + y/sqrt3 = x + y*sqrt3/3.
So provided y >= 0 and y <= sqrt3 x hold for every point,
      d_min = max_i ( x_i + y_i*sqrt3/3 ),   s_min = d_min + 2*sqrt3.
The certificate is TIGHT iff d_min == d exactly.
"""
from fractions import Fraction as F
from q3 import E, SQ3

FOUR = E(4, 0)
Z = E(0, 0)
SQ3_3 = E(0, F(1, 3))


def sqdist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def check(n, s, pts, want_pairs=True):
    d = s - E(0, 2)
    rep = {"n": n, "s": s.s(), "d": d.s(), "ok": True, "failures": []}
    if len(pts) != n:
        rep["ok"] = False
        rep["failures"].append(("count", len(pts), n))
        return rep
    if len(set(pts)) != n:
        rep["ok"] = False
        rep["failures"].append(("duplicate point",))

    # --- containment -----------------------------------------------------
    onb = 0
    for i, (x, y) in enumerate(pts):
        sl = (y, SQ3 * x - y, SQ3 * (d - x) - y)
        for nm, v in zip(("AB", "AC", "BC"), sl):
            if v < Z:
                rep["ok"] = False
                rep["failures"].append(("containment", i, nm, v.s()))
        if any(v == Z for v in sl):
            onb += 1
    rep["points_on_boundary"] = onb

    # --- separation ------------------------------------------------------
    if want_pairs:
        worst = None
        contacts = 0
        npairs = 0
        for i in range(n):
            for k in range(i + 1, n):
                npairs += 1
                q = sqdist(pts[i], pts[k])
                if q < FOUR:
                    rep["ok"] = False
                    if len(rep["failures"]) < 40:
                        rep["failures"].append(("separation", i, k, q.s()))
                if q == FOUR:
                    contacts += 1
                if worst is None or q < worst:
                    worst = q
        rep["pairs_checked"] = npairs
        rep["min_sq_distance"] = worst.s()
        rep["min_sq_distance_is_exactly_4"] = (worst == FOUR)
        rep["contacts"] = contacts

    # --- tightness -------------------------------------------------------
    dmin = Z
    for (x, y) in pts:
        v = x + SQ3_3 * y
        if v > dmin:
            dmin = v
    rep["d_min_exact"] = dmin.s()
    rep["s_min_exact"] = (dmin + E(0, 2)).s()
    if dmin > d:
        rep["ok"] = False
        rep["failures"].append(("tightness", "d_min > d", dmin.s()))
    rep["tight"] = bool(rep["ok"]) and (dmin == d)
    return rep


# ---------------------------------------------------------------------------
# Validation of the checker itself, BEFORE it is used on anything new.
# ---------------------------------------------------------------------------
def _known_optima():
    """Proven optima, from the problem README's table, transcribed as exact points.

    n=1: single point, d=0.   n=2: d=2.   n=3: d=2 (corners).
    n=4: three corners + centroid, d = 2 sqrt3.
    n=6: two rows (3+2+1) of the lattice, d = 4.
    n=10: Delta(4) lattice triangle, d = 6.
    These are s(n) = d + 2 sqrt3 with s(3)=2+2sqrt3, s(6)=4+2sqrt3, s(10)=6+2sqrt3.
    """
    out = []
    # n = 3 : corners of the triangle, d = 2
    d = E(2, 0)
    out.append((3, d, [(E(0), E(0)), (E(2), E(0)), (E(1), E(0, 1))]))
    # n = 4 : corners + centroid, d = 2 sqrt3
    d = E(0, 2)
    out.append((4, d, [(E(0), E(0)), (E(0, 2), E(0)), (E(0, 1), E(3)), (E(0, 1), E(1))]))
    # n = Delta(k) lattice triangles, d = 2(k-1)
    for k in (2, 3, 4, 5):
        d = E(2 * (k - 1), 0)
        pts = []
        for r in range(k):
            for x in range(r, 2 * (k - 1) - r + 1, 2):
                pts.append((E(x), E(0, r)))
        out.append((k * (k + 1) // 2, d, pts))
    return out


def selftest(verbose=True):
    ok = True
    for n, d, pts in _known_optima():
        s = d + E(0, 2)
        r = check(n, s, pts)
        good = r["ok"] and r["tight"]
        ok &= good
        if verbose:
            print("  POSITIVE n=%-3d d=%-10s -> ok=%s tight=%s minsq=%s"
                  % (n, d.s(), r["ok"], r["tight"], r.get("min_sq_distance")))
        assert good, r

    # negative controls
    n, d, pts = _known_optima()[3]          # Delta(3) = 6, d = 4
    s = d + E(0, 2)
    neg = []
    # (1) duplicate point
    p2 = list(pts); p2[1] = p2[0]
    neg.append(("duplicate", check(n, s, p2), False, None))
    # (2) s deflated by 1  -> must reject
    neg.append(("s deflated", check(n, s - E(1), pts), False, None))
    # (3) s inflated by 1  -> must ACCEPT but report NOT tight
    neg.append(("s inflated", check(n, s + E(1), pts), True, False))
    # (4) one point nudged out of the triangle by 1/1000
    p4 = list(pts); p4[0] = (p4[0][0] - E(F(1, 1000)), p4[0][1])
    neg.append(("outside", check(n, s, p4), False, None))
    # (5) two points at distance just under 2: 1999/1000
    p5 = [(E(0), E(0)), (E(F(1999, 1000)), E(0)), (E(1), E(0, 1))]
    neg.append(("overlap 1999/1000", check(3, E(2, 2), p5), False, None))
    for nm, r, want_ok, want_tight in neg:
        good = (r["ok"] == want_ok) and (want_tight is None or r["tight"] == want_tight)
        ok &= good
        if verbose:
            print("  NEGATIVE %-18s -> ok=%s tight=%s  (expected ok=%s tight=%s) %s"
                  % (nm, r["ok"], r["tight"], want_ok, want_tight, "PASS" if good else "FAIL"))
        assert good, (nm, r)
    print("checker selftest OK" if ok else "checker selftest FAILED")
    return ok


if __name__ == "__main__":
    selftest()
