"""Independent exact constants for the C1 squared-Fejer smoothing audit."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    N=1500;D=2*N-2;epsilon=F(7,300);alpha=F(2,15)-epsilon
    product_error_cap=F(10,4)/(epsilon**2*N**2)
    beta=alpha**2-product_error_cap
    rho=F(2,15)+F(13,15*(D+1));tree=8*rho-7*beta
    assert alpha==F(11,100) and product_error_cap==F(1,490)
    assert beta==F(4929,490000)
    assert tree==F(628885787,629790000)<1
    assert D**2==8988004 and 4*D**2==35952016
    checked=[]
    for n in list(range(2,101))+[N]:
        normalization=F(n*n+2*sum(j*j for j in range(1,n)),n*n)
        assert normalization==F(2*n*n+1,3*n)
        raw_second=F(1,12*n)+F(1,4*n)-F(1,4*n*n)
        assert raw_second==F(1,3*n)-F(1,4*n*n)
        assert raw_second/normalization<=F(1,2*n*n)
        checked.append(n)
    # x^4(1-x)^4=(1+x^2)Q(x)-4, integral Q=22/7.
    Q=[4,0,-4,0,5,-4,1]
    product=[0]*9
    for i,c in enumerate(Q):product[i]+=c;product[i+2]+=c
    product[0]-=4
    assert product==[0,0,0,0,1,-4,6,-4,1]
    assert sum(F(c,i+1) for i,c in enumerate(Q))==F(22,7)
    assert F(22,7)**2<10
    result={'status':'sketch; exact arithmetic supports separately audited analytic proof',
            'proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'N':N,'D':D,'epsilon':str(epsilon),'alpha':str(alpha),
            'strict_product_error_upper_bound':str(product_error_cap),
            'beta':str(beta),'rho':str(rho),'tree_upper_bound':str(tree),
            'gap':str(1-tree),'affine_slope_denominator_bound':D**2,
            'affine_constant_strict_bound':4*D**2,
            'second_moment_normalizations_checked':checked,
            'pi_squared_bound':'positive integral of x^4(1-x)^4/(1+x^2) gives pi<22/7 and (22/7)^2<10'}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS exact second-moment constants; tree gap',1-tree)
