# Reconstruction attempt for the public `0.2325` claim

**Status:** `numerical` reconstruction and reproducibility blocker. Nothing in
this attack is assumable. **Issue:** #172. **Search date:** 2 September 2026.

This is an independent attempt to locate or recreate the provisional claim on
the Proof.Fail page [*Moser's Worm*](https://proof.fail/p/12). No person was
contacted, no external post was made, and frozen PRs #168 and #171 were not
modified or treated as verified.

## Public claim, exactly as far as exposed

The page gives a status date of 24 August 2026 and attributes the attempt to a
Proof.Fail account displayed as Dan Stoyell. It says that a directed-rational
interval branch-and-bound closed the target `0.2325` for the convex cover of
all unit arcs. The stated forced data are:

1. a fixed unit segment;
2. a side-`1/2` equilateral triangle;
3. a `1/2` by `1/4` rectangle forced by a three-side unit worm;
4. a cited broadworm breadth constraint `b >= 0.4389`.

It describes a six-dimensional placement space consisting of the triangle
and rectangle orientation and two translations for each. It reports 499,842
effective boxes visited, 499,844 boxes or children pruned, zero unresolved
terminal boxes, maximum depth 45, and directed rational arithmetic with
denominator `2^100`. It says floating-point hull routines supplied only
candidate orders and that rational Taylor trigonometric enclosures and exact
determinant tests re-established pruning decisions.

The claim is explicitly conditional on the cited KPS inequalities and
broadworm theorem, and the page itself calls the priority provisional and the
result not peer reviewed or independently audited.

## Artifact and provenance search

The downloaded page is server-rendered HTML with no script bundle, attachment,
download, repository, commit, certificate, or data link. Its
"Reproducibility files" section only names local paths:

```text
moser_worm_research_note.md
worm_rigorous_checker.py
worm_02325_certificate_audit.py
worm_exchange_oracle.py
worm_z_landscape.py
wetzel-triangle-computation/
worm_exchange_z_landscape_batch3.json
worm_z_landscape_batch3_scan.json
```

The first three would be load-bearing for the lower bound, but none is linked.
The site's own [Why?](https://proof.fail/why) page says submissions may be
quick notes and may omit exact model output and prompts. The author profile
contains only a display name and hosted avatar; it provides no external
identity, repository, or artifact link.

Searches performed:

- exact filenames and distinctive phrases through the web search index;
- authenticated GitHub code, commit, issue, repository, user, and gist APIs;
- all public repositories, branches, recent events, and gists of the two
  GitHub profiles whose names exactly match the displayed author;
- Proof.Fail HTML links, `robots.txt`, sitemap, and obvious public routes;
- the Internet Archive CDX index for both `/p/12` and the full domain;
- arXiv, Crossref, OpenAlex, and Semantic Scholar in the companion literature
  audit in PR #171.

The exact lower-bound filenames returned zero GitHub code hits. The exact
Moser/`0.2325` GitHub commit search returned zero hits. The issue search found
only this repository's audit issue and PR. Neither matching public GitHub
profile exposes a Moser repository or gist; the Proof.Fail profile does not
identify either account, so even that negative association is only a search
boundary, not identity evidence. The Internet Archive returned no capture for
the page or domain. A sitemap route returned 404.

Pinned downloads and query responses:

| artifact | SHA-256 |
|---|---|
| Proof.Fail problem page | `ca92521471f955b288c898f63755c137ff693fbdcfa11020bfcd3cfc4e430ac2` |
| Proof.Fail author profile | `87e74252686fbb6fe5662ff181b2b174003089ed32cb580534f4e58e91d8bc5e` |
| Proof.Fail `Why?` page | `b852e52ee082370855dbf778a28458e76ad922b0e5b1ca46eb551e56af41c772` |
| Proof.Fail `robots.txt` | `842b34303164ead41bccb7c05d1707422e98d108753b397b6dcc19683eb02101` |
| Internet Archive empty CDX response | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| GitHub empty exact-filename response (each filename) | `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f` |
| GitHub empty exact Moser/`0.2325` commit response | `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f` |

The Internet Archive hash in the table is a hash of the literal empty JSON
response `[]`; it is not a content snapshot. Search responses are transient
index observations, not proofs that a private or deleted artifact never
existed.

## Clean-room interpretation of the six variables

The only natural six-variable lower functional recoverable from the summary
is the following. Pin the segment `L` from `(0,0)` to `(1,0)`. Independently
place the triangle `T` and rectangle `R`, using three pose variables each. The
full cover hull `K` contains their joint hull, so

```text
area(K) >= area(conv(L union T union R)).
```

If `rho` is the angle of the rectangle's long side to `L`, the KPS
rectangle/broadworm inequality specializes to

```text
area(K) >= b/4 + |cos(rho)|/8.
```

Thus every placement is lower-bounded by

```text
Phi = max(area(conv(L union T union R)), b/4 + |cos(rho)|/8).
```

This interpretation exactly accounts for the stated four witnesses, the
elimination of the broadworm placement down to its breadth, and the remaining
six pose variables. It is nevertheless an inference: the page supplies no
formula or schema confirming that `Phi` is what its checker accepted.

There is no hidden seventh pose variable in this clean-room model. A direct
isometry pins the unit segment with ordered endpoints at `(0,0)` and `(1,0)`.
Each remaining rigid witness then has two translations and one angle. An
equilateral triangle is periodic modulo `120` degrees and the rectangle modulo
`180` degrees. Although reflections are forbidden by the problem convention,
reflecting either of these two unlabeled symmetric shapes produces a direct
rotation of the same point set, so no reflected component is omitted from its
placement family. This checks the internal six-variable count only; it does
not establish which gauges, labels, or endpoint conventions the unavailable
producer used.

The breadth term has a similarly narrow justification. Applied to the pinned
unit segment and a `1/2` by `1/4` rectangle whose long side makes angle `rho`,
the cited KPS rectangle/broadworm inequality algebraically becomes
`b/4 + |cos(rho)|/8`; translations disappear from that inequality, but remain
essential in the joint-hull term. The broadworm itself contributes through
the scalar lower breadth `b`, not through a pose. This does not validate the
decimal `0.4389`, the applicability hypotheses, or any stronger predicates
the public checker may have used.

A clean-room compact root can also be derived without reflection. If a joint
hull `K` has diameter `d`, the side-`1/2` equilateral triangle supplies width
at least `sqrt(3)/4` perpendicular to a diameter. The four-point height bound
gives

```text
area(K) >= d*sqrt(3)/8.
```

For target `T = 93/400`, a counterexample therefore has
`d < 93/(50*sqrt(3))`. Since the pinned segment endpoint lies in `K`, every
triangle/rectangle centroid (and every vertex) is within `d` of it. The
rational choice `D = 537/500` is outward because

```text
3*D^2 > (93/50)^2.
```

Thus both moving centroids may safely use coordinates in `[-D,D]`. Direct
rotational symmetries give triangle angle `[0,120]` degrees and rectangle
angle `[0,180]` degrees. This is a six-dimensional compact box covering every
target-violating direct placement. It is one possible producer root, not
evidence that the missing checker used it.

The deterministic floating-point probe

```text
python3 experiments/moser-proof-fail-reconstruction/probe_six_dimensional.py
```

uses Python 3.14.6, NumPy 2.5.1, seed `5`, 50,000 global samples, and 15
deterministic pattern-search restarts. It finds

```text
Phi                 = 0.23280334124629035
hull area            = 0.23280334124629035
broadworm term       = 0.21815986875908386
rectangle angle rho  = 2.620908330738591 radians
```

with a four-vertex active hull cycle

```text
segment.P0, rectangle.P3, segment.P1, rectangle.P1.
```

At this candidate the triangle lies inside that quadrilateral and the
broadworm term is inactive. That is another warning that the local landscape
has qualitatively different basins; other seeded runs found balanced
hull/breadth basins near `0.23307`.

This makes the public target `0.2325` numerically plausible, with about
`3.03e-4` room below this local candidate. It proves no lower bound: a local
minimum is an upper bound on the global minimum of `Phi`, and the probe has no
interval arithmetic or exhaustive domain cover.

## Exact reproducibility blocker

Under the problem rules, the public summary is insufficient to check even one
terminal prune. A replay or independent checker still needs all of the
following absent data:

1. **Claim formula:** the exact objective and every geometric lower-bound
   predicate accepted by the producer. The clean-room `Phi` above is not
   confirmed by an artifact.
2. **Witness specification:** traversal-ordered coordinates for the U-worm,
   the exact broadworm construction or exact cited theorem, and the exact
   rational lower breadth used. The prose decimal `0.4389` does not identify a
   directed source derivation.
3. **Direct-motion gauges:** exact triangle and rectangle angular root domains,
   endpoint identifications, and proof that no reflection quotient was used.
4. **Compact translations:** the exact root translation box and the lemma that
   every target-violating configuration lies inside it.
5. **Tree:** all 499,842 visited boxes, rational split coordinates, parent/child
   coverage, terminal classifications, and maximum-depth leaves. Aggregate
   counts cannot establish coverage.
6. **Hull predicates:** the selected point cycle or support directions at each
   terminal leaf and the determinant intervals proving the proposed order.
7. **Intervals:** exact sine/cosine range reduction, Taylor degree and
   remainder, outward rounding rules, and every resulting rational endpoint.
   Saying the denominator was `2^100` does not determine any of these.
8. **Dependency boundary:** which KPS inequalities were imported, with their
   hypotheses and directed constants, versus independently re-established.
9. **Implementation provenance:** checker source, certificate/shard files,
   serialization schema, tool versions, deterministic replay command, and
   hashes or a signed/archived commit.
10. **Independent implementation:** even producer artifacts would remain
    `numerical` until another model family reimplemented the mathematical
    predicates as required by the Moser rules.

The kill criterion is therefore met for literal reconstruction: no accessible
artifact specifies a finite certificate, and the prose leaves multiple
load-bearing choices underdetermined. The public `0.2325` remains an
unreproducible grey claim, not a refuted claim. The clean-room probe supports
plausibility of one inferred route but supplies no verification credit.

## Comparison with frozen PR #168

This comparison is read-only and grants neither branch any status.

| feature | Proof.Fail public summary | PR #168 frozen candidate |
|---|---|---|
| endpoint | `0.2325`, provisional | `0.2323`, `sketch` |
| forced family | segment, equilateral triangle, `1/2` by `1/4` rectangle, broadworm breadth | segment, equilateral triangle, square, exact `t=10/13` rational arc |
| translations | apparently searched in six pose dimensions | algebraically cancelled by exact support allocations |
| remaining domain | six variables, exact root unavailable | explicit angular gauges; final replay covers worm angle `[0,180]` |
| area route | inferred actual L/T/R hull plus breadth predicate; unconfirmed | mixed-area/support-functional candidate |
| certificate | aggregate counts and filenames only | repository JSON, source checkers, tests, and replay command |
| independent status | unreproducible and unaudited | self-checked only; independent review pending |
| broadworm dependency | essential | absent from the final four-witness family |

PR #168's accessible artifacts make it reviewable but do not make it correct.
Conversely, the grey claim's larger endpoint and plausible numerical basin do
not compensate for the absent tree and checker. They are distinct proof
routes; neither can be used to validate the other.
