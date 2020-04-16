import math

def normalize(vector):
    magnitude = sum(vector)
    magnitude = Math.sqrt(magnitude)
    if magnitude != 0:
        for i in range(len(vector)):
            vector[i] = vector[i] / float(magnitude)
    return vector

def dotProduct(v1, v2):
    sum = 0;
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum

def crossProduct(v1, v2):
    x = v1[1] * v2[2] - v1[2] * v2[1]
    y = v1[2] * v2[0] - v1[0] * v2[2]
    z = v1[0] * v2[1] - v1[1] * v2[0]
    return [x, y, z]

def viewVector():
    return [0, 0, 1]

def surfaceVector(v1, v2):
    x = v2[0] - v1[0]
    y = v2[1] - v1[1]
    z = v2[2] - v1[2]
    return[x,y,z]
