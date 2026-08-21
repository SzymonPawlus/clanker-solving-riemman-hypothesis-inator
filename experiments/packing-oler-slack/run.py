"""Oler slack localisation: controls, atlas, and the face-excess probe.

Single command:  python3 run.py        (stdlib only, no dependencies, no seeds)

Sections, in the order the issue (#78) fixes them:

  1. controls   -- the decomposition identity must give exactly zero slack, and
                   exactly zero excess on every face and boundary edge, for the
                   triangular lattices n = 3, 6, 10.  Secondary kill-criterion.
  2. atlas      -- exactly where the slack lives for every exact certificate in
                   the repo (n = 1..10, 14, 15, 20, 21) plus results/.
  3. probe      -- is the *total* face excess >= 0 for unit-separated sets?
                   (the hypothesis a floored-perimeter strengthening of Oler
                   would need).  Primary kill-criterion.
  4. floored    -- consistency of the floored-perimeter *conclusion* against
                   every optimum this repo records as cited.
  5. best-known -- the same conclusion against every best-known construction the
                   repo records, n = 4..36 (Graham-Lubachevsky 1995).
  6. implication-- exact arithmetic showing that conclusion implies the full
                   Erdos-Oler conjecture, which is why nobody here should try to
                   prove it (RULES.md §7).

Everything printed is either exact (rational or in Q(sqrt3, sqrt11)) or a
rigorous rational interval.  No floating point enters a decision anywhere; the
`float(...)` values in the output are for reading only.
"""

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exact import Alg, Ival, parse_alg, sqrt_bounds          # noqa: E402
from geometry import Decomposition                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PROBLEM = os.path.join(REPO, "problems", "circle-packing-equilateral-triangle")
CERTS = os.path.join(PROBLEM, "attacks", "exact-algebraic-constructions", "certificates")
RESULTS = os.path.join(PROBLEM, "results")
OUT = os.path.join(HERE, "out")

HALF = F(1, 2)


def load_points(path):
    """Certificate -> point list in Oler normalisation (minimum separation 1).

    Certificates use minimum separation 2 (problem RULES.md §2), Oler's
    inequality is stated at minimum separation 1, so every coordinate is halved.
    """
    with open(path) as fh:
        cert = json.load(fh)
    points = [
        (parse_alg(x) * HALF, parse_alg(y) * HALF) for x, y in cert["coordinates"]
    ]
    return cert, points


def certificate_files():
    files = [(os.path.join(CERTS, f), f) for f in sorted(os.listdir(CERTS))]
    files += [(os.path.join(RESULTS, f), f) for f in sorted(os.listdir(RESULTS))]
    return [(p, f) for p, f in files if f.endswith(".json")]


# --- 1. controls -----------------------------------------------------------


def controls():
    print("=" * 78)
    print("1. CONTROLS -- triangular lattices must give exactly zero slack")
    print("=" * 78)
    rows, ok = [], True
    for n in (3, 6, 10):
        cert, points = load_points(os.path.join(CERTS, f"n{n:03d}-exact.json"))
        dec = Decomposition(points, label=f"n={n} lattice")
        exact_zero_faces = all(e.sign() == 0 for e in dec.face_excess)
        exact_unit_edges = all(l2 == 1 for l2 in dec.edge_len2)
        slack_zero = dec.slack.lo == 0 and dec.slack.hi == 0
        passed = (
            dec.check_identity()
            and exact_zero_faces
            and exact_unit_edges
            and dec.total_face_excess.sign() == 0
            and slack_zero
        )
        ok = ok and passed
        rows.append(
            {
                "n": n,
                "faces": dec.faces,
                "expected_faces": 2 * dec.n - dec.b - 2,
                "every_face_excess_exactly_zero": exact_zero_faces,
                "every_boundary_edge_exactly_length_1": exact_unit_edges,
                "total_face_excess_exact": str(dec.total_face_excess),
                "oler_slack_enclosure": repr(dec.slack),
                "passed": passed,
            }
        )
        print(
            f"  n={n:2d}  faces={dec.faces:2d} (=2n-b-2={2*dec.n-dec.b-2:2d})  "
            f"face excess all exactly 0: {exact_zero_faces}  "
            f"boundary edges all exactly length 1: {exact_unit_edges}  "
            f"slack={dec.slack}  -> {'PASS' if passed else 'FAIL'}"
        )
    print(f"\n  controls: {'PASS' if ok else 'FAIL'}\n")
    return ok, rows


