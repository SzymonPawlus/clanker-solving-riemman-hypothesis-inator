"""Exact arithmetic in the Q-vector space spanned by 1, sqrt3, sqrt6, sqrt33.

Only linear combinations are needed (no products of two surds), so a dict
{basis symbol: Fraction} with exact equality is enough, and no numerics enter
any decision.
"""
from fractions import Fraction as F

BASIS = {"1": 1.0, "r3": 3 ** .5, "r6": 6 ** .5, "r33": 33 ** .5}


class S(dict):
    def __add__(self, o):
        r = S(self)
        for k, v in o.items():
            r[k] = r.get(k, F(0)) + v
        return S({k: v for k, v in r.items() if v != 0})

    def __sub__(self, o):
        return self + (-o)

    def __neg__(self):
        return S({k: -v for k, v in self.items()})

    def scale(self, c):
        c = F(c)
        return S({k: v * c for k, v in self.items() if v * c != 0})

    def __eq__(self, o):
        return dict(self) == dict(o)

    def __float__(self):
        return float(sum(float(v) * BASIS[k] for k, v in self.items()))

    def __repr__(self):
        if not self:
            return "0"
        return " + ".join(f"{v}*{k}" if k != "1" else f"{v}" for k, v in
                          sorted(self.items()))


def s(**kw):
    return S({k: F(v) for k, v in kw.items() if F(v) != 0})
