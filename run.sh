#!/bin/bash

if [[ ${#} -ne 1 && ${#} -ne 2 ]]
then
    echo 'Usage: <year1,year2,...> <day1,day2,...>?'
    exit 1
fi

source ./language-setup.sh

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

    pushd ${day} > /dev/null

    solution_file=$(ls *olver* | tail -1)
    extension="${solution_file#*.}"

    echo "Running day ${day} with ${extension}"

    if [[ ${extension} == ${JAVA} ]]
    then
        setup_java

        # Runs in <year>/<day> directory, hence the ../..
        class_path=".:../../commons/java/*"
        find . -name '*java' | xargs javac -cp ${class_path} -d .
        time_run java -cp ${class_path} main.Solver
    elif [[ ${extension} == ${RUST} ]]
    then
      setup_rust
      time_run cargo run -rq --bin "aoc_${year}_${day}"
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

    # Since this is being executed in a for loop then we need to make sure
    # to change out of the directory before running the next iteration
    popd > /dev/null
}

# Store array of runtimes and days / years associated with each runtime
years_ran=()
days_ran=()
runtimes=()

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
        run_day ${day}
        years_ran+=(${year})
        days_ran+=(${day})
        runtimes+=(${runtime})
    done

    # Similar to running for each day, we need to change back out of the directory
    popd > /dev/null
done

green=$(tput setaf 2)
yellow=$(tput setaf 3)
red=$(tput setaf 1)
normal=$(tput sgr0)

set_color() {
    if (( $(echo "${1} < 0.5" | bc -l) ))
    then
        color=${green}
    elif (( $(echo "${1} < 1.5" | bc -l) ))
    then
        color=${normal}
    elif (( $(echo "${1} < 10.0" | bc -l) ))
    then
        color=${yellow}
    else
        color=${red}
    fi
}

# Generates a table with runtimes for all days / years
printf "\n"
printf "| Year | Day | Time (sec.) | \n"
printf "| ---- | --- | ----------- | \n"
for i in "${!runtimes[@]}"
do
    runtime=${runtimes[i]}
    set_color ${runtime}
    printf "${color}"
    printf "| %4.4s | %3.3s | %11.11s | \n" ${years_ran[i]} ${days_ran[i]} ${runtime}
done
