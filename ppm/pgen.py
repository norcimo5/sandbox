#!/usr/bin/python
#####################################################
# IMPORTS
#####################################################
import random


#####################################################
# GLOBALS
#####################################################
grid = [ 0 for i in range(0, 256*256*3) ]
red, green, blue = (255, 255, 255)
intToBool = lambda i : [False, True][i]

#####################################################
# FUNCTIONS (SWITCH TO CLASSES and/or FUNCTIONAL)
#####################################################
def getColor():
    global red
    global green
    global blue
    return (red, green, blue) 

def randColor():
    global red
    global green
    global blue
    red   = random.randrange(0,256)
    green = random.randrange(0,256)
    blue  = random.randrange(0,256)

def point(x, y):
    global grid
    red, green, blue = getColor()
    if x > 0 and x < 256 and y > 0 and y < 256:
        loc = 3 * ((y << 8 ) + x)
        
        grid[loc  ] = red
        grid[loc+1] = green
        grid[loc+2] = blue
     
def getpoint(x, y):
    global grid
    loc = 3 * ((y << 8 ) + x )
    return grid[loc:loc+3]

def box(x, y, w, h):
    for dx in range(x, x+w):
        point(dx, y)
        point(dx, y+h-1)

    for dy in range(y+1, y+h-1):
        point(x, dy)
        point(x+w-1, dy)

def solid_box(x, y, w, h):
    for dx in range(x, x+w):
        for dy in range(y, y+h):
            point(dx, dy)

def swap(a,b):
    if a > b:
        return (b, a)
    else:
        return (a, b)

def line(x1, y1, x2, y2):
    (x1, x2) = swap(x1, x2)
    (y1, y2) = swap(y1, y2)
    w = x2-x1
    h = y2-y1

    if w == 0 and w == h: return;

    if w < h:
        m = float(w) / float(h)
        for dy in range(0, h):
            dx = int(float(dy) * m)
            point(x1+dx, y1+dy)
    else:
        m = float(h) / float(w)
        for dx in range(0, w):
            dy = int(float(dx) * m)
            point(x1+dx, y1+dy)

def circle(x0, y0, radius, solid = False):
    x = radius
    y = 0
    radiusError = 1 - x
    
    while x >= y:
        if solid == False:
            point( x+x0,  y+y0)
            point( y+x0,  x+y0)
            point(-x+x0,  y+y0)
            point(-y+x0,  x+y0)
            point(-x+x0, -y+y0)
            point(-y+x0, -x+y0)
            point( x+x0, -y+y0)
            point( y+x0, -x+y0)
        else:
            line(-y+x0, -x+y0, y+x0, -x+y0)
            line(-x+x0, -y+y0, x+x0, -y+y0)
            line(-x+x0,  y+y0, x+x0,  y+y0)
            line(-y+x0,  x+y0, y+x0,  x+y0)

        y = y + 1
        if radiusError < 0:
            radiusError = radiusError + ( 2 * y + 1 )
        else:
            x = x - 1
            radiusError = radiusError + (2 * (y - x + 1))

def build_grid(x, y):
    global grid
    header = "P3\n%d %d\n255\n" % (x, y)
    for i in range(0, 5):
        randColor()
        line(random.randrange(0,256), random.randrange(0,256), \
             random.randrange(0,256), random.randrange(0,256))
        rx = random.randrange(0,255)
        ry = random.randrange(0,255)
        box(rx,ry,random.randrange(1,256 - rx), \
                  random.randrange(1,256 - ry))
        rx = random.randrange(0,255)
        ry = random.randrange(0,255)
        solid_box(rx,ry,random.randrange(1,256 - rx), \
                        random.randrange(1,256 - ry))
        rx = random.randrange(55,255)
        ry = random.randrange(55,255)
        radius = random.randrange(3,255)
        circle(rx,ry,radius, intToBool(random.randint(0,1)))

    #convert list into textfile
    newgrid = ""
    for dy in range (0, y):
        for dx in range (0, x):
            (a, b, c) = getpoint(dx, dy)
            newgrid = "%s %d %d %d" % (newgrid, a, b, c)
        newgrid = newgrid + "\n"

    return header + newgrid

######################################################
# MAIN
######################################################
with open("./image.ppm", 'w+') as f:
    f.write(build_grid(256,256))
