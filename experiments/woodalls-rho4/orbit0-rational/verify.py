#!/usr/bin/env python3
"""Verify the rational orbit-0 higher-cover obstruction."""

import json
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ID1009 = HERE.parent / "id1009-realization" / "certificate.json"


def word_mask(word: str) -> int:
    return sum(1 << int(char, 12) for char in word)


def image(value: int, relabelling: tuple[int, ...]) -> int:
    return sum(1 << relabelling[v] for v in range(8) if value >> v & 1)


def exchanges(first: int, second: int, bijection: dict[int, int]) -> tuple[int, ...]:
    first_elements = [v for v in range(12) if first >> v & 1]
    output = []
    for subset_bits in range(1, 1 << 4):
        subset = sum(1 << first_elements[i] for i in range(4) if subset_bits >> i & 1)
        image_subset = sum(
            1 << bijection[first_elements[i]] for i in range(4) if subset_bits >> i & 1
        )
        output.extend(((first & ~subset) | image_subset, (second & ~image_subset) | subset))
    return tuple(output)


def forced_nonbase(candidate: int, shore: int, demand: int) -> bool:
    """A demand y(X)>=d violates the M1 basis row for candidate Q."""
    return demand >= shore.bit_count() + (candidate & shore).bit_count()


def main() -> None:
    canonical = {word_mask(base) for base in json.loads(ID1009.read_text())["target_bases"]}
    left_map = (11, 4, 9, 8, 7, 5, 6, 10)
    right_map = (11, 0, 9, 8, 3, 1, 2, 10)
    families = ({image(base, left_map) for base in canonical},
                {image(base, right_map) for base in canonical})
    assert [len(family) for family in families] == [32, 32]
    assert len(families[0] | families[1]) == 63

    demand_items = tuple(
        (int(shore, 16), demand)
        for shore, demand in (("4cc", 5), ("7ee", 11), ("811", 3),
                              ("abb", 9), ("b55", 8), ("d33", 8))
    )
    for family in families:
        for shore, demand in demand_items:
            cap = min(
                shore.bit_count() + (base & shore).bit_count() - 1 for base in family
            )
            assert demand <= cap

    canonical_pair = (word_mask("0237"), word_mask("0456"))
    ordering_counts = []
    for relabelling, family in zip((left_map, right_map), families):
        first, second = (image(base, relabelling) for base in canonical_pair)
        assert first in family and second in family
        first_elements = [v for v in range(12) if first >> v & 1]
        second_elements = [v for v in range(12) if second >> v & 1]
        covered = 0
        for target_order in permutations(second_elements):
            bijection = dict(zip(first_elements, target_order))
            candidates = exchanges(first, second, bijection)
            if any(
                forced_nonbase(candidate, shore, demand)
                for candidate in candidates
                for shore, demand in demand_items
            ):
                covered += 1
        ordering_counts.append(covered)
    assert ordering_counts == [24, 24]

    demand_shores = tuple(shore for shore, _ in demand_items)
    cap_shores = tuple(int(shore, 16) for shore in ("022", "044", "088", "100", "200", "400"))
    special = int("811", 16)
    triple_intersections = {
        tuple(i + 1 for i in indices): hex(
            demand_shores[indices[0]]
            & demand_shores[indices[1]]
            & demand_shores[indices[2]]
        )
        for indices in combinations(range(6), 3)
        if (demand_shores[indices[0]] & demand_shores[indices[1]] & demand_shores[indices[2]])
    }
    assert triple_intersections == {
        (1, 2, 4): "0x88", (1, 2, 5): "0x44", (1, 2, 6): "0x400",
        (2, 4, 5): "0x200", (2, 4, 6): "0x22", (2, 5, 6): "0x100",
        (3, 4, 5): "0x811", (3, 4, 6): "0x811", (3, 5, 6): "0x811",
        (4, 5, 6): "0x811",
    }
    fourfold = {}
    for indices in combinations(range(6), 4):
        intersection = demand_shores[indices[0]]
        for i in indices[1:]:
            intersection &= demand_shores[i]
        if intersection:
            fourfold[tuple(i + 1 for i in indices)] = hex(intersection)
    assert fourfold == {(3, 4, 5, 6): "0x811"}
    assert not any(
        demand_shores[indices[0]]
        & demand_shores[indices[1]]
        & demand_shores[indices[2]]
        & demand_shores[indices[3]]
        & demand_shores[indices[4]]
        for indices in combinations(range(6), 5)
    )
    signatures: dict[tuple[str, str, int], tuple[int, int]] = {}
    for support_tuple in combinations_with_replacement(range(12), 3):
        support = sum(1 << v for v in set(support_tuple))
        demand_signature = "".join(
            str(i + 1) for i, shore in enumerate(demand_shores) if support & ~shore == 0
        ) or "-"
        cap_signature = "".join(
            str(i + 1) for i, shore in enumerate(cap_shores) if support & ~shore == 0
        ) or "-"
        special_containment = int(support & ~special == 0)
        gap = (
            len(demand_signature.replace("-", ""))
            - 2
            - len(cap_signature.replace("-", ""))
            - 2 * special_containment
        )
        assert gap <= 0
        key = (demand_signature, cap_signature, special_containment)
        count, maximum = signatures.get(key, (0, -10**9))
        signatures[key] = (count + 1, max(maximum, gap))

    assert len(signatures) == 19
    assert sum(count for count, _ in signatures.values()) == 364
    assert max(maximum for _, maximum in signatures.values()) == 0
    tau_caps = tuple((4 * shore.bit_count() - 3) // 3 for shore in cap_shores)
    assert tau_caps == (1, 1, 1, 0, 0, 0)
    assert (4 * special.bit_count() - 3) // 3 == 3
    demand_sum = sum(demand for _, demand in demand_items)
    upper_sum = 2 * 16 + sum(tau_caps) + 2 * 3
    assert demand_sum == 44 and upper_sum == 41
    print("ID1009 image bases: 32 + 32, union 63")
    print("candidate orderings covered:", ordering_counts)
    print("support multitriples: 364 in", len(signatures), "signatures")
    print("contradiction:", demand_sum, "<=", upper_sum)


if __name__ == "__main__":
    main()
