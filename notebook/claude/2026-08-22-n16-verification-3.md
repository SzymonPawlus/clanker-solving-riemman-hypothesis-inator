# 2026-08-22 — worker V3, verification pass 3 over the $n=16$ covering bound

Issue #97. Branch `claude/circle-packing-subagents-9yg5gt`. Role: **verification only**
(`RULES.md` §8 convergent lane). Deliverable `attacks/n16-verification-3/README.md`.

## What I did, in order

1. Read `RULES.md`, the problem `RULES.md`, the problem `README.md`, and `FINDINGS.md`'s
   separation-1/separation-2 entry. Did **not** open `verify_c1.py`, `q3.py`, `exact_1p2r3.py`,
   `selftest.py` or either predecessor certifier. The only thing I read out of
   `experiments/packing-n16-covering-2/` is certificate **data**: the vertex table printed in the
   attack README, and `cert_rational.json`.
2. Wrote `experiments/packing-n16-verify-3/` from scratch: `q3f.py` (exact $\mathbb{Q}(\sqrt3)$),
   `geom.py` (exact convex geometry in the triangular chart), `check_v3.py` (the checker),
   `cert_v3.py` (my own transcription of the 15 pieces), `surd.py` + `table_check.py` (the
   $a_n$ table), `dilation_check.py` (the $a_4$ discriminating test), `selftest_v3.py`
   (corruptions), `break_attempt.py` (the attempt to refute).
3. Ran everything. Wrote it up.

## The three things I want to remember

**The coverage check is the whole certificate, and the naive implementation explodes.**
My first residue algorithm — subtract each piece from a global list of residue parts — reached
30 208 parts at piece 10 and was still running. The fix was to make it depth-first with an index:
each stack item is a convex part $Q$ together with the index $j$ of the first piece that might
still meet it, and $Q$ is split only by the first piece it actually touches. 4 434 nodes, peak
stack 17, 20 s. The soundness argument that lets zero-area parts be dropped is worth writing down
once: $\bigcup P_i$ is closed, so $T_a\setminus\bigcup P_i$ is relatively **open** in $T_a$, and a
non-empty relatively open subset of a triangle has positive area. So "residue has measure zero"
really does mean "residue is empty" — it is not a slack step.

**My one false alarm was a certificate-format ambiguity, not a bug in the work.** My checker first
reported `cert_rational.json` as FAIL with $a\approx 6\cdot10^{14}$: their JSON writes `"a"` as
`[numerator, denominator]`, and I parsed the two-element list as $p+q\sqrt3$, which is my own
convention. Both are defensible and the repo's `RULES.md` §2 pins neither. Two independently
written checkers are *supposed* to disagree here; the lesson is that a JSON field whose meaning
depends on which paper you read is exactly the hole that §2 exists to close for the interval
encoding, and it is still open for covering certificates. Flagged, not counted against the claim.

**Everything I confirmed is still `sketch`.** I am Claude Opus 5; so was the author, and so were
the three checkers before me. §5's whole point is decorrelated families. A fourth Claude agreeing
is close to worthless as certification and I have said so at the top of the deliverable.

## Where I would push next

The bound is fine and the delicate step (dilation) is genuinely airtight. The soft spot in the
attack file is *not* the bound; it is finding **1** in "Why this is where the family stops", whose
case split over $n_2$ (pieces meeting two sides) covers $n_2=3$ and $n_2=6$ and skips $n_2\in
\{4,5\}$. That is a `sketch` auxiliary claim, so nothing downstream breaks, but "the layout is
forced to be 3 corner + 9 edge + 3 interior" is not established, and the Euler/trivalence count
built on it inherits the gap. If anyone builds an exhaustion argument on that structure, this is
where it will leak.
