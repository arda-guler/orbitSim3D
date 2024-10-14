from math_utils import *
from vector3 import *
from graphics import *
import math

class body():
    def __init__(self, name, model, model_path, surface_map_path, mass, radius, color, pos, vel, orient,
                 day_length, rot_axis, J2, luminosity, atmos_sea_level_density, atmos_scale_height,
                 point_mass_cloud):
        self.name = name
        self.model = model
        self.model_path = model_path
        self.surface_map_path = surface_map_path
        self.mass = mass
        self.radius = radius
        self.color = color
        self.pos = pos
        self.vel = vel
        self.orient = orient
        self.day_length = day_length
        self.rot_axis = rot_axis
        self.J2 = J2
        self.luminosity = luminosity # used for calculating radiation pressure due to Sun etc. (Watts)
        self.atmos_sea_level_density = atmos_sea_level_density
        self.atmos_scale_height = atmos_scale_height
        self.point_mass_cloud = point_mass_cloud # used for modeling bodies with non-uniform lumpy mass distributions

        if self.point_mass_cloud:
            self.check_pmc()

        self.traj_history = []
        self.draw_pos = self.pos * visual_scaling_factor

        if self.surface_map_path != None:
            # do additional processing of Wavefront obj for surface texture rendering
            # first, get the list of vertex texture coordinates
            self.us = []
            self.vs = []

            self.vtx_tex_mapping = []
            with open(self.model_path, "r") as f:
                lines = f.readlines()

                for line in lines:
                    if line.startswith("vt"):
                        line = line.strip().split()
                        u = float(line[1])
                        v = float(line[2])

                        self.us.append(u)
                        self.vs.append(v)

                # now get the vertex-coordinate mapping
                for line in lines:
                    if line.startswith("f"):
                        line = line.strip().split()
                        for i in range(1, 4): # 1, 2, 3
                            vertex_bunch = line[i]
                            vertex_bunch = vertex_bunch.split("/")
                            self.vtx_tex_mapping.append(int(vertex_bunch[1]) - 1)
                            # self.vtx_tex_mapping[int(vertex_bunch[0]) - 1] = int(vertex_bunch[1]) - 1

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

    def get_rot_axis(self):
        return self.rot_axis

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
        return self.vel.mag()

    def get_vel_mag_rel_to(self, obj):
        return (self.vel - obj.vel).mag()

    def set_vel(self, vel):
        self.vel = vel

    def get_orient(self):
        return self.orient

    def get_surface_map_path(self):
        if self.surface_map_path != None:
            return self.surface_map_path
        else:
            return "None"

    def load_surface_map(self):
        if self.surface_map_path != None:
            self.surface_map = loadTexture(self.surface_map_path)

    def check_pmc(self):
        # normally we don't reaallly want to print anything outside of main.py
        # but this can be an exception since it works only at initialization
        total_mass = sum([m[1] for m in self.point_mass_cloud])
        if abs(total_mass - self.mass) > self.mass * 1e-4:
            print("\nThe total mass of the point-mass-cloud of body " + self.get_name() + " does not match its mass!\nThe point-mass-cloud will be removed.\n")
            input("Press Enter to continue...")
            self.point_mass_cloud = []

        CoM_x = sum([m[0][0] * m[1] for m in self.point_mass_cloud])
        CoM_y = sum([m[0][1] * m[1] for m in self.point_mass_cloud])
        CoM_z = sum([m[0][2] * m[1] for m in self.point_mass_cloud])

        CoM = vec3(CoM_x, CoM_y, CoM_z)
        
        if CoM.mag() > self.radius * 1e-4:
            print("\nThe center of mass of the point-mass-cloud of body " + self.get_name() + " does not lie at the object's center!\nThe point-mass-cloud will be removed.\n")
            input("Press Enter to continue...")
            self.point_mass_cloud = []

        # if all is well, correct the miniscule amount of error in the center-of-mass by shifting all point masses by a little
        for m in self.point_mass_cloud:
            m[0] = m[0] - CoM

    def get_pm_abs(self, idx_pm):
        # get absolute position of the point mass (as they are stored in the form of relative
        # positions normally (that also helps reduce numerical errors))
        pm_rel_pos = self.point_mass_cloud[idx_pm][0]
        pm_abs_pos = self.pos + self.orient.vx() * pm_rel_pos[0] + self.orient.vy() * pm_rel_pos[1] + self.orient.vz() * pm_rel_pos[2]

        pm_mass = self.point_mass_cloud[idx_pm][1]
        
        return pm_abs_pos, pm_mass

    def pmc_to_str(self):
        # turn the point-mass-cloud data to a text-exportable format
        if not self.point_mass_cloud:
            return "[]"

        output = "["
        
        for idx_pm, pm in enumerate(self.point_mass_cloud):
            output += "[" + str(pm[0].tolist()) + "," + str(pm[1]) + "]"
            if idx_pm < len(self.point_mass_cloud) - 1:
                output += ","

        output += "]"
        
        return output

    def rotate_body(self, rotation):
        self.orient = self.orient.rotate_legacy(rotation)

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return (self.pos - obj.pos).mag()

    def get_unit_vector_towards(self, obj):
        return (obj.pos - self.pos).normalized()

    def get_gravity_by(self, body):
        if not body.point_mass_cloud:
            grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
            grav_vec = self.get_unit_vector_towards(body) * grav_mag

        else:
            grav_vec = vec3(0, 0, 0)

            # iterate over point mass elements and add their gravitational contribution
            for idx_pm in range(len(body.point_mass_cloud)):
                pm_pos, pm_mass = body.get_pm_abs(idx_pm)
                grav_mag = (grav_const * pm_mass)/(((self.pos - pm_pos).mag())**2)
                grav_vec = grav_vec + (pm_pos - self.pos).normalized() * grav_mag
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel = self.vel + accel * dt

    def update_pos(self, dt):
        self.pos = self.pos + self.vel * dt

    # rotate the planet around its rotation axis
    def update_orient(self, dt):
        if self.day_length:
            rotation_amount = dt*360/self.day_length
            rotation = self.rot_axis * rotation_amount
            self.rotate_body(rotation.tolist())

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
