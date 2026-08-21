"""Control: reproduce the record with the triangulated-group representation."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed import load_record, build_from_faces
from tri_group import Cover

a, faces = load_record()
V, tris, grp = build_from_faces(a, faces)
C = Cover(a, V, tris, grp)
print("a = %.6f  vertices %d  triangles %d  groups %d" % (a, len(V), len(tris), C.ng))
print("all triangles positively oriented:", C.all_ok())
print("seed max diam^2 = %.12f   a_max = %.6f" % (C.maxd(), a / math.sqrt(C.maxd())))
d = C.descend(ps=(4., 20., 100., 500., 2500.), step0=0.03)
print("after descent max diam^2 = %.12f   a_max = %.6f" % (d, a / math.sqrt(d)))
