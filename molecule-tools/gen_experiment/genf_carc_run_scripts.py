#!/usr/bin/env python3

#---------------------------------------------------------------------
# file: genf_carc_run_scripts.py
# author: Jon David (jdavid@cs.unm.edu)
# date: June 2022
# description:
#   Responsible for creating the scripts that are submitting to
#   CARC as jobs to be run on their machines.
#---------------------------------------------------------------------


import sys
import math

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric


class GenFileCarcRunScripts(GenFileGeneric):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def _helper_write_header(self, fout, minRunID, maxRunID, template_header):
        fin = open(template_header, "r")

        s1 = "__TMPL_EXP_NAME__"
        s2 = "__TMPL_MINRUN__"
        s3 = "__TMPL_MAXRUN__"

        experimentName = self.p.experimentName
        for line in fin:
            line = line.replace( s1, experimentName)
            line = line.replace( s2, str(minRunID) )
            line = line.replace( s3, str(maxRunID) )
            fout.write( line )
        fin.close()

    def _helper_write_body( self, f, minRunID, maxRunID ):
        for runID in range(minRunID, maxRunID):
            f.write( "\n" )
            f.write( "cd $PBS_O_WORKDIR\n" )
            f.write( "pwd\n" )
            f.write( "experiment{}_dir=$(echo ${{basedir}}_{})\n".format( runID, runID ))
            f.write( "echo \"experiment{}_dir: \" $experiment{}_dir\n".format( runID, runID ))
            f.write( "cd $experiment{}_dir\n".format( runID ) )
            f.write( "pwd\n" )
            f.write( "echo \"Running experiment {}...\"\n".format( runID ))
            f.write( "$exe -f ${{projname}}_{}.xml > output.txt &\n".format( runID ))
            f.write( "echo\n" )

    def _helper_write_footer( self, f ):
        f.write ( "\n" )
        f.write( "\necho \"Waiting for all experiments to terminate...\" \n" )
        f.write( "wait\n" )
        f.write( "echo \"Done.\" \n\n" )

    def _helper_write_file(self, fname, minRunID, maxRunID, template_header ):
        f = open(fname, "w")
        self._helper_write_header( f, minRunID, maxRunID, template_header )
        self._helper_write_body( f, minRunID, maxRunID )
        self._helper_write_footer( f )
        f.close()
        
    def write_file(self, fname_base, template_header):
        numRuns = self.p.numRuns
        maxProcessesPerNode = 15
        numGroups = math.ceil( numRuns / maxProcessesPerNode )

        for groupID in range(0, numGroups):
            fname = "{}_{}.sh".format(fname_base, groupID)
            minRunID = groupID * maxProcessesPerNode
            maxRunID = min( numRuns, minRunID + maxProcessesPerNode )
            self._helper_write_file( fname, minRunID, maxRunID, template_header )
        return
    
if __name__ == "__main__":
    fname = sys.argv[1]
    template_file = sys.argv[2]
    
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)
    fname_base = p.experimentName
    genf = GenFileCarcRunScripts( p )
    genf.write_file( fname_base, template_file )

