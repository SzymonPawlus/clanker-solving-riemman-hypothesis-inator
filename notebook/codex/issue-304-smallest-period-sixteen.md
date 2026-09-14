# Every seven-row maximal-anchor cover has a period at most sixteen

Status: `sketch`, with exact finite arithmetic obligations and an explicit
analytic tail. Independent review is required. This is separate from the
frozen universal-measure certificates and assumes none of their claims.

## Statement and endpoint semantics

Let `M` be a positive integer. Suppose at most seven distinct positive speeds
`w<M` cover every lower endpoint `(15j+1)/(15M)`, `0<=j<M`, at threshold
`1/15`: for each endpoint at least one selected speed has distance strictly
less than `1/15` from an integer. Then some selected speed has reduced period

```text
h=M/gcd(M,w) <=16.
```

This is a structural statement in the `k=14`, fifteen-total-runner attack.
Forbidden arcs are strict; equality is a valid witness. All endpoint
conditions concern one common time. Only common integer scaling is used.

For `g=gcd(M,w)`, put `h=M/g`, `a=w/g`. Then `2<=h`, `1<=a<h`,
`gcd(a,h)=1`, and the killed endpoint indices are the lift of

```text
B(h,a)={j mod h: min(s,15h-s)<h}, s=a(15j+1) mod15h.
```

Equivalently, write centered representatives `e=a+15k` with `-h<e<h`.
The associated residue is `j=a^(-1)k mod h`. Thus

```text
|B(h,a)| <= ceil((2h-1)/15) <= (2h+13)/15.
```

The first count concerns an interval of exactly `2h-1` integers, so no
rounded real endpoint enters the proof.

Remove redundant rows from a cover. Its remaining row sets are distinct;
in particular, identical sets at the same period cannot both occur. Write
`p` for the smallest period and `B` for a row at that period, with `b=|B|`.
If `p>=92`, all seven row densities are strictly below `1/7`, since
`(2h+13)/(15h)<1/7` for `h>91`. Hence `p<=91`.

## Exact charge outside the smallest row

For another row `(h,a)` with residue set `C`, let `d=gcd(p,h)`. Its density
on the complement of the selected base row is exactly

```text
Q(B;h,a) = d/(ph) * sum_(x in C)
             (p/d - #{r in B: r=x mod d}).
```

This follows by counting compatible pairs of residues modulo `p` and `h`.
There is one index modulo `lcm(p,h)` for each compatible pair, and
`1/lcm(p,h)=d/(ph)`. Therefore a cover with at most six further rows requires

```text
b/p + sum_of_the_six_further_charges >= 1.
```

It is safe to maximize this expression over all admissible reduced periods
and numerators, whether or not the periods can occur together in one `M`.
Removing this compatibility requirement enlarges the candidate family.

## Uniform analytic tail

For every fixed base residue `r mod p`, at least
`floor((2h-1)/(15d))` of the centered representatives for the new row have
`j=r mod d`. Indeed this condition selects one congruence class modulo `15d`
inside the consecutive integer interval `[-h+1,h-1]`. Thus

```text
Q(B;h,a)
 <= ceil((2h-1)/15)/h
       - (bd/(ph))*floor((2h-1)/(15d))
 <= (2/15)(1-b/p) + (13/15+bd/p)/h
 <= (2/15)(1-b/p) + (13/15+b)/h.
```

The middle inequality uses
`floor((2h-1)/(15d)) >= 2h/(15d)-1`, and the last uses `d<=p`.
The ordinary row-density bound is also available. Consequently every row
with `h>=301` has charge at most

```text
T(p,b)=min(41/301,
           (2/15)(1-b/p)+(13/15+b)/301).
```

This is a proved tail inequality for every numerator and every gcd class.
The unconditioned tail `41/301` alone is insufficient for this finite
certificate: at one period-18 base it would leave a bound slightly above
one. The base-intersection subtraction is necessary.

## Finite certificate

For every `17<=p<=91`, enumerate each distinct base set `B(p,a)` for
`1<=a<p`, `gcd(a,p)=1`. There are 2,472 such base sets. For each base:

1. Enumerate all distinct `B(h,a)` with `p<=h<=300` and remove the base set
   itself at period `p`.
2. Compute every charge by the exact compatible-residue formula above.
3. Retain the six largest finite charges, append six copies of `T(p,b)`,
   and retain the six largest numbers in the resulting list.
4. Add `b/p` and verify that the result is strictly below one.

This upper-bounds every possible choice of at most six other rows, including
any mixture of finite and omitted-tail periods. All 2,472 checks pass.
The largest resulting bound is

```text
1574/1581 < 1,
```

at `p=17`, for example `B={0,1,16}`. Its six finite leaders have charges
five copies of `7/51` and one copy of `70/527`; the analytic tail is lower.
Hence the smallest period cannot lie in `17,...,91`. Combined with the
initial density argument, this proves the statement subject only to the
explicit finite integer checks supplied.

The [author checker](./issue-304/check_minimum_period.py) is standalone and
uses only exact integer/rational arithmetic. For efficiency, it groups rows
having the same histogram modulo `gcd(p,h)` while preserving multiplicity
up to six. A charge depends only on that histogram, so the grouping changes
neither the rankings nor the upper bound. Its
[audit manifest](./issue-304/minimum-period-16-audit.json) records every
period's maximum and binds the checker with SHA-256. An earlier slower
enumeration computed all candidate charges individually and obtained the
same maximum; that exploratory implementation is not a logical dependency.

## Consequence for a finite core search

The manager has separately derived the following direct counting mechanism.
After some covering rows have been selected, let their period lcm be `L`.
An unselected row of period `h` meets each remaining fiber in a proportion
at most `ceil(2n/15)/n`, where `n=h/gcd(h,L)`. If `r` remaining rows cover
all residual indices, one must satisfy `r ceil(2n/15)>=n`. For `r=6,5,4,3,2,1`
the largest possible `n` are respectively `24,10,8,3,2,1`.

Choosing the period-at-most-sixteen row first and then making these choices
gives a final joint period at most

```text
16*24*10*8*3*2 = 184320.
```

For an inclusion-minimal seven-row core, all seven rows must be selected
before the residual set disappears. Its full joint period is
`M/gcd(M,w_1,...,w_7)`, as is seen prime by prime. Therefore the primitive
maximal speed of such a core is at most `184320`. This consequence concerns
inclusion-minimal cores: adding a redundant unrelated speed can arbitrarily
inflate the gcd-normalized maximum and is not covered by the argument.

There is a smaller explicit domain than every integer up to that maximum.
The successive multiplier sets are

```text
E6={1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24},
E5={1,2,3,4,5,8,9,10},
E4={1,2,3,4,8}, E3={1,2,3}, E2={1,2}, E1={1}.
```

Thus the primitive maximum belongs to the product set

```text
{p*n6*n5*n4*n3*n2:
  2<=p<=16, nr in Er for r=2,...,6} intersect {8,9,...}.
```

This contains exactly 1,326 integers. The lower bound eight follows because
seven distinct positive speeds are strictly below the maximal anchor. The
complete [maximum list](./issue-304/seven-core-primitive-maxima.txt) has
SHA-256 recorded in the work log. This product domain is an overestimate:
membership does not assert that a cover exists, and additional gcd,
minimality, and residue constraints remain to be checked.

Neither this finite bound nor the period-sixteen statement implies that
period two or three is compulsory. Those stronger properties hold in the
current bounded census but remain unproved here. A full `k=14` proof would
also need to handle maximal-anchor covers whose smallest inclusion-minimal
core has more than seven rows.

## Work log and audit status

- 2026-09-14 20:21:41 UTC: exact author classification completed. A slower
  direct ranking and a faster histogram implementation agree at global
  bound `1574/1581`.
- 20:27:07 UTC: helper clean-room direct-residue audit has passed 64,527,128
  candidate comparisons across all 2,472 bases. It also checked the analytic
  tail. This is same-family verification, not Claude/human approval.
- The 1,326-element primitive-maximum list has SHA-256
  `21b3b38016972bc98539d8501d9d0014c82dc53d566dfc5fb6b9257fb55e91e7`.
  Root, manager, and helper independently regenerated the product-set count.
- The current statement is frozen for later other-party review. Continued
  work attacks necessity of period two/three through the finite lcm states;
  it does not modify the universal-measure certificates already submitted.
