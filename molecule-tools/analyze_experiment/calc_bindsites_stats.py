#!/usr/bin/env python
# filename: calc_bindsites_stats.py
# author: Jon David
# description:
#   Calculates binding site statistics on aggregated binding sites data.
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



USAGE_STR = """

 Usage #1:
   python2 calc_bindsites_stats.py <ifile> <ofname> <molType> <totalMols> <startIndex>
 
   where, <ifile> = (string) name of input bindingsite data file,
          <ofname> = (string) name of output report CSV file,
          <molType> = {-1:UNKNOWN, 0:IgE, 1:MB4N},
          <totalMols> = (int) number of molecules of the given type,
          <startIndex> = (int) starting index of molecule ID for the given type

 Usage #2:
   python2 calc_bindsites_stats.py <report-file>

   where, <report-file> is the report file produced in USAGE 1.


"""

MOLTYPE_UNKNOWN = -1
MOLTYPE_IGE = 0
MOLTYPE_MB4N = 1

p = re.compile('\(\d+,\d+,\d+\,\d+\)')  ## RE for (mol1,b1,mol2,b2)
p2 = re.compile('\d+')

def getMoleculeType( mol_id ):
    molType = MOLTYPE_UNKNOWN
    if (mol_id >= 0) and (mol_id <= 19):
        molType = MOLTYPE_IGE
    elif (mol_id >= 20) and (mol_id <= 39):
        molType = MOLTYPE_MB4N
    return molType

def isMoltypeIge( mol_id ):
    return MOLTYPE_IGE == getMoleculeType( mol_id )

def isMoltypeMb4n( mol_id ):
    return MOLTYPE_MB4N == getMoleculeType( mol_id )

def isMoltype( moltype, mol_id ):
    return moltype == getMoleculeType( mol_id )


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


