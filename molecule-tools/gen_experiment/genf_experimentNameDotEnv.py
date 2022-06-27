#!/usr/bin/env python3

import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric

# experimentName.env

STR_ENVIRONMENT_VERSION = "20130201"

class GenFileExperimentNameDotEnv(GenFileGeneric):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def _helper_write_quadLine( self, f, moleculeTypeID ):
        """Assumes f is already open."""
        gfname = self._get_GFname( moleculeTypeID )
        
        f.write( "MultiBody Active\n" )
        f.write( "1\n" )
        f.write( "FreeBody 0 {} 0 0 0 0 0 0 Connection\n".format( gfname ) )
        f.write( "0\n" )
        
    def write_file(self, fname):
        totalNumMolecules = self._get_totalNumMolecules()

        f = open(fname, "w")
        f.write( "# Environment Version {}\n".format(STR_ENVIRONMENT_VERSION) )
        f.write( "{}\n".format(totalNumMolecules) )

        for moleculeTypeID in self.p.listOfMoleculeTypeIDs:
            numMolecules = self.p.moleculeTypeID_counts_table[ moleculeTypeID ]
            for i in range(0, numMolecules):
                f.write( "\n" )
                self._helper_write_quadLine(f, moleculeTypeID )
        f.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileExperimentNameDotEnv( p )
    genf.write_file("experimentName.env")
