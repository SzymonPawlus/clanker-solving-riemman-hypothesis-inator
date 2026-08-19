"""Branch-and-bound exhaustion: "no n points at mutual distance >= 2 fit in T(d)".

What the search decides
-----------------------
Given ``n`` and an exact rational side ``d``, it tries to prove

    d(n) > d          (equivalently  s(n) > d + 2*sqrt(3))

by exhausting a tree of *cell configurations*.  A node is a multiset of cells (see
``lattice.py``) with multiplicities summing to ``n``: "point 1..n live in these cells, with
this many in each".  The root puts all ``n`` points in the whole triangle.

Branching.  Take a cell of minimal level (the largest cell) and split it into its four
children.  Its ``k`` points are redistributed over the four children in every way -- all
``C(k+3,3)`` compositions of ``k`` into four non-negative parts.  Since the children are
closed and cover the parent, every real configuration consistent with the parent node is
consistent with at least one child node, so the branching loses no configurations.

Pruning.  A node is discarded when either test fires:

* **pair test** -- two occupied cells ``X != Y`` whose *maximum* separation is ``< 2``
  cannot hold two points at distance ``>= 2``.  Exact integer test (``lattice.py``).
  A single cell with multiplicity ``>= 2`` gets the same test against itself: its maximum
  internal separation is its side.
* **capacity test** -- a cell of side ``a`` holds at most ``cap(a)`` points at mutual
  distance ``>= 2``, where ``cap`` comes from the cited optimal ``d(k)`` (``caps.py``).
  ``--max-cited 2`` reduces this to "a cell of side ``< 2`` holds at most one point", which
  is the trivial case and makes the run depend on no literature at all.

Both tests are one-sided: they fire only when infeasibility is *certain*, so a node is
never discarded that could have contained a packing.

Symmetry.  The three level-1 corner cells are permuted transitively by the symmetry group
``D3`` of the triangle (its action on the corners is the full ``S3``).  Any configuration
therefore has an image whose three corner multiplicities are non-increasing, so the search
imposes that at the root split only.  Sound, and worth up to a factor of 6.  No deeper
symmetry reduction is attempted.

Termination.  Splitting always increases the total level, so with a cap ``max_level`` the
tree is finite.  Three outcomes:

* ``proved``      -- every branch pruned.  No ``n`` points at mutual distance ``>= 2`` lie
                     in ``T(d)``; hence ``d(n) > d``.
* ``unresolved``  -- some node survived with every cell already at ``max_level``.  Nothing
                     is proved; the resolution was too coarse.  A witness node is reported.
* ``timeout``     -- the wall-clock or node budget ran out.  Nothing is proved.  The
                     remaining stack is checkpointed so the run can be resumed.

Status of a ``proved`` outcome
------------------------------
It is a finite exhaustion in exact integer arithmetic, so *if the implementation is
correct* the conclusion ``d(n) > d`` is a theorem, not a numerical observation.  In this
repo's vocabulary that makes it a computational claim awaiting an independent
reimplementation (problem ``RULES.md`` §3); until then it is `numerical`.  The arithmetic
is not the weak link -- the enumeration logic is.
"""

from __future__ import annotations

import hashlib
import json
import time
from fractions import Fraction
from itertools import combinations_with_replacement

from .caps import capacity_by_level
from .lattice import ROOT, Cell, is_valid_cell, max_sq_form, subdivide

# A node is a tuple of (cell, multiplicity) pairs, sorted.
Node = tuple[tuple[Cell, int], ...]

#: Checkpoint format version.  Bump on any change to the frontier encoding.
CHECKPOINT_SCHEMA = 1

#: Checkpoint statuses that carry a resumable frontier.  ``proved``/``unresolved`` runs are
#: finished: they store no frontier, and resuming from one is always a user error.
RESUMABLE_STATUSES = ("running", "timeout")


class CheckpointError(Exception):
    """A checkpoint was rejected.  Never downgrade this to a warning.

    A resume replaces the root node -- i.e. the statement "all ``n`` points lie somewhere in
    the container" -- with a frontier that is *asserted* to cover everything the interrupted
    run had not yet refuted.  If that assertion is false, the search closes over a strict
    subset of the configuration space and reports ``proved`` for a theorem it never proved.
    Rejection is therefore the only safe response to any doubt about the file.
    """


