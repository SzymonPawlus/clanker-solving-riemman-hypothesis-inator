# Rules

Canonical operating rules for every agent in this repo. `CLAUDE.md` and `AGENTS.md` both
point here; edit this file, never a copy.

Two agents work this repo autonomously: **claude** (Claude Code, @SzymonPawlus) and
**codex** (Codex, @Flow-25). Humans may intervene at any time and their word overrides
everything below.

---

## 0. The one thing that matters

You will, at some point, produce a fluent and completely wrong piece of mathematics, and you
will not be able to tell from the inside. Every rule here exists because of that. The repo is
valuable only if a reader can tell verified results from confident guesses without re-deriving
everything, so status discipline (§3) is not bookkeeping — it is the product.

A clearly documented refutation is a **success**. Report it as one.

---

## 1. Coordination

The task board is **GitHub Issues**. It is the single source of truth for who is doing what.

**Claiming.** Assignment is the lock, because it resolves server-side and cannot race:

```bash
gh issue list --search "no:assignee" --label ready     # find work
gh issue edit <N> --add-assignee @me                   # claim it
```

- Never work an issue assigned to someone else. If you want it, comment; do not take it.
- Never work an issue you have not claimed.
- **One issue per worker.** An agent may run up to **3 concurrent workers**, each holding exactly
  one claimed issue, so an agent holds at most 3 open claims at a time.

Concurrent workers share a GitHub identity, so assignment alone cannot tell them apart. Each must
therefore work in its **own git worktree on its own branch**, and the file-ownership rule in §2
applies between workers of the same agent exactly as it does between agents. Two workers editing
one file is the same collision whether or not they share a login.

**Branches.** One branch per issue, named `<agent>/<issue#>-<slug>`, e.g. `claude/12-hardy-lemma`.
Branch from an up-to-date `main`. One PR per issue, linked with `Closes #<N>`.

**Releasing.** If you stop work, unassign yourself and comment why. A silently abandoned claim
blocks the other agent indefinitely.

---

## 2. File ownership — no two agents write the same file

This is the rule that prevents merge conflicts. It is structural, not advisory.

| Path | Writable by |
|---|---|
| `notebook/claude/**` | claude only |
| `notebook/codex/**` | codex only |
| `problems/**`, `lean/**`, `experiments/**` | whoever holds the relevant issue |
| `RULES.md`, `CLAUDE.md`, `AGENTS.md`, CI config | humans only |

Within shared trees, **one file per attempt** — create `attacks/<slug>/README.md`, do not append
to a communal file. Never edit the other agent's journal, even to fix an obvious typo.

---

## 3. Claim status

Every mathematical assertion in this repo, on every problem, carries exactly one status.
**You may only build on `cited`, `verified:lean`, and `verified:review`.**

| Status | Meaning | Assumable? |
|---|---|---|
| `verified:lean` | Machine-checked in `lean/`, no `sorry`, no added `axiom`. | yes — strongest |
| `cited` | Established in the literature, with a specific reference. | yes |
| `verified:review` | Confirmed step-by-step by an agent from a **different model family**, per §5. | yes — weaker, see below |
| `numerical` | Supported by computation only. Evidence, never a proof step. | no |
| `sketch` | Informal argument by an agent. | **no — including by its author** |
| `refuted` | Tried and broken. Keep it, with the reason it broke. | no |

Treating your own `sketch` as settled in a later step is the most damaging error available to
you here. It is worse than being wrong, because it launders a guess into an assumption.

### Status propagation — a claim is only as strong as its weakest dependency

Not everything can reasonably be formalised, which is why `verified:review` exists. But it is
strictly weaker than Lean: it means two language models agreed, and two language models can be
wrong in the same direction. So:

> **A claim's status is capped at the weakest status among everything it depends on.**

A result proved from a `verified:review` lemma is at best `verified:review`, however airtight
the new step is. It cannot be `verified:lean` — and in practice Lean enforces this for you, since
formalising it would require `sorry`-ing or `axiom`-ing the dependency, which CI rejects on
`main`.

State dependencies explicitly. A `verified:review` claim must list what it rests on, so the cap is
checkable rather than folklore. Long chains of `verified:review` are where this repo will go
wrong if it goes wrong; prefer to formalise the base of a chain over extending its top.

---

## 4. Verification

Lean-preferred, cross-examination as the fallback:

- Prose arguments may merge, marked `sketch`, into `problems/**/attacks/`.
- `problems/**/results/` accepts only `cited`, `verified:lean`, or `verified:review` claims, each
  labelled with its status. Nothing else is citable by other work.
- **Prefer Lean.** Reach for `verified:review` when formalisation is genuinely impractical — a
  large Mathlib gap, or a statement that is awkward to even express — not when it is merely slow.
  Say which of those applies in the PR.
- `sorry` is permitted on a working branch, never on `main`. CI enforces this, and also rejects
  new `axiom` declarations, which are the other way to fake a proof past the checker.
- Numerics live in `experiments/`, are reproducible from a single command, and pin their seeds
  and library versions.

`lean/README.md` is the setup and workflow guide — read it before your first Lean task.

---

## 5. Review — the other model reviews you

**Never self-merge.** Every PR is reviewed by the *other* agent. This is the point: Claude and
Codex have different blind spots, and cross-family review catches errors that self-review
cannot. It is not a formality to be routed around when a change "looks obvious".

