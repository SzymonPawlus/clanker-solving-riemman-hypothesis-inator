#!/usr/bin/env python3
"""
eo-epsilon: exact verification for the attack
`problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/`.

Every decision below is made over Q (fractions.Fraction) or over integers.
Square roots are never evaluated in floating point when a decision depends on
them: a comparison sqrt(r) >= c with r,c rational and c >= 0 is decided by
r >= c^2.  Floats appear only in the printed columns of tables, never in an
`assert` or an `if` that changes an outcome.

NORMALISATION (asserted in §0):
    separation 1, 27 points, closed equilateral triangle of side a, a < 6.
    slack(E) = (2/sqrt3) A(P) + M(P)/2 + 1 - n
    def(a,n) = (a^2+3a+2)/2 - n
    repo certificates use separation 2 and side d = 2a.

Stdlib only.  Reproduce with:  python3 verify.py > out/report.txt
"""

from fractions import Fraction as Q
import itertools, random, sys

random.seed(20260821)

OUT = []
def say(s=""):
    OUT.append(str(s))
    print(s)

def head(t):
    say(); say("=" * 78); say(t); say("=" * 78)

FAILURES = []
def check(name, cond):
    if not cond:
        FAILURES.append(name)
        say("  *** FAILED: %s" % name)
    return cond

# ---------------------------------------------------------------- rational sqrt
def isqrt_floor(n):
    return  __import__('math').isqrt(n)

def sqrt_bounds(r, denom=10**24):
    """Rational lo<=sqrt(r)<=hi with hi-lo <= 1/denom, r a nonnegative Fraction."""
    assert r >= 0
    # sqrt(r) = sqrt(p/q) = sqrt(p*q)/q
    p, q = r.numerator, r.denominator
    N = p * q * denom * denom
    s = isqrt_floor(N)
    lo = Q(s, q * denom)
    hi = Q(s + 1, q * denom)
    assert lo * lo <= r <= hi * hi, (r, lo, hi)
    return lo, hi

# =============================================================================
head("0. Normalisation, asserted")
# =============================================================================
n_target = 27
# a* is the root of (a^2+3a+2)/2 = 27  =>  a^2+3a-52 = 0  =>  a = (-3+sqrt(217))/2
# check: 217 = 9 + 4*52
check("a* discriminant 9+4*52 == 217", 9 + 4 * 52 == 217)
lo, hi = sqrt_bounds(Q(217))
a_star_lo, a_star_hi = (Q(-3) + lo) / 2, (Q(-3) + hi) / 2
say("  a*  in [%s, %s]  ~ %.12f" % (a_star_lo.limit_denominator(10**14),
                                    a_star_hi.limit_denominator(10**14), float(a_star_lo)))
check("a* in (5.86545993, 5.86545994)",
      a_star_lo > Q(586545993, 10**8) and a_star_hi < Q(586545994, 10**8))
check("a* is NOT an integer (5 < a* < 6)", a_star_hi < 6 and a_star_lo > 5)
# Oler value at a = 6 is exactly 28 = T(7)
check("Oler(6) == 28", (Q(6)**2 + 3*Q(6) + 2) / 2 == 28)
say("  Oler(a) := (a^2+3a+2)/2 ;  Oler(6) = 28 = T(7) ;  target n = 27, a < 6")
say("  separation-2 (certificate) form: d = 2a, s = d + 2*sqrt3.")
say("  at a = 6:  d = 12, s = 12 + 2*sqrt3 ~ %.6f" % (12 + 2*float(sqrt_bounds(Q(3))[0])))
say("  at a = a*: d = 2a* ~ %.9f" % (2*float(a_star_lo)))

# eps-scale:  def >= eps  <=>  a >= a_eps = (-3 + sqrt(217+8 eps))/2
say()
say("  eps-scale  a_eps = (-3+sqrt(217+8 eps))/2 :")
for e in [Q(0), Q(1,100), Q(1,10), Q(1,4), Q(1,2), Q(3,4), Q(1)]:
    l, h = sqrt_bounds(Q(217) + 8*e)
    say("    eps = %-6s  a_eps ~ %.9f" % (str(e), float((Q(-3)+l)/2)))
check("a_1 == 6 exactly (217+8 = 225 = 15^2)", 217 + 8 == 225 and isqrt_floor(225)**2 == 225)

# =============================================================================
head("1. Lemma T, re-derived and exactly checked  (K1)")
# =============================================================================
say("""  Claim (T1).  x,y,z >= 1 sides of a (possibly degenerate) triangle, S = x+y+z,
  alpha = y+z-x, beta = z+x-y, gamma = x+y-z  (all >= 0, alpha+beta+gamma = S).
  Heron: 16 A^2 = S*alpha*beta*gamma, hence

        tau := (2/sqrt3) A + S/2 - 2  =  sqrt(S*Q/12) + (S-4)/2,   Q := alpha*beta*gamma

  and tau >= 0 with equality exactly at (1,1,1) and the degenerate (2,1,1).

  Decision procedure used here, entirely over Q:
    S >= 4 : tau >= 0 always; tau = 0 iff S = 4 and Q = 0.
    S <  4 : tau >= 0  <=>  sqrt(S Q/12) >= (4-S)/2  <=>  S*Q >= 3*(4-S)^2.""")

