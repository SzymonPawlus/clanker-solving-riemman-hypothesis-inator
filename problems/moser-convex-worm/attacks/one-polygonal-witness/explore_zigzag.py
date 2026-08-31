"""Deterministic coarse search. Numerical hypotheses only; not a certificate."""
import math
import random
import numpy as np

SEG = np.array([[0., 0.], [1., 0.]])
TRI = np.array([[0., 0.], [.5, 0.], [.25, math.sqrt(3) / 4]])
SQUARE = np.array([[0., 0.], [1/3, 0.], [1/3, 1/3], [0., 1/3]])
ZIGZAG = np.array([[0., 0.], [1/4, 0.], [2/5, 1/5],
                   [1/5, 7/20], [-1/20, 7/20]])

def published_control_seed():
    """Convert the paper's rounded center/angle tuple to this script's gauge."""
    x1,y1,alpha,x2,y2,beta = .6605,.1878,1.3077,.741,.1274,1.6373
    square_theta = alpha + 3*math.pi/4
    square_shift = np.array([x1,y1])-place(SQUARE.mean(axis=0)[None,:],0,0,square_theta)[0]
    triangle_theta = (beta-7*math.pi/6) % (2*math.pi)
    triangle_shift = np.array([x2,y2])-place(TRI.mean(axis=0)[None,:],0,0,triangle_theta)[0]
    return np.array([*triangle_shift,triangle_theta,*square_shift,square_theta])

def place(points, tx, ty, theta):
    c, s = math.cos(theta), math.sin(theta)
    return points @ np.array([[c, s], [-s, c]]) + np.array([tx, ty])

def hull_area(clouds):
    pts = sorted(map(tuple, np.vstack(clouds)))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    h = lo[:-1] + hi[:-1]
    return abs(sum(h[i][0]*h[(i+1)%len(h)][1]-h[(i+1)%len(h)][0]*h[i][1]
                   for i in range(len(h))))/2

def objective(v, extra):
    clouds = [SEG, place(TRI, *v[:3]), place(SQUARE, *v[3:6])]
    if extra: clouds.append(place(ZIGZAG, *v[6:9]))
    return hull_area(clouds)

def run(extra, seed, generations=400, population=80, use_control=True):
    random.seed(seed)
    count = 3 if extra else 2
    bounds = [(-.5, 1.5), (-1., 1.), (0., 2*math.pi)]*count
    clip = lambda v: np.array([min(max(x,a),b) for x,(a,b) in zip(v,bounds)])
    pop = [np.array([random.uniform(a,b) for a,b in bounds])
           for _ in range(population)]
    if use_control:
        control = published_control_seed()
        if extra:
            # Start the new worm centered near the control hull; this is only a seed.
            control = np.r_[control, [.5,-.05,0.]]
        pop[0] = clip(control)
        for i in range(1, min(20, population)):
            rng = np.random.default_rng(seed*1000+i)
            pop[i] = clip(control+rng.normal(0,.05,3*count))
    vals = [objective(x, extra) for x in pop]
    for gen in range(generations):
        sigma = .35*(1-gen/generations)+.003
        for i in range(population):
            a,b,c = random.sample(range(population), 3)
            rng = np.random.default_rng(seed*100000+gen*population+i)
            trial = clip(pop[a]+.7*(pop[b]-pop[c])+rng.normal(0,sigma,3*count))
            value = objective(trial, extra)
            if value < vals[i]: pop[i], vals[i] = trial, value
    j = min(range(population), key=vals.__getitem__)
    # Piecewise-smooth local random descent around the best basin.
    best, best_value = pop[j].copy(), vals[j]
    rng = np.random.default_rng(900000+seed+100*int(extra))
    for k in range(30000):
        phase = k % 5000
        sigma = .03*(1-phase/5000)+1e-6
        trial = clip(best+rng.normal(0,sigma,3*count))
        value = objective(trial, extra)
        if value < best_value: best, best_value = trial, value
    pop[j], vals[j] = best, best_value
    return {"zigzag": extra, "seed": seed, "area": float(vals[j]),
            "pose": pop[j].tolist()}

if __name__ == "__main__":
    for extra in (False, True):
        for seed in range(3): print(run(extra, seed))
