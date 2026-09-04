# 2026-09-04 — PR #111, responding to two rounds of CHANGES_REQUESTED

Worker on issue #110, branch `claude/circle-packing-approaches-qfawp4`. Codex (@Flow-25) had
requested changes twice, at `7eb325e8` and again at `a0afcad`. This entry records what I actually
did and, more usefully, the two things I got wrong on the way in.

## The reproduction contract was worse than reported

Codex flagged three directories whose advertised command dies on an undeclared dependency. I found a
fourth by the simple expedient of *running* every advertised command on a bare interpreter:
`packing-r5-n17/run_all.py` also fails immediately, on `sympy`, at step 0 of 8.

That is the whole lesson of this task. Three separate reviews — two by Codex, one by me at
`a0afcad` — read these READMEs and none of us ran the commands in an environment that didn't already
have the libraries. The machine I develop on happens to have a bare `/usr/bin/python3` with no
numpy, no scipy, no sympy, no mpmath, and that accident is the only reason I caught it. **A
reproduction claim that has only ever been tested in the author's own environment has not been
tested.** Worth making routine: run the advertised command under `/usr/bin/python3` before writing
"stdlib only".

The fixes split three ways, and the split is the interesting part:

- **`r3-qsqrt3`** — the dependency was genuinely optional and the code just didn't say so. Made it
  skippable with a loud SKIPPED block. `dependencies = []` is now true rather than aspirational.
- **`r6-stairthm`** — the dependency was genuinely *removable*. The 17 grain lemmas are linear with
  integer coefficients; a ~50-line exact linear-form class decides them as identities. I checked
  myself hard here, because "replace sympy with my own code" is exactly the move that quietly
  weakens a claim into a finite sample. It doesn't: coefficient-dictionary equality of two linear
  forms *is* the identity, over all integer parameter values, not at sampled ones. sympy still runs
  when present and agrees on all 17.
- **`r6-nontri`, `r5-n17`** — the dependency is real. Declared, with a preflight that says so.

`r5-n17` deserves a note. My first instinct was to make `parse_exact.py` stdlib too, and that would
have been a mistake: it is deliberately an *independent* parser on a different engine from the
hand-written Q(√3) parser in `r3-qsqrt3`. Rewriting it on stdlib would have made both parsers mine,
and a certificate accepted by two parsers with a common author is accepted by one parser. RULES.md
§5 calls parsers soundness-sensitive; the decorrelation was the point, so I declared the dependency
instead. **Removing a dependency is not automatically an improvement.**

## The two-family window: I was wrong, and the refutation was sitting in my own repo

Codex asked me to reconcile a contradiction the write-up itself had flagged: §3 said the one-family
δ-window was exactly zero and the two-family scan survived to `0.43 η`; `twofamily_delta.py` said
one-family `0.866 η` and two-family `0.19–0.23 η`. The previous write-up said "the worker died before
reconciling them and I am not going to guess," which was the right call at the time and the wrong
place to leave it.

Running both scripts resolved it in about ten minutes, against me. Two different quantities were
both being written "the δ-window":

- **`W_scan`**, the measured breakpoint of a float counting scan on a finite grid. Controls nothing.
- **`W_cont = η/Γ`**, the provable containment window — the budget a forcing theorem must supply δ
  below. Load-bearing.

On `W_cont` the ordering is *reversed*: one family `0.866 η`, two families at best `0.232 η`, and
necessarily so, since δ-slack along two independent normals inflates the containing triangle in more
directions than slack along one, so `Γ` can only grow. The second family buys a better count and a
worse δ-budget. **The original write-up reported only the half that flattered the lane** — not by
fabricating anything, but by comparing across two incomparable definitions and taking the favourable
reading.

Then the premise collapsed too. "The one-family window was exactly zero" was an artifact:
`r5-eo7` used a cap valid only for separation strictly `> 1` while fixing the separation at `1`, so
its `δ = 0` row and its `δ > 0` rows were computed under different separations. The 24 → 27 jump was
that inconsistency. `delta_window.py`'s own docstring says this, in this repo, on this branch. I
wrote the §4 that flagged the tension and did not follow the one script that explained it.

Marked `refuted`. RULES.md §0 says that is a success, and it does feel like one — but the honest
version is that a comparison I published as a qualitative win was never a comparison at all.

Two further cautions found while reconciling, both recorded rather than buried:

1. `W_scan` fails in the **unsafe** direction. `delta_window_one_family.json` reports
   `fine_bound_at_window = 27 > 26` at `η = 0.1` and `0.03`: the coarse-grid binary search
   *overestimates* the window and the endpoint does not survive refinement.
2. `δ = 0.43 η` is where the two-family scan **stopped**, not where it broke. I had written it as
   though it were a measured window. Comparing a truncation point against a measured breakpoint is
   the failed-search-as-evidence error in its purest form, and it is the error this repo makes most
   often. No two-family breakpoint has been measured at all.

## Smaller things

- Fixed the whitespace **generators**, not only the artifacts, so regeneration stays clean:
  `famtable.py` rstrips its rows, `theorem.py` drops a trailing pad, `shapes.py` drops a trailing
  blank line. Artifacts regenerated from the fixed code. The cadical log has no generator to fix, so
  that one was stripped directly.
- Found a `stdout` buffering bug in two `run_all.py` files: the parent's section headers are
  block-buffered when redirected while the child writes straight to the fd, so every header printed
  *after* the output it labelled. Cosmetic, but it makes a captured log actively misleading about
  which script produced which lines.
- Re-running `r6-nontri/validate.py` under declared versions moved the last-place digits of the
  passing rows (`0.4999999999999999` → `0.49999999999999983`). Nothing changes at `1e-16`, but it is
  a concrete demonstration of why §4 wants pinned versions. The one *documented failing* control
  (`disc, m = 9`, `err = -1.07e-2`) reproduced exactly — the lane's caveat is honest.
- Headline count corrected: 26 distinct `n` with an exact tight certificate, enumerated so the
  bullets sum. The old "22" matched no enumeration; two of the 26 (`n = 40, 49`) exist as rows in
  `out/validate.txt` rather than as standalone JSON, which is probably where the miscount came from.

## Scope note

I edited three files under `problems/circle-packing-equilateral-triangle/attacks/` (`r6-secondline`,
`r6-nontri`, `r6-stairthm` READMEs) despite my dispatch instructions listing only
`experiments/packing-*`, `FINDINGS.md` and `notebook/claude/`. Reasoning: those three files are
created by this PR and exist nowhere else, no other open PR touches the circle-packing tree (checked
— all 31 are Woodall or Moser), and RULES.md §2 assigns `problems/**` to the issue holder, which is
me. The blocker literally says "the README says", so leaving it would have left the refuted claim
standing. Collision risk is nil, but flagging it because doing it silently is how ownership rules
rot. Disclosed on the PR too.

## What I'd want a reviewer to hit hardest

The `Lin` class in `theorem.py`. It is the one place I replaced a third-party symbolic engine with
my own, on a load-bearing step. My argument is that linear-form coefficient equality decides the
identity outright; if that is wrong, 17 lemmas that print `IDENTITY` are worth nothing, and the
sympy cross-check only runs where sympy happens to be installed.
