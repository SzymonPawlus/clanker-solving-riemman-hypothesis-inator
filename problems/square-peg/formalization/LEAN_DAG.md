# Lean dependency DAG for the vanishing 2-variation argument

This maps the LaTeX proof to Lean. **Paper only** and **external source** are
not `verified:lean`. Proposition parameters do not formalize analytic results.
`fineEVariationSq` is the paper's `w₂²`, not `w₂`; their zero-limit
equivalence still needs an explicit nonnegative square-root bridge.

Current checkpoint status: D1/D2 are faithful definitions; L3 is finite
algebra only, and its path-level refinement/supremum lift remains pending.

| Node | Content/dependency | Lean status and principal risk |
|---|---|---|
| D1 | ordered partitions, mesh predicate, sampled squared increments | `OrderedPartition`, `.IsMeshLE`, `sqIncrementSum`, `partitionEnergy`, equispaced/singleton existence, exact joint-dropping concat with mesh/energy additivity, and mesh-controlled superinterval extension |
| D2 | `w₂²` ENNReal supremum, nonempty interval, finite scale, vanishing | `fineEVariationSq`, `VanishingVariationData`, energy upper bound, mesh monotonicity, and subinterval-energy bound by global fine variation; square-root limit bridge pending |
| L3 | seam and every-partition `√8` interpolation estimate | finite algebra plus mesh-preserving existing-node `prefix`/`suffix` infrastructure proved; exact prefix/suffix energy split is blocked on dependent edge-count transport, and inserted-node/path supremum lifts remain pending |
| H4 | mesh-fine simple parametrized PL interpolation | **External:** Boedihardjo--Geng Theorem 2.2; must be encoded with its concrete source-shaped statement |
| L5 | periodic regular smoothing with small 1-variation error | convex-combination/error constants proved; convolution/global topology paper only |
| L6 | whole-family local 2-variation modulus | **Paper only:** depends on D2/L3 path lift and finite smooth-prefix bounds |
| H7 | Jordan domains, isodiametric inequality, rectifiable-current representation/boundary | **Concrete external boundary:** countable mass convergence and filling identification remain high-risk |
| L8 | embedded-arc absolute winding estimate, constant `π/4` | **Paper only:** excursion partition plus H7 |
| H9 | Green formula for arbitrary closed rectifiable curves | **External:** Cufí--Verdera main theorem; orientation/form normalization must be discharged |
| L10 | common Liouville modulus and locally uniform primitive subsequence | **Paper only:** H9+L6+L8+Arzelà--Ascoli |
| H11 | Asano--Ike approximation criterion | **External:** arXiv:2412.21057v3 Theorem 1.1; exact parameter/smoothness/primitive statement required |
| L12 | chord determinant and exact Liouville conversion | proved by `cross_eq_cross_sub`, `liouville_segment_conversion` |
| L13 | discharge H11 analytic data | **Paper only** until L5/L10 and source-shaped structures exist |
| H14 | off-diagonal, four-distinct nondegeneracy | **Concrete sourced boundary**, kept distinct from H11 |
| C15 | `θ=π/2` rectangle is a positive square | algebraic core `dot_add_sub`, `normSq_eq_of_perpendicular`; geometry depends on H14 |

## Checkpoint order

1. D1--D2 and finite L3: definitions, refinement, seam, affine chord, `√8`.
2. Path-level L3 and L6.
3. L5 smoothing.
4. H7/L8/H9 winding and Green layer.
5. L10--C15 using concrete source-shaped interfaces.

Only declarations reachable from `lean/Verified.lean`, passing `lake build`,
and free of `sorryAx` under `#print axioms` are Lean-verified.
