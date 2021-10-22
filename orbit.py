from math_utils import *
import math
import time

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
        
        self.vertices, self.draw_vertices, self.draw_ap, self.draw_pe, self.draw_an, self.draw_dn, self.inclination = self.generate_projection()

        self.body_draw_pos_prev = self.body.get_draw_pos()

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

    def get_inclination(self):
        return self.inclination

    def generate_projection(self):
        vertices = []

        if not self.period:
            end_time = 10000
        else:
            end_time = self.period
        
        current_pos = self.pos0
        current_vel = self.vel0

        inclination = None

        draw_vertices = []
        Rs = []
        Ys = []

        time_step = 0.1
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
            
            vertices.append(current_pos)
            draw_vertices.append(vector_scale(current_pos, visual_scaling_factor))
            Rs.append(mag(current_pos))
            Ys.append(abs2frame_coords(vector_add_safe(current_pos, self.get_body().get_pos()), self.get_body())[1])

            t += time_step
            time_step = min((self.mu/mag(current_grav) * 0.000000000000001), end_time/100000)

            current_rel_pos = abs2frame_coords(vector_add_safe(current_pos, self.get_body().get_pos()), self.get_body())
            
            try:
                current_lat = math.degrees(math.atan(current_rel_pos[1]/math.sqrt(current_rel_pos[0]**2 + current_rel_pos[2]**2)))
            except ZeroDivisionError:
                current_lat = 90
                
            if not inclination or inclination < current_lat:
                inclination = current_lat

        ap_index = Rs.index(max(Rs))
        pe_index = Rs.index(min(Rs))

        for i in range(len(Ys)-1):
            if not sign(Ys[i]) == sign(Ys[i+1]):
                if sign(Ys[i+1]) > 0:
                    an_index = i+1
                else:
                    dn_index = i+1

        draw_an = draw_vertices[an_index]
        draw_dn = draw_vertices[dn_index]

        draw_ap = draw_vertices[ap_index]
        draw_pe = draw_vertices[pe_index]

        return vertices, draw_vertices, draw_ap, draw_pe, draw_an, draw_dn, inclination

    def get_draw_vertices(self):
        return self.draw_vertices

    def get_params_str(self):
        output = "Kepler orbit projection of " + self.get_vessel().get_name() + " around " + self.get_body().get_name() + " at t = " + str(self.proj_time) + "\n"
        output += "Apoapsis_R: " + str(self.get_apoapsis()) + "   Apoapsis_Alt: " + str(self.get_apoapsis_alt()) + "\n"
        output += "Periapsis_R: " + str(self.get_periapsis()) + "   Periapsis_Alt: " + str(self.get_periapsis_alt()) + "\n"
        output += "Orbital Period: " + str(self.get_period()) + "\n"
        output += "Semi-major Axis: " + str(self.get_semimajor_axis()) + "   Eccentricity: " + str(self.eccentricity) + "\n"
        output += "Inclination: " + str(self.get_inclination()) + "\n"

        return output
