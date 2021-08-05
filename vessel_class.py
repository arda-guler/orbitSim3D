from math_utils import *

grav_const = (6.674*(10**-11)) # m^3 kg^-1 s^-2
visual_scaling_factor = (3*(10**(-4))) # arbitrary, unitless

class vessel():
    def __init__(self, name, model, color, pos, vel):
        self.name = name
        self.model = model
        self.color = color
        self.pos = pos
        self.vel = vel
        self.draw_pos = [self.pos[0]*visual_scaling_factor,
                         self.pos[1]*visual_scaling_factor,
                         self.pos[2]*visual_scaling_factor]
        self.traj_history = []
        self.draw_traj_history = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_pos_rel_to(self, obj):
        return [self.pos[0] - obj.pos[0],
                self.pos[1] - obj.pos[1],
                self.pos[2] - obj.pos[2]]

    def get_vel(self):
        return self.vel

    def get_vel_rel_to(self, obj):
        return [self.vel[0] - obj.vel[0],
                self.vel[1] - obj.vel[1],
                self.vel[2] - obj.vel[2]]

    def get_vel_mag(self):
        return (self.vel[0] ** 2 + self.vel[1] ** 2 + self.vel[2] ** 2) ** 0.5

    def get_vel_mag_rel_to(self, obj):
        return (((self.vel[0] - obj.vel[0])**2 +
                 (self.vel[1] - obj.vel[1])**2 +
                 (self.vel[2] - obj.vel[2])**2)**0.5)

    def set_vel(self, vel):
        self.vel = vel

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return ((self.pos[0] - obj.pos[0])**2 +
                (self.pos[1] - obj.pos[1])**2 +
                (self.pos[2] - obj.pos[2])**2)**0.5

    # get altitude above surface
    def get_alt_above(self, body):
        return (self.get_dist_to(body) - body.get_radius())

    # drawing scene is scaled down by a factor of 3x10^-4
    def update_draw_pos(self):
        self.draw_pos = [self.pos[0]*visual_scaling_factor,
                         self.pos[1]*visual_scaling_factor,
                         self.pos[2]*visual_scaling_factor]

    def get_draw_pos(self):
        return self.draw_pos

    def get_unit_vector_towards(self, obj):
        return [((obj.pos[0] - self.pos[0])/(self.get_dist_to(obj))),
                ((obj.pos[1] - self.pos[1])/(self.get_dist_to(obj))),
                ((obj.pos[2] - self.pos[2])/(self.get_dist_to(obj)))]

    def get_gravity_by(self, body):
        grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
        
        grav_vec = [grav_mag * self.get_unit_vector_towards(body)[0],
                    grav_mag * self.get_unit_vector_towards(body)[1],
                    grav_mag * self.get_unit_vector_towards(body)[2]]
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel[0] += accel[0] * dt
        self.vel[1] += accel[1] * dt
        self.vel[2] += accel[2] * dt

    def update_pos(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

    def update_traj_history(self):
        self.traj_history.append(self.pos)

    def clear_traj_history(self):
        self.traj_history = []

    def get_traj_history(self):
        return self.traj_history

    def update_draw_traj_history(self):
        self.draw_traj_history.append(self.draw_pos)

    def clear_draw_traj_history(self):
        self.draw_traj_history = []

    def get_draw_traj_history(self):
        return self.draw_traj_history

    def get_color(self):
        return self.color

    def get_orientation_rel_to(self, frame, orientation):
        if orientation == "prograde" or orientation == "prograde_dynamic":
            return [self.get_vel_rel_to(frame)[0]/self.get_vel_mag_rel_to(frame),
                    self.get_vel_rel_to(frame)[1]/self.get_vel_mag_rel_to(frame),
                    self.get_vel_rel_to(frame)[2]/self.get_vel_mag_rel_to(frame)]
        elif orientation == "retrograde" or orientation == "retrograde_dynamic":
            return [-self.get_vel_rel_to(frame)[0]/self.get_vel_mag_rel_to(frame),
                    -self.get_vel_rel_to(frame)[1]/self.get_vel_mag_rel_to(frame),
                    -self.get_vel_rel_to(frame)[2]/self.get_vel_mag_rel_to(frame)]
        elif orientation == "radial_in" or orientation == "radial_in_dynamic":
            return self.get_unit_vector_towards(frame)
        elif orientation == "radial_out" or orientation == "radial_out_dynamic":
            return [-self.get_unit_vector_towards(frame)[0],
                    -self.get_unit_vector_towards(frame)[1],
                    -self.get_unit_vector_towards(frame)[2]]
        elif orientation == "normal" or orientation == "normal_dynamic":
            cross_vec = cross(self.get_vel_rel_to(frame), self.get_unit_vector_towards(frame))
            cross_vec_mag = (cross_vec[0]**2 + cross_vec[1]**2 + cross_vec[2]**2)**0.5
            normal_vec = [cross_vec[0]/cross_vec_mag,
                          cross_vec[1]/cross_vec_mag,
                          cross_vec[2]/cross_vec_mag]
            return normal_vec
        elif orientation == "antinormal" or orientation == "antinormal_dynamic":
            cross_vec = cross(self.get_vel_rel_to(frame), self.get_unit_vector_towards(frame))
            cross_vec_mag = (cross_vec[0]**2 + cross_vec[1]**2 + cross_vec[2]**2)**0.5
            antinormal_vec = [-cross_vec[0]/cross_vec_mag,
                              -cross_vec[1]/cross_vec_mag,
                              -cross_vec[2]/cross_vec_mag]
            return antinormal_vec
