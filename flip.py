'''
Created on 19 Aug 2013

@author: xeryus
'''
from shape import Shape

class Flip(Shape):
    def __init__(self, shape):
        super().__init__(shape.width, shape.height, shape.depth)
        
        for x in range(self.width):
            for y in range(self.depth):
                for z in range(self.height):
                    self.shape[x][y][z] = shape.shape[x][z][y]