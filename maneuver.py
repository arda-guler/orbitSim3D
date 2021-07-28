class maneuver():
    def __init__(self, name, vessel):
        self.name = name
        self.vessel = vessel

    def get_vessel(self):
        return self.vessel

class maneuver_const_accel(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, accel, t_start, duration):
        super().__init__(name, vessel)
        self.frame_body = frame_body
        self.orientation = orientation
        self.accel = accel
        self.duration = duration
        self.t_start = t_start
        self.done = False

        self.draw_vertices = []

    def set_orientation(self):
        if not type(self.orientation) == list:
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):
        self.set_orientation()
        
        if (not self.done) and current_time >= self.t_start:
            self.vessel.update_vel([self.orientation[0] * self.accel,
                                    self.orientation[1] * self.accel,
                                    self.orientation[2] * self.accel], delta_t)

            self.draw_vertices.append([self.vessel.get_draw_pos()[0],
                                       self.vessel.get_draw_pos()[1],
                                       self.vessel.get_draw_pos()[2]])
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices

class maneuver_const_thrust(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, thrust, mass_init, mass_flow,
                 t_start, duration):
        
        super().__init__(name, vessel)
        self.frame_body = frame_body
        self.orientation = orientation
        self.thrust = thrust
        self.mass_init = mass_init
        self.mass_flow = mass_flow
        self.t_start = t_start
        self.duration = duration
        self.done = False

        self.mass = mass_init

        self.draw_vertices = []

    def set_orientation(self):
        if not type(self.orientation) == list:
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):
        self.set_orientation()

        if (not self.done) and current_time >= self.t_start:
            
            if self.mass <= 0:
                self.done = True
                return
            
            accel = self.thrust/self.mass
            self.mass -= self.mass_flow * delta_t
            
            self.vessel.update_vel([self.orientation[0] * accel,
                                    self.orientation[1] * accel,
                                    self.orientation[2] * accel], delta_t)

            self.draw_vertices.append([self.vessel.get_draw_pos()[0],
                                       self.vessel.get_draw_pos()[1],
                                       self.vessel.get_draw_pos()[2]])
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices
