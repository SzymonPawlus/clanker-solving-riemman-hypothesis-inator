# Woodall Lean cross-check — prose model vs literal models of the Lean

Status: **numerical** tooling for the faithfulness audit in
`problems/woodalls-conjecture/attacks/lean-foundations-audit/README.md` (issue #151). It
establishes no mathematical claim; it locates digraphs on which a Lean definition and the
README definition disagree.

Environment: CPython 3.11.15, standard library only, no randomness, deterministic.

Files:

- `prose_model.py` — dicut / dijoin / τ / max disjoint dijoins / "τ disjoint dijoins exist"
  from `problems/woodalls-conjecture/README.md` alone, plus the exhaustive labelled-digraph
  generator (`all_digraphs`). Written before any Lean was read.
- `test_prose_model.py` — fixtures: path, 3-cycle (no dicut), diamond (τ=2), near-miss DAG,
  parallel pair, empty-dicut reading.
- `lean_model_76.py` — literal model of `lean/Verified/Woodall/Basic.lean` on branch
  `claude/76-lean-woodall` @ 561af29 (superseded).
- `lean_model.py` — literal model of B1's `Basic.lean` + `Instances.lean` on branch
  `claude/150-lean-foundations` @ ad78d86.
- `sweep76.py`, `crosscheck.py` — the two sweeps; results in `results/`.

Reproduce:

```bash
cd experiments/woodall-lean-crosscheck
python3 -m unittest test_prose_model -v      # must pass first
python3 sweep76.py                            # ~1 min
python3 crosscheck.py                         # ~4 min; --max-n/--max-arcs/--max-mult/--loops
```

Search space, stated exactly: every labelled digraph on `1 ≤ n ≤ 4` vertices with at most 6
arcs, each ordered pair of distinct vertices used with multiplicity 0–2 — 13,615 digraphs, not
reduced up to isomorphism. A separate loop batch (`n ≤ 3`, `≤ 4` arcs, loops allowed) is in
`results/loop_batch.txt`.
