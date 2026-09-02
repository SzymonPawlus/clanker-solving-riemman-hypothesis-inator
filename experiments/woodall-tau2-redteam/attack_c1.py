"""Red-team checks on agent C1's write-up (branch claude/152-tau2-complete,
commit f69bd44).  Run against MY machinery (dicut.py/twocol.py), written before
C1's file was readable; C1's tau2lib is NOT imported.

C1's self-declared weak points:
  W1 blue witness in 5.4 | W2 Theorem R Case 2 (parallel edges, z=u) | W3 Prop 4.1(i)
"""
import random, itertools, sys
from dicut import dicuts, is_dijoin
from twocol import two_dijoins_exact
from robbins import components, has_bridge, strongly_connected_on


# ------------------------------------------------------------------ W2 -----
def robbins_C1(arcs):
    """C1's Theorem R procedure, transcribed from C1's PROSE (not its code).
    Returns dict edge_index -> (tail, head) for every non-loop arc."""
    E = {i: (u, v) for i, (u, v) in enumerate(arcs) if u != v}
    if not E:
        return {}
    X = {E[min(E)][0]}
    F = {}

    def path(src, dst, banned):
        adj = {}
        for j, (a, b) in E.items():
            if j == banned:
                continue
            adj.setdefault(a, []).append((b, j))
            adj.setdefault(b, []).append((a, j))
        prev = {src: None}
        st = [src]
        while st:
            x = st.pop()
            for (y, j) in adj.get(x, []):
                if y not in prev:
                    prev[y] = (x, j)
                    st.append(y)
        if dst not in prev:
            return None
        seq = []
        cur = dst
        while prev[cur] is not None:
            p, j = prev[cur]
            seq.append((p, cur, j))
            cur = p
        seq.reverse()
        return seq                                   # src -> ... -> dst

    while len(F) < len(E):
        pick = None
        for j, (a, b) in E.items():
            if j in F:
                continue
            if a in X:
                pick = (j, a, b); break
            if b in X:
                pick = (j, b, a); break
        assert pick is not None, "no unoriented edge meets X (G disconnected?)"
        j, u, v = pick
        if v in X:                                   # Case 1
            F[j] = (u, v)
            continue
        P = path(v, u, banned=j)                     # Case 2
        assert P is not None, "G-e disconnected: e is a bridge"
        F[j] = (u, v)
        newX = {v}
        for (a, b, k) in P:                          # walk v -> ... -> u
            F[k] = (a, b)                            # orient along P'
            newX.add(a); newX.add(b)
            if b in X:                               # b is z: stop here
                break
        X |= newX
    return F


def colouring(arcs, O):
    J1 = {i for i, (u, v) in enumerate(arcs) if u == v or O.get(i) == (u, v)}
    J2 = set(range(len(arcs))) - J1
    return J1, J2


# ------------------------------------------------------------------ W3 -----
def condensation(n, arcs):
    """My own condensation, to test C1's Prop 4.1 independently."""
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
    for (u, v) in arcs:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for jj in range(n):
                    if reach[k][jj]:
                        reach[i][jj] = True
    comp = {}
    nxt = 0
    for i in range(n):
        if i in comp:
            continue
        comp[i] = nxt
        for jj in range(i + 1, n):
            if jj not in comp and reach[i][jj] and reach[jj][i]:
                comp[jj] = nxt
        nxt += 1
    keep = [i for i, (u, v) in enumerate(arcs) if comp[u] != comp[v]]
    carcs = [(comp[u], comp[v]) for (u, v) in arcs if comp[u] != comp[v]]
    return nxt, carcs, keep, comp


def rand_multidigraph(rng, n, pmax=3):
    arcs = []
    for u in range(n):
        for v in range(n):
            if u == v:
                if rng.random() < .1: arcs.append((u, v))
                continue
            for _ in range(pmax):
                if rng.random() < .18:
                    arcs.append((u, v))
    return arcs


def main():
    rng = random.Random(153153)
    fails = {'W2_strong': 0, 'W2_partition': 0, 'W1_colouring': 0,
             'W3_dicuts': 0, 'W3_tau': 0, 'theorem': 0}
    seen = tested = 0
    for _ in range(60000):
        n = rng.choice([3, 4, 5, 6])
        arcs = rand_multidigraph(rng, n)
        if len(arcs) < 2:
            continue
        cs = dicuts(n, arcs)
        if cs and min(len(c) for c in cs) < 2:
            continue                      # need tau >= 2, C1's hypothesis
        seen += 1
        # --- W3: Prop 4.1 (iii): same dicuts as arc sets, same tau
        cn, carcs, keep, comp = condensation(n, arcs)
        idx = {orig: k for k, orig in enumerate(keep)}
        ccs = dicuts(cn, carcs) if cn > 1 else []
        lifted = {frozenset(keep[i] for i in c) for c in ccs}
        if lifted != {frozenset(c) for c in cs}:
            fails['W3_dicuts'] += 1
            print("W3 FAIL dicut correspondence", n, arcs); sys.stdout.flush()
        tau_D = min((len(c) for c in cs), default=None)
        tau_Dp = min((len(c) for c in ccs), default=None)
        if tau_D != tau_Dp:
            fails['W3_tau'] += 1
            print("W3 FAIL tau", n, arcs); sys.stdout.flush()
        # --- theorem itself
        if two_dijoins_exact(n, arcs, cs) is None:
            fails['theorem'] += 1
            print("THEOREM FAIL", n, arcs); sys.stdout.flush()
        # --- W2: C1's Theorem R procedure
        if has_bridge(n, arcs) is not None or len(components(n, arcs)) > 1:
            continue                      # Lemma A says this cannot happen; checked below
        tested += 1
        O = robbins_C1(arcs)
        if not strongly_connected_on(n, O, {v for a in arcs for v in a}):
            fails['W2_strong'] += 1
            print("W2 FAIL not strong", n, arcs); sys.stdout.flush()
            continue
        if len(O) != len([1 for (u, v) in arcs if u != v]):
            fails['W2_partition'] += 1
            print("W2 FAIL not all edges oriented", n, arcs); sys.stdout.flush()
        # --- W1: the agreement colouring
        J1, J2 = colouring(arcs, O)
        if not (is_dijoin(n, arcs, J1, cs) and is_dijoin(n, arcs, J2, cs)):
            fails['W1_colouring'] += 1
            print("W1 FAIL colouring", n, arcs, sorted(J1), sorted(J2)); sys.stdout.flush()
    print(f"instances with tau>=2: {seen}; C1-Robbins run on {tested} of them")
    print("failures:", fails)


if __name__ == "__main__":
    main()
