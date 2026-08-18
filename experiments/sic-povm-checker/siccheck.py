#!/usr/bin/env python3
"""Resource-bounded exact SIC-family checker over Q(sqrt(2), sqrt(3), i)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

MAX_FILE_BYTES = 1_000_000
MAX_SCALAR_CHARS = 128
MAX_INTEGER_BITS = 1024
MAX_DIMENSION = 3
RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


class CertificateError(ValueError):
    pass


def _multiply_basis(left: int, right: int) -> tuple[int, int]:
    """Multiply basis indices s2^a s3^b i^c, returning (factor,index)."""
    a = (left & 1) + (right & 1)
    b = ((left >> 1) & 1) + ((right >> 1) & 1)
    c = ((left >> 2) & 1) + ((right >> 2) & 1)
    factor = (2 if a >= 2 else 1) * (3 if b >= 2 else 1) * (-1 if c >= 2 else 1)
    return factor, (a % 2) | ((b % 2) << 1) | ((c % 2) << 2)


@dataclass(frozen=True)
class K:
    """Element of Q(sqrt(2),sqrt(3),i), in the fixed eight-element basis."""

    coefficients: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.coefficients) != 8:
            raise ValueError("field element needs eight coefficients")

    @staticmethod
    def rational(value: int | Fraction) -> "K":
        return K((Fraction(value),) + (Fraction(0),) * 7)

    def __add__(self, other: "K") -> "K":
        return K(tuple(a + b for a, b in zip(self.coefficients, other.coefficients, strict=True)))

    def __neg__(self) -> "K":
        return K(tuple(-x for x in self.coefficients))

    def __sub__(self, other: "K") -> "K":
        return self + (-other)

    def __mul__(self, other: "K") -> "K":
        out = [Fraction(0)] * 8
        for left_index, left in enumerate(self.coefficients):
            for right_index, right in enumerate(other.coefficients):
                factor, index = _multiply_basis(left_index, right_index)
                out[index] += factor * left * right
        return K(tuple(out))

    def conjugate(self) -> "K":
        return K(tuple(-value if index & 4 else value for index, value in enumerate(self.coefficients)))

    def is_zero(self) -> bool:
        return all(value == 0 for value in self.coefficients)


ZERO = K.rational(0)
ONE = K.rational(1)


def parse_rational(value: object, path: str) -> Fraction:
    if not isinstance(value, str) or len(value) > MAX_SCALAR_CHARS or not RATIONAL.fullmatch(value):
        raise CertificateError(f"{path}: expected bounded integer/fraction string; decimals forbidden")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CertificateError(f"{path}: invalid rational") from error
    if abs(result.numerator).bit_length() > MAX_INTEGER_BITS or result.denominator.bit_length() > MAX_INTEGER_BITS:
        raise CertificateError(f"{path}: rational exceeds bit bound")
    return result


def parse_scalar(value: object, path: str) -> K:
    if not isinstance(value, list) or len(value) != 8:
        raise CertificateError(f"{path}: scalar must have eight rational-string coefficients")
    return K(tuple(parse_rational(item, f"{path}[{index}]") for index, item in enumerate(value)))


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path):
    if path.stat().st_size > MAX_FILE_BYTES:
        raise CertificateError("certificate exceeds file-size bound")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise CertificateError(f"invalid JSON: {error}") from error


def inner(left: list[K], right: list[K]) -> K:
    total = ZERO
    for a, b in zip(left, right, strict=True):
        total = total + a.conjugate() * b
    return total


def squared_abs(value: K) -> K:
    return value.conjugate() * value


def verify(data: object) -> dict[str, object]:
    if not isinstance(data, dict):
        raise CertificateError("certificate must be an object")
    allowed = {"certificate_version", "claim", "status", "dimension", "field", "vectors", "povm_weights"}
    unknown = set(data) - allowed
    missing = {"certificate_version", "claim", "status", "dimension", "field", "vectors"} - set(data)
    if unknown:
        raise CertificateError(f"unknown fields: {sorted(unknown)}")
    if missing:
        raise CertificateError(f"missing fields: {sorted(missing)}")
    if data["certificate_version"] != 1 or data["claim"] != "sic-family":
        raise CertificateError("unsupported version or claim")
    if data["status"] != "numerical":
        raise CertificateError("v1 accepts status numerical only")
    if data["field"] != "Q(sqrt2,sqrt3,i)-basis-v1":
        raise CertificateError("unsupported field")
    d = data["dimension"]
    if isinstance(d, bool) or not isinstance(d, int) or not 1 <= d <= MAX_DIMENSION:
        raise CertificateError(f"dimension must be an integer in [1,{MAX_DIMENSION}]")
    raw_vectors = data["vectors"]
    if not isinstance(raw_vectors, list) or len(raw_vectors) != d * d:
        raise CertificateError(f"expected exactly {d*d} vectors")
    vectors = []
    for i, raw_vector in enumerate(raw_vectors):
        if not isinstance(raw_vector, list) or len(raw_vector) != d:
            raise CertificateError(f"vectors[{i}]: expected length {d}")
        vectors.append([parse_scalar(value, f"vectors[{i}][{j}]") for j, value in enumerate(raw_vector)])
    for i, vector in enumerate(vectors):
        if inner(vector, vector) != ONE:
            raise CertificateError(f"vector {i} is not normalized")
    target = K.rational(Fraction(1, d + 1))
    checked_pairs = 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            if squared_abs(inner(vectors[i], vectors[j])) != target:
                raise CertificateError(f"pair {i},{j} has wrong squared overlap")
            checked_pairs += 1

    completeness = False
    if "povm_weights" in data:
        raw_weights = data["povm_weights"]
        if not isinstance(raw_weights, list) or len(raw_weights) != d * d:
            raise CertificateError(f"expected exactly {d*d} POVM weights")
        weights = [parse_scalar(value, f"povm_weights[{i}]") for i, value in enumerate(raw_weights)]
        for i, weight in enumerate(weights):
            if any(weight.coefficients[index] for index in range(1, 8)) or weight.coefficients[0] < 0:
                raise CertificateError(f"povm_weights[{i}]: v1 weights must be nonnegative rationals")
        for row in range(d):
            for column in range(d):
                total = ZERO
                for weight, vector in zip(weights, vectors, strict=True):
                    total = total + weight * vector[row] * vector[column].conjugate()
                expected = ONE if row == column else ZERO
                if total != expected:
                    raise CertificateError(f"POVM completeness fails at matrix entry {row},{column}")
        completeness = True
    return {
        "accepted": True,
        "status": "numerical",
        "dimension": d,
        "vectors": len(vectors),
        "checked_pairs": checked_pairs,
        "povm_completeness_checked": completeness,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args(argv)
    try:
        report = verify(load(args.certificate))
    except (CertificateError, OSError) as error:
        print(json.dumps({"accepted": False, "error": str(error)}, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
