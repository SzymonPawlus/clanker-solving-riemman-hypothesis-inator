### 5a. What the sweep found

| $k$ | $n$ | solves | best $m$ found | $1/(k-1)$ | best $-$ threshold | landed on $1/(k-1)$ | distinct basins |
|---|---|---|---|---|---|---|---|
| 7 | 27 | 12344 | 0.166666666666666 | 0.166666666666667 | -1.94e-16 | 12001 | 196 |
| 7 | 27 | 12382 | 0.166666666666667 | 0.166666666666667 | -1.39e-16 | 12019 | 193 |
| 8 | 35 | 4734 | 0.142857142857143 | 0.142857142857143 | -1.67e-16 | 4519 | 156 |
| 9 | 44 | 902 | 0.125000000000000 | 0.125000000000000 | -2.08e-16 | 825 | 73 |
| 10 | 54 | 468 | 0.111111111111111 | 0.111111111111111 | -1.94e-16 | 413 | 49 |

**30830 local solves in total across the four targets, and not one exceeded $1/(k-1)$.** The largest value seen at any $k$ sits at the threshold to machine precision (the negative entries in the fourth column are the last bit of a double), so the abort-and-exactify trigger at $1/(k-1) + 10^{-9}$ never fired.

### 5b. How far below the lattice value the next basin lies

The naive statistic — best local optimum strictly below $1/(k-1)$ — is junk: it is dominated by incompletely converged copies of the lattice sitting $10^{-8}$ below it. Instead, for a ladder of exclusion radii $\varepsilon$, the best local optimum found below $1/(k-1) - \varepsilon$:

| $k$ | $\varepsilon = 10^{-9}$ | $10^{-6}$ | $10^{-4}$ | $10^{-3}$ |
|---|---|---|---|---|
| 7 | 0.166666665 | 0.166665586 | 0.166371035 | 0.165614855 |
| 8 | 0.142857141 | 0.142855825 | 0.142301027 | 0.140964689 |
| 9 | 0.124999994 | 0.124998969 | 0.123541185 | 0.123541185 |
| 10 | 0.111111025 | 0.109680570 | 0.109680570 | 0.109680570 |

Census keys are values rounded to 9 decimals and only the top 40 per run are kept, so 'none in top-40' means the retained tail did not reach that far down.

### 5c. Seed families

| $k$ | family | solves | reached $1/(k-1)$ | best $m$ |
|---|---|---|---|---|
| 7 | `corner_dense` | 2747 | 2707 (98.5%) | 0.166666666666666 |
| 7 | `hop` | 10874 | 10600 (97.5%) | 0.166666666666666 |
| 7 | `lattice_defect` | 2779 | 2778 (100.0%) | 0.166666666666666 |
| 7 | `rotated_lattice` | 2813 | 2732 (97.1%) | 0.166666666666667 |
| 7 | `rows` | 2750 | 2549 (92.7%) | 0.166666666666666 |
| 7 | `uniform` | 2763 | 2654 (96.1%) | 0.166666666666666 |
| 8 | `corner_dense` | 528 | 514 (97.3%) | 0.142857142857143 |
| 8 | `hop` | 2055 | 1975 (96.1%) | 0.142857142857143 |
| 8 | `lattice_defect` | 543 | 542 (99.8%) | 0.142857142857143 |
| 8 | `rotated_lattice` | 526 | 494 (93.9%) | 0.142857142857143 |
| 8 | `rows` | 545 | 496 (91.0%) | 0.142857142857143 |
| 8 | `uniform` | 537 | 498 (92.7%) | 0.142857142857143 |
| 9 | `corner_dense` | 110 | 100 (90.9%) | 0.125000000000000 |
| 9 | `hop` | 338 | 320 (94.7%) | 0.125000000000000 |
| 9 | `lattice_defect` | 119 | 117 (98.3%) | 0.125000000000000 |
| 9 | `rotated_lattice` | 116 | 100 (86.2%) | 0.125000000000000 |
| 9 | `rows` | 112 | 98 (87.5%) | 0.125000000000000 |
| 9 | `uniform` | 107 | 90 (84.1%) | 0.125000000000000 |
| 10 | `corner_dense` | 64 | 58 (90.6%) | 0.111111111111111 |
| 10 | `hop` | 181 | 157 (86.7%) | 0.111111111111111 |
| 10 | `lattice_defect` | 60 | 59 (98.3%) | 0.111111111111111 |
| 10 | `rotated_lattice` | 58 | 50 (86.2%) | 0.111111111111111 |
| 10 | `rows` | 50 | 46 (92.0%) | 0.111111111111111 |
| 10 | `uniform` | 55 | 43 (78.2%) | 0.111111111111111 |

### 5d. The best configuration at every $k$, put through the exact gate

Not just "$m$ agreed with $1/(k-1)$ to 15 digits": rationalised (denominator bound $10^8$) the best configuration found at each $k$ has $q_{\min}$ **exactly** equal to $1/(k-1)^2$, i.e. it *is* the $T(k)$ lattice minus a point, certified in exact rational arithmetic. The margin is exactly zero — not small, zero.

| $k$ | exact $a_{\min}$ | $q_{\min} - 1/(k-1)^2$ | gate reports refutation? |
|---|---|---|---|
| 7 | 6.000000000000000 | 0 | no |
| 8 | 7.000000000000000 | 0 | no |
| 9 | 8.000000000000000 | 0 | no |
| 10 | 9.000000000000000 | 0 | no |

### 6a. The insertion attack

| $k$ | $\Delta(k){-}2$ | best $m(\Delta(k){-}2)$ | its side $a$ | insertions tried | best $m(\Delta(k){-}1)$ | excess over $1/(k-1)$ | exact $a_{\min}$ |
|---|---|---|---|---|---|---|---|
| 7 | 26 | 0.166738399395270 | 5.997418732738 | 2494 | 0.166666666666666 | -1.94e-16 | 6.000000000000 |
| 8 | 34 | 0.142860447191429 | 6.999838091365 | 1172 | 0.142857142857143 | -2.50e-16 | 7.000000000000 |
| 9 | 43 | 0.125000668124556 | 7.999957240257 | 654 | 0.125000000000000 | -2.36e-16 | 8.000000000000 |
| 10 | 53 | 0.111111111111111 | 9.000000000000 | 352 | 0.111111111111111 | -3.33e-16 | 9.000000000000 |

**4672 insertions in total; the exact gate refuted every resulting configuration** (`exact_refutes` = [False, False, False, False]). In every case adding the extra point drove the separation back to exactly $1/(k-1)$ or below.

| $k$ | reference $d(\Delta(k){-}2)$ | ours | agreement |
|---|---|---|---|
| 7 | 0.166738399395271 | 0.166738399395270 | 14.5 digits |
| 8 | 0.142869646754496 | 0.142860447191429 | 4.2 digits |
| 9 | *no published value* (GL stops at $n=36$) | 0.125000668124556 | — |
| 10 | *no published value* (GL stops at $n=36$) | 0.111111111111111 | — |

