#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Calculates the spheric volume under a plane to be used for 
calculating the probability a ligand is "on the plane" and close enough to bind to IgE.

@author: jdavid
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.integrate import quad, dblquad, tplquad

DEBUG_ON = True


def print_debug(s, DEBUG_ON):
    if DEBUG_ON:
        print("(DEBUG) {}".format(s))

#def pdf(theta, phi, r):
#    return (1.0/(4*np.pi*np.power(t,(d/2.0)))) * np.exp(-1.0 * (np.power(r,2)) / (4*D*t))
    
#def f(theta, phi, r):
#    return np.pow(r,2) * np.sin(theta) * (pdf(theta, phi,r))

def calc_singleIntegral(r_lower, r_upper, t, d, D):
    f = lambda r: (1.0/(4*np.pi*D*np.power(t,(d/2.0)))) * \
        (np.exp(-1.0*np.power(r,2) / (4*D*t)))
        
    value = quad(f, r_lower, r_upper)
    return value

def ut_calc_singleIntegral():
    R1 = 0
    R2 = 9
    t = 5
    d = 3
    D = 20
    value = calc_singleIntegral(R1, R2, t, d, D)
    print("Calculated single integral: {}".format(value))
    print("Expected single integral: {}".format(0.0))

    

## Propagator function, as defined by Saxton et al.
def get_f(t, d, D):
    f = lambda phi, theta, r: \
        np.power(r,2) * np.sin(phi) * \
            (1.0/np.power((4*np.pi*D*t),(d/2.0))) * \
                (np.exp(-1.0 * np.power(r,2) / (4*D*t)))
    return f

def calc_tripleIntegral(r_lower, r_upper, theta_lower, theta_upper,
                        phi_lower, phi_upper, t, d, D):

    f = get_f(t,d,D)
    #f = lambda phi, theta, r: \
    #    np.power(r,2) * np.sin(phi) * \
    #        (1.0/np.power((4*np.pi*D*t),(d/2.0))) * \
    #            (np.exp(-1.0 * np.power(r,2) / (4*D*t)))
    
    ## just calculate volume of sphere
    #f = lambda phi, theta, r: np.power(r,2) * np.sin(phi)  ## this correctly calculates volume of a sphere

    value = tplquad(f,
                    r_lower, r_upper,
                    lambda r: theta_lower, lambda r: theta_upper,
                    lambda r,t: phi_lower, lambda r,t: phi_upper)[0]
    return value

def ut_calc_tripleIntegral():
    #t = 1E-5    ## 10 microseconds, is 1E-5 seconds.
    t = 1E-4    ## 10 microseconds, is 1E-5 seconds.
    d = 3        ## 3-dimensions
    D = 120      ## 120 micrometers^2 per second.
    ## integral limits
    R1 = 0
    R2 = np.inf
    theta_lower = 0
    theta_upper = 2*np.pi
    phi_lower = 0
    phi_upper = np.pi  #np.arccos(R1/R2)
    
    value = calc_tripleIntegral(R1, R2, theta_lower, theta_upper,
                                phi_lower, phi_upper, t, d, D)
    print("---- Unit Test for: calc_tripleIntegral() ----")
    print("[input] t: {}".format(t))
    print("[input] d: {}".format(d))
    print("[input] D: {}".format(D))
    
    print("[1] Calculated triple integral: {}".format(value))
    #print("[1] Expected triple integral: {}".format((4.0*np.pi/3.0)))
    print("[1] Expected triple integral: {}".format(1.0))
    
    print()
    value = calc_tripleIntegral(R1, R2, theta_lower, theta_upper,
                        phi_lower, phi_upper/2.0, t, d, D)
    print("[2] Calculated triple integral: {}".format(value))
    print("[2] Expected triple integral: {}".format(0.5))
    
    print()
    r_mean = np.power(2*d*D*t,1.0/2.0)
    r_mean = value * r_mean
    r_std = np.power((2.0/d),1.0/2.0) * r_mean
    value = calc_tripleIntegral(r_mean-r_std, r_mean+r_std,
                                        theta_lower, theta_upper,
                                        phi_lower, phi_upper, t, d, D)
    print("[3][input] r_mean: {}".format(r_mean))
    print("[3][input] r_std: {}".format(r_std))
    print("[3][input] R1: {}".format(r_mean-r_std))
    print("[3][input] R2: {}".format(r_mean+r_std))
    print("[3] Calculated triple integral: {}".format(value))
    print("[3] Expected triple integral: {}".format(0.68))
    
    
    ## what if you make D smaller?
    print()
    D=80
    r_mean = 2*d*D*t
    r_std = np.power((2.0/d),1.0/2.0) * r_mean
    value = value = calc_tripleIntegral(r_mean-r_std, r_mean+r_std,
                                        theta_lower, theta_upper,
                                        phi_lower, phi_upper, t, d, D)
    print("[4][input] r_mean: {}".format(r_mean))
    print("[4][input] r_std: {}".format(r_std))
    print("[4][input] R1: {}".format(r_mean-r_std))
    print("[4][input] R2: {}".format(r_mean+r_std))
    print("[4] Calculated triple integral: {}".format(value))
    print("[4] Expected triple integral: {}".format(0.68))
    
    
