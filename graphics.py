import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

def drawBodies(bodies):

    for b in bodies:
        glColor(b.get_color()[0], b.get_color()[1], b.get_color()[2])

        b.update_draw_pos()
        
        glPushMatrix()

        glTranslatef(b.get_draw_pos()[0], b.get_draw_pos()[1], b.get_draw_pos()[2])

        # no rotation yet
        #glRotate(0, 1, 0, 0)
        #glRotate(0, 0, 1, 0)
        #glRotate(0, 0, 0, 1)

        for mesh in b.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*b.model.vertices[vertex_i])
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

def drawTrajectories(vessels, cam_pos):
    
    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        vertices = v.get_traj_history()

        if len(vertices) > 3:
            for i in range(1, len(vertices)):
                glBegin(GL_LINES)
                glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
                glEnd()
