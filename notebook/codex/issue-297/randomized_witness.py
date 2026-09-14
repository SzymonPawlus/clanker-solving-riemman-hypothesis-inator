"""Exact-output randomized witness extraction from a frozen uniform measure.

Runtime guarantees are conditional on the caller's universal dual certificate.
The returned rational time is always directly checked against every speed.
"""
from fractions import Fraction
from math import lcm
from bisect import bisect_right
from random import SystemRandom


def construct(scale, core, extra_speeds, atoms, *, rng=None, max_trials=None):
    if not isinstance(scale,int) or isinstance(scale,bool) or scale<=0:
        raise ValueError('scale must be a positive integer')
    core=tuple(sorted(set(core)))
    if not core or any(not isinstance(v,int) or isinstance(v,bool) or v<=0 for v in core):
        raise ValueError('core must contain positive integers')
    supplied=tuple(extra_speeds)
    if len(supplied)>6 or any(not isinstance(v,int) or isinstance(v,bool) or not v for v in supplied):
        raise ValueError('at most six nonzero integer extra speeds are supported')
    fixed={scale*v for v in core}
    extras=tuple(sorted({abs(v) for v in supplied}-fixed))
    if any(v>=scale*max(core) for v in extras):
        raise ValueError('extra absolute speeds must be below the core maximum')
    atoms=tuple((Fraction(x)%1,Fraction(weight)) for x,weight in atoms)
    if not atoms or any(weight<0 for x,weight in atoms):
        raise ValueError('weights must be nonnegative and support nonempty')
    atoms=tuple((x,weight) for x,weight in atoms if weight)
    if not atoms:raise ValueError('total weight must be positive')
    for x,weight in atoms:
        a,b=x.numerator,x.denominator
        if any(15*min(v*a%b,-v*a%b)<b for v in core):
            raise ValueError('support must be safe for the primitive core')
    denominator=lcm(*(weight.denominator for x,weight in atoms))
    cumulative=[]
    total=0
    for x,weight in atoms:
        total+=weight.numerator*(denominator//weight.denominator)
        cumulative.append(total)
    if max_trials is not None and (not isinstance(max_trials,int) or max_trials<1):
        raise ValueError('max_trials must be positive or None')
    rng=SystemRandom() if rng is None else rng
    trial=0
    while max_trials is None or trial<max_trials:
        trial+=1
        x=atoms[bisect_right(cumulative,rng.randrange(total))][0]
        j=rng.randrange(scale)
        time=(j+x)/scale
        a,b=time.numerator,time.denominator
        if all(15*min(v*a%b,-v*a%b)>=b for v in extras):
            minimum=min(Fraction(min(v*a%b,-v*a%b),b) for v in fixed|set(extras))
            assert minimum>=Fraction(1,15)
            return {'time':str(time),'minimum_distance':str(minimum),'trials':trial,
                    'scale_decimal_digits':len(str(scale)),
                    'primitive_time':str(x),'lift_index':j}
    raise TimeoutError('no witness found within the requested trial cap')

