#!/usr/bin/env python3

import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric

class GenFileMoleculeTypesDotDef(GenFileGeneric):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def write_all_files(self, dir_path, fname_pattern):
        for moleculeType in self.p.listOfMoleculeTypes:
            fname = fname_pattern.format( moleculeType )
            fname_path = "{}/{}".format( dir_path, fname )
            self.write_file( fname_path, moleculeType )
        
    def write_file(self, fname, moleculeType ):
        f = open(fname, "w")
        for moleculeTypeID in self.p.moleculeTypeID_types_table:
            if self.p.moleculeTypeID_types_table[ moleculeTypeID ] == moleculeType:
                f.write( "{}\n".format( moleculeTypeID ))
        f.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileMoleculeTypesDotDef( p )
    genf.write_all_files( ".", "moleculeTypes.{}s.def" )
    
    #for moleculeType in p.listOfMoleculeTypes:
    #    fname = "moleculeType.{}.def".format(moleculeType)
    #    genf.write_file( fname, moleculeType )

