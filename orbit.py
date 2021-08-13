from math_utils import *

class kepler_projection():
    def __init__(self, name, vessel, body, proj_time):
        self.name = name
        self.vessel = vessel
        self.body = body

        self.proj_time = proj_time

        # state vectors
        self.pos0 = vessel.get_pos_rel_to(body)
        self.vel0 = vessel.get_vel_rel_to(body)

        # mu = standard gravitational parameter
        self.mu = body.get_mass() * grav_const

        self.angular_momentum = cross(self.pos0, self.vel0)

        self.eccentricity = self.get_eccentricity()
        self.energy = self.get_energy()
        self.semimajor_axis = self.get_semimajor_axis()

        self.periapsis = self.get_periapsis()
        self.apoapsis = self.get_apoapsis()

        self.period = self.get_period()
        
        self.vertices, self.draw_vertices, self.draw_ap, self.draw_pe = self.generate_projection()

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body

    def get_vessel(self):
        return self.vessel

    def get_eccentricity_vector(self):
        r_scaler = self.vessel.get_vel_mag_rel_to(self.body)**2 - (self.mu/self.vessel.get_dist_to(self.body))
        v_scaler = dot(self.pos0, self.vel0)

        scaled_r = vector_scale(self.pos0, r_scaler)
        scaled_v = vector_scale(self.vel0, v_scaler)

        e_vec = [(scaled_r[0] - scaled_v[0])/self.mu,
                 (scaled_r[1] - scaled_v[1])/self.mu,
                 (scaled_r[2] - scaled_v[2])/self.mu]

        return e_vec

    def get_eccentricity(self):
        return mag(self.get_eccentricity_vector())

    def get_energy(self):
        return ((mag(self.vel0)**2)/2) - (self.mu/mag(self.pos0))
    
    def get_semimajor_axis(self):
        if not self.eccentricity == 1:
            smj = (-self.mu)/(2*self.energy)
        else:
            smj = "inf"

        return smj

    def get_periapsis(self):
        if not self.semimajor_axis == "inf":
            p = self.semimajor_axis * (1 - (self.eccentricity**2))
        else:
            p = (mag(self.angular_momentum)**2)/self.mu

        return p

    def get_periapsis_alt(self):
        return self.get_periapsis() - self.body.get_radius()

    def get_apoapsis(self):
        if not self.semimajor_axis == "inf":
            a = self.semimajor_axis * (1 + (self.eccentricity**2))
        else:
            a = "inf"

        return a

    def get_apoapsis_alt(self):
        return self.get_apoapsis() - self.body.get_radius()

    def get_period(self):
        if not self.semimajor_axis == "inf":
            return 2*3.141*((self.semimajor_axis**3)/self.mu)**0.5
        else:
            return "inf"

    def generate_projection(self):
        vertices = []

        if not self.period:
            end_time = 10000
        else:
            end_time = self.period

        if end_time > 100000:
            time_step = end_time / 5000
        else:
            time_step = 0.1
        
        current_pos = self.pos0
        current_vel = self.vel0

        t = 0
        while t <= end_time:
            # update gravity
            current_grav = [((self.mu * -current_pos[0])/mag(current_pos)**3),
                            ((self.mu * -current_pos[1])/mag(current_pos)**3),
                            ((self.mu * -current_pos[2])/mag(current_pos)**3)]
            
            # update velocity
            current_vel[0] += current_grav[0] * time_step
            current_vel[1] += current_grav[1] * time_step
            current_vel[2] += current_grav[2] * time_step

            # update position
            current_pos[0] += current_vel[0] * time_step
            current_pos[1] += current_vel[1] * time_step
            current_pos[2] += current_vel[2] * time_step
            
            vertices.append([self.body.get_pos()[0] + current_pos[0],
                             self.body.get_pos()[1] + current_pos[1],
                             self.body.get_pos()[2] + current_pos[2]])

            t += time_step

        draw_vertices = []
        ap = None
        pe = None
        
        for vertex in vertices:
            draw_vertices.append(vector_scale(vertex, visual_scaling_factor))
            
            # get apoapsis and periapsis
            adjusted_r = mag([vertex[0] - self.body.get_pos()[0],
                              vertex[1] - self.body.get_pos()[1],
                              vertex[2] - self.body.get_pos()[2]])

            if ap:
                adjusted_ap = mag([ap[0] - self.body.get_pos()[0],
                                   ap[1] - self.body.get_pos()[1],
                                   ap[2] - self.body.get_pos()[2]])

            if pe:
                adjusted_pe = mag([pe[0] - self.body.get_pos()[0],
                                   pe[1] - self.body.get_pos()[1],
                                   pe[2] - self.body.get_pos()[2]])

            if not ap or adjusted_r > adjusted_ap:
                ap = vertex
            if not pe or adjusted_r < adjusted_pe:
                pe = vertex

        draw_ap = vector_scale(ap, visual_scaling_factor)
        draw_pe = vector_scale(pe, visual_scaling_factor)

        return vertices, draw_vertices, draw_ap, draw_pe

    def get_draw_vertices(self):
        return self.draw_vertices

    def get_params_str(self):
        output = "Kepler orbit projection of " + self.get_vessel().get_name() + " around " + self.get_body().get_name() + " at t = " + str(self.proj_time) + "\n"
        output += "Apoapsis_R: " + str(self.get_apoapsis()) + "   Apoapsis_Alt: " + str(self.get_apoapsis_alt()) + "\n"
        output += "Periapsis_R: " + str(self.get_periapsis()) + "   Periapsis_Alt: " + str(self.get_periapsis_alt()) + "\n"
        output += "Orbital Period: " + str(self.get_period()) + "\n"
        output += "Semi-major Axis: " + str(self.get_semimajor_axis()) + "   Eccentricity: " + str(self.eccentricity) + "\n"

        return output
