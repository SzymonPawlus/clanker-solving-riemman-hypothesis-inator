"""Exact 'two disjoint dijoins' decision via hypergraph 2-colourability.

Derivation (mine, from the definitions): a partition of A into J1, J2 with both
dijoins exists iff no dicut is monochromatic, i.e. iff the hypergraph of dicuts
is 2-colourable.  Any two disjoint dijoins can be grown to such a partition
because a superset of a dijoin is a dijoin, so partitions lose no generality.
Only MINIMAL dicuts matter (a dicut containing another is automatically
bichromatic once the smaller one is).
"""

def minimal_sets(sets):
    ss = sorted({frozenset(s) for s in sets}, key=len)
    out = []
    for s in ss:
        if not any(t <= s for t in out):
            out.append(s)
    return out


def two_colourable(hyperedges):
    """Backtracking with unit propagation. Returns a colouring dict or None."""
    E = minimal_sets(hyperedges)
    if any(len(e) == 0 for e in E):
        return None
    if any(len(e) == 1 for e in E):
        return None                       # singleton dicut cannot be bichromatic
    elems = sorted({x for e in E for x in e})
    col = {}

    def consistent():
        for e in E:
            seen = {col[x] for x in e if x in col}
            if len(e - set(col)) == 0 and len(seen) < 2:
                return False
        return True

    def rec(i):
        if not consistent():
            return False
        if i == len(elems):
            return True
        for c in (0, 1):
            col[elems[i]] = c
            if rec(i + 1):
                return True
            del col[elems[i]]
        return False

    return dict(col) if rec(0) else None


def two_dijoins_exact(n, arcs, dicut_list):
    """Returns (J1, J2) or None.  Arcs in no dicut are dumped into J1."""
    c = two_colourable(dicut_list)
    if c is None:
        return None
    J1 = {i for i in range(len(arcs)) if c.get(i, 0) == 0}
    J2 = {i for i in range(len(arcs)) if c.get(i, 0) == 1}
    return J1, J2
