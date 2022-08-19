#!/usr/bin/env python3
# filename: genData_popkinsForChains.py
# author: Jon David
# description:
#   Reads full_bindingsites.data and outputs a 2D csv representing
#   an array where,
#     * each row represents a single timestep for a single run
#     * each column represents a count for number of IgE
#         of class SINGLETON-SIZE-2, SINGLETON-SIZE-3, ..., *-SIZE-6Plus
#     * matrix should bedimension (50000 x 5)
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


USAGE_STR = """

 Usage #1:
   python2 genData_popkinsForChains.py <ifile> <ofname> <molType> <totalMols> <startIndex> <numTimesteps>
 
   where, <ifile> = (string) name of input bindingsite data file,
          <ofname> = (string) name of output report CSV file,
          <molType> = {-1:UNKNOWN, 0:IgE, 1:MB4N},
          <totalMols> = (int) number of molecules of the given type,
          <startIndex> = (int) starting index of molecule ID for the given type
"""

MOLTYPE_UNKNOWN = -1
MOLTYPE_IGE = 0
MOLTYPE_LIGAND = 1

p = re.compile('\(\d+,\d+,\d+\,\d+\)')  ## RE for (mol1,b1,mol2,b2)
p2 = re.compile('\d+')

def getMoleculeType( mol_id, numRecs, numLigs ):
    molType = MOLTYPE_UNKNOWN
    if (mol_id >= 0) and (mol_id < numRecs):
        molType = MOLTYPE_IGE
    elif (numRecs >= numRecs) and (mol_id < (numRecs+numLigs)):
        molType = MOLTYPE_LIGAND
    return molType

def isMoltypeIge( mol_id, numRecs, numLigs ):
    return MOLTYPE_IGE == getMoleculeType( mol_id, numRecs, numLigs )

def isMoltypeMb4n( mol_id, numRecs, numLigs ):
    return MOLTYPE_LIGAND == getMoleculeType( mol_id, numRecs, numLigs )

def isMoltype( moltype, mol_id, numRecs, numLigs ):
    return moltype == getMoleculeType( mol_id, numRecs, numLigs )


class BindingEdge:
    def __init__(self, mol1, bsite1, mol2, bsite2):
        self.mol1 = int(mol1)
        self.bsite1 = int(bsite1)
        self.mol2 = int(mol2)
        self.bsite2 = int(bsite2)

    def __init__(self, s):
        """Constructor given a string representing a tuple (m1,b1,m2,b2)"""
        clean_s = s[1:-1]  ## removes '(' and ')' characters
        result = clean_s.split(',')
        self.mol1 = int(result[0])
        self.bsite1 = int(result[1])
        self.mol2 = int(result[2])
        self.bsite2 = int(result[3])

    def __str__(self):
        s = "({},{},{},{})".format( self.mol1, self.bsite1, self.mol2, self.bsite2 )
        return s

class Graph:
    def __init__(self, llist_edges):
        self.raw_llist_edges = llist_edges
        self.adjDict = {}  ## type: <MoleculeID, [(Mol1,Site1,Mol2,Site2)]

        self.initialize( self.raw_llist_edges )

    def initialize(self, edge_list):
        """llist_edges is a list of list of BindingEdges."""
        for edge in edge_list:    ##   for each BindingEdge
            moleculeID = edge.mol1
            if moleculeID not in self.adjDict.keys():
                self.adjDict[moleculeID] = []
            self.adjDict[moleculeID].append(edge)

    def get_connectedComponents(self):
        """Returns a list of connected components of this graph. Each connected component is a list of moleculeIDs."""
        listOfExploredVertices = deque()
        visitedList = deque()
        listOfCCs = deque()
        for moleculeID in self.adjDict.keys():          ## for each vertex,
            if moleculeID not in listOfExploredVertices:  ##   if moleculeID is not already explored,
                visitedList = deque()
                visitedList = self.bfs( deque([moleculeID]), deque() )
                listOfCCs.append( visitedList )
                listOfExploredVertices.extend( visitedList )
        return listOfCCs
        

    def bfs(self, listOfMoleculesToVisit, visitedList):
        #print("[DEBUG] in bfs...")
        #print("\tlistOfMoleculesToVisit: {}".format( listOfMoleculesToVisit ))
        #print("\tvisitedList: {}".format( visitedList ))
        if not listOfMoleculesToVisit:   ## if list is empty...
            return visitedList
        moleculeID = listOfMoleculesToVisit[0]
        if moleculeID in visitedList:
            listOfMoleculesToVisit.popleft()  #listOfMoleculesToVisit.pop(0)     ## remove first element,
            return self.bfs( listOfMoleculesToVisit, visitedList )
        listOfMoleculesToVisit.popleft()      #listOfMoleculesToVisit.pop(0)
        visitedList.append( moleculeID )      ##  but add that element to the visited list
        listOfEdges = self.adjDict[moleculeID]
        for edge in listOfEdges:
            adjacent_moleculeID = edge.mol2
            if adjacent_moleculeID not in listOfMoleculesToVisit:
                listOfMoleculesToVisit.append( adjacent_moleculeID )
        return self.bfs(listOfMoleculesToVisit, visitedList)
            
    
    def print_me(self):
        print("Graph contents:")
        print( "len(adjDidct.keys()): {}".format( len(self.adjDict.keys()) ))
        for key in self.adjDict.keys():
            print("[{}]: ".format(key), end='')
            listOfEdges = self.adjDict[key]
            for edge in listOfEdges:
                print("{}, ".format(edge), end='')
            print()
