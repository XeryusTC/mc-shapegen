'''
Created on 19 Aug 2013

@author: xeryus
'''
from shape import *
import math

class Sphere(Shape):
    def generate(self):
        # Calculate the centre of the sphere (the origin)
        origin_x = math.floor(self.width/2)
        origin_y = math.floor(self.depth/2)
        origin_z = math.floor(self.height/2)
        # Use a slightly different offset for even widths
        origin_x -= 0.5 if self.width % 2 == 0 else 0
        origin_y -= 0.5 if self.depth % 2 == 0 else 0
        origin_z -= 0.5 if self.height % 2 == 0 else 0
        
        for x in range(math.ceil(self.width/2)):
            x2 = self.width - x - 1
            for y in range(math.ceil(self.depth/2)):
                y2 = self.depth - y - 1
                for z in range(math.ceil(self.height/2)):
                    z2 = self.height - z - 1
                    if ((origin_x - x)**2 / (self.width / 2)**2) \
                    +  ((origin_y - y)**2 / (self.depth / 2)**2) \
                    +  ((origin_z - z)**2 / (self.height/ 2)**2)  <= 1:
                        self.shape[x ][y ][z ] = FILLED
                        self.shape[x2][y ][z ] = FILLED
                        self.shape[x ][y2][z ] = FILLED
                        self.shape[x2][y2][z ] = FILLED
                        self.shape[x ][y ][z2] = FILLED
                        self.shape[x2][y ][z2] = FILLED
                        self.shape[x ][y2][z2] = FILLED
                        self.shape[x2][y2][z2] = FILLED