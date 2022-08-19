#!/usr/bin/env bash
# Filename: cumulate_con_stats.sh
# Author: Jon David
# Date: Thursday, July 11, 2019
# Description:
#   This script cumulates the number of edges per timestep
#   for an experiment (with multiple runs) into a single matrix.
#-----------------------------------------------------------------
# Input (example):
#   Each line represents an individual agg_stats_trim.m file:
#     consHist_50_50_86_50_0 = [ 0,0,1,1,2,3,...,69,70,70,70 ];
#     consHist_50_50_86_50_1 = [ 0,0,1,1,2,3,...,69,69,69,69 ];
#     consHist_50_50_86_50_2 = [ 0,0,1,1,2,3,...,69,70,71,71 ];
#     ...
#   
#-----------------------------------------------------------------
# Output (example):
#   A matrix where...
#   Each row represents a time step.
#   Each column represents a single experimental run.
#   Each cell represents the number of edges at specific timestep
#    for specific experimental run.
#
#   cumulative_agg_stats.csv
#   ------------------------
#     0,0,0,0,...
#     1,0,0,1,...
#     1,0,0,2,...
#     2,1,0,3,...
#     ...
#     70,68,67,71,...
#     70,69,68,71,...
#     ...


## Note: this is for a single experiment...
## create new cumulative_con_stats.csv
## for each run,
##   con_stats.m -> con_stats.csv
##   paste -d, cumulative_con_stats.csv con_stats.csv

function convert_m_to_csv {
    ## con_stats.m -> con_stats.csv
    infname=$1
    outfname=$2
    #sed "s/,/\n/g" con_stats.m | sed "s/[^[:digit:]]//g" > con_stats.csv
    #sed "s/,/\n/g" $infname | sed "s/[^[:digit:]]//g" > $outfname
    cut -d= -f2 $infname | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $outfname
}

experimentName=$1

outf=cumulative_con_stats.$experimentName.csv  ## output aggregate con_stats.csv
rm -f $outf; touch $outf  ## make sure to start empty
find . -name "con_stats.m" | while read line; do
    fname=$line
    #tempfname=temp_con_stats.csv
    tempfname=$fname.csv
    tempaggfname=temp_agg_con_stats.csv
    
    echo "Processing file $fname"
    convert_m_to_csv $fname $tempfname
    paste -d, $outf $tempfname > $tempaggfname
    mv $tempaggfname $outf

    rm $tempfname  ## cleanup
done

## final cleanup -- remove weird comma at start of each line
## weird comma is a consequence of using paste with an empty file
tempf=cons_stats.temp
sed "s/^,//" $outf > $tempf
mv $tempf $outf

echo "Generated cumulative con_stats file: $outf"

