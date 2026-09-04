"""Known-answer and randomised checks backing attacks/tau2-complete/README.md.  numerical."""
import itertools, random, unittest
from tau2lib import (dicuts, tau, is_dijoin, condensation, robbins_orientation, robbins_split,
                     check_split, strongly_connected, two_packing_within)


def bridgeless_connected(n, edges):
    """Independent bridge/connectivity test by edge deletion + BFS (not via robbins_orientation)."""
    def comps(skip):
        seen, c = [False] * n, 0
        for s in range(n):
            if seen[s]:
                continue
            c += 1
            seen[s] = True
            st = [s]
            while st:
                v = st.pop()
                for j, (a, b) in enumerate(edges):
                    if j == skip:
                        continue
                    for x, y in ((a, b), (b, a)):
                        if x == v and not seen[y]:
                            seen[y] = True
                            st.append(y)
        return c
    if comps(-1) != 1:
        return False
    return all(comps(j) == 1 for j in range(len(edges)))


def full_pipeline(n, arcs):
    """Condense, check Lemma A, run Theorem R, colour, verify.  Returns True if the theorem's
    conclusion is witnessed; raises if an intermediate lemma fails."""
    assert tau(n, arcs) >= 2
    c, arcs2, keep = condensation(n, arcs)
    # Prop 4.1: same dicuts as arc sets
    d1 = sorted(set(dicuts(n, arcs).values()))
    lift = []
    for C in dicuts(c, arcs2).values():
        m = 0
        for i, k in enumerate(keep):
            if k is not None and (C >> k) & 1:
                m |= 1 << i
        lift.append(m)
    assert d1 == sorted(set(lift)), "condensation correspondence failed"
    assert tau(c, arcs2) == tau(n, arcs)
    # Lemma A on the reduced instance
    assert bridgeless_connected(c, arcs2), "Lemma A failed"
    col2, O = robbins_split(c, arcs2)
    assert O is not None and strongly_connected(c, O), "Theorem R failed"
    assert check_split(c, arcs2, col2), "construction failed on condensation"
    # lift the colouring (arcs inside components -> colour 0) and verify on D directly
    col = [0 if k is None else col2[k] for k in keep]
    J0 = {i for i in range(len(arcs)) if col[i] == 0}
    J1 = {i for i in range(len(arcs)) if col[i] == 1}
    assert J0.isdisjoint(J1) and J0 | J1 == set(range(len(arcs)))
    assert is_dijoin(n, arcs, J0) and is_dijoin(n, arcs, J1)
    return True


class TestFixtures(unittest.TestCase):
    def test_path(self):
        self.assertEqual(tau(3, [(0, 1), (1, 2)]), 1)
        self.assertEqual(sorted(dicuts(3, [(0, 1), (1, 2)]).values()), [0b01, 0b10])

    def test_cycle_has_no_dicut(self):
        self.assertEqual(dicuts(4, [(0, 1), (1, 2), (2, 3), (3, 0)]), {})

    def test_diamond(self):
        arcs = [(0, 1), (0, 2), (1, 3), (2, 3)]
        self.assertEqual(tau(4, arcs), 2)
        self.assertEqual(sorted(dicuts(4, arcs).keys()), [0b0001, 0b0011, 0b0101, 0b0111])

    def test_near_miss(self):
        arcs = [(0, 2), (1, 2), (1, 3)]      # s1=0, s2=1, t1=2, t2=3
        self.assertEqual(tau(4, arcs), 1)
        self.assertEqual(dicuts(4, arcs)[0b0001], 0b001)   # delta+({s1}) = {s1->t1}
        doubled = arcs + arcs
        self.assertEqual(tau(4, doubled), 2)
        self.assertTrue(full_pipeline(4, doubled))

    def test_dicut_requires_no_entering_arc(self):
        # U={0,2} in the path 0->1->2 has 1->2 entering: not a dicut shore
        self.assertNotIn(0b101, dicuts(3, [(0, 1), (1, 2)]))

    def test_disconnected_has_empty_dicut(self):
        self.assertEqual(tau(3, [(0, 1)]), 0)


