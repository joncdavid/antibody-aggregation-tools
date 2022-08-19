#!/usr/bin/env python3


import sys
import math

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric


class GenFileCarcPkgDataScript( GenFileGeneric ):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def write_file( self, fname_run_base, template_header ):
        foutName = "{}/runCpResultFilesOnly.sh".format(fname_run_base)
        
        fout = open( foutName, "w" )
        fin = open( template_header, "r" )

        s1 = "__TMPL_EXP_NAME__"
        experimentName = self.p.experimentName
        for line in fin:
            line = line.replace( s1, experimentName )
            fout.write( line )

        fin.close()
        fout.close()
