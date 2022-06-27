#!/usr/bin/env python3

import unittest

from experiment_parameters import ExperimentParameters

class TestExperimentParameters(unittest.TestCase):

    ## docs.python.org/3/library/unittest_html
    def test_isValid1(self):
        """This test verifies that all of ExperimentParameters are initialized to None"""
        p = ExperimentParameters()
        self.assertEqual( p.experimentName, None )
        self.assertEqual( p.experimentType, None )
        self.assertEqual( p.numRuns, None )
        self.assertEqual( p.seed, None )
        self.assertEqual( p.maxTimesteps, None )
        self.assertEqual( p.minXZ, None )
        self.assertEqual( p.maxXZ, None )
        self.assertEqual( p.listOfMoleculeTypeIDs, None )
        self.assertEqual( p.listOfMoleculeTypes, None )
        self.assertEqual( p.moleculeTypeID_counts_table, None )
        self.assertEqual( p.moleculeTypeID_types_table, None )
        self.assertEqual( p.bindingPairs_set, None )
        self.assertEqual( p.moleculeTypeID_basename_table, None )

    def helper_setup_isValid2(self):
        p = ExperimentParameters()
        p.experimentName = ""  ## String
        p.experimentType = "" ## String :: {single, set}
        p.numRuns = 0 ## UInt
        p.seed = 0 ## UInt
        p.maxTimesteps = 0 ## UInt
        p.minXZ = 0 ## Int
        p.maxXZ = 0 ## Int        
        p.listOfMoleculeTypeIDs = [0,0]  ## [Int]
        p.listOfMoleculeTypes = ""  ## [String:lower]
        p.moleculeTypeID_counts_table = {}  ## f: moleculeTypeID -> UInt
        p.moleculeTypeID_types_table = {}  ## f: moleculeTypeID -> moleculeType (String)
        p.bindingPairs_set = set()  ## a set of (moleculeTypeID,moleculeTypeID) pairs.
        p.moleculeTypeID_basename_table = ""  ## moleculeTypeIDs have a unique basename
        return p
    
    def test_isValid2(self):
        """This test verifies that once all member variables are set, isValid returns True."""
        p = self.helper_setup_isValid2()
        result = p.isValid()
        self.assertEqual( result, True )

    def test_setExperimentName(self):
        p = ExperimentParameters()
        exp_name = "bob"
        p.setExperimentName( exp_name )
        self.assertEqual( p.experimentName, exp_name )

    def test_experimentType(self):
        p = ExperimentParameters()
        exp_type = "my_type"
        p.setExperimentType( exp_type )
        self.assertEqual( p.experimentType, exp_type )

    def test_setNumRuns(self):
        p = ExperimentParameters()
        num_runs = 10
        p.setNumRuns( num_runs )
        self.assertEqual( p.numRuns, num_runs )

    def test_setSeed(self):
        p = ExperimentParameters()
        seed = 0
        p.setSeed( seed )
        self.assertEqual( p.seed, seed )
        
    def test_setMaxTimesteps(self):
        p = ExperimentParameters()
        timesteps = 1000
        p.setMaxTimesteps( timesteps )
        self.assertEqual( p.maxTimesteps, timesteps )

    def test_setMinXZ(self):
        p = ExperimentParameters()
        minXZ = -100
        p.setMinXZ( minXZ )
        self.assertEqual( p.minXZ, minXZ )

    def test_setMaxXZ(self):
        p = ExperimentParameters()
        maxXZ = 100
        p.setMaxXZ( maxXZ )
        self.assertEqual( p.maxXZ, maxXZ )

    def helper_lists_are_equal(self, x, y):
        """Two lists x and y iff for i in range(0,len(x)),
        x_i == y_i."""
        if len(x) != len(y):
            return False
        for i in range(0, len(x)):
            if x[i] != y[i]:
                return False
        return True
    
    def test_addToListOfMoleculeTypeIDs(self):
        p = ExperimentParameters()
        new_moleculeTypeIDs = [1,2,3]
        p.addToListOfMoleculeTypeIDs( new_moleculeTypeIDs )
        result = self.helper_lists_are_equal( p.listOfMoleculeTypeIDs, new_moleculeTypeIDs )
        self.assertEqual( result, True ) ## expected to fail because can't pass empty list

        ## "what about the case where a user passes an empty list?

    def test_addToListOfMoleculeTypes(self):
        p = ExperimentParameters()
        new_types = [1234, 1235, 1236]
        p.addToListOfMoleculeTypes( new_types )
        result = self.helper_lists_are_equal( p.listOfMoleculeTypes, new_types )
        self.assertEqual( result, True )

    def test_updateMoleculeTypeIDCountTable(self):
        p = ExperimentParameters()
        new_pairs_list = [ (50,20), (1234,10), (1235,10) ]
        p.updateMoleculeTypeIDCountTable( new_pairs_list )
        x = list( p.moleculeTypeID_counts_table.items() )
        result = self.helper_lists_are_equal( new_pairs_list, x )
        self.assertEqual( result, True )

    def test_updateMoleculeTypeIDTypesTable(self):
        p = ExperimentParameters()
        new_pairs_list = [ (50,"receptor"), (1234,"ligand"), (1235,"ligand") ]
        p.updateMoleculeTypeIDTypesTable( new_pairs_list )
        x = list( p.moleculeTypeID_types_table.items() )
        result = self.helper_lists_are_equal( new_pairs_list, x )
        self.assertEqual( result, True )

    def test_updateMoleculeBindingPairsSet(self):
        p = ExperimentParameters()
        new_pairs_list = [ (50,1234), (50,1235) ]
        p.updateMoleculeBindingPairsSet( new_pairs_list )
        result = True
        for pair in new_pairs_list:
            if pair not in list( p.bindingPairs_set ):
                result = False
        self.assertEqual( result, True )

    def test_updateMoleculeTypeIDBaseNameTable(self):
        p = ExperimentParameters()
        new_pairs_list = [ (50,"IgE"), (1234,"myo1n1cv4"), (1235,"myo1n1cv5") ]
        p.updateMoleculeTypeIDBaseNameTable( new_pairs_list )
        x = list( p.moleculeTypeID_basename_table.items() )
        result = self.helper_lists_are_equal( new_pairs_list, x )
        self.assertEqual( result, True )

if __name__ == "__main__":
    ## otherwise you'd have to run...
    ## python3 -m unittest test_experiment_parameters.py
    unittest.main()
