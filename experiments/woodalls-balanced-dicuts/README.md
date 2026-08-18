# Balanced dicut hypergraphs — exact experiment

Status: **numerical**. Nothing produced by this directory is a proof of
Woodall's conjecture.

This experiment tests whether the hypergraph of inclusion-minimal nonempty
dicuts (dibonds) is balanced. A negative result includes a proper odd Berge
cycle: an odd number of distinct arc-vertices and distinct dibonds whose
selected incidence matrix has exactly two `1`s in every row and column.

Definitions used by the code:

- For `U` a proper nonempty vertex set, `delta+(U)` is a **dicut** when it is
  nonempty and `delta-(U)` is empty.
- A **dibond** here is an inclusion-minimal nonempty dicut as an arc set.
- A **dijoin** meets every nonempty dicut. Meeting every dibond is equivalent,
  because every finite nonempty family of dicuts below a given dicut contains
  an inclusion-minimal member.

Run the small deterministic tests with:

```bash
python -m unittest discover -s experiments/woodalls-balanced-dicuts -p 'test_*.py'
```

The two balancedness checks are deliberately different: the main checker
searches induced `4k+2` cycles in the incidence graph, while the tiny-instance
oracle enumerates odd square incidence submatrices directly.

The planned scope was through `n = 6`, but the attack's kill criterion fired at
`n = 5`, so the run stopped after exactly 1,099 fixed-order arc subsets. Reproduce
the completed run and both-checker cross-check with:

```bash
python experiments/woodalls-balanced-dicuts/census.py \
  --max-n 5 --cross-check-through 5 \
  --output experiments/woodalls-balanced-dicuts/results-n5.json
```

The output records elapsed time for budgeting, but that field is expected to
vary between runs. All graph and witness data are deterministic.

The smallest emitted obstruction has five vertices and arcs

```text
0->1  0->2  0->3  1->3  1->4  2->3  2->4.
```

It has one source (`0`) and two sinks (`3,4`), hence its source-to-sink
reachability graph is the two-edge star `0--3, 0--4`, a forest. This refutes
the structural conjecture tested by the attack; it does **not** refute
Woodall's conjecture.
