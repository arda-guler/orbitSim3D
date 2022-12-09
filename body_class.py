from math_utils import *
from vector3 import *
import math

class body():
    def __init__(self, name, model, model_path, mass, radius, color, pos, vel, orient,
                 day_length, J2, luminosity, atmos_sea_level_density, atmos_scale_height):
        self.name = name
        self.model = model
        self.model_path = model_path
        self.mass = mass
        self.radius = radius
        self.color = color
        self.pos = pos
        self.vel = vel
        self.orient = orient
        self.day_length = day_length
        self.traj_history = []
        self.J2 = J2
        self.luminosity = luminosity # used for calculating radiation pressure due to Sun etc. (Watts)
        self.atmos_sea_level_density = atmos_sea_level_density
        self.atmos_scale_height = atmos_scale_height

        self.draw_pos = self.pos * visual_scaling_factor

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_model_path(self):
        return self.model_path

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_luminosity(self):
        return self.luminosity

    def set_luminosity(self, luminosity):
        self.luminosity = luminosity

    def get_flux_density_at_dist(self, dist):
        if not self.luminosity:
            return 0
        else:
            # clamp to surface radiation just in case collision check is disabled and some spacecraft goes into the Sun
            return self.luminosity/(4*math.pi*(dist**2)) # W m-2

    def get_pos(self):
        return self.pos

    def get_pos_rel_to(self, obj):
        return self.pos - obj.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_vel(self):
        return self.vel

    def get_vel_rel_to(self, obj):
        return self.vel - obj.vel

    def get_vel_mag(self):
        return mag(self.vel)

    def get_vel_mag_rel_to(self, obj):
        return (self.vel - obj.vel).mag()

    def set_vel(self, vel):
        self.vel = vel

    def get_orient(self):
        return self.orient

    def rotate_body(self, rotation):
        self.orient = self.orient.rotate_legacy(rotation)

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return (self.pos - obj.pos).mag()

    def get_unit_vector_towards(self, obj):
        return (obj.pos - self.pos).normalized()

    def get_gravity_by(self, body):
        grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
        grav_vec = self.get_unit_vector_towards(body) * grav_mag
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel = self.vel + accel * dt

    def update_pos(self, dt):
        self.pos = self.pos + self.vel * dt

    # rotate the planet around its rotation axis
    def update_orient(self, dt):
        if self.day_length:
            rotation_amount = dt*360/self.day_length
            self.rotate_body([0,rotation_amount,0])

    # convert abosulte coords to body-centered reference frame coords, both cartezian
    # it's like the ECEF coordinate system
    def get_body_centered_coords(self, body):
        x_diff = self.pos.x - body.pos.x
        y_diff = self.pos.y - body.pos.y
        z_diff = self.pos.z - body.pos.z
        return vec3(lst=[(x_diff * body.orient.m11) + (y_diff * body.orient.m12) + (z_diff * body.orient.m13),
                         (x_diff * body.orient.m21) + (y_diff * body.orient.m22) + (z_diff * body.orient.m23),
                         (x_diff * body.orient.m31) + (y_diff * body.orient.m32) + (z_diff * body.orient.m33)])

    def update_traj_history(self):
        self.traj_history.append(self.pos)

    def clear_traj_history(self):
        self.traj_history = []

    def get_traj_history(self):
        return self.traj_history

    def update_draw_pos(self):
        self.draw_pos = self.pos * visual_scaling_factor

    def get_draw_pos(self):
        return self.draw_pos

    def get_J2(self):
        return self.J2

    def get_day_length(self):
        return self.day_length

    def get_atmospheric_density_at_alt(self, alt):
        if self.atmos_sea_level_density and self.atmos_scale_height:
            r = alt + self.radius
            R = self.radius
            H = self.atmos_scale_height

            return self.atmos_sea_level_density * math.e**((R-r)/H)
        else:
            return 0

    def get_angular_radius_at_dist(self, dist):
        return math.atan(self.radius/dist)

    def get_angular_radius_from(self, point):
        if type(point) == list:
            point = vec3(lst=point)
            dist = (self.pos - point).mag()
        else:
            dist = self.get_dist_to(point)

        return self.get_angular_radius_at_dist(dist)
