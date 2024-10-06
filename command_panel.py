import tkinter as tk
from tkinter import ttk

# There are probably better ways to code this, but it works just as well as you'd want.
# For loops create evil bugs for some reason, so I just did a lot of copy-pasting as a substitude.

def use_command_panel(vessels, bodies, surface_points, barycenters, maneuvers, radiation_pressures, atmospheric_drags, schwarzschilds, lensethirrings,
                      proximity_zones, surface_coverages, projections, resources, observations, plots, auto_dt_buffer, sim_time, delta_t, cycle_time,
                      output_rate, cam_strafe_speed, cam_rotate_speed, rapid_compute_buffer, scene_lock, scene_rot_target, solver_type, tolerance,
                      starfield, default_star_num):
    command_buffer = []

    def on_panel_close():
        root.destroy()
        return command_buffer

    def clear_command_buffer():
        for i in range(len(command_buffer)):
            remove_from_buffer(0)

    def generate_objects_text():
        objects_text = ""
        
        for v in vessels:
            objects_text += "VESSEL: " + v.get_name() + "\n"

        for b in bodies:
            objects_text += "BODY: " + b.get_name() + "\n"
            
        for sp in surface_points:
            objects_text += "SURFACE POINT: " + sp.get_name() + "\n"

        for bc in barycenters:
            objects_text += "BARYCENTER: " + bc.get_name() + "\n"

        for m in maneuvers:
            objects_text += "MANEUVER: " + m.get_name() + "\n"

        for rp in radiation_pressures:
            objects_text += "RADIATION PRESSURE: " + rp.get_name() + "\n"

        for ad in atmospheric_drags:
            objects_text += "ATMOSPHERIC DRAG: " + ad.get_name() + "\n"

        for sch in schwarzschilds:
            objects_text += "SCHWARZCHILD EFFECT: " + sch.get_name() + "\n"

        for lt in lensethirrings:
            objects_text += "LENSE-THIRRING EFFECT: " + lt.get_name() + "\n"

        for pz in proximity_zones:
            objects_text += "PROXIMITY ZONE: " + pz.get_name() + "\n"
            
        for p in projections:
            objects_text += "PROJECTION: " + p.get_name() + "\n"

        for res in resources:
            objects_text += "RESOURCE: " + res.get_name() + "\n"

        for obs in observations:
            objects_text += "OBSERVATION: " + obs.get_name() + "\n"

        for sc in surface_coverages:
            objects_text += "SURFACE COV.: " + sc.get_name() + "\n"
            
        for pl in plots:
            objects_text += "PLOTTER: " + pl.get_name() + "\n"
            
        return objects_text

    def set_objects_text():
        objects_panel.config(state="normal")
        obj_text = generate_objects_text()
        objects_panel.delete(1.0, "end")
        objects_panel.insert(1.0, obj_text)
        objects_panel.config(state="disabled")

    def set_buffer_field():
        cbx.config(state="normal")
        cb_out = ""
        for i in range(len(command_buffer)):
            cb_out += str(i) + ": " + command_buffer[i] + "\n"

        cbx.delete(1.0, "end")
        cbx.insert(1.0, cb_out)
        cbx.config(state="disabled")

    def set_vars_field():
        sim_variables_field.config(state="normal")
        vars_text = "Sim. Time: " + str(sim_time) + "\n\n"
        
        vars_text += "Solver Type: " + str(solver_type) + "\n("
        if solver_type == 0:
            vars_text += "Sym. Euler" + ")\n"
        elif solver_type == 1:
            vars_text += "Vel. Verlet" + ")\n"
        elif solver_type == 2:
            vars_text += "Yoshida4" + ")\n"
        elif solver_type == 3:
            vars_text += "Yoshida8" + ")\n"
        elif solver_type == 4:
            vars_text += "Adap. Sym. Euler" + ")\n"
        elif solver_type == 5:
            vars_text += "Adap. Vel. Verlet" + ")\n"
        elif solver_type == 6:
            vars_text += "Adap. Yoshida4" + ")\n"
        elif solver_type == 7:
            vars_text += "Adap. Yoshida8" + ")\n"

        vars_text += "Adap. Tolerance: " + str(tolerance) + "\n"
        if solver_type < 4:
            vars_text += "Using nonadaptive solver.\nTolerance is disregarded.\n\n"
            
        vars_text += "Delta T: " + str(delta_t) + "\n"
        vars_text += "Cycle Time: " + str(cycle_time) + "\n"
        vars_text += "Output Rate: " + str(output_rate) + "\n"
        vars_text += "\nCam. Strafe Speed: " + str(cam_strafe_speed) + "\n"
        vars_text += "Cam. Rotate Speed: " + str(cam_rotate_speed) + "\n"
        if scene_lock:
            vars_text += "Scene Lock: " + str(scene_lock.get_name()) + "\n"
        else:
            vars_text += "Scene Lock: None\n"

        if scene_rot_target:
            vars_text += "Scene Rot. Target: " + str(scene_rot_target) + "\n"
        else:
            vars_text += "Scene Rot. Target: None\n"

        if starfield:
            vars_text += "Strfld. Star Count: " + str(len(starfield)) + "\n"
        else:
            vars_text += "Strfld. Disabled\n"
            
        sim_variables_field.delete(1.0, "end")
        sim_variables_field.insert(1.0, vars_text)
        sim_variables_field.config(state="disabled")

    def add_to_buffer(command):
        command_buffer.append(command)
        set_buffer_field()

    def remove_from_buffer(cmd_index):
        if len(command_buffer):
            cmd_index = int(cmd_index)

            cmd_index = min(cmd_index, len(command_buffer)-1)
            command_buffer.remove(command_buffer[cmd_index])
            set_buffer_field()

    def time_command_on_buffer(cmd_idx, assigned_time):
        if len(command_buffer):
            cmd_idx = int(cmd_idx)

            cmd_idx = min(cmd_idx, len(command_buffer)-1)
            untimed_cmd = command_buffer[cmd_idx]
            command_buffer[cmd_idx] = "t=" + assigned_time + " " + untimed_cmd
            set_buffer_field()

    def use_command_delete_window():

        if len(command_buffer):

            deletion_window = tk.Tk()
            deletion_window.title("Delete Command")

            deletion_label = tk.Label(deletion_window, text="Type the index number of the command you want to delete from the buffer.")
            deletion_label.grid(row=0, column=0, columnspan=10)

            deletion_input = tk.Text(deletion_window, width=20, height=1)
            deletion_input.grid(row=1, column=4)

            deletion_button = tk.Button(deletion_window, text="Delete", command=lambda:remove_from_buffer(deletion_input.get("1.0","end-1c")))
            deletion_button.grid(row=2, column=4)

    def assign_cmd_time():

        if len(command_buffer):

            cmd_time_window = tk.Tk()
            cmd_time_window.title("Assign Command Execution Time")

            cmd_time_idx_label = tk.Label(cmd_time_window, text="Cmd. Index:")
            cmd_time_idx_label.grid(row=0, column=0)

            cmd_time_asgn_label = tk.Label(cmd_time_window, text="Exec. Time:")
            cmd_time_asgn_label.grid(row=0, column=1)

            cmd_time_idx_input = tk.Text(cmd_time_window, width=20, height=1)
            cmd_time_idx_input.grid(row=1, column=0)

            cmd_time_asgn_input = tk.Text(cmd_time_window, width=20, height=1)
            cmd_time_asgn_input.grid(row=1, column=1)

            cmd_time_asgn_button = tk.Button(cmd_time_window, text="Assign Time",
                                             command=lambda:time_command_on_buffer(cmd_time_idx_input.get("1.0","end-1c"),
                                                                                   cmd_time_asgn_input.get("1.0","end-1c")))
            cmd_time_asgn_button.grid(row=2, column=0, columnspan=2)

    def use_command_window():

        def on_command_window_close():
            cmd_window.destroy()

        def enter_cmd(cmd_a):
            entry_panel = tk.Tk()
            entry_panel.title(cmd_a)

            # SHOW COMMAND
            if cmd_a == "show":
                show_help = tk.Label(entry_panel, text="'show' command adds an output element to the command prompt/terminal.")
                show_help.grid(row=0, column=0, columnspan=10)

                # option 1
                show_s1t1_label = tk.Label(entry_panel, text="Object")
                show_s1t2_label = tk.Label(entry_panel, text="Variable")
                show_s1t3_label = tk.Label(entry_panel, text="Display Label")
                show_s1t1_label.grid(row=1, column=1)
                show_s1t2_label.grid(row=1, column=2)
                show_s1t3_label.grid(row=1, column=3)
                
                show_s1t1 = tk.Text(entry_panel, width=20, height=1)
                show_s1t2 = tk.Text(entry_panel, width=20, height=1)
                show_s1t3 = tk.Text(entry_panel, width=20, height=1)
                show_s1t1.grid(row=2, column=1)
                show_s1t2.grid(row=2, column=2)
                show_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if show_s1t1.get("1.0","end-1c") and show_s1t2.get("1.0","end-1c") and show_s1t3.get("1.0","end-1c"):
                        command = "show " + show_s1t1.get("1.0","end-1c") + " " + show_s1t2.get("1.0","end-1c") + " " + show_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s1_button = tk.Button(entry_panel, text="Show Global Variable", command=generate_s1)
                show_s1_button.grid(row=2, column=0)
                show_s1_button.config(width=20,height=1)

                # option 2
                show_s2t1_label = tk.Label(entry_panel, text="Object")
                show_s2t2_label = tk.Label(entry_panel, text= "Variable")
                show_s2t3_label = tk.Label(entry_panel, text="Frame of Ref.")
                show_s2t4_label = tk.Label(entry_panel, text="Display Label")
                show_s2t1_label.grid(row=3, column=1)
                show_s2t2_label.grid(row=3, column=2)
                show_s2t3_label.grid(row=3, column=3)
                show_s2t4_label.grid(row=3, column=4)

                show_s2t1 = tk.Text(entry_panel, width=20, height=1)
                show_s2t2 = tk.Text(entry_panel, width=20, height=1)
                show_s2t3 = tk.Text(entry_panel, width=20, height=1)
                show_s2t4 = tk.Text(entry_panel, width=20, height=1)
                show_s2t1.grid(row=4, column=1)
                show_s2t2.grid(row=4, column=2)
                show_s2t3.grid(row=4, column=3)
                show_s2t4.grid(row=4, column=4)

                def generate_s2():
                    if show_s2t1.get("1.0","end-1c") and show_s2t2.get("1.0","end-1c") and show_s2t3.get("1.0","end-1c") and show_s2t4.get("1.0","end-1c"):
                        command = "show " + show_s2t1.get("1.0","end-1c") + " " + show_s2t2.get("1.0","end-1c") + " " + show_s2t3.get("1.0","end-1c") + " " + show_s2t4.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s2_button = tk.Button(entry_panel, text="Show Relative Variable", command=generate_s2)
                show_s2_button.grid(row=4, column=0)
                show_s2_button.config(width=20,height=1)

                # option 3
                show_s3t1_label = tk.Label(entry_panel, text="Maneuver")
                show_s3t2_label = tk.Label(entry_panel, text="Data ('active'/'state'/'params')")
                show_s3t3_label = tk.Label(entry_panel, text="Display Label")
                show_s3t1_label.grid(row=5, column=1)
                show_s3t2_label.grid(row=5, column=2)
                show_s3t3_label.grid(row=5, column=3)

                show_s3t1 = tk.Text(entry_panel, width=20, height=1)
                show_s3t2 = tk.Text(entry_panel, width=20, height=1)
                show_s3t3 = tk.Text(entry_panel, width=20, height=1)
                show_s3t1.grid(row=6, column=1)
                show_s3t2.grid(row=6, column=2)
                show_s3t3.grid(row=6, column=3)

                def generate_s3():
                    if show_s3t1.get("1.0","end-1c") and show_s3t2.get("1.0","end-1c") and show_s3t3.get("1.0","end-1c"):
                        command = "show " + show_s3t1.get("1.0","end-1c") + " " + show_s3t2.get("1.0","end-1c") + " " + show_s3t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s3_button = tk.Button(entry_panel, text="Show Maneuver Data", command=generate_s3)
                show_s3_button.grid(row=6, column=0)
                show_s3_button.config(width=20,height=1)

                # option 4
                show_s4t1_label = tk.Label(entry_panel, text="Radiation Press.")
                show_s4t2_label = tk.Label(entry_panel, text="Data ('params')")
                show_s4t3_label = tk.Label(entry_panel, text="Display Label")
                show_s4t1_label.grid(row=7, column=1)
                show_s4t2_label.grid(row=7, column=2)
                show_s4t3_label.grid(row=7, column=3)

                show_s4t1 = tk.Text(entry_panel, width=20, height=1)
                show_s4t2 = tk.Text(entry_panel, width=20, height=1)
                show_s4t3 = tk.Text(entry_panel, width=20, height=1)
                show_s4t1.grid(row=8, column=1)
                show_s4t2.grid(row=8, column=2)
                show_s4t3.grid(row=8, column=3)

                def generate_s4():
                    if show_s4t1.get("1.0","end-1c") and show_s4t2.get("1.0","end-1c") and show_s4t3.get("1.0","end-1c"):
                        command = "show " + show_s4t1.get("1.0","end-1c") + " " + show_s4t2.get("1.0","end-1c") + " " + show_s4t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s4_button = tk.Button(entry_panel, text="Show Rad. Press. Data", command=generate_s4)
                show_s4_button.grid(row=8, column=0)
                show_s4_button.config(width=20,height=1)

                # option 5
                show_s5t1_label = tk.Label(entry_panel, text="Atmo. Drag")
                show_s5t2_label = tk.Label(entry_panel, text="Data ('params')")
                show_s5t3_label = tk.Label(entry_panel, text="Display Label")
                show_s5t1_label.grid(row=9, column=1)
                show_s5t2_label.grid(row=9, column=2)
                show_s5t3_label.grid(row=9, column=3)

                show_s5t1 = tk.Text(entry_panel, width=20, height=1)
                show_s5t2 = tk.Text(entry_panel, width=20, height=1)
                show_s5t3 = tk.Text(entry_panel, width=20, height=1)
                show_s5t1.grid(row=10, column=1)
                show_s5t2.grid(row=10, column=2)
                show_s5t3.grid(row=10, column=3)

                def generate_s5():
                    if show_s5t1.get("1.0","end-1c") and show_s5t2.get("1.0","end-1c") and show_s5t3.get("1.0","end-1c"):
                        command = "show " + show_s5t1.get("1.0","end-1c") + " " + show_s5t2.get("1.0","end-1c") + " " + show_s5t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s5_button = tk.Button(entry_panel, text="Show Atmo. Drag Data", command=generate_s5)
                show_s5_button.grid(row=10, column=0)
                show_s5_button.config(width=20,height=1)

                # option 6
                show_s6t1_label = tk.Label(entry_panel, text="Projection")
                show_s6t2_label = tk.Label(entry_panel, text="Data (attribute/'params')")
                show_s6t3_label = tk.Label(entry_panel, text="Display Label")
                show_s6t1_label.grid(row=11, column=1)
                show_s6t2_label.grid(row=11, column=2)
                show_s6t3_label.grid(row=11, column=3)

                show_s6t1 = tk.Text(entry_panel, width=20, height=1)
                show_s6t2 = tk.Text(entry_panel, width=20, height=1)
                show_s6t3 = tk.Text(entry_panel, width=20, height=1)
                show_s6t1.grid(row=12, column=1)
                show_s6t2.grid(row=12, column=2)
                show_s6t3.grid(row=12, column=3)

                def generate_s6():
                    if show_s6t1.get("1.0","end-1c") and show_s6t2.get("1.0","end-1c") and show_s6t3.get("1.0","end-1c"):
                        command = "show " + show_s6t1.get("1.0","end-1c") + " " + show_s6t2.get("1.0","end-1c") + " " + show_s6t3.get("1.0","end-1c")
                        add_to_buffer(command)

                show_s6_button = tk.Button(entry_panel, text="Show Projection Data", command=generate_s6)
                show_s6_button.grid(row=12, column=0)
                show_s6_button.config(width=20,height=1)

                # option 7
                show_s7t1_label = tk.Label(entry_panel, text="Resource")
                show_s7t2_label = tk.Label(entry_panel, text="Data ('value'/'delta')")
                show_s7t3_label = tk.Label(entry_panel, text="Display Label")
                show_s7t1_label.grid(row=13, column=1)
                show_s7t2_label.grid(row=13, column=2)
                show_s7t3_label.grid(row=13, column=3)

                show_s7t1 = tk.Text(entry_panel, width=20, height=1)
                show_s7t2 = tk.Text(entry_panel, width=20, height=1)
                show_s7t3 = tk.Text(entry_panel, width=20, height=1)
                show_s7t1.grid(row=14, column=1)
                show_s7t2.grid(row=14, column=2)
                show_s7t3.grid(row=14, column=3)

                def generate_s7():
                    if show_s7t1.get("1.0", "end-1c") and show_s7t2.get("1.0", "end-1c") and show_s7t3.get("1.0", "end-1c"):
                        command = "show " + show_s7t1.get("1.0", "end-1c") + " " + show_s7t2.get("1.0", "end-1c") + " " + show_s7t3.get("1.0", "end-1c")
                        add_to_buffer(command)

                show_s7_button = tk.Button(entry_panel, text="Show Resource Data", command=generate_s7)
                show_s7_button.grid(row=14, column=0)
                show_s7_button.config(width=20, height=1)

                # option 8
                show_s8t1_label = tk.Label(entry_panel, text="Observation")
                show_s8t2_label = tk.Label(entry_panel, text="Display Label")
                show_s8t1_label.grid(row=15, column=1)
                show_s8t2_label.grid(row=15, column=2)

                show_s8t1 = tk.Text(entry_panel, width=20, height=1)
                show_s8t2 = tk.Text(entry_panel, width=20, height=1)
                show_s8t1.grid(row=16, column=1)
                show_s8t2.grid(row=16, column=2)

                def generate_s8():
                    if show_s8t1.get("1.0", "end-1c") and show_s8t2.get("1.0", "end-1c"):
                        command = "show " + show_s8t1.get("1.0", "end-1c") + " " + show_s8t2.get("1.0", "end-1c")
                        add_to_buffer(command)

                show_s8_button = tk.Button(entry_panel, text="Show Obsrv. Data", command=generate_s8)
                show_s8_button.grid(row=16, column=0)
                show_s8_button.config(width=20, height=1)

                # option 9
                show_traj_button = tk.Button(entry_panel, text="Show Trajectories", command=lambda:add_to_buffer("show traj"))
                show_traj_button.grid(row=17, column=0)
                show_traj_button.config(width=20,height=1)

                # option 10
                show_labels_button = tk.Button(entry_panel, text="Show Labels", command=lambda:add_to_buffer("show labels"))
                show_labels_button.grid(row=17, column=1)
                show_labels_button.config(width=20,height=1)

                # option 11
                show_grid_button = tk.Button(entry_panel, text="Show Grid", command=lambda:add_to_buffer("show grid"))
                show_grid_button.grid(row=17, column=2)
                show_grid_button.config(width=20, height=1)

                # option 12
                show_polar_grid_button = tk.Button(entry_panel, text="Show Polar Grid", command=lambda:add_to_buffer("show polar_grid"))
                show_polar_grid_button.grid(row=17, column=3)
                show_polar_grid_button.config(width=20, height=1)

                # option 13
                show_pmcs_button = tk.Button(entry_panel, text="Show PMCs", command=lambda:add_to_buffer("show pmcs"))
                show_pmcs_button.grid(row=17, column=4)
                show_pmcs_button.config(width=20, height=1)

            elif cmd_a == "hide":
                hide_help = tk.Label(entry_panel, text="'hide' command removes an output element from the command prompt/terminal.")
                hide_help.grid(row=0, column=0, columnspan=10)
                
                hide_s1_button = tk.Button(entry_panel, text="Hide Trajectories", command=lambda:add_to_buffer("hide traj"))
                hide_s1_button.grid(row=1, column=0)
                hide_s1_button.config(width=20,height=1)

                hide_s2t1_label = tk.Label(entry_panel, text="Display Label")
                hide_s2t1_label.grid(row=2, column=1)

                hide_s2t1 = tk.Text(entry_panel, width=20, height=1)
                hide_s2t1.grid(row=3, column=1)

                def generate_s2():
                    if hide_s2t1.get("1.0","end-1c"):
                        command = "hide " + hide_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                hide_s2_button = tk.Button(entry_panel, text="Hide Output", command=generate_s2)
                hide_s2_button.grid(row=3, column=0)
                hide_s2_button.config(width=20,height=1)

                hide_s3_button = tk.Button(entry_panel, text="Hide Labels", command=lambda:add_to_buffer("hide labels"))
                hide_s3_button.grid(row=4, column=0)
                hide_s3_button.config(width=20,height=1)

                hide_s4_button = tk.Button(entry_panel, text="Hide Grid", command=lambda:add_to_buffer("hide grid"))
                hide_s4_button.grid(row=5, column=0)
                hide_s4_button.config(width=20, height=1)

                hide_s5_button = tk.Button(entry_panel, text="Hide Plr. Grid", command=lambda:add_to_buffer("hide polar_grid"))
                hide_s5_button.grid(row=5, column=1)
                hide_s5_button.config(width=20, height=1)

                hide_s6_button = tk.Button(entry_panel, text="Hide PMCs", command=lambda:add_to_buffer("hide pmcs"))
                hide_s6_button.grid(row=5, column=2)
                hide_s6_button.config(width=20, height=1)

            elif cmd_a == "clear":
                clear_help = tk.Label(entry_panel, text="'clear' command can remove all output element from the command prompt/terminal,\nremove all objects from the simulation, or clear trajectory trails up to current simulation time.")
                clear_help.grid(row=0, column=0, columnspan=10)
                
                clear_s1_button = tk.Button(entry_panel, text="Clear Output", command=lambda:add_to_buffer("clear output"))
                clear_s2_button = tk.Button(entry_panel, text="Clear Scene", command=lambda:add_to_buffer("clear scene"))
                clear_s3_button = tk.Button(entry_panel, text="Clear Trajectory Trails", command=lambda:add_to_buffer("clear traj_visuals"))
                clear_s1_button.grid(row=1, column=0)
                clear_s2_button.grid(row=2, column=0)
                clear_s3_button.grid(row=3, column=0)

            elif cmd_a == "generate_starfield":
                gsf_help_text = "'generate_starfield' command generates a starfield to aid the eye with camera rotations as well as make the sky look a bit more familiar.\nDefault number of stars is " + str(default_star_num) + ", you can click the button without entering a number to use the default.\nDefault number can be modified by editing the config file (requires restart)."
                gsf_help = tk.Label(entry_panel, text=gsf_help_text)
                gsf_help.grid(row=0, column=0, columnspan=10)

                gsf_s1t1_label = tk.Label(entry_panel, text="Num. of Stars")
                gsf_s1t1_label.grid(row=1, column=1)

                gsf_s1t1 = tk.Text(entry_panel, width=20, height=1)
                gsf_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if gsf_s1t1.get("1.0","end-1c"):
                        command = "generate_starfield " + gsf_s1t1.get("1.0","end-1c")
                    else:
                        command = "generate_starfield"
                        
                    add_to_buffer(command)

                gsf_s1_button = tk.Button(entry_panel, text="Gen. Strfld.", command=generate_s1)
                gsf_s1_button.grid(row=2, column=0)
            
            elif cmd_a == "create_vessel":
                cv_help = tk.Label(entry_panel, text="'create_vessel' command adds a new space vessel to the simulation.")
                cv_help.grid(row=0, column=0, columnspan=10)
                # option 1
                cv_s1t1_label = tk.Label(entry_panel, text="Vessel Name")
                cv_s1t2_label = tk.Label(entry_panel, text="3D Model Name")
                cv_s1t3_label = tk.Label(entry_panel, text="Color")
                cv_s1t4_label = tk.Label(entry_panel, text="Position")
                cv_s1t5_label = tk.Label(entry_panel, text="Velocity")
                cv_s1t1_label.grid(row=1, column=1)
                cv_s1t2_label.grid(row=1, column=2)
                cv_s1t3_label.grid(row=1, column=3)
                cv_s1t4_label.grid(row=1, column=4)
                cv_s1t5_label.grid(row=1, column=5)
                
                cv_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t5 = tk.Text(entry_panel, width=20, height=1)
                cv_s1t1.grid(row=2, column=1)
                cv_s1t2.grid(row=2, column=2)
                cv_s1t3.grid(row=2, column=3)
                cv_s1t4.grid(row=2, column=4)
                cv_s1t5.grid(row=2, column=5)

                def generate_s1():
                    if cv_s1t1.get("1.0","end-1c") and cv_s1t2.get("1.0","end-1c") and cv_s1t3.get("1.0","end-1c") and cv_s1t4.get("1.0","end-1c") and cv_s1t5.get("1.0","end-1c"):
                        command = "create_vessel " + cv_s1t1.get("1.0","end-1c") + " " + cv_s1t2.get("1.0","end-1c") + " " + cv_s1t3.get("1.0","end-1c") + " " + cv_s1t4.get("1.0","end-1c") + " " + cv_s1t5.get("1.0","end-1c")
                        add_to_buffer(command)

                cv_s1_button = tk.Button(entry_panel, text="Create Vessel", command=generate_s1)
                cv_s1_button.grid(row=2, column=0)

                # option 2
                cv_s2t1_label = tk.Label(entry_panel, text="Vessel Name")
                cv_s2t2_label = tk.Label(entry_panel, text="3D Model Name")
                cv_s2t3_label = tk.Label(entry_panel, text="Color")
                cv_s2t4_label = tk.Label(entry_panel, text="Frame of Ref.")
                cv_s2t5_label = tk.Label(entry_panel, text="Position (spherical)")
                cv_s2t6_label = tk.Label(entry_panel, text="Velocity")
                cv_s2t1_label.grid(row=3, column=1)
                cv_s2t2_label.grid(row=3, column=2)
                cv_s2t3_label.grid(row=3, column=3)
                cv_s2t4_label.grid(row=3, column=4)
                cv_s2t5_label.grid(row=3, column=5)
                cv_s2t6_label.grid(row=3, column=6)

                cv_s2t1 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t2 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t3 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t4 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t5 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t6 = tk.Text(entry_panel, width=20, height=1)
                cv_s2t1.grid(row=4, column=1)
                cv_s2t2.grid(row=4, column=2)
                cv_s2t3.grid(row=4, column=3)
                cv_s2t4.grid(row=4, column=4)
                cv_s2t5.grid(row=4, column=5)
                cv_s2t6.grid(row=4, column=6)

                def generate_s2():
                    if cv_s2t1.get("1.0","end-1c") and cv_s2t2.get("1.0","end-1c") and cv_s2t3.get("1.0","end-1c") and cv_s2t4.get("1.0","end-1c") and cv_s2t5.get("1.0","end-1c") and cv_s2t6.get("1.0","end-1c") :
                        command = "create_vessel " + cv_s2t1.get("1.0","end-1c") + " " + cv_s2t2.get("1.0","end-1c") + " " + cv_s2t3.get("1.0","end-1c") + " " + cv_s2t4.get("1.0","end-1c") + " " + cv_s2t5.get("1.0","end-1c") + " " + cv_s2t5.get("1.0","end-1c")
                        add_to_buffer(command)

                cv_s2_button = tk.Button(entry_panel, text="Create Vessel", command=generate_s1)
                cv_s2_button.grid(row=4, column=0)

            elif cmd_a == "delete_vessel":
                dv_help = tk.Label(entry_panel, text="'delete_vessel' command removes a space vessel from the simulation.")
                dv_help.grid(row=0, column=0, columnspan=10)
                
                dv_s1t1_label = tk.Label(entry_panel, text="Vessel Name")
                dv_s1t1_label.grid(row=1, column=1)

                dv_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dv_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dv_s1t1.get("1.0","end-1c"):
                        command = "delete_vessel " + dv_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dv_s1_button = tk.Button(entry_panel, text="Delete Vessel", command=generate_s1)
                dv_s1_button.grid(row=2, column=0)

            elif cmd_a == "fragment":
                frag_help = tk.Label(entry_panel, text="'fragment' command creates small fragments from an object in space\n(as if it was hit by a kinetic impactor).")
                frag_help.grid(row=0, column=0, columnspan=10)

                frag_s1t1_label = tk.Label(entry_panel, text="Object to Frag.")
                frag_s1t1_label.grid(row=1, column=1)
                frag_s1t2_label = tk.Label(entry_panel, text="Num. of Fragments")
                frag_s1t2_label.grid(row=1, column=2)
                frag_s1t3_label = tk.Label(entry_panel, text="Rel. Vel. of Fragments")
                frag_s1t3_label.grid(row=1, column=3)

                frag_s1t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t1.grid(row=2, column=1)
                frag_s1t2 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t2.grid(row=2, column=2)
                frag_s1t3 = tk.Text(entry_panel, width=20, height=1)
                frag_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if frag_s1t1.get("1.0","end-1c") and frag_s1t2.get("1.0","end-1c") and frag_s1t3.get("1.0","end-1c"):
                        command = "fragment " + frag_s1t1.get("1.0","end-1c") + " " + frag_s1t2.get("1.0","end-1c") + " " + frag_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s1_button = tk.Button(entry_panel, text="Fragment", command=generate_s1)
                frag_s1_button.grid(row=2, column=0)

                # s2 ---
                frag_s2t1_label = tk.Label(entry_panel, text="Object to Frag.")
                frag_s2t1_label.grid(row=3, column=1)
                frag_s2t2_label = tk.Label(entry_panel, text="Num. of Fragments")
                frag_s2t2_label.grid(row=3, column=2)

                frag_s2t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s2t1.grid(row=4, column=1)
                frag_s2t2 = tk.Text(entry_panel, width=20, height=1)
                frag_s2t2.grid(row=4, column=2)

                def generate_s2():
                    if frag_s2t1.get("1.0","end-1c") and frag_s2t2.get("1.0","end-1c"):
                        command = "fragment " + frag_s2t1.get("1.0","end-1c") + " " + frag_s2t2.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s2_button = tk.Button(entry_panel, text="Fragment", command=generate_s2)
                frag_s2_button.grid(row=4, column=0)

                # s3 ---
                frag_s3t1_label = tk.Label(entry_panel, text="Object to Frag.")
                frag_s3t1_label.grid(row=5, column=1)

                frag_s3t1 = tk.Text(entry_panel, width=20, height=1)
                frag_s3t1.grid(row=6, column=1)

                def generate_s3():
                    if frag_s3t1.get("1.0","end-1c"):
                        command = "fragment " + frag_s3t1.get("1.0","end-1c")
                        add_to_buffer(command)

                frag_s3_button = tk.Button(entry_panel, text="Fragment", command=generate_s3)
                frag_s3_button.grid(row=6, column=0)

            elif cmd_a == "create_maneuver":
                cm_help = tk.Label(entry_panel, text="'create_maneuver' command adds a new maneuver to be performed by a space vessel.")
                cm_help.grid(row=0, column=0, columnspan=10)
                
                # option 1
                cm_s1t1_label = tk.Label(entry_panel, text="Maneuver Name")
                cm_s1t2_label = tk.Label(entry_panel, text="Vessel Name")
                cm_s1t3_label = tk.Label(entry_panel, text="Frame of Ref.")
                cm_s1t4_label = tk.Label(entry_panel, text="Orientation")
                cm_s1t5_label = tk.Label(entry_panel, text="Acceleration")
                cm_s1t6_label = tk.Label(entry_panel, text="Start Time")
                cm_s1t7_label = tk.Label(entry_panel, text="Duration")
                cm_s1t1_label.grid(row=1, column=1)
                cm_s1t2_label.grid(row=1, column=2)
                cm_s1t3_label.grid(row=1, column=3)
                cm_s1t4_label.grid(row=1, column=4)
                cm_s1t5_label.grid(row=1, column=5)
                cm_s1t6_label.grid(row=1, column=6)
                cm_s1t7_label.grid(row=1, column=7)

                cm_s1t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t7 = tk.Text(entry_panel, width=15, height=1)
                cm_s1t1.grid(row=2, column=1)
                cm_s1t2.grid(row=2, column=2)
                cm_s1t3.grid(row=2, column=3)
                cm_s1t4.grid(row=2, column=4)
                cm_s1t5.grid(row=2, column=5)
                cm_s1t6.grid(row=2, column=6)
                cm_s1t7.grid(row=2, column=7)

                def generate_s1():
                    if cm_s1t1.get("1.0","end-1c") and cm_s1t2.get("1.0","end-1c") and cm_s1t3.get("1.0","end-1c") and cm_s1t4.get("1.0","end-1c") and cm_s1t5.get("1.0","end-1c") and cm_s1t6.get("1.0","end-1c") and cm_s1t7.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s1t1.get("1.0","end-1c") + " const_accel " + cm_s1t2.get("1.0","end-1c") + " " + cm_s1t3.get("1.0","end-1c") + " " + cm_s1t4.get("1.0","end-1c") + " " + cm_s1t5.get("1.0","end-1c") + " " + cm_s1t6.get("1.0","end-1c") + " " + cm_s1t7.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s1_button = tk.Button(entry_panel, text="Create Const. Accel. Mnv.", command=generate_s1)
                cm_s1_button.grid(row=2, column=0)

                # option 2
                cm_s2t1_label = tk.Label(entry_panel, text="Maneuver Name")
                cm_s2t2_label = tk.Label(entry_panel, text="Vessel Name")
                cm_s2t3_label = tk.Label(entry_panel, text="Frame of Ref.")
                cm_s2t4_label = tk.Label(entry_panel, text="Orientation")
                cm_s2t5_label = tk.Label(entry_panel, text="Thrust")
                cm_s2t6_label = tk.Label(entry_panel, text="Initial Mass")
                cm_s2t7_label = tk.Label(entry_panel, text="Mass Flow")
                cm_s2t8_label = tk.Label(entry_panel, text="Start Time")
                cm_s2t9_label = tk.Label(entry_panel, text="Duration")
                cm_s2t1_label.grid(row=3, column=1)
                cm_s2t2_label.grid(row=3, column=2)
                cm_s2t3_label.grid(row=3, column=3)
                cm_s2t4_label.grid(row=3, column=4)
                cm_s2t5_label.grid(row=3, column=5)
                cm_s2t6_label.grid(row=3, column=6)
                cm_s2t7_label.grid(row=3, column=7)
                cm_s2t8_label.grid(row=3, column=8)
                cm_s2t9_label.grid(row=3, column=9)

                cm_s2t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t7 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t8 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t9 = tk.Text(entry_panel, width=15, height=1)
                cm_s2t1.grid(row=4, column=1)
                cm_s2t2.grid(row=4, column=2)
                cm_s2t3.grid(row=4, column=3)
                cm_s2t4.grid(row=4, column=4)
                cm_s2t5.grid(row=4, column=5)
                cm_s2t6.grid(row=4, column=6)
                cm_s2t7.grid(row=4, column=7)
                cm_s2t8.grid(row=4, column=8)
                cm_s2t9.grid(row=4, column=9)

                def generate_s2():
                    if cm_s2t1.get("1.0","end-1c") and cm_s2t2.get("1.0","end-1c") and cm_s2t3.get("1.0","end-1c") and cm_s2t4.get("1.0","end-1c") and cm_s2t5.get("1.0","end-1c") and cm_s2t6.get("1.0","end-1c") and cm_s2t7.get("1.0","end-1c") and cm_s2t8.get("1.0","end-1c") and cm_s2t9.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s2t1.get("1.0","end-1c") + " const_thrust " + cm_s2t2.get("1.0","end-1c") + " " + cm_s2t3.get("1.0","end-1c") + " " + cm_s2t4.get("1.0","end-1c") + " " + cm_s2t5.get("1.0","end-1c") + " " + cm_s2t6.get("1.0","end-1c") + " " + cm_s2t7.get("1.0","end-1c") + " " + cm_s2t8.get("1.0","end-1c") + " " + cm_s2t9.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s2_button = tk.Button(entry_panel, text="Create Const. Thrust Mnv.", command=generate_s2)
                cm_s2_button.grid(row=4, column=0)

                # option 3
                cm_s3t1_label = tk.Label(entry_panel, text="Maneuver Name")
                cm_s3t2_label = tk.Label(entry_panel, text="Vessel Name")
                cm_s3t3_label = tk.Label(entry_panel, text="Frame of Ref.")
                cm_s3t4_label = tk.Label(entry_panel, text="Orientation")
                cm_s3t5_label = tk.Label(entry_panel, text="Delta-v")
                cm_s3t6_label = tk.Label(entry_panel, text="Perform Time")
                cm_s3t1_label.grid(row=5, column=1)
                cm_s3t2_label.grid(row=5, column=2)
                cm_s3t3_label.grid(row=5, column=3)
                cm_s3t4_label.grid(row=5, column=4)
                cm_s3t5_label.grid(row=5, column=5)
                cm_s3t6_label.grid(row=5, column=6)

                cm_s3t1 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t2 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t3 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t4 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t5 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t6 = tk.Text(entry_panel, width=15, height=1)
                cm_s3t1.grid(row=6, column=1)
                cm_s3t2.grid(row=6, column=2)
                cm_s3t3.grid(row=6, column=3)
                cm_s3t4.grid(row=6, column=4)
                cm_s3t5.grid(row=6, column=5)
                cm_s3t6.grid(row=6, column=6)

                def generate_s3():
                    if cm_s3t1.get("1.0","end-1c") and cm_s3t2.get("1.0","end-1c") and cm_s3t3.get("1.0","end-1c") and cm_s3t4.get("1.0","end-1c") and cm_s3t5.get("1.0","end-1c") and cm_s3t6.get("1.0","end-1c"):
                        command = "create_maneuver " + cm_s3t1.get("1.0", "end-1c") + " impulsive " + cm_s3t2.get("1.0","end-1c") + " " + cm_s3t3.get("1.0","end-1c") + " " + cm_s3t4.get("1.0","end-1c") + " " + cm_s3t5.get("1.0","end-1c") + " " + cm_s3t6.get("1.0","end-1c")
                        add_to_buffer(command)

                cm_s3_button = tk.Button(entry_panel, text="Create Impulsive Mnv.", command=generate_s3)
                cm_s3_button.grid(row=6, column=0)
                
            elif cmd_a == "delete_maneuver":
                dm_help = tk.Label(entry_panel, text="'delete_maneuver' command removes a maneuver from the simulation.")
                dm_help.grid(row=0, column=0, columnspan=10)
                
                dm_s1t1_label = tk.Label(entry_panel, text="Maneuver Name")
                dm_s1t1_label.grid(row=1, column=1)

                dm_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dm_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dm_s1t1.get("1.0","end-1c"):
                        command = "delete_maneuver " + dm_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dm_s1_button = tk.Button(entry_panel, text="Delete Maneuver", command=generate_s1)
                dm_s1_button.grid(row=2, column=0)

            elif cmd_a == "apply_radiation_pressure":
                arp_help = tk.Label(entry_panel, text="'apply_radiation_pressure' command sets up a radiation pressure effect on a vessel.")
                arp_help.grid(row=0, column=0, columnspan=10)

                arp_s1t1_label = tk.Label(entry_panel, text="Rad. Press. Name")
                arp_s1t2_label = tk.Label(entry_panel, text="Vessel Name")
                arp_s1t3_label = tk.Label(entry_panel, text="Rad. Source Body")
                arp_s1t4_label = tk.Label(entry_panel, text="Illuminated Area")
                arp_s1t5_label = tk.Label(entry_panel, text="Orient. Frame Body")
                arp_s1t6_label = tk.Label(entry_panel, text="React. Direction")
                arp_s1t7_label = tk.Label(entry_panel, text="Vessel Mass")
                arp_s1t8_label = tk.Label(entry_panel, text="Mass AutoUpdate(0/1)")
                arp_s1t1_label.grid(row=1, column=1)
                arp_s1t2_label.grid(row=1, column=2)
                arp_s1t3_label.grid(row=1, column=3)
                arp_s1t4_label.grid(row=1, column=4)
                arp_s1t5_label.grid(row=1, column=5)
                arp_s1t6_label.grid(row=1, column=6)
                arp_s1t7_label.grid(row=1, column=7)
                arp_s1t8_label.grid(row=1, column=8)

                arp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t2 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t3 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t4 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t5 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t6 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t7 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t8 = tk.Text(entry_panel, width=20, height=1)
                arp_s1t1.grid(row=2, column=1)
                arp_s1t2.grid(row=2, column=2)
                arp_s1t3.grid(row=2, column=3)
                arp_s1t4.grid(row=2, column=4)
                arp_s1t5.grid(row=2, column=5)
                arp_s1t6.grid(row=2, column=6)
                arp_s1t7.grid(row=2, column=7)
                arp_s1t8.grid(row=2, column=8)

                def generate_s1():
                    if (arp_s1t1.get("1.0", "end-1c") and arp_s1t2.get("1.0", "end-1c") and arp_s1t3.get("1.0", "end-1c") and arp_s1t4.get("1.0", "end-1c") and
                        arp_s1t5.get("1.0", "end-1c") and arp_s1t6.get("1.0", "end-1c") and arp_s1t7.get("1.0", "end-1c") and arp_s1t8.get("1.0", "end-1c")):
                        command = "apply_radiation_pressure " + arp_s1t1.get("1.0", "end-1c") + " " + arp_s1t2.get("1.0", "end-1c") + " " + arp_s1t3.get("1.0", "end-1c") + " " + arp_s1t4.get("1.0", "end-1c") + " " + arp_s1t5.get("1.0", "end-1c") + " " + arp_s1t6.get("1.0", "end-1c") + " " + arp_s1t7.get("1.0", "end-1c") + " " + arp_s1t8.get("1.0", "end-1c")
                        add_to_buffer(command)

                arp_s1_button = tk.Button(entry_panel, text="Apply Rad. Press.", command=generate_s1)
                arp_s1_button.grid(row=2, column=0)

            elif cmd_a == "remove_radiation_pressure":
                rrp_help = tk.Label(entry_panel, text="'remove_radiation_pressure' command removes a radiation pressure effect from the simulation.")
                rrp_help.grid(row=0, column=0, columnspan=10)
                
                rrp_s1t1_label = tk.Label(entry_panel, text="Rad. Press. Name")
                rrp_s1t1_label.grid(row=1, column=1)

                rrp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rrp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if rrp_s1t1.get("1.0","end-1c"):
                        command = "remove_radiation_pressure " + rrp_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rrp_s1_button = tk.Button(entry_panel, text="Remove Rad. Press.", command=generate_s1)
                rrp_s1_button.grid(row=2, column=0)

            elif cmd_a == "apply_atmospheric_drag":
                aad_help = tk.Label(entry_panel, text="'apply_atmospheric_drag' command sets up an atmospheric drag effect on a vessel.")
                aad_help.grid(row=0, column=0, columnspan=10)

                aad_s1t1_label = tk.Label(entry_panel, text="Atmo. Drag Name")
                aad_s1t2_label = tk.Label(entry_panel, text="Vessel Name")
                aad_s1t3_label = tk.Label(entry_panel, text="Body Name")
                aad_s1t4_label = tk.Label(entry_panel, text="Drag Area")
                aad_s1t5_label = tk.Label(entry_panel, text="Drag Coeff.")
                aad_s1t6_label = tk.Label(entry_panel, text="Vessel Mass")
                aad_s1t7_label = tk.Label(entry_panel, text="Mass AutoUpdate(0/1)")
                aad_s1t1_label.grid(row=1, column=1)
                aad_s1t2_label.grid(row=1, column=2)
                aad_s1t3_label.grid(row=1, column=3)
                aad_s1t4_label.grid(row=1, column=4)
                aad_s1t5_label.grid(row=1, column=5)
                aad_s1t6_label.grid(row=1, column=6)
                aad_s1t7_label.grid(row=1, column=7)

                aad_s1t1 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t2 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t3 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t4 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t5 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t6 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t7 = tk.Text(entry_panel, width=20, height=1)
                aad_s1t1.grid(row=2, column=1)
                aad_s1t2.grid(row=2, column=2)
                aad_s1t3.grid(row=2, column=3)
                aad_s1t4.grid(row=2, column=4)
                aad_s1t5.grid(row=2, column=5)
                aad_s1t6.grid(row=2, column=6)
                aad_s1t7.grid(row=2, column=7)
                
                def generate_s1():
                    if (aad_s1t1.get("1.0", "end-1c") and aad_s1t2.get("1.0", "end-1c") and aad_s1t3.get("1.0", "end-1c") and aad_s1t4.get("1.0", "end-1c") and
                        aad_s1t5.get("1.0", "end-1c") and aad_s1t6.get("1.0", "end-1c") and aad_s1t7.get("1.0", "end-1c")):
                        command = "apply_atmospheric_drag " + aad_s1t1.get("1.0", "end-1c") + " " + aad_s1t2.get("1.0", "end-1c") + " " + aad_s1t3.get("1.0", "end-1c") + " " + aad_s1t4.get("1.0", "end-1c") + " " + aad_s1t5.get("1.0", "end-1c") + " " + aad_s1t6.get("1.0", "end-1c") + " " + aad_s1t7.get("1.0", "end-1c")
                        add_to_buffer(command)

                aad_s1_button = tk.Button(entry_panel, text="Apply Atmo. Drag", command=generate_s1)
                aad_s1_button.grid(row=2, column=0)

            elif cmd_a == "remove_atmospheric_drag":
                rad_help = tk.Label(entry_panel, text="'remove_atmospheric_drag' command removes an atmospheric drag effect from the simulation.")
                rad_help.grid(row=0, column=0, columnspan=10)
                
                rad_s1t1_label = tk.Label(entry_panel, text="Atmo. Drag Name")
                rad_s1t1_label.grid(row=1, column=1)

                rad_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rad_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if rad_s1t1.get("1.0","end-1c"):
                        command = "remove_atmospheric_drag " + rad_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rad_s1_button = tk.Button(entry_panel, text="Remove Atmo. Drag", command=generate_s1)
                rad_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_projection":
                cp_help = tk.Label(entry_panel, text="'create_projection' command creates a 2-body Keplerian orbit projection of an object around a body.")
                cp_help.grid(row=0, column=0, columnspan=10)
                
                cp_s1t1_label = tk.Label(entry_panel, text="Projection Name")
                cp_s1t2_label = tk.Label(entry_panel, text="Satellite")
                cp_s1t3_label = tk.Label(entry_panel, text="Parent Body")
                cp_s1t1_label.grid(row=1, column=1)
                cp_s1t2_label.grid(row=1, column=2)
                cp_s1t3_label.grid(row=1, column=3)

                cp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cp_s1t1.grid(row=2, column=1)
                cp_s1t2.grid(row=2, column=2)
                cp_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if cp_s1t1.get("1.0", "end-1c") and cp_s1t2.get("1.0", "end-1c") and cp_s1t2.get("1.0", "end-1c"):
                        command = "create_projection " + cp_s1t1.get("1.0", "end-1c") + " " + cp_s1t2.get("1.0", "end-1c") + " " + cp_s1t3.get("1.0", "end-1c")
                        add_to_buffer(command)

                cp_s1_button = tk.Button(entry_panel, text="Create Projection", command=generate_s1)
                cp_s1_button.grid(row=2, column=0)
                
            elif cmd_a == "delete_projection":
                dp_help = tk.Label(entry_panel, text="'delete_projection' command removes a 2-body Keplerian orbit projection from the simulation.")
                dp_help.grid(row=0, column=0, columnspan=10)
                
                dp_s1t1_label = tk.Label(entry_panel, text="Projection Name")
                dp_s1t1_label.grid(row=1, column=1)

                dp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dp_s1t1.get("1.0", "end-1c"):
                        command = "delete_projection " + dp_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                dp_s1_button = tk.Button(entry_panel, text="Delete Projection", command=generate_s1)
                dp_s1_button.grid(row=2, column=0)

            elif cmd_a == "update_projection":
                up_help = tk.Label(entry_panel, text="'update_projection' command recalculates a 2-body Keplerian orbit projection at current simulation time.")
                up_help.grid(row=0, column=0, columnspan=10)

                up_s1t1_label = tk.Label(entry_panel, text="Projection Name")
                up_s1t1_label.grid(row=1, column=1)

                up_s1t1 = tk.Text(entry_panel, width=20, height=1)
                up_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if up_s1t1.get("1.0", "end-1c"):
                        command = "update_projection " + up_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                up_s1_button = tk.Button(entry_panel, text="Update Projection", command=generate_s1)
                up_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_resource":
                crs_help = tk.Label(entry_panel, text="'create_resource' command adds a resource item to the simulation to keep track of resources\nsuch as the stored energy aboard a vessel or the signal strength between vessels.")
                crs_help.grid(row=0, column=0, columnspan=10)
                # option 1
                crs_s1t1_label = tk.Label(entry_panel, text="Resource Name")
                crs_s1t2_label = tk.Label(entry_panel, text="Initial Value")
                crs_s1t3_label = tk.Label(entry_panel, text="Equation Type")
                crs_s1t4_label = tk.Label(entry_panel, text="Variable")
                crs_s1t5_label = tk.Label(entry_panel, text="Object 1")
                crs_s1t6_label = tk.Label(entry_panel, text="Object 2")
                crs_s1t7_label = tk.Label(entry_panel, text="Eqn. Coeffs.")
                crs_s1t8_label = tk.Label(entry_panel, text="Value Limits")
                crs_s1t1_label.grid(row=1, column=1)
                crs_s1t2_label.grid(row=1, column=2)
                crs_s1t3_label.grid(row=1, column=3)
                crs_s1t4_label.grid(row=1, column=4)
                crs_s1t5_label.grid(row=1, column=5)
                crs_s1t6_label.grid(row=1, column=6)
                crs_s1t7_label.grid(row=1, column=7)
                crs_s1t8_label.grid(row=1, column=8)

                crs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t2 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t3 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t4 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t5 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t6 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t7 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t8 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t1.grid(row=2, column=1)
                crs_s1t2.grid(row=2, column=2)
                crs_s1t3.grid(row=2, column=3)
                crs_s1t4.grid(row=2, column=4)
                crs_s1t5.grid(row=2, column=5)
                crs_s1t6.grid(row=2, column=6)
                crs_s1t7.grid(row=2, column=7)
                crs_s1t8.grid(row=2, column=8)

                def generate_s1():
                    if crs_s1t1.get("1.0", "end-1c") and crs_s1t2.get("1.0", "end-1c") and crs_s1t3.get("1.0", "end-1c") and crs_s1t4.get("1.0", "end-1c") and crs_s1t5.get("1.0", "end-1c") and crs_s1t6.get("1.0", "end-1c") and crs_s1t7.get("1.0", "end-1c") and crs_s1t8.get("1.0", "end-1c"):
                        command = "create_resource " + crs_s1t1.get("1.0", "end-1c") + " " + crs_s1t2.get("1.0", "end-1c") + " " + crs_s1t3.get("1.0", "end-1c") + " " + crs_s1t4.get("1.0", "end-1c") + " " + crs_s1t5.get("1.0", "end-1c") + " " + crs_s1t6.get("1.0", "end-1c") + " " + crs_s1t7.get("1.0", "end-1c") + " " + crs_s1t8.get("1.0", "end-1c")
                        add_to_buffer(command)

                crs_s1_button = tk.Button(entry_panel, text="Create Resource", command=generate_s1)
                crs_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_resource":
                drs_help = tk.Label(entry_panel, text="'delete_resource' command removes a resource item from the simulation.")
                drs_help.grid(row=0, column=0, columnspan=10)

                drs_s1t1_label = tk.Label(entry_panel, text="Resource Name")
                drs_s1t1_label.grid(row=1, column=1)

                drs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                drs_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if drs_s1t1.get("1.0", "end-1c"):
                        command = "delete_resource " + drs_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                drs_s1_button = tk.Button(entry_panel, text="Delete Resource", command=generate_s1)
                drs_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_plot":
                cpl_help = tk.Label(entry_panel, text="'create_plot' command adds a plotter to the simulation to plot some value against simulation time.\nNote: If you are creating a surface coverage plot, enter any placeholder for 'Object 2' field.")
                cpl_help.grid(row=0, column=0, columnspan=10)
                # option 1
                cpl_s1t1_label = tk.Label(entry_panel, text="Plotter Name")
                cpl_s1t2_label = tk.Label(entry_panel, text="Variable")
                cpl_s1t3_label = tk.Label(entry_panel, text="Object 1")
                cpl_s1t4_label = tk.Label(entry_panel, text="Object 2")
                cpl_s1t1_label.grid(row=1, column=1)
                cpl_s1t2_label.grid(row=1, column=2)
                cpl_s1t3_label.grid(row=1, column=3)
                cpl_s1t4_label.grid(row=1, column=4)

                cpl_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cpl_s1t1.grid(row=2, column=1)
                cpl_s1t2.grid(row=2, column=2)
                cpl_s1t3.grid(row=2, column=3)
                cpl_s1t4.grid(row=2, column=4)

                def generate_s1():
                    if cpl_s1t1.get("1.0","end-1c") and cpl_s1t2.get("1.0","end-1c") and cpl_s1t3.get("1.0","end-1c") and cpl_s1t4.get("1.0","end-1c"):
                        command = "create_plot " + cpl_s1t1.get("1.0","end-1c") + " " + cpl_s1t2.get("1.0","end-1c") + " " + cpl_s1t3.get("1.0","end-1c") + " " + cpl_s1t4.get("1.0","end-1c")
                        add_to_buffer(command)

                cpl_s1_button = tk.Button(entry_panel, text="Create Plotter (default time)", command=generate_s1)
                cpl_s1_button.grid(row=2, column=0)

                # option 2
                cpl_s2t1_label = tk.Label(entry_panel, text="Plotter Name")
                cpl_s2t2_label = tk.Label(entry_panel, text="Variable")
                cpl_s2t3_label = tk.Label(entry_panel, text="Object 1")
                cpl_s2t4_label = tk.Label(entry_panel, text="Object 2")
                cpl_s2t5_label = tk.Label(entry_panel, text="Start Time")
                cpl_s2t6_label = tk.Label(entry_panel, text="End Time")
                cpl_s2t1_label.grid(row=3, column=1)
                cpl_s2t2_label.grid(row=3, column=2)
                cpl_s2t3_label.grid(row=3, column=3)
                cpl_s2t4_label.grid(row=3, column=4)
                cpl_s2t5_label.grid(row=3, column=5)
                cpl_s2t6_label.grid(row=3, column=6)

                cpl_s2t1 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t2 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t3 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t4 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t5 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t6 = tk.Text(entry_panel, width=20, height=1)
                cpl_s2t1.grid(row=4, column=1)
                cpl_s2t2.grid(row=4, column=2)
                cpl_s2t3.grid(row=4, column=3)
                cpl_s2t4.grid(row=4, column=4)
                cpl_s2t5.grid(row=4, column=5)
                cpl_s2t6.grid(row=4, column=6)

                def generate_s2():
                    if cpl_s2t1.get("1.0","end-1c") and cpl_s2t2.get("1.0","end-1c") and cpl_s2t3.get("1.0","end-1c") and cpl_s2t4.get("1.0","end-1c") and cpl_s2t5.get("1.0","end-1c") and cpl_s2t6.get("1.0","end-1c"):
                        command = "create_plot " + cpl_s2t1.get("1.0","end-1c") + " " + cpl_s2t2.get("1.0","end-1c") + " " + cpl_s2t3.get("1.0","end-1c") + " " + cpl_s2t4.get("1.0","end-1c") + " " + cpl_s2t5.get("1.0","end-1c") + " " + cpl_s2t6.get("1.0","end-1c")
                        add_to_buffer(command)

                cpl_s2_button = tk.Button(entry_panel, text="Create Plotter", command=generate_s2)
                cpl_s2_button.grid(row=4, column=0)

            elif cmd_a == "delete_plot":
                dpl_help = tk.Label(entry_panel, text="'delete_plot' command removes a plotter from the simulation.")
                dpl_help.grid(row=0, column=0, columnspan=10)
                
                dpl_s1t1_label = tk.Label(entry_panel, text="Plotter Name")
                dpl_s1t1_label.grid(row=1, column=1)

                dpl_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dpl_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dpl_s1t1.get("1.0","end-1c"):
                        command = "delete_plot " + dpl_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dpl_s1_button = tk.Button(entry_panel, text="Delete Plotter", command=generate_s1)
                dpl_s1_button.grid(row=2, column=0)

            elif cmd_a == "display_plot":
                dsp1_help = tk.Label(entry_panel, text="'display_plot' command displays a plotter with matplotlib.")
                dsp1_help.grid(row=0, column=0, columnspan=10)

                dsp1_s1t1_label = tk.Label(entry_panel, text="Plotter Name")
                dsp1_s1t1_label.grid(row=1, column=1)

                dspl_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dspl_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dspl_s1t1.get("1.0","end-1c"):
                        command = "display_plot " + dspl_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dspl_s1_button = tk.Button(entry_panel, text="Display Plot", command=generate_s1)
                dspl_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_proximity_zone":
                cpz_help = tk.Label(entry_panel, text="'create_proximity_zone' command creates a proximity zone around a vessel that keeps track of close passes and collisions with other vessels.")
                cpz_help.grid(row=0, column=0, columnspan=10)

                cpz_s1t1_label = tk.Label(entry_panel, text="Zone Name")
                cpz_s1t2_label = tk.Label(entry_panel, text="Vessel Name")
                cpz_s1t3_label = tk.Label(entry_panel, text="Vessel Size (m)")
                cpz_s1t4_label = tk.Label(entry_panel, text="Zone Size (m)")
                cpz_s1t1_label.grid(row=1, column=1)
                cpz_s1t2_label.grid(row=1, column=2)
                cpz_s1t3_label.grid(row=1, column=3)
                cpz_s1t4_label.grid(row=1, column=4)

                cpz_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cpz_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cpz_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cpz_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cpz_s1t1.grid(row=2, column=1)
                cpz_s1t2.grid(row=2, column=2)
                cpz_s1t3.grid(row=2, column=3)
                cpz_s1t4.grid(row=2, column=4)

                def generate_s1():
                    if cpz_s1t1.get("1.0", "end-1c") and cpz_s1t2.get("1.0", "end-1c") and cpz_s1t3.get("1.0", "end-1c") and cpz_s1t4.get("1.0", "end-1c"):
                        command = "create_proximity_zone " + cpz_s1t1.get("1.0", "end-1c") + " " + cpz_s1t2.get("1.0", "end-1c") + " " + cpz_s1t3.get("1.0", "end-1c") + " " + cpz_s1t4.get("1.0", "end-1c")
                        add_to_buffer(command)

                cpz_s1_button = tk.Button(entry_panel, text="Create Zone", command=generate_s1)
                cpz_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_proximity_zone":
                dpz_help = tk.Label(entry_panel, text="'delete_promixity_zone' command removes a proximity zone from the simulation.")
                dpz_help.grid(row=0, column=0, columnspan=10)

                dpz_s1t1_label = tk.Label(entry_panel, text="Zone Name")
                dpz_s1t1_label.grid(row=1, column=1)

                dpz_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dpz_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dpz_s1t1.get("1.0", "end-1c"):
                        command = "delete_proximity_zone " + dpz_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                dpz_s1_button = tk.Button(entry_panel, text="Delete Zone", command=generate_s1)
                dpz_s1_button.grid(row=2, column=0)

            elif cmd_a == "batch":
                bch_help = tk.Label(entry_panel, text="'batch' command reads a batch file and queues the commands to be sent to the interpreter.")
                bch_help.grid(row=0, column=0, columnspan=10)
                
                bch_s1t1_label = tk.Label(entry_panel, text="Batch File (name or full path)")
                bch_s1t1_label.grid(row=1, column=1)

                bch_s1t1 = tk.Text(entry_panel, width=20, height=1)
                bch_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if bch_s1t1.get("1.0","end-1c"):
                        command = "batch " + bch_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                bch_s1_button = tk.Button(entry_panel, text="Read Batch", command=generate_s1)
                bch_s1_button.grid(row=2, column=0)

            elif cmd_a == "export":
                exp_help = tk.Label(entry_panel, text="'export' command exports the current scenario state into an OrbitSim3D scenario (.osf) file.")
                exp_help.grid(row=0, column=0, columnspan=10)

                exp_s1t1_label = tk.Label(entry_panel, text="Filename")
                exp_s1t1_label.grid(row=1, column=1)

                exp_s1t1 = tk.Text(entry_panel, width=20, height=1)
                exp_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if exp_s1t1.get("1.0", "end-1c"):
                        command = "export " + exp_s1t1.get("1.0", "end-1c")
                        add_to_buffer(command)

                exp_s1_button = tk.Button(entry_panel, text="Export", command=generate_s1)
                exp_s1_button.grid(row=2, column=0)

            elif cmd_a == "cam_strafe_speed":
                css_help = tk.Label(entry_panel, text="'cam_strafe_speed' command sets the speed of linear camera movement.")
                css_help.grid(row=0, column=0, columnspan=10)
                
                css_s1t1_label = tk.Label(entry_panel, text="Speed")
                css_s1t1_label.grid(row=1, column=1)

                css_s1t1 = tk.Text(entry_panel, width=20, height=1)
                css_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if css_s1t1.get("1.0","end-1c"):
                        command = "cam_strafe_speed " + css_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                css_s1_button = tk.Button(entry_panel, text="Set Speed", command=generate_s1)
                css_s1_button.grid(row=2, column=0)

            elif cmd_a == "cam_rotate_speed":
                crs_help = tk.Label(entry_panel, text="'cam_rotate_speed' command sets the speed of camera rotation.")
                crs_help.grid(row=0, column =0, columnspan=10)

                crs_s1t1_label = tk.Label(entry_panel, text="Speed")
                crs_s1t1_label.grid(row=1, column=1)

                crs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                crs_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if crs_s1t1.get("1.0","end-1c"):
                        command = "cam_rotate_speed " + crs_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                crs_s1_button = tk.Button(entry_panel, text="Set Speed", command=generate_s1)
                crs_s1_button.grid(row=2, column=0)

            elif cmd_a == "lock_cam":
                loc_help = tk.Label(entry_panel, text="'lock_cam' command locks the active camera to an object (if it exists).")
                loc_help.grid(row=0, column=0, columnspan=10)
                
                loc_s1t1_label = tk.Label(entry_panel, text="Target Obj.")
                loc_s1t1_label.grid(row=1, column=1)

                loc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                loc_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if loc_s1t1.get("1.0","end-1c"):
                        command = "lock_cam " + loc_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                loc_s1_button = tk.Button(entry_panel, text="Lock Camera", command=generate_s1)
                loc_s1_button.grid(row=2, column=0)

            elif cmd_a == "delta_t":
                det_help = tk.Label(entry_panel, text="'delta_t' command sets time step length of each physics frame.")
                det_help.grid(row=0, column=0, columnspan=10)
                
                det_s1t1_label = tk.Label(entry_panel, text="Delta T")
                det_s1t1_label.grid(row=1, column=1)

                det_s1t1 = tk.Text(entry_panel, width=20, height=1)
                det_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if det_s1t1.get("1.0","end-1c"):
                        command = "delta_t " + det_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                det_s1_button = tk.Button(entry_panel, text="Set Dt", command=generate_s1)
                det_s1_button.grid(row=2, column=0)

            elif cmd_a == "cycle_time":
                cyt_help = tk.Label(entry_panel, text="'cycle_time' command sets the amount of time the machine should take to calculate each physics frame.")
                cyt_help.grid(row=0, column=0, columnspan=10)
                
                cyt_s1t1_label = tk.Label(entry_panel, text="Cycle Time")
                cyt_s1t1_label.grid(row=1, column=1)

                cyt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cyt_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if cyt_s1t1.get("1.0","end-1c"):
                        command = "cycle_time " + cyt_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                cyt_s1_button = tk.Button(entry_panel, text="Set Cycle Time", command=generate_s1)
                cyt_s1_button.grid(row=2, column=0)

            elif cmd_a == "output_rate":
                otr_help = tk.Label(entry_panel, text="'output_rate' command sets the number of cycles per update for the output buffer.\n(Higher number, higher interval between updates.)")
                otr_help.grid(row=0, column=0, columnspan=10)
                
                otr_s1t1_label = tk.Label(entry_panel, text="Output Rate")
                otr_s1t1_label.grid(row=1, column=1)

                otr_s1t1 = tk.Text(entry_panel, width=20, height=1)
                otr_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if otr_s1t1.get("1.0","end-1c"):
                        command = "output_rate " + otr_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                otr_s1_button = tk.Button(entry_panel, text="Set Output Rate", command=generate_s1)
                otr_s1_button.grid(row=2, column=0)

            elif cmd_a == "solver_type":
                svt_help = tk.Label(entry_panel, text="'solver_type' command selects which physics solver to use.")
                svt_help.grid(row=0, column=0, columnspan=10)

                svt_b0 = tk.Button(entry_panel, text="0 (Symplectic Euler)", command=lambda:add_to_buffer("solver_type 0"))
                svt_b1 = tk.Button(entry_panel, text="1 (Velocity Verlet)", command=lambda:add_to_buffer("solver_type 1"))
                svt_b2 = tk.Button(entry_panel, text="2 (Yoshida 4th Order)", command=lambda:add_to_buffer("solver_type 2"))
                svt_b3 = tk.Button(entry_panel, text="3 (Yoshida 8th Order)", command=lambda:add_to_buffer("solver_type 3"))
                svt_b4 = tk.Button(entry_panel, text="4 (Adaptive Sym. Euler)", command=lambda:add_to_buffer("solver_type 4"))
                svt_b5 = tk.Button(entry_panel, text="5 (Adaptive Vel. Vrlt.)", command=lambda:add_to_buffer("solver_type 5"))
                svt_b6 = tk.Button(entry_panel, text="6 (Adaptive Yoshida4th)", command=lambda:add_to_buffer("solver_type 6"))
                svt_b7 = tk.Button(entry_panel, text="7 (Adaptive Yoshida8th)", command=lambda:add_to_buffer("solver_type 7"))

                svt_b0.config(width=25,height=1)
                svt_b1.config(width=25,height=1)
                svt_b2.config(width=25,height=1)
                svt_b3.config(width=25,height=1)
                svt_b4.config(width=25,height=1)
                svt_b5.config(width=25,height=1)
                svt_b6.config(width=25,height=1)
                svt_b7.config(width=25,height=1)

                svt_b0.grid(row=1, column=0)
                svt_b1.grid(row=2, column=0)
                svt_b2.grid(row=3, column=0)
                svt_b3.grid(row=4, column=0)
                svt_b4.grid(row=1, column=1)
                svt_b5.grid(row=2, column=1)
                svt_b6.grid(row=3, column=1)
                svt_b7.grid(row=4, column=1)

            elif cmd_a == "tolerance":
                tol_help = tk.Label(entry_panel, text="'tolerance' command sets the position error tolerance for adaptive time-step solvers.")
                tol_help.grid(row=0, column=0, columnspan=10)
                
                tol_s1t1_label = tk.Label(entry_panel, text="Tolerance")
                tol_s1t1_label.grid(row=1, column=1)

                tol_s1t1 = tk.Text(entry_panel, width=20, height=1)
                tol_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if tol_s1t1.get("1.0","end-1c"):
                        command = "tolerance " + tol_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                tol_s1_button = tk.Button(entry_panel, text="Set Tol.", command=generate_s1)
                tol_s1_button.grid(row=2, column=0)

            elif cmd_a == "note":
                nte_help = tk.Label(entry_panel, text="'note' command lets the user take a note on the output screen.")
                nte_help.grid(row=0, column=0, columnspan=10)
                
                nte_s1t1_label = tk.Label(entry_panel, text="Note Label")
                nte_s1t2_label = tk.Label(entry_panel, text="Note (spaces allowed)")
                nte_s1t1_label.grid(row=1, column=1)
                nte_s1t2_label.grid(row=1, column=2)

                nte_s1t1 = tk.Text(entry_panel, width=20, height=1)
                nte_s1t2 = tk.Text(entry_panel, width=50, height=3)
                nte_s1t1.grid(row=2, column=1)
                nte_s1t2.grid(row=2, column=2)

                def generate_s1():
                    if nte_s1t1.get("1.0","end-1c") and nte_s1t2.get("1.0","end-1c"):
                        command = "note " + nte_s1t1.get("1.0","end-1c") + " " + nte_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                nte_s1_button = tk.Button(entry_panel, text="Take Note", command=generate_s1)
                nte_s1_button.grid(row=2, column=0)

            elif cmd_a == "vessel_body_collision":
                vbc_help = tk.Label(entry_panel, text="'vessel_body_collision' commands activates or deactivates vessel-body collision checks.")
                vbc_help.grid(row=0, column=0, columnspan=10)

                vbc_s1_button = tk.Button(entry_panel, text="Activate", command=lambda:add_to_buffer("vessel_body_collision 1"))
                vbc_s1_button.config(width=15, height=1)
                vbc_s1_button.grid(row=1, column=0)

                vbc_s2_button = tk.Button(entry_panel, text="Deactivate", command=lambda:add_to_buffer("vessel_body_collision 0"))
                vbc_s2_button.config(width=15, height=1)
                vbc_s2_button.grid(row=1, column=1)

            elif cmd_a == "auto_dt":
                auto_dt_help = tk.Label(entry_panel, text="'auto_dt' is a system that automatically adjusts delta_t at user-set moments in simulation.\nUsually helpful for high-precision playbacks of scenarios.")
                auto_dt_help.grid(row=0, column=0, columnspan=10)

                auto_dt_buffer_field_label = tk.Label(entry_panel, text="Auto-Dt Buffer at T = " + str(sim_time))
                auto_dt_buffer_field_label.grid(row=1, column=0)
                auto_dt_buffer_field = tk.Text(entry_panel, width=20, height=15)
                auto_dt_buffer_field.grid(row=2, column=0, rowspan=5)
                auto_dt_buffer_field.config(state="disabled")

                def set_auto_dt_field():
                    field_text = "Sim. Time - Delta_T\n"
                    
                    n = 0
                    for setting in auto_dt_buffer:
                        field_text += str(n) + ": " + str(setting[0]) + " - " + str(setting[1]) + "\n"
                        n += 1

                    auto_dt_buffer_field.config(state="normal")
                    auto_dt_buffer_field.delete(1.0, "end")
                    auto_dt_buffer_field.insert(1.0, field_text)
                    auto_dt_buffer_field.config(state="disabled")

                set_auto_dt_field()

                # auto_dt
                auto_dt_s1t1_label = tk.Label(entry_panel, text="Sim. Time")
                auto_dt_s1t2_label = tk.Label(entry_panel, text="Delta T")
                auto_dt_s1t1_label.grid(row=1, column=2)
                auto_dt_s1t2_label.grid(row=1, column=3)

                auto_dt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s1t2 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s1t1.grid(row=2, column=2)
                auto_dt_s1t2.grid(row=2, column=3)

                def generate_s1():
                    if auto_dt_s1t1.get("1.0","end-1c") and auto_dt_s1t2.get("1.0","end-1c"):
                        command = "auto_dt " + auto_dt_s1t1.get("1.0","end-1c") + " " + auto_dt_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                auto_dt_s1_button = tk.Button(entry_panel, text="Add Auto-Dt", command=generate_s1)
                auto_dt_s1_button.grid(row=2, column=1)

                # auto_dt_remove
                auto_dt_s2t1_label = tk.Label(entry_panel, text="Auto-Dt Index")
                auto_dt_s2t1_label.grid(row=3, column=2)

                auto_dt_s2t1 = tk.Text(entry_panel, width=20, height=1)
                auto_dt_s2t1.grid(row=4, column=2)

                def generate_s2():
                    if auto_dt_s2t1.get("1.0","end-1c"):
                        command = "auto_dt_remove " + auto_dt_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                auto_dt_s2_button = tk.Button(entry_panel, text="Remove Auto-Dt", command=generate_s2)
                auto_dt_s2_button.grid(row=4, column=1)

                # auto_dt_clear
                auto_dt_s3_button = tk.Button(entry_panel, text="Clear Auto-Dt", command=lambda:add_to_buffer("auto_dt_clear"))
                auto_dt_s3_button.grid(row=5, column=1)

            elif cmd_a == "rapid_compute":
                rapid_compute_help = tk.Label(entry_panel, text="'Rapid compute' is a simulation mode in which very little user output is provided in order to allocate more resources\nfor trajectory calculations, increasing simulation progression rate dramatically without sacrificing physical accuracy.")
                rapid_compute_help.grid(row=0, column=0, columnspan=10)

                rc_buffer_field_label = tk.Label(entry_panel, text="Rapid Compute Buffer at T = " + str(sim_time))
                rc_buffer_field_label.grid(row=1, column=0)
                rc_buffer_field = tk.Text(entry_panel, width=21, height=15)
                rc_buffer_field.grid(row=2, column=0, rowspan=5)
                rc_buffer_field.config(state="disabled")

                def set_rc_field():
                    field_text = "Start Time - End Time\n"
                    
                    n = 0
                    for setting in rapid_compute_buffer:
                        field_text += str(n) + ": " + str(setting[0]) + " - " + str(setting[1]) + "\n"
                        n += 1

                    rc_buffer_field.config(state="normal")
                    rc_buffer_field.delete(1.0, "end")
                    rc_buffer_field.insert(1.0, field_text)
                    rc_buffer_field.config(state="disabled")

                set_rc_field()

                # rapid compute
                rc_s1t1_label = tk.Label(entry_panel, text="Start Time")
                rc_s1t2_label = tk.Label(entry_panel, text="End Time")
                rc_s1t1_label.grid(row=1, column=2)
                rc_s1t2_label.grid(row=1, column=3)

                rc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rc_s1t2 = tk.Text(entry_panel, width=20, height=1)
                rc_s1t1.grid(row=2, column=2)
                rc_s1t2.grid(row=2, column=3)

                def generate_s1():
                    if rc_s1t1.get("1.0","end-1c") and rc_s1t2.get("1.0","end-1c"):
                        command = "rapid_compute " + rc_s1t1.get("1.0","end-1c") + " " + rc_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                rc_s1_button = tk.Button(entry_panel, text="Add Rapid Compute", command=generate_s1)
                rc_s1_button.grid(row=2, column=1)

                # cancel
                rc_s2t1_label = tk.Label(entry_panel, text="Rapid Compute Index")
                rc_s2t1_label.grid(row=3, column=2)

                rc_s2t1 = tk.Text(entry_panel, width=20, height=1)
                rc_s2t1.grid(row=4, column=2)

                def generate_s2():
                    if rc_s2t1.get("1.0","end-1c"):
                        command = "cancel_rapid_compute " + rc_s2t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rc_s2_button = tk.Button(entry_panel, text="Cancel Rapid Compute", command=generate_s2)
                rc_s2_button.grid(row=4, column=1)

                # clear
                rc_s3_button = tk.Button(entry_panel, text="Clear RC Buffer", command=lambda:add_to_buffer("rapid_compute_clear"))
                rc_s3_button.grid(row=5, column=1)

            elif cmd_a == "create_barycenter":
                cbc_help = tk.Label(entry_panel, text="'create_barycenter' marks the barycenter of multiple celestial bodies and allows for calculations\nrelative to that imaginary point in space.")
                cbc_help.grid(row=0, column=0, columnspan=10)

                cbc_s1t1_label = tk.Label(entry_panel, text="Barycenter Name")
                cbc_s1t1_label.grid(row=1, column=1)
                cbc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cbc_s1t1.grid(row=2, column=1)

                cbc_s1t2_label = tk.Label(entry_panel, text="Bodies (separate names with single space)")
                cbc_s1t2_label.grid(row=1, column=2)
                cbc_s1t2 = tk.Text(entry_panel, width=30, height=1)
                cbc_s1t2.grid(row=2, column=2)

                def generate_s1():
                    if cbc_s1t1.get("1.0","end-1c") and cbc_s1t2.get("1.0","end-1c"):
                        command = "create_barycenter " + cbc_s1t1.get("1.0","end-1c") + " " + cbc_s1t2.get("1.0","end-1c")
                        add_to_buffer(command)

                cbc_s1_button = tk.Button(entry_panel, text="Create Barycenter", command=generate_s1)
                cbc_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_barycenter":
                dbc_help = tk.Label(entry_panel, text="'delete_barycenter' removes a previously marked barycenter.")
                dbc_help.grid(row=0, column=0, columnspan=10)

                dbc_s1t1_label = tk.Label(entry_panel, text="Barycenter Name")
                dbc_s1t1_label.grid(row=1, column=1)
                dbc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dbc_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dbc_s1t1.get("1.0","end-1c"):
                        command = "delete_barycenter " + dbc_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dbc_s1_button = tk.Button(entry_panel, text="Delete Barycenter", command=generate_s1)
                dbc_s1_button.grid(row=2, column=0)

            elif cmd_a == "draw_mode":
                draw_mode_help = tk.Label(entry_panel, text="'draw_mode' chooses between scene visualizing methods.")
                draw_mode_help.grid(row=0, column=0, columnspan=10)

                def generate_s1():
                    command = "draw_mode 0"
                    add_to_buffer(command)

                def generate_s2():
                    command = "draw_mode 1"
                    add_to_buffer(command)

                def generate_s3():
                    command = "draw_mode 2"
                    add_to_buffer(command)

                draw_mode_0_button = tk.Button(entry_panel, text="(0) Wireframe", command=generate_s1)
                draw_mode_0_button.config(width=20, height=1)
                draw_mode_0_button.grid(row=1, column=0)

                draw_mode_1_button = tk.Button(entry_panel, text="(1) Filled Polygons", command=generate_s2)
                draw_mode_1_button.config(width=20, height=1)
                draw_mode_1_button.grid(row=1, column=1)

                draw_mode_2_button = tk.Button(entry_panel, text="(2) Fill + Wireframe", command=generate_s3)
                draw_mode_2_button.config(width=20, height=1)
                draw_mode_2_button.grid(row=1, column=2)

            elif cmd_a == "point_size":
                psize_help = tk.Label(entry_panel, text="'point_size' command sets the size of points that represent distant objects in the scene (in pixels).")
                psize_help.grid(row=0, column=0, columnspan=10)
                
                psize_s1t1_label = tk.Label(entry_panel, text="Point Size")
                psize_s1t1_label.grid(row=1, column=1)

                psize_s1t1 = tk.Text(entry_panel, width=20, height=1)
                psize_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if psize_s1t1.get("1.0","end-1c"):
                        command = "point_size " + psize_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                psize_s1_button = tk.Button(entry_panel, text="Set Point Size", command=generate_s1)
                psize_s1_button.grid(row=2, column=0)

            elif cmd_a == "lock_origin":
                lock_origin_help = tk.Label(entry_panel, text="'lock_origin' command locks the global coordinate system origin to a body or vessel for optimizing precision for that particular object.")
                lock_origin_help.grid(row=0, column=0, columnspan=10)

                lo_s1t1_label = tk.Label(entry_panel, text="Object")
                lo_s1t1_label.grid(row=1, column=1)

                lo_s1t1 = tk.Text(entry_panel, width=20, height=1)
                lo_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if lo_s1t1.get("1.0","end-1c"):
                        command = "lock_origin " + lo_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                lo_s1_button = tk.Button(entry_panel, text="Lock Origin", command=generate_s1)
                lo_s1_button.grid(row=2, column=0)

            elif cmd_a == "lock_scene_rot":
                lock_scene_rot_help = tk.Label(entry_panel, text="'lock_scene_rot' command sets the scene rotation rate by locking the view direction to a target object or by defining a constant rotation rate.")
                lock_scene_rot_help.grid(row=0, column=0, columnspan=10)

                lsr_s1t1_label = tk.Label(entry_panel, text="Target Object or Rate (rad/s)")
                lsr_s1t1_label.grid(row=1, column=1)

                lsr_s1t1 = tk.Text(entry_panel, width=20, height=1)
                lsr_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if lsr_s1t1.get("1.0","end-1c"):
                        command = "lock_scene_rot " + lsr_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                lsr_s1_button = tk.Button(entry_panel, text="Lock Sn. Rot.", command=generate_s1)
                lsr_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_schwarzschild":
                create_schwarzschild_help = tk.Label(entry_panel, text="'create_schwarzschild' command adds a Schwarzschild component of the general relativity effects near a massive body.")
                create_schwarzschild_help.grid(row=0, column=0, columnspan=10)

                csch_s1t1_label = tk.Label(entry_panel, text="Name")
                csch_s1t1_label.grid(row=1, column=1)

                csch_s1t2_label = tk.Label(entry_panel, text="Msv. Body")
                csch_s1t2_label.grid(row=1, column=2)

                csch_s1t3_label = tk.Label(entry_panel, text="Vessel")
                csch_s1t3_label.grid(row=1, column=3)

                csch_s1t1 = tk.Text(entry_panel, width=20, height=1)
                csch_s1t1.grid(row=2, column=1)

                csch_s1t2 = tk.Text(entry_panel, width=20, height=1)
                csch_s1t2.grid(row=2, column=2)

                csch_s1t3 = tk.Text(entry_panel, width=20, height=1)
                csch_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if csch_s1t1.get("1.0","end-1c") and csch_s1t2.get("1.0","end-1c") and csch_s1t3.get("1.0","end-1c"):
                        command = "create_schwarzschild " + csch_s1t1.get("1.0","end-1c") + " " + csch_s1t2.get("1.0","end-1c") + " " + csch_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                csch_s1_button = tk.Button(entry_panel, text="Crt. Schwzschld.", command=generate_s1)
                csch_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_schwarzschild":
                dsch_help = tk.Label(entry_panel, text="'delete_schwarzschild' command removes a Schwarzschild component of the general relativity effect near a massive body from the simulation.")
                dsch_help.grid(row=0, column=0, columnspan=10)

                dsch_s1t1_label = tk.Label(entry_panel, text="Sch. Effect Name")
                dsch_s1t1_label.grid(row=1, column=1)
                dsch_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dsch_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dsch_s1t1.get("1.0","end-1c"):
                        command = "delete_schwarzschild " + dsch_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dsch_s1_button = tk.Button(entry_panel, text="Delete Sch. Effect", command=generate_s1)
                dsch_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_lensethirring":
                create_lensethirring_help = tk.Label(entry_panel, text="'create_lensethirring' command adds a frame-dragging component of the general relativity effects near a massive body.")
                create_lensethirring_help.grid(row=0, column=0, columnspan=10)

                clt_s1t1_label = tk.Label(entry_panel, text="Name")
                clt_s1t1_label.grid(row=1, column=1)

                clt_s1t2_label = tk.Label(entry_panel, text="Msv. Body")
                clt_s1t2_label.grid(row=1, column=2)

                clt_s1t3_label = tk.Label(entry_panel, text="Vessel")
                clt_s1t3_label.grid(row=1, column=3)

                clt_s1t4_label = tk.Label(entry_panel, text="Specific Ang. Momentum")
                clt_s1t4_label.grid(row=1, column=4)

                clt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                clt_s1t1.grid(row=2, column=1)

                clt_s1t2 = tk.Text(entry_panel, width=20, height=1)
                clt_s1t2.grid(row=2, column=2)

                clt_s1t3 = tk.Text(entry_panel, width=20, height=1)
                clt_s1t3.grid(row=2, column=3)

                clt_s1t4 = tk.Text(entry_panel, width=20, height=1)
                clt_s1t4.grid(row=2, column=4)

                def generate_s1():
                    if clt_s1t1.get("1.0","end-1c") and clt_s1t2.get("1.0","end-1c") and clt_s1t3.get("1.0","end-1c") and clt_s1t4.get("1.0","end-1c"):
                        command = "create_lensethirring " + clt_s1t1.get("1.0","end-1c") + " " + clt_s1t2.get("1.0","end-1c") + " " + clt_s1t3.get("1.0","end-1c") + " " + clt_s1t4.get("1.0","end-1c")
                        add_to_buffer(command)

                clt_s1_button = tk.Button(entry_panel, text="Crt. Lense-Thrng.", command=generate_s1)
                clt_s1_button.grid(row=2, column=0)

            elif cmd_a == "delete_lensethirring":
                dlt_help = tk.Label(entry_panel, text="'delete_lensethirring' command removes a frame-dragging component of the general relativity effect near a massive body from the simulation.")
                dlt_help.grid(row=0, column=0, columnspan=10)

                dlt_s1t1_label = tk.Label(entry_panel, text="L-T Effect Name")
                dlt_s1t1_label.grid(row=1, column=1)
                dlt_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dlt_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dlt_s1t1.get("1.0","end-1c"):
                        command = "delete_lensethirring " + dlt_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dlt_s1_button = tk.Button(entry_panel, text="Delete L-T Effect", command=generate_s1)
                dlt_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_observation":
                create_observation_help = tk.Label(entry_panel, text="'create_observation' command adds an observation setup to calculate observation ephemerides of a target from an observer.")
                create_observation_help.grid(row=0, column=0, columnspan=10)

                cobs_s1t1_label = tk.Label(entry_panel, text="Name")
                cobs_s1t1_label.grid(row=1, column=1)

                cobs_s1t2_label = tk.Label(entry_panel, text="Observer")
                cobs_s1t2_label.grid(row=1, column=2)

                cobs_s1t3_label = tk.Label(entry_panel, text="Target")
                cobs_s1t3_label.grid(row=1, column=3)

                cobs_s1t4_label = tk.Label(entry_panel, text="Equinox Axis")
                cobs_s1t4_label.grid(row=1, column=4)

                cobs_s1t5_label = tk.Label(entry_panel, text="On-Plane Axis")
                cobs_s1t5_label.grid(row=1, column=5)

                cobs_s1t6_label = tk.Label(entry_panel, text="Pole Axis")
                cobs_s1t6_label.grid(row=1, column=6)

                cobs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t1.grid(row=2, column=1)

                cobs_s1t2 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t2.grid(row=2, column=2)

                cobs_s1t3 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t3.grid(row=2, column=3)

                cobs_s1t4 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t4.grid(row=2, column=4)

                cobs_s1t5 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t5.grid(row=2, column=5)

                cobs_s1t6 = tk.Text(entry_panel, width=20, height=1)
                cobs_s1t6.grid(row=2, column=6)

                def generate_s1():
                    if cobs_s1t1.get("1.0","end-1c") and cobs_s1t2.get("1.0","end-1c") and cobs_s1t3.get("1.0","end-1c") and cobs_s1t4.get("1.0","end-1c") and cobs_s1t5.get("1.0","end-1c") and cobs_s1t6.get("1.0","end-1c"):
                        command = "create_observation " + cobs_s1t1.get("1.0","end-1c") + " " + cobs_s1t2.get("1.0","end-1c") + " " + cobs_s1t3.get("1.0","end-1c") + " " + cobs_s1t4.get("1.0","end-1c") + " " + cobs_s1t5.get("1.0","end-1c") + " " + cobs_s1t6.get("1.0","end-1c")
                        add_to_buffer(command)

                cobs_s1_button = tk.Button(entry_panel, text="Crt. Observ.", command=generate_s1)
                cobs_s1_button.grid(row=2, column=0)

                # --- s2 ---
                cobs_s2t1_label = tk.Label(entry_panel, text="Name")
                cobs_s2t1_label.grid(row=3, column=1)

                cobs_s2t2_label = tk.Label(entry_panel, text="Observer")
                cobs_s2t2_label.grid(row=3, column=2)

                cobs_s2t3_label = tk.Label(entry_panel, text="Target")
                cobs_s2t3_label.grid(row=3, column=3)

                cobs_s2t1 = tk.Text(entry_panel, width=20, height=1)
                cobs_s2t1.grid(row=4, column=1)

                cobs_s2t2 = tk.Text(entry_panel, width=20, height=1)
                cobs_s2t2.grid(row=4, column=2)

                cobs_s2t3 = tk.Text(entry_panel, width=20, height=1)
                cobs_s2t3.grid(row=4, column=3)

                def generate_s2():
                    if cobs_s2t1.get("1.0","end-1c") and cobs_s2t2.get("1.0","end-1c") and cobs_s2t3.get("1.0","end-1c"):
                        command = "create_observation " + cobs_s2t1.get("1.0","end-1c") + " " + cobs_s2t2.get("1.0","end-1c") + " " + cobs_s2t3.get("1.0","end-1c")
                        add_to_buffer(command)

                cobs_s2_button = tk.Button(entry_panel, text="Cr. Obs. (Def. Ax.)", command=generate_s2)
                cobs_s2_button.grid(row=4, column=0)

            elif cmd_a == "delete_observation":
                dobs_help = tk.Label(entry_panel, text="'delete_observation' command removes an observation setup from the simulation.")
                dobs_help.grid(row=0, column=0, columnspan=10)

                dobs_s1t1_label = tk.Label(entry_panel, text="Obsrv. Name")
                dobs_s1t1_label.grid(row=1, column=1)
                dobs_s1t1 = tk.Text(entry_panel, width=20, height=1)
                dobs_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if dobs_s1t1.get("1.0","end-1c"):
                        command = "delete_observation " + dobs_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                dobs_s1_button = tk.Button(entry_panel, text="Delete Obsrv.", command=generate_s1)
                dobs_s1_button.grid(row=2, column=0)

            elif cmd_a == "create_surface_coverage":
                csc_help = tk.Label(entry_panel, text="'create_surface_coverage' command adds a surface coverage computation to the\nsimulation to compute how much of the surface of a body is visible from a vessel.")
                csc_help.grid(row=0, column=0, columnspan=10)

                csc_s1t1_label = tk.Label(entry_panel, text="Surf. Cov. Name")
                csc_s1t2_label = tk.Label(entry_panel, text="Vessel Name")
                csc_s1t3_label = tk.Label(entry_panel, text="Body Name")
                csc_s1t1_label.grid(row=1, column=1)
                csc_s1t2_label.grid(row=1, column=2)
                csc_s1t3_label.grid(row=1, column=3)

                csc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                csc_s1t2 = tk.Text(entry_panel, width=20, height=1)
                csc_s1t3 = tk.Text(entry_panel, width=20, height=1)
                csc_s1t1.grid(row=2, column=1)
                csc_s1t2.grid(row=2, column=2)
                csc_s1t3.grid(row=2, column=3)

                def generate_s1():
                    if csc_s1t1.get("1.0","end-1c") and csc_s1t2.get("1.0","end-1c") and csc_s1t3.get("1.0","end-1c"):
                        command = "create_surface_coverage " + csc_s1t1.get("1.0","end-1c") + " " + csc_s1t2.get("1.0","end-1c") + " " + csc_s1t3.get("1.0","end-1c")
                        add_to_buffer(command)

                csc_s1_button = tk.Button(entry_panel, text="Crt. Surf. Cov.", command=generate_s1)
                csc_s1_button.grid(row=2, column=0)

            elif cmd_a == "remove_surface_coverage":
                rsc_help = tk.Label(entry_panel, text="'remove_surface_coverage' removes a surface coverage computation from the simulation.")
                rsc_help.grid(row=0, column=0, columnspan=10)

                rsc_s1t1_label = tk.Label(entry_panel, text="Surf. Cov. Name")
                rsc_s1t1_label.grid(row=1, column=1)

                rsc_s1t1 = tk.Text(entry_panel, width=20, height=1)
                rsc_s1t1.grid(row=2, column=1)

                def generate_s1():
                    if rsc_s1t1.get("1.0","end-1c"):
                        command = "remove_surface_coverage " + rsc_s1t1.get("1.0","end-1c")
                        add_to_buffer(command)

                rsc_s1_button = tk.Button(entry_panel, text="Rmv. Surf. Cov.", command=generate_s1)
                rsc_s1_button.grid(row=2, column=0)
                
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                
        cmd_window = tk.Tk()
        cmd_window.protocol("WM_DELETE_WINDOW", on_command_window_close)
        cmd_window.title("Commands")
        cmd_window.geometry("408x640")

        # scrolling window
        main_frame = tk.Frame(cmd_window, height=640)
        main_frame.grid(row=0, column=0)

        canvas = tk.Canvas(main_frame, height=640)
        canvas.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, rowspan=999, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # mouse scroll wheel
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # why no 'sender' functionality, tkinter!?
        # anyway, here comes a wall of button definitions
        # it better look decent at runtime, at least...

        current_row = 0
        output_commands_label = tk.Label(scrollable_frame, text="Output Management")
        output_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        show_button = tk.Button(scrollable_frame, text="Show", command=lambda:enter_cmd("show"))
        show_button.config(width=15,height=1)
        show_button.grid(row=current_row, column=0)
        hide_button = tk.Button(scrollable_frame, text="Hide", command=lambda:enter_cmd("hide"))
        hide_button.config(width=15,height=1)
        hide_button.grid(row=current_row, column=1)
        clear_button = tk.Button(scrollable_frame, text="Clear", command=lambda:enter_cmd("clear"))
        clear_button.config(width=15,height=1)
        clear_button.grid(row=current_row, column=2)

        current_row += 1
        vessel_commands_label = tk.Label(scrollable_frame, text="Vessel")
        vessel_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_vessel_button = tk.Button(scrollable_frame, text="Create Vessel", command=lambda:enter_cmd("create_vessel"))
        create_vessel_button.config(width=15,height=1)
        create_vessel_button.grid(row=current_row, column=0)
        delete_vessel_button = tk.Button(scrollable_frame, text="Delete Vessel", command=lambda:enter_cmd("delete_vessel"))
        delete_vessel_button.config(width=15,height=1)
        delete_vessel_button.grid(row=current_row, column=1)
        fragment_button = tk.Button(scrollable_frame, text="Fragment", command=lambda:enter_cmd("fragment"))
        fragment_button.config(width=15,height=1)
        fragment_button.grid(row=current_row, column=2)
        current_row += 1
        create_proximity_zone_button = tk.Button(scrollable_frame, text="Create Prox. Zn.", command=lambda:enter_cmd("create_proximity_zone"))
        create_proximity_zone_button.config(width=15, height=1)
        create_proximity_zone_button.grid(row=current_row, column=0)
        delete_proximity_zone_button = tk.Button(scrollable_frame, text="Delete Prox. Zn.", command=lambda: enter_cmd("delete_proximity_zone"))
        delete_proximity_zone_button.config(width=15, height=1)
        delete_proximity_zone_button.grid(row=current_row, column=1)

        current_row += 1
        mnv_commands_label = tk.Label(scrollable_frame, text="Maneuver")
        mnv_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_maneuver_button = tk.Button(scrollable_frame, text="Create Maneuver", command=lambda:enter_cmd("create_maneuver"))
        create_maneuver_button.config(width=15,height=1)
        create_maneuver_button.grid(row=current_row, column=0)
        delete_maneuver_button = tk.Button(scrollable_frame, text="Delete Maneuver", command=lambda:enter_cmd("delete_maneuver"))
        delete_maneuver_button.config(width=15,height=1)
        delete_maneuver_button.grid(row=current_row, column=1)

        current_row += 1
        rad_press_commands_label = tk.Label(scrollable_frame, text="Non-gravitational Perturbations")
        rad_press_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        apply_rad_press_button = tk.Button(scrollable_frame, text="Apply Rad. Press.", command=lambda:enter_cmd("apply_radiation_pressure"))
        apply_rad_press_button.config(width=15,height=1)
        apply_rad_press_button.grid(row=current_row, column=0)
        remove_rad_press_button = tk.Button(scrollable_frame, text="Remove Rad. Press.", command=lambda:enter_cmd("remove_radiation_pressure"))
        remove_rad_press_button.config(width=15,height=1)
        remove_rad_press_button.grid(row=current_row, column=1)
        current_row += 1
        apply_atmo_drag_button = tk.Button(scrollable_frame, text="Apply Atmo. Drag", command=lambda:enter_cmd("apply_atmospheric_drag"))
        apply_atmo_drag_button.config(width=15,height=1)
        apply_atmo_drag_button.grid(row=current_row, column=0)
        remove_atmo_drag_button = tk.Button(scrollable_frame, text="Remove Atmo. Drag", command=lambda:enter_cmd("remove_atmospheric_drag"))
        remove_atmo_drag_button.config(width=15,height=1)
        remove_atmo_drag_button.grid(row=current_row, column=1)

        current_row += 1
        proj_commands_label = tk.Label(scrollable_frame, text="Orbit Projection")
        proj_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_projection_button = tk.Button(scrollable_frame, text="Create Projection", command=lambda:enter_cmd("create_projection"))
        create_projection_button.config(width=15,height=1)
        create_projection_button.grid(row=current_row, column=0)
        delete_projection_button = tk.Button(scrollable_frame, text="Delete Projection", command=lambda:enter_cmd("delete_projection"))
        delete_projection_button.config(width=15,height=1)
        delete_projection_button.grid(row=current_row, column=1)
        update_projection_button = tk.Button(scrollable_frame, text="Update Projection", command=lambda:enter_cmd("update_projection"))
        update_projection_button.config(width=15,height=1)
        update_projection_button.grid(row=current_row, column=2)

        current_row += 1
        resource_commands_label = tk.Label(scrollable_frame, text="Resource Management")
        resource_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_resource_button = tk.Button(scrollable_frame, text="Create Resource", command=lambda:enter_cmd("create_resource"))
        create_resource_button.config(width=15, height=1)
        create_resource_button.grid(row=current_row, column=0)
        delete_resource_button = tk.Button(scrollable_frame, text="Delete Resource", command=lambda:enter_cmd("delete_resource"))
        delete_resource_button.config(width=15, height=1)
        delete_resource_button.grid(row=current_row, column=1)

        current_row += 1
        observation_commands_label = tk.Label(scrollable_frame, text="Observations")
        observation_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_observation_button = tk.Button(scrollable_frame, text="Create Obsv.", command=lambda:enter_cmd("create_observation"))
        create_observation_button.config(width=15, height=1)
        create_observation_button.grid(row=current_row, column=0)
        delete_observation_button = tk.Button(scrollable_frame, text="Delete Obsv.", command=lambda:enter_cmd("delete_observation"))
        delete_observation_button.config(width=15, height=1)
        delete_observation_button.grid(row=current_row, column=1)
        current_row += 1
        create_surface_coverage_button = tk.Button(scrollable_frame, text="Crt. Surf. Cov.", command=lambda:enter_cmd("create_surface_coverage"))
        create_surface_coverage_button.config(width=15, height=1)
        create_surface_coverage_button.grid(row=current_row, column=0)
        remove_surface_coverage_button = tk.Button(scrollable_frame, text="Rmv. Surf. Cov.", command=lambda:enter_cmd("remove_surface_coverage"))
        remove_surface_coverage_button.config(width=15, height=1)
        remove_surface_coverage_button.grid(row=current_row, column=1)

        current_row += 1
        plot_commands_label = tk.Label(scrollable_frame, text="Plotting")
        plot_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_plot_button = tk.Button(scrollable_frame, text="Create Plot", command=lambda:enter_cmd("create_plot"))
        create_plot_button.config(width=15,height=1)
        create_plot_button.grid(row=current_row, column=0)
        delete_plot_button = tk.Button(scrollable_frame, text="Delete Plot", command=lambda:enter_cmd("delete_plot"))
        delete_plot_button.config(width=15,height=1)
        delete_plot_button.grid(row=current_row, column=1)
        display_plot_button = tk.Button(scrollable_frame, text="Display Plot", command=lambda:enter_cmd("display_plot"))
        display_plot_button.config(width=15, height=1)
        display_plot_button.grid(row=current_row, column=2)

        current_row += 1
        barycenter_commands_label = tk.Label(scrollable_frame, text="Barycenters")
        barycenter_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_barycenter_button = tk.Button(scrollable_frame, text="Create Barycenter", command=lambda:enter_cmd("create_barycenter"))
        create_barycenter_button.grid(row=current_row, column=0)
        create_barycenter_button.config(width=15, height=1)
        delete_barycenter_button = tk.Button(scrollable_frame, text="Delete Barycenter", command=lambda:enter_cmd("delete_barycenter"))
        delete_barycenter_button.grid(row=current_row, column=1)
        delete_barycenter_button.config(width=15, height=1)

        current_row += 1
        batch_commands_label = tk.Label(scrollable_frame, text="File Operations")
        batch_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        read_batch_button = tk.Button(scrollable_frame, text="Read Batch", command=lambda:enter_cmd("batch"))
        read_batch_button.config(width=15,height=1)
        read_batch_button.grid(row=current_row, column=0)
        export_button = tk.Button(scrollable_frame, text="Export Scenario", command=lambda:enter_cmd("export"))
        export_button.config(width=15,height=1)
        export_button.grid(row=current_row, column=1)

        current_row += 1
        cam_commands_label = tk.Label(scrollable_frame, text="Camera Controls")
        cam_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        cam_strafe_speed_button = tk.Button(scrollable_frame, text="Cam. Strafe Speed", command=lambda:enter_cmd("cam_strafe_speed"))
        cam_strafe_speed_button.config(width=15,height=1)
        cam_strafe_speed_button.grid(row=current_row, column=0)
        lock_cam_button = tk.Button(scrollable_frame, text="Lock Camera", command=lambda:enter_cmd("lock_cam"))
        lock_cam_button.config(width=15,height=1)
        lock_cam_button.grid(row=current_row, column=1)
        unlock_cam_button = tk.Button(scrollable_frame, text="Unlock Camera", command=lambda:add_to_buffer("unlock_cam"))
        unlock_cam_button.config(width=15,height=1)
        unlock_cam_button.grid(row=current_row, column=2)
        current_row += 1
        cam_rotate_speed_button = tk.Button(scrollable_frame, text="Cam. Rotate Speed", command=lambda:enter_cmd("cam_rotate_speed"))
        cam_rotate_speed_button.config(width=15,height=1)
        cam_rotate_speed_button.grid(row=current_row, column=0)

        current_row += 1
        time_commands_label = tk.Label(scrollable_frame, text="Time Controls")
        time_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        delta_t_button = tk.Button(scrollable_frame, text="Delta T", command=lambda:enter_cmd("delta_t"))
        delta_t_button.config(width=15,height=1)
        delta_t_button.grid(row=current_row, column=0)
        cycle_time_button = tk.Button(scrollable_frame, text="Cycle Time", command=lambda:enter_cmd("cycle_time"))
        cycle_time_button.config(width=15, height=1)
        cycle_time_button.grid(row=current_row, column=1)
        output_rate_button = tk.Button(scrollable_frame, text="Output Rate", command=lambda:enter_cmd("output_rate"))
        output_rate_button.config(width=15, height=1)
        output_rate_button.grid(row=current_row, column=2)
        current_row += 1
        autodt_button = tk.Button(scrollable_frame, text="Auto-Dt", command=lambda:enter_cmd("auto_dt"))
        autodt_button.config(width=15, height=1)
        autodt_button.grid(row=current_row, column=1)
        rapid_compute_button = tk.Button(scrollable_frame, text="Rapid Compute", command=lambda:enter_cmd("rapid_compute"))
        rapid_compute_button.config(width=15, height=1)
        rapid_compute_button.grid(row=current_row, column=2)

        current_row += 1
        solver_commands_label = tk.Label(scrollable_frame, text="Solver Controls")
        solver_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        solver_type_button = tk.Button(scrollable_frame, text="Solver Type", command=lambda:enter_cmd("solver_type"))
        solver_type_button.config(width=15,height=1)
        solver_type_button.grid(row=current_row, column=0)
        tolerance_button = tk.Button(scrollable_frame, text="Tolerance", command=lambda:enter_cmd("tolerance"))
        tolerance_button.config(width=15,height=1)
        tolerance_button.grid(row=current_row, column=1)

        current_row += 1
        misc_commands_label = tk.Label(scrollable_frame, text="Miscellaneous")
        misc_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        note_button = tk.Button(scrollable_frame, text="Note", command=lambda:enter_cmd("note"))
        note_button.config(width=15, height=1)
        note_button.grid(row=current_row, column=0)
        vessel_body_collision_button = tk.Button(scrollable_frame, text="Vessel-Body Colsn.", command=lambda:enter_cmd("vessel_body_collision"))
        vessel_body_collision_button.config(width=15, height=1)
        vessel_body_collision_button.grid(row=current_row, column=1)

        current_row += 1
        graphics_commands_label = tk.Label(scrollable_frame, text="Graphics")
        graphics_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        draw_mode_button = tk.Button(scrollable_frame, text="Draw Mode", command=lambda:enter_cmd("draw_mode"))
        draw_mode_button.config(width=15, height=1)
        draw_mode_button.grid(row=current_row, column=0)
        point_size_button = tk.Button(scrollable_frame, text="Point Size", command=lambda:enter_cmd("point_size"))
        point_size_button.config(width=15, height=1)
        point_size_button.grid(row=current_row, column=1)
        current_row += 1
        generate_starfield_button = tk.Button(scrollable_frame, text="Gen. Starfield", command=lambda:enter_cmd("generate_starfield"))
        generate_starfield_button.config(width=15, height=1)
        generate_starfield_button.grid(row=current_row, column=0)
        clear_starfield_button = tk.Button(scrollable_frame, text="Clear Starfield", command=lambda:add_to_buffer("clear_starfield"))
        clear_starfield_button.config(width=15, height=1)
        clear_starfield_button.grid(row=current_row, column=1)

        current_row += 1
        selective_precision_commands_label = tk.Label(scrollable_frame, text="Selective Precision")
        selective_precision_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        lock_origin_button = tk.Button(scrollable_frame, text="Lock Origin", command=lambda:enter_cmd("lock_origin"))
        lock_origin_button.config(width=15, height=1)
        lock_origin_button.grid(row=current_row, column=0)
        unlock_origin_button = tk.Button(scrollable_frame, text="Unlock Origin", command=lambda:add_to_buffer("unlock_origin"))
        unlock_origin_button.config(width=15, height=1)
        unlock_origin_button.grid(row=current_row, column=1)
        current_row += 1
        lock_scene_rot_button = tk.Button(scrollable_frame, text="Lock Scene Rot.", command=lambda:enter_cmd("lock_scene_rot"))
        lock_scene_rot_button.config(width=15, height=1)
        lock_scene_rot_button.grid(row=current_row, column=0)
        unlock_scene_rot_button = tk.Button(scrollable_frame, text="Unlk. Sn. Rt.", command=lambda:add_to_buffer("unlock_scene_rot"))
        unlock_scene_rot_button.config(width=15, height=1)
        unlock_scene_rot_button.grid(row=current_row, column=1)

        current_row += 1
        general_relativity_commands_label = tk.Label(scrollable_frame, text="General Relativity")
        general_relativity_commands_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        create_sch_button = tk.Button(scrollable_frame, text="Create Schwrzchld.", command=lambda:enter_cmd("create_schwarzschild"))
        create_sch_button.config(width=15, height=1)
        create_sch_button.grid(row=current_row, column=0)
        delete_sch_button = tk.Button(scrollable_frame, text="Delete Schwrzchld.", command=lambda:enter_cmd("delete_schwarzschild"))
        delete_sch_button.config(width=15, height=1)
        delete_sch_button.grid(row=current_row, column=1)
        current_row += 1
        create_lt_button = tk.Button(scrollable_frame, text="Create Lense-Thrng.", command=lambda:enter_cmd("create_lensethirring"))
        create_lt_button.config(width=15, height=1)
        create_lt_button.grid(row=current_row, column=0)
        delete_lt_button = tk.Button(scrollable_frame, text="Delete Lense-Thrng.", command=lambda:enter_cmd("delete_lensethirring"))
        delete_lt_button.config(width=15, height=1)
        delete_lt_button.grid(row=current_row, column=1)
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_panel_close)
    root.title("OrbitSim3D Graphical Command Panel")

    # COLUMN - OBJECTS
    objects_panel_label = tk.Label(root, text="Simulation Items")
    objects_panel_label.grid(row=0, column=0)
    objects_panel = tk.Text(root, height=24, width=40)
    objects_panel.grid(row=1, column=0, rowspan=10)

    set_objects_text()

    # COLUMN - COMMAND BUTTONS
    command_button = tk.Button(root, text="Enter Command", command=lambda:use_command_window())
    command_button.config(width=25, height=1)
    command_button.grid(row=1, column=2)
    time_command_button = tk.Button(root, text="Asgn. Exec. Time", command=lambda:assign_cmd_time())
    time_command_button.config(width=25, height=1)
    time_command_button.grid(row=2, column=2)
    delete_command_button = tk.Button(root, text="Delete Command", command=lambda:use_command_delete_window())
    delete_command_button.config(width=25, height=1)
    delete_command_button.grid(row=3, column=2)
    confirm_and_close_button = tk.Button(root, text="Confirm Commands and Close", command=on_panel_close)
    confirm_and_close_button.config(width=25, height=1)
    confirm_and_close_button.grid(row=4, column=2)
    clear_button = tk.Button(root, text="Clear Command Buffer", command=clear_command_buffer)
    clear_button.config(width=25, height=1)
    clear_button.grid(row=5, column=2)

    sim_variables_field_label = tk.Label(root, text="Simulation Variables")
    sim_variables_field_label.grid(row=6, column=2)
    sim_variables_field = tk.Text(root, width=25, height=6)
    sim_variables_field.grid(row=7, column=2, rowspan=5)

    set_vars_field()

    # COLUMN - COMMAND BUFFER
    cbx_label = tk.Label(root, text="Command Buffer")
    cbx_label.grid(row=0, column=7)
    cbx = tk.Text(root, height=24, width=40)
    cbx.grid(row=1, column=7, rowspan=10)
    cbx.config(state="disabled")
    
    root.mainloop()

    return command_buffer
