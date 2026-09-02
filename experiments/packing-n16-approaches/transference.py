#!/usr/bin/env python3
"""Kill-experiments for transference proposals (worker I1, issue #97).

Question: can a lower bound for a_16 (triangle side, separation 1) be transferred
from a container we understand better -- the square, the disk, or "no container at
all" (the diameter / distance-matrix relaxation)?

Each transference has a hard algebraic CEILING: the best bound it could ever
prove, even given a *perfect* (currently unavailable) lower-bound theorem for the
other container.  This script computes exact rational bounds on each ceiling and
compares them against
  - Oler (cited):        a_16 >= (-3+sqrt(129))/2 = 4.17890835...
  - repo record (sketch): a_16 >= 1+2*sqrt(3)      = 4.46410161...

If the ceiling is below Oler, the transference is dead on arrival -- it cannot
even reproduce the classical bound.  All decisions are exact (Fraction + integer
square roots); floats appear only in printed columns.

Witnesses used (all are explicit separated point sets, verified here exactly):
  W1: 19 points of the unit triangular lattice with i^2+ij+j^2 <= 4  (disk kill)
  W2: 4x4 unit grid in a side-3 square                               (square kill)
  W3: best 16-subset of W1 minimizing diameter                       (diameter kill)

No value of a_16 / d(16) / s(16) and no property of any 16-point packing is an
input anywhere in this file.
"""
from fractions import Fraction
from itertools import combinations
import math

# ---------- exact sqrt enclosures ----------------------------------------------

def sqrt_bounds(x: Fraction, prec: int = 60) -> tuple[Fraction, Fraction]:
    """Return exact rationals lo < sqrt(x) < hi (or == if x is a perfect square)."""
    assert x >= 0
    scale = 10 ** prec
    n = x.numerator * scale * scale
    d = x.denominator
    # integer sqrt of n//d and (n//d)+1
    q = n // d
    r = math.isqrt(q)
    lo = Fraction(r, scale)
    hi = Fraction(r + 1, scale)
    assert lo * lo <= x <= hi * hi
    return lo, hi

OLER_LO, OLER_HI = sqrt_bounds(Fraction(129))
oler_lo = (Fraction(-3) + OLER_LO) / 2          # < true Oler bound
oler_hi = (Fraction(-3) + OLER_HI) / 2          # > true Oler bound
S3_LO, S3_HI = sqrt_bounds(Fraction(3))
record_lo = 1 + 2 * S3_LO                        # < 1+2*sqrt(3)

print("Oler bound  (-3+sqrt129)/2 in [%.12f, %.12f]" % (oler_lo, oler_hi))
print("repo record 1+2sqrt3       >= %.12f" % record_lo)
print()

# ---------- lattice helpers (oblique integer coordinates) -----------------------

