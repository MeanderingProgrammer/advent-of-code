#!/bin/bash

if [[ $# -ne 1 ]]
then
    echo 'Usage: <year>'
    exit 1
fi

JAVA="java"
PYTHON="python"

language () {
    if [[ ${1} == "2019" ]] && [[ ${2} == "18" ]]
    then
        to_run=${JAVA}
    else
        to_run=${PYTHON}
    fi
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

    language ${year} ${i}

    echo "Running day ${i} with ${to_run}"

    cd ${folder}

    if [[ ${to_run} == ${JAVA} ]]
    then
        javac Solver.java
        java Solver
    elif [[ ${to_run} == ${PYTHON} ]]
    then 
        python3 solver.py
    fi

    cd ..

done

