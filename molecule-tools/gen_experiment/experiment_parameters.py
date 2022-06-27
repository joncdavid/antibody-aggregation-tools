#!/usr/bin/env python3

import sys

STR_EXP_TYPE_SINGLE = "single"
STR_EXP_TYPE_SET = "set"

class ExperimentParameters(object):
    def __init__(self):
        self.experimentName = None  ## String
        self.experimentType = None ## String :: {single, set}
        self.numRuns = None ## UInt
        self.seed = None ## UInt
        self.maxTimesteps = None ## UInt
        self.minXZ = None ## Int
        self.maxXZ = None ## Int        
        self.listOfMoleculeTypeIDs = None  ## [Int]
        self.listOfMoleculeTypes = None  ## [String:lower]
        self.moleculeTypeID_counts_table = None  ## f: moleculeTypeID -> UInt
        self.moleculeTypeID_types_table = None  ## f: moleculeTypeID -> moleculeType (String)
        self.bindingPairs_set = None  ## a set of (moleculeTypeID,moleculeTypeID) pairs.
        self.moleculeTypeID_basename_table = None  ## moleculeTypeIDs have a unique basename

    def isValid(self):
        """This ExperimentParameters object is valid iff all member variables are non-None."""
        checkList = []
        checkList.append( self.experimentName )
        checkList.append( self.experimentType )
        checkList.append( self.numRuns )
        checkList.append( self.seed )
        checkList.append( self.maxTimesteps )
        checkList.append( self.minXZ )
        checkList.append( self.maxXZ )
        checkList.append( self.listOfMoleculeTypeIDs )
        checkList.append( self.listOfMoleculeTypes )
        checkList.append( self.moleculeTypeID_counts_table )
        checkList.append( self.moleculeTypeID_types_table )
        checkList.append( self.bindingPairs_set )
        checkList.append( self.moleculeTypeID_basename_table )

        temp = list( filter ( (lambda x: x is None), checkList ))
        if len(temp) == 0:
            return True
        return False

    def getDirLevel(self):
        dirLevel = None
        if self.experimentType == STR_EXP_TYPE_SINGLE:
            dirLevel = 1
        elif self.experimentType == STR_EXP_TYPE_SET:
            dirLevel = 2
        else:
            dirLevel = None
        return dirLevel
    
    def setExperimentName( self, experimentName ):
        if experimentName is None:
            raise Exception("[ERROR] passed None to setExperimentName...")
        self.experimentName = experimentName

    def setExperimentType( self, experimentType ):
        if experimentType is None:
            raise Exception("[ERROR] passed None to setExperimentType...")
        self.experimentType = experimentType

    def setNumRuns( self, numRuns ):
        if numRuns is None:
            raise Exception("[ERROR] passed None to setNumRuns...")
        self.numRuns = numRuns

    def setSeed( self, seed ):
        if seed is None:
            raise Exception("[ERROR] passed None to setSeed...")
        self.seed = seed

    def setMaxTimesteps( self, maxTimesteps ):
        if maxTimesteps is None:
            raise Exception("[ERROR] passed None to setMaxTimesteps...")
        self.maxTimesteps = maxTimesteps

    def setMinXZ( self, minXZ ):
        if minXZ is None:
            raise Exception("[ERROR] passed None to setMinXZ...")
        self.minXZ = minXZ

    def setMaxXZ( self, maxXZ):
        if maxXZ is None:
            raise Exception("[ERROR] passed None to setMaxXZ...")
        self.maxXZ = maxXZ

    def addToListOfMoleculeTypeIDs( self, newListOfMoleculeTypeIDs ):
        if self.listOfMoleculeTypeIDs is None:
            self.listOfMoleculeTypeIDs = []
        if newListOfMoleculeTypeIDs is None:
            raise Exception("[ERROR] passed None to addToListOfMoleculeTypeIDs...")
        if len(newListOfMoleculeTypeIDs) == 0:
            raise Exception("[ERROR] passing empty list to addToListOfMoleculeTypeIDs...")
        self.listOfMoleculeTypeIDs.extend( newListOfMoleculeTypeIDs )

    def addToListOfMoleculeTypes( self, newListOfMoleculeTypes ):
        if self.listOfMoleculeTypes is None:
            self.listOfMoleculeTypes = []
        if newListOfMoleculeTypes is None:
            raise Exception("[ERROR] passed None to addToListOfMoleculeTypes...")
        if len(newListOfMoleculeTypes) == 0:
            raise Exception("[ERROR] passing empty list to addToListOfMoleculeTypes...")
        self.listOfMoleculeTypes.extend( newListOfMoleculeTypes )

    def updateMoleculeTypeIDCountTable( self, newMoleculeTypeIDCountPairs ):
        """newMoleculeTypeIDCountPairs is list of ordered pairs."""
        
        if newMoleculeTypeIDCountPairs is None:
            raise Exception("[ERROR] passed None to updateMoleculeTypeIDCountTable...")
        if self.moleculeTypeID_counts_table is None:
            self.moleculeTypeID_counts_table = {}
        try:
            self.moleculeTypeID_counts_table.update( newMoleculeTypeIDCountPairs )
        except IndexError as e:
            print(e)
            quit(1)

    def updateMoleculeTypeIDTypesTable( self, newMoleculeTypeIDTypePairs ):
        """newMoleculeTypeIDTypePairs is a list of ordered pairs."""
        if newMoleculeTypeIDTypePairs is None:
            raise Exception("[ERROR] passed None to addToListOfMoleculeTypes...")
        if self.moleculeTypeID_types_table is None:
            self.moleculeTypeID_types_table = {}
        try:
            self.moleculeTypeID_types_table.update( newMoleculeTypeIDTypePairs )
        except Exception as e:
            print(e)
            print(1)

    def updateMoleculeBindingPairsSet( self, newBindingPairs ):
        """newBindingPairs is a list of ordered pairs."""
        if newBindingPairs is None:
            raise Exception("[ERROR] passed None to updateMoleculeBindingPairsSet...")
        if self.bindingPairs_set is None:
            self.bindingPairs_set = set()
        try:
            for pair in newBindingPairs:
                moleculeTypeID_a = int( pair[0] )
                moleculeTypeID_b = int( pair[1] )
                self.bindingPairs_set.add( (moleculeTypeID_a, moleculeTypeID_b) )
        except Exception as e:
            print(e)
            print(1)

    def updateMoleculeTypeIDBaseNameTable( self, newMoleculeTypeIDBasenamePairs ):
        """newMoleculeTypeIDBasenamePairs is a list of ordered pairs."""
        if newMoleculeTypeIDBasenamePairs is None:
            raise Exception("[ERROR] passed None to updateMoleculeTypeIDBaseNameTable...")
        if self.moleculeTypeID_basename_table is None:
            self.moleculeTypeID_basename_table = {}
        self.moleculeTypeID_basename_table.update( newMoleculeTypeIDBasenamePairs )
        
    def print_summary(self):
        print("\n====Summary of Experiment Parameters ====\n")
        _print_helper_scalar( "ExperimentName", self.experimentName )
        _print_helper_scalar( "ExperimentType", self.experimentType )
        _print_helper_scalar( "Number of Runs", self.numRuns )
        _print_helper_scalar( "Seed", self.seed )
        _print_helper_scalar( "Max Timesteps", self.maxTimesteps )
        _print_helper_scalar( "MinXZ", self.minXZ )
        _print_helper_scalar( "MaxXZ", self.maxXZ )
        _print_helper_list( "List of MoleculeTypeIDs", self.listOfMoleculeTypeIDs )
        _print_helper_list( "List of MoleculeTypes", self.listOfMoleculeTypes )
        _print_helper_table( "MoleculeTypeID-Counts Table", self.moleculeTypeID_counts_table )
        _print_helper_table( "MoleculeTypeID-Types Table", self.moleculeTypeID_types_table )
        _print_helper_set( "Binding Pairs Set", self.bindingPairs_set )
        _print_helper_table( "MoleculeTypeID-Basename Table", self.moleculeTypeID_basename_table )
        print()


def _print_hr():
    _print_hr_helper("-", 60)
        
def _print_hr_helper(dashSymbol, numDashes):
    for i in range(0, numDashes):
        print( "{}".format(dashSymbol), end="" )
    print()
        
def _print_helper_scalar(label, x):
    print( "{}: {}".format( label, x ))

def _print_helper_list(label, x ):
    print( "\n{}".format( label ))
    _print_hr()
    for item in x:
        print( "{}".format(item) )

def _print_helper_table( label, x ):
    print( "\n{}".format( label ))
    _print_hr()
    for k in x.keys():
        v = x[k]
        print( "{}: {}".format( k, v ))

def _print_helper_set( label, x ):
    print( "\n{}".format( label ))
    _print_hr()
    for pair in x:
        print( "{}".format( pair ))

