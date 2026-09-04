"""Dependency preflight for this directory.

WHY mpmath IS DECLARED AND NOT MADE "OPTIONAL".

`certify.py` is the certificate.  It runs a branch-and-bound in which **every
accept/reject decision is an mpmath interval comparison** at `iv.dps = 30`
(with `mp.dps = 50` for the scalar work).  The soundness of the whole lane rests
on those comparisons being outward-rounded: that is what makes "this box is
excluded" a rigorous statement rather than a float guess.

mpmath is therefore not a diagnostic that can be skipped, and it is emphatically
not something to reimplement here.  Hand-rolling interval arithmetic to avoid a
dependency would replace a widely-tested library with a fresh one at exactly the
point where an error is invisible and fatal -- the wrong direction on a single
rounding mode silently turns a non-proof into an apparent proof.  (Compare
../packing-r6-stairthm, where a dependency really was replaced by a stdlib
`Lin` class; that was trivial exact linear-form arithmetic over Fractions, not
outward-rounded interval arithmetic, and it still needed its own justification.)

So mpmath is DECLARED, and this module turns a bare ImportError traceback into
an actionable message with exit code 2.

numpy is a different case and is listed as an OPTIONAL extra: it is used only by
`scan_lattice.py` and `probe_forcing.py`, which are float *measurements*, not
part of the certificate.  The advertised `python3 run_all.py` does not need it.

STATUS (unchanged by this file): numerical (the branch-and-bound), sketch (the
reduction and F1-F4).  Not assumable.
"""
import importlib.util
import sys

# module -> (requirement spec, version this lane was actually re-run with)
REQUIRED = {
    "mpmath": ("mpmath>=1.3.0", "1.3.0"),
}

# Used ONLY by the float measurement scripts, never by the certificate.
OPTIONAL = {
    "numpy": ("numpy>=1.26", "2.5.2", "scan_lattice.py, probe_forcing.py"),
}


def require(script="run_all.py"):
    missing = [(m, spec, tested) for m, (spec, tested) in REQUIRED.items()
               if importlib.util.find_spec(m) is None]
    if not missing:
        return
    e = sys.stderr
    print("This lane requires dependencies that are not installed.", file=e)
    print("", file=e)
    for m, spec, tested in missing:
        print("  missing: %-7s  required: %-16s  tested with: %s" % (m, spec, tested), file=e)
    print("", file=e)
    print("  cd experiments/packing-r5-eo7", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install %s"
          % " ".join("'%s'" % spec for _, spec, _ in missing), file=e)
    print("  .venv/bin/python %s" % script, file=e)
    print("", file=e)
    print("mpmath is a REAL requirement, not an optional diagnostic: every", file=e)
    print("accept/reject decision in certify.py is an outward-rounded interval", file=e)
    print("comparison at iv.dps = 30.  There is no stdlib fallback, and", file=e)
    print("reimplementing interval arithmetic here would be a soundness hazard.", file=e)
    print("", file=e)
    print("numpy is NOT needed for this command; it is used only by the float", file=e)
    print("measurement scripts scan_lattice.py and probe_forcing.py.", file=e)
    raise SystemExit(2)


def require_numpy(script):
    """Preflight for the FLOAT MEASUREMENT scripts only (not the certificate)."""
    if importlib.util.find_spec("numpy") is not None:
        return
    spec, tested, users = OPTIONAL["numpy"]
    e = sys.stderr
    print("%s is a float measurement script and needs numpy, which is not installed."
          % script, file=e)
    print("", file=e)
    print("  missing: numpy    required: %-16s  tested with: %s" % (spec, tested), file=e)
    print("", file=e)
    print("  cd experiments/packing-r5-eo7", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install 'mpmath>=1.3.0' '%s'" % spec, file=e)
    print("  .venv/bin/python %s" % script, file=e)
    print("", file=e)
    print("This does NOT affect the certificate: `python3 run_all.py` and", file=e)
    print("`python3 exact_check.py` need mpmath only.  numpy is used here by", file=e)
    print("%s, which produce measurements, not proofs." % users, file=e)
    raise SystemExit(2)