def calc_partA(y, R, yMax, yMin):
    return (yMax-yMin) * np.pi * (np.power(R,2) - np.power(y,2))

def calc_partB(y, R, yMax, yMin):
    return (-1.0/3.0) * np.pi * (np.power(yMax,3) - np.power(yMin,3))

def calc_partC(y, R, yMax, yMin):
    return y * np.pi * (np.power(yMax,2) - np.power(yMin,2))

def calc_integral(y, R, yMax, yMin):
    A = calc_partA(y, R, yMax, yMin)
    B = calc_partB(y, R, yMax, yMin)
    C = calc_partC(y, R, yMax, yMin)
    volume = A + B + C
    return volume
    
def calc_sphericVolumeUnderPlane(y,heightOfIgE,R):
    """(boxLength, boxWidth, boxHeight) is the dimension of the box,
    heightOfIge in nm, numLigands (integer), and R is radius (in nm) represents
    a sphere where a ligand can appear anywhere in that volume after a given time step."""
    
    ## Note: x and z value are not used.
    ##       no need to when assuming periodic boundary conditions.
    yMax = 0
    yMin = 0
    
    
    if y-R >= heightOfIgE:
        ## case 0: sphere is entirely above XZ-plane, y=90.
        yMax = y+R
        yMin = y-R
    elif y+R <= heightOfIgE:
        ## case 1: sphere is completely above XZ-playe, y=90 and y=0
        yMax = y+R
        yMin = y-R
    elif (y-R <= heightOfIgE) and (heightOfIgE <= y+R):
        ## case 2: sphere is intersected by XZ-plane, y=90.
        yMax = heightOfIgE
        yMin = y-R
    elif (y-R <= 0) and (0 <= y+R):
        ## case 3: sphere is intersected by XZ-plane, y=0.
        yMax = y+R
        yMin = 0
    else:
        raise Exception("Error: no other cases should exist.")
        
    V = calc_integral(y,R,yMax,yMin)
    return V

def calc_maxVolume(numLigands, R):
    V = (4.0/3.0) * np.pi * np.power(R,3)
    return numLigands * V

def getRandomCoordinate(xMin, xMax, yMin, yMax, zMin, zMax):
    x = np.random.uniform(xMin, xMax)
    y = np.random.uniform(yMin, yMax)
    z = np.random.uniform(zMin, zMax)
    return (x,y,z)

