# Primitive eight-row endpoint covers through maximal speed thirty

Status: `numerical`; exact bounded enumeration, not an unbounded classification.

For each integer `9<=M<=30`, this calculation enumerates every eight-element
subset of the physical speeds `1,...,M-1`. A subset is retained precisely if
its strict forbidden masks cover every lower endpoint
`t_j=(15j+1)/(15M)`, each selected row has a private endpoint, and its gcd
together with `M` is one. There is no symmetry quotient and no period sieve.

The target remains fourteen moving velocities, fifteen total runners, with
threshold `1/15`. A retained tuple has nine fixed speeds and would leave five
additional speeds in the fourteen-speed target. An endpoint cover is not a
circle-covering certificate and does not refute Lonely Runner. All rows test
the same time. Equality is safe, and the accompanying seven-row regression
uses the same strict integer masks as the established endpoint fixtures.
Only common gcd normalization is used.

All 14,307,150 physical eight-subsets were inspected. There are 160 primitive
inclusion-minimal covers, with the following maxima:

| Maximum M | Primitive minimal eight-row covers |
|---|---:|
| 20 | 16 |
| 22 | 3 |
| 24 | 12 |
| 26 | 1 |
| 30 | 128 |

Every other maximum in `9,...,30`, including `M=15`, gives zero. The complete
per-anchor counts before each filter appear in `helper-eight-core-to30.json`.
As a regression, the same enumerator run on seven-subsets inspects 5,852,924
subsets and recovers exactly the twenty previously listed cores through
`M=30` (four at 18, eight at 24, eight at 30).

The first new nine-speed core is

    P=(1,3,4,7,9,10,11,13,20).

Private endpoint indices for its eight smaller speeds are, respectively,
`{1,19}`, `{7,13}`, `{5,15}`, `{17}`, `{11}`, `{2,4,8,12,14,16}`,
`{9}`, and `{3}`. This explicit example is separate from any claim about
arbitrary large maximal speeds.

For every output tuple, the driver rechecks primitive full coverage and all
private residues from direct integer arithmetic. It then forms the complete
set of distinct endpoints `(15j±1)/(15w)` for all fixed speeds `w in P`,
reduces modulo one, and keeps every endpoint safe for every fixed coordinate.
The exact safe endpoint universes contain between 46 and 112 points. They
are offered as candidate measure supports to the prover, not as certificates
for arbitrary completions.

Of the 160 examples, 136 contain reduced periods 2 and 3, twenty contain
period 2 without period 3, and four contain period 3 without period 2. This
shows that the seven-row necessity statements cannot simply be reused for
eight-row covers. For instance, the first displayed core has periods
`20,20,5,20,20,2,20,20` and has no period-3 row.

Replay with `helper_bounded_core_census.py --rows 8 --min-M 9 --max-M 30
--output PATH`. The output binds both the driver and literal C++ enumerator
by SHA-256. The C++ enumerator visits each increasing physical subset once;
the driver verifies that the recorded visit count equals the corresponding
binomial coefficient for every anchor.
