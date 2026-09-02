# Post-2013 record and motion-convention audit

**Status:** cited landscape, pending cross-family review. This file audits what
has been published; it does not independently verify the proof of the published
`0.232239` theorem, and it does not use PR #168.

**Search date:** 2 September 2026. **Issue:** #169.

## Verdict

No later stronger published or preprint convex lower bound was located as of
2 September 2026. The located record remains

\[
  m_{\rm conv}\ge 0.232239
\]

from Khandhawit--Pagonakis--Sriswasdi (KPS), published in 2013. No indexed
post-2013 primary source located in this audit claims a larger lower bound for
convex covers of all open unit arcs. In particular, a **certified lower
endpoint equal to the exact decimal** `0.2323` would exceed the located
published record by

\[
  0.2323-0.232239=0.000061.
\]

It would therefore appear to be a genuine published-record improvement for
the repo's orientation-preserving constant, subject to independent
verification and to a final current-literature check at submission time. A
numerical optimizer value near `0.2323`, or an interval whose lower endpoint
does not exceed `0.232239`, would not establish that claim.

This is a conclusion about the **published/preprint record**, not unrestricted
public priority. A non-journal web attempt posted to
[`Proof.Fail`](https://proof.fail/p/12) with status date 24 August 2026 claims a
provisional, independently unaudited interval certificate for `0.2325`. The
page itself says the result is not peer reviewed or independently audited and
describes its priority claim as provisional; it provides filenames but no
download links, repository, exact witness, or archival identifier for the
alleged lower-bound certificate. The page attributes the attempt to a
Proof.Fail account named Dan Stoyell; that account profile links no external
research identity or repository. Exact-filename web searches and authenticated
GitHub code searches for `worm_rigorous_checker.py` and
`worm_02325_certificate_audit.py` returned only the page itself and zero public
GitHub files, respectively. It is not a paper or scholarly preprint located by
either citation index, so it does not replace KPS as the published record and
cannot be reproduced from the located public artifacts. It does mean that
`0.2323` should **not** be called the first public stronger candidate without
resolving provenance and dates. The page downloaded on the search date has SHA-256
`ca92521471f955b288c898f63755c137ff693fbdcfa11020bfcd3cfc4e430ac2`.

The resulting three-tier landscape is:

| tier | endpoint | conclusion |
|---|---:|---|
| peer-reviewed/arXiv record located | `0.232239` | KPS remains the citable record; no later stronger paper or preprint was located as of the search date. |
| public grey claim | `0.2325` | Proof.Fail, dated 24 August 2026; explicitly provisional and unaudited, with no located certificate artifacts. It blocks a claim of first public priority, not a claim of improving the published record. |
| frozen PR #168 candidate | `0.2323` | Exact candidate endpoint under repository review; neither verified nor published, and weaker than the grey numerical claim. |

The motion convention does not obstruct this comparison. KPS says
"congruent" without defining whether reflections are admitted. Its actual
lower-bound witnesses and inequalities apply to orientation-preserving covers:
the segment, V-worm, and U-worm are achiral as unlabelled arcs, while the only
broadworm input is its reflection-invariant breadth. KPS's reflection in the
angular normalization acts only on the achiral rectangle/triangle placement;
it never requires the cover to contain a reflected broadworm. Thus the cited
`0.232239` is a lower bound under the repo's direct-isometry convention as
well.

By contrast, the two *definitions* are not automatically equivalent for all
worms: a chiral arc and its mirror form distinct direct-isometry orbits. A
cover allowed to use arbitrary congruences may cover both by the same handed
placement, whereas a direct-isometry universal cover must accommodate both
handednesses. Any new chiral witness must therefore keep the repo's no-reflection
placement domain unless its mirror is separately included or direct-achirality
is proved.

## Pinned record source

T. Khandhawit, D. Pagonakis, and S. Sriswasdi, *Lower Bound for Convex Hull
Area and Universal Cover Problems*, *International Journal of Computational
Geometry & Applications* **23**(3) (2013), 197--212, DOI
[`10.1142/S0218195913500076`](https://doi.org/10.1142/S0218195913500076).
The only arXiv version is
[`1101.5638v1`](https://arxiv.org/abs/1101.5638v1), submitted 28 January 2011.

The abstract, Section 1, Proposition 3.5, and the end of Section 3 state the
`0.232239` convex universal-cover bound. The proof uses a unit segment, a
two-edge V-worm, a three-edge U-worm forcing a `1/2` by `1/4` rectangle, and
Schaer's broadworm. The proof-level caveats and independent reconstruction are
recorded separately in
[`baseline-0232239`](../baseline-0232239/README.md); this audit relies only on
the publication claim as `cited`.

Pinned artifacts downloaded on the search date:

| artifact | SHA-256 |
|---|---|
| arXiv v1 source archive | `03518f85d1d19fc6b0888c60b05831dc130afbf10218913723c6764d2cd71ccb` |
| arXiv v1 generated PDF | `9fa6e50aaba59459efd7e62f578573c5be3f866732ad2903319d2f8ab4e0a261` |
| Crossref DOI response | `ba92cf9f34bebf96e3968917d9e2c67d0a265d36fb3848e16beff41b2b8f8c78` |

Crossref confirms the DOI, journal, volume 23, issue 3, pages 197--212, and
June 2013 publication date. The arXiv source hash agrees with the earlier
independent baseline audit.

## Forward-citation and current-source screen

OpenAlex work
[`W2163081350`](https://openalex.org/W2163081350) returned eight citing works.
The complete citing-work response had SHA-256
`0fa813960928a5ac05e795e3a59ca7029397d898b628c4e03af5451e3b52f392`.
Semantic Scholar paper
[`cdb40ad83fa0583d6e820993c7ed934301fddbb2`](https://www.semanticscholar.org/paper/cdb40ad83fa0583d6e820993c7ed934301fddbb2)
returned fourteen records; its response had SHA-256
`c382ceedca3202130598f8f64da1aeddfb035320458961edfa800814d0ed1a0c`.
The difference consists of duplicate/preprint records and additional recent
preprints, not a competing lower-bound paper.

The relevant forward citations were screened as follows:

| year | source | relevance to the lower-bound record |
|---|---|---|
| 2016 | P. Gibbs, *Lost in an Isosceles Triangle* | Lost-in-a-forest/upper-cover direction; no improved convex lower bound located. |
| 2019/2021 | Panraksa--Wichiramala, *Wetzel's sector covers unit arcs*, DOI [`10.1007/s10998-020-00354-x`](https://doi.org/10.1007/s10998-020-00354-x) | Convex **upper** cover. |
| 2019/2020 | Grechuk--Som-am, closed-unit-curve papers, DOIs [`10.1142/S0218195920500065`](https://doi.org/10.1142/S0218195920500065) and [`10.1016/j.disopt.2020.100608`](https://doi.org/10.1016/j.disopt.2020.100608) | Different family: closed unit curves. |
| 2022 | Haim-Kislev--Ostrover, *Viterbo's conjecture as a worm problem*, DOI [`10.1007/s00605-022-01806-x`](https://doi.org/10.1007/s00605-022-01806-x) | Symplectic/closed-trajectory worm variant; cites KPS but does not replace the open-arc convex bound. |
| 2023 | Cheong--Devillers--Glisse--Park, *Covering families of triangles*, DOI [`10.1007/s10998-022-00503-4`](https://doi.org/10.1007/s10998-022-00503-4) | The abstract and main theorems concern triangle families, not all unit arcs. Its introduction independently calls KPS's approximately `0.232` value the best known Moser lower bound. |
| 2025 | Y. Movshovich, *Recent advances in the worm problem*, DOI [`10.1007/s40879-025-00851-8`](https://doi.org/10.1007/s40879-025-00851-8) | Peer-reviewed survey of arc-cover progress, focused on the Wetzel sector theorem; cites KPS and lists no later lower-bound source. |
| 2026 | Deng, arXiv:`2607.18563` and arXiv:`2608.01393v2` | Broadworm/triangle fitting and numerical upper-cover directions. The full `2608.01393v2` text describes the current lower bound only as rounded `0.2322`, cites KPS for it, and derives numerical **upper** bounds; no improved lower-bound theorem is stated. The inspected v2 PDF hash is `fdeb4ab643b30e30ac11a266400ca160fcc2a2c50325fdb35b3df93f9d85a3de`. |

One obviously spurious OpenAlex citation (*Computation of Feasible and
Invariant Sets for Interpolation-based MPC*) was discarded as unrelated.

Two independent current checkpoints are especially strong evidence for the
record conclusion:

1. Wichiramala--Panraksa,
   [`arXiv:2606.14625v1`](https://arxiv.org/abs/2606.14625v1), a June 2026
   primary paper proving a convex triangular upper cover, explicitly states
   in its Introduction, immediately before its literature roadmap, that
   "For convex covers, the bounds prior to the sector theorem were
   `0.232239 < alpha <= 0.27091`" and the following sentence attributes the
   lower endpoint to KPS. Its
   downloaded 68-page PDF has SHA-256
   `93281aa646d4422b9146b498eeecf24e532fd0796d9bafc4659c9d2964e6b738`.
2. Tao's public optimization-constants index, problem 13a, still lists
   `0.232239` as the lower bound for the Moser convex worm cover constant:
   <https://github.com/teorth/optimizationproblems>. The pinned README commit
   is
   [`3a1491040076a3f67a52719e366f5e6b139e5c24`](https://github.com/teorth/optimizationproblems/commit/3a1491040076a3f67a52719e366f5e6b139e5c24)
   (27 August 2026), and the downloaded README has SHA-256
   `d767d9223389b54462275ec3bb457bc728d0b0758c231b11e35aad6994753f29`.

These searches cannot prove the nonexistence of an unindexed paper. They do
cover the exact-title/decimal searches, both major forward-citation indexes,
Crossref metadata, a peer-reviewed 2025 survey, and a June 2026 primary paper
that states the landscape. Exact-decimal web searches additionally found the
non-publication `Proof.Fail` candidate classified above, but no later stronger
published or arXiv lower-bound claim.

## Motion-convention audit

Let `direct` mean translation followed by rotation, as in this repository, and
let `full` additionally allow reflection.

- KPS normalizes the unit segment to horizontal by rotation. Its point
  reflection is a half-turn and hence direct. Its reflection across the
  y-axis reduces the rectangle/triangle angle domain. The U-shaped rectangle
  arc and equilateral V-arc are each direct-congruent to their mirrors, so
  this angular reduction is valid under `direct`.
- KPS never reflects the broadworm in deriving Proposition 3.4. It uses only
  the existence, in the placed broadworm, of two points with transverse
  separation at least its minimum breadth. Breadth is invariant under either
  convention.
- Consequently every repo-universal cover supplies exactly the placements
  needed by the KPS inequalities. No claim that the broadworm itself is
  direct-achiral is needed.
- The 2026 Wichiramala--Panraksa upper-cover paper explicitly treats
  "congruent copies" using rotations and possible reflections. This is an
  upper-bound convention and does not weaken the KPS lower-bound comparison
  just established. It does show why future sources must be classified rather
  than silently equated.

The safe novelty wording is therefore: **no later stronger published or
preprint bound was located as of 2026-09-02; a cross-verified bound
`m_conv >= 0.2323` for translations plus rotations appears to improve the
located published convex lower-bound record `0.232239`.** It should not be
advertised as a peer-reviewed record until publication, and it should not be
restated for the weaker full-congruence constant without a separate argument.

## Read-only chirality audit of frozen PR #168

This subsection classifies the proposed fourth witness and motion domain; it
does not rely on PR #168's area claim and makes no change to that frozen PR.
The inspected head was commit
`bd1371e5292e92c6388fcf565ffe2c3311f8ccab`.

For its `t=10/13` three-edge unit arc, the normalized edge directions are

```text
u0 = (1,0)
u1 = (69,260)/269
u2 = (-62839,35880)/72361.
```

Exact arithmetic gives, for both consecutive pairs,

```text
dot(ui,u(i+1))   = 69/269
cross(ui,u(i+1)) = 260/269.
```

Hence the two signed turning angles are equal. If the reflected chain is
traversed backwards, its edge-angle sequence differs from the original
sequence by one constant angle, so a rotation carries the original unlabelled
arc image to its mirror. Explicitly, writing that common turn as `delta`, the
original edge angles are `(0, delta, 2 delta)`, while the backwards traversal
of the mirror has angles
`(pi - 2 delta, pi - delta, pi)`; rotation through `2 delta - pi` turns the
latter into the former. The witness is therefore **direct-achiral**, although
it has no half-turn symmetry and is reasonably described as asymmetric in
that narrower sense. Reversing traversal alone does not perform the rotation;
the conclusion uses reversal only to compare the same unlabelled arc image.

PR #168 does not depend on this extra achirality:

- `domain.json` records
  `orientation_preserving_rotational_gauge_no_reflection`, with the rational
  arc angle in `[0,180]`.
- `support_bfs.json` records an
  `orientation_preserving_rotation_180_about_segment_midpoint`, shifts the
  worm angle by 180 degrees, and sets `reflection_used` to false.
- `check_domain.py` rejects a reflection convention. `check_support_bfs.py`
  rejects a changed action and instructs the caller to restore `[0,360]` if
  the direct half-turn is unavailable. Their adversarial tests exercise both
  rejections.
- `check_support_union.py` covers every atom of `[0,180]`; it does not identify
  mirror angles or shorten that quotient.

Geometrically, the global half-turn about the midpoint of the pinned unit
segment preserves that unlabelled segment, rotates every other placed witness
by 180 degrees, and shifts every translation anchor accordingly. It is a
direct isometry. Thus the frozen proof domain uses translations, rotations,
the triangle/square rotational symmetries, and this global half-turn only;
no reflection quotient was located.

## Reproducible index queries

The landscape was obtained with these read-only endpoints (responses vary as
indexes update):

```text
https://api.crossref.org/works/10.1142/S0218195913500076
https://api.openalex.org/works/https://doi.org/10.1142/S0218195913500076
https://api.openalex.org/works?filter=cites:W2163081350&per-page=100
https://api.semanticscholar.org/graph/v1/paper/DOI:10.1142/S0218195913500076?fields=paperId,title,year,citationCount,citations.paperId,citations.title,citations.year,citations.externalIds
```
