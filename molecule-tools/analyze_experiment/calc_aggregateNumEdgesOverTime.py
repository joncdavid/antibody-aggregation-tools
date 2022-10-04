#!/usr/bin/env python3


import sys
#import re
import csv

import glob
import pandas as pd
import numpy as np

from util_fullBindingSitesParser import *


def aggNumEdgesOverTime( ifnameBase ):
    maxTimesteps = 50001
    numRuns = 100
    M = np.zeros( (maxTimesteps, numRuns) )
    for fname in glob.glob( "**/{}".format( ifnameBase )):
        ## ==== Warning! the order these files are read is no by runID ====
        print( "fname: {}".format( fname ))
        str_list = read_file( fname )
        llist_edges = parse_edges_from_str_list( str_list )

        t = 0
        for listOfEdges in llist_edges:
            numEdges = len( listOfEdges )
            M[t] = numEdges
            t = 1 + t
        break ## remove me after debug.
    return M


def main():
    expName = sys.argv[1]
    ifnameBase = sys.argv[2]
    M = aggNumEdgesOverTime( ifnameBase )

    print( "M: {}".format( M ))

    
if __name__ == "__main__":
    main()
