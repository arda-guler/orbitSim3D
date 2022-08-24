import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import os
import keyboard
import glfw
import time
import re
import shutil
import sys
import random
import glob

from graphics import *
from vessel_class import *
from body_class import *
from camera_class import *
from surface_point_class import *
from barycenter_class import *
from math_utils import *
from maneuver import *
from orbit import *
from plot import *
from command_panel import *
from config_utils import *
from radiation_pressure import *
from atmospheric_drag import *

def clear_cmd_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

initial_run = True

vessels = []
bodies = []
barycenters = []
surface_points = []
objs = []
projections = []
plots = []
cameras = []

maneuvers = []
radiation_pressures = []
atmospheric_drags = []

batch_commands = []

preset_orientations = ["prograde", "prograde_dynamic", "retrograde", "retrograde_dynamic",
                       "normal", "normal_dynamic", "antinormal", "antinormal_dynamic",
                       "radial_in", "radial_in_dynamic", "radial_out", "radial_out_dynamic"]

sim_time = 0

def window_resize(window, width, height):
    glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

def read_batch(batch_path):

    try:
        batch_file = open(batch_path, "r")
    except FileNotFoundError:
        try:
            batch_file = open("scenarios/" + batch_path, "r")
        except FileNotFoundError:
            try:
                batch_file = open(batch_path + ".obf", "r")
            except FileNotFoundError:
                try:
                    batch_file = open("scenarios/" + batch_path + ".obf", "r")
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
    global objs, vessels, bodies, projections, maneuvers, surface_points, barycenters, plots, radiation_pressures, atmospheric_drags, sim_time

    objs = []
    vessels = []
    bodies = []
    maneuvers = []
    projections = []
    surface_points = []
    barycenters = []
    plots = []
    radiation_pressures = []
    atmospheric_drags = []
    sim_time = 0

def import_scenario(scn_filename):
    global objs, vessels, bodies, surface_points, maneuvers, barycenters, atmospheric_drags, sim_time

    clear_scene()

    try:
        scn_file = open(scn_filename, "r")
    except FileNotFoundError:
        try:
            scn_file = open("scenarios/" + scn_filename, "r")
        except FileNotFoundError:
            try:
                scn_file = open(scn_filename + ".osf", "r")
            except FileNotFoundError:
                try:
                    scn_file = open("scenarios/" + scn_filename + ".osf", "r")
                except FileNotFoundError:
                    print("Scenario file not found.")
                    time.sleep(2)
                    
                    if os.name == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")
                        
                    init_sim()

    start_time = 0

    print("\nImporting scenario:", scn_filename, "\n")             
    import_lines = scn_file.readlines()

    for line in import_lines:
        line = line[0:-1].split("|")

        # get sim start time
        if line[0] == "T":
            try:
                start_time = float(line[1])
            except:
                pass

        # import bodies
        if line[0] == "B":
            line[5] = line[5][1:-1].split(",")
            line[6] = line[6][1:-1].split(",")
            line[7] = line[7][1:-1].split(",")

            orient_nums = re.findall(r"[-+]?\d*\.\d+|\d+", line[8])
            
            new_body = body(line[1], pywavefront.Wavefront(line[2], collect_faces=True), line[2],
                            float(line[3]), float(line[4]),
                            
                            [float(line[5][0]), float(line[5][1]), float(line[5][2])],
                            [float(line[6][0]), float(line[6][1]), float(line[6][2])],
                            [float(line[7][0]), float(line[7][1]), float(line[7][2])],
                            
                            [[float(orient_nums[0]), float(orient_nums[1]), float(orient_nums[2])],
                             [float(orient_nums[3]), float(orient_nums[4]), float(orient_nums[5])],
                             [float(orient_nums[6]), float(orient_nums[7]), float(orient_nums[8])]],

                            float(line[9]),
                            
                            float(line[10]),

                            float(line[11]),

                            float(line[12]), float(line[13]))
            
            bodies.append(new_body)
            objs.append(new_body)
            print("Loading body:", new_body.get_name())

        # import vessels
        elif line[0] == "V":
            line[3] = line[3][1:-1].split(",")
            line[4] = line[4][1:-1].split(",")
            line[5] = line[5][1:-1].split(",")
            new_vessel = vessel(line[1], pywavefront.Wavefront(line[2], collect_faces=True), line[2],
                                [float(line[3][0]), float(line[3][1]), float(line[3][2])],
                                [float(line[4][0]), float(line[4][1]), float(line[4][2])],
                                [float(line[5][0]), float(line[5][1]), float(line[5][2])])
            vessels.append(new_vessel)
            objs.append(new_vessel)
            print("Loading vessel:", new_vessel.get_name())

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
            print("Loading maneuver:", new_maneuver.get_name())

        # import surface points
        elif line[0] == "S":
            line[3] = line[3][1:-1].split(",") # color
            line[4] = line[4][1:-1].split(",") # gpos
            new_sp = surface_point(line[1], find_obj_by_name(line[2]),
                                   [float(line[3][0]), float(line[3][1]), float(line[3][2])],
                                   [float(line[4][0]), float(line[4][1]), float(line[4][2])])

            surface_points.append(new_sp)
            objs.append(new_sp)
            print("Loading surface point:", new_sp.get_name())

        # import barycenters
        elif line[0] == "C":
            line[2] = line[2].split(",")
            bodies_included = []
            for body_name in line[2]:
                bodies_included.append(find_obj_by_name(body_name))

            new_bc = barycenter(line[1], bodies_included)
            barycenters.append(new_bc)
            objs.append(new_bc)
            print("Loading barycenter:", new_bc.get_name())

        # import radiation pressure data
        elif line[0] == "R":
            if line[6] in preset_orientations:
                new_rp = radiation_pressure(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                            float(line[4]), find_obj_by_name(line[5]), line[6], float(line[7]), int(line[8]))
            else:
                line[6] = line[6][1:-1].split(",")
                new_rp = radiation_pressure(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                            float(line[4]), find_obj_by_name(line[5]),
                                            [float(line[6][0]), float(line[6][1]), float(line[6][2])],
                                            float(line[7]), int(line[8]))

            radiation_pressures.append(new_rp)
            print("Loading radiation pressure:", new_rp.get_name())

        # import atmospheric drag data
        elif line[0] == "A":
            new_ad = atmospheric_drag(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                      float(line[4]), float(line[5]), float(line[6]), int(line[7]))

            atmospheric_drags.append(new_ad)
            print("Loading atmospheric drag:", new_ad.get_name())
            
    main(scn_filename, start_time)

