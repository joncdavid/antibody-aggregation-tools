#!/usr/bin/env python3
# file: bindingSitesDataReader.py
# author: Jon David
# date: Monday, September 7, 2020
# description:
#   Reads binding site data, stores it a a set of graphs, one for
#   each time step,t : G_t = (V_t, E_t, where V is a set of vertices
#   and E is a set of edges.
#--------------------------------------------------------------------
# input format (full_bindingsites.data):
#   Each line has the following format...
#
#   MOL_ID ::= integer representing molecule ID
#   SITE_ID ::= integer representing binding site ID
#
#   BOUND_PAIR ::= (MOL_ID.SITE_ID, MOL_ID.SITE_ID)
#   BOUND_PAIR_LIST ::= BOUND_PAIR
#   BOUND_PAIR_LIST ::= BOUND_PAIR, BOUND_PAIR_LIST
#   AGGREGATE ::= [BOUND_PAIR_LIST]
#   AGGREGATE_LIST ::= AGGREGATE
#   AGGREGATE_LIST ::= AGGREGATE, AGGREGATE_LIST
#   LINE = AGGREGATE_LIST
#--------------------------------------------------------------------
# input example:
#   [(0.1,20.4), (1.2,20.3)], [(4.1, 21.4)]
#   [(0.1,20.4), (1.2,20.3), (2.1, 20.2)], [(4.1, 21.4)]
#--------------------------------------------------------------------
# usage:
#  bindingSitesDataReader.py <ifname> <ofname>
#
#  where,
#    <ifname> :: filename of input binding sites data file
#    <ofname> :: filename of output file
# 
#--------------------------------------------------------------------

import sys
import re

USAGE = """
usage:
 bindingSitesDataReader.py <ifname> <ofname>

 where,
   <ifname> :: filename of input binding sites data file
   <ofname> :: filename of output file
"""

def run_all_ut():
    run_ut_series_parseGraphFromStr()

def run_ut_series_parseGraphFromStr():
    ut_parseGraphFromStr( "[(0.1,20.4)],[(4.1,21.4)]",
                          [0,20,4,21],
                          [(0,20,1,4),(4,21,1,4)])

    ut_parseGraphFromStr( "[(0.1,20.4),(1.2,20.3)],[(4.1,21.4)]",
                          [0,20,1,4,21],
                          [(0,20,1,4),(1,20,2,3),(4,21,1,4)])

    return

def ut_parseGraphFromStr(inputLine, expectedVertices, expectedEdges):
    """Tests parseGraphFromStr; returns true is pass, false is fail."""
    (V,E) = parseGraphFromStr(inputLine)
    actual_Vset = set(V)
    actual_Eset = set(E)
    expected_Vset = set(expectedVertices)
    expected_Eset = set(expectedEdges)

    criteria1 = actual_Vset == expected_Vset
    criteria2 = actual_Eset == expected_Eset
    result = criteria1 and criteria2

    print("\nRunning unit test on parseGraphFromStr(line)... [Pass={}]".format(result))
    print(" line: {}".format(inputLine))
    print(" expectedVertices: {}".format(expectedVertices))
    print(" expectedEdges: {}".format(expectedEdges))
    print(" actualVertices: {}".format(V))
    print(" actualEdges: {}".format(E))
    print(" result: {}".format(result))
    return result


def parseGraphFromStr(line):
    """generate a graph G=(V,E) from a single line"""
    V = []
    E = []

    re_boundPair = "\(\d+\.\d+,\d+\.\d+\)"
    #re_specific = r'(?P<mol1>\d+).(?P<site1>\d+),(?<mol2>\d+).(?<site2>\d+)'

    listOfBoundPairs = re.findall(re_boundPair, line)   ## list of strings '(m1.b1,m2.b2)', ...
    for boundPairStr in listOfBoundPairs:
        numbers = re.findall("\d+", boundPairStr)
        mol1 = int(numbers[0])
        site1 = int(numbers[1])
        mol2 = int(numbers[2])
        site2 = int(numbers[3])
        E.append( (mol1,mol2,site1,site2) )
        V.append( mol1 )
        V.append( mol2 )
    return (V,E)

def readBindingSitesData(fname):
    """For each line in fname, generate a graph G=(V,E)."""
    graphList = []
    with open(fname) as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            (V,E) = parseGraphFromStr(l)
            graphList.append( (V,E) )
    return graphList

def writeBindingSitesDataAsGraphs(ofname, graphList):
    """Writes to file ofname, graph representation of binding site data."""
    with open(ofname,'w') as f:
        for G in graphList:
            E = G[1]
            for e in E:
                f.write("{},".format(e))
            f.write("\n")
    print("wrote to: {}".format(ofname))
    return


def main():
    if (len(sys.argv) <= 1):
        print(USAGE)
        exit(0)
        
    if (len(sys.argv) == 2) and (sys.argv[1]=='ut'):
        print('i have been modified.')
        run_all_ut()
        exit(0)

    if len(sys.argv) < 3:
        print(USAGE)
        exit(1)

    ifname = sys.argv[1]
    ofname = sys.argv[2]

    print("(input) ifname: {}".format(ifname))
    print("(input) ofname: {}".format(ofname))
    graphList = readBindingSitesData(ifname)
    writeBindingSitesDataAsGraphs(ofname, graphList)
    return

if __name__ == "__main__":
    main()