def tau_state(x, y, z):
    """Return ('viol'|'eq'|'ok', S, Q) exactly."""
    S = x + y + z
    al, be, ga = y + z - x, z + x - y, x + y - z
    if min(al, be, ga) < 0:
        return None
    Qp = al * be * ga
    if S >= 4:
        return ("eq" if (S == 4 and Qp == 0) else "ok"), S, Qp
    lhs, rhs = S * Qp, 3 * (4 - S) ** 2
    if lhs < rhs:
        return "viol", S, Qp
    return ("eq" if lhs == rhs else "ok"), S, Qp

def scan(triples, label):
    nviol = neq = ntot = 0
    eqset = set()
    for (x, y, z) in triples:
        r = tau_state(x, y, z)
        if r is None:
            continue
        st, S, Qp = r
        ntot += 1
        if st == "viol":
            nviol += 1
            say("  VIOLATION at %s" % ((x, y, z),))
        elif st == "eq":
            neq += 1
            eqset.add(tuple(sorted((x, y, z))))
    say("  %-46s checked %7d  violations %d  equality %d  %s"
        % (label, ntot, nviol, neq, sorted(eqset) if len(eqset) <= 4 else "many"))
    check("no violation in " + label, nviol == 0)
    return eqset

allowed_eq = {(Q(1), Q(1), Q(1)), (Q(1), Q(1), Q(2))}

# grid
step = Q(1, 12)
g = [Q(1) + k * step for k in range(0, 37)]          # 1 .. 4
eq1 = scan(itertools.combinations_with_replacement(g, 3), "grid sides in [1,4] step 1/12")
# degenerate family x = y+z
deg = [(y + z, y, z) for y in [Q(1) + Q(k, 20) for k in range(61)]
                     for z in [Q(1) + Q(k, 20) for k in range(61)]]
eq2 = scan(deg, "degenerate x = y+z, y,z in [1,4] step 1/20")
# random rationals
rnd = []
for _ in range(200000):
    t = tuple(Q(random.randint(100, 700), 100) for _ in range(3))
    rnd.append(t)
eq3 = scan(rnd, "random rationals, sides in [1,7], seed 20260821")
# fine scans around the two equality points
fine = []
# sides must be >= 1: perturb (1,1,1) outward only, and (2,1,1) with its long side both ways
for da in range(0, 13):
    for db in range(0, 13):
        for dc in range(0, 13):
            fine.append((Q(1)+Q(da,1000), Q(1)+Q(db,1000), Q(1)+Q(dc,1000)))
for da in range(-12, 13):
    for db in range(0, 13):
        for dc in range(0, 13):
            fine.append((Q(2)+Q(da,1000), Q(1)+Q(db,1000), Q(1)+Q(dc,1000)))
eq4 = scan(fine, "fine perturbations at (1,1,1) and (2,1,1), sides >= 1")
# very large S
big = [(Q(a), Q(b), Q(c)) for a in range(1, 30) for b in range(1, 30) for c in range(1, 30)]
eq5 = scan(big, "integer sides 1..29")

eqall = eq1 | eq2 | eq3 | eq4 | eq5
say("  union of all equality triples found: %s" % sorted(eqall))
check("equality set is exactly {(1,1,1),(1,1,2)}", eqall == allowed_eq)

say()
say("""  Step 3 (the load-bearing step, flagged by its author).  Claim:
      min { alpha*beta*gamma : alpha+beta+gamma = S, 4-S <= alpha,beta,gamma <= S-2 }
      = m(S) := (S-2)^2 (4-S)     for S in [3,4].
  Re-derived here independently:
   (a) With gamma fixed, alpha*beta = alpha*(S-gamma-alpha) is a downward parabola in alpha,
       hence concave, hence minimised on any interval at an endpoint.  So a minimiser may be
       taken with alpha at a bound; repeating with beta leaves >= 2 coordinates at bounds, i.e.
       a vertex of the polytope.  (Concavity => endpoint minimum is exact, not heuristic.)
   (b) Vertex enumeration.  Two coordinates at bounds:
         both upper  (S-2,S-2)      -> third = 4-S,   feasible iff 4-S <= S-2 iff S >= 3.
         both lower  (4-S,4-S)      -> third = 3S-8,  feasible iff 3S-8 <= S-2 iff S <= 3.
         one of each (S-2,4-S)      -> third = S-2,   same orbit as the first.
       So for S in (3,4] the vertex set is exactly the permutations of (S-2,S-2,4-S),
       giving min = (S-2)^2 (4-S); at S=3 the polytope is the single point (1,1,1).
   (c) In side coordinates the minimiser (S-2,S-2,4-S) is the triple (1,1,S-2).""")

