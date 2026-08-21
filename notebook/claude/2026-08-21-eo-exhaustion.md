# 2026-08-21 — Erdős–Oler $k=7$ by exhaustion: measuring the wall

Role: numerical analyst on the Erdős–Oler $k = 7$ push (27 points at separation $\ge 1$ in side
$a < 6$; separation-2: $d(27) \ge 12$). Files I own this session:
`experiments/packing-eo-exhaustion/`, `problems/circle-packing-equilateral-triangle/attacks/eo-exhaustion/`,
this journal entry. No git commands run, no issues or PRs touched.

## What I picked and why

Three candidate targets were on the table. I picked **(1) validate the pipeline and measure the
true wall**, but on the *right family* — $n = T(k)-1$, which is what Erdős–Oler is actually about —
and against the *right baseline*, which is Oler's own closed form and not zero.

Reason for not picking (2), structure-aware exhaustion: I worked out on paper, before writing code,
that the obvious structure-aware pruning family (partition into regions, cap each by Oler, add up)
is **provably worse than global Oler for every partition**, by exactly $I + (m-1)$ where $I$ is the
internal cut length and $m$ the number of pieces (attack write-up §3.1). Since the deficit to
recover at $n = T(k)-1$ is exactly 1, any partition into $\ge 2$ pieces overspends the entire
budget. That is ten minutes of algebra rather than an hour of compute, and it is written down so
nobody re-derives it.

> **CORRECTED 2026-08-21.** The paragraph above originally ended "That killed the family", and I
> then wrote the same over-broad reading into the attack file and the experiment README, from where
> the manager propagated it and two theory routes were dropped on it. **The lemma is right; the
> corollary is false.** It kills *Oler-per-piece-then-sum*. It does **not** kill
> *true-capacity-per-piece-then-sum*, because Oler's bound on a small piece is far slacker than the
> piece's true capacity. The counterexample was already in my own write-up two sections earlier and
> I did not connect them: at $a = 1.999$, Oler on the whole triangle gives $n \le 5.9965$ and does
> not exclude 5 points, while four level-1 cells of side $0.9995 < 1$ hold one point each and give
> $n \le 4$, which does. That partition **beats Oler by nearly two points** and is how the only
> complete Erdős–Oler case in this repo ($k=3$) is proved — including by my own prover, in one
> node. Caught by an independent verifier, not by me. See attack write-up §3.2/§3.3.
>
> The lesson I want to keep: I proved a lemma about $\Omega(P_i)$ and then stated a corollary about
> *capacity*, which is a different quantity, and the substitution felt so natural that I never
> wrote the two symbols next to each other. My own code (`caps.py` takes a `min` over three caps,
> of which the diameter cap is exactly the live move) contradicted the corollary the whole time.

The one structure-aware rule that survives that objection is Oler applied to the *configuration's
own hull* — one $+1$, no internal cuts — so I implemented that as a per-node rule and measured it.

## The thing I want the team to read

**A finite exhaustion at rational side lengths cannot prove Erdős–Oler at any $k$.** Not a budget
problem. Refuting $n$ points at one rational $d$ gives $d(n) > d$; the conjecture needs refutation
at *every* $d < 2(k-1)$, and the configuration space at $d = 2(k-1)$ exactly is non-empty (delete a
point from the lattice packing), so the nested family of refutations has non-empty limit. There is
no limiting run. Equivalently: the conjecture says a maximum *is attained* at exactly 2, which is a
closed condition, and exhaustion refutes open ones.

> **CORRECTED 2026-08-21.** The justification above is **wrong** and the claim is over-scoped;
> refuted by an independent verifier. The sets $S(\varepsilon)$ are *decreasing* in $\varepsilon$,
> so $\bigcap_{\varepsilon>0} S(\varepsilon)$ is not an $\varepsilon \to 0$ limit and is **empty**,
> not $S(0)$ — at $k = 3$, where $d(5) = 4$, every $S(\varepsilon)$ with $\varepsilon>0$ is empty
> while $S(0)$ is not.
>
> The narrow conclusion survives on plain **monotonicity**: feasibility is monotone in $d$, so
> finitely many refutations at rationals $d_1..d_N < D$ collapse to $d(n) > \max_i d_i$, and a max
> of finitely many rationals each $< D$ is $< D$. So *fixed-rational-side refutation used alone*
> never reaches $d(n) \ge D$.
>
> The broad claim "no exhaustion at any $k$" is **not** established and I should not have written
> it. It excludes neither (a) a finite argument uniform in $d$ — my own $k \le 3$ case is one, and
> it proves the conjecture at $k=3$ outright — nor (b) exhaustion plus a gap/rigidity theorem, for
> which my measured wall is exactly the relevant cost data. See attack write-up §1.1–§1.3.

I wrote this at the top of both the experiment README and the attack, because the whole session
could otherwise have been spent buying orders of magnitude toward something unreachable.

## What ran

Wrote `eoex` from the problem statement — deliberately *not* adapted from
`experiments/circle-packing-bnb`, since problem `RULES.md` §3 makes the independent
reimplementation the unit of verification here. Exact integer pair tests
($p^2(a^2+ab+b^2) \ge 4q^2 4^L$), exact rational capacities, exact rational area in the Oler-hull
rule with outward-rounded rational upper bounds on the only surds (edge lengths). No float decides
anything.

