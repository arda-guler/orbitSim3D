from math_utils import *
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

        self.draw_pos = vector_scale(self.pos, visual_scaling_factor)

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
        return [self.pos[0] - obj.pos[0],
                self.pos[1] - obj.pos[1],
                self.pos[2] - obj.pos[2]]

    def set_pos(self, pos):
        self.pos = pos

    def get_vel(self):
        return self.vel

    def get_vel_rel_to(self, obj):
        return [self.vel[0] - obj.vel[0],
                self.vel[1] - obj.vel[1],
                self.vel[2] - obj.vel[2]]

    def get_vel_mag(self):
        return mag(self.vel)

    def get_vel_mag_rel_to(self, obj):
        return (((self.vel[0] - obj.vel[0])**2 +
                 (self.vel[1] - obj.vel[1])**2 +
                 (self.vel[2] - obj.vel[2])**2)**0.5)

    def set_vel(self, vel):
        self.vel = vel

    def get_orient(self):
        return self.orient

    def rotate_body(self, rotation):
        self.orient = rotate_matrix(self.orient, rotation)

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return ((self.pos[0] - obj.pos[0])**2 +
                (self.pos[1] - obj.pos[1])**2 +
                (self.pos[2] - obj.pos[2])**2)**0.5

    def get_unit_vector_towards(self, obj):
        return [((obj.pos[0] - self.pos[0])/(self.get_dist_to(obj))),
                ((obj.pos[1] - self.pos[1])/(self.get_dist_to(obj))),
                ((obj.pos[2] - self.pos[2])/(self.get_dist_to(obj)))]

    def get_gravity_by(self, body):
        grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
        grav_vec = vector_scale(self.get_unit_vector_towards(body), grav_mag)
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel[0] += accel[0] * dt
        self.vel[1] += accel[1] * dt
        self.vel[2] += accel[2] * dt

    def update_pos(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

    # rotate the planet around its rotation axis
    def update_orient(self, dt):
        if self.day_length:
            rotation_amount = dt*360/self.day_length
            self.rotate_body([0,rotation_amount,0])

    # convert abosulte coords to body-centered reference frame coords, both cartezian
    # it's like the ECEF coordinate system
    def get_body_centered_coords(self, body):        
        return [((self.pos[0] - body.pos[0]) * body.orient[0][0]) + ((self.pos[1] - body.pos[1]) * body.orient[0][1]) + ((self.pos[2] - body.pos[2]) * body.orient[0][2]),
                ((self.pos[0] - body.pos[0]) * body.orient[1][0]) + ((self.pos[1] - body.pos[1]) * body.orient[1][1]) + ((self.pos[2] - body.pos[2]) * body.orient[1][2]),
                ((self.pos[0] - body.pos[0]) * body.orient[2][0]) + ((self.pos[1] - body.pos[1]) * body.orient[2][1]) + ((self.pos[2] - body.pos[2]) * body.orient[2][2])]

    def update_traj_history(self):
        self.traj_history.append(self.pos)

    def clear_traj_history(self):
        self.traj_history = []

    def get_traj_history(self):
        return self.traj_history

    def update_draw_pos(self):
        self.draw_pos = vector_scale(self.pos, visual_scaling_factor)

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
