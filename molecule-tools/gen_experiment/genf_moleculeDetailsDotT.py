#!/usr/bin/env python3

import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric

class GenFileMoleculeDetailsDotT(GenFileGeneric):
    
    def __init__(self, exp_params):
        super().__init__( exp_params )
    
    def write_file(self, fname):
        """Writes the file fname at location loc."""
        numModels = self._get_num_models()

        f = open(fname, "w")
        f.write( "0.1\n" )
        f.write( "{}\n".format( numModels ) )

        for moleculeTypeID in self.p.listOfMoleculeTypeIDs:
            molef = self._get_molef( moleculeTypeID )
            moleculeCount = self._get_moleculeCount( moleculeTypeID )
            f.write( "{}\n".format( molef ))
            f.write( "{}\n".format( moleculeCount ))
        f.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileMoleculeDetailsDotT( p )
    genf.write_file("MoleculeDetails.t")