# --- 2. atlas --------------------------------------------------------------


def disp(x):
    """Display helper: a rounding artefact of size 1e-30 is printed as 0."""
    return 0.0 if abs(x) < 1e-30 else x


def stage_split(cert, dec):
    """Split the slack of Oler's *triangle* bound into its two stages.

    Oler bounds n twice over: first by the hull, n <= (2/sqrt3)A(H) + M(H)/2 + 1,
    then by relaxing the hull to the containing triangle T.  So

        [a^2/2 + 3a/2 + 1] - n  =  stage 1 (hull slack)  +  stage 2 (hull -> T),

    with stage 2 = (2/sqrt3)(A(T) - A(H)) + (M(T) - M(H))/2.  The repo's
    `attacks/oler-lower-bound/README.md` §2.1 flags that both stages can lose but
    does not say how much each loses; this is that measurement.
    """
    a = parse_alg(cert["point_triangle_side"]) * HALF        # Oler normalisation
    two_over_root3 = Alg(0, F(2, 3), 0, 0)
    area_t = Alg.sqrt(3) * F(1, 4) * a * a
    stage2 = Ival.of(two_over_root3 * (area_t - dec.area)) + (
        Ival.of(Alg(3) * a) - dec.perimeter
    ) * F(1, 2)
    total = Ival.of(two_over_root3 * area_t) + Ival.of(Alg(3) * a) * F(1, 2) + 1 - dec.n
    return a, stage2, total


def atlas():
    print("=" * 78)
    print("2. SLACK ATLAS -- where the slack sits, for every exact certificate")
    print("=" * 78)
    print("  stage 1 = slack of Oler applied to the hull; stage 2 = hull -> triangle")
    print(
        f"  {'file':<26} {'n':>3} {'b':>3} {'i':>3} {'F':>3} "
        f"{'face exc':>11} {'edge exc':>11} {'stage 1':>11} "
        f"{'stage 2':>11} {'total':>11}  id"
    )
    rows = []
    for path, name in certificate_files():
        cert, points = load_points(path)
        n = cert["n"]
        if n < 3:
            print(f"  {name:<26} {n:>3}   -- degenerate hull, identity not applicable")
            rows.append({"file": name, "n": n, "degenerate": True})
            continue
        dec = Decomposition(points, label=name)
        s = dec.summary()
        a, stage2, total = stage_split(cert, dec)
        s |= {
            "file": name,
            "point_triangle_side_oler_norm": str(a),
            "stage2_hull_to_triangle": stage2.mid(),
            "oler_triangle_slack_total": total.mid(),
            "stage1_is_exactly_zero": dec.slack.lo == 0 and dec.slack.hi == 0,
        }
        rows.append(s)
        print(
            f"  {name:<26} {s['n']:>3} {s['boundary_points']:>3} "
            f"{s['interior_points']:>3} {s['faces']:>3} "
            f"{disp(s['total_face_excess']):>11.7f} {disp(s['boundary_excess']):>11.7f} "
            f"{disp(s['oler_slack']):>11.7f} {disp(stage2.mid()):>11.7f} "
            f"{disp(total.mid()):>11.7f}  "
            f"{'ok' if dec.check_identity() else 'FAIL'}"
        )
    print()
    return rows


# --- 3. the probe ----------------------------------------------------------