class TestProof(unittest.TestCase):
    def test_diamond_split(self):
        arcs = [(0, 1), (0, 2), (1, 3), (2, 3)]
        col, O = robbins_split(4, arcs)
        self.assertTrue(strongly_connected(4, O))
        self.assertTrue(check_split(4, arcs, col))
        # the two colour classes are the two s-t paths
        classes = {frozenset(i for i in range(4) if col[i] == c) for c in (0, 1)}
        self.assertEqual(classes, {frozenset({0, 2}), frozenset({1, 3})})

    def test_all_simple_digraphs_up_to_4(self):
        cnt = 0
        for n in (2, 3, 4):
            pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
            for mask in range(1 << len(pairs)):
                arcs = [pairs[k] for k in range(len(pairs)) if (mask >> k) & 1]
                if tau(n, arcs) >= 2:
                    self.assertTrue(full_pipeline(n, arcs))
                    cnt += 1
        self.assertGreater(cnt, 100)

    def test_all_3vertex_multidigraphs_mult2(self):
        pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
        cnt = 0
        for mult in itertools.product((0, 1, 2), repeat=6):
            arcs = [p for p, m in zip(pairs, mult) for _ in range(m)]
            if tau(3, arcs) >= 2:
                self.assertTrue(full_pipeline(3, arcs))
                cnt += 1
        self.assertGreater(cnt, 50)

    def test_random_multidigraphs(self):
        rng = random.Random(152)
        done = 0
        while done < 3000:
            n = rng.randint(3, 7)
            m = rng.randint(n, 3 * n)
            arcs = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
            arcs = [(a, b) for a, b in arcs] + ([(0, 0)] if rng.random() < 0.2 else [])
            if tau(n, arcs) < 2:
                continue
            self.assertTrue(full_pipeline(n, arcs))
            done += 1

    def test_condensation_random(self):
        rng = random.Random(7)
        for _ in range(500):
            n = rng.randint(3, 7)
            arcs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(2, 3 * n))]
            arcs = [(a, b) for a, b in arcs if a != b]
            c, arcs2, keep = condensation(n, arcs)
            d1 = sorted(set(dicuts(n, arcs).values()))
            lift = []
            for C in dicuts(c, arcs2).values():
                m = 0
                for i, k in enumerate(keep):
                    if k is not None and (C >> k) & 1:
                        m |= 1 << i
                lift.append(m)
            self.assertEqual(d1, sorted(set(lift)))


class TestSchrijverFilter(unittest.TestCase):
    def test_schrijver_filter_step_fails(self):
        # diamond + weight-0 arc x->y ; s=0,x=1,y=2,t=3
        arcs = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]
        w = [1, 1, 1, 1, 0]
        self.assertEqual(tau(4, arcs, w), 2)
        self.assertEqual(sorted(dicuts(4, arcs).keys()), [0b0001, 0b0011, 0b0111])
        O = [(0, 1), (2, 0), (3, 1), (2, 3), (1, 2)]          # the orientation of README 6.2
        self.assertTrue(strongly_connected(4, O))
        col = [0 if O[i] == arcs[i] else 1 for i in range(5)]
        self.assertEqual(col, [0, 1, 1, 0, 0])
        self.assertTrue(check_split(4, arcs, col))               # fine when all arcs count ...
        colS = [c if w[i] else -1 for i, c in enumerate(col)]
        self.assertFalse(check_split(4, arcs, colS))             # ... fails restricted to S
        self.assertIsNotNone(two_packing_within(4, arcs, w))     # although a w-packing exists

    def test_positive_weights_are_multidigraphs(self):
        # weight-2 arc == two parallel copies: the split gives a packing respecting w
        arcs = [(0, 1), (0, 1), (1, 2), (1, 2)]
        self.assertTrue(full_pipeline(3, arcs))


if __name__ == "__main__":
    unittest.main()
