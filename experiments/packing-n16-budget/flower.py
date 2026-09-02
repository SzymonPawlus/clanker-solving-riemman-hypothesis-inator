"""Certified rational LOWER bounds on

    f(l) = sup{ area(S) : diam(S) <= 1, S subset {y >= 0}, (0,0) in S, (l,0) in S }.

A lower bound on f is what bounds what the AREA BUDGET can ever prove: the budget
inequality holds with the true f, so exhibiting admissible sets shows the budget
cannot be violated, hence gives a ceiling on the method.  Two explicit sets:

(D) THE CUT DISK.  Let r = 1/2 and c = (l/2, sqrt(1-l^2)/2).  Then |c-(0,0)| =
    |c-(l,0)| = sqrt(l^2 + 1 - l^2)/2 = 1/2, so both boundary points lie on the
    circle of radius r about c.  Put S = B(c,r) cap {y >= 0}.  diam S <= 2r = 1;
    S lies in the half-plane; both points are in S.  The centre is at height
    h = sqrt(1-l^2)/2 <= r above the line, so the part cut away is the circular
    segment of area r^2 arccos(h/r) - h sqrt(r^2 - h^2), and with h/r =
    sqrt(1-l^2), arccos(h/r) = arcsin(l), sqrt(r^2-h^2) = l/2:

        f(l) >= pi/4 - arcsin(l)/4 + l*sqrt(1-l^2)/4.

(L) THE LENS, VIA MONOTONICITY.  f is non-increasing on [0,1]: an admissible set
    for l' may be replaced by its convex hull (area up, diameter and half-plane
    preserved), and that hull contains (l,0) for every l <= l', so it is
    admissible for l as well; hence f(l) >= f(l') for l <= l'.  At l = 1 the set
    R = B((0,0),1) cap B((1,0),1) cap {y >= 0} is admissible: it is convex, and
    every point of its boundary is within 1 of C = (1/2, sqrt3/2) -- the two
    circular arcs subtend at most 60 degrees at their centres, which are at
    distance 1 from C, and the straight side has its maximum distance to C at an
    endpoint -- so R lies in the Reuleaux triangle ABC, of diameter 1.  Its area
    is half the lens of two unit circles at distance 1, i.e.

        f(l) >= f(1) >= pi/3 - sqrt3/4 = 0.6141848...   for every l <= 1.

Nothing here uses any packing, covering or literature value (K4/B4).
"""
from fractions import Fraction as F

from exact import PI_LO, PI_HI, SQRT3_HI, asin_hi, sqrt_lo

# f(1) >= pi/3 - sqrt3/4, rounded DOWN
LENS = PI_LO / 3 - SQRT3_HI / 4


def cut_disk(ell):
    """Area of (D), rounded DOWN: pi/4 - arcsin(l)/4 + l sqrt(1-l^2)/4."""
    ell = F(ell)
    assert 0 <= ell <= 1
    if ell == 1:                     # arcsin(1) = pi/2 exactly; the disk halves
        return PI_LO / 4 - PI_HI / 8
    return PI_LO / 4 - asin_hi(ell) / 4 + ell * sqrt_lo(1 - ell * ell) / 4


def f_lo(ell):
    """Best certified lower bound on f(ell) available here."""
    return max(cut_disk(ell), LENS)


if __name__ == "__main__":
    print(f"  lens value f(1) >= {float(LENS):.7f}")
    for num, den in ((0, 1), (13, 20), (8, 10), (85, 100), (9, 10), (95, 100), (1, 1)):
        ell = F(num, den)
        print(f"  f({float(ell):.4f}) >= {float(f_lo(ell)):.7f}"
              f"   [cut disk {float(cut_disk(ell)):.7f}, lens {float(LENS):.7f}]")
    # self-check: at l = 0 the cut disk is the half-disk of diameter 1 (pi/8)
    # plus nothing -- pi/4 - 0 + 0 = pi/4 is the WHOLE disk, correct since the
    # centre is then at height 1/2 = r and nothing is cut off.
    assert abs(float(cut_disk(F(0)) - PI_LO / 4)) < 1e-30
    # at l = 1 the centre is on the line and exactly half the disk survives
    assert abs(float(cut_disk(F(1)) - PI_LO / 8)) < 1e-6, float(cut_disk(F(1)))
    print("  self-tests passed (cut disk = pi/4 at l=0, pi/8 at l=1)")
