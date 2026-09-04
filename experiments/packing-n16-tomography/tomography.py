#!/usr/bin/env python3
"""6-direction (dodecagonal-norm) tomography for n-point packings in an equilateral
triangle: exact witnesses (upper bounds on M6(n)) and exact Farkas-certified lower
bounds via disjunctive branch-and-cut. Worker T2, issue #97, 2026-08-23.

Setup (re-derived, not inherited from I1's dodeca.py):
  oblique chart e1=(1,0), e2=(1/2,sqrt3/2); point (u,v) is u*e1+v*e2;
  |u*e1+v*e2|^2 = u^2+uv+v^2.  T_a = {u>=0, v>=0, u+v<=a}.
  For a difference D=(du,dv), Cartesian D_c=(du+dv/2, sqrt3*dv/2).  Projections
  onto unit directions at 0,30,...,150 degrees expand to exactly six weighted forms:
    weight sqrt3/2 : |dv|      (90d)   |du+dv|   (30d)   |du|      (150d)
    weight 1/2    : |2du+dv|  (0d)    |du+2dv|  (60d)   |dv-du|   (120d)
  The 12 signed directions are 30d apart, so every unit vector is within 15d of one:
    dod(D) := max_f w_f|L_f(D)| >= cos15 * |D|,   and also dod(D) <= |D|.
  Hence Euclid |pq|>=1  ==>  dod(pq) >= t := cos15,  and
    t*a_n <= M6(n) <= a_n            (a-priori sandwich used as a tripwire).

Lower-bound certification works with RATIONAL thresholds r_f <= t/w_f (verified
exactly in Q(sqrt3)), which only weakens the relaxation, so a certified
infeasibility at side a proves a_n > a outright.  Certificates: at every pruned
leaf a rational Farkas vector y>=0 with  sum_k a*min(z_k,0) > b.y  where z = A^T y,
checked in Fraction arithmetic; the box [0,a]^{2n} is implied by the node's own
containment rows, so small residuals in z are absorbed soundly.

CIRCULARITY GUARD: no value of a_16 / d(16) / s(16) enters any computation below.
The literal 4.47 (certification target) was chosen from I1's *relaxation* search
transcript only.  This file must never read experiments/circle-packing-search/out/.
"""
from fractions import Fraction
from itertools import combinations
import json, math, os, random, sys, time

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

F = Fraction
random.seed(20260823)
np.random.seed(20260823)

# ---------------------------------------------------------------- exact layer
# t = cos15, t^2 = (2+sqrt3)/4.
T_F = math.cos(math.pi / 12.0)
SQ3 = math.sqrt(3.0)

# six forms: coefficient pairs (cu, cv) applied to (du, dv); first three carry
# weight sqrt3/2 (w^2=3/4), last three weight 1/2 (w^2=1/4).
FORMS = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (-1, 1)]
W2 = [F(3, 4)] * 3 + [F(1, 4)] * 3
W_FLOAT = [SQ3 / 2] * 3 + [0.5] * 3


def ge_sqrt3(x):
    """Exact: is rational x >= sqrt3 ?"""
    return x >= 0 and x * x >= 3


def le_sqrt3(x):
    """Exact: is rational x <= sqrt3 ?"""
    return x <= 0 or x * x <= 3


def form_passes_true_t(w2, L):
    """Exact: does w|L| >= t hold?  w2*L^2 >= t^2=(2+sqrt3)/4  <=>  4*w2*L^2-2 >= sqrt3."""
    return ge_sqrt3(4 * w2 * L * L - 2)


def exact_witness_true_t(Q, a):
    """Q: list of (Fraction u, Fraction v).  Exact check: all in T_a and every pair
    has some form with w|L| >= t (TRUE threshold, Q(sqrt3) comparison).
    Returns (ok, first_failure)."""
    for u, v in Q:
        if u < 0 or v < 0 or u + v > a:
            return False, ("containment", (u, v))
    for i, j in combinations(range(len(Q)), 2):
        du = Q[i][0] - Q[j][0]
        dv = Q[i][1] - Q[j][1]
        Ls = [cu * du + cv * dv for cu, cv in FORMS]
        if not any(form_passes_true_t(w2, L) for w2, L in zip(W2, Ls)):
            return False, ("pair", (i, j))
    return True, None


