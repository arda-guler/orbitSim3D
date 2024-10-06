import math

from vector3 import *
from math_utils import *

# calculations for how much of the surface of a body is visible to a vessel
class surface_coverage:
    def __init__(self, name, vessel, body):
        self.name = name
        self.vessel = vessel
        self.body = body

        self.b = None
        self.h = None

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body

    def get_vessel(self):
        return self.vessel

    def get_body_surface_coverage(self):
        r = self.vessel.get_pos_rel_to(self.body)
        r_mag = r.mag()
        R_b = self.body.get_radius()

        if r_mag <= R_b:
            return None, None
        
        d_tangent = (r_mag**2 - R_b**2)**0.5
        alpha = math.atan(R_b / r_mag) # coverage cone half-angle

        h = d_tangent * math.sin(alpha)
        b = r_mag - (R_b**2 - h**2)**0.5

        # return distance of coverage circle from vessel and the radius of the coverage circle
        return b, h 

    def update(self):
        self.b, self.h = self.get_body_surface_coverage()

    def generate_plot_points(self):
        self.b, self.h = self.get_body_surface_coverage()

        if self.b == None:
            return [], []

        center = self.vessel.pos + self.vessel.get_unit_vector_towards(self.body) * self.b

        if abs((self.vessel.pos - self.body.pos).normalized().dot(vec3(0, 1, 0))) < 1:
            plane_maker = vec3(0, 1, 0)
        else:
            plane_maker = vec3(1, 0, 0)

        axis = (self.vessel.pos - self.body.pos).normalized()
        h_vec0 = axis.cross(plane_maker)

        lats = []
        lons = []
        poly = 256 # number of sample points
        for i in range(poly):
            theta = i / poly * 2 * math.pi
            h_vec = h_vec0.rotate(axis, theta)
            point_pos = center + h_vec * self.h

            # get body centered coords
            x_diff = point_pos.x - self.body.pos.x
            y_diff = point_pos.y - self.body.pos.y
            z_diff = point_pos.z - self.body.pos.z
            point_bcc = vec3(lst=[(x_diff * self.body.orient.m11) + (y_diff * self.body.orient.m12) + (z_diff * self.body.orient.m13),
                                  (x_diff * self.body.orient.m21) + (y_diff * self.body.orient.m22) + (z_diff * self.body.orient.m23),
                                  (x_diff * self.body.orient.m31) + (y_diff * self.body.orient.m32) + (z_diff * self.body.orient.m33)])
        
            point_gpos = impact_gpos(point_bcc)
            lats.append(point_gpos[0])
            lons.append(point_gpos[1])

        return lats, lons
