#!/usr/bin/env bash
# filename: gen_hopstatsData.sh
# author: Jon David
#--------------------------------------------------------------------------------------------------
# descriptions:
#   For each experimental run, read file: hop_stats_all.m
#   And produce:
#     hop_stats_all.m.csv
#
#--------------------------------------------------------------------------------------------------
# usage:
#   This script does not require arguments, and is independent of experiment name. Simply call...
# 
#   ./gen_hopstatsData.sh
#
#----
# ./gen_popkinsForChains.py full_bindingsites.data.noPeriods temp 1 25 20
#--------------------------------------------------------------------------------------------------


expName=my100mb2nrob20R10L
numMols=30
startIdx=20

f1a=hop_stats_all.m
f1b=hop_stats_all.m.listOnly
f1c=hop_stats_all.m.listOnly.csv

echo "expName: ${expName}"
echo "numMols: ${numMols}"
echo "startIdx: ${startIdx}"
echo "f1a: ${f1a}"
echo "f1b: ${f1b}"
echo "f1c: ${f1c}"
echo "outf: ${outf}"

## for each run, generate ${outf}
find . -maxdepth 1 -type d \( ! -name . \) \
    -exec bash -c "( cd '{}' && 
                     pwd && 
		     cut -d'=' -f2 ${f1a} > ${f1b} &&
                     sed 's/[^0-9,\.]//g' ${f1b} > ${f1c} )" \;  # &&
#                     ../gen_popkinsForChains.py ${f1b} ${outfPerRun} 1 ${numMols} ${startIdx} )" \;

python3 gen_aggregateHopkinsData.py $expName $f1c

## note: you may get an error that reads "tail: cannot open 'full_bindingsites.data' for reading: No such file or directory.
##       if this is inside a directory for an experimental run, this is a problem because the file wasn't generated;
##       if this happens in any other directory, then this is expected because that file won't be generated in that directory.


