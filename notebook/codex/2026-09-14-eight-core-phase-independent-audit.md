# Independent audit of the 160 nine-speed core measures

Status: `sketch`; independent implementation within the Codex family only.
Claude or human review is required before any status promotion.

The frozen mathematical input is the prover's `eight-core-phase-to30.json`,
SHA-256 `5598c63635bf372fbac906943da45ede93c7e5a9b827d49787132a8b9cf676ec`.
The author generator and checker were not read, imported, or translated.
The new independent Python acceptance path reuses the unchanged literal
integer-grid kernel already frozen for the forty-four-core audit.

All 160 measures pass. Their pattern lists equal the separately enumerated
160-core bounded inventory exactly. Every one of their 3,344 rational atoms
has strictly positive weight and is safe for every one of its nine fixed
speeds. The declared totals agree with the exact rational sums and lie in
`(5,51/10]`. The smallest total is `50981/10000`.

The complete required domain has 289,120 reduced pairs with `1<=n<=14`,
`1<=q<max(P)*n`, and `gcd(n,q)=1`, excluding fixed core speeds only when
`n=1`. The reused kernel has a fixed denominator bound of 30, so this audit
actually checks 1,260,680 reduced pairs once. The largest bad mass is
`19999/20000`. It also directly checks 235,300 physical lifted columns at
scales 1 through 10 against their coprime reductions. These regression scales
do not replace the all-scale proof.

The kernel receives the eight smaller core speeds in its exclusion list;
the ninth is the maximum M itself and lies outside `q<M` when `n=1`.
Consequently the unchanged eight-entry parser represents precisely the
required nine-speed exclusion rule. All nine fixed speeds are independently
checked for atom safety by the new Python driver.

The four sanity filters have the same explicit interpretation as the frozen
certificate specification: fourteen moving velocities, fifteen total runners,
one common time, threshold `1/15`, strict forbidden inequalities, and one
common scale on the nine-speed core. The kernel retains its equality fixtures
at `1/15` and `14/15`; zero remains forbidden. No coordinatewise scaling is
used. Negative speeds may be replaced by their absolute values, and repeated
speeds impose no additional condition.

For every `n>=15`, the bad fraction of any atom is at most `ceil(2n/15)/n`.
Thus its combined weighted mass is bounded by

    (51/10) ceil(2n/15)/n <= 51(2n+14)/(150n) <= 1.

The last inequality has slack `48n-714`, which is six at n=15 and increases
by 48 at every next integer n. This closes the infinite tail exactly.
At a common scale c, put weight z/c on each time `(k+x)/c`, `0<=k<c`.
Each arbitrary additional speed below `c max(P)` kills mass at most one
after gcd reduction. Five such speeds kill mass at most five, while total
mass exceeds five, so one supported rational time is safe for every speed.

This supplies candidate all-scale theorems for the 160 explicitly specified
nine-speed patterns and arbitrary five-speed completions. It makes no claim
that these patterns classify eight-row covers with unbounded maximal speed.
The bounded inventory's completeness is unnecessary for the validity of an
individual measure once its nine core speeds and columns are checked.

Replay `helper_eight_phase_audit.py PATH/TO/eight-core-phase-to30.json
--output PATH`. The default inventory is the tracked helper bounded census.
The report `helper-eight-phase-independent-audit.json` binds the input,
inventory, acceptance path, and literal-grid source by SHA-256 and records
every case's mass, maximum, maximizing pairs, and exact column counts.
