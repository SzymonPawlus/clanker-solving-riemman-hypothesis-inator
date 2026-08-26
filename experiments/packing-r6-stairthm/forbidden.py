"""Step 1 of the theorem: the FORBIDDEN DIFFERENCE VECTORS, exactly and once.

In the normal form  p = (x + a sqrt3, b + r sqrt3),  a pair of points with
grain-offset difference (da, db) and lattice difference (dx, dr) has

    D2(dx,dr; da,db) = (dx^2 + 3 da^2 + db^2 + 3 dr^2) + 2 sqrt3 (dx da + db dr)

which is EXACT and contains no j.  So for each of the ten ordered grain pairs
(including the four same-grain ones) the set

    F(g1,g2) = { (dx,dr) in Z^2 : dx = dr (mod 2), D2 < 4 }

is a fixed finite set, computable once, valid for every j.  The configuration is
feasible for a given j iff no ordered pair of its points realises a member of the
corresponding F.

Bounding the search.  D2 >= P - 2 sqrt3 |Q| with P = dx^2+3da^2+db^2+3dr^2 and
|Q| = |dx da + db dr| <= |dx||da| + |db||dr|.  With |da| <= 2, |db| <= 3 this gives
D2 >= dx^2 + 3 dr^2 - 4 sqrt3 |dx| - 6 sqrt3 |dr| + (3 da^2 + db^2), so D2 >= 4 as
soon as |dx| >= 9 or |dr| >= 6.  We search |dx| <= 20, |dr| <= 20 -- far past that
-- and assert nothing is found on the border of the box.
"""
from q3 import E, SQ3
from gen import GRAINS, OFFSET

FOUR = E(4, 0)
BOX = 20


def D2(dx, dr, da, db):
    P = dx * dx + 3 * da * da + db * db + 3 * dr * dr
    Q = dx * da + db * dr
    return E(P, 2 * Q)


def forbidden(g1, g2):
    a1, b1 = OFFSET[g1]
    a2, b2 = OFFSET[g2]
    da, db = a1 - a2, b1 - b2
    out = []
    border = False
    for dx in range(-BOX, BOX + 1):
        for dr in range(-BOX, BOX + 1):
            if (dx - dr) % 2:
                continue
            if g1 == g2 and dx == 0 and dr == 0:
                continue          # same point, not a pair
            v = D2(dx, dr, da, db)
            if v < FOUR:
                out.append((dx, dr, v))
                if abs(dx) >= BOX - 2 or abs(dr) >= BOX - 2:
                    border = True
    assert not border, ("forbidden set touches the search box border", g1, g2)
    return sorted(out)


def all_forbidden():
    return {(g1, g2): forbidden(g1, g2) for g1 in GRAINS for g2 in GRAINS}


if __name__ == "__main__":
    F = all_forbidden()
    for (g1, g2), lst in sorted(F.items()):
        a1, b1 = OFFSET[g1]; a2, b2 = OFFSET[g2]
        print("%-2s - %-2s   (da,db) = (%2d,%2d)   |F| = %d" %
              (g1, g2, a1 - a2, b1 - b2, len(lst)))
        for (dx, dr, v) in lst:
            print("        (dx,dr) = (%2d,%2d)   D2 = %-18s  (~%.4f)" % (dx, dr, v.s(), v.f()))
        if not lst:
            print("        (empty -- no violating difference exists at all)")
