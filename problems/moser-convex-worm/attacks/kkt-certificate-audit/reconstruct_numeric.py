#!/usr/bin/env python3
"""Independent floating-point reconnaissance; never used as a certificate."""
from math import atan, cos, pi, sin, sqrt

tb,ta,p=43133/53882,929/49257,7381/21619
q=.5-p
beta,alpha=2*atan(tb),2*atan(ta)
theta=(-beta,-alpha,alpha,beta,pi)
L=(p,q,q,p,2*(p*cos(beta)+q*cos(alpha)))

def fan_floor(ids,x):
    out=[]
    for i in ids:
        z=0
        for j,a in zip(ids,x):
            d=theta[j]-theta[i]
            qx,qy=sin(d),-cos(d)
            z += a*max(0,qx/2,(qx+sqrt(3)*qy)/4)
        out.append(z/2)
    return min(out)

z=q*sin(alpha)/sin(beta)
raw=(
 ("S",(),()),
 ("C",(1,2,4),(q,q,2*q*cos(alpha))),
 ("A",(0,2,4),(z,q,z*cos(beta)+q*cos(alpha))),
 ("D",(1,3,4),(q,z,q*cos(alpha)+z*cos(beta))),
 ("B",(0,3,4),(p,p,2*p*cos(beta))),
)
data=[]
for name,ids,x in raw:
    load=[0.]*5
    for i,a in zip(ids,x): load[i]=a
    data.append((name,fan_floor(ids,x) if ids else 0,load))

def g(d,phi):
    return d[1]+sum((a-b)*abs(sin(t-phi)) for a,b,t in zip(L,d[2],theta))/4

last=None; changes=[]; low=(1,0,"")
for k in range(1000001):
    phi=(pi/2)*k/1000000
    best=max((g(d,phi),d[0]) for d in data)
    if best[1]!=last:
        changes.append((phi, __import__('math').tan(phi/2),best))
        last=best[1]
    if best[0]<low[0]: low=(best[0],phi,best[1])
print("changes",*changes,sep="\n")
print("sample floor",low)
print("phi=0",[(d[0],g(d,0)) for d in data])

from itertools import combinations
vec=[(cos(t),sin(t)) for t in theta]
print("positive circuits")
for ids in combinations(range(5),3):
    i,j,k=ids
    signed=(vec[j][0]*vec[k][1]-vec[j][1]*vec[k][0],
            vec[k][0]*vec[i][1]-vec[k][1]*vec[i][0],
            vec[i][0]*vec[j][1]-vec[i][1]*vec[j][0])
    if all(x>1e-12 for x in signed) or all(x < -1e-12 for x in signed):
        print(ids,signed)
for u in (.22434865,.22434866,.22434867,.22434868,.22434869,.22434870,.22434871,.22434872,.22434873):
    phi=2*atan(u)
    print("cut",u,"C",g(data[1],phi),"A",g(data[2],phi))
for u in (.745974,.745975,.7459751,.74597518,.7459752,.745976):
    phi=2*atan(u)
    print("central",u,"S",g(data[0],phi),"B",g(data[4],phi))
for u,names in ((.224348713,("C","A")),(.745974447,("S","B"))):
    phi=2*atan(u)
    print("certificate cut",u,[(name,g(next(d for d in data if d[0]==name),phi)-.23518745713) for name in names])
