#!/usr/bin/env python3

#---------------------------------------------------------------------
# file: genf_bindingDefinitionsDotDef.py
# author: Jon David (jdavid@cs.unm.edu)
# date: June 2022
# description:
#   Responsible for creating the file "bindingDefinitions.def"
#---------------------------------------------------------------------


import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric


class GenFileBindingDefinitionsDotDef(GenFileGeneric):
    def __init__(self, exp_params):
        super().__init__( exp_params )

    def write_file(self, fname):
        numPairs = len(self.p.bindingPairs_set)

        f = open(fname, "w")
        f.write( "{}\n".format( numPairs ) )
        for (moleculeTypeID_A, moleculeTypeID_B) in self.p.bindingPairs_set:
            f.write( "{}\n".format( moleculeTypeID_A) )
            f.write( "{}\n".format( moleculeTypeID_B) )
        f.close()


if __name__ == "__main__":
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileBindingDefinitionsDotDef( p )
    genf.write_file("bindingDefinitions.def")
