#!/usr/bin/env python3

import sys
import traceback

from experiment_declaration_reader import ExperimentDeclarationReader
from experiment_parameters import ExperimentParameters

STR_CMD_NAME_DECL_EXP_NAME = "declare-experiment-name"
STR_CMD_NAME_DECL_EXP_TYPE = "declare-experiment-type"
STR_CMD_NAME_DECL_NUM_RUNS = "declare-num-runs"
STR_CMD_NAME_DECL_SEED = "declare-seed"
STR_CMD_NAME_MAX_TIMESTEPS = "declare-max-timesteps"
STR_CMD_NAME_MIN_XZ = "declare-min-xz"
STR_CMD_NAME_MAX_XZ = "declare-max-xz"
STR_CMD_NAME_DECL_MOLECULETYPEID_LIST = "declare-moleculeTypeID-list"
STR_CMD_NAME_DECL_MOLECULETYPE_LIST = "declare-moleculeType-list"
STR_CMD_NAME_DECL_MOLECULETYPEID_COUNT = "declare-moleculeTypeID-count"
STR_CMD_NAME_DECL_BINDING_PAIR = "declare-binding-pair"
STR_CMD_NAME_ASSIGN_MOLECULETYPEID_MOLECULETYPE = "assign-moleculeTypeID-to-moleculeType"
STR_CMD_NAME_ASSIGN_MOLECULETYPEID_BASENAME = "assign-moleculeTypeID-to-basename"
                   
valid_cmd_list = [ STR_CMD_NAME_DECL_EXP_NAME,
                   STR_CMD_NAME_DECL_EXP_TYPE,
                   STR_CMD_NAME_DECL_NUM_RUNS,
                   STR_CMD_NAME_DECL_SEED,
                   STR_CMD_NAME_MAX_TIMESTEPS,
                   STR_CMD_NAME_MIN_XZ,
                   STR_CMD_NAME_MAX_XZ,
                   STR_CMD_NAME_DECL_MOLECULETYPEID_LIST,
                   STR_CMD_NAME_DECL_MOLECULETYPE_LIST,
                   STR_CMD_NAME_DECL_MOLECULETYPEID_COUNT,
                   STR_CMD_NAME_DECL_BINDING_PAIR,
                   STR_CMD_NAME_ASSIGN_MOLECULETYPEID_MOLECULETYPE,
                   STR_CMD_NAME_ASSIGN_MOLECULETYPEID_BASENAME ]

## helper function not available until Python3 v3.8+
def isAlpha(c):
    asciiValue = ord( c )
    if ( (0x41 <= asciiValue and asciiValue <= 0x5a) or
         (0x61 <= asciiValue and asciiValue <= 0x7a) ):
        return True
    return False
    
class Command(object):
    def __init__(self, cmd_str, arg_list):
        self.cmd_str = cmd_str
        self.arg_list = arg_list
        if not self.cmd_str_is_valid():
            raise Exception("Command {} not valid.".format( cmd_str ) )
        return

    def cmd_str_is_valid(self,
                         valid_list=valid_cmd_list):
        result = self.cmd_str in valid_list
        return result

    # def arg_str_is_valid(self):
    #     """This method is meant to be overridden."""
    #     return False

    def parse_arg_simple_int(self):
        result = None
        try:
            result = int(self.arg_list[0])
        except ValueError as e:
            raise e
        return result

    def parse_arg_simple_int_list(self):
        result = None
        try:
            result = []
            for s in self.arg_list:
                val = int(s)
                result.append(val)
        except ValueError as e:
            print(e)
            exit(1)
        return result

    def parse_arg_simple_str(self):
        result = None
        try:
            result = str( self.arg_list[0] )
            ## aww str.isAlpha() only exists in Python3 3.8+
            if not isAlpha( result[0] ):
                raise Exception("[Error] String must begin with a letter. {}".format(result[0]))
        except ValueError as e:
            print(e)
            exit(1)
        
        return result

    def parse_arg_simple_str_list(self):
        result = None
        try:
            result = []
            for s in self.arg_list:
                result.append(s)
        except Exception as e:
            print(e)
            exit(1)
        return result

    def parse_arg_int_int_pair(self):
        a = None
        b = None
        try:
            a = int( self.arg_list[0] )
            b = int( self.arg_list[1] )
        except ValueError as e:
            print(e)
            exit(1)
        return (a, b)

    def parse_arg_int_str_pair(self):
        a = None
        s = None
        try:
            a = int( self.arg_list[0] )
            s = str( self.arg_list[1] )
        except ValueError as e:
            print(e)
            exit(1)
        return (a, s)

def handleCommand_declareExperimentName(c, p):
    experimentName = c.parse_arg_simple_str()
    p.setExperimentName( experimentName )

def handleCommand_declareExperimentType(c, p):
    experimentType = c.parse_arg_simple_str()
    p.setExperimentType( experimentType )

