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
- **One issue per worker.** An agent may run up to **3 active workers**, each holding exactly one
  claimed issue. A claim is *active* while implementation, computation, or revision is underway.
  A completed PR waiting only for the other model's review is an *awaiting-review claim* and does
  not consume an active-worker slot. An agent may have at most **6 open awaiting-review PRs**;
  when that queue is full, review backlog must shrink before the agent starts more work. Every PR
  must link its claimed issue; an unlinked PR still counts toward the cap and is a protocol error.
  The **review lane** of §9.4 is a fourth worker that sits *outside* this count; it runs review and
  review-driven work only, never new research. Its exclusion is defined by a **board marker, not by
  intent**: a claim is excluded from the 3-slot count exactly when its issue carries the
  `review-lane` label, and at most one open issue may carry that label at a time. So a legal
  allocation always reads off the board as *at most three `active-work` issues without
  `review-lane`, plus at most one with it*; four `active-work` issues none of which carries
  `review-lane` is a cap violation that anyone can see without asking what the dispatcher meant.

**Claim state transitions.** Use the issue labels `active-work` and `awaiting-review` so the board
records the distinction rather than keeping it in an agent's memory:

1. On claim, add `active-work` and remove `awaiting-review`.
2. After pushing a complete PR and requesting the required review, remove `active-work`, add
   `awaiting-review`, and keep the issue assigned. The open PR continues to lock every file it
   changes.
3. **Any push** to an awaiting-review PR requires first removing `awaiting-review` and reactivating
   the claim by adding `active-work`. The same transition is required when review requests changes.
   Which slot the reactivated claim occupies is then decided by exactly one of these two cases, and
   the labels say which:

   - **Normal slot — the default, and the only case unless the labels say otherwise.** Add
     `active-work` alone. **If all 3 active slots are occupied, finish or release one first**;
     review feedback has priority over new work.
   - **Review lane (§9.4) — the sole exception.** Available only when the push applies *requested
     changes* that qualify as **small** under §9.4 *and* no open issue currently carries
     `review-lane`. Add `active-work` **and** `review-lane`. This claim is then outside the 3-slot
     count, so the push proceeds **with all three normal slots still occupied** and nothing need be
     finished or released.

   The `review-lane` label is what makes the exception legal: a reactivated claim that does not
   carry it is governed by the normal-slot case whatever the dispatcher intended, and a lane fix
   that turns out not to be small must remove `review-lane` and take a normal slot under the first
   case (finishing or releasing one if all three are occupied). Remove `review-lane` whenever the
   claim leaves the lane — on return to `awaiting-review` (transition 2), on merge or closure
   (transition 4), or on the reclassification just described. The lane is free again only once no
   open issue carries the label.

   **Reviewing** another agent's PR and **merging** one create no author claim of ours, so they
   require no issue transition and no label at all; they are lane-eligible without touching the
   board.
4. On merge/closure, remove all three lifecycle labels (`active-work`, `awaiting-review`,
   `review-lane`). If a PR is abandoned, unassign the issue and explain why.

Labels are bookkeeping, not authority: a PR with unfinished work cannot be moved to
`awaiting-review` merely to evade the active limit, and `review-lane` on work that is not a small
requested-change fix is a cap violation dressed as a label, not a fourth slot. Conversely, an
unavailable reviewer must not freeze all research once complete review-ready PRs are honestly
queued.

Concurrent workers share a GitHub identity, so assignment alone cannot tell them apart. Each must
therefore work in its **own git worktree on its own branch**, and the file-ownership rule in §2
applies between workers of the same agent exactly as it does between agents. Two workers editing
one file is the same collision whether or not they share a login.

**Branches and PRs.** One branch and one PR per issue. `main` rejects ordinary direct pushes, so a
PR is the normal route in. The review gates in §5 are primarily **social policy**, not complete
mechanical enforcement: current branch protection does not require an approving review and does
not enforce rules for administrators. It does block force-push/deletion, dismisses stale formal
reviews, and requires conversation resolution. Never infer that an action is permitted merely
because GitHub's merge button allows it. The full sequence:

```bash
git checkout main && git pull            # branch from an up-to-date main
git checkout -b <agent>/<issue#>-<slug>  # e.g. codex/12-dicut-enumeration

# ... do the work, commit ...

git push -u origin <agent>/<issue#>-<slug>   # -u is required the first time
gh pr create --fill --body "Closes #<N>

<what you did, what to review hardest, what you are least sure of>"
gh pr edit <PR#> --add-reviewer <other-agent's-github-user>
```

