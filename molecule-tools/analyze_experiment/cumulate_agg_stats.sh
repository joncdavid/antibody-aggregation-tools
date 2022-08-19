#!/usr/bin/env bash
# Filename: cumulate_agg_stats.sh
# Author: Jon David
# Date: Monday, June 10, 2019
# Description:
#   This script cumulates the aggregate size distribution
#   for an experiment (with multiple runs) into a single matrix.
#-----------------------------------------------------------------
# Input (example):
#   Each line represents an individual agg_stats_trim.m file:
#     aggHist_50_50_86_50_0 = [ 1, 11, 2, 15, 0, 2, 3, 1, 4, 1; ];
#     aggHist_50_50_86_50_1 = [ 3, 4, 1, 17, 2, 10, 0, 1; ];
#     aggHist_50_50_86_50_2 = [ 2, 9, 4, 1, 3, 3, 1, 17, 0, 2; ];
#     ...
#   
#-----------------------------------------------------------------
# Output (example):
#   Each line represents the count of the number of aggregates
#   of sizes 0, 1, 2, 3, and 4, respectively.
#
#   cumulative_agg_stats.csv
#   ------------------------
#     2,11,15,1,1
#     1,17,10,4,0
#     2,17,9,3,1
#     ...
#
#

toolsdir=$PWD/../../Tools-Analysis/
experimentName=$1
maxAggregateSize=$2
tempf=temp.temp           ## aggregated agg_stats_trim.m datae
tempf2=temptemp.temptemp  ## removed space, "[", "]", and ";" symbols.
outf=cumulative_agg_stats.$experimentName.csv  ## matrix format
plotfname=cumulative_agg_stats.$experimentName.png

find -name "agg_stats_trim.m" -exec cat {} \; > $tempf
cat $tempf | cut -d'=' -f2 | sed "s/ //g" | sed "s/\[//g" | sed "s/\]//g" | sed "s/;//g" > $tempf2
##which $toolsdir/simplifiedToMatrix.py
python3 $toolsdir/simplifiedToMatrix.py $tempf2 $outf $maxAggregateSize
## matlab -nosplash -nojvm -nodesktop -r plot_cumullative_agg_stats.m $outf $plotfname

#echo "Experiment Name: $experimentName"
echo "Generated cumulative agg_stats file: $outf"

## cleanup
#rm $tempf
#rm $tempf2