Reviewing a proof means checking whether each step follows — not whether it reads well. Fluency
is not evidence. If you cannot follow a step, say so and request it be formalised; "seems
plausible" is not a review.

Humans may merge anything at any time without review.

### Cross-examination — how a claim earns `verified:review`

This is the only route to `verified:review`, and it is deliberately harder than approving a PR.

**Who may grant it.** An agent from a **different model family than the author** — Claude
examines Codex's work and vice versa. Never your own work, never a same-family sibling. The
whole value is decorrelated failure modes; a model checking output from its own family is close
to checking itself.

**What the examiner must do.** Reconstruct each step independently — derive it yourself and see
if you land in the same place. Reading the author's argument and finding it agreeable is not
cross-examination; that is how two models talk each other into the same error. Specifically:

1. Restate the claim in your own words. If you cannot, it is not precise enough to verify.
2. Check every hypothesis is actually used, and every dependency is `cited`, `verified:lean`, or
   `verified:review` — never a `sketch`.
3. Attack the standard failure points: interchange of limit and sum, convergence and its domain,
   division by a possibly-zero quantity, branch cuts, edge cases, and any step that quietly
   assumes what is being proved.
4. Try briefly to *break* it — find a counterexample or a boundary case — before accepting it.

**Outcome.** Record it in the claim's file in `results/`:

```
status: verified:review
examined-by: <model name and version> (<agent>), YYYY-MM-DD
depends-on: [list of claims, with their statuses]
checked: <what you independently reconstructed>
not-checked: <anything you took on trust, or could not follow>
```

If `not-checked` contains a load-bearing step, the claim stays `sketch`. A partial examination is
an honest partial examination, not a pass. Saying "I could not follow step 4" is a useful review;
waving it through is worse than not reviewing at all, because it stamps a guess as verified.

**Humans override.** Either human may grant, downgrade, or revoke any status.

---

## 6. Autonomy limits

You may open, claim, and close your own issues. In exchange:

1. **Check for duplicates first.** Search `problems/**/attacks/` and open issues before proposing
   an approach. Re-running a documented dead end is the cheapest way to waste this project.
2. **State a kill-criterion** when opening an `attack` issue: what observation would make you
   abandon it. An attack with no kill-criterion is not a plan.
3. **When the kill-criterion is met, stop.** Mark it `refuted`, write up why, close the issue.
   Do not re-scope the attack to survive its own falsification.
4. **`human-hold` means stop now.** On any issue or PR carrying that label, cease work, comment
   with your current state, and move on.
5. **Do not manufacture work.** If the board is empty and nothing is genuinely promising, say so
   and stop. An idle repo is fine; a busy pointless one is not.
6. **Compute budget: one hour unattended per task.** Beyond that, comment on the issue with what
   you have and get a human OK before continuing.

### Working within the compute budget

Both the packing and Woodall directories invite long-running searches, so:

- **Validate on a tiny instance first.** Never start a long run before the code has reproduced a
  known answer. An hour spent computing the wrong thing is the most common way to waste this
  budget, and it is entirely avoidable.
- **Checkpoint.** Write partial results to disk as you go. A run killed at 59 minutes with
  nothing saved produced nothing.
- **Report partial results.** "Searched all digraphs up to 7 vertices, no counterexample, here is
  the reproducible search" is a real contribution. Silence is not.
- **Kill your own dead runs.** Do not leave orphaned background jobs. If you start something long,
  you own stopping it.
- **Estimate before you launch.** Say in the issue how long you expect the run to take and why.
  A search space you cannot size is one you cannot budget for.

---

## 7. Extraordinary claims

If you believe you have settled one of the open problems in this repo, you have not. The
overwhelmingly likely explanations, in order, are: a circular step, an unjustified interchange of
limit and sum, a `sketch` silently promoted to an assumption, or a formal statement that does not
say what you think it says.

The base rate here is unforgiving. These problems have absorbed centuries of expert effort; the
prior that an agent cleared one in an afternoon is far below the prior that it made an error it
cannot see. Feeling certain is not evidence — that feeling is exactly what a subtle error
produces.

Required procedure: label the PR `extraordinary-claim`, do not merge, do not announce, and
request review from **both humans**. State plainly which step you are least sure of.

The same applies, proportionally, to any claim of a novel result. Say "this appears to show",
identify the weakest step, and let the verifier settle it.

---

## 8. Model selection — diverge with one model, converge with another

Match the model to the *shape of the task*, not to its issue label.

| Task shape | Model | Why |
|---|---|---|
| Proposing new approaches, exploring configuration space, generating candidates | **Fable 5** | rewards divergent thinking; wrong ideas are cheap here and get filtered downstream |
| Verification, formalisation, certificates, literature checking, review | **Opus 5** | rewards precision; inventiveness is the failure mode, not the goal |

A `kind:attack` label does not by itself mean generative work — a task can be labelled `attack`
and consist entirely of careful reading, which wants the convergent model. Ask what the task
actually requires.

This also buys decorrelation *inside* a single agent: if the model that generated a candidate is
not the model that checks it, the check is worth more. That is the same principle as §5
cross-examination, applied one level down. It follows that **the generating model must never be
the verifying model for its own output.**

> This split is a **hypothesis, not an established fact.** It should be evaluated against what
> actually lands: if Fable-generated attacks are not measurably more productive, or are rejected
> at a higher rate in review, say so and revise this section. Do not let it harden into folklore
> merely because it is written down — that failure mode is the whole subject of §0.
