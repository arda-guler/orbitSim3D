from math_utils import *
from vector3 import *

class vessel():
    def __init__(self, name, model, model_path, color, pos, vel):
        self.name = name
        self.model = model
        self.model_path = model_path
        self.color = color
        self.pos = pos
        self.vel = vel
        self.traj_history = []
        self.draw_traj_history = []

        self.draw_pos = self.pos * visual_scaling_factor

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_model_path(self):
        return self.model_path

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_pos_rel_to(self, obj):
        return self.pos - obj.pos

    def get_vel(self):
        return self.vel

    def get_vel_rel_to(self, obj):
        return self.vel - obj.vel

    def get_vel_mag(self):
        return self.vel.mag()

    def get_vel_mag_rel_to(self, obj):
        return (self.vel - obj.vel).mag()

    def set_vel(self, vel):
        self.vel = vel

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return (self.pos - obj.pos).mag()

    # get altitude above surface
    def get_alt_above(self, body):
        return self.get_dist_to(body) - body.get_radius()

    # drawing scene is scaled down by a factor of visual_scaling_factor
    def update_draw_pos(self):
        self.draw_pos = self.pos * visual_scaling_factor

    def get_draw_pos(self):
        return self.draw_pos

    def get_unit_vector_towards(self, obj):
        return (obj.pos - self.pos).normalized()

    # convert abosulte coords to body-centered reference frame coords, both cartezian
    # it's like the ECEF coordinate system
    def get_body_centered_coords(self, body):
        x_diff = self.pos.x - body.pos.x
        y_diff = self.pos.y - body.pos.y
        z_diff = self.pos.z - body.pos.z
        return vec3(lst=[(x_diff * body.orient.m11) + (y_diff * body.orient.m12) + (z_diff * body.orient.m13),
                         (x_diff * body.orient.m21) + (y_diff * body.orient.m22) + (z_diff * body.orient.m23),
                         (x_diff * body.orient.m31) + (y_diff * body.orient.m32) + (z_diff * body.orient.m33)])

    def get_gravity_by(self, body):
        grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
        grav_vec = self.get_unit_vector_towards(body) * grav_mag

        # Apply J2 perturbation
        # https://www.vcalc.com/equation/?uuid=1e5aa6ea-95a3-11e7-9770-bc764e2038f2
        if body.get_J2():
            # (3 J2 mu R_body^2) / (2 R^5)
            J2_mult_numerator = (3*body.get_J2()*(grav_const*body.get_mass())*body.get_radius()**2)
            J2_mult_denominator = 2 * self.get_dist_to(body)**5
            J2_mult = J2_mult_numerator / J2_mult_denominator

            R_squared = self.get_dist_to(body)**2
            Z_squared = self.get_body_centered_coords(body).y**2
            X = self.get_body_centered_coords(body).x
            Y = self.get_body_centered_coords(body).z
            Z = self.get_body_centered_coords(body).y
            J2_perturbation_accel = vec3(lst=[(((5*(Z_squared/R_squared))-1) * X),
                                              (((5*(Z_squared/R_squared))-3) * Z),
                                              (((5*(Z_squared/R_squared))-1) * Y)])

            J2_perturbation_accel = J2_perturbation_accel * J2_mult

            grav_vec = vec3(lst=[grav_vec.x + (J2_perturbation_accel.x * body.orient.m11) + (J2_perturbation_accel.y * body.orient.m21) + (J2_perturbation_accel.z * body.orient.m31),
                                 grav_vec.y + (J2_perturbation_accel.x * body.orient.m12) + (J2_perturbation_accel.y * body.orient.m22) + (J2_perturbation_accel.z * body.orient.m32),
                                 grav_vec.z + (J2_perturbation_accel.x * body.orient.m13) + (J2_perturbation_accel.y * body.orient.m23) + (J2_perturbation_accel.z * body.orient.m33)])
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel = self.vel + accel * dt

    def update_pos(self, dt):
        self.pos = self.pos + self.vel * dt

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
            return self.get_vel_rel_to(frame).normalized()

        elif orientation == "retrograde" or orientation == "retrograde_dynamic":
            return self.get_vel_rel_to(frame).normalized() * (-1)
        
        elif orientation == "radial_in" or orientation == "radial_in_dynamic":
            return self.get_unit_vector_towards(frame)
        
        elif orientation == "radial_out" or orientation == "radial_out_dynamic":
            return self.get_unit_vector_towards(frame) * (-1)
        
        elif orientation == "normal" or orientation == "normal_dynamic":
            return self.get_vel_rel_to(frame).cross(self.get_unit_vector_towards(frame)).normalized()

        elif orientation == "antinormal" or orientation == "antinormal_dynamic":
            return self.get_vel_rel_to(frame).cross(self.get_unit_vector_towards(frame)).normalized() * (-1)
        
        elif orientation == "prograde_tangential" or orientation == "prograde_tangential_dynamic":
            prograde = self.get_vel_rel_to(frame).normalized()
            radial = self.get_unit_vector_towards(frame)
            radial_dot = prograde.dot(radial)
            unvec = prograde - radial * radial_dot
            vec = unvec.normalized()
            return vec
        
        elif orientation == "retrograde_tangential" or orientation == "retrograde_tangential_dynamic":
            retrograde = self.get_vel_rel_to(frame).normalized() * (-1)
            radial = self.get_unit_vector_towards(frame)
            radial_dot = retrograde.dot(radial)
            unvec = retrograde - radial * radial_dot
            vec = unvec.normalized()
            return vec
