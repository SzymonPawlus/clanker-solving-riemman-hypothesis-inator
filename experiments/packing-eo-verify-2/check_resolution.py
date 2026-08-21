"""The 'resolution theorem', attacks/eo-exhaustion §5 -- checked from the statement.

Claim (§5).  If every cell of a surviving node is at level L, side h = d/2^L < 2 (so
multiplicities are 1 and there are exactly n cells) and the node survives the pairwise
test, then T(d) contains n points at pairwise distance >= 2 - 2h/sqrt3, hence
    d >= d(n) (1 - h/sqrt3).

Stated contrapositive (§5).  "a cell exhaustion can only close at ratio rho = d/d(n)
once h < sqrt3 (1 - rho), i.e. at level 2^L > d / (sqrt3 (1-rho))."

Two separate questions, kept apart:
  (A) is the CLAIM true?
  (B) is the stated contrapositive the contrapositive?

Everything below is exact.  Cells live in the lattice basis u=(1,0), v=(1/2,sqrt3/2);
in that basis the squared distance between (p1,q1) and (p2,q2) is
    dp^2 + dp*dq + dq^2,
which is rational whenever the coordinates are, so no sqrt3 is ever needed.
"""
from fractions import Fraction as F
from itertools import combinations
import sys

def sq(dp, dq):
    return dp * dp + dp * dq + dq * dq


def cells(level, d):
    """Level-`level` subdivision of the equilateral triangle with corners
    0, d*u, d*v.  Returns list of cells; each cell is a 3-tuple of (p,q) vertices."""
    N = 2 ** level
    h = F(d) / N
    out = []
    for i in range(N):
        for j in range(N - i):
            # upward cell
            out.append(((i * h, j * h), ((i + 1) * h, j * h), (i * h, (j + 1) * h)))
            if i + j <= N - 2:
                out.append((((i + 1) * h, j * h), (i * h, (j + 1) * h),
                            ((i + 1) * h, (j + 1) * h)))
    return out


def maxsep2(c1, c2):
    """Squared max distance between two convex cells = max over vertex pairs."""
    best = F(0)
    for a in c1:
        for b in c2:
            v = sq(a[0] - b[0], a[1] - b[1])
            if v > best:
                best = v
    return best


def centroid(c):
    return (sum(v[0] for v in c) / 3, sum(v[1] for v in c) / 3)


# ----------------------------------------------------------------------------
# (A) the claim itself, tested exactly on every pair of cells at several levels
# ----------------------------------------------------------------------------
def test_claim_geometry():
    print("=" * 78)
    print("(A) the geometric core:  maxsep(c_i,c_j) <= |g_i - g_j| + 2h/sqrt3")
    print("    equivalently  (maxsep - |g_i-g_j|)^2 <= 4h^2/3   [both sides rational]")
    print("=" * 78)
    bad = 0
    tested = 0
    for level in (1, 2, 3):
        for d in (F(4), F(3998, 1000), F(12), F(59, 10)):
            cs = cells(level, d)
            h = d / 2 ** level
            R2 = h * h / 3                      # circumradius^2 of a side-h equilateral cell
            for c1, c2 in combinations(cs, 2):
                g1, g2 = centroid(c1), centroid(c2)
                gd2 = sq(g1[0] - g2[0], g1[1] - g2[1])
                ms2 = maxsep2(c1, c2)
                # want sqrt(ms2) <= sqrt(gd2) + 2 sqrt(R2).  Square carefully:
                # equivalent to ms2 - gd2 - 4R2 <= 4 sqrt(gd2 R2), and LHS may be negative.
                lhs = ms2 - gd2 - 4 * R2
                tested += 1
                if lhs <= 0:
                    continue
                if lhs * lhs > 16 * gd2 * R2:
                    bad += 1
    print(f"  pairs tested (exact): {tested}   violations: {bad}")
    print(f"  [{'PASS' if bad == 0 else 'FAIL'}] the circumradius bound holds on every pair")
    return bad == 0


