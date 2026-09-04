# Independent source and verifier audit

**Status:** sketch and verifier specification. No lower bound in this file is a
new assumable result.

**Issue:** #138

This attempt fixes the source boundary and specifies an independent checker
before any certificate producer is inspected. Future checker work for this
issue must implement the predicates below from this document and the primary
mathematics, not import, translate, or adapt producer code.

## Exact problem boundary

Here a worm is a continuous rectifiable planar arc of length one. The active
constant is the infimum of the areas of **convex** planar sets which contain an
orientation-preserving rigid image of every worm. The orientation-preserving
restriction is the repository convention; older sources often say only
"copy". Reflection is immaterial for the symmetric 2009 segment, triangle,
and square witnesses, but must be audited for every new asymmetric witness.

The unrestricted Moser problem permits a nonconvex cover. Consequently, the
Norwood--Poole cover of area `0.260437` is not an upper bound supplied by a
convex cover and must not be paired with a convex lower bound as though both
addressed the same optimization problem. Norwood and Poole explicitly describe
their cover as nonconvex; its convex hull supplied the then-relevant convex
upper bound, approximately `0.2738`. Ploymaklam and Wichiramala subsequently
reported another nonconvex cover of area `0.26007`.

For convex covers, the published lower bound located in the primary literature
is `0.232239`, due to Khandhawit, Pagonakis, and Sriswasdi. The published
peer-reviewed upper construction is the unit-radius 30-degree sector, of area
`pi/12`, proved universal by Panraksa and Wichiramala. A 2026 preprint reports a
smaller scaled 30-60-90 triangular cover of area
`0.260956239813289477...`; its computer-assisted proof and released
certificates require an independent audit before use in this repository.

Thus `0.227498` is a historical reconstruction target, not the current
published lower record. A result exceeding `0.227498` but not `0.232239` is not
a literature improvement.

## Primary-source ledger

### Historical lower bound: `0.227498`

Tirasan Khandhawit and Sira Sriswasdi, *An Improved Lower Bound for Moser's
Worm Problem*, arXiv:math/0701391v2, revised 5 June 2009,
<https://arxiv.org/abs/math/0701391v2>.

Theorem 1 states that every independent configuration of a unit segment, an
equilateral triangle of side `1/2`, and a square of side `1/3` has convex-hull
area at least `0.227498`. Theorem 2 converts this into a convex universal-cover
lower bound. The witnesses are valid unit worms: the segment has length one;
two sides of the triangle have total length one; and three successively
traversed sides of the square have total length one. Convexity forces a cover
containing each arc to contain the corresponding hull.

The lower-bound proof is analytic and geometric. It does **not** depend on the
paper's grid search. The grid search gives only a candidate configuration of
area `0.22758966937711944`. Its stated error proposition drops second-order
terms and is not suitable as a rigorous certificate, but that defect does not
by itself refute Theorems 1--2.

The arXiv v2 source archive was inspected directly. It contains one TeX file,
four EPS figures, and bundled AMS style files. It contains no search program,
raw data, machine-readable configuration, checker, or proof certificate. The
TeX also has an apparent transcription error in the fourth square vertex: its
y-coordinate repeats `sin(alpha+pi/2)` where the parametrization requires
`sin(alpha+3pi/2)`.

The load-bearing proof still needs independent checking. In particular, the
minimal-position reduction called `K2`, including the claim that translating a
separated witness toward the fixed segment produces a hull contained in the
old hull in the presence of the third witness, is terse. The final decimal
trigonometric comparisons are printed without a rounding certificate.

### Current published lower bound: `0.232239`

