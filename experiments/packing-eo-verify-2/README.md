# packing-eo-verify-2 — second adversarial verification pass

One command: `./run.sh`. Python standard library only, no seeds affecting any verdict, no
tolerance anywhere. Every decision is an exact comparison in $\mathbb{Q}$, in
$\mathbb{Q}(\sqrt3)$ (`exactq3.py`, with an exact sign test), or in the symbolic ring
$\mathbb{Q}[\sqrt3,\pi]/(\sqrt3^2-3)$.

Written from the *statements* of the claims examined. No author's code was read, imported or
rerun (problem `RULES.md` §3).

| file | what it checks |
|---|---|
| `exactq3.py` | exact $\mathbb{Q}(\sqrt3)$ arithmetic, hull, shoelace, incidence |
| `check_part1_arith.py` | `eo-exhaustion` §2/§4/§5 and `eo-boundary-counting` §2 tables; independent reconstruction of the `oler-slack-analysis` §1 identity |
| `check_t1.py` | rebuilds the `eo-boundary-counting` §4 perturbed-lattice family; $b=3$, separation, containment, $\Phi(3)$ bound |
| `check_t1_unbounded.py` | whether that family actually makes $\Phi(3)$ unbounded — **it does not**; supplies and verifies a repaired $k$-dependent family |
| `check_lemma_t.py` | `eo-oler-equality` Lemma T (incl. the flagged Step 3), T2, S2 |
| `check_resolution.py` | `eo-exhaustion` §5: the geometric core, and a counterexample to its stated contrapositive |
| `break_p1.py` | break attempt on P1, $\lvert E\cap\partial T\rvert \le 3\lfloor a\rfloor$ |
| `check_epsilon.py` | round-2 `eo-epsilon`: Groemer$\equiv$Oler, Theorem E, Theorem Q, Proposition V |
| `covercheck.py` | independent exact verifier for a claimed small-diameter covering, with negative controls |

Findings: [`problems/circle-packing-equilateral-triangle/attacks/eo-verification-2/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-verification-2/README.md).

**This grants no status** (repo `RULES.md` §5: same model family as the authors).
