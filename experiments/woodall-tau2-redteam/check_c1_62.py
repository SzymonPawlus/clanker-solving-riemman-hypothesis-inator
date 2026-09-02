"""Independent check of C1 §6.2's mechanical demonstration instance:
diamond s->x, s->y, x->t, y->t (weight 1) plus a weight-0 arc x->y."""
from dicut import dicuts, dicut_shores, is_dijoin
from twocol import two_colourable

V = {'s': 0, 'x': 1, 'y': 2, 't': 3}
names = ['sx', 'sy', 'xt', 'yt', 'xy']
arcs  = [(0,1), (0,2), (1,3), (2,3), (1,2)]
S     = {0, 1, 2, 3}            # weight-1 arcs; arc 4 (xy) has weight 0
inv = {v: k for k, v in V.items()}

print("dicut shores and their dicuts:")
for U, C in dicut_shores(4, arcs):
    print("  U =", sorted(inv[u] for u in U),
          " C =", sorted(names[i] for i in C),
          " |C cap S| =", len(set(C) & S))
cs = dicuts(4, arcs)
print("tau_w =", min(len(set(c) & S) for c in cs), " (C1 claims 2)")
print("{s,y} a dicut shore?", any(U == frozenset({0,2}) for U, _ in dicut_shores(4, arcs)),
      " (C1 claims NO: x->y enters it)")

O = {0: (0,1), 4: (1,2), 1: (2,0), 3: (2,3), 2: (3,1)}   # C1's O: s->x, x->y, y->s, y->t, t->x
def strong(O, n=4):
    out = {v: [] for v in range(n)}; inn = {v: [] for v in range(n)}
    for (t_, h) in O.values(): out[t_].append(h); inn[h].append(t_)
    def r(adj, s):
        seen = {s}; st = [s]
        while st:
            z = st.pop()
            for y in adj[z]:
                if y not in seen: seen.add(y); st.append(y)
        return seen
    return r(out, 0) == set(range(n)) and r(inn, 0) == set(range(n))
print("C1's O strongly connected?", strong(O), " (C1 claims yes)")

J1 = {i for i in range(5) if O[i] == arcs[i]}
J2 = set(range(5)) - J1
print("red  J1 =", sorted(names[i] for i in J1), " (C1: sx, yt, xy)")
print("blue J2 =", sorted(names[i] for i in J2), " (C1: sy, xt)")
C = [c for U, c in dicut_shores(4, arcs) if U == frozenset({0,1})][0]
print("C = delta+({s,x}) =", sorted(names[i] for i in C), " (C1: sy, xt, xy)")
print("red cap C =", sorted(names[i] for i in set(C) & J1),
      "-> all weight-0?", (set(C) & J1) & S == set())
print("(J1 cap S) meets C?", bool((J1 & S) & set(C)),
      " -> C1's claim 'J1 cap S misses C' is", "CONFIRMED" if not ((J1 & S) & set(C)) else "REFUTED")
print("does a w-packing nevertheless exist?",
      two_colourable([set(c) & S for c in cs]) is not None,
      " (C1 claims yes: {sx,xt},{sy,yt})")
