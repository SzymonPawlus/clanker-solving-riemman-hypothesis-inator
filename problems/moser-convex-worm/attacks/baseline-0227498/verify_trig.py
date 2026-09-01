#!/usr/bin/env python3
"""Exact-rational audit of the load-bearing decimal trigonometry.

This uses Fraction interval arithmetic only.  A Machin formula encloses pi;
alternating Taylor partial sums enclose sin and cos.  No floating-point value
is used in an accepted predicate.
"""

import json
from fractions import Fraction as Q
from math import factorial
from pathlib import Path


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    products = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(products), max(products)


def scale(c, x):
    return (c * x[0], c * x[1]) if c >= 0 else (c * x[1], c * x[0])


def power(x, n):
    assert 0 <= x[0] <= x[1]
    return x[0] ** n, x[1] ** n


def atan_alt(x, n):
    """Enclose atan(x), 0<x<=1, between consecutive partial sums."""
    assert Q(0) < x <= Q(1)
    assert n >= 0
    terms = [(-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(n + 2)]
    a, b = sum(terms[:-1]), sum(terms)
    return min(a, b), max(a, b)


def pi_interval():
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239).
    a = atan_alt(Q(1, 5), 80)
    b = atan_alt(Q(1, 239), 30)
    return add(scale(16, a), scale(-4, b))


PI = pi_interval()


def radians(degrees):
    return scale(degrees / 180, PI)


def taylor_poly(x, parity, last):
    """Interval evaluation of a sin/cos Taylor partial sum.

    parity=1 gives powers 1,3,... (sin); parity=0 gives 0,2,... (cos).
    """
    out = (Q(0), Q(0))
    for k in range(last + 1):
        n = 2 * k + parity
        out = add(out, scale(Q((-1) ** k, factorial(n)), power(x, n)))
    return out


def trig_alt(x, parity, even_last=30):
    """Enclose sin/cos using consecutive, decreasing alternating sums."""
    limit = Q(2) if parity == 1 else Q(1)
    assert Q(0) <= x[0] <= x[1] <= limit
    assert even_last % 2 == 0
    a = taylor_poly(x, parity, even_last)
    b = taylor_poly(x, parity, even_last + 1)
    return min(a[0], b[0]), max(a[1], b[1])


def sin_deg(d):
    return trig_alt(radians(d), 1)


def cos_deg(d):
    # All calls use 0 <= d <= 36 degrees.
    return trig_alt(radians(d), 0)


def show(name, interval):
    # Binary floats are used only for compact human-readable diagnostics; all
    # accepted comparisons below remain exact Fraction comparisons.
    print(f"{name}: [{float(interval[0]):.15g}, {float(interval[1]):.15g}]")


def main():
    if not __debug__:
        raise RuntimeError("replay requires assertions; do not run Python with -O")
    cert = json.loads(Path(__file__).with_name("certificate.json").read_text())
    rat = lambda key: Q(*key)
    c = rat(cert["target"])
    coarse = rat(cert["coarse_target"])
    symmetry = cert["symmetry_domain"]
    domain = cert["low_area_domain"]
    cut = cert["core_cutoffs"]
    alpha_hi = rat(cut["alpha_upper"])
    beta_lo = rat(cut["beta_lower"])
    beta_hi = rat(cut["beta_upper"])

    assert cert["schema"] == "moser-baseline-analytic-v1"
    assert cert["angles"] == "degrees"
    assert cert["rationals"] == "[numerator, denominator]"
    assert cert["arithmetic"] == (
        "fractions.Fraction exact rationals with outward Machin/Taylor intervals"
    )
    assert cert["tested_python"] == "CPython 3.14.6"
    assert cert["replay"] == (
        "python3 problems/moser-convex-worm/attacks/"
        "baseline-0227498/verify_trig.py"
    )
    assert cert["source"] == {
        "arxiv": "math/0701391v2",
        "revision_date": "2009-06-05",
        "theorem": 1,
        "archive_sha256": (
            "0a593e37477c3a3bfa2a58b44c3e1787ebf11638d5f601cfc2ff21f5c02b7064"
        ),
        "tex_file": "LowerBoundMoser_v5.tex",
        "tex_sha256": (
            "e2c5fa66a54b46c83e1787645205ba105e386d0d5ff12d8af205b0dcca17b680"
        ),
    }
    assert cert["claim_scope"] == {
        "conclusion": (
            "max(f(alpha,beta),g(alpha),h(beta)) >= target "
            "on the symmetry domain"
        ),
        "machine_checked_nodes": ["T_endpoints", "T_branch_metadata"],
        "review_required_nodes": [
            "W", "N", "H4", "H", "D", "RW", "F", "M"
        ],
        "dependency_order": [
            "W", "N", "H4", "H", "D", "RW", "F", "M", "T", "LB"
        ],
        "translation_variables": (
            "eliminated analytically by translation-invariant H4 and RW bounds"
        ),
        "not_dependencies": [
            "source_K2",
            "source_compactness",
            "source_grid_proposition_8",
        ],
    }
    assert list(map(rat, symmetry["alpha"])) == [45, 90]
    assert list(map(rat, symmetry["beta"])) == [60, 120]
    assert list(map(rat, domain["alpha"])) == [45, 78]
    assert list(map(rat, domain["beta"])) == [83, 97]
    assert c == Q(113749, 500000)
    assert coarse == Q(23, 100)

    # Exact side conditions behind all monotonicity and endpoint arguments.
    assert 45 < alpha_hi < 75 < 78 < 90
    assert 83 < beta_lo < 90 < beta_hi < 97
    assert beta_lo + beta_hi == 180
    assert beta_hi - 15 - 45 < 36
    assert alpha_hi - 45 < 30

    # Check the structured branch partition rather than accepting descriptive
    # strings which could disagree with the endpoints evaluated below.
    branches = cert["branches"]
    assert len(branches) == 7
    expected = [
        ("alpha_lower_bound", [Q(78), Q(90)], "g", Q(78), "coarse_target"),
        ("beta_lower_tail", [Q(60), Q(83)], "h_plus", Q(83), "coarse_target"),
        ("beta_upper_tail", [Q(97), Q(120)], "h_minus", Q(97), "coarse_target"),
        ("alpha_lower_bound", [alpha_hi, Q(78)], "g", alpha_hi, "target"),
        ("beta_lower_tail", [Q(83), beta_lo], "h_plus", beta_lo, "target"),
        ("beta_upper_tail", [beta_hi, Q(97)], "h_minus", beta_hi, "target"),
    ]
    for branch, (kind, interval, predicate, endpoint, threshold) in zip(
        branches[:6], expected
    ):
        assert branch["kind"] == kind
        assert list(map(rat, branch["interval"])) == interval
        assert branch["predicate"] == predicate
        assert rat(branch["endpoint"]) == endpoint
        assert branch["threshold"] == threshold
    core = branches[6]
    assert core["kind"] == "concave_core"
    assert list(map(rat, core["alpha"])) == [Q(45), alpha_hi]
    assert list(map(rat, core["beta"])) == [beta_lo, beta_hi]
    assert core["predicate"] == "q_endpoints"
    assert core["threshold"] == "target"

    # sqrt(2) enclosure, with its validity checked exactly here.
    sqrt2 = (
        Q(1414213562373095048801688724209698078569, 10**39),
        Q(1414213562373095048801688724209698078570, 10**39),
    )
    assert sqrt2[0] ** 2 < 2 < sqrt2[1] ** 2

    g_cut = scale(Q(1, 6), mul(sqrt2, sin_deg(alpha_hi)))
    h_lo_cut = scale(Q(1, 4), sin_deg(beta_lo + 30))
    h_hi_cut = scale(Q(1, 4), sin_deg(beta_hi - 30))

    # Conservative integer-degree reduction from the symmetry domain to D.
    g_domain = scale(Q(1, 6), mul(sqrt2, sin_deg(Q(78))))
    h_domain_lo = scale(Q(1, 4), sin_deg(Q(83 + 30)))
    h_domain_hi = scale(Q(1, 4), sin_deg(Q(97 - 30)))

    # Worst beta endpoint for alpha <= 75 is beta_hi.  At alpha_hi the
    # resulting positive cosine argument has magnitude beta_hi-15-alpha_hi.
    q_right = scale(
        Q(1, 6),
        add(scale(Q(1, 2), cos_deg(beta_hi - 15 - alpha_hi)),
            cos_deg(alpha_hi - 45)),
    )
    q_left = scale(
        Q(1, 6),
        add(scale(Q(1, 2), cos_deg(beta_hi - 60)), (Q(1), Q(1))),
    )

    for name, value in (
        ("pi", PI),
        ("g(78)", g_domain),
        ("h(83)", h_domain_lo),
        ("h(97)", h_domain_hi),
        ("g(alpha_hi)", g_cut),
        ("h(beta_lo)", h_lo_cut),
        ("h(beta_hi)", h_hi_cut),
        ("q(45)", q_left),
        ("q(alpha_hi)", q_right),
    ):
        show(name, value)

    for name, value, threshold in (
        ("g(78)-0.23", g_domain, coarse),
        ("h(83)-0.23", h_domain_lo, coarse),
        ("h(97)-0.23", h_domain_hi, coarse),
        ("g(alpha_hi)-c", g_cut, c),
        ("h(beta_lo)-c", h_lo_cut, c),
        ("h(beta_hi)-c", h_hi_cut, c),
        ("q(45)-c", q_left, c),
        ("q(alpha_hi)-c", q_right, c),
    ):
        show(name, (value[0] - threshold, value[1] - threshold))

    assert g_domain[0] > coarse
    assert h_domain_lo[0] > coarse
    assert h_domain_hi[0] > coarse
    assert g_cut[0] > c
    assert h_lo_cut[0] > c
    assert h_hi_cut[0] > c
    assert q_left[0] > c
    assert q_right[0] > c
    print("PASS: every directed lower endpoint is greater than 0.227498")


if __name__ == "__main__":
    main()
