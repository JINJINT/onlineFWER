#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="onesided"   
for FWER in 1 2 3 4
do
for muN in -1.5 -1 -0.5 0
do 
for muA in 4 5
do
for gamma in 1.01 1.5 2
do
for alpha in 0.05 0.1 0.2
do
echo "Submitting job for experiment "$experiment_name" with para FWER = "$FWER" muN = "$muN" muA = "$muA" gamma = "$gamma" alpha = "$alpha
command="./runonet.sh $FWER $muN $muA $gamma $alpha"
# construct final call based on machine
sbatch --time=12:00:00 -p RM-shared -J "FWER"$FWER"muN"$muN"muA"$muA"gamma"$gamma"alpha"$alpha$experiment_name $command
done 
done
done
done
done
