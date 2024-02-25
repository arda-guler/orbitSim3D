import numpy as np

from vector3 import *
from math_utils import *

# please see https://github.com/arda-guler/GeneralRelativityOrbit
# for this to make a bit more sense, in case you are confused

class GR_Schwarzschild:
    def __init__(self, name, body, vessel):
        self.name = name
        self.body = body
        self.vessel = vessel

    def get_name(self):
        return self.name

    def compute_Schwarzschild(self):
        beta = 1
        gamma = 1
        c = 299792458 # m s-1

        r = (self.vessel.pos - self.body.pos).mag()
        mu = grav_const * self.body.mass

        # convert to body coords
        body_orient = np.array(self.body.orient.tolist())
        orbiter_pos = np.dot(body_orient, np.array((self.vessel.pos - self.body.pos).tolist()))
        orbiter_vel = np.dot(body_orient, np.array((self.vessel.vel - self.body.vel).tolist()))
        
        accel = mu / (c**2 * r**3) * ((2 * (beta + gamma) * mu / r - gamma * np.dot(orbiter_vel, orbiter_vel)) * orbiter_pos + 2 * (1 + gamma) * np.dot(orbiter_pos, orbiter_vel) * orbiter_vel)

        # reconvert to global coords.
        body_orient_inv = np.linalg.inv(body_orient)
        accel = np.dot(body_orient_inv, accel)

        accel = accel.tolist()
        accel = vec3(lst=accel)

        return accel

class GR_LenseThirring:
    def __init__(self, name, body, vessel, J):
        self.name = name
        self.body = body
        self.vessel = vessel
        self.J = J # not to be confused with the spherical harmonics coefficient J

    def get_name(self):
        return self.name

    def compute_LenseThirring(self):
        c = 299792458 # m s-1
        gamma = 1

        r = (self.vessel.pos - self.body.pos).mag()
        mu = grav_const * self.body.mass

        body_orient = np.array(self.body.orient.tolist())
        orbiter_pos = np.dot(body_orient, np.array((self.vessel.pos - self.body.pos).tolist()))
        orbiter_vel = np.dot(body_orient, np.array((self.vessel.vel - self.body.vel).tolist()))
        J = np.array(self.J)

        accel = (1 + gamma) * mu / (c**2 * r**3)
        accel = accel * (3/r**2 * np.cross(orbiter_pos, orbiter_vel) * np.dot(orbiter_pos, J) + np.cross(orbiter_vel, J))

        # reconvert to global coords.
        body_orient_inv = np.linalg.inv(body_orient)
        accel = np.dot(body_orient_inv, accel)

        accel = accel.tolist()
        accel = vec3(lst=accel)

        return accel
        