def run_singleTrial(boxLength, boxWidth, boxHeight, igeHeight,
                    numLigands, ligandR):
    xMax = boxLength/2.0
    xMin = -xMax
    yMax = boxHeight
    yMin = 0
    zMax = boxHeight/2.0
    zMin = -zMax
    
    t = 1E-5    ## 10 microseconds, is 1E-5 seconds.
    d = 3        ## 3-dimensions
    D = 120      ## 120 micrometers^2 per second.
    # D_ige = 0.09
    # d_ige = 2
    
    probSingleMolecule = 0.0
    for ligandID in range(0, numLigands):
        (x,y,z) = getRandomCoordinate(xMin, xMax, yMin, yMax, zMin, zMax)
        #V = calc_sphericVolumeUnderPlane(y,igeHeight,ligandR)
        r_lower = y-igeHeight
        r_mean = 2*d*D*t
        r_std = np.power((2.0/d),1.0/2.0) * r_mean
        r_upper = r_mean + r_std
        theta_lower = 0
        theta_upper = 2*np.pi
        phi_lower = 0
        phi_upper = np.arccos(r_lower/r_upper)
        probSingleMolecule = calc_tripleIntegral(r_lower, r_upper, theta_lower, theta_upper,
                        phi_lower, phi_upper, t, d, D)
    return probSingleMolecule

def run_experiment(boxLength ,boxWidth, boxHeight, igeHeight,
                   numLigands, ligandR, numTrials):
    
    probList = []
    for trialID in range(0,numTrials):
        prob = run_singleTrial(boxLength, boxWidth, boxHeight, igeHeight,
                            numLigands, ligandR)
        probList.append(prob)
    return probList


## used for sanity check.
## take-aways: as R increases, volume increases. The error increases as well.
def plotAsVolume_singleVaryR_experiment(expName, boxLength, boxWidth, boxHeight, igeHeight, numLigands, numTrials):
    listOfLists = []
    maxRValue = 90
    ligandRList = range(0, maxRValue)
    numLigandsList = [5,10,15,20]
    maxVolumeList = []
    for ligandR in ligandRList:
        volList = run_experiment(boxLength, boxWidth, boxHeight,
                                 igeHeight, numLigands, ligandR, numTrials)
        listOfLists.append( volList )
        maxVolume = calc_maxVolume(numLigands, ligandR)
        maxVolumeList.append( maxVolume )
        
    M = np.array( listOfLists )
    mean_vec = M.mean(axis=1)  ## calculate mean, row-wise
    std_vec = M.std(axis=1)    ## calculate std, row-wise
    
    maxVolume_vec = np.array( maxVolumeList )

    plt.plot(ligandRList, mean_vec, label=expName)
    plt.fill_between(ligandRList, mean_vec-std_vec, mean_vec+std_vec, alpha=0.2)
    
    plt.plot(ligandRList, maxVolume_vec, linestyle='--', label='maxVolume')
    plt.xlabel("Radius (nm)")
    plt.ylabel("Volume")
    plt.xlim(0.0, maxRValue)
    plt.ylim(0.0,calc_maxVolume(20,ligandR))
    plt.title(expName)
    plt.show()
    
## used for sanity check.
## take-aways: as R increases, volume increases. The error increases as well.
def plotAsProb_singleVaryR_experiment(expName, boxLength, boxWidth, boxHeight, igeHeight, numLigands, numTrials):
    listOfLists = []
    maxRValue = 90
    ligandRList = range(0, maxRValue)
    numLigandsList = [5,10,15,20]
    probList = []
    for ligandR in ligandRList:
        probList = run_experiment(boxLength, boxWidth, boxHeight,
                                  igeHeight, numLigands, ligandR, numTrials)
        #listOfLists.append( volList )
        #maxVolume = calc_maxVolume(numLigands, ligandR)
        #maxVolumeList.append( maxVolume )
        
    M = np.array( probList )
    mean_vec = M.mean()  ## axis=1calculate mean, row-wise
    std_vec = M.std()    ## calculate std, row-wise
    
    #maxVolume_vec = np.array( maxVolumeList )
    #proportion_vec = mean_vec / maxVolume_vec

    plt.plot(mean_vec,label=expName)
    plt.fill_between(mean_vec, mean_vec-std_vec, mean_vec+std_vec, alpha=0.2)
    #plt.plot(ligandRList, maxVolume_vec, linestyle='--', label='maxVolume')
    plt.xlabel("Radius (nm)")
    plt.ylabel("Proportion of volume near surface")
    plt.xlim(0.0, maxRValue)
    plt.ylim(0.0,1.0)
    plt.title(expName)
    plt.show()
    
    
