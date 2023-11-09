from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Layer:
    data: list[list[int]]

    def get_count(self, value: int) -> int:
        return sum([pixel == value for row in self.data for pixel in row])

    def get_pixel(self, r: int, c: int) -> int:
        return self.data[r][c]


@dataclass(frozen=True)
class LayeredImage:
    layers: list[Layer]
    width: int
    height: int

    def get_fewest(self) -> Layer:
        counts = [layer.get_count(0) for layer in self.layers]
        return self.layers[counts.index(min(counts))]

    def flatten(self) -> str:
        rows = []
        for r in range(self.height):
            row = [self.get_pixel(r, c) for c in range(self.width)]
            rows.append("".join(row))
        return "\n".join(rows)

    def get_pixel(self, r: int, c: int) -> str:
        pixels = [layer.get_pixel(r, c) for layer in self.layers]
        pixel = next(pixel for pixel in pixels if pixel != 2)
        return "." if pixel == 0 else "#"


def main() -> None:
    image = get_image(25, 6)
    layer = image.get_fewest()
    answer.part1(1965, layer.get_count(1) * layer.get_count(2))
    expected = [
        ".##..####.#..#...##.#...#",
        "#..#....#.#.#.....#.#...#",
        "#......#..##......#..#.#.",
        "#.##..#...#.#.....#...#..",
        "#..#.#....#.#..#..#...#..",
        ".###.####.#..#..##....#..",
    ]
    answer.part2("\n" + "\n".join(expected), "\n" + image.flatten())


def get_image(width: int, height: int) -> LayeredImage:
    data = Parser().string()
    layers = []
    layer_size = width * height
    for l in range(len(data) // layer_size):
        layer_start = l * layer_size
        layer_data = []
        for h in range(height):
            row_start = (h * width) + layer_start
            row = data[row_start : row_start + width]
            layer_data.append(list(map(int, row)))
        layers.append(Layer(layer_data))
    return LayeredImage(layers, width, height)


if __name__ == "__main__":
    main()
