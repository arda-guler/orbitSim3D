from math_utils import *

class atmospheric_drag:
    def __init__(self, name, vessel, body, area, drag_coeff, mass, mass_auto_update):
        self.name = name
        self.vessel = vessel
        self.body = body
        self.area = area
        self.drag_coeff = drag_coeff
        self.mass = mass
        self.mass_auto_update = mass_auto_update

    def get_name(self):
        return self.name

    def get_vessel(self):
        return self.vessel

    def get_body(self):
        return self.body

    def get_area(self):
        return self.area

    def get_drag_coeff(self):
        return self.drag_coeff

    def get_mass(self):
        return self.mass

    def set_mass(self, m):
        self.mass = m

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
        atmo_density = self.body.get_atmospheric_density_at_alt(self.vessel.get_alt_above(self.body))

        if not atmo_density:
            return [0,0,0]
        
        accel_dir = self.vessel.get_orientation_rel_to(self.body, "retrograde") # this "retrograde" obviously assumes the atmosphere is more or less static rel to frame
        accel_mag = 0.5 * atmo_density * self.drag_coeff * self.area * self.vessel.get_vel_mag_rel_to(self.body)**2 / self.mass
        return vector_scale(accel_dir, accel_mag)

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        output += "Body: " + self.body.get_name() + "\n"
        output += "Drag Area: " + str(self.area) + " m2\n"
        output += "Drag Coeff: " + str(self.drag_coeff) + " m2\n"
        output += "Current Atmo. Density: " + str(self.body.get_atmospheric_density_at_alt(self.vessel.get_alt_above(self.body))) + "kg m-3\n"
        output += "Vessel Mass: " + str(self.mass) + " kg\n"
        output += "Vessel Mass Auto-Update?: " + str(self.mass_auto_update)

        return output
