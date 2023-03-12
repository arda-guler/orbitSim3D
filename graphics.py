import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from math_utils import *
from vector3 import *
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
        glTranslatef(b.get_draw_pos().x, b.get_draw_pos().y, b.get_draw_pos().z)

        # if the object is too far and appears too small, we can just draw it as a point
        # (cam and object coord systems are opposite for some reason!!)
        camera_distance = (-b.get_draw_pos() - active_cam.get_pos()).mag()
        camera_physical_distance = camera_distance / visual_scaling_factor

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
                            vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient.tolist())
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
                            vertex_i = numpy.matmul(numpy.array(vertex_i), b.orient.tolist())
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
        glTranslatef(v.get_draw_pos().x, v.get_draw_pos().y, v.get_draw_pos().z)

        # if the vessel is too far away from camera, just draw a point and don't bother
        # with the whole object
        # (cam and object coord systems are opposite for some reason!!)
        camera_distance = (-v.get_draw_pos() - active_cam.get_pos()).mag()

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
                    # glVertex3f(vertices[i-1][0], vertices[i-1][1], vertices[i-1][2])
                    glVertex3f(vertices[i].x, vertices[i].y, vertices[i].z)
                glEnd()

def drawManeuvers(maneuvers, point_size, cam):

    for m in maneuvers:

        if m.type != "impulsive":

            if m.type == "const_accel":
                glColor(0.0, 1.0, 1.0)
            else: # const_thrust
                glColor(1.0, 1.0, 0.0)
                
            vertices = m.get_draw_vertices()

            if len(vertices) > 3:
                glBegin(GL_LINE_STRIP)
                for i in range(1, len(vertices)):
                    glVertex3f(vertices[i].x, vertices[i].y, vertices[i].z)
                glEnd()
                
        else:
            if m.get_draw_point():
                glColor(1.0, 0.0, 1.0)
                vertex = m.get_draw_point()
                cam_dist = (cam.get_pos() - vertex).mag()
                mnv_point_size = max(int(60000/cam_dist), 1)
                glPointSize(mnv_point_size)
                glBegin(GL_POINTS)
                glVertex3f(vertex.x, vertex.y, vertex.z)
                glEnd()
                glPointSize(point_size)

def drawProjections(projections):
    
    for p in projections:
        glColor(p.vessel.get_color()[0]/1.5, p.vessel.get_color()[1]/1.5, p.vessel.get_color()[2]/1.5)

        # draw dashed lines for trajectory

        vertices = p.get_draw_vertices()
            
        num_of_vertices = len(vertices)
        vertex_groups = []

        i = 0
        while i+500 < len(vertices):
            vertex_groups.append([vertices[i] + p.get_body().get_pos() * visual_scaling_factor,
                                  vertices[i+500] + p.get_body().get_pos() * visual_scaling_factor])
            i += 500

        for i in range(1, len(vertex_groups)-1, 2):
            glBegin(GL_LINES)
            glVertex3f(vertex_groups[i][0].x, vertex_groups[i][0].y, vertex_groups[i][0].z)
            glVertex3f(vertex_groups[i][1].x, vertex_groups[i][1].y, vertex_groups[i][1].z)
            glEnd()

        # draw lines to apoapsis and periapsis

        center = p.body.get_draw_pos()
        pe_adjusted = p.draw_pe + p.get_body().get_draw_pos()
        ap_adjusted = p.draw_ap + p.get_body().get_draw_pos()
        an_adjusted = p.draw_an + p.get_body().get_draw_pos()
        dn_adjusted = p.draw_dn + p.get_body().get_draw_pos()

        glBegin(GL_LINES)
        glVertex3f(center.x, center.y, center.z)
        glVertex3f(pe_adjusted.x, pe_adjusted.y, pe_adjusted.z)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center.x, center.y, center.z)
        glVertex3f(ap_adjusted.x, ap_adjusted.y, ap_adjusted.z)
        glEnd()

        glColor(p.vessel.get_color()[0]/2, p.vessel.get_color()[1]/2, p.vessel.get_color()[2]/2)

        glBegin(GL_LINES)
        glVertex3f(center.x, center.y, center.z)
        glVertex3f(an_adjusted.x, an_adjusted.y, an_adjusted.z)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(center.x, center.y, center.z)
        glVertex3f(dn_adjusted.x, dn_adjusted.y, dn_adjusted.z)
        glEnd()

def drawSurfacePoints(surface_points, active_cam):

    for sp in surface_points:
        b = sp.get_body()

        camera_distance = (-b.get_draw_pos() - active_cam.get_pos()).mag()
        camera_physical_distance = camera_distance / visual_scaling_factor

        # only draw if the parent body does not appear too small on the screen

        if not math.degrees(math.atan(b.get_radius()*2/camera_physical_distance)) < 1.5:
            glColor(sp.get_color()[0], sp.get_color()[1], sp.get_color()[2])
            glPushMatrix()
            glTranslate(sp.get_draw_pos().x, sp.get_draw_pos().y, sp.get_draw_pos().z)
            glBegin(GL_POINTS)
            glVertex3f(0,0,0)
            glEnd()
            glPopMatrix()

