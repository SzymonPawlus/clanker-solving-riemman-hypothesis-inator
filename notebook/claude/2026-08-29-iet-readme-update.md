# 2026-08-29 — bringing `problems/inscribed-equilateral-triangle/README.md` up to date

Worker: `claude` (Claude Opus 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane: exactly two files — the problem README and this journal. Nothing else touched; no git
command run (the dispatcher commits).

## What the task was

The README was written this morning by the literature lane, before any attack ran. It recorded the
literature landscape well and said nothing about what the repo had since produced. `problems/README.md`
makes a problem's README the place its state lives, so a reader arriving after round 1 and round 2
could not tell from it what this project knows.

## What I added

1. A new section, **"What this project has established — a separate table, and none of it
   assumable"**, sited between "Known results" and "What remains open". It carries:
   - a status banner asserting that every in-repo row is `sketch` or `numerical`, that nothing is
     `cited`/`verified:lean`/`verified:review`, that nothing is assumable including by its own
     author, that **no agent outside the Claude family has examined any of it and Codex has
     reviewed none of it**, and that the single lane with any examination at all
     (`convex-vertex-criterion`) has one same-family audit and one same-family cross-review, both
     of which confer no verification credit;
   - a one-line contrast with the literature table: those rows are *probably true and unread*,
     these are *read in full and unverified outside one model family*; neither is assumable, for
     opposite reasons;
   - a dependency-hygiene note: no in-repo result uses a `cited`\* row as an input, so a failure of
     the verification debt would not propagate into the new table. Every lane checked itself
     *against* Meyerson afterwards and said so;
   - a 10-row results table (A1–A10), each row carrying its statement, status, **regularity budget**
     and owning lane;
   - a 5-row **refuted/corrected** table, because those entries are what stop the work being redone;
   - the rectifiable/spiral synthesis, with the reason the two do not collide and an explicit note
     that the synthesis is capped at `sketch`.
2. A three-line pointer in the header block so a reader who never scrolls past the banner still
   learns that the in-repo material exists and is unassumable.
3. Two `Layout` entries: `results/` is still empty and correctly so, and this problem's numerics live
   in `experiments/inscribed-triangle-{polygons,angular}/`.

I did not touch the provenance warning, the `cited`\* table, the asterisk paragraph, the verification
debt section or the sources. The separation between "unread literature" and "unverified in-repo" is
now made twice — in the header and in the new banner — which was the point.

## Discrepancies between the dispatch brief and the source files

The brief said its summaries were "a map not the territory". Five places where the territory differs:

1. **The synthesis needs "with unit speed".** The brief's headline was "every exceptional point is a
   point where the arclength parametrisation fails to be differentiable". Theorem T's hypothesis is
   differentiability of $\gamma$ at $t_0$ **with $|\gamma'(t_0)| = 1$**, and Corollary T3 is stated
   with that qualifier (`attacks/rectifiable-case/README.md` §6.2, §6.4). Dropping the three words
   states something the lane did not prove — a point where $\gamma$ is differentiable with
   $|\gamma'| < 1$ is not covered. (Such points are a null set, so Corollary T1 is unaffected; the
   *pointwise* statement is the one that needs the qualifier.) I wrote the qualifier into the README
   and flagged it as load-bearing.
2. **The half-density bound is strict, and "≤ ½" undersells it.** The lane proves
   $\lambda(\overline\Omega \cap \bar B(O,R)) < \tfrac12\lambda(B(O,R))$ — strict, and for the
   *closure* $\overline\Omega$, not $\Omega$ (§5.2). The lane says both improvements are what let the
   contrapositive be stated with $\ge$. Separately, "½ sharp" is sharpness of the constant in the
   topology-free Lemma H (the angular sup is exactly 180°, and there is no route to 1/6), not
   sharpness of the ball statement for Jordan curves.
3. **The convex criterion's boundary case is two-sided, not a "subtlety".** At $\alpha(O) = 60°$
   exactly the lane proves an **iff** (good $\iff$ both extreme rays of the tangent cone meet $K$ in
   a positive-length segment, Thm B(ii)) and exhibits a convex witness $K^*$ where it fails. And the
   counting is two statements, not one: at most **two** points with $\alpha < 60°$ (Thm C(a)), at most
   **three** with $\alpha \le 60°$, with equality forcing $K$ to be an equilateral triangle whose
   vertices are all good (Thm C(b)). "At most two such points exist" is C(a) only.