13 checks pass. The one I care about is
`test_known_packings_survive_every_rule_at_every_level`: no rule may fire on the cells of the
actual optimal lattice packings $n = 3,6,10,15,21$ at levels 0–6. At those configurations Oler is
*exactly* tight, so the hull rule's margin is exactly zero — if the normalisation (separation 1 vs
separation 2, the factor of 2 the brief warned about) were wrong by any amount, that test fails
loudly in one direction or the other. It passes.

Measured (each `proved` row is a real finite exhaustion; every `timeout` proves nothing):

| $k$ | $n$ | Oler alone certifies $\rho$ | exhaustion proved | $\rho$ | beats Oler? |
|---|---|---|---|---|---|
| 3 | 5 | 0.851 | every $d<4$, uniformly — case settled | 1 | yes |
| 4 | 9 | 0.924 | $d > 5.9$ (684 k nodes, 12 s) | 0.983 | yes |
| 5 | 14 | 0.954 | $d > 7.99$ (4.2 M nodes, 98 s) | 0.99875 | yes |
| 6 | 20 | 0.969 | nothing — timeout at $d = 9.7$, 8.4 M nodes, 400 s | — | **no** |
| 7 | 27 | 0.978 | nothing — timeout at $d = 11.74$, 13.2 M nodes, 400 s | — | **no** |

**The wall sits between $k=5$ and $k=6$.** Below it the exhaustion is strictly stronger than
Oler's free closed form; at $k=6,7$ Oler is strictly stronger than everything the exhaustion
produced, and those rows prove nothing. Seven attempts at $k=6,7$ spanning $d = 9.7$–$9.75$ and
$11.74$–$11.75$, up to 400 s and $1.3\times10^7$ nodes each, all timed out with a non-empty
frontier. Total compute for the session: about 55 minutes wall on a 4-core box, roughly 2.5
CPU-hours; every run was time-limited in advance and reaped, no background job outlived the
session.

Kill-criterion, written before launching: *if $k=5$ cannot beat $\rho_{\text{Oler}}$ in 7 minutes
single-core, stop escalating.* It did not fire — $k=5$ cleared it in 40 s.

## Two things I got wrong or nearly wrong

1. **First arithmetic pass on Oler at $n=16$ gave $d(16) > 8$**, which would have been "no better
   than free". I had mis-solved the quadratic. Correct value $\sqrt{129}-3 = 8.3578$, which is
   *stronger* than the $d(16) > 7.999$ the repo's existing B&B spent CPU-hours on. Lesson recorded
   in the experiment README §1: always print the closed-form baseline before starting a search.
   (The value itself was already in `attacks/oler-lower-bound/` §2.3 — I re-derived it rather than
   reading it, which is how I caught my own slip, but it also means I should have read first.)
2. **The Oler-hull rule as first written was a net loss.** Ablation at $n=14$, $d=7.8$: with the
   rule at every node, 556 592 nodes / 64 s; with it off, 720 946 nodes / 14 s. It removes ~23 % of
   nodes and costs ~6× per node. Fixed by restricting it to shallow nodes (default: cells at level
   $\le 3$), which is sound because narrowing where a pruning rule fires can only lose pruning.
   The root application stays unconditional so no run can be weaker than Oler. I would not have
   found this without measuring; the rule *looked* obviously good.

## What I did not do

- No attempt at an optimality proof, and no certificate written to `results/`.
- Did not implement checkpoint *resume*. The frontier is written to the output JSON on timeout, so
  a killed run leaves a record, but I did not build the validated resume path that
  `circle-packing-bnb` has — its README documents a real false-`proved` bug found there in review,
  and a half-built version of that is worse than none.
- Did not cross-run `cpbnb` against `eoex` on a shared case. That is the obvious next check and the
  cheapest real verification available: two independent implementations, same verdicts.

## For the theory workers

The exact residual gap is $(2k+1) - \sqrt{4k^2+4k-7} \sim 2/(2k+1)$ in $d$; at $k=7$ that is
$0.2690801\ldots$, or 2.24 % of the target. The attack write-up §3.2 (which partition refinements
are dead and which are live — **corrected**, see above) and §5
(resolution theorem: a cell method needs level $\ge 9$, i.e. $\ge 2.6\times10^5$ cells, merely to
*match* Oler at $k=7$) are the two things there that constrain what a proof can look like. Both are
`sketch`. §3 and §1 **have** now been cross-examined, and both came back with a refutation of the
broad reading I had put on them — see the corrections above. §5 has not been examined at all.

## Postscript: the third thing I got wrong, and it is the worst one

Two of my negative claims were refuted by an independent verifier the same day. Both failed in the
*same direction*: I proved a narrow true thing and wrote down a broad false thing, and in both
cases my own file already contained the counterexample two sections earlier (the $k \le 3$
argument, which is both a uniform-in-$d$ exhaustion **and** a true-capacity partition that beats
Oler). I labelled it an "exception" and moved on instead of treating it as a refutation of the
general claim I was about to make.

Cost: the manager propagated the partition reading before it was caught and two theory routes were
dropped on it. That is the concrete damage from over-scoping a negative result, and it is worse
than a wrong positive claim would have been, because nobody re-checks a route that has been
declared dead.

Rule I want to apply next time: **when a write-up contains a sentence of the form "one exception,
and it is worth stating…", stop and check whether the exception refutes the general claim rather
than qualifying it.** In both of these it did.