def flat_arc(m):
    """m+1 points on a concave rational arc: p_i = (i, i(m-i)/m^3).

    Consecutive points are at distance >= 1 (their x-gap alone is 1) and
    non-consecutive ones at distance >= 2, so the set is unit-separated.  The
    second difference of the y-values is -2/m^3 < 0, so every point is a hull
    vertex.  The hull area is O(1/1) while the point count grows.
    """
    c = F(1, m ** 3)
    return [(Alg(F(i)), Alg(c * i * (m - i))) for i in range(m + 1)]


def probe():
    print("=" * 78)
    print("3. PROBE -- is the total face excess >= 0 for unit-separated sets?")
    print("=" * 78)

    cases = []

    # minimal counterexample: one obtuse triangle, all sides >= 1
    tri = [(Alg(0), Alg(0)), (Alg(1), Alg(0)), (Alg(2), Alg(F(1, 2)))]
    cases.append(("obtuse triangle (0,0),(1,0),(2,1/2)", tri))

    # a family, to show the deficit is unbounded rather than a small-n artefact
    for m in (3, 4, 6, 8, 12, 16):
        cases.append((f"flat arc, m={m} (n={m+1})", flat_arc(m)))

    rows = []
    print(
        f"  {'configuration':<38} {'n':>3} {'min sep^2':>10} "
        f"{'total face excess':>18} {'Oler slack':>12}"
    )
    for label, points in cases:
        dec = Decomposition(points, label=label)
        assert dec.check_identity(), f"identity failed on {label}"
        sep_ok = dec.min_sep2 >= 1
        rows.append(
            dec.summary()
            | {
                "unit_separated": sep_ok,
                "min_separation_sq_float": dec.min_sep2.float(),
            }
        )
        print(
            f"  {label:<38} {dec.n:>3} {dec.min_sep2.float():>10.6f} "
            f"{dec.total_face_excess.float():>18.9f} {dec.slack.mid():>12.9f}"
            + ("" if sep_ok else "   <-- NOT unit separated")
        )
        assert sep_ok, "counterexample must satisfy the separation hypothesis"

    refuted = any(r["total_face_excess_sign"] < 0 for r in rows)
    print(
        "\n  face-excess-nonnegativity hypothesis: "
        + ("REFUTED (exact, see negative column above)" if refuted else "not refuted")
    )
    print(
        "  note: the total face excess is triangulation-independent "
        "(= (2/sqrt3)A - (2n-b-2)/2),\n        so no choice of triangulation "
        "-- Delaunay included -- can repair the sign.\n"
    )
    return refuted, rows


# --- 4. the floored-perimeter conclusion -----------------------------------


def ival_expr(expr):
    """Evaluate an exact closed form such as '4 + 2*sqrt(6)/3' as an interval."""

    def sqrt(k):
        lo, hi = sqrt_bounds(F(k), 60)
        return Ival(lo, hi)

    return Ival(0) + eval(expr, {"__builtins__": {}, "sqrt": sqrt})  # noqa: S307


# s(n) for every n this repo records as settled (problem README, status cited).
# Best-known constructions are handled separately, in section 5.
KNOWN = [
    (1, "2*sqrt(3)", "cited"),
    (2, "2 + 2*sqrt(3)", "cited"),
    (3, "2 + 2*sqrt(3)", "cited"),
    (4, "4*sqrt(3)", "cited"),
    (5, "4 + 2*sqrt(3)", "cited"),
    (6, "4 + 2*sqrt(3)", "cited"),
    (7, "2 + 4*sqrt(3)", "cited"),
    (8, "2 + 2*sqrt(3) + 2*sqrt(33)/3", "cited"),
    (9, "6 + 2*sqrt(3)", "cited"),
    (10, "6 + 2*sqrt(3)", "cited"),
    (11, "4 + 2*sqrt(3) + 4*sqrt(6)/3", "cited"),
    (12, "4 + 4*sqrt(3)", "cited"),
    (13, "4 + 2*sqrt(6)/3 + 10*sqrt(3)/3", "cited"),
    (14, "8 + 2*sqrt(3)", "cited"),
    (15, "8 + 2*sqrt(3)", "cited"),
    (20, "10 + 2*sqrt(3)", "cited (qualified: Payan abstract only)"),
    (21, "10 + 2*sqrt(3)", "cited"),
]

