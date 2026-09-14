# A scale-independent trial bound for exact witness extraction

Status: `sketch`, conditional on the separately frozen uniform-measure
certificates. This is a practical alternative to the deterministic Euclidean
bisection in the earlier, unchanged constructive note.

Let a primitive core-good rational support have nonnegative weights z_x of
total mass T>6, and suppose each additional speed has bad mass at most1
after uniform lifting to every positive integer scale c. Choose x with
probability z_x/T, choose j uniformly from{0,...,c−1}, and test
t=(j+x)/c against all additional speeds using exact integer inequalities.

The union of their six bad sets has mass at most6. Thus each independent
trial succeeds with probability at least(T−6)/T. The expected number of
trials is at mostT/(T−6), independently of c. With probability1 the procedure
eventually returns a witness. Every returned time is checked exactly; the
randomness affects runtime only.

For the first frozen P18 certificate, T=6011/1000 and every column has load
at most749/750. The finite certificate supplies that bound, while the
large-denominator tail has the smaller bound T/7. The surviving mass is
therefore at least

```
6011/1000−6*(749/750)=19/1000.
```

The sharper success probability is19/6011 and the expected trial count is
at most6011/19. This is a conditional probability bound, not an empirical
estimate from one random example.

Rational weights can be sampled without floating point: clear their common
denominator, draw a uniform integer below the sum of numerators, and find
its cumulative-weight interval. The lift index is likewise a uniform integer.
Each trial checks only a fixed number of exact modular products on integers
with O(log c) bits. The implementation in `issue-297/randomized_witness.py`
uses the system random source by default and accepts a seeded generator for
reproducible diagnostics. A user-supplied trial cap may return a timeout;
the unbounded default is the procedure analyzed above.

This addresses a practical limitation observed in deterministic bisection:
although its arithmetic-operation count is polynomial in log c, a thousand-
digit scale still required thousands of Euclidean interval counts. Sampling
preserves exact verification of the answer while avoiding those interval
counts. No claim about full fifteen-runner configurations or all arbitrary
fourteen-speed tuples is added.

The portable diagnostic input copies the exact first P18 support and records
its source commit and hash. With seed3042971000 and c=10^1000+239, six
additional speeds were generated before sampling. The procedure returned a
witness in2 trials, and a separate direct rational check confirmed all14
coordinates at minimum distance exactly1/15. This is one reproducible
performance example, not an empirical replacement for the probability proof.
Replay it with `python3 notebook/codex/issue-297/check_randomized_witness.py`.
