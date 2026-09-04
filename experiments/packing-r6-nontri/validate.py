"""Validation ladder: reproduce KNOWN maximin values before trusting anything else."""
import _deps; _deps.require()   # numpy/scipy are REAL deps here (see pyproject.toml)
import json, time, numpy as np, shapes

SQ3 = np.sqrt(3.0); SQ2 = np.sqrt(2.0); SQ6 = np.sqrt(6.0); SQ33 = np.sqrt(33.0)

# delta = 1/a(m): equilateral triangle of side 1, from the problem README `cited` table
TRI = {2:1.0, 3:1.0, 4:1/SQ3, 5:0.5, 6:0.5, 7:1/(1+SQ3), 8:1/(1+SQ33/3),
       9:1/3, 10:1/3, 11:1/(2+2*SQ6/3), 12:1/(2+SQ3)}
# unit disc (radius 1): classical spreading-points values
DISC = {2:2.0, 3:SQ3, 4:SQ2, 5:2*np.sin(np.pi/5), 6:1.0, 7:1.0,
        8:2*np.sin(np.pi/7), 9:2*np.sin(np.pi/8)}
# unit square: classical (Goldberg / Schaer) values
SQUARE = {2:SQ2, 3:SQ6-SQ2, 4:1.0, 5:SQ2/2, 6:np.sqrt(13)/6, 7:2*(2-SQ3),
          8:(SQ6-SQ2)/2, 9:0.5}

if __name__ == '__main__':
    S = shapes.make_shapes()
    rows = []
    t0 = time.time()
    for key, ref in (('triangle', TRI), ('disc', DISC), ('square', SQUARE)):
        for m, want in sorted(ref.items()):
            got, P = shapes.maximin(S[key], m, restarts=40, seed=1234 + m)
            rows.append(dict(shape=key, m=m, known=want, found=got, err=got - want))
            print(f"{key:9s} m={m:2d} known={want:.6f} found={got:.6f} err={got-want:+.2e}")
    print("elapsed", time.time() - t0)
    json.dump(rows, open('out/validate.json', 'w'), indent=1)
