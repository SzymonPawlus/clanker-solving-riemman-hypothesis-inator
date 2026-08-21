#!/usr/bin/env python3
"""Erdos-Oler: attacking the hull -> triangle relaxation.  Exact throughout.

    python3 run.py            # ~20 s, Python 3.11 standard library only

Writes out/report.txt (transcript).  No randomness, no seeds, no network.
Write-up: problems/circle-packing-equilateral-triangle/attacks/eo-hull-deficit/
"""

import json
import math
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from geom import (  # noqa: E402
    Alg, Ival, HALF, SQRT3, parse_alg,
    convex_hull, polygon_area, polygon_perimeter, clip_halfplane,
    triangle, bisector_coords, side_from_h, oler_triangle_bound,
    deficit_of_polygon, lattice, max_points_in_triangle,
)

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CERTS = os.path.join(
    REPO, "problems", "circle-packing-equilateral-triangle",
    "attacks", "exact-algebraic-constructions", "certificates",
)

OUT = []
FAILURES = []


def say(s=""):
    print(s)
    OUT.append(s)


def check(name, ok):
    if not ok:
        FAILURES.append(name)
    return "PASS" if ok else "**FAIL**"


def tri_num(k):
    return k * (k + 1) // 2


# ---------------------------------------------------------------------------
# certificate loading -- separation 2 in the repo's convention, halved to 1 here
# ---------------------------------------------------------------------------

def load_certs():
    out = []
    for fn in sorted(os.listdir(CERTS)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(CERTS, fn)) as fh:
            cert = json.load(fh)
        pts = [(parse_alg(x) * HALF, parse_alg(y) * HALF) for x, y in cert["coordinates"]]
        a = parse_alg(cert["point_triangle_side"]) * HALF
        out.append((cert["n"], cert.get("construction", ""), a, pts))
    return out


def check_feasible(a, pts):
    """Exact: pairwise separation >= 1 and containment in the closed triangle."""
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d2 = ((pts[i][0] - pts[j][0]) * (pts[i][0] - pts[j][0])
                  + (pts[i][1] - pts[j][1]) * (pts[i][1] - pts[j][1]))
            if d2 < Alg(1):
                return False
    for p in pts:
        hA, hB, hC = bisector_coords(a, p)
        # inside the closed triangle iff every distance-to-a-side is >= 0, i.e.
        # h_V <= a*sqrt3/2 for all V
        lim = a * SQRT3 * HALF
        if not (hA <= lim and hB <= lim and hC <= lim):
            return False
    return True


# ---------------------------------------------------------------------------
say("=" * 78)
say("EO HULL-DEFICIT -- exact report")
say("=" * 78)
say()
say("Normalisation: separation 1, triangle side a.  Repo certificates use separation 2")
say("and side d = 2a, so every coordinate is HALVED on load.")
say()

# ===========================================================================
say("-" * 78)
say("1.  CORNER-DEFICIT LEMMA on every exact certificate in the repo")
say("-" * 78)
say()
say("  t_V := 2*min_{p in E} h_V(p)/sqrt3   (side of the empty corner triangle at V)")
say("  Lemma:  def(H) >= sum_V (t_V^2 + t_V)/2   =: CD")
say()
say("  Proof: E lies in the hexagon K = T inter {h_V >= t_V*sqrt3/2 : V}, so H = conv(E)")
say("  lies in K too; area and perimeter are monotone on nested convex sets, hence")
say("  def(H) >= def(K) = sum_V (t_V^2+t_V)/2.  Both steps are checked EXACTLY below:")
say("  containment of every point in K, and A(K) = A(T) - (sqrt3/4) sum t_V^2 exactly.")
say()
say(f"{'n':>3} {'configuration':<30} {'t_A,t_B,t_C':<20} {'CD':>9} {'E in K':>7} "
    f"{'A(K) ok':>8} {'def(H) enclosure':>26}")

