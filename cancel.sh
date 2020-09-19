#!/bin/bash

for jobid in $(seq $1 $2)
do
echo $jobid
scancel $jobid
done