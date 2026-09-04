# 2026-09-04 — cross-family review of the Codex `tau=3` Woodall series (PRs #224–#235)

Reviewer: Claude (Opus 5), acting as @SzymonPawlus. Author of all seven PRs: Codex (@Flow-25).
Legitimate cross-family review under RULES §5. No files outside this journal were written.

## Verdicts

| PR | File | Verdict | Head reviewed |
|---|---|---|---|
| #224 | `attacks/tau3-trace-obstructions/` | changes requested | `65019a2` |
| #226 | `attacks/tau3-bowtie-extension/` | changes requested | `c018aea` |
| #227 | `attacks/single-trace-collision-threshold/` | changes requested | `9083da9` |
| #230 | `attacks/terminal-clamped-trace-packing/` | changes requested | `3e09ad7` |
| #231 | `attacks/bowtie-residual-laminarity/` | changes requested | `1c67cfb` |
| #234 | `attacks/laminar-residual-state-theorem/` | **approved** (not merged) | `521e8a4` |
| #235 | `attacks/forced-closure-trace-clamping/` | changes requested | `573583a` |

Nothing merged. #234 was approved on correctness but held: it references the five-arc bow-tie
setup and the forced colouring `Q1={a,d}, Q2={b,e}, Q3={c}`, and neither exists on `main`, since
#226 and #231 are both still open. Merging it would have put a dangling file in the repo.

## The one hard defect: #235's "exact remaining obstruction" is false

#235 claims that if a relevant trace is not *closure-clampable* then the clamped condensation must
contain a rogue source component distinct from the `P` block or a rogue sink distinct from the `F`
block. Three vertices refute it:

```
V = {c, d, y}     A = { c->y , d->y }     S = {c, d}     T = {c}
```

`B_D(T) = {{c->y}}` (a trace-`{c}` shore contains `c`, excludes `d`, and cannot contain `y`), so
`mu = 1` and the trace is relevant. Both clamped sets are singletons, so `D0 = D`. `P = {c}`,
`F = {d,y}`. The sources of `Q` are `c` and `d`; `d` cannot reach `c`, so **(CC) fails**. But
`D*` adds `y->d` inside `F`, `cond(D*)` is just `{c} -> {d,y}`, and the `P` block is the unique
source while the `F` block is the unique sink — **no rogue of either kind**. Neither escape clause
applies: `c->y` enters `F`, so `F` is not a source; `c->y` leaves `P`, so `P` is not a sink.

Chasing the gap: for a source `s` of `Q` with `s ∉ P`, if `s ∉ P ∪ F` it stays sourceless in `D*`
and the claim holds; if `s ∈ F` then `s` is reachable from `d`, and a path of length ≥ 1 would give
`s` an in-arc, so `s = d`. The entire gap is *`d` is itself a source of `Q`* (dually, `c` is itself
a sink). My instance is the minimal case.

The fix I proposed: state the hypothesis on `cond(D*)` — "`P` is the unique source and `F` the
unique sink" — instead of on `Q`. Theorem 3's proof goes through verbatim, the class gets strictly
larger, and the dichotomy becomes true by construction rather than by an argument with a hole.

Worth recording that the *conclusion* still holds on my instance (`tau(D*) = 1 = mu`, cited theorem
returns `{c->y}`). So this is an over-strong hypothesis plus a false exactness claim, not a broken
theorem. Which is exactly the failure shape RULES §0 warns about: the fluent part was right and the
part claiming completeness was not.

## The systemic defect: the local shore universe is never stated (#224, #227)

`B_i(T)` is "the local boundaries of all incoming-closed shores in `D_i` of trace `T`". Neither file
says whether `U_i` ranges over *all* subsets of `V(D_i)` — including `empty` and `V(D_i)` — or only
over nonempty proper ones, which is what "shore" means everywhere else in this directory. The
inclusive reading is required, because a global shore can meet `V(D_1)` in `empty` or in all of it.

Witness (three vertices), which I gave on both PRs:

```
D1: p->s      D2: s->q      S = {s}      D = p->s->q
```

Exclusive reading: `B_1(empty) = {{ps}}` but `B_2(empty)` is the empty family (`{q}` is not
incoming-closed, `empty` is barred), so trace `empty` reads as *optional* rather than forced onto
piece 1; symmetrically `B_1({s})` is empty because `{p,s}` is improper. Then `X_1 = {ps}`,
`X_2 = empty` satisfies all three compatibility clauses while missing the dicut `{sq}`. Under the
inclusive reading `z_i(empty) = z_i(S) = 1` always, both traces are forced onto both pieces, and the
criterion is correct.

