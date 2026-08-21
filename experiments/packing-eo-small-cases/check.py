#!/usr/bin/env python3
"""
Exact checks for attacks/eo-small-cases.

Everything decided here is decided in exact arithmetic over Q(sqrt 3)
(and Q(sqrt 33) where the n=8 optimum is needed).  No floats decide anything;
floats appear only in the printed transcript, after the exact decision.

Normalisation: SEPARATION 1.  Points lie in the closed equilateral triangle
T_a with A=(0,0), B=(a,0), C=(a/2, a*sqrt3/2), pairwise distances >= 1.
(The certificates in problems/.../results use separation 2 and side 2a.)

Run:  python3 check.py
"""

from fractions import Fraction as F
from itertools import combinations

# ---------------------------------------------------------------- Q(sqrt d)
class Q:
    """u + v*sqrt(d), u,v rational, d a fixed squarefree positive integer."""
    __slots__ = ("u", "v", "d")

    def __init__(self, u=0, v=0, d=3):
        self.u = F(u); self.v = F(v); self.d = d

    def _co(self, o):
        if isinstance(o, Q):
            if self.d != o.d and self.v != 0 and o.v != 0:
                raise ValueError("mixed radicands")
            return o if o.v != 0 else Q(o.u, 0, self.d)
        return Q(o, 0, self.d)

    def __add__(self, o):
        o = self._co(o); return Q(self.u + o.u, self.v + o.v, self.d)
    __radd__ = __add__

    def __neg__(self):
        return Q(-self.u, -self.v, self.d)

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) + (-self)

    def __mul__(self, o):
        o = self._co(o)
        return Q(self.u * o.u + self.d * self.v * o.v,
                 self.u * o.v + o.u * self.v, self.d)
    __rmul__ = __mul__

    def sign(self):
        """Exact sign of u + v*sqrt(d)."""
        u, v, d = self.u, self.v, self.d
        if v == 0:
            return (u > 0) - (u < 0)
        if u == 0:
            return (v > 0) - (v < 0)
        if u > 0 and v > 0:
            return 1
        if u < 0 and v < 0:
            return -1
        # opposite signs: compare u^2 with d*v^2
        c = (u * u) - d * (v * v)          # >0 <=> |u| > sqrt(d)|v|
        s = 1 if u > 0 else -1             # sign of the dominant term if |u| wins
        if c == 0:
            return 0
        return s if c > 0 else -s

    def __ge__(self, o): return (self - self._co(o)).sign() >= 0
    def __gt__(self, o): return (self - self._co(o)).sign() > 0
    def __le__(self, o): return (self - self._co(o)).sign() <= 0
    def __lt__(self, o): return (self - self._co(o)).sign() < 0
    def __eq__(self, o): return (self - self._co(o)).sign() == 0

    def approx(self):
        import math
        return float(self.u) + float(self.v) * math.sqrt(self.d)

    def __repr__(self):
        return f"{self.u}+{self.v}v{self.d}"


def R3(u=0, v=0): return Q(u, v, 3)      # u + v*sqrt3

SQ3 = R3(0, 1)


# ------------------------------------------------------------- geometry
def d2(p, q):
    dx = p[0] - q[0]; dy = p[1] - q[1]
    return dx * dx + dy * dy


def separated(pts):
    """All pairwise squared distances >= 1, exactly."""
    return all(d2(p, q) >= 1 for p, q in combinations(pts, 2))


def in_triangle(p, a):
    """Closed T_a with A=(0,0), B=(a,0), C=(a/2, a*sqrt3/2).
    Half-planes: y>=0 ; y <= sqrt3 * x ; y <= sqrt3 * (a - x)."""
    x, y = p
    return (y >= 0) and (SQ3 * x - y >= 0) and (SQ3 * (R3(a) - x) - y >= 0)


def in_row_strip(p, a, j, rows=3):
    """Closed horizontal strip j (1-based, from the bottom) of the `rows`-fold
    row decomposition of T_a: y in [(j-1)*H/rows, j*H/rows], H = a*sqrt3/2."""
    x, y = p
    lo = SQ3 * R3(F(a) * F(j - 1, 2 * rows))
    hi = SQ3 * R3(F(a) * F(j, 2 * rows))
    return in_triangle(p, a) and (y - lo >= 0) and (hi - y >= 0)


