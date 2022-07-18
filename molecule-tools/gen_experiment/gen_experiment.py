#!/usr/bin/env python3

import sys
import os

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_carc_run_scripts import GenFileCarcRunScripts
from genf_moleculeDetailsDotT import GenFileMoleculeDetailsDotT
from genf_experimentNameDotEnv import GenFileExperimentNameDotEnv
from genf_experimentNameVDotEnv import GenFileExperimentNameVDotEnv
from genf_experimentNameDotXml import GenFileExperimentNameDotXml
from genf_bindingDefinitionsDotDef import GenFileBindingDefinitionsDotDef
from genf_moleculeTypesDotDef import GenFileMoleculeTypesDotDef


def populate_runDir( p, runDir ):
    """Populates the base directory with CARC run scripts."""
    fname_base = "{}/{}".format(runDir, p.experimentName)
    template_file = "./template_files/carc_run_script.sh.template.header"
    genf = GenFileCarcRunScripts( p )
    genf.write_file( fname_base, template_file )

def populate_runIDDir( p, runIDDir, runID ):
    experimentName = p.experimentName
    tmpl_xml_header = "./template_files/experimentName.xml.template.header"
    tmpl_xml_footer = "./template_files/experimentName.xml.template.footer"
    genf_moleculeDetails = GenFileMoleculeDetailsDotT( p )
    genf_experimentNameDotEnv = GenFileExperimentNameDotEnv( p )
    genf_experimentNameVDotEnv = GenFileExperimentNameVDotEnv( p )
    genf_experimentNameDotXml = GenFileExperimentNameDotXml( p )
    genf_bindingDefinitionsDotDef = GenFileBindingDefinitionsDotDef( p )
    genf_moleculeTypesDotDef = GenFileMoleculeTypesDotDef( p )

    genf_moleculeDetails.write_file( "{}/MoleculeDetails.t".format( runIDDir ))
    genf_experimentNameDotEnv.write_file( "{}/{}_{}.env".format( runIDDir, experimentName, runID ))
    genf_experimentNameVDotEnv.write_file( "{}/{}_{}_v.env".format( runIDDir, experimentName, runID ))
    genf_experimentNameDotXml.write_file( "{}/{}_{}.xml".format( runIDDir, experimentName, runID ),
                                          runID,
                                          tmpl_xml_header,
                                          tmpl_xml_footer )
    genf_bindingDefinitionsDotDef.write_file( "{}/bindingDefinitions.def".format( runIDDir ) )
    genf_moleculeTypesDotDef.write_all_files( runIDDir, "moleculeTypes.{}s.def")  ## note: the s before s.def...

def create_dirStructure( p ):
    """p is an ExperimentParameters object."""
    experimentName = p.experimentName
    runDir = "./Experiment/run-{}/".format( experimentName )
    baseDir = "{}/{}/".format( runDir, experimentName )
    try:
        os.makedirs( baseDir )
    except FileExistsError as e:
        print( "[Warning] directory {} already exists...".format( baseDir ))
    populate_runDir( p, runDir )
        
    numRuns = p.numRuns
    for runID in range(0, numRuns):
        p.seed = runID
        runIDDir = "{}/{}_{}".format( baseDir, experimentName, runID )
        try:
            os.makedirs( runIDDir )
        except FileExistsError as e:
            print( "[Warning] directory {} already exists...".format( runIDDir ))
        populate_runIDDir( p, runIDDir, runID )
    return baseDir

def main():
    if len(sys.argv) < 2:
        print( "[ERROR] cannot run without specifying filename." )
        exit(1)
        
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file( fname )

    #p.print_summary()

    create_dirStructure( p )
    
    return

if __name__ == "__main__":
    main()
