#!/usr/bin/env python3
"""Exact, dependency-free verifier for the issue-55 saturation witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


Arc = tuple[int, int]


def validate(data: object) -> tuple[int, tuple[Arc, ...], int, frozenset[int], Arc]:
    if not isinstance(data, dict) or set(data) != {
        "status",
        "n",
        "arcs",
        "claimed_tau",
        "minimum_dicut_shore",
        "unreachable_source_sink_pair",
    }:
        raise ValueError("unexpected witness schema")
    if data["status"] != "numerical":
        raise ValueError("the finite experiment must retain status numerical")
    n = data["n"]
    claimed_tau = data["claimed_tau"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer at least two")
    if isinstance(claimed_tau, bool) or not isinstance(claimed_tau, int):
        raise ValueError("claimed_tau must be an integer")

    def parse_arc(value: object, name: str) -> Arc:
        if (
            not isinstance(value, list)
            or len(value) != 2
            or any(isinstance(x, bool) or not isinstance(x, int) for x in value)
        ):
            raise ValueError(f"{name} must be an integer pair")
        u, v = value
        if not 0 <= u < v < n:
            raise ValueError(f"{name} must be forward in the declared topological order")
        return u, v

    raw_arcs = data["arcs"]
    if not isinstance(raw_arcs, list):
        raise ValueError("arcs must be a list")
    arcs = tuple(parse_arc(value, f"arcs[{index}]") for index, value in enumerate(raw_arcs))
    if len(set(arcs)) != len(arcs):
        raise ValueError("parallel copies are outside this simple-DAG witness")
    shore_data = data["minimum_dicut_shore"]
    if not isinstance(shore_data, list) or any(
        isinstance(v, bool) or not isinstance(v, int) or not 0 <= v < n for v in shore_data
    ):
        raise ValueError("minimum_dicut_shore must be a vertex list")
    shore = frozenset(shore_data)
    if len(shore) != len(shore_data):
        raise ValueError("minimum_dicut_shore repeats a vertex")
    bad_pair = parse_arc(data["unreachable_source_sink_pair"], "unreachable pair")
    return n, arcs, claimed_tau, shore, bad_pair


def dicuts(n: int, arcs: tuple[Arc, ...]) -> tuple[tuple[frozenset[int], tuple[Arc, ...]], ...]:
    """Enumerate dicuts directly from the no-entering/nonempty-outgoing definition."""
    result = []
    for mask in range(1, (1 << n) - 1):
        shore = frozenset(v for v in range(n) if mask & (1 << v))
        if any(u not in shore and v in shore for u, v in arcs):
            continue
        outgoing = tuple((u, v) for u, v in arcs if u in shore and v not in shore)
        if outgoing:
            result.append((shore, outgoing))
    return tuple(result)


def direct_tau(n: int, arcs: tuple[Arc, ...]) -> int:
    family = dicuts(n, arcs)
    return 0 if not family else min(len(cut) for _, cut in family)


def predecessor_tau(n: int, arcs: tuple[Arc, ...]) -> int:
    """Independent tau oracle using predecessor bitsets and cut popcounts."""
    predecessors = [0] * n
    arc_bits = []
    for u, v in arcs:
        predecessors[v] |= 1 << u
        arc_bits.append((1 << u, 1 << v))
    best: int | None = None
    for mask in range(1, (1 << n) - 1):
        if any(mask & (1 << v) and predecessors[v] & ~mask for v in range(n)):
            continue
        size = sum(bool(mask & tail and not mask & head) for tail, head in arc_bits)
        if size and (best is None or size < best):
            best = size
    return 0 if best is None else best


def source_sink_failure(n: int, arcs: tuple[Arc, ...], pair: Arc) -> bool:
    outgoing = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in arcs:
        outgoing[u].append(v)
        indegree[v] += 1
    source, sink = pair
    if indegree[source] != 0 or outgoing[sink]:
        return False
    reached = {source}
    stack = [source]
    while stack:
        for successor in outgoing[stack.pop()]:
            if successor not in reached:
                reached.add(successor)
                stack.append(successor)
    return sink not in reached


def verify(data: object) -> dict[str, object]:
    n, arcs, claimed_tau, claimed_shore, bad_pair = validate(data)
    actual_tau = direct_tau(n, arcs)
    oracle_tau = predecessor_tau(n, arcs)
    if actual_tau != claimed_tau or oracle_tau != claimed_tau:
        raise ValueError(
            f"tau mismatch: claimed={claimed_tau}, direct={actual_tau}, oracle={oracle_tau}"
        )
    matching = [cut for shore, cut in dicuts(n, arcs) if shore == claimed_shore]
    if len(matching) != 1 or len(matching[0]) != claimed_tau:
        raise ValueError("claimed shore is not a minimum dicut witness")
    minimum_shores = [shore for shore, cut in dicuts(n, arcs) if len(cut) == claimed_tau]
    if minimum_shores != [claimed_shore]:
        raise ValueError(
            "claimed shore is not the unique minimum dicut shore: "
            f"found {len(minimum_shores)}"
        )
    if not source_sink_failure(n, arcs, bad_pair):
        raise ValueError("claimed source-sink pair does not witness failure")

    present = set(arcs)
    additions = []
    for new_arc in (
        (u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in present
    ):
        enlarged = (*arcs, new_arc)
        after = direct_tau(n, enlarged)
        oracle_after = predecessor_tau(n, enlarged)
        if after != oracle_after:
            raise ValueError(f"tau oracles disagree after adding {new_arc}")
        if after <= claimed_tau:
            raise ValueError(f"adding {new_arc} does not strictly raise tau: {after}")
        additions.append({"arc": list(new_arc), "tau_after": after})
    return {
        "accepted": True,
        "status": "numerical",
        "n": n,
        "arcs": len(arcs),
        "tau": claimed_tau,
        "minimum_dicut_shores": len(minimum_shores),
        "minimum_dicut": list(matching[0]),
        "unreachable_source_sink_pair": list(bad_pair),
        "missing_forward_arcs": len(additions),
        "saturation_certificate": additions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness", type=Path, nargs="?", default=Path(__file__).with_name("witness.json"))
    args = parser.parse_args()
    try:
        data = json.loads(args.witness.read_text(encoding="utf-8"))
        report = verify(data)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"accepted": False, "error": str(error)}, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
