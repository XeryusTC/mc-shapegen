'''
Created on 18 Aug 2013

@author: xeryus
'''
#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
from shape import FILLED

IMAGE_VOXEL_SIZE = 10

EMPTY_COLOR = (255, 255, 255)
FILLED_COLOR = (255, 0, 0)
HINT_COLOR = (0, 0, 255)
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

        data - the data that defines the 3D shape
        start - the first layer to draw
        end - the last layer to draw'''
        # Information about shape that has been generated
        self.shape = shape
        self.start = start
        self.end = end

        # Text for in the image (done before the image because the image size depends on the font and text size)
        self.font = ImageFont.load_default()
        self.info_text = self.text_info()
        self.height_offset = self.info_text.size[1] # text height

        # Create image
        self.img = Image.new('RGB', (self.shape.width * IMAGE_VOXEL_SIZE,
                                     self.shape.depth * (self.end - self.start) * IMAGE_VOXEL_SIZE + self.height_offset), None)
        self.draw = ImageDraw.Draw(self.img)

    def text_info(self):
        # receive char size and create a seperate image based on this
        char_width, char_height = self.font.getsize("M")
        text_image = Image.new('RGB', (self.shape.width * IMAGE_VOXEL_SIZE, 4 * char_height+1), EMPTY_COLOR) # 4 = amount of lines
        text_draw = ImageDraw.Draw(text_image)

        # draw the text
        text_draw.text((1, 1),             "width (x):  " + str(self.shape.width),  font=self.font, fill=TEXT_COLOR)
        text_draw.text((1, 1+char_height),   "height (y): " + str(self.shape.height), font=self.font, fill=TEXT_COLOR)
        text_draw.text((1, 1+2*char_height), "depth (z):  " + str(self.shape.depth),  font=self.font, fill=TEXT_COLOR)
        text_draw.text((1, 1+3*char_height), "blocks:     " + str(self.shape.count_blocks(self.start, self.end)), font=self.font, fill=TEXT_COLOR)
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
            self.draw.text((1, z * self.shape.depth * IMAGE_VOXEL_SIZE + self.height_offset), str(z), fill=TEXT_COLOR, font=self.font)

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
            for y in range(self.shape.depth):
                for x in range(self.shape.width):
                    self.draw_to_image(self._image_coordinates(x, y, z), self._get_color(x, y, z, EMPTY_COLOR))

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
    img.image([[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]], 0, 3)
    img.write('test2.png')
