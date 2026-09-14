"""Direct strict-residue checks of the rational-support constructor."""
from fractions import Fraction
from random import Random
import json
from rational_witness import bad_count, construct


if __name__=='__main__':
    rng=Random(30429715)
    for _ in range(20000):
        c=rng.randrange(1,80)
        x=Fraction(rng.randrange(100),rng.randrange(1,100))%1
        w=rng.randrange(1,40*c)
        lo=rng.randrange(c+1)
        hi=rng.randrange(lo,c+1)
        direct=0
        for j in range(lo,hi):
            y=w*(j+x)/c
            f=y%1
            direct+=min(f,1-f)<Fraction(1,15)
        assert bad_count(c,x,w,lo,hi)==direct

    # This fixture exercises denominators not divisible by15 and an interior
    # safe time. It is one direct input, not a claim of a universal certificate
    # for the singleton support.
    core=(1,5,7,8,11,12,13,24)
    x=Fraction(59,528)
    result=construct(2,core,(5,7,9,13,29,31),(x,))
    assert result['time']=='59/1056'
    assert result['minimum_distance']=='7/66'
    print(json.dumps({'arbitrary_rational_interval_fixtures':20000,
                      'interior_witness_fixture':result},indent=2))
