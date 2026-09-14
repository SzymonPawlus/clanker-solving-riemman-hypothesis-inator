"""Exact exploratory row charges on the complement of periods two and three."""
from fractions import Fraction
from math import gcd
import json


def congruence_count(lo, hi, modulus, residue):
    return (hi-residue)//modulus - (lo-1-residue)//modulus


def charge(h, a):
    # a(15j+1)=a+15k (mod15h), so j=a^{-1}k(modh).
    # The allowed complement {1,5}(mod6) is invariant under its units.
    lo = -((h-1+a)//15)
    hi = (h-1-a)//15
    d = gcd(h, 6)
    if d == 1:
        return Fraction(hi-lo+1, 3*h)
    if d == 2:
        return Fraction(2*congruence_count(lo,hi,2,1), 3*h)
    if d == 3:
        count = hi-lo+1-congruence_count(lo,hi,3,0)
        return Fraction(count, 2*h)
    return Fraction(congruence_count(lo,hi,6,1)+congruence_count(lo,hi,6,5), h)


def literal(h, a):
    period = 6*h//gcd(6,h)
    return Fraction(sum(
        j%6 in (1,5) and min(a*(15*j+1)%(15*h),-a*(15*j+1)%(15*h))<h
        for j in range(period)
    ),period)


if __name__=='__main__':
    for h in range(2,121):
        for a in range(1,h):
            if gcd(h,a)==1:
                assert charge(h,a)==literal(h,a),(h,a)
    rows=[]
    for h in range(2,91):
        for a in range(1,h):
            if gcd(h,a)==1 and charge(h,a)>=Fraction(1,15):
                rows.append((str(charge(h,a)),h,a))
    rows.sort(key=lambda z:(-Fraction(z[0]),z[1],z[2]))
    print(json.dumps({'literal_bound':120,'ranking_bound':90,
                      'rows_charge_at_least_one_fifteenth':rows},indent=2))
