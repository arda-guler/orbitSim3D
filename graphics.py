import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math

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

def drawBodies(bodies, active_cam):

    for b in bodies:
        glColor(b.get_color()[0], b.get_color()[1], b.get_color()[2])

        b.update_draw_pos()
        
        glPushMatrix()
        glTranslatef(b.get_draw_pos()[0], b.get_draw_pos()[1], b.get_draw_pos()[2])

        # if the object is too far and appears too small, we can just draw it as a point
        # (cam and object coord systems are opposite for some reason!!)
        camera_distance = mag([-b.get_draw_pos()[0] - active_cam.get_pos()[0],
                               -b.get_draw_pos()[1] - active_cam.get_pos()[1],
                               -b.get_draw_pos()[2] - active_cam.get_pos()[2]])

        camera_physical_distance = camera_distance * (1/visual_scaling_factor)

        if math.degrees(math.atan(b.get_radius()*2/camera_physical_distance)) < 0.85:
            glBegin(GL_POINTS)
            glVertex3f(0, 0, 0)
            glEnd()

        else:
            for mesh in b.model.mesh_list:
                glBegin(GL_POLYGON)
                for face in mesh.faces:
                    for vertex_i in face:
                        vertex_i = b.model.vertices[vertex_i]
                        vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient)
                        vertex_i = [vertex_i[0], vertex_i[1], vertex_i[2]]
                        glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])
                glEnd()

        glPopMatrix()

def drawVessels(vessels, active_cam):

    for v in vessels:
        # change color we render with
        glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

        v.update_draw_pos()

        # here we go
        glPushMatrix()

        # put us in correct position
        glTranslatef(v.get_draw_pos()[0], v.get_draw_pos()[1], v.get_draw_pos()[2])

        # if the vessel is too far away from camera, just draw a point and don't bother
        # with the whole object
        # (cam and object coord systems are opposite for some reason!!)
        camera_distance = mag([-v.get_draw_pos()[0] - active_cam.get_pos()[0],
                               -v.get_draw_pos()[1] - active_cam.get_pos()[1],
                               -v.get_draw_pos()[2] - active_cam.get_pos()[2]])

        if camera_distance > 3000:
            glBegin(GL_POINTS)
            glVertex3f(0, 0, 0)
            glEnd()

        else:
            # actually render model now
            for mesh in v.model.mesh_list:
                glBegin(GL_POLYGON)
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

        center = p.body.get_draw_pos()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(p.draw_pe[0], p.draw_pe[1], p.draw_pe[2])
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(p.draw_ap[0], p.draw_ap[1], p.draw_ap[2])
        glEnd()

def drawSurfacePoints(surface_points, active_cam):

    for sp in surface_points:
        b = sp.get_body()
        
        camera_distance = mag([-b.get_draw_pos()[0] - active_cam.get_pos()[0],
                               -b.get_draw_pos()[1] - active_cam.get_pos()[1],
                               -b.get_draw_pos()[2] - active_cam.get_pos()[2]])

        camera_physical_distance = camera_distance * (1/visual_scaling_factor)

        # only draw if the parent body does not appear too small on the screen

        if not math.degrees(math.atan(b.get_radius()*2/camera_physical_distance)) < 1.5:
            glColor(sp.get_color()[0], sp.get_color()[1], sp.get_color()[2])
            glPushMatrix()
            glTranslate(sp.get_draw_pos()[0], sp.get_draw_pos()[1], sp.get_draw_pos()[2])
            glBegin(GL_POINTS)
            glVertex3f(0,0,0)
            glEnd()
            glPopMatrix()

def drawScene(bodies, vessels, surface_points, projections, maneuvers, active_cam, show_trajectories=True):
    
    # sort the objects by their distance to the camera so we can draw the ones in the front last
    # and it won't look like a ridiculous mess on screen
    # (cam and object coord systems are opposite for some reason!!)
    bodies.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)
    vessels.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)
    surface_points.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)

    # now we can draw, but make sure vessels behind the bodies are drawn in front too
    # for convenience
    drawBodies(bodies, active_cam)
    drawSurfacePoints(surface_points, active_cam)
    drawVessels(vessels, active_cam)

    # draw trajectory and predictions
    if show_trajectories:
        drawProjections(projections)
        drawTrajectories(vessels)
        drawManeuvers(maneuvers)
