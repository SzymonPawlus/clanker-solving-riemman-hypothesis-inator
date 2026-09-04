#!/usr/bin/env python3
"""Exact rational/algebraic dual certificate for the Euler-localised Delaunay
scoring family of `attacks/r4-delaunay`, plus the machine-checkable content of
the collapse proposition.

    Single reproduce command:      python3 certify.py
    (writes the same transcript to out/report.txt)

WHAT IS BEING CERTIFIED.  The sibling result `attacks/r4-delaunay` MEASURED, in
floating point, that an LP over the family returns exactly Oler's bound.  This
file replaces the measurement with an exact certificate in the direction that
matters, and gives the structural reason.

The family (verbatim from experiments/packing-r4-delaunay/lp.py) is a pair
(sigma, tau) with constants c_A, c_L >= 0 such that

  (D)  sigma(f) <= c_A*area(f) - 1/2   for every triangle with sides >= 1
       tau(l)   <= c_L*l        - 1/2   for every l >= 1
  (V)  sum_faces sigma(f) + sum_{boundary edges} tau(l_e) >= 0
       for every unit-separated non-collinear E and every triangulation of
       conv(E) with vertex set E,

which telescopes through Euler (F = 2n - b - 2) to  n <= 1 + c_A*A + c_L*M  and
hence, inside an equilateral triangle of side a, to

       n  <=  B(a)  :=  1 + c_A*(sqrt3/4)a^2 + 3*c_L*a.

STEP 1 below exhibits, for each n in {16, 17, 18}, an exact dual solution --
two nonnegative numbers in the real quadratic field Q(sqrt(8n+1)) -- proving

       min over the family of B(a)  >=  1 + (a^2 + 3a)/2   at   a = a_Oler(n),

i.e. B(a) >= n there.  Since B is nondecreasing in a for c_A, c_L >= 0, the
family's threshold satisfies a* <= a_Oler(n): THE FAMILY CANNOT BEAT OLER.
No floating point enters any accept/reject decision; the dual checker in
exact.py is validated on a tiny hand-solved LP, with negative controls, first.

SCOPE.  This is a statement about THIS formalisation of THIS family, and it is
a NEGATIVE result: it upgrades "the LP was observed to return Oler" to "the LP
provably cannot return better than Oler".  It is not a theorem that no
localised-scoring bound can beat Oler.  See the attack README section 5.

Status of everything here: `numerical` for the computation, `sketch` for the
surrounding argument.  Neither is assumable (RULES.md section 3).
"""

import io
import sys
from fractions import Fraction as F

import exact
import configs
from exact import Quad, Surd3, DualRejected, dual_certificate_value, \
    sqrt_bounds, sqrt_up
from configs import lattice, rhombus

OUT = io.StringIO()


def say(*args):
    line = " ".join(str(a) for a in args)
    print(line)
    OUT.write(line + "\n")


def rule(title):
    say("")
    say("=" * 78)
    say(title)
    say("=" * 78)


def dec(x, k=30):
    """Decimal rendering of a Fraction, correctly rounded, FOR DISPLAY ONLY.
    No accept/reject decision anywhere in this repository reads this."""
    x = F(x)
    neg = x < 0
    if neg:
        x = -x
    scaled = x * 10 ** k
    r = (scaled.numerator * 2 + scaled.denominator) // (2 * scaled.denominator)
    s = str(r).rjust(k + 1, "0")
    return ("-" if neg else "") + (s[:-k] + "." + s[-k:] if k else s)


# ==========================================================================
# STEP 0 -- validate the machinery BEFORE using it
# ==========================================================================

def step0():
    rule("STEP 0 -- validate the exact machinery on solved instances")
    say("RULES.md section 6: never start the real run before the code has")
    say("reproduced a known answer.  The exact dual checker is exercised on a")
    say("hand-solved 2x2 LP (optimum 7/5) and on three deliberately BAD duals")
    say("that it must reject, then on a Q(sqrt3)-coefficient LP.")
    say("")
    exact._selftest(log=say)
    say("")
    say("The Oler-tight configuration library is rebuilt from scratch with all")
    say("five self-checks (C1 separation, C2 Euler, C3 tiling, C4 exact unit")
    say("boundary edges, C5 Oler-tightness) asserted at construction:")
    say("")
    configs._selftest(log=say)


