"""Second-generation search for a tau_w = 2 counterexample to the 0/1-weighted
Edmonds-Giles statement (a Schrijver-type example), reconstructed from the
definitions because ir.cwi.nl / arxiv.org are blocked by this sandbox's proxy.

Method.  For a digraph D, the family of admissible weight supports
S ("every dicut C has |C cap S| >= 2") is UPWARD closed, and shrinking S can
only make the trace hypergraph harder to 2-colour.  So the interesting supports
are the MINIMAL admissible ones.  For each digraph we compute many minimal
admissible S by starting from S = A and greedily deleting arcs in random order,
then test exact 2-colourability of {C cap S}.  A failure is a counterexample.
"""
import random, sys
from dicut import dicuts
from twocol import two_colourable, minimal_sets


def minimal_supports(cs, m, tries, rng):
    """cs: list of frozensets (dicuts).  Yields minimal admissible supports."""
    full = set(range(m))
    if any(len(c) < 2 for c in cs):
        return
    order = list(range(m))
    for _ in range(tries):
        rng.shuffle(order)
        S = set(full)
        for a in order:
            S.discard(a)
            if any(len(c & S) < 2 for c in cs):
                S.add(a)
        yield frozenset(S)


def attack(n, arcs, rng, tries=60):
    cs = dicuts(n, arcs)
    if not cs:
        return None
    m = len(arcs)
    seen = set()
    for S in minimal_supports(cs, m, tries, rng):
        if S in seen:
            continue
        seen.add(S)
        traces = [c & S for c in cs]
        if two_colourable(traces) is None:
            return (S, minimal_sets(traces))
    return None


def random_dag(n, p, rng, maxmult=1):
    arcs = []
    for i in range(n):
        for j in range(i + 1, n):
            k = 0
            for _ in range(maxmult):
                if rng.random() < p:
                    k += 1
            arcs.extend([(i, j)] * k)
    return arcs


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    found = 0
    for t in range(trials):
        n = rng.choice([7,8,9,10,11,12])
        p = rng.uniform(0.10, 0.45)
        arcs = random_dag(n, p, rng, maxmult=rng.choice([1, 1, 2]))
        if len(arcs) < 5 or len(arcs) > 22:
            continue
        r = attack(n, arcs, rng)
        if r:
            found += 1
            S, traces = r
            print("COUNTEREXAMPLE FOUND")
            print("  n     =", n)
            print("  arcs  =", arcs)
            print("  S     =", sorted(S), "=", [arcs[i] for i in sorted(S)])
            print("  A\\S   =", [arcs[i] for i in range(len(arcs)) if i not in S])
            print("  minimal traces =", [sorted(t) for t in traces])
            sys.stdout.flush()
            if found >= 3:
                break
    print("done, found", found)
