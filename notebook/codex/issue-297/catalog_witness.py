"""Recognize 204 frozen scaled-core families and return an exact common time.

The mathematical runtime guarantee depends on certificates still marked sketch.
Every emitted witness is independently valid by direct integer inequalities.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
from random import Random
import argparse,json,sys
from randomized_witness import construct

CATALOG_SOURCES=(
 ('all-forty-four-cores.json','e8c26ff9ca2b405666ec33a4872f94a8b2897c8164dfa4d462ad3a51a56d23e6',44,8,6,'seven-row-maximal-core','fd602d4'),
 ('eight-core-phase-to30.json','5598c63635bf372fbac906943da45ede93c7e5a9b827d49787132a8b9cf676ec',160,9,5,'eight-row-core-maximum-at-most-30','2cc5bc8'),
)

def load_catalog(directory=None):
 directory=Path(__file__).with_name('witness_catalog') if directory is None else Path(directory)
 records=[]
 for name,expected,count,size,free,family,commit in CATALOG_SOURCES:
  raw=(directory/name).read_bytes()
  if sha256(raw).hexdigest()!=expected:raise ValueError('catalog hash mismatch: '+name)
  manifest=json.loads(raw)
  if len(manifest['cases'])!=count:raise ValueError('wrong catalog case count')
  for case in manifest['cases']:
   pattern=tuple(case['pattern'])
   if len(pattern)!=size or tuple(sorted(set(pattern)))!=pattern or gcd(*pattern)!=1 or any(type(v)!=int or v<=0 for v in pattern):raise ValueError('invalid primitive pattern')
   atoms=tuple((Fraction(x),Fraction(w)) for x,w in case['atoms'])
   if not atoms or any(w<=0 or not 0<=x<1 for x,w in atoms):raise ValueError('invalid positive atom')
   mass=sum((w for x,w in atoms),Fraction())
   if mass!=Fraction(case['total']) or mass<=free:raise ValueError('invalid certificate mass')
   for x,w in atoms:
    if any(15*min(v*x.numerator%x.denominator,-v*x.numerator%x.denominator)<x.denominator for v in pattern):raise ValueError('core-unsafe atom')
   records.append({'pattern':pattern,'atoms':atoms,'mass':mass,'max_extras':free,'family':family,'source_file':name,'source_sha256':expected,'source_commit':commit})
 if len({r['pattern'] for r in records})!=204:raise ValueError('duplicate catalog pattern')
 return tuple(records)

def checked_velocities(values):
 if not isinstance(values,(list,tuple)) or len(values)!=14:raise ValueError('exactly fourteen nonzero integer velocities are required')
 out=[]
 for value in values:
  if isinstance(value,str):
   if not value or value.lstrip('+-').isdigit() is False:raise ValueError('velocity strings must be decimal integers')
   value=int(value)
  if type(value)!=int or value==0:raise ValueError('velocities must be nonzero integers')
  out.append(value)
 return tuple(out)

def verify_time(velocities,time):
 t=Fraction(time);a,b=t.numerator,t.denominator
 distances=[Fraction(min((v*a)%b,(-v*a)%b),b) for v in velocities]
 return all(15*d.numerator>=d.denominator for d in distances),min(distances)

def solve(velocities,*,catalog=None,seed=None,max_trials=100000,rng=None):
 values=checked_velocities(velocities)
 if type(max_trials)!=int or max_trials<1:raise ValueError('max_trials must be a positive integer')
 records=load_catalog() if catalog is None else catalog
 spectrum=set(map(abs,values));M=max(spectrum);matches=[]
 for record in records:
  primitive_max=record['pattern'][-1]
  if M%primitive_max:continue
  scale=M//primitive_max;fixed={scale*v for v in record['pattern']}
  if not fixed<=spectrum:continue
  extras=tuple(sorted(spectrum-fixed))
  if len(extras)>record['max_extras']:continue
  probability=1-Fraction(len(extras),1)/record['mass']
  matches.append((probability,record,scale,extras))
 if not matches:
  return {'status':'unrecognized','message':'No scaled core from the 204 explicitly listed families was found. This is not a no-witness or counterexample result.','catalog_cases':204}
 probability,record,scale,extras=max(matches,key=lambda m:m[0])
 metadata={'catalog_cases':204,'matched_families':len(matches),'family':record['family'],'primitive_core':record['pattern'],'scale':str(scale),'extra_distinct_absolute_speeds':len(extras),'source_manifest':record['source_file'],'source_sha256':record['source_sha256'],'source_commit':record['source_commit'],'mathematical_certificate_status':'sketch; requires Claude or human review','conditional_trial_success_lower_bound':str(probability)}
 random_source=rng if rng is not None else (Random(seed) if seed is not None else None)
 try:
  result=construct(scale,record['pattern'],extras,record['atoms'],rng=random_source,max_trials=max_trials)
 except TimeoutError:
  return {'status':'trial_limit','message':'The sampling cap was reached; this does not imply that no witness exists.','max_trials':max_trials,**metadata}
 valid,minimum=verify_time(values,result['time'])
 if not valid:raise ArithmeticError('returned rational failed direct input verification')
 return {'status':'witness','time':result['time'],'minimum_distance':str(minimum),'all_fourteen_inequalities_checked':True,'trials':result['trials'],**metadata}

if __name__=='__main__':
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--input',type=Path,required=True,help='JSON with a velocities list; decimal strings also accepted')
 parser.add_argument('--output',type=Path)
 parser.add_argument('--seed',type=int)
 parser.add_argument('--max-trials',type=int,default=100000)
 args=parser.parse_args()
 try:
  data=json.loads(args.input.read_text());values=data['velocities'] if isinstance(data,dict) else data
  result=solve(values,seed=args.seed,max_trials=args.max_trials)
 except (ValueError,KeyError,TypeError,OSError) as error:
  result={'status':'invalid_input','message':str(error)}
 text=json.dumps(result,indent=2)+'\n'
 if args.output:args.output.write_text(text)
 else:print(text,end='')
 sys.exit({'witness':0,'unrecognized':2,'trial_limit':3,'invalid_input':4}[result['status']])