4. **The spiral's generalisation is explicitly *not* a classification.** The brief gave the
   generalisation as "arcs of width < 60° that rotate with the radius", which matches Lemma 2. But
   §12.3 of that file states plainly that rotating-wedge is a mechanism and not a classification of
   $E(J)$, with the counterexample $\Theta_J(r) = \{0°,100°,200°\}$. I carried that caveat into the
   row rather than letting the generalisation read as a characterisation.
5. **A lane the brief did not list is complete and belongs in the table.**
   `experiments/inscribed-triangle-angular/` is a second, structurally different exact decider
   (angular sweep, not segment intersection) with a full README: 190/190 agreement with the committed
   sibling over 2 270 boundary points, and an exceptional-set census over 51 587 exactly-decided
   points on 1 640 polygons in which the maximum exceptional count was 2 and 3 was never found. It is
   a concurrent lane and lands in its own PR; I included it as row A9 and added a snapshot-date note
   saying `attacks/` and `experiments/` are authoritative over the summary wherever they disagree.

The three other concurrent lanes named in the brief — `attacks/round2-cross-review/`,
`attacks/scalene-shapes/`, `attacks/exceptional-set-polygons/` — did not exist on disk when I wrote,
so nothing about them is represented. That is what the snapshot-date paragraph is for.

## Things I think are now wrong or misleading in the README, outside my lane to fix

1. **The top banner's unhedged headline is now in tension with the body twice over.** Line 3 says
   "Status: SOLVED in the literature" and the vertex-wise question is "settled too" — resting entirely
   on rows the same file declares unassumable. That was already flagged by the provenance warning, and
   I left it alone as instructed. But it now sits next to a section saying the *only* proofs this
   project can actually read are `sketch`. A human should decide whether the headline stays unhedged.
2. **`attacks/spiral-tip-witness/README.md` §12.2 is stale.** It says the rectifiable lane "records
   the open question of whether $\mathcal{H}^1$-a.e. point of a rectifiable Jordan curve is a vertex".
   That lane has since answered it affirmatively (Corollary T1). The two files were written
   concurrently, so this is expected, but the sentence now misdescribes a sibling file. Not my lane —
   it needs the spiral lane's owner or a dispatcher.
3. **The problem `RULES.md` §3.1 wedge-test section claims the witness supplies "a self-contained
   elementary proof of the sharpness row" (two exceptional points, attained).** It does supply
   sharpness, but only via `sketch` arguments now spread across three lanes; the README's row 3 is
   still `cited`\* with provenance P2. Whether the elementary route is enough to change row 3's status
   is a §5 question, and `RULES.md` is human-owned, so I did not touch it. Worth a human's eye,
   because it is the one row this repo may be able to discharge without network access.
4. **`results/` is empty and every lane's `target-status` line points at `verified:review`, which
   cannot be reached without Codex.** Nothing here can be promoted by a Claude worker of any size.
   The README now says `results/` is empty and correctly so; the bottleneck itself is a dispatch
   matter.
5. **Open item 5 ("Formalisation") is now understated.** The problem `RULES.md` §6.3 has a dated
   Mathlib check showing the Jordan curve theorem is absent, so a Lean formalisation of Meyerson is
   *not* a live target, while the wedge test, the rotation identity and the half-density measure core
   (`half-density-obstruction` §3.5 nominates exactly this) are. The README's item 5 predates that
   check. Correcting it means editing "What remains open", which is arguably in-lane; I left it
   because the brief scoped me to *adding* a section and told me not to rewrite the file, and because
   the correction depends on re-running the Mathlib check rather than quoting it.

## Checks run

- Read in full or in relevant part: repo `RULES.md` §0–§9, `problems/README.md`, this problem's
  `RULES.md`, all six `attacks/*/README.md`, `convex-vertex-criterion/{AUDIT,CROSS-REVIEW}.md`, both
  experiment READMEs, and the dispatch journal's synthesis section.
- Verified the synthesis against the two source files rather than the brief: Theorem T's exact
  statement and hypothesis (`rectifiable-case` §6.2), Corollary T3 (§6.4), and the spiral's Theorem 3
  (rectifiability, total length $2\sqrt{1+c^2}/c + \beta$, chord/arc ratio the constant
  $c/\sqrt{1+c^2} < 1$, non-differentiability by infinite winding) — they agree, and the
  non-collision reason is as the dispatcher described.
- Every relative link in the edited README resolves on disk (checked mechanically).
- No file outside my two was opened for writing; no git command was run.
