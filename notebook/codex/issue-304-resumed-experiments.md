# Resumed experiment checkpoints, 14 September 2026

Status: exploratory notes, not promoted results. All files are preserved in
the persistent issue-304 worktree; the lost earlier temporary state is not
used. The resumed productive cycle began at approximately 21:20 UTC.

## Seven-speed sharp upper-anchor example

For `P={4,5,6,7,11,12,13}`, the goal was a universal rational phase measure
of total greater than seven, which would survive seven arbitrary additions
below `13c` at every common scale. The complete reduced constraint set used
denominators `1,...,124`, a mass cap of `71/10`, and the elementary tail
bound for all larger denominators. There were 61,041 finite columns.

The endpoint-plus-quarter-point grid had 46 reflected atoms and numerical
optimum about `6.5616197`. Refining every safe interval to sixteenths gave
154 atoms and numerical optimum about `6.7121501`. Both fall below seven.
This only records a failure on two finite atom grids. It proves neither
that no continuous measure exists nor that the corresponding fourteen-speed
family lacks a common time. The JSON records are
`sharp-upper-anchor-phase.json` and `sharp-upper-anchor-phase-grid16.json`.

## Eight-row covers omitting periods two and three

A bounded discrete optimization scan inspected maximal anchors 31 through
400 using only rows of reduced period at least four. Candidate outputs
would have been checked by exact strict endpoint masks, followed by
redundant-row deletion and primitive normalization. No candidate was found.
Each solver call had a half-second discovery budget, so the absent
candidates are not an exhaustive exclusion. Some anchors separately fail
the exact cardinality bound obtained by subtracting the shared zero index
from the eight largest row sizes. The per-anchor record is
`eight-minperiod-discovery.json`.

The helper independently performs an exact bounded decision search; that
separate proof of finite exclusions is not inferred from this solver run.
The remaining proposed structural statement, that every eight-row cover
has period at most three, is still unresolved.

## Pair intersections and the next analytic reduction

Literal overlap experiments found extremely sparse pairs even when both
periods are large. This led to an exact infinite family and a smoothing
argument recorded separately in `issue-304-eight-row-short-relations.md`.
That analytic argument proves a proposed bounded-coefficient relation
alternative, subject to independent review. It does not assert that a
uniform lower bound near the product of the row densities holds.
