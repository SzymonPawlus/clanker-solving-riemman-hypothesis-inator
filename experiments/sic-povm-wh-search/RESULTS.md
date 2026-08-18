# Pilot result

Run on Linux 6.12.96-1-MANJARO x86_64 with CPython 3.14.6, NumPy 2.5.2,
and SciPy 1.17.0. The complete per-start vectors and metrics are retained in
the checkpoint JSON files under `results/`.

## Calibration gate

| dimension | seed | max absolute residual | RMS residual | evaluator disagreement |
|---:|---:|---:|---:|---:|
| 4 | 4005 | 2.3037127760972e-15 | 1.4938586094943e-15 | 5.5511151231258e-17 |
| 5 | 5005 | 5.3013149425851e-15 | 2.5556176413097e-15 | 1.9428902930940e-16 |

The gate passed in 0.032 seconds, below both the `1e-12` residual threshold and
the five-minute time limit.

## Dimension 56

Ten pinned starts (`56000` through `56009`) completed in 274.523 seconds. The
maximum-absolute-residual distribution was:

- minimum: 0.031279472560224605
- median: 0.03393800040654063
- mean: 0.0343736529396642
- maximum: 0.03954016712453355

The largest disagreement between the vectorized and literal residual paths in
any target start was 9.020562075079397e-17. No start reached `1e-8`, so the run
stopped at its ten-start kill condition. This bounded numerical failure does
not imply that a dimension-56 SIC fiducial does not exist.