bad = 0
for k in range(0, 121):
    S = Q(3) + Q(k, 120)                      # S in [3,4]
    m = (S - 2) ** 2 * (4 - S)
    # exact grid over the polytope
    lo_c, hi_c = 4 - S, S - 2
    NN = 60
    best = None
    for i in range(NN + 1):
        al = lo_c + (hi_c - lo_c) * Q(i, NN)
        for j in range(NN + 1):
            be = lo_c + (hi_c - lo_c) * Q(j, NN)
            ga = S - al - be
            if ga < lo_c or ga > hi_c:
                continue
            v = al * be * ga
            if best is None or v < best:
                best = v
    if best is None:
        continue
    if best < m:
        bad += 1
        say("  Step-3 grid beats the claimed minimum at S = %s" % S)
    # and the claimed minimiser is feasible & attains m
    check("vertex feasible at S=%s" % S, lo_c <= 4 - S <= hi_c and lo_c <= S - 2 <= hi_c)
    check("vertex value == m(S) at S=%s" % S, (S-2)*(S-2)*(4-S) == m)
say("  exact grid over the polytope for 121 values of S in [3,4]: %d values where the"
    " grid minimum fell below m(S)  (expected 0)" % bad)
check("Step 3 minimum never beaten on the exact grid", bad == 0)

say()
say("""  Step 4 identity (checked exactly as a polynomial identity on 200 rational points):
      S(S-2)^2 + 3S - 12  ==  (S-3)(S^2-S+4),  and S^2-S+4 > 0 (discriminant -15).""")
bad4 = 0
for k in range(200):
    S = Q(random.randint(-500, 900), 100)
    if S * (S - 2) ** 2 + 3 * S - 12 != (S - 3) * (S * S - S + 4):
        bad4 += 1
check("Step-4 polynomial identity", bad4 == 0)
say("  mismatches: %d" % bad4)
say()
say("  VERDICT K1(a): Lemma T re-derived independently and survived every exact scan.")
say("  I can follow and reproduce Step 3; the concavity argument is correct and the vertex")
say("  enumeration is complete.  It remains `sketch` per RULES.md §3 (it is my own derivation).")

# =============================================================================
head("2. The tau-identity T2, re-derived and its counts exactly checked  (K1)")
# =============================================================================
say("""  Claim (T2).  For any triangulation of P = conv(E) with vertex set exactly E,
      slack(E) = sum_f tau(f) - sum_{e interior} (len(e) - 1).
  The proof is three counts plus two sums.  I re-derive:
      3F = 2|Edges| - b,  Euler V - |Edges| + (F+1) = 2
        => F = 2n - b - 2,  |Edges_int| = 3n - 2b - 3
      sum_f A_f = A(P),   sum_f p_f = M(P) + 2 L_int.
  Then sum_f tau(f) = (2/sqrt3)A + M/2 + L_int - 2F and subtracting slack leaves
      L_int - (3n-2b-3) = sum_{e int} (len(e) - 1).       [ algebra, exact ]
  Below the two combinatorial counts and the area sum are verified exactly on explicit
  triangulations.  Points are exact in Z[1/2] x Z[1/2]*sqrt3, so (2/sqrt3)*A_f is RATIONAL
  and every area comparison is exact.""")

def tri_lattice(L):
    """Points of the side-L unit triangular lattice as (p,q) meaning (p, q*sqrt3)."""
    pts = {}
    for j in range(L + 1):
        for i in range(L - j + 1):
            pts[(i, j)] = (Q(i) + Q(j, 2), Q(j, 2))
    up = [((i, j), (i + 1, j), (i, j + 1)) for j in range(L) for i in range(L - j)]
    dn = [((i + 1, j), (i, j + 1), (i + 1, j + 1)) for j in range(L - 1) for i in range(L - j - 1)]
    return pts, up + dn

def two_area_over_sqrt3(P0, P1, P2):
    """(2/sqrt3)*Area of the triangle, exactly rational, for points (p,q)~(p,q*sqrt3)."""
    (x0, y0), (x1, y1), (x2, y2) = P0, P1, P2
    # cross = (x1-x0)*sqrt3*(y2-y0) - sqrt3*(y1-y0)*(x2-x0) = sqrt3 * r
    r = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
    if r < 0:
        r = -r
    # Area = sqrt3*r/2  =>  (2/sqrt3)*Area = r
    return r

def d2(P0, P1):
    (x0, y0), (x1, y1) = P0, P1
    return (x1 - x0) ** 2 + 3 * (y1 - y0) ** 2