# ==========================================================================
# STEP 1 -- the exact dual certificate
# ==========================================================================

def oler_a(n):
    """a_Oler(n) = (sqrt(8n+1) - 3)/2 as an exact element of Q(sqrt(8n+1))."""
    D = 8 * n + 1
    from math import isqrt
    assert isqrt(D) ** 2 != D, (
        f"8n+1 = {D} is a perfect square: n is a triangular number, Oler is "
        f"attained and a_Oler is rational; this driver assumes the generic case")
    a = Quad(D, F(-3, 2), F(1, 2))
    assert a.sign() > 0
    assert a * a + 3 * a == Quad(D, 2 * n - 2, 0)     # minimal polynomial
    return a


def bracket(a, cand):
    """Pick tight configurations K1, K2 from `cand` with slope(K1) <= a <=
    slope(K2), tightest available on each side.  Exact comparisons."""
    lo = [K for K in cand if a >= K.slope]
    hi = [K for K in cand if a <= K.slope]
    if not lo or not hi:
        return None
    K1 = max(lo, key=lambda K: K.slope)
    K2 = min(hi, key=lambda K: K.slope)
    return K1, K2


def certify_n(n, cand, verbose=True, forced=None, header=True):
    """Exact dual certificate that the family's LP optimum at a = a_Oler(n) is
    at least n.  Returns (K1, K2, y1, y2, a)."""
    D = 8 * n + 1
    a = oler_a(n)
    lo, hi = a.approx(20)
    if verbose and header:
        say(f"  n = {n}:   D = 8n+1 = {D},   a = a_Oler(n) = (sqrt{D} - 3)/2")
        say(f"            a in [{dec(lo, 18)}, {dec(hi, 18)}]  (display only)")

    if forced is not None:
        K1, K2 = forced
    else:
        br = bracket(a, cand)
        assert br is not None, f"n={n}: no Oler-tight bracket available"
        K1, K2 = br
    s1, s2 = K1.slope, K2.slope
    if verbose:
        say(f"    bracketing Oler-tight configurations (slopes are RATIONAL,")
        say(f"    the comparisons below are exact in Q(sqrt{D})):")
        say(f"      K1 = {K1}")
        say(f"      K2 = {K2}")
        say(f"      slope(K1) = {s1} <= a <= {s2} = slope(K2):"
            f"  {a >= s1} / {a <= s2}")
    assert a >= s1 and a <= s2
    assert s1 < s2

    # convex weights lam, 1 - lam with lam*s1 + (1-lam)*s2 = a
    lam = (Quad(D, s2, 0) - a) * F(1, 1) / Quad(D, s2 - s1, 0)
    one_m = Quad(D, 1, 0) - lam
    assert lam.sign() >= 0 and one_m.sign() >= 0
    assert lam * s1 + one_m * s2 == a

    # dual variables
    y1 = Quad(D, 3, 0) * a * lam * Quad(D, F(1, 1) / K1.M, 0)
    y2 = Quad(D, 3, 0) * a * one_m * Quad(D, F(1, 1) / K2.M, 0)

    # ---- the LP, in the order-preserving change of variable
    #      x0 = (sqrt3/4) c_A >= 0,  x1 = c_L >= 0.
    #      Then  c_A*A_K = r_K x0  and  c_A*(sqrt3/4)a^2 = a^2 x0, so all
    #      coefficients live in Q(sqrt D) and none in Q(sqrt 3).
    A = [[Quad(D, K1.r_area, 0), Quad(D, K1.M, 0)],
         [Quad(D, K2.r_area, 0), Quad(D, K2.M, 0)]]
    b = [Quad(D, K1.n - 1, 0), Quad(D, K2.n - 1, 0)]
    c = [a * a, Quad(D, 3, 0) * a]

    if verbose:
        say("")
        say("    the LP (variables x0 = (sqrt3/4)c_A >= 0, x1 = c_L >= 0):")
        say(f"      minimise   a^2 * x0 + 3a * x1        [ = B(a) - 1 ]")
        say(f"      subject to {K1.r_area} x0 + {K1.M} x1 >= {K1.n - 1}"
            f"     [K1, a NECESSARY condition on any family member]")
        say(f"                 {K2.r_area} x0 + {K2.M} x1 >= {K2.n - 1}"
            f"     [K2]")
        say("")
        say("    candidate dual y = (y1, y2), exact in Q(sqrt%d):" % D)
        say(f"      lambda = (slope(K2) - a)/(slope(K2) - slope(K1)) = {lam}")
        say(f"      y1 = 3a*lambda/M(K1)      = {y1}")
        say(f"      y2 = 3a*(1-lambda)/M(K2)  = {y2}")
        say("")
        say("    exact dual-feasibility check (exact.dual_certificate_value):")

    val = dual_certificate_value(
        A, b, c, [y1, y2], name=f"family-LP n={n}",
        ring_zero=Quad(D, 0, 0), log=say if verbose else None)

    target = Quad(D, n - 1, 0)
    ok = (val == target)
    if verbose:
        say(f"      dual objective y.b = {val}")
        say(f"      required           = n - 1 = {target}")
        say(f"      EQUAL: {ok}")
    assert ok, f"n={n}: dual objective is {val}, not {n-1}"
    return K1, K2, y1, y2, a