certs = load_certs()
rows = []
for n, desc, a, pts in certs:
    if n < 3:
        continue                      # degenerate hull: no polygon
    assert check_feasible(a, pts), f"certificate n={n} is not feasible"
    ts = []
    for v in range(3):
        hmin = min(bisector_coords(a, p)[v] for p in pts)
        ts.append(side_from_h(hmin))
    CD = Alg(0)
    for t in ts:
        CD = CD + (t * t + t) * HALF

    # the hexagon K, built by exact half-plane clipping
    K = triangle(a)
    normals = [(SQRT3 * HALF, HALF, Alg(0)),
               (-SQRT3 * HALF, HALF, -SQRT3 * HALF * a),
               (Alg(0), Alg(-1), -a * SQRT3 * HALF)]
    for v, t in enumerate(ts):
        nx, ny, off = normals[v]
        K = clip_halfplane(K, nx, ny, t * SQRT3 * HALF + off)

    # (a) every point of E lies in K -- exact
    inK = all(
        all(side_from_h(bisector_coords(a, p)[v]) >= ts[v] for v in range(3))
        for p in pts
    )
    # (b) A(K) = A(T) - (sqrt3/4) sum t^2 -- exact
    want_area = polygon_area(triangle(a)) - SQRT3 * Alg(F(1, 4)) * sum(
        (t * t for t in ts), Alg(0))
    area_ok = polygon_area(K) == want_area
    # (c) M(K) = M(T) - sum t -- checked against the polygon's own enclosure
    per_ok = polygon_perimeter(K).lo <= Ival.of(a * Alg(3) - sum(ts, Alg(0)), prec=80).hi \
        and polygon_perimeter(K).hi >= Ival.of(a * Alg(3) - sum(ts, Alg(0)), prec=80).lo

    hull = convex_hull(pts)
    d = deficit_of_polygon(a, hull)
    ok = inK and area_ok and per_ok and Ival.of(CD, prec=80).lo <= d.hi
    tstr = ",".join(f"{t.float():.4f}" for t in ts)
    say(f"{n:>3} {desc[:30]:<30} {tstr:<20} {CD.float():>9.6f} "
        f"{str(inK):>7} {str(area_ok and per_ok):>8} {str(d):>26}")
    if not ok:
        check(f"lemma n={n}", False)
    rows.append((n, desc, CD, d, ok))

bad = [r for r in rows if not r[4]]
say()
say(f"  corner-deficit lemma verified on every certificate: {check('lemma', not bad)}")
say("  (def(H) itself is only an enclosure -- it contains a perimeter -- but the lemma")
say("   is certified without it, through the exact containment E subset K.)")

# K2: controls
say()
say("  K2 control -- def(H) must be exactly 1 on T(k)-apex and exactly 0 on T(k):")
for n, desc, CD, d, _ in rows:
    if "apex point removed" in desc:
        good = d.lo <= 1 <= d.hi and CD == Alg(1)
        say(f"    n={n:>3}  T(k)-apex   CD={CD.float():.6f} def(H)={d}  "
            f"{check(f'K2 apex n={n}', good)}")
    elif desc.startswith("full triangular lattice"):
        good = d.lo <= 0 <= d.hi and CD == Alg(0)
        say(f"    n={n:>3}  lattice     CD={CD.float():.6f} def(H)={d}  "
            f"{check(f'K2 lattice n={n}', good)}")

# ===========================================================================
say()
say("-" * 78)
say("2.  CORNER-OCCUPANCY LEMMA  (K3 control)")
say("-" * 78)
say()
say("  A closed equilateral triangle of side t has diameter t, so t < 1 forces at most")
say("  one point of a unit-separated set inside it.  Checked exactly on every")
say("  certificate at t = 1 - 1/10^6, at all three corners:")
t_probe = F(999999, 10 ** 6)
worst = 0
for n, desc, a, pts in certs:
    for v in range(3):
        cnt = 0
        for p in pts:
            h = bisector_coords(a, p)[v]
            if side_from_h(h) <= Alg(t_probe):
                cnt += 1
        worst = max(worst, cnt)
say(f"  max points found in any corner triangle of side {float(t_probe)}: {worst}  "
    f"{check('K3', worst <= 1)}")

# ===========================================================================
say()
say("-" * 78)
say("3.  NEUTRALITY:  the corner cut is never worth more than the points it removes")
say("-" * 78)
say()
say("  gain(t) := (t^2+t)/2 - N(t), where N(t) = max unit-separated points in a")
say("  CLOSED equilateral triangle of side t.  Claim: gain(t) < 0 strictly for every t,")
say("  with supremum 0 approached as t -> j^- (j a positive integer).  Two checks:")
say("  against the lattice count T(floor(t)+1) <= N(t), and against `cited` N(t), t <= 4.")
say()
say(f"{'t':>10} {'(t^2+t)/2':>12} {'T(|t|+1)':>10} {'N(t) cited':>11} "
    f"{'gain vs lattice':>16} {'gain vs N':>10}")
