"""V3's own transcription of the 15-piece covering of T_a, a = 1 + 2*sqrt3,
read off the table in problems/circle-packing-equilateral-triangle/attacks/
n16-covering-2/README.md.  Coordinates only -- no code was taken from that
attack's certifier.

Each coordinate is written (p, q) meaning p + q*sqrt(3), p, q exact rationals.
"""
from fractions import Fraction as F
from q3f import Q3

A_SIDE = Q3(1, 2)          # a = 1 + 2 sqrt3

_h = F(1, 2)
_t = F(1, 3)

# shorthands: value = (rational part, sqrt3 coefficient)
Z   = (F(0), F(0))
ONE_ = (F(1), F(0))
TH  = (F(3, 2), F(0))       # 3/2
FH  = (F(5, 2), F(0))       # 5/2
R3_ = (F(0), F(1))          # sqrt3
R2  = (F(0), F(2))          # 2 sqrt3
Rt  = (F(0), _t)            # sqrt3/3
R4t = (F(0), F(4, 3))       # 4 sqrt3 / 3
P1t = (F(1), _t)            # 1 + sqrt3/3
P14 = (F(1), F(4, 3))       # 1 + 4 sqrt3/3
P1R = (F(1), F(1))          # 1 + sqrt3
P12 = (F(1), F(2))          # 1 + 2 sqrt3

FACES = [
    [(Z, Z), (ONE_, Z), (Rt, Rt), (Z, ONE_)],
    [(Rt, P1t), (Z, R3_), (Z, ONE_), (Rt, Rt), (ONE_, ONE_)],
    [(Rt, R4t), (Z, P1R), (Z, R3_), (Rt, P1t), (ONE_, R3_)],
    [(Rt, P14), (Z, R2), (Z, P1R), (Rt, R4t), (ONE_, FH)],
    [(ONE_, R2), (Z, P12), (Z, R2), (Rt, P14)],
    [(ONE_, Z), (R3_, Z), (P1t, Rt), (ONE_, ONE_), (Rt, Rt)],
    [(TH, TH), (ONE_, R3_), (Rt, P1t), (ONE_, ONE_), (P1t, Rt), (R3_, ONE_)],
    [(P1t, R4t), (ONE_, FH), (Rt, R4t), (ONE_, R3_), (TH, TH), (R3_, R3_)],
    [(R3_, P1R), (ONE_, R2), (Rt, P14), (ONE_, FH), (P1t, R4t)],
    [(R3_, Z), (P1R, Z), (R4t, Rt), (R3_, ONE_), (P1t, Rt)],
    [(R4t, P1t), (R3_, R3_), (TH, TH), (R3_, ONE_), (R4t, Rt), (FH, ONE_)],
    [(P1R, R3_), (R3_, P1R), (P1t, R4t), (R3_, R3_), (R4t, P1t)],
    [(P1R, Z), (R2, Z), (P14, Rt), (FH, ONE_), (R4t, Rt)],
    [(R2, ONE_), (P1R, R3_), (R4t, P1t), (FH, ONE_), (P14, Rt)],
    [(R2, Z), (P12, Z), (R2, ONE_), (P14, Rt)],
]


def faces():
    return [[(Q3(*c[0]), Q3(*c[1])) for c in f] for f in FACES]
