"""Independent re-run of the r4-famcert Gate-1/Gate-2 table with MY checker and MY
transcription of the generator, so the audit does not inherit their numbers."""
from q3 import Q3
import checker as ck, famgen

print(("%-3s %-4s %-16s %-6s %-6s %-8s %-9s %-6s" %
      ("j", "n", "s", "feas", "tight", "minsq=4", "contacts", "bdry")).rstrip())
for j in range(0, 8):
    pts = famgen.generate(j)
    n = famgen.law_n(j)
    assert len(pts) == n, (j, len(pts), n)
    rep = ck.check(pts, famgen.s_of(j), n)
    print(("%-3d %-4d %-16s %-6s %-6s %-8s %-9d %-6d" %
          (j, n, famgen.s_of(j).sexpr(), rep["ok"], rep["tight"],
           rep["min_sq_distance_is_exactly_4"], rep["n_contacts"], rep["n_boundary"])).rstrip())
    for f in rep["failures"][:3]:
        print("     FAIL", f)
