### 5a. What the sweep found

| $k$ | $n$ | solves | best $m$ found | $1/(k-1)$ | best $-$ threshold | landed on $1/(k-1)$ | distinct basins |
|---|---|---|---|---|---|---|---|
| 7 | 27 | 10737 | 0.166666666666666 | 0.166666666666667 | -1.94e-16 | 10433 | 180 |
| 7 | 27 | 10692 | 0.166666666666667 | 0.166666666666667 | -1.39e-16 | 10375 | 174 |
| 8 | 35 | 4067 | 0.142857142857143 | 0.142857142857143 | -1.67e-16 | 3872 | 143 |
| 9 | 44 | 902 | 0.125000000000000 | 0.125000000000000 | -2.08e-16 | 825 | 73 |
| 10 | 54 | 342 | 0.111111111111111 | 0.111111111111111 | -2.50e-16 | 299 | 38 |

**26740 local solves in total across the four targets, and not one exceeded $1/(k-1)$.** The largest value seen at any $k$ sits at the threshold to machine precision (the negative entries in the fourth column are the last bit of a double), so the abort-and-exactify trigger at $1/(k-1) + 10^{-9}$ never fired.

### 5b. How far below the lattice value the next basin lies

The naive statistic — best local optimum strictly below $1/(k-1)$ — is junk: it is dominated by incompletely converged copies of the lattice sitting $10^{-8}$ below it. Instead, for a ladder of exclusion radii $\varepsilon$, the best local optimum found below $1/(k-1) - \varepsilon$:

| $k$ | $\varepsilon = 10^{-9}$ | $10^{-6}$ | $10^{-4}$ | $10^{-3}$ |
|---|---|---|---|---|
| 7 | 0.166666665 | 0.166665586 | 0.166371035 | 0.165614855 |
| 8 | 0.142857141 | 0.142855785 | 0.142301027 | 0.140964689 |
| 9 | 0.124999994 | 0.124998969 | 0.123541185 | 0.123541185 |
| 10 | 0.109680570 | 0.109680570 | 0.109680570 | 0.109680570 |

Census keys are values rounded to 9 decimals and only the top 40 per run are kept, so 'none in top-40' means the retained tail did not reach that far down.

### 5c. Seed families

| $k$ | family | solves | reached $1/(k-1)$ | best $m$ |
|---|---|---|---|---|
| 7 | `corner_dense` | 2507 | 2471 (98.6%) | 0.166666666666666 |
| 7 | `hop` | 8721 | 8493 (97.4%) | 0.166666666666666 |
| 7 | `lattice_defect` | 2561 | 2560 (100.0%) | 0.166666666666666 |
| 7 | `rotated_lattice` | 2597 | 2527 (97.3%) | 0.166666666666667 |
| 7 | `rows` | 2519 | 2334 (92.7%) | 0.166666666666666 |
| 7 | `uniform` | 2524 | 2423 (96.0%) | 0.166666666666666 |
| 8 | `corner_dense` | 485 | 472 (97.3%) | 0.142857142857143 |
| 8 | `hop` | 1630 | 1561 (95.8%) | 0.142857142857143 |
| 8 | `lattice_defect` | 486 | 485 (99.8%) | 0.142857142857143 |
| 8 | `rotated_lattice` | 481 | 449 (93.3%) | 0.142857142857143 |
| 8 | `rows` | 495 | 450 (90.9%) | 0.142857142857143 |
| 8 | `uniform` | 490 | 455 (92.9%) | 0.142857142857143 |
| 9 | `corner_dense` | 110 | 100 (90.9%) | 0.125000000000000 |
| 9 | `hop` | 338 | 320 (94.7%) | 0.125000000000000 |
| 9 | `lattice_defect` | 119 | 117 (98.3%) | 0.125000000000000 |
| 9 | `rotated_lattice` | 116 | 100 (86.2%) | 0.125000000000000 |
| 9 | `rows` | 112 | 98 (87.5%) | 0.125000000000000 |
| 9 | `uniform` | 107 | 90 (84.1%) | 0.125000000000000 |
| 10 | `corner_dense` | 51 | 46 (90.2%) | 0.111111111111111 |
| 10 | `hop` | 99 | 82 (82.8%) | 0.111111111111111 |
| 10 | `lattice_defect` | 47 | 46 (97.9%) | 0.111111111111111 |
| 10 | `rotated_lattice` | 49 | 43 (87.8%) | 0.111111111111111 |
| 10 | `rows` | 46 | 42 (91.3%) | 0.111111111111111 |
| 10 | `uniform` | 50 | 40 (80.0%) | 0.111111111111111 |

### 5d. The best configuration at every $k$, put through the exact gate

Not just "$m$ agreed with $1/(k-1)$ to 15 digits": rationalised (denominator bound $10^8$) the best configuration found at each $k$ has $q_{\min}$ **exactly** equal to $1/(k-1)^2$, i.e. it *is* the $T(k)$ lattice minus a point, certified in exact rational arithmetic. The margin is exactly zero — not small, zero.

| $k$ | exact $a_{\min}$ | $q_{\min} - 1/(k-1)^2$ | gate reports refutation? |
|---|---|---|---|
| 7 | 6.000000000000000 | 0 | no |
| 8 | 7.000000000000000 | 0 | no |
| 9 | 8.000000000000000 | 0 | no |
| 10 | 9.000000000000000 | 0 | no |

