import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math_utils import *

class camera():
    def __init__(self, name, pos, orient, active, lock=None):
        self.name = name
        self.pos = pos
        self.orient = orient
        self.active = active
        self.lock = lock
        self.offset = [0,0,0]
        
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        req_trans = [new_pos[0] - self.pos[0],
                     new_pos[1] - self.pos[1],
                     new_pos[2] - self.pos[2]]
        glTranslate(req_trans[0], req_trans[1], req_trans[2])
        self.pos = new_pos

    def move(self, movement):
        
        glTranslate((movement[0] * self.orient[0][0]) + (movement[1] * self.orient[1][0]) + (movement[2] * self.orient[2][0]),
                    (movement[0] * self.orient[0][1]) + (movement[1] * self.orient[1][1]) + (movement[2] * self.orient[2][1]),
                    (movement[0] * self.orient[0][2]) + (movement[1] * self.orient[1][2]) + (movement[2] * self.orient[2][2]))
        
        if not self.lock:
            self.pos = [self.pos[0] + (movement[0] * self.orient[0][0]) + (movement[1] * self.orient[1][0]) + (movement[2] * self.orient[2][0]),
                        self.pos[1] + (movement[0] * self.orient[0][1]) + (movement[1] * self.orient[1][1]) + (movement[2] * self.orient[2][1]),
                        self.pos[2] + (movement[0] * self.orient[0][2]) + (movement[1] * self.orient[1][2]) + (movement[2] * self.orient[2][2])]

        else:
            self.offset = [self.offset[0] + (movement[0] * self.orient[0][0]) + (movement[1] * self.orient[1][0]) + (movement[2] * self.orient[2][0]),
                           self.offset[1] + (movement[0] * self.orient[0][1]) + (movement[1] * self.orient[1][1]) + (movement[2] * self.orient[2][1]),
                           self.offset[2] + (movement[0] * self.orient[0][2]) + (movement[1] * self.orient[1][2]) + (movement[2] * self.orient[2][2])]

    
    def get_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def rotate(self, rotation):
        if not self.lock:
            about_pos = self.pos
        else:
            about_pos = [self.pos[0] - self.offset[0],
                         self.pos[1] - self.offset[1],
                         self.pos[2] - self.offset[2]]
        
        glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
        glRotate(-rotation[0], self.orient[0][0], self.orient[0][1], self.orient[0][2])
        glTranslate(about_pos[0], about_pos[1], about_pos[2])

        glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
        glRotate(-rotation[1], self.orient[1][0], self.orient[1][1], self.orient[1][2])
        glTranslate(about_pos[0], about_pos[1], about_pos[2])

        glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
        glRotate(-rotation[2], self.orient[2][0], self.orient[2][1], self.orient[2][2])
        glTranslate(about_pos[0], about_pos[1], about_pos[2])

        self.orient = rotate_matrix(self.orient, rotation)

    def lock_to_target(self, target):
        self.lock = target
        if type(target).__name__ == "body":
            offset_amount = target.get_radius() * 2 * visual_scaling_factor
            self.offset = vector_scale(self.orient[2], -offset_amount)
        else:
            self.offset = [0,0,-100]

    def unlock(self):
        self.lock = None
        self.offset = [0,0,0]

    def move_with_lock(self):
        if self.lock:
            self.set_pos([self.lock.get_pos()[0] * -visual_scaling_factor + self.offset[0],
                          self.lock.get_pos()[1] * -visual_scaling_factor + self.offset[1],
                          self.lock.get_pos()[2] * -visual_scaling_factor + self.offset[2]])