## end class Graph


def initialize_histMappingDefault():
    """Initialize default mapping: {'Free':0, 'Singleton':1, 'XmerBase':2}"""
    a = { 'Free':0, 'Singleton':1, 'XmerBase':2 }
    return a

def initialize_histMappingDetailedSingletons( numRecs ):
    """Initialized detailed singletons mapping:
    {'Free':0, 'SingletonA':1, 'SingletonB':2, 'SingletonAB':3, ...}"""
    a = { 'Free':0, 'SingletonA':1, 'SingletonB':2, 'SingletonAB':3}
    xMerBaseIndex = 4
    xMerStartValue = 2
    for i in range(xMerStartValue, numRecs):
        keyStr = "{}mer".format( i )
        a[keyStr] = xMerBaseIndex + i - xMerStartValue
    return a

def which_singleton_type(cc, G, h):
    ##self.adjDict = {}  ## type: <MoleculeID, [(Mol1,Site1,Mol2,Site2)]
    """Assumes cc has exactly one element, a single MoleculeID."""
    #print( "[DEBUG][input] G" )
    #G.print_me()
    #print( "[DEBUG][input] cc: {}".format( cc ) )
    #print( "[DEBUG][input] h: {}".format( h ))
    
    moleculeID = cc[0]
    #print( "[DEBUG] moleculeID: {}".format( moleculeID ))
    singletonType = ""

    numSitesBound = len( G.adjDict[moleculeID] )
    #print( "[DEBUG] numSitesBound: {}".format( numSitesBound ))
    if numSitesBound == 2:
        singletonType = "SingletonAB"
    elif numSitesBound == 1:
        #print( "[DEBUG] G.adjDict[moleculeID], type: {}, {}".format( G.adjDict[moleculeID], type(G.adjDict[moleculeID] )))
        bsite = int( G.adjDict[moleculeID][0].bsite1 )
        if bsite == 0:
            singletonType = "SingletonA"
        elif bsite == 1:
            singletonType = "SingletonB"
    else:
        print("\n\nError. Impossible scenario in which_singleton_type.\n\n")
        exit(-1)
    #print( "[DEBUG] singletonType: {}".format( singletonType ))
    histKey = h[singletonType]
    return histKey

def count_numRecsInCC(connectedComponent, numReceptors, numLigands):
    """Counts the number of receptors in given Connected component.
       A connected component is represented as a list of moleculeIDs."""
    igeCount = 0
    for moleculeID in connectedComponent:
        if isMoltypeIge( moleculeID, numReceptors, numLigands ):
            igeCount = igeCount + 1
    return igeCount

def count_numLigsBoundToIgE( moleculeID_ige, G ):
    """Counts the number of ligands bound directly to IgE with this moleculeID."""
    ligCount = 0
    isSiteABound = False
    isSiteBBound = False

    ## e is a BindingEdge
    for e in G.adjDict[moleculeID_ige]:
        if int(e.bsite1) == 0:
            isSiteABound = True
            ligCount = 1 + ligCount
        elif int(e.bsite1) == 1:
            isSiteBBound = True
            ligCount = 1 + ligCount
    return ligCount, isSiteABound, isSiteBBound

def classify_aggregate( cc, G, numReceptors, numLigands ):
    """Classifies the given cc, a list of , and G, a Graph."""
    numIgE = count_numRecsInCC( cc, numReceptors, numLigands )
    aggregateType = None
    if numIgE >= 2:
        aggregateType = "{}mer".format( numIgE )
    elif numIgE == 1:
        moleculeID_ige = cc[0]
        numLigs, isSiteABound, isSiteBBound = count_numLigsBoundToIgE( moleculeID_ige, G )
        if isSiteABound and isSiteBBound:
            aggregateType = "SingletonAB"
        elif isSiteABound and not isSiteBBound:
            aggregateType = "SingletonA"
        elif not isSiteABound and isSiteBBound:
            aggregateType = "SingletonB"
    return aggregateType
    
