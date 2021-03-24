import numpy as np
from PIL import Image


class Layer:

    def __init__(self):
        self.data = []

    def add(self, row):
        row = [int(pixel) for pixel in row]
        self.data.append(row)

    def get_count(self, value):
        count = 0
        for row in self.data:
            for pixel in row:
                if pixel == value:
                    count += 1
        return count

    def get_pixel(self, r, c):
        return self.data[r][c]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.data)


class LayeredImage:

    def __init__(self, data, width, height):
        self.layers, self.width, self.height = [], width, height
        layer_size = width * height
        num_layers = len(data) // layer_size
        for l in range(num_layers):
            layer_start = l * layer_size
            layer = Layer()
            for h in range(height):
                row_start = (h * width) + layer_start
                row = data[row_start:row_start+width]
                layer.add(row)
            self.layers.append(layer)

    def get_fewest(self):
        counts = [layer.get_count(0) for layer in self.layers]
        min_index = counts.index(min(counts))
        return self.layers[min_index]

    def flatten_layers(self):
        flattened = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                pixel = self.get_pixel(r, c)
                row.append(pixel)
            flattened.append(row)
        return flattened

    def get_pixel(self, r, c):
        pixels = [layer.get_pixel(r, c) for layer in self.layers]
        for pixel in pixels:
            if pixel != 2:
                return pixel
        return 2

    def __str__(self):
        return str(self.layers)


def main():
    image = LayeredImage(get_image_data(), 25, 6)
    layer = image.get_fewest()
    # Part 1 = 1965
    print('Magic number = {}'.format(layer.get_count(1) * layer.get_count(2)))
    # Part 2 = GZKJY
    flattened = 255 * np.array(image.flatten_layers()).astype(np.uint8)
    Image.fromarray(flattened, mode='L').save('part-2.png')


def get_image_data():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return f.read()


if __name__ == '__main__':
    main()