def norm2(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv          # exact squared Euclidean distance

def check_separated(pts, min2=1):
    m = min(norm2(p, q) for p, q in combinations(pts, 2))
    assert m >= min2, f"witness not separated: min^2 = {m}"
    return m

def diameter2(pts):
    return max(norm2(p, q) for p, q in combinations(pts, 2))

# ---------- W1: 19 lattice points in the disk of radius 2 -----------------------

W1 = [(i, j) for i in range(-4, 5) for j in range(-4, 5) if i * i + i * j + j * j <= 4]
assert len(W1) == 19
check_separated(W1)
maxr2 = max(i * i + i * j + j * j for i, j in W1)
assert maxr2 == 4
print("[W1] 19 unit-separated points, all within Euclid distance 2 of origin  (exact)")

# Disk transference ceiling:
#   T_a is contained in its circumscribed disk of radius a/sqrt(3).
#   The transferred bound is  a >= sqrt(3) * R(16), R(16) = min radius holding 16
#   separated points.  16 <= 19 and W1 shows R(19) <= 2, so R(16) <= 2 and the
#   ceiling is  sqrt(3)*2 = 2*sqrt(3) = 3.4641...
disk_ceiling_hi = 2 * S3_HI
print("    disk-transference ceiling <= 2*sqrt(3) <= %.12f" % disk_ceiling_hi)
assert disk_ceiling_hi < oler_lo
print("    DEAD: ceiling < Oler  (exact comparison)")
print()

# ---------- W2: 4x4 grid --> square transference ---------------------------------

# 16 points of the integer grid {0..3}^2 are unit-separated in a side-3 square.
grid = [(x, y) for x in range(4) for y in range(4)]
mg = min((a - c) ** 2 + (b - d) ** 2 for (a, b), (c, d) in combinations(grid, 2))
assert mg >= 1
print("[W2] 4x4 grid: 16 unit-separated points in a side-3 square  (exact)")
# Smallest enclosing square of T_a has side kappa*a with kappa = (sqrt6+sqrt2)/4
# (equivalently the largest equilateral triangle in a unit square has side
#  sqrt6-sqrt2; the two constants are reciprocal because (sqrt6-sqrt2)(sqrt6+sqrt2)=4).
# Transferred bound: kappa*a >= L(16)  =>  a >= L(16)/kappa = L(16)*(sqrt6-sqrt2)/4*...
# ceiling = L16 / kappa  with L16 <= 3   =>  ceiling <= 3*(sqrt6-sqrt2)... careful:
# 1/kappa = 4/(sqrt6+sqrt2) = sqrt6-sqrt2.  So ceiling <= 3*(sqrt6-sqrt2)/1? No:
# 1/kappa = 4/(sqrt6+sqrt2) = (sqrt6-sqrt2).  ceiling <= L16 * (sqrt6-sqrt2) / ...
# dimensional check: kappa ~ 0.9659, L16 <= 3 => ceiling <= 3/0.9659 = 3.106.
S6_LO, S6_HI = sqrt_bounds(Fraction(6))
S2_LO, S2_HI = sqrt_bounds(Fraction(2))
inv_kappa_hi = S6_HI - S2_LO     # > sqrt6 - sqrt2 = 1/kappa
square_ceiling_hi = 3 * inv_kappa_hi
print("    square-transference ceiling <= 3*(sqrt6-sqrt2) <= %.12f" % square_ceiling_hi)
assert square_ceiling_hi < oler_lo
print("    DEAD: ceiling < Oler  (exact comparison)")
print()

# ---------- W3: diameter relaxation (distance-matrix / CNSD-rank route) ----------

# A relaxation that keeps only the pairwise distances (e.g. the conditionally-
# negative-semidefinite rank-4 formulation) sees the container only through
# diameter(T_a) = a.  Its ceiling is delta(16) = min diameter of a 16-point
# unit-separated planar set.  Upper-bound delta(16) by the best 16-subset of W1.
best = None
shell2 = [p for p in W1 if p[0] ** 2 + p[0] * p[1] + p[1] ** 2 == 4]
core = [p for p in W1 if p not in shell2]
assert len(core) == 13 and len(shell2) == 6
for drop in combinations(shell2, 3):          # keep 3 of the 6 outer points
    pts = core + [p for p in shell2 if p not in drop]
    assert len(pts) == 16
    d2 = diameter2(pts)
    if best is None or d2 < best[0]:
        best = (d2, pts)
d2, pts = best
check_separated(pts)
dia_lo, dia_hi = sqrt_bounds(Fraction(d2))
print("[W3] best 16-subset of W1: diameter^2 = %s, diameter <= %.12f" % (d2, dia_hi))
print("    => delta(16) <= %.12f  (diameter-relaxation ceiling)" % dia_hi)
assert dia_hi < oler_lo
print("    DEAD: ceiling < Oler  (exact comparison)")
print()

# ---------- second-moment (Lasserre level-1) value, for the record ---------------

# sum_{i<j} |pi-pj|^2 = n * sum_i |pi - centroid|^2  >= C(16,2)*1 = 120
# and sum_i |pi-c|^2 <= n * (a/sqrt3)^2, so a^2 >= 120*3/16^2 = 45/32... wait:
#   120 <= 16 * (a^2/3) * ... : sum_i |pi-c|^2 <= 16 * R^2 = 16 a^2/3
#   => 120 <= 16 a^2 /3 * ... times n? identity: sum_pairs = n * sum_i |pi-c|^2.
#   120 <= 16 * 16 * a^2 / 3?  No: sum_pairs = n*sum_i|pi-c|^2 <= 16 * 16 a^2/3.
# Keep it honest and loose (an upper bound on what level-1 can give):
#   a^2 >= 120*3/(16*16) = 45/64  =>  a >= 0.8385   (even weaker forms exist;
#   the point is the ORDER OF MAGNITUDE: level-1 moment information is hopeless).
lvl1 = sqrt_bounds(Fraction(45, 64))[1]
print("[level-1 moment bound] a >= sqrt(45/64) ~ %.4f  -- vs Oler 4.179: hopeless." % lvl1)
print()
print("All three transference ceilings are below Oler; the proposals are refuted")
print("as record routes.  (Ceilings, not current technology: even a PERFECT")
print("lower-bound oracle for the other container cannot push them past Oler.)")