def analyse(name, pts, faces, expected_n=None, expected_b=None):
    keys = sorted(pts)
    n = len(keys)
    F = len(faces)
    edge_count = {}
    for f in faces:
        for e in [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]:
            k = tuple(sorted(e))
            edge_count[k] = edge_count.get(k, 0) + 1
    interior = [e for e, c in edge_count.items() if c == 2]
    boundary = [e for e, c in edge_count.items() if c == 1]
    check(name + ": every edge in 1 or 2 faces", all(c in (1, 2) for c in edge_count.values()))
    b = len(boundary)                     # boundary edges = boundary points of E
    ok1 = (F == 2 * n - b - 2)
    ok2 = (len(interior) == 3 * n - 2 * b - 3)
    A_over = sum(two_area_over_sqrt3(pts[f[0]], pts[f[1]], pts[f[2]]) for f in faces)
    # perimeter and L_int with rigorous rational enclosures
    def L(edges):
        lo = hi = Q(0)
        for (u, v) in edges:
            l_, h_ = sqrt_bounds(d2(pts[u], pts[v]))
            lo += l_; hi += h_
        return lo, hi
    Mlo, Mhi = L(boundary)
    Ilo, Ihi = L(interior)
    slack_lo = A_over + Mlo / 2 + 1 - n
    slack_hi = A_over + Mhi / 2 + 1 - n
    # RHS of T2
    tlo = thi = Q(0)
    for f in faces:
        ar = two_area_over_sqrt3(pts[f[0]], pts[f[1]], pts[f[2]])
        plo = phi = Q(0)
        for e in [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]:
            l_, h_ = sqrt_bounds(d2(pts[e[0]], pts[e[1]]))
            plo += l_; phi += h_
        tlo += ar + plo / 2 - 2
        thi += ar + phi / 2 - 2
    rhs_lo = tlo - (Ihi - len(interior))
    rhs_hi = thi - (Ilo - len(interior))
    same = (slack_lo <= rhs_hi) and (rhs_lo <= slack_hi)
    say("  %-28s n=%3d b=%3d F=%3d  F=2n-b-2:%s  |Eint|=3n-2b-3:%s  T2:%s  slack~%.12f"
        % (name, n, b, F, "OK" if ok1 else "NO", "OK" if ok2 else "NO",
           "OK" if same else "NO", float(slack_lo)))
    check(name + ": F = 2n-b-2", ok1)
    check(name + ": |E_int| = 3n-2b-3", ok2)
    check(name + ": T2 both sides agree", same)
    if expected_n is not None: check(name + ": n", n == expected_n)
    if expected_b is not None: check(name + ": b", b == expected_b)
    return slack_lo, slack_hi

