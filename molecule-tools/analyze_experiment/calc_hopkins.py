#!/usr/bin/env python3
# file: calc_hopkins.py
# author: Jon David
# date: Friday, August 19, 2022
# description:
#   Calculates hopkins statistics for a single experimental run.



import sys
import random
import functools

import numpy as np


def gen_set_Y(xlim_min, xlim_max, zlim_min, zlim_max, m):
    """Generates a set of m uniformly random data points within a bounding box."""
    y_vec = []

    x_bounds = xlim_max - xlim_min
    z_bounds = x_bounds
    
    for i in range(0,m):
        x = (x_bounds * random.uniform(0,1)) - (x_bounds / float(2))
        z = (z_bounds * random.uniform(0,1)) - (z_bounds / float(2))    
        y_vec.append( (x,z) )
    return y_vec

def gen_random_sequence( m, mmin, mmax):
    """Generates a random sequence of m integers between mmin and mmax."""
    rrange = mmax-mmin
    if m > rrange:
        raise Exception( "You fool. You nearly caused an inifinte time loop!" )
    seq = []
    while ( m > 0 ):
        r = random.uniform(mmin, mmax)
        if r not in seq:
            seq.append(r)
            m = m - 1
    return seq
    
def gen_set_Xm(X, m):
    """Generates a subset of m elements from X, without repetition."""
    random_sequence = gen_random_sequence( m, 0, len(X) )
    Xm = []
    for i in range(0, len(random_sequence)):
        idx = random_sequence[i]
        Xm.append( X[i] )
    return Xm

def find_nn(p, X, allowSelfMatch=True):
    """Given a point p, finds the nearest vertex v in X."""
    v = (0,0)
    distances_vec = []  ## a list of (x_i, dist(x_i,p)).
    minDist = 99999
    for x in X:
        if (x == p) and not allowSelfMatch:
            continue
        dist = calc_dist(p, x)
        if dist < minDist:
            minDist = dist
            v = x
    return v

def calc_dist(p,q):
    """Calculates the Euclidean distance between two points p and q."""
    a = np.array(p)
    b = np.array(q)
    distance = np.linalg.norm( a - b )
    return distance

def calc_u_vec(Y, X, m):
    u_vec = []
    for y in Y:
        nearestX = find_nn(y,X)
        d = calc_dist(y, nearestX)
        u_vec.append( d )
    return u_vec

def calc_w_vec(Xm, X, m):
    w_vec = []
    for x in Xm:
        nearestX = find_nn(x, X, False)
        d = calc_dist(x, nearestX)
        w_vec.append( d )
    return w_vec
    
def calc_hopkins(u_vec, w_vec, m, d):
    """Calculates Hopkin's statistic from pre-computed u_vec, w_vec, m, and d (dimension of data)"""
    H = 0
    f = lambda a,b: a + b
    g = lambda x: np.power(x,2)
    A = functools.reduce( f, list( map(g, u_vec )))
    B = functools.reduce( f, list( map(g, w_vec )))
    H = float(A) / ( float(A) + float(B) )
    return H
    
def main():
    print( "Hello, I'm calculating Hopkins' statistic!" )

    n = 1234
    m = 0.2 * n
    d = 2  ## dimension of data (i.e. 2D)

    xlim_min = -100
    xlim_max = 100
    zlim_min = -100
    zlim_max = 100
    
    Y = gen_set_Y(xlim_min, xlim_max, zlim_min, zlim_max, m)
    Xm = gen_set_Xm(X, m)

    calc_u_vec(Y, X, m)
    calc_w_vec(Xm, X, m)
    calc_hopkins(u_vec, w_vec, m, d)
    
if __name__ == "__main__":
    main()

    
