#!/usr/bin/env python
# filename: genData_aggregateHopkinsForChains.py
# author: Jon David
# description:
#   Reads all cumulative_class_stats.groupByAggSize.<experimentName>.csv
#     from each run, and produces a single file for each:
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
   python2 gen_aggregateHopkinsData.py <expName> <inputFilename>
 
   where, <expName> :: (string) name of experiment
          <inputFilename> :: (string) self-descriptive

"""

def read_csv(fname):
    """Return matrix is numberOfTimesteps x numberOfRuns."""
    df = pd.read_csv(fname, sep=',',header=None)
    M = df.to_numpy()
    return M

def aggHopkinsData(expName, ifname):
    numRows = 0
    numCols = 0
    m_list = []
    numExperimentsFound = 0
    for f in glob.glob("**/{}".format( ifname )):
        print("Process file {}".format( f ))
        numExperimentsFound = 1 + numExperimentsFound
        M = read_csv(f)
        m_list.append( M )
        numRows, numCols = M.shape
        if numRows != 1:
            raise Exception("Invalid: more than one row found!")
    A = np.zeros( (numExperimentsFound, numCols) )  ## row-vector

    matrixCounter = 0
    for M in m_list:
        print("matrixCounter: {}".format(matrixCounter))
        A[matrixCounter] = M
        matrixCounter = 1 + matrixCounter

    np.savetxt("cumulative_hopkins_stats.{}.csv".format(expName), A.T.astype(float), fmt="%1.4f", delimiter=',')



if __name__ == '__main__':
    numCmdArgs = len(sys.argv)
    print("numCmdArgs: {}".format( numCmdArgs ))
    if (numCmdArgs != 3):
        print(USAGE_STR)
        sys.exit("Incorrent number of arguments.")
    expName = sys.argv[1]
    inputFilename = sys.argv[2]
    aggHopkinsData(expName, inputFilename)
