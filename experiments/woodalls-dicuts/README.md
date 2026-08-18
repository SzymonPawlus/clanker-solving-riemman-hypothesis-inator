# Exact dicut and dijoin primitives

Status: `numerical`

This is a dependency-free reference implementation for small digraphs.  It enumerates dicuts,
computes the minimum dicut size `tau`, tests dijoins in two independent ways, contracts strongly
connected components, and can exhaustively find a requested number of disjoint dijoins.

An arc is identified by its position in the input sequence, so parallel arcs remain distinct.
For a nonempty proper vertex set `U`, the enumerator accepts `delta+(U)` only when
`delta-(U)` is empty.  It does not replace that condition by merely requiring a nonempty outgoing
cut.

The second dijoin test uses the standard strong-connectivity equivalence: retain the original
digraph and **add** the reverse of every selected arc.  Literal replacement by reversed arcs is
not equivalent; reversing every arc of a directed path just produces the oppositely directed
path.

Run every validation from the repository root with:

```bash
python3 -m unittest discover -s experiments/woodalls-dicuts -p 'test_*.py' -v
```

The suite checks a directed cycle, a directed path by hand, a `tau = 2` diamond (including an
exhaustively found packing of two disjoint dijoins), two source--sink connected DAGs, SCC
condensation with parallel arcs, and the empty-dicut edge case.  On every small fixture it checks
all arc subsets and requires the cut-intersection and reverse-augmentation dijoin tests to agree.
It additionally checks both dijoin tests, SCC reduction, and preservation of `tau` on all 64
loopless labeled digraphs on three vertices (each of the six possible arcs is independently
present or absent; isomorphic copies are not removed).

The code deliberately uses exhaustive subset enumeration.  It is a correctness-oriented base
for later independently checked searches, not a claim of scalability and not evidence for the
conjecture beyond the explicitly listed finite fixtures.
