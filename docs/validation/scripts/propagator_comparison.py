import matplotlib.pyplot as plt

# -- INPUTS --
alt_start = 200e3 # satellite initial altitude in meters
vel_start = 10.8e3 # satellite initial tangential velocity in meters per second
dt = 240 # time step length in seconds
time_end = 60 * 60 * 24 * 30 # total propagation time in seconds

show_fwd_euler = False
show_sym_euler = True
show_verlet = True
show_Yoshida4 = True
show_Yoshida8 = True
# -- -- -- -- --

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, val):
        return vec2(self.x * val, self.y * val)

    def __truediv__(self, val):
        return vec2(self.x / val, self.y / val)

    def mag(self):
        return (self.x**2 + self.y**2)**0.5

    def normalized(self):
        return vec2(self.x / self.mag(), self.y / self.mag())

G = 6.67408e-11
M = 5.972e24
MU = G * M
R_Earth = 6371e3

pos1 = vec2(R_Earth + alt_start, 0)
vel1 = vec2(0, vel_start)

pos2 = vec2(R_Earth + alt_start, 0)
vel2 = vec2(0, vel_start)

pos3 = vec2(R_Earth + alt_start, 0)
vel3 = vec2(0, vel_start)

pos4 = vec2(R_Earth + alt_start, 0)
vel4 = vec2(0, vel_start)

pos5 = vec2(R_Earth + alt_start, 0)
vel5 = vec2(0, vel_start)

def accel(pos):
    r = pos.mag()
    a_dir = (pos * (-1)).normalized()

    return a_dir * MU / r**2

def ForwardEuler(pos, vel, dt):
    a = accel(pos)
    pos = pos + vel * dt
    vel = vel + a * dt

    return pos, vel

def SymplecticEuler(pos, vel, dt):
    a = accel(pos)
    vel = vel + a * dt
    pos = pos + vel * dt

    return pos, vel

def VelocityVerlet(pos, vel, dt):
    a = accel(pos)
    pos = pos + vel * dt + a * 0.5 * dt**2
    a2 = accel(pos)
    vel = vel + (a + a2) * 0.5 * dt

    return pos, vel

def Yoshida4(pos, vel, dt):
    c1 = 0.6756035959798289
    c2 = -0.17560359597982877
    c3 = -0.17560359597982877
    c4 = 0.6756035959798289
    d1 = 1.3512071919596578
    d2 = -1.7024143839193153
    d3 = 1.3512071919596578

    pos1 = pos + vel * c1 * dt
    vel1 = vel + accel(pos1) * d1 * dt
    pos2 = pos1 + vel1 * c2 * dt
    vel2 = vel1 + accel(pos2) * d2 * dt
    pos3 = pos2 + vel2 * c3 * dt
    vel3 = vel2 + accel(pos3) * d3 * dt
    pos4 = pos3 + vel3 * c4 * dt
    vel4 = vel3

    return pos4, vel4

def Yoshida8(pos, vel, dt):
    w1 = 0.311790812418427e0
    w2 = -0.155946803821447e1
    w3 = -0.167896928259640e1
    w4 = 0.166335809963315e1
    w5 = -0.106458714789183e1
    w6 = 0.136934946416871e1
    w7 = 0.629030650210433e0
    w0 = 1.65899088454396

    ds = [w7, w6, w5, w4, w3, w2, w1, w0, w1, w2, w3, w4, w5, w6, w7]

    cs = [0.3145153251052165, 0.9991900571895715, 0.15238115813844, 0.29938547587066, -0.007805591481624963,
          -1.619218660405435, -0.6238386128980216, 0.9853908484811935, 0.9853908484811935, -0.6238386128980216,
          -1.619218660405435, -0.007805591481624963, 0.29938547587066, 0.15238115813844, 0.9991900571895715,
          0.3145153251052165]

    for i in range(15):
        pos = pos + vel * cs[i] * dt
        vel = vel + accel(pos) * ds[i] * dt

    pos = pos + vel * cs[15] * dt

    return pos, vel

pos1xs = []
pos1ys = []
pos2xs = []
pos2ys = []
pos3xs = []
pos3ys = []
pos4xs = []
pos4ys = []
pos5xs = []
pos5ys = []
for i in range(int(time_end/dt)):
    pos1, vel1 = ForwardEuler(pos1, vel1, dt)
    pos2, vel2 = SymplecticEuler(pos2, vel2, dt)
    pos3, vel3 = VelocityVerlet(pos3, vel3, dt)
    pos4, vel4 = Yoshida4(pos4, vel4, dt)
    pos5, vel5 = Yoshida8(pos5, vel5, dt)

    pos1xs.append(pos1.x)
    pos1ys.append(pos1.y)

    pos2xs.append(pos2.x)
    pos2ys.append(pos2.y)

    pos3xs.append(pos3.x)
    pos3ys.append(pos3.y)

    pos4xs.append(pos4.x)
    pos4ys.append(pos4.y)

    pos5xs.append(pos5.x)
    pos5ys.append(pos5.y)

if show_fwd_euler:
    plt.plot(pos1xs, pos1ys, label="Fwd. Euler")
if show_sym_euler:
    plt.plot(pos2xs, pos2ys, label="Sym. Euler")
if show_verlet:
    plt.plot(pos3xs, pos3ys, label="Vel. Verlet")
if show_Yoshida4:
    plt.plot(pos4xs, pos4ys, label="Yoshida4")
if show_Yoshida8:
    plt.plot(pos5xs, pos5ys, label="Yoshida8")
    
ax = plt.gca()
ax.set_aspect('equal')
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.grid()
plt.legend()
plt.show()
