"""
Step 1 + step 2 of the r6-interaction assignment, done with a script (never by hand).

Normalisation used THROUGHOUT this file: SEPARATION 1, container T(a) = closed equilateral
triangle of side a.  The repo's d-normalisation is d = 2a; s = d + 2*sqrt(3).

Oler (1961), `cited`: for a finite non-collinear E in the plane with pairwise distances >= 1,
    |E| <= (2/sqrt3) * area(conv E) + perim(conv E)/2 + 1.
Write  r(E) := 4*area(conv E)/sqrt3   and   M(E) := perim(conv E).  Then Oler is

    n <= (r + M)/2 + 1                                        (*)

which is what makes (r, M) the natural coordinates: on a hull tiled by unit triangles with all
boundary edges of length 1, r = #faces and M = #boundary edges, both integers.

For T(a): r = a^2, M = 3a, so (*) gives n <= (a^2 + 3a)/2 + 1, i.e. a >= a_Oler(n) = (sqrt(8n+1)-3)/2.
"""
import math
from fractions import Fraction

SQ3 = math.sqrt(3.0)

def a_oler(n):
    return (math.sqrt(8*n+1) - 3)/2.0

def tri(k):
    return k*(k+1)//2

# ---------------------------------------------------------------- candidates
# Each candidate is a CONCLUSION SHAPE.  We evaluate the best value it can give
# at the equilateral triangle, i.e. the largest a it can rule out for n points.

def rho_lattice(n):
    """
    C2.  Conclusion shape:   n <= f*(area, perim),  f* = max point count realisable with hull
    area <= A and hull perimeter <= M.  NOT affine in (A, M): the container enters as

            a(n) >= rho(n) := min over n-point unit-separated E of  max( sqrt(r(E)), M(E)/3 ).

    Here we compute the value of that min restricted to OLER-TIGHT (lattice-tiled) configurations,
    for which r and M are integers with r + M = 2(n-1).  That is an UPPER bound on rho(n)
    coming from the tight family only, hence a bound on how much C2 could possibly give.
    """
    best = None
    tot = 2*(n-1)
    for M in range(3, tot):          # boundary edges; needs at least a triangle
        r = tot - M
        if r < 1:
            continue
        val = max(math.sqrt(r), M/3.0)
        if best is None or val < best[0]:
            best = (val, r, M)
    return best

def report():
    print("="*78)
    print("STEP 1/2.  Candidate conclusion shapes evaluated at the equilateral triangle")
    print("="*78)
    print()
    print("--- (a) Oler is EXACTLY tight at every triangular n (verification, exact) ---")
    for k in range(2, 9):
        n = tri(k); a = k-1
        lhs = Fraction(a*a + 3*a, 2) + 1
        print(f"  k={k:2d}  n=Delta(k)={n:3d}  a=k-1={a}   Oler RHS at a = {lhs}   equal to n: {lhs==n}")
    print()
    print("--- (b) C2 (max(sqrt r, M/3)) at triangular n: does it MATCH Oler? ---")
    print("     lattice T(k-1) has r=(k-1)^2, M=3(k-1) -> max(k-1, k-1) = k-1 = a_Oler.  Check:")
    for k in range(2, 9):
        n = tri(k)
        val, r, M = rho_lattice(n)
        print(f"  k={k:2d}  n={n:3d}  a_Oler={a_oler(n):.6f}   min over tight (r,M)={val:.6f}"
              f"  at (r,M)=({r},{M})   matches Oler: {abs(val-a_oler(n))<1e-12}")
    print()
    print("--- (c) C2, integer search over r+M=2(n-1).  *** NOT a valid upper bound on rho: ***")
    print("      such an (r,M) need not be REALISABLE.  Use families.py for the sound table.")
    print("      This block is kept only as a LOWER bound on the tight-family minimum.")
    print(f"  {'n':>4} {'a_Oler':>10} {'rho_tight<=':>12} {'(r,M)':>10} {'gain in a':>10} {'gain in d':>10}")
    for n in [16,17,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34]:
        val, r, M = rho_lattice(n)
        ao = a_oler(n)
        print(f"  {n:>4} {ao:>10.6f} {val:>12.6f} {str((r,M)):>10} {val-ao:>10.6f} {2*(val-ao):>10.6f}")
    print()
    print("--- (d) C2 at Delta(k)-1: WHERE DOES IT JUMP?  (same realisability caveat as (c)) ---")
    print("  EO(k) needs the bound to rule out n=Delta(k)-1 for every a < k-1.")
    print(f"  {'k':>3} {'n':>4} {'a_Oler':>10} {'rho_tight<=':>12} {'target a=k-1':>13} {'closes EO(k)?':>14}")
    for k in range(3, 9):
        n = tri(k)-1
        val, r, M = rho_lattice(n)
        print(f"  {k:>3} {n:>4} {a_oler(n):>10.6f} {val:>12.6f} {k-1:>13} "
              f"{str(val >= k-1):>14}")
    print()
    print("--- (e) The Jump Lemma, numerically illustrated ---")
    print("  N(a) = max points at separation 1 in T(a).  Any valid bound B has B(k-1) >= Delta(k)")
    print("  (the lattice witness).  To prove EO(k) it needs B(a) < Delta(k)-1 for a < k-1.")
    print("  So B must DROP BY MORE THAN 1 across a = k-1.  Oler's drop there is 0 (continuous):")
    for k in [4,5,6]:
        a = k-1
        for eps in [1e-3, 1e-6, 1e-9]:
            b = ((a-eps)**2 + 3*(a-eps))/2 + 1
            print(f"    k={k}  a={a}-{eps:g}:  Oler = {b:.9f}   need < {tri(k)-1}   "
                  f"shortfall = {b-(tri(k)-1):.9f}")
    print()
    print("--- (f) C3: Oler minus a defect,  n <= (r+M)/2 + 1 - D(E),  D>=0 ---")
    print("  Validity at any Oler-tight config forces D = 0 there (else the bound is FALSE).")
    print("  Delta(k)-1 optimum = lattice minus a point => D -> 0 => margin -> 0.  Dead by F3.")
    print("  Numerically: the corner-deleted T(3) hull (k=4, n=9) is Oler-tight:")
    r_, M_ = 8, 8   # trapezoid: area 2*sqrt3 -> r = 8; perimeter 8
    print(f"    (r,M)=({r_},{M_})  Oler RHS = {(r_+M_)/2+1}  n = 9  slack = {(r_+M_)/2+1-9}")

if __name__ == "__main__":
    report()
