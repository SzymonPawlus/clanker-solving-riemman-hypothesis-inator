"""Construct exact witnesses from arbitrary finite rational core-good support.

The support's universal dual supplies the existence guarantee separately.
Every returned witness is checked directly; this file is not that dual checker.
"""
from fractions import Fraction
from witness_bisection import floor_sum


def bad_count(c, x, w, lo, hi):
    a, b = x.numerator, x.denominator
    modulus = b*c
    # An integer residue is strictly less than modulus/15 iff it is <cut.
    cut = (modulus+14)//15
    step = b*w
    offset = w*a + step*lo
    n = hi-lo
    return n + floor_sum(n, modulus, step, offset+cut-1) - floor_sum(
        n, modulus, step, offset+modulus-cut
    )


def construct(scale, core, extra_speeds, support):
    if not isinstance(scale, int) or isinstance(scale, bool) or scale <= 0:
        raise ValueError('scale must be a positive integer')
    core = tuple(sorted(set(core)))
    if not core or any(not isinstance(v, int) or isinstance(v, bool) or v<=0 for v in core):
        raise ValueError('core must contain positive integers')
    supplied = tuple(extra_speeds)
    if len(supplied)>6 or any(not isinstance(v,int) or isinstance(v,bool) or not v for v in supplied):
        raise ValueError('at most six nonzero integer extra speeds are supported')
    fixed = {scale*v for v in core}
    extras = tuple(sorted({abs(v) for v in supplied}-fixed))
    if any(v>=max(core)*scale for v in extras):
        raise ValueError('additional absolute speeds must be below the core maximum')
    support = tuple(sorted({Fraction(x)%1 for x in support}))
    if not support:
        raise ValueError('empty support')
    for x in support:
        a,b=x.numerator,x.denominator
        if any(15*min(v*a%b,-v*a%b)<b for v in core):
            raise ValueError('support contains a time unsafe for the primitive core')
    counts=0
    def score(x,lo,hi):
        nonlocal counts
        counts+=len(extras)
        return hi-lo-sum(bad_count(scale,x,w,lo,hi) for w in extras)
    for x in support:
        initial=score(x,0,scale)
        if initial>0:break
    else:raise ValueError('no support fiber has positive signed score')
    lo,hi,current=0,scale,initial
    splits=0
    while hi-lo>1:
        mid=(lo+hi)//2
        left=score(x,lo,mid)
        if left>0:hi,current=mid,left
        else:lo,current=mid,current-left
        assert current>0
        splits+=1
    assert current==1
    time=(lo+x)/scale
    a,b=time.numerator,time.denominator
    minimum=min(Fraction(min(v*a%b,-v*a%b),b) for v in fixed|set(extras))
    assert minimum>=Fraction(1,15)
    return {'scale':scale,'primitive_time':str(x),'lift_index':lo,'time':str(time),
            'minimum_distance':str(minimum),'initial_signed_score':initial,
            'splits':splits,'modular_interval_counts':counts}

