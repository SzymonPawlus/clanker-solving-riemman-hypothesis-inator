"""Reject deliberate mutations of independently replayed graph certificates."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--checker', type=Path, required=True)
p.add_argument('--manager-graph', type=Path, required=True)
p.add_argument('--prover-graph', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
spec = importlib.util.spec_from_file_location('independent_graph_checker', a.checker)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
manager = json.loads(a.manager_graph.read_text())
prover = json.loads(a.prover_graph.read_text())
cases = []
x = copy.deepcopy(manager)
x['states'][0]['edges'].pop()
cases.append(('omitted-qualifying-child', x, 'no3'))
x = copy.deepcopy(manager)
x['states'][0]['edges'][0]['numerator'] = 0
cases.append(('invalid-representative', x, 'no3'))
x = copy.deepcopy(prover)
x['root_ids'] = []
cases.append(('missing-root', x, 'no2'))
x = copy.deepcopy(prover)
x['complete'] = False
cases.append(('incomplete-campaign', x, 'no2'))
x = copy.deepcopy(prover)
x['nodes'][0]['kind'] = 'dual'
cases.append(('unexpected-dual-leaf', x, 'no2'))
x = copy.deepcopy(prover)
x['nodes'][0]['residual'] = [1, 1, 2]
cases.append(('duplicate-residue', x, 'no2'))
results = []
with tempfile.TemporaryDirectory() as td:
    for name, data, mode in cases:
        path = Path(td) / (name + '.json')
        path.write_text(json.dumps(data))
        try:
            m.audit(path, mode)
        except AssertionError:
            results.append(dict(fixture=name, rejected=True))
        else:
            raise AssertionError('mutant wrongly accepted: ' + name)
a.output.write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results))
