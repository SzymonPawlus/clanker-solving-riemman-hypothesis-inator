# `packing-n16-dual` — covering lower bounds for $a_{16}$, designed against the packing

Write-up: [`problems/circle-packing-equilateral-triangle/attacks/n16-dual/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-dual/).
Python standard library only. Search is float and decides nothing; every conclusion is an exact
`Fraction` computation in the triangular basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$.

| file | what |
|---|---|
| `enemy.py` | structure of the best-known 16-point configuration: contacts, rattler, Voronoi cell diameters and areas. **Design heuristic only** — read-only input, never an input to a bound. |
| `pcenter.py` | $p$-centre (min covering radius) iteration. Fact used: if $C$ covers $T$ within radius $r$ then every Voronoi cell of $C$ has diameter $\le 2r$. Seeds the search. |
| `dual.py` | representation, power-diagram construction, validity checks, two optimisers (smoothed max; target-shrinking minimax `refine`), rational snapping, and the exact certifier `certify`. |
| `run.py` / `run2.py` | drivers. `run2.py <m> <seconds> [seed]` searches, checkpoints to `best_m<m>.json`, and freezes `cert_m<m>.json`. |
| `verify.py` | **independently written** exact re-verification of a certificate, plus a gapless-boundary-chain check and an exact grid smoke test. `python3 verify.py 15` |
| `overlay.py` | drops the enemy configuration onto the certified partition and reports which packing points share a piece. |
| `cert_m15.json` | the result: $a_{16} \ge 2232048569/500000000 = 4.4640971380$. |
| `cert_m3.json`, `cert_m8.json` | the controls: $a_4 \ge 1.7320507980$ (truth $\sqrt3$) and $a_9 \ge 2.9777759210$ (truth $3$). |
| `best_m16.json` | a **stuck** 16-piece search; no conclusion is drawn from it (see the write-up). |

```bash
python3 verify.py 15        # ~2 s, exact, no seeds, no network
python3 enemy.py
python3 overlay.py 15
python3 run2.py 15 600      # re-run the search (floats, seeded)
```