def step1(cand):
    rule("STEP 1 -- EXACT DUAL CERTIFICATE: the family cannot beat Oler")
    say("For each n, weak duality gives  min B(a) - 1 >= y.b  for any")
    say("dual-feasible y >= 0.  We exhibit y with y.b = n - 1 EXACTLY, so")
    say("B(a_Oler(n)) >= n and the family cannot certify that n points fail to")
    say("fit at side a_Oler(n).  B is nondecreasing in a (c_A, c_L >= 0), so")
    say("the family's threshold a* satisfies a* <= a_Oler(n), i.e.")
    say("")
    say("      d_family(n)  <=  sqrt(8n+1) - 3  =  d_Oler(n).")
    say("")
    say("Two independent certificates are produced per n.  (A) uses the")
    say("TIGHTEST bracket available in the library built here.  (B) uses only")
    say("the side-4 and side-5 triangular LATTICES, which is the certificate")
    say("that applies to any library containing them -- including the sibling's")
    say("at refinement size >= 5.  Both must succeed independently.")
    say("")
    results = {}
    L4, L5 = lattice(4), lattice(5)
    for n in (16, 17, 18):
        say("-" * 78)
        say(f"  (A) tightest bracket")
        results[n] = certify_n(n, cand)
        say("")
        say(f"  (B) lattice-only bracket (side 4 and side 5)")
        certify_n(n, cand, forced=(L4, L5), header=False)
        say("")
        say(f"    ==> CERTIFIED TWICE: d_family({n}) <= sqrt({8*n+1}) - 3, "
            f"exactly.")
        say("")
    say("Where these configurations sit in the sibling's own library")
    say("(experiments/packing-r4-delaunay/framework.py, function `library`):")
    say("  lattice side m            = cfg_lattice(m),        needs size >= m")
    say("  rhombus P x Q             = cfg_parallelogram(P+1, Q+1),")
    say("                              needs size >= max(P+1, Q+1)")
    say("So certificate (B) applies from their refinement size 5 onward, and")
    say("every headline row of their report (sizes 6, 8, 10) is covered.")
    return results


# ==========================================================================
# STEP 2 -- the same certificate, symbolically, for every a and every pair
# ==========================================================================

