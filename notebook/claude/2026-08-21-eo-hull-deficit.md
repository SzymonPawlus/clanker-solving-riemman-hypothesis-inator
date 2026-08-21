# 2026-08-21 — Erdős–Oler $k=7$: the hull → triangle relaxation

Worker: `claude` (Claude Opus 5), Prover A on the 5-agent push at
`problems/circle-packing-equilateral-triangle`. Branch `claude/circle-equklatetal-problem-sa7tx7`.
Write-up: `problems/circle-packing-equilateral-triangle/attacks/eo-hull-deficit/README.md`.
Code: `experiments/packing-eo-hull-deficit/` (one command, stdlib only, exact).

## What I was asked

Attack **stage 2** of Oler's route to $s(n)$ — the relaxation $A(H)\le A(T)$, $M(H)\le M(T)$ —
which `oler-slack-analysis` §3 had measured as carrying the whole missing unit at $n = T(k)-1$.
Target: 27 unit-separated points cannot fit in an equilateral triangle of side $a < 6$.

## What happened, in order

1. Wrote the kill-criterion first (`KILL-CRITERION.md`), before any code existed.
2. **Corner-Deficit Lemma.** $\mathrm{def}(H) \ge \sum_V (t_V^2+t_V)/2$ where $t_V$ is the side of
   the largest empty corner triangle. Falls out of $E \subseteq$ hexagon + convex monotonicity.
   Tight on all 12 exact certificates; reproduces "stage 2 = 1" exactly at $T(k)-\text{apex}$.
3. **Corner-Improved Oler (CIO).** Coupling the cut to a *count* of the points inside it. This is
   the real object: it is configuration-dependent and strictly stronger than the lemma.
4. **Conditional Erdős–Oler.** If some corner has an empty unit corner triangle, E–O holds — for
   every $k$, not just 7. Genuine, and tight on the extremal configurations.
5. **The kill.** $(t^2+t)/2 < T(\lfloor t\rfloor+1) \le N(t)$ *strictly*, for every $t$. So the
   guaranteed (worst-case) gain of any corner cut is strictly negative. Generalised to every convex
   cut by a three-line argument from the lattice's exact tightness. Route dead.

## The thing worth remembering

**I nearly shipped a wrong kill.** My first draft used the "$T(7)$ minus an interior point" witness
($\mathrm{def}(H) = 0$, hull $=$ triangle, all corner deficits $0$) to kill CIO as well as the
deficit lemma. Then the discrimination check I wrote to *illustrate* the kill contradicted it: CIO
excludes that configuration, at corner $A$, scale $j=3$, because the deleted point sits at
corner-side 2 and the count in $\Delta_A(3)^\circ$ drops from 6 to 5. The witness kills
$\mathrm{def}(H)$; it does not kill CIO. What kills CIO is Proposition 5.

The order matters: I had already written the confident paragraph. It read fine. It was wrong. The
only reason it did not survive is that I made the experiment print a table that could disagree with
the prose — and it did. **Write the check that can embarrass the claim, and print it.**

## Second correction, outward-facing

The manager sent mid-flight numbers claiming a worker's side-length gaps ($0.298$ at $k=3 \to
0.135$ at $k=7$) were a separation-1/2 normalisation slip, and gave $0.628 \to 0.272$ instead.
Re-derived exactly: the manager's four values solve $\mathrm{Oler}(a) = T(k)-\mathbf{2}$, not
$T(k)-1$. The relevant root is $a_0 = \tfrac{-3+\sqrt{8T(k)-7}}{2}$ ($=\tfrac{-3+\sqrt{217}}{2} =
5.86546$ at $k=7$), so the worker's figures were the correct ones and $2/(2k+1)$ is a decent
approximation to that gap rather than a factor-of-two error. Recorded in the write-up §0.1 rather
than silently used, because it is the `FINDINGS.md` pattern again — a correction that is itself the
error. Manager's qualitative conclusion ("measure in points, not side length") is right and I have
followed it throughout.

## Status discipline

Everything I produced is `sketch` or `numerical` or `refuted`. Nothing entered `results/`. Nothing
is assumable, including by me. The one `refuted` is the Steiner-type guess
$\mathrm{def} \ge \mu^2/6 + \mu/2$, which is exactly tight on three equal corner cuts and false on
deep ones.

## Where I would go next

Not here. §7.1's witness says Erdős–Oler is a statement about **stage 1** — Oler's inequality
applied to a hull that *is* the whole triangle — so what is wanted is a quantitative stability
theorem for Oler ("near-equality forces near-lattice"), which is the same gap
`oler-lower-bound` §5.2 already names. The alternative isolated in §6 is an integer counting
statement sensitive to $\lfloor a \rfloor$. Both are harder than what I tried.
