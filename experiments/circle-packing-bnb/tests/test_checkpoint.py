"""Resume must never turn a checkpoint into a proof of a different theorem.

A ``--resume`` replaces the root node -- "the ``n`` points are somewhere in the
container" -- with a frontier asserted to cover every branch the interrupted run had not
yet refuted.  If that assertion fails, the exhaustion closes over a strict subset of the
configuration space and prints ``proved`` for something it never proved.  There is no
tolerance and no partial credit here: the output of this program is a claim that a case
was ruled out, so every doubtful checkpoint must be rejected.

The headline case is the one Codex found in review of PR #56: at the pre-fix head,

    python -m cpbnb prove --n 2 --d 2 --max-level 6 --max-cited 2 \\
        --resume out/n12-d7_0-L6.ckpt.json

returned ``proved`` and printed ``d(2) > 2`` -- refuted by the two vertices of a side-2
equilateral triangle, which are at distance exactly 2.  ``load_frontier`` discarded the
checkpoint's ``n``, ``d``, ``max_level``, ``max_cited`` and ``symmetry``, and the n=12
frontier (cells far too small to hold 2 points at distance 2) pruned out instantly.

:func:`test_false_proof_class` is the regression net for the whole class, not just that
command line.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import pytest

from cpbnb.lattice import DOWN, ROOT, UP, is_valid_cell, subdivide
from cpbnb.search import (
    CHECKPOINT_SCHEMA,
    CheckpointError,
    Prover,
    frontier_digest,
    load_frontier,
    validate_node,
)

# The parameters the reference checkpoint below is produced under.
GOOD = dict(n=7, d=Fraction("53/10"), max_level=7, max_cited=2, symmetry=True)


@pytest.fixture()
def checkpoint(tmp_path: Path) -> Path:
    """A genuine, unfinished checkpoint: status ``timeout`` with a real frontier."""
    path = tmp_path / "ck.json"
    p = Prover(GOOD["n"], GOOD["d"], GOOD["max_level"], GOOD["max_cited"])
    res = p.run(node_limit=20_000, checkpoint_path=str(path), checkpoint_every=20_000)
    assert res["status"] == "timeout"
    payload = json.loads(path.read_text())
    assert payload["schema"] == CHECKPOINT_SCHEMA
    assert payload["frontier_count"] == len(payload["frontier"]) > 0
    return path


def edited(path: Path, tmp_path: Path, **changes) -> str:
    """A copy of the checkpoint with fields replaced (digest deliberately *not* refreshed)."""
    payload = json.loads(path.read_text())
    payload.update(changes)
    out = tmp_path / f"edited-{abs(hash(tuple(sorted(changes))))}.json"
    out.write_text(json.dumps(payload))
    return str(out)


# -- the honest path still works ------------------------------------------------------


def test_matching_resume_is_accepted_and_finishes_the_proof(checkpoint):
    frontier = load_frontier(str(checkpoint), **GOOD)
    assert frontier
    rest = Prover(GOOD["n"], GOOD["d"], GOOD["max_level"], GOOD["max_cited"]).run(
        initial_stack=frontier
    )
    assert rest["status"] == "proved"


def test_d_is_compared_as_a_rational_not_a_string(checkpoint):
    """``--d 5.3`` and ``--d 53/10`` name the same side and must both resume."""
    assert load_frontier(str(checkpoint), **{**GOOD, "d": Fraction("5.3")})


# -- every parameter mismatch is rejected ---------------------------------------------


@pytest.mark.parametrize(
    "field, wrong",
    [
        ("n", 2),
        ("n", 8),
        ("d", Fraction(2)),
        ("d", Fraction("53/10") - Fraction(1, 1000)),
        ("d", Fraction(100)),
        ("max_level", 6),
        ("max_level", 8),
        ("max_cited", 15),
        ("symmetry", False),
    ],
)
def test_every_parameter_mismatch_is_rejected(checkpoint, field, wrong):
    with pytest.raises(CheckpointError):
        load_frontier(str(checkpoint), **{**GOOD, field: wrong})


def test_literature_provenance_cannot_be_laundered(tmp_path):
    """A frontier pruned with cited d(k) must not be resumable as a ``--max-cited 2`` run.

    Otherwise the result JSON reports ``max_cited: 2`` -- the experiment's "depends on no
    literature at all" mode -- while the frontier it stands on was carved using the cited
    optimal side lengths.  The bound might still be true; the provenance would be a lie.
    """
    path = tmp_path / "cited.json"
    p = Prover(12, Fraction("73/10"), 6, 11)
    p.run(node_limit=20_000, checkpoint_path=str(path), checkpoint_every=20_000)
    with pytest.raises(CheckpointError, match="max_cited"):
        load_frontier(
            str(path), n=12, d=Fraction("73/10"), max_level=6, max_cited=2, symmetry=True
        )


# -- structural validation of an untrusted frontier -----------------------------------


def test_empty_frontier_is_never_a_proof(checkpoint, tmp_path):
    """The classic vacuous proof: no nodes to examine, so every branch is 'closed'."""
    with pytest.raises(CheckpointError, match="empty"):
        load_frontier(edited(checkpoint, tmp_path, frontier=[], frontier_count=0,
                             frontier_digest=frontier_digest([])), **GOOD)


def test_prover_refuses_an_empty_initial_stack():
    """Also closed at the API level, for callers that bypass ``load_frontier``."""
    with pytest.raises(CheckpointError, match="empty frontier"):
        Prover(7, Fraction("53/10"), 7, 2).run(initial_stack=[])


def test_finished_checkpoint_is_not_silently_restarted(checkpoint, tmp_path):
    """A ``proved``/``unresolved`` checkpoint stores no frontier.

    Before the fix this loaded as ``[]`` and silently started a *fresh* search, so the
    output answered a question the user had not asked.
    """
    for status in ("proved", "unresolved"):
        payload = json.loads(checkpoint.read_text())
        del payload["frontier"]
        payload["status"] = status
        p = tmp_path / f"{status}.json"
        p.write_text(json.dumps(payload))
        with pytest.raises(CheckpointError, match="no frontier"):
            load_frontier(str(p), **GOOD)


def test_metadata_free_checkpoint_is_rejected(checkpoint, tmp_path):
    """A frontier with no recorded parameters cannot be shown to be about this theorem."""
    payload = json.loads(checkpoint.read_text())
    bare = tmp_path / "bare.json"
    bare.write_text(json.dumps({"status": "timeout", "frontier": payload["frontier"]}))
    with pytest.raises(CheckpointError):
        load_frontier(str(bare), **GOOD)


@pytest.mark.parametrize(
    "frontier, why",
    [
        ([[]], "a node with no cells"),
        ([[[[4, UP, 0, 0], 1]]], "multiplicities summing to fewer than n"),
        ([[[[4, UP, 0, 0], 3], [[4, UP, 1, 0], 5]]], "multiplicities summing to more than n"),
        ([[[[3, UP, 999, 999], 7]]], "a cell outside the container"),
        ([[[[3, DOWN, 7, 7], 7]]], "a down-cell outside the container"),
        ([[[[9, UP, 0, 0], 7]]], "a cell deeper than max_level"),
        ([[[[-1, UP, 0, 0], 7]]], "a negative level"),
        ([[[[2, 5, 0, 0], 7]]], "an orientation that is neither up nor down"),
        ([[[[2, UP, 0], 7]]], "a cell that is not four integers"),
        ([[[[2, UP, 0, 0], "7"]]], "a multiplicity that is not an integer"),
        ([[[[2, UP, 0, 0], 0], [[2, UP, 1, 0], 7]]], "a zero multiplicity"),
        ([[[[2, UP, 0, 0], -1], [[2, UP, 1, 0], 8]]], "a negative multiplicity"),
        ([[[[2, UP, 0, 0], 3], [[2, UP, 0, 0], 4]]], "the same cell twice"),
        ([[[[4, UP, 0, 0], 3], [[1, UP, 0, 0], 4]]], "a non-minimal leading cell"),
        ([[[[2, UP, 0, 0], 7]], []], "a bad node after a good one"),
        (["not a node"], "a node that is not a list"),
        ([[["not a cell", 7]]], "a cell that is not a list"),
    ],
)
def test_malformed_frontier_is_rejected(checkpoint, tmp_path, frontier, why):
    path = edited(
        checkpoint,
        tmp_path,
        frontier=frontier,
        frontier_count=len(frontier),
        frontier_digest=frontier_digest(frontier),
    )
    with pytest.raises(CheckpointError), open(path):
        load_frontier(path, **GOOD)


def test_truncated_frontier_is_detected(checkpoint, tmp_path):
    """Deleting nodes leaves a *structurally perfect* frontier that closes early.

    This is the residual danger the digest exists for: every surviving node is a genuine
    node of a genuine run, so no per-node check can see the problem.
    """
    payload = json.loads(checkpoint.read_text())
    short = tmp_path / "short.json"
    payload["frontier"] = payload["frontier"][:2]
    short.write_text(json.dumps(payload))
    with pytest.raises(CheckpointError, match="truncated|digest"):
        load_frontier(str(short), **GOOD)


def test_schema_version_is_enforced(checkpoint, tmp_path):
    for schema in (None, 0, CHECKPOINT_SCHEMA + 1, "1"):
        payload = json.loads(checkpoint.read_text())
        if schema is None:
            del payload["schema"]
        else:
            payload["schema"] = schema
        p = tmp_path / f"schema-{schema}.json"
        p.write_text(json.dumps(payload))
        with pytest.raises(CheckpointError, match="schema"):
            load_frontier(str(p), **GOOD)


def test_non_json_and_missing_files_are_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with pytest.raises(CheckpointError, match="not valid JSON"):
        load_frontier(str(bad), **GOOD)
    arr = tmp_path / "arr.json"
    arr.write_text("[1, 2, 3]")
    with pytest.raises(CheckpointError, match="not a JSON object"):
        load_frontier(str(arr), **GOOD)
    with pytest.raises(OSError):
        load_frontier(str(tmp_path / "nope.json"), **GOOD)


# -- the cell-validity predicate -------------------------------------------------------


def test_is_valid_cell_matches_the_subdivision_exactly():
    """The predicate must admit precisely the cells ``subdivide`` can produce."""
    cells = {ROOT}
    for _ in range(5):
        cells = {c for parent in cells for c in subdivide(parent)}
        assert all(is_valid_cell(c) for c in cells)
        level = next(iter(cells))[0]
        n = 1 << level
        # everything in the bounding box that the predicate rejects is genuinely absent
        for orient in (UP, DOWN):
            for i in range(n + 2):
                for j in range(n + 2):
                    cell = (level, orient, i, j)
                    assert is_valid_cell(cell) == (cell in cells)


def test_validate_node_accepts_genuine_nodes():
    node = validate_node([[[1, UP, 0, 0], 4], [[2, DOWN, 0, 0], 3]], n=7, max_level=7)
    assert node == (((1, UP, 0, 0), 4), ((2, DOWN, 0, 0), 3))


# -- end to end: the exact false proof from the review ---------------------------------


def cli(*args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "cpbnb", *args], capture_output=True, text=True, cwd=cwd
    )


def test_false_proof_class(tmp_path):
    """The reviewed command line, end to end: it must not print PROVED, and must exit != 0.

    Asserting on the process is deliberate.  The bug was not in the search -- the search
    was right -- it was in the CLI accepting a frontier for one theorem while announcing a
    conclusion about another, so the regression net has to cover the announcement too.
    """
    root = Path(__file__).resolve().parent.parent
    ck = tmp_path / "n12.ckpt.json"
    made = cli("prove", "--n", "12", "--d", "7", "--max-level", "6", "--max-cited", "2",
               "--node-limit", "20000", "--checkpoint", str(ck), cwd=root)
    assert made.returncode == 0
    assert json.loads(ck.read_text())["status"] == "timeout"

    # d(2) = 2: two vertices of a side-2 triangle are at distance exactly 2, so ANY output
    # claiming d(2) > 2 is false.
    bad = cli("prove", "--n", "2", "--d", "2", "--max-level", "6", "--max-cited", "2",
              "--resume", str(ck), cwd=root)
    assert bad.returncode != 0, bad.stdout
    assert "PROVED" not in bad.stdout
    assert '"proved"' not in bad.stdout
    assert "refusing to resume" in bad.stderr

    # and the same for a resume that only gets *one* parameter wrong
    for wrong in (["--n", "13"], ["--d", "7.5"], ["--max-level", "7"], ["--max-cited", "9"],
                  ["--no-symmetry"]):
        args = {"--n": "12", "--d": "7", "--max-level": "6", "--max-cited": "2"}
        flags = []
        if wrong[0] == "--no-symmetry":
            flags = ["--no-symmetry"]
        else:
            args[wrong[0]] = wrong[1]
        res = cli("prove", *[x for kv in args.items() for x in kv], *flags,
                  "--resume", str(ck), cwd=root)
        assert res.returncode != 0 and "PROVED" not in res.stdout, wrong
