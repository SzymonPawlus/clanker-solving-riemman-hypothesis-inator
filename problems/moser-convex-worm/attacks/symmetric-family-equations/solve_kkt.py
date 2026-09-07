#!/usr/bin/env python3
"""Numerical locator for the exact active-well system in README.md."""
import math

def trig(t): return (1-t*t)/(1+t*t),2*t/(1+t*t)
def wells(x):
    ta,tb,p=x;q=.5-p;ca,sa=trig(ta);cb,sb=trig(tb)
    sd=sb*ca-cb*sa
    yo=sb*(ca*math.sqrt(3)-sa)/(4*sd);zo=math.sqrt(1-yo*yo)
    u=(2*cb+math.sqrt(3+cb*cb))/(3*sb);yc=2*u/(1+u*u)
    E=q*ca*math.sqrt(3)/4+p*sb/2
    O=q*ca*math.sqrt(3)/4+p*(cb*yo+sb*zo)/2
    M=p*sb/4+q*ca*yc
    return E,O,M
def gradients(x,h=2e-5):
    G=[]
    for k in range(3):
        row=[]
        for j in range(3):
            xp=x[:];xm=x[:];xp[j]+=h;xm[j]-=h
            row.append((wells(xp)[k]-wells(xm)[k])/(2*h))
        G.append(row)
    return G
def det(g):
    return (g[0][0]*(g[1][1]*g[2][2]-g[1][2]*g[2][1])
           -g[0][1]*(g[1][0]*g[2][2]-g[1][2]*g[2][0])
           +g[0][2]*(g[1][0]*g[2][1]-g[1][1]*g[2][0]))
def equations(x):
    z=wells(x);return z[0]-z[1],z[0]-z[2],det(gradients(x))
def solve3(A,b):
    A=[list(r)+[z] for r,z in zip(A,b)]
    for i in range(3):
        k=max(range(i,3),key=lambda j:abs(A[j][i]));A[i],A[k]=A[k],A[i]
        z=A[i][i]
        for j in range(i,4):A[i][j]/=z
        for k in range(3):
            if k==i:continue
            z=A[k][i]
            for j in range(i,4):A[k][j]-=z*A[i][j]
    return [A[i][3] for i in range(3)]
def multipliers(G):
    a,b=G[0][0]-G[2][0],G[1][0]-G[2][0]
    c,d=G[0][1]-G[2][1],G[1][1]-G[2][1];e,f=-G[2][0],-G[2][1]
    den=a*d-b*c;l0=(e*d-b*f)/den;l1=(a*f-e*c)/den
    return l0,l1,1-l0-l1
def cross3(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def quadratic(H,t):return sum(t[i]*H[i][j]*t[j] for i in range(3) for j in range(3))
def hessians(x,h=2e-4):
    base=wells(x);out=[]
    for k in range(3):
        H=[[0.]*3 for _ in range(3)]
        for i in range(3):
            xp=x[:];xm=x[:];xp[i]+=h;xm[i]-=h
            H[i][i]=(wells(xp)[k]-2*base[k]+wells(xm)[k])/(h*h)
            for j in range(i):
                xpp=x[:];xpm=x[:];xmp=x[:];xmm=x[:]
                xpp[i]+=h;xpp[j]+=h;xpm[i]+=h;xpm[j]-=h
                xmp[i]-=h;xmp[j]+=h;xmm[i]-=h;xmm[j]-=h
                H[i][j]=H[j][i]=(wells(xpp)[k]-wells(xpm)[k]-wells(xmp)[k]+wells(xmm)[k])/(4*h*h)
        out.append(H)
    return out
def constrained_curvature(x,G):
    H=hessians(x);d1=[G[0][i]-G[1][i] for i in range(3)];d2=[G[0][i]-G[2][i] for i in range(3)]
    t=cross3(d1,d2);z=math.sqrt(sum(a*a for a in t));t=[a/z for a in t]
    A=[d1,d2,t];b=[-quadratic([[H[0][i][j]-H[1][i][j] for j in range(3)] for i in range(3)],t),
                      -quadratic([[H[0][i][j]-H[2][i][j] for j in range(3)] for i in range(3)],t),0.]
    acc=solve3(A,b);curv=sum(G[0][i]*acc[i] for i in range(3))+quadratic(H[0],t)
    return t,acc,curv
def main():
    x=[.01886,.8005085,.34141265]
    for _ in range(8):
        f=equations(x);h=2e-5;J=[[0.]*3 for _ in range(3)]
        for j in range(3):
            xp=x[:];xm=x[:];xp[j]+=h;xm[j]-=h;fp=equations(xp);fm=equations(xm)
            for i in range(3):J[i][j]=(fp[i]-fm[i])/(2*h)
        dx=solve3(J,[-z for z in f]);x=[a+b for a,b in zip(x,dx)]
    print('parameters',x);print('wells',wells(x));print('equations',equations(x))
    G=gradients(x);print('gradients',G);print('multipliers',multipliers(G))
    print('equioscillation tangent/acceleration/curvature',constrained_curvature(x,G))
if __name__=='__main__':main()
