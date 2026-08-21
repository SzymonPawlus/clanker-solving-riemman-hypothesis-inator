"""Refine the n=16 hypothesis to 60+ digits by Newton on the contact system (mpmath).

Optimiser output is a hypothesis (problem RULES.md 0); this only sharpens the hypothesis.
Nothing here is exact and nothing here is a certificate.
"""
import json, math, pathlib, sys
from mpmath import mp, mpf, matrix, lu_solve, sqrt as msqrt, nstr

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from system import residuals, points, free_symbols_layout, CONTACTS, RATTLER

mp.dps = 80
S3 = msqrt(3)

SRC = pathlib.Path(__file__).resolve().parents[1] / "circle-packing-search" / "out" / "n16.json"


def initial():
    data = json.loads(SRC.read_text())
    m = data["m_min_pairwise_distance_unit_triangle"]
    d0 = 2.0 / m
    # normalisation assertion: s = d + 2 sqrt(3), separation-2 convention (RULES.md 2)
    assert abs((d0 + 2 * math.sqrt(3)) - data["s_side_for_unit_circles"]) < 1e-9
    P = {i: (x * d0, y * d0) for i, (x, y) in enumerate(data["unit_triangle_points"])}
    XY = {i: (mpf(x), mpf(y) / S3) for i, (x, y) in P.items()}   # shear to (X,Y)
    d = mpf(d0)
    return d, XY


def jac(f, v, h=None):
    n = len(v)
    F0 = f(v)
    m = len(F0)
    J = matrix(m, n)
    eps = mpf(10) ** (-mp.dps + 12)
    for k in range(n):
        vp = list(v); vp[k] = vp[k] + eps
        vm = list(v); vm[k] = vm[k] - eps
        Fp, Fm = f(vp), f(vm)
        for r in range(m):
            J[r, k] = (Fp[r] - Fm[r]) / (2 * eps)
    return F0, J


def newton(v):
    for it in range(200):
        F, J = jac(residuals, v)
        nrm = max(abs(x) for x in F)
        step = lu_solve(J, matrix([-x for x in F]))
        v = [v[k] + step[k] for k in range(len(v))]
        snrm = max(abs(step[k]) for k in range(len(v)))
        if snrm < mpf(10) ** (-mp.dps + 5):
            return v, nrm, it
    raise RuntimeError("Newton did not converge")


def main():
    d, XY = initial()
    v0 = [d, XY[5][0], XY[11][0],
          XY[1][0], XY[1][1], XY[2][0], XY[2][1], XY[9][0], XY[9][1],
          XY[14][0], XY[14][1], XY[15][0], XY[15][1]]
    v, nrm, it = newton(v0)
    names = free_symbols_layout()
    print(f"Newton converged in {it} iterations, residual before last step {nstr(nrm,5)}")
    print(f"final max |residual| = {nstr(max(abs(x) for x in residuals(v)), 5)}")
    for nm, val in zip(names, v):
        print(f"  {nm:4s} = {nstr(val, 50)}")
    dstar = v[0]
    print()
    print(f"d      = {nstr(dstar, 50)}")
    print(f"s      = {nstr(dstar + 2*S3, 50)}")
    print(f"m=2/d  = {nstr(2/dstar, 50)}   (Graham-Lubachevsky d(16) = 0.216227269309782)")

    # full point set incl. rattler, in (X,Y)
    P = points(*v)
    out = {int(k): [nstr(a, 60), nstr(b, 60)] for k, (a, b) in P.items()}
    # rattler 4 from the float file, sheared
    data = json.loads(SRC.read_text())
    m0 = data["m_min_pairwise_distance_unit_triangle"]
    rx, ry = data["unit_triangle_points"][4]
    out[4] = [nstr(mpf(rx) * (2 / mpf(m0)), 60), nstr(mpf(ry) * (2 / mpf(m0)) / S3, 60)]
    pathlib.Path(__file__).resolve().parent.joinpath("out", "refined.json").write_text(
        json.dumps({"dps": mp.dps, "d": nstr(dstar, 60), "s": nstr(dstar + 2*S3, 60),
                    "XY": out, "note": "sheared coords: x=X, y=sqrt(3)*Y. NUMERICAL, not a certificate."},
                   indent=1))

    # verify the *full* 120-pair separation and containment numerically at 80 digits
    xy = {k: (a, b) for k, (a, b) in P.items()}
    xy[4] = (mpf(rx) * (2 / mpf(m0)), mpf(ry) * (2 / mpf(m0)) / S3)
    worst = None
    for i in range(16):
        for j in range(i + 1, 16):
            q = (xy[i][0]-xy[j][0])**2 + 3*(xy[i][1]-xy[j][1])**2
            if worst is None or q < worst[0]:
                worst = (q, i, j)
    print(f"\nmin squared distance over all 120 pairs = {nstr(worst[0], 40)}  at {worst[1]}-{worst[2]}")
    dmin = max(xy[i][0] + xy[i][1] for i in range(16))
    print(f"exact minimal enclosing d (max X+Y)      = {nstr(dmin, 40)}")
    print(f"d - dmin                                  = {nstr(dstar - dmin, 10)}")

    # contact check at high precision: which pairs are within 1e-30 of 2?
    print("\npairs with squared distance in [4, 4+1e-12):")
    for i in range(16):
        for j in range(i + 1, 16):
            q = (xy[i][0]-xy[j][0])**2 + 3*(xy[i][1]-xy[j][1])**2
            if q - 4 < mpf(10)**-12:
                print(f"   {i:2d}-{j:2d}  q-4 = {nstr(q-4, 6)}")


if __name__ == "__main__":
    main()