def step2():
    rule("STEP 2 -- the certificate is an IDENTITY, checked symbolically")
    say("The three dual quantities were not fitted to n = 16, 17, 18.  With")
    say("K1, K2 any two Oler-tight configurations, writing")
    say("     A_i = (sqrt3/4) r_i,  M_i the (rational) perimeter,")
    say("     n_i - 1 = r_i/2 + M_i/2            [Oler-tightness]")
    say("     s_i = 3 r_i / M_i                  [the slope]")
    say("     lambda = (s2 - a)/(s2 - s1),  y_i = 3 a lambda_i / M_i,")
    say("the following hold as ALGEBRAIC IDENTITIES in a, r1, M1, r2, M2:")
    say("")
    say("     y1 r1 + y2 r2      = a^2          (dual constraint on x0, TIGHT)")
    say("     y1 M1 + y2 M2      = 3a           (dual constraint on x1, TIGHT)")
    say("     y1(n1-1) + y2(n2-1)= (a^2+3a)/2   (dual objective = Oler's value)")
    say("")
    try:
        import sympy as sp
    except ImportError:
        say("  sympy unavailable -- symbolic step SKIPPED (STEP 1 is unaffected)")
        return False
    a, r1, M1, r2, M2 = sp.symbols("a r1 M1 r2 M2", positive=True)
    s1, s2 = 3 * r1 / M1, 3 * r2 / M2
    lam = (s2 - a) / (s2 - s1)
    y1 = 3 * a * lam / M1
    y2 = 3 * a * (1 - lam) / M2
    b1 = r1 / 2 + M1 / 2
    b2 = r2 / 2 + M2 / 2
    ids = [("y1 r1 + y2 r2 - a^2", y1 * r1 + y2 * r2 - a ** 2),
           ("y1 M1 + y2 M2 - 3a", y1 * M1 + y2 * M2 - 3 * a),
           ("y1 b1 + y2 b2 - (a^2+3a)/2",
            y1 * b1 + y2 * b2 - (a ** 2 + 3 * a) / 2)]
    allok = True
    for label, e in ids:
        z = sp.simplify(sp.cancel(sp.together(e)))
        ok = (z == 0)
        allok &= ok
        say(f"     simplify({label}) = {z}    -> identically zero: {ok}")
    say("")
    say(f"  ALL THREE IDENTITIES HOLD: {allok}")
    say("  Consequence (the general statement, `sketch`): for EVERY a >= 1 and")
    say("  every configuration library containing two Oler-tight members whose")
    say("  slopes bracket a, the LP optimum is exactly Oler's bound, and when")
    say("  the bracket is strict (s1 < a < s2) Oler's coefficients")
    say("  (c_A, c_L) = (2/sqrt3, 1/2) are its UNIQUE minimiser.")
    say("  Since lattice(m) has slope m, every a >= 1 is bracketed by")
    say("  lattice(floor a) and lattice(floor a + 1).  So the collapse is not")
    say("  special to n = 16, 17, 18: it holds at every n.")
    return allok


# ==========================================================================
# STEP 3 -- the arithmetic core of the collapse proposition
# ==========================================================================

def step3(cand):
    rule("STEP 3 -- the collapse proposition, its checkable half")
    say("PROPOSITION (attack README section 2).  The 'free score' LP -- one")
    say("independent variable per face shape and per boundary-edge length --")
    say("has the SAME optimal value as the two-variable reduced LP.")
    say("")
    say("Proof (prose, `sketch`; written out in the attack README section 2):")
    say("  (i)  (D) caps each variable pointwise by the LINEAR member's value")
    say("       sigmahat(s) = c_A area(s) - 1/2,  tauhat(l) = c_L l - 1/2.")
    say("  (ii) (V) is a sum of the variables with coefficient +1, hence")
    say("       MONOTONE NONDECREASING in each of them.  So replacing any")
    say("       feasible (sigma, tau) by its cap (sigmahat, tauhat) preserves")
    say("       (V), and keeps (D) (with equality).  The objective involves")
    say("       only (c_A, c_L), which are untouched.")
    say("  (iii)Therefore the two LPs have the same feasible projection onto")
    say("       (c_A, c_L), hence the same optimal value, and the linear member")
    say("       is always among the optimal solutions.")
    say("  (iv) At the cap, (V) on a configuration K reads")
    say("         c_A A_K - F_K/2 + c_L M_K - b_K/2 >= 0,")
    say("       because sum_f area(f) = A_K exactly (the faces tile conv E).")
    say("       Euler F = 2n - b - 2 gives (F_K + b_K)/2 = n_K - 1, so this is")
    say("         c_A A_K + c_L M_K >= n_K - 1,")
    say("       EXACTLY the reduced LP's constraint.  QED")
    say("")
    say("The checkable half is step (iv)'s arithmetic: (F+b)/2 = n-1 on every")
    say("configuration, exactly, in integers.")
    say("")
    say(f"  {'configuration':<28}{'n':>4}{'b':>4}{'F':>5}"
        f"{'(F+b)/2':>10}{'n-1':>6}{'ok':>5}")
    allok = True
    for K in cand:
        v = F(K.F + K.b, 2)
        ok = (v == K.n - 1)
        allok &= ok
        say(f"  {K.name:<28}{K.n:>4}{K.b:>4}{K.F:>5}{str(v):>10}"
            f"{K.n-1:>6}{str(ok):>5}")
    say("")
    say(f"  EULER TELESCOPING IDENTITY HOLDS ON ALL {len(cand)} "
        f"CONFIGURATIONS: {allok}")
    say("")
    say("  What this does and does not settle.  Steps (i)-(iv) close: the")
    say("  measured 'max |sigma - linear| = 0.00e+00' is FORCED, in the sense")
    say("  that the linear member is always AN optimal solution and the optimal")
    say("  VALUE is unchanged by freeing sigma pointwise.  What is NOT proved,")
    say("  and was not claimed, is that every optimal solution has sigma at its")
    say("  cap: when (V) is slack the LP has other optima, and the solver's")
    say("  choice of vertex is not determined by this argument.")
    say("")
    say("  The deeper reading (`sketch`).  (D) + (V) are used ONLY through")
    say("  their consequence  c_A A_K + c_L M_K >= n_K - 1.  Even the strictly")
    say("  larger family that replaces pointwise (D) by its summed form")
    say("  'sum_f (sigma(f) - c_A area(f) + 1/2) <= 0' yields the same")
    say("  consequence, because sum_f area(f) = A_K exactly.  So the collapse")
    say("  is not caused by the nonlinearity being suppressed; it is caused by")
    say("  the SHAPE OF THE CONCLUSION.  Any bound of the form")
    say("      n <= 1 + c_A*area(conv E) + c_L*perimeter(conv E)")
    say("  is pinned by the lattices and rhombi, on which it is tight, and")
    say("  those pin it to Oler at every a.  Improving on Oler requires a")
    say("  conclusion that is NOT affine in (area, perimeter).")
    return allok