# Rational thresholds r_f <= t/w_f for the certification side.
#   normals: t/w = 2t/sqrt3 = (3sqrt2+sqrt6)/6 = 1.1153550716...
#   sides:   t/w = 2t       = sqrt6+sqrt2)/2  = 1.9318516525...
R_NORMAL = F(1115355, 1000000)
R_SIDE = F(1931851, 1000000)


def verify_thresholds():
    """Exact proofs that R_NORMAL <= 2t/sqrt3 and R_SIDE <= 2t, i.e. that the
    rational-threshold problem RELAXES the true-t problem.
      R_NORMAL <= 2t/sqrt3  <=>  3*R_NORMAL^2 <= 4t^2 = 2+sqrt3  <=>  3R^2-2 <= sqrt3
      R_SIDE   <= 2t        <=>  R_SIDE^2     <= 2+sqrt3         <=>  R^2 -2 <= sqrt3
    Also check both are lower bounds that are TIGHT to <2e-6 (so the weakening is
    negligible), via float only (informational)."""
    assert le_sqrt3(3 * R_NORMAL * R_NORMAL - 2), "R_NORMAL too big: UNSOUND"
    assert le_sqrt3(R_SIDE * R_SIDE - 2), "R_SIDE too big: UNSOUND"
    assert 2 * T_F / SQ3 - float(R_NORMAL) < 2e-6
    assert 2 * T_F - float(R_SIDE) < 2e-6
    return True


R_OF_FORM = [R_NORMAL] * 3 + [R_SIDE] * 3


def exact_witness_rational_t(Q, a):
    """Exact check for the rational-threshold relaxed problem R(a): every pair has
    some form with |L| >= r_f (pure Fraction comparisons)."""
    for u, v in Q:
        if u < 0 or v < 0 or u + v > a:
            return False
    for i, j in combinations(range(len(Q)), 2):
        du = Q[i][0] - Q[j][0]
        dv = Q[i][1] - Q[j][1]
        ok = False
        for (cu, cv), r in zip(FORMS, R_OF_FORM):
            L = cu * du + cv * dv
            if L >= r or -L >= r:
                ok = True
                break
        if not ok:
            return False
    return True


# --------------------------------------------------------- float search layer
def dod_float(du, dv):
    return max(w * abs(cu * du + cv * dv) for w, (cu, cv) in zip(W_FLOAT, FORMS))


def dodmin_float(P):
    return min(
        dod_float(P[i][0] - P[j][0], P[i][1] - P[j][1])
        for i, j in combinations(range(len(P)), 2)
    )


def iterated_lp_search(n, a, restarts=30, iters=40):
    """Best-effort feasibility search for pairwise dod >= t in T_a (float).
    Iterated LP over the currently-active (form, sign) of each pair, multistart.
    Returns (best_min_dod, best_points).  A failed search proves NOTHING."""

    def actives(P):
        act = {}
        for i, j in combinations(range(n), 2):
            du = P[i][0] - P[j][0]
            dv = P[i][1] - P[j][1]
            vals = [w * (cu * du + cv * dv) for w, (cu, cv) in zip(W_FLOAT, FORMS)]
            k = max(range(6), key=lambda f: abs(vals[f]))
            act[(i, j)] = (k, 1.0 if vals[k] >= 0 else -1.0)
        return act

    def lp_step(P):
        # max s s.t. containment, and per pair (w/t)*sign*L >= s
        nv = 2 * n + 1
        c = np.zeros(nv)
        c[-1] = -1.0
        A, b = [], []
        for i in range(n):
            row = np.zeros(nv)
            row[2 * i] = 1
            row[2 * i + 1] = 1
            A.append(row)
            b.append(a)
        for (i, j), (k, s) in actives(P).items():
            cu, cv = FORMS[k]
            w = W_FLOAT[k]
            row = np.zeros(nv)
            row[2 * i] -= s * w / T_F * cu
            row[2 * i + 1] -= s * w / T_F * cv
            row[2 * j] += s * w / T_F * cu
            row[2 * j + 1] += s * w / T_F * cv
            row[-1] = 1.0
            A.append(row)
            b.append(0.0)
        res = linprog(
            c, A_ub=np.array(A), b_ub=np.array(b),
            bounds=[(0, None)] * (2 * n) + [(None, None)], method="highs",
        )
        if not res.success:
            return None
        return [(res.x[2 * i], res.x[2 * i + 1]) for i in range(n)]

    def rand_start():
        P = []
        while len(P) < n:
            u, v = random.uniform(0, a), random.uniform(0, a)
            if u + v <= a:
                P.append((u, v))
        return P

    best, bestP = -1.0, None
    for _ in range(restarts):
        P = rand_start()
        cur = dodmin_float(P)
        for _ in range(iters):
            P2 = lp_step(P)
            if P2 is None:
                break
            m = dodmin_float(P2)
            if m > cur + 1e-12:
                cur, P = m, P2
            else:
                break
        if cur > best:
            best, bestP = cur, P
    return best, bestP


