# Five-cut owner monotonicity and boundary blocks

Issue #198. Status: **sketch**, verification-critical.

This fresh continuation integrates the frozen interfaces of PRs #189 and #197
without modifying either. `Verified.Moser.OwnerMonotonicity` proves the final
finite combinatorial part of the five-sector boundary sweep.

## Kernel-checked result

Cut a simple strict-convex polygon boundary at one ray and unwrap one full
turn. Let `ray : Nat -> alpha` be its strictly increasing outward-ray ledger.
A cut value `c` is owned by `i` under the half-open convention when

```text
ray i <= c < ray (i+1).
```

The module proves:

- a cut has at most one owner;
- if `c <= d`, their owners satisfy `owner(c) <= owner(d)`;
- five cyclically ordered cuts therefore have monotone owners
  `t0 <= t1 <= t2 <= t3 <= t4`;
- the consecutive block from prefix `a` to prefix `b` sums exactly to the
  difference of the corresponding boundary endpoints;
- after adjoining the next-cycle lift `t5` of `t0`, all five blocks—including
  the wrap block from `t4` to `t5`—have exactly the endpoint-difference sums
  consumed by PR #189's `five_block_telescoping`.

The combined theorem is `five_cut_sweep_blocks`. Empty blocks, caused by two
cuts sharing one owner cone, are allowed and correctly contribute zero.

## Dependency boundary

PR #197 proves determinant-only existence of a maximizing half-open owner for
every nonzero normal under strict turns and global edge support. The present
module proves that owners are monotone once the simple convex boundary is
represented by a strictly increasing unwrapped ray ledger. Thus no common-fan
merge, arbitrary exposed-point choice, or inserted repeated-vertex object is
needed.

One representation lemma remains outside this PR: construct the unwrapped
strict ray ledger from the cyclic edge normals of the concrete simple
strict-convex containing polygon, and identify PR #197's positive cone
coefficients with the corresponding half-open key interval. This is an order
encoding fact, not a remaining block-sum or tie-breaking identity. The exact
pentagram regression in PR #197 shows why global edge support/simple convexity
must remain explicit when constructing that ledger.

The module and full repository build compile without `sorry`, `unsafe`, custom
axioms, or `native_decide`.
