import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/',1)[0])
import run as R, lp
T = lambda m: m*(m+1)//2
k = int(sys.argv[1]); Ms = [int(x) for x in sys.argv[2].split(',')]
deltas = [F(1,100)] if len(sys.argv)<4 else [F(1,int(x)) for x in sys.argv[3].split(',')]
n = T(k)-1
for M in Ms:
    for delta in deltas:
        a = F(k-1)-delta
        Th = [a*F(i,M) for i in range(M+1)]
        t0=time.time()
        cells,cols,caps,meta,cache = R.build(a,Th)
        cols,caps,meta = R.prune(cols,caps,meta,len(cells))
        tb=time.time()-t0
        val,y = lp.solve_cover(cols,caps,len(cells))
        oler = int(a*a/2+3*a/2+1)
        print('k=%d n=%d M=%2d a=%.5f cells=%3d boxes=%5d  floor(Oler)=%d  LP=%s  target<=%d  (build %.0fs, lp %.0fs)'
              %(k,n,M,float(a),len(cells),len(cols),oler,val,n-1,tb,time.time()-t0-tb), flush=True)
        if val is not None and val < n-1e-6:
            for j,w in enumerate(y):
                if w>1e-9:
                    lo,hi,why=meta[j]
                    print('    w=%.4f cap=%d via %-12s lo=%s hi=%s'%(w,caps[j],why,[str(x) for x in lo],[str(x) for x in hi]), flush=True)
