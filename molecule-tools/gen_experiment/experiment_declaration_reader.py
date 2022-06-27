#!/usr/bin/env/ python3

import sys

class ExperimentDeclarationReader(object):
    def __init__(self):
        return

    def parse_line(self, s_line ):
        t = s_line.split()
        cmd_str = t[0]
        arg_str = t[1:]
        return (cmd_str, arg_str)

    def remove_comments(self, line):
        line = line.split("#")[0]
        return line
    
    def read_file(self, fname):
        cmd_arg_pairs_list = []
        with open(fname, "r") as f:
            for line in f:
                line = self.remove_comments( line )
                line = line.strip()
                if line:
                    (cmd_str, arg_str) = self.parse_line( line )
                    cmd_arg_pairs_list.append( (cmd_str, arg_str) )
        return cmd_arg_pairs_list

def main():
    fname = sys.argv[1]
    reader = ExperimentDeclarationReader()
    cmd_arg_pairs_list = reader.read_file( fname )
    return
    
if __name__ == "__main__":
    main()

    