Then move the issue to `awaiting-review` and refill the active slot if both queue caps permit.
**Do not merge your own PR.** Record its tier in the PR body and with exactly one of the labels
`tier:verification-critical` or `tier:non-claim`; merge authority is determined by §5.
Do not push to `main` — it will be rejected, and if you have admin rights it will warn about
bypassing rules, which is not yours to do. Merge authority is determined by §5.

**If this fails, the cause is almost always one of:**

| Symptom | Cause |
|---|---|
| `gh: command not found` | GitHub CLI not installed |
| `gh auth status` shows logged out | run `gh auth login`; needs the `repo` scope |
| `Permission denied (publickey)` on push | SSH key not registered, or use HTTPS instead |
| `remote: Permission to ... denied` | not a collaborator on the repo — ask a human |
| `pull request create failed: no commits between...` | you forgot to commit, or pushed the wrong branch |
| `Changes must be made through a pull request` | you tried to push to `main` as a non-admin; an admin may not receive this protection and must still not bypass policy |

If you cannot open a PR at all, **say so explicitly rather than doing the work and dropping it**.
Push the branch and comment the branch name on the issue — a human can open the PR. Silently
abandoning finished work is the worst outcome here, and it looks identical to having done
nothing.

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

Cross-family review remains mandatory whenever a PR creates or changes an assumable mathematical
claim (`cited`, `verified:review`, or `verified:lean`), touches `problems/**/results/`, changes
verification policy, or makes a novel/extraordinary claim. Claude and Codex have different blind
spots; this gate is not a formality to route around when a change "looks obvious".

To keep infrastructure moving when the other family is unavailable, PRs are divided into two
integration tiers:

| Tier | Scope | Merge gate |
|---|---|---|
| **verification-critical** | literature/citation work; assumable claims or status promotion; any change under `problems/**/results/` (including `numerical` files); proof dependencies; policy/CI; extraordinary claims; security- or soundness-sensitive tooling (parsers, verifiers, certificate acceptance) | formal approval by the other model family or a human; `verified:lean` also requires clean Lean CI with no `sorry`/new `axiom` |
| **non-claim** | `sketch` attacks, explicitly `numerical` experiments outside `results/`, ordinary tooling, generated data, and editorial changes, **provided the PR does not establish, alter, or rely upon an assumable claim** (`cited`, `verified:review`, `verified:lean`) | the exceptional same-agent audit procedure below, or a human review |

Same-family audit may integrate a **non-claim** PR but can never grant `verified:review`, promote a
claim into `results/`, or turn `numerical`/`sketch` evidence into an assumable dependency. If scope
is mixed or uncertain, use the verification-critical tier. Splitting a PR to evade the stronger
gate is forbidden.

Approval is tied to the reviewed commit. **Any push** after approval or audit invalidates it and
requires a fresh review at the new head. Before merging, recheck `human-hold`, head
SHA, changed-file scope, mergeability, and required tests; a stale approval is no approval.

**Exceptional same-agent audit for non-claim PRs.** This path is available only after cross-family
review was formally requested and either (a) 24 hours elapsed without a review, or (b) that
author's six-PR awaiting-review queue is full. The PR body and `tier:non-claim` label must make the
classification visible. The auditor must be a separate worker and worktree, must not be the
dispatcher or authoring worker, and must use a different model from the one that produced the
change, following §8. Before merge it records a PR comment containing:

- the condition, (a) or (b), that enabled the exceptional path;
- the exact audited head SHA, auditor model, worktree/branch, and changed-file scope;
- what was independently reconstructed or reimplemented, not merely rerun;
- tests and limitations, plus confirmation of no `human-hold`.

Because workers of one agent share a GitHub account, this comment is the audit artifact; GitHub
will not accept it as a formal approval. The auditing worker may merge only the exact commented
SHA. For computational content, the relevant problem `RULES.md` sets the audit standard and
normally requires an independent checker; rerunning the author's script is insufficient.

A later verification-critical review examines the complete claim and every dependency as they
exist on `main`, not merely the new PR diff. Content previously merged through the non-claim tier
carries no verification credit and must be independently reconstructed.

Reviewing a proof means checking whether each step follows — not whether it reads well. Fluency
is not evidence. If you cannot follow a step, say so and request it be formalised; "seems
plausible" is not a review.

Humans may merge anything at any time without review.

### Recording cross-family review versus exceptional audit

For verification-critical work, a comment is not an approval. Record a formal review:

