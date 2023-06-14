# astrometry.py
#
# Takes astrometry measurements and converts them into
# Earth-centered cartezian coordinates.

import math
PI = math.pi

PI_12 = PI/12
PI_720 = PI/720
PI_43200 = PI/43200

def cos(x):
    return math.cos(x)

def sin(x):
    return math.sin(x)

class RA:
    def __init__(self, h, m, s, neg=False):
        self.h = h
        self.m = m
        self.s = s
        self.neg = neg

    def toRad(self):
        if not self.neg:
            return self.h * PI_12 + self.m * PI_720 + self.s * PI_43200
        else:
            return -self.h * PI_12 - self.m * PI_720 - self.s * PI_43200

class Dec:
    def __init__(self, d, m, s, neg=False):
        self.d = d
        self.m = m
        self.s = s
        self.neg = neg

    def toRad(self):
        deg_decimal = self.d + self.m / 60 + self.s / 3600
        if self.neg:
            deg_decimal = -deg_decimal
        return math.radians(deg_decimal)

def mas2rad(mas):
    return mas * 4.8481368e-9

def mas_yr2rad_s(mas_yr):
    return mas_yr * 4.8481368e-9 / 3.15576e7

def ly2m(ly):
    return ly * 9.4607e15

def solarMass2kg(m):
    return m * 1.98847e30

def solarRadius2m(r):
    return r * 6.957e8

def astrometry2cartezian(ra, dec, r, raRate, decRate, rRate):
    """
    :param ra: right ascension of object (RA(hour, minute, second))
    :param dec: declination of object (Dec(degree, minute, second))
    :param r: distance of object (ly)
    :param raRate: right ascension rate (mas/yr)
    :param decRate: declination rate (mas/yr)
    :param rRate: radial velocity (km/s)
    :return: cartezian state vectors x, y, z, vx, vy, vz (m, m/s)
    """
    ra = ra.toRad()
    dec = dec.toRad()
    r = ly2m(r)

    raRate = mas_yr2rad_s(raRate)
    decRate = mas_yr2rad_s(decRate)
    rRate = rRate * 0.001

    # positions
    x = r * cos(ra) * cos(dec)
    y = r * sin(ra) * cos(dec)
    z = r * sin(dec)

    # velocities
    vx = rRate * cos(ra) * cos(dec) + r * (-sin(ra) * raRate) * cos(dec) + r * cos(ra) * (-sin(dec) * decRate)
    vy = rRate * sin(ra) * cos(dec) + r * (cos(ra) * raRate) * cos(dec) + r * sin(ra) * (-sin(dec) * decRate)
    vz = rRate * sin(dec) + r * cos(dec) * decRate

    return x, y, z, vx, vy, vz

def main():
    print("- - - OS3D ASTROMETRY TO CARTEZIAN CONVERTER - - -")
    print("Enter astrometry data of the object of interest one by one as prompted.\n")

    def process_astrometry():
        RA_input = input("Radial ascension (RA) in degrees, minutes, seconds; separated by commas. (e.g. -14, 39, 36.494): ")
        Dec_input = input("Declination (Dec) in degrees, minutes, seconds; separated by commas. (e.g. -60, 50, 2.3737): ")
        RAdot_input = input("RA proper motion in mas/yr: ")
        Decdot_input = input("Dec proper motion in mas/yr: ")
        dist_input = input("Distance in light years: ")
        distRate_input = input("Radial velocity in km/s: ")
        Ma_input = input("Mass in Solar masses: ")
        Ra_input = input("Radius in Solar radii: ")

        # sanitize RA input
        RA_input = RA_input.split(",")
        RA_deg = float(RA_input[0])
        RA_neg = False
        if RA_deg < 0:
            RA_neg = True
            RA_deg = -RA_deg
        RA_min = float(RA_input[1])
        RA_sec = float(RA_input[2])
        RA_1 = RA(RA_deg, RA_min, RA_sec, neg=RA_neg)

        # sanitize Dec input
        Dec_input = Dec_input.split(",")
        Dec_deg = float(Dec_input[0])
        Dec_neg = False
        if Dec_deg < 0:
            Dec_neg = True
            Dec_deg = -Dec_deg
        Dec_min = float(Dec_input[1])
        Dec_sec = float(Dec_input[2])
        Dec_1 = Dec(Dec_deg, Dec_min, Dec_sec, neg=Dec_neg)

        # get other inputs in proper form
        RAdot = float(RAdot_input)
        Decdot = float(Decdot_input)
        dist = float(dist_input)
        distRate = float(distRate_input)
        M = solarMass2kg(float(Ma_input))
        R = solarRadius2m(float(Ra_input))

        x, y, z, vx, vy, vz = astrometry2cartezian(RA_1, Dec_1, dist, RAdot, Decdot, distRate)

        print("\n- - - OUTPUT - - -")
        print("Mass (kg): ", M)
        print("Radius (m):", R)
        print("Position (m):", x, y, z)
        print("Velocity (m/s):", vx, vy, vz)
        print("")
        print("You can copy the line below to add this body into your scenario file (don't forget to fill in the blanks):")
        print("B|<name>|<model_path>|" + str(M) + "|" + str(R) + "|<rgb color>|" + str([x, y, z]) + "|" + str([vx, vy, vz]) + "|[[1,0,0],[0,1,0],[0,0,1]]|0|0|0|0|0")

        print("")
        again = input("Do you wish to process data for another object (y/N)?: ")
        if again.lower() == "y":
            print("- - - - - - - - - - - - - -\n")
            process_astrometry()

    process_astrometry()

main()
