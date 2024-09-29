import numpy as np

from math_utils import grav_const
from vector3 import *

class spherical_harmonics_model:
    def __init__(self, name, vessel, body, filepath):
        self.name = name
        self.vessel = vessel
        self.body = body
        self.filepath = "data/gravitational_fields/" + filepath

        self.n_max, self.m_max, self.C, self.S = self.readfile()
        self.norm1, self.norm2, self.norm11, self.normn10, self.norm1m, self.norm2m, self.normn1 = self.compute_gottlieb_normalization()

    def get_name(self):
        return self.name

    def get_params_str(self):
        output = "\nVessel: " + self.vessel.get_name() + ", Body: " + self.body.get_name() + "\n"
        output += "Perturbative Accel: " + str(self.gottliebnorm_accel()) + "\n"
        return output

    def readfile(self):
        print("\nReading spherical harmonics file " + self.filepath + "...")
        with open(self.filepath, "r") as f:
            lines = f.readlines()

            # get max n and m
            last_line = lines[-1].strip()
            n_max = int(last_line.split()[0])
            m_max = int(last_line.split()[0])

            # initialize coefficient matrices
            C = [[0 for _ in range(n_max+1)] for _ in range(m_max+1)]
            S = [[0 for _ in range(n_max+1)] for _ in range(m_max+1)]

            # fill the matrices
            for line in lines:
                # print(line)
                l = line.split()
                n = int(l[0])
                m = int(l[1])
                C[n][m] = float(l[2])
                S[n][m] = float(l[3])

        return n_max, m_max, C, S

    # this implementation is from https://ntrs.nasa.gov/citations/20160011252
    # it is a Pythonified version of the MATLAB code
    #
    # Eckman, R. A., Brown, A. J., Adamo, D. R. (2016). "Normalization and
    # Implementation of Three Gravitational Acceleration Models", NASA Technical
    # Report
    #
    # there are some coordinate system conversions between OpenGL coords and ICRF-like
    # coords. though
    def compute_gottlieb_normalization(self):
        print("Pre-computing normalization parameters...")
        print("Depending on model complexity, this might take a while.")
        nax = self.n_max
        
        norm1 = np.zeros(nax + 2)
        norm2 = np.zeros(nax + 2)
        norm11 = np.zeros(nax + 2)
        normn10 = np.zeros(nax + 2)
        norm1m = np.zeros((nax + 2, nax + 2))
        norm2m = np.zeros((nax + 2, nax + 2))
        normn1 = np.zeros((nax + 2, nax + 2))

        # Pre-computing norm values
        for n in range(2, nax + 2):
            norm1[n] = np.sqrt((2 * n + 1) / (2 * n - 1))
            norm2[n] = np.sqrt((2 * n + 1) / (2 * n - 3))
            norm11[n] = np.sqrt((2 * n + 1) / (2 * n)) / (2 * n - 1)
            normn10[n] = np.sqrt((n + 1) * n / 2)
            for m in range(1, n + 1):
                norm1m[n, m] = np.sqrt((n - m) * (2 * n + 1) / ((n + m) * (2 * n - 1)))
                norm2m[n, m] = np.sqrt((n - m) * (n - m - 1) * (2 * n + 1) / ((n + m) * (n + m - 1) * (2 * n - 3)))
                normn1[n, m] = np.sqrt((n + m + 1) * (n - m))

        return norm1, norm2, norm11, normn10, norm1m, norm2m, normn1

    def gottliebnorm_accel(self):
        sat_pos = self.vessel.pos - self.body.pos
        
        mu = grav_const * self.body.mass
        re = self.body.radius
        xin = np.array(sat_pos.tolist())
        c = self.C
        s = self.S
        n_max = self.n_max
        m_max = self.m_max

        orient_vx = self.body.orient.vz().tolist() # convert OpenGL coords into regular coords
        orient_vy = self.body.orient.vx().tolist()
        orient_vz = self.body.orient.vy().tolist()
        rnp = np.array([orient_vx, orient_vy, orient_vz])
        
        norm1 = np.zeros(n_max + 2)
        norm2 = np.zeros(n_max + 2)
        norm11 = np.zeros(n_max + 2)
        normn10 = np.zeros(n_max + 2)
        norm1m = np.zeros((n_max + 2, n_max + 2))
        norm2m = np.zeros((n_max + 2, n_max + 2))
        normn1 = np.zeros((n_max + 2, n_max + 2))
        p = np.zeros((n_max + 2, n_max + 3))
        ctil = np.zeros(n_max + 2)
        stil = np.zeros(n_max + 2)

        x = rnp @ xin
        r = np.linalg.norm(x)
        ri = 1 / r
        xor, yor, zor = x * ri
        ep = zor
        reor = re * ri
        reorn = reor
        muor2 = mu * ri * ri

        # Initialize p matrix and ctil/stil arrays
        p[1, 1] = 1
        p[1, 2] = p[1, 3] = p[2, 3] = p[2, 4] = 0
        p[2, 2] = np.sqrt(3)

        for n in range(2, n_max):
            ni = n + 1
            p[ni, ni] = norm11[n] * p[n, n] * (2 * n - 1)

        ctil[1], stil[1] = 1, 0
        ctil[2], stil[2] = xor, yor

        sumh, sumgm, sumj, sumk = 0, 1, 0, 0
        p[2, 1] = np.sqrt(3) * ep

        for n in range(2, n_max):
            ni = n + 1
            reorn *= reor
            n2m1 = 2 * n - 1
            nm1 = n - 1
            np1 = n + 1

            p[ni, n] = normn1[n, nm1] * ep * p[ni, ni]
            p[ni, 1] = (n2m1 * ep * norm1[n] * p[n, 1] - nm1 * norm2[n] * p[nm1, 1]) / n
            p[ni, 2] = (n2m1 * ep * norm1m[n, 1] * p[n, 2] - n * norm2m[n, 1] * p[nm1, 2]) / nm1

            sumhn = normn10[n] * p[ni, 2] * c[ni][1]
            sumgmn = p[ni, 1] * c[ni][1] * np1

            if m_max > 0:
                for m in range(2, n - 1):
                    mi = m + 1
                    p[ni, mi] = (n2m1 * ep * norm1m[n, m] * p[n, mi] - (nm1 + m) * norm2m[n, m] * p[nm1, mi]) / (n - m)

                sumjn, sumkn = 0, 0
                ctil[ni] = ctil[2] * ctil[ni - 1] - stil[2] * stil[ni - 1]
                stil[ni] = stil[2] * ctil[ni - 1] + ctil[2] * stil[ni - 1]

                lim = min(n, m_max)

                for m in range(1, lim + 1):
                    mi = m + 1
                    mm1 = mi - 1
                    mp1 = mi + 1
                    mxpnm = m * p[ni, mi]
                    bnmtil = c[ni][mi] * ctil[mi] + s[ni][mi] * stil[mi]
                    sumhn += normn1[n, m] * p[ni, mp1] * bnmtil
                    sumgmn += (n + m + 1) * p[ni, mi] * bnmtil

                    bnmtm1 = c[ni][mi] * ctil[mm1] + s[ni][mi] * stil[mm1]
                    anmtm1 = c[ni][mi] * stil[mm1] - s[ni][mi] * ctil[mm1]
                    sumjn += mxpnm * bnmtm1
                    sumkn -= mxpnm * anmtm1

                sumj += reorn * sumjn
                sumk += reorn * sumkn

            sumh += reorn * sumhn
            sumgm += reorn * sumgmn

        lambda_val = sumgm + ep * sumh
        g = np.zeros((3, 1))
        g[0, 0] = -muor2 * (lambda_val * xor - sumj)
        g[1, 0] = -muor2 * (lambda_val * yor - sumk)
        g[2, 0] = -muor2 * (lambda_val * zor - sumh)

        accel = np.matmul(rnp.T, g)

        # addendum: remove effect of point-mass gravity (only get perturbative acceleration)
        point_grav_accel = (self.body.pos - sat_pos).normalized() * grav_const * self.body.mass / (self.body.pos - sat_pos).mag()**2

        return vec3(accel[0], accel[1], accel[2]) - point_grav_accel
