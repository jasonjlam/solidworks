import array
import math
from matrix import *
from subprocess import Popen, PIPE
from os import remove

pixels = [0]
w = 0
h = 0
header = ""

def createPixels(width, height, maxval):
    global pixels
    global w
    global h
    global header
    pixels = array.array('B', [255, 255, 255] * width * height)
    w  = width
    h = height
    header = "P3 " + str(w) + " "+ str(h) + " " + str(maxval) + "\n"

def writeImage(path):
    fd = open(path, 'w')
    print ("Writing image...")
    fd.write(header)
    for pixel in pixels:
        fd.write(str(pixel) + " ")
    fd.close()

def clearpixels():
    global pixels
    for x in range(len(pixels)):
        pixels[x] = 255;

def newzbuffer():
    global w
    global h
    zb = []
    for y in range( h ):
        row = [ float('-inf') for x in range(w) ]
        zb.append( row )
    return zb

def plot(zbuffer, color, x, y, z ):
    newy = h - 1 - y
    index = (w * newy + x) * 3
    global pixels
    if ( x >= 0 and x < w and newy >= 0 and newy < h and z > zbuffer[y][x]):
        pixels[index] = color[0]
        pixels[index + 1] = color[1]
        pixels[index + 2] = color[2]
        zbuffer[y][x] = z

def clearzbuffer( zb ):
    for y in range( len(zb) ):
        for x in range( len(zb[y]) ):
            zb[y][x] = float('-inf')

def saveExtension(fname ):
    ppmName = fname[:fname.find('.')] + '.ppm'
    writeImage(ppmName)
    p = Popen( ["convert", ppmName, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppmName)

def display():
    ppmName = 'pic.ppm'
    writeImage(ppmName )
    p = Popen( ['imdisplay', ppmName], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppmName)

def addEdge( matrix, x0, y0, z0, x1, y1, z1 ):
    addPoint(matrix, x0, y0, z0)
    addPoint(matrix, x1, y1, z1)

def drawLines( matrix, zbuffer, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        drawLine( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   zbuffer, color)
        point+= 2

def drawLine( x0, y0, z0, x1, y1, z1, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt
        z0, z1 = z1, z0

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y
    if (loop_end != loop_start):
        dz = (z1-z0) / (loop_end - loop_start + 1)
    else:
        dz = 0

    while ( loop_start < loop_end ):
        plot(zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z += dz
        loop_start+= 1
    plot(zbuffer, color, x, y, z + 1 )


def addCurve (matrix, x0, y0, x1, y1, x2, y2, x3, y3, step, type):
    for i in range(int(1/step)):
        coeffMat = curveCoefficients([x0, y0, 0, 1], [x1, y1, 0, 1], [x2, y2, 0, 1], [x3, y3, 0, 1])
        if (type == "hermite"):
            curveMat = hermite()
        elif (type == "bezier"):
            curveMat = bezier()
        matrixMulti(curveMat, coeffMat)
        points = []
        stepMat = [(i * step) **3, (i *step) **2, (i * step), 1]
        for m in range(4):
            x = 0
            for  n in range(4):
                x += stepMat[n] * coeffMat[m][n]
            points.append(x)
        coeffMat = curveCoefficients([x0, y0, 0, 1], [x1, y1, 0, 1], [x2, y2, 0, 1], [x3, y3, 0, 1])
        matrixMulti(curveMat, coeffMat)
        stepMat = [((i+1) * step) **3, ((i+1) *step) **2, ((i+1) * step), 1]
        for m in range(4):
            x = 0
            for n in range(4):
                x += stepMat[n] * coeffMat[m][n]
            points.append(x)
        addEdge(matrix, points[0], points[1], 0, points[4], points[5], 0)