# ----------------------------------------------------------------------------
# (B) an independent uniform-level cell exhaustion
# ----------------------------------------------------------------------------
def close_at_level(n, d, level, node_budget=4_000_000, verbose=False):
    """Does the uniform level-`level` cell method close (prove n points impossible)?

    Rules, both derived from the problem statement only:
      * side h = d/2^level < 2  =>  each closed cell has diameter h < 2  =>  <=1 point
      * two occupied cells must admit points at distance >= 2, i.e. maxsep >= 2
    So the node set is exactly the set of n-cliques in the graph
      V = cells,  E = {(i,j) : maxsep2(i,j) >= 4}.
    Returns (closed, reason).
    """
    cs = cells(level, d)
    h = F(d) / 2 ** level
    if h >= 2:
        return (None, f"h = {float(h):.4f} >= 2, multiplicities not 1")
    m = len(cs)
    if m < n:
        return (True, f"pigeonhole: {m} cells < {n} points")
    adj = [set() for _ in range(m)]
    for i, j in combinations(range(m), 2):
        if maxsep2(cs[i], cs[j]) >= 4:
            adj[i].add(j)
            adj[j].add(i)
    # max clique via greedy-colouring-bounded branch and bound, looking only for size n
    order = sorted(range(m), key=lambda v: -len(adj[v]))
    best = [0]
    nodes = [0]
    found = [False]

    def expand(R, P):
        if found[0]:
            return
        nodes[0] += 1
        if nodes[0] > node_budget:
            raise RuntimeError("node budget exceeded")
        if len(R) == n:
            found[0] = True
            return
        if len(R) + len(P) < n:
            return
        Pl = sorted(P, key=lambda v: -len(adj[v] & P))
        for idx, v in enumerate(Pl):
            if len(R) + len(P) < n:
                return
            expand(R + [v], P & adj[v])
            P = P - {v}
            if found[0]:
                return

    try:
        expand([], set(range(m)))
    except RuntimeError as e:
        return (None, f"budget exceeded after {nodes[0]} nodes")
    return (not found[0], f"{m} cells, {nodes[0]} search nodes, "
            f"{'no' if not found[0] else 'a'} valid {n}-cell node")


def threshold_level(n, d, dn):
    """The level §5 says is 'needed': 2^L > d / (sqrt3 (1-rho)), rho = d/d(n)."""
    import math
    rho = float(d) / float(dn)
    thr = float(d) / (math.sqrt(3) * (1 - rho))
    L = 0
    while 2 ** L <= thr:
        L += 1
    return L, thr, rho


def test_contrapositive():
    print()
    print("=" * 78)
    print("(B) is  'can only close once h < sqrt3 (1-rho)'  the contrapositive?")
    print("=" * 78)
    print("  claim:      node survives  =>  d >= d(n)(1 - h/sqrt3)  =>  h >= sqrt3(1-rho)")
    print("  contrapos.: h < sqrt3(1-rho)  =>  NO node survives  =>  the search CLOSES")
    print("  §5 asserts: the search closes  =>  h < sqrt3(1-rho)      <-- that is the CONVERSE")
    print()
    print("  A single instance where the search closes with h WELL ABOVE the threshold")
    print("  refutes the asserted direction.  d(n) values below are the repo's `cited` table.")
    print()
    rows = [
        # n, d, d(n) cited, description
        (5,  F(3998, 1000), 4,  "k=3 EO case; d(5)=4 from s(5)=4+2sqrt3"),
        (5,  F(39998, 10000), 4, "k=3 EO case, even closer to 4"),
        (6,  F(3998, 1000), 4,  "n=6=T(3); d(6)=4 from s(6)=4+2sqrt3"),
        (9,  F(59, 10),     6,  "k=4 EO case; d(9)=6 from s(9)=6+2sqrt3"),
    ]
    print(f"{'n':>3} {'d':>10} {'rho':>9} {'L needed per §5':>16} {'cells 4^L':>12} "
          f"{'L that actually closes':>24}")
    verdicts = []
    for n, d, dn, desc in rows:
        L5, thr, rho = threshold_level(n, d, dn)
        closing = None
        for L in range(1, 5):
            h = F(d) / 2 ** L
            if h >= 2:
                continue
            res, why = close_at_level(n, d, L)
            if res:
                closing = (L, why)
                break
        cl = f"L={closing[0]}" if closing else "not found at L<=4"
        print(f"{n:>3} {float(d):>10.5f} {rho:>9.6f} {L5:>16} {4**L5:>12} {cl:>24}")
        if closing:
            print(f"      -> {desc}")
            print(f"         {closing[1]}")
            print(f"         h at that level = {float(F(d)/2**closing[0]):.6f}, "
                  f"threshold sqrt3(1-rho) = {3**0.5*(1-rho):.8f}")
            verdicts.append(closing[0] < L5)
    print()
    if all(verdicts) and verdicts:
        print("  [REFUTED] every instance closes at a level FAR COARSER than the level §5")
        print("            says is needed.  'can only close once h < sqrt3(1-rho)' is FALSE.")
    return verdicts


if __name__ == "__main__":
    a = test_claim_geometry()
    v = test_contrapositive()
    print()
    print("=" * 78)
    print("summary")
    print("=" * 78)
    print(f"  claim (A) geometric core: {'CONFIRMED' if a else 'BROKEN'}")
    print(f"  stated contrapositive (B): {'REFUTED' if all(v) and v else 'inconclusive'}")