def drawBarycenters(barycenters, active_cam):

    for bc in barycenters:

        cam_dist = (-bc.get_draw_pos() - active_cam.get_pos()).mag()
        crossline_length = cam_dist/6
        
        glColor(bc.get_color())
        glPushMatrix()
        glTranslate(bc.get_draw_pos().x, bc.get_draw_pos().y, bc.get_draw_pos().z)
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

        if world2cam(bc.get_pos().tolist(), cam):
            label_render_start = world2cam(bc.get_pos().tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(bc.get_name(), vector_scale(bc.get_color(), 2), label_render_start, cam)

def drawBodyLabels(bs, cam, offset=0.05):

    for b in bs:

        if world2cam(b.get_pos().tolist(), cam):
            label_render_start = world2cam(b.get_pos().tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(b.get_name(), vector_scale(b.get_color(), 2), label_render_start, cam)

def drawSurfacePointLabels(sps, cam, offset=0.05):

    for sp in sps:

        if world2cam(sp.get_pos(), cam):
            
            b = sp.get_body()

            camera_distance = (-b.get_draw_pos() - cam.get_pos()).mag()
            camera_physical_distance = camera_distance / visual_scaling_factor

            # only draw if the parent body does not appear too small on the screen

            if not math.degrees(math.atan(b.get_radius()*2/camera_physical_distance)) < 1.5:
                label_render_start = world2cam(sp.get_pos().tolist(), cam)
                label_render_start[0] += offset
                label_render_start[1] -= offset
                render_AN(sp.get_name(), vector_scale(sp.get_color(), 2), label_render_start, cam)

def drawVesselLabels(vs, cam, offset=0.05):

    for v in vs:

        if world2cam(v.get_pos().tolist(), cam):
            label_render_start = world2cam(v.get_pos().tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(v.get_name(), vector_scale(v.get_color(), 2), label_render_start, cam)

def drawProjectionLabels(ps, cam, offset=0.05, size=0.05):

    for p in ps:
        center = p.body.get_draw_pos()
        pe_adjusted = p.draw_pe + p.get_body().get_draw_pos()
        ap_adjusted = p.draw_ap + p.get_body().get_draw_pos()
        an_adjusted = p.draw_an + p.get_body().get_draw_pos()
        dn_adjusted = p.draw_dn + p.get_body().get_draw_pos()

        pe_adjusted = pe_adjusted / visual_scaling_factor
        ap_adjusted = ap_adjusted / visual_scaling_factor
        an_adjusted = an_adjusted / visual_scaling_factor
        dn_adjusted = dn_adjusted / visual_scaling_factor

        if world2cam(pe_adjusted, cam):
            label_render_start = world2cam(pe_adjusted.tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("PERI " + str(p.get_periapsis_alt())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(ap_adjusted, cam):
            label_render_start = world2cam(ap_adjusted.tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("APO " + str(p.get_apoapsis_alt())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(an_adjusted, cam):
            label_render_start = world2cam(an_adjusted.tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("ASCN " + str(p.get_inclination())), p.vessel.get_color(), label_render_start, cam, size)

        if world2cam(dn_adjusted, cam):
            label_render_start = world2cam(dn_adjusted.tolist(), cam)
            label_render_start[0] += offset
            label_render_start[1] -= offset
            render_AN(("DSCN " + str(p.get_inclination())), p.vessel.get_color(), label_render_start, cam, size)

def drawRapidCompute(cam, size=0.2):
    render_AN("RAPID COMPUTE ACTIVE", (1,0,0), [-5, 0.5], cam, size)
    render_AN("PLEASE BE PATIENT", (1,0,0), [-3, -0.5], cam, size/1.5)

def drawScene(bodies, vessels, surface_points, barycenters, projections, maneuvers, active_cam, show_trajectories=True, draw_mode=1, labels_visible=True, scene_lock=None, point_size=2):
    
    # sort the objects by their distance to the camera so we can draw the ones in the front last
    # and it won't look like a ridiculous mess on screen
    # (cam and object coord systems are opposite for some reason!!)
    bodies.sort(key=lambda x: (-x.get_draw_pos() - active_cam.get_pos()).mag(), reverse=True)
    vessels.sort(key=lambda x: (-x.get_draw_pos() - active_cam.get_pos()).mag(), reverse=True)
    surface_points.sort(key=lambda x: (-x.get_draw_pos() - active_cam.get_pos()).mag(), reverse=True)

    # now we can draw, but make sure vessels behind the bodies are drawn in front too
    # for convenience
    drawBarycenters(barycenters, active_cam)
    drawBodies(bodies, active_cam, draw_mode)
    drawSurfacePoints(surface_points, active_cam)
    drawVessels(vessels, active_cam, draw_mode)

    if not active_cam.get_lock() and labels_visible:
        glEnable(GL_LINE_SMOOTH)
        drawBarycenterLabels(barycenters, active_cam)
        drawBodyLabels(bodies, active_cam)
        drawSurfacePointLabels(surface_points, active_cam)
        drawVesselLabels(vessels, active_cam)
        glDisable(GL_LINE_SMOOTH)

    # draw trajectory and predictions
    if show_trajectories:
        
        drawProjections(projections)
        glEnable(GL_LINE_SMOOTH)
        if not active_cam.get_lock() and labels_visible:
            drawProjectionLabels(projections, active_cam)
            
        drawTrajectories(vessels, scene_lock)
        drawManeuvers(maneuvers, point_size, active_cam)
        glDisable(GL_LINE_SMOOTH)
        
