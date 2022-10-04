#!/usr/bin/env bash
# filename: gen_popkinsForChains.sh
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
#----
# ./gen_popkinsForChains.py full_bindingsites.data.noPeriods temp 1 25 20
#--------------------------------------------------------------------------------------------------


expName=my100GrpTwo20R10L10M
numMols=40
startIdx=20

f1a=full_bindingsites.data
f1b=full_bindingsites.data.noPeriods
outfPerRun=class_stats.groupByAggsize.${expName}.csv
outfPer2mer=cumulative_class_stats.2mer.${expName}.csv

echo "expName: ${expName}"
echo "numMols: ${numMols}"
echo "startIdx: ${startIdx}"
echo "f1a: ${f1a}"
echo "f1b: ${f1b}"
echo "outfPerRun: ${outfPerRun}"
echo "outfPer2mer: ${outfPer2mer}"

## for each run, generate ${outf}
find . -maxdepth 1 -type d \( ! -name . \) \
    -exec bash -c "( cd '{}' && 
                     pwd && 
                     sed 's/\./,/g' ${f1a} > ${f1b} &&
                     ../gen_popkinsForChains.py ${f1b} ${outfPerRun} 1 ${numMols} ${startIdx} )" \;

python3 gen_aggregatePopkinsForChains.py $expName

## note: you may get an error that reads "tail: cannot open 'full_bindingsites.data' for reading: No such file or directory.
##       if this is inside a directory for an experimental run, this is a problem because the file wasn't generated;
##       if this happens in any other directory, then this is expected because that file won't be generated in that directory.


