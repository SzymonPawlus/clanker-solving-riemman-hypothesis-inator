# Rational exclusion of the orbit-0 first core-free higher cover

Status: `sketch` pending independent review.

## Definitions and exact branch

For a nonempty proper vertex set `U`, a dicut is `delta+(U)` when no arc enters `U`; a
dijoin meets every dicut. Woodall's nontrivial direction asks for `tau` pairwise disjoint
dijoins when the smallest dicut has size `tau`.

In the unweighted sink-regular ACZ model at `tau=3,rho=4`, twelve active sources have degree
four and sixteen sinks have three-source multisupports. For a source shore `X`, let `y(X)`
count the sinks whose support is contained in `X`. The dicut bound is

```text
4|X|-3y(X) >= 3.                                      (1)
```

An M1 base `Q` also gives `y(X)<=|X|+|Q intersect X|-1`.

Hexadecimal masks use sources `0,1,...,9,A,B`. The selected orbit-0 higher-cover branch has

```text
y(4cc)>=5, y(7ee)>=11, y(811)>=3,
y(abb)>=9, y(b55)>=8, y(d33)>=8.                       (2)
```

The two ID1009 restrictions are the images of the merged canonical target-base family under

```text
left:  0->B, 1->4, 2->9, 3->8, 4->7, 5->5, 6->6, 7->A,
right: 0->B, 1->0, 2->9, 3->8, 4->3, 5->1, 6->2, 7->A.
```

Each image has 32 bases and their union has 63. The distinguished canonical non-SBO pair
`0237/0456` maps to `f00/8e0` on the left and `f00/80e` on the right. For each pair, all 24
bijections between the four-element bases have an exchange candidate forced nonbasic by at
least one lower demand in (2). The checker exhausts these ordering certificates directly.

Sanity checks: a directed path has singleton dicuts and its whole arc set is a dijoin; a directed
cycle has no dicuts; the two-source diamond has `tau=2` and two disjoint dijoins.

## Pointwise rational certificate

Write the six demanded shores in (2) as `D1,...,D6`. Their nonempty triple intersections are

```text
D1 D2 D4 -> 088    D1 D2 D5 -> 044    D1 D2 D6 -> 400
D2 D4 D5 -> 200    D2 D4 D6 -> 022    D2 D5 D6 -> 100
D3 D4 D5 -> 811    D3 D4 D6 -> 811    D3 D5 D6 -> 811
D4 D5 D6 -> 811.
```

The only nonempty fourfold intersection is `D3 intersect D4 intersect D5 intersect D6=811`,
and every fivefold intersection is empty. Therefore every three-source multisupport `S` obeys

```text
sum_{X in (4cc,7ee,811,abb,b55,d33)} [S subset X]
 <= 2 + [S subset 022]+[S subset 044]+[S subset 088]
      + [S subset 100]+[S subset 200]+[S subset 400]
      + 2[S subset 811].                              (3)
```

Indeed, a support lying in at most two demanded shores is paid for by the constant two. A support
in exactly three demanded shores lies in the corresponding bonus shore displayed above. A
support in four lies in `811`, whose coefficient two pays the excess over the constant; membership
in five demands is impossible. This proves (3) without enumeration. The checker independently
verifies the intersection list and also exhausts all 364 multisupports (19 signatures).

Sum (3) over the sixteen sinks. Applying (1) gives

```text
y(022),y(044),y(088) <= 1,  and y(811) <= 3.
```

The masks `100,200,400` are the singleton shores `{8},{9},{A}`. A three-source support
contained in one of them would contribute three parallel incidences at that source and make its
singleton dicut `4-3=1`, contradicting `tau=3`; equivalently, (1) gives
`y(100)=y(200)=y(400)=0`.

Consequently (3) implies

```text
sum_X y(X) <= 2*16 + 1+1+1 + 2*3 = 41.               (4)
```

But the six lower demands in (2) sum to `5+11+3+9+8+8=44`, contradicting (4). The
rational-relaxation gap is three; no integrality or residual case split is used.

## Mandatory filters and limits

- **Schrijver filter: passed.** The load-bearing equations are the unweighted degree-four and
  sink-indegree-three identities. They do not extend to arbitrary arc capacities.
- **Lucchesi--Younger filter: passed.** No dicut/dijoin role reversal is used.
- **Easy-direction filter: passed.** Excluding this obstruction advances the constructive ACZ
  partition route; it is not the trivial packing upper bound.

This proof excludes one higher witness cover in one relative `ID1009 x ID1009` orbit. It does
not exclude other covers in orbit 0, other relative orbits, or prove the bad-complement family
intersecting. Timeouts in the earlier monolithic integer model remain `UNKNOWN`; they are not
used as evidence here.
