"""Round-3 audit: independent re-derivation of every load-bearing number in the
r3-approaches triage file sections Z.1, 0.1 and 0.2.

Nothing here is read from the triage file. Every quantity is re-derived from a
primary statement quoted in a docstring below, using exact symbolic algebra
(sympy), and only then compared against the triage file's printed value.

Run:  python3 audit_calibration.py
"""

import sympy as sp

R3 = sp.sqrt(3)
PI = sp.pi
FAIL = []


def check(label, got, want, tol=None, exact=False):
    """Compare and record. `want` may be an exact sympy expr (exact=True) or a
    decimal string printed in the triage file (compared to `tol`)."""
    if exact:
        ok = sp.simplify(got - want) == 0
        shown = sp.srepr if False else str
        print(f"  [{'OK ' if ok else 'FAIL'}] {label}: {sp.nsimplify(got)}  ==  {want}")
    else:
        ok = abs(sp.N(got, 30) - sp.Rational(want)) <= sp.Rational(tol)
        print(f"  [{'OK ' if ok else 'FAIL'}] {label}: {sp.N(got, 16)}  vs triage {want}  (tol {tol})")
    if not ok:
        FAIL.append(label)
    return ok


# ----------------------------------------------------------------------------
# 1. OLER'S INEQUALITY -> d(n) >= sqrt(8n+1) - 3          (triage file s0.1)
# ----------------------------------------------------------------------------
# Oler, "A finite packing problem", Canad. Math. Bull. 4 (1961) 153-155.
# Statement (normalised to minimum mutual distance 1): if a convex region K of
# area A and perimeter P contains n points with pairwise distances >= 1, then
#
#            n  <=  (2/sqrt3) * A  +  P/2  +  1.
#
# We apply it to OUR object: an equilateral triangle of side d holding n points
# at pairwise distance >= 2.  Scale the whole picture by 1/2 so the separation
# becomes 1; the triangle then has side d/2.
print("=" * 78)
print("1. OLER  ->  d(n) >= sqrt(8n+1) - 3   [triage s0.1]")
print("=" * 78)

d, n, s, D = sp.symbols('d n s D', positive=True)

A_half = R3 / 4 * (d / 2) ** 2          # area of equilateral triangle of side d/2
P_half = 3 * (d / 2)                    # its perimeter
oler_rhs = sp.expand(2 / R3 * A_half + P_half / 2 + 1)
print(f"  Oler RHS for side-d triangle, separation 2:  n <= {oler_rhs}")
check("Oler RHS equals d^2/8 + 3d/4 + 1", oler_rhs, d**2/8 + 3*d/4 + 1, exact=True)

# Invert:  d^2/8 + 3d/4 + 1 >= n  <=>  (d+3)^2 >= 8n+1  <=>  d >= sqrt(8n+1)-3.
sols = sp.solve(sp.Eq(oler_rhs, n), d)
d_oler = [x for x in sols if sp.N(x.subs(n, 16)) > 0][0]
print(f"  solve(n = RHS, d), positive root:  d = {sp.simplify(d_oler)}")
check("closed form is sqrt(8n+1)-3", sp.simplify(d_oler), sp.sqrt(8*n+1) - 3, exact=True)

# Correctness check Oler's theorem MUST pass: exact tightness at triangular
# numbers n = k(k+1)/2, whose optimum is the side-2 triangular lattice, d = 2(k-1).
print("\n  Tightness at triangular numbers (Oler's own equality case):")
k = sp.symbols('k', positive=True, integer=True)
rhs_at_tri = sp.simplify(oler_rhs.subs(d, 2 * (k - 1)))
check("RHS at d=2(k-1) equals k(k+1)/2 identically in k",
      sp.expand(rhs_at_tri), sp.expand(k * (k + 1) / 2), exact=True)
for kk in range(2, 8):
    dd = 2 * (kk - 1)
    val = oler_rhs.subs(d, dd)
    tri = kk * (kk + 1) // 2
    ok = sp.simplify(val - tri) == 0
    if not ok:
        FAIL.append(f"tight k={kk}")
    print(f"    [{'OK ' if ok else 'FAIL'}] k={kk}: d={dd}, RHS={val}, Delta(k)={tri}")

