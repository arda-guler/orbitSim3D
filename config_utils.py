import tkinter as tk
import shutil

def configure_sim():

    def save():
        text_to_save = edit_field.get("1.0", "end-1c")
        current_cfg_file.seek(0)
        current_cfg_file.write(text_to_save)
        current_cfg_file.truncate()

    def dont_save_exit():
        current_cfg_file.close()
        editor_window.destroy()

    def reset_to_defaults():
        default_cfg_file = open("data/config/default.cfg", "r")
        default_cfg_file_text = default_cfg_file.read()
        default_cfg_file.close()
        edit_field.delete(1.0, "end")
        edit_field.insert(1.0, default_cfg_file_text)
        save()

    def on_window_close():
        
        def do_save_exit():
            save()
            current_cfg_file.close()
            editor_window.destroy()
            confirm_window.destroy()

        def dont_save_exit():
            current_cfg_file.close()
            editor_window.destroy()
            confirm_window.destroy()

        current_cfg_file = open("data/config/current.cfg", "r+")
        if not edit_field.get("1.0", "end-1c") == current_cfg_file.read():
            confirm_window = tk.Tk()  
            confirm_disc = tk.Label(confirm_window, text="Do you want to save your changes?")
            confirm_disc.grid(row=0, column=0, columnspan=2)
            b_yes = tk.Button(confirm_window, text="Yes", command=do_save_exit)
            b_no = tk.Button(confirm_window, text="No", command=dont_save_exit)
            b_yes.config(width=6, height=1)
            b_no.config(width=6, height=1)
            b_yes.grid(row=1, column=0)
            b_no.grid(row=1, column=1)
        else:
            dont_save_exit()

    # open current.cfg for edit
    try:
        current_cfg_file = open("data/config/current.cfg", "r+")

    # if current.cfg doesn't exist, duplicate default.cfg
    except FileNotFoundError:
        shutil.copyfile("data/config/default.cfg", "data/config/current.cfg")
        current_cfg_file = open("data/config/current.cfg", "r+")

    current_cfg_file_text = current_cfg_file.read()

    editor_window = tk.Tk()
    editor_window.protocol("WM_DELETE_WINDOW", on_window_close)
    editor_window.title("Config Editor")

    editor_label = tk.Label(editor_window, text="current.cfg")
    editor_label.grid(row=0,column=0,columnspan=3)

    edit_field = tk.Text(editor_window, width=100, height=25)
    edit_field.grid(row=1, column=0, columnspan=3)
    edit_field.insert(1.0, current_cfg_file_text)

    save_button = tk.Button(editor_window, text="Save", command=save)
    save_button.config(width=20, height=1)
    cancel_button = tk.Button(editor_window, text="Cancel Edit", command=dont_save_exit)
    cancel_button.config(width=20, height=1)
    reset_button = tk.Button(editor_window, text="Reset to Defaults", command=reset_to_defaults)
    reset_button.config(width=20, height=1)
    save_button.grid(row=2, column=0)
    cancel_button.grid(row=2, column=1)
    reset_button.grid(row=2, column=2)

    editor_window.mainloop()