# ------------------------------------------------- branch-and-cut certifier
class BranchAndCut:
    """Certify infeasibility of R(a): n points in T_a, every pair satisfying the
    12-fold disjunction  sign*L_f(p_i-p_j) >= r_f.

    WLOG symmetry rows (sound: relabel any configuration so u+v is nondecreasing):
      (u_i+v_i) - (u_{i+1}+v_{i+1}) <= 0.

    Node LP (floats, decisions only): phase-1  min s  s.t.  Ax - s*1 <= b.
    s* > tol  -> prune, then EXACT rational Farkas check (box absorption).
    s* <= tol -> branch on the most violated unresolved pair's 12 disjuncts,
    unless the LP point already satisfies all pairs -> exact rational-threshold
    witness check -> 'FEASIBLE' verdict (certification impossible at this a).
    """

    def __init__(self, n, a_rat, node_cap=10**6, time_cap=600.0, tag=""):
        self.n = n
        self.aF = F(a_rat)
        self.a = float(self.aF)
        self.node_cap = node_cap
        self.time_cap = time_cap
        self.tag = tag.replace("/", "_")
        self.nodes = 0
        self.leaves_certified = 0
        self.max_depth = 0
        self.t0 = None
        self.pairs = list(combinations(range(n), 2))
        # base rows: -u_i <= 0 ; -v_i <= 0 ; u_i+v_i <= a ; sort rows
        self.base_rows = []  # (coef dict var->int, rhs Fraction)
        for i in range(n):
            self.base_rows.append(({2 * i: -1}, F(0)))
            self.base_rows.append(({2 * i + 1: -1}, F(0)))
            self.base_rows.append(({2 * i: 1, 2 * i + 1: 1}, self.aF))
        for i in range(n - 1):
            self.base_rows.append(
                ({2 * i: 1, 2 * i + 1: 1, 2 * i + 2: -1, 2 * i + 3: -1}, F(0))
            )

    def disjunct_row(self, i, j, f, sgn):
        """Row for  sgn*L_f(p_i - p_j) >= r_f  as  coef.x <= rhs."""
        cu, cv = FORMS[f]
        coef = {}
        for var, c in ((2 * i, cu), (2 * i + 1, cv), (2 * j, -cu), (2 * j + 1, -cv)):
            coef[var] = coef.get(var, 0) - sgn * c
        return (coef, -R_OF_FORM[f])

    def _np_lp(self, rows):
        """Phase-1 LP.  Returns (s_star, x, y) with y >= 0 the row duals."""
        nv = 2 * self.n + 1
        m = len(rows)
        A = np.zeros((m, nv))
        b = np.zeros(m)
        for k, (coef, rhs) in enumerate(rows):
            for var, c in coef.items():
                A[k, var] = float(c)
            A[k, -1] = -1.0
            b[k] = float(rhs)
        c = np.zeros(nv)
        c[-1] = 1.0
        res = linprog(c, A_ub=A, b_ub=b,
                      bounds=[(None, None)] * (2 * self.n) + [(None, None)],
                      method="highs")
        if not res.success:
            return None, None, None
        y = -np.asarray(res.ineqlin.marginals)
        return res.fun, res.x[:-1], y

    def _exact_farkas(self, rows, y):
        """Exact: does rational rounding of y certify infeasibility of rows,
        given the box 0 <= x_k <= a implied by the containment rows?
        Check: y>=0 (clip), z = A^T y, beta = b.y, need sum_k a*min(z_k,0) > beta."""
        for den in (10**6, 10**9, 10**13):
            yF = [max(F(0), F(float(v)).limit_denominator(den)) for v in y]
            z = [F(0)] * (2 * self.n)
            beta = F(0)
            for (coef, rhs), yv in zip(rows, yF):
                if yv == 0:
                    continue
                beta += rhs * yv
                for var, c in coef.items():
                    z[var] += c * yv
            lo = sum(self.aF * zk for zk in z if zk < 0)
            if lo > beta:
                return True
        return False

    def run(self):
        self.t0 = time.time()
        rows = list(self.base_rows)
        try:
            verdict = self._dfs(rows, frozenset(), 0)
        except TimeoutError as e:
            return {"verdict": str(e), "nodes": self.nodes,
                    "leaves_certified": self.leaves_certified,
                    "max_depth": self.max_depth,
                    "seconds": round(time.time() - self.t0, 2)}
        return {"verdict": verdict, "nodes": self.nodes,
                "leaves_certified": self.leaves_certified,
                "max_depth": self.max_depth,
                "seconds": round(time.time() - self.t0, 2)}

    def _dfs(self, rows, resolved, depth):
        self.nodes += 1
        self.max_depth = max(self.max_depth, depth)
        if self.nodes > self.node_cap:
            raise TimeoutError("NODE_CAP")
        if time.time() - self.t0 > self.time_cap:
            raise TimeoutError("TIME_CAP")
        if self.nodes % 2000 == 0:
            self._checkpoint()
        s, x, y = self._np_lp(rows)
        if s is None:
            raise TimeoutError("LP_FAILURE")
        if s > 1e-9:
            if not self._exact_farkas(rows, y):
                raise TimeoutError("FARKAS_UNVERIFIED")
            self.leaves_certified += 1
            return "INFEASIBLE"
        # feasible node: find the unresolved pair with worst best-disjunct margin
        worst, worst_pair = None, None
        for (i, j) in self.pairs:
            if (i, j) in resolved:
                continue
            du = x[2 * i] - x[2 * j]
            dv = x[2 * i + 1] - x[2 * j + 1]
            best = max(
                abs(cu * du + cv * dv) - float(r)
                for (cu, cv), r in zip(FORMS, R_OF_FORM)
            )
            if worst is None or best < worst:
                worst, worst_pair = best, (i, j)
        if worst_pair is None or worst >= 0:
            # LP point may satisfy every remaining pair: exact check the witness
            Q = [(F(x[2 * i]).limit_denominator(10**9),
                  F(x[2 * i + 1]).limit_denominator(10**9)) for i in range(self.n)]
            Q = [(max(F(0), min(u, self.aF)), max(F(0), min(v, self.aF))) for u, v in Q]
            Q = [(u - max(F(0), (u + v - self.aF)) / 2,
                  v - max(F(0), (u + v - self.aF)) / 2) for u, v in Q]
            if exact_witness_rational_t(Q, self.aF):
                return "FEASIBLE"
            if worst_pair is None:
                # all pairs resolved, LP feasible, but rationalization failed the
                # exact check -- treat as unresolved feasibility, certification fails
                return "FEASIBLE_FLOAT_ONLY"
        i, j = worst_pair
        # order the 12 children by margin at x (descending: likely-feasible first)
        du = x[2 * i] - x[2 * j]
        dv = x[2 * i + 1] - x[2 * j + 1]
        kids = []
        for f, ((cu, cv), r) in enumerate(zip(FORMS, R_OF_FORM)):
            L = cu * du + cv * dv
            kids.append((L - float(r), f, 1))
            kids.append((-L - float(r), f, -1))
        kids.sort(reverse=True)
        newres = resolved | {(i, j)}
        for _, f, sgn in kids:
            child_rows = rows + [self.disjunct_row(i, j, f, sgn)]
            v = self._dfs(child_rows, newres, depth + 1)
            if v != "INFEASIBLE":
                return v  # a feasible leaf anywhere kills certification at this a
        return "INFEASIBLE"

    def _checkpoint(self):
        with open(os.path.join(OUT, "bnb_progress_%s.json" % self.tag), "w") as fh:
            json.dump({"tag": self.tag, "n": self.n, "a": str(self.aF),
                       "nodes": self.nodes, "max_depth": self.max_depth,
                       "seconds": round(time.time() - self.t0, 2)}, fh)


