"""Independent parser: exact field expression string -> Q3.

Uses sympy only to parse and to split the expression over the basis {1, sqrt(3)};
the resulting coefficients are exact sympy Rationals, converted to Fractions.
Rejects anything that is not of the form (rational) + (rational)*sqrt(3),
and rejects bare decimal strings (RULES.md forbids them in exact fields).
"""
import re
from fractions import Fraction as F
import sympy as sp
from q3 import Q3

_R3 = sp.sqrt(3)
_DECIMAL = re.compile(r"\d*\.\d")


def parse(s):
    if not isinstance(s, str):
        raise TypeError("exact fields must be strings, got %r" % (s,))
    if _DECIMAL.search(s):
        raise ValueError("decimal string banned in exact field: %r" % s)
    e = sp.expand(sp.sympify(s, rational=True))
    b = sp.nsimplify(sp.expand(e).coeff(_R3))
    a = sp.simplify(sp.expand(e) - b * _R3)
    if not (a.is_Rational and b.is_Rational):
        raise ValueError("not in Q(sqrt3): %r -> a=%r b=%r" % (s, a, b))
    return Q3(F(int(a.p), int(a.q)), F(int(b.p), int(b.q)))


if __name__ == "__main__":
    for t in ["0", "4", "5/2", "sqrt(3)", "3 + sqrt(3)", "4 + 2*sqrt(3)",
              "6 + 4*sqrt(3)", "3 + 3*sqrt(3)", "-1/3*sqrt(3)"]:
        print("%-16s -> %s" % (t, parse(t).sexpr()))
    for bad in ["10.928", "sqrt(2)", "sqrt(3)**3/7 + 2**(1/3)"]:
        try:
            parse(bad)
            print("ACCEPTED (BAD!):", bad)
        except Exception as ex:
            print("rejected:", bad, "->", type(ex).__name__)
