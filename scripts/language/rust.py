import os
from language.language import Language
from pojo.day import Day


class Rust(Language):

    @property
    def name(self) -> str:
        return 'rust'
    
    @property
    def suffix(self) -> str:
        return '.rs'

    def _run_setup(self):
        os.system('cargo build -rq --bins')
    
    def compile(self, day: Day):
        # Since our setup command builds all binary targets, each day does not
        # need to be individually compiled
        pass
    
    def _do_run(self, day: Day):
        os.system(f'cargo run -rq --bin "aoc_{day.year}_{day.day}"')
