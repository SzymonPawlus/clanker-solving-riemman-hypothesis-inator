"""Check the fixed exact M=36 classification falsifier, without a solver."""
from math import gcd
import json

MAXIMUM = 36
ASSIGNMENT = {
    2: [0, 1, 17, 18, 19, 35],
    12: [3, 6, 9, 12, 15, 21, 24, 27, 30, 33],
    15: [7, 31],
    18: [2, 4, 8, 10, 14, 16, 20, 22, 26, 28, 32, 34],
    26: [11, 29],
    28: [5, 23],
    33: [13, 25],
}
PRIVATE = {2: 17, 12: 3, 15: 7, 18: 2, 26: 11, 28: 5, 33: 13}


def bad(w, r):
    residue = w * (15*r+1) % 540
    return min(residue, 540-residue) < 36


if __name__ == '__main__':
    assert gcd(MAXIMUM, *ASSIGNMENT) == 1
    assert sorted(r for row in ASSIGNMENT.values() for r in row) == list(range(36))
    assert all(bad(w, r) for w, row in ASSIGNMENT.items() for r in row)
    assert all(bad(w, r) and all(not bad(v, r) for v in ASSIGNMENT if v != w)
               for w, r in PRIVATE.items())
    print(json.dumps({'core': sorted([MAXIMUM, *ASSIGNMENT]),
                      'covered_indices': 36, 'inclusion_minimal': True,
                      'gcd': 1, 'private_indices': PRIVATE}, indent=2))
