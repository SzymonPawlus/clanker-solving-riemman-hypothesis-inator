# 2026-08-21 — where Oler's slack actually lives (issue #78)

Single worker, branch `claude/circle-equklatetal-problem-sa7tx7` (the dispatcher fixed that branch
name, so it does not follow the `claude/<issue#>-<slug>` convention; the PR links #78 and says so).
Issue #78 was already claimed and labelled `active-work` from an earlier session with no branch and
no commits behind it, so I picked it up rather than opening a fourth claim.

## What I expected vs what happened

Expected: derive the face/edge decomposition, watch the face-excess hypothesis die on a thin
triangle, write it up. That is roughly what happened, and the probe died faster than expected —
three points, exact rationals, area $1/4$ against the lattice cell's $\sqrt3/4$. The hypothesis was
never plausible once you notice that "all sides $\ge 1$" does not bound a triangle's area below.

What I did *not* expect was that the interesting result would come out of the atlas rather than
the probe. For every lattice and lattice-minus-apex configuration in the repo — including all four
Erdős–Oler cases $n = T(k)-1$ we have exact coordinates for — **Oler applied to the configuration's
own convex hull is exactly tight**, zero slack in every face and every edge, and the entire deficit
of the triangle bound is the hull → triangle relaxation, exactly $1$. The repo's Oler write-up
(§2.1 of `attacks/oler-lower-bound/`) had already flagged that the two stages both *can* lose;
nobody had measured which one does. It is entirely the second, at exactly the cases that matter.

That reframes the Erdős–Oler question in a way I would not have got to by thinking about it: the
packing inequality is not what is failing at $T(k)-1$; the relaxation is, by exactly one point.

## The near-miss worth keeping

Checking the surviving conjecture against Graham–Lubachevsky's table, I got **five refutations** —
$n = 4, 27, 28, 35, 36$. For about a minute that looked like a result. All five were the last digit
of a printed decimal: those $n$ are the lattice cases where the triangle side is exactly an
integer, and $\lfloor a \rfloor$ is maximally sensitive there, so $d(27) = 0.166666666666667$
rounds $a$ from exactly $6$ to just under, and the floor drops by one.

This is the same shape as everything in `FINDINGS.md`: a secondhand record (a rounded table entry,
a repository metadata field) that agrees with everything you can check it against except the one
field you are actually using. The general lesson I want to remember is narrower than "be careful
with floats" — it is that **a truncated decimal is an interval, and the moment a computation takes
its floor, the interval is the only honest input.** The code now uses exact closed forms wherever
the repo has one and a $\pm 1$ ulp enclosure otherwise, and reports when a floor is undecidable
rather than guessing it.

## Discipline notes

- The kill-criterion did its job. Having written "if H is refuted, stop, do not re-scope" *before*
  starting made it easy not to go looking for a patched hypothesis — and there is an obvious
  tempting patch (restrict to configurations that are optimal packings), which is exactly the kind
  of survive-your-own-falsification move §6.3 forbids.
- I checked, and then wrote down, that the surviving conjecture implies the full Erdős–Oler
  conjecture. That is the §7 tripwire: if a short proof of it had shown up in my head, the prior
  says the proof is wrong, not that the conjecture is easy. Writing the implication down first is
  cheap insurance against that.
- Exact arithmetic in $\mathbb{Q}(\sqrt3,\sqrt{11})$ was enough for all 14 certificates (only
  $n = 8$ leaves $\mathbb{Q}(\sqrt3)$), and rational intervals covered the perimeters. Stdlib only,
  ~1.7 s, no seeds — the whole thing is deterministic, which makes "reproducible from one command"
  free rather than a chore.
- The one thing an independent reimplementation is most likely to disagree with me about is the
  normalisation: Oler wants separation 1, the certificates use separation 2. I halve on load and
  say so at every use site. If a checker disagrees with my numbers by a factor of 2 or 4, that is
  where to look first.

## Left open

Whether the identity or the conjecture is already in Folkman–Graham (1969, the obvious prior art).
`cambridge.org` is blocked at the egress proxy, so I could not read a word of it — recorded as
UNVERIFIED rather than guessed at. Also unproved: that stage 1 is exactly zero at $T(k)$ and
$T(k)-1$ for *all* $k$; I only have $k \le 6$, which is every $k$ the repo has exact coordinates
for.
