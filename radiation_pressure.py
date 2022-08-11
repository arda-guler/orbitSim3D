import math

from math_utils import *
c = 299792458 # m s-1, speed of light

class radiation_pressure:
    def __init__(self, name, vessel, body, area, direction, mass, mass_auto_update):
        self.name = name
        self.vessel = vessel
        self.body = body
        self.area = area
        self.direction = direction
        self.direction_input = direction
        self.mass = mass
        self.mass_auto_update = mass_auto_update

    def set_direction(self):
        if not type(self.direction) == list or self.direction_input[-8:] == "_dynamic":
            self.direction = self.vessel.get_orientation_rel_to(self.body, self.direction_input)

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

    def check_occlusion_simple(self, bodies):
        # checks if the light from the source body is blocked by another body
        # e.g. if satellite is on the night side on Low Earth Orbit
        
        occlusion = 0 # ratio of total light blocked, initialized at 0 (no occlusion)

        v = self.vessel
        b1 = self.body
        
        v_b1 = b1.get_unit_vector_towards(v)
        v_dist = v.get_dist_to(b1)
        
        for b2 in bodies:
            if not b2 == b1:
                
                if b2.get_dist_to(b1) > v_dist:
                    # body is more distant to light source than vessel is, no occlusion
                    pass

                # vessel is more distant to source than the body, there may be blocking
                else:
                    b2_dist = b1.get_dist_to(b2)
                    b1_b2 = b1.get_unit_vector_towards(b2)

                    # get point - planet separation angle
                    cos_point_separation_angle = dot(v_b1, b1_b2)/(mag(v_b1)*mag(b1_b2))
                    point_separation_angle = math.acos(cos_point_separation_angle)

                    # get angular size of planet
                    triangle_side_a = (b2_dist**2 - b2.radius**2)**(0.5)
                    triangle_side_b = b2_dist
                    triangle_side_c = b2.radius
                    
                    b2_half_angular_size = math.atan(triangle_side_c, triangle_side_a)

                    if b2_half_angular_size < point_separation_angle:
                        # point is not occluded at all
                        pass
                    
                    else:
                        # point is in shadow of the planet, but is it in umbra, penumbra, antumbra?
                        pass

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

        return vector_scale(self.direction, accel)
        
        
