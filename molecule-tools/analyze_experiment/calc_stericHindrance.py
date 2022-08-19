#!/usr/bin/env python3
# filename: calc_stericHindrance.py
# author: Jon David
# description:
#   Reads a file with the same format as full_bindingsites.data,
#     but now each row represents a single run, and the row is a list of edges
#     which are the list of edges at the last completed timestep.
#
#   Outputs counts and conditional probabilities used to describe
#     steric hindrance for each ligand type.

#--------------------------------------------------------------------
# input:
#   each row represents the binding site data for each run's
#   last successful timestep.
#
#   Each row consists of a list of edges (Mol1,Bind1,Mol2,Bind2)
#     separated by commas, and ending with a semicolon,
#     where Mol1, and Mol2 represent molecule IDs,
#     and Bind1 and Bind2 represent binding site IDs of the
#     corresponding molecule.
#
#   Example row: (1,1,2,2),(1,2,3,4);
#--------------------------------------------------------------------

import sys
import re
import csv

import numpy as np
from collections import deque

from util_fullBindingSitesParser import *

USAGE_STR = """

 Usage #1:
   python2 calc_stericHindrance.py <ifile> <ofname> <numMolTypes> <totalMols> <startIndex> <numTimesteps>
 
   where, <ifile> = (string) name of input bindingsite data file,
          <ofname> = (string) name of output report summary file,
          <numMolType> = (uint) the number of molecule types (including IgE receptor)
          <totalMols> = (int) total number of molecules
          <startIndexList> = [(int)] a list describing the start index of each molecule type.

  Example #1:
    Suppose I have an experiment with 20R, 10L, and 10M; then:
      <numMolType> = 3
      <totalMols> = 40
      <startIndexList> = "0,20,30"
"""

def checkIfSiteXIsBound( moleculeID, listOfEdges, expectedSiteVal ):
    for e in listOfEdges:
        if (e.mol1 == moleculeID) and (e.bsite1 == expectedSiteVal):
            return True
    return False

def checkIfSiteAIsBound( moleculeID, listOfEdges, expectedSiteVal = 0 ):
    return checkIfSiteXIsBound( moleculeID, listOfEdges, expectedSiteVal )

def checkIfSiteBIsBound( moleculeID, listOfEdges, expectedSiteVal = 1 ):
    return checkIfSiteXIsBound( moleculeID, listOfEdges, expectedSiteVal )

def checkIfBothSitesBound(moleculeID, listOfEdges):
    siteAIsBound = checkIfSiteAIsBound( moleculeID, listOfEdges )
    siteBIsBound = checkIfSiteBIsBound( moleculeID, listOfEdges )
    bothAreBound = siteAIsBound and siteBIsBound
    #print( "[DEBUG] moleculeID: {}, ABound: {}, BBound: {}, BothBound: {}".format( moleculeID, siteAIsBound, siteBIsBound, bothAreBound ))
    return bothAreBound

def classify_ligandID( moleculeID, startIdxList ):
    """Classifies ligand into one of the ligand types."""
    moleculeType = 0
    for i in range(1, len(startIdxList)):
        if (startIdxList[i-1] <= moleculeID) and (moleculeID < startIdxList[i]):
            break
        moleculeType = 1 + moleculeType
    #print( "\t[DEBUG] moleculeID: {}, classified type: {}".format( moleculeID, moleculeType ))
    return moleculeType

def update_grand_table( grandTable, lesserTable ):
    for key in lesserTable.keys():
        if key not in grandTable.keys():
            grandTable[key] = 0
        grandTable[key ]= lesserTable[key] + grandTable[key]
    return grandTable
    
def update_table_addAmount( tab, key, val ):
    if key not in tab.keys():
        tab[key] = 0
    tab[key] = val + tab[key]
    
def populate_stericHindranceTable( fout, llist_edges, numRecs, startIdxList ):
    grandBindEventTbl = {}
    for listOfEdges in llist_edges:
        activeMoleculeIDList = []
        bindEventTbl = {}
        for e in listOfEdges:
            moleculeID = e.mol1
            if moleculeID < numRecs: continue
            activeMoleculeIDList.append( moleculeID )
            moleculeType = classify_ligandID( moleculeID, startIdxList )
            siteID = e.bsite1
            k = (moleculeType, siteID)
            update_table_addAmount( bindEventTbl, k, 1 )  ## increment by one
        for moleculeID in set( activeMoleculeIDList ):
            bothSitesBound = checkIfBothSitesBound( moleculeID, listOfEdges)
            moleculeType = classify_ligandID( moleculeID, startIdxList )
            if bothSitesBound:
                k = (moleculeType, "both")
                update_table_addAmount( bindEventTbl, k, 1)
        update_grand_table( grandBindEventTbl, bindEventTbl )
    return grandBindEventTbl

