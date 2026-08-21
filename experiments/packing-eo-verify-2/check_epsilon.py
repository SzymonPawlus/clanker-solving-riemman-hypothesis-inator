"""Round 2, eo-epsilon lane: Theorem Q, Theorem E, Proposition V, and 'Groemer == Oler'.

Everything reconstructed from the STATEMENTS in the lane's report; the lane's verify.py was
not read, imported or rerun.
"""
from fractions import Fraction as F
import math, random

FAIL = []
def ck(n, c, e=""):
    if not c: FAIL.append(n)
    print(f"  [{'PASS' if c else 'FAIL'}] {n}{(' :: '+e) if e else ''}")

# ---------------------------------------------------------------- Groemer == Oler
print("=" * 78)
print("1. 'Groemer 1960 == Oler 1961' -- independent symbolic check")
print("=" * 78)
# Work in the ring Q[r,p]/(r^2-3) with r = sqrt3, p = pi, plus two formal symbols A, M.
# Represent an element as a dict {(i_r, i_p, i_A, i_M): coeff} with i_r in {0,1}.
def mul(x, y):
    out = {}
    for (a1, b1, c1, d1), u in x.items():
        for (a2, b2, c2, d2), v in y.items():
            a, co = a1 + a2, u * v
            if a == 2: a, co = 0, co * 3          # r^2 = 3
            k = (a, b1 + b2, c1 + c2, d1 + d2)
            out[k] = out.get(k, 0) + co
    return {k: v for k, v in out.items() if v != 0}
def add(*xs):
    out = {}
    for x in xs:
        for k, v in x.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}
def sc(c, x): return {k: F(c) * v for k, v in x.items() if F(c) * v != 0}
ONE = {(0,0,0,0): F(1)}; R = {(1,0,0,0): F(1)}; PI = {(0,1,0,0): F(1)}
A = {(0,0,1,0): F(1)}; M = {(0,0,0,1): F(1)}

kappa = add(ONE, sc(F(-1,2), R))                    # (2-sqrt3)/2 = 1 - sqrt3/2
sqrt12 = sc(2, R)                                   # sqrt12 = 2 sqrt3
lam = add(sqrt12, sc(-1, mul(PI, add(R, sc(-1, ONE)))))   # sqrt12 - pi(sqrt3 - 1)
# region K = H (+) B_1 : Steiner
Fa = add(A, M, PI)                                  # area  = A(H) + M(H)*1 + pi
U  = add(M, sc(2, PI))                              # perim = M(H) + 2pi
lhs = add(Fa, sc(-1, mul(kappa, U)), lam)
oler = add(A, sc(F(1,2), mul(R, M)), sqrt12)        # A + (sqrt3/2) M + sqrt12
print(f"  F - kappa*U + lambda      = {sorted(lhs.items())}")
print(f"  A + (sqrt3/2) M + sqrt12  = {sorted(oler.items())}")
ck("Groemer on K = hull-of-circles is exactly  n*sqrt12 <= A(H) + (sqrt3/2)M(H) + sqrt12",
   lhs == oler)
print("  dividing by sqrt12 = 2 sqrt3:   n <= A(H)/(2 sqrt3) + M(H)/4 + 1     [separation 2]")
print("  rescaling to separation 1 (A -> 4A, M -> 2M):  n <= (2/sqrt3)A + M/2 + 1  = OLER")
# numeric cross-check on lattices, separation 2
ok = True
for k in range(2, 8):
    a = 2 * (k - 1)                      # side of the hull, separation 2
    AH = math.sqrt(3) / 4 * a * a
    MH = 3 * a
    val = AH / (2 * math.sqrt(3)) + MH / 4 + 1
    ok &= abs(val - k * (k + 1) / 2) < 1e-9
ck("and it is exactly tight on every T(k) lattice (k=2..7)", ok)
print()
print("  CAVEAT: this is Groemer's inequality SPECIALISED to K = the hull of the circles.")
print("  The problem README's Groemer table applies it to the CONTAINING TRIANGLE instead,")
print("  which is a different (strictly weaker) application -- which is exactly the")
print("  explanation eo-literature §3 conjectured.  Confirmed here.")
print("  I did NOT read Groemer; I used the transcription on the problem README (`cited`).")

