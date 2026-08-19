#!/usr/bin/env python3
"""Exhaustive census of {0,1}-weighted Edmonds-Giles instances on small DAGs.

Issue #72 (attack: problems/woodalls-conjecture/attacks/zero-weight-frontier/).

Question decided per instance (D, w), D a weakly connected simple DAG given in a
topological labeling, w in {0,1}^A:

    with tau_w := min over dicuts B of w(B), does there exist a "w-packing" of
    tau_w dijoins, i.e. dijoins J_1..J_{tau_w} such that every arc a lies in at
    most w(a) of them?

Every instance with tau_w <= 1 is trivially feasible (see attack README), so the
census reports the instances with tau_w >= 2 that admit no packing.  Known
examples of such instances exist in the literature (Schrijver 1980, at 0/1
weights), which is what makes the infeasible side of this decision procedure
testable at all; the census asks how SMALL they can be.

Conventions (problems/woodalls-conjecture/README.md):
  - dicut = delta+(U) for nonempty proper U with delta-(U) empty and
    delta+(U) nonempty;
  - dijoin = arc set meeting every dicut.

Everything is exact integer arithmetic; there is no randomness anywhere.
Pure standard library.  Written independently of experiments/woodalls-dicuts/
per problems/woodalls-conjecture/RULES.md (independent reimplementation).

Status of everything this program outputs: numerical.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import combinations, product


# ---------------------------------------------------------------------------
# basic digraph machinery (general digraphs, so fixtures can use cycles too)
# ---------------------------------------------------------------------------

def dicut_arcsets(n: int, arcs: list[tuple[int, int]]) -> list[int]:
    """All distinct dicuts of the digraph, as bitmasks over arc indices.

    A shore U (nonempty proper vertex subset) yields the dicut delta+(U) iff
    delta-(U) is empty and delta+(U) is nonempty.  Distinct shores can carry
    the same arc set; the returned list is deduplicated.
    """
    out = set()
    for U in range(1, (1 << n) - 1):
        leaving = 0
        ok = True
        for i, (u, v) in enumerate(arcs):
            uin = (U >> u) & 1
            vin = (U >> v) & 1
            if vin and not uin:          # arc enters U -> not a dicut shore
                ok = False
                break
            if uin and not vin:          # arc leaves U
                leaving |= 1 << i
        if ok and leaving:
            out.add(leaving)
    return sorted(out)


def minimal_arcsets(masks: list[int]) -> list[int]:
    """Inclusion-minimal members of a family of bitmasks."""
    res = []
    for m in masks:
        if not any(o != m and (o & m) == o for o in masks):
            res.append(m)
    return res


def weakly_connected(n: int, arcs: list[tuple[int, int]]) -> bool:
    if n == 1:
        return True
    adj = [set() for _ in range(n)]
    for u, v in arcs:
        adj[u].add(v)
        adj[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == n


def source_sink_connected(n: int, arcs: list[tuple[int, int]]) -> bool:
    """Every source reaches every sink (DAG assumed; this is the condensation)."""
    out = [set() for _ in range(n)]
    indeg = [0] * n
    outdeg = [0] * n
    for u, v in arcs:
        out[u].add(v)
        indeg[v] += 1
        outdeg[u] += 1
    sources = [x for x in range(n) if indeg[x] == 0]
    sinks = [x for x in range(n) if outdeg[x] == 0]
    for s in sources:
        seen = {s}
        stack = [s]
        while stack:
            x = stack.pop()
            for y in out[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if any(t not in seen for t in sinks):
            return False
    return True


# ---------------------------------------------------------------------------
# packing feasibility: exact backtracking colouring
# ---------------------------------------------------------------------------

def packs(dicut_slotmasks: list[int], nslots: int, tau: int) -> bool:
    """Decide existence of a map c: slots -> {0..tau-1} such that every mask in
    dicut_slotmasks contains all tau colours.

    Equivalence with w-packings of dijoins (proof in the attack README):
    slots are the weight-1 arcs (more generally w(a) slots per arc); J_i :=
    {arcs with a slot of colour i} are tau dijoins with each arc in at most
    w(a) of them, and conversely any w-packing induces such a colouring.
    WLOG every slot is coloured, because supersets of dijoins are dijoins.
    """
    if tau <= 1:
        return True
    m = nslots
    slot_dicuts = [[] for _ in range(m)]
    for d, mask in enumerate(dicut_slotmasks):
        for s in range(m):
            if (mask >> s) & 1:
                slot_dicuts[s].append(d)

    # order slots: members of small dicuts first (better pruning)
    smallest = [min((dicut_slotmasks[d].bit_count() for d in slot_dicuts[s]),
                    default=1 << 30) for s in range(m)]
    order = sorted(range(m), key=lambda s: (smallest[s], s))
    pos_of = {s: i for i, s in enumerate(order)}

    ndc = len(dicut_slotmasks)
    colors_seen = [0] * ndc                       # bitmask of colours present
    remaining = [dicut_slotmasks[d].bit_count() for d in range(ndc)]
    full = (1 << tau) - 1

    def bt(i: int, maxc: int) -> bool:
        if i == m:
            return all(colors_seen[d] == full for d in range(ndc))
        s = order[i]
        # symmetry breaking: colours 0..min(maxc+1, tau-1)
        for c in range(min(maxc + 2, tau)):
            ok = True
            changed = []
            for d in slot_dicuts[s]:
                old = colors_seen[d]
                colors_seen[d] = old | (1 << c)
                remaining[d] -= 1
                changed.append((d, old))
                # prune: missing colours cannot exceed unassigned slots
                if tau - colors_seen[d].bit_count() > remaining[d]:
                    ok = False
            if ok and bt(i + 1, max(maxc, c)):
                return True
            for d, old in changed:
                colors_seen[d] = old
                remaining[d] += 1
        return False

    return bt(0, -1)


def packs_bruteforce(dicut_slotmasks: list[int], nslots: int, tau: int) -> bool:
    """Independent second implementation: try every colouring outright.

    Only usable when tau**nslots is small; used to double-check every
    infeasible instance the census flags, and in the test suite.
    """
    if tau <= 1:
        return True
    full = (1 << tau) - 1
    for assign in product(range(tau), repeat=nslots):
        good = True
        for mask in dicut_slotmasks:
            seen = 0
            for s in range(nslots):
                if (mask >> s) & 1:
                    seen |= 1 << assign[s]
            if seen != full:
                good = False
                break
        if good:
            return True
    return False


# ---------------------------------------------------------------------------
# Lucchesi-Younger cross-check oracle (unweighted; consistency test only)
# ---------------------------------------------------------------------------

def min_dijoin_size(min_dicuts: list[int], narcs: int) -> int:
    """Smallest arc set hitting every minimal dicut (brute force)."""
    if not min_dicuts:
        return 0
    for k in range(1, narcs + 1):
        for combo in combinations(range(narcs), k):
            mask = 0
            for i in combo:
                mask |= 1 << i
            if all(mask & d for d in min_dicuts):
                return k
    raise AssertionError("no transversal found; impossible")


def max_disjoint_dicuts(min_dicuts: list[int]) -> int:
    """Maximum number of pairwise arc-disjoint dicuts (brute force).

    Only inclusion-minimal dicuts need be considered: shrinking a member of a
    disjoint family to a minimal dicut inside it keeps the family disjoint.
    """
    best = 0
    k = len(min_dicuts)

    def bt(i: int, used: int, count: int) -> None:
        nonlocal best
        best = max(best, count)
        if i == k or count + (k - i) <= best:
            return
        for j in range(i, k):
            d = min_dicuts[j]
            if not (d & used):
                bt(j + 1, used | d, count + 1)

    bt(0, 0, 0)
    return best


# ---------------------------------------------------------------------------
# census over DAGs in topological labeling
# ---------------------------------------------------------------------------

def ut_pairs(n: int) -> list[tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(u + 1, n)]


def weight_vectors(narcs: int, wmax: int):
    """All w in {0..wmax}^narcs; bitmask fast path for wmax = 1."""
    if wmax == 1:
        for wmask in range(1 << narcs):
            yield tuple((wmask >> i) & 1 for i in range(narcs))
    else:
        yield from product(range(wmax + 1), repeat=narcs)


def census(n: int, deadline: float | None, ly_check: bool,
           out_path: str | None, wmax: int = 1) -> dict:
    """Exhaustive {0..wmax}-weighted census over all weakly connected simple
    DAGs on n vertices, each represented by every upper-triangular labeling.

    Coverage claim: every DAG admits a topological labeling, under which its
    arcs are upper-triangular, so ranging over ALL upper-triangular arc sets
    covers every isomorphism class (with redundancy across labelings, which
    affects speed, never coverage).
    """
    pairs = ut_pairs(n)
    npairs = len(pairs)
    stats = {
        "n": n,
        "wmax": wmax,
        "ut_graphs": 0,
        "connected_graphs": 0,
        "tau_ge2_graphs": 0,
        "weighted_instances": 0,          # 2^|A| per connected graph
        "tau_w_ge2_instances": 0,
        "infeasible": [],
        "ly_checked_graphs": 0,
        "complete": True,
        "last_graph_mask": None,
        "elapsed_sec": None,
    }
    t0 = time.time()
    for gmask in range(1, 1 << npairs):
        if deadline is not None and time.time() > deadline:
            stats["complete"] = False
            break
        stats["ut_graphs"] += 1
        arcs = [pairs[i] for i in range(npairs) if (gmask >> i) & 1]
        if not weakly_connected(n, arcs):
            continue
        stats["connected_graphs"] += 1
        narcs = len(arcs)
        stats["weighted_instances"] += (wmax + 1) ** narcs
        dcs = dicut_arcsets(n, arcs)
        mins = minimal_arcsets(dcs)
        tau_unw = min(d.bit_count() for d in mins)

        if ly_check:
            assert min_dijoin_size(mins, narcs) == max_disjoint_dicuts(mins), \
                f"LY violation at n={n} gmask={gmask}"
            stats["ly_checked_graphs"] += 1

        if tau_unw == 1 and wmax == 1:
            # some dicut is a single arc a: its weight w(a) <= 1, so tau_w <= 1
            # for EVERY weighting -> all 2^|A| instances trivially feasible.
            continue
        stats["tau_ge2_graphs"] += 1 if tau_unw >= 2 else 0
        ssc = source_sink_connected(n, arcs)
        min_arc_lists = [[i for i in range(narcs) if (d >> i) & 1] for d in mins]

        for w in weight_vectors(narcs, wmax):
            tau_w = min(sum(w[i] for i in al) for al in min_arc_lists)
            if tau_w <= 1:
                continue
            stats["tau_w_ge2_instances"] += 1
            # w(a) slots per arc, capped at tau_w (an arc contributes at most
            # tau_w distinct colours, so extra slots are redundant)
            slot_of_arc = [[] for _ in range(narcs)]
            nslots = 0
            for i in range(narcs):
                for _ in range(min(w[i], tau_w)):
                    slot_of_arc[i].append(nslots)
                    nslots += 1
            slotmasks = []
            for al in min_arc_lists:
                sm = 0
                for a in al:
                    for s in slot_of_arc[a]:
                        sm |= 1 << s
                slotmasks.append(sm)
            if not packs(slotmasks, nslots, tau_w):
                # cross-checks before recording
                assert not ssc, (
                    "infeasible source-sink-connected instance: encoding bug "
                    f"(n={n} gmask={gmask} w={w})")
                assert not (tau_w == 2 and all(x >= 1 for x in w)), (
                    "everywhere-positive tau_w=2 instance reported infeasible: "
                    "contradicts the tau=2 theorem via the parallel-arc "
                    f"reduction: encoding bug (n={n} gmask={gmask} w={w})")
                if tau_w ** nslots <= 10 ** 7:
                    assert not packs_bruteforce(slotmasks, nslots, tau_w), \
                        f"solver mismatch (n={n} gmask={gmask} w={w})"
                    confirmed = "bruteforce"
                else:
                    confirmed = "backtracking-only"
                stats["infeasible"].append({
                    "n": n,
                    "arcs": arcs,
                    "weights": list(w),
                    "tau_w": tau_w,
                    "n_positive_arcs": sum(1 for x in w if x >= 1),
                    "confirmed_by": confirmed,
                })
        stats["last_graph_mask"] = gmask
        if out_path and stats["connected_graphs"] % 2000 == 0:
            stats["elapsed_sec"] = round(time.time() - t0, 1)
            with open(out_path, "w") as fh:      # checkpoint
                json.dump(stats, fh, indent=1)
    stats["elapsed_sec"] = round(time.time() - t0, 1)
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(stats, fh, indent=1)
    return stats


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nmin", type=int, default=2)
    ap.add_argument("--nmax", type=int, default=5)
    ap.add_argument("--budget-sec", type=float, default=2400.0,
                    help="wall-clock budget for the whole run")
    ap.add_argument("--ly-nmax", type=int, default=4,
                    help="run the Lucchesi-Younger oracle on every graph up to "
                         "this n (it is brute force and slow)")
    ap.add_argument("--wmax", type=int, default=1,
                    help="weights range over {0..wmax} (default {0,1})")
    ap.add_argument("--out", type=str, default="out")
    args = ap.parse_args()

    deadline = time.time() + args.budget_sec
    for n in range(args.nmin, args.nmax + 1):
        suffix = f"-w{args.wmax}" if args.wmax != 1 else ""
        path = f"{args.out}/census-n{n}{suffix}.json"
        st = census(n, deadline, ly_check=(n <= args.ly_nmax), out_path=path,
                    wmax=args.wmax)
        print(f"n={n}: ut_graphs={st['ut_graphs']} "
              f"connected={st['connected_graphs']} "
              f"tau_ge2_graphs={st['tau_ge2_graphs']} "
              f"tau_w_ge2_instances={st['tau_w_ge2_instances']} "
              f"infeasible={len(st['infeasible'])} "
              f"complete={st['complete']} "
              f"elapsed={st['elapsed_sec']}s", flush=True)
        if not st["complete"]:
            print(f"n={n}: BUDGET HIT — partial coverage recorded in {path}",
                  flush=True)
            break


if __name__ == "__main__":
    main()
