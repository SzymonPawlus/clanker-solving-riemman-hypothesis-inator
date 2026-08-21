#!/usr/bin/env python3
"""Dependency-free verifier for the explicit ID1009 ACZ realization."""

import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def vertex(char: str) -> int:
    return int(char, 12)


def mask(word: str) -> int:
    return sum(1 << vertex(char) for char in word)


def word(value: int, ground_size: int = 8) -> str:
    return "".join(str(i) for i in range(ground_size) if value >> i & 1)


def main() -> None:
    certificate = json.loads((HERE / "certificate.json").read_text())
    sinks = [tuple(vertex(char) for char in support) for support in certificate["supports"]]
    target = {mask(base) for base in certificate["target_bases"]}

    assert len(sinks) == 16
    assert all(len(sink) == 3 for sink in sinks)
    degrees = [sum(sink.count(v) for sink in sinks) for v in range(12)]
    assert degrees == [4] * 12

    support_masks = [sum(1 << v for v in set(sink)) for sink in sinks]
    shore_data = []
    minimum = 10**9
    minimizers = []
    for shore in range(1, (1 << 12) - 1):
        contained = sum((support & ~shore) == 0 for support in support_masks)
        cut = 4 * shore.bit_count() - 3 * contained
        shore_data.append((shore, contained))
        if cut < minimum:
            minimum, minimizers = cut, [shore]
        elif cut == minimum:
            minimizers.append(shore)

    bases = set()
    for subset in combinations(range(8), 4):
        candidate = sum(1 << v for v in subset)
        if all(
            (candidate & shore).bit_count() >= 1 + contained - shore.bit_count()
            for shore, contained in shore_data
        ):
            bases.add(candidate)

    canonical_sinks = [list(sink) for sink in sinks]
    digest = hashlib.sha256(
        json.dumps(canonical_sinks, separators=(",", ":")).encode()
    ).hexdigest()

    assert minimum == 3
    assert minimizers == [mask("2345679AB")]
    assert bases == target
    assert digest == certificate["json_sink_digest"]

    output = {
        "source_degrees": degrees,
        "proper_shores_checked": len(shore_data),
        "minimum_dicut": minimum,
        "minimum_shores": ["2345679AB"],
        "four_subsets_checked": 70,
        "computed_bases": sorted(word(base) for base in bases),
        "missing_bases": [],
        "extra_bases": [],
        "json_sink_digest": digest,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
