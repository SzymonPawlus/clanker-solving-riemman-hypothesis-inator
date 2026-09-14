# Prover review handoff, resumed 14 September cycle

Status: all mathematical claims remain `sketch` pending Claude or human
review. Exact same-family checks do not promote that status. No new PR was
opened, no own PR was merged, and no result was moved into `results/`.

The actual UTC clock read 21:20:17 when the resumed prover began and
22:21:36 after the final capped searches and checkpoint integrity checks.
This is at least 61 minutes and 19 seconds of continuous productive work.
All essential data are in the persistent issue-304 worktree and are committed
to `codex/304-sept14-prover`; the old lost temporary graphs are not used.

## Frozen significant objects

- `764d6e1`: complete no-period-two seven-row residual graphs for minimum
  periods 3 through 16: 1,462 nodes, 1,545 edges, no open nodes. Root's
  independent direct-row replay passed every root and complete child set.
- `2cc5bc8`: universal positive rational measures for 160 explicit nine-speed
  cores, each surviving five arbitrary smaller added speeds at every common
  integer scale. There are 3,344 atoms, least mass `50981/10000`, and greatest
  required finite load `19999/20000`. The independent helper checked all
  289,120 required reduced columns and additional literal lifts. The core
  inventory is exhaustive only for primitive eight-row cores with maximum
  at most thirty; the individual measure statements hold at all scales.
- `7bbc832`: the analytic short-relation alternative and finite rational
  affine templates for large-period eight-row covers, with the original
  relation window 65,534. Independent mathematical audits passed. The
  manager separately improved that window to 2,998; the first version stays
  frozen.
- `fa4eb0b`: exact prime-lift criterion with the isolated-endpoint condition
  stated explicitly, plus bounded discovery records and restartable search
  machinery.
- `c7145bc`: stronger pure-power-of-three lift. Any qualifying integer affine
  open-cell cover in a common positive strip would generate primitive
  minimal eight-row covers with arbitrarily large row periods. Explicit
  sufficient size bounds handle distinctness and private endpoints. Root,
  manager, and helper independently checked the valuation argument; no
  qualifying template was found.

The original forty-four-core universal measures at `fd602d4` remain unchanged.
Their fresh independent audit passed. The root and manager supplied the
other seven-row obligations, including necessity of period three, exclusion
of at most six rows, and the forty-four-core census. The separate dependency
map describes the proposed composed corollary without treating sketches as
verified assumptions.

## Final incomplete eight-row graphs

All capped runs have now ended. The final six graph files and
`issue-304/eight-period-final-checkpoint.json` preserve 13,531 states and
1,991 open nodes. Every root remains unclosed; no covering tuple was
encountered. The final open counts for minimum periods 4,5,6,7,8,9 are
respectively 373,351,298,248,408,313. The restart specification records each
cap and the rule for reusing only fully closed subgraphs.

These are partial state explorations, not six proved exclusions and not an
exhaustive normalized maximum box. No completion claim may be based on
their timeout behavior or their closed-subgraph counts.

## Bounded affine checks and unresolved work

The helper independently excluded every unrestricted open-cell cover in the
complete integer-affine slope families `|a|<=24` (180 chambers, 1,460 exact
search states) and `|a|<=40` (490 chambers, 8,456 states). Both searches
completed without an unfinished case. The prover's larger `|a|<=60`
85-chamber samples found no candidate, but their optimization decisions
are exploratory only.

Late exact structural sieves exclude opposite slopes and same-sign doubling
inside a common positive strip, and force some slope divisible by fifteen.
Those separate manager/helper notes are the next useful constraints for the
affine attack. General shifted-runner statements are not assumed; the full
phase and arithmetic structure must be retained.

The fifteen-total-runner conjecture is still open in this campaign. The
eight-row minimum-period proposal is also unresolved. Further work should
either strengthen the graph pruning or continue the affine-template analysis
with the new structural sieves; the current significant objects are ready
for the required independent review.
