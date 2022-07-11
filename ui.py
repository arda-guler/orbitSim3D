import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

def drawPoint2D(x, y, color, camera):
    glPushMatrix()

    glTranslate(-camera.get_pos()[0],
                -camera.get_pos()[1],
                -camera.get_pos()[2])
    
    glColor(color[0], color[1], color[2])

    glBegin(GL_POINTS)

    x1 = x * 100
    y1 = y * 100

    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.get_pos()[0],
                -camera.get_pos()[1],
                -camera.get_pos()[2])
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)

    x1 = x1 * 100
    y1 = y1 * 100
    x2 = x2 * 100
    y2 = y2 * 100
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

# 7-segment display line defs
#
#    _3_
# 1 |   | 6
#   |_4_|
# 2 |   | 7
#   |_5_| . (dot)
#

def l1():
    p1 = (0, 2)
    p2 = (0, 1)
    return [p1, p2]

def l2():
    p1 = (0, 1)
    p2 = (0, 0)
    return [p1, p2]

def l3():
    p1 = (0, 2)
    p2 = (1, 2)
    return [p1, p2]

def l4():
    p1 = (0, 1)
    p2 = (1, 1)
    return [p1, p2]

def l5():
    p1 = (0, 0)
    p2 = (1, 0)
    return [p1, p2]

def l6():
    p1 = (1, 2)
    p2 = (1, 1)
    return [p1, p2]

def l7():
    p1 = (1, 1)
    p2 = (1, 0)
    return [p1, p2]

# 16 - segment display linedefs
# https://en.wikipedia.org/wiki/Sixteen-segment_display#/media/File:16-segmente.png
def l16s_a1():
    p1 = (0, 0)
    p2 = (1, 0)
    return [p1, p2]

def l16s_a2():
    p1 = (1, 0)
    p2 = (2, 0)
    return [p1, p2]

def l16s_b():
    p1 = (2, 0)
    p2 = (2, 2)
    return [p1, p2]

def l16s_c():
    p1 = (2, 2)
    p2 = (2, 4)
    return [p1, p2]

def l16s_d1():
    p1 = (0, 4)
    p2 = (1, 4)
    return [p1, p2]

def l16s_d2():
    p1 = (1, 4)
    p2 = (2, 4)
    return [p1, p2]

def l16s_e():
    p1 = (0, 2)
    p2 = (0, 4)
    return [p1, p2]

def l16s_f():
    p1 = (0, 0)
    p2 = (0, 2)
    return [p1, p2]

def l16s_h():
    p1 = (0, 0)
    p2 = (1, 2)
    return [p1, p2]

def l16s_i():
    p1 = (1, 0)
    p2 = (1, 2)
    return [p1, p2]

def l16s_j():
    p1 = (2, 0)
    p2 = (1, 2)
    return [p1, p2]

def l16s_g1():
    p1 = (0, 2)
    p2 = (1, 2)
    return [p1, p2]

def l16s_g2():
    p1 = (1, 2)
    p2 = (2, 2)
    return [p1, p2]

def l16s_k():
    p1 = (0, 4)
    p2 = (1, 2)
    return [p1, p2]

def l16s_l():
    p1 = (1, 2)
    p2 = (1, 4)
    return [p1, p2]

def l16s_m():
    p1 = (1, 2)
    p2 = (2, 4)
    return [p1, p2]

# Seven segment number defs
def zero():
    return [l1, l2, l3, l5, l6, l7]

def one():
    return [l6, l7]

def two():
    return [l3, l6, l4, l2, l5]

def three():
    return [l3, l6, l4, l7, l5]

def four():
    return [l1, l4, l6, l7]

def five():
    return [l3, l1, l4, l7, l5]

def six():
    return [l3, l1, l4, l2, l7, l5]

def seven():
    return [l3, l6, l7]

def eight():
    return [l1, l2, l3, l4, l5, l6, l7]

def nine():
    return [l4, l1, l3, l6, l7, l5]

def minus():
    return [l4]

def dot():
    return (0, 0)

numbers = {"0": zero(),
           "1": one(),
           "2": two(),
           "3": three(),
           "4": four(),
           "5": five(),
           "6": six(),
           "7": seven(),
           "8": eight(),
           "9": nine(),
           "-": minus()}

# 16 segment alphanumeric chardefs
def AN_A():
    return [l16s_e, l16s_f, l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_g1, l16s_g2]

def AN_B():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_i, l16s_l, l16s_g2]

def AN_C():
    return [l16s_a2, l16s_a1, l16s_f, l16s_e, l16s_d1, l16s_d2]

def AN_D():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_i, l16s_l]

def AN_E():
    return [l16s_a2, l16s_a1, l16s_f, l16s_e, l16s_d1, l16s_d2, l16s_g1, l16s_g2]

def AN_F():
    return [l16s_a2, l16s_a1, l16s_f, l16s_e, l16s_g1, l16s_g2]

def AN_G():
    return [l16s_a2, l16s_a1, l16s_f, l16s_e, l16s_d1, l16s_d2, l16s_g2, l16s_c]

def AN_H():
    return [l16s_e, l16s_f, l16s_g1, l16s_g2, l16s_b, l16s_c, l16s_g1, l16s_g2]

def AN_I():
    return [l16s_a1, l16s_a2, l16s_i, l16s_l, l16s_d1, l16s_d2]

def AN_J():
    return [l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_e]

def AN_K():
    return [l16s_f, l16s_e, l16s_g1, l16s_j, l16s_m]

def AN_L():
    return [l16s_f, l16s_e, l16s_d1, l16s_d2]

