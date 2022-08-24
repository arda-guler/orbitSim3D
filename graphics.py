import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from math_utils import *
from ui import *

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

def drawBodies(bodies, active_cam, draw_mode):

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
                
                if draw_mode == 1 or draw_mode == 2:
                    glPolygonMode(GL_FRONT, GL_FILL)
                    glBegin(GL_POLYGON)
                    for face in mesh.faces:
                        for vertex_i in face:
                            vertex_i = b.model.vertices[vertex_i]
                            vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient)
                            vertex_i = [vertex_i[0], vertex_i[1], vertex_i[2]]
                            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])
                    glEnd()
                            
                if draw_mode == 0 or draw_mode == 2:
                    glPolygonMode(GL_FRONT, GL_LINE)
                    if draw_mode == 2:
                        # darken color a bit so that lines are actually visible
                        glColor(b.get_color()[0]/1.25, b.get_color()[1]/1.25, b.get_color()[2]/1.25)
                    glBegin(GL_TRIANGLES)
                    for face in mesh.faces:
                        for vertex_i in face:
                            vertex_i = b.model.vertices[vertex_i]
                            vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient)
                            vertex_i = [vertex_i[0], vertex_i[1], vertex_i[2]]
                            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])
                    glEnd()

        glPopMatrix()

def drawVessels(vessels, active_cam, draw_mode):

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
                if draw_mode == 1 or draw_mode == 2:
                    glPolygonMode(GL_FRONT, GL_FILL)
                    glBegin(GL_POLYGON)
                    for face in mesh.faces:
                        for vertex_i in face:
                            glVertex3f(*v.model.vertices[vertex_i])
                    glEnd()
                if draw_mode == 0 or draw_mode == 2:
                    glPolygonMode(GL_FRONT, GL_LINE)
                    if draw_mode == 2:
                        # darken color a bit so that lines are actually visible
                        glColor(v.get_color()[0]/1.25, v.get_color()[1]/1.25, v.get_color()[2]/1.25)
                    glBegin(GL_TRIANGLES)
                    for face in mesh.faces:
                        for vertex_i in face:
                            glVertex3f(*v.model.vertices[vertex_i])
                    glEnd()

        # now get out
        glPopMatrix()

def drawTrajectories(vessels, scene_lock):
    
    for v in vessels:
        if not v == scene_lock:
            # change color we render with
            glColor(v.get_color()[0], v.get_color()[1], v.get_color()[2])

            vertices = v.get_draw_traj_history()

            if len(vertices) > 3:
                glBegin(GL_LINE_STRIP)
                for i in range(1, len(vertices)):
                    #glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                    glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
                glEnd()

def drawManeuvers(maneuvers):

    # change color to maneuver color
    glColor(1.0, 1.0, 0.0)

    for m in maneuvers:
        
        vertices = m.get_draw_vertices()

        if len(vertices) > 3:
            glBegin(GL_LINE_STRIP)
            for i in range(1, len(vertices)):
                #glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
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
            vertex_groups.append([vector_add_safe(vertices[i], vector_scale(p.get_body().get_pos(), visual_scaling_factor)),
                                  vector_add_safe(vertices[i+500], vector_scale(p.get_body().get_pos(), visual_scaling_factor))])
            i += 500

        for i in range(1, len(vertex_groups)-1, 2):
            glBegin(GL_LINES)
            glVertex3f(vertex_groups[i][0][0], vertex_groups[i][0][1], vertex_groups[i][0][2])
            glVertex3f(vertex_groups[i][1][0], vertex_groups[i][1][1], vertex_groups[i][1][2])
            glEnd()

        # draw lines to apoapsis and periapsis

        center = p.body.get_draw_pos()
        pe_adjusted = vector_add_safe(p.draw_pe, p.get_body().get_draw_pos())
        ap_adjusted = vector_add_safe(p.draw_ap, p.get_body().get_draw_pos())
        an_adjusted = vector_add_safe(p.draw_an, p.get_body().get_draw_pos())
        dn_adjusted = vector_add_safe(p.draw_dn, p.get_body().get_draw_pos())

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(pe_adjusted[0], pe_adjusted[1], pe_adjusted[2])
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(ap_adjusted[0], ap_adjusted[1], ap_adjusted[2])
        glEnd()

        glColor(p.vessel.get_color()[0]/2, p.vessel.get_color()[1]/2, p.vessel.get_color()[2]/2)

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(an_adjusted[0], an_adjusted[1], an_adjusted[2])
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center[0], center[1], center[2])
        glVertex3f(dn_adjusted[0], dn_adjusted[1], dn_adjusted[2])
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

def drawBarycenters(barycenters, active_cam):

    for bc in barycenters:
        
        cam_dist = mag([-bc.get_draw_pos()[0] - active_cam.get_pos()[0],
                        -bc.get_draw_pos()[1] - active_cam.get_pos()[1],
                        -bc.get_draw_pos()[2] - active_cam.get_pos()[2]])

        crossline_length = cam_dist/6
        
        glColor(bc.get_color())
        glPushMatrix()
        glTranslate(bc.get_draw_pos()[0], bc.get_draw_pos()[1], bc.get_draw_pos()[2])
        glBegin(GL_LINES)
        
        glVertex3f(-crossline_length/2, 0, 0)
        glVertex3f(crossline_length/2, 0, 0)

        glVertex3f(0, -crossline_length/2, 0)
        glVertex3f(0, crossline_length/2, 0)

        glVertex3f(0, 0, -crossline_length/2)
        glVertex3f(0, 0, crossline_length/2)

        glEnd()
        glPopMatrix()

