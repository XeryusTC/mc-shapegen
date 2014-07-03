'''
Created on 18 Aug 2013

@author: xeryus
'''
#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
from shape import FILLED, Shape
import math

IMAGE_VOXEL_SIZE = 10

EMPTY_COLOR = (255, 255, 255)
FILLED_COLOR = (255, 0, 0)
HINT_COLOR = (0, 0, 255)
CENTER_COLOR = (255, 255, 0)
TEXT_COLOR = (0, 0, 0)
COLOR_OFFSET = 24

class IllegalStateError(Exception):
    '''Gets raised when a part of the code has been invoked while initialization that is needed has not been done'''
    pass

class ExportToImage:
    def __init__(self):
        self.img = None
        self.draw = None

    def __repr__(self):
        return '<ExportToImage ' + str(self.__dict__) + '>'

    def image(self, shape, start, end):
        '''Initialises the image to draw, needs to be called first

        shape - the data that defines the 3D shape
        start - the first layer to draw
        end - the last layer to draw'''
        # Information about shape that has been generated
        self.shape = shape
        self.start = start
        self.end = end
        # determine the center layers (for the entire shape)
        if self.shape.height % 2 == 0:
            self.center = [self.shape.height / 2, self.shape.height / 2 - 1]
        else:
            self.center = [math.floor(self.shape.height / 2)]

        # Text for in the image (done before the image because the image size depends on the font and text size)
        self.font = ImageFont.load_default()
        self.info_text = self.text_info()
        self.height_offset = self.info_text.size[1] # text height

        # Create image
        self.img = Image.new('RGB', (max(self.shape.width * IMAGE_VOXEL_SIZE, self.info_text.size[0]),
                                     self.shape.depth * (self.end - self.start) * IMAGE_VOXEL_SIZE + self.height_offset), None)
        self.draw = ImageDraw.Draw(self.img)

    def text_info(self):
        lines = ["width (x):   " + str(self.shape.width),
            "height (y):  " + str(self.shape.height),
            "depth (z):   " + str(self.shape.depth),
            "block total: " + str(self.shape.count_blocks(self.start, self.end))]
        # receive char size and create a seperate image based on this
        line_width = 0
        char_height = 0
        for l in lines:
            width, char_height = self.font.getsize(l)
            if width > line_width:
                line_width = width
        text_image = Image.new('RGB', (max(line_width+1, self.shape.width * IMAGE_VOXEL_SIZE), len(lines) * char_height + 1), EMPTY_COLOR)
        text_draw = ImageDraw.Draw(text_image)

        # draw the text
        for i in range(len(lines)):
            text_draw.text((1, 1 + i * char_height), lines[i], TEXT_COLOR, self.font)
        return text_image

    def write(self, filename, hint=True):
        '''Writes the data to the disk

        filename - the name of the file to write to, include the extension!'''
        if self.img == None:
            raise IllegalStateError()
        self.draw_background()
        if hint:
            for z in range(self.end-self.start):
                self.draw_hint(z)
        for z in range(self.end-self.start):
            self.draw_layer(z)
            # draw layer number
            self.draw.text((1, z * self.shape.depth * IMAGE_VOXEL_SIZE + self.height_offset), str(z + self.start), fill=TEXT_COLOR, font=self.font)

        # add the info text to the image
        self.img.paste(self.info_text, (0, 0, self.info_text.size[0], self.info_text.size[1]))

        self.img.save(filename)

    def _image_coordinates(self, x, y, z):
        '''Converts the coordinates of a voxel to a square in the image

        (x, y, z) - the coordinate of the voxel in the data'''
        x1 = x * IMAGE_VOXEL_SIZE
        x2 = x1 + IMAGE_VOXEL_SIZE - 1
        y1 = (y + z * self.shape.depth) * IMAGE_VOXEL_SIZE
        y2 = y1 + IMAGE_VOXEL_SIZE - 1
        return ((x1, y1 + self.height_offset), (x2, y2 + self.height_offset))

    def _get_color(self, x, y, z, base_color, offset = COLOR_OFFSET):
        '''Gets the appropriate color for a voxel to be drawn on the image

        (x, y, z) - The voxel to draw
        base_color - The color that the voxel should have, this will be altered based on the voxel's position'''
        color = base_color if (x + y + z) % 2 else (max(c - offset, 0) for c in base_color)
        if z % 2:
            color = (max(c - offset * 2, 0) for c in color)
        return tuple(color)

    def draw_to_image(self, coords, color):
        '''Helper function that actually does the drawing'''
        self.draw.rectangle(coords, fill=color, outline=color)

    def draw_background(self):
        '''Draws the background for the image with alternating colors'''
        if self.img == None or self.draw == None:
            raise IllegalStateError()
        #Start drawing
        for z in range(self.end-self.start):
            if z + self.start in self.center:
                color = CENTER_COLOR
            else:
                color = EMPTY_COLOR
            for y in range(self.shape.depth):
                for x in range(self.shape.width):
                    self.draw_to_image(self._image_coordinates(x, y, z), self._get_color(x, y, z, color))

    def draw_layer(self, layer):
        for x in range(self.shape.width):
            for y in range(self.shape.depth):
                if self.shape.shape[x][y][layer + self.start] == FILLED:
                    self.draw_to_image(self._image_coordinates(x, y, layer), self._get_color(x, y, layer, FILLED_COLOR, int(COLOR_OFFSET*1.5)))

    def draw_hint(self, layer):
        if layer == 0:
            return
        for x in range(self.shape.width):
            for y in range(self.shape.depth):
                if self.shape.shape[x][y][layer + self.start - 1] == FILLED:
                    self.draw_to_image(self._image_coordinates(x, y, layer), self._get_color(x, y, layer, HINT_COLOR, int(COLOR_OFFSET*1.5)))

if __name__ == '__main__':
    print('This is a helper file and it should not be called directly')
    img = ExportToImage()
    s = Shape(2, 3, 3)
    s.shape = [[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]]
    img.image(s, 0, 3)
    img.write('test2.png')