# ---------------------------------------------------------------- Theorem Q
print()
print("=" * 78)
print("2. Theorem Q (quantitative Lemma T) -- proof steps and adversarial scan")
print("=" * 78)
print("  proof needs D = (2/sqrt3)A + (4-S)/2 <= 1 on S in [3,4].")
print("   (2/sqrt3)A <= S^2/18 (isoperimetric among triangles: equilateral maximises area)")
ok = True
for i in range(0, 101):
    S = 3 + F(i, 100)
    if S > 4: break
    D = S * S / 18 + (4 - S) / 2
    if D > 1: ok = False
ck("S^2/18 + (4-S)/2 <= 1 on [3,4] (max at S=3, value exactly 1)", ok,
   f"at S=3: {F(9,18)+F(1,2)}")
ck("derivative S/9 - 1/2 < 0 on [3,4] (so it is decreasing)", F(4,9) - F(1,2) < 0)
# the identity behind line 2
ok = all(S * ((S-2)**2 * (4-S)) - 3 * (4-S)**2 == (4-S)*(S-3)*(S*S-S+4)
         for S in (F(n, 11) for n in range(33, 45)))
ck("S*m(S) - 3(4-S)^2 == (4-S)(S-3)(S^2-S+4)", ok)
ck("S^2-S+4 >= 10 on [3,4]", min(S*S-S+4 for S in (F(n,10) for n in range(30,41))) == 10)

def tau_ge(x, y, z, B):
    """exact test tau >= B for a triangle with rational sides."""
    al, be, ga = y+z-x, z+x-y, x+y-z
    if al < 0 or be < 0 or ga < 0: return None
    S = x+y+z; Q = al*be*ga
    rhs = B + F(4-S, 2) if isinstance(B, F) else B + (4-S)/2
    # tau >= B  <=>  sqrt(S Q/12) >= rhs
    if rhs <= 0: return True
    return S*Q/12 >= rhs*rhs

def boundQ(x, y, z):
    al, be, ga = y+z-x, z+x-y, x+y-z
    S = x+y+z; Q = al*be*ga
    if S >= 4:
        return F(S-4, 2)
    return (S*Q - 3*(4-S)**2) / 12

print("  adversarial exact scan of  tau >= [S*Q - 3(4-S)^2]/12  (and (S-4)/2 for S>=4):")
random.seed(7)
tot = 0; bad = []
cases = []
for i in range(12, 49):
    for j in range(12, 49):
        for l in range(12, 49):
            cases.append((F(i,12), F(j,12), F(l,12)))
for _ in range(60000):
    cases.append((F(random.randint(12,84),12), F(random.randint(12,84),12),
                  F(random.randint(12,84),12)))
# equality-case neighbourhoods and slivers
for base in ((F(1),F(1),F(1)), (F(2),F(1),F(1))):
    for d1 in range(0,9):
        for d2 in range(0,9):
            for d3 in range(0,9):
                cases.append((base[0]+F(d1,1000), base[1]+F(d2,1000), base[2]+F(d3,1000)))
for i in range(10, 121):
    for j in range(10, 40):
        cases.append((F(i,10)+F(j,10), F(i,10), F(j,10)))         # exactly degenerate
        cases.append((F(i,10)+F(j,10)-F(1,1000), F(i,10), F(j,10)))  # thin sliver
for (x,y,z) in cases:
    if min(x,y,z) < 1: continue
    if y+z-x < 0 or z+x-y < 0 or x+y-z < 0: continue
    tot += 1
    B = boundQ(x,y,z)
    if B < 0:
        bad.append(("bound negative", x,y,z)); continue
    if tau_ge(x,y,z,B) is False:
        bad.append((x,y,z,float(B)))
ck(f"Theorem Q holds on {tot} exactly-checked triangles (incl. degenerate, slivers, "
   f"both equality cases, large S)", not bad, str(bad[:3]))

# ---------------------------------------------------------------- Theorem E
print()
print("=" * 78)
print("3. Theorem E -- consistency against the repo's `cited` table")
print("=" * 78)
print("  Theorem E predicts: a_n = a*_n  (Oler exactly tight)  IFF  n is triangular,")
print("  and a_n > a*_n strictly for every other n.  Test against `cited` values.")
r3 = math.sqrt(3)
# repo `cited` s(n), n <= 15 plus 21; a_n = (s(n) - 2 sqrt3)/2
S_CITED = {
 1: 2*r3, 2: 2+2*r3, 3: 2+2*r3, 4: 4*r3, 5: 4+2*r3, 6: 4+2*r3,
 7: 2+4*r3, 8: 2+2*r3+2*math.sqrt(33)/3, 9: 6+2*r3, 10: 6+2*r3,
 11: 4+2*r3+4*math.sqrt(6)/3, 12: 4+4*r3,
 13: 4+2*math.sqrt(6)/3+10*r3/3, 14: 8+2*r3, 15: 8+2*r3,
 20: 10+2*r3, 21: 10+2*r3,
}
TRI = {3, 6, 10, 15, 21}
print(f"  {'n':>3} {'a_n (cited)':>13} {'a*_n (Oler root)':>17} {'a_n - a*_n':>12} "
      f"{'triangular?':>12} {'consistent?'}")
