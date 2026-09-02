"""Hand-built adversarial instances (issue #149 step 4).  Each probes one classic
implementation error; the EXPECTED values were derived by hand and are asserted
against woodall_audit.py.  Run: python3 adversarial.py
"""
import sys
from woodall_audit import *
from woodall_audit import _strongly_connected

failures = []
def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)

def report(name, n, arcs):
    t, v = woodall_verdict(n, arcs)
    print(f"--- {name}: n={n} arcs={arcs}\n    tau={t} verdict={v} min-dicut={min_dicut_witness(n, arcs)} "
          f"#dicut-shores={len(all_dicuts(n, arcs))} #distinct={len(distinct_dicut_sets(n, arcs))} #minimal={len(minimal_dicut_sets(n, arcs))}")
    return t, v

# A. dicut without delta^-(U)=empty.  "Wide diamond" s->a,b,c ; a,b,c->t.
#    U={a} has delta^+ = {a->t} of size 1 but delta^- = {s->a} nonempty, so it is NOT a dicut.
#    Correct tau = 3 (dicuts: {s}:3, {s,a}:3, {s,a,b}:3, ... V\{t}:3).  A "delta^+ nonempty" impl says tau=1.
n, arcs = 5, [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
t, v = report("A wide-diamond K(1,3,1)", n, arcs)
check(t == 3 and v is True, "A: tau=3 and three disjoint dijoins (the three s-t paths)")
check(all((U >> 0) & 1 and not (U >> 4) & 1 for U, _ in all_dicuts(n, arcs)), "A: every dicut shore contains s and excludes t")
check(len(all_dicuts(n, arcs)) == 8, "A: exactly 2^3 dicut shores (s plus any subset of {a,b,c})")

# B. parallel arcs.  Three parallel arcs 0->1: tau=3, three one-arc dijoins.  Collapsed -> tau=1.
n, arcs = 2, [(0, 1), (0, 1), (0, 1)]
t, v = report("B triple parallel arc", n, arcs)
check(t == 3 and v is True, "B: tau=3 with parallel arcs kept distinct")
p = pack_dijoins(n, arcs, 3)
check(sorted(map(sorted, p)) == [[0], [1], [2]], f"B: packing is three singletons: {p}")
# B2. parallel arcs where collapsing changes tau from 3 to 2 in a bigger instance.
#    (First attempt used 2->3 doubled instead of 1->3 doubled; my hand value tau=3 was WRONG there,
#     U={0,1} cuts only {0->2, 1->3}; the tool correctly reported tau=2.  Instance fixed below.)
n, arcs = 4, [(0, 1), (0, 1), (0, 2), (1, 3), (1, 3), (2, 3)]
t, v = report("B2 diamond with doubled arcs", n, arcs)
check(t == 3 and v is True, "B2: tau=3 (U={0}:3, {0,1}:3, {0,2}:3, {0,1,2}:3), packs into 3")
simple = sorted(set(arcs))
check(tau(n, simple) == 2, "B2: collapsing parallel arcs would (wrongly) give tau=2")

# C. tau minimised over the wrong cut family (e.g. only single-vertex source/sink cuts).
#    Bottleneck: s->a,b,c->x, x->y, y->d,e,f->t.  Every single-source/sink cut has size 3,
#    but U={s,a,b,c,x} gives dicut {x->y} of size 1.  tau=1.
n = 10  # s=0 a=1 b=2 c=3 x=4 y=5 d=6 e=7 f=8 t=9
arcs = [(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(4,5),(5,6),(5,7),(5,8),(6,9),(7,9),(8,9)]
t, v = report("C bottleneck", n, arcs)
src, snk = sources_sinks(n, arcs)
check(t == 1 and v is True, "C: tau=1 via the bottleneck arc although source/sink degrees are 3")
check(min_dicut_witness(n, arcs)[1] == [6], "C: the minimum dicut is exactly arc 6 = x->y")

# D. easy direction confusion: tau+1 disjoint dijoins must never exist; tau exist on these.
for name, n, arcs in [("D wide diamond", 5, [(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)]),
                      ("D K(1,4,1)", 6, [(0,1),(0,2),(0,3),(0,4),(1,5),(2,5),(3,5),(4,5)]),
                      ("D crown", 6, [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)])]:
    t, v = report(name, n, arcs)
    check(v is True and pack_dijoins(n, arcs, t + 1) is None, f"{name}: tau={t} packs, tau+1 does not")

# E. empty set / U = V.  Neither is a shore; a strongly connected digraph has NO dicut.
n, arcs = 3, [(0,1),(1,2),(2,0),(0,2)]
t, v = report("E strongly connected", n, arcs)
check(t is None and v is None and all_dicuts(n, arcs) == [], "E: no dicut at all; tau undefined")
check(is_dijoin(n, arcs, []), "E: the EMPTY arc set is a dijoin of a strongly connected digraph")
# a single vertex: no proper nonempty subset
check(all_dicuts(1, []) == [] and tau(1, []) is None, "E: single vertex has no dicut")

# F. weakly disconnected digraph: an empty dicut exists -> tau=0 -> no dijoin exists.
n, arcs = 4, [(0,1),(2,3)]
t, v = report("F disconnected", n, arcs)
check(t == 0, "F: tau=0 (U={0,1} has empty delta^- and empty delta^+)")
check(not is_dijoin(n, arcs, [0, 1]), "F: even the full arc set is not a dijoin (contraction not SC)")
# G. disconnected but each piece strongly connected: still tau=0
n, arcs = 4, [(0,1),(1,0),(2,3),(3,2)]
t, v = report("G two 2-cycles", n, arcs)
check(t == 0, "G: tau=0 for two disjoint strong components")

# H. loops lie in no dicut and never help a dijoin
n, arcs = 2, [(0,0),(0,1),(1,1)]
t, v = report("H loops", n, arcs)
check(t == 1 and not is_dijoin(n, arcs, [0, 2]) and is_dijoin(n, arcs, [1]), "H: loops are in no dicut")

# I. dijoin vs strengthening (reversal). Path 0->1->2->3: all arcs is a dijoin (contraction), reversal not SC.
n, arcs = 4, [(0,1),(1,2),(2,3)]
check(is_dijoin(n, arcs, [0,1,2]) and not _strongly_connected(n, [(v,u) for u,v in arcs]), "I: dijoin != strengthening")
check(is_dijoin(n, arcs, [0,1,2]) and not is_dijoin(n, arcs, [0,2]), "I: every dicut of a path is a single arc; must take all")

# J. non-minimal dicuts: the packer only uses minimal dicuts; check it still meets ALL dicuts.
n, arcs = 6, [(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(4,5),(0,5),(1,5)]
t, v = report("J wide diamond + shortcuts", n, arcs)
dc = [c for _, c in all_dicuts(n, arcs)]
if v:
    P = pack_dijoins(n, arcs, t)
    check(all(all(c & set(cl) for c in dc) for cl in P), "J: every class meets every (not only minimal) dicut")

# K. condensation of a digraph with cycles must give a MULTI-DAG; verdicts agree.
n, arcs = 5, [(0,1),(1,0),(0,2),(1,2),(1,3),(0,3),(2,4),(3,4),(2,3),(3,2),(0,4)]
k, carcs = condensation(n, arcs)
report("K with 2-cycles", n, arcs)
check(k == 3 and len(carcs) == 7 and len(set(carcs)) < len(carcs), f"K: condensation is a multi-DAG on 3 vertices with parallel arcs: {carcs}")
check(woodall_verdict(n, arcs) == woodall_verdict(k, carcs) == (3, True), "K: tau=3 and verdict preserved by condensation")

print("FAILURES:", len(failures))
sys.exit(1 if failures else 0)
