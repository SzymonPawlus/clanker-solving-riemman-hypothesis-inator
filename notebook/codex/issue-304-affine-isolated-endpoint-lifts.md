# Exact prime lifts of integer affine endpoint-cover templates

Status: `sketch`; a separate lifting lemma, not an asserted eight-row
counterexample. The bounded discovery runs below found no candidate. This
note keeps the isolated-endpoint case explicit instead of silently treating
it as a positive safe interval.

## Template and common-time semantics

Let `(a_i,b_i)` be eight distinct integer pairs with nonzero `a_i`. Suppose
there is a nonempty open interval `I` inside `(0,1)` on which

```text
0<a_i*x+b_i<1 for every i.
```

Define the fixed bad subsets of the `z` circle by

```text
C_i={z mod1 : ||a_i*z+b_i/15||<1/15}.
```

Every bad set is open, has Lebesgue measure `2/15`, and has rational
endpoints whose reduced denominators divide `15|a_i|`. The target remains
fourteen moving velocities, fifteen total runners; this lemma describes
only eight rows covering the lower endpoints of a ninth, maximal speed.
It is not a counterexample to the full Lonely Runner conjecture.

## Infinite-family criterion

Suppose `E=(R/Z)\union_i C_i` is finite and at least one fifteenth-grid
point `l/15` lies in the bad union. Then there are arbitrarily large primes
`M` and integers `q` such that the eight distinct positive speeds

```text
w_i=a_i*q+b_i*M <M
```

cover every maximal lower endpoint `(15j+1)/(15M)`. Every row has reduced
period exactly `M`, and the full nine-speed core is primitive. At all
sufficiently large such scales the eight-row cover is inclusion-minimal.

**Choosing the integer speeds.** Take a prime `M>15 max_i|a_i|`, sufficiently
large that the interval `M*I` contains an integer in every residue class
modulo fifteen. Choose

```text
q/M in I, q=M*l mod15.
```

Then `1<=q<M` and each `w_i` lies strictly between zero and `M`. Primality
implies `gcd(q,M)=1`, and `w_i=a_i*q modM` is nonzero. Thus every reduced
row period equals `M`. If two physical speeds were equal, their difference
would show `M|(a_i-a_j)`. The bound on `M` forces `a_i=a_j`, then
`b_i=b_j`, contrary to pair distinctness.

**The sampled phase grid.** Put

```text
z_j=q(j+1/15)/M mod1.
```

Because `q` is invertible modulo `M`, these are exactly `M` equally spaced
points, with a common offset. Multiplying the original endpoint by `w_i`
gives

```text
w_i*(j+1/15)/M = a_i*z_j+b_i/15 mod1.
```

Thus it suffices to show that the sampled grid avoids `E`.

Every point in the finite complement `E` is an endpoint of one of the
finitely many bad intervals. If a reduced rational endpoint `u/v` is sampled,
then `M*u/v=q/15 mod1`, so `v|15M`. Since `v|15|a_i|` for some `i` and
`M>15 max|a_i|` is prime, `gcd(M,v)=1`; consequently `v|15`.

Among the fifteen points `h/15`, the grid contains exactly the one for
which `M*h=q mod15`. Indeed this congruence is necessary by the previous
formula and sufficient because the grid is a complete translate of
`(1/M)Z/Z`. Our choice of `q` makes that point `l/15`, which is bad for
at least one selected row. Hence the grid avoids every safe endpoint in
`E`, and all maximal lower endpoints are covered strictly.

There are arbitrarily large primes, and every sufficiently long interval
`M*I` contains the required congruence class, giving an infinite family.

**Minimality.** Removing any one row leaves seven bad sets of total measure
at most `14/15`. Their complement has positive measure and, being a finite
union of closed intervals and points, contains a positive interval. Apart
from the finite set `E`, it is covered by the removed row. Therefore that
row has a positive private interval. The equally spaced sampled grids hit
every one of these eight private intervals for all sufficiently large
`M`. Each row is then essential. No uniform integer scaling is used to
claim primality; these are new explicitly defined primitive cores.

## The other two cases cannot be discarded

If `E` contains an interval of positive length `ell`, any `M`-point equally
spaced grid with `M>1/ell` hits it. Such a fixed template can therefore
produce endpoint covers only for bounded `M`.

If `E` is finite but contains all fifteen points `h/15`, every grid for a
prime `M>15 max|a_i|` hits one of those safe points. This template produces
no prime endpoint cover at those scales. Thus a cell cover by itself is
insufficient: the fifteenth-grid condition is essential.

## Bounded discovery record and certificate specification

The current discovery family takes all slopes `a` with `1<=|a|<=24` and
`b=-floor(a*x)`. Its 180 open chambers are cut by the rational points
`k/a` in `(0,1)`. Within each chamber the integer row pairs are unchanged.
Every candidate is represented by one exact rational chamber point.

For a proposed candidate, an independent checker should generate all bad
interval endpoints, sort them, and check an exact midpoint of every open
cell. It must also list every safe endpoint and every bad fifteenth-grid
point. The lemma applies only if every open cell is covered and at least
one fifteenth-grid point is bad. A concrete integer lift should separately
check the original strict endpoint residues, gcd one, and one private
residue per row.

Two bounded optimization scans completed all 180 chambers: one asked for
coverage of the entire open-circle union, and the other allowed isolated
safe points while enforcing the fifteenth-grid condition. Neither found
a candidate. All solver outputs reported infeasibility, but those numerical
solver decisions have not been independently certified. They are not a
proof that this bounded template family, or all eight-row covers, is absent.
The data are `affine-template-discovery.json` and
`affine-template-isolated-discovery.json` under `issue-304/`.