## used for sanity check.
## take-aways: as R increases, volume increases. The error increases as well.
def plotAsProbFixedDenom_singleVaryR_experiment(expName, boxLength, boxWidth, boxHeight, igeHeight, numLigands, numTrials):
    listOfLists = []
    maxRValue = 90
    ligandRList = range(0, maxRValue)
    #numLigandsList = [5,10,15,20]
    maxVolumeList = []
    for ligandR in ligandRList:
        volList = run_experiment(boxLength, boxWidth, boxHeight,
                                 igeHeight, numLigands, ligandR, numTrials)
        listOfLists.append( volList )
        maxVolume = calc_maxVolume(numLigands, ligandR)
        maxVolumeList.append( maxVolume )
        
    M = np.array( listOfLists )
    mean_vec = M.mean(axis=1)  ## calculate mean, row-wise
    std_vec = M.std(axis=1)    ## calculate std, row-wise
    
    onSurfaceVolume = (boxLength * boxWidth * igeHeight) * numLigands
    proportion_vec = mean_vec / onSurfaceVolume
    proportion_std_vec = std_vec / onSurfaceVolume

    plt.plot(ligandRList, proportion_vec, label=expName)
    plt.fill_between(ligandRList,
                     proportion_vec-proportion_std_vec,
                     proportion_vec-proportion_std_vec, alpha=0.2)
    #plt.fill_between(ligandRList, mean_vec-std_vec, mean_vec+std_vec, alpha=0.2)
    #plt.plot(ligandRList, maxVolume_vec, linestyle='--', label='maxVolume')
    plt.xlabel("Radius (nm)")
    plt.ylabel("Proportion of volume near surface")
    plt.xlim(0.0, maxRValue)
    plt.ylim(0.0,1.0)
    plt.title(expName)
    plt.show()

## sanity check: yep, plots show expected behavior.
def run_varyR_experiments():
    boxLength = 200
    boxWidth = 200
    boxHeight = 200
    igeHeight = 90
    numTrials = 100
    
    #sns.set()
    #plotAsVolume_singleVaryR_experiment('L20', boxLength, boxWidth, boxHeight, igeHeight, 20, numTrials)
    #plotAsVolume_singleVaryR_experiment('L15', boxLength, boxWidth, boxHeight, igeHeight, 15, numTrials)
    #plotAsVolume_singleVaryR_experiment('L10', boxLength, boxWidth, boxHeight, igeHeight, 10, numTrials)
    #plotAsVolume_singleVaryR_experiment('L5', boxLength, boxWidth, boxHeight, igeHeight, 5, numTrials)
    
    #sns.set()
    #plotAsProb_singleVaryR_experiment('L20', boxLength, boxWidth, boxHeight, igeHeight, 20, numTrials)
    #plotAsProb_singleVaryR_experiment('L15', boxLength, boxWidth, boxHeight, igeHeight, 15, numTrials)
    #plotAsProb_singleVaryR_experiment('L10', boxLength, boxWidth, boxHeight, igeHeight, 10, numTrials)
    #plotAsProb_singleVaryR_experiment('L5', boxLength, boxWidth, boxHeight, igeHeight, 5, numTrials)
    
    sns.set()
    plotAsProbFixedDenom_singleVaryR_experiment('L20', boxLength, boxWidth, boxHeight, igeHeight, 20, numTrials)
    plotAsProbFixedDenom_singleVaryR_experiment('L15', boxLength, boxWidth, boxHeight, igeHeight, 15, numTrials)
    plotAsProbFixedDenom_singleVaryR_experiment('L10', boxLength, boxWidth, boxHeight, igeHeight, 10, numTrials)
    plotAsProbFixedDenom_singleVaryR_experiment('L5', boxLength, boxWidth, boxHeight, igeHeight, 5, numTrials)
            
        
