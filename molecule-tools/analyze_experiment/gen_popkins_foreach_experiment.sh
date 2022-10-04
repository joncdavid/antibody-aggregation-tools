#!/usr/bin/env bash
# Filename: gen_popkins_foreach_experiment.sh
# Author: Jon David
# Date: Thursday, July 18, 2019
# Description:
# 
#-----------------------------------------------------------------


## Call this script from .../molecule/Experiment-Results-Only/
ANALYSIS_TOOLS_DIR=$PWD/../Tools-Analysis/

function cumulate_class_stats_for_single_experiment {
    #echo "We are now in function cumulate_constats_for_single_experiment"
    experimentDir=$1
    experimentName=$2
    
    (cd $experimentDir;
     $ANALYSIS_TOOLS_DIR/cumulate_class_stats.sh $experimentName)
    ## this produces files cumulative_class_stats.free.$experimentName.csv
    ## this produces files cumulative_class_stats.singletons.$experimentName.csv
    ## this produces files cumulative_class_stats.chains.$experimentName.csv
    ## this produces files cumulative_class_stats.cycles.$experimentName.csv
    ## this produces files cumulative_class_stats.clusters.$experimentName.csv
}

##---- main ----
inFname=$1  ## e.g. cumulate_class_stats_all_experiments.config
while read line; do
    expDir=`echo $line | cut -d' ' -f1`
    expName=`echo $line | cut -d' ' -f2`

    cumulate_class_stats_for_single_experiment $expDir $expName
    # e.g. line: my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L
    # e.g. execute:
    # cumulate_constats_for_single_experiment my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L
done < $inFname
