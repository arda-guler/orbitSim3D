import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import os
import keyboard
import glfw
import time

from graphics import *
from vessel_class import *
from body_class import *

# DO NOT RUN FROM IDLE, RUN FROM COMMAND PROMPT/TERMINAL
# because there are system calls to clear the output
# every physics frame

# vessel args: name, model, color, pos, vel
station_a = vessel("Station-Alpha", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 1.0, 1.0], [6771000,0,0], [0,7672,0])

station_b = vessel("Station-Beta", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
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
objs = [earth, luna, station_a, station_b]

def find_obj_by_name(name):
    global objs

    result = None

    for obj in objs:
        if obj.get_name() == name:
            result = obj

    return result

# clear all keyboard buffer
# e.g. don't keep camera movement keys
# in buffer as we try to enter a command
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def main():
    global vessels, bodies, cam_trans, cam_pos, objs

    # initializing glfw
    glfw.init()

    # creating a window with 800 width and 600 height
    window = glfw.create_window(800,600,"OrbitSim3D", None, None)
    glfw.set_window_pos(window,200,200)
    glfw.make_context_current(window)
    
    gluPerspective(90, 800/600, 0.05, 5000000.0)
    glEnable(GL_CULL_FACE)

    # put "camera" in starting position
    glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

    delta_t = 1
    cycle_time = 0.01
    output_buffer = []

    cam_strafe_speed = 100

    while True:

        glfw.poll_events()

        # set to 0 so the "camera" doesn't fly off
        cam_trans = [0,0,0]

        frame_command = False

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

        if keyboard.is_pressed("c"):
            frame_command = True

        if frame_command:
            flush_input()
            command = input("\n > ")
            command = command.split(" ")

            # --- COMMAND INTERPRETER ---
            
            # SHOW command
            if command[0] == "show":
                
                if len(command) == 5:
                    if not find_obj_by_name(command[1]) == None:
                        obj = find_obj_by_name(command[1])
                        if command[2] == "pos":
                            output_buffer.append([command[4], "pos_rel", obj, command[3]])
                        elif command[2] == "vel":
                            output_buffer.append([command[4], "vel_rel", obj, command[3]])
                    else:
                        print("Object not found.")
                        time.sleep(2)
                            
                elif len(command) == 4:
                    if not find_obj_by_name(command[1]) == None:
                        obj = find_obj_by_name(command[1])
                        if command[2] == "pos":
                            output_buffer.append([command[3], "pos", obj])
                        elif command[2] == "vel":
                            output_buffer.append([command[3], "vel", obj])
                    else:
                        print("Object not found.")
                        time.sleep(2)

                else:
                    print("Wrong number of arguments for command 'show'.")
                    time.sleep(2)

            # HIDE command
            elif command[0] == "hide":
                for i in range(len(output_buffer)):
                    if output_buffer[i][0] == command[1]:
                        output_buffer.remove(output_buffer[i])
                        break

            # CLEAR command
            elif command[0] == "clear":
                output_buffer = []

            # CAM_STRAFE_SPEED command
            elif command[0] == "cam_strafe_speed":
                cam_strafe_speed = float(command[1])

            # DELTA_T command
            elif command[0] == "delta_t":
                delta_t = float(command[1])

            # CYCLE_TIME command
            elif command[0] == "cycle_time":
                cycle_time = float(command[1])

            # HELP command
            elif command[0] == "help":
                if len(command) == 1:
                    print("\nAvailable commands: help, show, hide, clear, cam_strafe_speed, delta_t, cycle_time\n")
                    print("Simulation is paused while typing a command.\n")
                    print("Type help <command> to learn more about a certain command.\n")
                    input("Press Enter to continue...")
                elif len(command) == 2:
                    if command[1] == "show":
                        print("\n'show' command adds an output element to the command prompt/terminal.\n")
                        print("Syntax Option 1: show <object_name> <attribute> <display_label>\n")
                        print("Syntax Option 2: show <object_name> <relative_attribute> <frame_of_reference_name> <display_label>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "hide":
                        print("\n'hide' command removes an output element from the command prompt/terminal.\n")
                        print("Syntax: hide <display_label>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "clear":
                        print("\n'clear' command removes all output element from the command prompt/terminal.\n")
                        print("Syntax: clear\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cam_strafe_speed":
                        print("\n'cam_strafe_speed' command sets the speed of linear camera movement.\n")
                        print("Syntax: cam_strafe_speed <speed>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "delta_t":
                        print("\n'delta_t' command sets time steps of each physics frame.\n")
                        print("Syntax: delta_t <seconds>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cycle_time":
                        print("\n'cycle_time' command sets the amount of time the machine should take to calculate each physics frame.\n")
                        print("Syntax: cycle_time <seconds>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "help":
                        print("\n'help' command prints out the help text.\n")
                        print("Syntax: help\n")
                        input("Press Enter to continue...")
                    else:
                        print("\nUnknown command.")
                        input("Press Enter to continue...")

            else:
                print("\nUnrecognized command.")
                input("Press Enter to continue...")

        cycle_start = time.perf_counter()

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
            v.update_draw_traj_history()

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

        # display what the user wants in cmd/terminal
        print("OrbitSim3D Command Interpreter & Output Display\n")
        print("Press C at any time to enter a command.\n")
        for element in output_buffer:

            if element[1] == "pos_rel":
                print(element[0], element[2].get_pos_rel_to(find_obj_by_name(element[3])))
            elif element[1] == "vel_rel":
                print(element[0], element[2].get_vel_rel_to(find_obj_by_name(element[3])))
            elif element[1] == "pos":
                print(element[0], element[2].get_pos())
            elif element[1] == "vel":
                print(element[0], element[2].get_vel())
            
            print("\n")
            
        # clear stuff from last frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # do the actual drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        drawOrigin()
        drawBodies(bodies)
        drawVessels(vessels)
        drawTrajectories(vessels)

        glfw.swap_buffers(window)

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < cycle_time:
            time.sleep(cycle_time - cycle_dt)
        elif cycle_time*2 <= cycle_dt:
            print("Cycle time too low! Machine can't update physics at the given cycle time!\n")
            print("Consider increasing cycle_time to get more consistent calculation rate.\n")

main()