d16 = sp.sqrt(8 * 16 + 1) - 3
s16_oler = 2 * R3 + d16
print()
check("d(16) >= sqrt(129)-3", d16, "8.357817", "5e-7")
check("s(16) >= 2sqrt3+sqrt129-3", s16_oler, "11.821918", "5e-7")

# ----------------------------------------------------------------------------
# 2. DENSITY <-> SIDE LENGTH DICTIONARY, then the Z.1 threshold 0.7559
# ----------------------------------------------------------------------------
# Convention (the only one that makes the two published baselines below come
# out right -- see s3, which is the actual evidence for this choice):
#     density of an n-circle packing of UNIT circles in an equilateral
#     triangle of side s  :=  n * pi * 1^2 / area(triangle) = n*pi/((sqrt3/4)s^2).
#
# If D_n is a valid UPPER bound on that density over all packings of n unit
# circles in an equilateral triangle, then the optimal packing (side s(n))
# satisfies  n*pi/((sqrt3/4)s(n)^2) <= D_n, hence
#
#     s(n) >= 2*sqrt( n*pi / (sqrt3 * D_n) ).
#
# Conversely a claimed lower bound L on s(n) corresponds to the density bound
#     D = 4*n*pi/(sqrt3 * L^2),
# and a published D_n beats L exactly when D_n <= that value.
print()
print("=" * 78)
print("2. DENSITY <-> SIDE DICTIONARY and the Gaspar-Tarnai threshold [triage Z.1]")
print("=" * 78)

density_of_side = lambda nn, ss: nn * PI / (R3 / 4 * ss ** 2)
side_from_density = lambda nn, DD: 2 * sp.sqrt(nn * PI / (R3 * DD))

# round-trip sanity check of the dictionary
rt = sp.simplify(side_from_density(n, density_of_side(n, s)) - s)
check("dictionary round-trips (side -> density -> side)", rt, 0, exact=True)

s16_repo = 2 + 6 * R3                    # the repo's sketch-tier n=16 lower bound
thresh = sp.simplify(density_of_side(16, s16_repo))
print(f"\n  repo sketch bound      s(16) >= 2+6sqrt3   = {sp.N(s16_repo, 16)}")
print(f"  equivalent density     D = 64pi/(sqrt3(2+6sqrt3)^2) = {sp.nsimplify(thresh)}")
check("THRESHOLD: G-T beat the repo iff their D(16) <=", thresh, "0.7559", "5e-5")
print(f"  exact threshold        = {sp.simplify(thresh)}")
print(f"  to 10 places           = {sp.N(thresh, 12)}")

# ----------------------------------------------------------------------------
# 3. The two published baselines -- this is what pins the density convention
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("3. BASELINES: plain Oler and plain Groemer at n=16 in the triangle")
print("=" * 78)

# (a) OLER, via s16_oler above.
D_oler16 = sp.simplify(density_of_side(16, s16_oler))
check("plain Oler density bound at n=16", D_oler16, "0.8306", "5e-5")

# (b) GROEMER, Math. Z. 73 (1960) 285-294, p.285, Satz (quoted verbatim in
#     problems/circle-packing-equilateral-triangle/README.md, read from the GDZ
#     scan by an earlier worker):
#         n * sqrt12 <= F - kappa*U + lambda,
#     for n UNIT circles packed in a convex region of area F and perimeter U,
#     with kappa = (2-sqrt3)/2 and lambda = sqrt12 - pi(sqrt3 - 1).
#     Apply with the region = the containing equilateral triangle of side s:
#     F = sqrt3 s^2/4, U = 3s.
kappa = (2 - R3) / 2
lam = sp.sqrt(12) - PI * (R3 - 1)
F, U = R3 * s ** 2 / 4, 3 * s
groemer = sp.Eq(16 * sp.sqrt(12), F - kappa * U + lam)
s16_groemer = max([x for x in sp.solve(groemer, s) if sp.im(sp.N(x)) == 0 and sp.N(x) > 0],
                  key=lambda x: sp.N(x))
