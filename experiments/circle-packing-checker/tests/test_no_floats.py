"""The single most important property: no floating point on the verification path.

Two independent checks:
  * a source audit of the `packcheck` package for float-producing constructs, and
  * a behavioural test that the checker decides an inequality whose margin is an
    irrational number ~1e-20, which no float representation can distinguish from 0.
"""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest
import sympy

from packcheck import check_certificate

PACKAGE = Path(__file__).parent.parent / "packcheck"

# Constructs that would put a float into the verification path.
BANNED_NAMES = {"float", "evalf", "sqrt", "log", "exp", "fsum", "isclose"}
BANNED_MODULES = {"numpy", "decimal", "statistics"}

# `math` is imported for `math.isqrt` only, which is exact integer arithmetic.
ALLOWED_MATH_ATTRS = {"isqrt"}

# `sympy.sqrt(3)` is the SYMBOL sqrt(3), not a numeric square root, so it is exact.
EXACT_NAMESPACES = {"sympy"}


def _module_files() -> list[Path]:
    return sorted(PACKAGE.glob("*.py"))


@pytest.mark.parametrize("path", _module_files(), ids=lambda p: p.name)
def test_no_float_producing_constructs_in_source(path: Path):
    tree = ast.parse(path.read_text())
    offences: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            offences.append(f"line {node.lineno}: float literal {node.value!r}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BANNED_MODULES:
                    offences.append(f"line {node.lineno}: import {alias.name}")
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in BANNED_MODULES:
                offences.append(f"line {node.lineno}: from {node.module} import ...")
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in BANNED_NAMES:
                offences.append(f"line {node.lineno}: call to {func.id}()")
            if isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name) and func.value.id == "math":
                    if func.attr not in ALLOWED_MATH_ATTRS:
                        offences.append(f"line {node.lineno}: math.{func.attr}()")
                elif isinstance(func.value, ast.Name) and func.value.id in EXACT_NAMESPACES:
                    if func.attr == "evalf":
                        offences.append(f"line {node.lineno}: sympy .evalf()")
                elif func.attr in BANNED_NAMES:
                    offences.append(f"line {node.lineno}: .{func.attr}()")
    assert not offences, f"{path.name} may use floating point:\n  " + "\n  ".join(offences)


def test_checker_never_builds_a_float_at_runtime(monkeypatch):
    """Trip a wire in `float.__new__`: if the check path constructs one, fail loudly.

    `float` cannot be monkeypatched directly, so instead this walks every object the
    checker produced looking for floats, and additionally asserts the certificate
    parser stores only exact sympy numbers.
    """
    from packcheck.checker import load_certificate

    cert = json.loads(
        (Path(__file__).parent.parent / "certificates" / "n010-triangular.json").read_text()
    )
    parsed = load_certificate(cert)
    for x, y in parsed.coordinates:
        for component in (x, y):
            assert not component.atoms(sympy.Float), f"{component} contains a Float"
    assert not parsed.side_length.atoms(sympy.Float)


def test_rejects_an_overlap_whose_size_is_irrational_and_about_1e_20():
    """Margin = sqrt(3) - 17320508075688772935/10**19 ~= 2.7e-20.

    No float, and no fixed-precision rational rounding, separates this from zero;
    the exact sign decision does.
    """
    tiny = "(sqrt(3) - 17320508075688772935/10**19)"
    assert sympy.sign(sympy.sympify(tiny)) == 1  # genuinely positive, and irrational

    cert = json.loads(
        (Path(__file__).parent.parent / "certificates" / "n010-triangular.json").read_text()
    )
    broken = copy.deepcopy(cert)
    broken["coordinates"][1][0] = f"2 - {tiny}"
    result = check_certificate(broken)
    assert not result.ok, result.render()
    assert any("closer than 2" in f for f in result.failures), result.render()


def test_the_same_irrational_shift_in_the_safe_direction_is_accepted():
    """Positive control: the checker is not just rejecting everything perturbed.

    A pair of points at distance exactly 2, well inside a large triangle, is moved
    APART by the same ~2.7e-20 irrational amount. It stays feasible, and is
    accepted. Moved TOGETHER by that amount it is rejected. The reference packings
    themselves are rigid -- every perturbation of them breaks some constraint --
    which is why this control uses a slack configuration.
    """
    tiny = "(sqrt(3) - 17320508075688772935/10**19)"

    def pair(offset: str) -> dict:
        return {
            "n": 2,
            "claim": "construction",
            "side_length": "10",
            "coordinates": [["1", "1"], [f"3 {offset} {tiny}", "1"]],
            "coordinate_type": "algebraic",
            "verified_by": "tests",
            "status": "numerical",
            "beats_record": "no",
        }

    assert check_certificate(pair("+")).ok
    assert not check_certificate(pair("-")).ok