def run_all_experiments():
    boxLength = 200
    boxWidth = 200
    boxHeight = 200
    igeHeight = 90
    numTrials = 1
    
    numRValues = 10
    numLigandValues = 20    
    results = np.zeros( (numRValues*numLigandValues, 4), dtype=float )
    print("begin experiment")
    experimentID = 0
    for ligandR in range(0,numRValues):
        for numLigands in range(0,numLigandValues):
            volList = run_experiment(boxLength, boxWidth, boxHeight,
                                     igeHeight, numLigands, ligandR, numTrials)
            print("running experiment R:{}, L:{}".format(ligandR, numLigands))
            volArray = np.array( volList )
            volMean = volArray.mean()
            maxVolume = numTrials * numLigands * calc_maxVolume(numLigands, ligandR)
            if maxVolume:
                probOnSurface = volMean / maxVolume
            else:
                probOnSurface = 0
            #results[ligandR, numLigands, experimentID] = probOnSurface
            results[experimentID, :] = np.array( [experimentID, ligandR, numLigands, probOnSurface] )
            experimentID = 1 + experimentID
    return results
            
def plot_results(results):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter( results[:,1], results[:,2], results[:,3] )
    
    ax.set_xlabel('Radius (nm)')
    ax.set_ylabel('Number of Ligands')
    ax.set_zlabel('On Surface Probability')
    
    plt.show()
    
def main():
    #results = run_all_experiments()
    #plot_results(results)
    
    run_varyR_experiments()
    
def ut_calc_integral():
    
    y=0
    R=10
    yMax=R
    yMin=-R
    actualV = calc_integral(y,R,yMax,yMin)
    expectedV = (4.0/3.0) * np.pi * np.power(R,3)
    
    print("----Unit Test: calc_integral()----")
    print("[input] y: {}".format(y))
    print("[input] R: {}".format(R))
    print("[input] yMax: {}".format(yMax))
    print("[input] yMin: {}".format(yMin))
    print()
    print("Calculated V: {}".format(actualV))
    print("Expected V: {}".format(expectedV))

def ut_calc_sphericVolumeUnderPlane():
    x = 0
    y = 9
    heightOfIgE = 9
    R = 5
    calculatedV = calc_sphericVolumeUnderPlane(y,heightOfIgE,R)
    expectedV = calc_integral(y,R,heightOfIgE,y-R)
    
    print("----Unit Test: calc_sphericVolumeUnderPlane()----")
    print("[input] x: {}".format(x))
    print("[input] y: {}".format(y))
    print("[input] R: {}".format(R))
    print("[input] heightOfIge: {}".format(heightOfIgE))
    print()
    print("Calculated V: {}".format(calculatedV))
    print("Expected V: {}".format(expectedV))
    
def ut_run_singleTrial():
    boxLength = 200
    boxWidth = 200
    boxHeight = 200
    igeHeight = 90
    numLigands = 20
    ligandR = 0
    
    volumeList = run_singleTrial(boxLength, boxWidth, boxHeight, igeHeight, numLigands, ligandR)
    print("----Unit Test: run_singleTrial()----")
    print("volumeList: {}".format(volumeList))
    
    
#def ut_run_experiment():
#    run_experiment(boxLength ,boxWidth, boxHeight, igeHeight, numLigands, ligandR, numTrials)

##---- main ----
#ut_calc_integral()
#ut_calc_sphericVolumeUnderPlane()
#ut_run_singleTrial()
#ut_calc_singleIntegral()
ut_calc_tripleIntegral()
#run_varyR_experiments()
#main()    
    
## create plot
## independent-axis is: number of trials
## dependent-axis is: average volume given number of trials (with errorbars)