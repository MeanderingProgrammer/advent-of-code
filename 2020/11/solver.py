import commons.answer as answer
from commons.aoc_parser import Parser


class Seat:

    def __init__(self, i, j, state):
        self.row = i
        self.col = j
        self.state = state

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_state(self):
        return self.state

    def is_occupied(self):
        return self.state == '#'

    def is_empty(self):
        return self.state == 'L'

    def is_floor(self):
        return self.state == '.'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.state


class SeatingChart:

    def __init__(self, chart, transform=True):
        if transform:
            self.chart = []
            for i, row in enumerate(chart):
                seats = []
                for j, state in enumerate(row):
                    seats.append(Seat(i, j, state))
                self.chart.append(seats)
        else:
            self.chart = chart

    def step_forward(self, look):
        next_chart = []
        for row in self.chart:
            next_row = []
            for seat in row:
                next_state = seat.get_state()
                if not seat.is_floor():
                    adjacent_seats = self.get_adjacent_seats(seat, look)
                    occupied = [adjacent_seat.is_occupied() for adjacent_seat in adjacent_seats]
                    if seat.is_empty():
                        if not any(occupied):
                            next_state = '#'
                    else:
                        to_empty = 5 if look else 4
                        if sum(occupied) >= to_empty:
                            next_state = 'L'
                next_row.append(Seat(seat.get_row(), seat.get_col(), next_state))
            next_chart.append(next_row)
        return SeatingChart(next_chart, False)

    def get_adjacent_seats(self, seat, look):
        seats = []

        directions = [-1, 0, 1]
        for d1 in directions:
            for d2 in directions:
                if d1 != 0 or d2 != 0:
                    row = seat.get_row()+d1
                    col = seat.get_col()+d2
                    adjacent_seat = self.explore_direction(row, col, (d1, d2), look)
                    if adjacent_seat is not None and not adjacent_seat.is_floor():
                        seats.append(adjacent_seat)

        return seats

    def explore_direction(self, i, j, direc, look):
        if i < 0 or j < 0:
            return None
        if i >= len(self.chart):
            return None
        if j >= len(self.chart[i]):
            return None

        seat = self.chart[i][j]
        if not look:
            return seat

        if not seat.is_floor():
            return seat
            
        i += direc[0]
        j += direc[1]
        return self.explore_direction(i, j, direc, look)

    def count_occupied(self):
        occupied = 0
        for row in self.chart:
            for seat in row:
                if seat.is_occupied():
                    occupied += 1
        return occupied

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = ''
        for row in self.chart:
            result += str(row) + '\n'
        return result


def main():
    answer.part1(2386, run_until_stable(False))
    answer.part2(2091, run_until_stable(True))


def run_until_stable(look):
    current_chart = process()
    next_chart = current_chart.step_forward(look)

    while not current_chart == next_chart:
        current_chart = next_chart
        next_chart = next_chart.step_forward(look)

    return current_chart.count_occupied()


def process():
    return SeatingChart(Parser().nested_lines())


if __name__ == '__main__':
    main()
