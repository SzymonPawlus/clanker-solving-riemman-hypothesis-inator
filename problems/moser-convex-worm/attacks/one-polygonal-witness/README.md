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

