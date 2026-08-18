#!/usr/bin/env python3
"""Deterministic bounded Weyl--Heisenberg SIC fiducial pilot."""

from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize

from evaluate import literal_residuals


def unpack(x: np.ndarray) -> np.ndarray:
    d = x.size // 2
    z = x[:d] + 1j * x[d:]
    return z / np.linalg.norm(z)


def fast_terms(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return overlaps, D_pq v, and labels in p-major order, excluding (0,0)."""
    d = vector.size
    omega = np.exp(2j * np.pi / d)
    tau = -np.exp(1j * np.pi / d)
    rows, labels = [], []
    basis = np.arange(d)
    for p in range(d):
        for q in range(d):
            if p or q:
                rows.append(tau ** (p * q) * np.roll(omega ** (q * basis) * vector, p))
                labels.append((p, q))
    displaced = np.asarray(rows)
    return displaced @ vector.conj(), displaced, np.asarray(labels)


def objective_and_gradient(x: np.ndarray) -> tuple[float, np.ndarray]:
    vector = unpack(x)
    d = vector.size
    overlaps, displaced, labels = fast_terms(vector)
    residuals = abs(overlaps) ** 2 - 1.0 / (d + 1)
    omega = np.exp(2j * np.pi / d)
    tau = -np.exp(1j * np.pi / d)
    basis = np.arange(d)
    # Apply D_pq^dagger = conjugate(tau^pq) Z^-q X^-p directly.  Using modular
    # labels here without the accompanying projective phase gives a wrong gradient.
    adjoint_rows = np.asarray([
        np.conj(tau ** (int(p) * int(q)))
        * omega ** (-int(q) * basis)
        * np.roll(vector, -int(p))
        for p, q in labels
    ])
    complex_gradient = np.sum(
        (2.0 * residuals)[:, None]
        * (overlaps.conj()[:, None] * displaced + overlaps[:, None] * adjoint_rows),
        axis=0,
    )
    # Pull the complex gradient back through z -> z/||z||.
    raw = x[:d] + 1j * x[d:]
    norm = np.linalg.norm(raw)
    tangent = complex_gradient - vector * np.real(np.vdot(vector, complex_gradient))
    gradient = 2.0 * np.concatenate((tangent.real, tangent.imag)) / norm
    return float(np.dot(residuals, residuals)), gradient


def run_start(d: int, seed: int, maxiter: int) -> dict:
    rng = np.random.default_rng(seed)
    x0 = rng.standard_normal(2 * d)
    started = time.monotonic()
    result = minimize(
        objective_and_gradient,
        x0,
        jac=True,
        method="L-BFGS-B",
        options={"maxiter": maxiter, "ftol": 0.0, "gtol": 1e-14, "maxls": 40},
    )
    vector = unpack(result.x)
    fast = abs(fast_terms(vector)[0]) ** 2 - 1.0 / (d + 1)
    literal = literal_residuals(vector)
    return {
        "d": d,
        "seed": seed,
        "seconds": time.monotonic() - started,
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
        "max_abs_residual": float(np.max(np.abs(literal))),
        "rms_residual": float(np.sqrt(np.mean(literal**2))),
        "fast_literal_max_abs_difference": float(np.max(np.abs(fast - literal))),
        "vector_real": vector.real.tolist(),
        "vector_imag": vector.imag.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("calibrate", "target"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maxiter", type=int, default=3000)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    plan = [(4, 4005), (5, 5005)] if args.phase == "calibrate" else [(56, 56000 + i) for i in range(10)]
    overall = time.monotonic()
    records = []
    for index, (d, seed) in enumerate(plan):
        if args.phase == "calibrate" and time.monotonic() - overall >= 300:
            break
        if args.phase == "target" and time.monotonic() - overall >= 2700:
            break
        record = run_start(d, seed, args.maxiter)
        records.append(record)
        checkpoint = {
            "phase": args.phase,
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
            "elapsed_seconds": time.monotonic() - overall,
            "records": records,
        }
        (args.output / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n")
        print(json.dumps({k: v for k, v in record.items() if not k.startswith("vector_")}), flush=True)
        if args.phase == "target" and record["max_abs_residual"] < 1e-8:
            break
    failed_calibration = args.phase == "calibrate" and (
        len(records) != 2 or any(r["max_abs_residual"] >= 1e-12 for r in records)
    )
    raise SystemExit(2 if failed_calibration else 0)


if __name__ == "__main__":
    main()