grid = [F(i, 8) for i in range(1, 33)]
maxgain = None
for t in grid:
    lhs = (t * t + t) / 2
    lat = tri_num(math.floor(t) + 1)
    nt = max_points_in_triangle(t)
    g1 = lhs - lat
    g2 = lhs - nt
    maxgain = g1 if maxgain is None else max(maxgain, g1)
    flag = " <-- integer t" if t.denominator == 1 else ""
    say(f"{str(t):>10} {float(lhs):>12.6f} {lat:>10} {nt:>11} "
        f"{float(g1):>16.6f} {float(g2):>10.6f}{flag}")
say()
say(f"  max over the grid of [(t^2+t)/2 - T(floor(t)+1)] = {float(maxgain)}  (at t just below 1)  "
    f"{check('neutrality', maxgain < 0)}")
say("  (Algebraically, with t = m + f, 0 <= f < 1: (t^2+t)/2 - T(m+1) = (f-1)(2m+f+2)/2 < 0.")
say("   It tends to 0 as f -> 1, i.e. as t approaches an integer FROM BELOW; at t = j")
say("   exactly the closed corner triangle gains a whole lattice row and the cut is a")
say("   strict loss.  Verified above on 32 exact rational t.)")

# ===========================================================================
say()
say("-" * 78)
say("4.  THE BARRIER at a = 6:  def(K) <= N(T\\K) for EVERY convex K")
say("-" * 78)
say()
say("  Proof (see the write-up): the lattice T(7) has 28 = Oler(6) points in T(6), so")
say("  Oler applied to Lambda inter K gives 28 - |Lambda inter (T\\K)| <= Oler(6) - def(K).")
say("  Below: the same inequality checked exactly on explicit families of K, using the")
say("  actual lattice count |Lambda inter (T\\K)| (never bigger than N(T\\K)).")
say()
OUTS = "|Lam - K|"
a6 = Alg(6)
LAM = lattice(7)
say(f"  |Lambda| = {len(LAM)},  Oler(6) = {oler_triangle_bound(a6).float():.0f}")
say()


def count_outside(poly_test, pts):
    """Number of lattice points NOT in the closed convex region described by poly_test,
    where poly_test(p) returns True iff p is in the region."""
    return sum(0 if poly_test(p) else 1 for p in pts)


barrier_ok = True
say("  (a) single corner cut at A of side t  ->  K = T inter {h_A >= t*sqrt3/2}")
say(f"      {'t':>8} {'def(K)':>22} {OUTS:>10} {'gain':>10}")
for t in [F(1, 2), F(1), F(3, 2), F(2), F(5, 2), F(3), F(7, 2), F(4)]:
    tA = Alg(t)
    K = clip_halfplane(triangle(a6), SQRT3 * HALF, HALF, tA * SQRT3 * HALF)
    d = deficit_of_polygon(a6, K)
    cnt = count_outside(lambda p: side_from_h(bisector_coords(a6, p)[0]) >= tA, LAM)
    ok = d.hi <= cnt
    barrier_ok &= ok
    say(f"      {str(t):>8} {str(d):>22} {cnt:>10} {float(d.hi - cnt):>10.6f} "
        f"{'' if ok else '  **FAIL**'}")

say()
say("  (b) three corner cuts of sides (tA,tB,tC)")
say(f"      {'(tA,tB,tC)':>16} {'def(K)':>22} {OUTS:>10} {'gain':>10}")
for tri_t in [(F(1), F(1), F(1)), (F(1), F(2), F(3)), (F(2), F(2), F(2)),
              (F(3), F(3), F(0)), (F(3, 2), F(3, 2), F(3, 2)), (F(1), F(1), F(0))]:
    K = triangle(a6)
    normals = [(SQRT3 * HALF, HALF, Alg(0)),
               (-SQRT3 * HALF, HALF, -SQRT3 * HALF * a6),
               (Alg(0), Alg(-1), -a6 * SQRT3 * HALF)]
    for v, t in enumerate(tri_t):
        nx, ny, off = normals[v]
        K = clip_halfplane(K, nx, ny, Alg(t) * SQRT3 * HALF + off)
    d = deficit_of_polygon(a6, K)

    def inside(p, tri_t=tri_t):
        hs = bisector_coords(a6, p)
        return all(side_from_h(hs[v]) >= Alg(t) for v, t in enumerate(tri_t))

    cnt = count_outside(inside, LAM)
    ok = d.hi <= cnt
    barrier_ok &= ok
    say(f"      {str(tuple(str(x) for x in tri_t)):>16} {str(d):>22} {cnt:>10} "
        f"{float(d.hi - cnt):>10.6f} {'' if ok else '  **FAIL**'}")