def handleCommand_declareNumRuns(c, p):
    numRuns = c.parse_arg_simple_int()
    p.setNumRuns( numRuns )

def handleCommand_declareSeed(c, p):
    try:
        seed = c.parse_arg_simple_int()
        p.setSeed( seed )
    except ValueError as e:
        raise e

def handleCommand_maxTimesteps(c, p):
    max_timesteps = c.parse_arg_simple_int()
    p.setMaxTimesteps( max_timesteps )

def handleCommand_minXZ(c, p):
    min_xz = c.parse_arg_simple_int()
    p.setMinXZ( min_xz )
    
def handleCommand_maxXZ(c, p):
    max_xz = c.parse_arg_simple_int()
    p.setMaxXZ( max_xz )

def handleCommand_moleculeTypeIDList(c, p):
    moleculeTypeID_list = c.parse_arg_simple_int_list()
    p.addToListOfMoleculeTypeIDs( moleculeTypeID_list )

def handleCommand_moleculeTypeList(c, p):
    moleculeType_list = c.parse_arg_simple_str_list()
    p.addToListOfMoleculeTypes( moleculeType_list )

def handleCommand_moleculeTypeIDCount(c, p):
    (moleculeTypeID, moleculeCount) = c.parse_arg_int_int_pair()
    p.updateMoleculeTypeIDCountTable( [(moleculeTypeID, moleculeCount)] )

def handleCommand_bindingPair(c, p):
    (moleculeTypeID_a, moleculeTypeID_b) = c.parse_arg_int_int_pair()
    p.updateMoleculeBindingPairsSet( [(moleculeTypeID_a, moleculeTypeID_b)] )

def handleCommand_moleculeTypeIDToType(c, p):
    (moleculeTypeID, moleculeType) = c.parse_arg_int_str_pair()
    p.updateMoleculeTypeIDTypesTable( [(moleculeTypeID, moleculeType)] )

def handleCommand_moleculeTypeIDToBasename(c, p):
    (moleculeTypeID, moleculeBasename) = c.parse_arg_int_str_pair()
    p.updateMoleculeTypeIDBaseNameTable( [(moleculeTypeID, moleculeBasename)] )
    
# python doesn't have switch statements so... here's a workaround!
switch_cases = { STR_CMD_NAME_DECL_EXP_NAME:handleCommand_declareExperimentName,
                 STR_CMD_NAME_DECL_EXP_TYPE:handleCommand_declareExperimentType,
                 STR_CMD_NAME_DECL_NUM_RUNS:handleCommand_declareNumRuns,
                 STR_CMD_NAME_DECL_SEED:handleCommand_declareSeed,
                 STR_CMD_NAME_MAX_TIMESTEPS:handleCommand_maxTimesteps,
                 STR_CMD_NAME_MIN_XZ:handleCommand_minXZ,
                 STR_CMD_NAME_MAX_XZ:handleCommand_maxXZ,
                 STR_CMD_NAME_DECL_MOLECULETYPEID_LIST:handleCommand_moleculeTypeIDList,
                 STR_CMD_NAME_DECL_MOLECULETYPE_LIST:handleCommand_moleculeTypeList,
                 STR_CMD_NAME_DECL_MOLECULETYPEID_COUNT:handleCommand_moleculeTypeIDCount,
                 STR_CMD_NAME_DECL_BINDING_PAIR:handleCommand_bindingPair,
                 STR_CMD_NAME_ASSIGN_MOLECULETYPEID_MOLECULETYPE:handleCommand_moleculeTypeIDToType,
                 STR_CMD_NAME_ASSIGN_MOLECULETYPEID_BASENAME:handleCommand_moleculeTypeIDToBasename,
    }

def handleCommand(c, p):
    cmd_str = c.cmd_str
    try:
        switch_cases[cmd_str](c, p)
    except ValueError as e:
        raise e
    except Exception as e:
        print( "[ERROR] instruction {} is not supported!".format( cmd_str ) )
        print(e)
        exit(1)
        return

class ExperimentDeclaration(object):
    def __init__(self):
        return


    def load_from_file(self, fname):
        reader = ExperimentDeclarationReader()
        cmd_arg_pairs_list = reader.read_file( fname )
        
        p = ExperimentParameters()
        lineNum = 1
        for (cmd_str, arg_list) in cmd_arg_pairs_list:
            try:
                c = Command( cmd_str, arg_list )
                handleCommand( c, p )
            except ValueError as e:
                print(e)
                print(" >> Error in file {}, line {}".format(fname, lineNum))
                exit(1)
            except Exception as e:
                print(e)
                print(" >> Error in file {}, line {}".format(fname,lineNum))
                exit(1)
                lineNum = lineNum + 1
        return p

def main():
    fname = sys.argv[1]
    d = ExperimentDeclaration()
    p = d.load_from_file( fname )
    p.print_summary()
    return

if __name__ == "__main__":
    main()
