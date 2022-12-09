from math_utils import *
from vector3 import *
from matrix3x3 import *

class barycenter:
    def __init__(self, name, bodies):
        self.name = name
        self.bodies = bodies
        self.pos = self.get_pos()
        self.vel = self.get_vel()

        # this is required so that orbit projections work
        self.orient = matrix3x3()

        self.color = self.calc_color()

    def get_name(self):
        return self.name

    def get_bodies(self):
        return self.bodies

    def get_color(self):
        return self.color

    def calc_color(self):

        num_of_bodies = len(self.get_bodies())
        
        r = 0
        g = 0
        b = 0

        for bd in self.get_bodies():
            r += bd.get_color()[0]
            g += bd.get_color()[1]
            b += bd.get_color()[2]

        r = r/num_of_bodies
        g = g/num_of_bodies
        b = b/num_of_bodies

        return [r, g, b]

    def get_mass(self):
        mass = 0
        for b in self.get_bodies():
            mass += b.get_mass()

        return mass

    def get_pos(self):

        sum_vec = vec3()
        
        for b in self.get_bodies():
            sum_vec += b.get_pos() * b.get_mass()

        return sum_vec/self.get_mass()

    def get_vel(self):

        sum_x = 0
        sum_y = 0
        sum_z = 0

        for b in self.get_bodies():
            sum_x += b.get_mass() * b.get_vel().x
            sum_y += b.get_mass() * b.get_vel().y
            sum_z += b.get_mass() * b.get_vel().z

        return [sum_x/self.get_mass(), sum_y/self.get_mass(), sum_z/self.get_mass()]

    def get_vel_mag(self):
        return mag(self.vel)

    def get_draw_pos(self):
        return self.get_pos() * visual_scaling_factor

    def get_pos_rel_to(self, obj):
        return self.pos - obj.pos

    def get_dist_to(self, obj):
        return (self.pos - obj.pos).mag()

    def get_vel_rel_to(self, obj):
        return self.vel - obj.vel

    def get_vel_mag_rel_to(self, obj):
        return (self.vel - obj.vel).mag()

