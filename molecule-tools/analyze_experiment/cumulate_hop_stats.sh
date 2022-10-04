#!/usr/bin/env bash
# Filename: cumulate_hop_stats.sh
# Author: Jon David
# Date: Thursday, January 2, 2020
# Description:
#   This script cumulates the aggregate hopkins statistics
#   for each run in an experiment into a single matrix.
#-----------------------------------------------------------------
# Usage (standalone terminal example):
#   ../../Tools-Analysis/cumulate_hop_stats.sh mb4nt50R50L
#   note: called from [...]/molecule/Experiment-Results-Only/my100mb4nt50R50L-mFilesOnly/
#
# Usage (called from another script example):
#   cumulate_hop_stats.sh $experimentName
#
#-----------------------------------------------------------------
# Generated Intermediate File (example):
#   Each line represents an individual hop_stats_rec.m file:
#     hopHistRec_50_50_86_50_0 = [ A, B, C, ... , ];
#     hopHistRec_50_50_86_50_1 = [ D, E, F, ... , ];
#     ...
#-----------------------------------------------------------------
# Output (example):
#   Columns represents Hopkin's statistic at each time step.
#   Rows represents individual runs
#     A,B,C,...
#     D,E,F,...
#     ...
#

toolsdir=$PWD/../../Tools-Analysis/
experimentName=$1
tempf=temp.temp           ## cumulative hop_stats_rec
tempf2=temptemp.temptemp  ## used for intermediate files
tempf3=temptemptemp.temptemptemp ## used for intermediate files
outf=cumulative_hop_stats_rec.$experimentName.csv  ## matrix format (as csv)
#plotfname=cumulative_hop_stats.$experimentName.png

## part 1: create single file; each line is content from an individual run's hop_stats_rec.m file.
rm -f $tempf; touch $tempf
find . -name "hop_stats_rec.m" | xargs cat >> $tempf

## part 2: cleanup into csv where each column represents a time step; every row represents a new experiment.
rm -f $tempf2 $tempf3; touch $tempf2; touch $tempf3
cut --delimiter== --fields=2 $tempf > $tempf2
sed "s/[^0-9.,]//g" $tempf2 > $tempf3  ## remove anything not a digit, '.', or ','
mv $tempf3 $outf

echo "Generated cumulative hop_stats file: $outf"

## cleanup
#rm $tempf
#rm $tempf2
