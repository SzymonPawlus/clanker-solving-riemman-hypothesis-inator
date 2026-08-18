"""Independent, deliberately literal WH SIC residual evaluator."""

from __future__ import annotations

import numpy as np


def literal_residuals(vector: np.ndarray) -> np.ndarray:
    """Return |<v,D_pq v>|^2-1/(d+1), building every D_pq explicitly."""
    vector = np.asarray(vector, dtype=np.complex128)
    vector = vector / np.linalg.norm(vector)
    d = vector.size
    omega = np.exp(2j * np.pi / d)
    tau = -np.exp(1j * np.pi / d)
    answer: list[float] = []
    for p in range(d):
        for q in range(d):
            if p == 0 and q == 0:
                continue
            displacement = np.zeros((d, d), dtype=np.complex128)
            for a in range(d):
                displacement[(a + p) % d, a] = tau ** (p * q) * omega ** (q * a)
            overlap = np.vdot(vector, displacement @ vector)
            answer.append(float(abs(overlap) ** 2 - 1.0 / (d + 1)))
    return np.asarray(answer)
