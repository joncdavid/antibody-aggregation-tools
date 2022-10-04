#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 15:14:14 2021

@author: jdavid

Given two points, transform those points such that they are co-planar
to the XZ-axis, where y=0. It gives you the transformed points, and also
the angles used to transform them.
"""


import numpy as np
import sys

from ast import literal_eval as make_tuple


USAGE = """
---- USAGE -----------------------------------

planarize_2points <p1> <p2>

Where,
  <p1> :: string of the form "(p1,x1,x2,x3)" 
  <p2> :: point 2 of the same format as <p1>
  
Output:
  Given <p1>, <p2>
  new-p1 is <new-p1>
  new-p2 is <new-p2>
  theta_y is <Real>
  theta_z is <Real>
  theta_x is <Real>
----------------------------------------------
"""

DEBUG_ON = True


class MyPoint(object):
    def __init__(self, name):
        self.name_ = name

    def initializeFromString(self, s):
        """ Expected input s is format: '(x,y,z)'... """
        t = make_tuple(s)
        self.x_ = float( t[0])
        self.y_ = float( t[1] )
        self.z_ = float( t[2] )
    
    def to_numpy(self):
        return np.array( [self.x_, self.y_, self.z_] )
    
    def __str__(self):
        s = "({},{},{},{})"
        return s.format(self.name_, self.x_, self.y_, self.z_)
## End of class Point


def helper_findAngleBetweenTwoVecs(v1,v2):
    ## note arccos returns angle in radians [0,pi]
    scalar_product = np.dot(v1,v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    
    ## Cauchy-Schwarz, if true then v1 and v2 are linearly dependent
    theta = 0
    if scalar_product == magnitude_v1 * magnitude_v2:
        theta = 0
    else:
        theta = np.arccos( scalar_product / (magnitude_v1 * magnitude_v2) )
    return theta


def helper_rotateVecAboutZAxis(v, theta):
    ## note: np.cos(x), np.sin(x) expects x to be in radians... 
    R_z = np.array( [ [np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta), np.cos(theta), 0],
                      [0,0,1]], dtype=np.single )
    v_rotated = np.dot(R_z,v.T)
    return v_rotated

def helper_rotateVecAboutYAxis(v, theta):
    ## note: np.cos(x), np.sin(x) expects x to be in radians... 
    R_y = np.array( [ [np.cos(theta), 0.0, np.sin(theta)],
                      [0.0, 1.0, 0.0],
                      [-np.sin(theta), 0, np.cos(theta)] ], dtype=np.single )
    v_rotated = np.dot(R_y,v.T)
    return v_rotated

def helper_rotateVecAboutXAxis(v, theta):
    ## note: np.cos(x), np.sin(x) expects x to be in radians...
    R_x = np.array( [ [1.0, 0.0, 0.0],
                      [0.0, np.cos(theta), -np.sin(theta)],
                      [0.0, np.sin(theta), np.cos(theta)] ], dtype=np.single )
    v_rotated = np.dot(R_x,v.T)
    return v_rotated


def solve(p1,p2):
    debug_print( DEBUG_ON, "Entering solve() function..." )
    x_hat = np.array( [1.0, 0.0, 0.0] )
    y_hat = np.array( [0.0, 1.0, 0.0] )
    z_hat = np.array( [0.0, 0.0, 1.0] )
    
    magnitude_p1 = np.linalg.norm(p1)
    magnitude_p2 = np.linalg.norm(p2)
    
    debug_print( DEBUG_ON, "Given...")
    debug_print( DEBUG_ON, "x_hat: {}".format(x_hat) )
    debug_print( DEBUG_ON, "y_hat: {}".format(y_hat) )
    debug_print( DEBUG_ON, "z_hat: {}".format(z_hat) )
    debug_print( DEBUG_ON, "p1: {}".format(p1) )
    debug_print( DEBUG_ON, "p2: {}".format(p2) )
    
    debug_print( DEBUG_ON, "\nTask: rotate p1 such that it is on XY-plane, where z=0...")
    p1_xz = np.array( [p1[0], 0, p1[2]] )
    theta_y = helper_findAngleBetweenTwoVecs( p1_xz, x_hat )
    theta_y = -theta_y if (p1[2] < 0) else theta_y
    p1_XYplane = helper_rotateVecAboutYAxis(p1, theta_y)  ## p1 now exists on XY plane, z=0
    #p1_XYplane = helper_rotateVecAboutYAxis(p1, -theta_y)  ## experimental
    magnitude_p1_XYplane = np.linalg.norm(p1_XYplane)
    debug_print( DEBUG_ON, "p1_xz: {}".format(p1_xz) )
    debug_print( DEBUG_ON, "theta_y (rad,deg): {}, {}".format(theta_y, np.degrees(theta_y)) )
    debug_print( DEBUG_ON, "p1_XZplane: {}".format(p1_XYplane) )
    debug_print( DEBUG_ON, "magnitude_p1: {}".format(magnitude_p1) )
    debug_print( DEBUG_ON, "magnitude_p1_XYplane: {}".format(magnitude_p1_XYplane) )
    debug_print( DEBUG_ON, "so now p1 is coplanar to XY-plane, z=0...")
    
    debug_print( DEBUG_ON, "\nTask: rotate p1 further such that it is colinear to x-axis, y=0, z=0...")
    theta_z = helper_findAngleBetweenTwoVecs( p1_XYplane, x_hat )
    theta_z = -theta_z if (p1[1] < 0) else theta_z
    p1_XAxis = helper_rotateVecAboutZAxis(p1_XYplane, -theta_z)  ## p1 now colinear with x-axis, y=0, z=0
    #p1_XAxis = helper_rotateVecAboutZAxis(p1_XYplane, theta_z)  ## experimental
    magnitude_p1_XAxis = np.linalg.norm(p1_XAxis)
    debug_print( DEBUG_ON, "theta_z (rad,deg): {}, {}".format(theta_z, np.degrees(theta_z)) )
    debug_print( DEBUG_ON, "p1_XAxis: {}".format( p1_XAxis ))
    debug_print( DEBUG_ON, "magnitude of p1 is: {}".format(magnitude_p1) )
    debug_print( DEBUG_ON, "magnitude of p1_XAxis: {}".format(magnitude_p1_XAxis) )
    debug_print( DEBUG_ON, "so now p1 is co-linear to x-axis, y=0, z=0...")
    
    debug_print( DEBUG_ON, "\nTask: rotate p2 using theta_y and theta_z...")
    p2_rotAboutY = helper_rotateVecAboutYAxis(p2, theta_y)
    p2_rotAboutYThenZ = helper_rotateVecAboutZAxis(p2_rotAboutY, -theta_z)  ## use -theta_z, just like when rotating p1...
    magnitude_p2_rotAboutY = np.linalg.norm(p2_rotAboutY)
    magnitude_p2_rotAboutYThenZ = np.linalg.norm(p2_rotAboutYThenZ)
    debug_print( DEBUG_ON, "p2: {}".format(p2) )
    debug_print( DEBUG_ON, "p2_rotAboutY: {} ".format(p2_rotAboutY) )
    debug_print( DEBUG_ON, "p2_rotAboutYThenZ: {}".format(p2_rotAboutYThenZ) )
    debug_print( DEBUG_ON, "magnitude_p2: {}".format(magnitude_p2) )
    debug_print( DEBUG_ON, "magnitude_p2: {}".format(magnitude_p2_rotAboutY) )
    debug_print( DEBUG_ON, "magnitude_p2_rotABoutYThenZ: {}".format(magnitude_p2_rotAboutYThenZ) )
    debug_print( DEBUG_ON, "so now p2 has been rotated in the same way p1 has been rotated...")
    
    debug_print( DEBUG_ON, "\ntTask: rotate p2 about x-axis such that its y-value is 0...")
    p2_yz = np.array( [0, p2_rotAboutYThenZ[1], p2_rotAboutYThenZ[2]] )
    phi_x = helper_findAngleBetweenTwoVecs( p2_yz, z_hat )
    phi_x = -phi_x if (p2[1] < 0) else phi_x
    p2_rotAboutYThenZThenX = helper_rotateVecAboutXAxis(p2_rotAboutYThenZ, phi_x)
    #p2_rotAboutYThenZThenX = helper_rotateVecAboutXAxis(p2_rotAboutYThenZ, -phi_x)  ## experimental
    magnitude_p2_rotAboutYThenZThenX = np.linalg.norm( p2_rotAboutYThenZThenX )
    debug_print( DEBUG_ON, "p2_yz: {}".format(p2_yz) )
    debug_print( DEBUG_ON, "phi_x (rad,deg): {}, {}".format(phi_x, np.degrees(phi_x)) )
    debug_print( DEBUG_ON, "p2_rotAboutYThenZThenX: {}".format(p2_rotAboutYThenZThenX) )
    debug_print( DEBUG_ON, "magnitude_p2: {}".format(magnitude_p2) )
    debug_print( DEBUG_ON, "magnitude_p2_rotYZX: {}".format( magnitude_p2_rotAboutYThenZThenX ))
    debug_print( DEBUG_ON, "so now p2 is co-planar to XZ-plane, where y=0...")
    
    p1_final = p1_XAxis
    p2_final = p2_rotAboutYThenZThenX
    return p1_final, p2_final, theta_y, theta_z, phi_x
    
def debug_print(debug_on, s):
    if debug_on:
        print( "[debug] {}".format(s) )
    return

def values_are_close_enough( a, b ):
    return np.absolute(a-b) <= 0.001

def main():
    if len(sys.argv) != 3:
        print(USAGE)
        return 1
    
    print( "arg1: {}".format(sys.argv[1]) )
    print( "arg2: {}".format(sys.argv[2]) )
    
    point1_str = sys.argv[1]
    point2_str = sys.argv[2]
    
    myp1 = MyPoint( "p1" )
    myp2 = MyPoint( "p2" )
    myp1.initializeFromString( point1_str )
    myp2.initializeFromString( point2_str )
    
    p1 = myp1.to_numpy()
    p2 = myp2.to_numpy()
    
    p1rot, p2rot, theta_y, theta_z, phi_x = solve(p1,p2)
    
    magnitude_p1 = np.linalg.norm(p1)
    magnitude_p2 = np.linalg.norm(p2)
    magnitude_p1rot = np.linalg.norm(p1rot)
    magnitude_p2rot = np.linalg.norm(p2rot)
    print( "\n---- Solution ---- ")
    print( "[given] p1: {}".format(p1) )
    print( "[given] p2: {}".format(p2) )
    print()
    print( "[solved] theta_y (rad,deg): {}, {}".format(theta_y, np.degrees(theta_y)) )
    print( "[solved] theta_z (rad,deg): {}, {}".format(theta_z, np.degrees(theta_z)) )
    print( "[solved] phi_x (rad,deg): {}, {}".format(phi_x, np.degrees(phi_x)) )
    print( "[solved] p1rot: {}".format( p1rot ))
    print( "[solved] p2rot: {}".format( p2rot ))
    print()
    print( "[derived] magnitude(p1): {}".format(magnitude_p1) )
    print( "[derived] magnitude(p2): {}".format(magnitude_p2) )
    print( "[derived] magnitude(p1rot): {}".format(magnitude_p1rot))
    print( "[derived] magnitude(p2rot): {}".format(magnitude_p2rot))
    print()
    check1 = values_are_close_enough(magnitude_p1, magnitude_p1rot)
    check2 = values_are_close_enough(magnitude_p2, magnitude_p2rot)
    check3a = values_are_close_enough(0, p1rot[1])
    check3b = values_are_close_enough(0, p1rot[2])
    check4 = values_are_close_enough(0, p2rot[1])
    print( "[pass: {}] magnitudes of p1, p1rot match.".format( check1 ) )
    print( "[pass: {}] magnitudes of p2, p2rot match.".format( check2 ) )
    print( "[pass: {}] p1rot is co-linear to x-axis (i.e. y=0, z=0)".format( check3a and check3b ))
    print( "[pass: {}] p2rot is co-planar to XZ-plane, y=0.".format( check4 ))
    
    return
    

def ut_helper_findAngleBetweenTwoVecs_test1():
    print("---- unit test: ut_transformation_aboutY ----")
    
    print(" [Test #1-- 2-dimensional vectors...]")
    v1 = np.array( [1.0, 1.0] )
    v2 = np.array( [1.0, 0.0] )
    theta_rad = helper_findAngleBetweenTwoVecs(v1,v2)
    theta_deg = np.degrees(theta_rad)
    print( "v1: {}".format(v1) )
    print( "v2: {}".format(v2) )
    print( "theta_rad: {}".format(theta_rad) )
    print( "theta_deg: {}".format(theta_deg) )
    
def ut_helper_findAngleBetweenTwoVecs_test2():
    print("---- unit test: ut_transformation_aboutY ----")
    
    print(" [Test #1-- 3-dimensional vectors...]")
    v1 = np.array( [1.0, 0.0, 1.0] )
    v2 = np.array( [1.0, 0.0, 0.0] )
    theta_rad = helper_findAngleBetweenTwoVecs(v1,v2)
    theta_deg = np.degrees(theta_rad)
    print( "v1: {}".format(v1) )
    print( "v2: {}".format(v2) )
    print( "theta_rad: {}".format(theta_rad) )
    print( "theta_deg: {}".format(theta_deg) )
    
def ut_helper_findAngleBetweenTwoVecs():
    ut_helper_findAngleBetweenTwoVecs_test1()
    ut_helper_findAngleBetweenTwoVecs_test2()

    
def ut_helper_rotateVecAboutYAxis_test1():
    print("\n---- unit test: ut_helper_rotateVecAboutYAxis (test #1) ----")
    print("  (easy case where p1 is already on the XZ-plane...)  ")
    p1 = np.array( [0.0, 0.0, 1.0] )
    x_hat = np.array( [1.0, 0.0, 0.0])
    
    p1_xz = np.array( [p1[0],0,p1[2]] )
    theta = helper_findAngleBetweenTwoVecs( p1_xz, x_hat)
    p1_rot = helper_rotateVecAboutYAxis(p1,theta)
    
    print( "p1: {}".format(p1) )
    print( "x_hat: {}".format(x_hat))
    print( "p1_xz: {}".format(p1_xz) )
    print( "theta (rad,deg): {}, {}".format(theta, np.degrees(theta)) )
    print( "p1_rot: {}".format(p1_rot) )
    print( "correct if z-value of p1-rotated is 0")
    
def ut_helper_rotateVecAboutYAxis_test2():
    print("\n---- unit test: ut_helper_rotateVecAboutYAxis (test #2) ----")
    print("  (regular case where p1 is not on the XZ-plane...)  ")
    p1 = np.array( [1.0, 1.0, 1.0] )
    x_hat = np.array( [1.0, 0.0, 0.0])
    
    p1_xz = np.array( [p1[0],0,p1[2]] )
    theta = helper_findAngleBetweenTwoVecs( p1_xz, x_hat)
    p1_rot = helper_rotateVecAboutYAxis(p1,theta)
    
    print( "p1: {}".format(p1) )
    print( "x_hat: {}".format(x_hat))
    print( "p1_xz: {}".format(p1_xz) )
    print( "theta (rad,deg): {}, {}".format(theta, np.degrees(theta)) )
    print( "p1_rot: {}".format(p1_rot) )
    print( "correct if z-value of p1-rotated is 0, y-value is unchanged")
    
def ut_helper_rotateVecAboutYAxis_test3():
    print("\n---- unit test: ut_helper_rotateVecAboutYAxis (test #3) ----")
    print("  (edge case where p1 is colinear with y-axis...)  ")
    p1 = np.array( [0.0, 1.0, 0.0] )
    x_hat = np.array( [1.0, 0.0, 0.0])
    
    p1_xz = np.array( [p1[0],0,p1[2]] )
    theta = helper_findAngleBetweenTwoVecs( p1_xz, x_hat)
    p1_rot = helper_rotateVecAboutYAxis(p1,theta)
    
    print( "p1: {}".format(p1) )
    print( "x_hat: {}".format(x_hat))
    print( "p1_xz: {}".format(p1_xz) )
    print( "theta (rad,deg): {}, {}".format(theta, np.degrees(theta)) )
    print( "p1_rot: {}".format(p1_rot) )
    print( "correct if z-value of p1-rotated is the same as p1")
    
def ut_helper_rotateVecAboutYAxis():
    ut_helper_rotateVecAboutYAxis_test1()
    ut_helper_rotateVecAboutYAxis_test2()
    ut_helper_rotateVecAboutYAxis_test3()
    
def ut_helper_rotateVecAboutXAxis():
    print("\n---- unit test: ut_helper_rotateVecAboutXAxis (test #1) ----")
    print("  (regular case where p1 is not on the YZ-plane...)  ")
    p1 = np.array( [1.0, 1.0, 1.0] )
    z_hat = np.array( [0.0, 0.0, 1.0])
    
    p1_yz = np.array( [0, p1[1], p1[2]] )
    theta = helper_findAngleBetweenTwoVecs( p1_yz, z_hat)
    p1_rot = helper_rotateVecAboutXAxis(p1,theta)
    
    print( "p1: {}".format(p1) )
    print( "norm(p1): {}".format( np.linalg.norm(p1)) )
    print( "z_hat: {}".format(z_hat))
    print( "p1_yz: {}".format(p1_yz) )
    print( "theta (rad,deg): {}, {}".format(theta, np.degrees(theta)) )
    print( "p1_rot: {}".format(p1_rot) )
    print( "correct if y-value of p1-rotated is 0, x-value is unchanged")

def ut_helper_rotateVecAboutZAxis():
    print("\n---- unit test: ut_helper_rotateVecAboutZAxis (test #1) ----")
    print("  (regular case where p1 is not on the XY-plane...)  ")
    p1 = np.array( [1.0, 1.0, 1.0] )
    y_hat = np.array( [0.0, 1.0, 0.0])

    p1_xy = np.array( [p1[0], p1[1], 0] )
    theta = helper_findAngleBetweenTwoVecs( p1_xy, y_hat)
    p1_rot = helper_rotateVecAboutZAxis(p1,theta)
    
    print( "p1: {}".format(p1) )
    print( "norm(p1): {}".format( np.linalg.norm(p1)) )
    print( "p1*cos(theta): {}".format( np.linalg.norm(p1) * np.cos(theta))  )
    print( "y_hat: {}".format(y_hat))
    print( "p1_xy: {}".format(p1_xy) )
    print( "theta (rad,deg): {}, {}".format(theta, np.degrees(theta)) )
    print( "p1_rot: {}".format(p1_rot) )
    print( "correct if x-value of p1-rotated is 0, z-value is unchanged")
    
def ut_MyPoint():
    print("---- unit test: ut_MyPoint ----")
    p1 = MyPoint( "p1" )
    p1.initializeFromString( "(1.0, 2.0, 3.0)" )
    
    p2 = MyPoint( "p2" )
    p2.initializeFromValues(10.0, 11.0, 12.0)
    
    print(p1)
    print(p2)


def ut_solve_testX(p1,p2):
    p1rot, p2rot, theta_y, theta_z, phi_x = solve(p1,p2)
    
    magnitude_p1 = np.linalg.norm(p1)
    magnitude_p2 = np.linalg.norm(p2)
    magnitude_p1rot = np.linalg.norm(p1rot)
    magnitude_p2rot = np.linalg.norm(p2rot)
    
    print( "\n\n---- unit test: ut_solve ---- ")
    print( "[given] p1: {}".format(p1) )
    print( "[given] p2: {}".format(p2) )
    
    print( "[derived] magnitude(p1): {}".format(magnitude_p1) )
    print( "[derived] magnitude(p2): {}".format(magnitude_p2) )
    
    print( "[solved] theta_y (rad,deg): {}, {}".format(theta_y, np.degrees(theta_y)) )
    print( "[solved] theta_z (rad,deg): {}, {}".format(theta_z, np.degrees(theta_z)) )
    print( "[solved] phi_x (rad,deg): {}, {}".format(phi_x, np.degrees(phi_x)) )
    print( "[solved] p1rot: {}".format( p1rot ))
    print( "[solved] p2rot: {}".format( p2rot ))
    
    print( "[check] magnitude(p1rot): {}".format(magnitude_p1rot))
    print( "[check] magnitude(p2rot): {}".format(magnitude_p2rot))
    print( "[check] p1rot is co-linear to x-axis (i.e. y=0, z=0)")
    print( "[check] p2rot is co-planar to XZ-plane, y=0.")
    
    p2rot_alt = np.array( [16.3740, 0, -8.7010] )
    magnitude_p2rot_alt = np.linalg.norm(p2rot_alt)
    print( "[check] magnitude(p2rot_alt): {}".format(magnitude_p2rot_alt) )
    angle_between_p1_p2 = helper_findAngleBetweenTwoVecs(p1, p2)
    angle_between_p1rot_p2rot = helper_findAngleBetweenTwoVecs(p1rot, p2rot)
    angle_between_p1rot_p2rot_alt = helper_findAngleBetweenTwoVecs(p1rot, p2rot_alt)
    check5 = values_are_close_enough( angle_between_p1_p2, angle_between_p1rot_p2rot )
    check6 = values_are_close_enough( angle_between_p1_p2, angle_between_p1rot_p2rot_alt )
    print( "[info] angle between p1,p2: {},{}".format(angle_between_p1_p2,
                                                      np.degrees(angle_between_p1_p2)))
    print( "[info] angle between p1rot,p2rot: {},{}".format(angle_between_p1rot_p2rot,
                                                            np.degrees(angle_between_p1rot_p2rot)))
    print( "[info] angle between p1rot,p2rot_alt: {},{}".format(angle_between_p1rot_p2rot_alt,
                                                                np.degrees(angle_between_p1rot_p2rot_alt)))
    print( "[pass: {}] angle between p1rot,p2rot: {}".format(angle_between_p1rot_p2rot,check5) )
    print( "[pass: {}] angle between p1rot, p2rot_alt: {}".format(angle_between_p1rot_p2rot_alt,check6) )
    
    norm_p1_p2 = np.cross(p1,p2)
    norm_p1rot_p2rot = np.cross(p1rot,p2rot)
    norm_p1rot_p2rotAlt = np.cross(p1rot, p2rot_alt)
    print( "[info] normal vector of p1 x p2: {}".format(norm_p1_p2) )
    print( "[info] normal vector of p1rot x p2rot: {}".format(norm_p1rot_p2rot) )
    print( "[info] normal vector of p1rot x p2rotAlt: {}".format(norm_p1rot_p2rotAlt))
    print( "\n" )
    
def ut_solve():
    #ut_solve_testX( np.array( [1.0, 1.0, 1.0] ), np.array( [3.0, 2.0, 1.0] ) )
    #ut_solve_testX( np.array( [1.0, 2.0, 3.0] ), np.array( [4.0, 5.0, 6.0] ) )
    #ut_solve_testX( np.array( [-4.376, -6.231, -20.592] ), np.array( [-11.088, -7.112, -12.958] ) )
    #ut_solve_testX( np.array( [-4.944, -6.175, -20.211] ), np.array( [-11.656, -7.056, -12.577] ) )
    
    # mb1n1csup
    #  note: this turned out to be wrong because our ep2 was missing
    #        four residues... garbage in, garbage out. can't trust the 
    #        output of this.
    #ut_solve_testX( np.array( [-10.975, -11.360, -10.615] ),
    #                np.array( [2.078, -14.329, 7.965] ) )
    
    # mb1n1a
    #ut_solve_testX( np.array( [8.102, -16.542, 6.673] ),
    #                np.array( [-20.799, 6.718, -1.416] ) )
    
    # mb2n -- weird... where'd i get these values?
    # how i got these values:
    # run loadLabelMb2nsup_v1
    # center the molecule by adding the negative of it's (x,y,z) orientation
    # now call centerofmass on ep1 and ep2.
    #---------------
    #ut_solve_testX( np.array( [-14.664, -2.587, -8.014] ),
    #                np.array( [-17.083, -6.178, 1.04] ) )
    
    # mb2n -- weird where'd i get these values
    ut_solve_testX( np.array( [1.747, 5.5531, 5.075] ),
                    np.array( [-0.6272, 1.940, 14.103] ) )
    
    # mb1n1csup -- second try
    # mb1n1csupv1_min2_roschi.pdb after centering it
    #    (where did i get ep2 2.078m -14.329, 7.965 last time)
    #-----------------------------------
    #ut_solve_testX( np.array( [-10.975, -11.360, -10.615] ),
    #                np.array( [1.250, -12.448, 11.857] ) )
    
    
    
    
if __name__ == '__main__':
    #ut_helper_rotate2d()  ## correct
    #ut_helper_findAngleBetweenTwoVecs()  ## correct
    #ut_helper_rotateVecAboutYAxis()  ## correct
    #ut_helper_rotateVecAboutXAxis()  ## correct
    #ut_helper_rotateVecAboutZAxis()  ## correct
    
    #ut_MyPoint()  ## correct
    
    ut_solve()
    #main()