for L in range(1, 7):
    pts, faces = tri_lattice(L)
    s = analyse("T(%d) lattice (side %d)" % (L + 1, L), pts, faces,
                expected_n=(L + 1) * (L + 2) // 2, expected_b=3 * L)
    check("T(%d) lattice slack == 0" % (L + 1), s[0] <= 0 <= s[1])

# T(7)-lattice minus its apex: n = 27, the configuration that matters
pts, faces = tri_lattice(6)
apex = (0, 6)
faces27 = [f for f in faces if apex not in f]
pts27 = {k: v for k, v in pts.items() if k != apex}
s = analyse("T(7) lattice minus apex", pts27, faces27, expected_n=27, expected_b=17)
check("T(7)-minus-apex slack == 0", s[0] <= 0 <= s[1])
say("  ^ n = 27 with slack exactly 0 -- but its hull needs side 6, not a < 6.")

# a lattice-convex set with a sqrt3 hull edge (the K3 witness of eo-oler-equality §3)
# hull = triangle (0,0),(2,0),(1/2, sqrt3/2): hull edges 1,1,sqrt3,1 with b = 4
P = {0: (Q(0), Q(0)), 1: (Q(1), Q(0)), 2: (Q(2), Q(0)), 3: (Q(1, 2), Q(1, 2))}
s = analyse("lattice hull with a sqrt3 edge", P, [(0, 1, 3), (1, 2, 3)])
lo3, hi3 = sqrt_bounds(Q(3))
check("sqrt3-edge slack == (sqrt3-1)/2",
      s[0] <= (hi3 - 1) / 2 and (lo3 - 1) / 2 <= s[1])
say("  ^ slack = (sqrt3-1)/2 = %.9f  (lattice-convex but NOT Oler-extremal)" % float((lo3-1)/2))

# a generic (non-lattice) 4-point set, rational coordinates in the plane (q = 0 component)
G = {0: (Q(0), Q(0)), 1: (Q(13, 10), Q(0)), 2: (Q(3, 2), Q(1, 2)), 3: (Q(1, 5), Q(2, 3))}
analyse("generic 4-point set", G, [(0, 1, 2), (0, 2, 3)])

say()
say("  VERDICT K1(b): T2's Euler counts, area sum and both sides of the identity check out")
say("  on every configuration tested.  T2 is re-derived, and stays `sketch` (my derivation).")

# =============================================================================
head("3. Quantitative Lemma T -- statement, proof, and adversarial exact scan  (K2)")
# =============================================================================
say("""  THEOREM Q (quantitative Lemma T).  Let x,y,z >= 1 be the sides of a (possibly degenerate)
  triangle, S = x+y+z, alpha = y+z-x etc., Q = alpha*beta*gamma, m(S) = (S-2)^2 (4-S).

    (i)  If S >= 4:      tau = (2/sqrt3)A + (S-4)/2   exactly, so  tau >= (S-4)/2  and
                         tau >= sqrt(S*Q/12).
    (ii) If 3 <= S <= 4:
                 tau >= [ S*Q - 3(4-S)^2 ] / 12
                      = [ S*(Q - m(S)) + (4-S)(S-3)(S^2-S+4) ] / 12
                      >= (S/12)*(Q - m(S)) + (5/6)(S-3)(4-S).

  PROOF of (ii).  Write N = S*Q/12 - (4-S)^2/4 and D = sqrt(S*Q/12) + (4-S)/2, so tau = N/D
  (rationalising tau = sqrt(S Q/12) - (4-S)/2; D > 0 unless S=4 and Q=0, where tau = 0 = N).
  N >= 0 is Lemma T.  For fixed perimeter S the area is maximal for the equilateral triangle,
  so (2/sqrt3)A <= S^2/18, hence D <= S^2/18 + (4-S)/2, which on [3,4] is decreasing in S
  (derivative S/9 - 1/2 < 0 there) and therefore <= 1 at S = 3.  With 0 <= N and 0 < D <= 1,
  tau = N/D >= N.  The second line is the identity
      S*m(S) - 3(4-S)^2 = (4-S)(S-3)(S^2-S+4)
  (both sides expand to (4-S)(S^3-4S^2+7S-12)); the third uses S >= 3 and S^2-S+4 >= 10 on
  [3,4].  Both summands are >= 0 and vanish simultaneously exactly at S = 3 (giving (1,1,1))
  and at S = 4 with Q = 0 (giving (2,1,1)).                                             []

  Decision procedure for the scan, entirely over Q:  tau >= B  <=>  sqrt(S Q/12) >= B+(4-S)/2,
  and when the right side is >= 0 this is  S*Q/12 >= (B+(4-S)/2)^2.""")

def qbound(S, Qp):
    """The claimed lower bound B on tau."""
    if S >= 4:
        return (S - 4) / 2
    return (S * Qp - 3 * (4 - S) ** 2) / 12

def qbound_coarse(S, Qp):
    if S >= 4:
        return (S - 4) / 2
    return (S * (Qp - (S - 2) ** 2 * (4 - S))) / 12 + Q(5, 6) * (S - 3) * (4 - S)

def tau_ge(S, Qp, B):
    """Exact decision of tau >= B."""
    # tau = sqrt(S*Qp/12) + (S-4)/2 ;  tau >= B  <=>  sqrt(S*Qp/12) >= B - (S-4)/2
    R = B - (S - 4) / 2
    if R <= 0:
        return True
    return S * Qp / 12 >= R * R

def qscan(triples, label):
    nt = nv = nv2 = 0
    worst = None
    for (x, y, z) in triples:
        S = x + y + z
        al, be, ga = y + z - x, z + x - y, x + y - z
        if min(al, be, ga) < 0:
            continue
        Qp = al * be * ga
        nt += 1
        B = qbound(S, Qp)
        if not tau_ge(S, Qp, B):
            nv += 1
            if nv <= 3:
                say("  *** Theorem Q (fine) violated at %s" % ((x, y, z),))
        B2 = qbound_coarse(S, Qp)
        if not tau_ge(S, Qp, B2):
            nv2 += 1
            if nv2 <= 3:
                say("  *** Theorem Q (coarse) violated at %s" % ((x, y, z),))
        if B < 0:
            say("  *** bound went negative at %s" % ((x, y, z),))
    say("  %-46s checked %7d  fine-violations %d  coarse-violations %d" % (label, nt, nv, nv2))
    check("Theorem Q fine on " + label, nv == 0)
    check("Theorem Q coarse on " + label, nv2 == 0)

qscan(itertools.combinations_with_replacement(g, 3), "grid sides in [1,4] step 1/12")
qscan(deg, "degenerate x = y+z (slivers, sides >= 1)")
qscan(rnd, "random rationals sides in [1,7]")
qscan(fine, "fine perturbations at (1,1,1) and (2,1,1), sides >= 1")
qscan(big, "integer sides 1..29 (large S)")
# adversarial: thin slivers with one very long side
sliv = []
for k in range(40, 440):                          # t >= 1, sides all >= 1
    t = Q(k, 40)
    for eps in [Q(0), Q(-1, 10**6), Q(-1, 10**3), Q(-1, 50)]:
        sliv.append((1 + t + eps, Q(1), t))       # near-degenerate, one long side
qscan(sliv, "near-degenerate slivers, long side up to 12")
# adversarial: isoceles (1,1,t), t in [1,2] -- the segment joining the two equality shapes
say()
say("  the segment (1,1,t) joining the two equality shapes:  tau vs bound")
say("    t        tau (exact-bracketed)   B(fine)      B(coarse)   ratio B/tau")
for t in [Q(1), Q(11,10), Q(5,4), Q(3,2), Q(7,4), Q(19,10), Q(199,100), Q(2)]:
    x, y, z = Q(1), Q(1), t
    S = x + y + z
    al, be, ga = y+z-x, z+x-y, x+y-z
    Qp = al*be*ga
    l_, h_ = sqrt_bounds(S*Qp/12)
    tau_lo = l_ + (S-4)/2
    B, B2 = qbound(S, Qp), qbound_coarse(S, Qp)
    say("    %-8s %.12f          %.9f  %.9f  %s"
        % (t, float(tau_lo), float(B), float(B2),
           ("%.3f" % (float(B)/float(tau_lo))) if tau_lo > 0 else "-"))
    check("Q fine at (1,1,%s)" % t, tau_ge(S, Qp, B))
say("  bound vanishes exactly at t=1 and t=2 (the two equality shapes) and nowhere between.")

# =============================================================================
head("4. Groemer 1960 == Oler 1961  (settles the open question of eo-literature §3)")
# =============================================================================
say("""  Groemer's Satz (as transcribed on the problem README from p.285 of the GDZ scan, `cited`):
  for n unit circles packed in a convex region of area F and perimeter U,
      n*sqrt(12) <= F - kappa*U + lambda,   kappa = (2-sqrt3)/2,  lambda = sqrt12 - pi(sqrt3-1),
  with equality iff the region is the convex hull of the circles AND the hull H of the centres
  decomposes into equilateral triangles of side 2 whose vertices are all centres (or H
  degenerates to a segment or a point).

  Apply it to the region K = H (+) B_1 (Minkowski sum), which IS the convex hull of the circles.
  Steiner:  F = A(H) + M(H) + pi,   U = M(H) + 2pi.  Substituting must give exactly Oler.
  Verified below symbolically over the basis {1, sqrt3, pi, pi*sqrt3} with rational coefficients
  and the single relation sqrt3*sqrt3 = 3 (A(H), M(H) carried as two further formal symbols).""")

# symbolic: elements are dicts monomial->Fraction, monomial = (e3, epi, eA, eM)
# e3 in {0,1} (power of sqrt3, reduced), epi >= 0, eA, eM in {0,1}
def sym(c=Q(0), **kw):
    d = {}
    if c: d[(0, 0, 0, 0)] = Q(c)
    return d
def mono(e3, epi, eA, eM, c=Q(1)):
    return {(e3, epi, eA, eM): Q(c)}
def sadd(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, Q(0)) + v
        if r[k] == 0: del r[k]
    return r
def sscale(a, c):
    return {k: v * Q(c) for k, v in a.items() if v * Q(c) != 0}
def smul(a, b):
    r = {}
    for (e3, ep, eA, eM), va in a.items():
        for (f3, fp, fA, fM), vb in b.items():
            n3, coef = e3 + f3, va * vb
            if n3 >= 2:
                n3 -= 2; coef *= 3
            k = (n3, ep + fp, eA + fA, eM + fM)
            r[k] = r.get(k, Q(0)) + coef
            if r[k] == 0: del r[k]
    return r

ONE   = mono(0, 0, 0, 0)
S3    = mono(1, 0, 0, 0)                 # sqrt3
PI    = mono(0, 1, 0, 0)
A_H   = mono(0, 0, 1, 0)
M_H   = mono(0, 0, 0, 1)
kappa = sscale(sadd(sscale(ONE, 2), sscale(S3, -1)), Q(1, 2))          # (2-sqrt3)/2
sqrt12 = sscale(S3, 2)                                                  # 2 sqrt3
lam   = sadd(sqrt12, sscale(smul(PI, sadd(S3, sscale(ONE, -1))), -1))   # sqrt12 - pi(sqrt3-1)
F_    = sadd(sadd(A_H, M_H), PI)
U_    = sadd(M_H, sscale(PI, 2))
rhs   = sadd(sadd(F_, sscale(smul(kappa, U_), -1)), lam)
target = sadd(sadd(A_H, sscale(M_H, Q(1, 2)) if False else smul(sscale(S3, Q(1,2)), M_H)), sqrt12)
say("  F - kappa U + lambda  =  %s" % sorted(rhs.items()))
say("  A(H) + (sqrt3/2) M(H) + sqrt12 = %s" % sorted(target.items()))
check("Groemer reduces to  n sqrt12 <= A + (sqrt3/2) M + sqrt12", rhs == target)
say("""  So Groemer's inequality on the hull of the circles is
      n*sqrt12 <= A(H) + (sqrt3/2) M(H) + sqrt12
      <=>  n <= A(H)/(2 sqrt3) + M(H)/4 + 1          [ separation 2 ]
      <=>  n <= (2/sqrt3) A + M/2 + 1                [ separation 1: A -> A/4, M -> M/2 ]
  which is EXACTLY Oler's inequality.""")
# verify the rescaling numerically-exactly on the T(k) lattices at separation 2
say("  rescaling check on T(k) lattices (separation 2, side 2(k-1)):")
for L in range(1, 7):
    n = (L + 1) * (L + 2) // 2
    # separation-2 lattice: A = sqrt3/4 (2L)^2, M = 3*2L
    # A/(2 sqrt3) = sqrt3 (2L)^2 / (4*2 sqrt3) = (2L)^2/8 = L^2/2 ; M/4 = 6L/4 = 3L/2
    val = Q(L * L, 2) + Q(3 * L, 2) + 1
    check("Groemer form gives T(%d) exactly at side 2L" % (L + 1), val == n)
    say("    L=%d  n=%3d  A/(2sqrt3)+M/4+1 = %s" % (L, n, val))

# =============================================================================
head("5. Theorem E -- the deficit is strictly positive at every non-triangular n")
# =============================================================================
say("""  THEOREM E.  Let n >= 1 and let E be a set of n points with pairwise distances >= 1 contained
  in the closed equilateral triangle T(a) of side a.  If def(a,n) = (a^2+3a+2)/2 - n = 0, then
      a is a positive INTEGER, E = Lambda cap T(a) for a unit triangular lattice, and
      n = (a+1)(a+2)/2 is a triangular number.
  Consequently, for every non-triangular n the minimum side d(n) satisfies d(n) > a*_n, the
  root of Oler(a) = n, i.e. eps_n := def(d(n), n) > 0 STRICTLY.

  PROOF.  Oler on P = conv(E) gives n <= (2/sqrt3)A(P) + M(P)/2 + 1, and monotonicity of area
  and of perimeter under inclusion of convex sets gives (2/sqrt3)A(P)+M(P)/2 <= (2/sqrt3)A(T)
  + M(T)/2 = (a^2+3a)/2.  def = G + slack with G = Phi(T)-Phi(P) >= 0 and slack >= 0, so
  def = 0 forces both to vanish.  G = 0 forces A(P) = A(T); a closed convex P strictly inside T
  would leave an open set of positive area, so P = T(a).  In particular P is non-degenerate,
  which already rules out Groemer's degenerate alternative (a segment or a point has area 0 and
  so has G > 0).  slack = 0 is then Groemer's equality case (§4): conv(E) is tiled by unit
  equilateral triangles with all vertices in E.  A triangle tiled by unit lattice triangles has
  each side a union of unit lattice edges, so a is a positive integer and E is the full lattice
  triangle, n = (a+1)(a+2)/2.
  For the consequence: d(n) is attained (T(a) decreasing in a, the configuration space compact,
  and pairwise distance >= 1 is a closed condition), so if d(n) = a*_n then the minimiser has
  def = 0, forcing n triangular.                                                          []

  DEPENDENCIES:  Oler (`cited`), Groemer's equality clause (`cited`, but see the caveat: this
  repo has read p.285 of the scan, which is the statement page, and not the proof), area and
  perimeter monotonicity for nested convex bodies (standard, `cited`).""")

say()
say("  n = T(k)-1:  a*_k is the root of a^2+3a+4-k(k+1) = 0, i.e. a = (-3+sqrt(4k^2+4k-7))/2.")
say("  Lemma:  4k^2+4k-7 is never a perfect square for k >= 1, so a*_k is never an integer.")
say("  Proof:  (2a+3)^2 = (2k+1)^2 - 8 forces (2k+1-2a-3)(2k+1+2a+3) = 8 with both factors")
say("          even, i.e. (k-a-1)(k+a+2) = 2, forcing k=1, a=-1; so no k >= 2 works.")
sq = 0
for k in range(2, 200001):
    v = 4 * k * k + 4 * k - 7
    if v >= 0 and isqrt_floor(v) ** 2 == v:
        sq += 1
        say("  *** 4k^2+4k-7 is a square at k = %d" % k)
check("4k^2+4k-7 never a perfect square for 2 <= k <= 200000", sq == 0)
say("  checked k = 2..200000: %d perfect squares found (expected 0);"
      " k=1 gives 1 = 1^2 but a = -1 < 0, excluded by the proof" % sq)
say()
say("  k    n=T(k)-1   a*_k                 Oler window        status of eps_k")
for k in range(2, 11):
    n = k * (k + 1) // 2 - 1
    disc = 4 * k * k + 4 * k - 7
    l, h = sqrt_bounds(Q(disc))
    astar = (Q(-3) + l) / 2
    known = "proved (E-O known)" if k <= 6 else "OPEN"
    say("    %-3d  %-9d %.12f       [a*, %d)        eps_%d > 0 by Theorem E; %s"
        % (k, n, float(astar), k - 1, k, known))
check("k=7 gives n=27 and disc 217", 7 * 8 // 2 - 1 == 27 and 4 * 49 + 28 - 7 == 217)

say()
say("""  WHAT THEOREM E DOES AND DOES NOT GIVE.
  It gives eps_7 > 0, hence d(27) > a* = 5.86545993...  This is strictly more than the repo has
  (everything sits at d(27) >= a*).  It gives NO explicit value: the final step is a compactness
  argument by contradiction, and no modulus is extracted.  On the eps-scale of
  `eo-oler-equality` §5 this is exactly the 0+ that the brief classifies as insufficient.
  EXPLICIT eps proved here: 0.""")

# =============================================================================
head("6. Proposition V -- step (1) of the programme is vacuous  (K3)")
# =============================================================================
say("""  PROPOSITION V.  Let Psi be ANY function of a triangle's side lengths with 0 <= Psi(f) <=
  tau(f) for every triangle with sides >= 1 (i.e. any correct quantitative Lemma T, however
  sharp -- including Psi = tau itself).  Feeding it into T2 gives, for every configuration E
  and every triangulation,
        slack(E) = sum_f tau(f) - sum_{e int}(len(e)-1) >= sum_f Psi(f) - sum_{e int}(len(e)-1).
  To conclude slack(E) >= eps > 0 for all 27-point configurations in T(a), a < 6, one must
  therefore prove
        sum_f Psi(f) - sum_{e int}(len(e)-1)  >=  eps                          (*)
  and the strongest instance of (*), Psi = tau, is LITERALLY the target statement
  slack(E) >= eps, because T2 is an identity.  Hence:

    (V1) no quantitative Lemma T, of any sharpness, is a strengthening of anything: the
         inequality it produces is weaker than or equal to the target it is meant to prove;
    (V2) all of the content must come from an independent upper bound on
         sum_{e int}(len(e)-1), and any such bound strong enough for (*) with Psi = tau is
         equivalent to the target;
    (V3) the per-face version -- distribute the interior-edge debt evenly, i.e. ask
         sigma(f) := tau(f) - (1/2) sum_{e in f, interior}(len(e)-1) >= 0 -- is exactly the
         REFUTED face-excess hypothesis, since for a face with all three edges interior
         sigma(f) = (2/sqrt3)A_f - 1/2, which is negative for every face of area < sqrt3/4.

  (V3) is checked exactly below, and the redistribution identity slack = sum_f sigma(f) with
        sigma(f) = (2/sqrt3)A_f - (1+j_f)/2 + (1/2) sum_{e in f on bdry} len(e)
  (j_f = number of boundary edges of f) is verified on the same configurations as §2.""")

say()
say("  sigma(f) for faces with all three edges interior, i.e. (2/sqrt3)A_f - 1/2 :")
for (x, y, z, note) in [(Q(1), Q(1), Q(1), "unit equilateral (the extremal face)"),
                        (Q(1), Q(1), Q(19,10), "near-degenerate (2,1,1)"),
                        (Q(1), Q(1), Q(3,2), "isoceles t=3/2"),
                        (Q(2), Q(2), Q(2), "side-2 equilateral")]:
    S = x + y + z
    Qp = (y+z-x)*(z+x-y)*(x+y-z)
    l_, h_ = sqrt_bounds(S*Qp/12)
    say("    (%-5s%-5s%-5s) (2/sqrt3)A = %.9f   sigma = %.9f   %s"
        % (x, y, z, float(l_), float(l_ - Q(1,2)), note))
check("sigma < 0 for the near-degenerate face",
      sqrt_bounds((Q(39,10))*((Q(1)+Q(19,10)-Q(1))*(Q(19,10)+Q(1)-Q(1))*(Q(1)+Q(1)-Q(19,10)))/12)[1]
      < Q(1, 2))
say("  => sigma(f) >= 0 is FALSE, confirming the repo's refutation of face-excess nonnegativity")
say("     (oler-slack-analysis §4, eo-boundary-counting §4 -- credited, not reclaimed).")

# verify the sigma redistribution identity exactly on the lattice configurations
say()
say("  redistribution identity  slack = sum_f sigma(f)  (exact where all lengths are 1):")
for L in [2, 3, 4, 5, 6]:
    pts, faces = tri_lattice(L)
    keys = list(pts)
    ec = {}
    for f in faces:
        for e in [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]:
            k = tuple(sorted(e)); ec[k] = ec.get(k, 0) + 1
    bnd = {e for e, c in ec.items() if c == 1}
    tot = Q(0)
    for f in faces:
        ar = two_area_over_sqrt3(pts[f[0]], pts[f[1]], pts[f[2]])
        es = [tuple(sorted(e)) for e in [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]]
        j = sum(1 for e in es if e in bnd)
        blen = Q(0)
        for e in es:
            if e in bnd:
                dd = d2(pts[e[0]], pts[e[1]])
                assert dd == 1, dd            # all lattice boundary edges are unit
                blen += 1
        tot += ar - Q(1 + j, 2) + blen / 2
    check("sigma-sum == 0 for T(%d) lattice" % (L + 1), tot == 0)
    say("    T(%d) lattice: sum_f sigma(f) = %s (slack = 0)" % (L + 1, tot))

say()
say("""  VERDICT K3: FIRED.  Step (1) of the brief's programme cannot by itself produce eps > 0,
  and no sharpening of Lemma T changes that, because T2 is an identity and the strongest
  admissible Psi returns the target unchanged.  Reported explicit eps from this route: 0.""")

# =============================================================================
head("7. Summary")
# =============================================================================
say("  explicit eps proved:              0")
say("  non-explicit eps (Theorem E):     > 0   (d(27) > a*, no modulus)")
say("  Theorem Q (quantitative Lemma T): proved, survived every adversarial exact scan")
say("  Proposition V:                    step (1) of the programme is vacuous")
say("  Groemer == Oler:                  verified symbolically; settles eo-literature §3")
say()
if FAILURES:
    say("  FAILED CHECKS (%d): %s" % (len(FAILURES), FAILURES[:20]))
else:
    say("  ALL EXACT CHECKS PASSED")
