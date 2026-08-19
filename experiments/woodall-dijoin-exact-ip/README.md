# Exact dijoin packing by polychromatic colouring — counterexample sweep

Status: **numerical**. Not a proof of Woodall's conjecture; an exhaustive search never is
(`problems/woodalls-conjecture/RULES.md` §2). Write-up and reasoning:
`problems/woodalls-conjecture/attacks/dijoin-exact-ip-search/README.md`. Issue #73.

## What this is

`dijoin_exact.py` decides, exactly, whether a digraph admits `τ` pairwise arc-disjoint
dijoins, by reformulating the question as a **polychromatic colouring** of the dicut
hypergraph: colour the arcs with `τ` colours so that every dicut sees all `τ` colours.
That is a CSP on `|A|` variables, replacing the reference implementation's enumeration of
all `2^|A|` arc subsets — the actual reason #7 and #31 stalled.

Everything is integer bitmask arithmetic. **No LP, no floating point, no relaxation, no
external solver**, so a negative answer is a completed exhaustive search rather than a
solver's word.

## Environment

Pinned: **CPython 3.11.15**, standard library only — no third-party dependency, no random
number generation anywhere, so there is no seed to pin and every run is bit-for-bit
deterministic. Runs below were single-process and `nice`d.

## Reproduce

Validation gate first. It must pass before any sweep is meaningful:

```bash
python3 -m unittest discover -s experiments/woodall-dijoin-exact-ip -p 'test_*.py' -v
```

This cross-checks the dicut family, `τ`, packing existence, and both of the reference
implementation's independent dijoin tests against `experiments/woodalls-dicuts/woodall.py`
over **all 64** labelled digraphs on 3 vertices, **all 4096** on 4 vertices (cyclic ones
included), and **all 1024** DAGs on 5 vertices, plus parallel-arc, loop, condensation and
definition fixtures.

Then the sweeps (each writes a JSON summary into `results/`):

```bash
# simple DAGs, complete over all tau
python3 experiments/woodall-dijoin-exact-ip/sweep.py --n 6 --min-tau 0

# simple DAGs, complete over tau >= 2 (tau <= 1 is trivially true; see attack README)
python3 experiments/woodall-dijoin-exact-ip/sweep.py --n 7 --min-tau 2

# DAGs with parallel arcs = the integer-capacitated statement
python3 experiments/woodall-dijoin-exact-ip/sweep_multi.py --n 4 --max-mult 4 --min-tau 2
python3 experiments/woodall-dijoin-exact-ip/sweep_multi.py --n 5 --max-mult 2 --min-tau 2
```

Exit code 2 and a loud banner if any counterexample is found; `results/*.json` records the
enumeration description, the totals, the counts by `τ`, and the wall time for each run.

## Results

See `results/*.json` — these are the authoritative numbers, not this prose.

Across every run: **no counterexample**, and in each case the positive answer came with an
explicit `τ`-packing that was re-verified against the full dicut family and for pairwise
disjointness. Notably the parallel-arc sweeps reach `τ = 12` with no failure.

## Enumeration semantics — read before quoting any count

The sweep enumerates **all strictly upper-triangular 0/1 matrices** on `n` labelled
vertices. Every DAG has a topological order, so this meets every isomorphism class at least
once. It is **redundant, not isomorph-free**: a class with several topological orders is
visited repeatedly. Therefore the `leaves_reached` figures are **not** unlabelled DAG
counts and must not be compared with OEIS A003087 as issue #31 proposed; nauty is not
available in this container, and redundancy costs time, never coverage.

## Limitations

- Simple DAGs only, except for the explicitly multiplicity-capped `sweep_multi.py` runs.
  Condensations of general digraphs have parallel arcs, so the simple-DAG result does not
  formally cover all digraphs. This gap is real and is stated, not papered over.
- `n = 7` covers `τ ≥ 2` only, by design.
- The `sweep.py` prune is exact (it discards only DAGs with `τ < min_tau`) but it means a
  run with `--min-tau k` reports counts only for `τ ≥ k`.
- Checkpointing is per-run rather than incremental: each sweep writes its summary on
  completion. The individual runs are seconds-to-minutes, so a kill loses at most one run,
  which is re-runnable by the single command above.
