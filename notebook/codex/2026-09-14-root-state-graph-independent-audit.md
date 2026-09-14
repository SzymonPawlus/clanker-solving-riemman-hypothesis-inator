# Preserved independent root audit of the residual-state certificates

Status: `sketch`; independent implementation within the Codex family only.
Claude or human review is still required. This preserves a separate audit
checkpoint and does not alter the frozen all-forty-four replay.

The root worker wrote `helper_state_graph_audit.py` from the manager's and
prover's prose mathematical specifications and JSON graph data, without
reading either author's generator or checker. The helper copied those exact
checker bytes into its own tracked worktree and reran all graphs. The
checker retains this provenance; it is not claimed as a second independent
implementation authored by the helper.

The combined replay passes all sixteen graph files: 2,580 states and 3,610
distinct child edges, with largest residual period 1,530. It completed in
82.33 seconds. The period-3 exclusion contributes 1,093 states and 2,022
edges; the fourteen period-2 exclusions contribute 1,462 states and 1,545
edges; the separate six-row exclusion contributes 25 states and 43 edges.

The target is fourteen moving velocities and fifteen total runners at
threshold `1/15`. The audited claims concern common lower maximal-anchor
endpoints, not arbitrary circle covers. All forbidden tests are strict
integer comparisons; the fixture `(h,a,j)=(16,1,1)` is safe at equality.
Only common scaling and exact compression of a periodic residue set are
used, with no coordinatewise rescaling or phase translation.

For every graph state `(r,L,R)`, the independent checker regenerates each
possible high-gain next row by enumerating the exact finite multiplier set
`E_r`, all divisors `h` of `L*n` with `h/gcd(h,L)=n`, and every numerator
`1<=a<h` coprime to `h`. It builds the full literal mask modulo `h`, lifts
both masks modulo `L*n`, checks the gain threshold, and compresses the exact
remaining mask to its smallest period. The entire set of resulting child
states must equal the recorded set, and each edge representative is checked
separately. Roots, descendants, nonempty leaves, strictly decreasing row
counts, uniqueness, and reachability are also checked.

The first input family contains fourteen graphs for minimum periods
`3,...,16`, excluding seven-row covers without period 2 within the separately
bounded minimum-period domain. The second begins with the period-2 row and
excludes period 3 from the remaining six rows. The third begins with periods
2 and 3 and gives four remaining rows, excluding a cover by at most six rows
under those two necessary-period hypotheses. None uses a linear-programming
dual leaf; unexpected dual node kinds are rejected.

The preserved original reports are `helper-state-graph-root-initial-audit.json`
and `helper-six-root-audit.json`. The new combined replay is
`helper-state-graph-combined-audit.json`; it binds the copied checker and every
input graph by SHA-256. `helper-state-graph-negative-fixtures.json` preserves
root's six successful rejection probes: omitted child, invalid row
representative, omitted root, incomplete campaign, unexpected dual leaf,
and duplicate residue.
The preserved `helper_state_graph_negative_fixtures.py` reproduces those
six rejection checks against the copied independent checker and graph data.

Replay `helper_state_graph_audit.py --manager-dir PATH --prover-dir PATH
--output PATH`, where the first two paths are the respective tracked
`notebook/codex/issue-297` and `notebook/codex/issue-304` directories. This
checker requires Python's standard library only. The graph results still
depend on independent review of the written high-gain reduction, the
minimum-period-sixteen reduction, and the original problem translation.
They do not establish the full fifteen-runner conjecture.
