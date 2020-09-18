#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="twosided"   
for muN in $(seq 0 0.2 2)
do
echo "Submitting job for experiment "$experiment_name" with para muN = "$muN
command="./runonetwosided.sh $muN"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "muN"$muN$experiment_name $command
done 