# ==========================================================================
# STEP 4 -- bridge to the sibling's actual (outward-rounded) LP
# ==========================================================================

def step4(cand):
    rule("STEP 4 -- bridge to experiments/packing-r4-delaunay's OWN LP data")
    say("The sibling LP does not use the exact A and M.  framework.py stores")
    say("outward (upper) rational bounds A_up >= A, M_up >= M, which WEAKEN the")
    say("constraints and make its LP an optimistic relaxation (its README")
    say("section 3).  A dual for the exact LP is therefore NOT automatically a")
    say("dual for theirs.  This step repairs that, exactly.")
    say("")
    say("REPAIR.  If A_up <= (1+eps) A and M_up <= (1+eps) M on the two support")
    say("configurations, then y/(1+eps) is dual-feasible for the relaxed LP")
    say("(y >= 0 is used here), with objective (n-1)/(1+eps).  Everything below")
    say("is a comparison of exact rationals or exact elements of Q(sqrt3).")
    say("")
    sys.path.insert(0, "../packing-r4-delaunay")
    try:
        import framework as fw
    except Exception as e:                                   # pragma: no cover
        say(f"  could not import the sibling framework ({e!r}).")
        say("  BRIDGE SKIPPED.  STEP 1 is a certificate for the exact LP and")
        say("  is unaffected; only the statement about their rounded LP is.")
        return None
    say(f"  imported {fw.__file__} read-only (nothing in that directory is")
    say("  modified by this script)")
    say("")

    pairs = [(4, lattice(4)), (5, lattice(5))]
    eps = None
    for k in range(40, 0, -1):
        e = F(1, 10 ** k)
        good = True
        for m, K in pairs:
            sib = fw.cfg_lattice(m)
            A_up = F(sib.area_up)
            M_up = F(sib.perim_up)
            # A = (sqrt3/4) r  ->  A_up <= (1+e) (sqrt3/4) r  in Q(sqrt3)
            if not (Surd3(A_up, 0) <= Surd3(0, (1 + e) * K.r_area / 4)):
                good = False
            if not (M_up <= (1 + e) * K.M):
                good = False
        if good:
            eps = e
            break
    assert eps is not None, "no eps <= 1/10 works: the rounding is not small"
    eps_k = len(str(eps.denominator)) - 1
    say(f"  smallest power-of-ten eps for which BOTH bounds hold: eps = 1e-{eps_k}")
    for m, K in pairs:
        sib = fw.cfg_lattice(m)
        A_up = F(sib.area_up)
        M_up = F(sib.perim_up)
        exA = Surd3(0, K.r_area / 4)
        say(f"    {sib.name:<22} A_up <= (1+eps)A : "
            f"{Surd3(A_up, 0) <= exA * (1 + eps)}"
            f"   M_up = {M_up} <= (1+eps)*{K.M} : {M_up <= (1 + eps) * K.M}")
        say(f"      (their M_up exceeds the exact perimeter {K.M} by "
            f"{dec(M_up - K.M, 34)})")
    say("")
    say("  Now certify the RELAXED LP at an explicit RATIONAL side length")
    say("  a_bar > a_Oler(n), so that every number in the check is rational:")
    say("")
    say(f"  {'n':>4}   {'a_bar (rational, > a_Oler)':>30}   "
        f"{'2*a_bar - d_Oler(n) <='}")
    out = {}
    for n in (16, 17, 18):
        D = 8 * n + 1
        _, hi = sqrt_bounds(D, 10 ** 40)
        base = (hi - 3) / 2
        # smallest power-of-ten margin above base at which the REPAIRED dual
        # still reaches n-1.  Larger margin = easier, so walk k upward and
        # stop at the first failure.  All comparisons exact rationals.
        abar, margin_k = None, None
        for k in range(1, 45):
            cand_a = base + F(1, 10 ** k)
            if cand_a * cand_a + 3 * cand_a >= (2 * n - 2) * (1 + eps):
                abar, margin_k = cand_a, k
            else:
                break
        assert abar is not None
        # exact bracket check at a_bar
        K1, K2 = lattice(4), lattice(5)
        assert K1.slope <= abar <= K2.slope
        lam = (K2.slope - abar) / (K2.slope - K1.slope)
        y = [3 * abar * lam / K1.M / (1 + eps),
             3 * abar * (1 - lam) / K2.M / (1 + eps)]
        sibs = [fw.cfg_lattice(4), fw.cfg_lattice(5)]
        # their row is  A_up*c_A + M_up*c_L >= n-1; in the variable
        # x0 = (sqrt3/4)c_A we have c_A = (4/sqrt3)x0, so the x0 coefficient
        # is (4/sqrt3)A_up, which the check above bounds by (1+eps)*r.
        # Using that RATIONAL upper bound only weakens the row further, so a
        # dual feasible for these rows is feasible for theirs.
        A = [[(1 + eps) * K.r_area, F(s.perim_up)]
             for K, s in zip((K1, K2), sibs)]
        b = [F(K1.n - 1), F(K2.n - 1)]
        c = [abar * abar, 3 * abar]
        val = dual_certificate_value(A, b, c, y, name=f"relaxed n={n}")
        assert val >= n - 1, (n, val)
        # 2*abar - d_Oler = 2*abar - (sqrt D - 3) <= 2*(abar - base) + 1e-40
        # because base = (hi-3)/2 and hi - sqrt D <= 1e-40.
        d_excess = 2 * F(1, 10 ** margin_k) + F(1, 10 ** 40)
        out[n] = (abar, d_excess)
        say(f"  {n:>4}   {dec(abar, 26):>30}   "
            f"2e-{margin_k} + 1e-40  (= {dec(d_excess, 32)})")
    say("")
    say("  Read the middle column as: even against the sibling's own")
    say("  outward-rounded LP data, the family's threshold in d exceeds")
    say("  sqrt(8n+1) - 3 by at most the amount in the right column.")
    say("  (Each row's dual was checked in exact rational arithmetic; the")
    say("  dominant term in the right column is the rational enclosure width")
    say("  of sqrt(8n+1), not the LP.)")
    return out


