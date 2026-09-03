# woodall-tau2-redteam — red-team checkers for the $\tau = 2$ argument (issue #153)

`numerical` throughout. Evidence, never a proof step (problem `RULES.md` §3).

Written from the definitions for issue #153. It deliberately does **not** import
or reuse any other dicut code in this repo — not `woodall-tau2-checks` (C1's),
not `woodall-zeroweight-census` — so that a shared encoding bug shows up as a
disagreement between implementations rather than as agreement.

Python 3.11, standard library only. No seeds are unpinned: every randomised
sweep sets an explicit seed in its source.

| file | what it does |
|---|---|
| `dicut.py` | dicuts, dijoins, $\tau$, weighted $\tau_w$, exact $k$-dijoin decision |
| `twocol.py` | exact "two disjoint dijoins" via hypergraph 2-colourability |
| `robbins.py` | DFS strong orientation + agreement colouring (my own construction) |
| `validate.py` | the four fixtures problem `RULES.md` §4 requires, plus three more |
| `exhaustive.py` | all $3^{12}$ multi-digraphs on 4 vertices: theorem + construction |
| `exhaustive5.py` | all $2^{20}$ simple digraphs on 5 vertices, + 300k random multi |
| `search_eg_exact.py` | exact weighted-counterexample search, all DAGs $n \le 6$ |
| `search_eg2.py` | randomised minimal-support search, $n = 7..12$ |
| `weighted_check.py` | strictly-positive-weight sharpness check |
| `attack_c1.py` | C1's Theorem R (from its prose), Prop 4.1, construction |
| `lemmaA_probe.py` | Lemma A under the opposite empty-dicut convention |
| `check_c1_62.py` | C1's §6.2 demonstration instance, rebuilt |

## Headline numbers

| sweep | instances | failures |
|---|---|---|
| $n=4$, all multiplicity-$\le2$ digraphs, $\tau=2$ | 31082 | 0 |
| $n=5$, all simple digraphs, $\tau=2$ | 181070 | 0 |
| $n=5$, 300k random multi, $\tau=2$ | 22363 | 0 |
| C1's lemmas, random multi $n=3..6$, $\tau\ge2$ | 42772 | 0 |
| Lemma A probe, other convention | 85664 | 0 connected+bridged |
| strictly-positive weights, $\tau_w=2$ | 1605210 | 0 without a packing |
| weighted counterexample search, all DAGs $n\le6$ | 118166 supports | 0 found |

`search_eg_exact7.py` ($n = 7$) was launched and killed at the budget checkpoint
when instance-hunting was reassigned to issue #156; its log is incomplete and it
establishes nothing.

## Reproduce

```
python3 validate.py && python3 exhaustive.py && python3 attack_c1.py
python3 lemmaA_probe.py && python3 check_c1_62.py && python3 weighted_check.py
python3 exhaustive5.py && python3 search_eg_exact.py     # the long ones
```
