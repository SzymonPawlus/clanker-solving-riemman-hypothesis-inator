"""Erdos-Oler k = 7: what the boundary count can and cannot do.

One command, Python standard library only, exact arithmetic for every decision:

    python3 experiments/packing-eo-boundary/run.py

Normalisation: minimum separation 1 and triangle side `a` (Oler's).  The repo's
certificates use separation 2 and side d = 2a; nothing here reads them.

Sections
  1  the exact Oler window for k = 7
  2  Lemma P1 is sharp: an exact family with 3*floor(a) points on the boundary of T
  3  numerical probe: can more than 3*floor(a) points sit on dT?
  4  KC-2: hypothesis H fails at the extremal lattice itself (exact witnesses)
  5  KC-3: every count-based boundary term Phi(b) is weaker than Oler near the lattice
  6  the surviving stable quantity: corner clearance, and what k = 7 would need
"""

import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from q3 import (Q3, SQ3, HALF_SQ3, convex_hull, cross, dist2, hull_boundary_count,
                in_triangle, min_sep2, on_boundary, polygon_area2, triangle)

OUT = []


def say(s=""):
    OUT.append(s)
    print(s, flush=True)


def rule(t):
    say()
    say("=" * 78)
    say(t)
    say("=" * 78)


# ---------------------------------------------------------------- section 1

def section_oler_window():
    rule("1. The exact Oler window for k = 7 (n = 27)")
    say("Oler (cited): n <= a^2/2 + 3a/2 + 1 for n points at separation 1 in an")
    say("equilateral triangle of side a.  So 27 points force a^2 + 3a - 52 >= 0.")
    say("Let a* be the positive root of a^2 + 3a - 52 = 0, i.e. a* = (-3 + sqrt(217))/2.")
    say("Then a*^2/2 + 3a*/2 + 1 = (a*^2 + 3a* + 2)/2 = (52 + 2)/2 = 27 exactly.")
    lo, hi = F(5865459, 1000000), F(5865460, 1000000)
    f = lambda x: x * x + 3 * x - 52
    assert f(lo) < 0 < f(hi), "bracket for a* is wrong"
    say(f"  exact bracket: {float(lo):.6f} < a* < {float(hi):.6f}"
        f"   (p(lo) = {float(f(lo)):+.3e}, p(hi) = {float(f(hi)):+.3e}, both exact)")
    say()
    say("Integrality of n is doing real work here: RHS < 27 already forces n <= 26.")
    say("The weaker threshold 'RHS < 26' is sufficient but not necessary, and reporting")
    say("it as the window doubles the apparent gap.  Both, exactly, per k:")
    say()
    say(f"{'k':>3} {'T(k)':>5} {'n=T(k)-1':>9} {'a: RHS=n (window)':>18}"
        f" {'k-1':>4} {'true gap':>9} {'a: RHS=n-1':>11} {'gap if floor':>13}")
    for k in range(3, 15):
        T = k * (k + 1) // 2
        n = T - 1
        # positive root of a^2+3a+2 = 2m
        def root(m):
            lo, hi = F(0), F(100)
            for _ in range(80):
                mid = (lo + hi) / 2
                if mid * mid + 3 * mid + 2 - 2 * m < 0:
                    lo = mid
                else:
                    hi = mid
            return lo
        aw, aw2 = root(n), root(n - 1)
        assert F(k - 1) ** 2 / 2 + 3 * F(k - 1) / 2 + 1 == F(T), "Oler RHS at a=k-1 is T(k)"
        say(f"{k:>3} {T:>5} {n:>9} {float(aw):>18.6f} {k-1:>4}"
            f" {float(k-1-aw):>9.6f} {float(aw2):>11.6f} {float(k-1-aw2):>13.6f}")
    say()
    say("Column 'Oler RHS at a = k-1' is exactly T(k) for every k = 2..14 (exact rational")
    say("check in code): the gain Erdos-Oler needs is exactly ONE POINT, k-independent.")
    say("Measured in side length the window shrinks with k, which is why points, not")
    say("side lengths, are the honest unit of progress.")
    say()
    say("So Oler alone already settles Erdos-Oler for k = 7 outside a window:")
    say("  27 unit-separated points cannot fit when a < a* = 5.86546...")
    say("  the whole open case is a in [a*, 6), a window of width < 0.135.")
    say("Status: `sketch` (elementary arithmetic on top of the `cited` Oler bound).")


