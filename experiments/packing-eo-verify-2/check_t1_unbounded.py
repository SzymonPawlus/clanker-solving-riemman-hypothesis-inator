"""Does the eo-boundary-counting §4 family, AS PARAMETERISED, actually make Phi(3) unbounded?

T1's proof says: "Apply the §4 family.  It has b = 3 for every k, its hull is a triangle
of side -> k-1".   The §4 family is fixed at lambda = 101/100, eps = 1/1000.
With lambda fixed > 1 the hull side is lambda*(k-1) - sqrt3*eps, which is NOT -> k-1:
the multiplicative 1% error is squared and eventually swamps the (3k-3)/2 gain.

Here the closed form is derived and checked against the exact geometric computation,
then evaluated far enough out to settle the question.
"""
from fractions import Fraction as F
from exactq3 import Q3, q3, shoelace2, convex_hull, on_hull_boundary, d2
from check_t1 import perturbed_family, min_sep2, inside_triangle

def closed_form_lower(k, lam, eps):
    """n - (2/sqrt3) A(hull) - 1 where hull is equilateral of side lam*(k-1) - sqrt3*eps."""
    side = q3(lam) * q3(k - 1) - Q3(0, 1) * q3(eps)
    # (2/sqrt3) * (sqrt3/4) side^2 = side^2 / 2
    return q3(F(k * k + k, 2)) - side * side * q3(F(1, 2)) - q3(1)

print("=" * 78)
print("Step 1: verify the closed form against the exact geometry (k = 3..10)")
print("=" * 78)
lam, eps = F(101, 100), F(1, 1000)
ok = True
for k in range(3, 11):
    pts, corners, tri = perturbed_family(k, lam, eps)
    hull = convex_hull(pts)
    A2 = shoelace2(hull)
    geo = q3(len(pts)) - A2 * Q3(0, F(1, 3)) - q3(1)
    cf = closed_form_lower(k, lam, eps)
    same = (geo == cf)
    ok &= same
    print(f"  k={k:>2}  geometric {geo.float():.12f}   closed form {cf.float():.12f}   "
          f"{'EQUAL (exact)' if same else 'DIFFER'}")
print(f"  closed form validated: {ok}")

print()
print("=" * 78)
print("Step 2: the fixed-parameter family, pushed out in k")
print("=" * 78)
print(f"  lambda = {lam}, eps = {eps}  (exactly the values §4 fixes)")
vals = [(k, closed_form_lower(k, lam, eps)) for k in range(3, 201)]
best_k, best_v = max(vals, key=lambda t: t[1].float())
for k in (10, 20, 40, 60, 70, 76, 80, 100, 150, 200):
    v = dict(vals)[k]
    print(f"  k={k:>4}   lower bound on Phi(3) = {v.float():>14.6f}")
print()
print(f"  MAXIMUM over k <= 200:  {best_v.float():.6f}  attained at k = {best_k}")
print(f"  and it is strictly decreasing thereafter (coefficient of k^2 is "
      f"(1 - lambda^2)/2 = {float((1 - (101/100)**2)/2):.6f} < 0)")
print()
print("  => with lambda fixed at 101/100 the family gives Phi(3) >= 55.97 and NOTHING MORE.")
print("     It is a FINITE lower bound.  T1's stated proof does not go through as written.")

print()
print("=" * 78)
print("Step 3: repair -- let lambda, eps depend on k.  delta_k = 1/k^3, eps_k = delta_k/2")
print("=" * 78)
print("  separation after the push >= lambda - 2 eps = 1 + delta - delta = 1, so still >= 1.")
print()
print(f"{'k':>4} {'n':>6} {'b':>3} {'minsep^2':>16} {'lower bd Phi(3)':>18} {'(3k-3)/2':>10}")
fails = []
for k in list(range(3, 13)) + [16, 20, 25]:
    delta = F(1, k ** 3)
    lam_k = 1 + delta
    eps_k = delta / 2
    pts, corners, tri = perturbed_family(k, lam_k, eps_k)
    ms2 = min_sep2(pts)
    hull = convex_hull(pts)
    b = sum(1 for p in pts if on_hull_boundary(p, hull))
    A2 = shoelace2(hull)
    lower = q3(len(pts)) - A2 * Q3(0, F(1, 3)) - q3(1)
    good = (ms2 >= q3(1)) and b == 3 and len(hull) == 3 and all(inside_triangle(p, tri) for p in pts)
    if not good:
        fails.append(k)
    print(f"{k:>4} {len(pts):>6} {b:>3} {ms2.float():>16.12f} {lower.float():>18.9f} "
          f"{F(3*k-3,2)!s:>10}  {'ok' if good else 'BAD'}")
print()
# closed-form continuation of the repaired family
print("  continued by closed form (geometry already validated in step 1):")
for k in (50, 100, 500, 1000, 10000):
    delta = F(1, k ** 3)
    print(f"    k={k:>6}  lower bound on Phi(3) = "
          f"{closed_form_lower(k, 1 + delta, delta / 2).float():>14.4f}   ((3k-3)/2 = {(3*k-3)/2})")
print()
print("  => Phi(3) must exceed every real number.  T1 is TRUE, with this repaired family.")
if fails:
    print("REPAIR FAILED at k =", fails)
    raise SystemExit(1)
