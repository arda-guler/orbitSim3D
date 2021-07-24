class maneuver():
    def __init__(self, name, vessel):
        self.name = name
        self.vessel = vessel

class maneuver_const_accel(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, accel, t_start, duration):
        super().__init__(name, vessel)
        self.frame_body = frame_body
        self.orientation = orientation
        self.accel = accel
        self.duration = duration
        self.t_start = t_start
        self.done = False

    def set_orientation(self):
        if self.orientation == "prograde":
            self.orientation = vessel.get_orientation_rel_to(frame_body, "prograde")
        elif self.orientation == "retrograde":
            self.orientation = vessel.get_orientation_rel_to(frame_body, "retrograde")

    def perform_maneuver(self, current_time, delta_t):
        if (not self.done) and current_time >= self.t_start:
            self.vessel.update_vel([self.orientation[0] * self.accel,
                                    self.orientation[1] * self.accel,
                                    self.orientation[2] * self.accel], delta_t)
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_name(self):
        return self.name
