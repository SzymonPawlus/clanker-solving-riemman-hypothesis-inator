"""Validation of the exact checker.

A checker that has never rejected anything is untested (issue #2), so this suite is
weighted towards rejections: for every reference packing we build deliberately
broken variants and require a REJECT, down to perturbations far below float epsilon.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import sympy

from packcheck import CertificateError, check_certificate
from packcheck.checker import load_certificate

from .naive_float import naive_float_check

CERT_DIR = Path(__file__).parent.parent / "certificates"
REFERENCE = [3, 6, 10]

# Perturbation sizes. 1e-12 is the size named in issue #2; the rest bracket the
# double-precision resolution limit (~1e-16 relative) from both sides.
EPSILONS = ["1/10**6", "1/10**12", "1/10**18", "1/10**30", "1/10**60"]


def load_reference(n: int) -> dict:
    return json.loads((CERT_DIR / f"n{n:03d}-triangular.json").read_text())


def shrink_coordinate(cert: dict, index: int, axis: int, eps: str) -> dict:
    """Return a copy with one coordinate moved by exactly -eps (exact string maths)."""
    broken = copy.deepcopy(cert)
    old = broken["coordinates"][index][axis]
    broken["coordinates"][index][axis] = f"({old}) - ({eps})"
    return broken


# --------------------------------------------------------------------------- #
# 1. The reference packings must be ACCEPTED.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("n", REFERENCE)
def test_accepts_reference_triangular_packing(n):
    result = check_certificate(load_reference(n))
    assert result.ok, result.render()
    assert result.failures == []


@pytest.mark.parametrize("n", REFERENCE)
def test_reference_side_length_is_tight(n):
    """s is exactly 2(k-1) + 2*sqrt(3): no 'not tight' warning, and --require-tight passes."""
    result = check_certificate(load_reference(n), require_tight=True)
    assert result.ok, result.render()
    assert not any("not tight" in w for w in result.warnings), result.warnings


def test_reference_side_lengths_match_the_problem_readme():
    """s(6) = 4 + 2*sqrt(3) and s(10) = 6 + 2*sqrt(3), per problems/.../README.md."""
    assert sympy.simplify(
        sympy.sympify(load_reference(6)["side_length"]) - (4 + 2 * sympy.sqrt(3))
    ) == 0
    assert sympy.simplify(
        sympy.sympify(load_reference(10)["side_length"]) - (6 + 2 * sympy.sqrt(3))
    ) == 0


# --------------------------------------------------------------------------- #
# 2. Overlap: two points closer than 2 must be REJECTED, however small the overlap.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("n", REFERENCE)
@pytest.mark.parametrize("eps", EPSILONS)
def test_rejects_tiny_overlap(n, eps):
    # Point 1 is the bottom row's second point, at (2, 0). Sliding it left by eps
    # makes it overlap point 0 at (0, 0).
    broken = shrink_coordinate(load_reference(n), index=1, axis=0, eps=eps)
    result = check_certificate(broken)
    assert not result.ok, f"checker ACCEPTED an overlap of {eps}:\n{result.render()}"
    assert any("closer than 2" in f for f in result.failures), result.render()


@pytest.mark.parametrize("n", REFERENCE)
def test_rejects_overlap_at_1e_12(n):
    """The size named in issue #2, called out on its own so it cannot be skipped."""
    broken = shrink_coordinate(load_reference(n), index=1, axis=0, eps="1/10**12")
    assert not check_certificate(broken).ok


# --------------------------------------------------------------------------- #
# 3. Containment: a point outside the triangle must be REJECTED.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("eps", EPSILONS)
def test_rejects_point_pushed_below_the_base(eps):
    broken = shrink_coordinate(load_reference(6), index=0, axis=1, eps=eps)
    result = check_certificate(broken)
    assert not result.ok, result.render()
    assert any("edge AB" in f for f in result.failures), result.render()


