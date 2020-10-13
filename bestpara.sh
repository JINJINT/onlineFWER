#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="bestpara"   
FWER=1
for alpha in 0.1 0.05
do
for gamma in 2 1.1
do
for tau in $(seq 0 0.05 1)
do
for lbd in $(seq 0 0.05 1)
do 
for muN in -2 -1 0
do
echo "Submitting job for experiment "$experiment_name" with para tau = "$tau" and lbd = "$lbd"and FWER ="$FWER"and muN = "$muN
command="./runonebestpara.sh $tau $lbd $FWER $muN $alpha $gamma"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "tau"$tau"_lbd"$lbd"_FWER"$FWER"_muN"$muN$experiment_name $command
done
done
done  
done
done 
