# Independent affine-template orbit audit and a stronger primitive bound

Status: `sketch`, pending Claude or human review. Helper read the root's
mathematical note, not an author implementation. The unchanged original is
preserved as `helper-affine-template-grid-original.md`; its SHA-256 is
`52399ec891f83d0e034acc44055706c6b0e92504699d09660465063c9d18cfe1`.
The original argument passes this audit. The sharper identity below also
gives a stronger bound under its same hypotheses.

The application remains fourteen moving velocities, fifteen total runners,
threshold 1/15. Eight smaller rows cover one maximal anchor's common lower
endpoint grid. Every bad inequality is strict; equality is safe. Only the
entire nine-speed core is normalized by a common gcd. This is a conditional
template lemma, not a finite reduction for every integer velocity tuple.

## Exact gcd identity and complete orbit

Use precisely the original notation and include its explicit pivot
`(P_0,Q_0,R_0)=(1,1,0)`. In particular,

```
L=lcm Q_i, b_i=L P_i/Q_i, c_i=L R_i/Q_i,
B=gcd |b_i|, P=lcm |P_i|, H=15(L/B)P.
```

The pivot gives `B|L`. Primitivity gives the exact identity

```
gcd(M,B w_0)
 = gcd(M,b_0 w_0,...,b_7 w_0)
 = gcd(M,L w_0,...,L w_7)
 = gcd(M,L).
```

The middle equality uses `b_i w_0=L w_i-c_i M`; the last follows by
Bezout from `gcd(M,w_0,...,w_7)=1`. Thus the original quantities `d` and
`g` are equal. For fixed `r`, the indices `j=Lk+r (mod M)`, with
`0<=k<M/g`, traverse the full anchor residue class. The transformed
coordinates

```
y_k=B(w_0/M)k+(B/L)(w_0/M)(r+1/15) (mod 1)
```

visit one coset of the `q=M/g` equally spaced circle points exactly once.
Substitution in every row's phase agrees modulo the integer `c_i k`.
Taking only `floor(M/L)` indices would be incomplete, particularly when
`L>M`. No such truncation is used.

## Boundary grid and sharpened conclusion

The safe set `S_r` is the intersection of the eight closed constraints
displayed in the original. Its boundary points have the form

```
[15Q_i k +/- Q_i - R_i(15r+1)] / [15L P_i/B]  (mod 1).
```

Their reduced denominators divide `H`. Therefore a nonempty interior of
any `S_r` contains a whole closed grid interval of length `1/H`. Any coset
of `q` equally spaced points meets that interval when `q>=H`, including
the equality case. A covering template with such an interior must obey

```
q<H, hence M<gH<=LH=15 L^2 P/B.
```

This improves the original valid bound `M<15 L^2 P`. The conclusion is
strict because boundary equality remains safe. If all the `S_r` are empty
or consist only of isolated points, neither version provides a finite
bound. This limitation remains explicit.

## Separate exact fixtures

`helper_affine_grid_audit.py` was independently written from the formulas.
Its hash-bound report `helper-affine-grid-audit.json` passes ten fixtures,
129,152 direct original-coordinate identities and 1,316 boundary checks.
It verifies unrepeated orbits and the exact identity `d=g`. The fixtures
include `L=10920>M=17`, a composite anchor with `g=6`, seven fixed-seed
prime anchors, and a positive-interior case with `q>=H` where direct
endpoint index 4 is safe. These are implementation regressions; the
quantified proof is the argument above.

Replay from this notebook directory:

```
python3 helper_affine_grid_audit.py --proof helper-affine-template-grid-original.md --output helper-affine-grid-audit.json
```
