# Numerical six-dimensional reconstruction probe

**Status:** `numerical`. This experiment is a clean-room interpretation of the
public Proof.Fail prose, not a replay of its unavailable certificate and not a
lower-bound proof.

From repository root, with Python 3.14.6 and NumPy 2.5.1:

```sh
python3 experiments/moser-proof-fail-reconstruction/probe_six_dimensional.py
```

Run the geometry sanity checks from the experiment directory with:

```sh
python3 -m unittest test_probe.py
```

The seed, sample count, restart count, breadth input, candidate pose, and all
three objective values are printed as JSON and pinned in
`default_output.json`. The default run takes roughly three seconds on the
development machine. It searches the inferred functional

```text
max(area(conv(segment, triangle, rectangle)),
    broadworm_breadth/4 + abs(cos(rectangle_angle))/8).
```

The output is only a locally optimized floating-point candidate. See
[`proof-fail-02325-reconstruction`](../../problems/moser-convex-worm/attacks/proof-fail-02325-reconstruction/README.md)
for the derivation, limitations, provenance search, and exact reproducibility
blocker.