def AN_M():
    return [l16s_e, l16s_f, l16s_h, l16s_j, l16s_b, l16s_c]

def AN_N():
    return [l16s_e, l16s_f, l16s_h, l16s_m, l16s_c, l16s_b]

def AN_O():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_e, l16s_f]

def AN_P():
    return [l16s_a1, l16s_a2, l16s_b, l16s_g2, l16s_g1, l16s_e, l16s_f]

def AN_Q():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_e, l16s_f, l16s_m]

def AN_R():
    return [l16s_a1, l16s_a2, l16s_b, l16s_g2, l16s_g1, l16s_e, l16s_f, l16s_m]

def AN_S():
    return [l16s_a1, l16s_a2, l16s_f, l16s_g1, l16s_g2, l16s_c, l16s_d2, l16s_d1]

def AN_T():
    return [l16s_a1, l16s_a2, l16s_i, l16s_l]

def AN_U():
    return [l16s_f, l16s_e, l16s_d1, l16s_d2, l16s_c, l16s_b]

def AN_V():
    return [l16s_f, l16s_e, l16s_k, l16s_j]

def AN_W():
    return [l16s_f, l16s_e, l16s_k, l16s_m, l16s_c, l16s_b]

def AN_X():
    return [l16s_h, l16s_j, l16s_k, l16s_m]

def AN_Y():
    return [l16s_f, l16s_g1, l16s_g2, l16s_b, l16s_c, l16s_d2, l16s_d1]

def AN_Z():
    return [l16s_a1, l16s_a2, l16s_j, l16s_k, l16s_d1, l16s_d2]

def AN_0():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_e, l16s_f, l16s_j, l16s_k]

def AN_1():
    return [l16s_j, l16s_b, l16s_c]

def AN_2():
    return [l16s_a1, l16s_a2, l16s_b, l16s_g2, l16s_g1, l16s_e, l16s_d1, l16s_d2]

def AN_3():
    return [l16s_a1, l16s_a2, l16s_b, l16s_g2, l16s_c, l16s_d2, l16s_d1]

def AN_4():
    return [l16s_f, l16s_g1, l16s_g2, l16s_b, l16s_c]

def AN_5():
    return [l16s_a2, l16s_a1, l16s_f, l16s_g1, l16s_m, l16s_d2, l16s_d1]

def AN_6():
    return [l16s_a2, l16s_a1, l16s_f, l16s_e, l16s_d1, l16s_d2, l16s_c, l16s_g2, l16s_g1]

def AN_7():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c]

def AN_8():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_e, l16s_f, l16s_g1, l16s_g2]

def AN_9():
    return [l16s_a1, l16s_a2, l16s_b, l16s_c, l16s_d2, l16s_d1, l16s_f, l16s_g1, l16s_g2]

def AN_MINUS():
    return [l16s_g1, l16s_g2]

def AN_SPACE():
    return None

alphanumerics = {"0": AN_0(),
                 "1": AN_1(),
                 "2": AN_2(),
                 "3": AN_3(),
                 "4": AN_4(),
                 "5": AN_5(),
                 "6": AN_6(),
                 "7": AN_7(),
                 "8": AN_8(),
                 "9": AN_9(),
                 "-": AN_MINUS(),
                 "A": AN_A(),
                 "B": AN_B(),
                 "C": AN_C(),
                 "D": AN_D(),
                 "E": AN_E(),
                 "F": AN_F(),
                 "G": AN_G(),
                 "H": AN_H(),
                 "I": AN_I(),
                 "J": AN_J(),
                 "K": AN_K(),
                 "L": AN_L(),
                 "M": AN_M(),
                 "N": AN_N(),
                 "O": AN_O(),
                 "P": AN_P(),
                 "Q": AN_Q(),
                 "R": AN_R(),
                 "S": AN_S(),
                 "T": AN_T(),
                 "U": AN_U(),
                 "V": AN_V(),
                 "W": AN_W(),
                 "X": AN_X(),
                 "Y": AN_Y(),
                 "Z": AN_Z(),
                 " ": AN_SPACE()}

def render_numbers(numstring, color, start_pt, cam, font_size=0.5):
    global numbers
    
    draw_start_x = start_pt[0]
    spacing = font_size * 0.5
    
    for char in numstring:
        if not char == ".":
            lines = numbers[char]
            for line in lines:
                x1 = draw_start_x + font_size * line()[0][0]
                y1 = start_pt[1] + font_size * line()[0][1]
                x2 = draw_start_x + font_size * line()[1][0]
                y2 = start_pt[1] + font_size * line()[1][1]
                drawLine2D(x1, y1, x2, y2, color, cam)

        else:
            x = draw_start_x
            y = start_pt[1]
            drawPoint2D(x, y, color, cam)

        draw_start_x += font_size + spacing

def render_AN(render_string, color, start_pt, cam, font_size=0.1):
    global alphanumerics

    render_string = render_string.upper()

    draw_start_x = start_pt[0]
    spacing = font_size * 1.75

    for char in render_string:
        if not char == "." and not char == " ":
            try:
                lines = alphanumerics[char]
                for line in lines:
                    x1 = draw_start_x + font_size * line()[0][0]
                    y1 = start_pt[1] + font_size * -line()[0][1]
                    x2 = draw_start_x + font_size * line()[1][0]
                    y2 = start_pt[1] + font_size * -line()[1][1]
                    drawLine2D(x1, y1, x2, y2, color, cam)
            except:
                pass

        elif char == ".":
            x = draw_start_x
            y = start_pt[1] - font_size * 4
            drawPoint2D(x, y, color, cam)

        else:
            # it is a space or unknown char
            pass

        draw_start_x += font_size + spacing

