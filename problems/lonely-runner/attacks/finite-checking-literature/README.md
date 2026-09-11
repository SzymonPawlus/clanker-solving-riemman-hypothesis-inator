# Finite checking for Lonely Runner: source and certificate ledger

```text
status:        literature (non-assumable pending independent review)
author:        codex (@Flow-25), 2026-09-11, issue #298
primary cut:   arXiv:2604.23906v2 (2026-09-01) and arXiv:2609.02604v1 (2026-09-02)
scope:         stationary-runner convention, finite reduction, sieves, current finite frontier
```

## Executive correction to the campaign premise

The issue was opened against `arXiv:2604.23906v1`, which reports the cases through thirteen
total runners and therefore makes fourteen runners look like the next case. That is no longer
the current primary-source frontier. Allikvere's preprint **Fourteen lonely runners**,
`arXiv:2609.02604v1`, submitted 2 September 2026, claims a computer-assisted proof of
`LRC(13)`, i.e. fourteen total runners [A]. Its 175 MB verification package is publicly
available on Zenodo [Z]. Neither [A] nor [ST] is presently a peer-reviewed publication.

This note does **not** promote either claim to an assumable repository status. In particular,
rerunning an author's audit is evidence that the archive is coherent, not an independent
reimplementation of its two exhaustive kernels.

## 1. Conventions and normalization

The papers write `LRC(k)` for the stationary-runner form with **k moving speeds and k+1 total
runners**. For positive integers `u=(u_1,...,u_k)`, the LR property is

```text
there exists real t such that ||t u_i|| >= 1/(k+1) for every i,
```

where `||x||` is distance to the nearest integer. The endpoint is non-strict. The original
distinct-real-speed formulation reduces to positive integral relative speeds; sign changes do
not matter because `||-x||=||x||`. Repeated relative speeds reduce to a smaller distinct set,
and a common nonzero scale changes witness time inversely. Thus a putative counterexample may
be taken positive, pairwise distinct, and primitive (`gcd(u)=1`). The primitive hypothesis is
load-bearing in the finite product bound below.

## 2. Exact finite-reduction ledger

Fix a prime `p` and a positive integer level `l`, and set

```text
Z_{p,l} = Z/(lp)Z minus the residue classes divisible by p.
```

A vector `v in Z_{p,l}^k` is `(k,p,l)`-proper if either:

1. for some omitted coordinate `i`, `gcd(l,v_1,...,v_hat_i,...,v_k)>1`; or
2. some grid time `t in (lp)^(-1) Z` satisfies `||t v_i|| >= 1/(k+1)` for every `i`.

Write `I(k,p,l)` for the improper vectors. A residue vector `v in Z_{p,1}^k` is *eventually
proper* if some level has no improper lift of `v`, and `J(k,p)` is the set not eventually
proper. [ST, Definitions 2.1 and 2.3]

The underlying finite theorem is slightly sharper than the product form used by the
computation. [MSS, Theorem A] says: assuming the conjecture for `k` total runners, the
`k+1`-runner conclusion holds for primitive positive integral speeds whenever

```text
sum_{S subseteq {1,...,k}} gcd(u_i : i in S) > binom(k+1,2)^(k-1).
```

(Their empty-set convention does not affect the corollary used here.) Its contrapositive,
combined with the AM--GM estimate in [R, Corollary 3], gives the following product form. This
is a bound on the **product**, not a coordinatewise box; the earlier Tao reduction is the one
usually stated as a very large coordinate bound.

The logical chain actually used is:

- [ST, Lemma 2.4] `J(k,p)=empty` iff `I(k,p,l)=empty` for some common `l`. The forward
  direction takes an lcm of finitely many per-vector levels.
- [ST, Lemma 2.2] if `LRC(k-1)` and `I(k,p,l)=empty`, then every counterexample to `LRC(k)`
  has `p | u_1...u_k`.
- [MSS, Theorem A], via [R, Corollary 3] and [ST, Lemma 2.6], says that under `LRC(k-1)` a
  **primitive** counterexample satisfies

  ```text
  u_1...u_k < B_k,
  B_k = ( binom(k+1,2)^(k-1) / k )^k.
  ```

- Hence [ST, Proposition 2.7]: if `LRC(k-1)`, every `p` in a finite prime set `P` has
  `J(k,p)=empty`, and `product(P) >= B_k`, then `LRC(k)`.

For `k=13`, `log B_13 = 13(12 log 91 - log 13) = 670.34974...`. This is the precise
completeness dependency behind a positive fourteen-runner claim: a finite gate computation
alone is insufficient without `LRC(12)`, the primitive product bound, and enough prime mass.

### Source-text hazards

The September v2 of [ST] still contains two errors which [A, Remarks 2.1--2.3] identifies and
repairs:

- [ST, Proposition 3.1] states lifting for an arbitrary shadow `S` and its proof prints an
  equality that is only one inclusion in general. The computation needs the reverse inclusion.
  It is valid for **complete per-row improper fibers**, because every improper finer lift reduces
  to an improper coarser parent; it is not justified by the proposition as literally stated.
