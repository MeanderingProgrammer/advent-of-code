class Parser:

    def __init__(self, file_name):
        self.file_name = '{}.txt'.format(file_name)

    def string(self):
        return self.__read(split=False)

    def entries(self):
        return self.__read()

    def int_entries(self):
        return self.__to_int(self.entries())

    def csv(self):
        return self.__read(sep=',')

    def int_csv(self):
        return self.__to_int(self.csv())

    def lines(self):
        return self.__read(sep='\n')

    def int_lines(self):
        return self.__to_int(self.lines())

    def nested_lines(self):
        return [[value for value in line] for line in self.lines()]
    
    def line_groups(self):
        return [group.split('\n') for group in self.__read(sep='\n\n')]

    def __read(self, split=True, sep=None):
        with open(self.file_name, 'r') as f:
            data = f.read()
        return data.split(sep) if split else data

    @staticmethod
    def __to_int(values):
        return [int(value) for value in values]

