from matrix import *
from graphics import *
from vectors import *
from math import *
from random import *

def scanlineConvert(top, mid, bot, zbuffer, color):
    xt = top[0]
    yt = top[1]
    zt = top[2]
    xm = mid[0]
    ym = mid[1]
    zm = mid[2]
    xb = bot[0]
    yb = bot[1]
    zb = bot[2]

    dx0 = (xt - xb) / (yt - yb + 1)
    dz0 = (zt - zb) / (yt - yb + 1)
    if (ym - yb) > 0:
        dx1 = (xm - xb) / (ym - yb + 1)
        dz1 = (zm - zb) / (ym - yb + 1)
    else:
        dx1 = 0
        dz1 = 0
    if (yt - ym) > 0:
        dx1_1 = (xt - xm) / (yt - ym + 1)
        dz1_1 = (zt - zm) / (yt - ym + 1)
    else:
        dx1_1 = 0
        dz1_1 = 0

    x0 = xb
    x1 = xb
    x2 = xb
    z0 = zb
    z1 = zb

    y = floor(yb)

    while (y <= ym):
        drawLine(floor(x0), y, z0, floor(x1), y, z1, zbuffer, color)
        x0 += dx0
        x1 += dx1
        y += 1
        z0 += dz0
        z1 += dz1
    y = floor(ym)
    x1 = xm
    z1 = zm
    while (y <= yt):
        drawLine(floor(x0), y, z0, floor(x1), y, z1, zbuffer, color)
        x0 += dx0
        x1 += dx1_1
        y += 1
        z0 += dz0
        z1 += dz1

def scanlineOrder(p0, p1, p2):
    if (p1[1] < p0[1]):
        p0, p1 = p1, p0
    if (p2[1] < p1[1]):
        p1, p2 = p2, p1
        if (p1[1] < p0[1]):
            p1, p0 = p0, p1
    return [p0, p1, p2]

def addPolygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    addPoint(polygons, x0, y0, z0)
    addPoint(polygons, x1, y1, z1)
    addPoint(polygons, x2, y2, z2)

def drawPolygons( polygons, zbuffer, color ):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return

    point = 0
    while point < len(polygons) - 2:

        normal = dotProduct(crossProduct(surfaceVector(polygons[point], polygons[point + 1]),
                            surfaceVector(polygons[point], polygons[point + 2])),
                            viewVector())
        color = [int(random() * 255), int(random() * 255), int(random() * 255)]
        if normal > 0:
            drawLine( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       zbuffer, color)
            drawLine( int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       zbuffer, color)
            drawLine( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       zbuffer, color)
            points = scanlineOrder(polygons[point], polygons[point+1], polygons[point+2])
            print(points[2][1], points[1][1], points[0][1])
            scanlineConvert(points[2], points[1], points[0], zbuffer, color)
        point+= 3



def addBox( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #top
    addPolygon(polygons, x, y, z, x1, y, z, x, y, z1)
    addPolygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    #front
    addPolygon(polygons, x, y, z, x, y1, z, x1, y1, z)
    addPolygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    #right
    addPolygon(polygons, x1, y1, z1, x1, y, z1, x1, y, z)
    addPolygon(polygons, x1, y1, z1, x1, y, z, x1, y1, z)
    #back
    addPolygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    addPolygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)
    #left
    addPolygon(polygons, x, y, z1, x, y1, z, x, y, z)
    addPolygon(polygons, x, y, z1, x, y1, z1, x, y1, z)
    #bot
    addPolygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    addPolygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def addSphere(polygons, cx, cy, cz, r, steps ):
    points = generateSphere(cx, cy, cz, r, steps)
    latStart = 0
    latStop = steps
    longtStart = 1
    longtStop = steps
    steps += 1
    size = len(points)
    for lat in range(latStart, latStop):
        index = lat * steps
        addPolygon(polygons,
                   points[index % size][0], points[index % size][1], points[index % size][2],
                   points[(index + 1) % size][0], points[(index + 1) % size][1], points[(index + 1) % size][2],
                   points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index + steps + 1) % size][2])
        for longt in range(longtStart, longtStop):
            index = lat * steps + longt
            addPolygon(polygons,
                       points[index % size][0], points[index % size][1], points[index % size][2],
                       points[(index + 1) % size][0], points[(index + 1) % size][1], points[(index + 1) % size][2],
                       points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index + steps + 1) % size][2])
            addPolygon(polygons,
                       points[index % size][0], points[index % size][1], points[index % size][2],
                       points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index + steps + 1) % size][2],
                       points[(index + steps) % size][0], points[(index + steps) % size][1], points[(index + steps) % size][2])
        index = lat * steps + steps - 2
        addPolygon(polygons,
                   points[index % size][0], points[index % size][1], points[index % size][2],
                   points[(index + 1) % size][0], points[(index + 1) % size][1], points[(index + 1) % size][2],
                   points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index+steps + 1) % size][2])


def generateSphere( cx, cy, cz, r, steps ):
    points = []

    rotStart = 0
    rotStop = steps
    circStart = 0
    circStop = steps + 1

    for rotation in range(rotStart, rotStop):
        rot = rotation/float(steps)
        for circle in range(circStart, circStop):
            circ = circle/float(steps)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def addTorus(polygons, cx, cy, cz, r0, r1, steps ):
    points = generateTorus(cx, cy, cz, r0, r1, steps)
    latStart = 0
    latStop = steps
    longtStart = 0
    longtStop = steps
    size = len(points)
    for lat in range(latStart, latStop):
        for longt in range(longtStart, longtStop):
            index = lat * steps + longt
            if longt == longtStop - 1:
                addPolygon(polygons,
                           points[index % size][0], points[index % size][1], points[index % size][2],
                           points[((lat + 1) * steps) % size][0], points[((lat + 1) * steps) % size][1], points[((lat + 1) * steps) % size][2],
                           points[(lat * steps) % size][0], points[(lat * steps) % size][1], points[(lat * steps) % size][2])
                addPolygon(polygons,
                           points[index % size][0], points[index % size][1], points[index % size][2],
                           points[(index + steps) % size][0], points[(index + steps) % size][1], points[(index + steps) % size][2],
                           points[((lat + 1) * steps) % size][0], points[((lat + 1) * steps) % size][1], points[((lat + 1) * steps) % size][2])
            else:
                addPolygon(polygons,
                           points[index % size][0], points[index % size][1], points[index % size][2],
                           points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index + steps + 1) % size][2],
                           points[(index + 1) % size][0], points[(index + 1) % size][1], points[(index + 1) % size][2])
                addPolygon(polygons,
                           points[index % size][0], points[index % size][1], points[index % size][2],
                           points[(index + steps) % size][0], points[(index + steps) % size][1], points[(index + steps) % size][2],
                           points[(index + steps + 1) % size][0], points[(index + steps + 1) % size][1], points[(index + steps + 1) % size][2])

def generateTorus( cx, cy, cz, r0, r1, steps ):
    points = []
    rotStart = 0
    rotStop = steps
    circStart = 0
    circStop = steps

    for rotation in range(rotStart, rotStop):
        rot = rotation/float(steps)
        for circle in range(circStart, circStop):
            circ = circle/float(steps)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points
