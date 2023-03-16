import matplotlib.pyplot as plt

from math_utils import *

class plot:
    
    def __init__(self, name, x_name, x_list, y_name, y_list,
                 obj1, obj2, variable, start_time, end_time):
        self.title = name
        self.x_axis = x_name
        self.x_list = x_list
        self.y_axis = y_name
        self.y_list = y_list
        self.obj1 = obj1
        self.obj2 = obj2
        self.var = variable

        self.start_time = start_time
        self.end_time = end_time

    def get_name(self):
        return self.title

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def update(self, time):
        if self.start_time <= time <= self.end_time:
            if self.var == "alt":
                self.x_list.append(time)
                self.y_list.append(self.obj1.get_alt_above(self.obj2))
            elif self.var == "dist":
                self.x_list.append(time)
                self.y_list.append(self.obj1.get_dist_to(self.obj2))
            elif self.var == "vel_mag":
                self.x_list.append(time)
                self.y_list.append(self.obj1.get_vel_mag_rel_to(self.obj2))
            elif self.var == "groundtrack":
                bcc = self.obj1.get_body_centered_coords(self.obj2)
                gpos = impact_gpos(bcc)
                lat = gpos[0]
                lon = gpos[1]
                self.x_list.append(lon)
                self.y_list.append(lat)

    def display(self):
        if self.var != "groundtrack":
            plt.plot(self.x_list, self.y_list)
        else:
            try:
                img_path = "data/images/surface_maps/" + self.obj2.name.lower() + ".png"
                img = plt.imread(img_path)
                plt.imshow(img, extent=[-180, 180, -90, 90])
            except FileNotFoundError:
                pass

            plt.scatter(self.x_list, self.y_list)
            plt.xlim(-180, 180)
            plt.ylim(-90, 90)
        plt.xlabel(self.x_axis)
        plt.ylabel(self.y_axis)
        plt.title(self.title)
        plt.show()
