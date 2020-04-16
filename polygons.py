from matrix import *
from graphics import *
from vectors import *

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
        print ("Checking normal")
        print (normal)
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
