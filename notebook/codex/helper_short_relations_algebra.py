"""Exact arithmetic and boundary regression for the short-relation proof audit."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    N=32768;D=2*N-2
    rho=F(2,15)+F(13,15*(D+1));beta=F(9,625)-F(225,2*N)
    bound=8*rho-7*beta
    assert rho==F(131083,983025) and beta==F(449199,40960000)
    assert bound==F(1594490420447,1610588160000)<1
    kernel_checks=[]
    for n in list(range(2,51))+[N]:
        A=F(n*n+2*sum(k*k for k in range(1,n)),n*n)
        assert A==F(2*n*n+1,3*n)
        moment=F(1,2)-F(1,4*n*n)
        assert moment/A<F(3,4*n)
        kernel_checks.append(n)
    fixtures=[]
    for m in range(1,501):
        M=3*m+5;v=M-m;w=M-1
        common=[j for j in range(M)
                if all(min(s*(15*j+1)%(15*M),(-s*(15*j+1))%(15*M))<M
                       for s in(v,w))]
        expected=[3*k for k in range((m+74)//75)]
        assert common==expected,(m,common,expected)
        if m%75 in(0,1,74):
            fixtures.append({'m':m,'M':M,'intersection':common,'count':len(common),
                             'periods':[M//gcd(M,v),M//gcd(M,w)]})
        assert 3*v+5*w==7*M
    result={'status':'sketch; exact algebra and bounded regression of self-contained proof; cross-family review required',
            'proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'N':N,'D':D,'rho':str(rho),'beta':str(beta),
            'union_upper_bound':str(bound),'gap':str(1-bound),
            'kernel_constant_coefficient_checks':kernel_checks,
            'sparse_pair_m_range':[1,500],'sparse_pair_cases_checked':500,
            'boundary_fixtures':fixtures}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS exact constants and 500 direct sparse-pair fixtures')
