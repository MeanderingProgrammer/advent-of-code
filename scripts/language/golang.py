import os
from language.language import Language
from pojo.day import Day


class Go(Language):

    @property
    def name(self) -> str:
        return 'golang'
    
    @property
    def suffix(self) -> str:
        return '.go'

    def _run_setup(self):
        pass
    
    def compile(self, day: Day):
        # For now we use go run, which both compiles and runs our code
        pass
    
    def _do_run(self, day: Day):
        os.system('go run solver.go')
