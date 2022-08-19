#!/usr/bin/env bash
# Filename: cumulate_con_stats.sh
# Author: Jon David
# Date: Thursday, July 18, 2019
# Description:
#
#-----------------------------------------------------------------
# Input (example):
#   Each line represents an individual class_stats.m file:
#     freeHist_50_50_86_50_0 = [ 50,50,...,0 ];
#     snglFound_50_50_86_50_1 = [ 0,0,1,...];  # maybe mono. inc.
#     chanFound_50_50_86_50_2 = [ 0,0,1,...];  # maybe mono. inc.
#     cyclFound_50_50_86_50_2 = [ 0,0,1,...];  # maybe mono. inc.
#     clstFound_50_50_86_50_2 = [ 0,0,1,...];  # always mono. inc.
#   
#-----------------------------------------------------------------
# Outputs (example):
#   class_stats.free.csv
#     * rows represent timesteps [0,499999]
#     * single column represents single run
#     * each cell represents number of receptors classified as free
#
#   Same format for outputs:
#     * class_stats.singletons.csv
#     * class_stats.chains.csv
#     * class_stats.cycles.csv
#     * class_stats.clusters.csv
#--------------------------------------------------------------------



## Note: this is for a single experiment...
## create new cumulative_con_stats.csv
## for each run,
##   con_stats.m -> con_stats.csv
##   paste -d, cumulative_con_stats.csv con_stats.csv

function convert_m_to_csvs {
    ### Given a single class_stats.m, generate 5 output CSV files for
    ###   free receptors, singletons, chains, cycles, and clusters.
    infname=$1           ## e.g. class_stats.m (input)
    ofnameFree=$2        ## e.g. class_stats.free.csv (output)
    ofnameSingletons=$3  ## e.g. class_stats.singletons.csv (output)
    ofnameChains=$4      ## e.g. class_stats.chains.csv (output)
    ofnameCycles=$5      ## e.g. class_stats.cycles.csv (output)
    ofnameClusters=$6    ## e.g. class_stats.clusters.csv (output)

    tempf1=temp.class_stats.line1.m
    tempf2=temp.class_stats.line2.m
    tempf3=temp.class_stats.line3.m
    tempf4=temp.class_stats.line4.m
    tempf5=temp.class_stats.line5.m
    
    sed "1q;d" $infname > $tempf1
    sed "2q;d" $infname > $tempf2
    sed "3q;d" $infname > $tempf3
    sed "4q;d" $infname > $tempf4
    sed "5q;d" $infname > $tempf5
    
    cut -d= -f2 $tempf1 | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $ofnameFree
    cut -d= -f2 $tempf2 | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $ofnameSingletons
    cut -d= -f2 $tempf3 | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $ofnameChains
    cut -d= -f2 $tempf4 | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $ofnameCycles
    cut -d= -f2 $tempf5 | sed "s/,/\n/g" | sed "s/[^[:digit:]]//g" > $ofnameClusters

    # cleanup
    rm -f $tempf1
    rm -f $tempf2
    rm -f $tempf3
    rm -f $tempf4
    rm -f $tempf5
}

experimentName=$1

## output filenames
ofFree=cumulative_class_stats.free.$experimentName.csv
ofSingletons=cumulative_class_stats.singletons.$experimentName.csv
ofChains=cumulative_class_stats.chains.$experimentName.csv
ofCycles=cumulative_class_stats.cycles.$experimentName.csv
ofClusters=cumulative_class_stats.clusters.$experimentName.csv

## make sure to start empty...
rm -f $ofFree; touch $ofFree
rm -f $ofSingletons; touch $ofSingletons
rm -f $ofChains; touch $ofChains
rm -f $ofCycles; touch $ofCycles
rm -f $ofClusters; touch $ofClusters

## define individual names of files to generate
tfFree=temp.class_stats.free.csv
tfSingletons=temp.class_stats.singletons.csv
tfChains=temp.class_stats.chains.csv
tfCycles=temp.class_stats.cycles.csv
tfClusters=temp.class_stats.clusters.csv

## define names of temporary aggregate files (before moving it to final aggregate file)...
tempaggfnameFree=temp_agg_class_stats.free.csv
tempaggfnameSingletons=temp_agg_class_stats.singletons.csv
tempaggfnameChains=temp_agg_class_stats.chains.csv
tempaggfnameCycles=temp_agg_class_stats.cycles.csv
tempaggfnameClusters=temp_agg_class_stats.clusters.csv

find . -name "class_stats.m" | while read line; do
    fname=$line
    
    echo "Processing file $fname"
    convert_m_to_csvs $fname $tfFree $tfSingletons $tfChains $tfCycles $tfClusters
    paste -d, $ofFree $tfFree > $tempaggfnameFree
    paste -d, $ofSingletons $tfSingletons > $tempaggfnameSingletons
    paste -d, $ofChains $tfChains > $tempaggfnameChains
    paste -d, $ofCycles $tfCycles > $tempaggfnameCycles
    paste -d, $ofClusters $tfClusters > $tempaggfnameClusters

    mv $tempaggfnameFree $ofFree
    mv $tempaggfnameSingletons $ofSingletons
    mv $tempaggfnameChains $ofChains
    mv $tempaggfnameCycles $ofCycles
    mv $tempaggfnameClusters $ofClusters

    ## cleanup
    rm -f $tfFree
    rm -f $tfSingletons
    rm -f $tfChains
    rm -f $tfCycles
    rm -f $tfClusters
    #break  ## test, only do the first run.
done

## final cleanup -- remove weird comma at start of each line
##   weird comma is a consequence of using paste with an empty file
tempf1=temp.withInitComma.class_stats.free.csv
tempf2=temp.withInitComma.class_stats.singletons.csv
tempf3=temp.withInitComma.class_stats.chains.csv
tempf4=temp.withInitComma.class_stats.cycles.csv
tempf5=temp.withInitComma.class_stats.clusters.csv

sed "s/^,//" $ofFree > $tempf1
sed "s/^,//" $ofSingletons > $tempf2
sed "s/^,//" $ofChains > $tempf3
sed "s/^,//" $ofCycles > $tempf4
sed "s/^,//" $ofClusters > $tempf5

mv $tempf1 $ofFree
mv $tempf2 $ofSingletons
mv $tempf3 $ofChains
mv $tempf4 $ofCycles
mv $tempf5 $ofClusters

#echo "Generated cumulative con_stats file: $outf"

