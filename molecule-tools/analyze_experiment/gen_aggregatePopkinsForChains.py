#!/usr/bin/env python3
# filename: genData_aggregatePopkinsForChains.py
# author: Jon David
# description:
#   Reads all cumulative_class_stats.groupByAggSize.<experimentName>.csv
#     from each run, and produces a single file for each:
#       * cumulative_class_stats.2mer.<expName>.csv
#       * cumulative_class_stats.3mer.<expName>.csv
#       * cumulative_class_stats.4mer.<expName>.csv
#       * cumulative_class_stats.5mer.<expName>.csv
#       * cumulative_class_stats.6mer.<expName>.csv
#       * cumulative_class_stats.7mer.<expName>.csv
#       * cumulative_class_stats.8mer.<expName>.csv
#       * cumulative_class_stats.9mer.<expName>.csv
#       * cumulative_class_stats.10mer.<expName>.csv
#
#    Where,
#      each row represents time, and columns represent runs.
#--------------------------------------------------------------------

import sys
import re
import csv

import glob
import pandas as pd
import numpy as np

USAGE_STR = """

 Usage #1:
   python2 genData_popkinsForChains.py <expName>
 
   where, <expName> = (string) name of experiment

"""

def read_csv(fname):
    """Return matrix is numberOfTimesteps x numberOfRuns."""
    df = pd.read_csv(fname, sep=',',header=None)
    M = df.to_numpy()
    return M

def _helper_fillMatrix(M, maxRows):
    ## matrix = fillInRows(matrix, numSteps)
    # currNumRows = M.shape[0]
    # numRowsToAdd = maxRows - currNumRows

    # lastRowID = currNumRows-1
    # lastRelevantRow = M[ lastRowID, : ]
    # print( "\t (before) M.shape: {}".format( M.shape ) )
    # for i in range(0, numRowsToAdd):
    #     M = np.vstack( [M, lastRelevantRow] )
    # print( "\t (after) M.shape: {}".format( M.shape ) )

    M_rows = M.shape[0]
    M_cols = M.shape[1]
    M_new = np.zeros( (maxRows, M_cols ))

    print( "\t (before) M.shape: {}".format( M.shape ))
    for i in range(0, M_rows):
        M_new[i,:] = M[i,:]

    for i in range(M_rows, maxRows):
        M_new[i,:] = M[M_rows-1,:]
    print( "\t (after) M_new.shape: {}".format( M_new.shape ))
    return M_new

    
def aggPopkinForChains(expName):
    m_list = []
    #numSteps = 0
    expectedNumSteps = 50001  ## 50k records, for 500k steps, recorded every 10.
    expectedNumRuns = 100
    numExperimentsFound = 0
    for f in glob.glob("**/*groupByAggsize.{}.csv".format(expName)):
        M = read_csv(f)
        m_list.append( M )
        numSteps = M.shape[0]
        numExperimentsFound = 1 + numExperimentsFound
    numRuns = numExperimentsFound

    AFree = np.zeros( (expectedNumSteps, expectedNumRuns) )
    #ASingleton = np.zeros( (expectedNumSteps, expectedNumRuns) )
    ASingletonA = np.zeros( (expectedNumSteps, expectedNumRuns) )
    ASingletonB = np.zeros( (expectedNumSteps, expectedNumRuns) )
    ASingletonAB = np.zeros( (expectedNumSteps, expectedNumRuns) )
    
    A2 = np.zeros( (expectedNumSteps, expectedNumRuns) )
    A3 = np.zeros( (expectedNumSteps, expectedNumRuns) )
    A4 = np.zeros( (expectedNumSteps, expectedNumRuns) )
    A5 = np.zeros( (expectedNumSteps, expectedNumRuns) )
    A6 = np.zeros( (expectedNumSteps, expectedNumRuns) )

    matrixCounter = 0
    for matrix in m_list:
        ## if matrix has less than numSteps rows,
        ##   fill in the rest of the values...
        if matrix.shape[0] < expectedNumSteps:
            print( "(test) matrix.shape[0] {} < expectedNumSteps {}".format( matrix.shape[0], expectedNumSteps ))
            print( "(before) matrix.shape: {}".format( matrix.shape ))
            matrix = _helper_fillMatrix(matrix, expectedNumSteps)
            print( "(after) matrix.shape: {}".format( matrix.shape ))
        print("matrixCounter: {}".format(matrixCounter))
        runID = matrixCounter

        AFree[:,runID] = matrix[:,0]
        #ASingleton[:,runID] = matrix[:,1]
        ASingletonA[:,runID] = matrix[:,1]
        ASingletonB[:,runID] = matrix[:,2]
        ASingletonAB[:,runID] = matrix[:,3]
        
        A2[:,runID] = matrix[:,4]
        A3[:,runID] = matrix[:,5]
        A4[:,runID] = matrix[:,6]
        A5[:,runID] = matrix[:,7]
        A6[:,runID] = matrix[:,8] + matrix[:,9] + matrix[:,10] + matrix[:,11]
        matrixCounter = 1 + matrixCounter

    np.savetxt("cumulative_class_stats.free.{}.csv".format(expName), AFree.astype(int), fmt="%i", delimiter=',')
    #np.savetxt("cumulative_class_stats.singletons.{}.csv".format(expName), ASingleton.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.singletonsA.{}.csv".format(expName), ASingletonA.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.singletonsB.{}.csv".format(expName), ASingletonB.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.singletonsAB.{}.csv".format(expName), ASingletonAB.astype(int), fmt="%i", delimiter=',')
        
    np.savetxt("cumulative_class_stats.2mer.{}.csv".format(expName), A2.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.3mer.{}.csv".format(expName), A3.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.4mer.{}.csv".format(expName), A4.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.5mer.{}.csv".format(expName), A5.astype(int), fmt="%i", delimiter=',')
    np.savetxt("cumulative_class_stats.6mer.{}.csv".format(expName), A6.astype(int), fmt="%i", delimiter=',')
    


if __name__ == '__main__':
    numCmdArgs = len(sys.argv)
    print("numCmdArgs: {}".format( numCmdArgs ))
    if (numCmdArgs != 2):
        print(USAGE_STR)
        sys.exit("Incorrent number of arguments.")
    expName = sys.argv[1]
    aggPopkinForChains(expName)