# ----------------------------------------------------------------- witnesses
def scaled_lattice_witness(k, spacing):
    """T_k lattice (k+1 points per side, (k+1)(k+2)/2 total) at rational spacing:
    points (i*s, j*s), i,j>=0, i+j<=k, in T_{k*s}.  All neighbor steps are
    parallel to one of the six directions, so pairwise dod = s * (lattice dod),
    and the lattice's minimum dod is 1 (achieved at (1,0),(0,1),(1,-1))."""
    s = F(spacing)
    Q = [(F(i) * s, F(j) * s) for i in range(k + 1) for j in range(k + 1 - i)]
    return Q, k * s


def corners_centroid_witness(a):
    """n=4: three corners + centroid of T_a, a rational.  Centroid=(a/3,a/3)."""
    a = F(a)
    return [(F(0), F(0)), (a, F(0)), (F(0), a), (a / 3, a / 3)], a


# ------------------------------------------------------------------- driver
def log(msg):
    print(msg, flush=True)
    with open(os.path.join(OUT, "run.log"), "a") as fh:
        fh.write(msg + "\n")


def controls():
    log("=== threshold soundness (exact, Q(sqrt3)) ===")
    verify_thresholds()
    log("R_NORMAL=%s <= 2t/sqrt3 and R_SIDE=%s <= 2t : PROVED exactly" %
        (R_NORMAL, R_SIDE))

    log("=== control: hex corner-cheat config must FAIL dod (I1's M3(4)<=3/2 cheat) ===")
    cheat = [(F(0), F(0)), (F(3, 2), F(0)), (F(0), F(3, 2)), (F(1, 2), F(1, 2))]
    ok, why = exact_witness_true_t(cheat, F(3, 2))
    log("cheat accepted? %s (expect False; failing pair %s)" % (ok, why))
    assert not ok

    # SPACING: rational s >= t exactly:  s>=t <=> 4s^2-2 >= sqrt3  (s>0)
    s = F(96593, 100000)
    assert ge_sqrt3(4 * s * s - 2), "spacing below t: witness invalid"
    log("=== exact lattice witnesses at spacing s=%s (>= t proved exactly) ===" % s)
    for k, n, a_n_name, a_n_sq in ((1, 3, "a_3=1", None), (2, 6, "a_6=2", None),
                                   (3, 10, "a_10=3", None), (4, 15, "a_15=4", None)):
        Q, a = scaled_lattice_witness(k, s)
        ok, why = exact_witness_true_t(Q, a)
        log("T_%d lattice: n=%d, a=%s=%.6f, exact dod>=t: %s  (vs %s)" %
            (k, len(Q), a, float(a), ok, a_n_name))
        assert ok and len(Q) == n
    # the n=15 line: M6(15) <= 4s = 3.86372 < 4 = a_15  -- I1's early question
    log("==> M6(15) <= %s = %.6f < 4 = a_15 : the relaxation UNDERSHOOTS the")
    log("    Euclidean value by ~cos15 on lattice configs (I1 early-check: YES).")

    log("=== n=4 corners+centroid witness ===")
    # dod-min of corners+centroid at side a is a/sqrt3 (centroid-corner along a
    # normal), so need a >= sqrt3*t = 1.673033.  Rational a4w just above:
    a4w = F(16731, 10000)
    Q, a = corners_centroid_witness(a4w)
    ok, why = exact_witness_true_t(Q, a)
    log("corners+centroid at a=%s: exact dod>=t: %s  => M6(4) <= %.6f  (< a_4=sqrt3=1.732051)" %
        (a4w, ok, float(a4w)))
    assert ok

    log("=== reverify I1's M6(16) <= 449/100 witness with THIS checker ===")
    with open(os.path.join(HERE, "..", "packing-n16-approaches", "out",
                           "dodeca_best16_fine.json")) as fh:
        d = json.load(fh)
    Q = [(F(u).limit_denominator(10**9), F(v).limit_denominator(10**9))
         for u, v in d["points_uv"]]
    aF = F(449, 100)
    Q = [(max(F(0), min(u, aF)), max(F(0), min(v, aF))) for u, v in Q]
    Q = [(u - max(F(0), (u + v - aF)) / 2, v - max(F(0), (u + v - aF)) / 2)
         for u, v in Q]
    ok, why = exact_witness_true_t(Q, aF)
    log("I1 16-point witness at a=449/100: exact dod>=t: %s" % ok)
    assert ok

    log("=== two-sided branch-and-cut controls, n=4 (target sqrt3*t=1.673033) ===")
    for a, expect in ((F(167, 100), "INFEASIBLE"), (F(1674, 1000), "FEASIBLE")):
        r = BranchAndCut(4, a, node_cap=20000, time_cap=60, tag="ctrl4_%s" % a).run()
        log("n=4 a=%s: %s (expected %s) nodes=%d leaves=%d %.2fs" %
            (a, r["verdict"], expect, r["nodes"], r["leaves_certified"], r["seconds"]))
        assert r["verdict"] == expect, "CONTROL FAILED"
    log("=== two-sided branch-and-cut controls, n=5 (target 2t=1.931852) ===")
    for a, expect in ((F(192, 100), "INFEASIBLE"), (F(1932, 1000), "FEASIBLE")):
        r = BranchAndCut(5, a, node_cap=40000, time_cap=120, tag="ctrl5_%s" % a).run()
        log("n=5 a=%s: %s (expected %s) nodes=%d leaves=%d %.2fs" %
            (a, r["verdict"], expect, r["nodes"], r["leaves_certified"], r["seconds"]))
        assert r["verdict"] == expect, "CONTROL FAILED"
    log("ALL CONTROLS PASSED")
    return True


