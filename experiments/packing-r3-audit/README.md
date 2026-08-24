# packing-r3-audit — arithmetic corroboration for the round-3 novelty audit

**Question.** Are the load-bearing numbers in
`problems/circle-packing-equilateral-triangle/attacks/r3-approaches/README.md` §0.1, §0.2 and
§Z.1 correct? They were produced by a Fable 5 ideation lens and checked once by the round-3
manager. This is the **second, decorrelated check**, and it also supplies the derivation §Z.1
omits: how a *density* upper bound converts into a lower bound on `s(n)`.

**Status.** `numerical`. Exact symbolic arithmetic, but a computation, not a proof. Nothing here
is `cited` and nothing may be built on it (`RULES.md` §3).

**Method.** Nothing is read from the triage file. Every quantity is re-derived from the
*statement* of the relevant inequality — quoted in the script's docstrings — using `sympy`, and
only then compared against the decimal the triage printed. The two external inputs are:

- Oler's inequality and Groemer's Satz, transcribed from the quotations in
  `problems/circle-packing-equilateral-triangle/README.md` (which an earlier worker read from the
  Cambridge Core PDF and the free GDZ scan respectively);
- the best-known table, read programmatically from the repo's own transcription of
  Graham & Lubachevsky's printed 15-significant-digit values,
  `experiments/circle-packing-search/reference.py` (`GL_D`), converted by `s = 2/d + 2√3`.

The script **reads** `../circle-packing-search/reference.py` and writes nothing outside this
directory.

## Reproduce

```
python3 experiments/packing-r3-audit/audit_calibration.py
```

No arguments, no seeds, no network, ~4 s. Deterministic (symbolic; no randomness anywhere).
Requires `sympy` (1.14.0 as run). Committed output: `output.txt`.

## Result

Exit status is 0 and the script prints its own `FAILURES:` line at the end. As run:

```
FAILURES: ['s0.2 exclusivity claim is FALSE']
```

Four sections:

1. **Oler → `d(n) ≥ √(8n+1) − 3`. CONFIRMED.** `sympy` expands the scaled substitution to exactly
   `d²/8 + 3d/4 + 1` and `solve` returns the closed form symbolically. Tightness at triangular
   numbers is confirmed **as a polynomial identity in k** (`k²/2 + k/2 ≡ k(k+1)/2` at
   `d = 2(k−1)`), which is stronger than the triage's six spot checks. `d(16) ≥ √129 − 3`,
   `s(16) ≥ 11.82191830673830`.
2. **Density ↔ side dictionary, and the §Z.1 threshold. CONFIRMED.** With
   `density := nπ/((√3/4)s²)` for unit circles, an upper bound `D` on density gives
   `s(n) ≥ 2√(nπ/(√3·D))`; the map is checked to round-trip symbolically. At n = 16 against the
   repo's `s(16) ≥ 2+6√3` the threshold is exactly `8π(14√3 − 9)/507 = 0.755901213657…` —
   the triage's 0.7559 to every digit it printed.
3. **Both published baselines. CONFIRMED, and now sourced.** Oler → `D = 0.83060265`; Groemer's
   Satz applied to the containing triangle → `s(16) ≥ 11.66796539`, `D = 0.85266602`. These match
   the triage's 0.8306 and 0.8527. **This is the evidence for the density convention in (2)**:
   two independent inequalities reproduce two independently printed numbers only under that
   convention. The section also prints the sharpening ladder — Groemer→Oler achieved 2.59 %,
   Oler→threshold would need 8.99 %, threshold→truth leaves 4.99 %.
4. **The Q(√3) family. PARTIALLY CONFIRMED — one claim REFUTED.** `s(17) = 6+4√3`,
   `s(24) = 8+4√3`, `s(31) = 10+4√3` all confirmed against `GL_D`, as are the exact `+2` spacings
   and `s(17) = s(12)+2`. But the triage's claim that **no other open n in 16–34** has a
   best-known value of the form `a + b√3` is **false**: a scan over `a,b ∈ [−40,40]` at tolerance
   2e-11, across every open n in the range (triangular 21 and 28 and Payan's 20 excluded by
   index), returns `{17, 24, 27, 31}`. **n = 27 is missed** — GL print `d(27) = 1/6`, giving
   `s(27) = 12 + 2√3`, and 27 = Δ(7) − 1 is the first open Erdős–Oler case. See §5.4 of
   `../../problems/circle-packing-equilateral-triangle/attacks/r3-audit/README.md`.

## Retraction recorded on purpose

The first run of section 4 typed the best-known table from the author's own recollection and
reported a larger, wrong disagreement set (n = 19, 25, 28, 32). Those were artefacts of a bad
table and are **retracted**; the section was rebuilt to read `GL_D` from the repo and rerun. The
episode is left in the script's comments because it is exactly the failure the audit is about.