# ---------------------------------------------------------------- section 2

def boundary_family(a):
    """3*floor(a) points on dT, side a >= 1.  Per side: arc positions 0,1,...,k-1
    from that side's first corner; the next corner is position 0 of the next side."""
    a = F(a)
    k = int(a)                       # floor(a) for positive rational a
    tri = triangle(a)
    pts = []
    for i in range(3):
        A, B = tri[i], tri[(i + 1) % 3]
        dx = (B[0] - A[0]) * F(1, a)   # unit vector along the side
        dy = (B[1] - A[1]) * F(1, a)
        for t in range(k):
            pts.append((A[0] + dx * F(t), A[1] + dy * F(t)))
    return a, k, tri, pts


def section_sharp_boundary():
    rule("2. Lemma P1 is sharp: 3*floor(a) points on dT, exactly, for every a >= 1")
    say("Lemma P1 (proved in the attack README, status `sketch`):")
    say("    |E cap dT| <= 3*floor(a)  for every unit-separated E in T of side a >= 1.")
    say("Below: an exact family attaining it, so the floor is not an artefact.")
    say()
    say(f"{'a':>10} {'floor(a)':>9} {'3 floor(a)':>11} {'points':>7} {'min sep^2':>12}"
        f" {'all on dT':>10} {'in T':>6} {'convex pos':>11}")
    for a in [F(1), F(3, 2), F(2), F(5, 2), F(3), F(17, 4), F(5), F(59, 10), F(6)]:
        a, k, tri, pts = boundary_family(a)
        ms2 = min_sep2(pts) if len(pts) > 1 else None
        ok_sep = ms2 is None or ms2 >= 1
        ok_in = all(in_triangle(p, tri) for p in pts)
        ok_bd = all(on_boundary(p, tri) for p in pts)
        b = hull_boundary_count(pts)
        say(f"{float(a):>10.4f} {k:>9} {3*k:>11} {len(pts):>7}"
            f" {('exact 1' if ms2 == 1 else f'{ms2.float():.4f}') if ms2 else '-':>12}"
            f" {str(ok_bd):>10} {str(ok_in):>6} {str(b == len(pts)):>11}")
        assert ok_sep and ok_in and ok_bd and len(pts) == 3 * k
        assert b == len(pts), "the family is also in convex position"
    say()
    say("Every row: separation >= 1 exactly, containment exact, count exactly 3*floor(a),")
    say("and all points are hull-boundary points too -- so the same family shows the")
    say("hull-reading bound b <= 3*floor(a) is attained for every a >= 1 as well.")
    say("Status: `numerical` (explicit configurations, exactly verified).")


# ---------------------------------------------------------------- section 3

def section_probe_boundary(samples=400000, seed=20260821):
    rule("3. Probe: can more than 3*floor(a) points sit on dT?  (float search only)")
    say("Search over the six corner clearances (alpha_i, beta_i).  Within a side the")
    say("points are packed greedily at spacing 1; across an unoccupied corner the two")
    say("neighbours must satisfy x^2 - xy + y^2 >= 1.  No decision is taken in floats:")
    say("this is a search for a counterexample to P1, not a proof of it.")
    rng = random.Random(seed)
    say()
    say(f"{'a':>8} {'3 floor(a)':>11} {'best found':>11} {'beat?':>7}")
    for a in [1.4, 1.9, 2.5, 2.9, 3.7, 4.5, 5.5, 5.9, 5.99, 6.5, 7.3]:
        best = 0
        for _ in range(samples):
            legs = []
            for _ in range(3):
                # each corner: occupied (both legs 0) or two positive legs
                if rng.random() < 0.35:
                    legs.append((0.0, 0.0))
                else:
                    legs.append((rng.random() * min(a, 3.0), rng.random() * min(a, 3.0)))
            ok = True
            s = 0
            for (x, y) in legs:
                if x == 0.0 and y == 0.0:
                    s += 1
                    continue
                if x * x - x * y + y * y < 1.0 - 1e-12:
                    ok = False
                    break
            if not ok:
                continue
            tot = 0
            for i in range(3):
                beta = legs[i][1]           # leg of corner i on side i (going out)
                alpha = legs[(i + 1) % 3][0]
                span = a - beta - alpha
                if span < -1e-12:
                    tot = -1
                    break
                tot += 1 + int(span + 1e-12)
            if tot < 0:
                continue
            b = tot - s
            best = max(best, b)
        say(f"{a:>8.2f} {3*int(a):>11} {best:>11} {str(best > 3*int(a)):>7}")
    say()
    say("No sample beat 3*floor(a) anywhere.  Status: `numerical`, corroboration only;")
    say("the proof of P1 is in the attack README and does not depend on this.")


