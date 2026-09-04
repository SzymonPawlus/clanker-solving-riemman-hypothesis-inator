"""THE THEOREM, as a finite exact verification.

CONSTRUCTION (upper bound) only.  Nothing below bears on optimality.

  THEOREM.  For every integer j >= 0 let P(j) be the four-grain staircase
  configuration of gen.py, n(j) = Delta(j+2) + floor(j/2) + 1 points, and
  d = 2j + 2*sqrt3.  Then
     (F) every pairwise distance is >= 2;
     (C) every point lies in the closed triangle A=(0,0), B=(d,0), C=(d/2, d sqrt3/2);
     (T) max_i ( x_i + y_i*sqrt3/3 ) = d exactly, i.e. d is the minimal enclosing
         side in that fixed placement -- the certificate is TIGHT.
  Consequently  s(n(j)) <= 2j + 4*sqrt3  for every j >= 0.

The proof is finite and j-free except for four explicitly j-dependent inequalities.
This file checks every ingredient mechanically.

 STEP A  parametric normal form of the four grains, and the four "grain lemmas".
         Each grain is swept by nonnegative integer parameters, and each grain
         lemma is an IDENTITY expressing the claimed slack as 2*(a nonnegative
         parameter combination).  The identities are verified symbolically in
         (j, U, M, par) with U+M = j, U-M = par, by the stdlib exact linear-form
         engine `Lin` below.  Every expression involved is linear with integer
         coefficients, so `Lin` decides identity exactly -- it is not sampling.
         If `sympy` happens to be installed it re-decides the same identities as
         an independent cross-check; it is NOT required and NOT load-bearing.

 STEP B  the forbidden difference vectors F(g1,g2) (forbidden.py): finite, j-free.

 STEP C  a separating linear functional L for each ordered grain pair, with
             L(p1 - p2) <= 0  for all p1 in g1, p2 in g2      (from step A)
             L(f) > 0         for every f in F(g1,g2)         (from step B)
         The single pair (BL,BR) at odd j does not admit such an L; it is closed
         by an explicit finite case analysis that consumes the dropped BR site.

 STEP D  containment and tightness, again from the step-A functionals.
"""
from fractions import Fraction as F
from q3 import E, SQ3
from gen import GRAINS, OFFSET, lattice_sites, n_of, d_of, s_of, UMp
from forbidden import all_forbidden, D2

FOUR = E(4, 0)

# ---------------------------------------------------------------------------
# STEP A -- parametric normal form + grain lemmas, verified symbolically
# ---------------------------------------------------------------------------
# Parameters: t,i,k,m >= 0 integers; U = ceil(j/2), M = floor(j/2), par = j mod 2,
# U + M = j, U - M = par.
#
#   BL : (r,x) = (t,        t + 2i),      0 <= t <= U, 0 <= i <= U - t
#   BR : (r,x) = (t,   2M + t + 2i),      0 <= t <= U, 0 <= i <= U - t
#        MINUS (t,i) = (0,0) when par = 1
#   C  : (r,x) = (par + k, j - k + 2i),   0 <= k <= M, 0 <= i <= k
#   T  : (r,x) = (U + m,   U + m + 2i),   0 <= m <= M, 0 <= i <= M - m
PARAM = {
    "BL": lambda U, M, j, par, p, q: (p, p + 2 * q),
    "BR": lambda U, M, j, par, p, q: (p, 2 * M + p + 2 * q),
    "C":  lambda U, M, j, par, p, q: (par + p, j - p + 2 * q),
    "T":  lambda U, M, j, par, p, q: (U + p, U + p + 2 * q),
}
# outer parameter range top, and inner range top (as expressions)
PRANGE = {"BL": ("U", "U - p"), "BR": ("U", "U - p"), "C": ("M", "p"), "T": ("M", "M - p")}


