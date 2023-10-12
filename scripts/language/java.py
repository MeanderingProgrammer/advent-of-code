import os
from pathlib import Path
from typing import List

from language.language import Language
from pojo.day import Day

# Runs in <year>/<day> directory, hence the ../..
COMMONS_DIRECTORY = "../../commons/java"
CLASS_PATH = f".:{COMMONS_DIRECTORY}/*"


class Java(Language):
    @property
    def name(self) -> str:
        return "java"

    @property
    def solution_file(self) -> str:
        return "Solver.java"

    def _run_setup(self):
        run_directory = os.getcwd()
        os.chdir(COMMONS_DIRECTORY)
        self._create_uber_jar(
            [
                "io/FileReader",
                "answer/Answer",
                "pojo/Position",
            ]
        )
        # Change back to directory we were running in
        os.chdir(run_directory)

    def _create_uber_jar(self, file_paths: List[str]) -> None:
        uber_jar = "uber-jar.jar"

        # Delete any previously generated class files to avoid masking failures
        self.__delete_classes()

        # Remove existing uber jar to avoid using old version on failure
        os.system(f"rm -f {uber_jar}")

        class_files = []
        for file_path in file_paths:
            # Include * in class path to use local jars, such as Lombok
            os.system(f"javac -cp '*' -d . {Path(file_path).stem}.java")
            class_files.append(f"{file_path}.class")

        # Create the uber jar and validate it was successfully created
        os.system(f'jar cf {uber_jar} {" ".join(class_files)}')
        if not Path(uber_jar).exists():
            raise Exception(f"Failed to generate Java uber jar: {uber_jar}")

    def compile(self, day: Day):
        # Delete existing classes, that way if compiling fails nothing
        # gets run, as opposed to runnning with previous artifacts
        self.__delete_classes()
        os.system(f"find . -name '*java' | xargs javac -cp {CLASS_PATH} -d .")

    def __delete_classes(self):
        os.system("find . -name '*class' | xargs rm -f")

    def _get_run_command(self, day: Day, run_args: List[str]) -> str:
        return f"java -cp {CLASS_PATH} main.Solver"

    def template_processing(self, day: Day):
        # No additional template processing needed
        pass
