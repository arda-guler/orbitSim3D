import numpy as np
PI = np.pi

# I dislike typing 'np.' every time
def mag(x):
    return np.linalg.norm(x)

def dot(x, y):
    return np.dot(x, y)

def sqrt(x):
    return np.sqrt(x)

def cos(x):
    return np.cos(x)

def sin(x):
    return np.sin(x)

def C2(ksi):
    return (1 - cos(sqrt(ksi))) / ksi

def C3(ksi):
    return (sqrt(ksi) - sin(sqrt(ksi))) / (ksi * sqrt(ksi))

# https://www.researchgate.net/publication/236012521_Lambert_Universal_Variable_Algorithm
def lambert(r0, r, delta_t, ksi_0, ksi_u, ksi_l, t_m, M, tol, mu):
    r0_mag = mag(r0)
    r_mag = mag(r)

    gamma = dot(r0, r) / (r_mag * r0_mag)
    # beta = t_m * sqrt(1 - gamma**2) unused. so why in the world is this thing in the algorithm in the paper?
    A = t_m * sqrt(r_mag * r0_mag * (1 + gamma))

    if (A == 0): # bad case, no solution
        return None, None

    for i in range(1, M):
        ksi = ksi_0

        c2 = C2(ksi)
        c3 = C3(ksi)

        # there is a fix here. the paper uses c2 twice,
        # but c3 goes unused. trial and error shows this version
        # used below is correct
        B = r0_mag + r_mag + 1/sqrt(c2) * (A * (ksi * c3 - 1))

        if A > 0 and B < 0:
            ksi_l += PI
            print("B =", B, "< 0")
            continue

        X = sqrt(B / c2)
        delta_tt = 1 / sqrt(mu) * (X**3 * c3 + A * sqrt(B))

        if abs(delta_t - delta_tt) < tol:
            print(abs(delta_t - delta_tt))
            break

        if delta_tt <= delta_t:
            ksi_l = ksi
        else:
            ksi_u = ksi
            
        ksi_l = 0.5 * (ksi_u + ksi_l)
        ksi_0 = ksi_l

    F = 1 - B / r0_mag
    G = A * sqrt(B / mu)
    Gdot = 1 - B / r_mag

    Ginv = 1/G

    v0 = np.array([Ginv * (r[0] - r0[0] * F),
                   Ginv * (r[1] - r0[1] * F),
                   Ginv * (r[2] - r0[2] * F)])

    v1 = np.array([Ginv * (Gdot * r[0] - r0[0]),
                   Ginv * (Gdot * r[1] - r0[1]),
                   Ginv * (Gdot * r[2] - r0[2])])

    return v0, v1

        
    
