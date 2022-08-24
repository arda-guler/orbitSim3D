import math

from math_utils import *
c = 299792458 # m s-1, speed of light

class radiation_pressure:
    def __init__(self, name, vessel, body, area, orientation_frame, direction, mass, mass_auto_update):
        self.name = name
        self.vessel = vessel
        self.body = body
        self.area = area
        self.orientation_frame = orientation_frame
        self.direction = direction
        self.direction_input = direction
        self.mass = mass
        self.mass_auto_update = mass_auto_update
        self.occultation = 0

    def set_direction(self):
        if not type(self.direction) == list or self.direction_input[-8:] == "_dynamic":
            self.direction = self.vessel.get_orientation_rel_to(self.orientation_frame, self.direction_input)

    def get_name(self):
        return self.name

    def get_vessel(self):
        return self.vessel

    def get_body(self):
        return self.body

    def get_area(self):
        return self.area

    def get_direction(self):
        return self.direction

    def get_mass(self):
        return self.mass

    def set_mass(self, m):
        self.mass = m

    def get_orientation_frame(self):
        return self.orientation_frame

    def update_occultation(self, bodies):
        # checks how much of the illuminating body's disk is occulted
        # returns 1 if the illuminating body is not visible, 0 if it is completely visible
        a = self.body.get_angular_radius_from(self.vessel)
        s = 0

        for occulting_body in bodies:
            if not occulting_body == self.body and self.vessel.get_dist_to(self.body) > occulting_body.get_dist_to(self.body):
                b = occulting_body.get_angular_radius_from(self.vessel)

                vec_to_illum_body = self.vessel.get_unit_vector_towards(self.body)
                vec_to_occult_body = self.vessel.get_unit_vector_towards(occulting_body)
                # the angular separation of the centers of both bodies
                c_numerator = dot(vec_to_illum_body, vec_to_occult_body)
                c_denominator = mag(vec_to_illum_body) * mag(vec_to_occult_body)
                c = math.acos(c_numerator / c_denominator)

                if b > a + c:
                    s_c = 1
                    
                elif c < a + b:
                    try:
                        A = 2 * math.acos((b**2 - a**2 - c**2)/(-2*a*c))
                    except ValueError:
                        print((b**2 - a**2 - c**2)/(-2*a*c))
                        time.sleep(5)
                        A = 2 * math.pi
                        
                    ratio_est = A / (2*math.pi)
                    s_c = ratio_est
                    
                else:
                    s_c = 0

##                print("a", a)
##                print("b", b)
##                print("c", c)
##
##                # now use the formulas
##                x = (c**2 + a**2 - b**2)/(2*c)
##                y = (a**2 - x**2)**(0.5)
##                try:
##                    A = a**2 * math.acos(x/a) + b**2 * math.acos((c-x)/b) - c * y
##                except ValueError:
##                    print("FF")
##                    A = 0
##
##                s_c = A/(math.pi * a**2)

                # multiple bodies may occlude the source. use the largest occlusion.
                if s_c > s:
                    s = s_c
        
        self.occultation = s

    def update_mass(self, maneuvers, sim_time, dt):
        # if a vessel makes a maneuver and spends propellant, its mass will change
        # we can auto-update it to make user's life easier (if they wish so)
        if self.mass_auto_update:
            for m in maneuvers:
                # mid-maneuver update
                if m.type == "const_thrust" and m.t_start <= sim_time <= m.t_start + m.duration:
                    self.mass = m.mass
                # maneuver finish update
                elif m.type == "const_thrust" and m.t_start + m.duration >= sim_time and m.t_start + m.duration <= sim_time + dt:
                    self.mass = m.mass_init - mass_flow * duration

            # in case of a const-accel maneuver the user will have to update manaully
            # if siginificant propellant mass was spent
            # we don't track mass through constant acceleration maneuvers because the
            # mass flow rate will vary according to some complex engineering variables
            # that are highly propulsion-system-design-specific

    def calc_accel(self):
        self.set_direction()
        
        # https://en.wikipedia.org/wiki/Radiation_pressure
        flux_density = self.body.get_flux_density_at_dist(self.vessel.get_dist_to(self.body)) # W m-2
        pressure = flux_density/c # N m-2
        zenith_dir = self.body.get_unit_vector_towards(self.vessel)
        cos_diverge_angle = (dot(zenith_dir, self.direction)/mag(zenith_dir)*mag(self.direction))
        scaled_area = self.area * cos_diverge_angle**2
        force = pressure * scaled_area # N
        accel = force/self.mass
        accel *= (1 - self.occultation)

        return vector_scale(self.direction, accel)
        
    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        output = "Body: " + self.body.get_name() + "\n"
        
        if not type(self.direction_input) == list:
            if self.direction_input[-8:] == "_dynamic":
                output += "Orientation: " + self.direction_input[0:-8] + " (dynamic) rel to " + self.orientation_frame.get_name()
            else:
                output += "Orientation: " + self.direction_input[-8:] + " rel to " + self.orientation_frame.get_name()
        else:
            output += "Orientation: " + str(self.direction) + " rel to global frame"
            
        output += "\nIlluminated Area: " + str(self.area) + " m2\n"
        output += "Vessel Mass: " + str(self.mass) + " kg\n"
        output += "Vessel Mass Auto-Update?: " + str(self.mass_auto_update) + "\n"
        output += "Illumination Source Occultation: " + str(self.occultation * 100) + "%\n"

        return output