def tri(k): return k * (k + 1) // 2


FAIL = []
def check(name, cond, note=""):
    ok = bool(cond)
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


# ============================================================== section 1
print("\n=== 1. Subdivision lemma: arithmetic of  m^2  vs  Delta(m+1)-2 ===")
print("  Lemma: a < m  =>  n <= m^2   (m^2 cells of side a/m < 1, diam < 1).")
print("  EO for k needs  n <= Delta(k)-2  at  a < k-1,  i.e. m = k-1.")
print(f"  {'k':>3} {'m=k-1':>6} {'m^2':>5} {'Delta(k)-2':>11} {'deficit':>8} {'(k-2)(k-3)/2':>13}")
for k in range(2, 11):
    m = k - 1
    need = tri(k) - 2
    defic = m * m - need
    closed = (k - 2) * (k - 3) // 2
    check(f"k={k}: deficit formula", defic == closed,
          f"m^2={m*m:3d}  need<={need:3d}  deficit={defic:3d}")
print("  => m^2 <= Delta(k)-2  iff  (k-2)(k-3) <= 0  iff  k <= 3.")
check("subdivision suffices exactly for k<=3",
      all((( k-1)**2 <= tri(k)-2) == (k <= 3) for k in range(2, 30)))

print("\n  Bonus: the same lemma re-proves Oler's triangular case when")
print("  Delta(k) > (k-1)^2, i.e. n=Delta(k) cannot fit at a<k-1:")
for k in range(2, 8):
    print(f"    k={k}: Delta(k)={tri(k):3d}  (k-1)^2={(k-1)**2:3d}  "
          f"{'PROVES a_Delta(k) >= k-1' if tri(k) > (k-1)**2 else 'no'}")
check("lemma re-proves triangular case exactly for k<=4",
      all((tri(k) > (k-1)**2) == (k <= 4) for k in range(2, 30)))


# ============================================================== section 2
print("\n=== 2. k=3 (n=5, a<2): the bound is attained at a=2 ===")
# T(3) lattice minus apex, side 2, separation exactly 1.
half = R3(F(1, 2))
h1 = R3(0, F(1, 2))          # sqrt3/2
five = [(R3(0), R3(0)), (R3(1), R3(0)), (R3(2), R3(0)),
        (half, h1), (R3(F(3, 2)), h1)]
check("5 points, pairwise dist >= 1", separated(five))
check("5 points inside T_2", all(in_triangle(p, 2) for p in five))
mind2 = min(d2(p, q) for p, q in combinations(five, 2))
check("min squared distance is exactly 1", mind2 == 1,
      f"min d^2 = {mind2.approx()}")
six = five + [(R3(1), SQ3)]
check("adding the apex gives 6 points still separated in T_2", separated(six)
      and all(in_triangle(p, 2) for p in six))
print("  => a_5 = a_6 = 2 : EO holds for k=3, and the lemma (m=2) is the proof.")


# ============================================================== section 3
print("\n=== 3. k=4: every decomposition tried is at capacity 9, not 8 ===")
print("  Working at a = 27/10 = 2.7 < 3, h = a/3 = 9/10 < 1.")
a = F(27, 10)
h = F(9, 10)

# --- 3a. bottom row (row 1 of 3) really does hold 5 -----------------------
ytop = SQ3 * R3(F(9, 20))          # = (sqrt3/2)*h , top of row 1
bottom5 = [(R3(0), R3(0)), (R3(F(27, 20)), R3(0)), (R3(F(27, 10)), R3(0)),
           (R3(F(7, 10)), ytop), (R3(2), ytop)]
check("bottom row: 5 points pairwise >= 1", separated(bottom5))
check("bottom row: all 5 lie in row-strip 1 of T_a",
      all(in_row_strip(p, a, 1) for p in bottom5))
print("     pairwise squared distances:",
      sorted(round(d2(p, q).approx(), 6) for p, q in combinations(bottom5, 2))[:4], "...")

# --- 3b. middle row really does hold 3 ------------------------------------
ymid_lo = ytop
ymid_hi = SQ3 * R3(F(9, 10))
mid3 = [(R3(F(9, 20)), ymid_lo), (R3(F(45, 20)), ymid_lo), (R3(F(27, 20)), ymid_hi)]
check("middle row: 3 points pairwise >= 1", separated(mid3))
check("bottom-row minimum squared distance is exactly 412/400",
      min(d2(p, q) for p, q in combinations(bottom5, 2)) == R3(F(412, 400)))