class SingleStateCountReport2Valency:
    """A report for a single state (i.e. a single list of edges)."""
    def __init__(self, molType, totalMolsOfType, moltypeStartIndex, lEdges):
        self.c0,tbl = count_singleSiteBound(0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c1,tbl = count_singleSiteBound(1, molType, totalMolsOfType, moltypeStartIndex, lEdges)


        ##---- size of sets where binding site x and 0 are bound.
        self.c10,tbl = count_twoSitesBound(1, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        ##---- size of sets where binding site x and 1 are bound.
        self.c01,tbl = count_twoSitesBound(0, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)

    def __str__(self):
        s = "{}, {}, {}, {}\n".format(self.c0, self.c1,
                                      self.c10,
                                      self.c01)
        return s
## end of class SingleStateCountReport2Valency


class SingleStateProbabiliesReport2Valency:
    """a report for a single state (a single list of edges."""
    def __init__(self, molType, totalMolsOfType, moltypeStartIndex, lEdges):
        ## probabilities that binding sites 0..1 are bound
        self.p0 = q_probSingleSiteBound(0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p1 = q_probSingleSiteBound(1, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p1_0 = q_probSiteXIsBoundGivenSiteYIsBound(1, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p0_1 = q_probSiteXIsBoundGivenSiteYIsBound(0, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)

    def __str__(self):
        s = "{}, {}, {}, {}\n".format(self.p0, self.p1,
                                      self.p1_0, 
                                      self.p0_1)
        return s
## end of class SingleStateProbabilitiesReport2Valency






class SingleStateCountReport4Valency:
    """A report for a single state (i.e. a single list of edges)."""
    def __init__(self, molType, totalMolsOfType, moltypeStartIndex, lEdges):
        self.c0,tbl = count_singleSiteBound(0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c1,tbl = count_singleSiteBound(1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c2,tbl = count_singleSiteBound(2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c3,tbl = count_singleSiteBound(3, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        ##---- size of sets where binding site x and 0 are bound.
        self.c10,tbl = count_twoSitesBound(1, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c20,tbl = count_twoSitesBound(2, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c30,tbl = count_twoSitesBound(3, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        ##---- size of sets where binding site x and 1 are bound.
        self.c01,tbl = count_twoSitesBound(0, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c21,tbl = count_twoSitesBound(2, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c31,tbl = count_twoSitesBound(3, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        ##---- size of sets where binding site x and 2 are bound.
        self.c02,tbl = count_twoSitesBound(0, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c12,tbl = count_twoSitesBound(1, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c32,tbl = count_twoSitesBound(3, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        ##---- size of sets where binding site x and 3 are bound.
        self.c03,tbl = count_twoSitesBound(0, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c13,tbl = count_twoSitesBound(1, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.c23,tbl = count_twoSitesBound(2, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)

    def __str__(self):
        s = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(self.c0, self.c1, self.c2, self.c3,
                                                                                    self.c10, self.c20, self.c30,
                                                                                    self.c01, self.c21, self.c31,
                                                                                    self.c02, self.c12, self.c32,
                                                                                    self.c03, self.c13, self.c23)
        return s
## end of class SingleStateCountReport4Valency


class SingleStateProbabiliesReport4Valency:
    """a report for a single state (a single list of edges."""
    def __init__(self, molType, totalMolsOfType, moltypeStartIndex, lEdges):
        ## probabilities that binding sites 0..1 are bound
        self.p0 = q_probSingleSiteBound(0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p1 = q_probSingleSiteBound(1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p2 = q_probSingleSiteBound(2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p3 = q_probSingleSiteBound(3, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p1_0 = q_probSiteXIsBoundGivenSiteYIsBound(1, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p2_0 = q_probSiteXIsBoundGivenSiteYIsBound(2, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p3_0 = q_probSiteXIsBoundGivenSiteYIsBound(3, 0, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p0_1 = q_probSiteXIsBoundGivenSiteYIsBound(0, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p2_1 = q_probSiteXIsBoundGivenSiteYIsBound(2, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p3_1 = q_probSiteXIsBoundGivenSiteYIsBound(3, 1, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p0_2 = q_probSiteXIsBoundGivenSiteYIsBound(0, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p1_2 = q_probSiteXIsBoundGivenSiteYIsBound(1, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p3_2 = q_probSiteXIsBoundGivenSiteYIsBound(3, 2, molType, totalMolsOfType, moltypeStartIndex, lEdges)

        self.p0_3 = q_probSiteXIsBoundGivenSiteYIsBound(0, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p1_3 = q_probSiteXIsBoundGivenSiteYIsBound(1, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)
        self.p2_3 = q_probSiteXIsBoundGivenSiteYIsBound(2, 3, molType, totalMolsOfType, moltypeStartIndex, lEdges)

    def __str__(self):
        s = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(self.p0, self.p1, self.p2, self.p3,
                                                                                    self.p1_0, self.p2_0, self.p3_0,
                                                                                    self.p0_1, self.p2_1, self.p3_1,
                                                                                    self.p0_2, self.p1_2, self.p3_2,
                                                                                    self.p0_3, self.p1_3, self.p2_3)
        return s
## end of class SingleStateProbabilitiesReport4Valency


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

def q_probSingleSiteBound(bsite_id, molType, totalMolsOfType, moltypeStartIndex, lEdges):
    """query: given a single graph, what is the probability that binding site bsite_id is bound?"""
    count, tbl = count_singleSiteBound(bsite_id, molType, totalMolsOfType, moltypeStartIndex, lEdges)
    return float(count)/totalMolsOfType

def q_probSiteXIsBoundGivenSiteYIsBound(bsiteX_id, bsiteY_id, molType, totalMolsOfType, moltypeStartIndex, lEdges):
    """
    query: what is the probability that binding site X is bound, given binding site Y is bound?
    solution: P(Li|Lj) = |Lij| / |Lj|,
    where Li is the set of ligands whose ith binding site is bound,
    Lj is the set of ligands whose jth binding site is bound,
    and Lij is the set of ligands whose ith and jth binding site are bound.
    """
    count_siteXY_bothBound, XYboundSitesTable = count_twoSitesBound(bsiteX_id, bsiteY_id, molType, totalMolsOfType, moltypeStartIndex, lEdges)
    count_singleYSiteBound, tbl = count_singleSiteBound(bsiteY_id, molType, totalMolsOfType, moltypeStartIndex, lEdges)
    prob = 0.0
    if count_singleYSiteBound > 0:
        prob = float(count_siteXY_bothBound) / count_singleYSiteBound
    return prob


def count_singleSiteBound(bsite_id, molType, totalMolsOfType, moltypeStartIndex, lEdges):
    """count the number of molecules of type moltype {}
    where binding site bsite_id is bound
    in the list of BindingEdges, lEdges"""
    #count = 0
    #for bindingEdge in lEdges:
    #    if ( isMoltype(molType, bindingEdge.mol1) and
    #        (bindingEdge.bsite1 == bsite_id) ):
    #        count = 1 + count
    #    elif ( isMoltype( molType, bindingEdge.mol2 ) and
    #              (bindingEdge.bsite2 == bsite_id) ):
    #        count = 1 + count
    #actualCount = count/2  ## because edges show up in pairs (a single edge is single-direction; one for each direction)
    #return count

    # (step 1) construct table: boundSitesTable<mol_id, [boundSite_id]>
    boundSitesTable = {}
    for i in range(0, totalMolsOfType):
        index = i + moltypeStartIndex
        boundSitesTable[index] = []
    for bindingEdge in lEdges:
        fmol1_id = bindingEdge.mol1
        fmol2_id = bindingEdge.mol2
        fbsite1_id = bindingEdge.bsite1
        fbsite2_id = bindingEdge.bsite2
        fmol1IsCorrectType = isMoltype(molType, fmol1_id)
        fmol2IsCorrectType = isMoltype(molType, fmol2_id)
        if fmol1IsCorrectType:
            boundSitesTable[fmol1_id].append(fbsite1_id)
        elif fmol2IsCorrectType:
            boundSitesTable[fmol2_id].append(fbsite2_id)

    # (step 2) iterate through table counting instances
    # where boundSite list contains both bsite1 and bsite2
    count = 0
    for key_molID in boundSitesTable:
        boundSitesList = boundSitesTable[key_molID]
        if bsite_id in boundSitesList:
            count = 1 + count
    return count, boundSitesTable

def count_twoSitesBound(bsite1_id, bsite2_id, molType, maxNumMolsOfType, moltypeStartIndex, lEdges):
    """Count the number of molecules of type moltype {}
    where binding sites bsite1_id and bsite2_id are bound in the same molecule
    in the list of BindingEdges, lEdges."""
    # (step 1) construct table: boundSitesTable<mol_id, [boundSite_id]>
    boundSitesTable = {}
    for i in range(0, maxNumMolsOfType):
        index = i + moltypeStartIndex
        boundSitesTable[index] = []
    for bindingEdge in lEdges:
        fmol1_id = bindingEdge.mol1
        fmol2_id = bindingEdge.mol2
        fbsite1_id = bindingEdge.bsite1
        fbsite2_id = bindingEdge.bsite2
        fmol1IsCorrectType = isMoltype(molType, fmol1_id)
        fmol2IsCorrectType = isMoltype(molType, fmol2_id)
        if fmol1IsCorrectType:
            boundSitesTable[fmol1_id].append(fbsite1_id)
        elif fmol2IsCorrectType:
            boundSitesTable[fmol2_id].append(fbsite2_id)

    # (step 2) iterate through table counting instances
    # where boundSite list contains both bsite1 and bsite2
    count = 0
    for key_molID in boundSitesTable:
        boundSitesList = boundSitesTable[key_molID]
        if (bsite1_id in boundSitesList) and (bsite2_id in boundSitesList):
            count = 1 + count
    return count, boundSitesTable

def calculateProbabilitiesFromCountReport(fname):
    ## why can't i import numpy?
    ## so, maybe i'll just finish the analysis using Matlab
    print(" ERROR: numpy not installed? just use Matlab on {}".format(fname) )
    return
        

def main():
    numCmdArgs = len(sys.argv)
    print("numCmdArgs: {}".format(numCmdArgs))
    if (numCmdArgs != 6) and (numCmdArgs != 2):
        print(USAGE_STR)
        exit(1)

    if numCmdArgs == 2:
        countReportFName = sys.argv[1]
        calculateProbabilitiesFromCountReport(countReportFName)
        return 0

    ## otherwise, numCmdArgs == 6...
    ifname = sys.argv[1]
    ofname = sys.argv[2]
    molType = int(sys.argv[3])
    totalMolsOfType = int(sys.argv[4])
    moltypeStartIndex = int(sys.argv[5])

    print( "" )
    print( "Running script: calc_bindingsites_stats.py ...")
    print( "\tinput(ifname): {}".format( ifname ) )
    print( "\tinput(ofname): {}".format( ofname ) )
    print( "\tinput(molType): {}".format( molType ) )
    print( "\tinput(totalMolsOfType): {}".format( totalMolsOfType ) )
    print( "\tintput(moltypeStartIndex): {}".format( moltypeStartIndex ) )
    print( "" )
    str_list = read_file(ifname)
    llist_edges = parse_edges_from_str_list( str_list )

    gen_finalReport(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, llist_edges)
    print( "Generated report: {}".format( ofname ) )
    print( "Done." )
    print( "" )

    #print(" str_list:")
    #print( str_list )
    #print(" llist_edges: ")
    #for list_edges in llist_edges:
    #    for edge in list_edges:
    #        print("{},".format(edge)),
    #    print("")
    return 0


def gen_finalReport(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, listOfListOfBindingEdges):
    gen_finalReport2Valency(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, listOfListOfBindingEdges)
    #gen_finalReport4Valency(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, listOfListOfBindingEdges)


def gen_finalReport2Valency(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, listOfListOfBindingEdges):
    str_list = read_file(ifname)  ## each string is a representation of final state for runs 0..99
    llist_edges = parse_edges_from_str_list( str_list )  ## list of list of BindingEdges
    with open(ofname, 'w') as f:
        for bindingEdgesList in listOfListOfBindingEdges:
            #singleReport = SingleStateProbabilitiesReport4Valency( molType, totalMolsOfType, moltypeStartIndex, bindingEdgesList)
            singleReport = SingleStateCountReport2Valency( molType, totalMolsOfType, moltypeStartIndex, bindingEdgesList)
            f.write( str(singleReport) )

def gen_finalReport4Valency(ifname, ofname, molType, totalMolsOfType, moltypeStartIndex, listOfListOfBindingEdges):
    str_list = read_file(ifname)  ## each string is a representation of final state for runs 0..99
    llist_edges = parse_edges_from_str_list( str_list )  ## list of list of BindingEdges
    with open(ofname, 'w') as f:
        for bindingEdgesList in listOfListOfBindingEdges:
            #singleReport = SingleStateProbabilitiesReport4Valency( molType, totalMolsOfType, moltypeStartIndex, bindingEdgesList)
            singleReport = SingleStateCountReport4Valency( molType, totalMolsOfType, moltypeStartIndex, bindingEdgesList)
            f.write( str(singleReport) )

def ut_read_file():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    print( str_list )

def ut_class_bindingedge():
    b = BindingEdge("(1,2,3,4)")
    print(b)

def ut_parse_edges_from_str():
    print("[Unit Test]: ut_parse_edges_from_str()...")
    s = "(1,1,2,2),(3,3,4,4)"
    print( "input s: {}".format(s) )
    print( "output: ")
    list_of_bindingedges = parse_edges_from_str(s)
    for bindingEdge in list_of_bindingedges:
        print( bindingEdge )

def ut_parse_edges_from_str_list():
    s_list = []
    s_list.append("(1,1,2,2),(3,3,4,4)")
    s_list.append("(5,5,6,6),(7,7,8,8),(9,9,10,10)")

    print("input s_list:")
    print( s_list )

    llist_edges = parse_edges_from_str_list(s_list)
    print("Output (a list of list of BindingEdges):")
    for list_of_edges in llist_edges:
        for edge in list_of_edges:
            print("{},".format(edge)),
        print('')

def ut_getMoleculeType():
    mol1 = 19
    mol2 = 20
    mol1Type = getMoleculeType( mol1 )
    mol2Type = getMoleculeType( mol2 )
    result = (mol1Type == MOLTYPE_IGE) and (mol2Type == MOLTYPE_MB4N)
    print( "unit test: ut_getMoleculeType()..." )
    print( "mol1: {}".format(mol1) )
    print( "mol2: {}".format(mol2) )
    print( "mol1Type: {}".format(mol1Type) )
    print( "mol2Type: {}".format(mol2Type) )
    print( "ut passed: {}".format(result) )

def ut_isMoltypeIge():
    mol_id = 19
    actualResult = isMoltypeIge( mol_id )
    expectedResult = True
    print( "unit test: ut_isMoltypeIge()..." )
    print( "mol_id: {}".format( mol_id ) )
    print( "actualResult: {}".format( actualResult ) )
    print( "expectedResult: {}".format( expectedResult ) )


def ut_isMoltypeMb4n():
    mol_id = 20
    actualResult = isMoltypeMb4n( mol_id )
    expectedResult = True
    print( "unit test: ut_isMoltypeMb4n()..." )
    print( "mol_id: {}".format( mol_id ) )
    print( "actualResult: {}".format( actualResult ) )
    print( "expectedResult: {}".format( expectedResult ) )

def ut_isMoltype():
    mol_id1 = 20
    moltype1 = MOLTYPE_MB4N
    actualResult1 = isMoltype( moltype1, mol_id1 )
    expectedResult1 = True

    mol_id2 = 19
    moltype2 = MOLTYPE_IGE
    actualResult2 = isMoltype( moltype2, mol_id2 )
    expectedResult2 = True

    print( "unit test: ut_isMoltype()..." )
    print( "mol_id1: {}".format( mol_id1 ) )
    print( "moltype1: {}".format( moltype1 ) )
    print( "actualResult1: {}".format( actualResult1 ) )
    print( "expectedResult1: {}".format( expectedResult1 ) )

    print( "mol_id2: {}".format( mol_id2 ) )
    print( "moltype2: {}".format( moltype2 ) )
    print( "actualResult2: {}".format( actualResult2 ) )
    print( "expectedResult2: {}".format( expectedResult2 ) )


def ut_count_totalNumOfSingleType():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    totalCountMb4n = count_totalNumOfSingleType(molType, lEdges)

    print( "unit test: ut_count_totalNumOfSingleType():..." )
    print( "BindingEdges: " )
    for edge in lEdges:
        print( edge ),
    print()
    print( "molType: {}".format( molType ) )
    print( "totalCountMb4n: {}".format( totalCountMb4n ) )


def ut_count_singleSiteBound():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    bsite_id = 0  ## binding site 0, of mb4n molecules
    count_b0 = count_singleSiteBound(bsite_id, molType, lEdges)

    print( "unit test: ut_count_singleSiteBound():..." )
    print( "BindingEdges: " )
    for edge in lEdges:
        print( edge ),
    print()
    print( "molType: {}".format( molType ) )
    print( "bsite_id: {}".format( bsite_id ) )
    print( "count_b0: {}".format( count_b0 ) )


def ut_count_twoSitesBound():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    bsite1_id = 1  ## binding site 0, of mb4n molecules
    bsite2_id = 2  ## binding site 1, of mb4n molecules
    maxNumMolsOfType = 5
    startIndex = 20
    count_b1_b2, boundSitesTable = count_twoSitesBound(bsite1_id, bsite2_id, molType, maxNumMolsOfType, startIndex, lEdges)

    print( "unit test: ut_count_twoSitesBound():..." )
    print( "BindingEdges: " )
    for edge in lEdges:
        print( edge ),
    print()
    print( "molType: {}".format( molType ) )
    print( "bsite1_id: {}".format( bsite1_id ) )
    print( "bsite2_id: {}".format( bsite2_id ) )
    print( "maxNumMolsOfType: {}".format( maxNumMolsOfType ) )
    print( "startIndex: {}".format( startIndex ) )
    print( "boundSitesTable: ")
    for key in boundSitesTable:
        print( "boundSitesTable[{}]: {}".format( key, boundSitesTable[key] ) )
    print( "count_b1_b2: {}".format( count_b1_b2 ) )


def ut_q_probSingleSiteBound():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    bsite_id = 0  ## binding site 0, of mb4n molecules
    totalMolsOfType = 5   ## total number of mb4n molecules
    prob = q_probSingleSiteBound(bsite_id, molType, totalMolsOfType, lEdges)

    print( "unit test: ut_q_probSingleSiteBound():..." )
    print( "BindingEdges: " )
    for edge in lEdges:
        print( edge ),
    print()
    print( "molType: {}".format( molType ) )
    print( "bsite_id: {}".format( bsite_id ) )
    print( "totalNumMolsOfType: {}".format( totalMolsOfType ) )
    print( "prob: {}".format( prob ) )


def ut_q_probSiteXIsBoundGivenSiteYIsBound():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    bsiteX_id = 1  ## binding site 0, of mb4n molecules
    bsiteY_id = 2  ## binding site 1, of mb4n molecules
    totalMolsOfType = 5
    startIndex = 20
    prob = q_probSiteXIsBoundGivenSiteYIsBound(bsiteX_id, bsiteY_id, molType, totalMolsOfType, startIndex, lEdges)

    print( "unit test: ut_q_probSiteXIsBoundGivenSiteYIsBound():..." )
    print( "BindingEdges: " )
    for edge in lEdges:
        print( edge ),
    print()
    print( "molType: {}".format( molType ) )
    print( "bsiteX_id: {}".format( bsiteX_id ) )
    print( "bsiteY_id: {}".format( bsiteY_id ) )
    print( "totalMolsOfType: {}".format( totalMolsOfType ) )
    print( "startIndex: {}".format( startIndex ) )
    print( "prob: {}".format( prob ) )

def ut_SingleStateProbabilitiesReport4Valency():
    fname = 'zztemp.bindingsite.data.aggregate.small'
    str_list = read_file(fname)
    llist_edges = parse_edges_from_str_list(str_list)
    lEdges = llist_edges[-1]
    molType = MOLTYPE_MB4N
    bsiteX_id = 1  ## binding site 0, of mb4n molecules
    bsiteY_id = 2  ## binding site 1, of mb4n molecules
    totalMolsOfType = 5
    startIndex = 20
    singleStateReport = SingleStateProbabilitiesReport4Valency(molType, totalMolsOfType, startIndex, lEdges)
    print( "unit test: ut_q_probSiteXIsBoundGivenSiteYIsBound():..." )
    print( singleStateReport )

if __name__ == '__main__':
    main()
    #ut_read_file()                  ## passed
    #ut_class_bindingedge()          ## passed
    #ut_parse_edges_from_str()       ## passed
    #ut_parse_edges_from_str_list()  ## passed
    #ut_getMoleculeType() ## passed
    #ut_isMoltypeIge()  ## passed
    #ut_isMoltypeMb4n() ## passed
    #ut_isMoltype()  ## passed
    #ut_count_singleSiteBound()  ## passed
    #ut_count_twoSitesBound()  ## passed
    #ut_q_probSingleSiteBound()  ## passed
    #ut_q_probSiteXIsBoundGivenSiteYIsBound()  ## passed
    #ut_SingleStateProbabilitiesReport4Valency()  ## passed
