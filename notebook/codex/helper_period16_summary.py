"""Exact rational summation of the independent C++ period-16 audit table."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import argparse,json

def summarize(path):
    records=[]
    for line in path.read_text().splitlines():
        values=list(map(int,line.split()))
        p,a,b=values[:3];B=values[3:3+b];rest=values[3+b:]
        assert len(rest)==24
        leaders=[]
        for i in range(0,24,4):
            h,aa,num,den=rest[i:i+4]
            leaders.append({'h':h,'a':aa,'charge':str(F(num,den))})
        total=F(b,p)+sum(F(x['charge']) for x in leaders)
        assert total<1,(p,a,B,total)
        records.append({'p':p,'a':a,'B':B,'total':str(total),'leaders':leaders})
    assert len(records)==2472
    maximum=max(F(r['total']) for r in records)
    return {'bases_checked':len(records),'maximum':str(maximum),
            'worst':[r for r in records if F(r['total'])==maximum],
            'source_sha256':sha256(Path(__file__).with_name('helper_period16_audit.cpp').read_bytes()).hexdigest(),
            'table_sha256':sha256(path.read_bytes()).hexdigest(),'all_bases':records}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('table');p.add_argument('--output',required=True)
    a=p.parse_args();out=summarize(Path(a.table))
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print('bases',out['bases_checked'],'maximum',out['maximum'])