def exact_or_interval(expr):
    """(kind, value): exact `Alg` when the closed form lies in Q(sqrt3, sqrt11),
    otherwise a rigorous interval (s(11) and s(13) bring in sqrt6)."""
    try:
        return "exact", parse_alg(expr)
    except ValueError:
        return "interval", ival_expr(expr)


def floored_table():
    print("=" * 78)
    print("4. THE FLOORED-PERIMETER CONCLUSION -- consistency, not evidence")
    print("=" * 78)
    print("   claim under test:  n <= a^2/2 + (3/2)*floor(a) + 1,  a = (s(n) - 2 sqrt3)/2")
    print(
        f"  {'n':>3} {'a':>14} {'floor a':>8} {'Oler bound':>12} "
        f"{'floored bound':>14} {'holds':>6}  {'status'}"
    )
    rows = []
    entries = sorted(
        ((n, exact_or_interval(expr), st) for n, expr, st in KNOWN), key=lambda e: e[0]
    )

    for n, (kind, s), status in entries:
        if kind == "exact":
            a = (s - Alg.sqrt(3) * 2) * F(1, 2)
            approx = a.float()
            fl = next(k for k in range(0, 200) if a >= k and a < k + 1)
            oler = a * a * F(1, 2) + a * F(3, 2) + 1
            floored = a * a * F(1, 2) + F(3, 2) * fl + 1
            holds = (floored - n).sign() >= 0
            settles = (floored - (n + 1)).sign() < 0
            oler_settles = (oler - (n + 1)).sign() < 0
            oler_val, floored_val = oler.float(), floored.float()
        else:
            a = (s - ival_expr("2*sqrt(3)")) * F(1, 2)
            approx = a.mid()
            fl = a.floor()
            oler = a * a * F(1, 2) + F(3, 2) * a + 1
            oler_val = oler.mid()
            if fl is None:                       # interval could not decide floor(a)
                floored = floored_val = holds = settles = None
            else:
                floored = a * a * F(1, 2) + F(3, 2) * fl + 1
                floored_val = floored.mid()
                holds = floored.lo >= n
                settles = floored.hi < n + 1
            oler_settles = oler.hi < n + 1
        rows.append(
            {
                "n": n,
                "arithmetic": kind,
                "a": approx,
                "floor_a": fl,
                "oler_bound": oler_val,
                "floored_bound": floored_val,
                "floored_bound_holds": holds,
                "oler_settles": oler_settles,
                "floored_settles": settles,
                "status": status,
            }
        )
        print(
            f"  {n:>3} {approx:>14.9f} {str(fl):>8} {oler_val:>12.6f} "
            f"{'-' if floored_val is None else f'{floored_val:>14.6f}'} "
            f"{str(holds):>6}  {status}"
        )
    print()
    settles = [
        r["n"]
        for r in rows
        if r["status"].startswith("cited")
        and r["floored_settles"]
        and not r["oler_settles"]
    ]
    print(
        "  values where the floored bound would newly pin n exactly (Oler does not): "
        f"{settles}\n"
    )
    return rows


