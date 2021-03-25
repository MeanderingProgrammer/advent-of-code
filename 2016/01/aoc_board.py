class Point:

    def __init__(self, *coords):
        self.coords = coords

    def reflect(self):
        return Point(-self.coords[0], self.coords[1])

    def rotate(self):
        return Point(-self.coords[1], self.coords[0])

    def adjacent(self):
        adjacent = []

        for i in range(len(self.coords)):
            coords_c1 = list(self.coords)
            coords_c1[i] -= 1
            adjacent.append(Point(*coords_c1))

            coords_c2 = list(self.coords)
            coords_c2[i] += 1
            adjacent.append(Point(*coords_c2))

        return adjacent

    def validate(self, o):
        if len(self.coords) != len(o.coords):
            raise Exception('Cannot compare points of different dimensionality')

    def __len__(self):
        return sum([abs(c) for c in self.coords])

    def __add__(self, o):
        self.validate(o)
        coords = []
        for c1, c2 in zip(self.coords, o.coords):
            coords.append(c1 + c2)
        return Point(*coords)

    def __sub__(self, o):
        self.validate(o)
        coords = []
        for c1, c2 in zip(self.coords, o.coords):
            coords.append(c1 - c2)
        return Point(*coords)

    def __mul__(self, o):
        coords = []
        for c in self.coords:
            coords.append(o * c)
        return Point(*coords)

    def __rmul__(self, o):
        return self.__mul__(o)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, o):
        self.validate(o)
        matches = []
        for c1, c2 in zip(self.coords, o.coords):
            matches.append(c1 < c2)
        return all(matches)

    def __le__(self, o):
        self.validate(o)
        matches = []
        for c1, c2 in zip(self.coords, o.coords):
            matches.append(c1 <= c2)
        return all(matches)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.coords)
