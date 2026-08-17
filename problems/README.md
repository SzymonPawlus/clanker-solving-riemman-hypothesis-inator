# Problems

One directory per problem, named with a kebab-case slug (`riemann-hypothesis`,
`collatz-conjecture`, …). Everything here follows the same shape so that agents and humans can
move between problems without relearning the conventions.

Operating rules live in [`../RULES.md`](../RULES.md); the claim status taxonomy in particular is
defined there and applies identically across all problems.

## What we are actually doing

To be explicit: two LLM agents are not going to settle a famous open problem. The point of this
repo is to see how far a disciplined, machine-checked, multi-agent workflow gets on problems
where *every* shortcut is a lie — and to leave behind an honest record of what was tried.

Realistic wins, for any problem here:

- a classical lemma formalised end-to-end in Lean,
- a precisely stated argument that survives cross-examination by a different model family,
- a clean, reproducible numerical experiment,
- a correctly stated and sourced equivalence,
- a **documented refutation** of an approach we tried.

Those are the deliverables. A "proof" is not. Refutations are first-class output — write them up
as carefully as you would a success, because they are the part of this repo most likely to be
true.

## Required layout

```
problems/<slug>/
  README.md     statement, known landscape, and problem-specific notes
  attacks/      one directory per approach — the working surface
  results/      statements that reached `cited`, `verified:lean`, or `verified:review`
```

**`README.md`** states the problem precisely, and lists the load-bearing known results an agent
may assume, each with attribution. Do not add to that list without a citation, and do not treat
the list itself as verified in-repo — it is a reading aid pointing at the literature.

**`attacks/<approach-slug>/README.md`** records, for one approach: the idea, its current status,
the kill-criterion (what observation would make us abandon it), and what has been tried so far.
Attacks with a documented history of failure in the literature belong here marked `refuted` —
recorded so nobody retries them unchanged, not as inspiration.

**`results/`** is the only surface other work may cite. Every file here states its status in
front matter, and the status determines how much weight it can bear:

- `verified:lean` — `sorry`-free Lean in `lean/`. Strongest.
- `cited` — a literature reference.
- `verified:review` — cross-examined by an agent from a different model family (`RULES.md` §5).

Weaker statuses propagate: anything built on a `verified:review` claim is itself capped at
`verified:review`. Record `depends-on` so that cap stays checkable.

## Adding a new problem

1. Create `problems/<slug>/` with the three items above (`attacks/` and `results/` may start
   empty).
2. In the README, state the problem formally and populate the known-results table with citations
   *before* opening any attack issue — an attack proposed without knowing the landscape is
   usually a rediscovery.
3. Add an `area:<slug>` GitHub label so issues for it are filterable.
