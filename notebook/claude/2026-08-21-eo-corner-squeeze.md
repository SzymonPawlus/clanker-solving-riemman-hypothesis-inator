# 2026-08-21 — eo-corner-squeeze (Prover E)

Attack: [`problems/circle-packing-equilateral-triangle/attacks/eo-corner-squeeze/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-corner-squeeze/).
Code: [`experiments/packing-eo-corner-squeeze/`](../../experiments/packing-eo-corner-squeeze/).

## What I was asked and what I got

Take Prover A's conditional Erdős–Oler contrapositively — a $k=7$ counterexample must have
$S_j^{(V)} \ge T(j)$ at every corner and every scale $j \le 5$ — and squeeze it against the count
of 27. Outcome: **not contradictory**, and the interesting part is *how* I established that.
Rather than failing to find a contradiction (which proves nothing), I formalised the whole idea as
an exact integer relaxation and ran it at $k = 4, 5, 6$, where Erdős–Oler is **known true** and the
geometric system therefore has no solution. The relaxation is feasible at all of them. A method
that cannot see a contradiction where one certainly exists cannot supply one at $k = 7$.

That is the shape of refutation this repo should want: not "I tried and failed" but "here is the
control that shows the method is neutral, with the witness attached."

## The mistake I nearly shipped, and what caught it

My first run reported the relaxation **infeasible at $k = 4$** — a counting proof of Erdős–Oler at
$k = 4$. I did not believe it, so I extracted the violated constraint instead of writing it up.
It was a single box: the *whole triangle*, capacity 8. That capacity came from the cited table
entry $d(9) = 3$ — which **is** Erdős–Oler at $k = 4$. Perfectly circular, and completely
invisible from inside the ILP output, which just says "infeasible".

What caught it was a habit rather than an insight: **when a search returns a verdict I want, get a
human-readable certificate for the verdict before believing it.** "Infeasible" is not a
certificate; "constraint X is violated by profile Y" is. The moment I had the violated constraint
in front of me the circularity was obvious in one line.

The generalisation I want to remember: *a cited table is an input to a proof, and inputs can
contain the conclusion.* This is the same failure as promoting a `sketch` to an assumption
(`RULES.md` §3), but disguised — the offending step was `cited`, the strongest status there is,
and it was still illegitimate **for this particular question**. Status is not context-free. The
guard is now a named variable in the code (`geom.EXCLUDE`), not a comment.

Had the same bug survived to $k=7$ it would have printed "infeasible" for the open case and I
would have been writing an `extraordinary-claim` PR for a tautology.

## The second error, caught earlier and cheaper

In scratch I derived a contradiction at $j = 4$ from "the pair region $\{u_A \ge 4\} \cap
\{u_B \ge 4\}$ is a small triangle". It is a **rhombus** of side $a-4$ with a vertex at $C$, and
it holds up to 8 points rather than 4. The contradiction evaporated. I caught this only because I
re-derived the region in $(u_A,u_B)$ coordinates instead of trusting the picture in my head: the
triangle $T$ in those coordinates has vertices $(0,a),(a,0),(a,a)$, not $(0,0),(a,0),(0,a)$, and
I had silently assumed the latter. Coordinates I have not written down are coordinates I have got
wrong.

## What is actually worth keeping

**Lemma P.** The top-scale corner constraint $\#\{u_V \ge k-2\} \le 2k-2$ has a three-line
projection proof — points in a strip of width $< \sqrt3/2$ have horizontal separations
$> 1/2$ — with no Oler and no CIO in it. It reproves the strongest instance of Prover A's
constraint independently, which is what §3 requires before building on a `sketch`. Better, it
*explains* the break-even: the bound is $1 + a/\sqrt{1-w^2}$, which equals $2k-1$ exactly at
$a = k-1$, so the constraint is worth exactly one point and exactly one point is the whole
conjecture. Every corner mechanism I have seen today is worth exactly one point. That is starting
to look like a theorem rather than a coincidence.

**Viviani only bites from $k = 7$.** $V(k) - C(k) = (k-1)(k-6)/2$: the three corners genuinely
interact, but only for $k \ge 7$, and the capacity ceiling still clears the floor by a margin
growing like $k^2$. So the "three corners must overcount" intuition is correct in sign and hopeless
in size.

## Process notes

- Writing the kill-criterion first paid off concretely. K1 named "$k=6$ feasible" as the stopping
  condition *before* I knew the method would be circular at $k=4$; when the guard fixed the
  circularity and $k=4,5,6$ all came out feasible, there was nothing to decide and no temptation
  to re-scope into "make the partition finer" — which is a different attack and belongs in a
  different issue.
- Two bugs in my own code found by controls rather than by reading: `nmax=40` silently truncating
  the $N$ table (which manufactured a fake contradiction at $k=12$), and a file rewrite that
  didn't persist so I was benchmarking code that wasn't on disk. Both were caught by checking a
  number against a formula I could compute by hand. Neither would have been caught by re-reading
  the code.
- The manager's retraction of "partition-and-count is dead" arrived mid-task and mattered: my
  relaxation *is* a partition/capacity scheme, and I would have been wrong to fence it off. Worth
  noting that the retraction did not save the attack — the scheme is live and still neutral — but
  it did mean I was testing the right thing rather than avoiding it.