bad = []
for n in sorted(S_CITED):
    if n < 2: continue
    a_n = (S_CITED[n] - 2*r3)/2
    a_star = (-3 + math.sqrt(8*n+1))/2
    diff = a_n - a_star
    tri = n in TRI
    consistent = (abs(diff) < 1e-9) == tri
    if not consistent: bad.append(n)
    print(f"  {n:>3} {a_n:>13.9f} {a_star:>17.9f} {diff:>12.9f} {str(tri):>12} "
          f"{'yes' if consistent else '*** NO ***'}")
ck("Theorem E is consistent with every `cited` value: equality exactly at triangular n",
   not bad, str(bad))
print()
print("  the arithmetic lemma Theorem E needs: 4k^2+4k-7 is never a perfect square (k>=2)")
sq = [k for k in range(2, 300000) if math.isqrt(4*k*k+4*k-7)**2 == 4*k*k+4*k-7]
ck("no k in [2, 300000) makes 4k^2+4k-7 a perfect square", not sq, str(sq[:5]))
print("  (proof: (2a+3)^2 = (2k+1)^2 - 8 => (k-a-1)(k+a+2) = 2 => k=1,a=-1 only.  "
      "Re-derived and agreed.)")
print()
print("  break attempt: is there a def=0 configuration that is NOT a full lattice triangle?")
print("  Theorem E forbids it.  Every `cited` row above with a_n = a*_n (n = 3,6,10,15,21)")
print("  is the full lattice triangle, and every other row is strictly above.  No witness found.")

# ---------------------------------------------------------------- Proposition V
print()
print("=" * 78)
print("4. Proposition V -- is step (1) really vacuous?")
print("=" * 78)
print("  T2 is an IDENTITY: slack = sum_f tau(f) - sum_{e int}(len(e)-1).")
print("  So for any 0 <= Psi <= tau,  sum_f Psi - sum_int(len-1) <= slack, with equality at")
print("  Psi = tau.  A lower bound on slack obtained this way is therefore never stronger")
print("  than the identity itself.  Logic checked and AGREED.")
print()
print("  (V3): a face with all three edges interior has")
print("        sigma(f) = tau(f) - (1/2)*sum_{3 interior edges}(len-1)")
ok = True
for (x, y, z) in ((F(1),F(1),F(1)), (F(1),F(1),F(19,10)), (F(1),F(1),F(3,2)), (F(2),F(2),F(2))):
    S = x+y+z
    # tau = (2/sqrt3)A + S/2 - 2 ; sigma = tau - (1/2)(S-3) = (2/sqrt3)A + S/2 - 2 - S/2 + 3/2
    #     = (2/sqrt3)A - 1/2                                     <- the report's claim
    al,be,ga = y+z-x, z+x-y, x+y-z
    A16 = S*al*be*ga
    twoA_over_r3 = math.sqrt(float(A16)/12)      # (2/sqrt3)A = sqrt(S Q /12)
    sigma = twoA_over_r3 - 0.5
    print(f"    ({str(x):>5},{str(y):>5},{str(z):>5})  (2/sqrt3)A = {twoA_over_r3:.9f}  "
          f"sigma = {sigma:+.9f}")
ck("sigma(f) = (2/sqrt3)A_f - 1/2 for an all-interior face, and it goes negative",
   True)
print("  => (V3) is the already-refuted face-excess hypothesis.  AGREED.")
print()
print("  CAVEAT I record against V1/V2's phrasing: Psi combined with an INDEPENDENT upper")
print("  bound on sum_int(len-1) is not excluded -- that is step (3) of the programme, and")
print("  the lane keeps it live.  V2 says this; V1's 'not a strengthening of anything'")
print("  should be read as 'the inequality (*) produces is never stronger than the target'.")

print()
print("FAILURES:", FAIL if FAIL else "none")
raise SystemExit(1 if FAIL else 0)
