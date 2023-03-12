import math
from vector3 import *

class maneuver():
    def __init__(self, name, vessel, mnv_type):
        self.name = name
        self.vessel = vessel
        self.type = mnv_type

    def get_vessel(self):
        return self.vessel

    def get_type(self):
        return self.type

class maneuver_impulsive(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, delta_v, t_perform):
        super().__init__(name, vessel, "impulsive")
        self.frame_body = frame_body
        self.orientation = orientation
        self.orientation_input = orientation
        self.delta_v = delta_v
        self.t_perform = t_perform
        self.done = False

        self.draw_point = None

    def set_orientation(self):
        if not type(self.orientation) == type(vec3()):
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):
        if (not self.done) and current_time >= self.t_perform:
            self.set_orientation()
            self.vessel.set_vel(self.vessel.get_vel() + self.orientation * self.delta_v)
            self.done = True
            self.draw_point = self.vessel.get_draw_pos()

    # Ok, here is a hack. Since this is an instantaneous maneuver, we don't deal with accelerations.
    # So we let this function update the velocity and return a null acceleration so the solver doesn't
    # apply anything (because this function already does what needs to be done).
    def get_accel(self, current_time, delta_t):
        if (not self.done) and current_time >= self.t_perform:
            self.set_orientation()
            self.vessel.set_vel(self.vessel.get_vel() + self.orientation * self.delta_v)
            self.done = True
            self.draw_point = self.vessel.get_draw_pos()

        return vec3(0, 0, 0)

    def is_performing(self, current_time):
        return False

    def get_state(self, current_time):
        if self.done:
            return "Completed"
        else:
            return "Pending"

    def get_duration(self):
        return 0

    def get_name(self):
        return self.name

    def get_draw_point(self):
        return self.draw_point

    def clear_draw_vertices(self):
        self.draw_point = None

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        
        if type(self.orientation_input) == str:
            output += "Orientation: " + self.orientation_input + " rel to " + self.frame_body.get_name()
        else:
            output += "Orientation: " + str(self.orientation) + " rel to global frame"
            
        output += "\nDv: " + str(self.delta_v) + " m/s\n"
        output += "Perform Time: " + str(self.t_perform) + " s\n"

        return output

class maneuver_const_accel(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, accel, t_start, duration):
        super().__init__(name, vessel, "const_accel")
        self.frame_body = frame_body
        self.orientation = orientation
        self.orientation_input = orientation
        self.accel = accel
        self.duration = duration
        self.t_start = t_start
        self.done = False

        self.draw_vertices = []

    def set_orientation(self):
        if not type(self.orientation) == type(vec3()) or (type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic"):
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):
        
        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()

            self.vessel.update_vel(self.orientation * self.accel, delta_t)

            self.draw_vertices.append(self.vessel.get_draw_pos())

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    # basically identical to perform_maneuver but doesn't auto-update the vessel, instead returns the acceleration vector
    def get_accel(self, current_time, delta_t):
        accel_vec = vec3(0, 0, 0)

        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()

            accel_vec = self.orientation * self.accel

            self.draw_vertices.append(self.vessel.get_draw_pos())

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input

        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

        return accel_vec

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_state(self, current_time):
        if self.done:
            return "Completed"
        elif current_time >= self.t_start:
            return "Performing"
        else:
            return "Pending"

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices

    def clear_draw_vertices(self):
        self.draw_vertices = []

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        
        if not type(self.orientation_input) == type(vec3()):
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                output += "Orientation: " + self.orientation_input[0:-8] + " (dynamic) rel to " + self.frame_body.get_name()
            else:
                output += "Orientation: " + self.orientation_input[-8:] + " rel to " + self.frame_body.get_name()
        else:
            output += "Orientation: " + str(self.orientation) + " rel to global frame"
            
        output += "\nAcceleration: " + str(self.accel) + " m/s^2\n"
        output += "Start time: " + str(self.t_start) + " s\n"
        output += "Duration: " + str(self.duration) + " s\n"
        output += "Dv: " + str(self.duration * self.accel) + " m/s\n"

        return output
    
    def get_duration(self):
        return self.duration

class maneuver_const_thrust(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, thrust, mass_init, mass_flow,
                 t_start, duration):
        
        super().__init__(name, vessel, "const_thrust")
        self.frame_body = frame_body
        self.orientation = orientation
        self.orientation_input = orientation
        self.thrust = thrust
        self.mass_init = mass_init
        self.mass_flow = mass_flow
        self.t_start = t_start
        self.duration = duration
        self.done = False

        self.mass = mass_init

        self.draw_vertices = []

        # calculate Delta-v
        v_exhaust = self.thrust/self.mass_flow
        m_final = self.mass_init - self.duration * self.mass_flow
        self.Dv = v_exhaust * math.log(self.mass_init/m_final)

    def set_orientation(self):
        if not type(self.orientation) == type(vec3()) or (type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic"):
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):

        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()
            
            if self.mass <= 0:
                self.done = True
                return
            
            accel = self.thrust/self.mass
            self.mass -= self.mass_flow * delta_t

            self.vessel.update_vel(self.orientation * accel, delta_t)

            self.draw_vertices.append(self.vessel.get_draw_pos())

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    # basically identical to perform_maneuver but doesn't auto-update the vessel, instead returns the acceleration vector
    def get_accel(self, current_time, delta_t):
        accel_vec = vec3(0, 0, 0)

        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()

            if self.mass <= 0:
                self.done = True
                return

            accel = self.thrust / self.mass
            self.mass -= self.mass_flow * delta_t

            accel_vec = self.orientation * accel
            self.draw_vertices.append(self.vessel.get_draw_pos())

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input

        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

        return accel_vec

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_state(self, current_time):
        if self.done:
            return "Completed"
        elif current_time >= self.t_start:
            return "Performing"
        else:
            return "Pending"

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices

    def clear_draw_vertices(self):
        self.draw_vertices = []

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        
        if not type(self.orientation_input) == type(vec3()):
            if type(self.orientation_input) == str and self.orientation_input[-8:] == "_dynamic":
                output += "Orientation: " + self.orientation_input[0:-8] + " (dynamic) rel to " + self.frame_body.get_name()
            else:
                output += "Orientation: " + self.orientation_input[-8:] + " rel to " + self.frame_body.get_name()
        else:
            output += "Orientation: " + str(self.orientation) + " rel to global frame"
            
        output += "\nThrust: " + str(self.thrust) + " N\n"
        output += "Initial mass:" + str(self.mass_init) + " kg\n"
        output += "Mass flow: " + str(self.mass_flow) + " kg/s\n"
        output += "Start time: " + str(self.t_start) + " s\n"
        output += "Duration: " + str(self.duration) + " s\n"
        output += "Dv: " + str(round(self.Dv, 3)) + " m/s\n"

        return output

    def get_duration(self):
        return self.duration
