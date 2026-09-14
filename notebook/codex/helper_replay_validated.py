"""Portable replay of frozen validated helper checkpoints (no state graphs).

Pass the prover's issue-304 certificate directory explicitly. New repaired
state-dual graphs are intentionally a separate audit until accepted.
"""
from pathlib import Path
import argparse,subprocess,sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prover-dir',required=True)
    p.add_argument('--output-dir',required=True)
    a=p.parse_args();source=Path(__file__).parent
    cert=Path(a.prover_dir).resolve();out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    def run(script,*args):
        subprocess.run([sys.executable,str(source/script),*map(str,args)],check=True)
    for name,P in [('p18','1,5,6,7,9,11,13,18'),('p18-6-14','1,5,6,9,11,13,14,18'),
                   ('p18-12-7','1,5,7,9,11,12,13,18'),('p18-12-14','1,5,9,11,12,13,14,18')]:
        run('helper_p18_dual_check.py',cert/(name+'-weights.tsv'),'--primitive',P,
            '--output',out/(name+'-audit.json'))
    names=[f'p24-{i}-interior-certificate.json' for i in(1,2,4)]
    names += [f'p30-{i}-interior-certificate.json' for i in range(1,8)]
    names += [f'p24-{i}-certificate.json' for i in(3,5,6,7,8)]
    names += ['p30-8-certificate.json']
    names += [f'new-core-{i}-interior-certificate.json' for i in(1,2,3)]
    run('helper_generic_dual_check.py',*(cert/name for name in names),'--output',out/'generic-audit.json')
    executable=out/'period16-audit'
    subprocess.run(['c++','-std=c++17','-O3',str(source/'helper_period16_audit.cpp'),'-o',str(executable)],check=True)
    table=out/'period16-topcharges.txt'
    with table.open('w') as f:subprocess.run([str(executable)],stdout=f,check=True)
    run('helper_period16_summary.py',table,'--output',out/'period16-audit.json')
    run('helper_conditional_core_census.py','--output',out/'conditional-census.json')
    print('All frozen universal-dual, period16 and conditional-classification replays passed.')

if __name__=='__main__':main()
