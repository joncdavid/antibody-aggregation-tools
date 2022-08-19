#!/usr/bin/env bash
# file: cleanHopStatsFile.sh
# author: Jon David
# date: Friday, December 20, 2019
# description:
#   Cleans up the raw hop_stats_[all|rec].m file to be suitable
#   for importing into matlab.
#     * replaces comma with newline
#     * removes non-numeric, non-white-space characters.
#--------------------------------------------------------------------
# original format (example):
#   hopHistRec_50_50_85_25_0 = [ 0.263953, 0.271767, ..., ] ;
#--------------------------------------------------------------------
# details (order matters):
#   * only focus on elements to the right of '='
#   * remove anything not a digit, '.', or ','
#   * replace comma with newlines
#--------------------------------------------------------------------

fname=$1              ## e.g. hop_stats_rec.m
ofname=$fname.clean   ## e.g. hop_stats_rec.m.clean
tempf=temp.temp
tempf2=temp2.temp2
tempf3=temp3.temp3
rm -f $tempf $tempf2 $tempf3

## only focus on elements to the right of '='
cut --delimiter== --fields=2 $fname > $tempf

## remove anything not a digit, '.', or ','
sed "s/[^0-9.,]//g" $tempf > $tempf2

## replace comma with newlines
sed "s/\,/\n/g" $tempf2 > $tempf3

## cleanup
mv $tempf3 $ofname
#rm -f $tempf $tempf2
