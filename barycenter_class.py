from math_utils import *

class barycenter:
    def __init__(self, name, bodies):
        self.name = name
        self.bodies = bodies
        self.pos = self.get_pos()
        self.vel = self.get_vel()

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
        
        sum_x = 0
        sum_y = 0
        sum_z = 0
        
        for b in self.get_bodies():
            sum_x += b.get_mass() * b.get_pos()[0]
            sum_y += b.get_mass() * b.get_pos()[1]
            sum_z += b.get_mass() * b.get_pos()[2]

        return [sum_x/self.get_mass(), sum_y/self.get_mass(), sum_z/self.get_mass()]

    def get_vel(self):

        sum_x = 0
        sum_y = 0
        sum_z = 0

        for b in self.get_bodies():
            sum_x += b.get_mass() * b.get_vel()[0]
            sum_y += b.get_mass() * b.get_vel()[1]
            sum_z += b.get_mass() * b.get_vel()[2]

        return [sum_x/self.get_mass(), sum_y/self.get_mass(), sum_z/self.get_mass()]

    def get_vel_mag(self):
        return mag(self.vel)

    def get_draw_pos(self):
        return vector_scale(self.get_pos(), visual_scaling_factor)

    def get_pos_rel_to(self, obj):
        return [self.pos[0] - obj.pos[0],
                self.pos[1] - obj.pos[1],
                self.pos[2] - obj.pos[2]]

    def get_dist_to(self, obj):
        return ((self.pos[0] - obj.pos[0])**2 +
                (self.pos[1] - obj.pos[1])**2 +
                (self.pos[2] - obj.pos[2])**2)**0.5

    def get_vel_rel_to(self, obj):
        return [self.vel[0] - obj.vel[0],
                self.vel[1] - obj.vel[1],
                self.vel[2] - obj.vel[2]]

    def get_vel_mag_rel_to(self, obj):
        return (((self.vel[0] - obj.vel[0])**2 +
                 (self.vel[1] - obj.vel[1])**2 +
                 (self.vel[2] - obj.vel[2])**2)**0.5)
