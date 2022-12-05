import os
from language.language import InterprettedLanguage
from pojo.day import Day


class Python(InterprettedLanguage):

    @property
    def name(self):
        return 'python'

    def _run_setup(self):
        pwd = os.environ['PWD']
        os.environ['PYTHONPATH'] = f'{pwd}/commons/python/'
    
    def _do_run(self, day: Day):
        os.system('python3 solver.py')