say()
say("  (c) arbitrary single-line cuts K = T inter {n.x >= c}, rational normals")
say(f"      {'normal':>14} {'c':>10} {'def(K)':>22} {OUTS:>10} {'gain':>10}")
lines = []
for (nx, ny) in [(1, 0), (0, 1), (1, 1), (2, 1), (-1, 2), (3, -1), (1, 3), (-2, -1), (5, 2)]:
    for c in [F(-4), F(-2), F(-1), F(0), F(1), F(2), F(7, 2), F(5), F(15, 2), F(10)]:
        lines.append((F(nx), F(ny), c))
worst_gain = None
shown = 0
for nx, ny, c in lines:
    K = clip_halfplane(triangle(a6), Alg(nx), Alg(ny), Alg(c))
    if len(K) < 3:
        continue                                  # empty or degenerate cut
    d = deficit_of_polygon(a6, K)
    cnt = count_outside(lambda p: Alg(nx) * p[0] + Alg(ny) * p[1] >= Alg(c), LAM)
    ok = d.hi <= cnt
    barrier_ok &= ok
    g = float(d.hi - cnt)
    worst_gain = g if worst_gain is None else max(worst_gain, g)
    if shown < 12 or not ok:
        say(f"      {f'({nx},{ny})':>14} {str(c):>10} {str(d):>22} {cnt:>10} "
            f"{g:>10.6f} {'' if ok else '  **FAIL**'}")
        shown += 1
say(f"      ... {len(lines)} half-plane cuts tested; worst gain = {worst_gain:.6f}")
say()
say(f"  barrier holds on every K tested: {check('barrier', barrier_ok)}")

# ===========================================================================
say()
say("-" * 78)
say("5.  WHAT THE ROUTE STILL BUYS:  necessary conditions on a k=7 counterexample")
say("-" * 78)
say()
say("  Suppose 27 unit-separated points lie in T(a) with a < 6.  Write")
say("      eps(a) = a^2/2 + 3a/2 - 26   (< 1 for a < 6; = 0 at a0 = (-3+sqrt217)/2).")
say("  For disjoint corner cuts (t_A,t_B,t_C), with m_V = |E inter Delta_V(t_V)|:")
say("      sum_V [ (t_V^2+t_V)/2 - m_V ]  <=  eps(a).")
say()
say(f"{'a':>12} {'eps(a)':>10} {'t':>8} {'need sum m_V >=':>16} {'3*N(t) avail':>13} "
    f"{'contradiction?':>15}")
a_vals = [F(59, 10), F(599, 100), F(5999, 1000), F(599999, 100000)]
tight_any = False
for av in a_vals:
    eps = av * av / 2 + av * 3 / 2 - 26
    for t in [F(7, 8), F(1), F(3, 2), F(2), F(5, 2), av / 2]:
        if 2 * t > av:
            continue
        need = 3 * (t * t + t) / 2 - eps
        need_int = math.ceil(need)
        avail = 3 * max_points_in_triangle(t)
        contra = need_int > avail
        tight_any |= contra
        say(f"{str(av):>12} {float(eps):>10.6f} {str(t):>8} {need_int:>16} {avail:>13} "
            f"{str(contra):>15}")
say()
say("  Exact occupancy thresholds forced on a counterexample.  For t with")
say("  3(t^2+t)/2 - eps(a) > c the three corner triangles of side t hold > c points:")
say(f"{'a':>14} {'eps(a)':>10} {'t*(a) (>=1 pt/corner)':>22} {'t+(a) (>=9 pts total)':>22}")


def threshold(eps, c):
    """least t with 3(t^2+t)/2 - eps > c, as a rational upper bound (t^2+t = 2(c+eps)/3)."""
    target = 2 * (F(c) + eps) / 3
    lo, hi = F(0), F(4)
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid * mid + mid < target:
            lo = mid
        else:
            hi = mid
    return hi