def drawBarycenterLabels(bcs, cam, offset=0.05):

    for bc in bcs:

        if world2cam(bc.get_pos(), cam):
            label_render_start = world2cam(bc.get_pos(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(bc.get_name(), vector_scale(bc.get_color(), 2), label_render_start, cam)

def drawBodyLabels(bs, cam, offset=0.05):

    for b in bs:

        if world2cam(b.get_pos(), cam):
            label_render_start = world2cam(b.get_pos(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(b.get_name(), vector_scale(b.get_color(), 2), label_render_start, cam)

def drawSurfacePointLabels(sps, cam, offset=0.05):

    for sp in sps:

        if world2cam(sp.get_pos(), cam):
            
            b = sp.get_body()
            
            camera_distance = mag([-b.get_draw_pos()[0] - cam.get_pos()[0],
                                   -b.get_draw_pos()[1] - cam.get_pos()[1],
                                   -b.get_draw_pos()[2] - cam.get_pos()[2]])

            camera_physical_distance = camera_distance * (1/visual_scaling_factor)

            # only draw if the parent body does not appear too small on the screen

            if not math.degrees(math.atan(b.get_radius()*2/camera_physical_distance)) < 1.5:
                label_render_start = world2cam(sp.get_pos(), cam)
                label_render_start[0] += offset
                label_render_start[1] -= offset
                render_AN(sp.get_name(), vector_scale(sp.get_color(), 2), label_render_start, cam)

def drawVesselLabels(vs, cam, offset=0.05):

    for v in vs:

        if world2cam(v.get_pos(), cam):
            label_render_start = world2cam(v.get_pos(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(v.get_name(), vector_scale(v.get_color(), 2), label_render_start, cam)

def drawProjectionLabels(ps, cam, offset=0.05, size=0.05):

    for p in ps:
        center = p.body.get_draw_pos()
        pe_adjusted = vector_add_safe(p.draw_pe, p.get_body().get_draw_pos())
        ap_adjusted = vector_add_safe(p.draw_ap, p.get_body().get_draw_pos())
        an_adjusted = vector_add_safe(p.draw_an, p.get_body().get_draw_pos())
        dn_adjusted = vector_add_safe(p.draw_dn, p.get_body().get_draw_pos())

        pe_adjusted = vector_scale(pe_adjusted, 1/visual_scaling_factor)
        ap_adjusted = vector_scale(ap_adjusted, 1/visual_scaling_factor)
        an_adjusted = vector_scale(an_adjusted, 1/visual_scaling_factor)
        dn_adjusted = vector_scale(dn_adjusted, 1/visual_scaling_factor)

        if world2cam(pe_adjusted, cam):
            label_render_start = world2cam(pe_adjusted, cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("PERI " + str(p.get_periapsis_alt())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(ap_adjusted, cam):
            label_render_start = world2cam(ap_adjusted, cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("APO " + str(p.get_apoapsis_alt())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(an_adjusted, cam):
            label_render_start = world2cam(an_adjusted, cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("ASCN " + str(p.get_inclination())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(dn_adjusted, cam):
            label_render_start = world2cam(dn_adjusted, cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("DSCN " + str(p.get_inclination())), p.vessel.get_color(), label_render_start, cam, size)

def drawRapidCompute(cam, size=0.2):
    render_AN("RAPID COMPUTE ACTIVE", (1,0,0), [-5, 0.5], cam, size)
    render_AN("PLEASE BE PATIENT", (1,0,0), [-3, -0.5], cam, size/1.5)

def drawScene(bodies, vessels, surface_points, barycenters, projections, maneuvers, active_cam, show_trajectories=True, draw_mode=1, labels_visible=True, scene_lock=None):
    
    # sort the objects by their distance to the camera so we can draw the ones in the front last
    # and it won't look like a ridiculous mess on screen
    # (cam and object coord systems are opposite for some reason!!)
    bodies.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)
    vessels.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)
    surface_points.sort(key=lambda x: mag([-x.get_draw_pos()[0] - active_cam.get_pos()[0], -x.get_draw_pos()[1] - active_cam.get_pos()[1], -x.get_draw_pos()[2] - active_cam.get_pos()[2]]), reverse=True)

    # now we can draw, but make sure vessels behind the bodies are drawn in front too
    # for convenience
    drawBarycenters(barycenters, active_cam)
    drawBodies(bodies, active_cam, draw_mode)
    drawSurfacePoints(surface_points, active_cam)
    drawVessels(vessels, active_cam, draw_mode)

    if not active_cam.get_lock() and labels_visible:
        drawBarycenterLabels(barycenters, active_cam)
        drawBodyLabels(bodies, active_cam)
        drawSurfacePointLabels(surface_points, active_cam)
        drawVesselLabels(vessels, active_cam)

    # draw trajectory and predictions
    if show_trajectories:
        
        drawProjections(projections)
        if not active_cam.get_lock() and labels_visible:
            drawProjectionLabels(projections, active_cam)
            
        drawTrajectories(vessels, scene_lock)
        drawManeuvers(maneuvers)
        
