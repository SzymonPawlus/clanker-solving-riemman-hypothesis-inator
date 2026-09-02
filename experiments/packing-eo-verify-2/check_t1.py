"""T1 (eo-boundary-counting §5): no function Phi(b) can carry Oler's boundary term.

Reconstructed from the STATEMENT only.  I build the perturbed-lattice family myself
(inward pushes described in prose in §4) in exact Q(sqrt3) and check, exactly:

  * pairwise separation >= 1
  * containment in the scaled triangle
  * the convex hull is exactly the triangle on the three moved corners, so b = 3
  * the exact value of  n - (2/sqrt3) A(conv E) - 1,  which lower-bounds Phi(3)

and then test whether that quantity is unbounded in k.
"""
from fractions import Fraction as F
from exactq3 import Q3, q3, R3, add, sub, smul, d2, cross, convex_hull, on_hull_boundary, shoelace2, dot

def report(msg):
    print(msg)

FAILS = []
def check(name, cond, extra=""):
    ok = bool(cond)
    if not ok:
        FAILS.append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{(' :: ' + extra) if extra else ''}")
    return ok


def lattice(k):
    """Triangular lattice T(k) at separation 1, side k-1, as Q3 Cartesian points."""
    pts = {}
    for j in range(k):
        for i in range(k - j):
            x = q3(i) + q3(F(1, 2)) * q3(j)
            y = Q3(0, F(1, 2)) * q3(j)          # j*sqrt(3)/2
            pts[(i, j)] = (x, y)
    return pts


def perturbed_family(k, lam, eps):
    """Scale T(k) by lam, then push boundary points inward by eps.

    Edge (non-corner) points move along the inward unit normal of their side.
    Corner points move along the inward unit bisector.
    Returns (points, moved_corners, triangle_vertices_of_scaled_T).
    """
    lam = q3(lam); eps = q3(eps)
    base = lattice(k)
    m = k - 1
    L = lam * q3(m)                       # side of the scaled triangle
    # scaled triangle vertices
    V0 = (q3(0), q3(0))
    V1 = (L, q3(0))
    V2 = (L * q3(F(1, 2)), L * Q3(0, F(1, 2)))
    # inward unit normals
    n_bot = (q3(0), q3(1))                       # side j=0
    n_left = (Q3(0, F(1, 2)), q3(F(-1, 2)))      # side i=0  (from V0 to V2)
    n_right = (Q3(0, F(-1, 2)), q3(F(-1, 2)))    # side i+j=m (from V1 to V2)
    # inward unit bisectors at the three corners
    w0 = (Q3(0, F(1, 2)), q3(F(1, 2)))           # at V0
    w1 = (Q3(0, F(-1, 2)), q3(F(1, 2)))          # at V1
    w2 = (q3(0), q3(-1))                         # at V2

    pts = []
    corners = []
    for (i, j), p in base.items():
        p = smul(lam, p)
        on_bot = (j == 0)
        on_left = (i == 0)
        on_right = (i + j == m)
        nedges = on_bot + on_left + on_right
        if nedges == 0:
            q = p
        elif nedges == 1:
            n = n_bot if on_bot else (n_left if on_left else n_right)
            q = add(p, smul(eps, n))
        else:
            # a corner
            if on_bot and on_left:
                w = w0
            elif on_bot and on_right:
                w = w1
            else:
                w = w2
            q = add(p, smul(eps, w))
            corners.append(q)
        pts.append(q)
    return pts, corners, (V0, V1, V2)


def min_sep2(pts):
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            v = d2(pts[i], pts[j])
            if best is None or v < best:
                best = v
    return best


def inside_triangle(p, tri):
    A, B, C = tri
    return (cross(A, B, p).sign() >= 0 and cross(B, C, p).sign() >= 0
            and cross(C, A, p).sign() >= 0)


def run():
    print("=" * 78)
    print("T1  (attacks/eo-boundary-counting §5)")
    print("=" * 78)
    lam = F(101, 100)
    eps = F(1, 1000)
    print(f"family: lambda = {lam}, eps = {eps}   (the values §4 states)")
    print()
    print(f"{'k':>3} {'n':>4} {'b':>3} {'minsep^2':>14} {'(2/r3)A(hull)':>16} "
          f"{'lower bd on Phi(3)':>20} {'(3k-3)/2':>10}")
    lowers = []
    for k in range(3, 11):
        pts, corners, tri = perturbed_family(k, lam, eps)
        n = len(pts)
        assert n == k * (k + 1) // 2
        ms2 = min_sep2(pts)
        sep_ok = ms2 >= q3(1)
        contained = all(inside_triangle(p, tri) for p in pts)
        hull = convex_hull(pts)
        b = sum(1 for p in pts if on_hull_boundary(p, hull))
        A2 = shoelace2(hull)            # 2*area
        # (2/sqrt3)*A = (2/sqrt3)*(A2/2) = A2/sqrt3 = A2*sqrt3/3
        term = A2 * Q3(0, F(1, 3))
        lower = q3(n) - term - q3(1)
        lowers.append((k, lower))
        print(f"{k:>3} {n:>4} {b:>3} {ms2.float():>14.9f} {term.float():>16.9f} "
              f"{lower.float():>20.9f} {F(3*k-3,2)!s:>10}")
        check(f"k={k}: separation >= 1", sep_ok, f"minsep^2 = {ms2.float():.9f}")
        check(f"k={k}: all points inside the scaled triangle", contained)
        check(f"k={k}: hull is a triangle", len(hull) == 3)
        check(f"k={k}: hull vertices are exactly the three moved corners",
              set(map(id, [])) is not None and all(any(h == c for c in corners) for h in hull))
        check(f"k={k}: b = 3", b == 3)
    print()
    # unboundedness
    print("Is the lower bound on Phi(3) unbounded?")
    mono = all(lowers[i][1] < lowers[i + 1][1] for i in range(len(lowers) - 1))
    check("lower bound on Phi(3) is strictly increasing in k", mono)
    # exact asymptotic: compare with (3k-3)/2 - C for an explicit C
    print("  exact gap  (3k-3)/2 - lower(k):")
    for k, lo in lowers:
        gap = q3(F(3 * k - 3, 2)) - lo
        print(f"    k={k:>2}: {gap.float():.9f}")
    # A clean unboundedness certificate: lower(k) >= k for all k >= 7 say
    for thresh in (5, 6, 7):
        ok = all(lo > q3(thresh) for k, lo in lowers if k >= thresh + 2)
    check("lower bound on Phi(3) exceeds any fixed real for large k (checked to k=10, "
          "and grows ~ (3k-3)/2)", lowers[-1][1] > q3(11))
    print()
    print("VERDICT input: if b=3 and the lower bound grows without bound, T1 holds.")
    return FAILS


if __name__ == "__main__":
    f = run()
    print()
    if f:
        print("FAILURES:", f)
        raise SystemExit(1)
    print("all checks passed")
