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
            
        confirm_window = tk.Tk()  
        confirm_disc = tk.Label(confirm_window, text="Do you want to save your changes?")
        confirm_disc.grid(row=0, column=0, columnspan=2)
        b_yes = tk.Button(confirm_window, text="Yes", command=do_save_exit)
        b_no = tk.Button(confirm_window, text="No", command=dont_save_exit)
        b_yes.grid(row=1, column=0)
        b_no.grid(row=1, column=1)

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
    editor_label.grid(row=0,column=0,columnspan=5)

    edit_field = tk.Text(editor_window, width=100, height=25)
    edit_field.grid(row=1, column=0, columnspan=5)
    edit_field.insert(1.0, current_cfg_file_text)

    save_button = tk.Button(editor_window, text="Save", command=save)
    cancel_button = tk.Button(editor_window, text="Cancel Edit", command=dont_save_exit)
    save_button.grid(row=2, column=0)
    cancel_button.grid(row=2, column=1)

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

    return sim_time, delta_t, cycle_time, output_rate, cam_pos_x, cam_pos_y, cam_pos_z, cam_strafe_speed,\
           window_x, window_y, fov, near_clip, far_clip, cam_yaw_right, cam_yaw_left, cam_pitch_down, cam_pitch_up, cam_roll_cw, cam_roll_ccw,\
           cam_strafe_left, cam_strafe_right, cam_strafe_forward, cam_strafe_backward, cam_strafe_up, cam_strafe_down
