setup_python() {
    # Setup PYTHONPATH so commons imports work
    export PYTHONPATH=$(pwd)
}

delete_java_classes() {
    find . -name '*class' | xargs rm -f
}

create_java_uber_jar() {
    jar="uber-jar.jar"

    delete_java_classes
    rm -f ${jar}

    class_files=()
    for class_file_path in "${@}"
    do
        class_file=$(basename $class_file_path)
        javac -cp "*" -d . ${class_file}.java
        class_files+=("${class_file_path}.class")
    done

    jar cf ${jar} ${class_files[@]}

    if [[ ! -f "${jar}" ]]
    then
        echo "Failed to create ${jar}"
        exit 1
    fi
}

# A hacky way to only build the jar once per execution of run script
is_java_setup="false"

setup_java() {
    delete_java_classes
    if [[ ${is_java_setup} == "false" ]]
    then
        pushd "../../commons/java" > /dev/null
        create_java_uber_jar "io/FileReader" "answer/Answer" "pojo/Position"
        popd > /dev/null
    fi
    is_java_setup="true"
}

# A hacky way to only build all binaries once per execution of run script
is_rust_setup="false"

setup_rust() {
    if [[ ${is_rust_setup} == "false" ]]
    then
        cargo build -rq --bins
    fi
    is_rust_setup="true"
}
