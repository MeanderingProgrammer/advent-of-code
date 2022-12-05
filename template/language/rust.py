import toml

from language.language import Language

_CARGO_FILE = 'Cargo.toml'

class Rust(Language):

    @property
    def name(self) -> str:
        return 'rust'
    
    @property
    def solution_file(self) -> str:
        return 'solver.rs'
    
    def additional_processing(self, year: str, day: str):
        cargo = toml.load(_CARGO_FILE)
        bin_config = {
            'name': f'aoc_{year}_{day}', 
            'path': f'{year}/{day}/{self.solution_file}'
        }
        cargo['bin'].append(bin_config)

        f = open(_CARGO_FILE, 'w+')
        f.write(toml.dumps(cargo))
        f.close()
