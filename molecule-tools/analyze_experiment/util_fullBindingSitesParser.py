#!/usr/bin/env python3


import re

from collections import deque


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

## end of class BindingEdge


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



