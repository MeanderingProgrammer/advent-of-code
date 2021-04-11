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
PYTHON="python"

JAVA_DAYS=(
    "2019:18"
    "2019:20"
)

language () {
    year_day="${1}:${2}"    
    runner="${PYTHON}"

    for java_day in "${JAVA_DAYS[@]}"
    do
        if [[ ${year_day} == ${java_day} ]]
        then
            runner="${JAVA}"
        fi
    done

    echo "${runner}"
}

year=${1}

echo "Runing year ${year}"
cd ${year}

for i in $(seq 1 25)
do
    
    if [[ ${#i} -eq 1 ]]
    then
        folder="0${i}"
    else
        folder="${i}"
    fi

    to_run=$(language ${year} ${i})

    echo "Running day ${i} with ${to_run}"

    cd ${folder}

    if [[ ${to_run} == ${JAVA} ]]
    then
        javac Solver.java
        time_run java Solver
    elif [[ ${to_run} == ${PYTHON} ]]
    then 
        time_run python3 solver.py
    fi

    cd ..

done

