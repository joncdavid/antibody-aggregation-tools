#!/usr/bin/env bash
# filename: filterOutInvalidDistances.sh
# author: Jon David
#--------------------------------------------------------------------------------------------------
# descriptions:
#   For each experimental run, read files: bindingDistances.data and full_bindingsites.data
#   And produce:
#     full_bindingsites.data.noPeriods
#     bindingDistances.data.onlyValidEdges
#
#   By using the Python script of the same name, filterOutInvalidDistances.py, at each directory.
#--------------------------------------------------------------------------------------------------
# usage:
#   This script does not require arguments, and is independent of experiment name. Simply call...
# 
#   ./filterOutInvalidDistances.sh
#
#--------------------------------------------------------------------------------------------------

f1=bindingDistances.data
f2a=full_bindingsites.data
f2b=full_bindingsites.data.last
f2c=full_bindingsites.data.last.noPeriods
outf=bindingDistances.data.onlyValidEdges
find . -maxdepth 1 -type d \( ! -name . \) \
    -exec bash -c "( cd '{}' && 
                     pwd && 
                     tail -n 1 ${f2a} > ${f2b} &&
                     sed 's/\./,/g' ${f2b} > ${f2c} &&
                     ../filterOutInvalidDistances.py ${f1} ${f2c} ${outf} )" \;

## note: you may get an error that reads "tail: cannot open 'full_bindingsites.data' for reading: No such file or directory.
##       if this is inside a directory for an experimental run, this is a problem because the file wasn't generated;
##       if this happens in any other directory, then this is expected because that file won't be generated in that directory.


##&& ../filterOutInvalidDistances.py ${} ${} ${})" \;

