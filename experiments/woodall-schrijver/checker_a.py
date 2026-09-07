"""Checker A: exhaustive bitmask enumeration.  Exact integer arithmetic, stdlib only.

DEFINITIONS USED (restated per problems/woodalls-conjecture/RULES.md §4).

Let D = (V, A) be a digraph (loops and parallel arcs allowed) and
w : A -> Z_{>=0}.

  delta^+(U) = { (x,y) in A : x in U, y not in U }
  delta^-(U) = { (x,y) in A : x not in U, y in U }

  U is a DICUT SHORE if  U != {} , U != V , and  delta^-(U) = {} .
  Its DICUT is delta^+(U).  (The condition is delta^-(U) = {}.  It is NOT
  "delta^+(U) != {}" -- that misreading is the error problems/.../RULES.md §4
  warns about.  Note that on a weakly connected D a shore with delta^-(U)={}
  automatically has delta^+(U) != {}; the code asserts this rather than
  assuming it.)

  tau_w(D) = min { w(delta^+(U)) : U a dicut shore },  = +infinity if there is
  no dicut shore at all (e.g. D a directed circuit).

  J subseteq A is a DIJOIN if J meets every dicut.

  A w-PACKING OF DIJOINS of size k is a list J_1,...,J_k of dijoins such that
  every arc a lies in at most w(a) of them.  nu_w(D) is the largest such k.
  In particular an arc of weight 0 lies in NO member of a packing, while it
  still contributes to no dicut weight -- but it does help decide *which*
  vertex sets are dicut shores.  That asymmetry is the whole mechanism.

  Easy direction (not proved here, but the code is consistent with it):
  nu_w <= tau_w always.  Edmonds-Giles conjectured equality.

Arcs are indexed 0..m-1 and arc sets are Python ints used as bitmasks, so all
set algebra is exact.
"""

from itertools import combinations


class Instance:
    def __init__(self, vertices, arcs, weights=None):
        self.V = list(vertices)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.arcs = [(self.idx[t], self.idx[h]) for (t, h, *_rest) in arcs]
        if weights is None:
            weights = [(a[2] if len(a) > 2 else 1) for a in arcs]
        self.w = list(weights)
        assert all(isinstance(x, int) and x >= 0 for x in self.w)
        self.n = len(self.V)
        self.m = len(self.arcs)

    # -- dicuts ---------------------------------------------------------
    def dicuts(self):
        """All (shore_bitmask, dicut_arcmask) pairs.  Enumerates every one of the
        2^n vertex subsets; cost Theta(2^n * m)."""
        out = []
        full = (1 << self.n) - 1
        for U in range(1, full):          # excludes {} (0) and V (full)
            plus = 0
            minus = 0
            for j, (t, h) in enumerate(self.arcs):
                tin = (U >> t) & 1
                hin = (U >> h) & 1
                if tin and not hin:
                    plus |= 1 << j
                elif hin and not tin:
                    minus |= 1 << j
            if minus == 0:
                assert plus != 0, "isolated component: delta^+ and delta^- both empty"
                out.append((U, plus))
        return out

    def weight(self, arcmask):
        s = 0
        for j in range(self.m):
            if (arcmask >> j) & 1:
                s += self.w[j]
        return s

    def tau_w(self):
        cuts = self.dicuts()
        if not cuts:
            return None                    # +infinity
        return min(self.weight(c) for _, c in cuts)

    def minimal_dicuts(self):
        cuts = sorted({c for _, c in self.dicuts()})
        return [c for c in cuts if not any(d != c and (d & c) == d for d in cuts)]

    # -- dijoins --------------------------------------------------------
    def is_dijoin(self, J):
        return all(J & c for _, c in self.dicuts())

    def nu_w(self, kmax=None):
        """Max size of a w-packing, by exhaustive search.

        Uses: an arc of weight 0 is in no member, so every member is a subset of
        S = {a : w(a) >= 1}; and members may be assumed pairwise disjoint only
        when w <= 1.  This routine handles general integer w by branching on, for
        each arc, which members contain it -- exponential, but the instances here
        are small.  For w in {0,1} it degenerates to: partition S into k parts
        (plus a discard part) so that every part is a dijoin."""
        cuts = [c for _, c in self.dicuts()]
        if not cuts:
            return None                    # tau = +infinity too
        if kmax is None:
            kmax = self.tau_w()
        best = 0
        for k in range(1, kmax + 1):
            if self._exists_packing(k, cuts):
                best = k
            else:
                break
        return best

    def _exists_packing(self, k, cuts):
        """Is there a w-packing of size k?  Branch over arcs: arc j is given to a
        subset of the k members of size at most w(j)."""
        m, w = self.m, self.w
        # choices[j] = list of k-bit masks of members that may contain arc j
        choices = []
        for j in range(m):
            cap = min(w[j], k)
            opts = []
            for r in range(cap + 1):
                for comb in combinations(range(k), r):
                    msk = 0
                    for i in comb:
                        msk |= 1 << i
                    opts.append(msk)
            choices.append(opts)
        # member[i] must hit every cut.  Search arc by arc, prune when a cut can
        # no longer be hit by some member.
        cut_arcs = [[j for j in range(m) if (c >> j) & 1] for c in cuts]
        # arcs ordered so that high-weight arcs come first (they are the only
        # ones that can help)
        order = sorted(range(m), key=lambda j: -w[j])
        pos_of = {j: p for p, j in enumerate(order)}
        # for pruning: for each cut, arcs of positive weight in it
        live = [[j for j in ca if w[j] > 0] for ca in cut_arcs]

        hit = [0] * len(cuts)              # bitmask of members that already hit cut i
        full = (1 << k) - 1

        def feasible(p):
            """Can every cut still be hit by every member using arcs at positions >= p?"""
            remaining = set(order[p:])
            for i, ls in enumerate(live):
                if hit[i] == full:
                    continue
                if not any(j in remaining for j in ls):
                    return False
            return True

        def rec(p):
            if p == len(order):
                return all(h == full for h in hit)
            if not feasible(p):
                return False
            j = order[p]
            if w[j] == 0:
                return rec(p + 1)          # weight-0 arcs are in nothing
            for msk in choices[j]:
                changed = []
                for i, c in enumerate(cuts):
                    if (c >> j) & 1 and (hit[i] | msk) != hit[i]:
                        changed.append((i, hit[i]))
                        hit[i] |= msk
                if rec(p + 1):
                    return True
                for i, old in changed:
                    hit[i] = old
            return False

        return rec(0)


def report(name, vertices, arcs):
    I = Instance(vertices, arcs)
    cuts = I.dicuts()
    tau = I.tau_w()
    nu = I.nu_w()
    print(f"--- {name}: n={I.n} m={I.m} dicuts={len(cuts)} "
          f"tau_w={'+inf' if tau is None else tau} "
          f"nu_w={'+inf' if nu is None else nu}")
    return I, tau, nu
