import os
from pathlib import Path
from language.language import Language
from pojo.day import Day

# Runs in <year>/<day> directory, hence the ../..
COMMONS_DIRECTORY = '../../commons/java'


class Java(Language):

    @property
    def name(self):
        return 'java'

    def _run_setup(self):
        os.environ['CLASSPATH'] = f'.:{COMMONS_DIRECTORY}/*'

        run_directory = os.getcwd()
        os.chdir(COMMONS_DIRECTORY)
        self._create_uber_jar([
            'io/FileReader',
            'answer/Answer',
            'pojo/Position',
        ])
        # Change back to directory we were running in
        os.chdir(run_directory)
    
    def _create_uber_jar(self, file_paths):
        uber_jar = 'uber-jar.jar'

        # Delete any previously generated class files to avoid masking failures
        self.__delete_classes()

        # Remove existing uber jar to avoid using old version on failure
        os.system(f'rm -f {uber_jar}')

        class_files = []
        for file_path in file_paths:
            # Include * in class path to use local jars, such as Lombok
            os.system(f'javac -cp "*" -d . {Path(file_path).stem}.java')
            class_files.append(f'{file_path}.class')
        
        # Create the uber jar and validate it was successfully created
        os.system(f'jar cf {uber_jar} {" ".join(class_files)}')
        if not Path(uber_jar).exists():
            raise Exception(f'Failed to generate Java uber jar: {uber_jar}')
    
    def compile(self):
        # Delete existing classes, that way if compiling fails nothing 
        # gets run, as opposed to runnning with previous artifacts
        self.__delete_classes()
        os.system(f'find . -name "*java" | xargs javac -d .')
    
    def __delete_classes(self):
        os.system('find . -name "*class" | xargs rm -f')
    
    def _do_run(self, day: Day):
        os.system(f'java main.Solver')
