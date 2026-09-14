# Exact open-cell chamber expansion through slope 40

Status: `numerical`; bounded exact search only. This extends the frozen
K24 campaign without changing its source or earlier report. The complete
mathematical decision and pruning proof are recorded in
`2026-09-14-affine-K24-exact-chambers.md`.

The input now consists of every nonzero integer slope `|a|<=40`, with
`b=-floor(a x)`, over all open chambers cut out by `k/n` for
`1<=n<=40`, `0<=k<=n`. There are 490 chambers and 80 possible rows in
each. Valid choices at chamber boundaries are represented in adjacent
chambers for the reason proved in the K24 note. No symmetry quotient is
taken. Every cell between all exact affine bad endpoints must be covered;
there is no condition on individual endpoints or fifteenth points.

All 490 decisions completed with no covering collection of at most eight
rows and no unfinished case. The run visited 8,456 exact recursive states
in 73.78 seconds; its slowest chamber took 0.211 seconds. The literal
finite universes ranged from 2,450 to 2,602 open cells. The report binds
the unchanged independent checker by SHA-256. Positive and negative exact
fixtures are embedded in the report.

Only residual cells and remaining budget enter failed-state memoization.
All 80 original rows remain available at every node; there are no
history-dependent private-index restrictions. Exact cell-count and
interval-measure bounds are the only pruning tests, as in the frozen K24
implementation. All row phases use one common circle point and strict
bad inequality `<1/15`; equality is safe. No coordinatewise normalization
is used. The broader problem remains fourteen moving, fifteen total
runners, and this bounded result does not prove the small-period proposal.

```
python3 helper_affine_open_chambers.py --K 40 --seconds 5 --output helper-affine-K40-open-chambers.json
```