D_groemer16 = sp.simplify(density_of_side(16, s16_groemer))
print(f"  kappa = {sp.N(kappa,10)}, lambda = {sp.N(lam,10)}")
print(f"  Groemer => s(16) >= {sp.N(s16_groemer, 16)}")
check("plain Groemer density bound at n=16", D_groemer16, "0.8527", "5e-5")

print("\n  >>> Both triage baselines reproduce under this density convention, from")
print("      the two primary inequalities. That is the evidence that the")
print("      convention (n*pi / area of the side-s triangle) is the right one.")

# Where the truth actually is, for calibrating 'how much sharpening is needed'.
s16_best = sp.Rational("12.713628774151")     # best-known construction, `numerical`
D_best16 = density_of_side(16, s16_best)
print()
print("  Ladder at n=16 (density; SMALLER = sharper upper bound):")
rows = [("Groemer 1960 (rigorous)", D_groemer16, s16_groemer),
        ("Oler 1961 (rigorous)", D_oler16, s16_oler),
        ("THRESHOLD to beat repo sketch", thresh, s16_repo),
        ("best-known packing (truth is <= this)", D_best16, s16_best)]
for lab, DD, ss in rows:
    print(f"    {lab:<40} D = {sp.N(DD,8)}   s = {sp.N(ss,10)}")
g1 = (sp.N(D_groemer16) - sp.N(D_oler16)) / sp.N(D_groemer16) * 100
g2 = (sp.N(D_oler16) - sp.N(thresh)) / sp.N(D_oler16) * 100
g3 = (sp.N(thresh) - sp.N(D_best16)) / sp.N(thresh) * 100
print(f"\n    Groemer -> Oler sharpening actually achieved : {g1:.2f}%")
print(f"    Oler -> threshold sharpening G-T would need  : {g2:.2f}%")
print(f"    threshold -> truth, headroom still left      : {g3:.2f}%")

# ----------------------------------------------------------------------------
# 4. The Q(sqrt3) family at n = 17, 24, 31                 (triage s0.2)
# ----------------------------------------------------------------------------
# IMPORTANT METHODOLOGICAL NOTE.  The first draft of this audit typed the
# best-known table from the auditor's own recollection and got n = 19, 25, 28
# and 32 wrong, which manufactured a false "disagreement".  The table is now
# read from the repo's own transcription of Graham & Lubachevsky's printed
# 15-significant-digit values, experiments/circle-packing-search/reference.py
# (GL_D), which is d(n) = disk diameter in units of the side of the triangle
# containing the CENTRES, so  s(n) = 2/d(n) + 2*sqrt3.
print()
print("=" * 78)
print("4. Q(sqrt3) CLOSED FORMS among OPEN n   [triage s0.2]")
print("=" * 78)

import importlib.util, pathlib
_ref_path = pathlib.Path(__file__).resolve().parents[1] / "circle-packing-search" / "reference.py"
_spec = importlib.util.spec_from_file_location("gl_reference", _ref_path)
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)
print(f"  best-known table read from: {_ref_path}")

# s(n) as an EXACT rational-plus-2sqrt3 value, from GL's printed decimal for d(n).
def s_of(nn):
    return 2 / sp.Rational(_ref.GL_D[nn]) + 2 * R3

for nn, cf in [(17, 6 + 4 * R3), (24, 8 + 4 * R3), (31, 10 + 4 * R3)]:
    v = sp.N(s_of(nn), 30)
    ok = abs(v - sp.N(cf, 30)) <= sp.Rational(2, 10**11)
    if not ok:
        FAIL.append(f"closed form n={nn}")
    print(f"  [{'OK ' if ok else 'FAIL'}] n={nn}: GL d={_ref.GL_D[nn]} -> s={sp.N(s_of(nn),15)}"
          f"  vs  {sp.nsimplify(cf)} = {sp.N(cf,15)}")

