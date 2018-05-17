

import numpy
from stl import mesh
import numpy as np
from vpython import*
import random
import math
import socket
from copy import deepcopy
from win32api import GetSystemMetrics



# Using an existing stl file:

scene1 = canvas(width=GetSystemMetrics(0)-100, height=GetSystemMetrics(1)-100, title='Main scene')
scene1.background = color.white
# sphere1= sphere(radius = 0.1, pos=vec(4,0,50),color=color.red)
# sphere2= sphere(radius = 0.1, pos=vec(-4,0,50),color=color.red)
shelf = mesh.Mesh.from_file('a380_reduced.stl')
shelf_normals = shelf.normals
shelf_positions = shelf.vectors
xFactor=0.0001
yFactor= 0.0001
zFactor=0.0001
x=[]
y=[]
z=[]
for i in range(len(shelf_positions)):
    for ii in range(len(shelf_positions[i])):
        x.append(shelf_positions[i][ii][0])
        y.append(shelf_positions[i][ii][1])
        z.append(shelf_positions[i][ii][2])
        shelf_positions[i][ii][0] = shelf_positions[i][ii][0] * xFactor
        shelf_positions[i][ii][2] = shelf_positions[i][ii][2] * yFactor
        shelf_positions[i][ii][1] = shelf_positions[i][ii][1] * zFactor

print(len(shelf_normals))

triangles = []
for i in range(len(shelf_normals)):

    if i < 6000:
        color_select= color.red
    elif i < 10000:
        color_select = color.blue
    elif i < 16000:
        color_select = color.green
    a = vertex( pos=vec(shelf_positions[i][0][0], shelf_positions[i][0][2], shelf_positions[i][0][1]), color=color_select,normal=vec(shelf_normals[i][0], shelf_normals[i][1], shelf_normals[i][2]))
    b = vertex( pos=vec(shelf_positions[i][1][0], shelf_positions[i][1][2], shelf_positions[i][1][1]), color=color_select,normal=vec(shelf_normals[i][0], shelf_normals[i][1], shelf_normals[i][2]))
    c = vertex( pos=vec(shelf_positions[i][2][0], shelf_positions[i][2][2], shelf_positions[i][2][1]), color=color_select,normal=vec(shelf_normals[i][0], shelf_normals[i][1], shelf_normals[i][2]))

    triangles.append(triangle(canvas=scene1,vs=[a, b, c],color=color_select))

shelf_compund = compound(triangles, canvas=scene1, opacity=1, pos=vec(0,0,-10))


shelf_compund.rotate(angle=math.radians(180), axis=vec(0,1,0))

plane1 = shelf_compund.clone(pos=vec(0,0,20))
plane1.color = color.blue

plane1.rotate(angle=math.radians(180), axis=vec(0,1,0))
print(shelf_compund.size)

#scene1.camera.follow(shelf_compund)

#print(shelf_compund.pos.x/2,shelf_compund.pos.y/2,1)
scene.camera.pos = vec(shelf_compund.pos.x/2,shelf_compund.pos.y/2,0.1)
time.sleep(3)
ycounter = 0
for i in range(1000):
    rate(50)

    if i > 80 and i < 100:
        shelf_compund.rotate(angle=math.radians(1),axis=vec(1,0,0))
        plane1.rotate(angle=math.radians(1), axis=vec(1, 0, 0))
        shelf_compund.pos.y = ycounter
        plane1.pos.y = -ycounter
        ycounter +=0.1
    elif i > 120 and i < 140:
        shelf_compund.rotate(angle=math.radians(-1), axis=vec(1, 0, 0))
        plane1.rotate(angle=math.radians(-1), axis=vec(1, 0, 0))
    shelf_compund.pos.z=i*0.1
    plane1.pos.z = 30-(0.1*i)