def export_scenario(scn_filename):
    global objs, vessels, bodies, surface_points, maneuvers, barycenters, radiation_pressures, atmospheric_drags, sim_time
    
    scn_filename = "scenarios/" + scn_filename
    if not scn_filename.endswith(".osf"):
        scn_filename += ".osf"

    clear_cmd_terminal()
    print("Saving scenario into " + scn_filename)
        
    with open(scn_filename, "w") as scn_file:
        print("Writing header...")
        header_string = """
;.osf -- orbitSim3D scenario format
;
;An arbitrary file extension/format to
;distinguish scenario files from
;regular text files for human reading.
;
;Lines starting in B are for bodies,
;lines starting in V are for vessels,
;lines starting in M are for maneuvers,
;lines starting in S are for surface points,
;lines starting in C are for barycenters,
;lines starting in R are for radiation pressure effects,
;lines starting in A are for atmoshperic drag effects.
;
;All other lines will be ignored and
;can be used for comments.
;
;(For redundancy, you can use an
;arbitrary non-letter character to
;denote comments.)
;
;= = = = = = = = = =\n
"""
                         
        scn_file.write(header_string)

        print("Writing simulation time...")
        time_save_string = "T|" + str(sim_time) + "\n"
        scn_file.write(time_save_string)

        print("Writing bodies...")
        for b in bodies:
            body_save_string = "B|" + b.get_name() + "|" + b.get_model_path() + "|" + str(b.get_mass()) + "|" +\
                               str(b.get_radius()) + "|" + str(b.get_color()) + "|" + str(b.get_pos()) + "|" +\
                               str(b.get_vel()) + "|" + str(b.get_orient()) + "|" + str(b.get_day_length()) + "|" +\
                               str(b.get_J2()) + "|" + str(b.luminosity) + "|" + str(b.atmos_sea_level_density) + "|" +\
                               str(b.atmos_scale_height) + "\n"
            scn_file.write(body_save_string)

        print("Writing vessels...")
        for v in vessels:
            vessel_save_string = "V|" + v.get_name() + "|" + v.get_model_path() + "|" + str(v.get_color()) + "|" +\
                                 str(v.get_pos()) + "|" + str(v.get_vel()) + "\n"
            scn_file.write(vessel_save_string)

        print("Writing maneuvers...")
        for m in maneuvers:
            maneuver_save_string = "M|" + m.get_name() + "|"
            if m.get_type() == "const_accel":
                maneuver_save_string += "const_accel|" + m.get_vessel().get_name() + "|" + m.frame_body.get_name() + "|" +\
                                        str(m.orientation_input) + "|" + str(m.accel) + "|" + str(m.t_start) + "|" + str(m.duration) + "\n"
            elif m.get_type() == "const_thrust":
                maneuver_save_string += "const_thrust|" + m.get_vessel().get_name() + "|" + m.frame_body.get_name() + "|" +\
                                        str(m.orientation_input) + "|" + str(m.thrust) + "|" +  str(m.mass_init) + "|" + str(m.mass_flow) + "|" +\
                                        str(m.t_start) + "|" + str(m.duration) + "\n"
            scn_file.write(maneuver_save_string)

        print("Writing surface points...")
        for s in surface_points:
            sp_save_string = "S|" + s.get_name() + "|" + s.get_body().get_name() + "|" + str(s.get_color()) + "|" + str(s.get_gpos()) + "\n"
            scn_file.write(sp_save_string)

        print("Writing barycenters...")
        for bc in barycenters:
            bc_save_string = "C|" + bc.get_name() + "|"
            for b in bc.get_bodies():
                bc_save_string += b.get_name() + ","
            bc_save_string = bc_save_string[:-1]+"\n"
            scn_file.write(bc_save_string)

        print("Writing radiation pressures...")
        for rp in radiation_pressures:
            rp_save_string = "R|" + rp.get_name() + "|" + rp.vessel.get_name() + "|" + rp.body.get_name() + "|" + str(rp.get_area()) +\
                             "|" + rp.orientation_frame.get_name() + "|" + str(rp.direction_input) + "|" + str(rp.mass) + "|" + str(rp.mass_auto_update) + "\n"
            scn_file.write(rp_save_string)

        print("Writing atmospheric drags...")
        for ad in atmospheric_drags:
            ad_save_string = "A|" + ad.get_name() + "|" + ad.vessel.get_name() + "|" + ad.body.get_name() + "|" + str(ad.get_area()) +\
                             "|" + str(ad.get_drag_coeff()) + "|" + str(ad.get_mass()) + "|" + str(ad.mass_auto_update) + "\n"
            scn_file.write(ad_save_string)

        print("Scenario export complete!")
        time.sleep(2)

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

def apply_radiation_pressure(rp_name, rp_vessel, rp_body, rp_area, rp_orient_frame, rp_direction, rp_mass, rp_mass_auto_update):
    global radiation_pressures

    if find_radiation_pressure_by_name(rp_name):
        print("A radiation pressure effect with this name already exists. Please pick another name for the new effect.\n")
        input("Press Enter to continue...")
        return

    new_rp = radiation_pressure(rp_name, rp_vessel, rp_body, rp_area, rp_orient_frame, rp_direction, rp_mass, rp_mass_auto_update)
    radiation_pressures.append(new_rp)

def remove_radiation_pressure(rp_name):
    global radiation_pressures

    rp = find_radiation_pressure_by_name(rp_name)

    if not rp:
        print("Radiation pressure effect not found!")
        time.sleep(2)
        return

    radiation_pressures.remove(rp)
    del rp

def find_radiation_pressure_by_name(rp_name):
    global radiation_pressures

    result = None

    for rp in radiation_pressures:
        if rp.name == rp_name:
            result = rp
            break

    return result

def apply_atmospheric_drag(ad_name, ad_vessel, ad_body, ad_area, ad_drag_coeff, ad_mass, ad_mass_auto_update):
    global atmospheric_drags

    if find_atmospheric_drag_by_name(ad_name):
        print("An atmospheric drag effect with this name already exists. Please pick another name for the new effect.\n")
        input("Press Enter to continue...")
        return

    new_ad = atmospheric_drag(ad_name, ad_vessel, ad_body, ad_area, ad_drag_coeff, ad_mass, ad_mass_auto_update)
    atmospheric_drags.append(new_ad)

def remove_atmospheric_drag(ad_name):
    global atmospheric_drags

    ad = find_atmospheric_drag_by_name(ad_name)
    if not ad:
        print("Atmospheric drag effect not found!")
        time.sleep(2)
        return

    atmospheric_drags.remove(ad)
    del ad

def find_atmospheric_drag_by_name(ad_name):
    global atmospheric_drags

    result = None

    for ad in atmospheric_drags:
        if ad.name == ad_name:
            result = ad
            break

    return result

def create_vessel(name, model_name, color, pos, vel):
    global vessels, objs

    if find_obj_by_name(name):
        print("An object with this name already exists. Please pick another name for the new vessel.\n")
        input("Press Enter to continue...")
        return

    try:
        model_path = "data/models/" + model_name + ".obj"
        model = pywavefront.Wavefront(model_path, collect_faces=True)
    except:
        print("Could not load model:", model_path)
        time.sleep(3)
        return

    try:
        new_vessel = vessel(name, model, model_path, color, pos, vel)
    except:
        print("Could not create vessel:", name)
        
    vessels.append(new_vessel)
    objs.append(new_vessel)

def fragment(vessel_name, num_of_frags, vel_of_frags):

    if num_of_frags < 1:
        print("Cannot fragment vessel into less than 1 parts! (Duh.)")
        input("Press Enter to continue...")
        return
    
    if find_obj_by_name(vessel_name):
        vessel = find_obj_by_name(vessel_name)
    else:
        print("A vessel with name \'" + vessel_name + "\' does not exist! Cannot create fragments!")
        input("Press Enter to continue...")
        return

    for i in range(num_of_frags):
        
        fragment_vel = [vessel.get_vel()[0] + random.uniform(-vel_of_frags, vel_of_frags),
                        vessel.get_vel()[1] + random.uniform(-vel_of_frags, vel_of_frags),
                        vessel.get_vel()[2] + random.uniform(-vel_of_frags, vel_of_frags)]

        fragment_pos = [vessel.get_pos()[0], vessel.get_pos()[1], vessel.get_pos()[2]]
        
        create_vessel(vessel_name + "_frag_" + str(i), "fragment", vessel.get_color(), fragment_pos, fragment_vel)

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

