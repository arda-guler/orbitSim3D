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
from math_utils import *
from maneuver import *

# DO NOT RUN FROM IDLE, RUN FROM COMMAND PROMPT/TERMINAL
# because there are system calls to clear the output
# every physics frame

# vessel args: name, model, color, pos, vel
station_a = vessel("Station-Alpha", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 0.2, 0.2], [6771000,0,0], [0,7672,0])

station_b = vessel("Station-Beta", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [1.0, 0.2, 0.5], [0,0,7000000], [7546,0,0])

station_c = vessel("Station-Gamma", pywavefront.Wavefront('data\models\ministation.obj', collect_faces=True),
                   [0.0, 1.0, 1.0], [0,7500000,0], [0,0,-7350])

# celestial body args: name, model, mass, radius, color, pos, vel
earth = body("Earth", pywavefront.Wavefront('data\models\miniearth.obj', collect_faces=True),
             5.972 * 10**24, 6371000, [0.0, 0.25, 1.0], [0,0,0], [0,0,0])

luna = body("Luna", pywavefront.Wavefront('data\models\miniluna.obj', collect_faces=True),
            7.342 * 10**22, 1737000, [0.8, 0.8, 0.8], [0, 202700000, -351086000], [966,0,0])

# constant acceleration maneuver args: vessel, frame body, direction, acceleration, start time, duration
demo_maneuver = maneuver_const_accel("mnv_demo", station_b, earth, "prograde", 0.5, 10, 50)
demo_maneuver2 = maneuver_const_accel("mnv_demo2", station_a, earth, "normal", 2, 15, 55)
demo_maneuver3 = maneuver_const_accel("mnv_demo3", station_c, earth, "radial_out", 0.5, 20, 60)

# this is for OpenGL
cam_trans = [0, 0, -5000]
cam_pos = [0,0,-5000]

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

vessels = [station_a, station_b, station_c]
bodies = [earth, luna]
objs = [earth, luna, station_a, station_b, station_c]

maneuvers = [demo_maneuver, demo_maneuver2, demo_maneuver3]

sim_time = 0

def create_maneuver_const_accel(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_accel, mnv_start,
                                mnv_duration):

    global maneuvers

    if find_maneuver_by_name(mnv_name):
        print("A maneuver with this name already exists. Please pick another name for the new maneuver.\n")
        input("Press Enter to continue...")
        return

    new_maneuver = maneuver_const_accel(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_accel,
                                        mnv_start, mnv_duration)
    maneuvers.append(new_maneuver)

def create_maneuver_const_thrust(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_thrust, mnv_mass_init,
                                 mnv_mass_flow, mnv_start, mnv_duration):

    global maneuvers

    if find_maneuver_by_name(mnv_name):
        print("A maneuver with this name already exists. Please pick another name for the new maneuver.\n")
        input("Press Enter to continue...")
        return

    new_maneuver = maneuver_const_thrust(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_thrust,
                                         mnv_mass_init, mnv_mass_flow, mnv_start, mnv_duration)

    maneuvers.append(new_maneuver)

def delete_maneuver(mnv_name):
    global maneuvers

    mnv = find_maneuver_by_name(mnv_name)

    if not mnv:
        print("Maneuver not found!")
        time.sleep(2)
        return
    
    maneuvers.remove(mnv)
    del mnv

def find_maneuver_by_name(mnv_name):
    global maneuvers

    result = None

    for m in maneuvers:
        if m.name == mnv_name:
            result = m
            break

    return result

def create_vessel(name, model_name, color, pos, vel):
    global vessels, objs

    if find_obj_by_name(name):
        print("An object with this name already exists. Please pick another name for the new vessel.\n")
        input("Press Enter to continue...")
        return

    try:
        model_path = "data\\models\\" + model_name + ".obj"
        model = pywavefront.Wavefront(model_path, collect_faces=True)
    except:
        print("Could not load model:", model_path)
        time.sleep(3)
        return

    try:
        new_vessel = vessel(name, model, color, pos, vel)
    except:
        print("Could not create vessel:", name)
        
    vessels.append(new_vessel)
    objs.append(new_vessel)