@pytest.mark.parametrize("eps", EPSILONS)
def test_rejects_point_pushed_past_the_left_edge(eps):
    """The apex sits on edges AC and BC; nudging it left leaves the triangle."""
    cert = load_reference(6)
    apex = len(cert["coordinates"]) - 1
    broken = shrink_coordinate(cert, index=apex, axis=0, eps=eps)
    result = check_certificate(broken)
    assert not result.ok, result.render()
    assert any("edge AC" in f for f in result.failures), result.render()


@pytest.mark.parametrize("eps", EPSILONS)
def test_rejects_side_length_shrunk_below_what_the_points_need(eps):
    """Shrinking s pulls edge BC inwards past the bottom-right point."""
    broken = load_reference(6)
    broken["side_length"] = f"({broken['side_length']}) - ({eps})"
    result = check_certificate(broken)
    assert not result.ok, result.render()
    assert any("edge BC" in f for f in result.failures), result.render()


# --------------------------------------------------------------------------- #
# 4. Side-length consistency in the other direction: inflated s.
# --------------------------------------------------------------------------- #

def test_inflated_side_length_warns_but_is_still_a_valid_upper_bound():
    cert = load_reference(6)
    cert["side_length"] = f"({cert['side_length']}) + 1"
    result = check_certificate(cert)
    assert result.ok, result.render()
    assert any("not tight" in w for w in result.warnings), result.warnings


def test_inflated_side_length_fails_under_require_tight():
    cert = load_reference(6)
    cert["side_length"] = f"({cert['side_length']}) + 1/10**30"
    assert not check_certificate(cert, require_tight=True).ok


def test_rejects_side_length_smaller_than_2_sqrt_3():
    cert = load_reference(3)
    cert["side_length"] = "3"  # 3 < 2*sqrt(3) ~= 3.464, so not even one circle fits
    result = check_certificate(cert)
    assert not result.ok
    assert any("no unit circle fits" in f for f in result.failures), result.render()


# --------------------------------------------------------------------------- #
# 5. What exact arithmetic actually buys, demonstrated against a float checker.
# --------------------------------------------------------------------------- #

def test_float_checker_with_zero_tolerance_rejects_a_valid_packing():
    """False NEGATIVE: sqrt(3) is not representable, so exact contacts come out short."""
    cert = load_reference(10)
    assert naive_float_check(cert, tol=0.0) is False
    assert check_certificate(cert).ok  # ... while the exact checker accepts it


@pytest.mark.parametrize("eps", ["1/10**12", "1/10**18", "1/10**30"])
def test_float_checker_with_a_working_tolerance_accepts_infeasible_packings(eps):
    """False POSITIVE: the tolerance needed above also hides real overlaps.

    tol = 1e-9 is the smallest round tolerance that makes the float checker accept
    the true n = 10 packing. At that tolerance it happily accepts an overlap of
    1e-12 -- exactly the failure mode the problem's RULES.md warns about.
    """
    tol = 1e-9
    assert naive_float_check(load_reference(10), tol=tol) is True
    broken = shrink_coordinate(load_reference(10), index=1, axis=0, eps=eps)
    assert naive_float_check(broken, tol=tol) is True, "float checker caught it after all"
    assert not check_certificate(broken).ok, "exact checker must reject it"


def test_float_checker_cannot_even_represent_the_perturbation():
    """Below ~1e-16 relative, the perturbed coordinate rounds back to the original."""
    broken = shrink_coordinate(load_reference(10), index=1, axis=0, eps="1/10**18")
    assert float(sympy.sympify(broken["coordinates"][1][0]).evalf(30)) == 2.0
    assert naive_float_check(broken, tol=0.0) is False  # only for the sqrt(3) reason
    assert not check_certificate(broken).ok


# --------------------------------------------------------------------------- #
# 6. Malformed certificates are rejected as malformed, not silently coerced.
# --------------------------------------------------------------------------- #

def test_rejects_json_float_coordinates():
    cert = load_reference(3)
    cert["coordinates"][1][0] = 1.9999999999
    with pytest.raises(CertificateError, match="JSON float"):
        check_certificate(cert)