def compositions(k: int, parts: int = 4) -> list[tuple[int, ...]]:
    """All ways to write ``k`` as an ordered sum of ``parts`` non-negative integers."""
    out: list[tuple[int, ...]] = []
    for cuts in combinations_with_replacement(range(k + 1), parts - 1):
        prev = 0
        comp = []
        for c in cuts:
            comp.append(c - prev)
            prev = c
        comp.append(k - prev)
        out.append(tuple(comp))
    return out


class Prover:
    def __init__(
        self,
        n: int,
        d: Fraction,
        max_level: int,
        max_cited: int,
        symmetry: bool = True,
    ) -> None:
        if n < 2:
            raise ValueError("n must be at least 2")
        if d <= 0:
            raise ValueError("d must be positive")
        self.n = n
        self.d = d
        self.max_level = max_level
        self.max_cited = max_cited
        self.symmetry = symmetry

        self.p2 = d.numerator * d.numerator
        self.q2 = d.denominator * d.denominator
        # threshold[L] = 4^(L+1) * q^2 ; pair is compatible iff p^2 * qmax >= threshold[L]
        self.threshold = [(1 << (2 * (level + 1))) * self.q2 for level in range(max_level + 2)]
        self.cap = capacity_by_level(d, max_level + 1, max_cited)
        self._compat_cache: dict[tuple, bool] = {}
        self._pair: dict = {}
        self._comps: dict[int, list[tuple[int, ...]]] = {}

        self.nodes = 0
        self.pruned_pair = 0
        self.pruned_cap = 0
        self.max_depth_reached = 0

    # -- tests -----------------------------------------------------------------

    def pair_row(self, a: Cell) -> dict:
        """Per-cell memo table ``b -> compatible(a, b)``; keeps the hot loop to one dict get."""
        row = self._pair.get(a)
        if row is None:
            row = {}
            self._pair[a] = row
        return row

    def compatible(self, a: Cell, b: Cell) -> bool:
        """Can cells ``a`` and ``b`` hold two points at distance ``>= 2``?"""
        la, oa, ia, ja = a
        lb, ob, ib, jb = b
        level = la if la >= lb else lb
        sa = 1 << (level - la)
        sb = 1 << (level - lb)
        key = (level, sa, oa, sb, ob, ib * sb - ia * sa, jb * sb - ja * sa)
        hit = self._compat_cache.get(key)
        if hit is not None:
            return hit
        qmax, lvl = max_sq_form(a, b)
        ok = self.p2 * qmax >= self.threshold[lvl]
        self._compat_cache[key] = ok
        return ok

    def cap_ok(self, cell: Cell, mult: int) -> bool:
        c = self.cap[cell[0]]
        return c is None or mult <= c

    def comps(self, k: int) -> list[tuple[int, ...]]:
        got = self._comps.get(k)
        if got is None:
            got = compositions(k)
            self._comps[k] = got
        return got

    # -- search ----------------------------------------------------------------

    def run(
        self,
        time_limit: float | None = None,
        node_limit: int | None = None,
        checkpoint_path: str | None = None,
        checkpoint_every: int = 200_000,
        initial_stack: list[Node] | None = None,
    ) -> dict:
        start = time.monotonic()
        if initial_stack is None:
            stack: list[Node] = [((ROOT, self.n),)]
        else:
            # Defence in depth: a caller reaching past ``load_frontier`` (tests, notebooks,
            # a future driver) must not be able to inject a node the checkpoint loader
            # would have rejected.  An *empty* resume stack is never legitimate -- a
            # checkpoint is only written with a frontier while the stack is non-empty -- and
            # accepting one would report ``proved`` without examining a single node.
            stack = list(initial_stack)
            if not stack:
                raise CheckpointError(
                    "refusing to resume from an empty frontier: an empty search stack "
                    "would be reported as 'proved' without examining any configuration"
                )
            for node in stack:
                validate_node(node, n=self.n, max_level=self.max_level)
        # The initial node is the only one never produced by the branching step, so it is
        # the only one that would otherwise skip the capacity test.
        stack = [node for node in stack if all(self.cap_ok(c, m) for c, m in node)]
        status = "proved"
        witness: Node | None = None
        next_checkpoint = checkpoint_every
        poll = 20_000
        next_poll = poll

        while stack:
            self.nodes += 1
            if self.nodes >= next_poll:
                next_poll += poll
                if time_limit is not None and time.monotonic() - start > time_limit:
                    status = "timeout"
                    break
                if node_limit is not None and self.nodes > node_limit:
                    status = "timeout"
                    break
                if self.nodes >= next_checkpoint:
                    next_checkpoint += checkpoint_every
                    if checkpoint_path:
                        self._write_checkpoint(checkpoint_path, "running", stack, start, None)

            node = stack.pop()

            # Cells are held in FIFO order: the front cell always has minimal level,
            # because every child appended at the back is one level deeper than the cell
            # it replaced.  So "split a largest cell" is index 0, with no search or sort.
            cell, mult = node[0]
            best_level = cell[0]
            if best_level >= self.max_level:
                status = "unresolved"
                witness = node
                break
            if best_level + 1 > self.max_depth_reached:
                self.max_depth_reached = best_level + 1

            rest = node[1:]
            children = subdivide(cell)
            is_root_split = cell == ROOT and self.symmetry

            for comp in self.comps(mult):
                if is_root_split and not (comp[0] >= comp[1] >= comp[2]):
                    continue
                occupied = [(children[t], comp[t]) for t in range(4) if comp[t] > 0]

                bad = False
                for child, m in occupied:
                    if not self.cap_ok(child, m):
                        self.pruned_cap += 1
                        bad = True
                        break
                    if m >= 2 and not self.compatible(child, child):
                        self.pruned_pair += 1
                        bad = True
                        break
                if bad:
                    continue

                nocc = len(occupied)
                for a in range(nocc):
                    ca = occupied[a][0]
                    row = self._pair.get(ca)
                    if row is None:
                        row = {}
                        self._pair[ca] = row
                    for b in range(a + 1, nocc):
                        cb = occupied[b][0]
                        ok = row.get(cb)
                        if ok is None:
                            ok = row[cb] = self.compatible(ca, cb)
                        if not ok:
                            bad = True
                            break
                    if bad:
                        break
                    for other, _ in rest:
                        ok = row.get(other)
                        if ok is None:
                            ok = row[other] = self.compatible(ca, other)
                        if not ok:
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    self.pruned_pair += 1
                    continue

                stack.append(rest + tuple(occupied))

        elapsed = time.monotonic() - start
        result = {
            "status": status,
            "n": self.n,
            "d": str(self.d),
            "d_float": float(self.d),
            "max_level": self.max_level,
            "max_cited": self.max_cited,
            "symmetry": self.symmetry,
            "nodes": self.nodes,
            "pruned_pair": self.pruned_pair,
            "pruned_cap": self.pruned_cap,
            "max_split_level": self.max_depth_reached,
            "stack_remaining": len(stack),
            "elapsed_seconds": elapsed,
            "capacity_by_level": [c for c in self.cap],
            "witness": _jsonable(witness) if witness else None,
        }
        if checkpoint_path:
            self._write_checkpoint(checkpoint_path, status, stack, start, result)
        return result

    def _write_checkpoint(
        self, path: str, status: str, stack: list[Node], start: float, result: dict | None
    ) -> None:
        payload = {
            "schema": CHECKPOINT_SCHEMA,
            "status": status,
            "n": self.n,
            "d": str(self.d),
            "max_level": self.max_level,
            "max_cited": self.max_cited,
            "symmetry": self.symmetry,
            "nodes": self.nodes,
            "pruned_pair": self.pruned_pair,
            "pruned_cap": self.pruned_cap,
            "elapsed_seconds": time.monotonic() - start,
            "stack_remaining": len(stack),
            "result": result,
        }
        if status in RESUMABLE_STATUSES:
            frontier = [_jsonable(node) for node in stack]
            payload["frontier"] = frontier
            payload["frontier_count"] = len(frontier)
            payload["frontier_digest"] = frontier_digest(frontier)
        tmp = path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(payload, fh)
        import os

        os.replace(tmp, path)