class Lin:
    """Exact linear form  c0 + sum_v c_v * v  over integer symbols. Stdlib only.

    Every grain-lemma expression below is linear with integer coefficients in
    (U, M, p, q), so equality of two such forms is decided EXACTLY by comparing
    coefficient dictionaries.  This is a symbolic identity decision, not a
    numeric sample over finitely many parameter values.
    """
    __slots__ = ("c",)
    CONST = ""

    def __init__(self, c=None):
        self.c = {k: v for k, v in (c or {}).items() if v != 0}

    @staticmethod
    def sym(name):
        return Lin({name: 1})

    @classmethod
    def _coerce(cls, o):
        return o if isinstance(o, Lin) else Lin({cls.CONST: o})

    def __add__(self, o):
        o = Lin._coerce(o)
        d = dict(self.c)
        for k, v in o.c.items():
            d[k] = d.get(k, 0) + v
        return Lin(d)

    __radd__ = __add__

    def __neg__(self):
        return Lin({k: -v for k, v in self.c.items()})

    def __sub__(self, o):
        return self + (-Lin._coerce(o))

    def __rsub__(self, o):
        return Lin._coerce(o) + (-self)

    def __mul__(self, k):
        if isinstance(k, Lin):
            raise TypeError("grain lemmas must stay linear; refusing a product of two forms")
        return Lin({a: v * k for a, v in self.c.items()})

    __rmul__ = __mul__

    def is_zero(self):
        return not self.c

    def __str__(self):
        if not self.c:
            return "0"
        parts = []
        for k in sorted(self.c, key=lambda s: (s == Lin.CONST, s)):
            v = self.c[k]
            if k == Lin.CONST:
                parts.append("%+d" % v)
            elif v == 1:
                parts.append("+ %s" % k)
            elif v == -1:
                parts.append("- %s" % k)
            else:
                parts.append("%+d*%s" % (v, k))
        s = " ".join(parts)
        return s[2:] if s.startswith("+ ") else s


def _grain_claims(sym):
    """Build the grain lemmas over any symbolic engine providing `sym(name)`.

    Returns a list of (grain, lemma name, slack expression, claimed identity).
    The claim is that slack - expect is identically zero as a form in (U,M,p,q).
    """
    U, M, p, q = sym("U"), sym("M"), sym("p"), sym("q")
    j, par = U + M, U - M
    claims = []

    def add(g, name, slack, expect):
        claims.append((g, name, slack, expect))

    r_, x_ = PARAM["BL"](U, M, j, par, p, q)
    add("BL", "r >= 0",        r_,                 p)
    add("BL", "x - r >= 0",    x_ - r_,            2 * q)
    add("BL", "x + r <= 2U",   2 * U - (x_ + r_),  2 * (U - p - q))
    add("BL", "r <= U",        U - r_,             U - p)

    r_, x_ = PARAM["BR"](U, M, j, par, p, q)
    add("BR", "r >= 0",        r_,                 p)
    add("BR", "x - r >= 2M",   (x_ - r_) - 2 * M,  2 * q)
    add("BR", "x + r <= 2j",   2 * (U + M) - (x_ + r_), 2 * (U - p - q))
    add("BR", "r <= U",        U - r_,             U - p)

    r_, x_ = PARAM["C"](U, M, j, par, p, q)
    add("C",  "r >= par",      r_ - (U - M),       p)
    add("C",  "x + r >= 2U",   (x_ + r_) - 2 * U,  2 * q)
    add("C",  "x - r <= 2M",   2 * M - (x_ - r_),  2 * (p - q))
    add("C",  "x - r >= 0",    x_ - r_,            2 * (M - p + q))
    add("C",  "x + r <= 2j",   2 * (U + M) - (x_ + r_), 2 * (M - q))
    add("C",  "r <= U",        U - r_,             M - p)

    r_, x_ = PARAM["T"](U, M, j, par, p, q)
    add("T",  "r >= U",        r_ - U,             p)
    add("T",  "x - r >= 0",    x_ - r_,            2 * q)
    add("T",  "x + r <= 2j",   2 * (U + M) - (x_ + r_), 2 * (M - p - q))
    return claims


def step_A():
    """Decide the grain lemmas as exact symbolic identities, stdlib only."""
    claims = _grain_claims(Lin.sym)
    print("STEP A -- grain lemmas as symbolic identities (stdlib exact linear forms)")
    ok = True
    for g, name, slack, expect in claims:
        good = (slack - expect).is_zero()
        ok &= good
        print("   %-2s  %-14s   slack = %-22s  %s" % (g, name, str(expect),
                                                      "IDENTITY" if good else "*** FAILS ***"))
        assert good, (g, name, str(slack), str(expect))
    print("   all %d grain lemmas are identities in (U,M,p,q); the parameter ranges" % len(claims))
    print("   0<=p, 0<=q and the range tops make every right-hand side >= 0.")
    return ok


