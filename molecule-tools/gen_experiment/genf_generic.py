#!/usr/bin/env python3

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration

class GenFileGeneric(object):
    def __init__(self, exp_params):
        self.p = exp_params
        self.dirLevel = self.p.getDirLevel()

    def _get_num_models(self):
        """Gets the number of molecule models."""
        numMolecules = len( self.p.listOfMoleculeTypeIDs )
        return numMolecules

    def _get_moleculeCount(self, moleculeTypeID):
        """Gets the number of molecules for a given moleculeTypeID."""
        moleculeCount = self.p.moleculeTypeID_counts_table[moleculeTypeID]
        return moleculeCount

    def _get_totalNumMolecules(self):
        """Gets the total number of molecules in this experiment."""
        totalNumMolecules = 0
        for k in self.p.moleculeTypeID_counts_table:
            count = self.p.moleculeTypeID_counts_table[k]
            totalNumMolecules = totalNumMolecules + count
        return totalNumMolecules


    def _get_molef(self, moleculeTypeID):
        """Gets the mole file of a given moleculeTypeID."""
        basename = self.p.moleculeTypeID_basename_table[ moleculeTypeID ]
        path_str = ""
        for i in range(0, self.dirLevel):
            path_str = path_str + "../"
        molef = "{}{}/{}.mole".format(path_str, "DATA", basename)
        return molef


    def _get_GFname(self, moleculeTypeID ):
        """Gets the object g file of a given moleculeTypeID."""
        basename = self.p.moleculeTypeID_basename_table[ moleculeTypeID ]
        data_path = ""
        for i in range(0, self.dirLevel):
            data_path = data_path + "../"
        data_path = data_path + "DATA"
        gfname = "{}/{}.g".format(data_path, basename)
        return gfname
    

    
