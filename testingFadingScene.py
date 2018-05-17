import numpy
from stl import mesh
import numpy as np
from vpython import*
import random
import math
import socket
from copy import deepcopy
from win32api import GetSystemMetrics


class plot3D:

    # There is an L by L grid of vertex objects, numbered 0 through L-1 by 0 through L-1.
    # Only the vertex operators numbered L-2 by L-2 are used to create quads.
    # The extra row and extra column of vertex objects simplifies edge calculations.
    # The stride length from y = 0 to y = 1 is L.
    L = 50
    scene.center = vec(0.05 * L, 0.2 * L, 0)
    scene.range = 1.3 * L
    def __init__(self, scene1, f, xmin, xmax, ymin, ymax, zmin, zmax):
        # The x axis is labeled y, the z axis is labeled x, and the y axis is labeled z.
        # This is done to mimic fairly standard practive for plotting
        #     the z value of a function of x and y.
        self.scene1=scene1
        self.f = f
        if not xmin:
            self.xmin = 0
        else:
            self.xmin = xmin
        if not xmax:
            self.xmax = 1
        else:
            self.xmax = xmax
        if not ymin:
            self.ymin = 0
        else:
            self.ymin = ymin
        if not ymax:
            self.ymax = 1
        else:
            self.ymax = ymax
        if not zmin:
            self.zmin = 0
        else:
            self.zmin = zmin
        if not zmax:
            self.zmax = 1
        else:
            self.zmax = zmax

        R = L / 100
        d = L - 2
        xaxis = cylinder(pos=vec(0, 0, 0), axis=vec(0, 0, d), radius=R, color=color.yellow)
        yaxis = cylinder(pos=vec(0, 0, 0), axis=vec(d, 0, 0), radius=R, color=color.yellow)
        zaxis = cylinder(pos=vec(0, 0, 0), axis=vec(0, d, 0), radius=R, color=color.yellow)
        k = 1.02
        h = 0.05 * L
        text(pos=xaxis.pos + k * xaxis.axis, text='x', height=h, align='center', billboard=True, emissive=True)
        text(pos=yaxis.pos + k * yaxis.axis, text='y', height=h, align='center', billboard=True, emissive=True)
        text(pos=zaxis.pos + k * zaxis.axis, text='z', height=h, align='center', billboard=True, emissive=True)

        self.vertices = []
        for x in range(L):
            for y in range(L):
                val = self.evaluate(x, y)
                self.vertices.append(self.make_vertex(x, y, val))

        self.make_quads()
        self.make_normals()

    def evaluate(self, x, y):
        d = L - 2
        return (d / (self.zmax - self.zmin)) * (self.f(self.xmin + x * (self.xmax - self.xmin) / d,
                                                       self.ymin + y * (self.ymax - self.ymin) / d) - self.zmin)

    def make_quads(self):
        # Create the quad objects, based on the vertex objects already created.
        for x in range(L - 2):
            for y in range(L - 2):
                v0 = self.get_vertex(x, y)
                v1 = self.get_vertex(x + 1, y)
                v2 = self.get_vertex(x + 1, y + 1)
                v3 = self.get_vertex(x, y + 1)
                quad(vs=[v0, v1, v2, v3])

    def make_normals(self):
        # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
        # The vectors a and b point to the right and up around a vertex in the xy plance.
        for i in range(L * L):
            x = int(i / L)
            y = i % L
            if x == L - 1 or y == L - 1: continue
            v = self.vertices[i]
            a = self.vertices[i + L].pos - v.pos
            b = self.vertices[i + 1].pos - v.pos
            v.normal = cross(a, b)

    def replot(self):
        for i in range(L * L):
            x = int(i / L)
            y = i % L
            v = self.vertices[i]
            v.pos.y = self.evaluate(x, y)
        self.make_normals()

    def make_vertex(self, x, y, value):
        return vertex(pos=vec(y, value, x), color=color.cyan, normal=vec(0, 1, 0))

    def get_vertex(self, x, y):
        return self.vertices[x * L + y]

    def get_pos(self, x, y):
        return self.get_vertex(x, y).pos

def fadeIn(t, sleepTime):
    time.sleep(sleepTime)
    #t.opacity = 0
    t.visible = True
    r = 1
    g = 1
    b = 1
    for i in range(50):
        rate(50)
        r = r - 0.02
        g = g - 0.02
        b = b - 0.02
        t.color = vec(r, g, b)

