"""The input boundary: hostile certificate text, and certificates of the wrong claim.

Both sections exist because of the PR #16 review, which found that

  1. `parse_exact` handed certificate strings to sympy's `parse_expr`, which
     evaluates them as Python -- so a certificate could write a file, and did,
     *before* the checker rejected it; and
  2. the `claim` field was never looked at, so a geometrically valid packing was
     ACCEPTed while claiming `optimality`, which this checker cannot establish.

Section 1 asserts rejection *and the absence of the side effect*, since rejecting
after the damage is done is the exact failure being fixed.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import sympy

from packcheck import CertificateError, check_certificate
from packcheck.checker import load_certificate, parse_exact, validate_schema
from packcheck.safeparse import UnsafeExpression, parse_scalar

CERT_DIR = Path(__file__).parent.parent / "certificates"

# The payload from the review, verbatim. It creates the file under the old parser.
CODEX_PAYLOAD = "open('/tmp/pr16-parser-proof','w').write('executed')"
CODEX_PAYLOAD_PATH = Path("/tmp/pr16-parser-proof")


def load_reference(n: int) -> dict:
    return json.loads((CERT_DIR / f"n{n:03d}-triangular.json").read_text())


# --------------------------------------------------------------------------- #
# 1. Hostile expressions are rejected, and nothing is executed.
# --------------------------------------------------------------------------- #

ATTACKS = {
    "file_write": CODEX_PAYLOAD,
    "attribute_access": "(3).__class__",
    "dunder_traversal": "().__class__.__base__.__subclasses__()",
    "dunder_globals": "sqrt.__globals__",
    "import_call": "__import__('os').system('touch /tmp/pr16-parser-proof')",
    "import_statement": "import os",
    "from_import": "from os import system",
    "exec_call": "exec('open(\"/tmp/pr16-parser-proof\",\"w\")')",
    "eval_call": "eval('1+1')",
    "builtin_call": "print(1)",
    "getattr_call": "getattr(sqrt, 'x')",
    "open_call": "open('/tmp/pr16-parser-proof', 'w')",
    "comprehension": "[i for i in range(3)]",
    "generator": "sum(i for i in range(3))",
    "dict_comprehension": "{i: i for i in range(3)}",
    "lambda_call": "(lambda: 1)()",
    "lambda_literal": "lambda: 1",
    "bare_name": "pi",
    "assignment_expression": "(x := 1)",
    "string_literal": "'abc'",
    "fstring": "f'{1}'",
    "subscript": "[1, 2][0]",
    "tuple_literal": "(1, 2)",
    "list_literal": "[1, 2]",
    "conditional": "1 if 1 else 2",
    "comparison": "1 < 2",
    "boolean_op": "1 and 2",
    "bitwise_or": "1 | 2",
    "modulo": "5 % 2",
    "floor_division": "5 // 2",
    "matmul": "1 @ 2",
    "attribute_call": "sqrt.conjugate()",
    "keyword_argument": "sqrt(x=3)",
    "starred_argument": "sqrt(*[3])",
    "two_arguments": "sqrt(3, 4)",
    "unknown_function": "cos(3)",
    "semicolon_statements": "1; open('/tmp/pr16-parser-proof','w')",
    "decimal_literal": "10.928",
    "complex_literal": "1j",
    "true_literal": "True",
    "none_literal": "None",
}


@pytest.mark.parametrize("text", ATTACKS.values(), ids=list(ATTACKS))
def test_hostile_expression_is_rejected_by_the_parser(text):
    with pytest.raises(UnsafeExpression):
        parse_scalar(text)


@pytest.mark.parametrize("text", ATTACKS.values(), ids=list(ATTACKS))
def test_hostile_expression_is_rejected_as_a_certificate_error(text):
    with pytest.raises(CertificateError):
        parse_exact(text)


@pytest.mark.parametrize("text", ATTACKS.values(), ids=list(ATTACKS))
def test_hostile_expression_has_no_side_effect(text, tmp_path):
    """Nothing in the input is ever run, so no file appears and no import happens.

    The payloads that would write `/tmp/pr16-parser-proof` are the ones that mattered
    in review; this also watches `tmp_path` in case a payload is retargeted later.
    """
    CODEX_PAYLOAD_PATH.unlink(missing_ok=True)
    before = set(tmp_path.iterdir())
    with pytest.raises(UnsafeExpression):
        parse_scalar(text)
    assert not CODEX_PAYLOAD_PATH.exists(), f"{text!r} executed: the payload file was created"
    assert set(tmp_path.iterdir()) == before


def test_the_exact_review_payload_creates_no_file(tmp_path):
    """The regression from the PR #16 review, stated on its own so it cannot be lost.

    Both the reported spelling (a fixed path in /tmp) and a per-test path are tried,
    at the scalar level and embedded in a certificate coordinate.
    """
    target = tmp_path / "pr16-parser-proof"
    payloads = [
        CODEX_PAYLOAD,
        f"open({str(target)!r},'w').write('executed')",
    ]
    for payload in payloads:
        CODEX_PAYLOAD_PATH.unlink(missing_ok=True)

        with pytest.raises(CertificateError):
            parse_exact(payload)
        assert not CODEX_PAYLOAD_PATH.exists()
        assert not target.exists()

        cert = load_reference(3)
        cert["coordinates"][1][0] = payload
        with pytest.raises(CertificateError):
            check_certificate(cert)
        assert not CODEX_PAYLOAD_PATH.exists(), "the payload ran during a full check"
        assert not target.exists()


def test_hostile_side_length_is_rejected():
    cert = load_reference(3)
    cert["side_length"] = CODEX_PAYLOAD
    CODEX_PAYLOAD_PATH.unlink(missing_ok=True)
    with pytest.raises(CertificateError):
        check_certificate(cert)
    assert not CODEX_PAYLOAD_PATH.exists()


def test_hostile_interval_endpoint_is_rejected():
    """The interval path parses scalars too, so it needs the same guarantee."""
    cert = {
        "n": 1,
        "claim": "construction",
        "side_length": "10",
        "coordinates": [[["1", "1"], ["1", CODEX_PAYLOAD]]],
        "coordinate_type": "interval",
        "verified_by": "tests",
        "status": "numerical",
        "beats_record": "no",
    }
    CODEX_PAYLOAD_PATH.unlink(missing_ok=True)
    with pytest.raises(CertificateError):
        check_certificate(cert)
    assert not CODEX_PAYLOAD_PATH.exists()


# --------------------------------------------------------------------------- #
# 2. Resource bounds: an allowlisted grammar can still ask for something absurd.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "text",
    [
        "10**10**9",              # exponent over the cap
        "(10**10000)**10000",     # cheap to write, enormous to materialise
        "2**(1/10**9)",           # denominator over the cap
        "1" + "+1" * 400,         # more syntax nodes than the cap
        "1" * 5000,               # longer than the source-length cap
    ],
)
def test_expensive_expressions_are_refused(text):
    with pytest.raises(UnsafeExpression):
        parse_scalar(text)


@pytest.mark.parametrize("text", ["1/0", "1/(2-2)", "0**(-1)"])
def test_division_by_zero_is_a_parse_error_not_a_crash(text):
    with pytest.raises(UnsafeExpression):
        parse_scalar(text)


# --------------------------------------------------------------------------- #
# 3. Positive control: the grammar still accepts everything a certificate needs.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "text,expected",
    [
        ("0", sympy.Integer(0)),
        ("-5", sympy.Integer(-5)),
        ("+5", sympy.Integer(5)),
        ("7/3", sympy.Rational(7, 3)),
        ("2 + 2*sqrt(3)", 2 + 2 * sympy.sqrt(3)),
        ("(1 - 2)*(3 + 4)", sympy.Integer(-7)),
        ("1/10**60", sympy.Rational(1, 10**60)),
        ("5**(1/3)", sympy.Integer(5) ** sympy.Rational(1, 3)),
        ("sqrt(3)/3", sympy.sqrt(3) / 3),
        ("sqrt(sqrt(16))", sympy.Integer(2)),
        (
            "sqrt(3) - 17320508075688772935/10**19",
            sympy.sqrt(3) - sympy.Rational(17320508075688772935, 10**19),
        ),
    ],
)
def test_legitimate_expressions_still_parse(text, expected):
    assert sympy.simplify(parse_scalar(text) - expected) == 0


def test_reference_certificates_still_load():
    """Whole-file regression: the grammar covers every scalar the fixtures use."""
    for n in (3, 6, 10):
        assert check_certificate(load_reference(n)).ok


def test_negative_radicand_is_rejected_as_not_real():
    with pytest.raises(CertificateError, match="not a real number"):
        parse_exact("sqrt(-1)")


# --------------------------------------------------------------------------- #
# 4. The `claim` field. This checker certifies constructions and nothing else.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "claim",
    ["optimality", "counterexample", "", "Construction", "construction ", None, 0, True, []],
)
def test_rejects_a_claim_other_than_construction(claim):
    """A geometrically valid packing must NOT be accepted under a claim it cannot support."""
    cert = load_reference(6)
    cert["claim"] = claim
    assert check_certificate(load_reference(6)).ok  # the same packing, correctly claimed
    with pytest.raises(CertificateError, match="claim must be"):
        check_certificate(cert)


def test_rejects_a_missing_claim_rather_than_defaulting_it():
    """Absent `claim` used to default to `construction`; it now fails closed."""
    cert = load_reference(6)
    del cert["claim"]
    with pytest.raises(CertificateError, match="missing required field"):
        check_certificate(cert)


def test_accepts_the_construction_claim():
    assert load_certificate(load_reference(6)).claim == "construction"


# --------------------------------------------------------------------------- #
# 5. The rest of the schema pinned by problems/.../RULES.md §2.
# --------------------------------------------------------------------------- #

REQUIRED = [
    "n",
    "claim",
    "side_length",
    "coordinates",
    "coordinate_type",
    "verified_by",
    "status",
    "beats_record",
]


@pytest.mark.parametrize("field", REQUIRED)
def test_every_required_field_is_required(field):
    cert = load_reference(6)
    del cert[field]
    with pytest.raises(CertificateError, match="missing required field"):
        validate_schema(cert)


@pytest.mark.parametrize("status", ["sketch", "cited", "refuted", "verified", "", None])
def test_rejects_a_status_outside_the_pinned_set(status):
    cert = load_reference(6)
    cert["status"] = status
    with pytest.raises(CertificateError, match="status must be"):
        validate_schema(cert)


@pytest.mark.parametrize("status", ["numerical", "verified:review", "verified:lean"])
def test_accepts_the_pinned_statuses(status):
    cert = load_reference(6)
    cert["status"] = status
    validate_schema(cert)  # must not raise


@pytest.mark.parametrize("field", ["verified_by", "beats_record"])
@pytest.mark.parametrize("value", ["", "   ", None, 7, ["a"]])
def test_rejects_an_empty_or_non_string_provenance_field(field, value):
    cert = load_reference(6)
    cert[field] = value
    with pytest.raises(CertificateError, match="non-empty string"):
        validate_schema(cert)


@pytest.mark.parametrize("n", [0, -1, "6", 6.0, True, None])
def test_rejects_a_bad_n(n):
    cert = load_reference(6)
    cert["n"] = n
    with pytest.raises(CertificateError, match="n must be a positive integer"):
        validate_schema(cert)


@pytest.mark.parametrize("data", [None, [], "certificate", 3])
def test_rejects_a_certificate_that_is_not_an_object(data):
    with pytest.raises(CertificateError, match="must be a JSON object"):
        validate_schema(data)


def test_unknown_fields_are_tolerated():
    """The fixtures carry a `_note`; the schema does not forbid extra keys."""
    cert = load_reference(6)
    cert["_note"] = "regenerate rather than hand-editing"
    cert["future_field"] = 1
    validate_schema(cert)
    assert check_certificate(cert).ok


def test_schema_validation_does_not_parse_scalars():
    """Stage 1 is shape only: a hostile scalar passes the schema and dies in stage 2.

    Keeping the stages separate is what makes the failure message say which one it
    is -- 'not a certificate' versus 'a certificate of something false'.
    """
    cert = load_reference(3)
    cert["side_length"] = CODEX_PAYLOAD
    CODEX_PAYLOAD_PATH.unlink(missing_ok=True)
    validate_schema(cert)  # shape is fine
    with pytest.raises(CertificateError, match="could not parse"):
        load_certificate(cert)
    assert not CODEX_PAYLOAD_PATH.exists()


def test_reference_certificates_satisfy_the_schema():
    for n in (3, 6, 10):
        validate_schema(load_reference(n))
