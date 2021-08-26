import matplotlib.pyplot as plt

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
            
            self.x_list.append(time)

            if self.var == "alt":
                self.y_list.append(self.obj1.get_alt_above(self.obj2))
            elif self.var == "dist":
                self.y_list.append(self.obj1.get_dist_to(self.obj2))
            elif self.var == "vel_mag":
                self.y_list.append(self.obj1.get_vel_mag_rel_to(self.obj2))

    def display(self):
        plt.plot(self.x_list, self.y_list)
        plt.xlabel(self.x_axis)
        plt.ylabel(self.y_axis)
        plt.title(self.title)
        plt.show()