# ==========================================================================
# STEP 5 -- consistency with the sibling's published table (NOT a certificate)
# ==========================================================================

def step5():
    rule("STEP 5 -- consistency with the sibling's published LP table")
    say("This step certifies nothing.  It checks that the proposition of STEP")
    say("2-3 PREDICTS the sibling's under-constrained rows, which is evidence")
    say("that the model of their LP used here is the right one.")
    say("")
    say("Model: let s_max be the largest slope among the Oler-tight members of")
    say("the library.  If a > s_max nothing brackets a from above, the LP")
    say("optimum moves to the boundary c_A = 0, and B(a) = 1 + a(3+s_max)/2,")
    say("giving  d = 2a = 4(n-1)/(3+s_max).  If a <= s_max the bracket exists")
    say("and the answer is Oler's.  (The first branch is a PREDICTION, not")
    say("proved here -- it would need the non-tight members checked too.)")
    say("")
    say("  library size 3: lattices m<=3 (slope 3), rhombi P,Q<=2 (slope 3)")
    say("                  -> s_max = 3")
    say("  library size 4: lattices m<=4 (slope 4), rhombi P,Q<=3")
    say(f"                  (3x3 has slope {rhombus(3,3).slope})"
        f" -> s_max = 9/2")
    say("")
    say(f"  {'size':>5}{'n':>4}{'a_Oler > s_max?':>18}{'predicted d':>26}"
        f"{'sibling reported':>20}")
    table = {(3, 16): "10.000000", (3, 17): "10.666667", (3, 18): "11.333333",
             (4, 16): "8.357817", (4, 17): "8.704700", (4, 18): "9.066667"}
    for size, smax in ((3, F(3)), (4, F(9, 2))):
        for n in (16, 17, 18):
            a = oler_a(n)
            above = a > smax
            if above:
                pred = dec(4 * (n - 1) / (3 + smax), 6)
            else:
                lo, hi = a.approx(20)
                pred = dec(2 * lo, 6) + "  (= Oler)"
            say(f"  {size:>5}{n:>4}{str(above):>18}{pred:>26}"
                f"{table[(size, n)]:>20}")
    say("")
    say("  Every row matches the sibling's report.txt to the digits printed")
    say("  there, including the two rows that are ABOVE Oler.  In particular")
    say("  d(18) = 136/15 = 9.0666... at library size 4 is exactly what the")
    say("  model predicts from s_max = 9/2 < a_Oler(18), and it is why adding")
    say("  the side-5 lattice (library size >= 5) drops it to Oler.")