def graham_lubachevsky_table():
    """Test the floored-perimeter conclusion against every best-known packing the
    repo records, n = 4..36, using Graham-Lubachevsky's own 15-significant-digit
    d(n) values as loaded from `experiments/circle-packing-search/reference.py`
    (read-only; loaded rather than retyped so no digit can be transcribed wrong).

    d(n) is the minimum separation in a *unit* triangle, so in Oler normalisation
    the triangle side is a = 1/d(n).  Each row is a configuration that provably
    exists (a published construction), so the conjecture is required to hold on
    every one of them: a single row with `holds = False` would refute it.
    """
    import importlib.util

    ref_path = os.path.join(REPO, "experiments", "circle-packing-search", "reference.py")
    spec = importlib.util.spec_from_file_location("gl_reference", ref_path)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)

    print("=" * 78)
    print("5. THE SAME CONCLUSION vs EVERY BEST-KNOWN PACKING (Graham-Lubachevsky)")
    print("=" * 78)
    print("   d(n) read from experiments/circle-packing-search/reference.py (GL 1995)")
    print("   exact closed forms are used wherever the repo has one; a printed")
    print("   15-s.f. decimal is used only as a +-1 ulp enclosure (see note below)")
    print(
        f"  {'n':>3} {'a = 1/d(n)':>14} {'floor a':>8} {'floored bound':>14} "
        f"{'margin':>10} {'holds':>6}  arithmetic"
    )
    exact_side = {n: expr for n, expr, _ in KNOWN}          # n <= 15, 20, 21
    for k in range(2, 9):                                    # lattice rows T(k), T(k)-1
        t = k * (k + 1) // 2
        exact_side.setdefault(t, f"{2 * (k - 1)} + 2*sqrt(3)")
        exact_side.setdefault(t - 1, f"{2 * (k - 1)} + 2*sqrt(3)")

    rows, violations, undecided = [], [], []
    for n in sorted(ref.GL_D):
        if n in exact_side:
            kind, s = exact_or_interval(exact_side[n])
            # the closed form must agree with GL's printed decimal to within its
            # last digit, or one of the two is wrong and the row is not usable
            printed = F(ref.GL_D[n])
            ulp_p = F(1, 10 ** len(ref.GL_D[n].split(".")[1]))
            s_iv = Ival.of(s) if isinstance(s, Alg) else s
            d_here = 2 / (s_iv - ival_expr("2*sqrt(3)"))
            assert d_here.lo <= printed + ulp_p and d_here.hi >= printed - ulp_p, (
                f"closed form for n={n} disagrees with GL's printed d(n)"
            )
            arith = f"exact ({exact_side[n]})" if kind == "exact" else "enclosure of closed form"
            if kind == "exact":
                a = (s - Alg.sqrt(3) * 2) * F(1, 2)
                fl = next(k for k in range(0, 200) if a >= k and a < k + 1)
                bound = a * a * F(1, 2) + F(3, 2) * fl + 1
                lo = hi = bound.float()
                holds, violated = (bound - n).sign() >= 0, (bound - n).sign() < 0
                a_mid = a.float()
            else:
                a = (s - ival_expr("2*sqrt(3)")) * F(1, 2)
                fl, a_mid = a.floor(), a.mid()
                bound = a * a * F(1, 2) + F(3, 2) * fl + 1
                lo, hi = bound.mid(), bound.mid()
                holds, violated = bound.lo >= n, bound.hi < n
        else:
            # a printed decimal may have been rounded either way: enclose it
            decimal = ref.GL_D[n]
            v = F(decimal)
            ulp = F(1, 10 ** len(decimal.split(".")[1])) if "." in decimal else F(0)
            m = Ival(v - ulp, v + ulp)
            a = 1 / m
            fl, a_mid = a.floor(), a.mid()
            arith = "+-1 ulp enclosure of GL decimal"
            if fl is None:
                undecided.append(n)
                print(f"  {n:>3} {a_mid:>14.9f}   floor(a) undecided from the decimal")
                continue
            bound = a * a * F(1, 2) + F(3, 2) * fl + 1
            lo, hi = bound.lo, bound.hi
            holds, violated = bound.lo >= n, bound.hi < n
        margin = float(lo) - n
        rows.append(
            {
                "n": n,
                "a": a_mid,
                "floor_a": fl,
                "floored_bound": float(lo),
                "margin": margin,
                "holds": holds,
                "refuted": violated,
                "arithmetic": arith,
            }
        )
        if violated:
            violations.append(n)
        print(
            f"  {n:>3} {a_mid:>14.9f} {fl:>8} {float(lo):>14.6f} "
            f"{margin:>10.6f} {str(holds):>6}  {arith}"
        )
    print(
        f"\n  refuting rows: {violations if violations else 'none'} "
        f"(a single one would kill the conjecture); undecided: "
        f"{undecided if undecided else 'none'}"
    )
    tight = sorted(rows, key=lambda r: r["margin"])[:6]
    print("  tightest margins: " + ", ".join(f"n={r['n']} ({r['margin']:.4f})" for r in tight))
    print(
        "\n  NOTE, recorded because it nearly went the other way: feeding the printed\n"
        "  15-s.f. decimals in blind -- i.e. treating d(20), d(27), d(35) = 0.2,\n"
        "  0.166666666666667, 0.142857142857143 as if exact -- makes floor(a) come out\n"
        "  one too small at n = 4, 27, 28, 35, 36 and reports five refutations of the\n"
        "  conjecture.  All five are artefacts of the last printed digit: those n are the\n"
        "  lattice cases T(k), T(k)-1, where a = k-1 is exactly an integer.  A conjecture\n"
        "  is not refuted by the rounding of a table.\n"
    )
    return rows


