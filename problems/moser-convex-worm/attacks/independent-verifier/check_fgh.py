#!/usr/bin/env python3
"""Independent exact-rational checker for the conditional f/g/h angular gate."""

import json
import sys
from fractions import Fraction as Q
from math import factorial
from pathlib import Path

TARGET = Q(113749, 500000)


class Reject(ValueError):
    pass


def strict_object(pairs):
    """Build a JSON object while rejecting duplicate keys."""
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject(f"duplicate JSON field: {key}")
        out[key] = value
    return out


def rational(value, label):
    """Accept only canonical JSON strings encoding finite rational numbers."""
    if not isinstance(value, str):
        raise Reject(f"{label} must be a rational string")
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise Reject(f"invalid rational in {label}") from exc
    if str(result) != value:
        raise Reject(f"non-canonical rational in {label}")
    return result


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise Reject("reversed interval")

    def __add__(self, other):
        other = interval(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -interval(other)

    def __mul__(self, other):
        other = interval(other)
        products = (self.lo*other.lo, self.lo*other.hi,
                    self.hi*other.lo, self.hi*other.hi)
        return I(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = interval(other)
        if other.lo <= 0 <= other.hi:
            raise Reject("division interval contains zero")
        return self * I(1/other.hi, 1/other.lo)

    def square(self):
        if self.lo <= 0 <= self.hi:
            return I(0, max(self.lo*self.lo, self.hi*self.hi))
        return I(min(self.lo*self.lo, self.hi*self.hi),
                 max(self.lo*self.lo, self.hi*self.hi))


def interval(value):
    return value if isinstance(value, I) else I(value)


def atan_reciprocal(n, terms):
    """Enclose atan(1/n) by consecutive alternating-series partial sums."""
    n = Q(n)
    total = Q(0)
    for k in range(terms):
        term = Q(1, (2*k + 1) * n**(2*k + 1))
        total += term if k % 2 == 0 else -term
    k = terms
    next_term = Q(1, (2*k + 1) * n**(2*k + 1))
    following = total + (next_term if k % 2 == 0 else -next_term)
    return I(min(total, following), max(total, following))


def pi_interval():
    """Derive pi via Machin's identity, with no trusted decimal endpoint."""
    # atan series terms decrease strictly for 0 < 1/n < 1.  Machin's exact
    # identity is pi/4 = 4 atan(1/5) - atan(1/239).
    enclosure = 16*atan_reciprocal(5, 55) - 4*atan_reciprocal(239, 18)
    if not Q(3) < enclosure.lo <= enclosure.hi < Q(4):
        raise Reject("derived pi enclosure invariant failed")
    return enclosure


PI = pi_interval()


def degrees(value):
    value = Q(value)
    if value >= 0:
        return I(value*PI.lo/180, value*PI.hi/180)
    return I(value*PI.hi/180, value*PI.lo/180)


def trig_taylor(x, cosine, terms=18):
    x2 = x.square()
    power = I(1) if cosine else x
    total = I(0)
    last_degree = 0
    for k in range(terms):
        degree = 2*k if cosine else 2*k+1
        total = total + (-1 if k % 2 else 1)*power/factorial(degree)
        power = power*x2
        last_degree = degree
    # |derivative| <= 1 gives a Lagrange remainder; one extra degree is a
    # deliberately conservative exponent.
    radius = max(abs(x.lo), abs(x.hi))
    remainder = radius**(last_degree+2)/factorial(last_degree+2)
    return I(total.lo-remainder, total.hi+remainder)


def sin_point(angle):
    return trig_taylor(degrees(angle), False)


def cos_point(angle):
    return trig_taylor(degrees(angle), True)


def sqrt2():
    hi = Q(2)
    for _ in range(12):
        hi = (hi+2/hi)/2
    lo = 2/hi
    if not (lo*lo <= 2 <= hi*hi):
        raise Reject("sqrt(2) enclosure invariant failed")
    return I(lo, hi)


def require(bound, label):
    if bound.lo < TARGET:
        raise Reject(f"{label} lower endpoint does not clear target")


def validate(alpha, beta_low, beta_high):
    # These inequalities are the exact subdivision ledger: the four leaves
    # cover alpha >= alpha_cut, beta <= beta_low, beta >= beta_high, and the
    # remaining closed rectangle.  Checking only the function values would
    # leave the certificate's claimed compact-domain coverage implicit.
    if not Q(45) <= alpha <= Q(78):
        raise Reject("alpha cutoff lies outside root domain")
    if not Q(83) <= beta_low <= beta_high <= Q(97):
        raise Reject("beta cutoffs do not form an ordered partition of root domain")

    # Check the exact monotonicity domains used by the three outer leaves.
    if not alpha <= Q(90):
        raise Reject("g monotonicity interval is not certified")
    if not Q(90) <= Q(83)+30 <= beta_low+30 <= Q(180):
        raise Reject("h_plus monotonicity interval is not certified")
    if not Q(0) <= beta_high-30 <= Q(97)-30 <= Q(90):
        raise Reject("h_minus monotonicity interval is not certified")

    # For fixed alpha, the first cosine in f is concave in beta, hence its
    # minimum is at an endpoint. beta_high is the farther endpoint from the
    # symmetry centre alpha+15 exactly under this midpoint inequality.
    if alpha+15 > (beta_low+beta_high)/2:
        raise Reject("f beta-endpoint reduction is not certified")
    if Q(45)-beta_high+15 < -90 or alpha-beta_low+15 > 90:
        raise Reject("f cosine argument leaves certified range")

    # Endpoint evaluation is justified by the monotonic intervals recorded in
    # the schema: g increases, h_plus decreases, and h_minus increases.
    require(sqrt2()*sin_point(alpha)/6, "g cutoff")
    require(sin_point(beta_low+30)/4, "h_plus cutoff")
    require(sin_point(beta_high-30)/4, "h_minus cutoff")

    def reduced_f(a):
        return (cos_point(a-beta_high+15)/2 + cos_point(a-45))/6

    # Both cosine arguments stay in [-pi/2,pi/2], so reduced_f is concave;
    # exact endpoint checks cover the whole remaining alpha interval.
    require(reduced_f(Q(45)), "f left endpoint")
    require(reduced_f(alpha), "f right endpoint")


def check(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"),
                     object_pairs_hook=strict_object,
                     parse_constant=lambda value: (_ for _ in ()).throw(
                         Reject(f"non-finite JSON number: {value}")))
    expected = {"schema_version", "claim_scope", "target_rational", "angle_unit",
                "root_domain", "cutoffs", "proof_partition"}
    if not isinstance(doc, dict) or set(doc) != expected:
        raise Reject("unknown or missing top-level field")
    if doc["schema_version"] != "moser-fgh-cutoff-v1":
        raise Reject("unsupported schema")
    if doc["claim_scope"] != "conditional_angular_fgh_only":
        raise Reject("certificate must not claim a global placement theorem")
    if rational(doc["target_rational"], "target_rational") != TARGET:
        raise Reject("wrong target")
    if doc["angle_unit"] != "degree":
        raise Reject("wrong angle unit")
    if doc["root_domain"] != {"alpha": ["45", "78"], "beta": ["83", "97"]}:
        raise Reject("wrong root domain")
    if doc["proof_partition"] != ["g", "h_plus", "h_minus", "f_reduced_concave"]:
        raise Reject("wrong proof partition")
    cut = doc["cutoffs"]
    if not isinstance(cut, dict) or set(cut) != {"alpha", "beta_low", "beta_high"}:
        raise Reject("wrong cutoff fields")
    validate(rational(cut["alpha"], "cutoffs.alpha"),
             rational(cut["beta_low"], "cutoffs.beta_low"),
             rational(cut["beta_high"], "cutoffs.beta_high"))


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} CERTIFICATE.json", file=sys.stderr)
        return 2
    try:
        check(sys.argv[1])
    except (OSError, json.JSONDecodeError, Reject) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1
    print("PASS exact conditional f/g/h angular certificate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
