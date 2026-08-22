# packing-n16-occupancy — occupancy exhaustion engine (worker O2, issue #97)

Code for the attack written up in
[`problems/circle-packing-equilateral-triangle/attacks/n16-occupancy/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-occupancy/README.md)
— read that first; kill-criteria in its `KILL-CRITERION.md` were fixed before any run.

**Outcome, honestly:** K1 fired. Nothing above the standing $a_{16} \ge 1+2\sqrt3$ record was
certified. The controls all pass in both directions and the $a = 4.47$ probe quantifies the
cost wall; see the attack README.

| file | what |
|---|---|
| `occ.py` | everything load-bearing: exact `Fraction` geometry in lattice coordinates ($\lvert ue_1+ve_2\rvert^2 = u^2+uv+v^2$), exact clipping/hull, clipped-Voronoi-hexagon cover builder + greedy exact merge, residual-subtraction cover verifier, capacity ladder with the named circularity guard `CAP_MAX_INDEX_FOR(n) = n-1`, pattern enumeration as cliques of the exact pair-compatibility graph, per-pattern branch-and-bound |
| `controls.py` | the four two-sided K0 controls ($n = 4, 6, 7, 10$); asserts, ~8 min |
| `run16.py` | the $n = 16$ runs: `python3 run16.py <num> <den> <seconds>`; refuses $a \ge 4.62$ (K3 tripwire) |
| `out/` | checkpointed JSON results of every run reported in the attack README |

Soundness rules: floats are pre-filters and branching heuristics only; every reported
refutation is decided in exact rational arithmetic (radical comparisons via `lt_radical`).
Deterministic — no randomness, no seeds, no network. Single core.
