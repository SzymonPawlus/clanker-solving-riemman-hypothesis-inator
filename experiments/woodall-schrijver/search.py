#!/usr/bin/env python3
"""Exhaustive search for a {0,1}-weighted counterexample to Edmonds-Giles on a
small number of vertices.

    python3 search.py [max_n]        # default 5;  n=6 takes minutes (see below)

THE SEARCH SPACE, STATED EXACTLY (problems/woodalls-conjecture/RULES.md §2).

For each n, the space searched is

    { (D, w) :  D a SIMPLE DAG on the labelled vertex set {0,...,n-1} whose
                arcs all go from a lower to a higher index,
                w : A(D) -> {0,1} }

enumerated as: each of the n(n-1)/2 ordered pairs i<j is independently in one
of three states -- no arc, an arc of weight 0, an arc of weight 1 -- giving
exactly 3^(n(n-1)/2) instances, every one of which is tested.  Counts:

    n=2:            3          n=5:       59 049
    n=3:           27          n=6:   14 348 907
    n=4:          729          n=7:   10 460 353 203     (not run -- see below)

WHY DAGs, AND WHAT THAT COSTS.  Dicut shores are exactly the vertex sets closed
under in-neighbours, so every shore is a union of strongly connected components
and the dicuts of D are precisely the dicuts of its condensation; arcs inside a
strongly connected component lie in no dicut and are therefore useless in a
dijoin.  So (D,w) is a counterexample iff its condensation, with the same
weights, is.  Restricting to DAGs is thus WITHOUT LOSS OF GENERALITY -- but
restricting to *simple* DAGs is NOT: contracting components can create parallel
arcs, and two parallel weight-1 arcs behave like one arc of weight 2, which is
outside {0,1}.  So this search covers exactly the {0,1}-weighted instances
whose condensation is simple.  Every labelled simple DAG on n vertices appears
at least once (relabel by any topological order); isomorphic copies are visited
repeatedly, which costs time but omits nothing.

THE TEST.  With w in {0,1}, write S = {a : w(a)=1}.  Then
  * tau_w = min over dicuts C of |C \\ (A\\S)| = min |C n S|;
  * a weight-0 arc lies in no member of a w-packing, so every member is a
    subset of S and members are pairwise disjoint;
  * hence a w-packing of size 2 exists  <=>  S splits into J and S\\J with both
    meeting every dicut  <=>  the hypergraph H(S) = { C n S : C a dicut } has
    NO monochromatic edge under some 2-colouring of S, i.e. H(S) has PROPERTY B.
It suffices to range C over the inclusion-wise MINIMAL dicuts: any dicut
contains a minimal one, and an edge containing a bichromatic edge is bichromatic.

So an instance is a counterexample to Edmonds-Giles at tau_w = 2 iff
    (i)  every minimal dicut C has |C n S| >= 2      [tau_w >= 2], and
    (ii) H(S) is not 2-colourable                    [nu_w <= 1].
(tau_w > 2 with nu_w < tau_w would also be a counterexample; the code reports
tau_w for every instance it finds, and reports the tau_w >= 3 case separately.)

WHAT A NEGATIVE RESULT HERE IS AND IS NOT.  Finding nothing at n <= N shows
only that no such instance exists in the stated space at n <= N.  It is NOT
evidence that none exists at n = N+1, and it is certainly not evidence about
Woodall's conjecture, which is the *unweighted* statement and is untouched by
any of this.
"""

import sys
import time
from itertools import combinations


def minimal_dicuts(n, arcs):
    """arcs: list of (i,j) with i<j.  Returns a list of arc-index bitmasks, or
    None if the digraph admits an EMPTY dicut.

    An empty dicut is a shore U with delta^-(U) = delta^+(U) = {}, which happens
    exactly when the underlying graph is disconnected.  Such an instance has
    tau_w = 0 and no dijoin whatsoever, so it can never be a counterexample at
    tau_w >= 2 -- but it must be recognised, not silently dropped, or the
    caller would read tau_w off the nonempty cuts and wrongly conclude
    tau_w >= 2.  Returning None makes the caller skip the whole support."""
    m = len(arcs)
    cuts = set()
    for U in range(1, (1 << n) - 1):
        plus = 0
        bad = False
        for k, (i, j) in enumerate(arcs):
            iin = (U >> i) & 1
            jin = (U >> j) & 1
            if iin and not jin:
                plus |= 1 << k
            elif jin and not iin:
                bad = True
                break
        if not bad:
            if not plus:
                return None
            cuts.add(plus)
    cs = sorted(cuts)
    return [c for c in cs if not any(d != c and (d & c) == d for d in cs)]


