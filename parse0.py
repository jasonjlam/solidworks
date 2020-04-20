from graphics import *
from matrix import *
from polygons import *
import math

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         push: push a copy of the current top of the coordinate system stack to the stack
         pop: pop off the current top of the coordinate system stack
         All the shape commands work as follows:
             1) Add the shape to a temporary matrix
             2) Multiply that matrix by the current top of the coordinate system stack
             3) Draw the shape to the screen
             4) Clear the temporary matrix
         sphere: add a sphere to the POLYGON matrix -
                 takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the POLYGON matrix -
                takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the POLYGON matrix -
              takes 6 arguemnts (x, y, z, width, height, depth)
         clear: clears the edge and POLYGON matrices
    	 circle: add a circle to the edge matrix -
    	         takes 4 arguments (cx, cy, cz, r)
    	 hermite: add a hermite curve to the edge matrix -
    	          takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
    	 bezier: add a bezier curve to the edge matrix -
    	         takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)`
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
               then multiply the transform matrix by the translation matrix -
               takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge and POLYGON matrices
         display: clear the screen, then
                  draw the lines of the edge and POLYGON matrices to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge and POLYGON matrices to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""
def parseFile( fname, edges, polygons, cstack, screen, zbuffer, color ):
    fd = open(fname, "r")
    lines = fd.readlines()
    lines = list(map(str.rstrip,lines))
    print(lines)
    for line in range(0, len(lines)):
        print (line)
        printMatrix(cstack[-1])
        if lines[line] == "line":
            args = lines[line+1].split(" ")
            addEdge(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
            matrixMulti(cstack[-1], edges)
            drawLines(edges, zbuffer, color)
            edges = newMatrix(4,0)

        elif lines[line] == "scale":
            args = lines[line+1].split(" ")
            temp = scaleMatrix(float(args[0]), float(args[1]), float(args[2]))
            matrixMulti(cstack[-1], temp)
            cstack[-1] = temp

        elif lines[line] == "move":
            args = lines[line+1].split(" ")
            temp = translateMatrix(float(args[0]), float(args[1]), float(args[2]))
            matrixMulti(cstack[-1], temp)
            cstack[-1] = temp

        elif lines[line] == "rotate":
            args = lines[line+1].split(" ")
            temp = rotateMatrix(args[0], float(args[1]))
            matrixMulti(cstack[-1], temp)
            cstack[-1] = temp

        elif lines[line] == "circle":
            args = lines[line+1].split(" ")
            addCircle(edges, int(args[0]), int(args[1]), int(args[2]), int(args[3]), 0.02)
            matrixMulti(cstack[-1], edges)
            drawLines(edges, zbuffer, color)
            edges = []

        elif lines[line] == "bezier":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addCurve(edges, int(args[0]), args[1], args[2], args[3], args[4], args[5], args[6], args[7], 0.02, "bezier")
            matrixMulti(cstack[-1], edges)
            drawLines(edges, zbuffer, color)
            edges = []

        elif lines[line] == "hermite":
            args = lines[line+1].split(" ")
            args = [float(i) for i in args]
            args = [int(i) for i in args]
            addCurve(edges, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 0.05, "hermite")
            matrixMulti(cstack[-1], edges)
            drawLines(edges, zbuffer, color)
            edges = []

        elif lines[line] == "box":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addBox(polygons, args[0], args[1], args[2], args[3], args[4], args[5])
            matrixMulti(cstack[-1], polygons)
            drawPolygons(polygons, zbuffer, color)
            polygons = []

        elif lines[line] == "sphere":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addSphere(polygons, args[0], args[1], args[2], args[3], 10)
            matrixMulti(cstack[-1], polygons)
            drawPolygons(polygons, zbuffer, color)
            polygons = []

        elif lines[line] == "torus":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addTorus(polygons, args[0], args[1], args[2], args[3], args[4], 10)
            matrixMulti(cstack[-1], polygons)
            drawPolygons(polygons, zbuffer, color)
            polygons = []

        elif lines[line] == "color":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            color = [args[0], args[1], args[2]]

        elif lines[line] == "push":
            copy = newMatrix(0,0)
            for x in cstack[-1]:
                copy.append(x)
            cstack.append(copy)

        elif lines[line] == "pop":
            cstack.pop()

        elif lines[line] == "clear":
            clearzbuffer(zbuffer)
            clearpixels()
        elif lines[line] == "display":
            display()

        elif lines[line] == "save":
            args = lines[line+1].split(" ")
            saveExtension(args[0])
        elif lines[line] == "quit":
            return
