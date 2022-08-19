#!/usr/bin/env bash
# filename: gen_bindProbsMatrix.sh
# author: Jon David
# date: Monday, June 14, 2021
# description:
#   Generates a CSV file containing data to analyze binding probabilities of this experiment.
#

experimentName=my100GrpTwo20R10L10M
totalNumMols=40
numMolType=3
startIdxList=0,20,30


fname=zztemp.bindingsites.data.aggregate
fname2=$fname.noPeriods
fname3=results-$experimentName.bindingsites.data.aggregate.csv

echo "==== inputs for gen_binProbsMatrix.sh ===="
echo "experimentName: ${experimentName}"
echo "totalNumMols: ${totalNumMols}"
echo "startIdxList: ${startIdxList}"
echo "fname: ${fname}"
echo "fname2: ${fname2}"
echo "fname3: ${fname3}"

## cleanup previous...
rm -f $fname; touch $fname
rm -f $fname2; touch $fname2
rm -f $fname3; touch $fname3

find . -name "full_bindingsites.data" -exec tail -n 1 {} \; >> $fname
sed "s/\./,/g" $fname > $fname2
#./calc_bindsites_stats.py $fname2 $fname3 1 $totalNumMols $ligandStartIdx

echo""
echo "Now calling calc_stericHindrance.py..."
echo ""
./calc_stericHindrance.py $fname2 $fname3 $numMolType $totalNumMols $startIdxList

echo "Wrote to: " $fname3
