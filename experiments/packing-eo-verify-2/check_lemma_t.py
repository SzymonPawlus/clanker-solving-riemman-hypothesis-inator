"""Lemma T, T2, S2 (attacks/eo-oler-equality §§1,2,5) -- independent check.

Lemma T:  x,y,z >= 1 triangle sides  =>  (2/sqrt3)A + p/2 >= 2, equality iff (1,1,1) or (2,1,1).
Decided exactly: with rational sides, 16A^2 = S*alpha*beta*gamma is rational, and
   (2/sqrt3)A >= 2 - p/2
is, when the RHS is >= 0, equivalent to  (16/3)A^2 >= (4-S)^2  -- a rational comparison.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import random

FAIL = []
def ck(n, c, e=""):
    if not c: FAIL.append(n)
    print(f"  [{'PASS' if c else 'FAIL'}] {n}{(' :: '+e) if e else ''}")

def lemma_t(x, y, z):
    """returns (holds, is_equality) exactly, or None if not a (possibly degenerate) triangle"""
    a, b, c = y + z - x, z + x - y, x + y - z
    if a < 0 or b < 0 or c < 0:
        return None
    S = x + y + z
    A2_16 = S * a * b * c            # = 16 A^2
    if S >= 4:
        # p/2 >= 2 and A >= 0
        return (True, S == 4 and A2_16 == 0)
    # 3 <= S < 4 : need (16/3) A^2 >= (4-S)^2, i.e. A2_16/3 >= (4-S)^2
    lhs = F(A2_16, 3)
    rhs = (4 - S) ** 2
    return (lhs >= rhs, lhs == rhs)

print("=" * 78)
print("Lemma T -- exhaustive-ish exact scan")
print("=" * 78)
eqs = set(); viol = []; cnt = 0
step = F(1, 12)
vals = [1 + i * step for i in range(0, 37)]     # 1 .. 4
for x, y, z in combinations_with_replacement(vals, 3):
    r = lemma_t(x, y, z)
    if r is None: continue
    cnt += 1
    if not r[0]: viol.append((x, y, z))
    if r[1]: eqs.add(tuple(sorted((x, y, z))))
print(f"  grid scan (sides in [1,4], step 1/12): {cnt} triangles, {len(viol)} violations")
print(f"  equality triples found: {sorted(str(t) for t in eqs)}")
ck("no violation on the grid", not viol)
ck("equality set is exactly {(1,1,1),(1,1,2)}",
   eqs == {(F(1), F(1), F(1)), (F(1), F(1), F(2))})

random.seed(20260821)
viol = []; eqs2 = set(); cnt = 0
for _ in range(200000):
    x = F(random.randint(12, 84), 12); y = F(random.randint(12, 84), 12); z = F(random.randint(12, 84), 12)
    r = lemma_t(x, y, z)
    if r is None: continue
    cnt += 1
    if not r[0]: viol.append((x, y, z))
    if r[1]: eqs2.add(tuple(sorted((x, y, z))))
print(f"  random scan (sides in [1,7]): {cnt} triangles, {len(viol)} violations, "
      f"equality {sorted(str(t) for t in eqs2)}")
ck("no violation in the random scan", not viol)
ck("random scan finds no third equality triple", eqs2 <= {(F(1),F(1),F(1)),(F(1),F(1),F(2))})

# adversarial: the two equality cases perturbed, and thin slivers
print()
print("  adversarial probes around the two equality cases and at degeneracy:")
bad = []
for base in ((F(1),F(1),F(1)), (F(2),F(1),F(1))):
    for d1 in range(-6, 7):
        for d2 in range(-6, 7):
            for d3 in range(-6, 7):
                t = (base[0]+F(d1,1000), base[1]+F(d2,1000), base[2]+F(d3,1000))
                if any(s < 1 for s in t): continue
                r = lemma_t(*t)
                if r is None: continue
                if not r[0]: bad.append(t)
                if r[1] and tuple(sorted(t)) not in {(F(1),F(1),F(1)),(F(1),F(1),F(2))}:
                    bad.append(("EXTRA EQ", t))
ck("no violation and no new equality within 6/1000 of either equality case", not bad,
   str(bad[:3]))
# degenerate x = y+z
bad = []
for i in range(20, 81):
    for j in range(20, 81):
        y, z = F(i,20), F(j,20)
        r = lemma_t(y+z, y, z)
        if r is None: continue
        if not r[0]: bad.append((y,z))
        if r[1] and tuple(sorted((y+z,y,z))) != (F(1),F(1),F(2)): bad.append(("EXTRA", y, z))
ck("degenerate family x=y+z: no violation, equality only at (2,1,1)", not bad)
# thin sliver with a very long side
bad = []
for L in (F(10), F(100), F(1000)):
    for eps in (F(1,10), F(1,100), F(1,1000)):
        r = lemma_t(L, L + eps - eps, L)   # near-equilateral large
        if r and not r[0]: bad.append((L, eps))
        r = lemma_t(2*L, L, L)             # degenerate long
        if r and not r[0]: bad.append(("deg", L))
        r = lemma_t(2*L - eps, L, L)       # thin sliver
        if r and not r[0]: bad.append(("sliver", L, eps))
ck("large-S / thin-sliver probes: no violation", not bad)

print()
print("=" * 78)
print("Step 3 (the author's flagged step): min of a*b*c over Delta_S")
print("=" * 78)
print("  claim: for S in (3,4), Delta_S is the triangle on the permutations of (S-2,S-2,4-S),")
print("         and min a*b*c = (S-2)^2 (4-S).")
bad = []
for num in range(30, 40):
    S = F(num, 10)
    lo, hi = 4 - S, S - 2
    # brute-force minimum over a fine grid of the feasible set
    best = None
    N = 200
    for i in range(N + 1):
        al = lo + (hi - lo) * F(i, N)
        for j in range(N + 1):
            be = lo + (hi - lo) * F(j, N)
            ga = S - al - be
            if ga < lo or ga > hi: continue
            p = al * be * ga
            if best is None or p < best: best = p
    claimed = hi * hi * lo
    if best != claimed:
        bad.append((S, best, claimed))
ck("grid minimum equals (S-2)^2(4-S) for S = 3.0 .. 3.9", not bad, str(bad[:2]))
# the polynomial identity

ok = all((S - 3) * (S * S - S + 4) == S**3 - 4*S**2 + 7*S - 12
         for S in (F(n, 7) for n in range(21, 60)))
ck("identity S(S-2)^2+3S-12 == (S-3)(S^2-S+4)",
   all(S*(S-2)**2 + 3*S - 12 == (S-3)*(S*S-S+4) for S in (F(n,7) for n in range(21,60))))
ck("S^2-S+4 > 0 always (discriminant -15)", (-1)**2 - 4*1*4 == -15)

print()
print("=" * 78)
print("T2 identity and S2")
print("=" * 78)
ok = True
for n in range(3, 40):
    for b in range(3, n + 1):
        Ff = 2*n - b - 2
        Eall = F(3*Ff + b, 2)
        Eint = Eall - b
        if Eint != 3*n - 2*b - 3: ok = False
ck("|E_int| = 3n-2b-3 follows from F = 2n-b-2", ok)
def Tk(k): return k*(k+1)//2
ok = all(F((k-1)**2 + 3*(k-1) + 2, 2) == Tk(k) for k in range(2, 40))
ck("S2: (a^2+3a+2)/2 = T(k) exactly at a=k-1, so deficit>=1 <=> a>=k-1 <=> EO", ok)
# epsilon scale table
import math
print("  epsilon scale a_eps = (-3+sqrt(217+8eps))/2:")
for e_s in ("0", "1/4", "1/2", "3/4", "1"):
    e = F(e_s)
    v = (-3 + math.sqrt(217 + 8*float(e)))/2
    print(f"    eps={e_s:>4}  a_eps = {v:.6f}")
ck("eps=1 gives a=6 exactly (sqrt225=15)", 217 + 8 == 225)

print()
print("FAILURES:", FAIL if FAIL else "none")
raise SystemExit(1 if FAIL else 0)
