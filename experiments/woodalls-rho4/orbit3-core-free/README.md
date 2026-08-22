# Orbit-3 core-free certificate

Run:

```text
python experiments/woodalls-rho4/orbit3-core-free/verify.py
```

The dependency-free checker regenerates the two relabelled ID1009 base families from the
committed catalogue fixture, checks their 63-base union and the four required-base cap witnesses,
then checks the pointwise inequality in the accompanying attack note on all 364 unordered
three-source multisupports.  The finite support check collapses to 12 containment signatures.

This certificate closes one specified higher-cover branch of one relative `ID1009 x ID1009`
orbit.  It is not an exhaustive check of all witness covers or relative orbits and is not a proof
of Woodall's conjecture.
