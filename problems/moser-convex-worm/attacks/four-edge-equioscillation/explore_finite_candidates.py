#!/usr/bin/env python3
"""Numerically evaluate the finite analytic candidate set from the README.

This is a conjecture locator only.  It samples no worm orientation: all tested
orientations are projection walls or pairwise equioscillation roots.
"""
import itertools
import math
import random


ROOT3 = math.sqrt(3.0)
TRIANGLE = ((0.0, 0.0), (0.5, 0.0), (0.25, ROOT3 / 4))


def support_triangle(n):
    return max(x * n[0] + y * n[1] for x, y in TRIANGLE)


def circuit_allocations(angles, loads):
    vectors = [(math.cos(a), math.sin(a)) for a in angles]
    answer = []
    for inds in itertools.combinations(range(len(angles)), 3):
        us = [vectors[i] for i in inds]
        raw = [us[(j + 1) % 3][0] * us[(j + 2) % 3][1]
               - us[(j + 1) % 3][1] * us[(j + 2) % 3][0]
               for j in range(3)]
        if not (all(x > 1e-11 for x in raw)
                or all(x < -1e-11 for x in raw)):
            continue
        raw = list(map(abs, raw))
        scale = min(loads[i] / x for i, x in zip(inds, raw))
        allocation = [0.0] * len(angles)
        for i, x in zip(inds, raw):
            allocation[i] = scale * x
        answer.append(tuple(allocation))
    return answer


def triangle_floor(angles, allocation):
    normals = [(math.sin(a), -math.cos(a)) for a in angles]
    candidates = []
    for i, amount in enumerate(allocation):
        if amount <= 1e-14:
            continue
        ni = normals[i]
        # Align triangle-frame (0,-1) with ni.
        cp, sp = -ni[1], ni[0]
        value = 0.0
        for x, n in zip(allocation, normals):
            frame = (cp * n[0] + sp * n[1],
                     -sp * n[0] + cp * n[1])
            value += x * support_triangle(frame) / 2
        candidates.append(value)
    return min(candidates)


def bounds(angles, loads):
    zero = tuple(0.0 for _ in loads)
    answer = [(zero, 0.0)]
    for allocation in circuit_allocations(angles, loads):
        answer.append((allocation, triangle_floor(angles, allocation)))
    return answer


def value_at(phi, angles, loads, menu):
    projections = [abs(math.sin(a - phi)) for a in angles]
    return max(tau + sum((cap - x) * p for cap, x, p
                         in zip(loads, allocation, projections)) / 4
               for allocation, tau in menu)


def coefficients(midpoint, angles, loads, menu):
    answer = []
    for allocation, tau in menu:
        aa = bb = 0.0
        for angle, cap, used in zip(angles, loads, allocation):
            residual = cap - used
            sign = 1.0 if math.sin(angle - midpoint) > 0 else -1.0
            # sign*sin(angle-phi) = sign*(sin(angle)cos(phi)
            #                                  -cos(angle)sin(phi)).
            aa -= sign * residual * math.cos(angle) / 4
            bb += sign * residual * math.sin(angle) / 4
        answer.append((tau, aa, bb))
    return answer


def analytic_floor(angles, loads):
    menu = bounds(angles, loads)
    walls = sorted({0.0, math.pi}
                   | {a % math.pi for a in angles if 1e-14 < a % math.pi < math.pi-1e-14})
    candidates = set(walls)
    for lo, hi in zip(walls, walls[1:]):
        coeffs = coefficients((lo + hi) / 2, angles, loads, menu)
        for left, right in itertools.combinations(coeffs, 2):
            dc, da, db = (left[k] - right[k] for k in range(3))
            # (dc-db)u^2+2da*u+(db+dc)=0, u=tan(phi/2).
            qa, qb, qc = dc - db, 2 * da, db + dc
            roots = []
            if abs(qa) < 1e-13:
                if abs(qb) > 1e-13:
                    roots.append(-qc / qb)
            else:
                discriminant = qb * qb - 4 * qa * qc
                if discriminant >= 0:
                    root = math.sqrt(discriminant)
                    roots.extend(((-qb - root) / (2 * qa),
                                  (-qb + root) / (2 * qa)))
            for u in roots:
                if u >= 0:
                    phi = 2 * math.atan(u)
                    if lo - 1e-10 <= phi <= hi + 1e-10:
                        candidates.add(phi)
    ranked = sorted((value_at(phi, angles, loads, menu), phi)
                    for phi in candidates)
    return ranked[0], ranked, menu


def closed_surface(traversed_angles, traversed_loads):
    rx = sum(l * math.cos(a) for l, a in zip(traversed_loads, traversed_angles))
    ry = sum(l * math.sin(a) for l, a in zip(traversed_loads, traversed_angles))
    closing = math.hypot(rx, ry)
    return (tuple(traversed_angles) + (math.atan2(-ry, -rx),),
            tuple(traversed_loads) + (closing,))


def perturb(seed=185, trials=20_000):
    rng = random.Random(seed)
    beta, alpha = 2 * math.atan(4/5), 2 * math.atan(1/72)
    p, q = 163/480, 77/480
    base_angles = (-beta, -alpha, alpha, beta)
    base_loads = (p, q, q, p)
    angles, loads = closed_surface(base_angles, base_loads)
    best = (analytic_floor(angles, loads)[0][0], base_angles, base_loads)
    current = best
    print("symmetric", best, flush=True)
    for stage in range(7):
        angular = 0.025 * 0.48 ** stage
        length = 0.012 * 0.48 ** stage
        for _ in range(trials // 7):
            old_value, old_angles, old_loads = current
            trial_angles = sorted(a + rng.gauss(0, angular) for a in old_angles)
            trial_loads = [max(1e-5, l + rng.gauss(0, length)) for l in old_loads]
            total = sum(trial_loads)
            trial_loads = [x / total for x in trial_loads]
            full_angles, full_loads = closed_surface(trial_angles, trial_loads)
            # Retain a strict five-edge hull order with closing last after
            # unwrapping; this numerical filter is not a proof predicate.
            closing = full_angles[-1]
            while closing < trial_angles[-1]:
                closing += 2 * math.pi
            if closing >= trial_angles[0] + 2 * math.pi:
                continue
            value = analytic_floor(full_angles, full_loads)[0][0]
            if value > old_value:
                current = (value, tuple(trial_angles), tuple(trial_loads))
            if value > best[0]:
                best = (value, tuple(trial_angles), tuple(trial_loads))
                print("best", stage, best, flush=True)
        print("stage", stage, current[0], flush=True)
    return best


if __name__ == "__main__":
    print("FINAL", perturb())
