"""CLI: `python -m packcheck <certificate.json> [...]`.

Exit status 0 iff every certificate given was ACCEPTED.
"""

from __future__ import annotations

import argparse
import sys

from .checker import CertificateError, check_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="packcheck",
        description=(
            "Verify circle-packing certificates in exact arithmetic. "
            "No floating point is used on the verification path."
        ),
    )
    parser.add_argument("certificates", nargs="+", help="certificate JSON files")
    parser.add_argument(
        "--require-tight",
        action="store_true",
        help=(
            "treat a reported side_length larger than the coordinates require as a "
            "failure rather than a warning"
        ),
    )
    args = parser.parse_args(argv)

    all_ok = True
    for path in args.certificates:
        print(f"=== {path}")
        try:
            result = check_file(path, require_tight=args.require_tight)
        except CertificateError as exc:
            print(f"  MALFORMED: {exc}")
            print("RESULT: REJECT")
            all_ok = False
            continue
        print(result.render())
        all_ok = all_ok and result.ok
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
