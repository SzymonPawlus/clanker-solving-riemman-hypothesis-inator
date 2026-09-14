# Repeated absolute slopes cannot cover the affine circle

Status: `sketch`, awaiting cross-family or human review. This is a small
structural reduction for the eight-row affine search. It does not resolve
fourteen moving speeds, fifteen total runners, at threshold 1/15.

Suppose eight integer-affine rows (a_i,b_i), with nonzero a_i, have a common
physical strip: for some real x, every a_i*x+b_i belongs to (0,1). Put
delta=1/15 and B_i={z modulo 1: ||a_i*z+delta*b_i||<delta}. If two slopes
have equal absolute values, the union of all eight B_i has measure less
than one. In particular it cannot cover every open cell of its endpoint
arrangement, so it cannot be a candidate for the power-of-three lift.

If two slopes are equal, their integer shifts are equal, since the open
interval (-a_i*x,1-a_i*x) contains at most one integer. The two bad sets
coincide. There are at most seven distinct sets, each of measure 2/15,
so their union has measure at most 14/15.

If two slopes are a and -a, their shifts b_+,b_- satisfy b_++b_-=1:
their two physical ratios are positive and sum to the integer b_++b_-,
which is strictly between zero and two. In the variable y=a*z+b_+/15,
the two bad conditions are ||y||<delta and ||delta-y||<delta. Their
intersection on the y-circle is the interval (0,delta), of length delta.
The nonzero integer map z -> y preserves normalized circle measure.
Consequently the union of the two bad sets has measure 3*delta.

The six remaining bad sets each have measure 2*delta. The coarse union
bound for these seven groups is 3*delta+12*delta=1. It is strictly loose:
at z=x/15 every row value equals (a_i*x+b_i)/15 and lies strictly between
zero and delta. Thus all eight bad sets contain a common open neighborhood
of z. The union of the opposite pair and any remaining set has positive
intersection. Subtracting even that one intersection gives total measure
strictly below one. Endpoint equality remains safe, and a positive-measure
safe set for a finite rational endpoint arrangement contains an open cell.

The conclusion applies specifically to the common-strip affine phases.
Arbitrary shifted phases need not give b_++b_-=1 or a common bad neighborhood.
This reduction therefore does not assert a general shifted Lonely Runner
theorem. It does justify restricting this affine candidate hunt to eight
pairwise distinct absolute slopes.

## Same-sign doubling, observed by the prover

The same argument excludes a pair of slopes a and 2a. Write v=a*x+b in
(0,1). The doubled row's integer shift must be 2b-c, where c=floor(2v)
is either zero or one. In the coordinate theta=a*z+b/15, the two conditions
are ||theta||<delta and ||2theta-c*delta||<delta. Within the first arc,
the second gives (-delta/2,delta/2) if c=0 and (0,delta) if c=1. Each has
length delta, so the pair union again has measure 3*delta. The common open
bad neighborhood makes the full eight-row union bound strictly below one.
The physical strip excludes 2v=1, because then the doubled physical ratio
would be an integer, outside (0,1). No exclusion of opposite-sign doubling
is asserted: its pair intersection need not have measure delta.

The repeated-absolute-slope proof was independently reconstructed by the
root and prover from the prose; the manager independently checked the
prover's same-sign doubling corollary. All remain sketches pending the
required Claude or human review.
