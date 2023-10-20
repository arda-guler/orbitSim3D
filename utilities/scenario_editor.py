import tkinter as tk
import sys

def edit_scenario(filename):

    def add_entry_field(wnd, entry_text, entry_column, entry_row=0):
        new_label = tk.Label(wnd, text=entry_text)
        new_text_field = tk.Text(wnd)
        new_text_field.config(width=15, height=1)
        new_label.grid(row=entry_row * 3, column=entry_column)
        new_text_field.grid(row=entry_row * 3 + 1, column=entry_column)
        return new_text_field
                
    def lineify():
        lineified_text = ""
        for idx, i in enumerate(item_lines):
            lineified_text += str(idx) + ": " + i + "\n"

        return lineified_text

    def update_text_field():
        text_display.configure(state="normal")
        text_display.delete(1.0, "end-1c")
        text_display.insert("end-1c", lineify())
        text_display.configure(state="disabled")

    def add_body():

        def do_add_body():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_body_text = "B|"
            for i in tfs:
                new_body_text += i.get("1.0", "end-1c") + "|"
            new_body_text = new_body_text[:-1]
                
            item_lines.append(new_body_text)
            update_text_field()
        
        wnd_add_body = tk.Tk()
        wnd_add_body.title("Add Body")

        c_column = 0
        tf1 = add_entry_field(wnd_add_body, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_body, "Model", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_body, "Mass (kg)", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_body, "Radius (m)", c_column)
        c_column += 1
        tf5 = add_entry_field(wnd_add_body, "Color (r, g, b)", c_column)
        c_column += 1
        tf6 = add_entry_field(wnd_add_body, "Position (m, m, m)", c_column)
        c_column += 1
        tf7 = add_entry_field(wnd_add_body, "Velocity (m/s, m/s, m/s)", c_column)
        c_column += 1
        tf8 = add_entry_field(wnd_add_body, "Orientation (3x3 matrix)", c_column)
        c_column += 1
        tf9 = add_entry_field(wnd_add_body, "Day Length (s)", c_column)
        c_column += 1
        tf10 = add_entry_field(wnd_add_body, "Rot. Axis", c_column)
        c_column += 1
        tf11 = add_entry_field(wnd_add_body, "J2 Coefficient", c_column)
        c_column += 1
        tf12 = add_entry_field(wnd_add_body, "Luminosity (W)", c_column)
        c_column += 1
        tf13 = add_entry_field(wnd_add_body, "Sea Lvl. Atmo. Dens. (kg m-3)", c_column)
        c_column += 1
        tf14 = add_entry_field(wnd_add_body, "Scale Height (m)", c_column)

        tfs = [tf1, tf2, tf3, tf4, tf5, tf6, tf7, tf8, tf9, tf10, tf11, tf12, tf13, tf14]

        btn_add_body = tk.Button(wnd_add_body, text="Add Body", command=do_add_body)
        btn_add_body.grid(row=2, column=0, columnspan=13)

    def add_vessel():
        
        def do_add_vessel():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_vessel_text = "V|"
            for i in tfs:
                new_vessel_text += i.get("1.0", "end-1c") + "|"
            new_vessel_text = new_vessel_text[:-1]
                
            item_lines.append(new_vessel_text)
            update_text_field()
        
        wnd_add_vessel = tk.Tk()
        wnd_add_vessel.title("Add Vessel")

        c_column = 0
        tf1 = add_entry_field(wnd_add_vessel, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_vessel, "Model", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_vessel, "Color (r, g, b)", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_vessel, "Position (m, m, m)", c_column)
        c_column += 1
        tf5 = add_entry_field(wnd_add_vessel, "Velocity (m/s, m/s, m/s)", c_column)

        tfs = [tf1, tf2, tf3, tf4, tf5]

        btn_add_vessel = tk.Button(wnd_add_vessel, text="Add Vessel", command=do_add_vessel)
        btn_add_vessel.grid(row=2, column=0, columnspan=5)

    def add_maneuver():
        
        def do_add_mnv_impulsive():
            for i in imp_tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_imp_mnv_text = "M|"
            new_imp_mnv_text += imp_tfs[0].get("1.0", "end-1c") + "|impulsive|"
            for i in imp_tfs[1:]:
                new_imp_mnv_text += i.get("1.0", "end-1c") + "|"
            new_imp_mnv_text = new_imp_mnv_text[:-1]
                
            item_lines.append(new_imp_mnv_text)
            update_text_field()

        def do_add_mnv_const_accel():
            for i in cac_tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_cac_mnv_text = "M|"
            new_cac_mnv_text += cac_tfs[0].get("1.0", "end-1c") + "|const_accel|"
            for i in cac_tfs[1:]:
                new_cac_mnv_text += i.get("1.0", "end-1c") + "|"
            new_cac_mnv_text = new_cac_mnv_text[:-1]
                
            item_lines.append(new_cac_mnv_text)
            update_text_field()

        def do_add_mnv_const_thrust():
            for i in cth_tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_cth_mnv_text = "M|"
            new_cth_mnv_text += cth_tfs[0].get("1.0", "end-1c") + "|const_thrust|"
            for i in cth_tfs[1:]:
                new_cth_mnv_text += i.get("1.0", "end-1c") + "|"
            new_cth_mnv_text = new_cth_mnv_text[:-1]
                
            item_lines.append(new_cth_mnv_text)
            update_text_field()
        
        wnd_add_mnv = tk.Tk()
        wnd_add_mnv.title("Add Maneuver")

        c_row = 0
        c_column = 0
        imp_tf1 = add_entry_field(wnd_add_mnv, "Name", c_column, c_row)
        c_column += 1
        imp_tf2 = add_entry_field(wnd_add_mnv, "Vessel", c_column, c_row)
        c_column += 1
        imp_tf3 = add_entry_field(wnd_add_mnv, "Frame of Ref.", c_column, c_row)
        c_column += 1
        imp_tf4 = add_entry_field(wnd_add_mnv, "Direction", c_column, c_row)
        c_column += 1
        imp_tf5 = add_entry_field(wnd_add_mnv, "Dv (m/s)", c_column, c_row)
        c_column += 1
        imp_tf6 = add_entry_field(wnd_add_mnv, "Time (s)", c_column, c_row)

        imp_tfs = [imp_tf1, imp_tf2, imp_tf3, imp_tf4, imp_tf5, imp_tf6]

        btn_add_mnv_imp = tk.Button(wnd_add_mnv, text="Add Impulsive Maneuver", command=do_add_mnv_impulsive)
        btn_add_mnv_imp.grid(row=2, column=0, columnspan=10)

        c_row += 1
        c_column = 0
        cac_tf1 = add_entry_field(wnd_add_mnv, "Name", c_column, c_row)
        c_column += 1
        cac_tf2 = add_entry_field(wnd_add_mnv, "Vessel", c_column, c_row)
        c_column += 1
        cac_tf3 = add_entry_field(wnd_add_mnv, "Frame of Ref.", c_column, c_row)
        c_column += 1
        cac_tf4 = add_entry_field(wnd_add_mnv, "Direction", c_column, c_row)
        c_column += 1
        cac_tf5 = add_entry_field(wnd_add_mnv, "Accel. (m/s/s)", c_column, c_row)
        c_column += 1
        cac_tf6 = add_entry_field(wnd_add_mnv, "Start Time (s)", c_column, c_row)
        c_column += 1
        cac_tf7 = add_entry_field(wnd_add_mnv, "Duration (s)", c_column, c_row)

        cac_tfs = [cac_tf1, cac_tf2, cac_tf3, cac_tf4, cac_tf5, cac_tf6, cac_tf7]

        btn_add_mnv_cac = tk.Button(wnd_add_mnv, text="Add Const. Accel.", command=do_add_mnv_const_accel)
        btn_add_mnv_cac.grid(row=5, column=0, columnspan=10)

        c_row += 1
        c_column = 0
        cth_tf1 = add_entry_field(wnd_add_mnv, "Name", c_column, c_row)
        c_column += 1
        cth_tf2 = add_entry_field(wnd_add_mnv, "Vessel", c_column, c_row)
        c_column += 1
        cth_tf3 = add_entry_field(wnd_add_mnv, "Frame of Ref.", c_column, c_row)
        c_column += 1
        cth_tf4 = add_entry_field(wnd_add_mnv, "Direction", c_column, c_row)
        c_column += 1
        cth_tf5 = add_entry_field(wnd_add_mnv, "Thrust (N)", c_column, c_row)
        c_column += 1
        cth_tf6 = add_entry_field(wnd_add_mnv, "Init. Mass (kg)", c_column, c_row)
        c_column += 1
        cth_tf7 = add_entry_field(wnd_add_mnv, "Mass Flow (kg/s)", c_column, c_row)
        c_column += 1
        cth_tf8 = add_entry_field(wnd_add_mnv, "Start Time (s)", c_column, c_row)
        c_column += 1
        cth_tf9 = add_entry_field(wnd_add_mnv, "Duration (s)", c_column, c_row)

        cth_tfs = [cth_tf1, cth_tf2, cth_tf3, cth_tf4, cth_tf5, cth_tf6, cth_tf7, cth_tf8, cth_tf9]

        btn_add_mnv_cth = tk.Button(wnd_add_mnv, text="Add Const. Thrust", command=do_add_mnv_const_thrust)
        btn_add_mnv_cth.grid(row=8, column=0, columnspan=10)

    def add_surface_pt():
        
        def do_add_surface_point():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_sp_text = "S|"
            for i in tfs:
                new_sp_text += i.get("1.0", "end-1c") + "|"
            new_sp_text = new_sp_text[:-1]
                
            item_lines.append(new_sp_text)
            update_text_field()
        
        wnd_add_sp = tk.Tk()
        wnd_add_sp.title("Add Surface Point")

        c_column = 0
        tf1 = add_entry_field(wnd_add_sp, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_sp, "Body", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_sp, "Color (r, g, b)", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_sp, "Position (lat, lon, alt)", c_column)

        tfs = [tf1, tf2, tf3, tf4]

        btn_add_sp = tk.Button(wnd_add_sp, text="Add Surface Point", command=do_add_surface_point)
        btn_add_sp.grid(row=2, column=0, columnspan=5)

    def add_barycenter():
        
        def do_add_bc():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_bc_text = "C|"
            for i in tfs:
                new_bc_text += i.get("1.0", "end-1c") + "|"
            new_bc_text = new_bc_text[:-1]
                
            item_lines.append(new_bc_text)
            update_text_field()
        
        wnd_add_bc = tk.Tk()
        wnd_add_bc.title("Add Barycenter")

        c_column = 0
        tf1 = add_entry_field(wnd_add_bc, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_bc, "Bodies (separated by comma (,))", c_column)

        tfs = [tf1, tf2]

        btn_add_bc = tk.Button(wnd_add_bc, text="Add Surface Point", command=do_add_bc)
        btn_add_bc.grid(row=2, column=0, columnspan=5)

    def add_atmos_drag():
        
        def do_add_ad():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_ad_text = "A|"
            for i in tfs:
                new_ad_text += i.get("1.0", "end-1c") + "|"
            new_ad_text = new_ad_text[:-1]
                
            item_lines.append(new_ad_text)
            update_text_field()
        
        wnd_add_ad = tk.Tk()
        wnd_add_ad.title("Add Atmospheric Drag")

        c_column = 0
        tf1 = add_entry_field(wnd_add_ad, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_ad, "Vessel", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_ad, "Body", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_ad, "Drag Area (m2)", c_column)
        c_column += 1
        tf5 = add_entry_field(wnd_add_ad, "Drag Coeff.", c_column)
        c_column += 1
        tf6 = add_entry_field(wnd_add_ad, "Vessel Mass", c_column)
        c_column += 1
        tf7 = add_entry_field(wnd_add_ad, "Auto-update (0/1)", c_column)

        tfs = [tf1, tf2, tf3, tf4, tf5, tf6, tf7]

        btn_add_ad = tk.Button(wnd_add_ad, text="Add Atmo. Drag", command=do_add_ad)
        btn_add_ad.grid(row=2, column=0, columnspan=10)

    def add_rad_press():

        def do_add_rp():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_rp_text = "R|"
            for i in tfs:
                new_rp_text += i.get("1.0", "end-1c") + "|"
            new_rp_text = new_rp_text[:-1]
                
            item_lines.append(new_rp_text)
            update_text_field()
        
        wnd_add_rp = tk.Tk()
        wnd_add_rp.title("Add Radiation Pressure")

        c_column = 0
        tf1 = add_entry_field(wnd_add_rp, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_rp, "Vessel", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_rp, "Body", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_rp, "Illuminated Area (m2)", c_column)
        c_column += 1
        tf5 = add_entry_field(wnd_add_rp, "React. Force Axis", c_column)
        c_column += 1
        tf6 = add_entry_field(wnd_add_rp, "Vessel Mass", c_column)
        c_column += 1
        tf7 = add_entry_field(wnd_add_rp, "Auto-update (0/1)", c_column)

        tfs = [tf1, tf2, tf3, tf4, tf5, tf6, tf7]

        btn_add_rp = tk.Button(wnd_add_rp, text="Add Radiation Press.", command=do_add_rp)
        btn_add_rp.grid(row=2, column=0, columnspan=10)

    def add_prox_zone():

        def do_add_pz():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_pz_text = "P|"
            for i in tfs:
                new_pz_text += i.get("1.0", "end-1c") + "|"
            new_pz_text = new_pz_text[:-1]
                
            item_lines.append(new_pz_text)
            update_text_field()
        
        wnd_add_pz = tk.Tk()
        wnd_add_pz.title("Add Proximity Zone")

        c_column = 0
        tf1 = add_entry_field(wnd_add_pz, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_pz, "Vessel", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_pz, "Vessel Size (m, radius)", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_pz, "Zone Size (m, radius)", c_column)

        tfs = [tf1, tf2, tf3, tf4]

        btn_add_pz = tk.Button(wnd_add_pz, text="Add Prox. Zone", command=do_add_pz)
        btn_add_pz.grid(row=2, column=0, columnspan=10)

    def add_resource():
        
        def do_add_resource():
            for i in tfs:
                if not i.get("1.0", "end-1c"):
                    return

            new_resource_text = "U|"
            for i in tfs:
                new_resource_text += i.get("1.0", "end-1c") + "|"
            new_resource_text = new_resource_text[:-1]
                
            item_lines.append(new_resource_text)
            update_text_field()
        
        wnd_add_resource = tk.Tk()
        wnd_add_resource.title("Add Resource")

        c_column = 0
        tf1 = add_entry_field(wnd_add_resource, "Name", c_column)
        c_column += 1
        tf2 = add_entry_field(wnd_add_resource, "Init. Value", c_column)
        c_column += 1
        tf3 = add_entry_field(wnd_add_resource, "Equation Type", c_column)
        c_column += 1
        tf4 = add_entry_field(wnd_add_resource, "Variable", c_column)
        c_column += 1
        tf5 = add_entry_field(wnd_add_resource, "Object 1", c_column)
        c_column += 1
        tf6 = add_entry_field(wnd_add_resource, "Object 2", c_column)
        c_column += 1
        tf7 = add_entry_field(wnd_add_resource, "Eqn. Coefficients", c_column)
        c_column += 1
        tf8 = add_entry_field(wnd_add_resource, "Value Limits [Min, Max]", c_column)

        tfs = [tf1, tf2, tf3, tf4, tf5, tf6, tf7, tf8]

        btn_add_resource = tk.Button(wnd_add_resource, text="Add Resource", command=do_add_resource)
        btn_add_resource.grid(row=2, column=0, columnspan=10)

    def remove_item():

        def do_remove_item():
            try:
                idx = int(tf1.get("1.0", "end-1c"))
            except:
                return
            
            if len(item_lines) > idx:
                item_lines.remove(item_lines[idx])

            update_text_field()

        wnd_remove_item = tk.Tk()
        wnd_remove_item.title("Remove Item")

        c_column = 0
        tf1 = add_entry_field(wnd_remove_item, "Item Index", c_column)

        tfs = [tf1]

        btn_remove_item = tk.Button(wnd_remove_item, text="Remove Item", command=do_remove_item)
        btn_remove_item.grid(row=2, column=0, columnspan=10)
    
    def add_cmd_button(btn_text, btn_row, btn_cmd):
        new_button = tk.Button(root, text=btn_text, command=btn_cmd)
        new_button.config(width=25, height=1)
        new_button.grid(row=btn_row, column=0)
        btns.append(new_button)

    def save_scenario():
        if len(item_lines):
            with open(filename, "w") as f:
                for i in item_lines:
                    f.write(i + "\n")
        
    if not "." in filename:
        filename = filename + ".osf"

    item_lines = []
    root = tk.Tk()
    root.title("OS3D Scenario Editor - " + filename)
    cmds_label = tk.Label(root, text="Commands")
    cmds_label.grid(row=0, column=0)

    # COMMAND BUTTONS
    btns = []
    btn_texts = ["Add Body", "Add Vessel", "Add Maneuver", "Add Surface Pt.", "Add Barycenter", "Add Atmos. Drag",
                 "Add Rad. Press.", "Add Prox. Zone", "Add Resource", "Remove Item"]
    btn_cmds = [add_body, add_vessel, add_maneuver, add_surface_pt, add_barycenter, add_atmos_drag,
                add_rad_press, add_prox_zone, add_resource, remove_item]

    for i in range(len(btn_texts)):
        add_cmd_button(btn_texts[i], i+1, btn_cmds[i])

    text_display = tk.Text(root)
    text_display.config(width=80, height=30)
    text_display.configure(state="disabled")
    text_display.grid(column=1, row=0, rowspan=50)

    save_button = tk.Button(root, text="Save Scenario", command=save_scenario)
    save_button.grid(row=20, column=0)

    try:
        f = open(filename, "r")
        f_read = f.read()
        item_lines = f_read.split("\n")
        f.close()
        update_text_field()
    except FileNotFoundError:
        pass

def main(sys_args):

    print("OS3D Scenario Editor")
    print("Do not close this window until you save your scenario.")

    def accept_filename():
        if filename_input_field.get("1.0", "end-1c"):
            filename = filename_input_field.get("1.0", "end-1c")
            filename_input_window.destroy()
            edit_scenario(filename)
        else:
            pass

    if len(sys_args) > 2:
        filename = sys_args[1]
    else:
        filename = None

    if not filename:
        filename_input_window = tk.Tk()
        filename_input_window.title("OS3D Scenario Editor")
        filename_input_label = tk.Label(filename_input_window, text="Enter the filename of your scenario:")
        filename_input_label.grid(row=0, column=0)
        filename_input_field = tk.Text(filename_input_window)
        filename_input_field.config(width=50, height=1)
        filename_input_field.grid(row=1, column=0)
        filename_accept_button = tk.Button(filename_input_window, text="OK", command=accept_filename)
        filename_accept_button.config(width=30, height=1)
        filename_accept_button.grid(row=2, column=0)
        filename_input_window.mainloop()

main(sys.argv)
