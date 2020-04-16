from parse import *
from matrix import *
from graphics import *
import random

edges = newMatrix(4,0)
polygons = newMatrix(4,0)

t = identity(newMatrix())
cstack = [t]
zbuffer = newzbuffer()
color = [80, 175, 60]
createPixels(600, 600, 255)
parseFile("script", edges, polygons, cstack, pixels, zbuffer, color)
# Uncomment if you want to make the image
# parseFile("creeper", edges, polygons, cstack, pixels, color)
