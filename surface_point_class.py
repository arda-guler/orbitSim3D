# this is used to mark surface features or
# space ports that move with the surface of the
# body they are on

import math

from math_utils import *

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
            tangent_vel_rel_to_body = [-math.sin(math.radians(self.gpos[1])),
                                       0,
                                       -math.cos(math.radians(self.gpos[1]))]
            tangent_vel_rel_to_body = vector_scale(tangent_vel_rel_to_body, tangent_vel_mag)
            tangent_vel_rel_to_body = [tangent_vel_rel_to_body[0] * self.get_body().get_orient()[0][0] + tangent_vel_rel_to_body[2] * self.get_body().get_orient()[2][0],
                                       tangent_vel_rel_to_body[0] * self.get_body().get_orient()[0][1] + tangent_vel_rel_to_body[2] * self.get_body().get_orient()[2][1],
                                       tangent_vel_rel_to_body[0] * self.get_body().get_orient()[0][2] + tangent_vel_rel_to_body[2] * self.get_body().get_orient()[2][2]]
            self.vel = vector_add(tangent_vel_rel_to_body, self.get_body().get_vel())
        else:
            self.vel = self.get_body().get_vel()

        return self.vel

    def get_vel_rel_to(self, obj):
        return vector_add(self.get_vel(), vector_scale(obj.get_vel(), -1))

    def get_vel_mag(self):
        return mag(self.get_vel())

    def get_vel_mag_rel_to(self, obj):
        return mag(self.get_vel_rel_to(obj))

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

        rel_pos = [math.cos(long) * math.cos(lat), # X axis is on 0 longitude
                   math.sin(lat),                  # planet Z axis is the OpenGL Y axis
                   -math.cos(lat) * math.sin(long)]

        rel_pos = vector_scale(rel_pos, R)

        # now take the planet's orientation matrix into account
        rel_pos = [rel_pos[0] * self.get_body().get_orient()[0][0] + rel_pos[1] * self.get_body().get_orient()[1][0] + rel_pos[2] * self.get_body().get_orient()[2][0],
                   rel_pos[0] * self.get_body().get_orient()[0][1] + rel_pos[1] * self.get_body().get_orient()[1][1] + rel_pos[2] * self.get_body().get_orient()[2][1],
                   rel_pos[0] * self.get_body().get_orient()[0][2] + rel_pos[1] * self.get_body().get_orient()[1][2] + rel_pos[2] * self.get_body().get_orient()[2][2]]
        
        return [self.get_body().get_pos()[0] + rel_pos[0],
                self.get_body().get_pos()[1] + rel_pos[1],
                self.get_body().get_pos()[2] + rel_pos[2]]

    def get_pos_rel_to(self, obj):
        return vector_add(self.get_pos(), vector_scale(obj.get_pos(), -1))

    def get_dist_to(self, obj):
        return mag(self.get_pos_rel_to(obj))

    def get_alt_above(self, body):
        return (self.get_dist_to(body) - body.get_radius())

    def get_draw_pos(self):
        return vector_scale(self.get_pos(), visual_scaling_factor)
