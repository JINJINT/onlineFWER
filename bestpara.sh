#!/bin/bash

# specify name of experiment, which will correspond to an input file
experiment_name="bestpara"   

for tau in $(seq 0 0.05 1)
do
for lbd in $(seq 0 0.05 1)
do 
for FWER in $(seq 1 3 4)
do
if [ FWER==4 ]
then
muN=-2
echo "Submitting job for experiment "$experiment_name" with para tau = "$tau" and lbd = "$lbd"and FWER ="$FWER"and muN = "$muN
command="./runonebestpara.sh $tau $lbd $FWER $muN"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "tau"$tau"_lbd"$lbd"_FWER"$FWER"_muN"$muN$experiment_name $command
fi
if [ FWER==1 ]
then
for muN in $(seq 0 -1 -2) 
do
echo "Submitting job for experiment "$experiment_name" with para tau = "$tau" and lbd = "$lbd"and FWER ="$FWER"and muN = "$muN
command="./runonebestpara.sh $tau $lbd $FWER $muN"
# construct final call based on machine
sbatch --time=06:00:00 -p RM-shared -J "tau"$tau"_lbd"$lbd"_FWER"$FWER"_muN"$muN$experiment_name $command
done
fi	
done
done
done    
