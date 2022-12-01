import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math_utils import *
from vector3 import *

class camera():
    def __init__(self, name, pos, orient, active, lock=None):
        self.name = name
        self.pos = pos
        self.orient = orient
        self.active = active
        self.lock = lock
        self.offset = vec3()
        
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        req_trans = new_pos - self.pos
        glTranslate(req_trans.x, req_trans.y, req_trans.z)
        self.pos = new_pos

    def move(self, movement):
        
        glTranslate((movement.x * self.orient[0][0]) + (movement.y * self.orient[1][0]) + (movement.z * self.orient[2][0]),
                    (movement.x * self.orient[0][1]) + (movement.y * self.orient[1][1]) + (movement.z * self.orient[2][1]),
                    (movement.x * self.orient[0][2]) + (movement.y * self.orient[1][2]) + (movement.z * self.orient[2][2]))
        
        if not self.lock:
            self.pos = vec3(lst=[self.pos.x + (movement.x * self.orient[0][0]) + (movement.y * self.orient[1][0]) + (movement.z * self.orient[2][0]),
                                 self.pos.y + (movement.x * self.orient[0][1]) + (movement.y * self.orient[1][1]) + (movement.z * self.orient[2][1]),
                                 self.pos.z + (movement.x * self.orient[0][2]) + (movement.y * self.orient[1][2]) + (movement.z * self.orient[2][2])])

        else:
            self.offset = vec3(lst=[self.offset.x + (movement.x * self.orient[0][0]) + (movement.y * self.orient[1][0]) + (movement.z * self.orient[2][0]),
                                    self.offset.y + (movement.x * self.orient[0][1]) + (movement.y * self.orient[1][1]) + (movement.z * self.orient[2][1]),
                                    self.offset.z + (movement.x * self.orient[0][2]) + (movement.y * self.orient[1][2]) + (movement.z * self.orient[2][2])])

    def get_orient(self):
        return self.orient
    
    def get_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_lock(self):
        return self.lock

    def rotate(self, rotation):
        if not self.lock:
            about_pos = self.pos
        else:
            about_pos = self.pos - self.offset
        
        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[0], self.orient[0][0], self.orient[0][1], self.orient[0][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[1], self.orient[1][0], self.orient[1][1], self.orient[1][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[2], self.orient[2][0], self.orient[2][1], self.orient[2][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        self.orient = rotate_matrix(self.orient, rotation)

    def lock_to_target(self, target):
        self.lock = target
        if type(target).__name__ == "body":
            offset_amount = target.get_radius() * 2 * visual_scaling_factor
            self.offset = vec3(lst=self.orient[2]) * -offset_amount
        else:
            self.offset = vec3(0,0,-100)

    def unlock(self):
        self.lock = None
        self.offset = vec3()

    def move_with_lock(self):
        if self.lock:
            self.set_pos(self.lock.get_pos() - self.offset * visual_scaling_factor)
