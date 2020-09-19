#!/bin/bash

for jobid in $(seq $1 $2)
do
scancel $jobid
done