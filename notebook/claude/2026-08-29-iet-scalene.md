# 2026-08-29 — scalene shapes: the spiral-similarity criterion (idea I3)

Worker journal. `claude` (Claude Opus 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane: [`problems/inscribed-equilateral-triangle/attacks/scalene-shapes/`](../../problems/inscribed-equilateral-triangle/attacks/scalene-shapes/README.md).
Kill-criterion written first: [`KILL-CRITERION.md`](../../problems/inscribed-equilateral-triangle/attacks/scalene-shapes/KILL-CRITERION.md).

This journal is the **reproduction record**: the complete source of every program run in the lane
is reproduced below (§B), together with the exact commands and the raw outputs (§C).

---

## A. How the day went, in order, including the wrong turns

1. **Read first, compute later.** Repo `RULES.md` §0/§3/§6/§7, the problem `RULES.md`, the problem
   `README.md` (open item 2 is this lane's target), ideation §I3, and the spiral lane — whose §10
   corollary is explicitly handed to I3 and flagged as the least-checked line in that file.
2. **Wrote `KILL-CRITERION.md` before any code.** Its provenance paragraph is honest about what
   preceded what: the hand derivations (criterion, sharp constant, Lemma A dichotomy, convex
   theorem) were done on paper before the file; every line of *code* came after it.
3. **Derived the criterion.** The key simplification, and the thing that made the whole lane
   computable exactly: parametrise the shape by $w$ with $T = (0,1,w)$; then the six corner-role
   multipliers are $w$, $1-w$, $(w-1)/w$ and their conjugates. **If $w$ is a Gaussian rational,
   all six are Gaussian rational and the entire computation stays in $\mathbb{Q}$.** That is why
   the decider needs no algebraic number field for the scalene search, and only needs
   $\mathbb{Q}(\sqrt3)$ to talk to the committed equilateral decider.
4. **Realised the equilateral case is $\lvert M(w)\rvert = 1$**, isosceles $3$, scalene $6$, and
   that the collapse is exactly $\mu^{-1} = \bar\mu \iff \lvert\mu\rvert = 1$. This is the
   one-line answer to "where is the symmetry lost".
5. **Half-density.** Guessed the ball form fails; found the shell witness $1/(1+k^2)$; then found
   the matching upper bound by (a) a measure-preserving shear that kills the rotation part, (b)
   Fubini over directions, (c) a max-weight independent set on a path with geometric weights.
   Checked the 1-D optimum numerically against an exact DP. Then realised the punchline: it does
   not matter, because the *hypothesis* comes from Lemma A and Lemma A is what breaks.
6. **Lemma A.** Re-derived the equilateral proof, found the exact step that dies ($\lambda(\sigma A)
   = k^2\lambda(A)$ instead of $\lambda(A)$) and noticed that the *expanding* nesting is still
   killed by the same area argument. So the dichotomy is one-sided, not two-sided — a sharper
   statement than I3's prediction.
7. **Spiral tip.** Derived $\Lambda_c(\mu) = \arg\mu + \ln\lvert\mu\rvert/c$ from the direction-set
   normal form, *before* re-reading the spiral lane's §10, then compared: agreement, sign included.
   Then wrote an independent brute-force over $r$ (`spiralcheck.py`) which agrees on 480 random
   parameter sets. **K3 not met**; the spiral lane's least-checked line survives an independent
   check.
8. **A false start that taught the most.** I hand-computed that for $J$ = equilateral triangle and
   $T = (20°,40°,120°)$ every vertex would be exceptional, giving $\lvert E_T\rvert = 3$
   immediately. **It is wrong.** The error: at the two extreme directions of the tangent cone at a
   polygon vertex, the ray meets $J$ in a whole *segment*, not a single point, so the achievable
   ratio $\lvert OQ\rvert/\lvert OP\rvert$ ranges over an unbounded interval and not over a single
   value. Chasing that correction is what produced Theorem C — the convex theorem — which says the
   opposite of what I first thought: on convex curves *every* shape obeys "all but two". Worth
   recording as the day's most useful mistake, and as an instance of exactly the failure the
   problem `RULES.md` §2/§3 warn about (a fluent computation that omits one case).
9. **Built the exact decider** and cross-checked it against the committed equilateral enumerator:
   190 fixtures, 1566 points, 0 disagreements.
10. **A checker bug, caught by the checker aborting.** My witness verifier hard-coded the corner
    correspondence $O\!\to\!0, P\!\to\!1, X\!\to\!w$, valid only for the role $\mu = w$; on the role
    $\mu = 1-w$ it rejected correct witnesses. The decider was right, the checker was wrong. Fixed
    by making the check correspondence-free (sort the three squared side lengths, compare ratios),
    which is also more independent of how the witness was found. Four checkers had already failed
    this session against zero mathematical errors of that kind; this is the fifth.
11. **Searched.** Three passes: a coarse grid (3906 pairs), a raster of the blocked-multiplier
    region per point with a bitmask search over shape space (75 polygons), and a census
    (66 075 pairs). Max $\lvert E_T\rvert$ found: **2**. The raster flagged 5 polygons; all 5 were
    false positives of the float screen and died under exact re-decision (984 shapes).
12. **Classified mechanisms.** 1774 exactly-confirmed exceptional points; 22 of them are *not*
    wedge-blocked. Ran the same scan for the equilateral shape as a control and found non-wedge
    exceptional points there too (4 of 30) — so this is a fact about non-convex curves, not about
    $k \ne 1$. Recorded that way in the README rather than as a scalene phenomenon, which is how I
    first wanted to write it.
13. **Wrote up**, including §12 "where to attack", where my own bet on an error is Theorem C(1)'s
    boundary behaviour — the one branch ($L=0$ at an extreme direction) that no polygon fixture
    exercises.

**Compute:** under 10 minutes of wall clock in total, against the 20-minute self-imposed budget of
K7 and the repo's one hour. Two runs were backgrounded; both were collected. Nothing left running.

**Not done (K8):** the three-tip construction. The obstruction is written up in the lane README
§11.2 and no partial construction is presented as a result.

---

## B. Source

File-ownership note: this lane owns exactly three files (the two in `attacks/scalene-shapes/` and
this journal), so the code is not a tracked `experiments/` directory. It is reproduced here in
full. To run it, save each block below to the named file in one empty directory and run the
commands of §C from that directory; Python **3.11.15**, standard library only except that
`screen.py`/`raster.py`'s *search* heuristics use **numpy 2.4.6** (no decision depends on them).
Seeds are pinned at `20260829`; the decider contains no randomness. A follow-up issue should
promote this to `experiments/inscribed-triangle-scalene/` with a `run.sh`, which is where it
belongs once a worker owns that path.

### `exact.py`

```python
"""Exact arithmetic in K = Q(sqrt 3), and exact plane geometry over K.

Written for the scalene-shapes lane. Independent of
experiments/inscribed-triangle-polygons/ (which is read-only for this lane and
decides only the equilateral case): no code is shared, only the mathematics.

No floats decide anything. float() exists for printing only.
No sympy anywhere.
"""
from fractions import Fraction as F


class K:
    """a + b*sqrt(3), a,b rational.  1 and sqrt3 are Q-independent, so the
    representation is unique and the zero test is syntactic."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    # --- ring ops -----------------------------------------------------
    def __add__(s, o):
        o = mk(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return K(-s.a, -s.b)

    def __sub__(s, o):
        o = mk(o); return K(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return mk(o) - s

    def __mul__(s, o):
        o = mk(o)
        return K(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 3 * s.b * s.b          # norm; zero only if s == 0
        if n == 0:
            raise ZeroDivisionError("K.inv of 0")
        return K(s.a / n, -s.b / n)

    def __truediv__(s, o):
        return s * mk(o).inv()

    def __rtruediv__(s, o):
        return mk(o) * s.inv()

    # --- comparison ---------------------------------------------------
    def is_zero(s):
        return s.a == 0 and s.b == 0

    def sign(s):
        a, b = s.a, s.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # mixed signs: compare a^2 with 3 b^2.  a^2 == 3 b^2 with b != 0 would
        # make sqrt3 rational, so it cannot happen; raise rather than guess.
        lhs, rhs = a * a, 3 * b * b
        if lhs == rhs:
            raise ArithmeticError("a^2 = 3b^2 with b != 0 is impossible")
        big = 1 if lhs > rhs else -1
        return big if a > 0 else -big

    def __eq__(s, o):
        return (s - mk(o)).is_zero()

    def __hash__(s):
        return hash((s.a, s.b))

    def __lt__(s, o):
        return (s - mk(o)).sign() < 0

    def __le__(s, o):
        return (s - mk(o)).sign() <= 0

    def __gt__(s, o):
        return (s - mk(o)).sign() > 0

    def __ge__(s, o):
        return (s - mk(o)).sign() >= 0

    def __float__(s):          # display only
        return float(s.a) + 1.7320508075688772 * float(s.b)

    def __repr__(s):
        if s.b == 0:
            return f"{s.a}"
        return f"({s.a}+{s.b}r3)"


def mk(x):
    return x if isinstance(x, K) else K(x)


ZERO, ONE = K(0), K(1)
R3 = K(0, 1)          # sqrt 3


# ---------------------------------------------------------------------
# points / vectors over K
# ---------------------------------------------------------------------
class P:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = mk(x), mk(y)

    def __add__(s, o): return P(s.x + o.x, s.y + o.y)
    def __sub__(s, o): return P(s.x - o.x, s.y - o.y)
    def __eq__(s, o):  return s.x == o.x and s.y == o.y
    def __hash__(s):   return hash((s.x, s.y))
    def __repr__(s):   return f"({float(s.x):.6g},{float(s.y):.6g})"
    def exact(s):      return f"({s.x!r},{s.y!r})"

    def scal(s, t):    return P(s.x * t, s.y * t)


def cross(u, v): return u.x * v.y - u.y * v.x
def dot(u, v):   return u.x * v.x + u.y * v.y
def d2(p, q):    return dot(p - q, p - q)


# complex numbers over K, as pairs
class C:
    """p + q i with p,q in K."""
    __slots__ = ("p", "q")

    def __init__(s, p, q): s.p, s.q = mk(p), mk(q)
    def __mul__(s, o):     return C(s.p * o.p - s.q * o.q, s.p * o.q + s.q * o.p)
    def __sub__(s, o):     return C(s.p - o.p, s.q - o.q)
    def __add__(s, o):     return C(s.p + o.p, s.q + o.q)
    def conj(s):           return C(s.p, -s.q)
    def norm2(s):          return s.p * s.p + s.q * s.q

    def inv(s):
        n = s.norm2()
        if n.is_zero():
            raise ZeroDivisionError
        return C(s.p / n, -s.q / n)

    def __truediv__(s, o): return s * o.inv()
    def __eq__(s, o):      return s.p == o.p and s.q == o.q
    def __hash__(s):       return hash((s.p, s.q))
    def __repr__(s):       return f"{float(s.p):.6g}{float(s.q):+.6g}i"
    def exact(s):          return f"{s.p!r}{'+' if s.q.sign()>=0 else ''}{s.q!r}i"


CONE, CZERO = C(1, 0), C(0, 0)


def apply(mu, O, z):
    """spiral similarity  z |-> O + mu (z - O)."""
    v = z - O
    return P(O.x + mu.p * v.x - mu.q * v.y, O.y + mu.q * v.x + mu.p * v.y)


# ---------------------------------------------------------------------
# exact segment intersection
# ---------------------------------------------------------------------
def seg_intersect(a, b, c, d):
    """Intersection of closed segments [a,b] and [c,d].
    Returns ('empty',), ('point', p) or ('segment', p, q)."""
    r, s = b - a, d - c
    den = cross(r, s)
    qp = c - a
    if not den.is_zero():
        t = cross(qp, s) / den
        u = cross(qp, r) / den
        if ZERO <= t <= ONE and ZERO <= u <= ONE:
            return ("point", P(a.x + r.x * t, a.y + r.y * t))
        return ("empty",)
    # parallel
    if not cross(qp, r).is_zero():
        return ("empty",)
    rr = dot(r, r)
    if rr.is_zero():                       # a == b, degenerate
        raise ValueError("zero-length segment")
    t0 = dot(qp, r) / rr
    t1 = t0 + dot(s, r) / rr
    lo, hi = (t0, t1) if t0 <= t1 else (t1, t0)
    lo = lo if lo > ZERO else ZERO
    hi = hi if hi < ONE else ONE
    if hi < lo:
        return ("empty",)
    pl = P(a.x + r.x * lo, a.y + r.y * lo)
    if lo == hi:
        return ("point", pl)
    ph = P(a.x + r.x * hi, a.y + r.y * hi)
    return ("segment", pl, ph)


def edges(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n)]


def is_simple(poly):
    n = len(poly)
    if n < 3:
        return False
    E = edges(poly)
    for i, (a, b) in enumerate(E):
        if a == b:
            return False
    for i in range(n):
        for j in range(i + 1, n):
            a, b = E[i]; c, d = E[j]
            res = seg_intersect(a, b, c, d)
            adjacent = (j == i + 1) or (i == 0 and j == n - 1)
            if adjacent:
                shared = poly[j] if j == i + 1 else poly[0]
                if res[0] != "point" or not (res[1] == shared):
                    return False
            else:
                if res[0] != "empty":
                    return False
    return True


def on_polygon(poly, z):
    for a, b in edges(poly):
        u = b - a
        if cross(u, z - a).is_zero():
            t_num = dot(z - a, u)
            if ZERO <= t_num <= dot(u, u):
                return True
    return False
```

### `decide.py`

```python
"""Exact decision of T-goodness of a point O on a rational (or Q(sqrt3)) polygon.

Criterion (derived in the lane README, sec. 1):
  O is a vertex of a triangle inscribed in J and similar to T, in the corner
  role with multiplier mu, iff  J n sigma(J) contains a point other than O,
  where sigma(z) = O + mu (z - O).
"""
from exact import *


# ---------------------------------------------------------------------
# shapes: T = triangle (0, 1, w),  w in K(i) = Q(sqrt3)(i)
# ---------------------------------------------------------------------
def multipliers(w):
    """The six corner-role multipliers of the shape T = (0,1,w).

    corner 0: 1 |-> w         mu = w
    corner 1: 0 |-> w         mu = 1 - w
    corner w: 0 |-> 1         mu = (w-1)/w
    each with its mirror (complex conjugate).  mu and 1/mu give the same
    condition (swap the two neighbours), so these six representatives cover
    all 12 maps.
    """
    m1 = w
    m2 = CONE - w
    m3 = (w - CONE) / w
    out = [m1, m2, m3, m1.conj(), m2.conj(), m3.conj()]
    return out


def shape_sides2(w):
    """squared side lengths of T = (0,1,w), in the order |01|,|0w|,|1w|."""
    return (K(1), w.norm2(), (w - CONE).norm2())


def is_scalene(w):
    a, b, c = shape_sides2(w)
    return a != b and b != c and a != c


def is_nondegenerate(w):
    return not w.q.is_zero()


# ---------------------------------------------------------------------
# the decision
# ---------------------------------------------------------------------
def role_witness(poly, O, mu):
    """Return X != O in J n sigma(J), or None."""
    E = edges(poly)
    SE = [(apply(mu, O, a), apply(mu, O, b)) for (a, b) in E]
    for (a, b) in E:
        for (c, d) in SE:
            res = seg_intersect(a, b, c, d)
            if res[0] == "point":
                if not (res[1] == O):
                    return res[1]
            elif res[0] == "segment":
                if not (res[1] == O):
                    return res[1]
                if not (res[2] == O):
                    return res[2]
    return None


def verify_witness(poly, O, w, mu, X):
    """Independent check that X really certifies a T-similar inscribed triangle.

    Does NOT trust the construction: it recomputes P, checks membership on the
    polygon from scratch, checks distinctness, and checks SSS similarity to
    T = (0,1,w) by comparing all three squared side ratios.
    """
    Pp = apply(mu.inv(), O, X)          # sigma^{-1}(X)
    if not on_polygon(poly, X):
        return False, "X not on J"
    if not on_polygon(poly, Pp):
        return False, "P not on J"
    if X == O or Pp == O or X == Pp:
        return False, "degenerate"
    # SSS similarity, correspondence-free: sort both triples of squared sides
    # (similar triangles have their sides in the same order) and check
    # proportionality exactly.  mu is not used here beyond recovering P.
    tri = sorted([d2(O, Pp), d2(O, X), d2(Pp, X)])
    sh = sorted(list(shape_sides2(w)))
    if not (tri[0] * sh[1] == tri[1] * sh[0]):
        return False, "side ratio 0:1 wrong"
    if not (tri[0] * sh[2] == tri[2] * sh[0]):
        return False, "side ratio 0:2 wrong"
    return True, "ok"


def decide(poly, O, w, want_witness=True):
    """Return (good?, dict role -> witness or None)."""
    res = {}
    good = False
    for i, mu in enumerate(multipliers(w)):
        X = role_witness(poly, O, mu)
        if X is not None:
            ok, msg = verify_witness(poly, O, w, mu, X)
            if not ok:
                raise AssertionError(f"witness failed verification: {msg}")
            good = True
        res[i] = X
        if good and not want_witness:
            break
    return good, res


# convenient shape constructors -----------------------------------------
def w_equilateral():
    """e^{i 60 deg} = 1/2 + (sqrt3/2) i -- the equilateral shape."""
    return C(K(F"1/2"), K(0, F"1/2"))


def w_gauss(px, py):
    """Gaussian-rational w = px + py i (everything then lives in Q)."""
    return C(K(px), K(py))
```

### `angles.py`

```python
"""Exact angle comparisons.  An angle in [0,180] is represented by (cos-numer,
cos-denom-square) i.e. by A/sqrt(B) = cos theta with B > 0 -- monotone, so
comparing angles is comparing cosines the other way round."""
from exact import *


def cmp_cos(A, B, Cc, D):
    """sign of A/sqrt(B) - Cc/sqrt(D), with B, D > 0 in K."""
    sa, sc = A.sign(), Cc.sign()
    if sa != sc:
        return 1 if sa > sc else -1
    if sa == 0:
        return 0
    lhs, rhs = A * A * D, Cc * Cc * B
    d = (lhs - rhs).sign()
    return d if sa > 0 else -d


def cos_of_vertex(poly, i):
    """(A,B) with cos(interior angle at vertex i) = A/sqrt(B), for a CONVEX polygon
    (for a reflex vertex this returns the cosine of the unsigned angle, which is
    not the interior angle -- callers must handle reflexness themselves)."""
    n = len(poly)
    O = poly[i]
    u = poly[(i - 1) % n] - O
    v = poly[(i + 1) % n] - O
    return dot(u, v), dot(u, u) * dot(v, v)


def cos_of_mult(mu):
    """(A,B) with cos|arg mu| = A/sqrt(B)."""
    return mu.p, mu.norm2()


def cmp_vertex_angle_to_mult(poly, i, mu):
    """-1 / 0 / +1  as  gamma(O)  <  =  >  |arg mu|."""
    A, B = cos_of_vertex(poly, i)
    Cc, D = cos_of_mult(mu)
    # gamma < |arg mu|  <=>  cos gamma > cos|arg mu|
    c = cmp_cos(A, B, Cc, D)
    return -c


def orient2(poly):
    s = ZERO
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        s = s + (a.x * b.y - b.x * a.y)
    return s.sign()


def is_convex(poly):
    n = len(poly)
    o = orient2(poly)
    for i in range(n):
        a, b, c = poly[i], poly[(i + 1) % n], poly[(i + 2) % n]
        s = cross(b - a, c - b).sign()
        if s == 0 or s != o:
            return False
    return True


def is_reflex(poly, i, o=None):
    n = len(poly)
    if o is None:
        o = orient2(poly)
    a, b, c = poly[(i - 1) % n], poly[i], poly[(i + 1) % n]
    s = cross(b - a, c - b).sign()
    return s != 0 and s != o
```

### `polys.py`

```python
"""Exact simple-polygon families for the scalene hunt.  Every polygon is
verified simple by the exact is_simple() before use."""
import random
from fractions import Fraction as F
from exact import *
from angles import is_convex, orient2


def _angle_key(c, p):
    """exact sort key for direction of p-c: (half, ) with cross-product comparator"""
    v = p - c
    half = 0 if (v.y.sign() > 0 or (v.y.sign() == 0 and v.x.sign() > 0)) else 1
    return (half, v)


def star_shaped(pts, c):
    """sort pts by direction about c -> star-shaped, hence simple, polygon."""
    import functools
    def cmp(p, q):
        u, v = p - c, q - c
        hp = 0 if (u.y.sign() > 0 or (u.y.sign() == 0 and u.x.sign() > 0)) else 1
        hq = 0 if (v.y.sign() > 0 or (v.y.sign() == 0 and v.x.sign() > 0)) else 1
        if hp != hq: return -1 if hp < hq else 1
        s = cross(u, v).sign()
        if s != 0: return -1 if s > 0 else 1
        return 0
    out = sorted(pts, key=functools.cmp_to_key(cmp))
    for i in range(len(out)):
        if cross(out[i]-c, out[(i+1) % len(out)]-c).is_zero():
            return None
    return out


def rand_star(rng, n, span=30):
    for _ in range(40):
        c = P(0, 0)
        pts = []
        for _ in range(n):
            while True:
                p = P(F(rng.randint(-span, span)), F(rng.randint(-span, span)))
                if not (p.x.is_zero() and p.y.is_zero()):
                    break
            pts.append(p)
        poly = star_shaped(pts, c)
        if poly and len(poly) == n and is_simple(poly):
            return poly
    return None


def spike_star(k, R, rho, rng=None, jitter=0):
    """k outward spikes.  Tips at radius ~R, valleys at ~rho, on rational points
    obtained from the rational rotation (3+4i)/5 applied to a base point --
    exact, no trigonometry."""
    # rational rotation by arctan(4/3) ~ 53.13 deg
    rot = C(K(F(3, 5)), K(F(4, 5)))
    tips, vals = [], []
    z = C(K(R), K(0))
    for j in range(k):
        tips.append(P(z.p, z.q))
        z = z * rot
    z = C(K(rho), K(0)) * C(K(F(3, 5)), K(F(4, 5)))   # offset half-ish
    # place valleys between consecutive tips: use midpoint direction scaled
    out = []
    for j in range(k):
        t1 = tips[j]; t2 = tips[(j+1) % k]
        m = P((t1.x + t2.x) / K(2), (t1.y + t2.y) / K(2))
        # scale m to radius factor rho/|m|-ish: just scale by the rational rho
        out.append(t1)
        out.append(P(m.x * K(rho), m.y * K(rho)))
    return out if is_simple(out) else None


def spiral_poly(steps, s, arms=2, close=True):
    """Polygonal two-armed logarithmic spiral with EXACT rational vertices:
    z_{n+1} = s*(3+4i)/5 * z_n, i.e. rotation by arctan(4/3) and scaling by s."""
    mu = C(K(s * F(3, 5)), K(s * F(4, 5)))
    z = C(K(1), K(0))
    arm1 = []
    for _ in range(steps):
        arm1.append(P(z.p, z.q))
        z = z * mu
    tipish = arm1[-1]
    # second arm = first arm rotated by the rational rotation (5+12i)/13 (~67.4 deg)
    rot = C(K(F(5, 13)), K(F(12, 13)))
    arm2 = []
    for p in arm1:
        w = C(p.x, p.y) * rot
        arm2.append(P(w.p, w.q))
    poly = arm1 + arm2[::-1]
    return poly if is_simple(poly) else None


def comb(teeth, w=F(1), h=F(6), gap=F(1)):
    pts = []
    x = F(0)
    pts.append(P(F(0), F(0)))
    for t in range(teeth):
        pts.append(P(x, F(0)))
        pts.append(P(x, h))
        pts.append(P(x + w, h))
        pts.append(P(x + w, F(0)))
        x = x + w + gap
    pts.append(P(x, F(0)))
    pts.append(P(x, -F(2)))
    pts.append(P(F(0), -F(2)))
    ded = []
    for p in pts:
        if not ded or not (ded[-1] == p):
            ded.append(p)
    if ded[0] == ded[-1]: ded.pop()
    return ded if is_simple(ded) else None
```

### `screen.py`

```python
"""Float PRE-SCREEN only.  Decides nothing: every candidate it emits is
re-decided exactly by decide.py before being reported (KILL-CRITERION K6)."""
import math

def fmul(mu, O, z):
    p, q = mu; ox, oy = O; x, y = z[0]-ox, z[1]-oy
    return (ox + p*x - q*y, oy + q*x + p*y)

def fseg(a, b, c, d):
    """approximate intersection point(s) of segments; returns list of points."""
    rx, ry = b[0]-a[0], b[1]-a[1]
    sx, sy = d[0]-c[0], d[1]-c[1]
    den = rx*sy - ry*sx
    qx, qy = c[0]-a[0], c[1]-a[1]
    if abs(den) > 1e-12:
        t = (qx*sy - qy*sx)/den
        u = (qx*ry - qy*rx)/den
        if -1e-12 <= t <= 1+1e-12 and -1e-12 <= u <= 1+1e-12:
            return [(a[0]+rx*t, a[1]+ry*t)]
        return []
    if abs(qx*ry - qy*rx) > 1e-9:
        return []
    rr = rx*rx + ry*ry
    if rr == 0: return []
    t0 = (qx*rx + qy*ry)/rr
    t1 = t0 + (sx*rx + sy*ry)/rr
    lo, hi = min(t0, t1), max(t0, t1)
    lo, hi = max(lo, 0.0), min(hi, 1.0)
    if hi < lo: return []
    return [(a[0]+rx*lo, a[1]+ry*lo), (a[0]+rx*hi, a[1]+ry*hi)]

def screen_good(fpoly, O, mus, tol):
    E = [(fpoly[i], fpoly[(i+1) % len(fpoly)]) for i in range(len(fpoly))]
    for mu in mus:
        SE = [(fmul(mu, O, a), fmul(mu, O, b)) for (a, b) in E]
        for (a, b) in E:
            for (c, d) in SE:
                for z in fseg(a, b, c, d):
                    if math.hypot(z[0]-O[0], z[1]-O[1]) > tol:
                        return True
    return False
```

### `raster.py`

```python
"""Float RASTER SEARCH (search only; every candidate is re-decided exactly).

For O in J let  D = {z - O : z in J, z != O}  and
    G(O) = { d2/d1 : d1,d2 in D }   ("achievable multipliers").
O is T-good iff M(T) meets G(O), by the criterion of the lane README sec.1.
In log-polar coordinates mu = e^{u+i th}, G(O) is the DIFFERENCE SET of the
log-polar image of D.  We sample D, rasterise the difference set, and take the
complement as an OUTER approximation of the blocked set B(O) = C* \\ G(O)
(sampling can only shrink G, hence only grow the reported B -- the error is in
the safe direction for a screen).
"""
import numpy as np

NU, NT = 240, 720            # raster: u in [-6,6] (0.05), theta 0.5 deg
UMIN, UMAX = -6.0, 6.0


def _u_idx(u):
    return np.clip(((u - UMIN) / (UMAX - UMIN) * NU).astype(np.int64), 0, NU - 1)


def _t_idx(t):
    return (np.mod(t, 2 * np.pi) / (2 * np.pi) * NT).astype(np.int64) % NT


def sample_curve(fpoly, O, geo=28, uni=60, rho=0.62):
    """points of J sampled with geometric refinement toward every vertex."""
    xs, ys = [], []
    n = len(fpoly)
    ts = list(np.linspace(0.0, 1.0, uni, endpoint=False))
    g = [rho ** k for k in range(1, geo)]
    ts += g + [1.0 - t for t in g]
    ts = np.array(sorted(set(ts)))
    for i in range(n):
        ax, ay = fpoly[i]
        bx, by = fpoly[(i + 1) % n]
        xs.append(ax + (bx - ax) * ts)
        ys.append(ay + (by - ay) * ts)
    x = np.concatenate(xs) - O[0]
    y = np.concatenate(ys) - O[1]
    r2 = x * x + y * y
    m = r2 > 0
    x, y, r2 = x[m], y[m], r2[m]
    u = 0.5 * np.log(r2)
    th = np.arctan2(y, x)
    return u, th


def blocked_mask(fpoly, O, dilate=1):
    """boolean raster [NU,NT]: True where mu = e^{u+i th} is (approximately) BLOCKED."""
    u, th = sample_curve(fpoly, O)
    # difference set, chunked
    hit = np.zeros((NU, NT), dtype=bool)
    m = len(u)
    step = max(1, 4_000_000 // max(m, 1))
    for s in range(0, m, step):
        du = u[s:s + step][:, None] - u[None, :]
        dt = th[s:s + step][:, None] - th[None, :]
        du = du.ravel(); dt = dt.ravel()
        k = (du >= UMIN) & (du <= UMAX)
        if not k.any():
            continue
        hit[_u_idx(du[k]), _t_idx(dt[k])] = True
    # dilate the achievable set => shrink the blocked set (screen stays safe)
    for _ in range(dilate):
        h = hit.copy()
        h[1:, :] |= hit[:-1, :]; h[:-1, :] |= hit[1:, :]
        h |= np.roll(hit, 1, axis=1); h |= np.roll(hit, -1, axis=1)
        hit = h
    return ~hit


def mult_cells(W):
    """W: complex array of multipliers -> (iu, it) raster indices."""
    u = np.log(np.abs(W))
    t = np.angle(W)
    return _u_idx(u), _t_idx(t)
```

### `mechanism.py`

```python
"""Exact classification of an exceptional point as WEDGE or NON-WEDGE.

O is wedge-blocked for T iff the whole polygon lies in a closed convex cone at O
of opening < phi_min(T).  Exact test: search pairs of vertex directions spanning
a cone containing every vertex direction, and compare its opening with phi_min
by an exact cosine comparison.
"""
import sys
sys.path.insert(0, '.')
from exact import *
from decide import multipliers
from angles import cmp_cos, cos_of_mult

def phi_min_mult(w):
    ms = multipliers(w)[:3]; best = ms[0]
    for m in ms[1:]:
        A,B = cos_of_mult(m); Cc,D = cos_of_mult(best)
        if cmp_cos(A,B,Cc,D) > 0: best = m
    return best

def wedge_blocked(poly, O, w):
    vs = [p - O for p in poly if not (p == O)]
    # also the two edge directions from O if O is interior to an edge
    if not vs: return None
    mmin = phi_min_mult(w)
    Cc, D = cos_of_mult(mmin)
    n = len(vs)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            if cross(vs[i], vs[j]).sign() <= 0: continue     # need ccw, < 180
            ok = True
            for k in range(n):
                if cross(vs[i], vs[k]).sign() < 0 or cross(vs[k], vs[j]).sign() < 0:
                    ok = False; break
            if not ok: continue
            A = dot(vs[i], vs[j]); B = dot(vs[i],vs[i]) * dot(vs[j],vs[j])
            # cone opening < phi_min  <=>  cos(opening) > cos(phi_min)
            if cmp_cos(A, B, Cc, D) > 0:
                return True
    return False
```

### `hunt.py`

```python
"""The hunt: look for a curve J and a scalene shape T with |E_T(J)| >= 3.

Float pre-screen (screen.py) narrows candidates; every reported verdict is
re-decided exactly by decide.py.  Seeds pinned.  See KILL-CRITERION.md.
"""
import sys, time, random, json, math
sys.path.insert(0, ".")
from fractions import Fraction as F
from exact import *
from decide import *
from angles import *
from polys import *
from screen import screen_good

SEED = 20260829
rng = random.Random(SEED)

def fpoly_of(poly):
    return [(float(p.x), float(p.y)) for p in poly]

def fmu(mu):
    return (float(mu.p), float(mu.q))

def shape_grid(N=6, dens=4):
    """Gaussian-rational shapes w = a/dens + (b/dens) i, Im w > 0, plus wide ones."""
    out = []
    for a in range(-N*dens, N*dens+1):
        for b in range(1, N*dens+1):
            w = w_gauss(F(a, dens), F(b, dens))
            if is_nondegenerate(w) and is_scalene(w):
                out.append(w)
    return out

def candidates(poly, nmid=1):
    """points of J to test: all vertices, plus edge midpoints."""
    pts = list(poly)
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        for k in range(1, nmid+1):
            t = K(F(k, nmid+1))
            pts.append(P(a.x + (b.x-a.x)*t, a.y + (b.y-a.y)*t))
    return pts

def hunt(polys, shapes, tol_rel=1e-9, want=3, log=None, budget=None):
    t0 = time.time()
    hits = []
    best = 0
    stats = {"pairs": 0, "screened_exc": 0, "exact_exc": 0}
    for pname, poly in polys:
        fp = fpoly_of(poly)
        diam = max(math.hypot(a[0]-b[0], a[1]-b[1]) for a in fp for b in fp)
        tol = tol_rel * max(diam, 1.0)
        cands = candidates(poly)
        fcands = [(float(p.x), float(p.y)) for p in cands]
        for w in shapes:
            stats["pairs"] += 1
            mus = [fmu(m) for m in multipliers(w)]
            sc = [i for i, fo in enumerate(fcands) if not screen_good(fp, fo, mus, tol)]
            if len(sc) < want:
                if len(sc) > best: best = len(sc)
                continue
            stats["screened_exc"] += len(sc)
            exc = []
            for i in sc:
                good, roles = decide(poly, cands[i], w)
                if not good:
                    exc.append(i)
            stats["exact_exc"] += len(exc)
            if len(exc) > best: best = len(exc)
            if len(exc) >= want:
                hits.append({"poly": pname, "w": w.exact(), "points": [cands[i].exact() for i in exc]})
                if log: print("HIT", pname, w, [cands[i] for i in exc], flush=True)
        if budget and time.time()-t0 > budget:
            print(f"  budget reached after {pname}", flush=True)
            break
    return hits, best, stats, time.time()-t0
```

### `crosscheck.py`

```python
"""K1: my general-T decider, specialised to mu = e^{i60}, versus the committed
equilateral decider, on the committed decider's own battery.

Reads and runs experiments/inscribed-triangle-polygons/ ; modifies nothing there.
"""
import sys, time, json
sys.path.insert(0, ".")
sys.path.insert(0, "../../experiments/inscribed-triangle-polygons")

import exact as X
from decide import decide, w_equilateral
import fixtures as FX
import geom as G

def conv(pt):
    a, b = pt
    return X.P(X.K(a.a, a.b), X.K(b.a, b.b))

w = w_equilateral()
bat = FX.battery()
print(f"{len(bat)} fixtures")
t0 = time.time()
n_pts = 0
disagree = []
for f in bat:
    poly_theirs = f["poly"]
    poly_mine = [conv(p) for p in poly_theirs]
    assert X.is_simple(poly_mine), f["name"]
    for i, O in enumerate(poly_theirs):
        mine = decide(poly_mine, conv(O), w)[0]
        theirs = G.decide_good(poly_theirs, O)["good"]
        n_pts += 1
        if mine != theirs:
            disagree.append((f["name"], i, mine, theirs))
    # also edge midpoints, which their sample_edge_point covers
    E = G.edges(poly_theirs)
    for j, (A, B) in enumerate(E):
        M = G.sample_edge_point(A, B, G.Fraction(1, 2)) if hasattr(G, "Fraction") else None
        if M is None:
            from fractions import Fraction as F
            M = G.sample_edge_point(A, B, F(1, 2))
        mine = decide(poly_mine, conv(M), w)[0]
        theirs = G.decide_good(poly_theirs, M)["good"]
        n_pts += 1
        if mine != theirs:
            disagree.append((f["name"], f"mid{j}", mine, theirs))
print(f"points compared: {n_pts}   disagreements: {len(disagree)}   {time.time()-t0:.1f}s")
for d in disagree[:20]:
    print("  DISAGREE", d)
json.dump({"points": n_pts, "disagreements": disagree}, open("out_crosscheck.json", "w"), indent=1)
```

### `test_convex.py`

```python
"""K2: does  O T-exceptional  <=>  gamma(O) < phi_min(T)  hold on convex polygons?"""
import sys, time, random
sys.path.insert(0, ".")
from fractions import Fraction as F
from exact import *
from decide import *
from angles import *

def phi_min_index(w):
    """index into multipliers() of the smallest |arg mu| among the three corners."""
    ms = multipliers(w)[:3]
    best = 0
    for i in range(1, 3):
        A, B = cos_of_mult(ms[i]); Cc, D = cos_of_mult(ms[best])
        if cmp_cos(A, B, Cc, D) > 0:      # bigger cosine = smaller angle
            best = i
    return best

def hull(pts):
    pts = sorted(set((p.x, p.y) for p in pts), key=lambda t: (float(t[0]), float(t[1])))
    pts = [P(x, y) for (x, y) in pts]
    if len(pts) < 3: return None
    def half(ps):
        st = []
        for p in ps:
            while len(st) >= 2 and cross(st[-1] - st[-2], p - st[-1]).sign() <= 0:
                st.pop()
            st.append(p)
        return st
    lo = half(pts); up = half(pts[::-1])
    h = lo[:-1] + up[:-1]
    return h if len(h) >= 3 else None

rng = random.Random(20260829)
shapes = [w_gauss(F(a), F(b)) for (a, b) in
          [(F(1,2),F(1,3)), (2,1), (4,1), (F(1,3),3), (-1,2), (F(3,2),F(1,5)),
           (F(1,10),F(1,10)), (5,F(1,2)), (-2,F(1,4)), (F(7,3),F(5,2))]]
shapes.append(w_equilateral())
polys = []
# committed-style convex fixtures plus random hulls
polys.append([P(0,0),P(1,0),P(1,1),P(0,1)])
polys.append([P(0,0),P(100,0),P(50,1)])
polys.append([P(0,0),P(1000,0),P(500,1)])
polys.append([P(0,0),P(7,1),P(9,6),P(4,9),P(-1,4)])
polys.append([P(0,0),P(10,0),P(9,1)])
polys.append([P(0,0),P(1,0),P(0,F(1,1000))])
for s in range(60):
    pts = [P(F(rng.randint(-30,30)), F(rng.randint(-30,30))) for _ in range(rng.randint(3,8))]
    h = hull(pts)
    if h and is_simple(h) and is_convex(h):
        polys.append(h)
print(len(polys), "convex polygons,", len(shapes), "shapes")
t0=time.time(); bad=[]; n=0; cnt_exc={}
for pi,poly in enumerate(polys):
    for si,w in enumerate(shapes):
        j = phi_min_index(w)
        mmin = multipliers(w)[j]
        exc = 0
        for i,O in enumerate(poly):
            good,_ = decide(poly,O,w)
            c = cmp_vertex_angle_to_mult(poly,i,mmin)   # -1: gamma<phi_min
            pred_good = (c >= 0)
            n += 1
            if good != pred_good:
                bad.append((pi,si,i,good,pred_good,c))
            if not good: exc += 1
        # edge midpoints: gamma = 180 > phi_min always, predict good
        for i in range(len(poly)):
            M = P((poly[i].x+poly[(i+1)%len(poly)].x)/K(2),
                  (poly[i].y+poly[(i+1)%len(poly)].y)/K(2))
            good,_ = decide(poly,M,w); n += 1
            if not good: bad.append((pi,si,f"mid{i}",good,True,None))
        cnt_exc[exc] = cnt_exc.get(exc,0)+1
print(f"points {n}, mismatches {len(bad)}, {time.time()-t0:.1f}s")
print("distribution of #exceptional vertices per (convex polygon, shape):", dict(sorted(cnt_exc.items())))
for b in bad[:15]: print("  MISMATCH", b)
```

### `run_raster.py`

```python
import sys, time, math, json
sys.path.insert(0, '.')
import numpy as np
from hunt import *
import raster as R

def build_polys():
    polys=[]
    polys.append(("tri-30-30-120", [P(-1,0),P(1,0),P(0,K(0,F(1,3)))]))
    polys.append(("sliver", [P(0,0),P(100,0),P(50,1)]))
    polys.append(("square", [P(0,0),P(1,0),P(1,1),P(0,1)]))
    polys.append(("thinY", [P(0,0),P(60,1),P(60,-1),P(1,-2),P(-30,-52),P(-32,-50),
                            P(-1,1),P(-30,53),P(-32,51)]))
    for k in (3,4,5,6,7):
        for rho in (F(1,5),F(1,4),F(1,3),F(1,2),F(2,3)):
            s = spike_star(k, F(10), rho)
            if s: polys.append((f"spike{k}-{rho}", s))
    for st,s in ((4,F(4,5)),(5,F(4,5)),(5,F(3,4)),(6,F(2,3)),(7,F(1,2)),(8,F(2,5))):
        sp = spiral_poly(st, s)
        if sp: polys.append((f"spiral{st}-{s}", sp))
    for t in (2,3,4):
        c = comb(t)
        if c: polys.append((f"comb{t}", c))
    for i in range(40):
        p = rand_star(rng, rng.randint(5,12))
        if p: polys.append((f"rand{i}", p))
    return polys

polys = build_polys()
print(len(polys),"polygons")

# shape grid in w-space (float, search only)
gx = np.linspace(-6, 6, 481)
gy = np.linspace(0.02, 6, 241)
WX, WY = np.meshgrid(gx, gy, indexing="ij")
Wg = WX + 1j*WY
M1 = Wg; M2 = 1-Wg; M3 = (Wg-1)/Wg
MU = [M1, M2, M3, np.conj(M1), np.conj(M2), np.conj(M3)]

t0=time.time(); results=[]; best_overall=0
for pname, poly in polys:
    fp = fpoly_of(poly)
    cands = candidates(poly)
    if len(cands) > 63:
        cands = cands[:63]
    masks = []
    for c in cands:
        masks.append(R.blocked_mask(fp, (float(c.x), float(c.y))))
    # bitmask per raster cell: which candidate points block it
    bits = np.zeros((R.NU, R.NT), dtype=np.uint64)
    for i,m in enumerate(masks):
        bits |= (m.astype(np.uint64) << np.uint64(i))
    acc = np.full(Wg.shape, np.uint64(0xFFFFFFFFFFFFFFFF), dtype=np.uint64)
    for Marr in MU:
        iu, it = R.mult_cells(Marr)
        acc &= bits[iu, it]
    pc = np.zeros(acc.shape, dtype=np.int32)
    a = acc.copy()
    while a.any():
        pc += (a & np.uint64(1)).astype(np.int32)
        a >>= np.uint64(1)
    mx = int(pc.max())
    best_overall = max(best_overall, mx)
    if mx >= 3:
        idx = np.argwhere(pc >= 3)
        results.append((pname, mx, len(idx), idx[:200], Wg))
        print(f"  {pname}: raster says up to {mx} simultaneous blocked points at {len(idx)} shape cells", flush=True)
print(f"raster pass: {time.time()-t0:.1f}s; best simultaneous blocked-point count = {best_overall}")
print("candidate polygons with >=3:", [r[0] for r in results])
json.dump({"best": best_overall, "cands": [(r[0], r[1], r[2]) for r in results]}, open("out_raster.json","w"), indent=1)
np.save("raster_hits.npy", np.array([r[0] for r in results], dtype=object), allow_pickle=True)
```

### `confirm.py`

```python
import sys, time, json
sys.path.insert(0, '.')
import numpy as np
from fractions import Fraction as F
from hunt import *
import raster as R
from run_raster_polys import build_polys   # same construction, imported

gx = np.linspace(-6, 6, 481); gy = np.linspace(0.02, 6, 241)
WX, WY = np.meshgrid(gx, gy, indexing="ij"); Wg = WX + 1j*WY
M1 = Wg; M2 = 1-Wg; M3 = (Wg-1)/Wg
MU = [M1, M2, M3, np.conj(M1), np.conj(M2), np.conj(M3)]

TARGETS = sys.argv[1:] if len(sys.argv)>1 else None
polys = build_polys()
best = 0; report=[]
for pname, poly in polys:
    if TARGETS and pname not in TARGETS: continue
    fp = fpoly_of(poly); cands = candidates(poly)[:63]
    masks=[R.blocked_mask(fp,(float(c.x),float(c.y))) for c in cands]
    bits = np.zeros((R.NU,R.NT),dtype=np.uint64)
    for i,m in enumerate(masks): bits |= (m.astype(np.uint64) << np.uint64(i))
    acc = np.full(Wg.shape, np.uint64(0xFFFFFFFFFFFFFFFF), dtype=np.uint64)
    for Marr in MU:
        iu,it = R.mult_cells(Marr); acc &= bits[iu,it]
    pc = np.zeros(acc.shape,dtype=np.int32); a=acc.copy()
    while a.any():
        pc += (a & np.uint64(1)).astype(np.int32); a >>= np.uint64(1)
    idx = np.argwhere(pc>=3)
    print(f"{pname}: {len(idx)} raster cells with >=3; max {int(pc.max()) if pc.size else 0}", flush=True)
    seen=set(); tested=0
    order = sorted(range(len(idx)), key=lambda j: -pc[idx[j][0],idx[j][1]])
    for j in order:
        i0,i1 = idx[j]
        wr, wi = float(WX[i0,i1]), float(WY[i0,i1])
        for den in (1,2,3,4,6,8,12,16,24,32,48,64):
            a_ = F(round(wr*den), den); b_ = F(round(wi*den), den)
            if b_ <= 0: continue
            w = w_gauss(a_, b_)
            if not (is_nondegenerate(w) and is_scalene(w)): continue
            key=(a_,b_)
            if key in seen: continue
            seen.add(key); tested+=1
            exc=[]
            for c in cands:
                if not decide(poly,c,w)[0]: exc.append(c)
            if len(exc)>best:
                best=len(exc); print("   new best",best,"w=",w,"pts",exc, flush=True)
            if len(exc)>=3:
                report.append({"poly":pname,"w":w.exact(),"pts":[c.exact() for c in exc]})
        if tested > 400: break
    print(f"   tested {tested} exact shapes for {pname}; running best = {best}", flush=True)
json.dump({"best":best,"report":report}, open("out_confirm.json","w"), indent=1)
print("BEST EXACT |E_T| FOUND:", best, " hits:", len(report))
```

### `census.py`

```python
"""Big exact-backed census: for many (polygon, shape) pairs, how many candidate
points of J are T-exceptional?  Float screen (validated point-for-point against
the exact decider) counts; every count >= 3 is re-decided exactly."""
import sys, time, json, math
sys.path.insert(0, '.')
from hunt import *
from run_raster_polys import build_polys

polys = build_polys()
shapes = []
D = 3
for a in range(-8*D, 8*D+1):
    for b in range(1, 6*D+1):
        w = w_gauss(F(a,D), F(b,D))
        if is_nondegenerate(w) and is_scalene(w):
            shapes.append(w)
shapes.append(w_equilateral())          # control: Meyerson says <= 2
print(len(polys),"polygons x",len(shapes),"shapes =",len(polys)*len(shapes),"pairs", flush=True)

def cands_of(poly): return candidates(poly, nmid=3)

t0=time.time(); dist={}; hits=[]; exact_calls=0; pairs=0
for pname,poly in polys:
    fp = fpoly_of(poly); cs = cands_of(poly)
    fcs=[(float(p.x),float(p.y)) for p in cs]
    diam=max(math.hypot(a[0]-b[0],a[1]-b[1]) for a in fp for b in fp)
    tol=1e-9*max(diam,1.0)
    for w in shapes:
        pairs+=1
        mus=[fmu(m) for m in multipliers(w)]
        sc=[i for i,fo in enumerate(fcs) if not screen_good(fp,fo,mus,tol)]
        n=len(sc)
        if n>=3:
            exc=[i for i in sc if not decide(poly,cs[i],w)[0]]
            exact_calls+=len(sc); n=len(exc)
            if n>=3:
                hits.append({"poly":pname,"w":w.exact(),"pts":[cs[i].exact() for i in exc]})
                print("HIT",pname,w,[cs[i] for i in exc], flush=True)
        dist[n]=dist.get(n,0)+1
    print(f"  {pname} done  t={time.time()-t0:.0f}s  dist so far={dict(sorted(dist.items()))}", flush=True)
print("pairs",pairs,"exact point-decisions",exact_calls,f"{time.time()-t0:.0f}s")
print("distribution of #exceptional candidate points:",dict(sorted(dist.items())))
print("hits with >=3:",len(hits))
json.dump({"pairs":pairs,"dist":{str(k):v for k,v in dist.items()},"hits":hits},open("out_census.json","w"),indent=1)
```

### `mech_scan.py`

```python
import sys, time, json
sys.path.insert(0, '.')
from hunt import *
from run_raster_polys import build_polys
from mechanism import wedge_blocked
import math, random
polys = build_polys()
D=3; shapes=[]
for a in range(-8*D,8*D+1):
    for b in range(1,6*D+1):
        w=w_gauss(F(a,D),F(b,D))
        if is_nondegenerate(w) and is_scalene(w): shapes.append(w)
t0=time.time(); nonwedge=[]; nexc=0; ncheck=0
for pname,poly in polys:
    fp=fpoly_of(poly); cs=candidates(poly,nmid=3); fcs=[(float(p.x),float(p.y)) for p in cs]
    diam=max(math.hypot(a[0]-b[0],a[1]-b[1]) for a in fp for b in fp); tol=1e-9*max(diam,1.)
    for w in shapes:
        mus=[fmu(m) for m in multipliers(w)]
        sc=[i for i,fo in enumerate(fcs) if not screen_good(fp,fo,mus,tol)]
        for i in sc:
            good,_=decide(poly,cs[i],w); ncheck+=1
            if good: continue
            nexc+=1
            if not wedge_blocked(poly,cs[i],w):
                nonwedge.append({"poly":pname,"pt":cs[i].exact(),"w":w.exact()})
    if time.time()-t0>1200: print("budget",pname,flush=True); break
print(f"exact decisions on screened-exceptional points: {ncheck}; confirmed exceptional {nexc}; "
      f"NON-WEDGE among them: {len(nonwedge)}  ({time.time()-t0:.0f}s)")
for r in nonwedge[:10]: print("   NON-WEDGE", r)
json.dump({"checked":ncheck,"exceptional":nexc,"nonwedge":nonwedge},open("out_mech.json","w"),indent=1)
```

### `detail.py`

```python
import sys, math, json
sys.path.insert(0, '.')
from hunt import *
from run_raster_polys import build_polys
from mechanism import wedge_blocked, phi_min_mult
polys = dict(build_polys())

# ---- equilateral control: any NON-WEDGE exceptional point for k = 1 ? -------
weq = w_equilateral()
mus = [fmu(m) for m in multipliers(weq)]
tot=exc=nw=0
for pname,poly in build_polys():
    fp=fpoly_of(poly); cs=candidates(poly,nmid=3)
    diam=max(math.hypot(a[0]-b[0],a[1]-b[1]) for a in fp for b in fp); tol=1e-9*max(diam,1.)
    for c in cs:
        tot+=1
        if screen_good(fp,(float(c.x),float(c.y)),mus,tol): continue
        good,_=decide(poly,c,weq)
        if good: continue
        exc+=1
        if not wedge_blocked(poly,c,weq):
            nw+=1; print("  equilateral NON-WEDGE:",pname,c)
print(f"equilateral control: {tot} candidate points, {exc} exceptional, {nw} of them non-wedge")

# ---- detail on one scalene non-wedge witness -------------------------------
for pname, pt, wtxt in [("rand15","(26,18)","1/3+1i"), ("rand17","(23,29)","2/3+1i")]:
    poly = polys[pname]
    O = [p for p in poly if p.exact()==pt]
    O = O[0] if O else None
    if O is None:
        # a midpoint candidate
        for c in candidates(poly,nmid=3):
            if c.exact()==pt: O=c
    a,b = wtxt.split('+'); b=b[:-1]
    w = w_gauss(F(a), F(b))
    good, roles = decide(poly, O, w)
    ms = multipliers(w)
    print(f"\n--- {pname}  O={O.exact()}  w={w.exact()} ---")
    print("polygon:", [p.exact() for p in poly])
    print("simple:", is_simple(poly), " convex:", __import__('angles').is_convex(poly))
    print("scalene:", is_scalene(w), " sides^2:", [s for s in shape_sides2(w)])
    angs = [math.degrees(math.atan2(float(m.q), float(m.p))) for m in ms[:3]]
    print("angles of T (deg):", [round(abs(x),4) for x in angs], "sum", round(sum(abs(x) for x in angs),4))
    print("ratios |mu|:", [round(math.sqrt(float(m.norm2())),6) for m in ms[:3]])
    print("good:", good, " roles(witness per multiplier):", {i:(None if v is None else v.exact()) for i,v in roles.items()})
    print("wedge_blocked:", wedge_blocked(poly,O,w))
```

### `spiralcheck.py`

```python
"""Independent numerical check of the spiral-tip corollary.

Model of J_{c,beta} via its radial normal form ONLY (directions at radius r):
    0<r<1 : {tau(r), tau(r)+beta},  tau(r) = -ln r / c
    r=1   : the whole arc [0,beta]
    r>1   : empty
Criterion: O good in role (phi, k)  iff  exists r>0 with
    (Theta(r) + phi) n Theta(k r) != empty.
Brute force over r; compare with the predicted rule |phi + (ln k)/c| <= beta (mod 2pi).
This tests the DERIVATION, not Lemma 3 (which is re-derived by hand in the README).
"""
import math, random

TWO = 2*math.pi

def theta_set(r, c, beta, n=2000):
    if r > 1 + 1e-15: return []
    if abs(r-1) < 1e-15: return ("arc", 0.0, beta)
    tau = -math.log(r)/c
    return [tau % TWO, (tau+beta) % TWO]

def meets(A, B, phi, tol):
    """does (A + phi) meet B ?  A,B each a list of angles or an ('arc',lo,hi)."""
    def to_iv(S, shift=0.0):
        if isinstance(S, tuple):
            return [((S[1]+shift) % TWO, (S[2]+shift) % TWO, True)]
        return [((a+shift) % TWO, (a+shift) % TWO, False) for a in S]
    for (a0,a1,arcA) in to_iv(A, phi):
        for (b0,b1,arcB) in to_iv(B):
            # both are (possibly degenerate) arcs of length < pi, no wraparound issue
            lo1,hi1 = (a0,a1) if a1>=a0 else (a0,a1+TWO)
            lo2,hi2 = (b0,b1) if b1>=b0 else (b0,b1+TWO)
            for sh in (-TWO,0.0,TWO):
                if max(lo1+sh,lo2) <= min(hi1+sh,hi2)+tol:
                    return True
    return False

def good(c, beta, phi, k, N=200000, tol=1e-9):
    # r ranges over (0, min(1,1/k)];  sample log-uniformly plus the endpoints
    rmax = min(1.0, 1.0/k)
    for i in range(N+1):
        r = rmax*math.exp(-8.0*i/N)
        A = theta_set(r, c, beta); B = theta_set(k*r, c, beta)
        if not A or not B: continue
        if meets(A, B, phi, tol): return True, r
    # explicit endpoints where an arc is in play
    for r in (1.0, 1.0/k):
        A = theta_set(r,c,beta); B = theta_set(k*r,c,beta)
        if A and B and meets(A,B,phi,tol): return True, r
    return False, None

def predicted(c, beta, phi, k):
    L = (phi + math.log(k)/c) % TWO
    d = min(L, TWO-L)
    return d <= beta + 1e-12

random.seed(20260829)
bad = 0; tot = 0
for c in (0.3, 1.0, 2.0, 5.0):
    for beta in (math.radians(10), math.radians(30), math.radians(55)):
        for _ in range(40):
            phi = random.uniform(0.05, math.pi-0.05)
            k = math.exp(random.uniform(-2.5, 2.5))
            g,_r = good(c,beta,phi,k, N=4000)
            p = predicted(c,beta,phi,k)
            tot += 1
            if g != p:
                bad += 1
                if bad < 8:
                    L=(phi+math.log(k)/c)%TWO
                    print(f"  MISMATCH c={c} beta={math.degrees(beta):.0f} phi={math.degrees(phi):.2f} "
                          f"k={k:.4f} brute={g} pred={p} Lam={math.degrees(min(L,TWO-L)):.3f}")
print(f"spiral corollary: {tot} random (c,beta,phi,k), mismatches {bad}")
```

### `halfdensity.py`

```python
"""Check of the sharp constant in the spiral-similarity half-density lemma.

Claim: for sigma a spiral similarity about O with |mu| = k < 1,
   sup { lambda(V n B(O,R)) / lambda(B(O,R)) : V measurable, V n sigma(V) = empty }
 = 1/(1+k^2),  attained by the union of alternate geometric shells.

After the measure-preserving shear that kills the rotation part (see README),
the problem is rotation-free and separates over directions into the 1-D problem
   maximise  int_S e^{2u} du   over S subset (-inf,0]  with  S n (S+a) = empty,
where a = -ln k > 0.  Solve that 1-D problem by exact DP on a fine grid
(max-weight independent set on a path) and compare with 1/(1+k^2).
"""
import math

def one_d(a, m=4000, tail=40):
    """discretise u in [-tail*a, 0] into m*tail bins of width a/m; constraint links
    bin i and bin i+m."""
    n = m*tail
    du = a/m
    w = [math.exp(2*(-(n-i)*du)) * (math.exp(2*du)-1)/2 for i in range(n)]  # exact bin integrals
    # MWIS on the graph i ~ i+m: decomposes into m independent paths
    total = sum(w)
    bestsum = 0.0
    for r in range(m):
        chain = w[r::m]
        inc, exc = 0.0, 0.0
        for x in chain:
            inc, exc = exc + x, max(inc, exc)
        bestsum += max(inc, exc)
    return bestsum, total

print(f"{'k':>8} {'DP ratio':>12} {'1/(1+k^2)':>12} {'shells':>12}")
for k in (0.9, 0.7, 0.5, 0.3, 0.1):
    a = -math.log(k)
    b, t = one_d(a)
    shells = 1.0/(1+k*k)
    print(f"{k:8.2f} {b/t:12.6f} {shells:12.6f} {1/(1+k*k):12.6f}")
```

### `run_raster_polys.py` (the polygon family, factored out so the later drivers share it)

```python
import sys
sys.path.insert(0,'.')
from hunt import *

def build_polys():
    polys=[]
    polys.append(("tri-30-30-120", [P(-1,0),P(1,0),P(0,K(0,F(1,3)))]))
    polys.append(("sliver", [P(0,0),P(100,0),P(50,1)]))
    polys.append(("square", [P(0,0),P(1,0),P(1,1),P(0,1)]))
    polys.append(("thinY", [P(0,0),P(60,1),P(60,-1),P(1,-2),P(-30,-52),P(-32,-50),
                            P(-1,1),P(-30,53),P(-32,51)]))
    for k in (3,4,5,6,7):
        for rho in (F(1,5),F(1,4),F(1,3),F(1,2),F(2,3)):
            s = spike_star(k, F(10), rho)
            if s: polys.append((f"spike{k}-{rho}", s))
    for st,s in ((4,F(4,5)),(5,F(4,5)),(5,F(3,4)),(6,F(2,3)),(7,F(1,2)),(8,F(2,5))):
        sp = spiral_poly(st, s)
        if sp: polys.append((f"spiral{st}-{s}", sp))
    for t in (2,3,4):
        c = comb(t)
        if c: polys.append((f"comb{t}", c))
    for i in range(40):
        p = rand_star(rng, rng.randint(5,12))
        if p: polys.append((f"rand{i}", p))
    return polys

```

---

## C. Commands and raw output

Run from the directory holding the files of §B (the committed equilateral enumerator must be
reachable at the relative path used in `crosscheck.py`; it is **read and run only**, never
modified):

```
python3 crosscheck.py      # K1: my decider at mu=e^{i60} vs the committed one
python3 test_convex.py     # K2: Theorem C on convex polygons
python3 run_raster.py      # blocked-multiplier rasters + shape-space bitmask search
python3 confirm.py sliver spike3-2/3 spiral4-4/5 rand17 rand25   # exact re-decision of the flags
python3 census.py          # 66 075 (polygon, shape) pairs
python3 mech_scan.py       # wedge / non-wedge classification of every exceptional point
python3 detail.py          # equilateral control + detail on two non-wedge witnesses
python3 spiralcheck.py     # Theorem 5 by brute force over r
python3 halfdensity.py     # the sharp constant 1/(1+k^2) vs an exact DP
```

### Raw output

```
$ python3 crosscheck.py
190 fixtures
points compared: 1566   disagreements: 0   21.9s

$ python3 test_convex.py
66 convex polygons, 11 shapes
points 6380, mismatches 0, 92.5s
distribution of #exceptional vertices per (convex polygon, shape): {0: 617, 1: 64, 2: 45}

$ python3 run_raster.py
75 polygons
  sliver: raster says up to 6 simultaneous blocked points at 60928 shape cells
  spike3-2/3: raster says up to 4 simultaneous blocked points at 37 shape cells
  spiral4-4/5: raster says up to 4 simultaneous blocked points at 19 shape cells
  rand17: raster says up to 3 simultaneous blocked points at 3 shape cells
  rand25: raster says up to 5 simultaneous blocked points at 338 shape cells
raster pass: 84.7s; best simultaneous blocked-point count = 6

$ python3 confirm.py sliver spike3-2/3 spiral4-4/5 rand17 rand25
sliver: 60928 raster cells with >=3; max 6
   new best 2 w= -3+2i pts [(0,0), (100,0)]
   tested 402 exact shapes for sliver; running best = 2
spike3-2/3: 37 raster cells with >=3; max 4
   tested 112 exact shapes for spike3-2/3; running best = 2
spiral4-4/5: 19 raster cells with >=3; max 4
   tested 48 exact shapes for spiral4-4/5; running best = 2
rand17: 3 raster cells with >=3; max 3
   tested 19 exact shapes for rand17; running best = 2
rand25: 338 raster cells with >=3; max 5
   tested 403 exact shapes for rand25; running best = 2
BEST EXACT |E_T| FOUND: 2  hits: 0

$ python3 census.py
75 polygons x 881 shapes = 66075 pairs
pairs 66075 exact point-decisions 0 68s
distribution of #exceptional candidate points: {0: 65146, 1: 50, 2: 879}
hits with >=3: 0

$ python3 mech_scan.py
exact decisions on screened-exceptional points: 1774; confirmed exceptional 1774; NON-WEDGE among them: 22  (70s)
  (22 NON-WEDGE lines follow; the first two:)
   NON-WEDGE {'poly': 'rand15', 'pt': '(26,18)', 'w': '1/3+1i'}
   NON-WEDGE {'poly': 'rand15', 'pt': '(26,18)', 'w': '2/3+1i'}

$ python3 detail.py
  equilateral control: 2868 candidate points, 30 exceptional, 4 of them non-wedge
    (spiral4-4/5 (1,0);  spiral4-4/5 (-0.350681,-0.373051);  rand9 (26,-27);  rand39 (24,24))
  rand15  O=(26,18)  w=1/3+1i : simple True, convex False, scalene True, sides^2 [1,10/9,13/9],
     angles 71.5651 / 56.3099 / 52.125 (sum 180), |mu| 1.054093 / 1.20185 / 1.140175,
     good False (all six roles return no witness), wedge_blocked False
  rand17  O=(23,29)  w=2/3+1i : good False, wedge_blocked False

$ python3 spiralcheck.py
spiral corollary: 480 random (c,beta,phi,k), mismatches 0

$ python3 halfdensity.py
       k     DP ratio    1/(1+k^2)
    0.90     0.552486     0.552486
    0.70     0.671141     0.671141
    0.50     0.800000     0.800000
    0.30     0.917431     0.917431
    0.10     0.990099     0.990099
```

### The hand-checkable fixture of README §7.7

```
J = ['(0,0)', '(100,0)', '(50,1)']   w = -3+2i
T sides^2: [1, 13, 20]  scalene: True
T angles (deg): [146.3099, 26.5651, 7.125]
vertex (0,0): good=False  wedge_blocked=True
vertex (100,0): good=False  wedge_blocked=True
vertex (50,1): good=True  wedge_blocked=False   [role mu=-3+2i  P=(48,0)  X=(58,0)]
```
