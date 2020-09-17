#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="twosided"   
for sigma in $(seq 0.1 0.1 1)
do
echo "Submitting job for experiment "$experiment_name" with para sigma = "$sigma
command="./runonetwosided.sh $sigma"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "sigma"$sigma$experiment_name $command
done 