```bash
gh pr review <N> --approve         --body "..."   # or
gh pr review <N> --request-changes --body "..."
```

If `gh pr review` fails (its GraphQL endpoint has been flaky), use the REST route:

```bash
gh api -X POST repos/<owner>/<repo>/pulls/<N>/reviews \
  -f event=APPROVE -f body="..."
```

For the exceptional same-agent non-claim path, GitHub refuses formal approval from the shared
author account, so the structured exact-SHA comment specified above is intentionally the record.
This exception does not satisfy a cross-family review requirement.

**What is forbidden is reviewing or merging your *own* work — not approving the other agent's.**
Approving their PR is the entire point of cross-review; withholding the formal approval does not
make you careful, it just blocks the queue while looking like diligence.

**Who merges.** Verification-critical PRs are merged by the cross-family reviewer or a human,
never the author. Non-claim PRs may be merged by the independent auditing worker or a human; the
author still does not audit its own output. A human may explicitly override either rule.

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
| **Ideation** — proposing approaches, exploring configuration space, generating candidates | **Fable 5** | rewards divergent thinking; wrong ideas are cheap here and get filtered downstream |
| **Administration** — board management, issue triage, scoping, docs | **Opus 5** | wants consistency, not novelty |
| **Calculation and simple transformation** — numerics, format conversion, certificate generation | **Opus 5** | wants exactness; a creative arithmetic step is just an error |
| **Verification** — formalisation, checking, literature, review | **Opus 5** | inventiveness is the failure mode here, not the goal |

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

---

## 9. Orchestration — running the worker pool

An agent that dispatches workers follows these. They govern *what to run next*, and the ordering
is deliberate.

### 9.1 Review before own work

**A PR awaiting your cross-examination outranks starting anything new.** When a slot frees, check
for reviewable PRs *first*; only if there are none do you pick up a task.

An unreviewed PR blocks its author, blocks every issue touching the same files, and grows stale
against a moving `main` — so the queue costs more the longer it sits. Producing more unreviewed
work while a review is outstanding makes the pile worse, not the project faster. Review precedence
applies **across problems**: a pending review on any problem outranks new work on the one you were
focused on today.

For cross-family review, "reviewable" means PRs authored by the *other* agent. Same-agent
non-claim audit is the narrow exception in §5 and follows its delay/queue precondition. If neither
kind is eligible, say so rather than inventing a review.

### 9.2 Slot cycling

Run up to **3 active workers**, one issue each (§1), independently of the bounded awaiting-review
queue and of the review lane (§9.4). When a worker produces a complete review-ready PR, move that claim to `awaiting-review`
and refill the active slot immediately in this order:

1. **A PR to cross-review** (§9.1).
2. **An eligible non-claim PR for exceptional audit** (§5), after cross-review work.
3. **Requested changes** on an awaiting-review PR; reactivate its issue first (§1 transition 3 —
   a *small* fix may instead go to the review lane, §9.4).
4. **A `ready` issue** whose files are not locked by an open PR. Check that — dispatching a worker
   onto a file some open PR already rewrites guarantees a conflict.
5. **Ideation.** If nothing is ready and unblocked, dispatch a Fable worker to generate and triage
   new approaches (§8), which refills the board.

Do not open a seventh awaiting-review PR. At that point all active capacity goes to reviews,
review feedback, conflict repair, or tasks that can land without adding to that queue.

Idling is better than manufacturing work (§6.5), but genuine ideation is not manufactured work —
an empty board is itself a signal that the next approach has not been thought of yet.

### 9.3 Dispatch hygiene

Before dispatching, confirm the new worker's files are disjoint from every running worker *and*
every open PR. State the ownership boundary explicitly in the worker's instructions — do not
assume it will infer one. Each worker gets its own worktree and branch (§1); §9.4 states how a
review-lane worker satisfies that when it must update an existing branch.

### 9.4 The review lane — a dedicated fourth slot

A fourth worker slot exists **in addition to** the three active slots of §9.2, reserved for keeping
the review queue moving. It never runs new research.

Eligible work, and nothing else:

1. **Cross-family review** of a PR by the other agent (§5).
2. **Applying requested changes** to one of our own PRs, when the change is *small* — see below.
3. **Merging a PR we reviewed and approved**, plus the board bookkeeping §1 requires.

Reviews are lane-eligible **regardless of size**. A long review occupying the lane is still the
lane doing its job; bouncing it to a normal slot would recreate the bottleneck the lane exists to
remove. The *small* test below therefore gates only case 2, applying requested changes.

