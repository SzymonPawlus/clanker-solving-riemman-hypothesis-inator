"""Portable tracked-only replay of the all-44 and structural checkpoints.

Pass the prover's issue-304 directory, whose sole required file is the committed
all-forty-four-cores.json. No historical untracked individual certificates are
needed. State graphs remain a separate audit until independently accepted.
"""
from pathlib import Path
from hashlib import sha256
import json
import argparse,subprocess,sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prover-dir',required=True)
    p.add_argument('--output-dir',required=True)
    a=p.parse_args();source=Path(__file__).parent
    cert=Path(a.prover_dir).resolve();out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((source/'helper-validated-manifest.json').read_text())
    root=source.parent.parent
    for relative,expected in manifest['files'].items():
        assert sha256((root/relative).read_bytes()).hexdigest()==expected,relative
    for name,expected in manifest['external_inputs'].items():
        assert sha256((cert/name).read_bytes()).hexdigest()==expected,name
    def run(script,*args):
        subprocess.run([sys.executable,str(source/script),*map(str,args)],check=True)
    run('helper_all44_audit.py',cert/'all-forty-four-cores.json',
        '--output',out/'all44-audit.json')
    executable=out/'period16-audit'
    subprocess.run(['c++','-std=c++17','-O3',str(source/'helper_period16_audit.cpp'),'-o',str(executable)],check=True)
    table=out/'period16-topcharges.txt'
    with table.open('w') as f:subprocess.run([str(executable)],stdout=f,check=True)
    run('helper_period16_summary.py',table,'--output',out/'period16-audit.json')
    run('helper_conditional_core_census.py','--output',out/'conditional-census.json')
    census=json.loads((out/'conditional-census.json').read_text())
    assert len(census['anchors'])==37 and all(r['complete'] for r in census['anchors'])
    found=[tuple(c['speeds']) for r in census['anchors'] for c in r['primitive_certificates']]
    cores=json.loads((source/'helper-fortyfour-primitive-cores.json').read_text())
    expected=[tuple(c['speeds']) for c in cores['cores']]
    assert len(found)==len(set(found))==44 and set(found)==set(expected)
    summary={'status':'sketch; independent Claude or human review required',
             'complete':True,'source_manifest_sha256':sha256((source/'helper-validated-manifest.json').read_bytes()).hexdigest(),
             'core_count':44,'conditional_anchors_complete':37,
             'outputs':{p.name:sha256(p.read_bytes()).hexdigest()
                        for p in (out/'all44-audit.json',out/'period16-audit.json',
                                  out/'period16-topcharges.txt',out/'conditional-census.json')}}
    (out/'replay-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('All tracked-only all44, period16 and conditional-classification replays passed.')

if __name__=='__main__':main()
