#!/bin/bash

if [[ $# -ne 1 ]]
then
    echo 'Usage: <year>'
    exit 1
fi

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

    echo "Running day ${i}"

    cd ${folder}
    python3 solver.py
    cd ..

done

