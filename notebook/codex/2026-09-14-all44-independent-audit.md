# Independent audit of the normalized forty-four-core certificate

Status: `sketch`, requiring Claude or human review. This is an independent
implementation within the Codex family; it does not earn `verified:review`.

The audited mathematical input is the prover's committed
`notebook/codex/issue-304/all-forty-four-cores.json`, SHA-256
`e8c26ff9ca2b405666ec33a4872f94a8b2897c8164dfa4d462ad3a51a56d23e6`.
The author's checker was not read, imported, or translated. The independent
implementation reads rational atoms and weights and enumerates their literal
integer grids in `helper_all44_grid.cpp`.

## Scope and four sanity filters

The ambient target has fourteen moving velocities and fifteen total runners,
with threshold 1/15. This special-case argument concerns a tuple containing
one common positive integer scaling `cP` of any of the specified eight-speed
cores, plus at most six further positive integer speeds less than `c max(P)`.
It supplies one common time for all coordinates. It does not assert that an
arbitrary fourteen-speed tuple contains such a core. The general necessity
of the core's period-2 and period-3 assumptions remains a separate obligation.

All forbidden tests use the strict inequality. The endpoint fixtures
`x=1/15` and `x=14/15` are accepted for speed 1, and `x=0` is rejected.
The first core has the positive-weight common safe endpoint `x=1/15`.
All actual core atoms are checked against every fixed speed, including atoms
with zero weight. Only a common integer scaling is used. Absolute values
preserve the distance test for signed speeds, but no coordinatewise scaling
or unsupported distinct-speed reduction is used in this audit.

## Exact checks and result

The manifest's 44 distinct core lists equal the complete independently
classified conditional inventory exactly. The maxima histogram is
`18:4, 24:8, 30:8, 36:16, 48:4, 72:4`. Each core is separately checked to
have gcd one, to cover all lower endpoints of its maximal speed, and to
leave each of its seven smaller speeds a private endpoint.

Every listed rational atom is fixed-core-safe, every weight is nonnegative,
and each declared total agrees exactly with the sum and belongs to `(6,61/10]`.
For each core, every reduced pair

    1 <= n <= 30, 1 <= q < max(P)*n, gcd(n,q)=1

is checked, excluding `q in P` only when `n=1`. For an atom `x=a/b`, its bad
count is obtained by iterating every `k=0,...,n-1`, reducing
`q(kb+a)` modulo `nb`, and testing `15 min(r,nb-r)<nb`.
The weighted count divided by `n` never exceeds one.

All 433,328 reduced columns pass. The largest bad mass is `9999/10000`.
An additional 82,280 literal columns at scales 1 through 10 verify equality
between direct lifting and the coprime reduction. These small-scale checks
are regressions, not a substitute for the unbounded argument below.
The complete per-case totals, maxima, and maximizing pairs are in
`helper-all44-independent-audit.json`, which binds the input and checker hashes.

## Unbounded denominator tail and witness implication

For a reduced pair, multiplication by `q` permutes the `n` equally spaced
points, so any open forbidden arc of length `2/15` contains at most
`ceil(2n/15)` of them. Thus its bad mass is at most
`(61/10) ceil(2n/15)/n`. Write `n=15k+r`. The desired inequality is

    28k >= 61 ceil(2r/15) - 10r.

The checker verifies the first admissible `n>=31` in each of the fifteen
residue classes; increasing `n` by 15 increases slack by 28. This proves
the whole infinite tail without a numerical cutoff assumption.

At scale `c`, put the measure of mass `z/c` on each time `(k+x)/c` for every
atom `(x,z)` and `0<=k<c`. Its total mass is `T>6`, and every core coordinate
is safe. For an additional speed `w`, division by `gcd(c,w)` gives a reduced
column whose bad mass is at most one. The union of at most six forbidden
sets has mass at most six, so positive measure remains at a time safe for
the whole tuple. Repeated additional speeds already in the core are harmless.

## Portable replay repair

The earlier wrapper depended on historical untracked individual certificates
which did not survive loss of `/tmp`. It has been replaced. It now consumes
only the committed normalized manifest above, together with tracked helper
sources and inventory. `helper-validated-manifest.json` binds all helper
sources and the external input by SHA-256 before replay.

Run `helper_replay_validated.py --prover-dir PATH --output-dir PATH` where
the first directory contains the normalized manifest. The replay audits all
44 measures, independently reruns the period-at-most-16 calculation, reruns
all 37 conditional classification anchors, requires every anchor to complete,
and compares the new complete inventory with the audited 44 core lists.
State-graph necessity claims are excluded from this frozen replay.