# 'point' here can either be an object with property 'pos' or an
# arbitrary point in the 3D scene
def get_closest_object_to(point):
    global objs
    current_pos = [0,0,0]
    result_obj = None
    
    if point.get_pos:
        current_pos = point.get_pos()
    else:
        current_pos = point

    min_dist = None
    for obj in objs:
        current_dist = ((obj.get_pos()[0] - current_pos[0])**2 + (obj.get_pos()[1] - current_pos[1])**2 + (obj.get_pos()[2] - current_pos[2])**2)**0.5
        if not min_dist or current_dist < min_dist:
            min_dist = current_dist
            result_obj = obj

    return obj

def find_proj_by_name(name):
    global projections

    result = None

    for proj in projections:
        if proj.get_name() == name:
            result = proj
            break

    return result

def create_keplerian_proj(name, vessel, body, proj_time):
    global projections

    if find_proj_by_name(name):
        print("A projection with this name already exists. Please pick another name for the new projection.\n")
        input("Press Enter to continue...")
        return

    new_proj = kepler_projection(name, vessel, body, proj_time)
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

def update_keplerian_proj(name, update_time):
    global projections
    proj_tbu = find_proj_by_name(name)

    if not proj_tbu:
        print("Projection not found!")
        time.sleep(2)
        return

    proj_vessel = proj_tbu.get_vessel()
    proj_body = proj_tbu.get_body()

    try:
        delete_keplerian_proj(name)
        create_keplerian_proj(name, proj_vessel, proj_body, update_time)
    except:
        print("Can not update projection!")
        time.sleep(2)
        return

def find_plot_by_name(name):
    global plots

    result = None

    for plot in plots:
        if plot.get_name() == name:
            result = plot
            break

    return result

def create_plot(name, variable, obj1_name, obj2_name, start_time=-1, end_time=-1):
    global plots, sim_time

    if find_plot_by_name(name):
        print("A plot with this name already exists. Please pick another name for the new plot.\n")
        input("Press Enter to continue...")
        return

    if start_time == -1:
        start_time = sim_time

    if end_time == -1:
        end_time = start_time + 100

    # plot title, x name, x list, y name, y list, obj1, obj2, variable, start_time, end_time
    if variable == "alt":
        obj1 = find_obj_by_name(obj1_name)
        obj2 = find_obj_by_name(obj2_name)
        new_plot = plot(name, "Time", [], "Altitude of " + obj1_name + " above " + obj2_name, [],
                        obj1, obj2, "alt", start_time, end_time)
    elif variable == "dist":
        obj1 = find_obj_by_name(obj1_name)
        obj2 = find_obj_by_name(obj2_name)
        new_plot = plot(name, "Time", [], "Distance between " + obj1_name + " and " + obj2_name, [],
                        obj1, obj2, "dist", start_time, end_time)
    elif variable == "vel_mag":
        obj1 = find_obj_by_name(obj1_name)
        obj2 = find_obj_by_name(obj2_name)
        new_plot = plot(name, "Time", [], "Velocity of " + obj1_name + " rel to " + obj2_name, [],
                        obj1, obj2, "vel_mag", start_time, end_time)

    plots.append(new_plot)

def delete_plot(name):
    global plots
    plot_tbd = find_plot_by_name(name)

    if not plot_tbd:
        print("Plot not found!")
        time.sleep(2)
        return

    plots.remove(plot_tbd)
    del plot_tbd

def find_barycenter_by_name(name):
    global barycenters

    result = None

    for bc in barycenters:
        if bc.get_name() == name:
            result = bc
            break

    return result

def create_barycenter(name, b_bodies):
    global barycenters, objs

    if find_barycenter_by_name(name):
        print("A barycenter with this name already exists. Please pick another name for the new barycenter.\n")
        input("Press Enter to continue...")
        return

    for x in b_bodies:
        x = find_obj_by_name(b_bodies)

    for x in b_bodies:
        if type(x) == "__body__":
            print("You must only use celestial bodies when calculating barycenters.")
            input("Press Enter to continue...")
            return

    new_barycenter = barycenter(name, b_bodies)
    barycenters.append(new_barycenter)
    objs.append(new_barycenter)

def delete_barycenter(name):
    global barycenters, objs
    bc_tbd = find_barycenter_by_name(name)

    if not bc_tbd:
        print("Barycenter not found!")
        time.sleep(2)
        return

    objs.remove(bc_tbd)
    barycenters.remove(bc_tbd)
    del bc_tbd

def find_surface_point_by_name(name):
    global surface_points

    for sp in surface_points:
        if sp.name == name:
            return sp

    return None

def create_surface_point(name, b, color, coords):
    global surface_points
    
    if find_surface_point_by_name(name):
        print("A barycenter with this name already exists. Please pick another name for the new barycenter.\n")
        input("Press Enter to continue...")
        return

    try:
        new_sp = surface_point(name, b, color, coords)
        surface_points.append(new_sp)
    except:
        print("Could not create new surface point:", name)

def vessel_body_crash(v, b):
    # a vessel has crashed into a celestial body. We will convert the vessel object
    # into a surface point on the body (a crash site) and remove all references to
    # the vessel object
    global maneuvers, surface_points, plots, batch_commands

    for m in maneuvers:
        if m.vessel == v or m.frame_body == v:
            delete_maneuver(m.name)

    for p in plots:
        if p.obj1 == v or p.obj2 == v:
            p.display()
            delete_plot(p.name)

    # orbit projections can stay since their calculation time is known

    bcc = v.get_body_centered_coords(b)
    crash_site_gpos = impact_gpos(bcc)
    crash_site_color = v.get_color()
    crash_site_name = v.get_name() + "_impact_site"
    create_surface_point(crash_site_name, b, crash_site_color, crash_site_gpos)

    note_name = v.name.upper() + "_IMPACT"
    batch_commands.append(["note", note_name, v.name + " has impacted " + b.name + "."])

    delete_vessel(v.name)

def lock_active_cam_by_obj_name(name):
    target = find_obj_by_name(name)

    if not target:
        print("Object '" + name + "' not found.")
        time.sleep(2)
        return

    get_active_cam().lock_to_target(target)

def lock_active_cam_by_proximity():
    target = get_closest_object_to(get_active_cam())
    get_active_cam().lock_to_target(target)

def unlock_active_cam():
    get_active_cam().unlock()
    
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

def get_active_cam():
    global cameras

    for cam in cameras:
        if cam.active:
            return cam

    # just a fail-safe
    return cameras[0]

