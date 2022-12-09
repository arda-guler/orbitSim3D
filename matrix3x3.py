import math

from vector3 import *

class matrix3x3:
    def __init__(self, i1=None, i2=None, i3=None, i4=None, i5=None, i6=None, i7=None, i8=None, i9=None):

        # no input -> identity matrix
        if i1 == None:
            self.m11 = 1
            self.m12 = 0
            self.m13 = 0
            
            self.m21 = 0
            self.m22 = 1
            self.m23 = 0

            self.m31 = 0
            self.m32 = 0
            self.m33 = 1

        # constructing from 3 lists
        elif type(i1) == list and type(i2) == list:
            self.m11 = i1[0]
            self.m12 = i1[1]
            self.m13 = i1[2]

            self.m21 = i2[0]
            self.m22 = i2[1]
            self.m23 = i2[2]

            self.m31 = i3[0]
            self.m32 = i3[1]
            self.m33 = i3[2]

        # constructing from pseudo-matrix outdated lists-in-list
        elif type(i1) == list and i2 == None:
            self.m11 = i1[0][0]
            self.m12 = i1[0][1]
            self.m13 = i1[0][2]

            self.m21 = i1[1][0]
            self.m22 = i1[1][1]
            self.m23 = i1[1][2]

            self.m31 = i1[2][0]
            self.m32 = i1[2][1]
            self.m33 = i1[2][2]

        # constructing from 3 vec3's
        elif type(i1) == type(vec3()):
            self.m11 = i1.x
            self.m12 = i1.y
            self.m13 = i1.z

            self.m21 = i2.x
            self.m22 = i2.y
            self.m23 = i2.z

            self.m31 = i3.x
            self.m32 = i3.y
            self.m33 = i3.z

        # constructing from 9 numbers
        elif type(i1) == float or type(i1) == int:
            self.m11 = i1
            self.m12 = i2
            self.m13 = i3

            self.m21 = i4
            self.m22 = i5
            self.m23 = i6

            self.m31 = i7
            self.m32 = i8
            self.m33 = i9

    def vx(self):
        return vec3(self.m11, self.m12, self.m13)

    def vy(self):
        return vec3(self.m21, self.m22, self.m23)

    def vz(self):
        return vec3(self.m31, self.m32, self.m33)

    def tolist(self):
        return [[self.m11, self.m12, self.m13],
                [self.m21, self.m22, self.m23],
                [self.m31, self.m32, self.m33]]

    def __repr__(self):
        output = "Matrix 3x3\n"
        output += str(self.m11) + "   " + str(self.m12) + "   " + str(self.m13) + "\n"
        output += str(self.m21) + "   " + str(self.m22) + "   " + str(self.m23) + "\n"
        output += str(self.m31) + "   " + str(self.m32) + "   " + str(self.m33) + "\n"

        return output

    def __mul__(self, other):
        n11 = self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31;
        n12 = self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32;
        n13 = self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33;

        n21 = self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31;
        n22 = self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32;
        n23 = self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33;

        n31 = self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31;
        n32 = self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32;
        n33 = self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33;

        return matrix3x3(n11, n12, n13, n21, n22, n23, n31, n32, n33)

    def rotated(self, angle, axis):
        v = axis.normalized()
        a = -math.radians(angle)
        
        c = math.cos(a)
        s = math.sin(a)

        m11 = v.x * v.x * (1 - c) + c;
        m12 = v.x * v.y * (1 - c) - v.z * s;
        m13 = v.x * v.z * (1 - c) + v.y * s;
        m21 = v.y * v.x * (1 - c) + v.z * s;
        m22 = v.y * v.y * (1 - c) + c;
        m23 = v.y * v.z * (1 - c) - v.x * s;
        m31 = v.x * v.z * (1 - c) - v.y * s;
        m32 = v.y * v.z * (1 - c) + v.x * s;
        m33 = v.z * v.z * (1 - c) + c;

        rotation_matrix = matrix3x3(m11, m12, m13, m21, m22, m23, m31, m32, m33)

        return (rotation_matrix * self).normalized()

    def rotate_legacy(self, rotation):
        # take a list of angles to rotate with, in order
        return self.rotate_rel_X(rotation[0]).rotate_rel_Y(rotation[1]).rotate_rel_Z(rotation[2])

    def rotate_rel_X(self, angle):
        return self.rotated(angle, vec3(1,0,0))

    def rotate_rel_Y(self, angle):
        return self.rotated(angle, vec3(0,1,0))

    def rotate_rel_Z(self, angle):
        return self.rotated(angle, vec3(0,0,1))

    def rotate_abs_X(self, angle):
        return self.rotated(angle, self.vx())

    def rotate_abs_Y(self, angle):
        return self.rotated(angle, self.vy())

    def rotate_abs_Z(self, angle):
        return self.rotated(angle, self.vz())

    def normalized(self):
        vx = vec3(self.m11, self.m12, self.m13).normalized()
        vz = vec3(self.m31, self.m32, self.m33)
        vy = vz.cross(vx).normalized()
        vz = vx.cross(vy)

        return matrix3x3(vx, vy, vz)

