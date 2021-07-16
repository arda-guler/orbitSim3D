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

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_vel(self):
        return self.vel

    def get_vel_mag(self):
        return (self.vel[0] ** 2 + self.vel[1] ** 2 + self.vel[2] ** 2) ** 0.5

    def set_vel(self, vel):
        self.vel = vel

    def get_alt_R(self):
        return (self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2)**0.5

    # drawing scene is scaled down by a factor of 3x10^-4
    def update_draw_pos(self):
        self.draw_pos = [self.pos[0]*(3*(10**(-4))),
                         self.pos[1]*(3*(10**(-4))),
                         self.pos[2]*(3*(10**(-4)))]

    # unit vector that points towards the planet from the
    # position of the spacecraft
    def get_vessel_planet_unit_vector(self):
        return [-self.pos[0]/(self.get_alt_R()), -self.pos[1]/(self.get_alt_R()), -self.pos[2]/(self.get_alt_R())]

    def get_gravity(self):
        grav_mag = (grav_const * Earth_mass)/((self.get_alt_R())**2)
        grav_vec = [grav_mag * self.get_vessel_planet_unit_vector()[0],
                    grav_mag * self.get_vessel_planet_unit_vector()[1],
                    grav_mag * self.get_vessel_planet_unit_vector()[2]]
        return grav_vec

    def update_vel(self, dt):
        self.vel[0] += self.get_gravity()[0] * dt
        self.vel[1] += self.get_gravity()[1] * dt
        self.vel[2] += self.get_gravity()[2] * dt

    def update_pos(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

    def get_color(self):
        return self.color

# vessel args: name, model, color, pos, vel
station_a = vessel("Station Alpha", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 1.0, 1.0], [6771000,0,0], [0,7750,0])

station_b = vessel("Station Beta", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 0.5, 0.2], [0,6771000,0], [0,0,-7750])

# there is only Earth for now
# TO DO: Make planet class
planet = pywavefront.Wavefront('data\models\miniearth.obj', collect_faces=True)
planet_trans = [0,0,0]
planet_rot = [0,0,0]

# this is for OpenGL
cam_trans = [0, 0, -5000]

# get user input
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

def drawPlanet():
    glColor(0.0, 0.25, 1.0)
    glPushMatrix()

    glTranslatef(planet_trans[0], planet_trans[1], planet_trans[2])
    
    glRotate(planet_rot[0], 1, 0, 0)
    glRotate(planet_rot[1], 0, 1, 0)
    glRotate(planet_rot[2], 0, 0, 1)

    for mesh in planet.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*planet.vertices[vertex_i])
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
        glTranslatef(v.draw_pos[0], v.draw_pos[1], v.draw_pos[2])

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

def main():
    global vessels, cam_trans

    # initializing glfw
    glfw.init()

    # creating a window with 800 width and 600 height
    window = glfw.create_window(800,600,"OrbitSim3D", None, None)
    glfw.set_window_pos(window,200,200)
    glfw.make_context_current(window)
    
    gluPerspective(45, 800/600, 0.05, 50000.0)
    glEnable(GL_CULL_FACE)

    delta_t = 1

    # put "camera" in starting position
    glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

    while True:

        glfw.poll_events()

        # set to 0 so the "camera" doesn't fly off
        cam_trans = [0,0,0]

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
            cam_trans[2] = 10
        if keyboard.is_pressed("k"):
            cam_trans[2] = -10
        if keyboard.is_pressed("j"):
            cam_trans[0] = 10
        if keyboard.is_pressed("l"):
            cam_trans[0] = -10
        if keyboard.is_pressed("o"):
            cam_trans[1] = 10
        if keyboard.is_pressed("u"):
            cam_trans[1] = -10

        glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

        # update physics
        for v in vessels:
            v.update_vel(delta_t)
            v.update_pos(delta_t)

        # update output
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
            
        for v in vessels:
            print("Name:", v.get_name())
            print("Alt:", v.get_alt_R() - 6371000)
            print("Vel:", v.get_vel_mag())
            print("\n")

        # clear stuff from last frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # do the actual drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        drawPlanet()
        drawVessels()

        glfw.swap_buffers(window)
        time.sleep(0.01)

main()

