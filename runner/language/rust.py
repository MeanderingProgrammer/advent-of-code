import os
from language.language import Language
from pojo.day import Day


class Rust(Language):

    @property
    def name(self):
        return 'rust'

    def _run_setup(self):
        os.system('cargo build -rq --bins')
    
    def compile(self):
        # Since our setup command builds all binary targets, each day does not
        # need to be individually compiled
        pass
    
    def run(self, day: Day):
        os.system(f'cargo run -rq --bin "aoc_{day.year}_{day.day}"')
