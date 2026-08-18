#!/usr/bin/env python3
"""Unreduced size counts for the Lasserre/moment hierarchy of approach C.

Status of the *approach* this supports: sketch (see README.md).  This script
itself makes no mathematical claim beyond elementary counting; it exists so
that the numbers quoted in section C of README.md are reproducible rather than
hand-computed.  Two successive hand-counts in that section were wrong, which is
the whole reason this file exists.

Formulation being counted (README.md section C, "the idea"):

    maximise  t
    subject to  ||p_i - p_j||^2 >= t      for all i < j
                p_i in the triangle       (3 linear constraints each)

so `t` is a *decision variable of the polynomial program*, on the same footing
as the point coordinates.  In the plane with n points that is

    N = 2n + 1

variables.  If instead you fix `t` externally and ask only for feasibility, drop
the +1; pass --fixed-t to get those counts.

Counting facts used (both elementary):

  * the number of monomials of degree <= k in N variables is C(N + k, k);
  * a moment/localizing matrix of order r is indexed by the monomials of degree
    <= r, so it is C(N + r, r) square;
  * a relaxation of level L constrains moments up to degree 2L, of which there
    are C(N + 2L, 2L).

At level L, the moment matrix has order L and the localizing matrix of a
constraint of degree d has order L - ceil(d/2).  Both the pairwise-distance
constraints and the containment constraints are used here at level 2: the
distance constraints are quadratic (order 1), and the containment constraints
are linear, but a linear constraint may be localized at order L - 1 = 1 as
well, which is what section C quotes.

Run:  python3 moment_sizes.py            # n = 16, level 2
      python3 moment_sizes.py --n 5 --level 2
      python3 moment_sizes.py --fixed-t
"""

from __future__ import annotations

import argparse
from math import comb


def n_monomials(n_vars: int, max_degree: int) -> int:
    """Monomials of degree <= max_degree in n_vars variables."""
    return comb(n_vars + max_degree, max_degree)


def report(n: int, level: int, fixed_t: bool) -> str:
    coords = 2 * n
    n_vars = coords if fixed_t else coords + 1

    pairs = comb(n, 2)
    containment = 3 * n

    lines = []
    lines.append(f"n = {n} points, relaxation level L = {level}")
    if fixed_t:
        lines.append(
            f"  formulation: FIXED-t feasibility "
            f"(t is an external parameter, not a variable)"
        )
    else:
        lines.append(
            f"  formulation: maximise t "
            f"(t is a decision variable of the polynomial program)"
        )
    lines.append(f"  variables N = 2*{n}{'' if fixed_t else ' + 1'} = {n_vars}")
    lines.append("")

    for r in (1, 2, 3):
        dim = n_monomials(n_vars, r)
        lines.append(
            f"  order-{r} moment matrix: C({n_vars} + {r}, {r}) = {dim} "
            f"rows/cols"
        )
    lines.append("")

    deg = 2 * level
    n_moments = n_monomials(n_vars, deg)
    lines.append(
        f"  scalar moment variables at level {level} "
        f"(monomials of degree <= {deg}): C({n_vars} + {deg}, {deg}) = "
        f"{n_moments:,}"
    )
    lines.append("")

    loc_order = level - 1
    loc_dim = n_monomials(n_vars, loc_order)
    lines.append(
        f"  localizing matrices of order {loc_order}: "
        f"{loc_dim} x {loc_dim} apiece"
    )
    lines.append(
        f"    - {pairs} of them for the pairwise-distance constraints "
        f"(C({n},2))"
    )
    lines.append(
        f"    - {containment} of them for the containment constraints (3*{n})"
    )
    lines.append(f"    - {pairs + containment} localizing blocks in total")
    lines.append("")
    lines.append(
        "  These are UNREDUCED counts: no S_n x D_3 symmetry reduction, no"
    )
    lines.append(
        "  sparsity exploitation.  They are the starting point for the size"
    )
    lines.append("  gate in README.md section C, not the gate itself.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=16, help="number of points")
    parser.add_argument("--level", type=int, default=2, help="relaxation level")
    parser.add_argument(
        "--fixed-t",
        action="store_true",
        help="count the 2n-variable fixed-t feasibility formulation instead",
    )
    args = parser.parse_args()
    if args.n < 2 or args.level < 1:
        parser.error("need n >= 2 and level >= 1")
    print(report(args.n, args.level, args.fixed_t))


if __name__ == "__main__":
    main()
