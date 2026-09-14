"""Exact constants for the C1/second-moment relation-window improvement."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
N=1500;D=2*N-2;epsilon=F(7,300);alpha=F(2,15)-epsilon
norm=sum((1-F(abs(k),N))**2 for k in range(1-N,N))
assert norm==F(2*N*N+1,3*N) and norm>=F(2*N,3)
raw_second=F(1,12*N)+F(1,4*N)-F(1,4*N*N)
assert raw_second<=F(1,3*N)
assert raw_second/norm<=F(1,2*N*N)
product_error_bound=F(10,4)/(epsilon*epsilon*N*N)
assert product_error_bound==F(1,490)
beta=alpha*alpha-product_error_bound
rho=F(2,15)+F(13,15*(D+1))
union=8*rho-7*beta
assert alpha==F(11,100) and beta==F(4929,490000)
assert union==F(628885787,629790000) and union<1
report={'status':'exact arithmetic passed; analytic proof requires review','N':N,'D':D,'epsilon':str(epsilon),'alpha':str(alpha),'product_error_upper':str(product_error_bound),'beta':str(beta),'tree_union_upper':str(union),'tree_slack':str(1-union),'affine_P_Q_bound':D*D,'affine_R_strict_bound':4*D*D,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('smooth-relations-2998-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
