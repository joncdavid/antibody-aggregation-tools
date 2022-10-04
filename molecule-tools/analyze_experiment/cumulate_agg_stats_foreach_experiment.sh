#!/usr/bin/env bash
# Filename: cumulate_agg_stats_foreach_experiment.sh
# Author: Jon David
# Date: Monday, June 10, 2019
# Description:
#   For each experiment found in some directory,
#   cumulate the aggregate size distribution into a single matrix.
#-----------------------------------------------------------------


## Call this script from .../molecule/Experiment-Results-Only/
ANALYSIS_TOOLS_DIR=$PWD/../Tools-Analysis/

function cumulate_aggstats_for_single_experiment {
    #echo "We are now in function cumulate_aggstats_for_single_experiment"
    experimentDir=$1
    experimentName=$2
    maxAggregateSize=$3

    #echo "PWD: $PWD"
    #echo "experimentDir: $experimentDir"
    #echo "experimentName: $experimentName"
    #echo "maxAggregateSize: $maxAggregateSize"
    #echo "ANALYSIS_TOOLS_DIR: $ANALYSIS_TOOLS_DIR"
    
    (cd $experimentDir;
     $ANALYSIS_TOOLS_DIR/cumulate_agg_stats.sh $experimentName $maxAggregateSize)
    ## this produces file cumulative_agg_stats.$experimentName.csv
}

#maxAggregateSize=5
#cumulate_aggstats_for_single_experiment my100mb4nt50R66L-mFilesOnly/ my100mb4nt50R66L $maxAggregateSize
#cumulate_aggstats_for_single_experiment my100mb4nt50R75L-mFilesOnly/ my100mb4nt50R75L $maxAggregateSize
#cumulate_aggstats_for_single_experiment my100mb4nt50R100L-mFilesOnly/ my100mb4nt50R100L $maxAggregateSize

##---- main ----

inFname=$1  ## e.g. infname.config
while read line; do
    expDir=`echo $line | cut -d' ' -f1`
    expName=`echo $line | cut -d' ' -f2`
    maxAggSize=`echo $line | cut -d' ' -f3`

    cumulate_aggstats_for_single_experiment $expDir $expName $maxAggSize
    # e.g. line: line: my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L 5
    # e.g. execute:
    # cumulate_aggstats_for_single_experiment my100mb4nt50R50L-mFilesOnly/ my100mb4nt50R50L $maxAggregateSize
    
done < $inFname
