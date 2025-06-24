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
class Image:
    layers: list[Layer]
    width: int
    height: int

    def get_fewest(self) -> Layer:
        counts = [layer.get_count(0) for layer in self.layers]
        return self.layers[counts.index(min(counts))]

    def flatten(self) -> str:
        rows: list[str] = []
        for r in range(self.height):
            row = [self.get_pixel(r, c) for c in range(self.width)]
            rows.append("".join(row))
        return "\n".join(rows)

    def get_pixel(self, r: int, c: int) -> str:
        pixels = [layer.get_pixel(r, c) for layer in self.layers]
        pixel = next(pixel for pixel in pixels if pixel != 2)
        return "." if pixel == 0 else "#"


@answer.timer
def main() -> None:
    data = Parser().string()
    image = get_image(data, 25, 6)
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


def get_image(data: str, width: int, height: int) -> Image:
    layers: list[Layer] = []
    for layer_start in range(0, len(data), width * height):
        layer_data: list[list[int]] = []
        for h in range(height):
            start = layer_start + (h * width)
            row = data[start : start + width]
            layer_data.append(list(map(int, row)))
        layers.append(Layer(layer_data))
    return Image(layers, width, height)


if __name__ == "__main__":
    main()
