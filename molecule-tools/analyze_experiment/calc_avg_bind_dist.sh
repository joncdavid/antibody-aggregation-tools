#!/usr/bin/env bash
# filename: calc_avg_bind_dist.sh
# author: Jon David
# description:
#   Calculates the average bound distance between epitopes.
#   Makes use of the script "filterOutInvalidDistances.sh".
#
#----------------------------------------------------------------
# prerequisite:
#   run "filterOutInvalidDistances.sh"
#
#
#----------------------------------------------------------------
# usage:
#   this script does not have any arguments and is independent of
#   experiment name. Simply call:
#
#     ./calc_avg_bind_dist.sh
#
#----------------------------------------------------------------

faccumulate=bindingDistances.data.onlyValidEdges.allRuns
fdistancesOnly=$faccumulate.distancesOnly.csv

## cleanup from last time
rm -f $faccumulate
rm -f $fdistancesOnly

find . -name "bindingDistances.data.onlyValidEdges" -exec cat {} + >> $faccumulate
cut -d, -f5 $faccumulate > $fdistancesOnly

echo "wrote to ${fdistancesOnly}"
#echo "Sorry, Numpy isn't installed. Download ${fdistancesOnly} and use Matlab or something externally."

