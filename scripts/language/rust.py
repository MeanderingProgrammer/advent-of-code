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
    
    def _get_run_command(self, day: Day, is_test: bool) -> str:
        args = ''
        if is_test:
            args += '--test'
        return f'cargo run -rq --bin "aoc_{day.year}_{day.day}" -- {args}'
    
    def template_processing(self, day: Day):
        cargo = toml.load(_CARGO_FILE)
        bin_config = {
            'name': f'aoc_{day.year}_{day.day}', 
            'path': f'{day.year}/{day.day}/{self.solution_file}'
        }
        if bin_config in cargo['bin']:
            print('Do not need to update Cargo file')
            return

        cargo['bin'].append(bin_config)
        Rust.__save_cargo_file(cargo)

    @staticmethod
    def __save_cargo_file(cargo):
        f = open(_CARGO_FILE, 'w+')
        f.write(toml.dumps(cargo))
        f.close()
