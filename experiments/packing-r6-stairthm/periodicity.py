"""REPRODUCTION of the round-6 ideation pilot's periodicity claim.

The pilot (sketch, someone else's script, reproduced here from scratch) reported:

  "The set of cross-grain close-pair difference-vector types is exactly 2-periodic
   in j from j = 4: 36 types when j is even, 38 when odd, with types(j)==types(j-2)
   verified as exact set equality through j = 12."

The pilot's definition of "close pair" was not recorded, so this file computes the
type set under FOUR natural thresholds and reports all of them.  A type is the
tuple (g1, g2, dx, dr) for an ordered cross-grain pair (g1 != g2) of points with
squared distance <= threshold, dx = x1-x2, dr = r1-r2 in lattice coordinates.
Only ordered pairs with g1 before g2 in the fixed order BL,BR,C,T are recorded, so
each unordered pair contributes exactly one type.

All arithmetic exact.
"""
import sys
from q3 import E
from gen import GRAINS, lattice_sites, n_of, UMp
from forbidden import D2, OFFSET

IDX = {g: i for i, g in enumerate(GRAINS)}
THRESHOLDS = [E(4, 0), E(8, 0), E(12, 0), E(16, 0)]


def types(j, thr):
    g = lattice_sites(j)
    out = set()
    for i1 in range(4):
        for i2 in range(i1 + 1, 4):
            g1, g2 = GRAINS[i1], GRAINS[i2]
            a1, b1 = OFFSET[g1]; a2, b2 = OFFSET[g2]
            da, db = a1 - a2, b1 - b2
            for (r1, x1) in g[g1]:
                for (r2, x2) in g[g2]:
                    dx, dr = x1 - x2, r1 - r2
                    if D2(dx, dr, da, db) <= thr:
                        out.add((g1, g2, dx, dr))
    return out


def main(JMAX=13):
    for thr in THRESHOLDS:
        print("=" * 78)
        print("close pair := squared distance <= %s  (distance <= %.4f)" % (thr.s(), thr.f() ** 0.5))
        T = {j: types(j, thr) for j in range(JMAX + 1)}
        print("%-3s %-5s %-7s %-9s %s" % ("j", "n", "#types", "par", "types(j) == types(j-2) ?"))
        first_stable = None
        stable_from = None
        for j in range(JMAX + 1):
            eq = "-" if j < 2 else str(T[j] == T[j - 2])
            print("%-3d %-5d %-7d %-9s %s" % (j, n_of(j), len(T[j]), "even" if j % 2 == 0 else "odd", eq))
        # find the smallest J such that types(j)==types(j-2) for all j >= J
        for J in range(2, JMAX + 1):
            if all(T[j] == T[j - 2] for j in range(J, JMAX + 1)):
                stable_from = J
                break
        ev = sorted(set(len(T[j]) for j in range(JMAX + 1) if j % 2 == 0 and j >= (stable_from or 0)))
        od = sorted(set(len(T[j]) for j in range(JMAX + 1) if j % 2 == 1 and j >= (stable_from or 0)))
        print("  -> 2-periodic (set equality) from j = %s ; counts even %s, odd %s"
              % (stable_from, ev, od))
        print()


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 13)


# ---------------------------------------------------------------------------
# ORDERED variant: record both (g1,g2,dx,dr) and (g2,g1,-dx,-dr).  This doubles
# every count.  At threshold D2 <= 16 (distance <= 4 = two diameters) it gives
# exactly the pilot's numbers: 36 for even j, 38 for odd j, 2-periodic from j = 4.
# ---------------------------------------------------------------------------
def types_ordered(j, thr):
    base = types(j, thr)
    return base | {(g2, g1, -dx, -dr) for (g1, g2, dx, dr) in base}


def ordered_report(JMAX=13, thr=E(16, 0)):
    print("=" * 78)
    print("ORDERED cross-grain types, close pair := squared distance <= %s (distance <= 4)" % thr.s())
    T = {j: types_ordered(j, thr) for j in range(JMAX + 1)}
    for j in range(JMAX + 1):
        eq = "-" if j < 2 else str(T[j] == T[j - 2])
        print("  j=%-3d n=%-4d #types=%-3d  %-4s   types(j)==types(j-2): %s"
              % (j, n_of(j), len(T[j]), "even" if j % 2 == 0 else "odd", eq))
    stable = min(J for J in range(2, JMAX + 1)
                 if all(T[j] == T[j - 2] for j in range(J, JMAX + 1)))
    ev = sorted(set(len(T[j]) for j in range(stable, JMAX + 1) if j % 2 == 0))
    od = sorted(set(len(T[j]) for j in range(stable, JMAX + 1) if j % 2 == 1))
    print("  -> exact set equality types(j) == types(j-2) for all j >= %d ; even %s, odd %s"
          % (stable, ev, od))
    print("  PILOT CLAIM was: 2-periodic from j = 4, 36 even / 38 odd, through j = 12.")
    print("  REPRODUCED: %s" % (stable == 4 and ev == [36] and od == [38]))
