#!/usr/bin/env python3

import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric


class GenFileExperimentNameVDotEnv(GenFileGeneric):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def write_file(self, fname):
        totalNumMolecules = self._get_totalNumMolecules()
        
        f = open(fname, "w")

        f.write( "1\n" )
        f.write( "\n" )
        f.write( "MultiBody Active\n" )
        f.write( "{}\n".format( totalNumMolecules ))

        index = 0
        for moleculeTypeID in self.p.listOfMoleculeTypeIDs:
            count = self.p.moleculeTypeID_counts_table[ moleculeTypeID ]
            for i in range(0, count):
                gfname = self._get_GFname( moleculeTypeID )
                f.write( "FreeBody {} {} 0 0 0 0 0 0 \n".format(index, gfname) )
                index = index + 1
        f.write( "Connection\n" )
        f.write( "0\n")
        
        f.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileExperimentNameVDotEnv( p )
    genf.write_file("experimentName_v.env")

