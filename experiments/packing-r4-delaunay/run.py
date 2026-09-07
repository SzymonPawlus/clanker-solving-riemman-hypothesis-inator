#!/usr/bin/env python3
"""Round-4 proposal AB: does a NONLINEAR Euler-localised score on the Delaunay
triangulation beat Oler's inequality at n = 16, 17, 18?

Single reproduce command:      python3 run.py
(writes the same transcript to out/report.txt)

Everything printed is `numerical`.  An LP optimum from a float solver is not a
bound; see the attack README for what is and is not claimed.

Order of business, and the order is the point:
  STEP 0  self-checks of the exact configuration library (Euler, tiling,
          separation), plus reproduction of the merged oler-slack-analysis atlas
  STEP 1  THE CONTROL: recover Oler, d(n) >= sqrt(8n+1) - 3, as the linear
          member of the family.  If this fails nothing after it means anything.
  STEP 2  the reduced LP (2 variables) at n = 16, 17, 18, over three library
          refinements
  STEP 3  the full LP: one free score value per face shape -- the actual
          nonlinearity test
  STEP 4  verdict against the kill-criterion
"""

import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Importable when run as `python3 experiments/packing-r4-delaunay/run.py` from the
# repo root (the documented command), where cwd is NOT this directory.
sys.path.insert(0, HERE)

import _deps

_deps.require()   # fail fast with an actionable message, before `import lp` pulls
                  # in numpy/scipy and raises a bare ModuleNotFoundError traceback

import framework as fw
import lp as LP

OUT = io.StringIO()


def say(*args):
    line = " ".join(str(a) for a in args)
    print(line)
    OUT.write(line + "\n")


SQRT3 = math.sqrt(3.0)


def step0():
    say("=" * 78)
    say("STEP 0 -- exact self-checks on the configuration library")
    say("=" * 78)
    say("Each Config asserts, exactly: min separation >= 1; Euler F = 2n-b-2;")
    say("face areas tile conv(E).  Construction below therefore IS the check.")
    cfgs = fw.library(size=6)
    say(f"built {len(cfgs)} configurations, all checks passed")
    say("")
    say("Cross-check against the merged attacks/oler-slack-analysis atlas")
    say("(face excess / boundary-edge excess of the Oler linear member):")
    say(f"{'configuration':<26}{'n':>4}{'b':>4}{'F':>5}"
        f"{'face exc':>12}{'edge exc':>12}{'Oler slack':>12}")
    probe = [fw.cfg_lattice(1), fw.cfg_lattice(2), fw.cfg_lattice(3),
             fw.cfg_lattice(4), fw.cfg_lattice(5),
             fw.cfg_lattice_minus_apex(3), fw.cfg_lattice_minus_apex(4),
             fw.cfg_lattice_minus_apex(5), fw.cfg_corners_centroid(),
             fw.cfg_flat_arc(3), fw.cfg_flat_arc(4), fw.cfg_flat_arc(6),
             fw.cfg_flat_arc(8), fw.cfg_flat_arc(12), fw.cfg_flat_arc(16)]
    for c in probe:
        s = c.summary()
        say(f"{s['name']:<26}{s['n']:>4}{s['b']:>4}{s['F']:>5}"
            f"{s['face_excess']:>12.7f}{s['edge_excess_up']:>12.7f}"
            f"{s['oler_slack_up']:>12.7f}")
    say("")
    say("Expected from the merged atlas (attacks/oler-slack-analysis README):")
    say("  lattices and lattice-minus-apex: face exc = edge exc = 0 exactly;")
    say("  n=4 corners+centroid: 0 and 1.0980762;")
    say("  flat arcs m=3,4,6,8,12,16: face exc -0.8289333, -1.3195780,")
    say("  -2.3128957, -3.3105569, -5.3088864, -7.3083017 and Oler slack")
    say("  0.1738065, 0.1816421, 0.1874793, 0.1896033, 0.1911615, 0.1917186.")
    say("Agreement here is an independent reconstruction, not a rerun: this")
    say("directory shares no code with experiments/packing-oler-slack.")
    return cfgs


def step1(cfgs):
    say("")
    say("=" * 78)
    say("STEP 1 -- THE CONTROL.  Recover Oler as the linear member.")
    say("=" * 78)
    say("Member:  sigma(f) = (2/sqrt3) area(f) - 1/2,  tau(l) = (l-1)/2,")
    say("         c_A = 2/sqrt3,  c_L = 1/2.")
    say("")
    say("(1a) (D) holds with equality by definition of this member.")
    say("(1b) (V) on every library configuration -- sum sigma + sum tau >= 0:")
    worst, worst_name = None, None
    for c in cfgs:
        fe, be = c.oler_terms()
        tot = fw.kfloat(fe) + float(be)
        if worst is None or tot < worst:
            worst, worst_name = tot, c.name
    say(f"     min over {len(cfgs)} configurations = {worst:.10f}"
        f"   (at {worst_name})")
    ok_v = worst >= -1e-12
    say(f"     (V) satisfied on the whole library: {ok_v}")
    say("     [(V) in general is exactly Oler's inequality, `cited`; the")
    say("      library check is a consistency test of THIS framework, not a")
    say("      proof of Oler.]")
    say("")
    say("(1c) the telescoped bound B(a) = 1 + c_A(sqrt3/4)a^2 + 3 c_L a")
    say("     must equal Oler's 1 + a^2/2 + 3a/2, and the threshold in d must")
    say("     equal sqrt(8n+1) - 3.")

    def oler_bound(a):
        return 1.0 + (2.0 / SQRT3) * (SQRT3 / 4.0) * a * a + 3.0 * 0.5 * a

    say(f"     {'n':>4}{'d from framework':>22}{'sqrt(8n+1)-3':>18}"
        f"{'abs diff':>14}")
    ok_c = True
    for n in (2, 3, 6, 10, 15, 16, 17, 18, 21, 28):
        a = LP.threshold_a(oler_bound, n)
        d = 2.0 * a
        ref = LP.oler_d(n)
        diff = abs(d - ref)
        ok_c &= diff < 1e-9
        say(f"     {n:>4}{d:>22.12f}{ref:>18.12f}{diff:>14.2e}")
    say("")
    say(f"     CONTROL PASSED: {ok_v and ok_c}")
    if not (ok_v and ok_c):
        say("     CONTROL FAILED -- everything below is meaningless.  Stop.")
        sys.exit(1)
    return ok_v and ok_c