def gate(n, a_str, node_cap, time_cap):
    a = F(a_str)
    log("=== growth gate: n=%d at a=%s (caps: %d nodes, %ds) ===" %
        (n, a, node_cap, time_cap))
    r = BranchAndCut(n, a, node_cap=node_cap, time_cap=time_cap,
                     tag="gate%d" % n).run()
    log("n=%d a=%s: %s nodes=%d certified_leaves=%d max_depth=%d %.2fs" %
        (n, a, r["verdict"], r["nodes"], r["leaves_certified"],
         r["max_depth"], r["seconds"]))
    with open(os.path.join(OUT, "gate_n%d.json" % n), "w") as fh:
        json.dump({"n": n, "a": a_str, **r}, fh, indent=1)
    return r


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "controls"
    if cmd == "controls":
        controls()
    elif cmd == "gate":
        n, a_str, ncap, tcap = int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
        gate(n, a_str, ncap, tcap)
    elif cmd == "search":
        n, a_str = int(sys.argv[2]), sys.argv[3]
        aF = F(a_str)
        a = float(aF)
        m, P = iterated_lp_search(n, a, restarts=int(sys.argv[4]) if len(sys.argv) > 4 else 30)
        log("search n=%d a=%s: best min dod = %.6f = %.5f*t" % (n, a_str, m, m / T_F))
        if m >= T_F - 1e-9:
            Q = [(F(u).limit_denominator(10**9), F(v).limit_denominator(10**9))
                 for u, v in P]
            Q = [(max(F(0), min(u, aF)), max(F(0), min(v, aF))) for u, v in Q]
            Q = [(u - max(F(0), (u + v - aF)) / 2, v - max(F(0), (u + v - aF)) / 2)
                 for u, v in Q]
            ok, why = exact_witness_true_t(Q, aF)
            log("exact check at a=%s: %s%s" %
                (a_str, ok, "  => M6(%d) <= %s" % (n, a_str) if ok else ""))
            if ok:
                with open(os.path.join(OUT, "witness_n%d_%s.json" % (n, a_str.replace("/", "_"))), "w") as fh:
                    json.dump({"n": n, "a": a_str,
                               "points_uv": [[str(u), str(v)] for u, v in Q]}, fh, indent=1)
