#!/usr/bin/env python3
"""Exact census of bad complementary bases in rho=4 ACZ fixtures."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
from itertools import combinations, permutations
import json
import multiprocessing
from pathlib import Path

from acz import BipartiteDigraph, d27, minimum_dicut, random_rho4
from independent_verify import bases_by_sink_subsets


Ground = frozenset[int]
BaseFamily = frozenset[Ground]


def failed_sbo_pair(bases: BaseFamily, ground: Ground) -> tuple[Ground, Ground] | None:
    """Return a base pair admitting no strong ordering, or None if SBO."""

    restricted = frozenset(base for base in bases if base <= ground)
    rank = len(next(iter(restricted))) if restricted else 0
    # Uniform matroids are strongly base orderable.  This exact equality check
    # avoids enumerating every pair and bijection in the overwhelmingly common
    # unconstrained restriction.
    if restricted == frozenset(map(frozenset, combinations(ground, rank))):
        return None
    for first in restricted:
        for second in restricted:
            common = first & second
            left = tuple(sorted(first - common))
            right = tuple(sorted(second - common))
            pair_ok = False
            for image_tuple in permutations(right):
                image = dict(zip(left, image_tuple))
                if all(
                    (
                        (first - chosen) | frozenset(image[x] for x in chosen) in restricted
                        and (second - frozenset(image[x] for x in chosen)) | chosen in restricted
                    )
                    for size in range(len(left) + 1)
                    for chosen in map(frozenset, combinations(left, size))
                ):
                    pair_ok = True
                    break
            if not pair_ok:
                return first, second
    return None


def eligible_split(bases: BaseFamily, ground: Ground) -> tuple[Ground, Ground] | None:
    for first in bases:
        if first <= ground and ground - first in bases:
            return first, ground - first
    return None


def maximum_disjoint_subfamily(family: BaseFamily) -> tuple[Ground, ...]:
    ordered = tuple(sorted(family, key=lambda item: tuple(sorted(item))))
    best: tuple[Ground, ...] = ()

    def visit(index: int, used: Ground, chosen: tuple[Ground, ...]) -> None:
        nonlocal best
        if len(chosen) + len(ordered) - index <= len(best):
            return
        if index == len(ordered):
            if len(chosen) > len(best):
                best = chosen
            return
        candidate = ordered[index]
        if not candidate & used:
            visit(index + 1, used | candidate, chosen + (candidate,))
        visit(index + 1, used, chosen)

    visit(0, frozenset(), ())
    return best


def census(graph: BipartiteDigraph) -> dict[str, object]:
    bases = bases_by_sink_subsets(graph)
    ground = frozenset(range(len(graph.active_sources)))
    eligible: list[tuple[Ground, Ground, Ground]] = []
    bad: list[tuple[Ground, Ground, Ground, Ground, Ground]] = []
    for complement_base in bases:
        eight_ground = ground - complement_base
        split = eligible_split(bases, eight_ground)
        if split is None:
            continue
        eligible.append((complement_base, *split))
        obstruction = failed_sbo_pair(bases, eight_ground)
        if obstruction is not None:
            bad.append((complement_base, *split, *obstruction))
    bad_family = frozenset(item[0] for item in bad)
    matching = maximum_disjoint_subfamily(bad_family)
    by_complement = {item[0]: item for item in bad}

    def serial(item: Ground) -> list[int]:
        return sorted(item)

    return {
        "base_count": len(bases),
        "eligible_complement_count": len(eligible),
        "bad_complement_count": len(bad),
        "bad_family": [serial(item) for item in sorted(bad_family, key=lambda x: tuple(sorted(x)))],
        "bad_matching_number": len(matching),
        "bad_matching": [
            {
                "K": serial(item),
                "U": serial(ground - item),
                "eligible_split": [serial(by_complement[item][1]), serial(by_complement[item][2])],
                "failed_sbo_pair": [serial(by_complement[item][3]), serial(by_complement[item][4])],
            }
            for item in matching
        ],
    }


def committed_verified_fixtures(directory: Path) -> list[tuple[str, BipartiteDigraph]]:
    fixtures: list[tuple[str, BipartiteDigraph]] = []
    for path in sorted(directory.glob("results*.json")):
        payload = json.loads(path.read_text())
        source_count = int(payload["search_space"]["family"].split(" with ")[1].split(" sources")[0])
        for record in payload["records"]:
            if record.get("independently_verified"):
                seed = int(record["seed"])
                graph = random_rho4(seed, source_count=source_count)
                digest = hashlib.sha256(repr(sorted(graph.arcs)).encode()).hexdigest()
                if digest != record["graph_sha256"]:
                    raise AssertionError(
                        f"fixture digest mismatch for {path.name}:seed={seed}: "
                        f"stored {record['graph_sha256']}, regenerated {digest}"
                    )
                fixtures.append((f"{path.name}:seed={seed}", graph))
    return fixtures


def id1009_graph(directory: Path) -> BipartiteDigraph:
    payload = json.loads((directory / "id1009-realization" / "certificate.json").read_text())
    arcs = tuple(
        (int(source, 12), sink)
        for sink, support in enumerate(payload["supports"])
        for source in support.lower()
    )
    return BipartiteDigraph(12, 16, arcs)


def switch_mutation(graph: BipartiteDigraph, first: int, second: int) -> BipartiteDigraph:
    """Degree-preserving bipartite 2-switch at two arc-list positions."""

    arcs = list(graph.arcs)
    (source_a, sink_a), (source_b, sink_b) = arcs[first], arcs[second]
    if source_a == source_b or sink_a == sink_b:
        raise ValueError("degenerate switch")
    arcs[first] = (source_a, sink_b)
    arcs[second] = (source_b, sink_a)
    mutated = BipartiteDigraph(graph.source_count, graph.sink_count, tuple(arcs))
    if minimum_dicut(mutated) < 3:
        raise AssertionError("selected adversarial switch does not preserve tau=3")
    return mutated


def one_switch_candidates(
    graph: BipartiteDigraph,
) -> tuple[list[tuple[int, int, BipartiteDigraph]], dict[str, int]]:
    """Enumerate and canonically deduplicate the complete one-switch space."""
    original_arcs = tuple(sorted(graph.arcs))
    seen_arc_multisets = {original_arcs}
    candidates: list[tuple[int, int, BipartiteDigraph]] = []
    nondegenerate_pairs = 0
    for first, second in combinations(range(len(graph.arcs)), 2):
        (source_a, sink_a), (source_b, sink_b) = graph.arcs[first], graph.arcs[second]
        if source_a == source_b or sink_a == sink_b:
            continue
        nondegenerate_pairs += 1
        arcs = list(graph.arcs)
        arcs[first], arcs[second] = (source_a, sink_b), (source_b, sink_a)
        canonical = tuple(sorted(arcs))
        if canonical in seen_arc_multisets:
            continue
        seen_arc_multisets.add(canonical)
        candidates.append(
            (first, second, BipartiteDigraph(graph.source_count, graph.sink_count, tuple(arcs)))
        )
    return candidates, {
        "arc_position_pair_count": len(graph.arcs) * (len(graph.arcs) - 1) // 2,
        "nondegenerate_arc_position_pair_count": nondegenerate_pairs,
        "unique_canonical_mutation_count": len(candidates),
    }


def evaluate_one_switch(
    item: tuple[int, int, BipartiteDigraph]
) -> tuple[int, int, dict[str, object] | None]:
    first, second, graph = item
    if minimum_dicut(graph) < 3:
        return first, second, None
    return first, second, census(graph)


def exhaustive_adversarial_census(
    graph: BipartiteDigraph, jobs: int, mutation_cache: Path | None = None
) -> tuple[list[dict[str, object]], dict[str, object]]:
    candidates, counts = one_switch_candidates(graph)
    candidate_by_pair = {(first, second): item for first, second, *rest in candidates for item in [(first, second, rest[0])]}
    evaluated_by_pair: dict[tuple[int, int], tuple[int, int, dict[str, object] | None]] = {}
    if mutation_cache and mutation_cache.exists():
        payload = json.loads(mutation_cache.read_text())
        for item in payload["records"]:
            pair = (item["first"], item["second"])
            if pair not in candidate_by_pair:
                raise AssertionError(f"mutation cache contains unknown pair {pair}")
            evaluated_by_pair[pair] = (pair[0], pair[1], item["result"])
    pending = [item for item in candidates if (item[0], item[1]) not in evaluated_by_pair]
    if jobs == 1:
        iterator = map(evaluate_one_switch, pending)
        for completed, result in enumerate(iterator, 1):
            evaluated_by_pair[(result[0], result[1])] = result
            if mutation_cache and (completed % 10 == 0 or completed == len(pending)):
                mutation_cache.write_text(
                    json.dumps(
                        {
                            "candidate_count": len(candidates),
                            "records": [
                                {"first": first, "second": second, "result": value[2]}
                                for (first, second), value in sorted(evaluated_by_pair.items())
                            ],
                        },
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n"
                )
                print(f"mutation checkpoint {len(evaluated_by_pair)}/{len(candidates)}", flush=True)
    else:
        with ProcessPoolExecutor(
            max_workers=jobs, mp_context=multiprocessing.get_context("fork")
        ) as executor:
            for result in executor.map(evaluate_one_switch, pending):
                evaluated_by_pair[(result[0], result[1])] = result
    evaluated = [evaluated_by_pair[(first, second)] for first, second, _ in candidates]
    tau3 = [(first, second, result) for first, second, result in evaluated if result is not None]
    retaining = [item for item in tau3 if item[2]["bad_complement_count"]]
    kills = [item for item in retaining if item[2]["bad_matching_number"] >= 2]
    graph_by_pair = {(first, second): graph for first, second, graph in candidates}
    representatives: list[dict[str, object]] = []
    seen_signatures: set[tuple[int, ...]] = set()
    for first, second, result in retaining:
        signature = tuple(
            int(result[key])
            for key in (
                "base_count", "eligible_complement_count", "bad_complement_count",
                "bad_matching_number",
            )
        )
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        representatives.append({"fixture": f"ID1009-switch={first},{second}", **result})
    counts.update(
        {
            "tau3_mutation_count": len(tau3),
            "f_bad_retaining_mutation_count": len(retaining),
            "disjoint_bad_pair_mutation_count": len(kills),
            "distinct_census_signature_count": len(representatives),
            "jobs": jobs,
            "kill_records": [
                {
                    "fixture": f"ID1009-switch={first},{second}",
                    "graph": {
                        "source_count": graph_by_pair[(first, second)].source_count,
                        "sink_count": graph_by_pair[(first, second)].sink_count,
                        "arcs": [list(arc) for arc in graph_by_pair[(first, second)].arcs],
                    },
                    **result,
                }
                for first, second, result in kills
            ],
        }
    )
    return representatives, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--committed-cache", type=Path)
    parser.add_argument("--mutation-cache", type=Path)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    fixtures = committed_verified_fixtures(directory)
    controls = [
        {"fixture": "D27-rho3-control", **census(d27())},
        {"fixture": "ID1009-realization-control", **census(id1009_graph(directory))},
    ]
    if args.committed_cache and args.committed_cache.exists():
        records = json.loads(args.committed_cache.read_text())
        if [record["fixture"] for record in records] != [fixture_id for fixture_id, _ in fixtures]:
            raise AssertionError("committed cache fixture list mismatch")
    else:
        records = []
        for fixture_id, graph in fixtures:
            record = {"fixture": fixture_id, **census(graph)}
            records.append(record)
            print(
                f"{fixture_id}: bases={record['base_count']} bad={record['bad_complement_count']} "
                f"matching={record['bad_matching_number']}",
                flush=True,
            )
        if args.committed_cache:
            args.committed_cache.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    seed_graph = id1009_graph(directory)
    adversarial, adversarial_scan = exhaustive_adversarial_census(
        seed_graph, args.jobs, args.mutation_cache
    )
    details = {
        "definition": "F_bad consists of full M1 bases K whose eight-element complement splits into two bases and has a non-SBO restriction",
        "committed_verified_fixture_count": len(fixtures),
        "controls": controls,
        "adversarial_family": "complete canonical one-switch mutation space of ID1009; retained records represent distinct census signatures, not isomorphism classes",
        "adversarial_count": len(adversarial),
        "adversarial_scan": adversarial_scan,
        "adversarial_records": adversarial,
        "record_count": len(records),
        "maximum_bad_matching_number": max(
            (record["bad_matching_number"] for record in controls + records + adversarial),
            default=0,
        ),
        "records": records,
    }
    summary = {
        "adversarial_count": len(adversarial),
        "adversarial_family": details["adversarial_family"],
        "adversarial_records": [
            {
                key: record[key]
                for key in (
                    "fixture", "base_count", "eligible_complement_count",
                    "bad_complement_count", "bad_matching_number", "bad_family",
                )
            }
            for record in adversarial
        ],
        "adversarial_scan": adversarial_scan,
        "committed_verified_corpus": {
            "fixture_count": len(fixtures),
            "fixtures": "seed 0 for source counts 13,14,15,16 and seeds 0,10,...,990 for source count 12, exactly records marked independently_verified in results*.json",
            "maximum_bad_complement_count": max(record["bad_complement_count"] for record in records),
            "maximum_bad_matching_number": max(record["bad_matching_number"] for record in records),
        },
        "controls": {
            record["fixture"]: {
                key: record[key]
                for key in (
                    "base_count", "eligible_complement_count", "bad_complement_count",
                    "bad_matching_number", "bad_family",
                )
            }
            for record in controls
        },
        "definition": details["definition"],
        "maximum_bad_matching_number_observed": details["maximum_bad_matching_number"],
        "status": "numerical-no-disjoint-bad-pair",
    }
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.details_output:
        args.details_output.write_text(json.dumps(details, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
