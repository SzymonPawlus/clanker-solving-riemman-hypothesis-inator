"""Strict parser for exact Q(sqrt 3) expression strings in certificates.

Per problems/circle-packing-equilateral-triangle/RULES.md §2, DECIMAL STRINGS ARE
BANNED in exact fields.  This parser rejects any token containing '.', 'e' or 'E'
in a numeric position, so a truncated float cannot enter the pipeline at all.

Grammar accepted (whitespace-insensitive):
    expr  := term (('+'|'-') term)*
    term  := rat | rat '*' 'sqrt(3)' | 'sqrt(3)'
    rat   := int | int '/' int
"""
import re
from fractions import Fraction as F
from qsqrt3 import Q3

_TOK = re.compile(r"\s*(sqrt\(3\)|[+\-*/]|\d+)")


def _rat(tok):
    if "." in tok or "e" in tok.lower():
        raise ValueError("decimal string in an exact field: %r" % tok)
    return F(int(tok))


def parse_q3(s):
    if not isinstance(s, str):
        raise ValueError("exact fields must be strings, got %r" % (s,))
    if "." in s or "e" in s or "E" in s:
        raise ValueError("decimal string / float in an exact field: %r" % s)
    toks = []
    i = 0
    while i < len(s):
        m = _TOK.match(s, i)
        if not m:
            raise ValueError("cannot parse %r at %d" % (s, i))
        toks.append(m.group(1))
        i = m.end()
    # shunting-free tiny recursive parse
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        t = toks[pos[0]]
        pos[0] += 1
        return t

    def term():
        sign = F(1)
        while peek() in ("+", "-"):
            if take() == "-":
                sign = -sign
        t = peek()
        if t == "sqrt(3)":
            take()
            return Q3(0, sign)
        c = _rat(take())
        if peek() == "/":
            take()
            c = c / _rat(take())
        if peek() == "*":
            take()
            if take() != "sqrt(3)":
                raise ValueError("expected sqrt(3) in %r" % s)
            return Q3(0, sign * c)
        return Q3(sign * c, 0)

    val = term()
    while peek() in ("+", "-"):
        op = take()
        t = term()
        val = val + t if op == "+" else val - t
    if pos[0] != len(toks):
        raise ValueError("trailing junk in %r" % s)
    return val


def load_certificate(path):
    import json
    with open(path) as f:
        raw = f.read()
    cert = json.loads(raw)
    pts = [(parse_q3(x), parse_q3(y)) for x, y in cert["coordinates"]]
    s = parse_q3(cert["side_length"])
    d = s - Q3(0, 2)
    return cert, pts, s, d


if __name__ == "__main__":
    for t in ["10 + 4*sqrt(3)", "sqrt(3)", "-sqrt(3)", "0", "5/2", "3 - 2*sqrt(3)"]:
        print("%-16s -> %s" % (t, parse_q3(t).sexpr()))
    for bad in ["10.928", "1e3", "3.0 + sqrt(3)"]:
        try:
            parse_q3(bad)
            print("FAIL: accepted %r" % bad)
        except ValueError as e:
            print("rejected %-16r  (%s)" % (bad, e))