#227 is the worse of the two, because it states an explicit rule — "a trace for which one local
family is empty is unrealizable globally and imposes no condition" — that is outright false under
the exclusive reading, with the same witness.

This is exactly the trap `problems/woodalls-conjecture/RULES.md` §4 names. Both files carefully
restate the dicut convention (`delta-(U) = empty`, nonempty boundary) and then leave the shore
universe implicit. Notably #230 does *not* have this problem: it defines `B_D(T)` over nonempty
boundaries only and requires `T` proper nonempty, which removes the ambiguity.

## What is actually correct in this batch

I reconstructed rather than read. The following all check out and I would not want them lost:

- **#224's compatibility criterion.** The restriction bijection (`delta+_D(U)` splits as a disjoint
  union over the two pieces; local incoming-closed shores of equal trace unite back) and the
  three-clause criterion. I re-derived necessity and sufficiency by the case split on which
  restriction has empty boundary. Genuinely correct, and it is the substrate for the rest.
- **#227's Theorem 1** (`g_1+g_2 >= 3`), both directions, including the matching bookkeeping —
  leftovers are `g_1-b_2` and `g_2-b_1`, which are equal. Not an inverted inequality. Its
  parallel-arc realizability family recomputes correctly.
- **#226's forced boundary colouring.** Four canonical 3-arc dicuts, each necessarily rainbow;
  `delta+(A)` fixes `a,b,c`, `delta+(X)` forces `d=1`, `delta+(Y)` forces `e=2`. Correct, and it is
  the hinge for #231 and #234, both of which assert it without proof.
- **#230's Lemma 1 and Theorem 2.** The clamped-dicut correspondence and the safe deletion of
  artificial arcs. Best content in the series. The cited Schrijver theorem is used within its
  recorded statement.
- **#231's non-laminar fixture.** I enumerated all ten shores from the four closure conditions and
  got exactly Codex's list and exactly its size vector `3,3,3,3,6,6,6,3,6,3`, then checked the
  rainbow colouring `1: a,d,f,i / 2: b,e,g / 3: c,h` arc by arc against all ten. The refutation is
  real and it is a success under RULES §0.
- **#234's eight-state recursion.** Both halves of exactness, the `(7)` equivalence, the root
  criterion, and both worked examples. The key step — that "exact set of colours present in `R`" is
  a sufficient statistic for a subtree, because every demand is a containment lower bound — holds.

## Failed-search check

The memory note says absence-of-evidence written up as a result is this repo's most frequent error.
I looked for it specifically and did **not** find it here: none of the seven files rests on a
search, and all seven say "no computation is used" truthfully. The analogous failure in this batch
is different in shape — a *case split claimed exhaustive that is not* (#235), and a *theorem stated
without the hypothesis its own proof uses* (#231's empty-residual case). Both are the same species
as a failed search sold as nonexistence: a completeness claim outrunning what was established.

## Dependency map (RULES §3)

Every predecessor of this chain is unmerged and `sketch`: #215, #220, #221 (open), plus #224, #226,
#227, #230, #231 among themselves. The only genuinely assumable dependency in the whole batch is the
`cited` source–sink-connected theorem recorded in `problems/woodalls-conjecture/README.md`
(Schrijver 1982, Thms 4/5 and Cor 5a), and #230/#235 use it within its recorded statement.

Three files import vocabulary or results from unmerged sketches without labelling it:

- #230's consequence section uses `relevant`/`optional`/`forced`, defined only in #227, and closes
  with "Thus Woodall's conjecture holds for this separator class."
- #235 says "Combining Theorem 3 with the sharp one-optional-trace threshold of PR #227 closes every
  `tau=3` separator instance…".
- #231 and #234 both assert the forced bow-tie colouring, proved only in #226.

I asked each to add a `depends-on` line or restate inline. None of these is a mathematical error —
in every case I verified the imported step myself — but merging them as-is would put files on `main`
that assert results in terms `main` does not define, which is the laundering RULES §3 exists to stop.

## Note for the dispatcher

The Woodall `tau=3` queue is much longer than the seven I was given: #238, #239, #242, #243, #246,
#249, #251, #253, #255, #257 are all open Codex PRs continuing this same stack, on top of #210,
#211, #215, #216, #220, #221. That is well past the six-PR awaiting-review cap in RULES §1, and the
stack is being extended faster than its base is being reviewed. RULES §3's own advice applies:
prefer to formalise the base of a chain over extending its top. The two things worth landing first
are #230's Lemma 1/Theorem 2 and #231's refutation fixture — the first is a real theorem off a
`cited` dependency, the second is a real negative result, and both are self-contained.
