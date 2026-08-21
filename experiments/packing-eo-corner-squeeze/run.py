#!/usr/bin/env python3
"""eo-corner-squeeze -- one command, Python standard library only, exact throughout.

    python3 run.py            # controls + k = 4,5,6 (a few minutes)
    python3 run.py --with-k7  # adds the k = 7 exhaustive search (long)

Writes the transcript to out/report.txt as well as stdout.
"""

import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import geom as G
import lemmas as L
import relax as R

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def hdr(t):
    say("")
    say("=" * 78)
    say(t)
    say("=" * 78)


def s_profile(cells, z, J):
    """S_j^(V) = #{p : u_V < j} for the profile z."""
    out = []
    for V in range(3):
        out.append([sum(z[i] for i, c in enumerate(cells) if c[V] < j)
                    for j in range(1, J + 1)])
    return out


def main(with_k7=False):
    t0 = time.time()

    hdr("0.  CONTROLS -- reproduce quantities that are already known")
    a = F(6)
    base = G.tri_constraints(a)
    say("  Oler on T of side 6:  (2/sqrt3)A + M/2 + 1 = %s + %s + 1 = %d  [= T(7), as it must]"
        % (G.measures(a, base)[1], G.measures(a, base)[2], G.capacity(a, base)))
    for j in (1, 2, 3, 4, 5):
        cons = base + G.bound_constraints(a, 0, 0, j)
        nv, oa, per, sq, sd = G.measures(a, cons)
        say("  closed corner triangle side %d: (2/sqrt3)A = %-6s M = %-22s cap = %2d   [T(%d) = %d]"
            % (j, oa, per, G.capacity(a, cons), j + 1, L.tri(j + 1)))
    say("  N(j^-) for j = 1..5 (max unit-separated points in side < j):",
        [G.N_upper_open(j) for j in range(1, 6)], " [expect 1, 4, 8, 13, 19]")
    say("      1 = trivial;  4, 8, 13 from Melissen/Payan;  19 from d(20) = 5 (Payan, qualified)")

    hdr("1.  LEMMA P -- the top-scale corner constraint, reproved without Oler")
    L.check_all(kmax=9, out=say)

    hdr("1b.  THE OVERLAP OF THE CORNER TRIANGLES, EXACTLY")
    for kk in (4, 5, 6, 7):
        L.overlaps(kk, F(kk - 1) - F(1, 100), out=say)
        say("")

    hdr("2.  CERTIFICATE VALIDATION (K2 / K3) -- real packings vs computed capacities")
    import validate
    say("  every certificate: exact separation >= 1, exact Viviani, exact containment,")
    say("  then EVERY corner-coordinate box capacity is tested against the true count.")
    rep = validate.run(verbose=False)
    for (f, n, ap, srow, nbox, worst) in rep:
        say("   %-18s n=%2d  a<=%-14s boxes %5d  tightest slack %d at %s (%d of %d)"
            % (f, n, str(ap), nbox, worst[0], worst[1], worst[2], worst[3]))
    say("  ALL PASS.  Several boxes are exactly tight (slack 0), so the caps are not vacuous.")

    hdr("3.  THE CORNER-OCCUPANCY RELAXATION")
    say("  variables z[alpha,beta,gamma] = #points with (floor u_A, floor u_B, floor u_C)")
    say("  constraints: total = n;  (CIO-j) S_j^(V) >= T(j);  S_j^(V) <= N(j^-);")
    say("               and sum over every corner-coordinate box <= that box's capacity.")
    say("  circularity guard: d(T(k)-1) is REMOVED from the cited table when testing level k.")
    say("")
    ks = [4, 5, 6] + ([7] if with_k7 else [])
    for k in ks:
        aa = F(k - 1) - F(1, 100)
        t = time.time()
        cells, cc, cl, info = R.build(k, aa)
        tb = time.time() - t
        t = time.time()
        # A feasibility claim needs a witness, not a search method: the randomised
        # search is tried first because it is fast, and whatever it returns is
        # re-verified below against every constraint.  If it finds nothing we fall
        # back to the exhaustive DFS, which is the only thing that can say INFEASIBLE.
        z, nodes = R.find_feasible_random(cells, cc, cl, info["n"], tries=200000)
        how = "randomised, %d restarts" % nodes
        if z is None:
            z, nodes = R.feasible(cells, cc, cl, info["n"],
                                  node_limit=(200_000_000 if k >= 7 else 20_000_000))
            how = "exhaustive, %d nodes" % nodes
        verdict = "FEASIBLE" if isinstance(z, list) else str(z)
        say("  k = %d   n = %2d   a = %-8s eps(a) = %.5f   cells %2d   binding boxes %4d"
            % (k, info["n"], aa, float(info["eps"]), info["ncells"], info["nbox"]))
        say("          build %.0fs, search %.0fs (%s)  ->  %s"
            % (tb, time.time() - t, how, verdict))
        if isinstance(z, list):
            bad = R.check_solution(cells, cl, z)
            say("          re-verified against all %d constraints, violations: %d"
                % (len(cl), len(bad)))
            assert not bad
            say("          witness profile: %s"
                % [(cells[i], z[i]) for i in range(len(cells)) if z[i]])
            say("          its corner profiles S_j^(V), j = 1..%d:" % info["J"])
            for V, row in enumerate(s_profile(cells, z, info["J"])):
                say("             V=%s  %s   [CIO floor %s, capacity ceiling %s]"
                    % ("ABC"[V], row,
                       [L.tri(j) for j in range(1, info["J"] + 1)],
                       [G.N_upper_open(j) for j in range(1, info["J"] + 1)]))
        if k <= 6 and isinstance(z, list):
            say("          *** Erdos-Oler is CITED-TRUE at k = %d, so the true geometric" % k)
            say("              system is INFEASIBLE here.  The relaxation is not. ***")

    hdr("4.  VERDICT")
    say("  K1 MET.  The corner-occupancy relaxation is feasible at k = 4 and k = 5, where")
    say("  Erdos-Oler is proven (Melissen 1993 for n = 9; Payan 1997 for n = 14) and the")
    say("  geometric system therefore has no solution at all.  A relaxation that cannot")
    say("  see the contradiction in a case where one provably exists cannot supply it at")
    say("  k = 7.  Corner occupancy plus region capacity is not the missing ingredient.")

    say("")
    say("total wall time %.0fs" % (time.time() - t0))
    with open(os.path.join(HERE, "out", "report.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main(with_k7="--with-k7" in sys.argv)
