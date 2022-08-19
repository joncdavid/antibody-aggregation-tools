#!/usr/bin/env bash
# Filename: cumulate_con_stats_foreach_experiment.sh
# Author: Jon David
# Date: Thursday, July 11, 2019
# Description:
# 
#-----------------------------------------------------------------


## Call this script from .../molecule/Experiment-Results-Only/
ANALYSIS_TOOLS_DIR=$PWD/../Tools-Analysis/

function cumulate_constats_for_single_experiment {
    #echo "We are now in function cumulate_constats_for_single_experiment"
    experimentDir=$1
    experimentName=$2
    
    (cd $experimentDir;
     $ANALYSIS_TOOLS_DIR/cumulate_con_stats.sh $experimentName)
    ## this produces file cumulative_con_stats.$experimentName.csv
}

##---- main ----
inFname=$1  ## e.g. cumulate_con_stats_all_experiments.config
while read line; do
    expDir=`echo $line | cut -d' ' -f1`
    expName=`echo $line | cut -d' ' -f2`

    cumulate_constats_for_single_experiment $expDir $expName
    # e.g. line: line: my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L
    # e.g. execute:
    # cumulate_constats_for_single_experiment my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L
    
done < $inFname
