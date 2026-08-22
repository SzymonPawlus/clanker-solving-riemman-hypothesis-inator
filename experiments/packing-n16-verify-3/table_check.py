"""Task (b) and (f): the reduction s(n) = 2 a_n + 2 sqrt3, and the a_n table.

Derivation, reconstructed from problems/circle-packing-equilateral-triangle/README.md
without reading any attack file:

  * A unit circle inside an equilateral triangle of side s has its centre at
    distance >= 1 from each of the three sides; the locus of such centres is the
    inner-parallel equilateral triangle.  Moving each side inward by 1 shortens
    the side by 1/tan(30 deg) = sqrt3 at each end, so the inner triangle has
    side  d = s - 2 sqrt3.  Two unit circles are non-overlapping iff their
    centres are >= 2 apart.  Hence
          s(n) = 2 sqrt3 + d(n),   d(n) = min side holding n points, sep >= 2.
  * a_n is defined with separation 1.  x -> 2x is a similarity carrying a
    separation-1 configuration in T_a to a separation-2 configuration in T_{2a}
    and back, so  d(n) = 2 a_n  and therefore

          s(n) = 2 a_n + 2 sqrt3          <-- THE identity under audit

  This is the separation-1 / separation-2 step that FINDINGS.md records as the
  standing trap on this problem, so it is done in one direction only, explicitly.
"""
from fractions import Fraction as F
from surd import S, s as sv

TWO_R3 = sv(r3=2)

# s(n) exactly as printed in the problem README's "proven optimal" table.
S_TABLE = {
    1:  sv(r3=2),
    2:  sv(**{"1": 2, "r3": 2}),
    3:  sv(**{"1": 2, "r3": 2}),
    4:  sv(r3=4),
    5:  sv(**{"1": 4, "r3": 2}),
    6:  sv(**{"1": 4, "r3": 2}),
    7:  sv(**{"1": 2, "r3": 4}),
    8:  sv(**{"1": 2, "r3": 2, "r33": F(2, 3)}),
    9:  sv(**{"1": 6, "r3": 2}),
    10: sv(**{"1": 6, "r3": 2}),
    11: sv(**{"1": 4, "r3": 2, "r6": F(4, 3)}),
    12: sv(**{"1": 4, "r3": 4}),
    13: sv(**{"1": 4, "r6": F(2, 3), "r3": F(10, 3)}),
    14: sv(**{"1": 8, "r3": 2}),
    15: sv(**{"1": 8, "r3": 2}),
}

# The a_n list the n=16 campaign uses as capacity inputs, transcribed from the
# dispatch brief.  Re-derived below, NOT trusted.
A_CLAIMED = {
    1:  sv(),
    2:  sv(**{"1": 1}),
    3:  sv(**{"1": 1}),
    4:  sv(r3=1),
    5:  sv(**{"1": 2}),
    6:  sv(**{"1": 2}),
    7:  sv(**{"1": 1, "r3": 1}),
    8:  sv(**{"1": 1, "r33": F(1, 3)}),
    9:  sv(**{"1": 3}),
    10: sv(**{"1": 3}),
    11: sv(**{"1": 2, "r6": F(2, 3)}),
    12: sv(**{"1": 2, "r3": 1}),
    13: None,          # brief gives a decimal only: 3.971197119
    14: sv(**{"1": 4}),
    15: sv(**{"1": 4}),
}

print("Identity under audit:  s(n) = 2*a_n + 2*sqrt3,  i.e. a_n = (s(n) - 2 sqrt3)/2")
print()
print(f"{'n':>3} {'s(n) (README)':>34} {'a_n = (s-2r3)/2':>34} {'brief':>8}")
bad = []
for n in range(1, 16):
    a = (S_TABLE[n] - TWO_R3).scale(F(1, 2))
    claim = A_CLAIMED[n]
    if claim is None:
        # only a decimal was supplied; check it to the printed precision
        ok = abs(float(a) - 3.971197119) < 5e-10
        mark = "dec ok" if ok else "DEC BAD"
    else:
        ok = (a == claim)
        mark = "ok" if ok else "MISMATCH"
    if not ok:
        bad.append(n)
    print(f"{n:>3} {repr(S_TABLE[n]):>34} {repr(a):>34} {mark:>8}   "
          f"(a_{n} = {float(a):.9f})")

print()
# n = 16: the conversion the standing record makes
a16 = sv(**{"1": 1, "r3": 2})              # 1 + 2 sqrt3
s16 = a16.scale(2) + TWO_R3
target = sv(**{"1": 2, "r3": 6})           # 2 + 6 sqrt3
print(f"a_16 >= {a16} = {float(a16):.15f}")
print(f"  => s(16) >= 2*a_16 + 2 sqrt3 = {s16} = {float(s16):.15f}")
print(f"  claimed 2 + 6 sqrt3          = {target} = {float(target):.15f}")
print(f"  conversion exact match: {s16 == target}")

# the trap: what the wrong (separation-confusing) conversion would have given
wrong = a16 + TWO_R3
print(f"  [trap check] the separation-1/2 slip s = a + 2 sqrt3 would give "
      f"{float(wrong):.9f}, which is NOT what the attack claims -- good.")

# sanity: known packing upper bound for n=16 in a-units
print()
print(f"  Melissen-Schuur s(16) <= 12.713629  =>  a_16 <= "
      f"{(12.713629 - 2 * 3 ** .5) / 2:.7f}   (bound must lie below this)")
print(f"  1 + 2 sqrt3 = {float(a16):.7f} < that: consistent")

print()
print("TABLE VERDICT:", "all rows reproduce" if not bad else f"MISMATCHES at n={bad}")
