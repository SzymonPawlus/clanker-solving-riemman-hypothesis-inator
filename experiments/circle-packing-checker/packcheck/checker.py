"""Exact verification of a circle-packing certificate.

WHAT IS BEING CHECKED (the definition lives in
`problems/circle-packing-equilateral-triangle/README.md`, not here)
-------------------------------------------------------------------
By the reduction in that README, packing `n` unit circles into an equilateral
triangle of side `s` is equivalent to placing `n` points at pairwise distance `>= 2`
inside an equilateral triangle of side

    d = s - 2*sqrt(3).

This module verifies exactly that, for a certificate in the JSON format of the
problem's `RULES.md` §2, in two clearly separated stages:

  stage 1, `validate_schema` -- the object has the required fields, of the right
      types, with values in the sets the spec pins (in particular `claim` must be
      `construction`; nothing is defaulted);
  stage 2, `check_certificate` -- the geometry:
      (1) all C(n,2) pairwise distances are >= 2,
      (2) all n points lie in the (closed) equilateral triangle of side d,
      (3) the reported `side_length` is consistent with the coordinates.

A certificate arrives from outside, so its scalar strings are untrusted input; they
are read by the allowlisted grammar in `safeparse.py`, which never evaluates Python.

Everything is decided in exact arithmetic -- see `exact.py` for the representation
choice and the sign-decision procedure. No float is constructed anywhere on this
path, and "very nearly feasible" is reported as infeasible.

CONVENTIONS, NOW PINNED BY THE SPEC
-----------------------------------
These were reported as ambiguities when this checker was written; `RULES.md` §2 of
the problem has since fixed all of them ("Fixed conventions -- do not reinterpret
these"), and what follows is what this checker implements, matching that text. Two
independently written checkers are supposed to agree here, so a disagreement is a
finding to investigate rather than to average away.

  A. *Placement of the triangle.* This checker fixes the canonical placement

         A = (0, 0),   B = (d, 0),   C = (d/2, d*sqrt(3)/2)

     and requires the points to lie in it as given. It does NOT search over
     rotations or translations, so a certificate written against a different
     placement is invalid, not merely inconvenient.
  B. *Closed vs open triangle.* "Inside" is read as the CLOSED triangle. It has to
     be: in every optimal packing some circles touch the sides, so points sit
     exactly on the boundary.
  C. *Distance `>= 2` is non-strict.* Touching circles are feasible. Again forced:
     optima are tight.
  D. *`side_length` is `s`, not `d`.* The format calls it "value of s(n)" and the
     tables in README.md quote `s`, so the string is parsed as `s` and `d` is
     derived. A certificate that reports `d` will (correctly) fail containment.
  E. *"Consistent with the coordinates" is ambiguous.* Containment alone only
     certifies the upper bound `s(n) <= s`; a certificate could report a wildly
     inflated `s` and pass. This checker therefore also computes the exact minimal
     side `d_min` for which the given points fit the canonical placement, and
     reports whether `s == d_min + 2*sqrt(3)`. By default a non-tight `s` is a
     WARNING (an inflated `s` is a weak but true claim); `--require-tight` makes it
     an error, which §4 requires for any record claim.
  F. *Decimal strings are banned in exact fields.* `"10.928"` is exactly 1366/125,
     but is almost always truncated optimiser output, so it is rejected rather than
     parsed with a warning.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import sympy

from .exact import (
    SQRT3,
    RatInterval,
    UndecidedSign,
    UnsupportedExpression,
    enclose,
    is_nonneg,
    sign_of,
)
from .safeparse import UnsafeExpression, parse_scalar

__all__ = [
    "CheckResult",
    "Certificate",
    "validate_schema",
    "check_certificate",
    "check_file",
]

# Enclosure precision used for `coordinate_type: interval` certificates.
INTERVAL_BITS = 256


class CertificateError(Exception):
    """The certificate is malformed -- distinct from being infeasible."""


# --------------------------------------------------------------------------- #
# Parsing: strings -> exact algebraic numbers. Floats are refused, and so is
# anything outside the allowlisted grammar in `safeparse` -- see that module for
# why sympy's `parse_expr` is not used here.
# --------------------------------------------------------------------------- #

def parse_exact(text) -> sympy.Expr:
    """Parse a certificate scalar into an exact sympy number.

    Accepts integers, rationals like `7/3`, and radical expressions like
    `4 + 4*sqrt(3)`. Certificate text is untrusted, so it goes through
    `safeparse.parse_scalar`, which interprets an allowlisted syntax tree and never
    evaluates Python -- no builtin, attribute or import is reachable from it.
    Decimal literals such as `10.928` are rejected outright, per the ban on decimal
    strings in exact fields in the problem's `RULES.md` §2.
    """
    if isinstance(text, bool):
        raise CertificateError(f"boolean where a number was expected: {text!r}")
    if isinstance(text, float):
        raise CertificateError(
            f"JSON float {text!r} in a certificate; coordinates must be exact "
            "(quote them as strings: \"7/3\", \"4 + 4*sqrt(3)\")"
        )
    if isinstance(text, int):
        return sympy.Integer(text)
    if not isinstance(text, str):
        raise CertificateError(f"cannot parse {text!r} as an exact number")
    try:
        expr = parse_scalar(text)
    except UnsafeExpression as exc:
        raise CertificateError(f"could not parse {text!r} exactly: {exc}") from exc
    if not expr.is_real:
        raise CertificateError(f"{text!r} is not a real number")
    if expr.free_symbols:
        # Unreachable through `parse_scalar` (it admits no names), kept as a second
        # gate so a future grammar change cannot silently let a symbol through.
        raise CertificateError(f"{text!r} contains free symbols {expr.free_symbols}")
    return expr


# --------------------------------------------------------------------------- #
# Certificate model
# --------------------------------------------------------------------------- #

@dataclass
class Certificate:
    n: int
    claim: str
    side_length: sympy.Expr
    coordinates: list[tuple]  # exprs, or (RatInterval, RatInterval) for interval type
    coordinate_type: str
    raw: dict
    warnings: list[str] = field(default_factory=list)

    @property
    def is_interval(self) -> bool:
        return self.coordinate_type == "interval"


# Checking a certificate happens in two clearly separated stages:
#
#   1. `validate_schema` -- is this object the right SHAPE? Required fields present,
#      of the right type, with values in the sets the problem's `RULES.md` §2 pins.
#      Nothing geometric happens here and no scalar is parsed.
#   2. `check_certificate` -- given a well-formed certificate, is the packing it
#      describes actually FEASIBLE?
#
# The split matters because a schema failure and a geometry failure mean different
# things: the first says the file is not a certificate, the second says it is a
# certificate of something false. Stage 1 also fails closed on anything it does not
# recognise, so a missing or unexpected field is never defaulted into a pass.

REQUIRED_FIELDS = (
    "n",
    "claim",
    "side_length",
    "coordinates",
    "coordinate_type",
    "verified_by",
    "status",
    "beats_record",
)

# This checker certifies CONSTRUCTIONS -- upper bounds `s(n) <= c` -- and nothing
# else. `RULES.md` §1 of the problem separates that from an optimality claim, which
# needs an exhaustive lower-bound argument no feasibility check can supply.
SUPPORTED_CLAIM = "construction"

COORDINATE_TYPES = ("rational", "algebraic", "interval")
STATUSES = ("numerical", "verified:review", "verified:lean")


def validate_schema(data) -> None:
    """Raise `CertificateError` unless `data` matches the pinned certificate schema.

    Shape only -- see `problems/circle-packing-equilateral-triangle/RULES.md` §2.
    Extra fields are permitted (the reference fixtures carry a `_note`); missing or
    ill-typed required fields are not, and no field is given a default.
    """
    if not isinstance(data, dict):
        raise CertificateError(f"certificate must be a JSON object, got {type(data).__name__}")

    missing = [key for key in REQUIRED_FIELDS if key not in data]
    if missing:
        raise CertificateError(
            f"certificate is missing required field(s) {', '.join(repr(k) for k in missing)}; "
            f"the schema requires {', '.join(REQUIRED_FIELDS)} (problem RULES.md §2)"
        )

    claim = data["claim"]
    if claim != SUPPORTED_CLAIM:
        raise CertificateError(
            f"claim must be {SUPPORTED_CLAIM!r}, got {claim!r}. This checker verifies "
            "feasibility, which certifies an upper bound s(n) <= side_length and nothing "
            "more; an optimality or counterexample claim needs an argument it cannot supply."
        )

    n = data["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise CertificateError(f"n must be a positive integer, got {n!r}")

    ctype = data["coordinate_type"]
    if ctype not in COORDINATE_TYPES:
        raise CertificateError(
            f"coordinate_type must be {'|'.join(COORDINATE_TYPES)}, got {ctype!r}"
        )

    status = data["status"]
    if status not in STATUSES:
        raise CertificateError(f"status must be {'|'.join(STATUSES)}, got {status!r}")

    for key in ("verified_by", "beats_record"):
        value = data[key]
        if not isinstance(value, str) or not value.strip():
            raise CertificateError(f"{key} must be a non-empty string, got {value!r}")

    coords = data["coordinates"]
    if not isinstance(coords, list):
        raise CertificateError("coordinates must be a list")
    if len(coords) != n:
        raise CertificateError(
            f"certificate declares n = {n} but lists {len(coords)} coordinates"
        )


def load_certificate(data: dict) -> Certificate:
    """Validate the schema, then parse every scalar into an exact number."""
    validate_schema(data)

    n = data["n"]
    ctype = data["coordinate_type"]
    side = parse_exact(data["side_length"])

    coords = []
    for index, point in enumerate(data["coordinates"]):
        if not isinstance(point, list) or len(point) != 2:
            raise CertificateError(f"coordinate {index} is not a [x, y] pair: {point!r}")
        if ctype == "interval":
            coords.append(tuple(_parse_interval(c, index) for c in point))
        else:
            parsed = tuple(parse_exact(c) for c in point)
            if ctype == "rational" and not all(c.is_Rational for c in parsed):
                raise CertificateError(
                    f"coordinate {index} is not rational but coordinate_type is 'rational'"
                )
            coords.append(parsed)

    return Certificate(
        n=n,
        claim=data["claim"],
        side_length=side,
        coordinates=coords,
        coordinate_type=ctype,
        raw=data,
    )


def _parse_interval(component, index: int) -> RatInterval:
    """An interval coordinate component, encoded as a two-element [lo, hi] list.

    SPEC AMBIGUITY: RULES.md §2 permits `coordinate_type: "interval"` but never says
    how an interval is written inside the `coordinates` array. This checker requires
    the nested form  [[xlo, xhi], [ylo, yhi]]  and rejects anything else rather than
    guessing.
    """
    if not isinstance(component, list) or len(component) != 2:
        raise CertificateError(
            f"coordinate {index}: interval components must be written [lo, hi]; got "
            f"{component!r}. (RULES.md §2 does not specify this encoding -- see "
            "the experiment README.)"
        )
    lo_expr, hi_expr = (parse_exact(c) for c in component)
    if not (lo_expr.is_Rational and hi_expr.is_Rational):
        raise CertificateError(
            f"coordinate {index}: interval endpoints must be rational, got "
            f"{lo_expr} .. {hi_expr}"
        )
    lo = Fraction(int(lo_expr.p), int(lo_expr.q))
    hi = Fraction(int(hi_expr.p), int(hi_expr.q))
    if lo > hi:
        raise CertificateError(f"coordinate {index}: empty interval [{lo}, {hi}]")
    return RatInterval(lo, hi)


# --------------------------------------------------------------------------- #
# The check itself
# --------------------------------------------------------------------------- #

@dataclass
class CheckResult:
    ok: bool
    n: int
    coordinate_type: str
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def render(self) -> str:
        lines = [
            f"n = {self.n}   coordinate_type = {self.coordinate_type}",
            *(f"  note:    {m}" for m in self.notes),
            *(f"  WARNING: {m}" for m in self.warnings),
            *(f"  FAIL:    {m}" for m in self.failures),
            "RESULT: ACCEPT (exact)" if self.ok else "RESULT: REJECT",
        ]
        return "\n".join(lines)


def _nonneg(value) -> bool:
    return is_nonneg(value)


def check_certificate(data: dict, require_tight: bool = False) -> CheckResult:
    """Verify a certificate dict exactly. Returns a CheckResult; never raises on
    infeasibility (that is a REJECT), only on a malformed certificate."""
    cert = load_certificate(data)
    failures: list[str] = []
    warnings: list[str] = list(cert.warnings)
    notes: list[str] = []

    if cert.is_interval:
        sqrt3 = enclose(SQRT3, INTERVAL_BITS)
        side = enclose(cert.side_length, INTERVAL_BITS)
        two = RatInterval.exact(2)
        four = RatInterval.exact(4)
        notes.append(
            f"interval mode: enclosures at 2**-{INTERVAL_BITS}; a certificate whose "
            "circles exactly touch cannot be certified this way (see exact.py)."
        )
    else:
        sqrt3 = SQRT3
        side = cert.side_length
        two = sympy.Integer(2)
        four = sympy.Integer(4)

    d = side - two * sqrt3  # side of the triangle of admissible centres

    # (3a) the point-formulation triangle must be non-degenerate.
    try:
        if not _nonneg(d):
            failures.append(
                f"side_length {sympy.sstr(cert.side_length)} gives d = s - 2*sqrt(3) < 0: "
                "no unit circle fits at all"
            )
            return CheckResult(False, cert.n, cert.coordinate_type, failures, warnings, notes)
    except (UndecidedSign, UnsupportedExpression) as exc:
        failures.append(f"could not decide sign of d = s - 2*sqrt(3) exactly: {exc}")
        return CheckResult(False, cert.n, cert.coordinate_type, failures, warnings, notes)

    # (1) pairwise distances >= 2, i.e. dx^2 + dy^2 - 4 >= 0.
    pts = cert.coordinates
    for i in range(cert.n):
        for j in range(i + 1, cert.n):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            gap = dx * dx + dy * dy - four
            try:
                if not _nonneg(gap):
                    failures.append(
                        f"points {i} and {j} are closer than 2: "
                        f"|p{i}-p{j}|^2 - 4 = {_show(gap)} < 0"
                    )
            except (UndecidedSign, UnsupportedExpression) as exc:
                failures.append(f"points {i},{j}: distance sign undecided: {exc}")

    # (2) containment in the CLOSED triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2).
    #     Edge AB: y >= 0.  Edge AC: sqrt(3)*x - y >= 0.  Edge BC: sqrt(3)*(d - x) - y >= 0.
    for i, (x, y) in enumerate(pts):
        constraints = (
            ("below edge AB (y >= 0)", y),
            ("outside edge AC (sqrt(3)*x - y >= 0)", sqrt3 * x - y),
            ("outside edge BC (sqrt(3)*(d - x) - y >= 0)", sqrt3 * (d - x) - y),
        )
        for label, value in constraints:
            try:
                if not _nonneg(value):
                    failures.append(f"point {i} is {label}: value = {_show(value)} < 0")
            except (UndecidedSign, UnsupportedExpression) as exc:
                failures.append(f"point {i}: containment sign undecided ({label}): {exc}")

    # (3b) tightness of the reported side length.
    tight_note = _tightness(cert, pts, sqrt3, side, two)
    if tight_note is not None:
        if require_tight:
            failures.append(tight_note)
        else:
            warnings.append(tight_note)

    if cert.n == 1:
        notes.append("n = 1: there are no pairwise constraints to check")

    return CheckResult(
        ok=not failures,
        n=cert.n,
        coordinate_type=cert.coordinate_type,
        failures=failures,
        warnings=warnings,
        notes=notes,
    )


def _tightness(cert: Certificate, pts, sqrt3, side, two) -> str | None:
    """Return a message if the reported s is strictly larger than necessary.

    With the canonical placement, edges AB and AC do not involve d, so the smallest
    admissible d is  d_min = max_i (x_i + y_i/sqrt(3)),  read straight off the BC
    constraint. `None` means s == d_min + 2*sqrt(3) exactly (or the question does not
    apply, e.g. interval coordinates).
    """
    if cert.is_interval:
        return None  # an interval certificate cannot certify an equality; see exact.py
    if not pts:
        return None
    try:
        needed = [x + y / sqrt3 for (x, y) in pts]
        d_min = needed[0]
        for value in needed[1:]:
            if sign_of(value - d_min) > 0:
                d_min = value
        s_min = sympy.simplify(d_min + two * sqrt3)
        slack = sympy.expand(cert.side_length - s_min)
        if sign_of(slack) == 0:
            return None
        return (
            f"side_length is not tight: the coordinates fit in a triangle of side "
            f"{sympy.sstr(s_min)} ~= {_approx(s_min)}, but the certificate reports "
            f"{sympy.sstr(cert.side_length)} ~= {_approx(cert.side_length)}. "
            "Containment still holds, so the upper bound s(n) <= reported value is "
            "valid, just weak."
        )
    except (UndecidedSign, UnsupportedExpression) as exc:
        return f"could not decide side-length tightness exactly: {exc}"


def _show(value) -> str:
    if isinstance(value, RatInterval):
        return f"[{value.lo}, {value.hi}]"
    return sympy.sstr(sympy.simplify(value))


def _approx(expr) -> str:
    """A human-readable decimal, for MESSAGES ONLY -- never used in any decision.

    Produced from an exact rational enclosure, not from float arithmetic.
    """
    iv = enclose(expr, 64)
    mid = (iv.lo + iv.hi) / 2
    scaled = (mid.numerator * 10**9) // mid.denominator
    sign = "-" if scaled < 0 else ""
    scaled = abs(scaled)
    return f"{sign}{scaled // 10**9}.{scaled % 10**9:09d}"


def check_file(path: str | Path, require_tight: bool = False) -> CheckResult:
    data = json.loads(Path(path).read_text())
    return check_certificate(data, require_tight=require_tight)
