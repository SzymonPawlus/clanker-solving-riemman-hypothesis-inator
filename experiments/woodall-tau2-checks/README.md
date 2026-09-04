# tau = 2 checks

Status of everything here: **`numerical`** — evidence for the write-up in
[`problems/woodalls-conjecture/attacks/tau2-complete/README.md`](../../problems/woodalls-conjecture/attacks/tau2-complete/README.md),
never a proof step. Issue #152.

## Reproduce

```sh
./run.sh            # 13 known-answer / randomised checks, ~2 s
./run.sh --hunt     # additionally re-runs the (empty) counterexample hunts, ~12 min
```

Pure Python 3 standard library, no third-party packages; recorded run: Python 3.11.15, one
core. Seeds are fixed in the scripts (152 for the tests and the n=7–8 hunt, 153 for the
n=9–11 hunt, 7 for the condensation test); the family searches are exhaustive and seedless.

## Contents

- `tau2lib.py` — dicut enumeration (`delta-(U) = ∅` required, empty dicut counted), weighted
  `tau`, dijoin test, strong components / condensation, the ear-by-ear strong orientation of
  Theorem R exactly as proved in the write-up, the agreement colouring, a brute-force
  2-colouring of dicut traces (used for the weighted packing decision). Written from the
  definitions, independently of `experiments/woodalls-dicuts/` and
  `experiments/woodall-zeroweight-census/`.
- `test_tau2.py` — the four problem-RULES §4 fixtures; the diamond split; the full pipeline
  (condensation correspondence, Lemma A, Theorem R, colouring, brute-force dijoin check on the
  original digraph) on all simple digraphs on ≤ 4 vertices, all 3-vertex multidigraphs with
  multiplicity ≤ 2, and 3 000 seeded random multidigraphs (cycles, loops, parallel and
  antiparallel arcs, 3–7 vertices); the condensation correspondence on 500 random digraphs;
  the mechanical failure of the colouring step under one weight-0 arc (README §6.2); and the
  positive-weights-as-parallel-arcs check.
- `hunt_counterexample.py` — seeded random hunt for a `{0,1}`-weighted Edmonds–Giles
  counterexample with `tau_w = 2`.
- `ring_family.py`, `ring_family2.py` — exhaustive searches of the "6-ring of weight-0 arcs plus
  three solid paths" families suggested by literature snippets about Schrijver's / Younger's
  examples.
- `build_counterexample.py` — shore-lattice construction with three out-star gadgets and a
  prescribed odd cycle of 2-arc dicut traces.

## Results of the hunts (all empty)

| search | space | instances with `tau_w = 2` decided | hits |
|---|---|---|---|
| `hunt_counterexample.py --n 7 8 --seconds 45 --seed 152` | random DAGs, random `{0,1}` weights | 410 237 (7 137 DAGs) | 0 |
| `hunt_counterexample.py --n 9 10 11 --seconds 300 --seed 153 --weightings 200` | same | 1 059 705 (38 690 DAGs) | 0 |
| `ring_family.py` | 6-ring (all 64 orientations) + 3 solid 3-arc paths, same orientation pattern on all paths, 3 endpoint patterns | 1 536 (exhaustive) | 0 |
| `ring_family2.py 270` | 6-ring (32 orientations up to reversal) + 3 solid paths, independent orientations, lengths 2–4, all 6 perfect matchings of endpoints | 803 528 (lengths 2, 3 complete; 4 cut off at the 270 s deadline) | 0 |
| `build_counterexample.py` | out-star gadgets, nine prescribed 2-traces, wholesale gadget memberships | 32 768 configurations | 0 solutions |

Interpretation, strictly inside the stated spaces: none of these families contains a
`{0,1}`-weighted instance with minimum dicut weight 2 and no packing of two dijoins inside the
weight-1 arcs. This says nothing about Woodall's conjecture; its only purpose was to obtain a
concrete Schrijver-type instance to walk the proof against, which did not succeed (write-up,
gap G2). Every hit would have been re-verified by the independent brute-force path
(`tau2lib.tau` + `tau2lib.two_packing_within`); none occurred. Logs of the recorded runs:
`hunt_n9-11.log`, `ring2.log`.
