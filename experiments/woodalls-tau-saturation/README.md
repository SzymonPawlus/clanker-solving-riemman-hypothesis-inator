# Tau-preserving arc saturation

Status: **numerical**. The elementary lifting lemma is discussed separately as
a `sketch`; the census does not prove a structural theorem.

For a fixed vertex order, a DAG is called **tau-saturated** here when adding
any missing forward arc strictly increases its minimum dicut cardinality.
The experiment enumerates every subset of the forward arcs and tests that
definition exactly.

Run tests:

```bash
python -m unittest discover -s experiments/woodalls-tau-saturation -p 'test_*.py' -v
```

Run the declared census:

```bash
python experiments/woodalls-tau-saturation/census.py \
  --max-n 6 --cross-check-through 5 \
  --output experiments/woodalls-tau-saturation/results-n6.json
```

The scope contains `1+2+8+64+1024+32768 = 33867` fixed-order labeled arc
subsets. It is not isomorphism-free, and it intentionally stops before the
seven-vertex scope of issue #31. The direct shore scanner is cross-checked
through `n=5` by a separate predecessor-bitset implementation.

The completed census found 55 tau-saturated instances with `tau>=3`: one at
`n=4`, eight at `n=5`, and 46 at `n=6`. All 55 are source-sink-connected.
This is bounded **numerical** evidence only and does not prove that the pattern
continues.