def step_A_sympy_crosscheck():
    """OPTIONAL, NOT load-bearing: re-decide the same identities with sympy.

    Skipped silently-but-loudly when sympy is absent.  Step A above has already
    decided them exactly; this only buys a second, independently written engine.
    """
    try:
        import sympy as sp
    except ImportError:
        print("STEP A cross-check -- SKIPPED: sympy is not installed.")
        print("   This is an OPTIONAL second opinion only.  Step A above already decided")
        print("   every grain lemma exactly with the stdlib linear-form engine, so nothing")
        print("   load-bearing was skipped and the theorem check below is unaffected.")
        return None
    claims = _grain_claims(lambda nm: sp.Symbol(nm, integer=True))
    print("STEP A cross-check -- the same identities re-decided by sympy %s" % sp.__version__)
    ok = True
    for g, name, slack, expect in claims:
        good = sp.simplify(sp.expand(slack - expect)) == 0
        ok &= good
        assert good, (g, name, sp.expand(slack), sp.expand(expect))
    print("   sympy agrees on all %d grain lemmas." % len(claims))
    return ok


def step_A_numeric_guard(JMAX=40):
    """Independent guard: brute-force the same grain lemmas on the generated sites."""
    print("STEP A guard -- the same lemmas re-checked on the generated site lists, j = 0..%d" % JMAX)
    for j in range(JMAX + 1):
        U, M, par = UMp(j)
        g = lattice_sites(j)
        for (r, x) in g["BL"]:
            assert r >= 0 and x - r >= 0 and x + r <= 2 * U, (j, "BL", r, x)
        for (r, x) in g["BR"]:
            assert r >= 0 and x - r >= 2 * M and x + r <= 2 * j, (j, "BR", r, x)
            assert not (par == 1 and r == 0 and x == 2 * M), (j, "BR dropped site present")
        for (r, x) in g["C"]:
            assert r >= par and x + r >= 2 * U and 0 <= x - r <= 2 * M and x + r <= 2 * j, (j, "C", r, x)
        for (r, x) in g["T"]:
            assert r >= U and x - r >= 0 and x + r <= 2 * j, (j, "T", r, x)
        for nm in GRAINS:
            for (r, x) in g[nm]:
                assert (x - r) % 2 == 0, (j, nm, r, x, "parity x = r mod 2")
    print("   OK -- and x = r (mod 2) holds for every site of every grain.")
    return True


# ---------------------------------------------------------------------------
# STEP C -- separating functionals
# ---------------------------------------------------------------------------
# For an ordered pair (g1,g2), L(dx,dr) = alpha*dx + beta*dr.  We need
#   (i)  L(x1-x2, r1-r2) <= 0 for every p1 in g1, p2 in g2, every j  -- from step A
#   (ii) L(f) > 0 for every f in F(g1,g2)                            -- finite check
# Justification of (i) is recorded as the pair of grain lemmas used.
SEP = {
    ("BL", "C"):  ((1, 1),  "BL: x+r <= 2U ;  C: x+r >= 2U"),
    ("C", "BL"):  ((-1, -1), "same pair, reversed"),
    ("C", "BR"):  ((1, -1), "C: x-r <= 2M ;  BR: x-r >= 2M"),
    ("BR", "C"):  ((-1, 1), "same pair, reversed"),
    ("BL", "T"):  ((0, 1),  "BL: r <= U ;  T: r >= U"),
    ("T", "BL"):  ((0, -1), "same pair, reversed"),
    ("BR", "T"):  ((0, 1),  "BR: r <= U ;  T: r >= U"),
    ("T", "BR"):  ((0, -1), "same pair, reversed"),
    ("C", "T"):   ((0, 1),  "C: r <= par+M = U ;  T: r >= U"),
    ("T", "C"):   ((0, -1), "same pair, reversed"),
}
# BL <-> BR is handled separately (see step_C_BLBR).


def step_C(Fsets):
    print("STEP C -- separating functionals, and the finite check L(f) > 0")
    ok = True
    for (g1, g2), ((al, be), why) in sorted(SEP.items()):
        lst = Fsets[(g1, g2)]
        vals = [al * dx + be * dr for (dx, dr, _) in lst]
        good = all(v > 0 for v in vals)
        ok &= good
        print("   %-2s - %-2s  L = %2d*dx + %2d*dr   |F| = %d   L(F) = %-18s %s"
              % (g1, g2, al, be, len(lst), str(vals), "CLOSED" if good else "*** OPEN ***"))
        print("            because  %s" % why)
        assert good, (g1, g2, vals)
    return ok


