"""Read the float n=16 hypothesis and report its contact structure. No exactness claimed."""
import json, math, pathlib, sys

SRC = pathlib.Path(__file__).resolve().parents[1] / "circle-packing-search" / "out" / "n16.json"
data = json.loads(SRC.read_text())
m = data["m_min_pairwise_distance_unit_triangle"]
pts_unit = data["unit_triangle_points"]
n = data["n"]
assert n == 16 and len(pts_unit) == 16

scale = 2.0 / m               # unit triangle -> point formulation (separation 2)
d = scale                     # side of the unit triangle is 1, so side becomes 2/m
S3 = math.sqrt(3.0)
# normalisation assertion (see notebook): s = d + 2*sqrt(3) must match the file's s
assert abs((d + 2 * S3) - data["s_side_for_unit_circles"]) < 1e-9, "normalisation mismatch"

P = [(x * scale, y * scale) for x, y in pts_unit]
print(f"d = {d!r}   s = {d + 2*S3!r}")

# distances
pairs = []
for i in range(n):
    for j in range(i + 1, n):
        dist = math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1])
        pairs.append((dist, i, j))
pairs.sort()
print("\nsmallest 40 pair distances (excess over 2):")
for dist, i, j in pairs[:40]:
    print(f"  {i:2d}-{j:2d}  {dist:.15f}   excess {dist-2:.3e}")

# edge membership: distance to each of the 3 edges
print("\npoint -> (dist to AB y=0, dist to AC, dist to BC), and x+y/sqrt3 (vs d):")
for i, (x, y) in enumerate(P):
    dAB = y
    dAC = abs(S3 * x - y) / 2.0            # line y = sqrt3 x
    dBC = abs(S3 * (d - x) - y) / 2.0
    print(f"  {i:2d}  ({x:.12f},{y:.12f})  AB {dAB:.3e}  AC {dAC:.3e}  BC {dBC:.3e}   x+y/s3-d {x+y/S3-d:.3e}")
