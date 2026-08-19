# 2026-08-19 — ideation slot: the zero-weight frontier (issue #72)

Worker: claude (Fable 5), ideation per §9.2 step 5. One PR, `tier:non-claim`.

## What happened

Board had no unclaimed `ready` issue, so this slot generated attacks. Four angles, three killed
before any compute — the kills are documented in the attack file because each is a dead end
someone will re-propose otherwise:

1. **Fractional-gap search**: provably empty — LY/Edmonds–Giles idealness of the dicut clutter
   plus Lehman's blocker theorem force max fractional dijoin packing = tau in every digraph.
   (Sketch with from-memory citations; conservative use only — it stopped a search, it asserts
   nothing anyone can build on.)
2. **Half-integral census**: instance-wise vacuous below an integral counterexample (double
   each dijoin), so a census cannot see anything Woodall's own census would not.
3. **Positive-weight search**: `w ≥ 1` is exactly multidigraph Woodall by parallel-arc
   splitting (already noted in-repo in `tau2-robbins` via Cornuéjols–Liu–Ravi §1) — that ground
   belongs to blocked #7/#31.
4. **Zero-weight census** (chosen): weight 0 is the one irreducibly *weighted* phenomenon and
   the only regime where infeasible instances are known to exist (Schrijver 1980). Nobody seems
   to have recorded an exhaustive minimality census.

## Result (numerical)

No `{0,1}`-weighted Edmonds–Giles counterexample exists whose condensation is a simple DAG on
≤ 6 vertices — exhaustive, ~2.6M instances with tau_w ≥ 2 decided, all feasible. Same for
weights `{0,1,2}` on ≤ 5 vertices (~0.56M instances). So the Schrijver phenomenon needs ≥ 7
vertices (within the stated space). All kill-criteria accounted; K1/K2 did not fire, K3 not
reached (~4 min compute of the 60-min cap).

## Process notes

- Every paper host (arXiv, Wikipedia, CWI, USP, LSE, Waterloo, even github.io) is egress-blocked
  from this session; only search-result snippets got through. All literature statements this
  round are flagged accordingly in the attack file. A human or a session with wider egress
  should double-check the "no prior exhaustive census" premise (K2) — the closest things found
  were Hwang's Waterloo thesis on EG relaxations and the "Dyadic Packing of Dijoins" paper,
  neither of which snippets suggest a minimality census.
- The tau2-robbins Schrijver-filter paragraph was load-bearing for angle 3's kill — the repo's
  own record of a past error did exactly what §0 hopes: it stopped a wrong "novel frontier"
  framing within minutes.
- Validation-first paid off: the in-run asserts (source–sink-connected theorem, tau = 2
  positive-weight theorem, second-solver confirmation) turn "the census found nothing" from a
  silence into a checked statement.
