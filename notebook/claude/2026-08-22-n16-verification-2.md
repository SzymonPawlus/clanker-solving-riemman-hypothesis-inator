# 2026-08-22 — Verifier pass 2 on the $n=16$ covering lower bound

Role: Verifier for the $n=16$ push. Branch `claude/circle-equklatetal-problem-sa7tx7`.
Write-up: `problems/circle-packing-equilateral-triangle/attacks/n16-verification-2/README.md`.
Code: `experiments/packing-n16-verify-2/`.

## What I was expecting to do, and what was actually there

Briefed to check three live lanes (`n16-covering-2`, `n16-shapes`, `n16-dual`) pushing the record
upward toward the $4.6247636$ ceiling. **None of them has produced anything** — no directory in
this worktree, no local branch, nothing under `refs/remotes/origin/claude/`. The newest artefacts
on disk are `n16-covering/README.md` and `packing-n16-verify/manager_covering_check.py`, both from
the previous pass.

So the pass reduced to: re-verify the standing record from scratch, and leave calibrated checkers
behind for when the lanes land. That is what I did. Worth recording that "no artefact" is a
verdict — `could-not-follow, for want of an artefact` — and not a reason to invent one.

## The standing record: confirmed, no break found

`sub_s2_cert.json`, $a = 89267/20000 = 4.46335$. I wrote `covercheck.py` from
`problems/.../README.md` + `RULES.md` §2 without opening either existing certifier, and it agrees
on every number including the exact max squared diameter $\tfrac{2499900001}{2500000000}$.

Then eight families of break attempts (`adversarial.py`) — corners, per-edge 2001-point probes,
$\varepsilon$-balls around all 31 piece vertices, second/third diameters, per-piece maxima, union
area by a second route, dilate-to-the-ceiling. Nothing broke.

Then ten corruptions of the real certificate (`negative_controls.py`), all rejected. The two that
matter:

- **C1, diameter exactly 1** — the Lemma L equality case. Caught by the strict comparison.
- **C8, overlap + equal-area hole** — I translated one piece by $1/100$. Areas still sum exactly
  to $|T_a|$, and the area identity **does not fire**. Disjointness and the grid probe both do.
  That is the concrete demonstration that the first certifier's "areas sum, therefore covers"
  inference was genuinely unsound and not merely under-argued.

Building the negative controls was the most useful hour. A checker that has never rejected
anything is not evidence, and I would not have believed my own confirmation without them.

## The thing I did not expect: the certificate proves more than it claims

$2499900001 = 49999^2$. So the max diameter is **exactly** $49999/50000$, not "some number below
1" — there is $2\times10^{-5}$ of unused diameter slack sitting in the certificate.

Dilation about the chart origin by rational $\mu$ scales every squared distance and every area by
$\mu^2$ and maps $T_a\to T_{\mu a}$, preserving convexity and disjointness. So the same 15 pieces
give a valid covering for every $a' < a\cdot 50000/49999 = 446335/99998$, and since the set of
admissible sides is upward-closed,

$$a_{16}\ \ge\ 446335/99998 = 4.4634392687853754\ldots,\qquad s(16)\ \ge\ 12.3909801527\ldots$$

$+8.93\times10^{-5}$ in $a$. Tiny, but exact and free. I made `scale_up.py` emit five dilated
certificates and run each through the full nine-check pipeline rather than argue it in prose, so
the only unmachine-checked step is the one-line supremum.

The lesson is the mirror image of this campaign's usual one. The standing pattern is *the
arithmetic is right and the sentence after it is one step too broad*. Here the sentence was one
step too **narrow**: `KILL-CRITERION.md` had already defined the deliverable as "the supremum of
side lengths for which such a covering is exhibited", and the write-up reported the exhibited $a$
instead. Under-claiming is the safe direction, but it is still a mismatch between the certificate
and the sentence about it, and it is found the same way — by re-deriving rather than reading.

**Instruction I left for the lanes:** report $a/\mathrm{diam}_{\max}$, not the optimiser's frozen
$a$.

## Three disagreements

**D1 is the one with teeth.** `KILL-CRITERION.md` K4 caps a piece of diameter $<1$ at
$3\sqrt3/8 = 0.6495$ — the regular hexagon of diameter 1 — and derives $a\lesssim 4.5603$. The cap
is flagged "asserted, not cited", but it is worse than uncited: it is **false**. The disk of
diameter 1 is convex with area $\pi/4 = 0.7854$, and even among hexagons Graham's largest small
hexagon (1975) has area $0.6750$. With the isodiametric bound instead, the ceiling becomes
$a\le 5.0392$ — above the packing ceiling, hence vacuous.

This matters *now* rather than academically: three lanes are climbing from $4.4634$, K4 says
"stall within 1% of the ceiling, stop", and a lane that reads $4.5603$ as a wall will either quit
a live push or throw away a correct certificate at $a^\star\in(4.5603, 4.6248)$ as obviously
buggy. **$a^\star > 4.5603$ contradicts nothing proved.**

**D2.** `n16-covering` states the $4.6247636$ ceiling unconditionally. It is a literature value,
`numerical`, and `attacks/n16-exact/certificates/` is still empty. The previous pass wrote the
conditional form; this one dropped it. Same overread pattern, and it lands on the *only* tripwire
that would catch a wrong certificate near the top — which is exactly where you want the status
discipline to be strictest.

**D3.** Nit: "headroom is at most $0.161$" — it is $0.1614136$. Rounded the wrong way.

## Status, said plainly

**This grants nothing.** Same model family as every author, so `RULES.md` §5 gives it no weight
and the problem's `RULES.md` §3 is only half-satisfied — I wrote the independent checker, but a
Claude checking Claude is close to a checker checking itself. Everything stays `sketch`.

Highest exactly-verified bound surviving: $a_{16}\ge 446335/99998$, $s(16)\ge 12.3909801527$.
Against the best known packing $s(16)\le 12.7136288$, the interval is still $0.3226$ wide. **$n=16$
is nowhere near settled and nothing here should be written as if it were.**

## Housekeeping

Wrote only to `attacks/n16-verification-2/`, `experiments/packing-n16-verify-2/`, and this file,
per the ownership boundary I was given. No git commands, no PR, no issue comments — those are the
manager's to make.