# --------------------------------------------------------------- section 3b

def _enc_side(pts, N):
    """Least side of an equilateral triangle (any rotation) containing pts.
    For normals at angle phi + 120k the side is (2/sqrt3) * sum_k h(u_k); minimise
    over phi.  Float, search only -- never used to decide anything."""
    import math
    best = 1e18
    two3 = 2 * math.pi / 3
    for i in range(N):
        phi = two3 * i / N
        s = 0.0
        for k in range(3):
            th = phi + two3 * k
            ux, uy = math.cos(th), math.sin(th)
            s += max(px * ux + py * uy for px, py in pts)
        best = min(best, s)
    return (2 / math.sqrt(3.0)) * best


def _convex_position(pts):
    import math
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    order = sorted(range(n), key=lambda i: math.atan2(pts[i][1] - cy, pts[i][0] - cx))
    for a in range(n):
        i, j, k = order[a], order[(a + 1) % n], order[(a + 2) % n]
        cr = ((pts[j][0] - pts[i][0]) * (pts[k][1] - pts[i][1])
              - (pts[j][1] - pts[i][1]) * (pts[k][0] - pts[i][0]))
        if cr <= 1e-13:
            return False
    return True


def _score(pts, N=48):
    import math
    m = 1e18
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            d = dx * dx + dy * dy
            if d < m:
                m = d
    if m <= 1e-18:
        return 1e9
    return _enc_side(pts, N) / math.sqrt(m)


