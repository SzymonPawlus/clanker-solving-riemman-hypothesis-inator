# `packing-eo-epsilon`

Exact verification for
[`problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/).

```
python3 verify.py > out/report.txt
```

Stdlib only (`fractions`, `itertools`, `math.isqrt`, `random`); no third-party dependency, no
pinned versions needed. Runtime ~14 s. Seed `20260821`, set at import time. Deterministic.

**Everything that decides anything is exact.** Comparisons involving $\sqrt r$ with $r,c$
rational and $c\ge0$ are decided as $r \ge c^2$; lattice coordinates are carried as pairs
$(p,q)$ meaning $(p,\,q\sqrt3)$ with $p,q\in\mathbb Q$, which makes squared distances and
$\frac2{\sqrt3}\times\text{area}$ **rational**; perimeters use rigorous rational enclosures of
width $\le10^{-24}$ from `math.isqrt`. Floats appear only inside printed columns, never inside an
`assert` or a branch that changes an outcome. Every check routes through `check()`, and the last
line of `out/report.txt` is `ALL EXACT CHECKS PASSED` or a list of failures.

**Normalisation, asserted in §0:** separation $1$, $n=27$ points, closed equilateral triangle of
side $a$ with $a<6$, $\operatorname{def}(a,n)=\frac{a^2+3a+2}{2}-n$. Certificates elsewhere in
the repo use separation $2$ and side $d=2a$; nothing here reads them.

Sections of `verify.py` / `out/report.txt`:

| § | What |
|---|---|
| 0 | normalisation and the $\varepsilon$-scale $a_\varepsilon=\frac{-3+\sqrt{217+8\varepsilon}}2$, exactly bracketed |
| 1 | Lemma T re-derived and scanned exactly (173 314 triangles), including its Step 3 |
| 2 | identity T2: Euler counts, area sums and both sides, on nine explicit triangulations |
| 3 | Theorem Q (quantitative Lemma T) and its adversarial scan (174 914 triangles) |
| 4 | symbolic proof that Groemer's 1960 inequality on the hull of the circles *is* Oler's |
| 5 | Theorem E and the lemma that $4k^2+4k-7$ is never a square for $k\ge2$ |
| 6 | Proposition V and the exact $\sigma$-redistribution check |
