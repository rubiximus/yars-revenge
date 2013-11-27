"""
tuple.py

Utilities and constants for 2D vectors represented as (x, y) tuples
"""

from math import sqrt, copysign

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
NORTHEAST = (1, -1)
SOUTHEAST = (1, 1)
NORTHWEST = (-1, -1)
SOUTHWEST = (-1, 1)

tan225 = 0.41421356237309503
tan675 = 2.414213562373095

def round_to_90(vector):
    """Returns the cardinal direction closest to vector, favoring N/S
    
    Note: For simplicity the return value is currently normal"""
    
    if abs(vector[0]) >= abs(vector[1]):
        return (copysign(1, vector[0]), 0)
    else:
        return (0, copysign(1, vector[1]))
    

def round_to_45(vector):
    """Returns the cardinal or intermediate direction closest to vector, favoring cardinal
    
    Note: For simplicity the return value is currently normal"""
    
    if vector[0] == 0:
        return (0, copysign(1, vector[1]))
    
    ratio = abs(vector[1] / vector[0])
    
    #round to horizontal
    if ratio < tan225:
        return (copysign(1, vector[0]), 0)
    
    #round to vertical
    if ratio > tan675:
        return (0, copysign(1, vector[1]))
        
    #round to intermediate
    return (copysign(1, vector[0]), copysign(1, vector[1]))
    
    
def get_direction(start, end):
    """get the vector from start coordinates to end coordinates
    """
    
    x = end[0] - start[0]
    y = end[1] - start[1]
    return (x, y)
    
    
def normalize(vector):
    """Returns the normalized (unit) vector. Zero vector (0, 0) will be unchanged"""
    
    mag = magnitude(vector)
    
    if mag == 0:
        return vector
    else: norm = (vector[0] / mag, vector[1] / mag)
    return norm
    

def magnitude(vector):
    """Returns the magnitude of vector"""
    
    return sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    
    
def add(left, right):
    """Returns the vector sum of left and right"""
    
    return (left[0] + right[0], left[1] + right[1])
    

def dist(left, right):
    """Returns the distance between vectors left and right"""
    
    return sqrt( (left[0] - right[0]) ** 2 + (left[1] - right[1]) ** 2 )

    
def scale(vector, scaler):
    """Returns the vector multiplied by the scaler"""
    
    return (vector[0] * scaler, vector[1] * scaler)
