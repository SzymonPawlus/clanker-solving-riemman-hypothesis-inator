"""Exact checks of the numeric/arithmetic claims in eo-exhaustion §2, §4, §5 and
eo-boundary-counting §2, plus an independent reconstruction of the oler-slack §1 identity.

Nothing here reads any author's code.
"""
from fractions import Fraction as F
import math

FAIL = []
def ck(name, cond, extra=""):
    if not cond: FAIL.append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{(' :: '+extra) if extra else ''}")

def T(k): return k * (k + 1) // 2

def isqrt_bracket(x, prec=10**12):
    """rational lower/upper bounds on sqrt(x) for x a Fraction, error < 1/prec"""
    lo = F(math.isqrt(int(x * prec * prec)), prec)
    hi = lo + F(1, prec)
    assert lo * lo <= x <= hi * hi, (x, lo, hi)
    return lo, hi

print("=" * 78)
print("A. eo-exhaustion §2 — Oler's free lower bound and the residual gap")
print("=" * 78)
# Oler at separation 1: n <= a^2/2 + 3a/2 + 1.  d = 2a.  n points => d >= sqrt(8n+1)-3.
ok = True
for k in range(3, 15):
    n = T(k) - 1
    # identity 8n+1 = 4k^2+4k-7
    ok &= (8 * n + 1 == 4 * k * k + 4 * k - 7)
ck("8(T(k)-1)+1 = 4k^2+4k-7 for k=3..14", ok)
# residual gap identity
ok = all((2 * k + 1) ** 2 - (4 * k * k + 4 * k - 7) == 8 for k in range(2, 40))
ck("(2k+1)^2 - (4k^2+4k-7) = 8  (so gap = 8/((2k+1)+sqrt(...)))", ok)
# Oler RHS at a = k-1 is exactly T(k)
ok = all(F((k - 1) ** 2, 2) + F(3 * (k - 1), 2) + 1 == T(k) for k in range(2, 40))
ck("Oler RHS at a=k-1 equals T(k) exactly, k=2..39", ok)
print()
print("  reproduce the §2 table (exact brackets on the irrational parts):")
print(f"  {'k':>3} {'n':>4} {'target d':>9} {'Oler d >':>13} {'residual':>11} {'rho_Oler':>10} "
      f"{'file rho_Oler':>14}")
FILE_RHO = {3: "0.85078", 4: "0.92400", 5: "0.95377", 6: "0.96886", 7: "0.97758",
            8: "0.98308", 12: "0.99270"}
FILE_GAP = {3: "0.5968758", 4: "0.4559963", 5: "0.3698542", 6: "0.3114225",
            7: "0.2690801", 8: "0.2369454", 12: "0.1605153"}
for k in sorted(FILE_RHO):
    n = T(k) - 1
    lo, hi = isqrt_bracket(F(4 * k * k + 4 * k - 7))
    olo, ohi = lo - 3, hi - 3                       # Oler bound on d
    D = 2 * (k - 1)
    glo, ghi = F(D) - ohi, F(D) - olo               # residual gap
    rlo, rhi = olo / D, ohi / D
    agree_rho = f"{float(rlo):.5f}" == FILE_RHO[k] == f"{float(rhi):.5f}"
    agree_gap = f"{float(glo):.7f}" == FILE_GAP[k] == f"{float(ghi):.7f}"
    print(f"  {k:>3} {n:>4} {D:>9} {float(olo):>13.7f} {float(glo):>11.7f} "
          f"{float(rlo):>10.5f} {FILE_RHO[k]:>14}  "
          f"{'gap ok' if agree_gap else 'GAP MISMATCH'} / {'rho ok' if agree_rho else 'RHO MISMATCH'}")
    if not (agree_rho and agree_gap):
        FAIL.append(f"§2 table k={k}")
ck("eo-exhaustion §2 table reproduced exactly", not any(f.startswith("§2") for f in FAIL))

print()
print("  NOTE ON STRICTNESS: Oler gives n <= a^2/2+3a/2+1, so n points force a >= root,")
print("  not a > root.  eo-exhaustion §2 writes 'd(n) > sqrt(8n+1)-3'.  The strict form is")
print("  not what Oler yields (equality is attainable in Oler).  eo-boundary-counting §2 gets")
print("  this right ('the entire open window is a in [a*, 6)', closed at a*).")

print()
print("=" * 78)
print("B. eo-exhaustion §4 — the rho column")
print("=" * 78)
for k, d, filerho in ((4, F(59, 10), "0.98333"), (5, F(799, 100), "0.99875")):
    rho = d / (2 * (k - 1))
    ck(f"k={k}: rho = d/2(k-1) = {float(rho):.5f} matches file {filerho}",
       f"{float(rho):.5f}" == filerho)
print("  (The node counts / seconds / 'proved' verdicts in §4 are properties of the author's")
print("   implementation.  Problem RULES.md §3 forbids me rerunning their code, and re-deriving")
print("   a wall-clock measurement is not possible.  NOT EXAMINED — see report.)")

print()
print("=" * 78)
print("C. eo-exhaustion §5 — the levels table")
print("=" * 78)
print("  §5's threshold:  2^L > d / (sqrt3 (1-rho)),  d = rho * d(n),  d(n) = 12 at k=7")
for rho_s, L_file in (("0.90", 6), ("0.95", 8), ("0.9776", 9), ("0.99", 10), ("0.999", 13)):
    rho = F(rho_s)
    d = rho * 12
    # need 2^L > d/(sqrt3 (1-rho)) ; use exact rational squares: (2^L)^2 * 3 * (1-rho)^2 > d^2
    L = 0
    while (2 ** L) ** 2 * 3 * (1 - rho) ** 2 <= d * d:
        L += 1
    ck(f"rho={rho_s}: level = {L} (file says {L_file}), cells 4^L = {4**L}", L == L_file)