def step_C_BLBR(Fsets):
    """The one pair with no separating functional: BL vs BR.

    From step A:  x1 <= 2U - r1 (BL)  and  x2 >= 2M + r2 (BR), so
        dx = x1 - x2 <= 2U - 2M - r1 - r2 = 2*par - r1 - r2.            (*)
    """
    print("STEP C' -- BL vs BR, the pair with no separating functional")
    lst = Fsets[("BL", "BR")]
    dxs = sorted(set(dx for (dx, dr, _) in lst))
    print("   F(BL,BR) = %s ;  dx values = %s" % ([(a, b) for a, b, _ in lst], dxs))

    # even j: par = 0, (*) gives dx <= -r1-r2 <= 0
    good_even = all(dx > 0 for (dx, dr, _) in lst)
    print("   j EVEN (par=0):  (*) gives dx <= -r1-r2 <= 0, and every f in F has dx > 0 -> CLOSED"
          if good_even else "   j EVEN: *** OPEN ***")
    assert good_even

    # odd j: par = 1, (*) gives dx + r1 + r2 <= 2
    survivors = [(dx, dr) for (dx, dr, _) in lst if dx <= 2]
    print("   j ODD  (par=1):  (*) gives dx + r1 + r2 <= 2.")
    print("       f with dx >= 3 need r1+r2 <= -1  -> impossible (r1,r2 >= 0).  Killed: %s"
          % [f for f in [(a, b) for a, b, _ in lst] if f[0] >= 3])
    print("       surviving f: %s" % survivors)
    assert survivors == [(2, 0)], survivors
    print("       f = (2,0) forces r1 = r2 = 0 AND equality in both step-A bounds,")
    print("       i.e. x1 = 2U and x2 = 2M, i.e. the BR site (r,x) = (0, 2M).")
    print("       That site is REMOVED from BR exactly when j is odd -> CLOSED.")

    # mechanical confirmation of the equality analysis, for a range of odd j
    for j in range(1, 42, 2):
        U, M, par = UMp(j)
        g = lattice_sites(j)
        bl0 = set(x for (r, x) in g["BL"] if r == 0)
        br0 = set(x for (r, x) in g["BR"] if r == 0)
        assert max(bl0) == 2 * U and (2 * M) not in br0 and min(br0) == 2 * M + 2, (j, bl0, br0)
        assert not any((x1 - x2, 0) in [(a, b) for a, b, _ in lst] for x1 in bl0 for x2 in br0)
    print("   mechanical confirmation for odd j = 1,3,...,41: BL row 0 max x = 2U,")
    print("   BR row 0 min x = 2M+2, so dx = x1-x2 <= 2U-2M-2 = 0 in row 0.  CLOSED.")
    return True


