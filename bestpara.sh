#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="bestpara"   

for tau in $(seq 0 0.05 1)
do
for lbd in $(seq 0 0.05 1)
do 
echo "Submitting job for experiment "$experiment_name" with para tau = "$tau" and lbd = "$lbd
command="./runonebestpara.sh $tau $lbd"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "tau"$tau"_lbd"$lbd$experiment_name $command
done
done    
