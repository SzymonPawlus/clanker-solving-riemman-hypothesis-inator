# Kill-criterion — r4-krawczyk

**Construction / upper bound only. Nothing in this file bears on optimality.**

## The criterion, as stated in the assignment

> If Krawczyk fails to contract on the calibration cases — e.g. contact systems at optimal
> packings are degenerate, or rattlers make the system rank-deficient — record exactly which
> `n` failed and the diagnosed reason, and **STOP**. Do not proceed to open `n` with an
> uncalibrated pipeline.

Two gates, both required before any open `n` was run:

1. **Contraction.** The Krawczyk test must succeed (`K(X)` strictly inside `X`) at
   `n = 3, 6, 10, 15, 21, 8, 12`.
2. **Correctness of the enclosure.** The certified interval must **contain** the known exact
   `d(n)`, decided by exact rational comparison against `a + b*sqrt(c)` — not by float
   distance.

## Verdict: did not fire

| n | exact d(n) | Krawczyk contracted | enclosure contains exact d(n) | certified d >= exact d |
|---:|---|:--|:--|:--|
| 3 | 2 | yes | yes | yes |
| 6 | 4 | yes | yes | yes |
| 8 | 2 + 2*sqrt(33)/3 | yes | yes | yes |
| 10 | 6 | yes | yes | yes |
| 12 | 4 + 2*sqrt(3) | yes | yes | yes |
| 15 | 8 | yes | yes | yes |
| 21 | 10 | yes | yes | yes |

Enclosure widths on the calibration set are 2e-50 (the lattice cases, where the solution is
exactly rational in the sheared coordinates) to 1.3e-49. Both gates passed, so the run
continued to `n = 16, 18, 19, 22, 23, 25, 26, 27, 29, 30, 32, 33, 34`, where Krawczyk
contracted at all 13.

Reproduce: `cd experiments/packing-r4-krawczyk && python3 run_all.py 3 6 10 15 21 8 12`, then
read `out/n0NN.json` field `comparison`.

## The degeneracies the criterion anticipated are real — they just land elsewhere

The criterion named two ways the pipeline could die. Both phenomena occur; neither killed it,
and saying precisely why is the point of this file.

- **Rank deficiency from rattlers.** Real, at `n = 16, 22, 23, 29, 30, 32`: the tight
  constraint system leaves 1–4 of the `2n+1` variables undetermined. It does not stop
  contraction because the rank-revealing pivoting freezes exactly those variables at exact
  rationals and applies Krawczyk to the square remainder. What is certified is then a solution
  of the *frozen* system, which is weaker than it sounds and is stated as such.
- **Over-determination.** Real at **all 20** `n` (`K > rank`, deficiency 1 to 24). This is the
  one that bites, and it bites the *conclusion* rather than the *test*: the square subsystem
  must drop `K - rank` tight equations, each of which is an active inequality at the solution,
  so it straddles zero over any box containing the solution and cannot be verified. Therefore
  **the Krawczyk box can never, at these packings, be turned into a packing certificate on its
  own.** The bound comes from an explicit exact configuration instead (attack README §4).

So the honest one-line summary of what the interval-Newton idea bought: it **enclosed** the
contact solutions to 49 digits at every `n` tried, and it **could not** certify feasibility by
itself at any of them.

## What would have made it fire

Any of: the Krawczyk test failing to contract at a calibration `n` at every box radius tried
(1e-30 down to 1e-25 and up to 1e-35); an enclosure not containing the known exact value; or
the exact witness check rejecting a configuration the enclosure claimed. None occurred.
