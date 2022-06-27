import unittest

from experiment_declaration import *
from experiment_declaration import Command
from experiment_parameters import ExperimentParameters


class TestExperimentDeclaration(unittest.TestCase):
    
    def test_cmd_declareExperimentName(self):
        cmd_str = "declare-experiment-name"
        exp_name = "my100MultiSet"
        arg_str_list = [ exp_name ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( p.experimentName, exp_name )

    def test_cmd_declareExperimentType(self):
        cmd_str = "declare-experiment-type"
        exp_type = "set"
        arg_str_list = [ exp_type ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( p.experimentType, exp_type )

    def test_cmd_declareNumRuns(self):
        cmd_str = "declare-num-runs"
        numRuns = 100
        arg_str_list = [ str(numRuns) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True)
        self.assertEqual( p.numRuns, numRuns )
        return

    def test_cmd_declareSeed(self):
        cmd_str = "declare-seed"
        seed = 0
        arg_str_list = [ str(seed) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p)

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True)
        self.assertEqual( p.seed, seed )

    def test_cmd_declareMaxTimesteps(self):
        cmd_str = "declare-max-timesteps"
        maxTimesteps = 500000
        arg_str_list = [ str(maxTimesteps) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )
        
        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( p.maxTimesteps, maxTimesteps )

    def test_cmd_declareMinXz(self):
        cmd_str = "declare-min-xz"
        minXZ = -100
        arg_str_list = [ str(minXZ) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( p.minXZ, minXZ )

    def test_cmd_declareMaxXz(self):
        cmd_str = "declare-max-xz"
        maxXZ = 100
        arg_str_list = [ str(maxXZ) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( p.maxXZ, maxXZ )

    def test_cmd_declareMoleculeTypeIDList(self):
        cmd_str = "declare-moleculeTypeID-list"
        moleculeTypeID_A = 50
        moleculeTypeID_B = 1234
        moleculeTypeID_C = 1235
        
        arg_str_list = [ str(moleculeTypeID_A), str(moleculeTypeID_B), str(moleculeTypeID_C) ]
        c = Command( cmd_str, arg_str_list )
        cmd_is_valid = c.cmd_str_is_valid()
        p = ExperimentParameters()
        handleCommand( c, p )

        resultA = moleculeTypeID_A in p.listOfMoleculeTypeIDs
        resultB = moleculeTypeID_B in p.listOfMoleculeTypeIDs
        resultC = moleculeTypeID_C in p.listOfMoleculeTypeIDs
        
        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( cmd_is_valid, True )
        self.assertEqual( resultA, True )
        self.assertEqual( resultB, True )
        self.assertEqual( resultC, True )

    def test_cmd_declareMoleculeTypeList(self):
        cmd_str = "declare-moleculeType-list"
        moleculeType_A = "receptor"
        moleculeType_B  = "ligand"
        
        arg_str_list = [ str(moleculeType_A), str(moleculeType_B) ]
        c = Command( cmd_str, arg_str_list )
        p = ExperimentParameters()
        handleCommand( c, p )

        resultA = moleculeType_A in p.listOfMoleculeTypes
        resultB = moleculeType_B in p.listOfMoleculeTypes
        
        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( c.cmd_str_is_valid(), True )
        self.assertEqual( resultA, True )
        self.assertEqual( resultB, True )


    def test_cmd_declareMoleculeTypeIDCount(self):
        cmd_str = "declare-moleculeTypeID-count"
        moleculeTypeID_A = 50
        moleculeTypeID_Acount = 20

        moleculeTypeID_B = 1234
        moleculeTypeID_Bcount = 10

        arg_str_list1 = [ str(moleculeTypeID_A), str(moleculeTypeID_Acount) ]
        arg_str_list2 = [ str(moleculeTypeID_B), str(moleculeTypeID_Bcount) ]

        c1 = Command( cmd_str, arg_str_list1 )
        c2 = Command( cmd_str, arg_str_list2 )
        p = ExperimentParameters()
        handleCommand( c1, p )
        handleCommand( c2, p )

        tableContents = list( p.moleculeTypeID_counts_table.items() )
        resultA = (moleculeTypeID_A, moleculeTypeID_Acount) in tableContents
        resultB = (moleculeTypeID_B, moleculeTypeID_Bcount) in tableContents
        
        self.assertEqual( c1.cmd_str, cmd_str )
        self.assertEqual( c1.cmd_str, cmd_str )
        self.assertEqual( c2.cmd_str_is_valid(), True )
        self.assertEqual( c2.cmd_str_is_valid(), True )
        self.assertEqual( resultA, True )
        self.assertEqual( resultB, True )

    
    def test_cmd_declareBindingPair(self):
        cmd_str = "declare-binding-pair"
        moleculeTypeID_A = 50
        moleculeTypeID_B = 1234
        moleculeTypeID_C = 1235

        arg_str_list1 = [ str(moleculeTypeID_A), str(moleculeTypeID_B) ]
        arg_str_list2 = [ str(moleculeTypeID_A), str(moleculeTypeID_C) ]
        c1 = Command( cmd_str, arg_str_list1 )
        c2 = Command( cmd_str, arg_str_list2 )
        p = ExperimentParameters()
        handleCommand( c1, p )
        handleCommand( c2, p )

        resultA = (moleculeTypeID_A, moleculeTypeID_B) in p.bindingPairs_set
        resultB = (moleculeTypeID_A, moleculeTypeID_C) in p.bindingPairs_set

        self.assertEqual( c1.cmd_str, cmd_str )
        self.assertEqual( c1.cmd_str_is_valid(), True )
        self.assertEqual( c2.cmd_str, cmd_str )
        self.assertEqual( c2.cmd_str_is_valid(), True )
        self.assertEqual( resultA, True )
        self.assertEqual( resultB, True )

    def test_cmd_assignMoleculeTypeIDToMoleculeType(self):
        cmd_str = "assign-moleculeTypeID-to-moleculeType"
        moleculeTypeID = 50
        moleculeType = "receptor"

        arg_str_list = [ str(moleculeTypeID), str(moleculeType) ]
        c = Command( cmd_str, arg_str_list )
        p = ExperimentParameters()
        handleCommand( c, p )

        tableContents = list( p.moleculeTypeID_types_table.items() )
        result = (moleculeTypeID, moleculeType) in tableContents
        
        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( c.cmd_str_is_valid(), True )
        self.assertEqual( result, True )


    def test_cmd_assignMoleculeTypeIDToBasename(self):
        cmd_str = "assign-moleculeTypeID-to-basename"
        moleculeTypeID = 1234
        moleculeBasename = "myo1n1cv4"

        arg_str_list = [ str(moleculeTypeID), str(moleculeBasename) ]
        c = Command( cmd_str, arg_str_list )
        p = ExperimentParameters()
        handleCommand( c, p )

        tableContents = list( p.moleculeTypeID_basename_table.items() )
        result = (moleculeTypeID, moleculeBasename) in tableContents
        
        self.assertEqual( c.cmd_str, cmd_str )
        self.assertEqual( c.cmd_str_is_valid(), True )
        self.assertEqual( result, True )



if __name__ == "__main__":
    unittest.main()
