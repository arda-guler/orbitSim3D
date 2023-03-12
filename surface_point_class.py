# this is used to mark surface features or
# spaceports that move with the surface of the
# body they are on

import math

from math_utils import *
from vector3 import *

class surface_point:
    def __init__(self, name, body, color, gpos):
        self.name = name
        self.body = body
        self.color = color

        # ground position;
        # [latitude, longitude, altitude]
        self.gpos = gpos
        
        self.pos = self.get_pos()
        self.vel = self.get_vel()

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body

    def get_color(self):
        return self.color

    def get_gpos(self):
        return self.gpos

    def get_lat(self):
        return self.gpos[0]

    def get_lon(self):
        return self.gpos[1]

    def get_alt(self):
        return self.gpos[2]

    def get_vel(self):
        # velocity can be determined analytically here
        if self.get_body().get_day_length():
            tangent_vel_mag = 2 * math.pi * self.get_body().get_radius() * math.cos(math.radians(self.gpos[0])) / self.get_body().get_day_length()
            tangent_vel_rel_to_body = vec3(lst=[-math.sin(math.radians(self.gpos[1])), 0, -math.cos(math.radians(self.gpos[1]))])
            tangent_vel_rel_to_body = tangent_vel_rel_to_body * tangent_vel_mag
            tangent_vel_rel_to_body = vec3(lst=[tangent_vel_rel_to_body.x * self.get_body().get_orient().m11 + tangent_vel_rel_to_body.z * self.get_body().get_orient().m31,
                                                tangent_vel_rel_to_body.x * self.get_body().get_orient().m12 + tangent_vel_rel_to_body.z * self.get_body().get_orient().m32,
                                                tangent_vel_rel_to_body.x * self.get_body().get_orient().m13 + tangent_vel_rel_to_body.z * self.get_body().get_orient().m33])
            self.vel = tangent_vel_rel_to_body + self.get_body().get_vel()
        else:
            self.vel = self.get_body().get_vel()

        return self.vel

    def get_vel_rel_to(self, obj):
        return self.get_vel() - obj.get_vel()

    def get_vel_mag(self):
        return self.get_vel().mag()

    def get_vel_mag_rel_to(self, obj):
        return self.get_vel_rel_to(obj).mag()

    def update_state_vectors(self, dt):
        self.vel = self.get_vel()
        self.pos = self.get_pos()

    def get_pos(self):
        # OpenGL axes use Y as up-down whereas planet-centered inertial
        # reference frames are easier to use as the Z axis being up-down
        # look at this picture: https://en.wikipedia.org/wiki/Earth-centered_inertial#/media/File:Earth_Centered_Inertial_Coordinate_System.png

        # there comes a painful conversion...
        lat = math.radians(self.get_gpos()[0])
        long = math.radians(self.get_gpos()[1])
        R = self.get_body().get_radius() + self.get_gpos()[2]

        rel_pos = vec3(lst=[math.cos(long) * math.cos(lat), # X axis is on 0 longitude
                            math.sin(lat),                  # planet Z axis is the OpenGL Y axis
                            -math.cos(lat) * math.sin(long)])

        rel_pos = rel_pos * R

        # now take the planet's orientation matrix into account
        rel_pos = vec3(lst=[rel_pos.x * self.get_body().get_orient().m11 + rel_pos.y * self.get_body().get_orient().m21 + rel_pos.z * self.get_body().get_orient().m31,
                            rel_pos.x * self.get_body().get_orient().m12 + rel_pos.y * self.get_body().get_orient().m22 + rel_pos.z * self.get_body().get_orient().m32,
                            rel_pos.x * self.get_body().get_orient().m13 + rel_pos.y * self.get_body().get_orient().m23 + rel_pos.z * self.get_body().get_orient().m33])

        return self.get_body().get_pos() + rel_pos

    def get_pos_rel_to(self, obj):
        return self.get_pos() - obj.get_pos()

    def get_dist_to(self, obj):
        return self.get_pos_rel_to(obj).mag()

    def get_alt_above(self, body):
        return self.get_dist_to(body) - body.get_radius()

    def get_draw_pos(self):
        return self.get_pos() * visual_scaling_factor

    def is_obj_above_horizon(self, obj):
        surface_normal = self.get_pos_rel_to(self.body).normalized()
        obj_dir = obj.get_pos_rel_to(self).normalized()

        if obj_dir.dot(surface_normal) > 0:
            return True
        else:
            return False

    def get_obj_angle_above_horizon(self, obj):
        surface_normal = self.get_pos_rel_to(self.body).normalized()
        obj_dir = obj.get_pos_rel_to(self).normalized()

        return math.degrees(math.pi/2 - math.acos(obj_dir.dot(surface_normal)))
