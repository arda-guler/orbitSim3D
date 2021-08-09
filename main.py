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
from kepler_orbit import *

# DO NOT RUN FROM IDLE, RUN FROM COMMAND PROMPT/TERMINAL
# because there are system calls to clear the output
# every physics frame

# this is for OpenGL
cam_trans = [0, 0, -5000]

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

vessels = []
bodies = []
objs = []
projections = []

maneuvers = []
batch_commands = []

preset_orientations = ["prograde", "prograde_dynamic", "retrograde", "retrograde_dynamic",
                           "normal", "normal_dynamic", "antinormal", "antinormal_dynamic",
                           "radial_in", "radial_in_dynamic", "radial_out", "radial_out_dynamic"]

sim_time = 0

def read_batch(batch_path):

    try:
        batch_file = open(batch_path, "r")
    except FileNotFoundError:
        try:
            batch_file = open("scenarios\\" + batch_path, "r")
        except FileNotFoundError:
            try:
                batch_file = open(batch_path + ".obf", "r")
            except FileNotFoundError:
                try:
                    batch_file = open("scenarios\\" + batch_path + ".obf", "r")
                except FileNotFoundError:
                    print("\nError reading batch file.\n")
                    time.sleep(2)
                    return [[""]]

    batch_lines = batch_file.readlines()

    commands = []

    for line in batch_lines:
        if not line[0] == ";":
            commands.append(line[0:-1].split(" "))
            
    return commands

def clear_scene():
    global objs, vessels, bodies, projections, maneuvers, sim_time

    objs = []
    vessels = []
    bodies = []
    maneuvers = []
    projections = []
    sim_time = 0

def import_scenario(scn_filename):
    global objs, vessels, bodies, maneuvers, sim_time

    clear_scene()

    try:
        scn_file = open(scn_filename, "r")
    except FileNotFoundError:
        try:
            scn_file = open("scenarios\\" + scn_filename, "r")
        except FileNotFoundError:
            try:
                scn_file = open(scn_filename + ".osf", "r")
            except FileNotFoundError:
                try:
                    scn_file = open("scenarios\\" + scn_filename + ".osf", "r")
                except FileNotFoundError:
                    print("Scenario file not found.")
                    time.sleep(2)
                    quit()
                    
    import_lines = scn_file.readlines()

    for line in import_lines:
        line = line[0:-1].split("|")

        # import bodies
        if line[0] == "B":
            line[5] = line[5][1:-1].split(",")
            line[6] = line[6][1:-1].split(",")
            line[7] = line[7][1:-1].split(",")
            new_body = body(line[1], pywavefront.Wavefront(line[2], collect_faces=True),
                            float(line[3]), float(line[4]),
                            [float(line[5][0]), float(line[5][1]), float(line[5][2])],
                            [float(line[6][0]), float(line[6][1]), float(line[6][2])],
                            [float(line[7][0]), float(line[7][1]), float(line[7][2])])
            bodies.append(new_body)
            objs.append(new_body)

        # import vessels
        elif line[0] == "V":
            line[3] = line[3][1:-1].split(",")
            line[4] = line[4][1:-1].split(",")
            line[5] = line[5][1:-1].split(",")
            new_vessel = vessel(line[1], pywavefront.Wavefront(line[2], collect_faces=True),
                                [float(line[3][0]), float(line[3][1]), float(line[3][2])],
                                [float(line[4][0]), float(line[4][1]), float(line[4][2])],
                                [float(line[5][0]), float(line[5][1]), float(line[5][2])])
            vessels.append(new_vessel)
            objs.append(new_vessel)

        # import maneuvers
        elif line[0] == "M":
            if line[2] == "const_accel":
                if (line[5] in preset_orientations):
                    new_maneuver = maneuver_const_accel(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                        line[5], float(line[6]), float(line[7]), float(line[8]))
                else:
                    line[5] = line[5][1:-1].split(",")
                    new_maneuver = maneuver_const_accel(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                        [float(line[5][0]), float(line[5][1]), float(line[5][2])],
                                                        float(line[6]), float(line[7]), float(line[8]))
                    
            elif line[2] == "const_thrust":
                if (line[5] in preset_orientations):
                    new_maneuver = maneuver_const_thrust(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                         line[5], float(line[6]), float(line[7]), float(line[8]),
                                                         float(line[9]), float(line[10]))
                else:
                    line[5] = line[5][1:-1].split(",")
                    new_maneuver = maneuver_const_thrust(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                         [float(line[5][0]), float(line[5][1]), float(line[5][2])],
                                                         float(line[6]), float(line[7]), float(line[8]),
                                                         float(line[9]), float(line[10]))

            maneuvers.append(new_maneuver)

    main()

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