def delete_vessel(name):
    global vessels, objs
    vessel_tbd = find_obj_by_name(name)

    if not vessel_tbd:
        print("Object not found!")
        time.sleep(2)
        return
    
    vessels.remove(vessel_tbd)
    objs.remove(vessel_tbd)
    del vessel_tbd

def find_obj_by_name(name):
    global objs

    result = None

    for obj in objs:
        if obj.get_name() == name:
            result = obj
            break

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
    global vessels, bodies, cam_trans, cam_pos, objs, sim_time

    # initializing glfw
    glfw.init()

    # creating a window with 800 width and 600 height
    window = glfw.create_window(800,600,"OrbitSim3D", None, None)
    glfw.set_window_pos(window,200,200)
    glfw.make_context_current(window)
    
    gluPerspective(70, 800/600, 0.05, 5000000.0)
    glEnable(GL_CULL_FACE)

    # put "camera" in starting position
    glTranslate(cam_trans[0], cam_trans[1], cam_trans[2])

    delta_t = 1
    cycle_time = 0.1
    output_buffer = []

    cam_strafe_speed = 100
    show_trajectories = True

    while True:

        sim_time += delta_t

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
                    if find_obj_by_name(command[1]):
                        obj = find_obj_by_name(command[1])
                        if command[2] == "pos":
                            output_buffer.append([command[4], "pos_rel", obj, command[3]])
                        elif command[2] == "vel":
                            output_buffer.append([command[4], "vel_rel", obj, command[3]])
                    else:
                        print("Object not found.")
                        time.sleep(2)
                            
                elif len(command) == 4:
                    
                    if find_obj_by_name(command[1]):
                        obj = find_obj_by_name(command[1])
                        if command[2] == "pos":
                            output_buffer.append([command[3], "pos", obj])
                        elif command[2] == "vel":
                            output_buffer.append([command[3], "vel", obj])
                            
                    elif find_maneuver_by_name(command[1]):
                        maneuver = find_maneuver_by_name(command[1])
                        if command[2] == "active":
                            output_buffer.append([command[3], "active", maneuver])
                            
                    else:
                        print("Object/maneuver not found.")
                        time.sleep(2)

                elif len(command) == 2:
                    if command[1] == "traj":
                        show_trajectories = True

                else:
                    print("Wrong number of arguments for command 'show'.")
                    time.sleep(2)

            # HIDE command
            elif command[0] == "hide":
                if command[1] == "traj":
                    show_trajectories = False
                else:
                    for i in range(len(output_buffer)):
                        if output_buffer[i][0] == command[1]:
                            output_buffer.remove(output_buffer[i])
                            break

            # CLEAR command
            elif command[0] == "clear":
                output_buffer = []

            # CREATE_VESSEL command
            elif command[0] == "create_vessel":
                if len(command) == 6:
                    create_vessel(command[1], command[2],
                                  
                                  [float(command[3][1:-1].split(",")[0]),
                                   float(command[3][1:-1].split(",")[1]),
                                   float(command[3][1:-1].split(",")[2])],

                                  [float(command[4][1:-1].split(",")[0]),
                                   float(command[4][1:-1].split(",")[1]),
                                   float(command[4][1:-1].split(",")[2])],
                                  
                                  [float(command[5][1:-1].split(",")[0]),
                                   float(command[5][1:-1].split(",")[1]),
                                   float(command[5][1:-1].split(",")[2])])

                elif len(command) == 7:
                    # TO DO - SPHERICAL VELOCITY INPUT
                    parent_pos = find_obj_by_name(command[4]).get_pos()
                    
                    vessel_offset_from_parent = spherical2cartesian([float(command[5][1:-1].split(",")[0]),
                                                                     float(command[5][1:-1].split(",")[1]),
                                                                     float(command[5][1:-1].split(",")[2])])
                    
                    create_vessel(command[1], command[2],
                                  
                                  [float(command[3][1:-1].split(",")[0]),
                                   float(command[3][1:-1].split(",")[1]),
                                   float(command[3][1:-1].split(",")[2])],

                                  [parent_pos[0] + vessel_offset_from_parent[0],
                                   parent_pos[1] + vessel_offset_from_parent[1],
                                   parent_pos[2] + vessel_offset_from_parent[2]],

                                  [float(command[6][1:-1].split(",")[0]),
                                   float(command[6][1:-1].split(",")[1]),
                                   float(command[6][1:-1].split(",")[2])])
                else:
                    print("Wrong number of arguments for command 'create_vessel'.\n")
                    time.sleep(2)

            # DELETE_VESSEL command
            elif command[0] == "delete_vessel":
                if len(command) == 2:
                    delete_vessel(command[1])
                else:
                    print("Wrong number of arguments for command 'delete_vessel'.\n")
                    time.sleep(2)

            # CREATE_MANEUVER command
            elif command[0] == "create_maneuver":
                if command[2] == "const_accel" and len(command) == 9:
                    # name, type, vessel, frame, orientation, accel, start, duration
                    if (not command[5] == "prograde" and not command[5] == "retrograde" and
                        not command[5] == "radial_in" and not command[5] == "radial_out" and
                        not command[5] == "normal" and not command[5] == "antinormal"):
                        create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                        
                                                    [float(command[5][1:-1].split(",")[0]),
                                                    float(command[5][1:-1].split(",")[1]),
                                                    float(command[5][1:-1].split(",")[2])],
                                        
                                                    float(command[6]), float(command[7]), float(command[8]))
                    else:
                        create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                        
                                                    command[5],
                                        
                                                    float(command[6]), float(command[7]), float(command[8]))
                elif command[2] == "const_thrust" and len(command) == 11:
                    # name, type, vessel, frame, orientation, thrust, mass_init, mass_flow, start, duration
                    if (not command[5] == "prograde" and not command[5] == "retrograde" and
                        not command[5] == "radial_in" and not command[5] == "radial_out" and
                        not command[5] == "normal" and not command[5] == "antinormal"):
                        create_maneuver_const_thrust(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),

                                                     [float(command[5][1:-1].split(",")[0]),
                                                     float(command[5][1:-1].split(",")[1]),
                                                     float(command[5][1:-1].split(",")[2])],

                                                     float(command[6]), float(command[7]), float(command[8]),
                                                     float(command[9]), float(command[10]))
                    else:
                        create_maneuver_const_thrust(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),

                                                     command[5],

                                                     float(command[6]), float(command[7]), float(command[8]),
                                                     float(command[9]), float(command[10]))
                else:
                    print("Wrong syntax for command 'create_maneuver'.\n")
                    time.sleep(2)

            # DELETE_MANEUVER command
            elif command[0] == "delete_maneuver":
                if len(command) == 2:
                    delete_maneuver(command[1])
                else:
                    print("Wrong number of arguments for command 'delete_maneuver'.\n")
                    time.sleep(2)

            # GET_OBJECTS command
            elif command[0] == "get_objects":
                print("Objects currently in simulation:\n")
                for b in bodies:
                    print("BODY:", b.get_name() + "\n")
                for v in vessels:
                    print("VESSEL:", v.get_name() + "\n")
                input("Press Enter to continue...")

            # GET_MANEUVERS command
            elif command[0] == "get_maneuvers":
                print("\nManeuvers currently in the simulation:\n")
                for m in maneuvers:
                    print("MANEUVER:", m.get_name(), "\nIs Performing?:", str(m.is_performing(sim_time)), "\n\n")
                input("Press Enter to continue...")

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
                    print("\nAvailable commands: help, show, hide, clear, cam_strafe_speed, delta_t, cycle_time,")
                    print("create_vessel, delete_vessel, get_objects, create_maneuver, delete_maneuver, get_maneuvers\n")
                    print("Simulation is paused while typing a command.\n")
                    print("Type help <command> to learn more about a certain command.\n")
                    input("Press Enter to continue...")
                elif len(command) == 2:
                    if command[1] == "show":
                        print("\n'show' command adds an output element to the command prompt/terminal.\n")
                        print("Syntax Option 1: show <object_name> <attribute> <display_label>\n")
                        print("Syntax Option 2: show <object_name> <relative_attribute> <frame_of_reference_name> <display_label>\n")
                        print("Syntax Option 3: show <maneuver_name> active <display_label>\n")
                        print("Syntax Option 4: show traj (enables trajectory trails)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "hide":
                        print("\n'hide' command removes an output element from the command prompt/terminal.\n")
                        print("Syntax Option 1: hide <display_label>\n")
                        print("Syntax Option 2: hide traj (disables trajectory trails)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "clear":
                        print("\n'clear' command removes all output element from the command prompt/terminal.\n")
                        print("Syntax: clear\n")
                        input("Press Enter to continue...")
                    elif command[1] == "create_vessel":
                        print("\n'create_vessel' command adds a new space vessel to the simulation.\n")
                        print("Syntax Option 1: create_vessel <name> <model_name> <color> <position> <velocity>\n")
                        print("Syntax Option 2: create_vessel <name> <model_name> <color> <frame_of_reference_name> <position(spherical)> <velocity>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_vessel":
                        print("\n'delete_vessel' command removes a space vessel from the simulation.\n")
                        print("Syntax: delete_vessel <name>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "create_maneuver":
                        print("\n'create_maneuver' command adds a new maneuver to be performed by a space vessel.\n")
                        print("Syntax: create_maneuver <name> <type> + <<type-specific arguments>>")
                        print("Maneuver types: const_accel, const_thrust")
                        print("const_accel params: <vessel> <frame_of_reference> <orientation> <acceleration> <start_time> <duration>")
                        print("const_thrust params: <vessel> <frame_of_reference> <orientation> <thrust> <initial_mass> <mass_flow> <start_time> <duration>")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_maneuver":
                        print("\n'delete_maneuver' command removes a maneuver from the simulation.\n")
                        print("Syntax: delete_maneuver <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "get_objects":
                        print("\n'get_objects' command prints out the names of objects currently in simulation.\n")
                        print("Syntax: get_objects\n")
                        input("Press Enter to continue...")
                    elif command[1] == "get_maneuvers":
                        print("\n'get_maneuvers' command prints out the names of maneuvers currently in the simulation.\n")
                        print("Syntax: get_maneuvers\n")
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

        for m in maneuvers:
            m.perform_maneuver(sim_time, delta_t)

        # update output
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        # display what the user wants in cmd/terminal
        print("OrbitSim3D Command Interpreter & Output Display\n")
        print("Press C at any time to enter a command.\n")
        print("Time:", sim_time, "\n")
        for element in output_buffer:

            if element[1] == "pos_rel":
                print(element[0], element[2].get_pos_rel_to(find_obj_by_name(element[3])))
            elif element[1] == "vel_rel":
                print(element[0], element[2].get_vel_rel_to(find_obj_by_name(element[3])))
            elif element[1] == "pos":
                print(element[0], element[2].get_pos())
            elif element[1] == "vel":
                print(element[0], element[2].get_vel())
                
            elif element[1] == "active":
                print(element[0], element[2].is_performing(sim_time))
            
            print("\n")
            
        # clear stuff from last frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # do the actual drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        drawOrigin()
        drawBodies(bodies)
        drawVessels(vessels)

        if show_trajectories:
            drawTrajectories(vessels)
            drawManeuvers(maneuvers)

        glfw.swap_buffers(window)

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < cycle_time:
            time.sleep(cycle_time - cycle_dt)
        elif cycle_time*2 <= cycle_dt:
            print("Cycle time too low! Machine can't update physics at the given cycle time!\n")
            print("Consider increasing cycle_time to get more consistent calculation rate.\n")

main()