**Small** means: confined to files the PR already touches, introducing no new argument or
computation, and finishable well inside the §6.6 budget — a citation locator, a wrong volume
number, a status or label correction, wording a review named explicitly, metadata a review asked to
reconcile. A rework is **not** small if it needs a new derivation, a new experiment, a re-run, a
rebase onto a moved `main`, or a judgement call about what the claim should now say. **When
uncertain, use a normal §9.2 slot** — the same default-to-strict rule as §5's tiers.

The lane runs one worker at a time, like any other slot.

**Board bookkeeping — the lane must be visible, not remembered.** The board is the single source of
truth (§1), so an allocation of 3+1 has to be distinguishable from a cap violation by looking at it:

- A lane fix (case 2) reactivates an existing claim under §1 transition 3 and its issue carries
  **`active-work` *and* `review-lane`** for exactly as long as the fix is in progress. `review-lane`
  goes on when the fix starts and comes off the moment the claim returns to `awaiting-review`, is
  merged, closed, or is reclassified as not-small.
- **At most one open issue may carry `review-lane`.** That label is therefore both the lane's
  occupancy signal and the thing that excludes the claim from the 3-slot count — the exclusion is
  defined by the marker, never by the dispatcher's intent. Before dispatching a lane fix, check
  `gh issue list --label review-lane --state open` and require it to be empty.
- Cases 1 and 3 — reviewing another agent's PR, and merging one we reviewed — create **no author
  claim**, so they need **no issue transition and no label**. Nothing on the board changes. The
  one-worker-at-a-time rule still binds the dispatcher, but a slip there cannot corrupt the active
  count, because claimless work is never counted in the first place.
- A dispatcher auditing the board asks only: are there at most three `active-work` issues without
  `review-lane`, and at most one with it? If not, the cap is breached and the excess must be
  released before anything new starts.

**Worktree and branch for a lane fix.** A small fix updates the **existing** PR, so it inherits that
claim's one branch and one PR (§1). It must **not** open a second branch, a second PR, or a
same-branch duplicate checkout:

- The lane worker takes **exclusive** use of the dormant worktree that already holds that branch, or
  a replacement worktree explicitly handed over to it. Dormant is guaranteed, not hoped for: a claim
  sitting at `awaiting-review` has no running worker by definition, and the label transitions above
  make that checkable.
- **Expect `git worktree add` to refuse a second checkout of a branch already checked out
  elsewhere.** Reusing the existing worktree is the intended path, not a workaround; that refusal is
  the rule working. Do not defeat it with `--force`, a detached checkout, or a `-2` branch name.
- **Never share a worktree concurrently** with another worker. Exclusive means the lane worker is
  the only one in it for the duration; if the original worker is somehow still live there, the fix
  waits or takes a normal slot.
- Cases 1 and 3 do not touch a branch of ours: a review may check out the *other* agent's branch in
  a fresh worktree of its own, and a merge is performed through `gh` against the remote.

**Anti-evasion.** A spare slot is exactly the kind of thing that gets borrowed, so:

- It may never be used to start a `ready` issue, ideation, or anything that would otherwise queue
  for §9.2. Work does not become eligible because the lane happens to be idle. `review-lane` on an
  issue whose PR is not already awaiting review is a protocol error on its face — the label is only
  ever added to a claim being reactivated from `awaiting-review` under §1 transition 3.
- Splitting a large rework into "small" pieces to fit the lane is forbidden, exactly as §5 forbids
  splitting a mixed PR to evade the stronger tier. Smallness is judged against the **whole** set of
  changes the review asked for, not against the slice a worker chooses to push first; and since the
  lane holds one claim at a time and the fix reuses the claim's single branch and PR, serialising a
  large rework through it is neither faster nor permitted.
- The lane changes *scheduling only*. Everything in §2 (file ownership), §3 (status), §5 (who may
  review, grant, and merge) and §9.3 (dispatch hygiene) applies unchanged. Speed is the point;
  a lower bar is not. In particular the lane never grants `verified:review`.
- An idle lane is fine — it is a dedicated lane, not a quota to fill (§6.5).

**Why this exists.** Review throughput, not research capacity, is the binding constraint. Under
§9.2 alone a review competes with multi-hour experiments for the same three slots, and since a
running worker is not preempted, §9.1's review precedence silently degrades into "review next time
a slot happens to free". An approved PR then sits unmerged, which blocks its author, blocks every
issue touching the same files, and pushes the other agent into work it would not otherwise take.
