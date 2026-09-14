"""Negative fixtures for the independent complete sharp-ratio replay."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=argparse.ArgumentParser();p.add_argument('--checker',type=Path,required=True)
p.add_argument('--common-checker',type=Path,required=True)
p.add_argument('--graph',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();checker=module(a.checker,'independent_sharp');common=module(a.common_checker,'independent_common')
d=json.loads(a.graph.read_text());assert d['number_rows']==3
cases=[]
x=copy.deepcopy(d);x['roots'].pop();cases.append(('omitted-root',x))
x=copy.deepcopy(d);next(n for n in x['states'] if n['children'])['children'].pop();cases.append(('omitted-child',x))
x=copy.deepcopy(d);x['complete']=False;cases.append(('incomplete-certificate',x))
x=copy.deepcopy(d);x['states'][0]['minimum_period']=1;cases.append(('lost-physical-period',x))
x=copy.deepcopy(d);next(e for e in x['roots'] if e['row'][0]==4)['row'][1]=15
cases.append(('forbidden-ratio-equality',x))
results=[]
with tempfile.TemporaryDirectory() as td:
    for name,data in cases:
        path=Path(td)/(name+'.json');path.write_text(json.dumps(data))
        try: checker.audit(path,3,common)
        except AssertionError: results.append(dict(fixture=name,rejected=True))
        else: raise AssertionError('mutant accepted: '+name)
a.output.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