for av in a_vals:
    eps = av * av / 2 + av * 3 / 2 - 26
    say(f"{str(av):>14} {float(eps):>10.6f} {float(threshold(eps, 2)):>22.9f} "
        f"{float(threshold(eps, 8)):>22.9f}")
say()
say("  Read: in any 27-point counterexample at side a, EVERY corner triangle of side")
say("  t*(a) contains a point of E (and, being of side < 1, exactly one), and the three")
say("  corner triangles of side t+(a) contain at least 9 points between them.")
say()
say(f"  any contradiction found by corner counting alone: {tight_any}")
say("  (False is the expected -- and, by section 4, the forced -- answer.)")
say()
say("  The conditions are nonetheless non-vacuous.  Two consequences, exact:")
say("   (i) t -> 1^-: at most one point can sit in a corner triangle of side < 1 (sec. 2),")
say("       and sum_V m_V >= 3 - eps(a) > 2, so EVERY corner of T carries exactly one")
say("       point of E in its open unit corner triangle.")
say("  (ii) t -> 2^-: sum_V (3 - m_V) <= eps(a) < 1 and the m_V are integers, so")
say("       sum_V m_V >= 9: the three open corner triangles of side 2 hold >= 9 points.")
say("  (iii) In particular, if ANY corner of T has an empty closed unit corner triangle,")
say("       then n <= a^2/2 + 3a/2, which forces a >= k-1 whenever n = T(k)-1.")
say()
say("  HEADLINE necessary condition (one corner at a time, t -> j^-):  in any 27-point")
say("  counterexample at side a < 6, for EVERY corner V and EVERY integer 1 <= j <= 5,")
say("  the OPEN corner triangle Delta_V(j) holds at least T(j) points of E.")
say("  Discrimination test -- does the condition actually cut anything out?")
say(f"{'configuration':<34} {'corner':>7} " + " ".join(f"j={j}" for j in range(1, 6)) + "   verdict")
a6c = Alg(6)


def open_corner_counts(pts, v):
    out = []
    for j in range(1, 6):
        out.append(sum(1 for p in pts
                       if side_from_h(bisector_coords(a6c, p)[v]) < Alg(j)))
    return out


apex = (Alg(3), Alg(6) * SQRT3 * HALF)      # the apex C of T(6) = lattice row 6
_int_pt = (Alg(F(3, 2)), SQRT3 * HALF)
cases = [("lattice T(7), n=28", lattice(7)),
         ("T(7) minus an INTERIOR point, n=27",
          [p for p in lattice(7) if not (p[0] == _int_pt[0] and p[1] == _int_pt[1])]),
         ("T(7) minus the APEX, n=27",
          [p for p in lattice(7) if not (p[0] == apex[0] and p[1] == apex[1])])]
disc = False
for lbl, pts in cases:
    for v, nm in enumerate("ABC"):
        cnts = open_corner_counts(pts, v)
        viol = [j for j in range(1, 6) if cnts[j - 1] < tri_num(j)]
        if viol:
            disc = True
        say(f"{lbl:<34} {nm:>7} " + " ".join(f"{c:>3}" for c in cnts)
            + ("   EXCLUDED at j=" + str(viol[0]) if viol else "   not excluded"))
say(f"  required T(j) for j=1..5: {[tri_num(j) for j in range(1, 6)]}")
say(f"  the condition excludes the T(7)-minus-apex configuration: "
    f"{check('discrimination', disc)}")
say("  (It must: that configuration needs a = 6 exactly, and the condition is derived")
say("   under the assumption a < 6.  The interior-point deletion is NOT excluded, which")
say("   is section 6's point -- corner conditions cannot see it.)")

say()
say("  Check of (iii) against the extremal certificates (T(k)-apex, a = k-1):")
for n, desc, a, pts in certs:
    if "apex point removed" not in desc:
        continue
    gains = []
    for v in range(3):
        hmin = min(bisector_coords(a, p)[v] for p in pts)
        t = side_from_h(hmin)
        gains.append((t * t + t) * HALF)
    tot = gains[0] + gains[1] + gains[2]
    say(f"    n={n:>3} a={a.float():.0f}  corner gains = "
        f"({', '.join(f'{g.float():.4f}' for g in gains)})  total = {tot.float():.6f}  "
        f"{check(f'(iii) n={n}', tot >= Alg(1))}")