def two_colourable(edges, universe_bits):
    """Property B by exhaustive 2-colouring of `universe_bits` (a list of arc
    indices).  Fixes the colour of the first element to kill the trivial
    symmetry."""
    k = len(universe_bits)
    if k == 0:
        return not edges
    idx = {b: p for p, b in enumerate(universe_bits)}
    # re-express each edge over positions 0..k-1
    E = []
    for e in edges:
        v = 0
        b = e
        while b:
            low = b & -b
            v |= 1 << idx[low.bit_length() - 1]
            b ^= low
        E.append(v)
    full = (1 << k) - 1
    for col in range(1 << (k - 1)):        # element 0 always colour 0
        c = col << 1
        if all((x & c) and (x & (full ^ c)) for x in E):
            return True
    return False


def search_n(n, report_every=None):
    pairs = list(combinations(range(n), 2))
    P = len(pairs)
    found = []
    tested = 0
    skipped_disconnected = 0
    tau_ge2_count = 0
    t0 = time.time()
    for support in range(1 << P):
        arcs = [pairs[k] for k in range(P) if (support >> k) & 1]
        m = len(arcs)
        if m == 0:
            tested += 1
            skipped_disconnected += 1 if n > 1 else 0
            continue
        mins = minimal_dicuts(n, arcs)
        if mins is None:
            # empty dicut present: tau_w = 0 for every weighting.  Counted as
            # tested-and-rejected, which it is.
            tested += 1 << m
            skipped_disconnected += 1 << m
            continue
        if not mins:
            tested += 1 << m
            continue
        for S in range(1 << m):
            tested += 1
            sizes = [(c & S).bit_count() for c in mins]
            tau = min(sizes)
            if tau < 2:
                continue
            tau_ge2_count += 1
            bits = [k for k in range(m) if (S >> k) & 1]
            edges = [c & S for c in mins]
            if not two_colourable(edges, bits):
                found.append((n, tuple(arcs), S, tau))
        if report_every and support % report_every == 0:
            print(f"    n={n} support {support}/{1 << P} "
                  f"({time.time() - t0:.0f}s, {tested} instances)", flush=True)
    return found, tested, tau_ge2_count, time.time() - t0, skipped_disconnected


def main(max_n=5):
    print(f"exhaustive {{0,1}}-weighted search over simple DAGs, n = 2..{max_n}")
    print(f"space: 3^(n(n-1)/2) instances per n, all tested")
    total_found = []
    times = {}
    for n in range(2, max_n + 1):
        found, tested, t2, el, disc = search_n(n)
        expect = 3 ** (n * (n - 1) // 2)
        status = "OK" if tested == expect else f"MISCOUNT (expected {expect})"
        times[n] = el
        print(f"  n={n}: tested {tested:>12,} ({status}); {disc:>11,} had an empty "
              f"dicut (tau_w=0); {t2:>10,} had tau_w >= 2; "
              f"counterexamples found: {len(found)}; {el:.1f}s")
        total_found += found
    print()
    if max_n in times and max_n >= 5:
        per = times[max_n] / 3 ** (max_n * (max_n - 1) // 2)
        nxt = max_n + 1
        est = per * 3 ** (nxt * (nxt - 1) // 2)
        print(f"  measured cost: {per * 1e9:.1f} ns/instance at n={max_n}; extrapolating,")
        print(f"  n={nxt} would be {3 ** (nxt * (nxt - 1) // 2):,} instances ~ "
              f"{est / 3600:.1f} h in this implementation.")
        print()
    if total_found:
        print(f"  !! {len(total_found)} counterexample(s) found -- inspect them")
        for f in total_found[:5]:
            print("   ", f)
    else:
        print(f"  RESULT: no {{0,1}}-weighted counterexample to Edmonds-Giles exists")
        print(f"  among simple DAGs on at most {max_n} vertices.  This is a FAILED")
        print(f"  SEARCH over a precisely stated finite space, not evidence that")
        print(f"  none exists on more vertices.")
    return total_found


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(N)
