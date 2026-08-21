# Zero-weight Edmonds–Giles census

Status of every output here: **`numerical`**. Issue #72.

Exhaustive search for small `{0,1}`- and `{0,1,2}`-weighted counterexamples to the
Edmonds–Giles dijoin-packing conjecture (the weighted Woodall statement, known false in general
by Schrijver 1980). The write-up — definitions, reductions, the encoding lemma, validation,
exact search-space statement, results, and kill-criteria accounting — is the attack file:
[`problems/woodalls-conjecture/attacks/zero-weight-frontier/README.md`](../../problems/woodalls-conjecture/attacks/zero-weight-frontier/README.md).

## Reproduce

```sh
./run.sh
```

Deterministic (no randomness anywhere), pure Python 3 standard library; recorded run used
Python 3.11.15 and took ~4 minutes on one core. Results are checkpointed during the run and
written to `out/census-n<N>.json` (and `census-n<N>-w2.json` for the `{0,1,2}` cube).

## Contents

- `census.py` — dicut enumeration, minimal-dicut filtering, exact packing decision (pruned
  backtracking colouring + an independent full-enumeration second solver used to confirm every
  infeasible hit and in tests), Lucchesi–Younger brute-force oracle, and the census driver.
  Written independently of `experiments/woodalls-dicuts/` per the problem `RULES.md`.
- `test_census.py` — 13 known-answer tests (run first by `run.sh`): the problem-RULES §4
  fixtures, exhaustive two-solver agreement on all weighted 4-vertex instances, the tau = 2
  unweighted theorem on ≤ 4 vertices, LY on fixtures, source–sink-connectivity fixtures, and a
  hand-checkable infeasible colouring instance.
- `out/` — committed result JSONs from the recorded run.
