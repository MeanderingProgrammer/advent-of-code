import os
from language.language import InterprettedLanguage
from pojo.day import Day


class Python(InterprettedLanguage):

    @property
    def name(self) -> str:
        return 'python'
    
    @property
    def solution_file(self) -> str:
        return 'solver.py'

    def _run_setup(self):
        pwd = os.getcwd()
        os.environ['PYTHONPATH'] = f'{pwd}/commons/python/'
    
    def _do_run(self, day: Day, is_test: bool):
        os.system('python3 solver.py')
    
    def template_processing(self, day: Day):
        # No additional template processing needed
        pass
