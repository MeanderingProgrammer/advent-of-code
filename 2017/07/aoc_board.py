class Graph:

    def __init__(self):
        self.graph = {}
        self.to_change = None

    def add_node(self, node):
        self.graph[node] = set()

    def add_edge(self, node, edge):
        self.graph[node].add(edge)

    def top_most(self):
        all_ids = set([node.id for node in self.graph])
        are_dependencies = set([value for values in self.graph.values() for value in values])

        top_most = all_ids - are_dependencies
        if len(top_most) == 1:
            return next(iter(top_most))

    def get_weight(self, node):
        total_weight = node.weight

        edges = self.graph[node]

        weight_edges = {}

        seen_bad = False

        for edge in edges:
            edge_node = self.get_node(edge)
            edge_weight, seen = self.get_weight(edge_node)

            seen_bad |= seen

            if edge_weight not in weight_edges:
                weight_edges[edge_weight] = set()
            weight_edges[edge_weight].add(edge_node)

            total_weight += edge_weight

        if len(weight_edges) == 2 and not seen_bad:
            seen_bad = True

            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    bad_weight = weight
                else:
                    good_weight = weight

            amount = good_weight - bad_weight

            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    change = next(iter(edges))
                    weight = change.weight
                    self.to_change = weight + amount

        return total_weight, seen_bad

    def get_node(self, node_id):
        for node in self.graph:
            if node.id == node_id:
                return node

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.graph)

class Grid:

    def __init__(self):
        self.grid = {}

    def get(self, point, default_value):
        return self[point] if point in self else default_value

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def xs(self):
        return [point.coords[0] for point in self.grid]

    def ys(self):
        return [point.coords[1] for point in self.grid]

    def __setitem__(self, point, value):
        self.grid[point] = value

    def __getitem__(self, point):
        return self.grid.get(point, None)

    def __contains__(self, point):
        return point in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        xs, ys = self.xs(), self.ys()

        if len(xs) == 0 or len(ys) == 0:
            return ''

        rows = []
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                point = Point(x, y)
                value = str(self[point]) if point in self else '.'
                row.append(value)                
            rows.append(''.join(row))

        return '\n'.join(rows)


class Point:

    def __init__(self, *coords):
        self.coords = coords

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
