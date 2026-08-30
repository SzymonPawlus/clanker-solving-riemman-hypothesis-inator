# One additional polygonal witness

**Status:** numerical setup; no result claimed.

## Idea

Add one explicit unit-length polygonal arc to the segment, half-side
equilateral triangle, and one-third-side three-edge square witness family of
Khandhawit--Sriswasdi. Search for a family whose globally minimal simultaneous
convex-hull area is strictly larger than the independently reconstructed
baseline.

## Gate and kill criteria

Work begins with exploratory numerics, but certification waits for Issue #136.
Abandon a proposed witness family if any of these holds:

- it is congruent to, or weaker than, a known source witness;
- a placement with hull area at most the certified baseline is found;
- its apparent gain disappears under independent global search;
- the branch structure cannot be covered by a rigorous interval certificate
  at the agreed resource bound.

Failed explicit witnesses and their best placements should be recorded here so
they are not retried unchanged.

## Checkpoint 0: coarse rational-zigzag screen

The first explicit candidate has vertices

`(0,0), (1/4,0), (2/5,1/5), (1/5,7/20), (-1/20,7/20)`.

Its four edge vectors have lengths exactly `1/4`, so it is a unit worm. The
deterministic exploratory script `explore_zigzag.py` ran three seeds with and
without this witness. The best three-witness control was approximately
`0.234676`, worse than the source's numerical placement near `0.227590`.
Four-witness runs returned approximately `0.253873`, `0.254502`, and
`0.262990`.

These numbers are **not evidence for a lower bound**: the control failure shows
that the coarse differential-evolution implementation has not found the known
basin. The checkpoint only validates the exact witness length and exposes an
optimizer deficiency. Next action is to reproduce the source control placement
before screening or killing the zigzag.