def read_current_config():

    def get_float_in_line(line):
        result = None
        
        for word in line.split(" "):
            try:
                result = float(word)
                break
            except:
                pass

        return result

    def get_char_in_line(line):
        result = None

        for word in line.split(" "):
            if len(word) == 1 and not word == "=":
                result = word
                break

        return result

    sim_time = 0
    delta_t = 1
    cycle_time = 0.1
    output_rate = 1

    cam_pos_x = 0
    cam_pos_y = 0
    cam_pos_z = -5000
    cam_strafe_speed = 100
    cam_rotate_speed = 3

    window_x = 800
    window_y = 600
    fov = 70
    near_clip = 0.05
    far_clip = 5000000

    cam_yaw_right = "d"
    cam_yaw_left = "a"
    cam_pitch_down = "w"
    cam_pitch_up = "s"
    cam_roll_cw = "e"
    cam_roll_ccw = "q"
    cam_strafe_left = "j"
    cam_strafe_right = "l"
    cam_strafe_forward = "i"
    cam_strafe_backward = "k"
    cam_strafe_up = "u"
    cam_strafe_down = "o"

    cam_increase_speed = "t"
    cam_decrease_speed = "g"

    warn_cycle_time = 1

    draw_mode = 1
    point_size = 2
    labels_visible = 1
    maneuver_auto_dt = 1
    vessel_body_collision = 1
    batch_autoload = 1
    solver_type = 0
    
    try:
        current_cfg_file = open("data/config/current.cfg", "r")

    # if current.cfg doesn't exist, duplicate default.cfg
    except FileNotFoundError:
        shutil.copyfile("data/config/default.cfg", "data/config/current.cfg")
        current_cfg_file = open("data/config/current.cfg", "r")

    cfg_lines = current_cfg_file.readlines()

    # I swear there is a better way of doing this, I'm probably just dumb
    # at least I don't need this to run fast or anything
    for line in cfg_lines:
        if line[:-1].startswith("sim_time"):
            sim_time = get_float_in_line(line[:-1])
        elif line[:-1].startswith("delta_t"):
            delta_t = get_float_in_line(line[:-1])
        elif line[:-1].startswith("cycle_time"):
            cycle_time = get_float_in_line(line[:-1])
        elif line[:-1].startswith("output_rate"):
            output_rate = get_float_in_line(line[:-1])

        elif line[:-1].startswith("cam_pos_x"):
            cam_pos_x = get_float_in_line(line[:-1])
        elif line[:-1].startswith("cam_pos_y"):
            cam_pos_y = get_float_in_line(line[:-1])
        elif line[:-1].startswith("cam_pos_z"):
            cam_pos_z = get_float_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_speed"):
            cam_strafe_speed = get_float_in_line(line[:-1])
        elif line[:-1].startswith("cam_rotate_speed"):
            cam_rotate_speed = get_float_in_line(line[:-1])

        elif line[:-1].startswith("window_x"):
            window_x = get_float_in_line(line[:-1])
        elif line[:-1].startswith("window_y"):
            window_y = get_float_in_line(line[:-1])
        elif line[:-1].startswith("fov"):
            fov = get_float_in_line(line[:-1])
        elif line[:-1].startswith("near_clip"):
            near_clip = get_float_in_line(line[:-1])
        elif line[:-1].startswith("far_clip"):
            far_clip = get_float_in_line(line[:-1])

        elif line[:-1].startswith("cam_yaw_right"):
            cam_yaw_right = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_yaw_left"):
            cam_yaw_left = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_pitch_up"):
            cam_pitch_up = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_pitch_down"):
            cam_pitch_down = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_roll_cw"):
            cam_roll_cw = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_roll_ccw"):
            cam_roll_ccw = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_left"):
            cam_strafe_left = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_right"):
            cam_strafe_right = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_up"):
            cam_strafe_up = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_down"):
            cam_strafe_down = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_forward"):
            cam_strafe_forward = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_strafe_backward"):
            cam_strafe_backward = get_char_in_line(line[:-1])

        elif line[:-1].startswith("cam_increase_speed"):
            cam_increase_speed = get_char_in_line(line[:-1])
        elif line[:-1].startswith("cam_decrease_speed"):
            cam_decrease_speed = get_char_in_line(line[:-1])

        elif line[:-1].startswith("warn_cycle_time"):
            warn_cycle_time = get_float_in_line(line[:-1])
            
        elif line[:-1].startswith("maneuver_auto_dt"):
            maneuver_auto_dt = get_float_in_line(line[:-1])  
        elif line[:-1].startswith("draw_mode"):
            draw_mode = int(get_float_in_line(line[:-1]))
        elif line[:-1].startswith("point_size"):
            point_size = int(get_float_in_line(line[:-1]))
        elif line[:-1].startswith("labels_visible"):
            labels_visible = int(get_float_in_line(line[:-1]))
        elif line[:-1].startswith("vessel_body_collision"):
            vessel_body_collision = int(get_float_in_line(line[:-1]))
        elif line[:-1].startswith("batch_autoload"):
            batch_autoload = int(get_float_in_line(line[:-1]))
        elif line[:-1].startswith("solver_type"):
            solver_type = int(get_float_in_line(line[:-1]))

    return sim_time, delta_t, cycle_time, output_rate, cam_pos_x, cam_pos_y, cam_pos_z, cam_strafe_speed, cam_rotate_speed,\
           window_x, window_y, fov, near_clip, far_clip, cam_yaw_right, cam_yaw_left, cam_pitch_down, cam_pitch_up, cam_roll_cw, cam_roll_ccw,\
           cam_strafe_left, cam_strafe_right, cam_strafe_forward, cam_strafe_backward, cam_strafe_up, cam_strafe_down, cam_increase_speed, cam_decrease_speed, warn_cycle_time,\
           maneuver_auto_dt, draw_mode, point_size, labels_visible, vessel_body_collision, batch_autoload, solver_type