check("middle-row minimum squared distance is exactly 567/400",
      min(d2(p, q) for p, q in combinations(mid3, 2)) == R3(F(567, 400)))
check("closest bottom/middle cross pair is exactly 1/16",
      min(d2(p, q) for p in bottom5 for q in mid3) == R3(F(1, 16)))
check("middle row: all 3 lie in row-strip 2 of T_a",
      all(in_row_strip(p, a, 2) for p in mid3))

# --- 3c. top row holds 1 (its cell has diameter h < 1) --------------------
check("top row cell has diameter h = 9/10 < 1", h < 1)

# --- 3d. the three row witnesses are NOT jointly realisable ---------------
bad = [(p, q) for p in bottom5 for q in mid3 if d2(p, q) < 1]
check("bottom-row and middle-row witnesses collide (interaction is real)",
      len(bad) > 0,
      f"{len(bad)} cross pairs below separation 1, smallest d^2 = "
      f"{min(d2(p,q).approx() for p,q in bad):.6f}")

print("\n  Capacity of each decomposition of T_a, a<3  (h = a/3 < 1):")
print("    3-row decomposition            : 5 + 3 + 1                    = 9")
print("    row1 + top sub-triangle 2h<2   : 5 + 4   (4 by the k=3 lemma) = 9")
print("    rows 1-2 + top cell            : 8 + 1                        = 9")
print("    uniform 9-cell subdivision     : 1 x 9                        = 9")
print("  EO for k=4 needs total capacity <= 8.  Each summand above is attained")
print("  (rows 1 and 2 by the exact witnesses just checked), so no decomposition")
print("  of this kind can reach 8: the missing point is an interaction term.")


# ============================================================== section 4
print("\n=== 4. What Oler alone gives, and the size of the residual gap ===")
print("  Oler (cited, attacks/oler-lower-bound): n <= a^2/2 + 3a/2 + 1,")
print("  i.e.  a >= (sqrt(8n+1) - 3)/2.")
print(f"  {'k':>3} {'n=D(k)-1':>9} {'Oler a >=':>12} {'target k-1':>11} {'a-gap':>9} {'pt-gap':>7}")
for k in range(3, 9):
    n = tri(k) - 1
    # exact: compare (sqrt(8n+1)-3)/2 with k-1  <=>  8n+1 vs (2k+1)^2
    disc = 8 * n + 1
    import math
    olb = (math.sqrt(disc) - 3) / 2
    # point-count gap at a = k-1 exactly:
    #   Oler RHS at a=k-1 is (k-1)^2/2 + 3(k-1)/2 + 1 = Delta(k)
    rhs = F((k - 1) ** 2, 2) + F(3 * (k - 1), 2) + 1
    check(f"k={k}: Oler RHS at a=k-1 equals Delta(k) exactly", rhs == tri(k),
          f"n={n:3d}  Oler a>={olb:.6f}  target={k-1}  a-gap={k-1-olb:.6f}  "
          f"pt-gap={tri(k)-1-(tri(k)-2)}")
print("  The a-gap shrinks like 2/(2k+1) (0.228 at k=4, 0.135 at k=7),")
print("  but the POINT gap is exactly 1 for every k: Oler permits Delta(k)-1")
print("  points as a -> (k-1)^-, and EO needs Delta(k)-2.  The required gain is")
print("  scale-free.  Any mechanism whose yield grows or shrinks with k is the")
print("  wrong shape for this problem.")


# ============================================================== section 5
print("\n=== 5. Why the dissection route needs an OPTIMAL covering ===")
print("  If T_a is covered by N sets of diameter < 1 then n <= N.")
print("  Conversely N >= n*(a) := max # points in T_a at pairwise distance > 1,")
print("  and n*(a) = max{ n : a_n < a }.")
# cited a_n values (separation 1) for n <= 8, all from the proven table
sqrt33_over_3 = Q(0, F(1, 3), 33)
a_vals = {1: R3(0), 2: R3(1), 3: R3(1), 4: SQ3, 5: R3(2), 6: R3(2),
          7: R3(1, 1), 8: Q(1, F(1, 3), 33)}