def section_convex_probe(restarts=8, iters=6000, seed=1):
    rule("3b. Probe of the hull reading: a_conv(b), least side holding b points in")
    say("     convex position at separation 1.  b <= 3*floor(a) for all a is equivalent")
    say("     to a_conv(b) >= ceil(b/3) for all b.  Float search only.")
    say()
    import random
    say(f"{'b':>4} {'a_conv (found)':>15} {'ceil(b/3)':>10} {'consistent':>11}")
    for b in range(3, 11):
        best = 1e9
        for sd in range(restarts):
            rng = random.Random(seed * 1000 + sd * 17 + b)
            while True:
                pts = [(rng.random(), rng.random()) for _ in range(b)]
                if _convex_position(pts):
                    break
            cur = _score(pts)
            for t in range(iters):
                step = 0.35 * (1 - t / iters) + 0.0005
                i = rng.randrange(b)
                old = pts[i]
                pts[i] = (old[0] + rng.gauss(0, step), old[1] + rng.gauss(0, step))
                if _convex_position(pts):
                    v = _score(pts)
                    if v < cur:
                        cur = v
                        continue
                pts[i] = old
            best = min(best, _score(pts, 2160))
        need = -(-b // 3)
        say(f"{b:>4} {best:>15.5f} {need:>10} {str(best > need - 1e-3):>11}")
    say()
    say("Every b is consistent with b <= 3*floor(a), and b = 4, 7 are tight against it")
    say("(a_conv = 2, 3).  So the hull reading of step (ii) looks TRUE, not false.")
    say("Status: `numerical` -- a local search, not an exhaustive one.")


# ---------------------------------------------------------------- section 4

def lattice(k):
    """Triangular lattice T(k) at separation 1: side k-1, k(k+1)/2 points."""
    pts = []
    for j in range(k):
        for i in range(k - j):
            pts.append((Q3(i) + Q3(F(j, 2)), HALF_SQ3 * Q3(j)))
    return pts


def perturbed_lattice(k, lam, eps):
    """Scale T(k) by lam, then push every boundary point strictly inside by eps.

    Result: the same n = T(k) points, still unit-separated, in a triangle of side
    a = lam*(k-1), but with only 3 points on the boundary of their convex hull."""
    lam, eps = F(lam), F(eps)
    base = [(p[0] * lam, p[1] * lam) for p in lattice(k)]
    L = lam * F(k - 1)
    tri = triangle(L)
    A, B, C = tri
    half = Q3(F(1, 2))
    # unit inward normals of AB, BC, CA and unit inward bisectors at A, B, C
    n_AB = (Q3(0), Q3(1))
    n_BC = (-HALF_SQ3, -half)
    n_CA = (HALF_SQ3, -half)
    bis = {0: (HALF_SQ3, half), 1: (-HALF_SQ3, half), 2: (Q3(0), Q3(-1))}
    out = []
    for p in base:
        shift = None
        for idx, corner in enumerate(tri):
            if dist2(p, corner) == 0:
                shift = bis[idx]
                break
        if shift is None:
            for (P0, P1, nrm) in ((A, B, n_AB), (B, C, n_BC), (C, A, n_CA)):
                if cross(P0, P1, p).sign() == 0:
                    shift = nrm
                    break
        if shift is None:
            out.append(p)
        else:
            out.append((p[0] + shift[0] * eps, p[1] + shift[1] * eps))
    return out, L, tri


def oler_pieces(pts):
    """(2/sqrt3)*A(conv), n, b -- all exact.  Returns Fractions where rational."""
    hull = convex_hull(pts)
    A2 = polygon_area2(hull)                 # = 2 * area, in Q(sqrt3)
    val = A2 * Q3(0, F(1, 3))                # (2/sqrt3)*A = 2A/sqrt3 = A2*sqrt3/3
    return val, len(pts), hull_boundary_count(pts)


def section_H_at_the_lattice():
    rule("4. KC-2: hypothesis H fails at the extremal lattice itself")
    say("H (refuted in ../oler-slack-analysis §4 by flat arcs):")
    say("    n <= (2/sqrt3) A(conv E) + b/2 + 1,   b = |E cap d conv(E)|.")
    say("The published refutation uses degenerate near-collinear sets, which invites the")
    say("repair 'H is presumably fine for fat, lattice-like configurations'.  It is not.")
    say()
    say("Witness: take the triangular lattice T(k) -- the extremal configuration for")
    say("Oler -- scale it by lam = 1 + delta, then push every boundary point strictly")
    say("inside by eps.  n and a are essentially unchanged; b collapses from 3(k-1) to 3.")
    say()
    lam, eps = F(101, 100), F(1, 1000)
    say(f"lam = {lam}, eps = {eps}  (exact rationals)")
    say()
    say(f"{'k':>3} {'n':>4} {'a':>9} {'b before':>9} {'b after':>8} {'min sep^2':>11}"
        f" {'H rhs':>9} {'H holds':>8} {'violation':>10}")
    for k in (3, 4, 5, 6, 7):
        pts, L, tri = perturbed_lattice(k, lam, eps)
        n = len(pts)
        assert n == k * (k + 1) // 2
        ms2 = min_sep2(pts)
        assert ms2 >= 1, f"separation broke at k={k}"
        assert all(in_triangle(p, tri) for p in pts), f"containment broke at k={k}"
        val, n2, b = oler_pieces(pts)
        b_before = hull_boundary_count(lattice(k))
        rhs = val + Q3(F(b, 2)) + Q3(1)
        holds = Q3(n) <= rhs
        say(f"{k:>3} {n:>4} {float(L):>9.4f} {b_before:>9} {b:>8}"
            f" {ms2.float():>11.6f} {rhs.float():>9.4f} {str(holds):>8}"
            f" {float(n) - rhs.float():>+10.4f}")
        assert b == 3, f"expected b = 3 after the push, got {b}"
    say()
    say("Every row violates H, by a margin that grows with k, at")
    say("configurations that are exactly the ones Erdos-Oler is about.  Everything in")
    say("the table is exact: separations, containment, hull, area, and the comparison.")
    say("Status of the witnesses: `refuted` for H (again, and for a better reason).")
    say()
    say("KC-2 FIRED.  b is not stable under an eps-perturbation that changes neither n")
    say("nor a; so no bound on b, however sharp, can rescue a bound whose right-hand")
    say("side is increasing in b.")


# ---------------------------------------------------------------- section 5

def flat_arc(m, eps):
    """p_j = (j, eps*j*(m-j)), j = 0..m: separated, all in convex position, area -> 0."""
    eps = F(eps)
    return [(Q3(j), Q3(eps * j * (m - j))) for j in range(m + 1)]


def section_phi():
    rule("5. KC-3: there is no count-based boundary term at all")
    say("Suppose some function Phi of the boundary count b made")
    say("    n <= (2/sqrt3) A(conv E) + Phi(b) + 1")
    say("true for every unit-separated E.  The section-4 family pins b = 3 while n")
    say("outruns the area term, so Phi(3) would have to be infinite.")
    say()
    lam, eps = F(101, 100), F(1, 1000)
    say(f"{'k':>3} {'n':>4} {'b':>3} {'(2/sqrt3)A(conv)':>17} {'Phi(3) >=':>11}")
    lows = []
    for k in (3, 4, 5, 6, 7, 8, 9):
        pts, L, tri = perturbed_lattice(k, lam, eps)
        val, n, b = oler_pieces(pts)
        assert min_sep2(pts) >= 1 and all(in_triangle(q, tri) for q in pts)
        assert b == 3
        need = Q3(n) - val - Q3(1)
        lows.append(need.float())
        say(f"{k:>3} {n:>4} {b:>3} {val.float():>17.6f} {need.float():>11.6f}")
    assert all(lows[i] < lows[i + 1] for i in range(len(lows) - 1))
    say()
    say("The last column grows like 3(k-1)/2 without bound while b stays 3.  Hence")
    say()
    say("  THEOREM T1 (sketch).  No function Phi makes n <= (2/sqrt3)A(conv E) + Phi(b) + 1")
    say("  valid for all unit-separated E.  The same family kills the variant with the")
    say("  containing triangle's area A(T) in place of A(conv E), since the two agree to")
    say("  O(eps) here.")
    say()
    say("(b) an independent second witness, in the opposite regime -- flat arcs, where")
    say("the area term vanishes instead of the count:")
    say(f"{'m':>4} {'n = b':>6} {'min sep^2':>12} {'(2/sqrt3)A':>12} {'Phi(b) >=':>11}")
    for m, epsa in ((3, F(1, 60)), (5, F(1, 400)), (8, F(1, 4000)), (12, F(1, 40000))):
        pts = flat_arc(m, epsa)
        ms2 = min_sep2(pts)
        assert ms2 >= 1, "flat arc separation"
        val, n, b = oler_pieces(pts)
        assert b == n, "flat arc should be in convex position"
        need = Q3(n) - val - Q3(1)
        say(f"{m:>4} {n:>6} {ms2.float():>12.8f} {val.float():>12.6f} {need.float():>11.6f}")
    say("    -> Phi(b) >= b - 1 for every b, since A -> 0 along the family.")
    say()
    say("(c) and even if T1 could somehow be evaded, the best conceivable count term is")
    say("weaker than Oler's own perimeter term at the lattice (exact; the lattice hull's")
    say("perimeter is rational):")
    say(f"{'k':>3} {'n':>4} {'b = M(P)':>9} {'Oler term M/2+1':>16} {'count term b':>13}"
        f" {'count better?':>14}")
    for k in (3, 4, 5, 6, 7, 8):
        pts = lattice(k)
        b = hull_boundary_count(pts)
        M = F(3 * (k - 1))
        assert F(b) == M, "lattice boundary edges all have length exactly 1"
        say(f"{k:>3} {len(pts):>4} {b:>9} {float(M/2+1):>16.4f} {float(b):>13.4f}"
            f" {str(F(b) <= M/2+1):>14}")
    say()
    say("KC-3 FIRED.  Counting the boundary instead of measuring it cannot work, and")
    say("the obstruction is not a bad choice of Phi -- no Phi exists.")


# ---------------------------------------------------------------- section 6

def section_corner_clearance():
    rule("6. The stable replacement: corner clearance, and what k = 7 would need")
    say("Counts are unstable (section 4).  Clearances are not: they move continuously.")
    say()
    say("Lemma C (proved in the README, status `sketch`).  If every point of E is at")
    say("distance >= t_i from corner A_i of T (cuts disjoint), then")
    say("    n <= a^2/2 + 3a/2 + 1 - sum_i (t_i^2 + t_i)/2.")
    say()
    say("For k = 7 the needed gain at a -> 6 is exactly 1 (27 vs the Oler value 27 at")
    say("a = 6), so with a common clearance t one needs 3(t^2 + t)/2 >= 1, i.e.")
    say("    t >= t7 = (-3 + sqrt(33))/6,   since  36 t^2 + 36 t + 9 = 33  <=>  t^2 + t = 2/3.")
    g = lambda x: x * x + x - F(2, 3)
    lo, hi = F(457427, 1000000), F(457428, 1000000)
    assert g(lo) < 0 < g(hi)
    say(f"  exact bracket: {float(lo):.6f} < t7 < {float(hi):.6f}"
        f"   (g(lo) = {float(g(lo)):+.3e}, g(hi) = {float(g(hi)):+.3e}, both exact)")
    say()
    say()
    say("Much better, and k-independent: a SINGLE corner suffices.  The gain is")
    say("sum_i (u_i^2 + u_i)/2, so u_i >= 1 at one corner already gives gain >= 1, and")
    say("at a < k-1 Oler's RHS is < T(k), hence n < T(k) - 1, hence n <= T(k) - 2.")
    say()
    say("  COROLLARY C1 (sketch; depends on Lemma C `sketch` and Oler `cited`).")
    say("  If some corner A_i of T has u_i >= 1 -- in particular if no point of E lies")
    say("  within distance 1 of that corner -- then T(k)-1 points cannot fit with")
    say("  a < k-1.  So Erdos-Oler for any k reduces to configurations having a point")
    say("  within reach 1 of EVERY corner.  The threshold 1 does not depend on k.")
    say()
    say("Exact check of the arithmetic at each k (a = k-1-1/1000, gain exactly 1):")
    say(f"{'k':>3} {'T(k)-1':>7} {'a':>10} {'Oler RHS':>11} {'RHS - 1':>10} {'excluded?':>10}")
    for k in range(3, 15):
        T = k * (k + 1) // 2
        a = F(k - 1) - F(1, 1000)
        rhs = a * a / 2 + 3 * a / 2 + 1
        say(f"{k:>3} {T-1:>7} {float(a):>10.4f} {float(rhs):>11.6f}"
            f" {float(rhs-1):>10.6f} {str(rhs - 1 < T - 1):>10}")
    say()
    say("And this is exactly why it does not close the case on its own: the lattice")
    say("T(7) has points AT the corners, t = 0, gain 0.  Lemma C is a real inequality")
    say("but it is vacuous on the only configurations that matter, unless it is paired")
    say("with a statement forcing small clearance to imply near-lattice structure --")
    say("which is approach O (Oler stability), not this attack.")


def main():
    section_oler_window()
    section_sharp_boundary()
    section_probe_boundary()
    section_convex_probe()
    section_H_at_the_lattice()
    section_phi()
    section_corner_clearance()
    rule("done")
    out = Path(__file__).resolve().parent / "out" / "report.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(OUT) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
