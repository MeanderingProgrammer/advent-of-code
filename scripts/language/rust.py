import os
import toml
from language.language import Language
from pojo.day import Day

_CARGO_FILE = 'Cargo.toml'


class Rust(Language):

    @property
    def name(self) -> str:
        return 'rust'
    
    @property
    def solution_file(self) -> str:
        return 'solver.rs'

    def _run_setup(self):
        os.system('cargo build -rq --bins')
    
    def compile(self, day: Day):
        # Since our setup command builds all binary targets, each day does not
        # need to be individually compiled
        pass
    
    def _do_run(self, day: Day):
        os.system(f'cargo run -rq --bin "aoc_{day.year}_{day.day}"')
    
    def template_processing(self, day: Day):
        cargo = toml.load(_CARGO_FILE)
        bin_config = {
            'name': f'aoc_{day.year}_{day.day}', 
            'path': f'{day.year}/{day.day}/{self.solution_file}'
        }
        cargo['bin'].append(bin_config)

        f = open(_CARGO_FILE, 'w+')
        f.write(toml.dumps(cargo))
        f.close()