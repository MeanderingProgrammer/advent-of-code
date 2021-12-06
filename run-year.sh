#!/bin/bash

if [[ $# -ne 1 ]]
then
    echo 'Usage: <year>'
    exit 1
fi

# Setup PYTHONPATH so commons imports work
current_directory=$(pwd)
export PYTHONPATH=${current_directory}

time_run() {
    command time -f "Runtime: %E" $@
}

JAVA="java"
PYTHON="py"
GO="go"

year=${1}

echo "Runing year ${year}"
cd ${year}

days=$(ls | sort)
for day in ${days}
do
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

    cd ..
done
