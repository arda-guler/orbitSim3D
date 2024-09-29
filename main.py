# import OpenGL
# from OpenGL.GL import *
# from OpenGL.GLU import *
import pywavefront
import os
import keyboard
import glfw
# import time
import re
# import shutil
import sys
import random
import glob
import ast

from graphics import *
from vessel_class import *
from body_class import *
from camera_class import *
from surface_point_class import *
from barycenter_class import *
# from math_utils import *
from maneuver import *
from orbit import *
from plot import *
from command_panel import *
from config_utils import *
from spherical_harmonics_model import *
from radiation_pressure import *
from atmospheric_drag import *
# from vector3 import *
from solver import *
from proximity import *
from resource import *
from general_relativity import *
from test_propagator import *
from observation import *

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
spherical_harmonics = []
radiation_pressures = []
atmospheric_drags = []
schwarzschilds = []
lensethirrings = []
proximity_zones = []
resources = []
observations = []

starfield = []

batch_commands = []
command_history = []

preset_orientations = ["prograde", "prograde_dynamic", "retrograde", "retrograde_dynamic",
                       "normal", "normal_dynamic", "antinormal", "antinormal_dynamic",
                       "radial_in", "radial_in_dynamic", "radial_out", "radial_out_dynamic",
                       "prograde_tangential", "prograde_tangential_dynamic",
                       "retrograde_tangential", "retrograde_tangential_dynamic"]

sim_time = 0

# these three below are default values, should be changed by main() once the program reads config data
gvar_fov = 70
gvar_near_clip = 0.01
gvar_far_clip = 10E5

def window_resize(window, width, height):
    global gvar_fov, gvar_near_clip, gvar_far_clip, cameras

    try:
        # glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        glLoadIdentity()
        main_cam = cameras[0]
        gluPerspective(gvar_fov, width/height, gvar_near_clip, gvar_far_clip)
        glTranslate(main_cam.pos.x, main_cam.pos.y, main_cam.pos.z)
        main_cam.orient = matrix3x3()
    except ZeroDivisionError:
        # if the window is minimized it makes height = 0, but we don't need to update projection in that case anyway
        pass

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
    global objs, vessels, bodies, projections, maneuvers, surface_points, barycenters, resources,\
           plots, spherical_harmonics, radiation_pressures, atmospheric_drags, schwarzschilds,\
           lensethirrings, observations, sim_time

    objs = []
    vessels = []
    bodies = []
    maneuvers = []
    projections = []
    surface_points = []
    barycenters = []
    resources = []
    plots = []
    spherical_harmonics = []
    radiation_pressures = []
    atmospheric_drags = []
    schwarzschilds = []
    lensethirrings = []
    observations = []
    sim_time = 0

def import_scenario(scn_filename):
    global objs, vessels, bodies, surface_points, maneuvers, barycenters, spherical_harmonics, radiation_pressures,\
           atmospheric_drags, schwarzschilds, lensethirrings, observations, proximity_zones, resources, sim_time

    def construct_point_mass_cloud(pmc_str):
        # this is a bit of an operation unfortunately, but should be more readable to the user
        data_list = ast.literal_eval(pmc_str)
        point_mass_cloud = []

        for pos_lst, scalar in data_list:
            pos = vec3(lst=pos_lst)
            point_mass_cloud.append([pos, scalar])

        return point_mass_cloud

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
            line[5] = eval(line[5])
            line[6] = eval(line[6])
            line[7] = eval(line[7])

            orient_nums = re.findall(r"[-+]?\d*\.\d+|\d+", line[8])
            
            new_body = body(line[1], pywavefront.Wavefront(line[2], collect_faces=True), line[2],
                            float(line[3]), float(line[4]),
                            
                            line[5], vec3(lst=line[6]), vec3(lst=line[7]),
                            
                            matrix3x3([[float(orient_nums[0]), float(orient_nums[1]), float(orient_nums[2])],
                                       [float(orient_nums[3]), float(orient_nums[4]), float(orient_nums[5])],
                                       [float(orient_nums[6]), float(orient_nums[7]), float(orient_nums[8])]]),

                            float(line[9]), # day length
                            
                            vec3(lst=eval(line[10])), # rot axis

                            float(line[11]), # J2

                            float(line[12]), # luminosity

                            float(line[13]), float(line[14]), # atmosphere

                            construct_point_mass_cloud(line[15])) # point-mass-cloud
            
            bodies.append(new_body)
            objs.append(new_body)
            print("Loading body:", new_body.get_name())

        # import vessels
        elif line[0] == "V":
            line[3] = eval(line[3])
            line[4] = eval(line[4])
            line[5] = eval(line[5])
            new_vessel = vessel(line[1], pywavefront.Wavefront(line[2], collect_faces=True), line[2],
                                line[3], vec3(lst=line[4]), vec3(lst=line[5]))
            vessels.append(new_vessel)
            objs.append(new_vessel)
            print("Loading vessel:", new_vessel.get_name())

        # import maneuvers
        elif line[0] == "M":
            if line[2] == "const_accel":
                if line[5] in preset_orientations:
                    new_maneuver = maneuver_const_accel(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                        line[5], float(line[6]), float(line[7]), float(line[8]))
                else:
                    line[5] = eval(line[5])
                    new_maneuver = maneuver_const_accel(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                        vec3(lst=line[5]),
                                                        float(line[6]), float(line[7]), float(line[8]))
                    
            elif line[2] == "const_thrust":
                if line[5] in preset_orientations:
                    new_maneuver = maneuver_const_thrust(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                         line[5], float(line[6]), float(line[7]), float(line[8]),
                                                         float(line[9]), float(line[10]))
                else:
                    line[5] = eval(line[5])
                    new_maneuver = maneuver_const_thrust(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                         vec3(lst=line[5]),
                                                         float(line[6]), float(line[7]), float(line[8]),
                                                         float(line[9]), float(line[10]))

            elif line[2] == "impulsive":
                if line[5] in preset_orientations:
                    new_maneuver = maneuver_impulsive(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                      line[5], float(line[6]), float(line[7]))
                else:
                    line[5] = eval(line[5])
                    new_maneuver = maneuver_impulsive(line[1], find_obj_by_name(line[3]), find_obj_by_name(line[4]),
                                                      vec3(lst=line[5]), float(line[6]), float(line[7]))

            maneuvers.append(new_maneuver)
            print("Loading maneuver:", new_maneuver.get_name())

        # import surface points
        elif line[0] == "S":
            line[3] = eval(line[3]) # color
            line[4] = eval(line[4]) # gpos
            new_sp = surface_point(line[1], find_obj_by_name(line[2]), line[3], line[4])

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

        # include spherical harmonics data
        elif line[0] == "SH":
            new_sh = spherical_harmonics_model(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]), line[4])
            spherical_harmonics.append(new_sh)
            print("Loading spherical harmonics:", new_sh.get_name())

        # import radiation pressure data
        elif line[0] == "R":
            if line[6] in preset_orientations:
                new_rp = radiation_pressure(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                            float(line[4]), find_obj_by_name(line[5]), line[6], float(line[7]), int(line[8]))
            else:
                line[6] = eval(line[6])
                new_rp = radiation_pressure(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                            float(line[4]), find_obj_by_name(line[5]), vec3(lst=line[6]),
                                            float(line[7]), int(line[8]))

            radiation_pressures.append(new_rp)
            print("Loading radiation pressure:", new_rp.get_name())

        # import atmospheric drag data
        elif line[0] == "A":
            new_ad = atmospheric_drag(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]),
                                      float(line[4]), float(line[5]), float(line[6]), int(line[7]))

            atmospheric_drags.append(new_ad)
            print("Loading atmospheric drag:", new_ad.get_name())

        # import proximity zone data
        elif line[0] == "P":
            new_pz = proximity_zone(line[1], find_obj_by_name(line[2]), float(line[3]), float(line[4]))
            proximity_zones.append(new_pz)
            print("Loading proximity zone:", new_pz.name)

        # import resource data
        elif line[0] == "U":
            new_res = resource(line[1], float(line[2]), line[3], line[4], find_obj_by_name(line[5]), find_obj_by_name(line[6]), eval(line[7]), eval(line[8]))
            resources.append(new_res)
            print("Loading resource:", new_res.name)

        # import Schwarzschild effect data
        elif line[0] == "GR0":
            new_sch = GR_Schwarzschild(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]))
            schwarzschilds.append(new_sch)
            print("Loading Schwarzschild effect:", new_sch.name)

        # import Lense-Thirring effect data
        elif line[0] == "GR1":
            new_lt = GR_LenseThirring(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]), eval(line[4]))
            lensethirrings.append(new_lt)
            print("Loading Lense-Thirring effect:", new_lt.name)

        elif line[0] == "OBS":
            new_obs = observation(line[1], find_obj_by_name(line[2]), find_obj_by_name(line[3]))
            observations.append(new_obs)
            print("Loading observation:", new_obs.name)
            
    main(scn_filename, start_time)

