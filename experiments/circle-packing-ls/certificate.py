"""Turn a float candidate into a certificate the exact checker can consume.

WHAT THIS IS, AND WHAT IT IS NOT
--------------------------------
``ls.py`` produces floats.  The problem's ``RULES.md`` SS2 bans bare floats in a
certificate, for the reason its SS0 gives: an optimiser's output is always *slightly*
infeasible, and a float certificate cannot tell that apart from a real packing.  So this
module does the only honest thing available to a float generator — it **snaps the
configuration to exact rationals and then inflates the reported side length until the
rational configuration is exactly feasible.**

The result is a genuine, exactly-feasible upper bound that is *weaker* than the float
optimum by roughly 1e-11, and is therefore never a record claim.  That is the point: an
honest slightly-loose certificate is worth more than a tight one you cannot check.

The feasibility test in ``exact_feasible`` below is exact integer arithmetic and is
**our own**.  Under ``problems/circle-packing-equilateral-triangle/RULES.md`` SS3 that is
not verification: a certificate earns ``verified:review`` only when the *other* agent's
independently written checker confirms it.  Everything here stays ``numerical``.

The output schema is the one pinned in that ``RULES.md`` SS2, matched field for field
against ``experiments/circle-packing-checker/certificates/n010-triangular.json``.

CONVENTIONS (copied from the spec, not reinterpreted)
-----------------------------------------------------
* Point formulation: ``n`` points at pairwise distance ``>= 2`` in an equilateral
  triangle of side ``d``, and ``side_length`` reports ``s = d + 2*sqrt(3)``.
* Canonical placement ``A = (0,0)``, ``B = (d,0)``, ``C = (d/2, d*sqrt(3)/2)``.  We
  translate the snapped configuration into this placement; no rotation is applied and
  none is searched over.
* All inequalities non-strict.

AVOIDING sqrt(3) IN THE ARITHMETIC
----------------------------------
Containment in the canonical triangle is ``y >= 0``, ``sqrt(3) x >= y`` and
``sqrt(3)(d - x) >= y``.  With ``x, y`` rational and ``y >= 0`` these are equivalent to

    x >= 0  and  3 x^2 >= y^2,        (d - x) >= 0  and  3 (d - x)^2 >= y^2,

which are exact integer comparisons.  Squaring is safe *only* because the sign of the
left factor is checked first; that check is not decoration.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SQRT3 = math.sqrt(3.0)

#: Denominator used when snapping floats to rationals.  1e-15 is below double precision,
#: so the snap loses nothing the float ever had.
SNAP_DEN = 10**15

#: Relative inflation applied before snapping, so the rational configuration has genuine
#: slack rather than sitting exactly on the constraint.  Must comfortably exceed the
#: snapping error (~1e-15 absolute on coordinates of size <= 15).
INFLATE = Fraction(1, 10**11)


def _inv_sqrt3_upper(digits: int = 30) -> Fraction:
    """A rational ``R >= 1/sqrt(3)``, certified by ``3 R^2 >= 1``.

    Used only to *choose* a safe triangle side; the feasibility of that choice is then
    re-established from scratch by ``exact_feasible``, so an error here would show up as
    a rejected certificate, never as an accepted bad one.
    """
    N = 10**digits
    k = math.isqrt((N * N + 2) // 3)
    while 3 * k * k < N * N:
        k += 1
    R = Fraction(k, N)
    assert 3 * R.numerator**2 >= R.denominator**2
    return R


INV_SQRT3 = _inv_sqrt3_upper()


def _snap(value, den: int = SNAP_DEN) -> Fraction:
    """Nearest multiple of ``1/den``, computed in exact rational arithmetic.

    ``Fraction(float)`` is exact and ``round(Fraction)`` is exact, so no bit is lost to
    the intermediate.  Doing this as ``round(value * den) / den`` in float would silently
    overflow the 53-bit mantissa once ``value * den`` passes 2**53 -- which it does, since
    coordinates reach ~15 and ``den`` is 1e15.
    """
    return Fraction(round(Fraction(value) * den), den)


def _ceil_snap(value: Fraction, den: int = SNAP_DEN) -> Fraction:
    """Smallest multiple of ``1/den`` that is ``>= value``.  Exact."""
    return Fraction(-((-value.numerator * den) // value.denominator), den)


def min_pair_sq(coords) -> Fraction:
    """Exact minimum squared pairwise distance of rational coordinate strings."""
    pts = [(Fraction(a), Fraction(b)) for a, b in coords]
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            v = dx * dx + dy * dy
            if best is None or v < best:
                best = v
    return best if best is not None else Fraction(0)


def _fmt(f: Fraction) -> str:
    """Exact rational as a string the checker's allowlisted grammar accepts.

    Never a decimal: ``RULES.md`` SS2 bans decimal strings in exact fields precisely
    because truncated optimiser output is indistinguishable from an exact value.
    """
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def build_certificate(
    n: int,
    unit_points: np.ndarray,
    *,
    note: str = "",
    beats_record: str | None = None,
    source: str = "experiments/circle-packing-ls",
) -> dict:
    """Snap a unit-triangle float candidate into an exactly-feasible rational certificate.

    ``unit_points`` are ``n`` floats in the unit triangle (the ``ls.py`` formulation).
    Returns the certificate dict; call ``exact_feasible`` on it before trusting it.
    """
    pts = np.asarray(unit_points, dtype=float)
    if pts.shape != (n, 2):
        raise ValueError(f"expected shape ({n}, 2), got {pts.shape}")

    m = float(
        min(
            math.dist(pts[i], pts[j])
            for i in range(n)
            for j in range(i + 1, n)
        )
    ) if n >= 2 else float("inf")
    if not (m > 0.0):
        raise ValueError("degenerate candidate: two points coincide")

    # Scale so that pairwise distances are >= 2 with room to absorb the snap.
    sigma = Fraction(2) / _snap(m) * (1 + INFLATE)

    snapped = [
        (_snap(sigma * Fraction(float(px))), _snap(sigma * Fraction(float(py))))
        for px, py in pts
    ]

    # Translate into the canonical placement A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2).
    # ``INV_SQRT3`` has a 1e30 denominator, so the shift and the side are rounded back
    # onto the 1e-15 grid before use -- otherwise every coordinate would carry a
    # 40-digit denominator and the exact checker would do 40-digit integer arithmetic
    # for no gain.  Both are rounded *up*, i.e. away from feasibility's boundary:
    # a larger ``tx`` only moves points further from edge AC, and ``d`` is recomputed
    # from the final placed points, so rounding it up can only add slack at edge BC.
    ty = _ceil_snap(max(Fraction(0), -min(p[1] for p in snapped)))
    shifted_y = [p[1] + ty for p in snapped]
    tx = _ceil_snap(max(INV_SQRT3 * y - p[0] for p, y in zip(snapped, shifted_y)))
    placed = [(p[0] + tx, y) for p, y in zip(snapped, shifted_y)]
    d = _ceil_snap(max(x + INV_SQRT3 * y for x, y in placed))

    coordinates = [[_fmt(x), _fmt(y)] for x, y in placed]
    s_float = float(d) + 2.0 * SQRT3

    if beats_record is None:
        beats_record = (
            "no. This is a rounded-and-inflated snapshot of floating-point search output, "
            "deliberately loosened by ~1e-11 so that it is exactly feasible over the "
            "rationals; it is weaker than the float optimum it came from and weaker than "
            "the published values in Graham-Lubachevsky (EJC 2 (1995) #A1) and Friedman's "
            "Packing Center. No record is claimed."
        )

    cert = {
        "n": n,
        "claim": "construction",
        "side_length": f"{_fmt(d)} + 2*sqrt(3)",
        "coordinates": coordinates,
        "coordinate_type": "rational",
        "verified_by": (
            "UNVERIFIED. Self-checked only, by certificate.exact_feasible in "
            f"{source} (exact integer arithmetic). Under "
            "problems/circle-packing-equilateral-triangle/RULES.md §3 a certificate "
            "earns verified:review only from the OTHER agent's independently written "
            "checker; this has not had one."
        ),
        "status": "numerical",
        "beats_record": beats_record,
        "_generator": source,
        "_note": (
            "Candidate from a Lubachevsky-Stillinger billiard run, polished by SLSQP, "
            "then snapped to rationals and inflated until exactly feasible. NOT tight: "
            "the reported side_length exceeds the float optimum by roughly 1e-11. "
            + note
        ).strip(),
        "_s_float": s_float,
        "_d_rational": _fmt(d),
    }
    return cert


def exact_feasible(cert: dict) -> tuple[bool, str]:
    """Exact feasibility check of a ``coordinate_type: rational`` certificate.

    Independent of ``experiments/circle-packing-checker`` by construction — it shares no
    code with it — but it is *our* code checking *our* output, so per the problem's
    ``RULES.md`` SS3 it confers no status.  It exists to stop this directory ever emitting
    a certificate that is infeasible, which is the failure that SS0 warns about.

    Returns ``(ok, reason)``.  There is no tolerance parameter anywhere in it.
    """
    if cert.get("coordinate_type") != "rational":
        return False, "exact_feasible only handles coordinate_type 'rational'"

    d = Fraction(cert["_d_rational"])
    pts = [(Fraction(a), Fraction(b)) for a, b in cert["coordinates"]]
    if len(pts) != cert["n"]:
        return False, f"n = {cert['n']} but {len(pts)} coordinates"

    for idx, (x, y) in enumerate(pts):
        if y < 0:
            return False, f"point {idx}: y < 0"
        # sqrt(3) x >= y  with y >= 0
        if x < 0 or 3 * x * x < y * y:
            return False, f"point {idx}: outside edge AC"
        # sqrt(3) (d - x) >= y  with y >= 0
        if d - x < 0 or 3 * (d - x) * (d - x) < y * y:
            return False, f"point {idx}: outside edge BC"

    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            if dx * dx + dy * dy < 4:
                return False, f"pair ({i}, {j}): distance < 2"

    return True, "exactly feasible"