print("\n  Spacing / recurrence claims of s0.2:")
check("s(24) - s(17) == 2 exactly", (8 + 4*R3) - (6 + 4*R3), 2, exact=True)
check("s(31) - s(24) == 2 exactly", (10 + 4*R3) - (8 + 4*R3), 2, exact=True)
check("s(17) == s(12)+2 with s(12)=4+4sqrt3", 6 + 4*R3, (4 + 4*R3) + 2, exact=True)
print(f"    index spacing: 24-17 = {24-17}, 31-24 = {31-24}")

# --- the exclusivity claim, scanned over the CORRECT open set -----------------
# Settled per problems/.../README.md: all n <= 15, all triangular n = k(k+1)/2,
# and n = 20.  Triangular numbers in range: 21 = Delta(6), 28 = Delta(7).
TRIANGULAR = {k * (k + 1) // 2 for k in range(2, 12)}
SETTLED_EXTRA = {20}
open_n = [nn for nn in sorted(_ref.GL_D)
          if 16 <= nn <= 34 and nn not in TRIANGULAR and nn not in SETTLED_EXTRA]
print(f"\n  Open n in 16..34 with a GL entry: {open_n}")
print("  (21 and 28 dropped as triangular/proven, 20 dropped as Payan-proven)")
print("\n  Scan for s(n) = a + b*sqrt3, a,b integers in -40..40, |err| <= 2e-11:")

r3f = sp.N(R3, 50)
hits = {}
for nn in open_n:
    v = sp.N(s_of(nn), 50)
    found = []
    for b in range(-40, 41):
        rem = v - b * r3f
        a = sp.Integer(sp.floor(rem + sp.Rational(1, 2)))
        if abs(rem - a) <= sp.Rational(2, 10**11) and abs(a) <= 40:
            found.append((int(a), b))
    if found:
        hits[nn] = found
    tag = ", ".join(f"{a}+{b}sqrt3" for a, b in found) or "-- none --"
    print(f"    n={nn:<3} s={sp.N(s_of(nn),15)!s:<18} {tag}")

expected = {17, 24, 31}
got = set(hits)
print(f"\n  triage s0.2 claims the Q(sqrt3) open cases are exactly {sorted(expected)}")
print(f"  this audit finds                                        {sorted(got)}")
if got != expected:
    extra = sorted(got - expected)
    print(f"\n  >>> DISAGREEMENT: triage s0.2 MISSES n = {extra}.")
    for nn in extra:
        a, b = hits[nn][0]
        print(f"      n={nn}: GL prints d({nn}) = {_ref.GL_D[nn]}, giving s({nn}) = {a}+{b}sqrt3 "
              f"= {sp.N(sp.Integer(a)+b*R3,15)}")
    FAIL.append("s0.2 exclusivity claim is FALSE")
else:
    print("  [OK ] exclusivity claim reproduces")

# Why n=27 matters: it is Delta(7)-1, the first OPEN Erdos-Oler case, and its
# best-known value is the Erdos-Oler prediction s(27) = s(28) exactly.
if 27 in got:
    print("\n  n=27 detail (the consequential one):")
    print(f"    Delta(7) = 28, so 27 = Delta(7)-1: the first OPEN Erdos-Oler case (k=7).")
    print(f"    GL print d(27) = d(28) = {_ref.GL_D[27]} = 1/6 to the digits printed;")
    print(f"    1/6 exactly gives s = 2*6 + 2sqrt3 = {sp.nsimplify(12+2*R3)} = {sp.N(12+2*R3,15)}")
    print(f"    err vs GL's printed decimal for n=27: "
          f"{sp.N(abs(s_of(27) - (12+2*R3)), 5)}")
    print("    => an exact tight certificate for n=27 is the 28-point side-2 triangular")
    print("       lattice minus one point. It is the CHEAPEST open case in the range,")
    print("       cheaper than n=17, and triage s0.2/proposal Y both miss it.")

print()
print("=" * 78)
print("FAILURES:", FAIL if FAIL else "none")
print("=" * 78)