def _jsonable(node: Node) -> list:
    return [[list(cell), mult] for cell, mult in node]


def _from_jsonable(raw: list) -> Node:
    return tuple((tuple(cell), mult) for cell, mult in raw)


def frontier_digest(frontier: list) -> str:
    """SHA-256 over the canonical JSON encoding of a frontier.

    Detects truncation and hand-editing of a checkpoint written by this code.  It is an
    integrity check, not a signature: anyone who edits the frontier can recompute it.  See
    the trust note on :func:`load_frontier`.
    """
    blob = json.dumps(frontier, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def validate_node(node: object, n: int, max_level: int) -> Node:
    """Check that ``node`` is a well-formed search node for this theorem, or raise.

    A node claims "the ``n`` points are distributed over these cells with these
    multiplicities".  Every clause below is required for that reading to be true:

    * at least one cell -- an empty node describes nothing (and crashes the hot loop);
    * every cell is a genuine cell of the subdivision (``lattice.is_valid_cell``), so it is
      a subset of the container rather than an arbitrary lattice triangle somewhere else;
    * every cell is at level ``<= max_level``, since the branching cannot create a deeper
      one and a deeper cell would evade the ``max_level`` termination test;
    * cells are distinct, and multiplicities are ``>= 1``;
    * **multiplicities sum to exactly ``n``** -- a node summing to fewer points describes a
      configuration of ``< n`` points, which the search may legitimately refute while
      saying nothing whatever about ``n``;
    * the first cell has minimal level, the FIFO invariant the branching step relies on to
      pick "a largest cell" as ``node[0]`` without searching.
    """
    if not isinstance(node, (list, tuple)) or not node:
        raise CheckpointError(f"frontier node is empty or not a list: {node!r}")
    pairs: list[tuple[Cell, int]] = []
    total = 0
    for entry in node:
        if not isinstance(entry, (list, tuple)) or len(entry) != 2:
            raise CheckpointError(f"frontier entry is not a [cell, multiplicity] pair: {entry!r}")
        raw_cell, mult = entry
        cell = tuple(raw_cell) if isinstance(raw_cell, (list, tuple)) else raw_cell
        if not is_valid_cell(cell):
            raise CheckpointError(
                f"frontier entry names {raw_cell!r}, which is not a cell of the "
                f"subdivision of the container"
            )
        if cell[0] > max_level:
            raise CheckpointError(
                f"frontier cell {cell!r} is at level {cell[0]} > max_level {max_level}; "
                f"the branching cannot produce it"
            )
        if not isinstance(mult, int) or isinstance(mult, bool) or mult < 1:
            raise CheckpointError(f"frontier multiplicity {mult!r} is not a positive integer")
        pairs.append((cell, mult))
        total += mult
    cells = [cell for cell, _ in pairs]
    if len(set(cells)) != len(cells):
        raise CheckpointError(f"frontier node repeats a cell: {node!r}")
    if total != n:
        raise CheckpointError(
            f"frontier node distributes {total} points, but the requested theorem is about "
            f"n = {n}; this node says nothing about n = {n}"
        )
    if cells[0][0] != min(c[0] for c in cells):
        raise CheckpointError(
            f"frontier node does not lead with a minimal-level cell, breaking the "
            f"branching invariant: {node!r}"
        )
    return tuple(pairs)


def load_frontier(
    path: str,
    *,
    n: int,
    d: Fraction,
    max_level: int,
    max_cited: int,
    symmetry: bool,
) -> list[Node]:
    """Load a checkpoint frontier, rejecting anything that is not this exact theorem.

    The parameters are the ones the *caller* is about to prove something about.  Every one
    of them must match what the checkpoint was produced under, because each changes what
    the discarded branches meant:

    ``n``          the frontier's nodes distribute ``n`` points and the pruned branches were
                   pruned for ``n``;
    ``d``          the pair and capacity tests are thresholds in ``d``; a frontier carved at
                   a smaller ``d`` omits branches that are live at a larger one;
    ``max_level``  bounds the resolution the frontier was developed to;
    ``max_cited``  fixes which literature values were allowed to prune, so resuming a
                   literature-pruned frontier under ``--max-cited 2`` would report a run
                   that "depends on no literature" while standing on cited values;
    ``symmetry``   the root-level D3 corner ordering was applied, or was not.

    **What this does not do.** Validation cannot establish the one property a resume really
    needs -- that the frontier *covers* everything the interrupted run had not refuted.
    A checkpoint with half its nodes deleted is still internally consistent, and -- once
    its digest is *recomputed* -- would still yield a false ``proved``.  The mandatory
    digest reduces that to deliberate forgery rather than accident or truncation, which is
    as far as a file-based checkpoint can go; it catches damage, not a determined editor.  So a resumed ``proved`` is only as trustworthy as the file it resumed
    from; a result that must stand on its own should be produced by an uninterrupted run,
    and ``prove`` records ``resumed_from`` in its output so a reader can tell the
    difference.
    """
    try:
        with open(path) as fh:
            payload = json.load(fh)
    except json.JSONDecodeError as exc:
        raise CheckpointError(f"{path}: not valid JSON ({exc})") from exc
    if not isinstance(payload, dict):
        raise CheckpointError(f"{path}: checkpoint is not a JSON object")

    schema = payload.get("schema")
    if schema != CHECKPOINT_SCHEMA:
        raise CheckpointError(
            f"{path}: checkpoint schema {schema!r}, expected {CHECKPOINT_SCHEMA}.  "
            f"Checkpoints written before frontier integrity fields existed (schema 0, no "
            f"'schema' key) are not resumable: their frontier can be truncated or edited "
            f"undetectably, and a short frontier closes early as a false 'proved'.  Re-run "
            f"to produce a current checkpoint."
        )

    status = payload.get("status")
    if status not in RESUMABLE_STATUSES:
        raise CheckpointError(
            f"{path}: checkpoint status {status!r} carries no frontier "
            f"(resumable statuses: {', '.join(RESUMABLE_STATUSES)})"
        )

    expected = {
        "n": n,
        "d": str(d),
        "max_level": max_level,
        "max_cited": max_cited,
        "symmetry": symmetry,
    }
    for key, want in expected.items():
        if key not in payload:
            raise CheckpointError(
                f"{path}: checkpoint does not record {key!r}, so it cannot be shown to be "
                f"a checkpoint of the requested theorem"
            )
        got = payload[key]
        if key == "d":
            try:
                same = Fraction(str(got)) == d
            except (TypeError, ValueError, ZeroDivisionError) as exc:
                raise CheckpointError(f"{path}: checkpoint d={got!r} is not a rational") from exc
        else:
            same = type(got) is type(want) and got == want
        if not same:
            raise CheckpointError(
                f"{path}: checkpoint was produced with {key}={got!r}, but this run requests "
                f"{key}={want!r}.  Resuming would report a result for the wrong theorem."
            )

    raw = payload.get("frontier")
    if not isinstance(raw, list):
        raise CheckpointError(f"{path}: checkpoint has no frontier list")
    if not raw:
        raise CheckpointError(
            f"{path}: frontier is empty.  A {status!r} checkpoint is only written while "
            f"nodes remain, and an empty stack would be reported as 'proved' without "
            f"examining any configuration."
        )
    count = payload.get("frontier_count")
    if count != len(raw):
        raise CheckpointError(
            f"{path}: frontier holds {len(raw)} nodes but the checkpoint records "
            f"{count!r}; the file has been truncated or edited"
        )
    digest = payload.get("frontier_digest")
    if digest != frontier_digest(raw):
        raise CheckpointError(
            f"{path}: frontier digest mismatch; the file has been edited since it was "
            f"written"
        )
    return [validate_node(node, n=n, max_level=max_level) for node in raw]
