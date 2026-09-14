# Seven-row obstruction: dependency map and proposed corollary

Status: `sketch` throughout. This separate synthesis records the exact
remaining obligations; it does not edit or promote any frozen object.
Same-family independent replay is evidence, not Claude or human approval.

## Sanity filters

The problem is fourteen nonzero moving integer velocities, fifteen total
runners, with one common time satisfying all distances at least `1/15`.
Absolute values and repeated-speed deletion preserve the common-time
problem. Let `M` be the largest positive speed. Its lower endpoints are
`(15j+1)/(15M)`, for `0<=j<M`. A speed kills an endpoint only when its
distance is strictly less than `1/15`; the maximal speed itself has
distance exactly `1/15` there and is allowed. Scaling a selected core by
one common integer is permitted. The remaining speeds are not scaled
coordinatewise or restricted to multiples of the core gcd.

## Obligations, without assuming an unreviewed conclusion

| Component | Exact content | Frozen evidence / remaining check |
|---|---|---|
| A: small minimum period | A cover by at most seven smaller rows contains a row of period at most sixteen. | `2acd3bc`, 2,472 exact base checks plus the analytic period tail; same-family direct replay passed. |
| B: period two | For each minimum period `p=3,...,16`, no six further rows with periods at least `p` complete its first-row residual. | `764d6e1`, 1,462 graph nodes with complete child coverage; fresh independent literal-row replay passed. |
| C: period three | A cover by at most seven rows containing period two must also contain period three. | Manager's separate exact residual graph, 1,093 states; independent literal-row replay passed. |
| D: exclude at most six rows | The period-two and period-three residual cannot be covered by at most four additional rows. | Separate 25-state, 43-edge graph; root independent literal-row replay passed. The exactly-seven census alone does not imply this obligation. |
| E: conditional census | Every primitive inclusion-minimal seven-row cover containing periods two and three is one of forty-four listed physical speed cores. | Thirty-seven possible primitive maxima, maximum 2,880; helper and manager independently enumerate the same forty-four tuples. |
| F: universal core measures | Each of the forty-four fixed eight-speed cores, at every common scale, admits one time surviving six arbitrary additional smaller speeds. | `fd602d4`, positive rational atoms with mass above six; 433,328 exact reduced columns and the analytic denominator tail. Fresh helper replay also checks 82,280 literal lift columns. |

Each component has a mathematical specification that can be reconstructed
without relying on the author's implementation. A completed proof package
must either independently establish all of A--F or cite an appropriately
reviewed version. This map does not treat the sketches as verified axioms.

## Proposed corollary once all obligations are discharged

For any set of at most fourteen positive integer speeds, if the maximal
anchor admits a cover by at most seven of its smaller speeds, then the
whole set has a common rational time with all distances at least `1/15`.

To derive it, delete redundant covering rows. Components A--C force periods
two and three in the resulting inclusion-minimal cover. Component D excludes
a cover of fewer than seven rows. The remaining cover consists of exactly
seven smaller speeds and the maximal anchor. Divide these eight speeds by
their common gcd `c`. Component E identifies the primitive tuple as one of
the forty-four explicit cores. There are at most six other speeds in the
original fourteen-speed set, all strictly below the same maximal anchor;
component F provides the required one common rational time for them and
the scaled fixed core. This also explains why a gcd normalization of the
core does not constrain the other six speeds.

If the thirteen smaller speeds fail to cover the maximal lower endpoints
at all, an uncovered endpoint already is a witness. Consequently, after
the complete proposed corollary is established, any counterexample must
have an inclusion-minimal cover of the maximal lower endpoints of size
between eight and thirteen. This is a structural reduction, not a proof of
the full Lonely Runner conjecture. The next attack treats minimal eight-row
covers, which fix nine speeds and leave five arbitrary additions.

## Preservation and review

The false earlier twenty-pattern completeness proposal is not a dependency.
The forty-four single-core measures are true-or-false individually, without
any classification assumption. Lost uncommitted state graphs, including
their rejected negative-weight versions, are not evidence for any component.
The new graph certificates have no dual weights at all.
