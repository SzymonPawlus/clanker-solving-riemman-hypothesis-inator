# Exact cut conditions for reduced capped-depth chain linkages

**Issue:** #256. **Status:** `sketch`, targeting `verified:review`.

The local existence hypothesis isolated in PR #255 is false.  A four-arc
acyclic piece with three comparable traces has minimum boundary sizes
`(2,4,2)`, hence capped targets `(2,3,2)`, but every path family attaining
depth two at both endpoint traces has depth four at the middle trace.

This attack gives an exact replacement.  The desired depth sequence
`a_0,...,a_m` determines positive path births and negative path deaths at
the separator layers.  Routing those imbalances is an ordinary
unit-capacity transshipment.  Max-flow/min-cut yields necessary and
sufficient inequalities for a **reduced** capped-depth linkage.  On a prefix
trace the inequality is exactly the familiar boundary lower bound
`|delta+(X)|>=a_t`; the genuinely new inequalities come from non-prefix
shores.  The counterexample fails one such inequality with an empty
off-chain boundary.

Thus individual fixed-trace minima do not imply local chain linkage.  The
precise missing data are mixed-trace cut capacities in the transshipment
network.

## Directed setup

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(X)` with `delta-(X)=empty`.  A **dijoin** meets every dicut.

Let a separator carry realizable comparable traces

```text
R_0 proper-subset R_1 proper-subset ... proper-subset R_m
```

and define layers

```text
Z_0=R_0,
Z_j=R_j-R_(j-1)       (1<=j<=m),
Z_(m+1)=S-R_m.                                          (1)
```

The first and last layers are nonempty.  Let `mu_t` be the minimum nonempty
boundary size among incoming-closed shores of trace `R_t`, and put

```text
a_t=min(3,mu_t),
a_(-1)=a_(m+1)=0,
d_j=a_j-a_(j-1)       (0<=j<=m+1).                      (2)
```

The sequence begins and ends at zero, so its total positive variation equals
its total negative variation.  Write

```text
r_j=max(d_j,0),  s_j=max(-d_j,0),
K=sum_j r_j=sum_j s_j.                                  (3)
```

## Reduced linkages

A **reduced linkage** for the depth sequence `a` is a family of pairwise
arc-disjoint directed paths satisfying:

- exactly `r_j` paths begin at vertices of layer `Z_j`;
- exactly `s_j` paths end at vertices of layer `Z_j`;
- internal vertices and different path endpoints may coincide.

Every path begins in an earlier layer than the layer where it ends.  To see
this, suppose a directed path went from `Z_p` to `Z_q` with `p>q`.  Choose
`q<=t<p`.  A realizable incoming-closed shore of trace `R_t` contains the
endpoint in `Z_q` and excludes the start in `Z_p`; the path would have to
enter that shore, impossible.  Equal endpoint layers cannot occur because a
layer has only births or only deaths in (3).

A path from `Z_p` to `Z_q`, `p<q`, crosses every fixed-trace boundary
`R_t` for `p<=t<q`.  It therefore supplies one unit of linkage depth on that
whole interval.

The depth at trace `t` of any reduced linkage is exactly

```text
sum_(j<=t) r_j - sum_(j<=t) s_j
  = sum_(j<=t) d_j
  = a_t.                                                 (4)
```

Thus a reduced linkage is a sufficient local object for the chain-coloring
theorem of PR #255.  “Reduced” means it has no simultaneous birth and death
which cancel at one layer; such extra endpoint pairs are not needed to
represent the prescribed depth vector, but their removal is not assumed to
be always possible in an arbitrary linkage.

## The transshipment network

Construct an auxiliary network with source `sigma`, sink `omega`, and the
original arcs of `D`, each of capacity one.  Put `M=K+1`.  For every layer
with `r_j>0`, add a distributor `P_j` and arcs

```text
sigma -> P_j       capacity r_j,
P_j -> v           capacity M,  for every v in Z_j.
```

For every layer with `s_j>0`, add a collector `Q_j` and arcs

```text
v -> Q_j           capacity M,  for every v in Z_j,
Q_j -> omega       capacity s_j.
```

A flow of value `K` saturates every `sigma->P_j` and every `Q_j->omega`,
because the capacities on either group sum to `K`.  Integrality and path
decomposition then give exactly the births and deaths in (3).  Unit original
capacities make the resulting directed paths arc-disjoint.  Conversely every
reduced linkage gives such an integral flow.

## Exact mixed-cut inequalities

For `W subseteq V`, define

```text
rho(W) = sum_{j: Z_j subseteq W} r_j
         - sum_{j: Z_j intersection W nonempty} s_j.     (5)
```

**Theorem 1.**  A reduced linkage of depth `a_t` exists if and only if

```text
|delta+(W)| >= rho(W)       for every W subseteq V.      (6)
```

**Proof.**  Fix the original-vertex part `W` of an auxiliary source side.
To avoid a capacity-`M` distributor arc, `P_j` can lie on the source side
only when all of `Z_j` lies in `W`; otherwise its cheapest placement pays
`r_j` on `sigma->P_j`.  Dually, a collector `Q_j` must lie on the source side
whenever `W` meets `Z_j`, paying `s_j` on `Q_j->omega`; if the layer is
disjoint from `W`, it can lie with the sink at no cost.  Hence the least
capacity of an auxiliary cut with original part `W` is

```text
|delta+(W)|
 + sum_{j: Z_j not-subseteq W} r_j
 + sum_{j: Z_j intersection W nonempty} s_j.             (7)
