#PBS -l nodes=1:ppn=2
#PBS -l walltime=00:15:00
#PBS -N whoHasFinished
#PBS -S /bin/bash

#echo "PBS_O_WORKDIR: $PBS_O_WORKDIR"
#echo ""

ofname=finishedRuns.out

##cd $PBS_O_WORKDIR
nice find . -name "tmpPath.fl" | xargs tail -n 3 > $ofname

echo "Finished-runs query saved to: " $ofname
wait
echo "Done."
