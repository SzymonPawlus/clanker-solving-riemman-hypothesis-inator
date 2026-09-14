# Literature hypotheses for the affine-template attack

Status: `literature notes / sketch`, not a reconstructed or approved computational
theorem. The active target remains fourteen moving speeds and fifteen total
runners at1/15. No claim in this note is used to complete that target.

Blanco, Criado and Santos, arXiv:2603.24784v2 (27 April 2026), define LVP using
the multiset of 2u_i and u_i+u_j,u_i-u_j for i<j: one entry must have a direction
not proportional to another entry. Multiplicities matter. Their projected
zonotope reduction requires this property for its actual Gale configuration.
The positive-strip condition 0<a_i*x+b_i<1 in our affine search is not that
condition. They also explicitly require distinct absolute velocities for the
shifted conjecture. Their claimed counterexamples begin with five moving
speeds; this is a different, shifted statement.
[Definitions 4.5 and Theorem 4.8; Conjecture 1.1(ii)](https://arxiv.org/html/2603.24784v2)

Here is a direct warning against dropping the absolute-value restriction. At
threshold1/3, take slopes+1,-1 and both initial phases3/10. The first safe set
on t modulo1 is [1/30,11/30], and the second is [19/30,29/30]. They are disjoint,
so the strict bad sets cover the circle. Both phases lie in(0,1/3). This also
refutes a proposed general principle that clustering arbitrary shifted phases
inside the forbidden interval automatically gives a lonely time. It is not a
counterexample to standard LRC, nor to the distinct-absolute-speed shifted
formulation, nor to an eight-row statement at1/15.

The earlier Alcántara, Criado and Santos paper states a signed distinct-speed
formulation in its introduction, but its actual finite computational theorem
checks 2,133,561 primitive positive strictly increasing four-speed vectors with
sum at most195. Its separate cited reduction handles sum at least196. Those
are four moving speeds, five total runners, and threshold1/5. Its signed wording
must not be applied to opposite slopes using the false shortcut above. The
published certificate checker and the reduction have not been independently
reconstructed here.
[Theorems 1.2 and 1.3](https://arxiv.org/html/2506.13379v1)

An additional elementary observation: independently changing vector signs
preserves the projective-direction multiset relevant to LVP. A generic rational
linear functional avoids zero on each of finitely many nonzero rational vectors;
orienting each vector to make the functional positive places them in an open
half-plane without changing LVP. Thus half-plane positivity by itself cannot
prove LVP. A useful reduction would need the complete additional strip/Gale
structure, checked on the exact configuration rather than inferred by analogy.
