"""Meaningful rejection fixtures for the independent certificate acceptance path."""
import argparse
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import tempfile
from helper_all44_audit import audit


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('manifest',type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(); source=Path(__file__).parent
    original=json.loads(a.manifest.read_text())
    mutations=[]
    def add(name,change):
        data=deepcopy(original);change(data);mutations.append((name,data))
    add('negative_weight',lambda d:d['cases'][0]['atoms'][0].__setitem__(1,'-1/1000'))
    add('unsafe_atom',lambda d:d['cases'][0]['atoms'][0].__setitem__(0,'0'))
    add('stale_total',lambda d:d['cases'][0].__setitem__('total','61/10'))
    add('missing_core',lambda d:d['cases'].pop())
    add('zero_weight_unsafe_atom',lambda d:d['cases'][0]['atoms'].append(['0','0']))
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='helper-all44-negative-') as temp:
        temp=Path(temp);exe=temp/'grid'
        subprocess.run(['c++','-std=c++17','-O3',str(source/'helper_all44_grid.cpp'),'-o',str(exe)],check=True)
        for name,data in mutations:
            path=temp/(name+'.json');path.write_text(json.dumps(data))
            try:audit(path,source/'helper-fortyfour-primitive-cores.json',exe,temp/'output.json')
            except AssertionError:rejected.append(name)
            else:raise RuntimeError('invalid certificate accepted: '+name)
    result={'rejected':rejected,'input_sha256':sha256(a.manifest.read_bytes()).hexdigest(),
            'fixture_source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'checker_sha256':sha256((source/'helper_all44_audit.py').read_bytes()).hexdigest()}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('Rejected all',len(rejected),'invalid fixtures.')
