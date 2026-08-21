import sys, os, math, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed import load_record, build_from_faces
from refine import refine, triangulate
from tri_group import Cover

a, faces = load_record()
pg = int(sys.argv[1]) if len(sys.argv) > 1 else 1
nf, bites = refine(a, faces, per_gap=pg)
V, tris, grp = triangulate(a, nf, bites)
C = Cover(a, V, tris, grp)
print("per_gap=%d  vertices %d  triangles %d  groups %d  valid %s"
      % (pg, len(V), len(tris), C.ng, C.all_ok()))
print("seed max diam^2 %.12f  a_max %.7f" % (C.maxd(), a / math.sqrt(C.maxd())))
# area control: the triangles must still tile T_a
tot = 0.0
for t in C.tris:
    p, q, r = C.V[t[0]], C.V[t[1]], C.V[t[2]]
    tot += 0.5 * ((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]))
print("uv-area of triangulation %.10f   uv-area T_a %.10f   diff %.2e"
      % (tot, a*a/2, tot - a*a/2))
t0 = time.time()
d = C.descend(ps=(4., 20., 100., 500., 2500.), step0=0.02)
print("after descent max diam^2 %.12f  a_max %.7f   (%.1fs)"
      % (d, a / math.sqrt(d), time.time()-t0))