def find_proj_by_name(name):
    global projections

    result = None

    for proj in projections:
        if proj.get_name() == name:
            result = proj
            break

    return result

def create_keplerian_proj(name, vessel, body):
    global projections

    if find_proj_by_name(name):
        print("A projection with this name already exists. Please pick another name for the new projection.\n")
        input("Press Enter to continue...")
        return

    new_proj = kepler_projection(name, vessel, body)
    projections.append(new_proj)

def delete_keplerian_proj(name):
    global projections
    proj_tbd = find_proj_by_name(name)

    if not proj_tbd:
        print("Projection not found!")
        time.sleep(2)
        return
    
    projections.remove(proj_tbd)
    del proj_tbd
    
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
    global vessels, bodies, projections, cam_trans, objs, sim_time, batch_commands

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
        if keyboard.is_pressed("k"):
            cam_trans[2] = -cam_strafe_speed
        if keyboard.is_pressed("j"):
            cam_trans[0] = cam_strafe_speed
        if keyboard.is_pressed("l"):
            cam_trans[0] = -cam_strafe_speed
        if keyboard.is_pressed("o"):
            cam_trans[1] = cam_strafe_speed
        if keyboard.is_pressed("u"):
            cam_trans[1] = -cam_strafe_speed

        if keyboard.is_pressed("c"):
            frame_command = True

        if frame_command or len(batch_commands) > 0:
            flush_input()

            if frame_command:
                command = input("\n > ")
                command = command.split(" ")

            # --- COMMAND INTERPRETER ---

            # BATCH command
            if command[0] == "batch":
                batch_commands = read_batch(command[1])

            if len(batch_commands) > 0 and (not frame_command or command[0] == "batch"):
                command = batch_commands[0]
                batch_commands.remove(command)
            
            # SHOW command
            if command[0] == "show":
                
                if len(command) == 5:
                    if find_obj_by_name(command[1]):
                        obj = find_obj_by_name(command[1])
                        if command[2] == "pos":
                            output_buffer.append([command[4], "pos_rel", obj, command[3]])
                        elif command[2] == "vel":
                            output_buffer.append([command[4], "vel_rel", obj, command[3]])
                        elif command[2] == "pos_mag" or command[2] == "dist":
                            output_buffer.append([command[4], "pos_mag_rel", obj, command[3]])
                        elif command[2] == "vel_mag":
                            output_buffer.append([command[4], "vel_mag_rel", obj, command[3]])
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
                        elif command[2] == "pos_mag" or command[2] == "dist":
                            output_buffer.append([command[3], "pos_mag", obj])
                        elif command[2] == "vel_mag":
                            output_buffer.append([command[3], "vel_mag", obj])
                            
                    elif find_maneuver_by_name(command[1]):
                        maneuver = find_maneuver_by_name(command[1])
                        if command[2] == "active":
                            output_buffer.append([command[3], "active", maneuver])
                        elif command[2] == "state":
                            output_buffer.append([command[3], "state", maneuver])
                        elif command[2] == "params":
                            output_buffer.append([command[3], "params", maneuver])
                            
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
                if len(command) == 2:
                    if command[1] == "output":
                        output_buffer = []
                    elif command[1] == "scene":
                        clear_scene()
                    elif command[1] == "traj_visuals":
                        for v in vessels:
                            v.clear_draw_traj_history()
                        for m in maneuvers:
                            m.clear_draw_vertices()
                else:
                    print("Wrong number of arguments for command 'clear'.")
                    time.sleep(2)

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
                if len(command) == 9 and command[2] == "const_accel":
                    # name, type, vessel, frame, orientation, accel, start, duration
                    if (not command[5] in preset_orientations):
                        create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                        
                                                    [float(command[5][1:-1].split(",")[0]),
                                                    float(command[5][1:-1].split(",")[1]),
                                                    float(command[5][1:-1].split(",")[2])],
                                        
                                                    float(command[6]), float(command[7]), float(command[8]))
                    else:
                        create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                        
                                                    command[5],
                                        
                                                    float(command[6]), float(command[7]), float(command[8]))
                elif len(command) == 11 and command[2] == "const_thrust":
                    # name, type, vessel, frame, orientation, thrust, mass_init, mass_flow, start, duration
                    if (not command[5] in preset_orientations):
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

            # CREATE_PROJECTION command
            elif command[0] == "create_projection":
                if len(command) == 4:
                    create_keplerian_proj(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]))
                else:
                    print("Wrong number of arguments for command 'create_projection'.\n")
                    time.sleep(2)

            # DELETE_PROJECTION command
            elif command[0] == "delete_projection":
                if len(command) == 2:
                    delete_keplerian_proj(command[1])
                else:
                    print("Wrong number of arguments for command 'delete_projection'.\n")
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
                    print("MANEUVER:", m.get_name(), "\nState:", str(m.get_state(sim_time)), "\n\n")
                input("Press Enter to continue...")

            # GET_PROJECTIONS command
            elif command[0] == "get_projections":
                print("\nProjections currently in the simulation:\n")
                for p in projections:
                    print("PROJECTION:", p.get_name(), "\n")
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

            # NOTE command
            elif command[0] == "note":
                new_note = ""
                for i in range(2,len(command)):
                    new_note = new_note + " " + command[i]
                output_buffer.append([command[1], "note", new_note])

            # HELP command
            elif command[0] == "help":
                if len(command) == 1:
                    print("\nAvailable commands: help, show, hide, clear, cam_strafe_speed, delta_t, cycle_time,")
                    print("create_vessel, delete_vessel, get_objects, create_maneuver, delete_maneuver, get_maneuvers,")
                    print("batch, note, create_projection, delete_projection, get_projections\n")
                    print("Simulation is paused while typing a command.\n")
                    print("Type help <command> to learn more about a certain command.\n")
                    input("Press Enter to continue...")
                elif len(command) == 2:
                    if command[1] == "show":
                        print("\n'show' command adds an output element to the command prompt/terminal.\n")
                        print("Syntax Option 1: show <object_name> <attribute> <display_label>\n")
                        print("Syntax Option 2: show <object_name> <relative_attribute> <frame_of_reference_name> <display_label>\n")
                        print("Syntax Option 3: show <maneuver_name> <(active/state/params)> <display_label>\n")
                        print("Syntax Option 4: show traj (enables trajectory trails)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "hide":
                        print("\n'hide' command removes an output element from the command prompt/terminal.\n")
                        print("Syntax Option 1: hide <display_label>\n")
                        print("Syntax Option 2: hide traj (disables trajectory trails)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "clear":
                        print("\n'clear' command removes all output element from the command prompt/terminal.\n")
                        print("Syntax: clear <thing>\n")
                        print("Things to clear: output (clears the output display buffer), scene (removes everything from the physics scene),")
                        print("traj_visuals (clears vessel trajectories up to current time in the 3D scene)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "batch":
                        print("\n'batch' command reads a batch file and queues the commands to be sent to the interpreter.\n")
                        print("Syntax: batch <file_path>\n")
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
                    elif command[1] == "create_projection":
                        print("\n'create_projection' command creates a 2-body Keplerian orbit projection of a vessel around a body.\n")
                        print("Syntax: create_projection <name> <vessel> <body>")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_projection":
                        print("\n'delete_projection' command removes a 2-body Keplerian orbit projection from the simulation.\n")
                        print("Syntax: delete_projection <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "get_objects":
                        print("\n'get_objects' command prints out the names of objects currently in simulation.\n")
                        print("Syntax: get_objects\n")
                        input("Press Enter to continue...")
                    elif command[1] == "get_maneuvers":
                        print("\n'get_maneuvers' command prints out the names of maneuvers currently in the simulation.\n")
                        print("Syntax: get_maneuvers\n")
                        input("Press Enter to continue...")
                    elif command[1] == "get_projections":
                        print("\n'get_projections' command prints out the names of Keplerian orbit projections currently in the simulation.\n")
                        print("Syntax: get_projections\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cam_strafe_speed":
                        print("\n'cam_strafe_speed' command sets the speed of linear camera movement.\n")
                        print("Syntax: cam_strafe_speed <speed>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "delta_t":
                        print("\n'delta_t' command sets time steps of each physics frame.")
                        print("Set delta_t negative to run the simulation backwards (to retrace an object's trajectory).\n")
                        print("Syntax: delta_t <seconds>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cycle_time":
                        print("\n'cycle_time' command sets the amount of time the machine should take to calculate each physics frame.\n")
                        print("Syntax: cycle_time <seconds>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "note":
                        print("\n'note' command lets the user take a note on the output screen.")
                        print("Syntax: note <note_label> <note>")
                        print("(<note> represents all words beyond <note_label>, spaces can be used while taking notes)\n")
                        input("Press Enter to continue...")
                    elif command[1] == "help":
                        print("\n'help' command prints out the help text.\n")
                        print("Syntax: help\n")
                        input("Press Enter to continue...")
                    else:
                        print("\nUnknown command.")
                        input("Press Enter to continue...")

            elif command[0] == "":
                # user probably changed their mind
                pass
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
            # lower delta_t if a maneuver is in progress
            if (delta_t > 1 and (m.get_state(sim_time) == "Performing" or
                                 (m.get_state(sim_time) == "Pending" and
                                  not m.get_state(sim_time+delta_t) == "Pending"))):
                delta_t = 1
                
            m.perform_maneuver(sim_time, delta_t)

        # update output
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        # display what the user wants in cmd/terminal
        print("OrbitSim3D Command Interpreter & Output Display\n")
        if sim_time < 30:
            print("Press C at any time to enter a command.\n")
        print("Time:", sim_time, "\n")
        for element in output_buffer:

            if element[1] == "pos_rel":
                print(element[0], element[2].get_pos_rel_to(find_obj_by_name(element[3])))
            elif element[1] == "vel_rel":
                print(element[0], element[2].get_vel_rel_to(find_obj_by_name(element[3])))

            elif element[1] == "pos_mag_rel":
                print(element[0], element[2].get_dist_to(find_obj_by_name(element[3])))
            elif element[1] == "vel_mag_rel":
                print(element[0], element[2].get_vel_mag_rel_to(find_obj_by_name(element[3])))
            
            elif element[1] == "pos":
                print(element[0], element[2].get_pos())
            elif element[1] == "vel":
                print(element[0], element[2].get_vel())

            elif element[1] == "pos_mag":
                print(element[0], float((element[2].get_pos()[0]**2 +
                                         element[2].get_pos()[1]**2 +
                                         element[2].get_pos()[2]**2)**0.5))
            elif element[1] == "vel_mag":
                print(element[0], float((element[2].get_vel()[0]**2 +
                                         element[2].get_vel()[1]**2 +
                                         element[2].get_vel()[2]**2)**0.5))
                
            elif element[1] == "active":
                print(element[0], element[2].is_performing(sim_time))
            elif element[1] == "state":
                print(element[0], element[2].get_state(sim_time))
            elif element[1] == "params":
                print(element[0], "\n" + element[2].get_params_str())

            elif element[1] == "note":
                print(element[0], element[2])
            
            print("\n")
            
        # clear stuff from last frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # do the actual drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        drawOrigin()
        drawBodies(bodies)
        drawVessels(vessels)

        if show_trajectories:
            drawProjections(projections)
            drawTrajectories(vessels)
            drawManeuvers(maneuvers)

        glfw.swap_buffers(window)

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < cycle_time:
            time.sleep(cycle_time - cycle_dt)
        elif cycle_time*2 <= cycle_dt:
            print("Cycle time too low! Machine can't update physics at the given cycle time!\n")
            print("Consider increasing cycle_time to get more consistent calculation rate.\n")

def init_sim():
    print("\nOrbitSim3D Initialization\n")
    print("Enter scenario file path to load scenario, or leave blank to start an empty scene.")
    print("(for example 'scenarios\\three_vessels.osf' or just 'three_vessels')\n")
    scn_path = input("Scenario path: ")
    if scn_path:
        import_scenario(scn_path)
    else:
        main()

init_sim()
