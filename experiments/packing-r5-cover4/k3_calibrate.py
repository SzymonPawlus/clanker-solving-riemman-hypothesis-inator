"""k = 3 calibration (n = 5, a = 2).

Claim being reconstructed (cited, Melissen): a(5) = 2 in Oler normalisation,
i.e. s(5) = 4 + 2*sqrt(3) in repo normalisation.

Covering route:  a dissection of T(k-1) into m pieces of squared diameter <= 1
scales, for every a < k-1, to a cover of T(a) by m pieces of diameter
a/(k-1) < 1.  Hence any m+1 points of T(a) contain two at distance < 1, so
a(m+1) >= k-1.

k = 3 needs m = Delta(3) - 2 = 4 pieces for T(2).  The medial subdivision does it.
Everything below is verified exactly in Q(sqrt 3); no floats are consulted.
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exactgeom import *
from fractions import Fraction as F

H = Q3(F(1, 2))


def medial_pieces(a):
    """The four triangles of the medial subdivision of T(a) (side a/2 each)."""
    A, B, C = triangle(a)
    MAB = ((A[0] + B[0]) * H, (A[1] + B[1]) * H)
    MBC = ((B[0] + C[0]) * H, (B[1] + C[1]) * H)
    MCA = ((C[0] + A[0]) * H, (C[1] + A[1]) * H)
    return [[A, MAB, MCA], [MAB, B, MBC], [MCA, MBC, C], [MAB, MBC, MCA]]


def centroid_kites(a):
    """Negative control: the 3-piece centroid dissection of T(a)."""
    A, B, C = triangle(a)
    G = ((A[0] + B[0] + C[0]) * Q3(F(1, 3)), (A[1] + B[1] + C[1]) * Q3(F(1, 3)))
    MAB = ((A[0] + B[0]) * H, (A[1] + B[1]) * H)
    MBC = ((B[0] + C[0]) * H, (B[1] + C[1]) * H)
    MCA = ((C[0] + A[0]) * H, (C[1] + A[1]) * H)
    return [[A, MAB, G, MCA], [MAB, B, MBC, G], [G, MBC, C, MCA]]


def run(label, a, pieces, strict=False):
    t0 = time.time()
    ok, rep = verify_cover(a, pieces, strict=strict)
    dt = time.time() - t0
    print(f"--- {label}: a={a}, {len(pieces)} pieces, strict={strict} -> OK={ok}"
          f"   ({dt*1000:.1f} ms)")
    for k, v in rep.items():
        print(f"      {k}: {v}")
    return ok, rep, dt


if __name__ == "__main__":
    res = {}
    # 1. THE CALIBRATION: 4 pieces of diameter <= 1 dissect T(2).
    ok4, rep4, dt4 = run("k=3 YES  T(2) by 4 medial triangles", 2, medial_pieces(2))
    res["k3_medial_T2"] = {"ok": ok4, "ms": dt4 * 1000}
    assert ok4

    # 2. The scaled statement actually used: for a < 2 the same dissection has
    #    squared diameter (a/2)^2 < 1 STRICTLY.  Check at a = 199/100.
    a = F(199, 100)
    ok4s, rep4s, dt4s = run("k=3 YES  T(199/100) by 4 medial triangles", a,
                            medial_pieces(a), strict=True)
    res["k3_medial_T199_100_strict"] = {"ok": ok4s, "ms": dt4s * 1000}
    assert ok4s

    # 3. Negative control: 3 pieces via the centroid dissection cover T(2) but
    #    FAIL the diameter test (diam^2 = 4/3 > 1).  The machinery must say so.
    ok3, rep3, dt3 = run("k=3 control  T(2) by 3 centroid kites", 2, centroid_kites(2))
    res["k3_kites_T2_should_fail_diam"] = {"ok": ok3, "ms": dt3 * 1000}
    assert not ok3, "negative control unexpectedly passed"
    assert rep3["covers"] is True, "3 kites must still COVER T(2); only diameter fails"

    # 4. Negative control: drop one of the four medial triangles.  Coverage must fail.
    p = medial_pieces(2)[:3]
    ok3b, rep3b, dt3b = run("k=3 control  T(2) by 3 of the 4 medial triangles", 2, p)
    res["k3_medial_minus_one_should_fail_cover"] = {"ok": ok3b, "ms": dt3b * 1000}
    assert not ok3b and rep3b["covers"] is False

    # 5. The kites DO work at a = 3/2 < sqrt(3): validates the same machine at a
    #    second (m, a) pair with a cited answer, a(4) = sqrt(3).
    okk, repk, dtk = run("k=? control  T(3/2) by 3 centroid kites", F(3, 2),
                         centroid_kites(F(3, 2)), strict=True)
    res["kites_T3_2_strict"] = {"ok": okk, "ms": dtk * 1000}
    assert okk

    print("\nALL k=3 CALIBRATION CHECKS PASSED")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "k3_results.json"), "w"), indent=2)