for k, target in ((3, 2), (4, 3)):
    ns = [n for n in sorted(a_vals) if a_vals[n] < target]
    nstar = max(ns)
    check(f"k={k}: n*(a->({target})^-) = Delta(k)-2",
          nstar == tri(k) - 2,
          f"n* = {nstar}, Delta({k})-2 = {tri(k)-2}, "
          f"a_{nstar} = {a_vals[nstar].approx():.6f} < {target}")
print("  So the number of diameter-<1 pieces the method needs is EXACTLY the")
print("  minimum possible: the dissection must be an optimal covering.")
print("  k=3 (m=2): 4 pieces needed, the trivial subdivision gives 4  -> works.")
print("  k=4 (m=3): 8 pieces needed, every construction tried gives 9 -> stalls.")
print("  k=7 (m=6): 26 pieces needed, uniform subdivision gives 36.")


# ============================================================== section 6
print("\n=== 6. The best covering construction I found also gives 9, not 8 ===")
print("  Scaled to side 3 (a cover of T_3 by sets of diameter <= 1 rescales to")
print("  a cover of T_a, a<3, by sets of diameter <= a/3 < 1).")
print("  Take the 6 maximal diameter-1 sets that cover the boundary:")
print("    3 corner sectors  S_V = {P : |P-V| <= 1}  (a 60-degree sector of")
print("      radius 1 has diameter exactly 1, and is the LARGEST diameter-1")
print("      set containing the corner V);")
print("    3 edge-middle Reuleaux triangles, one per edge, on the middle unit")
print("      segment of that edge and the centroid.")
V = {"A": (R3(0), R3(0)), "B": (R3(3), R3(0)), "C": (R3(F(3,2)), R3(0, F(3,2)))}
G = (R3(F(3,2)), R3(0, F(1,2)))                       # centroid of T_3
REU = [
    [(R3(1), R3(0)), (R3(2), R3(0)), G],                                  # bottom
    [(R3(F(1,2)), R3(0, F(1,2))), (R3(1), SQ3), G],                       # left
    [(R3(F(5,2)), R3(0, F(1,2))), (R3(2), SQ3), G],                       # right
]
def covered(P):
    if any(d2(P, v) <= 1 for v in V.values()):
        return True
    return any(all(d2(P, w) <= 1 for w in R) for R in REU)

check("each corner sector has diameter exactly 1 (extreme chord)",
      d2((R3(1), R3(0)), (R3(F(1,2)), R3(0, F(1,2)))) == 1)
for name, R in zip(("bottom", "left", "right"), REU):
    ok = all(d2(p, q) == 1 for p, q in combinations(R, 2))
    check(f"{name} Reuleaux triangle is built on a unit equilateral triangle", ok)

rho = R3(F(3,2)) - R3(0, F(1,2))          # 3/2 - sqrt3/2
gaps = [(R3(F(3,2)), R3(F(3,2))),
        (R3(F(9,4)) - R3(0, F(3,4)), R3(0, F(3,4)) - R3(F(3,4))),
        (R3(F(3,4)) + R3(0, F(3,4)), R3(0, F(3,4)) - R3(F(3,4)))]
for i, P in enumerate(gaps):
    check(f"gap point {i+1} lies in T_3", in_triangle(P, 3))
    check(f"gap point {i+1} is NOT covered by the 6 sets", not covered(P),
          f"P = ({P[0].approx():.6f}, {P[1].approx():.6f})")
gd = [d2(p, q) for p, q in combinations(gaps, 2)]
check("the 3 gap points are pairwise at distance > 1", all(g > 1 for g in gd),
      f"squared distances {[round(g.approx(), 6) for g in gd]}")
check("that squared distance is exactly 9 - 9*sqrt3/2",
      all(g == R3(9, F(-9, 2)) for g in gd))
print("  => within the regime where each edge is met by exactly 3 pieces (which")
print("     forces every boundary piece into one of these 6 maximal sets), a")
print("     cover needs >= 6 + 3 = 9 pieces.  Outside that regime I have no")
print("     bound, so this is NOT a proof that 8 pieces are impossible -- only")
print("     that the natural construction lands on 9, like every other one.")


# ============================================================== summary
print("\n=== summary ===")
if FAIL:
    print(f"  {len(FAIL)} CHECK(S) FAILED: {FAIL}")
    raise SystemExit(1)
print("  all checks passed")
