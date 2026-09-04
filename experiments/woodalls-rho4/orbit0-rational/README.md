# Orbit-0 rational higher-cover certificate

Run from the repository root:

```text
python experiments/woodalls-rho4/orbit0-rational/verify.py
```

The checker regenerates the selected two ID1009 images from the merged target-base list, verifies
that the six demanded shores are compatible with every required base, checks that those demands
cover all 24 candidate orderings in each distinguished non-SBO base pair, and verifies the
rational support inequality on all 364 three-source multisupports.

The conclusion excludes only issue #105's specified first core-free higher cover in relative
orbit 0. It does not exclude every higher cover or prove Woodall's conjecture.
