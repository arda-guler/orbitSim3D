from math_utils import *
from vector3 import *
import math
import time

class kepler_projection():
    def __init__(self, name, vessel, body, proj_time):
        self.name = name
        self.vessel = vessel
        self.body = body

        self.proj_time = proj_time

        # state vectors
        self.pos0 = vessel.get_pos_rel_to(body)
        self.vel0 = vessel.get_vel_rel_to(body)

        # mu = standard gravitational parameter
        self.mu = body.get_mass() * grav_const
        
        self.vertices, self.draw_vertices, self.draw_ap, self.draw_pe, self.draw_an, self.draw_dn, self.inclination = self.generate_projection()

        self.body_draw_pos_prev = self.body.get_draw_pos()

        self.angular_momentum = self.pos0.cross(self.vel0)

        self.eccentricity = self.get_eccentricity()
        self.energy = self.get_energy()
        self.semimajor_axis = self.get_semimajor_axis()

        self.periapsis = self.get_periapsis()
        self.apoapsis = self.get_apoapsis()

        self.period = self.get_period()

        if type(self.period) == complex:
            self.apoapsis = float("inf")
            self.period = float("inf")

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body

    def get_vessel(self):
        return self.vessel

    def get_eccentricity_vector(self):
        return self.e_vec

    def get_eccentricity(self):
        return self.e

    def get_energy(self):
        return (self.vel0.mag()**2)/2 - self.mu/self.pos0.mag()
    
    def get_semimajor_axis(self):
        return self.sma

    def get_periapsis(self):
        #if not self.semimajor_axis == float("inf"):
        #    p = self.semimajor_axis * (1 - (self.eccentricity**2))
        #else:
        #    p = self.angular_momentum.mag()**2/self.mu
        #
        #return p
        return self.periapsis

    def get_periapsis_alt(self):
        return self.periapsis_alt

    def get_apoapsis(self):
        return self.apoapsis

    def get_apoapsis_alt(self):
        return self.apoapsis_alt

    def get_period(self):
        if not self.sma == float("inf"):
            return 2*3.141*((self.sma**3)/self.mu)**0.5
        else:
            return float("inf")

    def get_inclination(self):
        return self.inclination

    def generate_projection(self):
        r_vec = self.vessel.pos - self.body.pos
        v_vec = self.vessel.vel - self.body.vel
        r = r_vec.mag()
        v = v_vec.mag()
        mu = self.mu

        # = = = DETERMINE KEPLER ELEMENTS = = =
        # sma: semi-major axis
        # e: eccentricity
        # argper: argument of periapsis
        # inc: inclination
        # lonasc: longitude/right ascension of ascending node

        v_r = v_vec.dot(r_vec / r)
        v_t = (v**2 - v_r**2)**0.5

        sma = 1/(2/r - v**2/mu)
        self.sma = sma

        h_vec = r_vec.cross(v_vec)
        h = h_vec.mag()

        inc = math.acos(h_vec.z / h)

        K = vec3(0, 0, 1)
        N_vec = K.cross(h_vec)
        N = N_vec.mag()

        if not N:
            if (r_vec.y > 0 and v_vec.x > 0) or (r_vec.y < 0 and v_vec.x < 0):
                lon_asc = math.pi * 1.5
            else:
                lon_asc = math.pi * 0.5

        else:
            lon_asc = math.acos(N_vec.x / N)
            if N_vec.y < 0:
                lon_asc = 2 * math.pi - lon_asc

        e_vec = v_vec.cross(h_vec) / mu - r_vec / r
        e = e_vec.mag()
        self.e = e

        if (N * e):
            arg_peri = math.acos(N_vec.dot(e_vec) / (N * e))
            if e_vec.z < 0:
                arg_peri = 2 * math.pi - arg_peri
        else:
            arg_peri = math.pi * 0.5

        # all orbital elements determined, now visualise it
        resolution = 1000

        vertices = []
        draw_vertices = []
        max_ap = None
        min_pe = None
        prev_y = -1
        draw_ap, draw_pe, draw_an, draw_dn = vec3(), vec3(), vec3(), vec3()

        for i_nu in range(0, int(2 * math.pi * resolution * 1.1)):
            nu = i_nu / resolution

            vis_r = vec3(math.cos(nu), math.sin(nu), 0) * h**2 / mu / (1 + e * math.cos(nu))
            vis_r_mag = vis_r.mag()

            R1 = matrix3x3(math.cos(-arg_peri), -math.sin(-arg_peri), 0,
                           math.sin(-arg_peri), math.cos(-arg_peri), 0,
                           0, 0, 1)

            R2 = matrix3x3(1, 0, 0,
                           0, math.cos(-inc), -math.sin(-inc),
                           0, math.sin(-inc), math.cos(-inc))

            R3 = matrix3x3(math.cos(-lon_asc), -math.sin(-lon_asc), 0,
                           math.sin(-lon_asc), math.cos(-lon_asc), 0,
                           0, 0, 1)

            rmx = R1 * R2 * R3

            r_trans = vec3(vis_r.x * rmx.m11 + vis_r.y * rmx.m21 + vis_r.z * rmx.m31,
                           vis_r.x * rmx.m12 + vis_r.y * rmx.m22 + vis_r.z * rmx.m32,
                           vis_r.x * rmx.m13 + vis_r.y * rmx.m23 + vis_r.z * rmx.m33)

            cpos = r_trans
            vertices.append(cpos)
            draw_vertices.append(cpos * visual_scaling_factor)

            if not max_ap or vis_r_mag > max_ap:
                draw_ap = cpos * visual_scaling_factor
                max_ap = vis_r_mag

            if not min_pe or vis_r_mag < min_pe:
                draw_pe = cpos * visual_scaling_factor
                min_pe = vis_r_mag

            if prev_y * r_trans.y < 0:
                if r_trans.y < 0:
                    draw_an = cpos * visual_scaling_factor
                else:
                    draw_dn = cpos * visual_scaling_factor

            prev_y = r_trans.y

        # compute additional parameters
        self.apoapsis = sma * (1 + (e**2))
        self.apoapsis_alt = self.apoapsis - self.body.get_radius()
        self.periapsis = self.sma * (1 - (e**2))
        self.periapsis_alt = self.periapsis - self.body.get_radius()

        # correct coordinate sys.
        self.inc = math.acos(h_vec.y / h)

        return vertices, draw_vertices, draw_ap, draw_pe, draw_an, draw_dn, math.degrees(self.inc)

    def get_draw_vertices(self):
        return self.draw_vertices

    def get_params_str(self):
        output = "Kepler orbit projection of " + self.get_vessel().get_name() + " around " + self.get_body().get_name() + " at t = " + str(self.proj_time) + "\n"
        output += "Apoapsis_R: " + str(self.get_apoapsis()) + "   Apoapsis_Alt: " + str(self.get_apoapsis_alt()) + "\n"
        output += "Periapsis_R: " + str(self.get_periapsis()) + "   Periapsis_Alt: " + str(self.get_periapsis_alt()) + "\n"
        output += "Orbital Period: " + str(self.get_period()) + "\n"
        output += "Semi-major Axis: " + str(self.get_semimajor_axis()) + "   Eccentricity: " + str(self.eccentricity) + "\n"
        output += "Inclination: " + str(self.get_inclination()) + "\n"

        return output
