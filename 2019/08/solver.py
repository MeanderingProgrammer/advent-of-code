from commons.aoc_parser import Parser


class Layer:

    def __init__(self):
        self.data = []

    def add(self, row):
        row = [int(pixel) for pixel in row]
        self.data.append(row)

    def get_count(self, value):
        return sum([pixel == value for row in self.data for pixel in row])

    def get_pixel(self, r, c):
        return self.data[r][c]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.data)


class LayeredImage:

    def __init__(self, data, width, height):
        self.layers = []
        self.width, self.height = width, height

        layer_size = width * height
        for l in range(len(data) // layer_size):
            layer_start = l * layer_size
            layer = Layer()
            for h in range(height):
                row_start = (h * width) + layer_start
                row = data[row_start:row_start+width]
                layer.add(row)
            self.layers.append(layer)

    def get_fewest(self):
        counts = [layer.get_count(0) for layer in self.layers]
        return self.layers[counts.index(min(counts))]

    def flatten(self):
        rows = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                row.append(self.get_pixel(r, c))
            rows.append(''.join(row))
        return '\n'.join(rows)

    def get_pixel(self, r, c):
        pixels = [layer.get_pixel(r, c) for layer in self.layers]
        pixel = next(pixel for pixel in pixels if pixel != 2)
        return '.' if pixel == 0 else '#'

    def __str__(self):
        return str(self.layers)


def main():
    image = LayeredImage(get_image_data(), 25, 6)
    layer = image.get_fewest()
    # Part 1: 1965
    print('Part 1: {}'.format(layer.get_count(1) * layer.get_count(2)))
    # Part 2: GZKJY
    print(image.flatten())


def get_image_data():
    return Parser().string()


if __name__ == '__main__':
    main()
