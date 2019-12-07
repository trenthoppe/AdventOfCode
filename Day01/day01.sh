#!/bin/bash

calculateModuleFuel() {
    fuel=$(($1/3))
    fuel=$(printf "%.0f" $fuel)
    fuel=$(($fuel-2))
    echo $fuel
}

calculateModuleFuelRecursive() {
    fuel=$(calculateModuleFuel $1)
    if (( $fuel < 0 )); then
	echo 0
    else
    	echo $(($fuel + $(calculateModuleFuelRecursive $fuel)))
    fi
}

filename=$1
fuelTotal=0
while read line; do
# Part 1 (non-recursive)
# fuelTotal=$(($fuelTotal + $(calculateModuleFuel $line)))
fuelTotal=$(($fuelTotal + $(calculateModuleFuelRecursive $line)))
done < $filename
echo $fuelTotal



