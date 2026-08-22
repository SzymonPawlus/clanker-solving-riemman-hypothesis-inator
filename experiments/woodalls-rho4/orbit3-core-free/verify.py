#!/usr/bin/env python3
"""Verify the compact rational certificate for the orbit-3 core-free branch."""

import json
from itertools import combinations_with_replacement
from pathlib import Path


HERE = Path(__file__).resolve().parent
ID1009 = HERE.parent / "id1009-realization" / "certificate.json"


def mask(word: str) -> int:
    return sum(1 << int(char, 12) for char in word)


def hexmask(value: str) -> int:
    return int(value, 16)


def image(value: int, relabelling: dict[int, int]) -> int:
    return sum(1 << relabelling[v] for v in range(8) if value >> v & 1)


def contained(support: int, shore: int) -> int:
    return int(support & ~shore == 0)


def main() -> None:
    target = {mask(base) for base in json.loads(ID1009.read_text())["target_bases"]}
    left_map = dict(enumerate((11, 4, 8, 9, 7, 5, 6, 10)))
    right_map = dict(enumerate((10, 0, 9, 8, 3, 1, 2, 11)))
    left = {image(base, left_map) for base in target}
    right = {image(base, right_map) for base in target}
    required_bases = left | right

    assert len(left) == len(right) == 32
    assert len(required_bases) == 63
    assert {hexmask(base) for base in ("107", "0f0", "4d0", "350")} <= required_bases

    demand_shores = tuple(hexmask(shore) for shore in ("344", "4c1", "81c"))
    cap_shores = tuple(hexmask(shore) for shore in ("818", "81c", "b3e", "cbf"))
    expected_caps = (2, 4, 8, 9)
    witnesses = tuple(hexmask(base) for base in ("107", "0f0", "4d0", "350"))
    for shore, expected, witness in zip(cap_shores, expected_caps, witnesses):
        base_cap = min(
            shore.bit_count() + (base & shore).bit_count() - 1
            for base in required_bases
        )
        assert base_cap == expected
        assert shore.bit_count() + (witness & shore).bit_count() - 1 == expected

    weights = (-1, 2, -1, 2, 2, 2, -4, -1, -1, -1, -1, 2)
    assert sum(weights) == 0
    signatures: dict[tuple[str, str], tuple[int, int]] = {}
    checked = 0
    for support_tuple in combinations_with_replacement(range(12), 3):
        support = sum(1 << v for v in set(support_tuple))
        demand_signature = "".join(
            str(i + 1) for i, shore in enumerate(demand_shores) if contained(support, shore)
        ) or "-"
        cap_signature = "".join(
            str(i + 1) for i, shore in enumerate(cap_shores) if contained(support, shore)
        ) or "-"
        left_value = 6 * len(demand_signature.replace("-", "")) + sum(
            weights[v] for v in support_tuple
        )
        right_value = 3 * len(cap_signature.replace("-", ""))
        assert left_value <= right_value
        count, maximum = signatures.get((demand_signature, cap_signature), (0, -10**9))
        signatures[(demand_signature, cap_signature)] = (
            count + 1,
            max(maximum, left_value - right_value),
        )
        checked += 1

    assert checked == 364
    assert len(signatures) == 12
    assert sum(count for count, _ in signatures.values()) == 364
    assert all(maximum == 0 for _, maximum in signatures.values())
    print("required bases:", len(required_bases))
    print("support multitriples checked:", checked)
    print("containment signatures:", len(signatures))
    print("cap sum:", sum(expected_caps))
    print("demand lower bound after doubling:", 2 * 12)
    print("certificate: 24 <= 23 contradiction")


if __name__ == "__main__":
    main()