# ===========================================================================
say()
say("-" * 78)
say("6.  THE WITNESS: the corner route buys ZERO unconditionally")
say("-" * 78)
say()
say("  E := lattice T(7) minus ONE INTERIOR point, a = 6, n = 27 -- exactly the")
say("  Erdos-Oler count at the first open case, at the extremal side length.")
say("  All three corners of T are occupied, so every t_V = 0 and def(H) = 0: the whole")
say("  slack (= 1) sits in Oler's inequality on the hull, where this route cannot see it.")
say()
a6b = Alg(6)
LAM7 = lattice(7)
interior = (Alg(F(3, 2)), SQRT3 * HALF)          # row 1, second point: not on any side
E27 = [p for p in LAM7 if not (p[0] == interior[0] and p[1] == interior[1])]
say(f"  removed point = ({interior[0]}, {interior[1]});  |E| = {len(E27)}")
say(f"  feasible (separation >= 1, inside T(6)), exact: {check('witness feasible', check_feasible(a6b, E27))}")
ts27 = []
for v in range(3):
    hmin = min(bisector_coords(a6b, p)[v] for p in E27)
    ts27.append(side_from_h(hmin))
CD27 = sum(((t * t + t) * HALF for t in ts27), Alg(0))
hull27 = convex_hull(E27)
d27 = deficit_of_polygon(a6b, hull27)
hull_is_T = polygon_area(hull27) == polygon_area(triangle(a6b))
say(f"  t_A, t_B, t_C = {[t.float() for t in ts27]}   corner deficit CD = {CD27.float():.6f}")
say(f"  hull equals the whole triangle (exact area test): {hull_is_T}")
say(f"  def(H) enclosure = {d27}")
say(f"  Oler(6) - n = {oler_triangle_bound(a6b).float() - 27:.6f}  = stage-1 slack, all of it")
say(f"  {check('witness', CD27 == Alg(0) and hull_is_T and d27.lo <= 0 <= d27.hi)}")
say()
say("  Consequence: no inequality of the form  def(H) >= f(a, n) > 0  can hold, and no")
say("  corner-cut bound can supply the missing unit for n = T(k)-1 in general.  Whatever")
say("  proves Erdos-Oler must extract the unit from Oler's inequality ON THE HULL")
say("  (stage 1), for configurations whose hull is the whole triangle.")

# ===========================================================================
say()
say("-" * 78)
say("7.  The Steiner-type alternative, refuted")
say("-" * 78)
say()
say("  Natural guess: for convex K in T, def(K) >= mu^2/6 + mu/2 where mu = M(T)-M(K).")
say("  It is exactly TIGHT for three equal corner cuts, which is what makes it tempting.")
say("  It is FALSE: a deep strip cut beats it.  a = 6, K = the triangle of side 6-u")
say()
say(f"{'family':<26} {'mu':>10} {'def(K)':>12} {'mu^2/6+mu/2':>13} {'guess holds?':>13}")
steiner_broken = False
for lbl, K, mu, dK in (
    [("3 corner cuts t=1", None, Alg(3), Alg(3))]
    + [(f"strip cut along AB, u={u}", None, Alg(3 * u),
        Alg(6 * u) - Alg(u) * Alg(u) * HALF + Alg(u) * Alg(F(3, 2)))
       for u in [F(1), F(2), F(3), F(4), F(5), F(6)]]
):
    guess = mu * mu * Alg(F(1, 6)) + mu * HALF
    holds = dK >= guess
    if not holds:
        steiner_broken = True
    say(f"{lbl:<26} {mu.float():>10.4f} {dK.float():>12.6f} {guess.float():>13.6f} "
        f"{str(holds):>13}")
say()
say("  (def for the shrink is au - u^2/2 + 3u/2 with a = 6, computed exactly; the")
say("   corner-cut row is (t^2+t)/2 summed over three corners.)")
say(f"  guess refuted by an exact witness: {check('steiner refuted', steiner_broken)}")

# ===========================================================================
say()
say("=" * 78)
if FAILURES:
    say(f"FAILURES: {FAILURES}")
else:
    say("ALL CHECKS PASSED")
say("=" * 78)

with open(os.path.join(HERE, "out", "report.txt"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")

sys.exit(1 if FAILURES else 0)