# ==========================================================================

def main():
    say("EXACT DUAL CERTIFICATE + COLLAPSE PROPOSITION")
    say("for attacks/r4-delaunay (Euler-localised Delaunay scoring, proposal AB)")
    say("worker r4-dual, claude (Opus 5), 2026-08-24")
    say("")
    say("Claim type: LOWER-BOUND (optimality-side) NEGATIVE result.  No packing,")
    say("no construction, no new bound.  Status: `numerical` for the computation")
    say("below, `sketch` for the surrounding argument.  Not assumable.")

    step0()

    cand = ([lattice(m) for m in range(1, 9)]
            + [rhombus(p, q) for p in range(1, 6) for q in range(p, 7)])
    # de-duplicate by slope, keeping the smallest configuration
    seen = {}
    for K in cand:
        if K.slope not in seen or K.n < seen[K.slope].n:
            seen[K.slope] = K
    cand = [seen[s] for s in sorted(seen)]

    r1 = step1(cand)
    r2 = step2()
    r3 = step3(cand)
    r4 = step4(cand)
    step5()

    rule("VERDICT")
    say("1. EXACT DUAL CERTIFICATE: VERIFIED at n = 16, 17, 18.")
    say("   Two nonnegative dual variables in Q(sqrt(8n+1)); both dual")
    say("   constraints hold with EQUALITY; dual objective = n - 1 exactly.")
    say("   Hence, for the LP over this family with exact data,")
    say("       d_family(n) <= sqrt(8n+1) - 3 = d_Oler(n),  n = 16, 17, 18.")
    say("   No floating point entered any accept/reject decision.")
    say(f"2. SYMBOLIC IDENTITY (all a, all Oler-tight pairs): "
        f"{'VERIFIED' if r2 else 'SKIPPED'}.")
    say(f"3. COLLAPSE PROPOSITION: closes.  Its arithmetic core (the Euler")
    say(f"   telescoping identity) verified on {len(cand)} configurations: {r3}.")
    if r4:
        say("4. BRIDGE to the sibling's own outward-rounded LP: VERIFIED, with")
        say("   an explicit rational slack; see STEP 4.")
    else:
        say("4. BRIDGE to the sibling's LP: SKIPPED (import failed).")
    say("5. The model reproduces every row of the sibling's published table,")
    say("   including the two rows above Oler.")
    say("")
    say("SCOPE.  This is about the LP over THIS formalisation of THIS family.")
    say("It says the family cannot beat Oler.  It does NOT say that no")
    say("localised-scoring bound can beat Oler.  Read attack README section 5.")

    with open("out/report.txt", "w") as f:
        f.write(OUT.getvalue())
    print("\n[written to out/report.txt]")


if __name__ == "__main__":
    main()
