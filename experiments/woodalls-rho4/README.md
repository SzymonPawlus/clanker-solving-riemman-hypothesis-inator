# ACZ `rho = 4` strong-base-orderability search

Status: `numerical`

This dependency-free experiment tests the sufficient matroid condition in Question 8.1 of
Abdi--Cornuejols--Zlatin (ACZ), *On Packing Dijoins in Digraphs and Weighted Digraphs*, SIAM
J. Discrete Math. 37 (2023), 2417--2461, DOI
[10.1137/22M1506511](https://doi.org/10.1137/22M1506511).  It does **not** prove a new case of
Woodall's conjecture.

## Exact objects and tests

Every generated object is a sink-regular unweighted `(3,4)`-bipartite directed multigraph.  All
arcs point from sources to sinks.  Exactly 12 sources have degree 4 (the active vertices), any
remaining sources have degree 3, and every sink has degree 3.  If there are `m` sources then
there are `m + 4` sinks, so ACZ Lemma 3.7 gives `rho = 4`.  The code also computes the minimum
dicut exactly and rejects an object unless it is 3.

For a source subset `X`, let `Y(X)` contain every sink all of whose neighbours are in `X`.
Definition 4.7 reduces to the following exact basis oracle on the 12 active sources:

```text
Q is an M1 basis iff |Q| = 4 and
|Q intersect X| >= 1 + |Y(X)| - |X| for every nonempty proper source subset X.
```

`acz.py` enumerates these source subsets using integer bitmasks.  The independent verifier uses
the dual enumeration direction: for every nonempty proper sink subset `Y`, it forms `N(Y)` and
checks

```text
|Q intersect N(Y)| >= 1 + |Y| - |N(Y)|.
```

The two implementations use different representations (bitmasks versus Python sets) and
different strong-base-orderability routines.  For a restriction to eight active vertices, both
check the definition directly: for every pair of bases they enumerate all bijections fixing the
intersection, and require every partial symmetric exchange to remain a basis.

## Primary-source validation

The D27 fixture is the 27-vertex, 45-arc multigraph in ACZ Figure 11.  Its explicit adjacency
list was transcribed from the vector graphic in the arXiv source; parallel arcs remain repeated.
The tests reproduce all checkable claims ACZ makes there:

- 12 sources, 15 sinks, 9 active sources, `rho = tau = 3`;
- `Q1={1,2,3}`, `Q2={4,5,6}`, and `Q3={7,8,9}` are M1 bases;
- the restriction to `Q1 union Q2` has 16 bases and is not strongly base orderable;
- its symmetric exchanges between `Q1,Q2` are exactly
  `{4,1}, {4,2}, {4,3}, {5,3}, {6,3}`, as stated by ACZ;
- another partition satisfies the Question 8.1 condition, as ACZ Theorem 6.8 requires at
  `rho = 3`.

Both M1 implementations agree on every D27 basis and both route tests agree.

## Finite search space and outcome

The committed JSON files cover these labelled samples:

| file | sources | sinks | inactive sources | integer seeds |
|---|---:|---:|---:|---:|
| `results.json` | 12 | 16 | 0 | 0 through 999 |
| `results-m13.json` | 13 | 17 | 1 | 0 through 99 |
| `results-m14.json` | 14 | 18 | 2 | 0 through 99 |
| `results-m15.json` | 15 | 19 | 3 | 0 through 99 |
| `results-m16.json` | 16 | 20 | 4 | 0 through 99 |

For each seed, `random.Random(seed)` shuffles 3 copies of every sink label against a fixed list
containing 4 copies of each active-source label and 3 copies of each inactive-source label.  It
accepts the first shuffled configuration having minimum dicut at least 3.  Parallel arcs are
allowed, as in ACZ.  There is no isomorphism reduction.  Each output records a SHA-256 digest of
the sorted labelled arc multiset; all 1,400 committed objects are distinct as labelled
multigraphs.

Every one of the 1,400 objects has a partition into three M1 bases for which the restriction to
two bases is strongly base orderable.  This is finite evidence for the ACZ route, not a theorem
about the sampled family or about arbitrary `rho = 4` instances.  The full independent basis and
route implementations recheck 100 evenly spaced `m=12` objects and seed 0 at each of
`m=13,14,15,16`; they agree in all 104 cases.  Any route counterexample would automatically be
rechecked independently and emitted with its full arc list.  None was found, so the issue's kill
criterion was not met.

The sampling distribution is over labelled stub matchings, is not uniform over labelled or
unlabelled multigraphs, and is biased toward weakly constrained M1 matroids.  This is the main
limitation; no exhaustiveness claim is made.

## Bad-complement matching census

`bad_complement_census.py` tests the proposed intersecting-family mechanism exactly.  For each
full M1 base `K`, it puts `K` in `F_bad` when the eight-element complement `U=E-K` splits into
two full M1 bases but the restriction `M1|U` is not strongly base orderable.  Matching and
disjointness refer to the four-element bases `K`, not to their eight-element complements.

The independent sink-subset basis oracle and direct definition-level SBO checker give:

- D27 control: 71 bases, 71 eligible complements, one bad complement, matching number one;
- merged ID1009 realization: 271 bases, 222 eligible complements, three bad complements,
  matching number one;
- all 104 committed fixtures marked `independently_verified`: no bad complements;
- the complete canonically deduplicated space of degree-preserving one-switch mutations of
  ID1009: 1,128 unordered arc-position pairs, 1,016 nondegenerate switches, and 700 unique
  canonical arc multisets.  Of these, 642 preserve minimum dicut at least three, 189 retain a
  nonempty bad family, and none has two disjoint bad bases.  The 189 positive cases have 26
  distinct census signatures.

The last family deliberately targets a known non-SBO-containing realization while changing its
sink incidence structure.  Every unordered arc-position pair is considered; degenerate swaps
are discarded and sorted arc multisets are deduplicated before exact minimum-dicut and `F_bad`
tests.  One representative of each distinct tuple `(base count, eligible count, bad count,
matching number)` is retained in the compact artifact.  Different count tuples certify
different M1 matroids; no full graph-isomorphism classification is claimed.  No disjoint bad
pair was found.  This finite negative result is `numerical` and does not prove that `F_bad` is
always intersecting.

The compact JSON has one representative for each of the 26 census signatures.  The optional
details output has all 104 committed records plus those representatives; the full 700 mutation
outcomes are reproducibly held in the checkpoint cache during the run.  These artifacts are
regenerated deterministically by the command below.

## Reproduction

From the repository root:

```bash
python3 -m unittest discover -s experiments/woodalls-rho4 -p 'test_*.py' -v
python3 experiments/woodalls-rho4/search.py --source-count 12 --count 1000 \
  --independent-every 10 --checkpoint experiments/woodalls-rho4/results.json
python3 experiments/woodalls-rho4/search.py --source-count 13 --count 100 \
  --independent-every 100 --checkpoint experiments/woodalls-rho4/results-m13.json
python3 experiments/woodalls-rho4/bad_complement_census.py \
  --output /tmp/bad-complement-census.json \
  --details-output /tmp/bad-complement-census-details.json --jobs 1 \
  --committed-cache /tmp/bad-complement-committed-cache.json \
  --mutation-cache /tmp/bad-complement-mutation-cache.json
```

Repeat the source-count 13 search command with source counts 14, 15, and 16 and matching output
names.  Every search run checkpoints after each accepted graph.  The committed runs used Python
3.14.6; the exact version is recorded in each output.  Total wall-clock time was well below the
one-hour unattended budget.