def fadeOut(t,sleepTime):
    time.sleep(sleepTime)
    r = 0
    g = 0
    b = 0
    for i in range(50):
        rate(25)
        r = r + 0.02
        g = g + 0.02
        b = b + 0.02
        t.color = vec(r, g, b)
    t.visible = False
    #t.visible = False
    #del t
def show_2D_plot():
    oscillation = graph(align="right",xtitle='time', ytitle='value', fast=True, width=600, markers=False, position=vec(0,0,0))
    funct1 = gcurve(color=color.blue, width=4, markers=True, marker_color=color.orange, label='curve')
    funct2 = gvbars(delta=0.4, color=color.green, label='bars')
    funct3 = gdots(color=color.red, size=6, label='dots')

    for t in range(-200, 0, 1):
        rate(25)
        funct1.plot(t, 5.0 + 5.0 * cos(-0.2 * t) * exp(0.015 * t))
        funct2.plot(t, 2.0 + 5.0 * cos(-0.1 * t) * exp(0.015 * t))
        funct3.plot(t, 5.0 * cos(-0.03 * t) * exp(0.015 * t))
def show_3D_plot():





    t = 0
    dt = 0.02

    def f(x, y):
        # Return the value of the function of x and y:
        return 0.7 + 0.2 * sin(10 * x) * cos(10 * y) * sin(5 * t)

    p = plot3D(f, 0, 1, 0, 1, 0, 1)  # function, xmin, xmax, ymin, ymax (defaults 0, 1, 0, 1, 0, 1)

    run = True

    def running(ev):
        global run
        run = not run

    scene.forward = vec(-0.7, -0.5, -1)

    while True:
        rate(30)
        if run:
            p.replot()
            t += dt


screenWidthThreshold = 1005
screenHeightThreshold = 670

scene_1 = canvas(width=GetSystemMetrics(0)-screenWidthThreshold, height=GetSystemMetrics(1)-screenHeightThreshold, background=color.white)

textList = ['Hello Everyone!','Welcome to \nPython Learning Nürnberg.', 'Together, we \'ll do a lot of cool & amazing stuff with Python.',
            'We \'ll plot 2D & 3D plots', 'We \'ll create Graphical User Interfaces', 'We \'ll build airplanes', 'And make them fly!',
            'We \'ll code with a style.', 'It looks complicated?', 'Don\'t worry, we \'ll get there together.',
            'And always remember, it all started with','Hello World']
textObjectsDict ={}
for i in range(len(textList)):
    textObjectsDict['text' + str(i)] = label(text=textList[i], align='center', color=vec(1, 1, 1), pos=vec(0, 0, 0), box=False, opacity=1,height=30, visible = False)

time.sleep(3)

for i in range(len(textList)):
    #rate(30)
    if i == 3:
        show_2D_plot()
    fadeIn(textObjectsDict['text' +str(i)],0.5)
    fadeOut(textObjectsDict['text' +str(i)],3)

# for i in range(len(text_list)):
#     fadeIn(T, text_list[i])
#     fadeOut(T, text_list[i])
    #T.opacity = T.opacity+0.01
    #scene_1.opacity=scene_1.opacity + 0.01

# a1 = a2 = 0
# l1 = local_light(pos=vec(0,np.sin(math.radians(a1)),np.cos(math.radians(a1))), color=color.red)

#ball = sphere(radius=0.01, pos=vec(0,0,0))
#ball1= sphere(radius=0.01, pos=vec(-1,0,0))
# color_steps = []
# r_component = 0
# g_component = 0
# b_component = 0
# for i in range(3000):
#     rate(200)
#     if i < 1000:
#         r_component += 0.001
#     elif i < 2000:
#         g_component += 0.001
#     elif i < 3000:
#         b_component += 0.001
#     #scene_1.background = vec(r_component,g_component,b_component)
# while True:
#     rate(200)
#     a1+=1
#     l1.pos = 1*vec(0,np.sin(math.radians(a1)),np.cos(math.radians(a1)))



# for i in range(len(color_steps)):
#     rate(30)
#     scene_1.background = color_steps[i]
#     #print('here')