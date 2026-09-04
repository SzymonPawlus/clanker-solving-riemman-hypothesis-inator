"""Independent re-derivation of the chord profile of T(a) for a family of parallel lines.

Written from the problem statement (problems/circle-packing-equilateral-triangle/RULES.md §2),
NOT by reading experiments/packing-r5-eo7/geometry.py.  The two are compared in
`crosscheck.py`; agreement is a check, not an input.

Conventions.  T(a) is the CLOSED equilateral triangle A=(0,0), B=(a,0), C=(a/2, a*sqrt3/2).
Points are 1-separated (Oler normalisation).  Erdos-Oler at k=7 is the open statement that
27 points at pairwise distance >= 1 force a >= 6.

Derivation (mine).  Take line direction u = (cos p, sin p), normal n = (-sin p, cos p).
  <A,n> = 0,  <B,n> = -a sin p,  <C,n> = a cos(p + pi/6).
For p in [0, pi/3] the order is B < A < C, so put s = <x,n> + a sin p, giving
  s_B = 0,  s_A = d1 = a sin p,  s_C = w = a cos(p - pi/6).
The chord length ell(s) is a "tent": 0 at s=0, peak Lstar at s=d1, 0 at s=w.  Its integral is
the area sqrt3 a^2 / 4 = Lstar*w/2, hence
  Lstar = sqrt3 a / (2 cos(p - pi/6)).
STATUS: numerical / sketch.  Nothing here is assumable.
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _deps

_deps.require('geom2.py')   # fail fast, before the numpy import below

import numpy as np

SQRT3 = np.sqrt(3.0)
PI6 = np.pi / 6.0


def profile(p, a):
    """(d1, w, Lstar) for line direction angle p in [0, pi/3]."""
    d1 = a * np.sin(p)
    w = a * np.cos(p - PI6)
    Lstar = SQRT3 * a / (2.0 * np.cos(p - PI6))
    return d1, w, Lstar


def chord(p, a, s):
    """Chord length of T(a) at level s (array ok).  0 outside [0, w]."""
    d1, w, Lstar = profile(p, a)
    s = np.asarray(s, dtype=float)
    out = np.zeros_like(s)
    if d1 > 0:
        rise = (s >= 0.0) & (s <= d1)
        out = np.where(rise, Lstar * np.divide(s, d1, out=np.zeros_like(s), where=(d1 > 0)), out)
    else:
        out = np.where(s == 0.0, Lstar, out)
    fall = (s > d1) & (s <= w)
    den = w - d1
    if den > 0:
        out = np.where(fall, Lstar * (w - s) / den, out)
    else:                      # p = pi/3: the tent degenerates to a single peak at s = w
        out = np.where(s == w, Lstar, out)
    return out


def chord_sup(p, a, lo, hi):
    """sup of the chord over the level interval [lo, hi], clipped to [0, w]."""
    d1, w, Lstar = profile(p, a)
    lo = np.maximum(np.asarray(lo, dtype=float), 0.0)
    hi = np.minimum(np.asarray(hi, dtype=float), w)
    empty = hi < lo
    v = np.maximum(chord(p, a, np.where(empty, 0.0, lo)), chord(p, a, np.where(empty, 0.0, hi)))
    v = np.where((lo <= d1) & (d1 <= hi), Lstar, v)
    return np.where(empty, -1.0, v)


def in_triangle(xy, a, tol=0.0):
    """Boolean mask: rows of xy inside the closed T(a) (tol >= 0 dilates)."""
    x, y = xy[..., 0], xy[..., 1]
    return (y >= -tol) & (SQRT3 * x - y >= -tol * 2.0) & (SQRT3 * (a - x) - y >= -tol * 2.0)
