# The ACZ strong-base-orderability route at `tau = 3, rho = 4`

Status: `numerical`

## Definitions and cited dependency

For a nonempty proper vertex set `U`, a dicut is `delta+(U)` when no arc enters `U`.  A dijoin
meets every dicut, and Woodall's existence direction asks for `tau` pairwise disjoint dijoins when
the smallest dicut has `tau` arcs.  A directed path has singleton dicuts and needs its full arc set
as a dijoin; a directed cycle has no dicuts; the two-branch source--sink diamond has `tau=2` and
two disjoint dijoins.  These sanity checks are executable in `experiments/woodalls-dicuts/`.

The attack uses Abdi--Cornuejols--Zlatin (ACZ), *On Packing Dijoins in Digraphs and Weighted
Digraphs*, SIAM J. Discrete Math. 37 (2023), 2417--2461,
[doi:10.1137/22M1506511](https://doi.org/10.1137/22M1506511), as a `cited` dependency:

- Definitions 1.2 and 1.5 define `rho` and sink-regular `(tau,tau+1)`-bipartite instances;
- Theorem 2.8 reduces the unweighted bounded-`rho` question to those instances;
- Definition 4.7 defines the matroid M1;
- Theorems 6.5 and 6.8 establish the sufficient strong-base-orderability route and settle
  `rho <= 3` when `tau=3`;
- Question 8.1 asks whether that route continues in general.

At `tau=3,rho=4`, the reduced M1 matroid has rank 4 on 12 active vertices.  This is the first
parameter value not covered by ACZ.

## What was attacked

The exact experiment in [`experiments/woodalls-rho4/`](../../../../experiments/woodalls-rho4/README.md)
first reproduces ACZ's D27 example, including its non-strongly-base-orderable M(K4) restriction
and exact symmetric-exchange list.  It then tests Question 8.1 on 1,400 deterministic labelled
sink-regular `rho=4` multigraph samples with 12 through 16 sources.

All 1,400 samples admit the required partition.  Two independently implemented M1 and
strong-base-orderability checkers agree on D27 and on 104 sampled `rho=4` instances.  This is
`numerical` evidence only: the generator does not enumerate isomorphism classes, and a random
configuration sample cannot establish a universally quantified statement.

The planned structural-proof stage is therefore **not** presented as completed.  A future proof
must explain why the favorable partition exists rather than use this finite sample as an
assumption.

## Kill criterion and filters

The kill criterion was a valid sink-regular `(3,4)`-bipartite `rho=4` instance for which every
three-base partition has every two-base restriction non-strongly-base-orderable.  No such instance
was found, so the route is not refuted.  A failure of the D27 validation would instead have killed
the implementation; it passed.

- **Schrijver filter: passed.** The load-bearing ACZ reduction is specifically the unweighted
  `w=1`, `tau>=3` construction.  No weighted Edmonds--Giles conclusion is inferred.
- **Lucchesi--Younger filter: passed.** No min-dijoin/max-dicut role reversal is used.  The imported
  implications are ACZ's cited reduction and sufficient matroid criterion.
- **Easy-direction filter: passed.** The tested condition is sufficient for constructing three
  disjoint dijoins.  It is not the trivial statement that at most three can exist.

Weakest point: the finite generator is biased toward sparse constraints and provides no coverage
guarantee.  The mathematical reduction and the D27 claims are taken from ACZ as `cited`; the new
implementation and all search outcomes remain `numerical` pending review.
