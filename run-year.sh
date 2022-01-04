#!/bin/bash

if [[ $# -ne 1 && $# -ne 2 ]]
then
    echo 'Usage: <year> <day1,day2,...>?'
    exit 1
fi

# Setup PYTHONPATH so commons imports work
current_directory=$(pwd)
export PYTHONPATH=${current_directory}

# Store array of runtimes
runtimes=()

time_run() {
    start=$(date -u +%s.%N)
    $@
    end=$(date -u +%s.%N)
    runtime=$(echo "$end - $start" | bc)
    printf "Runtime: %f \n" ${runtime}
}

JAVA="java"
PYTHON="py"
GO="go"

run_day() {
    day=${1}

    cd ${day}

    solution_file=$(ls *olver* | tail -1)
    extension="${solution_file#*.}"

    echo "Running day ${day} with ${extension}"

    if [[ ${extension} == ${JAVA} ]]
    then
        javac Solver.java
        time_run java Solver
    elif [[ ${extension} == ${PYTHON} ]]
    then
        time_run python3 solver.py
    elif [[ ${extension} == ${GO} ]]
    then
        time_run go run solver.go
    else
        echo "Unhandled extension: ${extension}"
        exit 1
    fi

    # If this is being executed in a for loop then we need to make sure
    # to change out of the directory before running the next iteration
    cd ..
}

year=${1}

echo "Runing year ${year}"
cd ${year}

if [[ $# -eq 1 ]]
then
    days=($(ls | sort))
else
    days=($(echo ${2} | tr "," "\n"))
fi

# Run each day specified and append runtime to an array
for day in "${days[@]}"
do
    run_day ${day}
    runtimes+=(${runtime})
done

# Generates a table with runtimes for all days
printf "\n"
printf "| Year | Day | Time (sec.) | \n"
printf "| ---- | --- | ----------- | \n"
for i in "${!runtimes[@]}"
do
    printf "| %4.4s | %3.3s | %11.11s | \n" ${year} ${days[i]} ${runtimes[i]}
done
