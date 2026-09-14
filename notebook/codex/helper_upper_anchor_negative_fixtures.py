"""Reproducible rejection fixtures for the independent upper-anchor checker."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile


def module(path, name):
    spec = importlib.util.spec_from_file_location(name,path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


p = argparse.ArgumentParser()
p.add_argument('--checker',type=Path,required=True)
p.add_argument('--common-checker',type=Path,required=True)
p.add_argument('--graph',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a = p.parse_args()
checker = module(a.checker,'upper_independent')
common = module(a.common_checker,'common_independent')
data = json.loads(a.graph.read_text())
cases=[]
x=copy.deepcopy(data);x['roots'].pop();cases.append(('omitted-root',x))
x=copy.deepcopy(data);x['states'][0]['children'].pop();cases.append(('omitted-child',x))
x=copy.deepcopy(data);x['complete']=False;cases.append(('incomplete-graph',x))
x=copy.deepcopy(data);x['states'][0]['minimum_period']=1;cases.append(('lost-physical-period-bound',x))
x=copy.deepcopy(data)
next(r for r in x['roots'] if r['row'][0]==12)['row'][1]=13
cases.append(('forbidden-ratio-equality',x))
out=[]
with tempfile.TemporaryDirectory() as td:
    for name,mutation in cases:
        path=Path(td)/(name+'.json');path.write_text(json.dumps(mutation))
        try: checker.audit(path,common)
        except AssertionError: out.append(dict(fixture=name,rejected=True))
        else: raise AssertionError('mutant wrongly accepted: '+name)
a.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
