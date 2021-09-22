import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

from math_utils import *

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1000,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(1000,0,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1000)
    glEnd()

def drawBodies(bodies):

    for b in bodies:
        glColor(b.get_color()[0], b.get_color()[1], b.get_color()[2])

        b.update_draw_pos()
        
        glPushMatrix()

        glTranslatef(b.get_draw_pos()[0], b.get_draw_pos()[1], b.get_draw_pos()[2])

        for mesh in b.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    vertex_i = b.model.vertices[vertex_i]
                    vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient)
                    vertex_i = [vertex_i[0] + b.pos[0], vertex_i[1] + b.pos[1], vertex_i[2] + b.pos[2]]
                    glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])
            glEnd()

        glPopMatrix()

def drawVessels(vessels):

    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        v.update_draw_pos()

        # here we go
        glPushMatrix()

        # put us in correct position
        glTranslatef(v.get_draw_pos()[0], v.get_draw_pos()[1], v.get_draw_pos()[2])

        # (we don't rotate things yet)
        #glRotate(vessel_rot[0], 1, 0, 0)
        #glRotate(vessel_rot[1], 0, 1, 0)
        #glRotate(vessel_rot[2], 0, 0, 1)

        # actually render model now, with triangles
        for mesh in v.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*v.model.vertices[vertex_i])
            glEnd()

        # now get out
        glPopMatrix()

def drawTrajectories(vessels):
    
    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        vertices = v.get_draw_traj_history()

        if len(vertices) > 3:
            for i in range(1, len(vertices)):
                glBegin(GL_LINES)
                glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
                glEnd()

def drawManeuvers(maneuvers):

    for m in maneuvers:
        # change color to maneuver color
        glColor(1.0, 1.0, 0.0)

        vertices = m.get_draw_vertices()

        if len(vertices) > 3:
            for i in range(1, len(vertices)):
                glBegin(GL_LINES)
                glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
                glEnd()

def drawProjections(projections):
    
    for p in projections:
        glColor(p.vessel.get_color()[0]/1.5, p.vessel.get_color()[1]/1.5, p.vessel.get_color()[2]/1.5)

        # draw dashed lines for trajectory
        vertices = p.get_draw_vertices()
        num_of_vertices = len(vertices)
        vertex_groups = []

        i = 0
        while i+500 < len(vertices):
            vertex_groups.append([vertices[i], vertices[i+500]])
            i += 500

        for i in range(1, len(vertex_groups)-1, 2):
            glBegin(GL_LINES)
            glVertex3f(vertex_groups[i][0][0], vertex_groups[i][0][1], vertex_groups[i][0][2])
            glVertex3f(vertex_groups[i][1][0], vertex_groups[i][1][1], vertex_groups[i][1][2])
            glEnd()

        # draw lines to apoapsis and periapsis

        center = p.body.get_pos()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(p.draw_pe[0], p.draw_pe[1], p.draw_pe[2])
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(p.draw_ap[0], p.draw_ap[1], p.draw_ap[2])
        glEnd()
