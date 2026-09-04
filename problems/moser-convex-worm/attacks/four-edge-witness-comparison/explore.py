#!/usr/bin/env python3
"""Clean-room numerical reconnaissance for symmetric four-edge witnesses.

This deliberately uses only the geometric definition: balanced three-edge
subcircuits and residual segment widths.  It is not a certificate checker.
"""

from math import atan, cos, pi, sin, sqrt


def unit(t):
    return ((1 - t*t) / (1 + t*t), 2*t / (1 + t*t))


def tri_floor(theta, load):
    # Align each loaded outward normal in turn with a triangle fan wall.
    # In that frame q_ij=(sin(theta_j-theta_i),-cos(theta_j-theta_i)).
    values = []
    for a in theta:
        total = 0.0
        for b, x in zip(theta, load):
            qx, qy = sin(b-a), -cos(b-a)
            total += x*max(0.0, qx/2, (qx+sqrt(3)*qy)/4)
        values.append(total/2)
    return min(values)


def data(tb, ta, p, q):
    beta, alpha = 2*atan(tb), 2*atan(ta)
    th = [-beta, -alpha, alpha, beta, pi]
    R = 2*(p*cos(beta) + q*cos(alpha))
    # C inner pair, B outer pair, A/D crossed pairs.
    circuits = [("S", 0.0, [0.0]*5)]
    for name, ids, x in (
        ("C", (1, 2, 4), (q, q, 2*q*cos(alpha))),
        ("B", (0, 3, 4), (p, p, 2*p*cos(beta))),
        ("A", (0, 2, 4), (q*sin(alpha)/sin(beta), q,
                            q*sin(alpha)*cos(beta)/sin(beta)+q*cos(alpha))),
        ("D", (1, 3, 4), (q, q*sin(alpha)/sin(beta),
                            q*cos(alpha)+q*sin(alpha)*cos(beta)/sin(beta))),
    ):
        loads = [0.0]*5
        for i, z in zip(ids, x): loads[i] = z
        tau = tri_floor([th[i] for i in ids], x)
        circuits.append((name, tau, loads))
    L = [p, q, q, p, R]
    def bound(c, phi):
        name, tau, x = c
        return tau + sum((a-b)*abs(sin(t-phi)) for a,b,t in zip(L,x,th))/4
    return th, circuits, bound


def inspect(name, args):
    _, cs, bound = data(*args)
    n = 400000
    best = (9.0, 0.0, "")
    changes = []
    prev = None
    for k in range(n+1):
        phi = pi*k/n
        vals = [(bound(c,phi), c[0]) for c in cs]
        top = max(vals)
        if top[1] != prev:
            changes.append((phi, top[1], top[0]))
            prev = top[1]
        if top[0] < best[0]: best = (top[0], phi, top[1])
    print(name, "floor", best, "changes", changes)
    print("at zero", [(c[0], bound(c,0)) for c in cs])


inspect("W191", (313/391, 1/53, 169/495, 157/990))
inspect("W192", (19999/25000, 3/200, 683/2000, 317/2000))