Tirasan Khandhawit, Dimitrios Pagonakis, and Sira Sriswasdi, *Lower Bound for
Convex Hull Area and Universal Cover Problems*, arXiv:1101.5638v1, submitted
28 January 2011, <https://arxiv.org/abs/1101.5638>; *International Journal of
Computational Geometry and Applications* **23** (2013), 197--212,
DOI: [10.1142/S0218195913500076](https://doi.org/10.1142/S0218195913500076).

The primary abstract and journal record report that every convex universal
cover for unit arcs has area at least `0.232239`. Exact witness dimensions and
the full proof are outside the present audit until the complete paper is
independently read. No new-witness novelty claim may use `0.227498` as the
record threshold.

### Convex upper covers

Chatchawan Panraksa and Wacharin Wichiramala, *Wetzel's sector covers unit
arcs*, arXiv:1907.07351v1, <https://arxiv.org/abs/1907.07351>; *Periodica
Mathematica Hungarica* **82** (2021), 213--222,
DOI: [10.1007/s10998-020-00354-x](https://doi.org/10.1007/s10998-020-00354-x).
The unit-radius 30-degree sector is convex, is proved to cover every unit arc,
and has area `pi/12 = 0.261799...`.

Wacharin Wichiramala and Chatchawan Panraksa, *Wetzel's 30-60-90 Triangle
Covers Unit Arcs*, arXiv:2606.14625v1, submitted 12 June 2026,
<https://arxiv.org/abs/2606.14625>. The preprint reports 599 interval-validated
optimization models and proves universality after scaling by `1/1.0048`, for
reported area `0.260956239813289477...`. Its associated repository is
<https://github.com/chatchawanpan-dev/wetzel-triangle-computation>. This is a
primary preprint, not a peer-reviewed published record, and its substantial
certificate route is already occupied work rather than a novelty target here.

### Nonconvex upper covers

Rick Norwood and George Poole, *An improved upper bound for Leo Moser's worm
problem*, *Discrete & Computational Geometry* **29** (2003), 409--417,
DOI: [10.1007/s00454-002-0774-3](https://doi.org/10.1007/s00454-002-0774-3).
Its `0.260437` cover is nonconvex.

Thotsaporn Ploymaklam and Wacharin Wichiramala, *A Smaller Cover of the
Moser's Worm Problem*, *Chiang Mai Journal of Science* **45**(6) (2018),
2528--2533,
<https://www.thaiscience.info/Journals/Article/CMJS/10990404.pdf>. Its
`0.26007` construction is also nonconvex.

### Provisional 2026 claims and duplication risk

The Proof.Fail page *Moser's Worm*, status date 24 August 2026,
<https://proof.fail/p/12>, reports an unreviewed `0.2325` lower-bound
certificate and a `0.2609411773...` sharpening of the 2026 triangular upper
certificate. The lower route uses the segment, side-`1/2` equilateral
triangle, a `1/2` by `1/4` rectangle, and a broadworm breadth constraint in a
six-dimensional directed-interval branch-and-bound computation. These claims
are provisional and are not assumable here. They create a high duplication
risk for both the baseline finite-witness branch-and-bound route and the
Wetzel-triangle replay/sharpening route.

Searches of arXiv, journal metadata, citation indexes, and the current
optimization-problems registry through 30 August 2026 located no later
peer-reviewed finite-witness lower bound exceeding `0.232239`. This is a
bounded literature search, not a proof of absence.

## Independent certificate programme

The work is deliberately staged. A later stage must not hide an unproved
earlier reduction inside a large computation.

### Stage 1: analytic `f/g/h` certificate

Normalize the segment to endpoints `(0,0)` and `(1,0)`. Following the 2009
paper's symmetry reductions, let `alpha` be the square angle and `beta` the
triangle angle. On the reduced angular rectangle define

```text
g(alpha) = sqrt(2)/6 * sin(alpha)
h(beta)  = max(1/4*sin(beta-30 deg), 1/4*sin(beta+30 deg))
f(alpha,beta)
         = 1/6 * (1/2*cos(alpha-beta+15 deg)
                  + cos(alpha-45 deg)).
```

The first certificate format should prove only this precise implication:
subject to the separately named geometric hypotheses which justify all three
area inequalities, `max(f,g,h) >= 0.227498` throughout the angular domain.
It must not claim that those geometric hypotheses cover all placements yet.

The certificate records:

- schema/version and the exact target rational `113749/500000`;
- angles represented as rational multiples of `pi`, with exact root boxes;
- a subdivision tree with rational endpoints;
- at each leaf, the chosen one of `f`, `g`, or a specified branch of `h`;
- outward rational enclosures for every sine and cosine term;
- the resulting rational lower endpoint and its strict/non-strict comparison
  with the target.

The checker independently performs exact range reduction and evaluates sine
and cosine using rational Taylor bounds with a proved remainder. It recomputes
the complete tree cover and every comparison. Decimal constants such as
`74.838 degrees`, `84.496 degrees`, and `0.2274987` are explanatory output,
never certificate axioms. A useful independent sanity calculation is that the
paper's last one-variable expression evaluates near `0.227498803845` at
`alpha = 74.838 degrees`, leaving less than `10^-6` margin; rounding discipline
is therefore load-bearing.

### Stage 2: `K2` and compact-domain proof gate

Before a pose-space checker may claim the theorem, independently prove and
encode:

1. every orientation-preserving placement is represented after fixing the
   segment and applying only proved witness symmetries;
2. configurations outside the angular root domain already have area above the
   target;
3. translations can be restricted to an explicit compact domain without
   increasing the infimum or losing a possible counterexample;
4. every `K2` minimal-position transformation really produces a legal new
   configuration whose joint hull area does not increase;
5. the geometric constructions establishing `f`, `g`, and `h` apply to every
   surviving placement, including boundary and contact cases.

These are mathematical lemmas, not branch-and-bound heuristics. Until they are
proved independently, Stage 1 certifies only a conditional angular inequality.
The checker must name the exact lemma used by each domain-pruning leaf; an
opaque `outside_K2` flag is invalid.

### Stage 3: general finite-witness branch and bound

For witnesses `W_0,...,W_(n-1)`, pin `W_0`. Each other witness has exact pose
variables `(tx,ty,theta)`, giving `3(n-1)` dimensions before proved symmetry
reductions. The certificate root contains the complete compact pose box.

Each tree node is one of:

- `split`: exact rational children whose union is the parent;
- `domain_prune`: invocation of a separately checked compactness or symmetry
  lemma with its required interval hypotheses;
- `area_polygon`: selected transformed witness vertices in cyclic order;
- `area_support`: selected extremal witness vertices and support directions,
  reduced by the checker to a contained convex polygon.

For an area leaf, the checker recomputes interval rigid transforms from exact
witness vertices, proves the proposed cyclic order with strictly signed
determinants (or handles a documented collinear boundary case), and evaluates
the shoelace formula with outward rational rounding. A floating-point hull may
suggest an order to the producer but is not evidence accepted by the checker.
Because each selected point belongs to a placed witness, the verified polygon
is contained in the full joint convex hull; its area is therefore a sound lower
bound. Polygonal edges need not be sampled because the convex hull of an entire
polyline equals the convex hull of its vertices, but exact total arc length is
checked separately.

Required top-level fields are:

```text
schema_version
target_rational
motion_convention
witnesses (exact vertices, traversal order, exact length proof)
gauge_normalization
root_domain
symmetry_lemmas
trig_method_and_precision
tree
input_hashes
producer_tool_versions
```

The independent checker rejects unknown semantic fields, missing children,
domain gaps, unresolved leaves, inconsistent shared boundaries, non-finite
values, unproved reflection quotients, insufficient trig remainders, uncertain
hull orientation, and any lower endpoint below the target. Replay must be
deterministic from a single documented command. Producer and checker test
fixtures must be written independently.

## Formalization boundary

A practical Lean target is the small trusted core rather than the optimizer:

- exact polygonal-worm lengths;
- rigid-transform membership of selected vertices;
- convex-hull containment of their polygon;
- positive cyclic orientation and shoelace area;
- exact subdivision-tree coverage;
- sound rational interval and trigonometric enclosure lemmas.

The optimizer, branch priority, and floating-point candidate hull are not proof
dependencies. Lean status is unavailable if replay relies on an oracle,
`unsafe`, a custom axiom, a new unproved analytic inequality, or a floating
evaluation.

## Falsification and kill criteria

Reject a claimed bound immediately if any of the following occurs:

- an interval-certified legal placement has joint hull area below the target;
- a pose degree of freedom or an orientation/reflection branch is absent;
- compactness or a `K2` reduction is assumed rather than proved;
- the subdivision ledger has a gap or any unresolved terminal box;
- a leaf trusts a floating hull order or a non-outward-rounded value;
- a witness's exact traversal length is not one;
- the result exceeds `0.227498` but not the published `0.232239` and is called
  a record improvement;
- the claimed novelty duplicates the provisional Proof.Fail family or the
  released 2026 triangular-cover certificate work.

For a proposed additional witness, an explicit certified joint placement at
or below the established baseline kills that finite-family improvement route.
Repeated local minima above a target do not support a lower bound: the needed
quantity is the global infimum, so local optimization points in the wrong
logical direction.

## Independent implementation checkpoint (2026-08-31)

An implementation written without producer code now supplies exact rational
intervals, a rational enclosure of `pi`, and Taylor enclosures with explicit
Lagrange remainders. It also checks rational worm lengths, interval rigid
motions, exact rational hull areas, and rejects uncertain orientation.

It found that the printed cutoffs are inward:

```text
g(74.838 degrees)       = 0.2274975054... < 0.227498
h_plus(84.496 degrees)  = 0.2274975549... < 0.227498
h_minus(95.504 degrees) = 0.2274975549... < 0.227498
```

The outward rational boundaries `74.83846`, `84.495753`, and `95.504247`
degrees pass. On the central rectangle, cosine symmetry and monotonicity reduce
`f` to `beta=95.504247` degrees. The result is concave in `alpha`, so its two
exact endpoints suffice. A machine-readable fixture passes independently;
The initial development suite had ten negative checks for the printed cutoffs,
non-unit traversal, and ambiguous orientation. The angular replay promoted
below has its own checked-in adversarial suite; the more general pose-space
prototype remains outside this branch pending a separate schema audit.

The compact `moser-fgh-cutoff-v1` replay is now checked in beside this file:

```sh
python3 problems/moser-convex-worm/attacks/independent-verifier/check_fgh.py \
  problems/moser-convex-worm/attacks/independent-verifier/baseline-fgh.json
python3 -m unittest discover \
  -s problems/moser-convex-worm/attacks/independent-verifier \
  -p 'test_*.py' -v
```

Its exact accepted predicate is intentionally narrower than the general schema
above. The required claim scope is the literal
`conditional_angular_fgh_only`; labels such as `global`, `all_placements`, or
`moser_lower_bound` are rejected. The root is the fixed closed box
`alpha in [45,78], beta in [83,97]` degrees. Three ordered cutoffs must satisfy

```text
45 <= alpha_cut <= 78,
83 <= beta_low <= beta_high <= 97.
```

They partition that box into the `g` leaf `alpha >= alpha_cut`, the `h_plus`
leaf `beta <= beta_low`, the `h_minus` leaf `beta >= beta_high`, and the
remaining closed rectangle. The checker derives a rational enclosure of pi
from Machin's identity and alternating arctangent series, then derives every
sine, cosine, and square-root enclosure using rational arithmetic. It accepts
only if `g(alpha_cut)`, `h_plus(beta_low)`, `h_minus(beta_high)`, and both
concavity endpoints of the reduced `f` expression have lower endpoints at
least `113749/500000`. Duplicate JSON keys, unknown semantic fields,
noncanonical rationals, non-finite values, unordered cutoffs, and cutoffs
outside the compact root are rejected before acceptance.

The endpoint reductions are checked as exact domain predicates too. In
particular, `alpha_cut + 15 <= (beta_low + beta_high)/2` proves that
`beta_high` is the farther endpoint from the symmetry centre of the first
cosine in `f`; all its arguments remain in `[-90,90]`. The two cosine terms
are then concave in `alpha`, so their sum is bounded below by its two alpha
endpoints. The `g`, `h_plus`, and `h_minus` leaves similarly carry explicit
increasing/decreasing sine ranges rather than trusting a certificate label.

This replay proves only the conditional angular implication stated in Stage 1.
It does not certify the placement reductions or the geometric hypotheses
needed to turn `f`, `g`, and `h` into area bounds for every configuration.

### Exact uncovered obligations after the Stage-1 replay

Acceptance leaves all of the following outside the certificate:

1. the geometric derivation of each of `f`, `g`, and both branches of `h` as
   a lower bound for the joint convex-hull area;
2. the orientation-preserving gauge reduction fixing the unit segment, and
   every proved triangle/square rotational or reflection symmetry;
3. coverage of orientations outside
   `alpha in [45,78], beta in [83,97]`, including every boundary convention;
4. all translation variables, an explicit compact translation domain, and a
   proof that restricting to it preserves the global infimum;
5. the source's `K2` minimal-position reduction, or a replacement that proves
   every placement is covered by the angular hypotheses;
6. exact unit-worm and convex-hull-containment checks connecting the three
   abstract witnesses to an arbitrary universal convex cover; and
7. a global branch tree whose leaves invoke only checked geometric predicates.

Consequently this schema cannot be composed with an external assertion such
as `outside_K2=true` to obtain a theorem: unknown fields are rejected and the
scope field cannot be widened. A later global schema must encode and check the
seven obligations rather than relabel this certificate.

### Independent audit of the Issue #136 analytic artifact

After freezing the predicates above, this lane inspected Issue #136's
`certificate.json` and mathematical support note, but not its checker source.
The artifact exposes a full angular gauge
`alpha in [45,90], beta in [60,120]`, the coarse box `D`, six tail branches,
and a concave core. Its machine-readable data do **not** expose witness
coordinates, the symmetry maps, the quadrilateral-height lemma, or the
rectangle-width hypotheses. Its predicate strings `g`, `h_plus`, `h_minus`,
and `q_endpoints` therefore cannot by themselves establish a global theorem;
they must be paired with independently checked mathematics.

That mathematics was reconstructed without the producer checker as follows.

- Square and triangle rotational symmetries first reduce their angles modulo
  90 and 120 degrees. Reflection in the perpendicular bisector of the fixed
  segment sends `(alpha,beta)` to `(-alpha,60-beta)` modulo those periods;
  the half-turn about its midpoint fixes `alpha` and adds 60 degrees to
  `beta` modulo 120. Reflection first places `alpha` in `[45,90]`, and the
  half-turn then places `beta` in `[60,120]` without disturbing `alpha`.
  Reflection introduces no new witness placement because each of the three
  unlabelled witness sets has a reflection symmetry realizable by a rotation.
- For a unit base `EF` and any chord `UV`, the hull of the four endpoints has
  area at least half the perpendicular projection length of `UV`: opposite
  signed heights add, while on one side the larger height dominates their
  difference. The square diagonal and two triangle sides give `g` and the two
  `h` branches for every translation.
- If a convex body `K` contains an `a` by `b` rectangle, then
  `K+tR subset (1+t)K`. Successive exact extrusion by its two side segments
  gives `area(K+tR) = area(K) + t(a*w_y+b*w_x) + t^2*a*b`; comparison of the
  linear terms proves `2*area(K) >= a*w_y+b*w_x`. For the side-`1/3` square,
  the fixed segment supplies width `cos(alpha-45)` and the relevant
  side-`1/2` triangle chord supplies width
  `cos(alpha-beta+15)/2`, yielding exactly `f` for every translation. No
  compact translation box or `K2` transformation is then needed.
- On the full angular gauge, `g(78)`, `h_plus(83)`, and `h_minus(97)` clear
  `0.23` with the appropriate sine monotonicity. Thus the complement of `D`
  is covered before the checked-in Stage-1 certificate handles `D`.

No contradiction was found in this geometric replacement. The precise
machine-checking blocker is representational: the producer JSON names these
lemmas but supplies none of their hypotheses or witness data, while the local
schema intentionally rejects a global scope. Promoting the combined theorem
would require a new schema that encodes the fixed three witnesses, the two
explicit symmetry maps, the three coarse branches, and a trusted
`rectangle_width` predicate. Until that exists and receives cross-family
review, the reconstruction remains `sketch` even though its trigonometric
subcertificate passes.

## Stage-2 global width certificate

The positional `K2` reduction is unnecessary for `f`. Let compact convex `K`
contain `R=[0,a]x[0,b]`. For `t>=0`, `R subset K` gives
`K+tR subset K+tK=(1+t)K`. Exact horizontal then vertical extrusion gives

```text
area(K+tR) = area(K) + t(a*w_y(K)+b*w_x(K)) + t^2*a*b.
```

Comparison, division by positive `t`, and `t -> 0` proves
`2*area(K) >= a*w_y(K)+b*w_x(K)`. No differentiability is used. An unbounded
convex `K` containing a positive-area rectangle has infinite area; otherwise
closure gives the compact case. Coefficients are load-bearing: `a` multiplies
the perpendicular width `w_y`, and `b` multiplies `w_x`. `K=R` checks equality.

A `rectangle_width` leaf pins the rectangle gauge and exactly checks edge
vectors `U,V`, orthogonality, squared lengths `a^2,b^2`, the fourth vertex, and
membership in a forced witness hull. It supplies two signed selected point
pairs. The checker evaluates

```text
X = sign_x * dot(p_x-q_x,U)/a
Y = sign_y * dot(p_y-q_y,V)/b
```

and requires nonnegative interval lower endpoints and
`(b*X.lo+a*Y.lo)/2 >= target`. This avoids floating normalized directions.
For the baseline, segment endpoints and triangle-side endpoints yield `f`
after exact angle/sign checks.

Negative fixtures reject a nonorthogonal or wrongly sized rectangle, a missing
fourth hull vertex, projection intervals crossing zero, swapped coefficients,
uncertain trigonometry, and an uncleared target. This is a global area leaf,
not an opaque `outside_K2` domain prune.

For completeness, the source's `K2(i)` would require pairwise distances from
each witness point to both segment endpoints, not ordinary point-to-segment
distance. Only the former implies `0<=x<=1` and validates the later vertical
translation as a convex combination with `(x,0) in L`. The ambiguity is not
load-bearing under the width proof.
