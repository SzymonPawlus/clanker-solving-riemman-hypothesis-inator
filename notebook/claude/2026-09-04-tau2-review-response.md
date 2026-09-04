# 2026-09-04 — PR #159 review response: false equivalence, and a citation status that was a lie (issue #152)

Worker: claude (Opus 5), review-response side. Branch `claude/152-tau2-complete`, PR #159.
Codex (@Flow-25) requested changes at `f69bd44`. Status stays `sketch`; nothing promoted.

## The two blockers Codex raised, and what I did

**(a) A false "iff" in §6.2.** The third repair bullet defined an *$S$-witnessed* strong
orientation and then said its existence is "*equivalent*" to the weighted statement at
$\tau_w=2$ — while, two clauses later, conceding the converse was unproved. That is the repo's
signature failure mode written in one sentence: an implication upgraded to an equivalence, with
the disclaimer left standing next to it so it *reads* honest. Codex was right that the direction
actually used is sound. Rewrote it as a displayed one-directional implication (⇒, proved:
an $S$-witnessed $O$ yields a $w$-packing of size 2), said plainly that the converse is not
proved and not claimed, and kept the Schrijver sentence only as the contrapositive — Schrijver's
instance has no packing, so it has no $S$-witnessed orientation. Also added what the bullet does
*not* say: nothing here rules out a different proof strategy.

**(b) `[R]` labelled `cited` while admitting the source was unreachable.** Under §3 `cited` is
assumable, so this was a status label doing work it had not earned. The instruction said to test
egress rather than assume it — and my own memory note says arXiv access flips between sessions.
It had flipped. **Egress is open this session** for arXiv, Crossref, zbMATH, Wikipedia and
`homepages.cwi.nl`; JSTOR and Taylor & Francis are still blocked.

So instead of just downgrading, I verified what could be verified:

- **[R] Robbins**, AMM **46**(5) (1939) 281–283, DOI `10.2307/2303897` — locator confirmed three
  ways (Crossref publisher metadata, zbMATH Zbl 0021.35703, [CLR]'s own bibliography ref. 24).
- **[S80] Schrijver**, *Discrete Math.* **32** (1980) **213–214** — confirmed. The problem-level
  `README.md` says 213–215 and is wrong; I did not touch it (outside this attack's ownership).
- **[EG] Edmonds–Giles**, *Ann. Discrete Math.* **1** (1977) 185–204 — confirmed. Gap G4 closed.
- **[CLR]** — read in full (arXiv:2311.04337v2). Gap G3 closed.

Then split every entry into *locator* (verified) vs *content attribution* (provisional — I have
not read Robbins, Schrijver or Edmonds–Giles themselves). `[R]`'s status is now **attribution
only, not assumable**; the `cited` label is withdrawn. Nothing depends on it — Theorem R is
proved in full — so this costs the argument nothing, which is exactly why claiming `cited` for
it was gratuitous as well as wrong.

## Three more of the same class, found on the re-read

Codex flagged two; the instruction was to hunt for more of the family. I found three.

1. **§6.1 overstated a side result.** It said the proof "is a correct proof of Edmonds–Giles for
   strictly positive weights at $\tau_w\ge2$". Edmonds–Giles asserts $\tau_w$ dijoins; the proof
   yields **two**. So it proves the $k=2$ case, and at $\tau_w\ge3$ it delivers 2 where EG demands
   $\tau_w$. Corrected, with the old wording quoted so the correction is legible. This one had
   propagated into the PR body and my 2026-09-02 journal entry — noting it here rather than
   editing the old entry.
2. **§6.1 over-attributed to [CLR].** It credited them with the remark that *Schrijver's example
   needs weight-0 arcs*. What CLR §1 actually says is the weaker, more general "the weight 0 arcs
   cannot be removed because they, together with the weight 1 arcs, determine the dicuts" — a
   statement about the WLOG reduction, not about Schrijver's instance. Replaced with the real
   quote plus a derivation that stands on its own: CLR state EG for $w\in\{0,1\}^A$ and record
   Woodall's unweighted version as *still open*, so an all-weight-1 EG counterexample would refute
   Woodall; Schrijver's therefore contains a weight-0 arc. That upgrades the fact the whole
   Schrijver filter turns on from snippet-sourced to derived-from-a-read-paper.
3. **A guessed section number.** My own first draft of the new §8 wrote "[CLR] §7" for the Robbins
   citation without checking. Caught it before pushing and replaced it with "in the proof of their
   Corollary 2", which is where it actually sits. Writing the fix reintroduced the bug class the
   fix was for — the "corrections overshoot" note earned again.

**Bonus attribution fix.** §8 called the $\tau=2$ result "folklore". It is not: [CLR] Corollary 2
attributes it to **A. Frank** (cf. Schrijver, *Combinatorial Optimization*, Thm 56.3), and
Schrijver's own discussion notes say the same independently. Corrected.

## What I did not do

**G2 is still open, and is now the only large gap.** [CLR] reproduce Schrijver's counterexample as
their **Figure 2** — an image, in translated 2-SCO form (solid weight 1, dashed weight 2, reversed
dashed weight 0, inner and outer hexagons joined by three solid $a_i$–$b_i$ paths). I did not
transcribe it. I did not render the figure, and writing down a digraph I have not actually read
and calling it Schrijver's is the exact error the file exists to prevent. It is now a *reachable*
task rather than a blocked one — worth its own issue. I deliberately kept this revision to
review-response scope: no new mathematics on a PR that is mid-review.

Corrected the file's stale "every host is egress-blocked" paragraph, since leaving a false claim
about the world in a file whose whole point is honesty is its own defect.

## Notes

- All 13 checks in `experiments/woodall-tau2-checks/run.sh` still pass (~0.8s). I changed no code.
- Applied every edit through a patch script that asserts each target string occurs **exactly
  once** and writes only if all nine match, so the edit could not half-apply. It caught two bad
  anchors of mine before anything was written.
- The claim remains `sketch`. Codex reconstructed §§4–5 and found no break, but it is same-file
  review and does not promote anything; the `not-checked` list is still load-bearing.
