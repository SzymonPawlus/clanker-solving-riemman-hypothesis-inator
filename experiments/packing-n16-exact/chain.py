"""The contact chain solved as an explicit function of d (mpmath), for branch/structure probing.

NUMERICAL. Used only to (a) pick algebraic branches and (b) test whether observed coincidences
(e.g. X15 == d/2 + 1) are identities of the chain or accidents at the solution.
"""
from mpmath import mp, mpf, sqrt as msqrt, mpmathify

mp.dps = 60


def two_circles(P, Q, r2, pick):
    """Intersections of {|Z-P|^2 = 4} and {|Z-Q|^2 = 4} in the metric dX^2 + 3 dY^2.

    Subtracting gives a line; `pick` in {+1,-1} chooses the branch.
    """
    (px, py), (qx, qy) = P, Q
    # (X-px)^2+3(Y-py)^2 = (X-qx)^2+3(Y-qy)^2  ->  2(qx-px)X + 6(qy-py)Y = qx^2-px^2+3(qy^2-py^2)
    a = 2 * (qx - px)
    b = 6 * (qy - py)
    c = qx**2 - px**2 + 3 * (qy**2 - py**2)
    # parametrise the line and intersect with the first circle
    if abs(a) >= abs(b):
        # X = (c - b Y)/a
        A = ((-b / a) ** 2 + 3)
        B = 2 * (c / a - px) * (-b / a) - 6 * py
        C = (c / a - px) ** 2 + 3 * py**2 - r2
        disc = B * B - 4 * A * C
        Y = (-B + pick * msqrt(disc)) / (2 * A)
        X = (c - b * Y) / a
    else:
        A = 1 + 3 * (-a / b) ** 2
        B = -2 * px + 6 * (c / b - py) * (-a / b)
        C = px**2 + 3 * (c / b - py) ** 2 - r2
        disc = B * B - 4 * A * C
        X = (-B + pick * msqrt(disc)) / (2 * A)
        Y = (c - a * X) / b
    return (X, Y)


def chain(d, br=(-1, +1, +1, +1, +1)):
    """Given d, propagate the contact chain.  Returns all points and the closure residual."""
    d = mpmathify(d)
    b2, b15, b9, b14, b1 = br
    g = msqrt(3 * (10 - d) * (d - 2))
    Y2 = (3 * d + 6 + b2 * g) / 12
    X2 = 3 * Y2 - 2
    P3 = (d - 2, mpf(2))
    P13 = (d - 2, mpf(0))
    P12 = (d / 2 - 1, d / 2 - 1)
    P10 = (d / 2 + 1, d / 2 - 1)
    P2 = (X2, Y2)
    P15 = two_circles(P2, P3, mpf(4), b15)
    P9 = two_circles(P15, P13, mpf(4), b9)
    u = 2 * P9[0] - (d - 2)
    X14 = u / 2
    Y14 = b14 * msqrt((16 - u * u) / 12)
    t = (u + 6 * Y14) / 4
    P5 = (t, t)
    P1 = two_circles(P2, P12, mpf(4), b1)
    res = (P1[0] - t) ** 2 + 3 * (P1[1] - t) ** 2 - 4
    return dict(d=d, P1=P1, P2=P2, P3=P3, P5=P5, P9=P9, P10=P10, P12=P12, P13=P13,
                P14=(X14, Y14), P15=P15, u=u, t=t, g=g, res=res)


if __name__ == "__main__":
    from mpmath import nstr, findroot
    dstar = mpmathify("9.2495271590127914277871897476431186449900705005529")
    for lbl, dv in [("d*", dstar), ("d*+0.01", dstar + mpf("0.01")), ("d*-0.013", dstar - mpf("0.013"))]:
        c = chain(dv)
        print(f"--- {lbl}: d = {nstr(c['d'],20)}")
        print(f"    residual E_K = {nstr(c['res'], 12)}")
        print(f"    X15 - (d/2+1) = {nstr(c['P15'][0] - (c['d']/2+1), 12)}")
        print(f"    Y15 - (2*Y2 - (d/2-1)) = {nstr(c['P15'][1] - (2*c['P2'][1] - (c['d']/2-1)), 12)}")
        print(f"    X2 - (3*Y2-2) = {nstr(c['P2'][0] - (3*c['P2'][1]-2), 12)}")
        print(f"    X1 - (X2-2)  = {nstr(c['P1'][0] - (c['P2'][0]-2), 12)}  Y1-Y2 = {nstr(c['P1'][1]-c['P2'][1],12)}")
    print()
    root = findroot(lambda x: chain(x)["res"], dstar)
    print("findroot on closure residual:", nstr(root, 50))
    print("matches Newton d*:", nstr(root - dstar, 5))
