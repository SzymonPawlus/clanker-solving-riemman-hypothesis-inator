# Issue #134 audit repair

## Verdict

`VERIFIED CONDITIONAL ON CITED INTERFACES`

This is the verdict for the repaired paper proof in
`c02var-prescribed-angle-formalization.tex`. It is not a `verified:review`
status grant, not an end-to-end `verified:lean` claim, and not a promotion of
PR #122 beyond `sketch`. PR #135 remains verification-critical and must not be
merged without the cross-family or human review required by `RULES.md`.

## Concise changelog

1. **Anchored smoothing.** Lemma 5 now translates the periodic mollification
   so that `Q(0)=P(0)`, preserves regularity and embeddedness, proves equality
   of the `1`-variation error after translation, and derives the required
   uniform error from the anchored variation bound.
2. **Residual line cycle.** Proposition 8 now constructs a compactly supported
   smooth primitive for the tangential restriction of an arbitrary test
   one-form and uses the rectifiable tangent representation to prove that the
   residual cycle supported on the chord line vanishes.
3. **Short lifted arcs.** Proposition 10 now proves that a lifted restriction
   of parameter length at most `1/2` is injective with distinct endpoints
   before invoking the embedded-arc winding estimate.
4. **Dependency hygiene.** Downstream equation references and subsequence
   wording were synchronized; the generated PDF was rebuilt from the revised
   TeX.

## Dependency audit: `V₀` to Asano--Ike

| Stage | Audit result | Dependency/status |
|---|---|---|
| Fine squared variation and short-interval modulus | The seam factor and finite-scale use are explicit. | Internal `PROVED` |
| Polygonal interpolation | The every-partition `sqrt(8)` estimate supplies `2`-variation convergence; the simple interpolants are supplied by BG. | Internal `PROVED` + BG `CITED` |
| Regular smoothing | The translated mollifier is regular, embedded, anchored, small in `1`-variation, and therefore uniformly close. | Internal `PROVED` |
| Whole-family local modulus | Tail control comes from convergence in `2`-variation; the finite smooth prefix is Lipschitz. | Internal `PROVED` |
| Arc winding/current estimate | Excursion energy, isodiametric area, current decomposition, and line-cycle uniqueness yield the sharp `pi/4` bound. | Internal `PROVED` using pinned Jordan/index/current citations |
| Primitive compactness | Every short lifted restriction is now verified embedded; Green gives a common modulus and Arzela--Ascoli gives a relabelled subsequence. | Internal `PROVED` + Green/AA `CITED` |
| Liouville conversion | The exact-form identity transfers local uniform convergence to the Asano--Ike primitive convention. | Internal `PROVED` |
| Rectangle/nondegeneracy | The approximation hypotheses match AI Theorem 1.1; the source's off-diagonal/four-distinct conclusion makes the perpendicular-diagonal rectangle a positive square. | AI `CITED` + internal square algebra |

No `UNKNOWN`, `CITED-UNVERIFIED`, or assumed paper interface remains in this
ledger. The current Lean module formalizes only a growing foundational and
algebraic subset; its unformalized analytic interfaces remain documented in
`LEAN_DAG.md`.

## External interfaces independently rechecked

- **Boedihardjo--Geng**, arXiv:1309.1576v2, Theorem 2.2, PDF pp. 6--7:
  arbitrarily fine parameter partitions whose piecewise minimizing-geodesic
  interpolation is Jordan; in the plane these are affine chords.
- **Carmona--Cufi**, *J. Analyse Math.* 120 (2013), 225--253,
  DOI 10.1007/s11854-013-0019-9, preprint Theorem 2, PDF p. 8:
  the `L^2` index bound used to obtain `L^1` integrability on compact support.
- **Cufi--Verdera**, arXiv:1306.6832v1, main theorem, PDF p. 1:
  the rectifiable-curve Green identity, including the test-form and
  `f(z)=conj(z)` specializations and orientation signs used here.
- **Gilman--Kra--Rodriguez**, *Complex Analysis: In the Spirit of Lipman
  Bers*, GTM 245 (2007), Theorem 5.23: Jordan separation and the
  `0`/`plus-or-minus 1` index description.
- **Bieberbach**, *Jahresbericht DMV* 24 (1915), 247--250: the planar
  isodiametric inequality with constant `pi/4`.
- **Rudin**, *Principles of Mathematical Analysis*, 3rd ed., Theorem 7.25,
  p. 158: Arzela--Ascoli on a compact domain.
- **Asano--Ike**, arXiv:2412.21057v3, Theorem 1.1, PDF p. 2, together with
  the rectangle/nondegeneracy discussion on pp. 2--3 and the off-diagonal
  conclusion in the proof of Theorem 4.1 on p. 19.

These checks were performed separately from the TeX repair. No external
interface was promoted to a Lean theorem or hidden behind a new Lean axiom.

## Reproduction and artifact ledger

From the repository root:

```sh
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp \
  problems/square-peg/formalization/c02var-prescribed-angle-formalization.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp \
  problems/square-peg/formalization/c02var-prescribed-angle-formalization.tex
```

Final artifact hashes at the coherent repair checkpoint:

- TeX: `6492e7da223d0afd17a4498230c08bd48bc6eb5a224c5dbc3a25b9a12dea2f88`
- PDF: `32540d1f3eba87c064115e32878b67623eecda10f08952addda65934b2da65d8`