def main(scn_filename=None, start_time=0):
    global vessels, bodies, surface_points, projections, objs, sim_time, batch_commands,\
           plots, cameras, barycenters, radiation_pressures, atmospheric_drags

    # read config to get start values
    sim_time, delta_t, cycle_time, output_rate, cam_pos_x, cam_pos_y, cam_pos_z, cam_strafe_speed, cam_rotate_speed,\
    window_x, window_y, fov, near_clip, far_clip, cam_yaw_right, cam_yaw_left, cam_pitch_down, cam_pitch_up, cam_roll_cw, cam_roll_ccw,\
    cam_strafe_left, cam_strafe_right, cam_strafe_forward, cam_strafe_backward, cam_strafe_up, cam_strafe_down, warn_cycle_time,\
    maneuver_auto_dt, draw_mode, point_size, labels_visible, vessel_body_collision, batch_autoload = read_current_config()

    # initializing glfw
    glfw.init()

    # creating a window
    window = glfw.create_window(int(window_x),int(window_y),"OrbitSim3D", None, None)
    glfw.set_window_pos(window,100,100)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    
    gluPerspective(fov, int(window_x)/int(window_y), near_clip, far_clip)
    glEnable(GL_CULL_FACE)
    glPointSize(point_size)

    main_cam = camera("main_cam", [cam_pos_x,cam_pos_y,cam_pos_z], [[1,0,0],[0,1,0],[0,0,1]], True)
    cameras.append(main_cam)
    # put "camera" in starting position
    glTranslate(main_cam.get_pos()[0], main_cam.get_pos()[1], main_cam.get_pos()[2])

    batch_commands = []
    output_buffer = []
    auto_dt_buffer = []
    rapid_compute_buffer = []
    rapid_compute_flag = False

    show_trajectories = True

    sim_time = start_time

    # look if there is a batch file associated so we can autoload it
    if batch_autoload and scn_filename:

        complete_path = None
        
        if "/" in scn_filename:
            complete_path = scn_filename
            scn_filename = scn_filename.split("/")[-1]
        elif "\\" in scn_filename:
            complete_path = scn_filename
            scn_filename = scn_filename.split("\\")[-1]

        if scn_filename.endswith(".osf"):
            scn_filename = scn_filename[:-4]
            
        if os.path.exists("scenarios/" + scn_filename + ".obf"):
            batch_commands.append(["batch", scn_filename])
            print("Autoloading associated batch file...")
        elif os.path.exists(scn_filename + ".obf"):
            batch_commands.append(["batch", scn_filename + ".obf"])
            print("Autoloading associated batch file...")
        elif complete_path and os.path.exists(complete_path[:-4] + ".obf"):
            batch_commands.append(["batch", complete_path[:-4] + ".obf"])
            print("Autoloading associated batch file...")
        else:
            pass

    while not glfw.window_should_close(window):

        sim_time += delta_t

        glfw.poll_events()

        frame_command = False

        # get input and move the "camera" around
        get_active_cam().rotate([(keyboard.is_pressed(cam_pitch_down) - keyboard.is_pressed(cam_pitch_up)) * cam_rotate_speed,
                                 (keyboard.is_pressed(cam_yaw_left) - keyboard.is_pressed(cam_yaw_right)) * cam_rotate_speed,
                                 (keyboard.is_pressed(cam_roll_ccw) - keyboard.is_pressed(cam_roll_cw)) * cam_rotate_speed])

        get_active_cam().move([(keyboard.is_pressed(cam_strafe_left) - keyboard.is_pressed(cam_strafe_right)) * cam_strafe_speed,
                               (keyboard.is_pressed(cam_strafe_down) - keyboard.is_pressed(cam_strafe_up)) * cam_strafe_speed,
                               (keyboard.is_pressed(cam_strafe_forward) - keyboard.is_pressed(cam_strafe_backward)) * cam_strafe_speed])

        if keyboard.is_pressed("c") and not rapid_compute_flag:
            frame_command = True

        elif keyboard.is_pressed("p") and not rapid_compute_flag:
            panel_commands = use_command_panel(vessels, bodies, surface_points, barycenters, maneuvers, radiation_pressures, atmospheric_drags, projections, plots,
                                               auto_dt_buffer, sim_time, delta_t, cycle_time, output_rate, cam_strafe_speed, cam_rotate_speed, rapid_compute_buffer)
            if panel_commands:
                for panel_command in panel_commands:
                    panel_command = panel_command.split(" ")
                    batch_commands.append(panel_command)

        if frame_command or len(batch_commands) > 0:
            flush_input()

            if frame_command:
                command = input("\n > ")
                command = command.split(" ")
                command[0] = command[0].lower()

            # --- COMMAND INTERPRETER ---

            if len(batch_commands) > 0 and (not frame_command or command[0] == "batch"):
                command = batch_commands[0]
                batch_commands.remove(command)

            # BATCH command
            if command[0] == "batch":
                batch_commands = read_batch(command[1])
            
            # SHOW command
            elif command[0] == "show":
                
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
                        elif command[2] == "alt":
                            if (type(find_obj_by_name(command[3])).__name__ == "body" and
                                type(find_obj_by_name(command[1])).__name__ == "vessel"):
                                output_buffer.append([command[4], "alt", obj, command[3]])
                            else:
                                print("You can only get altitude of a vessel above a celestial body!\n")
                                time.sleep(2)
                            
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
                        elif command[2] == "gps" or command[2] == "gpos":
                            if type(obj).__name__ == "surface_point":
                                output_buffer.append([command[3], "gpos", obj])
                            else:
                                print("You can only get ground position of a surface point!\n")
                                time.sleep(2)
                            
                    elif find_maneuver_by_name(command[1]):
                        maneuver = find_maneuver_by_name(command[1])
                        if command[2] == "active" or command[2] == "state" or command[2] == "params":
                            output_buffer.append([command[3], command[2], maneuver, "m"])
                        else:
                            print("Illegal parameter!\n")
                            time.sleep(2)

                    elif find_radiation_pressure_by_name(command[1]):
                        rad_press = find_radiation_pressure_by_name(command[1])
                        if command[2] == "params":
                            output_buffer.append([command[3], command[2], rad_press, "rp"])
                        else:
                            print("Illegal parameter!\n")
                            time.sleep(2)

                    elif find_atmospheric_drag_by_name(command[1]):
                        atmo_drag = find_atmospheric_drag_by_name(command[1])
                        if command[2] == "params":
                            output_buffer.append([command[3], command[2], atmo_drag, "ad"])
                        else:
                            print("Illegal parameter!\n")
                            time.sleep(2)

                    elif find_proj_by_name(command[1]):
                        proj = find_proj_by_name(command[1])
                        if (command[2] == "apoapsis" or command[2] == "periapsis" or command[2] == "params" or
                            command[2] == "apoapsis_r" or command[2] == "periapsis_r" or
                            command[2] == "period" or command[2] == "body" or command[2] == "vessel" or
                            command[2] == "energy" or command[2] == "semimajor_axis" or command[2] == "eccentricity"):
                            output_buffer.append([command[3], command[2], proj, "p"])
                        else:
                            print("Illegal parameter!\n")
                            time.sleep(2)
                            
                    else:
                        print("Object/maneuver/projection not found.")
                        time.sleep(2)

                elif len(command) == 2:
                    if command[1] == "traj":
                        show_trajectories = True
                    elif command[1] == "labels":
                        labels_visible = 1

                else:
                    print("Wrong number of arguments for command 'show'.")
                    time.sleep(2)

            # HIDE command
            elif command[0] == "hide":
                if command[1] == "traj":
                    show_trajectories = False
                elif command[1] == "labels":
                    labels_visible = 0
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

            # FRAGMENT command
            elif command[0] == "fragment":
                if len(command) == 4:
                    fragment(command[1], int(command[2]), float(command[3]))
                elif len(command) == 3:
                    fragment(command[1], int(command[2]), 100)
                elif len(command) == 2:
                    fragment(command[1], 5, 100)
                else:
                    print("Wrong number of arguments for command 'fragment'.\n")
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

            # APPLY_RADIATION_PRESSURE command
            elif command[0] == "apply_radiation_pressure":
                if len(command) == 9:
                    if command[6] in preset_orientations:
                        apply_radiation_pressure(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                                 float(command[4]), find_obj_by_name(command[5]), command[6], float(command[7]), int(command[8]))
                    else:
                        apply_radiation_pressure(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                                 float(command[4]), find_obj_by_name(command[5]),
                                                 [float(command[6][1:-1].split(",")[0]),
                                                  float(command[6][1:-1].split(",")[1]),
                                                  float(command[6][1:-1].split(",")[2])],
                                                 float(command[7]), int(command[8]))
                else:
                    print("Wrong number of arguments for command 'apply_radiation_pressure'.\n")
                    time.sleep(2)

            # REMOVE_RADIATION_PRESSURE command
            elif command[0] == "remove_radiation_pressure":
                if len(command) == 2:
                    remove_radiation_pressure(command[1])
                else:
                    print("Wrong number of arguments for command 'remove_radiation_pressure'.\n")
                    time.sleep(2)

            # APPLY_ATMOSPHERIC_DRAG command
            elif command[0] == "apply_atmospheric_drag":
                if len(command) == 8:
                    apply_atmospheric_drag(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                           float(command[4]), float(command[5]), float(command[6]), int(command[7]))
                else:
                    print("Wrong number of arguments for command 'apply_atmospheric_drag'.\n")
                    time.sleep(2)

            # REMOVE_ATMOSPHERIC_DRAG command
            elif command[0] == "remove_atmospheric_drag":
                if len(command) == 2:
                    remove_atmospheric_drag(command[1])
                else:
                    print("Wrong number of arguments for command 'remove_atmospheric_drag'.\n")
                    time.sleep(2)

            # CREATE_PROJECTION command
            elif command[0] == "create_projection":
                if len(command) == 4:
                    create_keplerian_proj(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]), sim_time)
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

            # UPDATE_PROJECTION command
            elif command[0] == "update_projection":
                if len(command) == 2:
                    update_keplerian_proj(command[1], sim_time)
                else:
                    print("Wrong number of arguments for command 'delete_projection'.\n")
                    time.sleep(2)

            # CREATE_PLOT command
            elif command[0] == "create_plot":
                if len(command) == 5:
                    create_plot(command[1], command[2], command[3], command[4])
                elif len(command) == 6:
                    if command[5].startswith("end_time"):
                        create_plot(command[1], command[2], command[3], command[4], -1, float(command[5].split("=")[1]))
                    elif command[5].startswith("start_time"):
                        create_plot(command[1], command[2], command[3], command[4], float(command[5].split("=")[1]))
                    else:
                        create_plot(command[1], command[2], command[3], command[4], float(command[5]))
                elif len(command) == 7:
                    create_plot(command[1], command[2], command[3], command[4], float(command[5]), float(command[6]))
                else:
                    print("Wrong number of arguments for command 'create_plot'.\n")
                    time.sleep(2)
                    
            # DELETE_PLOT command
            elif command[0] == "delete_plot":
                if len(command) == 2:
                    delete_plot(command[1])
                else:
                    print("Wrong number of arguments for command 'delete_plot'.\n")
                    time.sleep(2)

            # DISPLAY_PLOT
            # this is not within 'show' command because this doesn't use the output buffer
            elif command[0] == "display_plot":
                if len(command) == 2:
                    plot_to_display = find_plot_by_name(command[1])
                    if plot_to_display and sim_time > plot_to_display.get_start_time():
                        plot_to_display.display()
                    else:
                        print("This plotter doesn't exist, or it didn't start plotting yet!")
                        time.sleep(2)
                else:
                    print("Wrong number of arguments for command 'display_plot'.\n")
                    time.sleep(2)

            # CREATE_BARYCENTER
            elif command[0] == "create_barycenter":
                if len(command) < 3:
                    print("Not enough arguments!\n")
                    time.sleep(2)
                else:
                    bodies_names = []
                    for name in command[2:]:
                        bodies_names.append(find_obj_by_name(name))
                    create_barycenter(command[1], bodies_names)

            # DELETE_BARYCENTER
            elif command[0] == "delete_barycenter":
                delete_barycenter(command[1])

            # GET_OBJECTS command
            elif command[0] == "get_objects":
                print("Objects currently in simulation:\n")
                for b in bodies:
                    print("BODY:", b.get_name() + "\n")
                for v in vessels:
                    print("VESSEL:", v.get_name() + "\n")
                for sp in surface_points:
                    print("SURFACE POINT:", sp.get_name() + "\n")
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

            # GET_PLOTS command
            elif command[0] == "get_plots":
                print("\nPlots currently in the simulation:\n")
                for p in plots:
                    print("PLOT:", p.get_name(), "\n")
                input("Press Enter to continue...")

            # CAM_STRAFE_SPEED command
            elif command[0] == "cam_strafe_speed":
                cam_strafe_speed = float(command[1])

            # CAM_ROTATE_SPEED command
            elif command[0] == "cam_rotate_speed":
                cam_rotate_speed = float(command[1])

            # DELTA_T command
            elif command[0] == "delta_t":
                delta_t = float(command[1])

            # AUTO_DT command
            elif command[0] == "auto_dt":
                if len(command) == 3:
                    auto_dt_buffer.append([float(command[1]), float(command[2])])
                    # keep this sorted because the simulation only looks at index 0
                    auto_dt_buffer = sorted(auto_dt_buffer)
                else:
                    print("Wrong number of arguments for command 'auto_dt'.")
                    time.sleep(2)

            # AUTO_DT_REMOVE command
            elif command[0] == "auto_dt_remove":
                if len(command) == 2:
                    auto_dt_buffer.remove(auto_dt_buffer[int(command[1])])

            # GET_AUTO_DT_BUFFER command
            elif command[0] == "get_auto_dt_buffer":
                print(auto_dt_buffer)
                input("Press enter to continue...")

            # AUTO_DT_CLEAR command
            elif command[0] == "auto_dt_clear":
                auto_dt_buffer = []

            # RAPID_COMPUTE command
            elif command[0] == "rapid_compute":
                if len(command) == 2:
                    rapid_compute_buffer.append([sim_time, float(command[1])])
                elif len(command) == 3:
                    rapid_compute_buffer.append([float(command[1]), float(command[2])])
                else:
                    print("Wrong number of arguments for command 'rapid_compute'.")
                    time.sleep(2)

                rapid_compute_buffer = sorted(rapid_compute_buffer)

            # CANCEL_RAPID_COMPUTE command
            elif command[0] == "cancel_rapid_compute":
                try:
                    del rapid_compute_buffer[int(command[1])]
                except IndexError:
                    print("Given index does not exist in the rapid compute buffer.")
                    time.sleep(2)

            # GET_RAPID_COMUTE_BUFFER command
            elif command[0] == "get_rapid_compute_buffer":
                print(rapid_compute_buffer)

            # RAPID_COMPUTE_CLEAR command
            elif command[0] == "rapid_compute_clear":
                rapid_compute_buffer = []

            # VESSEL_BODY_COLLISION command
            elif command[0] == "vessel_body_collision":
                vessel_body_collision = int(command[1])

            # OUTPUT_RATE command
            elif command[0] == "output_rate":
                output_rate = int(command[1])

            # CYCLE_TIME command
            elif command[0] == "cycle_time":
                cycle_time = float(command[1])

            # NOTE command
            elif command[0] == "note":
                new_note = ""
                for i in range(2,len(command)):
                    new_note = new_note + " " + command[i]
                output_buffer.append([command[1], "note", new_note])

            # LOCK_CAM command
            elif command[0] == "lock_cam":
                if len(command) > 1:
                    lock_active_cam_by_obj_name(command[1])
                else:
                    lock_active_cam_by_proximity()

            elif command[0] == "unlock_cam":
                unlock_active_cam()

            # DRAW_MODE command
            elif command[0] == "draw_mode":
                try:
                    draw_mode = int(command[1])
                except ValueError:
                    print("Illegal command! Accepted draw modes: 0, 1, 2")
                    time.sleep(2)

            # POINT_SIZE command
            elif command[0] == "point_size":
                try:
                    glPointSize(int(command[1]))
                except:
                    print("Illegal command!")
                    time.sleep(2)

            # EXPORT command
            elif command[0] == "export":
                export_scenario(command[1])

            # HELP command
            elif command[0] == "help":
                if len(command) == 1:
                    print("\nAvailable commands: help, show, hide, clear, cam_strafe_speed, cam_rotate_speed, delta_t, cycle_time,")
                    print("create_vessel, delete_vessel, fragment, get_objects, create_maneuver, delete_maneuver, get_maneuvers,")
                    print("batch, note, create_projection, delete_projection, update_projection, get_projections, create_plot,")
                    print("delete_plot, display_plot, get_plots, output_rate, lock_cam, unlock_cam, auto_dt, auto_dt_remove,")
                    print("auto_dt_clear, get_auto_dt_buffer, draw_mode, point_size, create_barycenter, delete_barycenter,")
                    print("export, rapid_compute, cancel_rapid_compute, get_rapid_compute_buffer, rapid_compute_clear,")
                    print("vessel_body_collision, apply_radiation_pressure, remove_radiation_pressure,")
                    print("apply_atmospheric_drag, remove_atmospheric_drag\n")
                    print("Press P to use the command panel interface or C to use the command line (...like you just did.)\n")
                    print("Simulation is paused while typing a command or using the command panel interface.\n")
                    print("Type help <command> to learn more about a certain command.\n")
                    input("Press Enter to continue...")
                elif len(command) == 2:
                    if command[1] == "show":
                        print("\n'show' command adds an output element to the command prompt/terminal.\n")
                        print("Syntax Option 1: show <object_name> <attribute> <display_label>\n")
                        print("Syntax Option 2: show <object_name> <relative_attribute> <frame_of_reference_name> <display_label>\n")
                        print("Syntax Option 3: show <maneuver_name> <(active/state/params)> <display_label>\n")
                        print("Syntax Option 4: show <radiation_pressure_name> params <display_label>\n")
                        print("Syntax Option 5: show <atmospheric_drag_name> params <display_label>\n")
                        print("Syntax Option 6: show <projection_name> <(attrib_name/params)> <display_label>\n")
                        print("Syntax Option 7: show traj (enables trajectory trails)\n")
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
                    elif command[1] == "fragment":
                        print("\n'fragment' command creates small fragments from an object in space\n(as if it was hit by a kinetic impactor).\n")
                        print("Syntax Option 1: fragment <object_name> <num_of_fragments> <velocity of fragments>\n")
                        print("Syntax Option 2: fragment <object_name> <num_of_fragments>\n")
                        print("Syntax Option 3: fragment <object_name>\n")
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
                    elif command[1] == "apply_radiation_pressure":
                        print("\n'apply_radiation_pressure' command sets up a radiation pressure effect on a vessel.\n")
                        print("Syntax: apply_radiation_pressure <name> <vessel> <radiation_source_body> <illuminated_area> <frame_of_reference> <orientation> <vessel_mass> <mass_auto_update>")
                        input("Press Enter to continue...")
                    elif command[1] == "remove_radiation_pressure":
                        print("\n'remove_radiation_pressure' command removes a radiation pressure effect from the simulation.\n")
                        print("Syntax: remove_radiation_pressure <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "apply_atmospheric_drag":
                        print("\n'apply_atmospheric_drag' command sets up an atmospheric drag effect on a vessel.\n")
                        print("Syntax: apply_atmospheric_drag <name> <vessel> <body> <drag_area> <drag_coeff> <vessel_mass> <mass_auto_update>")
                        input("Press Enter to continue...")
                    elif command[1] == "remove_atmospheric_drag":
                        print("\n'remove_atmospheric_drag' command removes an atmospheric drag effect from the simulation.\n")
                        print("Syntax: remove_atmospheric_drag <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "create_projection":
                        print("\n'create_projection' command creates a 2-body Keplerian orbit projection of a vessel around a body.\n")
                        print("Syntax: create_projection <name> <vessel> <body>")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_projection":
                        print("\n'delete_projection' command removes a 2-body Keplerian orbit projection from the simulation.\n")
                        print("Syntax: delete_projection <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "update_projection":
                        print("\n'update_projection' command recalculates a 2-body Keplerian orbit projection at current simulation time.\n")
                        print("Syntax: update_projection <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "create_plot":
                        print("\n'create_plot' command adds a plotter to the simulation to plot some value against simulation time")
                        print("during some interval. It will display automatically when finished, or on demand with 'display_plot' command.")
                        print("Syntax: create_plot <name> <variable> <obj_1_name> <obj_2_name> (+ <start_time> <end_time>)")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_plot":
                        print("\n'delete_plot' command removes a plotter from the simulation.\n")
                        print("Syntax: delete_plot <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "display_plot":
                        print("\n'display_plot' command displays a plotter with matplotlib.\n")
                        print("Syntax: display_plot <name>")
                        input("Press Enter to continue...")
                    elif command[1] == "create_barycenter":
                        print("'create_barycenter' marks the barycenter of multiple celestial bodies and allows for calculations\nrelative to that imaginary point in space.")
                        print("Syntax: create_barycenter <name> <bodies (separate names with single space)>")
                        input("Press Enter to continue...")
                    elif command[1] == "delete_barycenter":
                        print("'delete_barycenter' removes a previously marked barycenter.")
                        print("Syntax: delete_barycenter <name>")
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
                    elif command[1] == "get_plots":
                        print("\n'get_plots' command prints out the names of plotters currently in the simulation.\n")
                        print("Syntax: get_plots\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cam_strafe_speed":
                        print("\n'cam_strafe_speed' command sets the speed of linear camera movement.\n")
                        print("Syntax: cam_strafe_speed <speed>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cam_rotate_speed":
                        print("\n'cam_rotate_speed' command sets the speed of camera rotation.\n")
                        print("Syntax: cam_rotate_speed <speed> \n")
                        input("Press Enter to continue...")
                    elif command[1] == "delta_t":
                        print("\n'delta_t' command sets time step length of each physics frame.")
                        print("Set delta_t negative to run the simulation backwards (to retrace an object's trajectory).\n")
                        print("Syntax: delta_t <seconds>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "auto_dt":
                        print("\n'auto_dt' command adds an automatic delta_t adjustment to happen at a certain time in the simulation.")
                        print("This is usually useful for playing back certain scenarios exactly the way they were initially created, since the.")
                        print("choice of delta_t can have a big influence on the physics.\n")
                        print("Syntax: auto_dt <simulation_time_at_which_the_change_should_happen> <delta_t_value>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "auto_dt_remove":
                        print("\n'auto_dt_remove' command removes an auto_dt command from the buffer.")
                        print("It is a good idea to see the buffer first with the 'get_auto_dt_buffer' command.\n")
                        print("Syntax: auto_dt_remove <buffer_index>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "auto_dt_clear":
                        print("\n'auto_dt_clear' command clears the auto_dt buffer.")
                        print("Syntax: auto_dt_clear\n")
                        input("Press Enter to continue...")
                    elif command[1] == "get_auto_dt_buffer":
                        print("\n'get_auto_dt_buffer' command displays the current state of the auto_dt buffer.")
                        print("The commands are displayed in format [[<time>, <delta_t>],[<time>, <delta_t>],[<time>, <delta_t>]...]")
                        print("Syntax: get_auto_dt_buffer\n")
                        input("Press Enter to continue...")
                    elif command[1] == "rapid_compute":
                        print("\n'rapid_compute' command sets a time interval for the simulation to enter rapid computation mode.")
                        print("In this mode, the simulation proceeds much faster without losing sacrificing physical accuracy, but")
                        print("provides no meaningful user output in the meanwhile.")
                        print("Syntax Option 1: rapid_compute <end_time>")
                        print("Syntax Option 2: rapid_compute <start_time> <end_time>\n")
                        input("Press Enter to continue...")
                    elif command[1] == "cancel_rapid_compute":
                        print("\n'cancel_rapid_compute' command removes a rapid computation iterval from the buffer.")
                        print("Syntax: cancel_rapid_compute <buffer_index>")
                        input("Press Enter to continue...")
                    elif command[1] == "get_rapid_compute_buffer":
                        print("\n'get_rapid_compute_buffer' command prints out the rapid compute buffer.")
                        print("Syntax: get_rapid_compute_buffer")
                        input("Press Enter to continue...")
                    elif command[1] == "rapid_compute_clear":
                        print("\n'rapid_compute_clear' command clears the rapid compute buffer.")
                        print("Syntax: clear_rapid_compute")
                        input("Press Enter to continue...")
                    elif command[1] == "vessel_body_collision":
                        print("\n'vessel_body_collision' commands activates or deactivates vessel-body collision checks.")
                        print("Syntax: vessel_body_collision <{0, 1}>")
                        input("Press Enter to continue...")
                    elif command[1] == "output_rate":
                        print("\n'output_rate' command sets the number of cycles per update for the output buffer.")
                        print("Must be a positive integer.\n")
                        print("Syntax: output_rate <integer>\n")
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
                    elif command[1] == "lock_cam":
                        print("\n'lock_cam' command locks the active camera to an object (if it exists).")
                        print("Syntax: lock_cam <object_name>")
                        input("Press Enter to continue...")
                    elif command[1] == "unlock_cam":
                        print("\n'lock_cam' command unlocks the active camera and makes it stationary rel. to global coordinates.")
                        print("Syntax: unlock_cam")
                        input("Press Enter to continue...")
                    elif command[1] == "draw_mode":
                        print("\n'draw_mode' command selects scene visualization mode.")
                        print("0 = lines, 1 = filled polygon, 2 = filled polygon with line overlay")
                        print("Syntax: draw_mode <selection>")
                        input("Press Enter to continue...")
                    elif command[1] == "point_size":
                        print("\n'point_size' command sets the size of points that represent distant objects in the scene (in pixels).")
                        print("Syntax: point_size <size>")
                        input("Press Enter to continue...")
                    elif command[1] == "export":
                        print("\n'export' command exports the current scenario state into an OrbitSim3D scenario (.osf) file.")
                        print("Syntax: export <filename>")
                        input("Press Enter to continue...")
                    elif command[1] == "help":
                        print("\n'help' command prints out the help text.\n")
                        print("Syntax: help\n")
                        input("Press Enter to continue...")
                    else:
                        print("\nUnknown command.")
                        input("Press Enter to continue...")

            elif command[0] == "" or not command[0]:
                # user probably changed their mind
                pass
            else:
                print("\nUnrecognized command: " + str(command[0]))
                input("Press Enter to continue...")

        cycle_start = time.perf_counter()

        # change delta_t according to auto_dt_buffer
        if auto_dt_buffer and auto_dt_buffer[0][0] <= sim_time:
            delta_t = auto_dt_buffer[0][1]
            auto_dt_buffer.remove(auto_dt_buffer[0])

        # set rapid compute flag according to rapid_compute_buffer
        if rapid_compute_buffer and rapid_compute_buffer[0][0] <= sim_time < rapid_compute_buffer[0][1] and not rapid_compute_flag:
            rapid_compute_flag = True
            old_cycle_time = cycle_time
            old_cam_strafe_speed = cam_strafe_speed
            old_cam_rotate_speed = cam_rotate_speed
            cam_strafe_speed = 0
            cam_rotate_speed = 0
            cycle_time = 0
            clear_cmd_terminal()
            print("OrbitSim3D Command Interpreter & Output Display\n")
            print("Simulation is in rapid computation mode from T=" + str(rapid_compute_buffer[0][0]) + " to T=" + str(rapid_compute_buffer[0][1]) + ".")
            print("Minimal user output will be provided to allocate more resources for mathematical operations.")
            print("Please wait until the calculations are complete.")
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            drawRapidCompute(get_active_cam())
            glfw.swap_buffers(window)

        # this prevents 'jumps' in trajectory trails during rapid compute
        if rapid_compute_buffer and rapid_compute_buffer[0][0] <= sim_time < rapid_compute_buffer[0][1] and rapid_compute_flag:
            for v in vessels:
                v.update_draw_pos()
                
        if rapid_compute_flag and sim_time > rapid_compute_buffer[0][1]:
            rapid_compute_flag = False
            cycle_time = old_cycle_time
            cam_strafe_speed = old_cam_strafe_speed
            cam_rotate_speed = old_cam_rotate_speed
            rapid_compute_buffer.remove(rapid_compute_buffer[0])

        # update physics
        for rp in radiation_pressures:
            rp.update_occultation(bodies)
            rp.update_mass(maneuvers, sim_time, delta_t)
            accel = rp.calc_accel()
            rp.vessel.update_vel(accel, delta_t)
            # do not update vessel position in this 'for' loop, we did not apply all accelerations!

        for ad in atmospheric_drags:
            ad.update_mass(maneuvers, sim_time, delta_t)
            accel = ad.calc_accel()
            ad.vessel.update_vel(accel, delta_t)
            # do not update vessel position in this 'for' loop, we did not apply all accelerations!

        for m in maneuvers:
            # lower delta_t if a maneuver is in progress
            if maneuver_auto_dt and ((delta_t > maneuver_auto_dt and (m.get_state(sim_time) == "Performing" or
               (m.get_state(sim_time) == "Pending" and not m.get_state(sim_time+delta_t) == "Pending")))):
                delta_t = maneuver_auto_dt
                
            m.perform_maneuver(sim_time, delta_t)
        
        for v in vessels:
            accel = [0,0,0]

            for b in bodies:

                if vessel_body_collision and v.get_alt_above(b) <= 0:
                    vessel_body_crash(v, b)
                    
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

            # planets rotate!
            x.update_orient(delta_t)

        # update surface point positions
        for sp in surface_points:
            # this doesn't require a delta_t since it only uses
            # parent body attributes
            sp.update_state_vectors(delta_t)

        # update plots
        for p in plots:
            p.update(sim_time)
            
            # going to display any of the plots?
            if sim_time >= p.get_end_time() and (sim_time - delta_t) < p.get_end_time():
                p.display()

        # update cameras
        for cam in cameras:
            cam.move_with_lock()

        if (int(sim_time) % int(output_rate) < delta_t) and not rapid_compute_flag:

            # update output
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")

            # display what the user wants in cmd/terminal
            print("OrbitSim3D Command Interpreter & Output Display\n")
            if sim_time < 30 * delta_t:
                print("Press C at any time to use the command line or P to open the command panel interface.\n")
            print("Time:", sim_time, "\n")

            for element in output_buffer:

                # relative pos and vel
                if element[1] == "pos_rel":
                    print(element[0], element[2].get_pos_rel_to(find_obj_by_name(element[3])))
                elif element[1] == "vel_rel":
                    print(element[0], element[2].get_vel_rel_to(find_obj_by_name(element[3])))

                # relative pos and vel magnitude
                elif element[1] == "pos_mag_rel":
                    print(element[0], element[2].get_dist_to(find_obj_by_name(element[3])))
                elif element[1] == "vel_mag_rel":
                    print(element[0], element[2].get_vel_mag_rel_to(find_obj_by_name(element[3])))

                # absolute pos and vel
                elif element[1] == "pos":
                    print(element[0], element[2].get_pos())
                elif element[1] == "vel":
                    print(element[0], element[2].get_vel())

                # absolute pos and vel magnitude
                elif element[1] == "pos_mag":
                    print(element[0], mag(element[2].get_pos()))
                elif element[1] == "vel_mag":
                    print(element[0], mag(element[2].get_vel()))

                # altitude
                elif element[1] == "alt":
                    print(element[0], element[2].get_alt_above(find_obj_by_name(element[3])))

                # ground pos
                elif element[1] == "gpos":
                    print(element[0] +
                          "\nLat: " + str(element[2].get_gpos()[0]) + " deg" +
                          "\nLong: " + str(element[2].get_gpos()[1]) + " deg" +
                          "\nAlt: " + str(element[2].get_gpos()[2]) + " m")

                # maneuver state and parameters
                elif element[1] == "active":
                    print(element[0], element[2].is_performing(sim_time))
                elif element[1] == "state":
                    print(element[0], element[2].get_state(sim_time))
                elif element[1] == "params" and element[3] == "m":
                    print(element[0], "\n" + element[2].get_params_str())

                # radiation pressure params
                elif element[1] == "params" and element[3] == "rp":
                    print(element[0], "\n" + element[2].get_params_str())

                # atmospheric drag params
                elif element[1] == "params" and element[3] == "ad":
                    print(element[0], "\n" + element[2].get_params_str())

                # orbit projection parameters
                elif element[1] == "apoapsis":
                    print(element[0], proj.get_apoapsis_alt())
                elif element[1] == "apoapsis_r":
                    print(element[0], proj.get_apoapsis())
                elif element[1] == "periapsis":
                    print(element[0], proj.get_periapsis_alt())
                elif element[1] == "periapsis_r":
                    print(element[0], proj.get_periapsis())
                elif element[1] == "period":
                    print(element[0], proj.get_period())
                elif element[1] == "body":
                    print(element[0], proj.get_body())
                elif element[1] == "vessel":
                    print(element[0], proj.get_vessel())
                elif element[1] == "semimajor_axis":
                    print(element[0], proj.get_semimajor_axis())
                elif element[1] == "eccentricity":
                    print(element[0], proj.eccentricity)
                elif element[1] == "energy":
                    print(element[0], proj.get_energy())
                elif element[1] == "params" and element[3] == "p":
                    print(element[0], "\n" + element[2].get_params_str())
                    
                # note taking
                elif element[1] == "note":
                    print(element[0], element[2])
                
                print("")
                    
            # clear stuff from last frame
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # do the actual drawing

            # drawOrigin() -- maybe it'll be useful for debugging one day
            drawScene(bodies, vessels, surface_points, barycenters, projections, maneuvers, get_active_cam(), show_trajectories, draw_mode, labels_visible)
            glfw.swap_buffers(window)
            
        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < cycle_time:
            time.sleep(cycle_time - cycle_dt)
        elif warn_cycle_time and cycle_time*2 <= cycle_dt and not cycle_time == 0:
            print("Cycle time too low! Machine can't update physics at the given cycle time!\n")
            print("Consider increasing cycle_time to get more consistent calculation rate.\n")

    # destroy OpenGL window and return to menu
    glfw.destroy_window(window)
    init_sim()

def pick_scenario():
    clear_cmd_terminal()

    scenarios_list = glob.glob("scenarios/*.osf")
    scn_max_name_length = 0
    
    for scn in scenarios_list:
        if len(scn) > scn_max_name_length:
            scn_max_name_length = len(scn)
            
    loader_frame_width = max(60, (scn_max_name_length + 6))
    loader_lines = []
    
    num_of_dashes = int(loader_frame_width / 2)
    header_line = "= " * int((num_of_dashes - 5)/2) + " SCENARIOS" + " =" * int((num_of_dashes - 5)/2)
    loader_lines.append(header_line)

    i = 0
    for scn in scenarios_list:
        i += 1
        current_line = "|| " + str(i) + ") " + scn
        loader_lines.append(current_line)

    bottom_line = "= " * int(num_of_dashes)
    loader_lines.append(bottom_line)

    for line in loader_lines:
        print(line)
        time.sleep(0.015)

    print("\nPlease type in the name of the scenario you wish to load.")
    scn_filename = input(" > ")
    return scn_filename
    
def init_sim():
    global initial_run

    # do not run if started from IDLE, it must be
    # run from terminal/command prompt
    if "idlelib" in sys.modules:
        print("OrbitSim3D does not run properly on IDLE Shell!")
        print("Please run this program from the command line/terminal.")
        print("Exiting...")
        return -1
    
    clear_cmd_terminal()

    # on windows, change text color to green because yes
    if os.name == "nt":
        os.system("color a")

    # display icon because it's cool
    icon_stages = []
    for i in range(10):
        icon_stages.append(open("./data/images/anim_icon/" + str(i) + ".txt").readlines())

    # do it slowly the first time
    if initial_run:
        for stage in icon_stages:
            clear_cmd_terminal()
            for line in stage:
                print(line, end="")
            time.sleep(0.015)
            
    # don't bother with eye candy otherwise
    else:
        for line in icon_stages[-1]:
            print(line, end="")

    print("\n")

    for i in range(50):
        sys.stdout.write("= ")
        sys.stdout.flush()
        # this one too
        if initial_run:
            time.sleep(0.005)

    # global variable, yes, I know what I'm doing
    if initial_run:
        time.sleep(0.5)

    initial_run = False
    
    print("\n\nOrbitSim3D Initialization\n")
    print("1) (L)oad Scenario")
    print("2) (S)tart Empty Scene")
    print("3) (C)onfigure OrbitSim3D")

    menu_select = input("\n > ")

    if menu_select == "1" or menu_select.lower() == "l":
        scn_path = pick_scenario()
        
        if scn_path:
            import_scenario(scn_path)
        else:
            init_sim()
            
    elif menu_select == "2" or menu_select.lower() == "s":
        main()

    elif menu_select == "3" or menu_select.lower() == "c":
        configure_sim()
        init_sim()

    # :) do the intro again
    elif menu_select == ":)" or menu_select == ":-)":
        initial_run = True
        init_sim()

    else:
        print("Invalid selection!")
        time.sleep(2)
        init_sim()

init_sim()