```

Since `M=K+1`, no cut of capacity below the target `K` uses a distributor or
collector arc of capacity `M`.  Using `sum r_j=K`, expression (7) is at
least `K` exactly when (6) holds.  Therefore every auxiliary cut has capacity
at least `K` if and only if (6) holds.  Max-flow/min-cut and integrality give
a value-`K` integral flow exactly in that case, and the preceding path
decomposition is exactly a reduced linkage.  QED

For an incoming-closed shore `W` whose trace is the chain prefix `R_t`, the
whole layers `Z_0,...,Z_t` lie in `W` and all later layers are disjoint from
it.  Thus

```text
rho(W)=sum_(j<=t)(r_j-s_j)=a_t.                           (8)
```

The usual fixed-trace minimum inequality guarantees (6) on all such shores.
But Theorem 1 ranges over every vertex set, including non-prefix traces and
sets with entering arcs.  Those are precisely the additional common-capacity
constraints invisible to the separate numbers `mu_t`.

## Four-arc directed obstruction

Let every vertex be in the separator, with four nonempty layers

```text
Z_0={x_1,x_2},   Z_1={y_1,y_2},
Z_2={x'_1,x'_2}, Z_3={y'_1,y'_2}.
```

The only arcs are

```text
x_1 -> x'_1,  x_2 -> x'_2,
y_1 -> y'_1,  y_2 -> y'_2.                              (9)
```

Use the three prefix traces

```text
R_0=Z_0,
R_1=Z_0 union Z_1,
R_2=Z_0 union Z_1 union Z_2.                            (10)
```

Each trace fixes its shore uniquely, and all three shores are
incoming-closed.  Their boundaries in (9) have sizes

```text
(mu_0,mu_1,mu_2)=(2,4,2),
(a_0,a_1,a_2)=(2,3,2).                                  (11)
```

No capped-depth linkage exists.  Depth two at trace 0 forces both
`Z_0->Z_2` arcs to occur as paths.  Depth two at trace 2 forces both
`Z_1->Z_3` arcs.  There are no other directed paths and all four chosen paths
also cover trace 1, forcing depth four there instead of the prescribed
depth three.

Theorem 1 exposes the same failure as one mixed cut.  From (11),

```text
(d_0,d_1,d_2,d_3)=(2,1,-1,-2).
```

Take `W=Z_0 union Z_2`.  Its outgoing boundary is empty.  It contains the
whole positive layer `Z_0`, meets the negative layer `Z_2`, and contains or
meets no other contributing layer, so

```text
rho(W)=2-1=1 > 0=|delta+(W)|.                            (12)
```

This is a genuine directed obstruction, not an abstract set system.  It is
acyclic, uses four arcs, and its three relevant prefix traces have unique
shores.  The obstruction is the off-chain trace `Z_0 union Z_2`, whose empty
boundary traps one unit of the prescribed transshipment.

The example does not refute Woodall's conjecture or even global chain
packing.  It refutes the proposed *local exact-depth linkage theorem*.
Allowing all four paths gives middle depth four, and excess local depth may
still be globally colorable.  Any continuation must therefore either allow
upper slack in the layer depths or incorporate all mixed inequalities (6).

## Corrected chain target

Theorem 1 replaces the false assertion that the prefix minima alone produce
the capped linkage.  There are two viable strengthened hypotheses:

1. require every mixed inequality (6), which is necessary and sufficient for
   the reduced linkage used by the interval-coloring construction; or
2. allow depths greater than `a_t` and solve a lower-bound circulation whose
   extra paths can be colored without exhausting unit arcs needed elsewhere.

The first is now completely characterized by an ordinary max-flow.  The
second is the narrower remaining route toward an unconditional comparable-
trace theorem.

## Mandatory filters

1. **Schrijver filter: passed.**  Every original arc has unit capacity and an
   integral flow decomposes into paths using distinct arcs.  The theorem is
   an exact feasibility criterion, not an inference from weighted dicut
   values; the counterexample shows the separate unweighted minima are
   insufficient.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin min-max reversal is
   used.  Max-flow is applied only to the explicit transshipment network,
   and path coverage of fixed traces is checked directly.
3. **Easy-direction filter: passed.**  The positive theorem constructs the
   linkage when all mixed cuts pass.  The negative result exhibits the exact
   violated cut and proves nonexistence directly.

## Dependency, status, and review targets

The external input is integral max-flow/min-cut: L. R. Ford Jr. and D. R.
Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of
Mathematics* **8** (1956), 399--404,
<https://doi.org/10.4153/CJM-1956-045-5>.

The theorem and counterexample are noncomputational and self-contained.  They
remain `sketch` until independently reviewed.  The highest-risk points are
the all-of-layer versus any-of-layer terms in (5), the claim that backward
layer paths contradict realizability of every prefix trace, and the exact
distinction between reduced linkages and linkages with canceling endpoint
pairs.
