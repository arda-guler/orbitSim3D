grav_const = (6.674*(10**-11)) # m^3 kg^-1 s^-2

class vessel():
    def __init__(self, name, model, color, pos, vel):
        self.name = name
        self.model = model
        self.color = color
        self.pos = pos
        self.vel = vel
        self.draw_pos = [0,0,0]
        self.traj_history = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_pos_rel_to(self, obj):
        return [self.pos[0] - obj.pos[0],
                self.pos[1] - obj.pos[1],
                self.pos[2] - obj.pos[2]]

    def get_vel(self):
        return self.vel

    def get_vel_rel_to(self, obj):
        return [self.vel[0] - obj.vel[0],
                self.vel[1] - obj.vel[1],
                self.vel[2] - obj.vel[2]]

    def get_vel_mag(self):
        return (self.vel[0] ** 2 + self.vel[1] ** 2 + self.vel[2] ** 2) ** 0.5

    def get_vel_mag_rel_to(self, obj):
        return (((self.vel[0] - obj.vel[0])**2 +
                 (self.vel[1] - obj.vel[1])**2 +
                 (self.vel[2] - obj.vel[2])**2)**0.5)

    def set_vel(self, vel):
        self.vel = vel

    # dist. between centers (ignore surface)
    def get_dist_to(self, obj):
        return ((self.pos[0] - obj.pos[0])**2 +
                (self.pos[1] - obj.pos[1])**2 +
                (self.pos[2] - obj.pos[2])**2)**0.5

    # get altitude above surface
    def get_alt_above(self, body):
        return (self.get_dist_to(body) - body.get_radius())

    # drawing scene is scaled down by a factor of 3x10^-4
    def update_draw_pos(self):
        self.draw_pos = [self.pos[0]*(3*(10**(-4))),
                         self.pos[1]*(3*(10**(-4))),
                         self.pos[2]*(3*(10**(-4)))]

    def get_draw_pos(self):
        return self.draw_pos

    def get_unit_vector_towards(self, obj):
        return [((obj.pos[0] - self.pos[0])/(self.get_dist_to(obj))),
                ((obj.pos[1] - self.pos[1])/(self.get_dist_to(obj))),
                ((obj.pos[2] - self.pos[2])/(self.get_dist_to(obj)))]

    def get_gravity_by(self, body):
        grav_mag = (grav_const * body.get_mass())/((self.get_dist_to(body))**2)
        
        grav_vec = [grav_mag * self.get_unit_vector_towards(body)[0],
                    grav_mag * self.get_unit_vector_towards(body)[1],
                    grav_mag * self.get_unit_vector_towards(body)[2]]
        
        return grav_vec

    def update_vel(self, accel, dt):
        self.vel[0] += accel[0] * dt
        self.vel[1] += accel[1] * dt
        self.vel[2] += accel[2] * dt

    def update_pos(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

    def update_traj_history(self):
        self.traj_history.append(self.pos)

    def clear_traj_history(self):
        self.traj_history = []

    def get_traj_history(self):
        return self.traj_history

    def get_color(self):
        return self.color