- In [ST, Proposition 5.1]'s unit-action proof, choosing a multiplier congruent to `1 mod l`
  silently needs `gcd(l,p)=1`, and the displayed witness transfer uses the inverse in the wrong
  direction. [A] repairs this by writing `l=p^nu l_0`, choosing
  `b = a^(-1) mod p^(nu+1)` and `b=1 mod l_0`, setting `u'=bv'`, and transferring witness
  `t` to `bt`.

Also, [ST, Corollary 2.5] displays `LRC(k)` although it purports to restate Lemma 2.2 and the
needed hypothesis is `LRC(k-1)`. The safe derivation bypasses that corollary and uses Lemmas
2.2 and 2.4 directly. Lemma 2.6 must be read with `gcd(u)=1`, as in its source; without it,
scaling immediately falsifies any fixed product bound.

## 3. The Sungkawichai--Trakulthongchai sieves

[ST, Proposition 3.1] motivates two operations, subject to the complete-fiber qualification
above:

- a `c`-lift enumerates all `c^k` coordinatewise children modulo `clp` and retains precisely
  improper children;
- backward projection maps a retained family modulo `lp` back modulo `p`.

Permutation, coordinate sign changes, and multiplication of the whole tuple by a unit modulo
`p` preserve eventual properness [ST, Proposition 5.1, with the repaired unit proof above].
The implemented representative convention sorts folded residues and fixes the first to `1`.

The exact published pipelines are:

```text
k=11: I(k,p,1) --x2--> level 2 --x2--> 4 --x2--> 8 --x2--> 16
                    --x3--> 48 --x3--> 144; require the final set empty.

k=10 or 12: I(k,p,1) --x2--> 2 --x2--> 4 --x2--> 8 --project--> modulo p;
              require only the orbit of (1,2,...,k) to remain.
```

For the second pipeline, `k+1` is an odd prime. [ST, Proposition 4.4] analytically proves the
remaining orbit eventually proper when `p>k(k+1)` (with five explicitly checked smaller-prime
exceptions listed in its footnote). This replaces an otherwise enormous `(k+1)^k` lift. The
argument does **not** apply at `k=13`, because `k+1=14` is composite.

[ST, Remark 3.2] explains why a terminal level divisible by `k+1` is unavoidable for the tight
tuple `(1,...,k)`: its equality witness times have denominator `k+1`. This is a structural
reason, not merely an implementation choice.

## 4. What `arXiv:2609.02604v1` claims for fourteen runners

[A, Theorem 4.2] applies the ledger at `k=13`. It reports 111 closed prime gates: five small
gates, every prime from 199 through 479, and 59 listed tail primes through 877. Their total
natural-log mass is `681.52920...`; the required 110 gates excluding the insurance gate 877
already have mass `674.75270... > log B_13`.

For each gate the claimed exact pipeline is:

1. Generate all level-one improper 13-multisets after folding signs. A class `v` covers folded
   time `a` exactly when `14*d_p(av) < p`; the strict sign is the exact complement of the
   non-strict witness inequality.
2. Split generation into irredundant 13-class covers and extensions of covers supported on at
   most 12 classes. The restricted exactly-12 variant is used only where an exhaustive
   `tau(p)>=12` cover-number check is supplied; the tail uses a general at-most-12 generator.
3. Quotient by the global unit action using a private-time quota. [A, Lemma 3.1] proves that
   every orbit has a quota-passing normalization, so canonicalization cannot erase an orbit.
4. Carry the **entire** improper fiber through binary levels `2,4,8,16,32`. Only two unit
   orbits persist at closed gates:

   ```text
   (1,2,...,13),  (1,2,...,11,13,24).
   ```

5. For every improper level-2 component of those orbits, search the complete `7^13` lift fiber
   from level 2 to level 14 by exact integer branch-and-bound. Every no-witness leaf reportedly
   has all coordinates divisible by 7, so the gcd clause makes it proper. Thus no improper
   level-14 lift remains.

The least common multiple of possible elimination levels `2,4,8,16,32,14` is 224, so Lemma
2.4 can supply a common empty level for each gate. Seventeen explicitly named primes produced
genuine surviving improper level-14 lifts for this pipeline; four more failed operationally;
neither outcome asserts `J(13,p)` nonempty.

### Dependency audit for `LRC(12)`

[A, Lemma 4.1] reports an important irregularity in [ST]'s archived `k=12` run: most logs end
with twelve residual tuples, then a configuration performs a `c=0` lift and reports the set
empty vacuously. [A] says it independently checked all 1,092 residual tuples across the 91
primes used in [ST, Table 1] and found them unit-equivalent to `(1,...,12)`, which is eliminated
by [ST, Proposition 4.4] because every used prime exceeds 156. It separately recomputed the
prime mass `547.3807... > log B_12=545.2667...`. The Zenodo archive includes the copied logs,
provenance, and `st_k12_seed_check.py`. This repairs the evidence path if its checker and inputs
survive independent review; it does not turn [ST] into a peer-reviewed result.

