"""Portable replay and direct verification of one thousand-digit example."""
from pathlib import Path
from fractions import Fraction
from random import Random
import json
from randomized_witness import construct


if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('randomized-example-input.json').read_text())
    c=10**data['scale_power_of_ten']+data['scale_offset']
    rng=Random(data['random_seed'])
    extras=[rng.randrange(1,18*c) for _ in range(6)]
    result=construct(c,data['pattern'],extras,data['atoms'],rng=rng,max_trials=10000)
    t=Fraction(result['time'])
    speeds=[c*v for v in data['pattern']]+extras
    exact_distances=[min((v*t)%1,(-v*t)%1) for v in speeds]
    assert min(exact_distances)>=Fraction(1,15)
    assert sum(Fraction(weight) for x,weight in data['atoms'])==Fraction(6011,1000)
    print(json.dumps({'scale_decimal_digits':len(str(c)),'trials':result['trials'],
                      'directly_verified_coordinates':len(speeds),
                      'minimum_distance':str(min(exact_distances))},indent=2))
