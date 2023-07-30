import math

from body_class import *

class resource:
    def __init__(self, name, value, equation, variable, obj1, obj2, coeffs, limits):
        self.name = name
        self.value = value
        self.equation = equation
        self.variable = variable
        self.obj1 = obj1
        self.obj2 = obj2
        self.coeffs = coeffs
        self.limits = limits

        self.occultation = 0
        self.last_delta = 0

    def get_name(self):
        return self.name

    def update_occultation(self, bodies):
        s = 0

        if type(self.obj2) is body:
            a = self.obj2.get_angular_radius_from(self.obj1)

            for occulting_body in bodies:
                if (not occulting_body == self.obj2) and self.obj1.get_dist_to(self.obj2) > occulting_body.get_dist_to(self.obj2):

                    b = occulting_body.get_angular_radius_from(self.obj1)

                    vec_to_illum_body = self.obj1.get_unit_vector_towards(self.obj2)
                    vec_to_occult_body = self.obj1.get_unit_vector_towards(occulting_body)
                    c_numerator = vec_to_illum_body.dot(vec_to_occult_body)
                    c_denominator = vec_to_illum_body.mag() * vec_to_occult_body.mag()
                    eq_c = math.acos(c_numerator / c_denominator)

                    # body is covering the star entirely
                    if b - eq_c > a:
                        c_s = 1

                    # the body-star separation is too large, no shadow
                    elif eq_c > b + a:
                        c_s = 0

                    else:
                        eq_x = (eq_c**2 + a**2 - b**2)/(2*eq_c)
                        eq_y = (a**2 - eq_x**2)**(0.5)

                        A = a**2 * math.acos(eq_x/a) + b**2 * math.acos((eq_c-eq_x)/b) - eq_c * eq_y

                        c_s = A/(math.pi * a**2)

                    if c_s > s:
                        s = c_s

        else:
            a = 0

            for occulting_body in bodies:
                if self.obj1.get_dist_to(self.obj2) > occulting_body.get_dist_to(self.obj2):

                    b = occulting_body.get_angular_radius_from(self.obj1)

                    vec_to_illum_body = self.obj1.get_unit_vector_towards(self.obj2)
                    vec_to_occult_body = self.obj1.get_unit_vector_towards(occulting_body)
                    c_numerator = vec_to_illum_body.dot(vec_to_occult_body)
                    c_denominator = vec_to_illum_body.mag() * vec_to_occult_body.mag()
                    eq_c = math.acos(c_numerator / c_denominator)

                    # body is covering the star entirely
                    if b - eq_c > a:
                        c_s = 1

                    # the body-star separation is too large, no shadow
                    elif eq_c > b + a:
                        c_s = 0

                    else:
                        eq_x = (eq_c ** 2 + a ** 2 - b ** 2) / (2 * eq_c)
                        eq_y = (a ** 2 - eq_x ** 2) ** (0.5)

                        A = a ** 2 * math.acos(eq_x / a) + b ** 2 * math.acos((eq_c - eq_x) / b) - eq_c * eq_y

                        c_s = A / (math.pi * a ** 2)

                    if c_s > s:
                        s = c_s

        self.occultation = max(min(s, 1), 0)

    def get_variable(self):
        if self.variable == "dist":
            return self.obj1.get_dist_to(self.obj2)

        elif self.variable == "occultation":
            return self.occultation

        elif self.variable == "dist_occultation":
            return self.obj1.get_dist_to(self.obj2)

        elif self.variable == "alt":
            return self.obj1.get_alt_above(self.obj2)

        elif self.variable == "vel" or self.variable == "vel_mag":
            return self.obj1.get_vel_mag_rel_to(self.obj2)

        elif self.variable == "grav_accel":
            return self.obj1.get_gravity_mag_by(self.obj2)

        elif self.variable == "dummy":
            return 0

    def set_value(self, x):
        self.value = x

    def update_value(self, dt):
        y = 1
        if self.variable.endswith("_occultation"):
            y = (1 - self.occultation)

        x = self.get_variable()
        last_val = self.value

        # = = = INCREMENTAL EQUATIONS = = =
        # y += a
        # y += ax + b
        # y += ax^2 + bx + c
        # and so on...
        if self.equation == "polynomial":
            csum = 0

            for i in range(len(self.coeffs)):
                csum += self.coeffs[i] * x**(len(self.coeffs) - 1 - i) * y

            self.value += csum * dt

        # y += a * log_b(x) + c
        elif self.equation == "logarithmic":
            if not x <= 0:
                self.value += (self.coeffs[0] * math.log(x, self.coeffs[1]) * y + self.coeffs[2]) * dt
            else:
                self.value = float("-inf")

        # y += a * x^b + c
        elif self.equation == "power":
            if not (x == 0 and self.coeffs[1] < 0):
                self.value += (self.coeffs[0] * x**self.coeffs[1] * y + self.coeffs[2]) * dt
            else:
                self.value += self.coeffs[2] * dt

        # = = = ABSOLUTE EQUATIONS = = =
        elif self.equation == "polynomial_abs":
            csum = 0

            for i in range(len(self.coeffs)):
                csum += self.coeffs[i] * x ** (len(self.coeffs) - 1 - i)

            self.value = csum * y

        # y += a * log_b(x) + c
        elif self.equation == "logarithmic_abs":
            if not x <= 0:
                self.value = (self.coeffs[0] * math.log(x, self.coeffs[1]) * y + self.coeffs[2])
            else:
                self.value = float("-inf")

        # y += a * x^b + c
        elif self.equation == "power_abs":
            if not (x == 0 and self.coeffs[1] < 0):
                self.value = (self.coeffs[0] * x ** self.coeffs[1] * y + self.coeffs[2])
            else:
                self.value = self.coeffs[2]

        if self.limits:
            self.value = max(min(self.value, self.limits[1]), self.limits[0])

        self.last_delta = (self.value - last_val) / dt
