# packing-n16-upper-2 — search, polish and exact certification of the n = 16 record

Code for attack
[`problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/)
(issue #97, worker U2). Written from scratch; shares no code with `packing-n16-upper/` or
`circle-packing-search/`.

**Versions pinned for the recorded runs:** Python 3.11.15, numpy 2.4.6, scipy 1.17.1,
mpmath 1.4.1. All RNG seeds are explicit CLI arguments; recorded outputs live in `out/`.

## One-command reproduce

```bash
# validation gate (cited optima; each must land within 1e-9 of target, lands within ~2e-16)
python3 search.py --n 12 --starts 400 --seed 20260822 --out out/n12.json
python3 search.py --n 13 --starts 400 --seed 20260822 --out out/n13.json
python3 search.py --n 15 --starts 400 --seed 20260822 --out out/n15.json

# main run and fresh-seed reproduction (~25 s and ~10 s wall)
python3 search.py --n 16 --starts 1500 --seed 20260822 --out out/n16.json
python3 search.py --n 16 --starts 600  --seed 777      --out out/n16-freshseed.json

# high-precision polish (mpmath dps=60, Gauss-Newton on the active set)
python3 polish.py

# rational certificate + exact integer-arithmetic gate with negative controls
python3 make_certificate.py
python3 exact_gate.py out/n16-certificate.json

# structure: contact graph, rattler, walls
python3 contacts.py out/n16.json 1e-7
```

## Files

| file | role |
|---|---|
| `search.py` | multistart SLSQP maximin (unit triangle, maximise min pairwise distance $m$); seed families `uniform`, `lattice_defect` ($T(6)$ minus 5), `t5_plus_one`, `perturb_best`; floats, search only |
| `polish.py` | active set (20 contacts + 13 wall incidences on the 15 jammed points; point 13 = rattler, held fixed) → Gauss–Newton in mpmath at 60 dps; final residual $1.5\times10^{-61}$ |
| `contacts.py` | contact graph, wall incidences, rattler identification, constraint/dof counts |
| `make_certificate.py` | scale to repo convention (separation 2, side $d$), inflate $d$ by $10^{-13}$ relative, contract toward the incenter by $10^{-14}$, round coordinates to denominator $10^{18}$ |
| `exact_gate.py` | pure `fractions.Fraction` checker: 120 pairwise squared distances $\ge 4$, closed-triangle containment via squared comparisons, exact minimal-enclosing $d$ in $\mathbb{Q}(\sqrt3)$, two negative controls that must be rejected |

## Recorded results

- $m(16) = 0.21622726930978182173463497539634897\ldots$ (polish residual $1.5\times10^{-61}$),
  agreeing with Graham–Lubachevsky's printed $d(16) = 0.216227269309782$ in all 15 digits.
- Certificate: $d = 9249527159013717/10^{15}$, i.e.
  $s = d + 2\sqrt3 = 12.71362877415147\ldots$, exactly feasible, $9.3\times10^{-13}$ above the
  numerical optimum $12.71362877415054601\ldots$
- No configuration beat the record in 2100 recorded solves; the best value was hit from two
  independent seeds (20260822, 777) to 16 digits.
