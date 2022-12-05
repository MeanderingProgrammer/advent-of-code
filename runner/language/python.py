import os
from language.language import Language
from pojo.day import Day


class Python(Language):

    @property
    def name(self):
        return 'python'

    def _run_setup(self):
        os.environ['PYTHONPATH'] = '{}/commons/python/'.format(os.environ['PWD'])
    
    def compile(self):
        # Python is an interpreted language, nothing to compile
        pass
    
    def run(self, day: Day):
        os.system('python3 solver.py')