## 5. Artifact availability and what was checked here

Zenodo record `10.5281/zenodo.22066772` describes the artifact as a dataset and provides:

- `fourteen_lonely_runners_package.zip`, 174,600,959 bytes,
  MD5 `9b6564895671a1d5e03d4ff21e124f7c`;
- the manuscript PDF, final generator source, a code guide, and a small framework benchmark.

I downloaded the package on 11 September 2026; its size and MD5 matched the record. It contains
the advertised generator/filter/kill/audit sources, per-gate summaries, retained `.stats` and
`.out` evidence, kill logs, 52 tau-precondition records, and 111 gate directories. Running

```text
python3 audit_gates_v2.py
```

from the extracted archive finished with exit code 0 and independently recomputed within that
script: 111 full-tier gates, `TAU_MANIFEST` 52/52, required mass `674.7527/670.3497`,
`all_ok=True`, and `proof_complete=True`.

The scope limitation is decisive. The audit independently recomputes level-2 counts for all
persistent rows plus samples, but it **reparses rather than reimplements** the complete
`7^13` terminal search. Generator completeness rests on the program's decomposition proof,
small regressions, and comparisons with the framework code, not a second full generator for
all gates. Bulky raw generator intermediates were deliberately omitted; hashes remain but
cannot validate files that are absent. Consequently this rerun is a consistency check, not the
independent reproduction required for `verified:review`.

## 6. Reproduction target

The smallest peer-reviewed result using this finite-checking line is Rosenfeld's eight-total-
runner case (`k=7`) [R], now electronically published in *Mathematics of Computation*. A cleaner
small first reproduction of the **sieve** itself is Trakulthongchai's nine-total-runner case
(`k=8`) [T], published in *Electronic Journal of Combinatorics* 33 (2026), P2.46, with public
code and logs. Its prescribed algorithm is:

```text
for every listed prime p:
  compute all I(8,p,1);
  enumerate every 3^8 lift, retaining exactly I(8,p,3);
  enumerate every 3^8 retained lift again, retaining exactly I(8,p,9);
  require I(8,p,9)=empty;
verify that the listed distinct-prime product reaches B_8;
invoke LRC(7) and the prime-product criterion.
```

For a genuinely independent reproduction, do not treat the public C++ as the specification.
Implement properness from Definition 2.1 using integer residues (`(k+1)*d_{lp}(a v_i) >= lp`)
so endpoints are exact; enumerate full child fibers; separately implement the omitted-coordinate
gcd clause; validate permutation/sign/unit orbit reductions rather than inheriting them; and
recompute the prime product with arbitrary-precision integers. This is small enough to anchor
the method before auditing `k=12` or the new fourteen-runner archive.

The highest-value next check is not another same-script audit of all 111 gates. It is a
from-scratch implementation of (a) the level-one cover generator and (b) the level-14 `7^13`
fiber decision for one closed gate, preferably `p=83` or `p=199`, followed by exact comparison
of canonical orbit counts and terminal leaves. Those are the two places where [A]'s supplied
audit is explicitly not independent.

## References and publication status (checked 2026-09-11)

- **[A]** Jaan Allikvere, *Fourteen lonely runners*,
  [arXiv:2609.02604v1](https://arxiv.org/abs/2609.02604), submitted 2 September 2026.
  **Preprint; no peer-reviewed venue stated.**
- **[ST]** Touch Sungkawichai and Tanupat Trakulthongchai, *Eleven, twelve, and thirteen lonely
  runners*, [arXiv:2604.23906v2](https://arxiv.org/abs/2604.23906), submitted 26 April and
  revised 1 September 2026. **Preprint; no published venue stated.** Issue text naming v1 is
  stale relative to the source used here.
- **[MSS]** Romanos-Diogenes Malikiosis, Francisco Santos, Matthias Schymura, *Linearly-
  exponential checking is enough for the Lonely Runner Conjecture and some of its variants*,
  [Forum of Mathematics, Sigma 13 (2025), e164](https://doi.org/10.1017/fms.2025.10107).
  **Peer reviewed.**
- **[R]** Matthieu Rosenfeld, *The lonely runner conjecture holds for eight runners*,
  [Mathematics of Computation (2026), DOI 10.1090/mcom/4243](https://doi.org/10.1090/mcom/4243),
  also [arXiv:2509.14111](https://arxiv.org/abs/2509.14111). **Electronically published.**
- **[T]** Tanupat Trakulthongchai, *Nine and ten lonely runners*,
  [Electronic Journal of Combinatorics 33 (2026), P2.46](https://doi.org/10.37236/14972), also
  [arXiv:2511.22427](https://arxiv.org/abs/2511.22427). **Peer reviewed.**
- **[Z]** Allikvere, *Fourteen lonely runners: manuscript, gate certificates, and audit code*,
  [Zenodo 22066772](https://doi.org/10.5281/zenodo.22066772), dataset dated 23 August 2026 and
  updated with the 2 September manuscript. **Public archival artifact, not peer review.**