def step2():
    say("")
    say("=" * 78)
    say("STEP 2 -- reduced LP (variables c_A, c_L) at n = 16, 17, 18")
    say("=" * 78)
    say("The LP is an OPTIMISTIC relaxation: it imposes (V) only on the")
    say("library, so its answer is an upper estimate of what the family can")
    say("prove.  Larger library = more constraints = answer decreases toward")
    say("the truth.  Oler's value is the number to beat.")
    say("")
    rows = []
    for size in (3, 4, 5, 6, 8, 10):
        cfgs = fw.library(size=size)
        line = [size, len(cfgs)]
        for n in (16, 17, 18):
            a = LP.threshold_a(lambda x: LP.reduced_lp(cfgs, x)[0], n)
            line.append(2.0 * a)
        _, x = LP.reduced_lp(cfgs, 4.1789)
        line += [x[0], x[1]]
        rows.append(line)
    say(f"{'size':>5}{'#cfgs':>7}{'d(16)':>14}{'d(17)':>14}{'d(18)':>14}"
        f"{'c_A*':>12}{'c_L*':>10}")
    for r in rows:
        say(f"{r[0]:>5}{r[1]:>7}{r[2]:>14.6f}{r[3]:>14.6f}{r[4]:>14.6f}"
            f"{r[5]:>12.6f}{r[6]:>10.6f}")
    say("")
    say(f"{'Oler':>12}{LP.oler_d(16):>14.6f}{LP.oler_d(17):>14.6f}"
        f"{LP.oler_d(18):>14.6f}{2/SQRT3:>12.6f}{0.5:>10.6f}")
    return rows


def step3():
    say("")
    say("=" * 78)
    say("STEP 3 -- full LP: ONE FREE SCORE VALUE PER FACE SHAPE")
    say("=" * 78)
    say("This is the nonlinearity test.  sigma is no longer forced to be an")
    say("affine function of area: every distinct triangle shape occurring in")
    say("the library gets its own LP variable, and likewise every distinct")
    say("boundary edge length.  If nonlinearity buys anything, it shows here.")
    say("")
    say(f"{'size':>5}{'#shapes':>9}{'#edges':>8}{'d(16)':>14}{'d(17)':>14}"
        f"{'d(18)':>14}{'max |sigma - linear|':>24}")
    for size in (4, 6, 8):
        cfgs = fw.library(size=size)
        ds = []
        for n in (16, 17, 18):
            a = LP.threshold_a(lambda x: LP.score_lp(cfgs, x)[0], n, iters=60)
            ds.append(2.0 * a)
        _, _, dev, (ns, ne) = LP.score_lp(cfgs, 4.1789, return_solution=True)
        say(f"{size:>5}{ns:>9}{ne:>8}{ds[0]:>14.6f}{ds[1]:>14.6f}"
            f"{ds[2]:>14.6f}{dev:>24.2e}")
    say("")
    say("`max |sigma - linear|` is the largest deviation of the LP-optimal")
    say("score from the linear member c_A*area(f) - 1/2 at the same c_A.")
    say("It is 0 to solver precision: the LP drives every sigma to the top of")
    say("its (D) constraint, which is the linear member.  That is forced, not")
    say("accidental -- see the collapse proposition in the attack README.")


def step4(rows):
    say("")
    say("=" * 78)
    say("STEP 4 -- verdict against the kill-criterion")
    say("=" * 78)
    ref = LP.oler_d(16)
    say(f"Kill-criterion: if the LP optimum at n = 16 does not strictly exceed")
    say(f"sqrt(129) - 3 = {ref:.10f}, the family is no stronger than its")
    say("linear member.  Record the LP, the discretisation and the value; stop.")
    say("")
    say("Trend of d(16) across library refinement:")
    for r in rows:
        say(f"   size {r[0]:>3} ({r[1]:>4} cfgs):  d(16) = {r[2]:.10f}"
            f"   excess over Oler = {r[2]-ref:+.3e}")
    final = rows[-1][2]
    say("")
    if final > ref + 1e-9:
        say(f"  d(16) = {final:.10f} STRICTLY EXCEEDS Oler by {final-ref:.3e}.")
        say("  Kill-criterion NOT met at this refinement.  Check whether the")
        say("  excess is a truncation artifact before claiming anything.")
    else:
        say(f"  d(16) = {final:.10f} does NOT strictly exceed Oler's")
        say(f"  {ref:.10f}.  KILL-CRITERION MET.  Outcome (a): the family is")
        say("  no stronger than its linear member.  Stop.")


def main():
    cfgs = step0()
    step1(cfgs)
    rows = step2()
    step3()
    step4(rows)
    # Anchor the transcript to THIS directory, not to the caller's cwd.  The
    # documented command is run from the repo root, where a relative "out/..."
    # raised FileNotFoundError after every LP had already been solved.
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "report.txt"), "w") as fh:
        fh.write(OUT.getvalue())
    say("")
    say("transcript written to %s" % os.path.join(out_dir, "report.txt"))


if __name__ == "__main__":
    main()