def initializeNewHistogram(totalNumReceptors):
    histogram = {}
    histogram["Free"] = totalNumReceptors  ## on init, assume receptors are Free.
    histogram["SingletonA"] = 0
    histogram["SingletonB"] = 0
    histogram["SingletonAB"] = 0
    for i in range(2, totalNumReceptors):
        k = "{}mer".format(i)
        histogram[k] = 0
    return histogram

def histogramToString(histogram, numRecs):
    #s = str( histogram[0] )
    #for i in range(1, numRecs):
    #    s = s + "," + str(histogram[i])
    #s = s + "\n"

    s = str( histogram["Free"] )
    s = s + "," + str( histogram["SingletonA"] )
    s = s + "," + str( histogram["SingletonB"] )
    s = s + "," + str( histogram["SingletonAB"] )
    
    for i in range(2, numRecs ):
        k = "{}mer".format(i)
        s = s + "," + str(histogram[k])
    s = s + "\n"
    return s

def read_file(fname):
    """Reads aggregated binding sites file, and returns a list of strings."""
    str_list = []
    with open(fname) as f:
        for line in f:
            clean_line = line.strip()
            str_list.append( clean_line )
    return str_list

def parse_edges_from_str_list(list_s):
    """Parses a list of strings and returns a list of list of tuples."""
    llist_edges = []  ## a list of list of edges
    for s in list_s:
        edges_list = parse_edges_from_str(s)  ## a list of edges
        llist_edges.append( edges_list )
    return llist_edges

def parse_edges_from_str(s):
    """Parses a string s and returns a list of BindingEdges."""
    list_of_matched_tuples = p.findall(s)  ## list of strings (each element represents a tuple)
    edge_list = []  ## list of BindingEdges
    for s in list_of_matched_tuples:
        edge = BindingEdge(s)
        edge_list.append( edge )
    return edge_list


def main():

    numCmdArgs = len(sys.argv)
    print("numCmdArgs: {}".format(numCmdArgs))
    if (numCmdArgs != 6):
        print(USAGE_STR)
        exit(1)

    ## otherwise, numCmdArgs == 6...
    ifname = sys.argv[1]
    ofname = sys.argv[2]
    molType = int(sys.argv[3])
    totalMols = int(sys.argv[4])
    startIndex = int(sys.argv[5])

    totalNumLigs = totalMols-startIndex
    totalNumRecs = totalMols-totalNumLigs

    #histKeysDict = initialize_histMappingDefault()
    histKeysDict = initialize_histMappingDetailedSingletons( totalNumRecs )
    
    str_list = read_file(ifname)
    llist_edges = parse_edges_from_str_list( str_list )

    timestep = 0
    f = open(ofname, 'w')
    for listOfEdges in llist_edges:
        myG = Graph(listOfEdges)  #Graph(llist_edges)
        #myG.print_me()
        histogram = initializeNewHistogram(totalNumRecs)
        #print( "[DEBUG] new histogram: {}".format( histogramToString(histogram, totalNumRecs) ))
        listOfConnectedComponents = myG.get_connectedComponents()

        #histKeyDict = initialize_histMappingDefault()
        histKeyDict = initialize_histMappingDetailedSingletons( totalNumRecs )
        #print( "[DEBUG] timestep: {}".format( timestep ))
        for cc in listOfConnectedComponents:
            #print( "[DEBUG] cc: {}".format( cc ))
            countNumRecs = count_numRecsInCC(cc, totalNumRecs, totalNumLigs)
            aggregateType = classify_aggregate(cc, myG, totalNumRecs, totalNumLigs )
            #print( "[DEBUG] aggregateType: {}".format( aggregateType ))
            #histKey = histKeyDict[ aggregateType ] 
            if aggregateType not in histogram.keys():
                #print( "[DEBUG] oopsies, aggregateType {} wasn't in histogram.keys() {} ...".format(aggregateType, histogram.keys()) )
                print( "[DEBUG] Warning! Found undefined aggregateType: {}".format( aggregateType ))
                histogram[ aggregateType ] = 0
            #histogram[countNumRecs] = countNumRecs + histogram[countNumRecs]
            histogram[ aggregateType ] = countNumRecs + histogram[aggregateType]
            histogram["Free"] = histogram["Free"] - countNumRecs  ## remove from free.
        f.write( histogramToString(histogram,totalNumRecs) )
        timestep = 1 + timestep
    f.close()
    print( "Done. Wrote to {}".format( ofname ))
    print( "" )
    return

if __name__ == '__main__':
    main()