def compute_stericHindrance_perType( T, moleculeType ):
    countSiteA = 0
    countSiteB = 0
    countSiteBoth = 0

    if (moleculeType, 0) not in T.keys():
        T[ (moleculeType,0) ] = 0
    if (moleculeType, 1) not in T.keys():
        T[ (moleculeType,1) ] = 0     
    if (moleculeType, "both") not in T.keys():
        T[ (moleculeType,"both") ] = 0         

    for key in T.keys():
        kmoleculeType = key[0]
        if moleculeType == kmoleculeType:
            countSiteA = T[ (moleculeType, 0) ]
            countSiteB = T[ (moleculeType, 1) ]
            countSiteBoth = T[ (moleculeType, "both") ]
            # if (moleculeType, "both") not in T.keys():
            #     countSiteBoth = 0
            # else:
            #     countSiteBoth = T[ (moleculeType, "both")]
    ## P(Li|Lj) = Count(Lij) / Count(Lj)


    #PA_givenB = countSiteBoth / countSiteB
    #PB_givenA = countSiteBoth / countSiteA

    PA_givenB = -1 if (countSiteB == 0) else (countSiteBoth / countSiteB)
    PB_givenA = -1 if (countSiteA == 0) else (countSiteBoth / countSiteA)
    
    return PA_givenB, PB_givenA

def compute_stericHindrance(f, T, numMolTypes ):
    """T is the steric hindrance table."""

    print( "\n Computing Steric Hindrance per ligand type... \n" )
    for ligandType in range(1, numMolTypes):
        PA_givenB, PB_givenA  = compute_stericHindrance_perType( T, ligandType )

        print("{}: P(A|B) = {}".format( ligandType, PA_givenB ))
        print("{}: P(B|A) = {}".format( ligandType, PB_givenA ))
        
        f.write("{}: P(A|B) = {}\n".format( ligandType, PA_givenB ))
        f.write("{}: P(B|A) = {}\n".format( ligandType, PB_givenA ))

def computeNumLigs( numMolsPerType ):
    """ numMolsPerType is a list..."""
    numLigs = 0
    for i in range(1, len(numMolsPerType) ):
        numLigs = numLigs + numMolsPerType[i]
    return numLigs

def main():

    numCmdArgs = len(sys.argv)
    print("numCmdArgs: {}".format(numCmdArgs))
    if (numCmdArgs < 6):
        print(USAGE_STR)
        exit(1)

    ## otherwise, numCmdArgs == 6...
    ifname = sys.argv[1]
    ofname = sys.argv[2]
    numMolType = int(sys.argv[3])
    totalNumMols = int(sys.argv[4])

    startIndexList =  []
    for startIdx in sys.argv[5].split(","):
        startIndexList.append( int(startIdx) )

    numMolsPerType = []
    for i in range(1, len(startIndexList)):
        numMols = startIndexList[i] - startIndexList[i-1]
        numMolsPerType.append( numMols )
    numMols = totalNumMols - startIndexList[-1]
    numMolsPerType.append( numMols )
    
    totalNumLigs = computeNumLigs( numMolsPerType )
    totalNumRecs = numMolsPerType[0]

    print( "\tstartIndexList: {}".format( startIndexList ))
    print( "\tnumMolsPerType: {}".format( numMolsPerType ))
    print( "\ttotalNumLigs: {}".format( totalNumLigs ))
    print( "\ttotalNumRecs: {}".format( totalNumRecs ))
    
    
    str_list = read_file(ifname)
    llist_edges = parse_edges_from_str_list( str_list )

    timestep = 0
    f = open(ofname, 'w')
    T = populate_stericHindranceTable( f, llist_edges, totalNumRecs, startIndexList )
    compute_stericHindrance(f, T, numMolType )
    print( "\n[DEBUG] Final Result Table:\n{}\n".format( T ) )
    result = "{}\n".format(T)
    f.write( result )
    f.close()
    
    print( "Done. Wrote to {}".format( ofname ))
    print( "" )
    return

if __name__ == '__main__':
    main()
