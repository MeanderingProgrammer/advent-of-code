import os
from language.language import Language
from pojo.day import Day


class Go(Language):

    @property
    def name(self):
        return 'golang'

    def _run_setup(self):
        pass
    
    def compile(self):
        # For now we use go run, which both compiles and runs our code
        pass
    
    def _do_run(self, day: Day):
        os.system('go run solver.go')