def export_scenario(scn_filename, verbose=True):
    global objs, vessels, bodies, surface_points, maneuvers, barycenters, resources, spherical_harmonics,\
           radiation_pressures, atmospheric_drags, schwarzschilds, lensethirrings, observations,\
           proximity_zones, sim_time, command_history

    os.makedirs("scenarios/", exist_ok=True)

    scn_filename = "scenarios/" + scn_filename
    if not scn_filename.endswith(".osf"):
        scn_filename += ".osf"

    if verbose:
        clear_cmd_terminal()
        print("Saving scenario into " + scn_filename)
        
    with open(scn_filename, "w") as scn_file:
        print("Writing header...")
        header_string = """
;.osf -- orbitSim3D scenario format
; This scenario was exported by orbitSim3D.
;= = = = = = = = = =\n
"""
                         
        scn_file.write(header_string)

        if verbose:
            print("Writing simulation time...")
        time_save_string = "T|" + str(sim_time) + "\n"
        scn_file.write(time_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing bodies...")
        for b in bodies:
            body_save_string = "B|" + b.get_name() + "|" + b.get_model_path() + "|" + str(b.get_mass()) + "|" +\
                               str(b.get_radius()) + "|" + str(b.get_color()) + "|" + str(b.get_pos().tolist()) + "|" +\
                               str(b.get_vel().tolist()) + "|" + str(b.get_orient().tolist()) + "|" + str(b.get_day_length()) + "|" + str(b.get_rot_axis().tolist()) + "|" +\
                               str(b.get_J2()) + "|" + str(b.luminosity) + "|" + str(b.atmos_sea_level_density) + "|" +\
                               str(b.atmos_scale_height) + "|" + b.pmc_to_str() + "\n"
            scn_file.write(body_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing vessels...")
        for v in vessels:
            vessel_save_string = "V|" + v.get_name() + "|" + v.get_model_path() + "|" + str(v.get_color()) + "|" +\
                                 str(v.get_pos().tolist()) + "|" + str(v.get_vel().tolist()) + "\n"
            scn_file.write(vessel_save_string)

        scn_file.write("\n")

        if verbose:
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

            elif m.get_type() == "impulsive":
                maneuver_save_string += "impulsive|" + m.get_vessel().get_name() + "|" + m.frame_body.get_name() + "|" +\
                                        str(m.orientation_input) + "|" + str(m.delta_v) + "|" + str(m.t_perform) + "\n"
            scn_file.write(maneuver_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing surface points...")
        for s in surface_points:
            sp_save_string = "S|" + s.get_name() + "|" + s.get_body().get_name() + "|" + str(s.get_color()) + "|" + str(s.get_gpos()) + "\n"
            scn_file.write(sp_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing barycenters...")
        for bc in barycenters:
            bc_save_string = "C|" + bc.get_name() + "|"
            for b in bc.get_bodies():
                bc_save_string += b.get_name() + ","
            bc_save_string = bc_save_string[:-1]+"\n"
            scn_file.write(bc_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing resources...")
        for res in resources:
            res_save_string = "U|" + res.get_name() + "|" + str(res.value) + "|" + res.equation + "|" + res.variable + "|" + res.obj1.name + "|" + res.obj2.name + "|" + str(res.coeffs) + "|" + str(res.limits) + "\n"
            scn_file.write(res_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing spherical harmonics...")
        for sh in spherical_harmonics:
            sh_save_string = "SH|" + sh.get_name() + "|" + sh.vessel.get_name() + "|" + sh.body.get_name() + "|" + sh.filepath + "\n"
            scn_file.write(sh_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing radiation pressures...")
        for rp in radiation_pressures:
            rp_save_string = "R|" + rp.get_name() + "|" + rp.vessel.get_name() + "|" + rp.body.get_name() + "|" + str(rp.get_area()) +\
                             "|" + rp.orientation_frame.get_name() + "|" + str(rp.direction_input) + "|" + str(rp.mass) + "|" + str(rp.mass_auto_update) + "\n"
            scn_file.write(rp_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing atmospheric drags...")
        for ad in atmospheric_drags:
            ad_save_string = "A|" + ad.get_name() + "|" + ad.vessel.get_name() + "|" + ad.body.get_name() + "|" + str(ad.get_area()) +\
                             "|" + str(ad.get_drag_coeff()) + "|" + str(ad.get_mass()) + "|" + str(ad.mass_auto_update) + "\n"
            scn_file.write(ad_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing proximity zones...")
        for pz in proximity_zones:
            pz_save_string = "P|" + pz.name + "|" + pz.vessel.get_name() + "|" + str(pz.vessel_size) + "|" + str(pz.zone_size) + "\n"
            scn_file.write(pz_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing Schwarzschild effects...")
        for sch in schwarzschilds:
            sch_save_string = "GR0|" + sch.name + "|" + sch.body.get_name() + "|" + sch.vessel.get_name() + "\n"
            scn_file.write(sch_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing Lense-Thirring effects...")
        for lt in lensethirrings:
            lt_save_string = "GR1|" + lt.name + "|" + lt.body.get_name() + "|" + lt.vessel.get_name() + "|" + str(lt.J) + "\n"
            scn_file.write(lt_save_string)

        scn_file.write("\n")

        if verbose:
            print("Writing observation setups...")
        for obs in observations:
            obs_save_string = "OBS|" + obs.name + "|" + obs.observer.get_name() + "|" + obs.obj.get_name() + "|" + str(obs.axes[0].tolist()).replace(" ", "") + "|" + str(obs.axes[1].tolist()).replace(" ", "") + "|" + str(obs.axes[2].tolist()).replace(" ", "") + "\n"
            scn_file.write(obs_save_string)

        scn_file.write("\n")

        if verbose:
            print("Scenario export complete!")
            time.sleep(2)

    # Export commands
    if command_history:
        if verbose:
            print("Saving command history into " + scn_filename[:-4] + "_cmdhist.obf")
            
        with open(scn_filename[:-4] + "_cmdhist.obf", "w") as cmd_file:
            for cmd in command_history:
                cmd_file.write(' '.join(cmd) + "\n")

        if verbose:
            print("Command history export complete!")
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

def create_maneuver_impulsive(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_deltav, mnv_t_perform):
    global maneuvers

    if find_maneuver_by_name(mnv_name):
        print("A maneuver with this name already exists. Please pick another name for the new maneuver.\n")
        input("Press Enter to continue...")
        return

    new_maneuver = maneuver_impulsive(mnv_name, mnv_vessel, mnv_frame, mnv_orientation, mnv_deltav, mnv_t_perform)
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

def create_spherical_harmonics(sh_name, sh_vessel, sh_body, sh_filepath):
    global spherical_harmonics

    if find_spherical_harmonics_by_name(sh_name):
        print("A spherical harmonics model with this name already exists. Please pick another name for the new model.\n")
        input("Press Enter to continue...")
        return

    new_sh = spherical_harmonics_model(sh_name, sh_vessel, sh_body, sh_filepath)
    spherical_harmonics.append(new_sh)

def remove_spherical_harmonics(sh_name):
    global spherical_harmonics

    sh = find_spherical_harmonics_by_name(sh_name)

    if not sh:
        print("Spherical harmonics model not found!")
        time.sleep(2)
        return

    spherical_harmonics.remove(sh)
    del sh

def find_spherical_harmonics_by_name(sh_name):
    global spherical_harmonics

    result = None

    for sh in spherical_harmonics:
        if sh.name == sh_name:
            result = sh
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

    if type(pos) == list:
        pos = vec3(lst=pos)

    if type(vel) == list:
        vel = vec3(lst=vel)

    try:
        new_vessel = vessel(name, model, model_path, color, pos, vel)
    except:
        print("Could not create vessel:", name)
        time.sleep(3)
        return
        
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
        
        fragment_vel = vec3(lst=[vessel.get_vel().x + random.uniform(-vel_of_frags, vel_of_frags),
                                 vessel.get_vel().y + random.uniform(-vel_of_frags, vel_of_frags),
                                 vessel.get_vel().z + random.uniform(-vel_of_frags, vel_of_frags)])

        fragment_pos = vessel.get_pos()
        
        create_vessel(vessel_name + "_frag_" + str(i), "fragment", vessel.get_color(), fragment_pos, fragment_vel)

def delete_vessel(name):
    global vessels, objs, proximity_zones
    vessel_tbd = find_obj_by_name(name)

    if not vessel_tbd:
        print("Object not found!")
        time.sleep(2)
        return

    for pz in proximity_zones:
        if vessel_tbd == pz.vessel:
            delete_proximity_zone(pz.name)

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
    current_pos = vec3(0, 0, 0)
    result_obj = None
    
    if point.get_pos:
        current_pos = point.get_pos()
    else:
        current_pos = point

    min_dist = None
    for obj in objs:
        current_dist = ((obj.get_pos().x - current_pos.x)**2 + (obj.get_pos().y - current_pos.y)**2 + (obj.get_pos().z - current_pos.z)**2)**0.5
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

        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "Velocity of " + obj1_name + " rel to " + obj2_name, [],
                            obj1, obj2, "vel_mag", start_time, end_time)

        else:
            new_plot = plot(name, "Time", [], "Velocity of " + obj1_name, [],
                            obj1, None, "vel_mag", start_time, end_time)

    elif variable == "groundtrack":
        obj1 = find_obj_by_name(obj1_name)
        obj2 = find_obj_by_name(obj2_name)
        new_plot = plot(name, "Longitude", [], "Latitude", [], obj1, obj2, "groundtrack",
                        start_time, end_time)

    elif variable == "pos_x":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "X Position of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "pos_x", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "X Position of " + obj1_name, [],
                            obj1, None, "pos_x", start_time, end_time)

    elif variable == "pos_y":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "Y Position of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "pos_y", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "Y Position of " + obj1_name, [],
                            obj1, None, "pos_y", start_time, end_time)

    elif variable == "pos_z":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "Z Position of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "pos_z", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "Z Position of " + obj1_name, [],
                            obj1, None, "pos_z", start_time, end_time)

    elif variable == "vel_x":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "X Velocity of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "vel_x", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "X Velocity of " + obj1_name, [],
                            obj1, None, "vel_x", start_time, end_time)

    elif variable == "vel_y":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "Y Velocity of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "vel_y", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "Y Velocity of " + obj1_name, [],
                            obj1, None, "vel_y", start_time, end_time)

    elif variable == "vel_z":
        obj1 = find_obj_by_name(obj1_name)
        if not obj2_name == "None":
            obj2 = find_obj_by_name(obj2_name)
            new_plot = plot(name, "Time", [], "Z Velocity of " + obj1_name + " rel. to " + obj2_name, [],
                            obj1, obj2, "vel_z", start_time, end_time)
        else:
             new_plot = plot(name, "Time", [], "Z Velocity of " + obj1_name, [],
                            obj1, None, "vel_z", start_time, end_time)

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

def find_proximity_zone_by_name(pz_name):
    global proximity_zones

    for pz in proximity_zones:
        if pz.name == pz_name:
            return pz

    return None

def create_proximity_zone(pz_name, vessel, vessel_size, zone_size):
    global proximity_zones

    if find_proximity_zone_by_name(pz_name):
        print("A proximity zone with this name already exists. Please pick another name for the new proximity zone.\n")
        input("Press Enter to continue...")
        return

    try:
        new_pz = proximity_zone(pz_name, vessel, vessel_size, zone_size)
        proximity_zones.append(new_pz)
    except:
        print("Could not create new proximity zone:", pz_name)

def delete_proximity_zone(pz_name):
    global proximity_zones
    pz_tbd = find_proximity_zone_by_name(pz_name)

    if not pz_tbd:
        print("Proximity zone not found!")
        time.sleep(2)
        return

    proximity_zones.remove(pz_tbd)
    del pz_tbd

def find_resource_by_name(res_name):
    global resources

    for res in resources:
        if res.name == res_name:
            return res

    return None

def create_resource(res_name, value, equation, variable, obj1, obj2, coeffs, limits):
    global resources

    if find_resource_by_name(res_name):
        print("A resource with this name already exists. Please pick another name for the new resource.\n")
        input("Press Enter to continue...")
        return

    try:
        new_res = resource(res_name, value, equation, variable, obj1, obj2, coeffs, limits)
        resources.append(new_res)
    except:
        print("Could not create new resource:", res_name)

def delete_resource(res_name):
    global resources
    res_tbd = find_resource_by_name(res_name)

    if not res_tbd:
        print("Resource not found!")
        time.sleep(2)
        return

    resources.remove(res_tbd)
    del res_tbd

def find_schwarzschild_by_name(sch_name):
    global schwarzschilds

    for sch in schwarzschilds:
        if sch.name == sch_name:
            return sch

    return None

def create_schwarzschild(sch_name, body, vessel):
    global schwarzschilds

    if find_schwarzschild_by_name(sch_name):
        print("A Schwarzschild effect with this name already exists. Please pick another name for the new effect.\n")
        input("Press Enter to continue...")
        return

    try:
        new_sch = GR_Schwarzschild(sch_name, body, vessel)
        schwarzschilds.append(new_sch)
    except:
        print("Could not create new Schwarzschild effect:", sch_name)

def delete_schwarzschild(sch_name):
    global schwarzschilds
    sch_tbd = find_schwarzschild_by_name(sch_name)

    if not sch_name:
        print("Schwarzschild effect not found!")
        time.sleep(2)
        return

    schwarzschilds.remove(sch_tbd)
    del sch_tbd

def find_lensethirring_by_name(lt_name):
    global lensethirrings

    for lt in lensethirrings:
        if lt.name == lt_name:
            return lt

    return None

def create_lensethirring(lt_name, body, vessel, J):
    global lensethirrings

    if find_lensethirring_by_name(lt_name):
        print("A Lense-Thirring effect with this name already exists. Please pick another name for the new effect.\n")
        input("Press Enter to continue...")
        return

    try:
        new_lt = GR_LenseThirring(lt_name, body, vessel, J)
        lensethirrings.append(new_lt)
    except:
        print("Could not create new Lense-Thirring effect:", lt_name)

def delete_lensethirring(lt_name):
    global lensethirrings
    lt_tbd = find_lensethirring_by_name(lt_name)

    if not lt_name:
        print("Lense-Thirring effect not found!")
        time.sleep(2)
        return

    lensethirrings.remove(lt_tbd)
    del lt_tbd

def find_observation_by_name(obs_name):
    global observations

    for obs in observations:
        if obs.name == obs_name:
            return obs

    return None

def create_observation(obs_name, observer, target, axes=[vec3(1, 0, 0), vec3(0, 1, 0), vec3(0, 0, 1)]):
    global observations
    
    if find_observation_by_name(obs_name):
        print("An observation by this name already exists. Please pick a new name for the new observation.")
        input("Press Enter to continue...")
        return

    try:
        new_obs = observation(obs_name, observer, target, axes)
        observations.append(new_obs)
    except:
        print("Could not create new observation:", obs_name)

def delete_observation(obs_name):
    global observations
    obs_tbd = find_observation_by_name(obs_name)

    if not obs_tbd:
        print("Observation not found!")
        time.sleep(2)
        return

    observations.remove(obs_tbd)
    del obs_tbd

def vessel_body_crash(v, b):
    # a vessel has crashed into a celestial body. We will convert the vessel object
    # into a surface point on the body (a crash site) and remove all references to
    # the vessel object
    global maneuvers, surface_points, plots, proximity_zones, batch_commands

    for m in maneuvers:
        if m.vessel == v or m.frame_body == v:
            delete_maneuver(m.name)

    for p in plots:
        if p.obj1 == v or p.obj2 == v:
            p.display()
            delete_plot(p.title)

    for pz in proximity_zones:
        if pz.vessel == v:
            delete_proximity_zone(pz.name)

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
        import sys, termios  # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def get_active_cam():
    global cameras

    for cam in cameras:
        if cam.active:
            return cam

    # just a fail-safe
    return cameras[0]

def rotate_scene(pivot, target, dt):
    global vessels, bodies, objs, observations, projections, starfield

    # get the rotation vector
    rotation_vector = vec3()
    if type(target) == type(vec3()):
        rotation_vector = target
        theta = rotation_vector.mag() * dt
    else:
        if pivot:
            dx = target.pos.x - pivot.pos.x
            dz = target.pos.z - pivot.pos.z
        else:
            dx = target.pos.x
            dz = target.pos.z

        theta = math.atan2(dx, dz)

    base_mtx = matrix3x3()
    rot_mtx = base_mtx.rotated(theta, vec3(0, 1, 0))

    for o in objs:
        o.pos = rot_mtx.dot(o.pos)
        o.vel = rot_mtx.dot(o.vel)

    for b in bodies:
        b.orient = b.orient.rotated(theta, vec3(0, -1, 0))

    for p in projections:
        for i, dv in enumerate(p.draw_vertices):
            p.draw_vertices[i] = rot_mtx.dot(dv)

        p.draw_ap = rot_mtx.dot(p.draw_ap)
        p.draw_pe = rot_mtx.dot(p.draw_pe)
        p.draw_an = rot_mtx.dot(p.draw_an)
        p.draw_dn = rot_mtx.dot(p.draw_dn)

    # keep observation axes locked to stars
    for obs in observations:
        for i_vec in range(3):
            obs.axes[i_vec] = rot_mtx.dot(obs.axes[i_vec])

    for idx_s in range(len(starfield)):
        starfield[idx_s] = rot_mtx.dot(vec3(lst=starfield[idx_s])).tolist()

def generate_starfield(N_stars):
    global starfield
    PI = 3.14159265358979323846264338327950288

    starfield = []

    for i in range(N_stars):
        RA = random.uniform(0, 2 * PI)
        DEC = math.asin(random.uniform(-1, 1))

        x = math.cos(RA) * math.cos(DEC)
        y = math.sin(DEC)
        z = math.sin(RA) * math.cos(DEC)

        starfield.append([x, y, z])

def clear_starfield():
    global starfield
    starfield = []

def main(scn_filename=None, start_time=0):
    global vessels, bodies, surface_points, projections, objs, sim_time, batch_commands, command_history,\
           plots, resources, cameras, barycenters, spherical_harmonics, radiation_pressures, atmospheric_drags,\
           proximity_zones, schwarzschilds, lensethirrings, observations, gvar_fov, gvar_near_clip, gvar_far_clip,\
           starfield

    # read config to get start values
    sim_time, delta_t, cycle_time, output_rate, cam_pos_x, cam_pos_y, cam_pos_z, cam_strafe_speed, cam_rotate_speed,\
    window_x, window_y, fov, near_clip, far_clip, cam_yaw_right, cam_yaw_left, cam_pitch_down, cam_pitch_up, cam_roll_cw, cam_roll_ccw,\
    cam_strafe_left, cam_strafe_right, cam_strafe_forward, cam_strafe_backward, cam_strafe_up, cam_strafe_down, cam_increase_speed, cam_decrease_speed, warn_cycle_time,\
    maneuver_auto_dt, draw_mode, point_size, labels_visible, pmcs_visible, vessel_body_collision, batch_autoload, solver_type, tolerance,\
    default_star_num, autostarfield = read_current_config()

    # set global vars
    gvar_fov = fov
    gvar_near_clip = near_clip
    gvar_far_clip = far_clip

    # initializing glfw
    glfw.init()

    # creating a window
    window = glfw.create_window(int(window_x), int(window_y), "OrbitSim3D", None, None)
    glfw.set_window_pos(window, 100, 100)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    
    gluPerspective(fov, int(window_x)/int(window_y), near_clip, far_clip)
    glEnable(GL_CULL_FACE)
    glPointSize(point_size)

    main_cam = camera("main_cam", vec3(cam_pos_x, cam_pos_y, cam_pos_z), matrix3x3(), True)
    cameras = [main_cam]
    # put "camera" in starting position
    glTranslate(main_cam.get_pos().x, main_cam.get_pos().y, main_cam.get_pos().z)

    command_history = []
    batch_commands = []
    timed_commands = []
    output_buffer = []
    auto_dt_buffer = []
    rapid_compute_buffer = []
    rapid_compute_flag = False
    show_trajectories = True
    scene_lock = None
    scene_rot_target = None
    accept_keyboard_input = True
    speed_input_locked = False
    grid_active = False
    polar_grid_active = False
    cycle_dt = 1

    if autostarfield:
        generate_starfield(default_star_num)

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
        glfw.poll_events()

        frame_command = False

        if (not accept_keyboard_input) and len(batch_commands) < 1:
            if keyboard.is_pressed("CTRL+L"):
                accept_keyboard_input = True

        else:
            
            if accept_keyboard_input:
                # get input and move the "camera" around

                # don't allow rotation on multiple axes at once because the orientation matrix screws up
                if keyboard.is_pressed(cam_pitch_down):
                    get_active_cam().rotate([cam_rotate_speed*cycle_dt,0,0])
                elif keyboard.is_pressed(cam_pitch_up):
                    get_active_cam().rotate([-cam_rotate_speed*cycle_dt,0,0])

                elif keyboard.is_pressed(cam_yaw_left):
                    get_active_cam().rotate([0, cam_rotate_speed*cycle_dt,0])
                elif keyboard.is_pressed(cam_yaw_right):
                    get_active_cam().rotate([0, -cam_rotate_speed*cycle_dt,0])

                elif keyboard.is_pressed(cam_roll_ccw):
                    get_active_cam().rotate([0,0,cam_rotate_speed*cycle_dt])
                elif keyboard.is_pressed(cam_roll_cw):
                    get_active_cam().rotate([0,0,-cam_rotate_speed*cycle_dt])

                get_active_cam().move(vec3(lst=[(keyboard.is_pressed(cam_strafe_left) - keyboard.is_pressed(cam_strafe_right)) * cam_strafe_speed * cycle_dt,
                                                (keyboard.is_pressed(cam_strafe_down) - keyboard.is_pressed(cam_strafe_up)) * cam_strafe_speed * cycle_dt,
                                                (keyboard.is_pressed(cam_strafe_forward) - keyboard.is_pressed(cam_strafe_backward)) * cam_strafe_speed * cycle_dt]))

                # adjust camera speed via hotkey
                if not speed_input_locked and keyboard.is_pressed(cam_increase_speed):
                    cam_strafe_speed *= 2
                    speed_input_locked = True

                elif not speed_input_locked and keyboard.is_pressed(cam_decrease_speed):
                    cam_strafe_speed *= 0.5
                    speed_input_locked = True

                if speed_input_locked and (not keyboard.is_pressed(cam_increase_speed) and not keyboard.is_pressed(cam_decrease_speed)):
                    speed_input_locked = False

                # get command line/panel request
                if keyboard.is_pressed("c") and not rapid_compute_flag:
                    frame_command = True

                elif keyboard.is_pressed("p") and not rapid_compute_flag:
                    panel_commands = use_command_panel(vessels, bodies, surface_points, barycenters, maneuvers, spherical_harmonics, radiation_pressures, atmospheric_drags, schwarzschilds, lensethirrings,
                                                       proximity_zones, projections, resources, observations, plots, auto_dt_buffer, sim_time, delta_t, cycle_time, output_rate, cam_strafe_speed,
                                                       cam_rotate_speed, rapid_compute_buffer, scene_lock, scene_rot_target, solver_type, tolerance, starfield, default_star_num)
                    if panel_commands:
                        for panel_command in panel_commands:
                            panel_command = panel_command.split(" ")
                            batch_commands.append(panel_command)

            if frame_command or len(batch_commands) > 0 or len(timed_commands) > 0:
                flush_input()

                if frame_command:
                    command = input("\n > ")
                    command = command.split(" ")
                    command[0] = command[0].lower()

                # --- COMMAND INTERPRETER ---
                if len(timed_commands) > 0 and timed_commands[0][0] <= sim_time:
                    command = timed_commands[0][1]
                    timed_commands.remove(timed_commands[0])

                elif len(batch_commands) > 0 and (not frame_command or command[0] == "batch"):
                    command = batch_commands[0]
                    batch_commands.remove(command)

                # timed command
                if command[0].startswith("t="):
                    timed_commands.append([float(command[0][2:]), command[1:]])
                    timed_commands = sorted(timed_commands)

                # BATCH command
                elif command[0] == "batch":
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
                            
                            elif command[2] == "horizon_angle":
                                if find_surface_point_by_name(command[3]) and find_obj_by_name(command[1]):
                                    output_buffer.append([command[4], "horizon_angle", find_surface_point_by_name(command[3]), find_obj_by_name(command[1])])
                                    
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

                        elif find_resource_by_name(command[1]):
                            res = find_resource_by_name(command[1])
                            output_buffer.append([command[3], command[2], res, "res"])
                                
                        else:
                            print("Object/maneuver/projection not found.")
                            time.sleep(2)

                    elif len(command) == 3:
                        if find_observation_by_name(command[1]):
                            obs = find_observation_by_name(command[1])
                            output_buffer.append([command[2], "params", obs, "obs"])

                        elif find_spherical_harmonics_by_name(command[1]):
                            sh = find_spherical_harmonics_by_name(command[1])
                            output_buffer.append([command[2], "params", sh, "sh"])

                        else:
                            print("Observation not found.")
                            time.sleep(2)

                    elif len(command) == 2:
                        if command[1] == "traj":
                            show_trajectories = True
                        elif command[1] == "labels":
                            labels_visible = 1
                        elif command[1] == "pmcs":
                            pmcs_visible = 1
                        elif command[1] == "grid":
                            grid_active = True
                        elif command[1] == "polar_grid":
                            polar_grid_active = True

                    else:
                        print("Wrong number of arguments for command 'show'.")
                        time.sleep(2)

                # HIDE command
                elif command[0] == "hide":
                    if command[1] == "traj":
                        show_trajectories = False
                    elif command[1] == "labels":
                        labels_visible = 0
                    elif command[1] == "pmcs":
                        pmcs_visible = 0
                    elif command[1] == "grid":
                        grid_active = False
                    elif command[1] == "polar_grid":
                        polar_grid_active = False
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

                # LOCK_ORIGIN command
                elif command[0] == "lock_origin":
                    scene_lock = find_obj_by_name(command[1])
                    for v in vessels:
                        v.clear_draw_traj_history() # so we don't get odd "jumps" in the trajectory trails

                # LOCK_SCENE_ROT command
                elif command[0] == "lock_scene_rot":
                    scene_rot_target = find_obj_by_name(command[1])
                    if not scene_rot_target:
                        scene_rot_target = vec3(0, 1, 0) * float(command[1])

                # UNLOCK_ORIGIN command
                elif command[0] == "unlock_origin":
                    scene_lock = None

                # UNLOCK_SCENE_ROT command
                elif command[0] == "unlock_scene_rot":
                    scene_rot_target = None

                # GENERATE_STARFIELD command
                elif command[0] == "generate_starfield":
                    if len(command) >= 2:
                        generate_starfield(int(command[1]))
                    else:
                        generate_starfield(1000)

                # CLEAR_STARFIELD command
                elif command[0] == "clear_starfield":
                    clear_starfield()

                # CREATE_VESSEL command
                elif command[0] == "create_vessel":
                    if len(command) == 6:
                        create_vessel(command[1], command[2], eval(command[3]), eval(command[4]), eval(command[5]))

                    elif len(command) == 7:
                        # TO DO - SPHERICAL VELOCITY INPUT
                        parent_pos = find_obj_by_name(command[4]).get_pos()
                        
                        vessel_offset_from_parent = spherical2cartesian(eval(command[5]))
                        
                        create_vessel(command[1], command[2], eval(command[3]),
                                      parent_pos + vessel_offset_from_parent,
                                      eval(command[6]))
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
                        if not command[5] in preset_orientations:
                            create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                            
                                                        vec3(lst=eval(command[5])),
                                            
                                                        float(command[6]), float(command[7]), float(command[8]))
                        else:
                            create_maneuver_const_accel(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                            
                                                        command[5],
                                            
                                                        float(command[6]), float(command[7]), float(command[8]))
                    elif len(command) == 11 and command[2] == "const_thrust":
                        # name, type, vessel, frame, orientation, thrust, mass_init, mass_flow, start, duration
                        if not command[5] in preset_orientations:
                            create_maneuver_const_thrust(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),

                                                         vec3(lst=eval(command[5])),

                                                         float(command[6]), float(command[7]), float(command[8]),
                                                         float(command[9]), float(command[10]))
                        else:
                            create_maneuver_const_thrust(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),

                                                         command[5],

                                                         float(command[6]), float(command[7]), float(command[8]),
                                                         float(command[9]), float(command[10]))

                    elif len(command) == 8 and command[2] == "impulsive":
                        # name, type, vessel, frame, orientation, delta_v, perform_time
                        if not command[5] in preset_orientations:
                            create_maneuver_impulsive(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                                      vec3(lst=eval(command[5])), float(command[6]), float(command[7]))
                        else:
                            create_maneuver_impulsive(command[1], find_obj_by_name(command[3]), find_obj_by_name(command[4]),
                                                      command[5], float(command[6]), float(command[7]))
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

                # CREATE_SPHERICAL_HARMONICS command
                elif command[0] == "create_spherical_harmonics":
                    if len(command) == 5:
                        create_spherical_harmonics(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]), command[4])
                    else:
                        print("Wrong number of arguments for command 'create_spherical_harmonics'.\n")
                        time.sleep(2)

                # REMOVE_SPHERICAL_HARMONICS command
                elif command[0] == "remove_spherical_harmonics":
                    remove_spherical_harmonics(command[1])

                # GET_SPHERICAL_HARMONICS command
                elif command[0] == "get_spherical_harmonics":
                    print("Spherical harmonics models currently in simulation:")
                    for sh in spherical_harmonics:
                        print(sh.name)
                    input("Press Enter to continue...")

                # APPLY_RADIATION_PRESSURE command
                elif command[0] == "apply_radiation_pressure":
                    if len(command) == 9:
                        if command[6] in preset_orientations:
                            apply_radiation_pressure(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                                     float(command[4]), find_obj_by_name(command[5]), command[6], float(command[7]), int(command[8]))
                        else:
                            apply_radiation_pressure(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                                     float(command[4]), find_obj_by_name(command[5]),
                                                     eval(command[6]),
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

                # CREATE_PROXIMITY_ZONE
                elif command[0] == "create_proximity_zone":
                    if len(command) == 5:
                        create_proximity_zone(command[1], find_obj_by_name(command[2]), float(command[3]), float(command[4]))
                    elif len(command) == 4:
                        create_proximity_zone(command[1], find_obj_by_name(command[2]), float(command[3]), float(command[3]) * 10)
                    elif len(command) == 3:
                        create_proximity_zone(command[1], find_obj_by_name(command[2]), 10, 100)
                    else:
                        print("Wrong number of arguments for command 'create_proximity_zone'.\n")
                        time.sleep(2)

                # DELETE_PROXIMITY_ZONE
                elif command[0] == "delete_proximity_zone":
                    delete_proximity_zone(command[1])

                # GET_PROXIMITY_ZONES
                elif command[0] == "get_proximity_zones":
                    print("\nProximity zones currently in simulation:\n")
                    for pz in proximity_zones:
                        print("PROX ZONE:", pz.name, "around VESSEL:", pz.vessel.name)
                        print("Zone size:", pz.zone_size, "Vessel size:", pz.vessel_size, "\n")

                    input("Press Enter to continue...")

                # CREATE_RESOURCE
                elif command[0] == "create_resource":
                    create_resource(command[1], float(command[2]), command[3], command[4],
                                    find_obj_by_name(command[5]), find_obj_by_name(command[6]), eval(command[7]),
                                    eval(command[8]))

                # DELETE_RESOURCE
                elif command[0] == "delete_resource":
                    delete_resource(command[1])

                # GET_RESOURCES
                elif command[0] == "get_resources":
                    print("Resources currently in simulation:\n")
                    for res in resources:
                        print(res.name)
                    input("Press Enter to continue...")

                # CREATE_SCHWARZSCHILD
                elif command[0] == "create_schwarzschild":
                    create_schwarzschild(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]))

                # DELETE_SCHWARZSCHILD
                elif command[0] == "delete_schwarzschild":
                    delete_schwarzschild(command[1])

                # GET_SCHWARZSCHILDS
                elif command[0] == "get_schwarzschilds":
                    print("Schwarzschild effects currently in simulation:\n")
                    for sch in schwarzschilds:
                        print(sch.name)
                    input("Press Enter to continue...")

                # CREATE_LENSETHIRRING
                elif command[0] == "create_lensethirring":
                    create_lensethirring(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]), eval(command[4]))

                # DELETE_LENSETHIRRING
                elif command[0] == "delete_lensethirring":
                    delete_lensethirring(command[1])

                # GET_LENSETHIRRINGS
                elif command[0] == "get_lensethirrings":
                    print("Lense-Thirring effects currently in simulation:\n")
                    for lt in lensethirrings:
                        print(lt.name)
                    input("Press Enter to continue...")

                # CREATE_OBSERVATION
                elif command[0] == "create_observation":
                    if len(command) == 7:
                        create_observation(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]),
                                           vec3(lst=eval(command[4])), vec3(lst=eval(command[5])), vec3(lst=eval(command[6])))
                    else:
                        create_observation(command[1], find_obj_by_name(command[2]), find_obj_by_name(command[3]))

                # DELETE_OBSERVATION
                elif command[0] == "delete_observation":
                    delete_observation(command[1])

                # GET_OBSERVATIONS
                elif command[0] == "get_observations":
                    print("Observation setups currently in simulation:")
                    for obs in observations:
                        print(obs.name)
                    input("Press Enter to continue...")

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
                    input("Press Enter to continue...")

                # AUTO_DT_CLEAR command
                elif command[0] == "auto_dt_clear":
                    auto_dt_buffer = []

                # GET_TIMED_COMMANDS command
                elif command[0] == "get_timed_commands":
                    print(timed_commands)
                    input("Press Enter to continue...")

                # TIMED_COMMANDS_REMOVE command
                elif command[0] == "timed_commands_remove":
                    if len(command) == 2:
                        timed_commands.remove(timed_commands[int(command[1])])

                # TIMED_COMMANDS_CLEAR command
                elif command[0] == "timed_commands_clear":
                    timed_commands = []

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

                # UNLOCK_CAM command
                elif command[0] == "unlock_cam":
                    unlock_active_cam()

                # MOVE_CAM_BY command
                elif command[0] == "move_cam_by":
                    temp_orient = get_active_cam().orient
                    get_active_cam().orient = matrix3x3(1, 0, 0,
                                                        0, 1, 0,
                                                        0, 0, 1)
                    if get_active_cam().lock:
                        cam_lock_temp = get_active_cam().lock
                        get_active_cam().lock = None
                        get_active_cam().move(-vec3(float(command[1]), float(command[2]), float(command[3])))
                        get_active_cam().lock = cam_lock_temp
                        cam_lock_temp = None
                    else:
                        get_active_cam().move(-vec3(float(command[1]), float(command[2]), float(command[3])))
                    get_active_cam().orient = temp_orient
                    temp_orient = matrix3x3(1, 0, 0,
                                            0, 1, 0,
                                            0, 0, 1)
                    
                # MOVE_CAM_TO command
                elif command[0] == "move_cam_to":
                    temp_orient = get_active_cam().orient
                    get_active_cam().orient = matrix3x3(1, 0, 0,
                                                        0, 1, 0,
                                                        0, 0, 1)
                    if get_active_cam().lock:
                        cam_lock_temp = get_active_cam().lock
                        get_active_cam().lock = None
                        get_active_cam().move(-vec3(float(command[1]), float(command[2]), float(command[3])) - get_active_cam().pos)
                        get_active_cam().lock = cam_lock_temp
                        cam_lock_temp = None
                    else:
                        get_active_cam().move(-vec3(float(command[1]), float(command[2]), float(command[3])) - get_active_cam().pos)
                    get_active_cam().orient = temp_orient
                    temp_orient = matrix3x3(1, 0, 0,
                                            0, 1, 0,
                                            0, 0, 1)

                # ROTATE_CAM_BY command
                elif command[0] == "rotate_cam_by":
                    if command[1].lower() == "x":
                        get_active_cam().rotate([float(command[2]), 0, 0])
                    elif command[1].lower() == "y":
                        get_active_cam().rotate([0, float(command[2]), 0])
                    elif command[1].lower() == "z":
                        get_active_cam().rotate([0, 0, float(command[2])])

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

                # SOLVER_TYPE command
                elif command[0] == "solver_type":
                    solver_type = int(command[1])

                # TOLERANCE command
                elif command[0] == "tolerance":
                    tolerance = float(command[1])

                # HELP command
                elif command[0] == "help":
                    if len(command) == 1:
                        print("\nAvailable commands: help, show, hide, clear, cam_strafe_speed, cam_rotate_speed, delta_t, cycle_time,")
                        print("create_vessel, delete_vessel, fragment, get_objects, create_maneuver, delete_maneuver, get_maneuvers,")
                        print("batch, note, create_projection, delete_projection, update_projection, get_projections, create_plot,")
                        print("delete_plot, display_plot, get_plots, create_resource, delete_resource, get_resources,")
                        print("create_spherical_harmonics, remove_spherical_harmonics, get_spherical_harmonics,")
                        print("create_schwarzschild, delete_schwarzschild, get_schwarzschild, create_lensethirring, delete_lensethirring,")
                        print("get_lensethirrings, output_rate, lock_cam, unlock_cam, auto_dt, auto_dt_remove, auto_dt_clear, get_auto_dt_buffer,")
                        print("draw_mode, point_size, create_barycenter, delete_barycenter, export,")
                        print("rapid_compute, cancel_rapid_compute, get_rapid_compute_buffer, rapid_compute_clear,")
                        print("vessel_body_collision, apply_radiation_pressure, remove_radiation_pressure,")
                        print("apply_atmospheric_drag, remove_atmospheric_drag, lock_origin, unlock_origin, lock_scene_rot, unlock_scene_rot,")
                        print("create_proximity_zone, delete_proximity_zone, get_proximity_zones,")
                        print("get_timed_commands, timed_commands_remove, timed_commands_clear,")
                        print("solver_type, tolerance, generate_starfield, clear_starfield\n")
                        print("Commands can be buffered to run at specific simulation times by adding 't=<execution_time> '")
                        print("in front of them.\n")
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
                            print("Syntax Option 8: show grid (enables xz plane grid)\n")
                            print("Syntax Option 9: show polar_grid (enables xz plane grid in polar coordinates)\n")
                            print("Syntax Option 10: show labels (enables text labels for objects)\n")
                            print("Syntax Option 11: show pmcs (shows point-mass-clouds)\n")
                            input("Press Enter to continue...")
                        elif command[1] == "hide":
                            print("\n'hide' command removes an output element from the command prompt/terminal.\n")
                            print("Syntax Option 1: hide <display_label>\n")
                            print("Syntax Option 2: hide traj (disables trajectory trails)\n")
                            print("Syntax Option 3: hide grid (disables xz plane grid)\n")
                            print("Syntax Option 4: hide polar_grid (disables xz plane grid, polar coordinates)\n")
                            print("Syntax Option 5: hide pmcs (hides point-mass-clouds)\n")
                            input("Press Enter to continue...")
                        elif command[1] == "clear":
                            print("\n'clear' command removes all output element from the command prompt/terminal.\n")
                            print("Syntax: clear <thing>\n")
                            print("Things to clear: output (clears the output display buffer), scene (removes everything from the physics scene),")
                            print("traj_visuals (clears vessel trajectories up to current time in the 3D scene)\n")
                            input("Press Enter to continue...")
                        elif command[1] == "generate_starfield":
                            print("\n'generate_starfield' command generates a starfield to aid the eye with camera rotations as well as make the sky look a bit more familiar.")
                            print("Default number of stars is", default_star_num, "and can be changed via configuration (requires restart).\n")
                            print("Syntax 1: generate_starfield <num_of_stars>")
                            print("Syntax 2: generate_starfield (uses default number of stars)\n")
                            input("Press Enter to continue...")
                        elif command[1] == "clear_starfield":
                            print("\n'clear_starfield' command clears the starfield and stops a starry background from being rendered.\n")
                            print("Syntax: clear_starfield\n")
                            input("Press Enter to continue...")
                        elif command[1] == "batch":
                            print("\n'batch' command reads a batch file and queues the commands to be sent to the interpreter.\n")
                            print("Syntax: batch <file_path>\n")
                            input("Press Enter to continue...")
                        elif command[1] == "lock_origin":
                            print("\n'lock_origin' command locks the global coordinate system origin to a body or vessel for optimizing precision for that particular object.\n")
                            print("Syntax: lock_origin <object_name>\n")
                            input("Press Enter to continue...")
                        elif command[1] == "unlock_origin":
                            print("\n'unlock_origin' command releases coordinate system origin from the object it was locked to.\n")
                            print("Syntax: unlock_origin\n")
                            input("Press Enter to continue...")
                        elif command[1] == "lock_scene_rot":
                            print("\n'lock_scene_rot' command sets the scene rotation rate by locking the view direction to a target object or by defining a constant rotation rate.\n")
                            print("Syntax Option 1: lock_scene_rot <object_name>\n")
                            print("Syntax Option 2: lock_scene_rot <rotation_rate>\n")
                            input("Press Enter to continue...")
                        elif command[1] == "unlock_scene_rot":
                            print("\n'unlock_scene_rot' stops the scene reference frame from rotating.")
                            print("Syntax: unlock_scene_rot\n")
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
                        elif command[1] == "create_proximity_zone":
                            print("\n'create_proximity_zone' command creates a proximity zone around a vessel that keeps track of close passes and collisions with other vessels.\n")
                            print("Syntax Option 1: create_proximity_zone <zone_name> <vessel_name> <vessel_size> <zone_size>")
                            print("Syntax Option 2: create_proximity_zone <zone_name> <vessel_name> <vessel_size>")
                            print("Syntax Option 3: create_proximity_zone <zone_name> <vessel_name>")
                            input("Press Enter to continue...")
                        elif command[1] == "delete_proximity_zone":
                            print("\n'delete_promixity_zone' command removes a proximity zone from the simulation.\n")
                            print("Syntax: delete_proximity_zone <zone_name>")
                            input("Press Enter to continue...")
                        elif command[1] == "get_proximity_zones":
                            print("\n'get_proximity_zones' command prints a list of proximity zones and their properties.\n")
                            print("Syntax: get_proximity_zones")
                            input("Press Enter to continue...")
                        elif command[1] == "create_maneuver":
                            print("\n'create_maneuver' command adds a new maneuver to be performed by a space vessel.\n")
                            print("Syntax: create_maneuver <name> <type> + <<type-specific arguments>>")
                            print("Maneuver types: const_accel, const_thrust")
                            print("const_accel params: <vessel> <frame_of_reference> <orientation> <acceleration> <start_time> <duration>")
                            print("const_thrust params: <vessel> <frame_of_reference> <orientation> <thrust> <initial_mass> <mass_flow> <start_time> <duration>")
                            print("impulsive params: <vessel> <frame_of_reference> <orientation> <delta_v> <perform_time>")
                            input("Press Enter to continue...")
                        elif command[1] == "delete_maneuver":
                            print("\n'delete_maneuver' command removes a maneuver from the simulation.\n")
                            print("Syntax: delete_maneuver <name>")
                            input("Press Enter to continue...")
                        elif command[1] == "create_spherical_harmonics":
                            print("\n'create_spherical_harmonics' command sets up a spherical harmonics model around a body affecting a vessel.\n")
                            print("Syntax: create_spherical_harmonics <name> <vessel> <body> <model_filename>")
                            input("Press Enter to continue...")
                        elif command[1] == "remove_spherical_harmonics":
                            print("\n'remove_spherical_harmonics' command removes a spherical harmonics model from the simulation.\n")
                            print("Syntax: remove_spherical_harmonics <name>")
                            input("Press Enter to continue...")
                        elif command[1] == "get_spherical_harmonics":
                            print("\n'get_spherical_harmonics' command prints out a list of all spherical harmonics models currently in simulation.\n")
                            print("Syntax: get_spherical_harmonics")
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
                        elif command[1] == "create_resource":
                            print("'create_resource' command adds a resource item to the simulation to keep track of\nresources such as the stored energy aboard a vessel or the signal strength between\nvessels.")
                            # name, value, equation, variable, obj1, obj2, coeffs, limits
                            print("Syntax: create_resource <name> <init_value> <equation_type> <equation_variable> <object_1> <object_2> <list_of_coefficients> <min_max_limits>")
                            input("Press Enter to continue...")
                        elif command[1] == "delete_resource":
                            print("'delete_resource' command removes a resource item from the simulation.")
                            print("Syntax: delete_resources <name>")
                            input("Press Enter to continue...")
                        elif command[1] == "get_resources":
                            print("'get_resources' command prints out the names of resource items currently in the simulation.")
                            print("Syntax: get_resources")
                            input("Press Enter to continue...")
                        elif command[1] == "create_schwarzschild":
                            print("'create_schwarzschild' command adds a Schwarzschild component of the general relativity effects near a massive body.")
                            print("Syntax: create_schwarzschild <name> <massive_body_name> <vessel_name>")
                            input("Press Enter to continue...")
                        elif command[1] == "delete_schwarzschild":
                            print("'delete_schwarzschild' command removes a Schwarzschild component of the general relativity effect near a massive body from the simulation.")
                            print("Syntax: delete_schwarzschild <name>")
                            input("Press Enter to continue...")
                        elif command[1] == "get_schwarzschilds":
                            print("'get_schwarzschild' command lists Schwarzschild components of the general relativity effect near massive bodies in the simulation.")
                            print("Syntax: get_schwarzschilds")
                            input("Press Enter to continue...")
                        elif command[1] == "create_lensethirring":
                            print("'create_lensethirring' command adds a frame-dragging component of the general relativity effects near a massive body.")
                            print("Syntax: create_lensethirring <name> <massive_body_name> <vessel_name> <specific_angular_momentum>")
                            input("Press Enter to continue...")
                        elif command[1] == "delete_lensethirring":
                            print("'delete_lensethirring' command removes a frame-dragging component of the general relativity effect near a massive body from the simulation.")
                            print("Syntax: delete_lensethirring <name>")
                            input("Press Enter to continue...")
                        elif command[1] == "get_lensethirrings":
                            print("'get_lensethirrings' command lists frame-dragging components of the general relativity effect near massive bodies in the simulation.")
                            print("Syntax: get_lensethirrings")
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
                        elif command[1] == "solver_type":
                            print("\n'solver_type' command selects which physics solver to use.")
                            print("Syntax: solver_type <type_number>")
                            print("Type numbers --> 0: Symplectic Euler, 1: Velocity Verlet, 2: Yoshida4, 3: Yoshida8")
                            print("             --> 4: Adpt. Sym. Euler, 5: Adpt. Vel. Vrt., 6: Adpt. Y4, 7: Adpt. Y8\n")
                            input("Press Enter to continue...")
                        elif command[1] == "tolerance":
                            print("\n'tolerance' command sets the position error tolerance for adaptive time-step solvers.")
                            print("Syntax: tolerance <tolerance>\n")
                            input("Press Enter to continue...")
                        elif command[1] == "delta_t":
                            print("\n'delta_t' command sets time step length of each physics frame.")
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
                        elif command[1] == "get_timed_commands":
                            print("\n'get_timed_commands' displays the scheduled commands yet to be executed.")
                            print("Syntax: get_timed_commands\n")
                            input("Press Enter to continue...")
                        elif command[1] == "timed_commands_remove":
                            print("\n'timed_commands_remove' aborts the execution of a timed command.")
                            print("Syntax: timed_commands_remove <cmd_index>\n")
                            input("Press Enter to continue...")
                        elif command[1] == "timed_commands_clear":
                            print("\n'timed_commands_clear' aborts the execution of all timed commands.")
                            print("Syntax: timed_commands_clear\n")
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

                # add executed command to history
                if command != [""] and command != [" "]:
                    if command[0].startswith("t="):
                        command_history.append(command)
                    elif command[0] != "batch":
                        command_history.append(["t=" + str(sim_time)] + command)

                command = [""]

            if keyboard.is_pressed("CTRL+K"):
                accept_keyboard_input = False

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
            print("")
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            drawRapidCompute(get_active_cam())
            glfw.swap_buffers(window)

        # this prevents 'jumps' in trajectory trails during rapid compute
        if rapid_compute_buffer and rapid_compute_buffer[0][0] <= sim_time < rapid_compute_buffer[0][1] and rapid_compute_flag:
            for v in vessels:
                v.update_draw_pos()

            if int(sim_time) % int(output_rate * 1000) < delta_t:
                rapid_compute_complete_percent = ((sim_time - rapid_compute_buffer[0][0])/(rapid_compute_buffer[0][1] - rapid_compute_buffer[0][0])) * 100
                print("Time: " + str(sim_time) + " (Current rapid compute is " + str(rapid_compute_complete_percent) + "% complete.)")
                
        if rapid_compute_flag and sim_time > rapid_compute_buffer[0][1]:
            rapid_compute_flag = False
            cycle_time = old_cycle_time
            cam_strafe_speed = old_cam_strafe_speed
            cam_rotate_speed = old_cam_rotate_speed
            rapid_compute_buffer.remove(rapid_compute_buffer[0])

        # update physics

        # lower delta_t if a maneuver is in progress
        for m in maneuvers:
            if maneuver_auto_dt and ((delta_t > maneuver_auto_dt and (m.get_state(sim_time) == "Performing" or
                                                                      (m.get_state(
                                                                          sim_time) == "Pending" and not m.get_state(
                                                                          sim_time + delta_t) == "Pending")))):
                delta_t = maneuver_auto_dt

        # compute time step with the selected solver
        increase_delta_t = False
        adaptive_warning = False
        if solver_type == 0:
            SymplecticEuler(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, spherical_harmonics, schwarzschilds, lensethirrings, sim_time, delta_t)
        elif solver_type == 1:
            VelocityVerlet(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, spherical_harmonics, schwarzschilds, lensethirrings, sim_time, delta_t)
        elif solver_type == 2:
            Yoshida4(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, spherical_harmonics, schwarzschilds, lensethirrings, sim_time, delta_t)
        elif solver_type == 3:
            Yoshida8(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, spherical_harmonics, schwarzschilds, lensethirrings, sim_time, delta_t)
        else:
            delta_t, increase_delta_t, adaptive_warning = adaptive(bodies, vessels, surface_points, maneuvers, atmospheric_drags, radiation_pressures, spherical_harmonics, schwarzschilds, lensethirrings, sim_time, delta_t, solver_type-4, tolerance)

        if solver_type > 3 and output_rate != 1:
            output_rate = 1
            output_buffer.append(["ADPT_OUTPUT", "note", "output_rate automatically set to 1 to ensure proper screen updates."])

        # rotate scene
        if scene_rot_target:
            rotate_scene(scene_lock, scene_rot_target, delta_t)

        # check collisions
        for v in vessels:
            for b in bodies:
                if vessel_body_collision and v.get_alt_above(b) <= 0:
                    vessel_body_crash(v, b)

        proximity_zone_violations = []
        colliding_vessels = []
        for prox in proximity_zones:
            violators, colliders = prox.check_violations(vessels)
            proximity_zone_violations.append([prox.vessel, violators])
            if colliders:
                colliding_vessels.append([prox.vessel, colliders])

        for collision_set in colliding_vessels:
            prox_vessel = collision_set[0]
            violating_colliders = collision_set[1]
            rel_vel_max = 0
            for vc in violating_colliders:
                rel_vel = vc.get_vel_rel_to(prox_vessel)
                rel_vel_mag = rel_vel.mag()

                if rel_vel_mag > 0.282842712474619: # more energy than 40 J/g
                    fragment(vc.name, 5, rel_vel_mag**0.5)
                    output_buffer.append([vc.name + "_ALERT", "note", vc.name + " has broken-up after a collision with " + prox_vessel.name + "!"])
                    delete_vessel(vc.name)
                else:
                    if not [vc.name + "_WARNING", "note", vc.name + " has bumped into " + prox_vessel.name + "!"] in output_buffer:
                        output_buffer.append([vc.name + "_WARNING", "note", vc.name + " has bumped into " + prox_vessel.name + "!"])

                if rel_vel_mag > rel_vel_max:
                    rel_vel_max = rel_vel_mag

            if rel_vel_max > 0.282842712474619: # more energy than 40 J/g
                fragment(prox_vessel.name, 5, rel_vel_max**0.5)
                delete_vessel(prox_vessel.name)

        for violation_set in proximity_zone_violations:
            prox_vessel = violation_set[0]
            for vl in violation_set[1]:
                if not [vl.name + "_WARNING", "note", vl.name + " has violated the proximity zone around " + prox_vessel.name + "!"] in output_buffer:
                    output_buffer.append([vl.name + "_WARNING", "note", vl.name + " has violated the proximity zone around " + prox_vessel.name + "!"])

        # update resources
        for res in resources:
            res.update_occultation(bodies)
            res.update_value(delta_t)

        # update observations
        for obs in observations:
            obs.calculate(delta_t)

        # update plots
        for p in plots:
            p.update(sim_time)

            # going to display any of the plots?
            if sim_time >= p.get_end_time() > (sim_time - delta_t):
                p.display()

                clear_cmd_terminal()
                print("Exporting plot data to /exported_data/" + p.title + ".csv...")
                p.export_to_file()
                print("Done!")
                time.sleep(2)

        # update cameras
        for cam in cameras:
            cam.move_with_lock()

        # lock coordinate system to specified object
        if scene_lock:
            delta_pos = scene_lock.pos * (-1)
            for o in objs:
                o.pos = o.get_pos() + delta_pos

        if (int(sim_time) % int(output_rate) < delta_t) and not rapid_compute_flag:

            # update output
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")

            # display what the user wants in cmd/terminal
            print("OrbitSim3D Command Interpreter & Output Display\n")
            if not accept_keyboard_input:
                print(" - KEYBOARD INPUT LOCKED - \n")
            if sim_time < 30 * delta_t:
                print("Press C at any time to use the command line or P to open the command panel interface.\n")
            print("Time:", sim_time, "\n")

            for element in output_buffer:

                try:
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
                        print(element[0], (element[2].get_pos().mag()))
                    elif element[1] == "vel_mag":
                        print(element[0], (element[2].get_vel().mag()))

                    # altitude
                    elif element[1] == "alt":
                        print(element[0], element[2].get_alt_above(find_obj_by_name(element[3])))

                    # ground pos
                    elif element[1] == "gpos":
                        print(element[0] +
                              "\nLat: " + str(element[2].get_gpos()[0]) + " deg" +
                              "\nLong: " + str(element[2].get_gpos()[1]) + " deg" +
                              "\nAlt: " + str(element[2].get_gpos()[2]) + " m")

                    # angle above horizon
                    elif element[1] == "horizon_angle":
                        print(element[0] + " " + str(element[2].get_obj_angle_above_horizon(element[3])) + " deg")

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

                    # resources
                    elif element[1] == "value" and element[3] == "res":
                        print(element[0], element[2].value)

                    elif element[1] == "delta" and element[3] == "res":
                        print(element[0], element[2].last_delta)

                    # observations
                    elif element[1] == "params" and element[3] == "obs":
                        print(element[0], element[2].get_params_str())

                    # spherical harmonics
                    elif element[1] == "params" and element[3] == "sh":
                        print(element[0], element[2].get_params_str())

                    # note taking
                    elif element[1] == "note":
                        print(element[0], element[2])
                
                    print("")

                except:
                    # print("ERROR with following output element:", element)
                    output_buffer.remove(element)
                    del element
                    
            # clear stuff from last frame
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # do the actual drawing

            # drawOrigin() -- maybe it'll be useful for debugging one day
            drawScene(bodies, vessels, surface_points, barycenters, projections, maneuvers, get_active_cam(), show_trajectories,
                      draw_mode, labels_visible, pmcs_visible, scene_lock, point_size, grid_active, polar_grid_active, scene_rot_target,
                      starfield, far_clip)
            glfw.swap_buffers(window)
            
        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < cycle_time:
            time.sleep(cycle_time - cycle_dt)
        elif warn_cycle_time and cycle_time*2 <= cycle_dt and not cycle_time == 0:
            print("Cycle time too low! Machine can't update physics at the given cycle time!\n")
            print("Consider increasing cycle_time to get more consistent calculation rate.\n")

        if adaptive_warning:
            print("Adaptive time-step solver has had some trouble achieving the desired tolerance in the last step.")
            print("Max. time-step attempts had been reached.")

        sim_time += delta_t
        if increase_delta_t:
            delta_t = delta_t * 2

    # save latest simulation state
    export_scenario("_latest", verbose=False)

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
    