def erdos_oler_implication(kmax=12):
    """Exact check that the floored-perimeter conclusion implies Erdos-Oler.

    For a < k-1 we have floor(a) <= k-2, so the bound gives
        n <= a^2/2 + (3/2)(k-2) + 1 < (k-1)^2/2 + (3/2)(k-2) + 1 = T(k) - 3/2,
    i.e. at most T(k) - 2 points.  So T(k) - 1 points force a >= k-1, which is
    exactly s(T(k) - 1) = s(T(k)).  Everything here is exact rational arithmetic.
    """
    print("=" * 78)
    print("6. WHAT THE CONCLUSION WOULD IMPLY -- the full Erdos-Oler conjecture")
    print("=" * 78)
    print(f"  {'k':>3} {'T(k)':>5} {'sup of bound for a < k-1':>26} {'=> max points':>14}")
    rows = []
    for k in range(2, kmax + 1):
        t = k * (k + 1) // 2
        sup = F(k - 1) ** 2 / 2 + F(3, 2) * (k - 2) + 1        # limit as a -> (k-1)^-
        max_points = (sup - 1).__floor__() if sup == int(sup) else sup.__floor__()
        rows.append(
            {
                "k": k,
                "T_k": t,
                "sup_bound_below_k_minus_1": str(sup),
                "max_points_below_k_minus_1": max_points,
                "implies_erdos_oler_at_k": max_points <= t - 2,
            }
        )
        print(f"  {k:>3} {t:>5} {str(sup):>26} {max_points:>14}   T(k)-2 = {t - 2}")
    ok = all(r["implies_erdos_oler_at_k"] for r in rows)
    print(
        f"\n  every k gives at most T(k)-2 points strictly below side k-1: {ok}"
        "\n  => the conjecture implies s(T(k)-1) = s(T(k)) for every k, i.e. Erdos-Oler"
        "\n  => by RULES.md §7 it should be assumed FALSE or out of reach, not attacked\n"
    )
    return ok, rows


def main():
    os.makedirs(OUT, exist_ok=True)
    controls_ok, control_rows = controls()
    atlas_rows = atlas()
    refuted, probe_rows = probe()
    floored_rows = floored_table()
    gl_rows = graham_lubachevsky_table()
    implies_eo, eo_rows = erdos_oler_implication()

    report = {
        "normalisation": "minimum separation 1 (certificate coordinates halved)",
        "controls_passed": controls_ok,
        "controls": control_rows,
        "atlas": atlas_rows,
        "face_excess_nonnegativity_refuted": refuted,
        "probe": probe_rows,
        "floored_perimeter_consistency": floored_rows,
        "floored_perimeter_vs_best_known": gl_rows,
        "floored_perimeter_implies_erdos_oler": implies_eo,
        "erdos_oler_implication": eo_rows,
    }
    with open(os.path.join(OUT, "report.json"), "w") as fh:
        json.dump(report, fh, indent=1, default=str)
    print(f"wrote {os.path.join(OUT, 'report.json')}")

    if not controls_ok:
        raise SystemExit("CONTROLS FAILED - nothing downstream is trustworthy")


if __name__ == "__main__":
    main()
