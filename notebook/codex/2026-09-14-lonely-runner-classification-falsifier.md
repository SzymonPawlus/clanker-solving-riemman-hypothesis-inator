# A primitive seven-row maximal cover at maximum 36

Status: `sketch`, requiring cross-family or human review. This is a
counterexample to an exploratory classification conjecture, **not** a
counterexample to the Lonely Runner Conjecture.

The inherited seven-cover burden notebook conjectured that every minimal
seven-row cover of a maximal anchor's lower endpoints was an integer scaling
of one of twenty patterns at maxima18,24,30. The following exact primitive
core disproves that completeness statement:

```
P={2,12,15,18,26,28,33,36}.
```

Its gcd is1 and its maximum is36, so it is not an integer scaling of a core
with maximum18,24, or30. Its seven smaller speeds cover every lower endpoint
of the anchor36 at threshold1/15.

## Exact cover certificate

Index the lower endpoints by

```
t_r=(15r+1)/540,  0<=r<36.
```

A speed w kills an index exactly when

```
min(w(15r+1) mod540, −w(15r+1) mod540)<36.
```

The following disjoint assignment partitions all36 indices. Every listed
index satisfies the strict inequality for the assigned speed.

| Speed w | Assigned covered indices |
| --- | --- |
| 2 | 0,1,17,18,19,35 |
| 12 | 3,6,9,12,15,21,24,27,30,33 |
| 15 | 7,31 |
| 18 | 2,4,8,10,14,16,20,22,26,28,32,34 |
| 26 | 11,29 |
| 28 | 5,23 |
| 33 | 13,25 |

The cover is inclusion-minimal. Indices17,3,7,2,11,5,13 are private to
speeds2,12,15,18,26,28,33 respectively: the indicated speed kills the index
and every other speed in the seven-row cover is safe there. Thus removing
any one row destroys the cover.

## Scope and consequence

This falsifies only the proposed completeness of the twenty primitive cores.
It does not falsify the separate claim that a seven-row maximal cover exists
only when the maximum is divisible by18,24, or30:36 is divisible by18.
It also does not affect the independently specified uniform-measure theorems
for those twenty cores. Those remain restricted-family statements.

An anchor's endpoints can all fail even while the complete velocity tuple
has a good time elsewhere. No no-witness certificate for this tuple is
claimed, and no inference about arbitrary fourteen-speed tuples is made.

The manager's bounded search first returned a scaling of this core at
maximum144 on14 September2026. Direct integer residue enumeration then
verified the normalized maximum36 example. The root coordinator independently
reconstructed all seven kill sets and their private indices from the formula.
Both checks belong to the Codex family and do not supply the required
cross-family approval.

The exact certificate checker is
`issue-297/check_classification_falsifier.py`; its finite input is precisely
the36 indices and seven displayed speeds. It uses no solver and no search
cutoff. The broader exploratory search is separate and is not needed for
this falsifier.

