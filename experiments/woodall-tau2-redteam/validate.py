from dicut import *

def show(name, n, arcs, expect_tau=None, expect_two=None):
    cs = dicuts(n, arcs)
    t = tau(n, arcs)
    two = two_disjoint_dijoins(n, arcs)
    print(f"{name}: n={n} m={len(arcs)} #dicuts={len(cs)} tau={t} two_dijoins={'YES' if two else 'NO'}")
    print(f"   dicuts (arc-index sets): {[sorted(c) for c in cs]}")
    if two: print(f"   partition: J+={sorted(two[0])} J-={sorted(two[1])}")
    ok = True
    if expect_tau is not None and t != expect_tau: ok=False; print("   !! TAU MISMATCH, expected", expect_tau)
    if expect_two is not None and bool(two) != expect_two: ok=False; print("   !! TWO-DIJOIN MISMATCH, expected", expect_two)
    print("   ->", "PASS" if ok else "FAIL")
    return ok

allok = True
# 1. directed path s->v->t  : tau = 1
allok &= show("directed path P3", 3, [(0,1),(1,2)], expect_tau=1, expect_two=False)
# 2. directed 3-cycle: NO dicuts at all, tau = inf
allok &= show("directed cycle C3", 3, [(0,1),(1,2),(2,0)], expect_tau=float('inf'), expect_two=True)
# 3. diamond s->x,s->y,x->t,y->t : tau = 2, two dijoins = two s-t paths
allok &= show("diamond", 4, [(0,1),(0,2),(1,3),(2,3)], expect_tau=2, expect_two=True)
# 4. near-miss DAG s1->t1, s2->t1, s2->t2 : tau = 1
allok &= show("near-miss DAG", 4, [(0,2),(1,2),(1,3)], expect_tau=1, expect_two=False)
# 5. doubled two-source DAG (from the tau2-robbins sanity check)
allok &= show("doubled s1->t<-s2", 3, [(0,2),(0,2),(1,2),(1,2)], expect_tau=2, expect_two=True)
# 6. single arc: tau=1
allok &= show("single arc", 2, [(0,1)], expect_tau=1, expect_two=False)
# 7. two parallel arcs: tau=2
allok &= show("two parallel arcs", 2, [(0,1),(0,1)], expect_tau=2, expect_two=True)
print("\nALL FIXTURES:", "PASS" if allok else "FAIL")