# ---------------------------------------------------------------------------
# STEP D -- containment and tightness, symbolically
# ---------------------------------------------------------------------------
def step_D():
    """For p = (x + a sqrt3, b + r sqrt3) with grain offset (a,b), and d = 2j+2sqrt3:

       AB:  y >= 0            <=>  b + r sqrt3 >= 0
       AC:  sqrt3 x_p - y_p >= 0  <=>  sqrt3(x - r) + (3a - b) >= 0
       BC:  sqrt3(d - x_p) - y_p >= 0  <=>  sqrt3(2j - x - r) + (6 - 3a - b) >= 0
       enclosing functional:  x_p + y_p sqrt3/3 = (x + r) + (a + b/3) sqrt3
    """
    print("STEP D -- containment and tightness")
    rows = []
    for g in GRAINS:
        a, b = OFFSET[g]
        rows.append((g, a, b, 3 * a - b, 6 - 3 * a - b, E(0, F(3 * a + b, 3))))
    print("   grain   (a,b)   AC const 3a-b   BC const 6-3a-b   enclosing sqrt3-part (a+b/3)")
    for g, a, b, ac, bc, enc in rows:
        print("     %-3s   (%d,%d)        %3d               %3d              %s" % (g, a, b, ac, bc, enc.s()))
    print()
    print("   AB: b >= 0 and r >= 0 in every grain (step A)  ->  y >= 0.                  OK")
    print("   AC: sqrt3*(x-r) + (3a-b) >= 0.  Step A gives x-r >= 0 for ALL FOUR grains,")
    print("       and the constant 3a-b is >= 0 for all four (table above), so AC holds")
    print("       with room to spare.  Worst case is x-r = 0:")
    for g, a, b, ac, bc, enc in rows:
        # worst case is the minimum of (x-r) allowed by step A, which is 0 for BL, C, T and 2M for BR
        xr_min = 0 if g != "BR" else 0   # 2M >= 0, and 2M = 0 at j = 0
        v = SQ3 * E(xr_min) + E(ac)
        print("        %-3s at x-r = %d :  sqrt3*%d + %d = %-10s  >= 0 ? %s"
              % (g, xr_min, xr_min, ac, v.s(), v >= E(0)))
        assert v >= E(0), (g, "AC")
    print("   BC: sqrt3*(2j-x-r) + (6-3a-b) >= 0.  Step A gives 2j-x-r >= 0 for all four")
    print("       grains (BL via x+r <= 2U <= 2j), and 6-3a-b >= 0 for all four.  Worst case:")
    for g, a, b, ac, bc, enc in rows:
        v = SQ3 * E(0) + E(bc)
        print("        %-3s at 2j-x-r = 0 :  %d = %-6s >= 0 ? %s" % (g, bc, v.s(), v >= E(0)))
        assert v >= E(0), (g, "BC")
    print()
    print("   TIGHTNESS.  x_p + y_p sqrt3/3 = (x+r) + (a + b/3) sqrt3, and step A gives")
    print("   x+r <= 2j for BR, C, T and x+r <= 2U <= 2j for BL.  So the value is at most")
    print("   2j + max_g (a + b/3) sqrt3 = 2j + 2 sqrt3 = d, attained by BR (and T):")
    for g, a, b, ac, bc, enc in rows:
        cap = E(0) + enc
        print("        %-3s  max (x+r) + (a+b/3)sqrt3  <=  2j + %s" % (g, cap.s()))
    print("   BR contains (r,x) = (0, 2j) for every j (2j != 2M unless par=0 and U=0, i.e. j=0,")
    print("   where nothing is dropped), so the maximum 2j + 2 sqrt3 = d is ATTAINED.")
    for j in range(0, 41):
        U, M, par = UMp(j)
        g = lattice_sites(j)
        assert (0, 2 * j) in g["BR"], j
        assert max(x + r for (r, x) in g["BR"]) == 2 * j
    print("   mechanically confirmed for j = 0..40:  (0,2j) in BR and max(x+r) = 2j.   OK")
    return True


def main():
    Fsets = all_forbidden()
    print("=" * 78)
    step_A()
    print()
    step_A_sympy_crosscheck()
    print()
    step_A_numeric_guard()
    print()
    print("=" * 78)
    print("STEP B -- forbidden difference vectors (finite, j-free); see forbidden.py")
    for g in GRAINS:
        assert Fsets[(g, g)] == [], g
    print("   INTRA-GRAIN: F(g,g) is EMPTY for all four grains -- the separation-2")
    print("   triangular lattice has minimum distance exactly 2, so intra-grain pairs")
    print("   are never violating.  (dx^2 + 3 dr^2 >= 4 whenever dx = dr mod 2, not both 0.)")
    for (g1, g2), lst in sorted(Fsets.items()):
        if g1 != g2:
            print("   |F(%s,%s)| = %d" % (g1, g2, len(lst)))
    print()
    print("=" * 78)
    step_C(Fsets)
    print()
    step_C_BLBR(Fsets)
    print()
    print("=" * 78)
    step_D()
    print()
    print("=" * 78)
    print("THEOREM VERIFIED (construction / upper bound only):")
    print("  for every j >= 0, P(j) is feasible, contained, and tight, hence")
    print("  s(n(j)) <= 2j + 4 sqrt(3)  with  n(j) = Delta(j+2) + floor(j/2) + 1.")
    print("  Status: sketch (agent prose) + numerical (the finite exact checks).")
    print("  NO OPTIMALITY IS CLAIMED.")


if __name__ == "__main__":
    main()
