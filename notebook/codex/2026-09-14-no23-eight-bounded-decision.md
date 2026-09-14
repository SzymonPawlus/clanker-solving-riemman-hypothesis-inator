# Exact bounded exclusion of eight-row covers omitting periods two and three

Status: `numerical`; exact bounded decision results, not an unbounded theorem.

For every integer anchor `9<=M<=400`, the completed exact searches find no
cover of all lower maximal-anchor endpoints by at most eight smaller speeds
whose reduced periods omit both 2 and 3. All 392 anchors are complete after
the explicitly recorded retries. The accepted completed runs inspect
14,065,130 search states. Initial time-capped outputs are preserved with
their `complete:false` flags; the final report uses their completed retries.
For `M<=14`, the last lower endpoint is not killed by any smaller speed:
it is killed precisely when `14w<M`, which has no positive solution there.

The target remains fourteen moving velocities and fifteen total runners,
with one common endpoint family at threshold 1/15. Every row is computed
by the literal strict residue inequality. No float decides coverage and no
coordinatewise scaling is used. A putative positive is gcd-normalized and
then independently checked for full strict coverage and private residues.
There is no inference here about primitive maximal speeds above 400.

## First implementation: private sets and pivot partitioning, without caching

`helper_no23_eight_cover.py` lists every physical speed `1,...,M-1`, removes
periods 2 and 3, and computes its exact M-bit bad mask. Identical nonempty
masks are interchangeable for existence and are grouped with one physical
representative. A found family can subsequently be normalized; absence of
the two reduced periods is preserved by a common gcd division.

At every state, any inclusion-minimal completion must preserve a private
residue for each selected row. Therefore a row that erases one selected
row's last private residue is removed. Rows with zero new coverage are also
removed. The sum of the r largest remaining gains must be at least the
uncovered cardinality. The algorithm then chooses an uncovered endpoint
with fewest available covering rows and branches on every one of them.
Later siblings exclude only earlier options for that same pivot. Every
minimal completing family has a unique first applicable option, proving
the partition complete. Any cover by at most eight rows has such a minimal
subcover. This implementation has no failure cache.

## Second implementation: residual-only memoization, without private constraints

`helper_no23_memo.cpp`, driven by `helper_no23_memo.py`, has a different
state definition. Its state is only `(uncovered_mask, remaining_rows)`, and
the entire original allowed row universe is available at every state.
It has no history-dependent private-residue condition and no sibling
exclusions. A previously selected row has zero gain on the current residual
and therefore cannot cover the chosen uncovered pivot again.

It prunes only when the sum of the largest residual gains cannot cover the
residual. Otherwise it selects an uncovered endpoint, branches on every
original row covering it, and decreases the remaining-row budget. Every
completing family supplies one such row. A failed state consequently proves
that the residual itself has no completion within the budget, independent
of any prefix. Caching by exactly that residual and budget is sound.
Combining this cache key with the first implementation's private constraints
would be unsound; the implementations deliberately do not do that.

Positive outputs are minimized and checked separately by direct Python
integer residues, including gcd normalization and a private endpoint for
each row. Both implementations recover known positive seven-row and
eight-row fixtures at M=18 and M=20 without the period exclusions. The
second implementation also exactly agrees with the first on every
M=31,...,120. No author's solver or checker was read or used.

## Recorded scope and replay

The complete summary `helper-no23-eight-complete-to400.json` binds all
accepted input reports and both source versions by SHA-256. It records an
empty incomplete-anchor list and no found cover. The historical bounded
reports include `helper-no23-eight-31-120.json`,
`helper-no23-eight-121-240.json`, and `helper-no23-eight-241-400.json`;
the separate retry reports close all time-capped cases. The overlap check
is `helper-no23-eight-memo-regression.json`.

Both drivers take `--first`, `--last`, `--seconds`, and `--output`. The
Python driver was used through 240; the memoized driver was used from 241
through 400. Per-anchor time limits affect completion status only. A run
that hits its limit cannot supply a negative conclusion for that anchor.
The final completed runs do not establish that every eight-row cover has
period 2 or 3 for unbounded M.
