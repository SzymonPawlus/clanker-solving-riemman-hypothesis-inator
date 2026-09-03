"""Independent reimplementation of the Robbins agreement/disagreement
construction that the tau2-robbins sketch uses, so the CONSTRUCTION (not just
the theorem) can be attacked on small instances.

Robbins orientation, derived independently: run a DFS on the connected
bridgeless multigraph G; orient every tree edge away from the root and every
non-tree (back) edge towards the root's side, i.e. from the later-discovered
endpoint to the earlier one.  Every vertex can then reach the root along tree
edges reversed?  -- no: the standard argument is the other way round, so we do
it explicitly and VERIFY strong connectivity afterwards rather than trusting it.
"""
from dicut import dicuts, is_dijoin


def underlying(arcs):
    """edges as (u,v) unordered-with-multiplicity, index-aligned with arcs."""
    return list(arcs)


def dfs_orientation(n, arcs):
    """Return a dict edge_index -> (tail, head) orienting each non-loop edge.
    Tree edges point away from the DFS root; back edges point from the
    deeper endpoint to the shallower one (i.e. 'up' the tree)."""
    adj = {v: [] for v in range(n)}
    for i, (u, v) in enumerate(arcs):
        if u == v:
            continue
        adj[u].append((v, i))
        adj[v].append((u, i))
    disc = {}
    orient = {}
    time = [0]

    def dfs(u):
        disc[u] = time[0]; time[0] += 1
        for (w, i) in adj[u]:
            if i in orient:
                continue
            if w not in disc:
                orient[i] = (u, w)          # tree edge, away from root
                dfs(w)
            else:
                orient[i] = (u, w)          # back edge, from deeper to shallower
        return

    for s in range(n):
        if s not in disc:
            dfs(s)
    return orient


def strongly_connected_on(n, orient, verts):
    """check the oriented graph restricted to `verts` is strongly connected"""
    if len(verts) <= 1:
        return True
    out = {v: [] for v in verts}
    inn = {v: [] for v in verts}
    for (t, h) in orient.values():
        if t in verts and h in verts:
            out[t].append(h); inn[h].append(t)
    def reach(adj, s):
        seen = {s}; st = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        return seen
    s = next(iter(verts))
    return reach(out, s) == set(verts) and reach(inn, s) == set(verts)


def robbins_colouring(n, arcs):
    """Return (J_plus, J_minus, orient) per the sketch: J_plus = arcs whose own
    direction agrees with the orientation O of the underlying edge."""
    orient = dfs_orientation(n, arcs)
    Jp, Jm = set(), set()
    for i, (u, v) in enumerate(arcs):
        if u == v:
            Jp.add(i); continue
        Jp.add(i) if orient[i] == (u, v) else Jm.add(i)
    return Jp, Jm, orient


def components(n, arcs):
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for (u, v) in arcs:
        a, b = find(u), find(v)
        if a != b: par[a] = b
    comp = {}
    for v in range(n):
        comp.setdefault(find(v), set()).add(v)
    return list(comp.values())


def has_bridge(n, arcs):
    """edge i is a bridge iff removing it disconnects its endpoints"""
    for i, (u, v) in enumerate(arcs):
        if u == v: continue
        rest = [a for j, a in enumerate(arcs) if j != i]
        adj = {x: [] for x in range(n)}
        for (a, b) in rest:
            adj[a].append(b); adj[b].append(a)
        seen = {u}; st = [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if v not in seen:
            return i
    return None