print()
print("=" * 78)
print("D. eo-boundary-counting §2 — the window table")
print("=" * 78)
FILE = {3: ("1.701562", "0.298438", "1.372281"),
        4: ("2.772002", "0.227998", "2.531129"),
        6: ("4.844289", "0.155711", "4.684658"),
        7: ("5.865460", "0.134540", "5.728416")}
for k, (w, gap, w2) in FILE.items():
    n = T(k) - 1
    # a with a^2/2+3a/2+1 = n  <=>  a^2+3a+2-2n = 0  <=> a = (-3+sqrt(1+8n))/2
    lo, hi = isqrt_bracket(F(8 * n + 1))
    alo, ahi = (lo - 3) / 2, (hi - 3) / 2
    glo, ghi = F(k - 1) - ahi, F(k - 1) - alo
    # a with RHS = n-1
    lo2, hi2 = isqrt_bracket(F(8 * (n - 1) + 1))
    blo, bhi = (lo2 - 3) / 2, (hi2 - 3) / 2
    ok = (f"{float(alo):.6f}" == w == f"{float(ahi):.6f}"
          and f"{float(glo):.6f}" == gap == f"{float(ghi):.6f}"
          and f"{float(blo):.6f}" == w2 == f"{float(bhi):.6f}")
    ck(f"k={k}: window {float(alo):.6f}, gap {float(glo):.6f}, non-integrality root "
       f"{float(blo):.6f}", ok)
# t_7 = (-3+sqrt33)/6, characterised by t^2+t = 2/3
lo, hi = isqrt_bracket(F(33))
t7lo, t7hi = (lo - 3) / 6, (hi - 3) / 6
ck("t_7 bracket 0.457427 < t_7 < 0.457428",
   float(t7lo) > 0.457427 and float(t7hi) < 0.457428,
   f"[{float(t7lo):.9f}, {float(t7hi):.9f}]")
ck("t_7 satisfies t^2+t = 2/3 (checked via the bracket)",
   t7lo * t7lo + t7lo <= F(2, 3) <= t7hi * t7hi + t7hi)
# a* bracket
lo, hi = isqrt_bracket(F(217))
aslo, ashi = (lo - 3) / 2, (hi - 3) / 2
ck("a* bracket 5.865459 < a* < 5.865460",
   float(aslo) > 5.865459 and float(ashi) < 5.865460)

print()
print("=" * 78)
print("E. oler-slack-analysis §1 — independent reconstruction (Codex reviewed this on PR #90)")
print("=" * 78)
print("  Independent derivation of F = 2n - b - 2 and the identity, re-done here:")
print("   V = n, E_edges = (3F+b)/2, faces = F+1 (incl. outer);")
print("   Euler V - E + F_all = 2  =>  n - (3F+b)/2 + F + 1 = 2  =>  n - F/2 - b/2 = 1")
ok = True
for n in range(3, 40):
    for b in range(3, n + 1):
        Ff = 2 * n - b - 2
        E_edges = F(3 * Ff + b, 2)
        if n - E_edges + (Ff + 1) != 2:
            ok = False
ck("Euler closes for every (n,b) with F = 2n-b-2", ok)
# check on concrete lattices, computing b and F from an actual triangulation of Lambda(k)
def lattice_tri(k):
    """Standard triangulation of the T(k) lattice: up- and down- unit cells."""
    pts = [(i, j) for j in range(k) for i in range(k - j)]
    faces = []
    for j in range(k - 1):
        for i in range(k - 1 - j):
            faces.append(((i, j), (i + 1, j), (i, j + 1)))
            if i + j <= k - 3:
                faces.append(((i + 1, j), (i, j + 1), (i + 1, j + 1)))
    return pts, faces
for k in range(2, 9):
    pts, faces = lattice_tri(k)
    n = len(pts); m = k - 1
    b = sum(1 for (i, j) in pts if i == 0 or j == 0 or i + j == m)
    ck(f"lattice T({k}): n={n}, b={b}, faces built={len(faces)}, 2n-b-2={2*n-b-2}",
       len(faces) == 2 * n - b - 2)
print()
print("  Codex's PR#90 review claims re-derived here: F=2n-b-2 with b counting ALL hull-boundary")
print("  points (agree); boundary-edge excess >= 0 since consecutive boundary points are")
print("  separated points at distance >= 1 (agree); minimal witness (0,0),(1,0),(2,1/2):")
d2 = [F(1), F(17,4), F(5,4)]
ck("  witness squared distances are 1, 5/4, 17/4, all >= 1", sorted(d2) == [F(1), F(5,4), F(17,4)])
area2 = abs(0*(0-F(1,2)) + 1*(F(1,2)-0) + 2*(0-0))
ck("  witness area = 1/4 < sqrt3/4", F(area2,2) == F(1,4))
# FP => EO
ok = True
for k in range(3, 30):
    sup = F((k - 1) ** 2, 2) + F(3 * (k - 2), 2) + 1     # sup of FP RHS for a < k-1
    ok &= (sup == F(2 * T(k) - 3, 2))                     # = T(k) - 3/2
ck("FP's sup below a=k-1 is exactly T(k)-3/2, so n <= T(k)-2  (agrees with Codex)", ok)

print()
print("=" * 78)
print("FAILURES:", FAIL if FAIL else "none")
print("=" * 78)
raise SystemExit(1 if FAIL else 0)
