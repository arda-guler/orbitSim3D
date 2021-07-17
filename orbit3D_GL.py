import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import os
import keyboard
import glfw
import time

# DO NOT RUN FROM IDLE, RUN FROM COMMAND PROMPT/TERMINAL
# because there are system calls to clear the output
# every physics frame

grav_const = (6.674*(10**-11)) # m^3 kg^-1 s^-2
Earth_mass = 5.972 * 10**24 # kg

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

class body():
    def __init__(self, name, model, mass, radius, color, pos, vel):
        self.name = name
        self.model = model
        self.mass = mass
        self.radius = radius
        self.color = color
        self.pos = pos
        self.vel = vel
        self.traj_history = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.pos

    def get_pos_rel_to(self, obj):
        return [self.pos[0] - obj.pos[0],
                self.pos[1] - obj.pos[1],
                self.pos[2] - obj.pos[2]]

    def set_pos(self, pos):
        self.pos = pos

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

    def update_draw_pos(self):
        self.draw_pos = [self.pos[0]*(3*(10**(-4))),
                         self.pos[1]*(3*(10**(-4))),
                         self.pos[2]*(3*(10**(-4)))]

    def get_draw_pos(self):
        return self.draw_pos

# vessel args: name, model, color, pos, vel
station_a = vessel("Station Alpha", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 1.0, 1.0], [6771000,0,0], [0,7672,0])

station_b = vessel("Station Beta", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 0.2, 0.2], [0,0,7000000], [7546,0,0])

# celestial body args: name, model, mass, radius, color, pos, vel
earth = body("Earth", pywavefront.Wavefront('data\models\miniearth.obj', collect_faces=True),
             5.972 * 10**24, 6371000, [0.0, 0.25, 1.0], [0,0,0], [0,0,0])

luna = body("Luna", pywavefront.Wavefront('data\models\miniluna.obj', collect_faces=True),
            7.342 * 10**22, 1737000, [0.8, 0.8, 0.8], [0, 202700000, -351086000], [966,0,0])

# this is for OpenGL
cam_trans = [0, 0, -5000]
cam_pos = [0,0,-5000]

# get user input?
custom_input = False

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

if input("Custom Input?: ") == "y":
    custom_input = True

if custom_input:
    station_a.set_pos(list(input("station_a Position [X,Y,Z]: ")))
    station_a.set_vel(list(input("station_a Velocity [X,Y,Z]: ")))

    station_b.set_pos(list(input("station_b Position [X,Y,Z]: ")))
    station_b.set_vel(list(input("station_b Velocity [X,Y,Z]: ")))

vessels = [station_a, station_b]
bodies = [earth, luna]

def drawBodies():
    global bodies

    for b in bodies:
        glColor(b.get_color()[0], b.get_color()[1], b.get_color()[2])

        b.update_draw_pos()
        
        glPushMatrix()

        glTranslatef(b.get_draw_pos()[0], b.get_draw_pos()[1], b.get_draw_pos()[2])

        # no rotation yet
        #glRotate(0, 1, 0, 0)
        #glRotate(0, 0, 1, 0)
        #glRotate(0, 0, 0, 1)

        for mesh in b.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*b.model.vertices[vertex_i])
            glEnd()

        glPopMatrix()

def drawVessels():
    global vessels

    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        v.update_draw_pos()

        # here we go
        glPushMatrix()

        # put us in correct position
        glTranslatef(v.get_draw_pos()[0], v.get_draw_pos()[1], v.get_draw_pos()[2])

        # (we don't rotate things yet)
        #glRotate(vessel_rot[0], 1, 0, 0)
        #glRotate(vessel_rot[1], 0, 1, 0)
        #glRotate(vessel_rot[2], 0, 0, 1)

        # actually render model now, with triangles
        for mesh in v.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*v.model.vertices[vertex_i])
            glEnd()

        # now get out
        glPopMatrix()

def drawTrajectories():
    global vessels, cam_pos

    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        vertices = v.get_traj_history()

        if len(vertices) > 3:
            for i in range(1, len(vertices)):
                glBegin(GL_LINES)
                glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
                glEnd()

def main():
    global vessels, cam_trans, cam_pos

    # initializing glfw
    glfw.init()

    # creating a window with 800 width and 600 height
    window = glfw.create_window(800,600,"OrbitSim3D", None, None)
    glfw.set_window_pos(window,200,200)
    glfw.make_context_current(window)
    
    gluPerspective(90, 800/600, 0.05, 5000000.0)
    glEnable(GL_CULL_FACE)

    delta_t = 10

    # put "camera" in starting position
    glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

    while True:

        glfw.poll_events()

        # set to 0 so the "camera" doesn't fly off
        cam_trans = [0,0,0]
        cam_strafe_speed = 100

        # get input and move the "camera" around
        if keyboard.is_pressed("a"):
            glRotate(1,0,1,0)
        if keyboard.is_pressed("d"):
            glRotate(-1,0,1,0)
        if keyboard.is_pressed("w"):
            glRotate(1,1,0,0)
        if keyboard.is_pressed("s"):
            glRotate(-1,1,0,0)
        if keyboard.is_pressed("q"):
            glRotate(1,0,0,1)
        if keyboard.is_pressed("e"):
            glRotate(-1,0,0,1)

        if keyboard.is_pressed("i"):
            cam_trans[2] = cam_strafe_speed
            cam_pos[2] += cam_strafe_speed
        if keyboard.is_pressed("k"):
            cam_trans[2] = -cam_strafe_speed
            cam_pos[2] -= cam_strafe_speed
        if keyboard.is_pressed("j"):
            cam_trans[0] = cam_strafe_speed
            cam_pos[0] += cam_strafe_speed
        if keyboard.is_pressed("l"):
            cam_trans[0] = -cam_strafe_speed
            cam_pos[0] -= cam_strafe_speed
        if keyboard.is_pressed("o"):
            cam_trans[1] = cam_strafe_speed
            cam_pos[1] += cam_strafe_speed
        if keyboard.is_pressed("u"):
            cam_trans[1] = -cam_strafe_speed
            cam_pos[1] -= cam_strafe_speed

        glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

        # update physics
        for v in vessels:
            accel = [0,0,0]
            for b in bodies:
                accel[0] += v.get_gravity_by(b)[0]
                accel[1] += v.get_gravity_by(b)[1]
                accel[2] += v.get_gravity_by(b)[2]

            v.update_vel(accel, delta_t)
            v.update_pos(delta_t)
            v.update_traj_history()

        for x in bodies:
            accel = [0,0,0]
            for y in bodies:
                if not x == y: # don't attempt to apply gravity to self
                    accel[0] += x.get_gravity_by(y)[0]
                    accel[1] += x.get_gravity_by(y)[1]
                    accel[2] += x.get_gravity_by(y)[2]

            x.update_vel(accel, delta_t)
            x.update_pos(delta_t)

        # update output
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
            
        for v in vessels:
            print("Name:", v.get_name())
            print("Alt:", v.get_alt_above(earth))
            print("Vel:", v.get_vel_mag_rel_to(earth))
            print("\n")

        # clear stuff from last frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # do the actual drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        drawBodies()
        drawVessels()
        # drawTrajectories()

        glfw.swap_buffers(window)
        time.sleep(0.01)

main()

