#!/bin/bash

if [[ ${#} -ne 1 && ${#} -ne 2 ]]
then
    echo 'Usage: <year1,year2,...> <day1,day2,...>?'
    exit 1
fi

source ./runner/language-setup.sh

setup_python

time_run() {
    start=$(date -u +%s.%N)
    $@
    end=$(date -u +%s.%N)
    runtime=$(echo "$end - $start" | bc)
    printf "Runtime: %f \n" ${runtime}
}

JAVA="java"
RUST="rs"
PYTHON="py"
GO="go"

update_days() {
    if [[ ${#} -eq 0 ]]
    then
        days=($(ls | sort))
    else
        days=($(echo ${1} | tr "," "\n"))
    fi
}

run_day() {
    day=${1}
    solution_file=${2}
    language="${solution_file#*.}"

    echo "Running day ${day} with ${language}"

    if [[ ${language} == ${JAVA} ]]
    then
        setup_java
        # Runs in <year>/<day> directory, hence the ../..
        class_path=".:../../commons/java/*"
        find . -name '*java' | xargs javac -cp ${class_path} -d .
        time_run java -cp ${class_path} main.Solver
    elif [[ ${language} == ${RUST} ]]
    then
      setup_rust
      time_run cargo run -rq --bin "aoc_${year}_${day}"
    elif [[ ${language} == ${PYTHON} ]]
    then
        time_run python3 solver.py
    elif [[ ${language} == ${GO} ]]
    then
        time_run go run solver.go
    else
        echo "Unhandled language extension: ${language}"
        exit 1
    fi
}

echo "year,day,language,runtime" > runner/runtimes.csv

years=($(echo ${1} | tr "," "\n"))

for year in "${years[@]}"
do
    echo "Running year ${year}"
    pushd ${year} > /dev/null

    # Sets days array based on input and current year being run
    update_days ${2}

    # Run each day specified and update arrays
    for day in "${days[@]}"
    do
        pushd ${day} > /dev/null
        solution_files=($(ls *olver*))

        for solution_file in "${solution_files[@]}"
        do
            run_day ${day} ${solution_file}
            echo "${year},${day},${language},${runtime}" >> ../../runner/runtimes.csv
        done

        # Since this is being executed in a for loop then we need to make sure
        # to change out of the directory before running the next iteration
        popd > /dev/null
    done

    # Similar to running for each day, we need to change back out of the directory
    popd > /dev/null
done

python3 runner/display_runtimes.py
