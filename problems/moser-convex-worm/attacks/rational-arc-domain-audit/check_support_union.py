#!/usr/bin/env python3
"""Coverage-only union audit for the exact worm-angle support slabs."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import check_support_complement as complement
import check_support_slab as slab


class Reject(ValueError):
    pass


def check(path):
    certificate_path = Path(path)
    data = json.loads(certificate_path.read_text())
    expected = {
        "schema_version": "moser-support-union-v1",
        "claim_scope": "complete_angular_coverage_pending_mixed_area_review",
        "global_claim": False,
        "target": "232239/1000000",
        "slabs": [
            {"source": "support_complement.json", "worm_intervals": [["0", "80"], ["259/2", "180"]]},
            {"source": "support_slab.json", "worm_intervals": [["75", "269/2"]]},
        ],
        "triangle_domain": ["0", "120"],
        "square_domain": ["0", "90"],
    }
    if data != expected:
        raise Reject("union schema, sources, or withheld scope changed")
    complement_report = complement.check(certificate_path.with_name("support_complement.json"))
    slab_report = slab.check(certificate_path.with_name("support_slab.json"))
    if complement_report["certified_lower"] != Q(93, 400) or \
       slab_report["certified_lower"] != Q(2323, 10000):
        raise Reject("source checker lower endpoint changed")
    intervals = [(Q(0), Q(80)), (Q(259, 2), Q(180)), (Q(75), Q(269, 2))]
    endpoints = sorted({Q(0), Q(180), *(x for pair in intervals for x in pair)})
    for lo, hi in zip(endpoints, endpoints[1:]):
        midpoint = (lo + hi) / 2
        if not any(a <= midpoint <= b for a, b in intervals):
            raise Reject("uncovered worm-angle atom")
    return {"certified_lower": min(complement_report["certified_lower"],
                                    slab_report["certified_lower"]),
            "worm_domain_covered": (Q(0), Q(180)), "overlap_one": (Q(75), Q(80)),
            "overlap_two": (Q(259, 2), Q(269, 2)), "global_claim": False}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print(f"PASS complete angular union with theorem scope withheld: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
