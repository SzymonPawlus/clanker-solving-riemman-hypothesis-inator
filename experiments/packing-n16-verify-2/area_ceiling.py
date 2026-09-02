#!/usr/bin/env python3
"""
D1: KILL-CRITERION.md K4's area ceiling  a <~ 4.5603  is not a theorem, and the
per-piece cap it rests on is false.

K4 (attacks/n16-covering/KILL-CRITERION.md) asserts:

    "A piece of diameter <1 has area < 3 sqrt3 / 8 *if* the hexagonal bound is the
     truth (it is asserted, not cited, in eo-covering-construct sec.5.3), and the
     corner pieces have area <= pi/6 (proved).  With 3 corner + E >= 9 edge +
     interior pieces this caps
         sqrt3/4 a^2 <= 3*(pi/6) + 9*0.6095 + 3*(3 sqrt3/8),  i.e.  a <~ 4.5603."

Two separate problems.

(1) THE CAP IS FALSE, not merely uncited.  3 sqrt3/8 = 0.6495190 is the area of
    the REGULAR HEXAGON of diameter 1.  The isodiametric inequality says the
    maximiser of area among planar sets of diameter 1 is the DISK, area pi/4 =
    0.7853982 -- 21% larger, and convex.  Even among hexagons the regular one is
    not the maximiser: Graham's "largest small hexagon" (Graham 1975, J. Combin.
    Theory Ser. A 18, 165-170) has area 0.6749814, 3.9% larger.

(2) EVEN AS AN INEQUALITY THE CENSUS IS ASSUMED.  "3 corner + 9 edge + 3 interior"
    is a guess at the piece census, not a derived constraint.  The real
    certificate has 15 pieces with vertex counts [6,6,6,5,5,5,5,5,4,4,5,5,5,5,4]
    -- so 'edge' and 'interior' are not even well-defined categories for it.

Replacing the cap with the isodiametric bound (a theorem) and keeping K4's own
PROVED corner bound (a piece containing a 60-degree vertex of T_a and of diameter
<= 1 lies in a 60-degree sector of radius 1, so its area is at most pi/6):

    sqrt3/4 a^2 <= 3*(pi/6) + 12*(pi/4)   =>   a <= 5.0391657

which is ABOVE the packing ceiling 4.6247636 and therefore says nothing.

CONCLUSION.  There is no rigorous area-based ceiling on the 15-piece covering
method below the packing ceiling.  a* > 4.5603 contradicts nothing that has been
proved, and a certificate must not be discarded for exceeding K4.
"""

import math

S3 = math.sqrt(3)
PI = math.pi

HEX_REG = 3 * S3 / 8            # regular hexagon of diameter 1
DISK = PI / 4                   # isodiametric maximiser, diameter 1
GRAHAM_HEX = 0.674981099846     # Graham 1975, largest small hexagon
CORNER = PI / 6                 # 60-degree sector of radius 1  (K4's proved bound)
CEILING = 4.6247636             # Melissen-Schuur / Graham-Lubachevsky 16-point packing


def a_from_area(total):
    """largest a with area(T_a) = sqrt3/4 a^2 <= total."""
    return math.sqrt(total / (S3 / 4))


print("=" * 74)
print("D1  --  K4's area ceiling")
print("=" * 74)

print("\n(1) the per-piece cap, for convex sets of diameter 1")
rows = [
    ("regular hexagon, circumradius 1/2  (K4's cap)", HEX_REG),
    ("Graham 1975 largest small hexagon", GRAHAM_HEX),
    ("the DISK -- isodiametric maximiser", DISK),
]
for name, v in rows:
    rel = "" if v == HEX_REG else "   (%+.1f%% vs the cap)" % (100 * (v / HEX_REG - 1))
    print("    %-46s %.7f%s" % (name, v, rel))
assert DISK > HEX_REG and GRAHAM_HEX > HEX_REG
print("    => K4's cap 3sqrt3/8 is FALSE for convex sets of diameter 1,")
print("       and false even if pieces are restricted to hexagons.")

print("\n(2) K4's own arithmetic, reproduced")
k4 = 3 * CORNER + 9 * 0.6095 + 3 * HEX_REG
print("    3*(pi/6) + 9*0.6095 + 3*(3sqrt3/8) = %.9f" % k4)
print("    a <= %.7f          (K4 reports 4.5603 -- reproduces)" % a_from_area(k4))

print("\n(3) rigorous replacement: isodiametric everywhere, K4's proved corner bound")
rig = 3 * CORNER + 12 * DISK
print("    3*(pi/6) + 12*(pi/4)               = %.9f" % rig)
print("    a <= %.7f" % a_from_area(rig))
crude = 15 * DISK
print("    (crudest form, 15*(pi/4)           = %.9f -> a <= %.7f)"
      % (crude, a_from_area(crude)))

print("\n(4) is any of it binding?")
for label, v in (("K4 as written", a_from_area(k4)),
                 ("rigorous, with corner bound", a_from_area(rig)),
                 ("rigorous, crude", a_from_area(crude))):
    binds = v < CEILING
    print("    %-30s a <= %.7f   vs packing ceiling %.7f  -> %s"
          % (label, v, CEILING, "BINDS" if binds else "vacuous"))

print("\n" + "=" * 74)
print("VERDICT: the only rigorous area ceilings (5.0392, 5.2160) both sit ABOVE")
print("         the packing ceiling 4.6247636, so they are vacuous.  K4's 4.5603")
print("         is NOT a theorem and must not be used as a tripwire: a certified")
print("         a* in (4.5603, 4.6248) contradicts nothing that has been proved.")
print("=" * 74)
