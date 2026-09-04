"""Step zero: re-derive the Q(sqrt 3) closed forms against the published table.

This checks a NUMERICAL coincidence, not a theorem: it shows that the published
best-known values for n = 17, 24, 31 agree with 6+4sqrt3, 8+4sqrt3, 10+4sqrt3 to
the full precision at which they are published.  It does not establish that the
published values ARE those numbers.
"""
import sys, os
from mpmath import mp, mpf, sqrt

mp.dps = 40
REF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "circle-packing-search")
sys.path.insert(0, os.path.abspath(REF_DIR))
import reference as R   # published m(n), Graham-Lubachevsky 1995, 15 s.f.

r3 = sqrt(mpf(3))
CONJ = {17: (6, 4), 24: (8, 4), 31: (10, 4)}   # s = a + b sqrt3

print("published m(n) from %s (Graham-Lubachevsky 1995, 15 s.f.)" % os.path.normpath(REF_DIR))
print()
print(" n   conjectured s        m implied by it            m published            agree s.f.")
for n, (a, b) in sorted(CONJ.items()):
    s = a + b * r3
    d = s - 2 * r3
    m_conj = 2 / d
    m_pub = mpf(R.GL_D[n])
    err = abs(m_conj - m_pub)
    digits = mp.mpf('inf') if err == 0 else -mp.log10(err / abs(m_pub))
    print(" %2d  %d + %d*sqrt(3)   %s   %s   %.1f"
          % (n, a, b, mp.nstr(m_conj, 18), mp.nstr(m_pub, 18), float(digits)))
    # The table stores m to 15 significant figures, so the strongest agreement
    # attainable is a match to within one unit in the last published place.
    ulp = abs(m_pub) * mpf(10) ** (-14)
    assert err <= mpf('1.5') * ulp, "n=%d does NOT match the published value" % n
print()
print("All three agree with the published m(n) to within 1.5 units in the last")
print("published significant figure (n = 17 and 31 exactly to 15 s.f.; n = 24")
print("differs by 1 in the 15th, i.e. the published 0.174457630187010 against")
print("0.174457630187009439 -- a last-place rounding difference in the table,")
print("the same 1-ulp offset already recorded in ../circle-packing-ls/README.md).")
print()
print("status: numerical.  This is agreement of a float table with a closed form;")
print("it is EVIDENCE that the published optima lie in Q(sqrt 3), not a proof.")
