import math

from vector3 import *

class observation:
    def __init__(self, name, observer, obj, axes=[vec3(1, 0, 0), vec3(0, 1, 0), vec3(0, 0, 1)]):
        self.name = name
        self.observer = observer
        self.obj = obj
        self.axes = axes
        
        self.RA = None
        self.DEC = None

        self.RA_rate = None
        self.DEC_rate = None

    def get_name(self):
        return self.name

    def calculate(self, dt):
        rel_pos = self.obj.pos - self.observer.pos

        # normally, in ICRF:
        # x is vernal equinox
        # y is some other planar vector
        # z is pole

        # in OS3D:
        # z is vernal equinox
        # y is pole
        # x is some other planar vector
        # (to match OpenGL)

        # convert to ICRF for convenience
        rel_pos_z = self.axes[2].dot(rel_pos)
        rel_pos_x = self.axes[0].dot(rel_pos)
        rel_pos_y = self.axes[1].dot(rel_pos)
        
        x = rel_pos_z
        y = rel_pos_x
        z = rel_pos_y

        r = (x**2 + y**2 + z**2)**0.5

        # the sort of calculations below calculate the "apparent" sky position rather than the "astrometric"
        # positions - be careful while validating with other software! (e.g. using JPL Horizons API, you can specify
        # which one of those you wish to print out)
        
        RA = math.atan2(y, x)
        
        # note - for this to calculate actual declination, the scene should have been rotated
        # such the x-z plane of the simulation matches the celestial equator
        # otherwise it is going to calculate the angle from whatever the elevation above the xz-plane is
        DEC = math.asin(z / r)

        if self.RA and self.DEC:
            RA_rate = (RA - self.RA) / dt
            DEC_rate = (DEC - self.DEC) / dt
        else:
            RA_rate = None
            DEC_rate = None

        self.RA = RA
        self.DEC = DEC

        self.RA_rate = RA_rate
        self.DEC_rate = DEC_rate

    def get_degrees(self):
        return math.degrees(self.RA), math.degrees(self.DEC), math.degrees(self.RA_rate), math.degrees(self.DEC_rate)

    def get_degrees_pos_only(self):
        return math.degrees(self.RA), math.degrees(self.DEC)

    def get_params_str(self):
        if self.RA_rate != None and self.DEC_rate != None:
            RA, DEC, RAr, DECr = self.get_degrees()
            
            output = "\nObservation of " + self.obj.get_name() + " from " + self.observer.get_name() + ":\n"
            output += "RA: " + str(RA) + " deg, DEC: " + str(DEC) + " deg\n"
            output += "RA rate: " + str(RAr) + " deg/s, DEC rate: " + str(DECr) + " deg/s\n"
            output += "\nPseudo-ICRF Base Vectors:\n Equinox (X): " + str(self.axes[0]) + " Plane Definer (Y): " + str(self.axes[1]) + " Pole (Z): " + str(self.axes[2]) + "\n"

        elif self.RA and self.DEC:
            RA, DEC = self.get_degrees_pos_only()

            output = "\nObservation of " + self.obj.get_name() + " from " + self.observer.get_name() + ":\n"
            output += "RA: " + str(RA) + " deg, DEC: " + str(DEC) + " deg\n"
            output += "Calculating angular rates...\n"
            output += "\nPseudo-ICRF Base Vectors:\n Equinox (X): " + str(self.axes[0]) + " Plane Definer (Y): " + str(self.axes[1]) + " Pole (Z): " + str(self.axes[2]) + "\n"

        else:
            output = "Calculating...\n"

        return output

