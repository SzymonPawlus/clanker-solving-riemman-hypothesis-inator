"""The SEAM-DEPTH DEGREE OF FREEDOM, made explicit.

famcert's KILL-CRITERION records that the authoring worker's FIRST n = 49
transcription was infeasible "due to a seam-depth degree of freedom".  The
construction fixes the four grain offsets

    BL (0,0)   BR (2,0)   C (1,1)   T (1,3)

in the normal form p = (x + a sqrt3, b + r sqrt3).  BL and BR are pinned by the
two bottom corners.  The remaining freedom is the pair (a,b) for the centre grain
C and for the top grain T -- how deep each sinks into the notch below it.  This
file scans that freedom exhaustively over a box and reports which choices give a
feasible, contained, tight packing.

Exact arithmetic; every verdict comes from checker.py.
"""
import sys
from q3 import E
import gen, checker

BOXA = range(0, 3)
BOXB = range(0, 7)


def try_offset(j, ac, bc, at, bt):
    off = {"BL": (0, 0), "BR": (2, 0), "C": (ac, bc), "T": (at, bt)}
    pts = gen.points(j, off)
    n = gen.n_of(j)
    if len(set(pts)) != n:
        return {"ok": False, "tight": False, "why": "duplicate"}
    rep = checker.check(n, gen.s_of(j), pts)
    return rep


def main(js=(6, 7, 8)):
    print("Scanning the seam-depth freedom: C offset (a,b) and T offset (a,b),")
    print("a in %s, b in %s -- %d combinations per j." %
          (list(BOXA), list(BOXB), (len(BOXA) * len(BOXB)) ** 2))
    for j in js:
        good = []
        feas_only = []
        for ac in BOXA:
            for bc in BOXB:
                for at in BOXA:
                    for bt in BOXB:
                        rep = try_offset(j, ac, bc, at, bt)
                        if rep["ok"] and rep.get("tight"):
                            good.append((ac, bc, at, bt))
                        elif rep["ok"]:
                            feas_only.append((ac, bc, at, bt))
        print("  j = %-2d (n = %3d):  feasible AND tight: %s" % (j, gen.n_of(j), good))
        print("                     feasible but NOT tight (honest but slack upper bound): %s"
              % (feas_only if len(feas_only) < 12 else "%d choices" % len(feas_only)))
    print()
    print("Nearest misses at j = 7 (n = 49), the transcription that failed in r4-famcert:")
    for (ac, bc, at, bt) in [(1, 1, 1, 3), (1, 0, 1, 3), (1, 2, 1, 3), (1, 1, 1, 2),
                             (1, 1, 1, 4), (0, 1, 1, 3), (2, 1, 1, 3), (1, 1, 0, 3)]:
        rep = try_offset(7, ac, bc, at, bt)
        f = rep.get("failures", [])
        print("   C=(%d,%d) T=(%d,%d) -> ok=%-5s tight=%-5s  %s"
              % (ac, bc, at, bt, rep["ok"], rep.get("tight"),
                 ("first failures: " + str(f[:2])) if f else "d_min = " + rep.get("d_min_exact", "?")))


if __name__ == "__main__":
    main()