def test_rejects_json_float_side_length():
    cert = load_reference(3)
    cert["side_length"] = 5.464101615137754
    with pytest.raises(CertificateError, match="JSON float"):
        check_certificate(cert)


def test_rejects_n_mismatch():
    cert = load_reference(6)
    cert["n"] = 7
    with pytest.raises(CertificateError, match="lists 6 coordinates"):
        check_certificate(cert)


def test_rejects_unknown_coordinate_type():
    cert = load_reference(3)
    cert["coordinate_type"] = "float"
    with pytest.raises(CertificateError, match="coordinate_type"):
        check_certificate(cert)


def test_rejects_irrational_coordinate_declared_rational():
    cert = load_reference(3)
    cert["coordinate_type"] = "rational"
    with pytest.raises(CertificateError, match="not rational"):
        check_certificate(cert)


def test_rejects_a_decimal_string():
    """`"5.5"` is exactly 11/2, but decimals are banned in exact fields.

    The problem's `RULES.md` §2 bans them because such a value is almost always
    truncated optimiser output wearing an exact value's clothes. This used to be a
    warning; the pinned spec makes it an error.
    """
    cert = load_reference(3)
    cert["side_length"] = "5.5"
    with pytest.raises(CertificateError, match="decimal"):
        check_certificate(cert)


# --------------------------------------------------------------------------- #
# 7. Interval certificates (conservative mode).
# --------------------------------------------------------------------------- #

def _box(cx: str, cy: str, pad: str) -> list:
    return [[cx, f"({cx}) + ({pad})"], [cy, f"({cy}) + ({pad})"]]


def _interval_certificate(pad: str) -> dict:
    """n = 3 strictly inside the triangle of side 6 (d = 6 - 2*sqrt(3) ~= 2.536).

    The three points sit ~0.2 inside each corner along the angle bisector, giving
    pairwise distances ~2.19 and containment margins ~0.2 -- comfortably more than
    any plausible enclosure width, so interval arithmetic can certify it.
    """
    return {
        "n": 3,
        "claim": "construction",
        "side_length": "6",
        "coordinates": [
            _box("173/1000", "1/10", pad),
            _box("2363/1000", "1/10", pad),
            _box("1268/1000", "1996/1000", pad),
        ],
        "coordinate_type": "interval",
        "verified_by": "tests",
        "status": "numerical",
        "beats_record": "no",
    }


@pytest.mark.parametrize("pad", ["0", "1/10**9", "1/10**3"])
def test_accepts_a_strictly_feasible_interval_certificate(pad):
    result = check_certificate(_interval_certificate(pad))
    assert result.ok, result.render()


def _touching_pair(pad: str) -> dict:
    """Two points at distance exactly 2, well inside a triangle of side 10."""
    return {
        "n": 2,
        "claim": "construction",
        "side_length": "10",
        "coordinates": [_box("1", "1", pad), _box("3", "1", pad)],
        "coordinate_type": "interval",
        "verified_by": "tests",
        "status": "numerical",
        "beats_record": "no",
    }


def test_interval_mode_certifies_contact_only_for_degenerate_boxes():
    """Documented limitation: a non-degenerate enclosure cannot certify an equality.

    An exactly-touching pair is feasible, and interval mode accepts it when the
    boxes are points (pad = 0) but REJECTS it as soon as they have width -- the
    enclosure of |p0-p1|^2 - 4 then straddles 0. Failing closed is the correct
    direction, and it is why the reference certificates are `algebraic`, not
    `interval`: every optimal packing has contacts.
    """
    assert check_certificate(_touching_pair("0")).ok
    result = check_certificate(_touching_pair("1/10**30"))
    assert not result.ok, result.render()
    assert any("closer than 2" in f for f in result.failures), result.render()


def test_rejects_interval_written_in_an_unspecified_encoding():
    cert = load_reference(3)
    cert["coordinate_type"] = "interval"
    with pytest.raises(CertificateError, match="interval components must be written"):
        check_certificate(cert)
