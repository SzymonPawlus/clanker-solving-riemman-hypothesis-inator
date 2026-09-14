"""Direct output checks for every frozen family plus boundary/failure fixtures."""
from pathlib import Path
from random import Random
from fractions import Fraction
from hashlib import sha256
import json,shutil,tempfile
from catalog_witness import load_catalog,solve,verify_time

class ZeroDraw:
 def randrange(self,n):return 0

def check():
 catalog=load_catalog();rng=Random(297304204);count=0;trials=0;big_result=None;big_input=None
 for index,case in enumerate(catalog):
  # An off-lattice completion exercises all lifts rather than common scaling alone.
  c=97 if index%2==0 else 10**1000+239
  fixed={c*v for v in case['pattern']};M=max(fixed);speeds=set(fixed)
  while len(speeds)<14:speeds.add(rng.randrange(1,M))
  values=[v if i%2 else -v for i,v in enumerate(sorted(speeds))]
  result=solve(values,catalog=catalog,seed=10000+index,max_trials=100000)
  assert result['status']=='witness',(index,result)
  # Recompute each coordinate using numerator/remainder, independent of sampler.
  time=Fraction(result['time']);den=time.denominator
  remainders=[(v*time.numerator)%den for v in values]
  assert all(15*min(r,den-r)>=den for r in remainders)
  assert set(c*v for v in case['pattern'])<=set(map(abs,values))
  count+=1;trials+=result['trials']
  if c>10**1000 and big_result is None:big_result=result;big_input={'velocities':[str(v) for v in values]}
 endpoint=[1,5,6,7,9,11,13,18,2,3,4,8,10,15]
 result=solve(endpoint,catalog=catalog,seed=7)
 assert result['status']=='witness' and result['minimum_distance']=='1/15'
 assert solve(list(range(1,15)),catalog=catalog)['status']=='unrecognized'
 assert solve(endpoint,catalog=catalog,max_trials=3,rng=ZeroDraw())['status']=='trial_limit'
 for invalid in (endpoint[:-1],[0]+endpoint[1:],[True]+endpoint[1:],[1.5]+endpoint[1:]):
  try:solve(invalid,catalog=catalog)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 # Repeated and negative velocities are legal and receive the same common time.
 dup=[1,5,6,7,9,11,13,18,-1,5,-6,7,-9,11]
 assert solve(dup,catalog=catalog,seed=5)['status']=='witness'
 with tempfile.TemporaryDirectory() as directory:
  source=Path(__file__).with_name('witness_catalog')
  for p in source.glob('*.json'):shutil.copyfile(p,Path(directory)/p.name)
  path=Path(directory)/'all-forty-four-cores.json';path.write_bytes(path.read_bytes()+b' ')
  try:load_catalog(directory)
  except ValueError:pass
  else:raise AssertionError('catalog corruption accepted')
 report={'status':'all direct rational-output checks passed','recognized_family_fixtures':count,'total_trials':trials,'scales':['97','10^1000+239'],'threshold':'1/15','extra_fixtures':['endpoint equality','unrecognized distinct spectrum','forced sampling cap','zero rejection','length rejection','Boolean rejection','float rejection','signs and repetitions','catalog hash corruption'],'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'interface_sha256':sha256(Path(__file__).with_name('catalog_witness.py').read_bytes()).hexdigest(),'sampler_sha256':sha256(Path(__file__).with_name('randomized_witness.py').read_bytes()).hexdigest(),'source_manifest_sha256':{r['source_file']:r['source_sha256'] for r in catalog}}
 base=Path(__file__).parent
 (base/'catalog-witness-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 (base/'catalog-witness-1001digit-input.json').write_text(json.dumps(big_input,indent=2)+'\n')
 (base/'catalog-witness-1001digit-result.json').write_text(json.dumps(big_result,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':check()
