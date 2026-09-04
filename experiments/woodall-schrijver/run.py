#!/usr/bin/env python3
"""Reproduce everything in attacks/schrijver-instance/README.md with one command:

    python3 experiments/woodall-schrijver/run.py

Stdlib only.  Python 3.11+ (developed and run on CPython 3.14.5).  No randomness,
no seeds, no third-party libraries -- exact integer arithmetic throughout.

Stage 1 validates both checkers against fixtures with independently known
answers (problems/woodalls-conjecture/RULES.md §4).
Stage 2 runs them on Schrijver's instance.
Stage 3 cross-checks the transcription against published assertions about it.
Stage 4 records what an exhaustive {0,1}-weighted search at small n does and
does not establish.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checker_a import Instance                      # noqa: E402
from checker_b import InstanceB                     # noqa: E402
from instance import VERTICES, ARCS, rotation       # noqa: E402

FAIL = []


def expect(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def both(name, vertices, arcs, exp_tau, exp_nu, exp_ndicuts=None):
    """Run both checkers, require they agree with each other and with the
    independently derived expected values."""
    A = Instance(vertices, arcs)
    B = InstanceB(vertices, arcs)
    tA, tB = A.tau_w(), B.tau()
    nA = A.nu_w()
    kmax = 4 if tA is None else tA
    nB = B.nu01(kmax) if all((a[2] if len(a) > 2 else 1) in (0, 1) for a in arcs) else nA
    cA = len(A.dicuts())
    cB = len(B.shores())
    print(f"[{name}] tau_w A={tA} B={tB} | nu_w A={nA} B={nB} | #dicut-shores A={cA} B={cB}")
    expect(tA == tB, f"{name}: the two checkers agree on tau_w")
    expect(nA == nB, f"{name}: the two checkers agree on nu_w")
    expect(cA == cB, f"{name}: the two checkers agree on the number of dicut shores")
    expect(tA == exp_tau, f"{name}: tau_w = {exp_tau} (independently derived by hand)")
    expect(nA == exp_nu, f"{name}: nu_w = {exp_nu} (independently derived by hand)")
    if exp_ndicuts is not None:
        expect(cA == exp_ndicuts, f"{name}: {exp_ndicuts} dicut shores")
    if tA is not None and nA is not None:
        expect(nA <= tA, f"{name}: easy direction nu_w <= tau_w holds")
    return A, B


# ---------------------------------------------------------------------------
print("=" * 74)
print("STAGE 1 -- fixtures with hand-derived answers")
print("=" * 74)

# (1) directed path a->b->c.  Shores {a},{a,b}; dicuts {ab},{bc}; tau=1.
#     A dijoin must contain both arcs, so only one disjoint dijoin exists.
both("path P3", "abc", [("a", "b"), ("b", "c")], 1, 1, 2)

# (2) directed circuit: EVERY nonempty proper U has an entering arc, so there
#     are NO dicuts, tau = +infinity (convention).  This is the fixture that
#     catches the delta^+/delta^- confusion: under the wrong reading
#     "delta^+(U) != {}" a circuit would have many "dicuts".
both("circuit C4", "abcd",
     [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")], None, None, 0)

# (3) DAG with two sources s1,s2 both into t.  Shores {s1},{s2},{s1,s2}.
both("two sources", ["s1", "s2", "t"], [("s1", "t"), ("s2", "t")], 1, 1, 3)

# (4) the diamond: tau = 2 and two disjoint dijoins {sx,xt},{sy,yt} exist.
#     This is the tau=2 case, which is a known theorem, so nu must equal tau.
both("diamond", "sxyt",
     [("s", "x"), ("s", "y"), ("x", "t"), ("y", "t")], 2, 2, 4)

# (5) the diamond plus a weight-0 arc x->y.  attacks/tau2-complete/README.md §6
#     states independently: dicut shores are exactly {s},{s,x},{s,x,y}
#     (NOT {s,y}, since x->y enters it), tau_w = 2, and a w-packing
#     {sx,xt},{sy,yt} exists.  Agreement here is a cross-check on a *weighted*
#     instance whose numbers another worker derived without this code.
both("diamond + 0-arc", "sxyt",
     [("s", "x", 1), ("s", "y", 1), ("x", "t", 1), ("y", "t", 1), ("x", "y", 0)],
     2, 2, 3)

# (6) tau = 3: complete bipartite orientation, sources 1,2,3 -> sinks 4,5,6.
#     Every dijoin needs an arc out of each source; 3 disjoint dijoins therefore
#     use each of the 9 arcs exactly once and are perfect matchings, which do
#     hit every dicut.  So tau = nu = 3.  Fixture beyond tau=2.
#     Shores: the 7 nonempty subsets of {1,2,3}, plus {1,2,3} u T for the 6
#     nonempty proper subsets T of {4,5,6}  =  13.  (My first hand count said 7;
#     I had forgotten the shores containing sinks.  The checkers caught it.)
both("K33 orientation", [1, 2, 3, 4, 5, 6],
     [(i, j) for i in (1, 2, 3) for j in (4, 5, 6)], 3, 3, 13)

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("STAGE 2 -- Schrijver's instance")
print("=" * 74)

arcs = [(t, h, w) for (t, h, w, _lab) in ARCS]
t0 = time.time()
A, B = both("Schrijver", VERTICES, arcs, 2, 1)
print(f"  elapsed {time.time() - t0:.2f}s")

print()
print("  arc list (tail, head, weight, label in arXiv:2501.10918v2 Fig. 1 left):")
for (t, h, w, lab) in ARCS:
    print(f"    {t:>3s} -> {h:<3s}  w={w}   {lab}")

tau = A.tau_w()
nu = A.nu_w()
print()
expect(tau == 2, "Schrijver: tau_w = 2")
expect(nu == 1, "Schrijver: nu_w = 1, i.e. NO w-packing of 2 dijoins")
expect(nu < tau, "Schrijver: nu_w < tau_w -- this IS a counterexample to Edmonds-Giles")
solid = 0
for j, (_t, _h, w) in enumerate(arcs):
    if w:
        solid |= 1 << j
expect(A.is_dijoin(solid), "Schrijver: the 9 weight-1 arcs together DO form one dijoin "
                           "(so nu_w = 1 exactly, not 0)")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("STAGE 3 -- cross-checks on the transcription itself")
print("=" * 74)

# 3a. order-3 rotational symmetry claimed in instance.py
arcset = {(t, h, w) for (t, h, w, _l) in ARCS}
rot = {(rotation(t), rotation(h), w) for (t, h, w) in arcset}
expect(rot == arcset, "the order-3 rotation is an automorphism preserving weights")

# 3b. arXiv:2501.10918v2, Fig. 1 caption, asserts of Schrijver's instance:
#     "Among all minimal dicuts, six have weight 2 such as D_1 >= {1,1'} and
#      D_2 >= {1,1''}, and four have weight 3 such as D_3 >= {1,2,3} and
#      D_4 >= {1',2'',3}."
#     Read as "minimal as arc sets" that is false -- there are 49 of those, of
#     weights 2,3,4,5 (printed below).  The reading that matches, and the one
#     the dijoin question actually turns on, is: minimal among the TRACES
#     C n S of dicuts on the weight-1 arcs S.  Those are exactly what a dijoin
#     has to hit, and the caption's "D_i >= {...}" notation -- a dicut
#     CONTAINING the listed weight-1 arcs -- says precisely this.
mins = A.minimal_dicuts()
from collections import Counter                      # noqa: E402
print(f"  minimal dicuts as arc sets: {len(mins)}, weights "
      f"{dict(sorted(Counter(A.weight(c) for c in mins).items()))}")
expect(min(A.weight(c) for c in mins) == 2, "no dicut of weight < 2")

solid_mask = 0
for j, (_t, _h, w) in enumerate(arcs):
    if w:
        solid_mask |= 1 << j
LAB = [lab or f"({t}->{h})" for (t, h, _w, lab) in ARCS]
traces = sorted({c & solid_mask for _U, c in A.dicuts()})
mintr = [c for c in traces if not any(d != c and (d & c) == d for d in traces)]


def names(c):
    return frozenset(LAB[j] for j in range(A.m) if (c >> j) & 1)


named = {names(c) for c in mintr}
cnt = Counter(bin(c).count("1") for c in mintr)
print(f"  distinct traces C n S: {len(traces)};  minimal ones: {len(mintr)};  "
      f"sizes {dict(sorted(cnt.items()))}")
for c in sorted(mintr, key=lambda x: (bin(x).count("1"), x)):
    print("     {" + ", ".join(sorted(names(c))) + "}")
expect(cnt.get(2) == 6, "six minimal traces of size 2   [arXiv:2501.10918v2 Fig.1: "
                        "'six have weight 2']")
expect(cnt.get(3) == 4, "four minimal traces of size 3  [arXiv:2501.10918v2 Fig.1: "
                        "'four have weight 3']")
expect(len(mintr) == 10, "exactly 10 minimal traces in all")
for nm in ({"1", "1'"}, {"1", "1''"}, {"1", "2", "3"}, {"1'", "2''", "3"}):
    expect(frozenset(nm) in named,
           "the paper's named example {" + ", ".join(sorted(nm)) + "} is one of them")

# 3b'. A HAND-CHECKABLE proof that no w-packing of size 2 exists, not relying on
#      the exhaustive searches in checker A or checker B.
#      A 2-packing is exactly a 2-colouring of S with no monochromatic trace.
#      The traces {1,1'} and {1,1''} force c(1') = c(1'') = not c(1), and
#      likewise inside the 2- and 3-families.  Writing x=c(1), y=c(2), z=c(3),
#      the four size-3 traces {1,2,3}, {1',2'',3}, {1'',2,3'}, {1,2',3''} read
#          (x,y,z), (~x,~y,z), (~x,y,~z), (x,~y,~z)
#      and forbid respectively  x=y=z,  x=y!=z,  x=z!=y,  y=z!=x.  Every triple
#      in {0,1}^3 has either all three equal or exactly two equal, so it falls
#      under one of those four patterns and no colouring survives.  Checked:
bad = 0
for x in (0, 1):
    for y in (0, 1):
        for z in (0, 1):
            col = {"1": x, "1'": 1 - x, "1''": 1 - x,
                   "2": y, "2'": 1 - y, "2''": 1 - y,
                   "3": z, "3'": 1 - z, "3''": 1 - z}
            if all(len({col[a] for a in nm}) == 2 for nm in named):
                bad += 1
expect(bad == 0, "hand argument: none of the 8 forced colourings avoids a "
                 "monochromatic trace, so nu_w = 1 with no search at all")

# 3c. arXiv:2311.04337v2 Fig. 2 caption and issue #156's snippet hint:
#     the weight-1 arcs fall into (at least) three weakly connected components.
parent = {v: v for v in VERTICES}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


for (t, h, w, _l) in ARCS:
    if w:
        parent[find(t)] = find(h)
comps = {find(v) for v in VERTICES if any(w and v in (t, h) for (t, h, w, _l) in ARCS)}
expect(len(comps) == 3, "the weight-1 arcs form exactly 3 weakly connected components "
                        "[snippet hint in issue #156, and CLR Fig.2's three a_i-b_i paths]")

# 3d. arXiv:2501.10918v2 §5: "Schrijver's counterexample has a chordless cycle
#     of length 6".  Check the underlying simple undirected graph has one.
und = {}
for (t, h, _w, _l) in ARCS:
    und.setdefault(t, set()).add(h)
    und.setdefault(h, set()).add(t)


def chordless_cycles(length):
    found = []
    vs = sorted(und)
    for start in vs:
        stack = [[start]]
        while stack:
            path = stack.pop()
            if len(path) == length:
                if path[0] in und[path[-1]]:
                    # chordless?  no non-consecutive pair adjacent
                    ok = True
                    L = len(path)
                    for i in range(L):
                        for j in range(i + 2, L):
                            if i == 0 and j == L - 1:
                                continue
                            if path[j] in und[path[i]]:
                                ok = False
                    if ok:
                        found.append(frozenset(path))
                continue
            for nb in sorted(und[path[-1]]):
                if nb in path or nb < start:
                    continue
                stack.append(path + [nb])
    # each cycle is traversed once in each direction; de-duplicate by vertex set
    # (a chordless cycle is determined by its vertex set)
    return sorted(set(found), key=sorted)


c6 = chordless_cycles(6)
expect(len(c6) > 0, f"underlying graph has a chordless 6-cycle "
                    f"[asserted in arXiv:2501.10918v2 §5]; found {len(c6)}")
#     The underlying graph is NOT triangle-free: each "long" weight-1 arc closes
#     a triangle with a spoke and a hexagon edge (e.g. l-TL, l-tl, tl-TL).  My
#     first guess -- "two hexagons plus spokes, so no short cycles" -- was
#     wrong, and is recorded here because it is exactly the kind of eyeballed
#     structural claim that has to be machine-checked rather than asserted.
expect(len(chordless_cycles(3)) == 6, "underlying graph has exactly 6 triangles")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("STAGE 4 -- what a small-n exhaustive search does and does not show")
print("=" * 74)
import search                                         # noqa: E402
search.main()

# ---------------------------------------------------------------------------
print()
print("=" * 74)
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 74)
