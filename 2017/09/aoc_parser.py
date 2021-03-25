class Parser:

    def __init__(self, file_name):
        self.file_name = '{}.txt'.format(file_name)

    def lines(self):
        data = self.read()
        return data.split('\n')

    def int_lines(self):
        return [int(line) for line in self.lines()]
    
    def line_groups(self):
        data = self.read()
        return [group.split('\n') for group in data.split('\n\n')]

    def nested_array(self):
        return [[value for value in line] for line in self.lines()]

    def int_entries(self):
        return [int(entry) for entry in self.read().split()]

    def read(self):
        with open(self.file_name, 'r') as f:
            return f.read()