def init_sim(sys_args=None):
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

    if sys_args and len(sys_args) > 1:
        try:
            import_scenario(sys_args[1])
        except FileNotFoundError:
            try:
                import_scenario("scenarios/" + sys_args[1])
            except FileNotFoundError:
                try:
                    import_scenario("scenarios/" + sys_args[1] + ".osf")
                except FileNotFoundError:
                    print("The program run argument is not a valid scenario - loading main menu...")
                    time.sleep(3)
                    clear_cmd_terminal()

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
    print("0) (R)esume Latest Simulation")
    print("1) (L)oad Scenario")
    print("2) (S)tart Empty Scene")
    print("3) (C)onfigure OrbitSim3D")
    print("4) (T)est Propagator")

    menu_select = input("\n > ")

    if menu_select == "0" or menu_select.lower() == "r":
        try:
            import_scenario("scenarios/_latest.osf")
        except FileNotFoundError:
            print("Could not find latest scenario state 'scenarios/_latest.osf'.")
            time.sleep(2)
            init_sim()

    if menu_select == "1" or menu_select.lower() == "l":
        scn_path = pick_scenario()
        
        if scn_path:
            import_scenario(scn_path)
        else:
            init_sim()
            
    elif menu_select == "2" or menu_select.lower() == "s":
        clear_scene()
        main()

    elif menu_select == "3" or menu_select.lower() == "c":
        configure_sim()
        init_sim()

    elif menu_select == "4" or menu_select.lower() == "t":
        test_propagator()
        init_sim()

    # :) do the intro again
    elif menu_select == ":)" or menu_select == ":-)":
        initial_run = True
        init_sim()

    else:
        print("Invalid selection!")
        time.sleep(2)
        init_sim()

init_sim(sys.argv)
