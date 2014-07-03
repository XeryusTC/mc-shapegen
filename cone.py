'''
Created on 19 Aug 2013

@author: xeryus
'''
from shape import *
import math

class Cone(Shape):
    def generate(self):
        #Calculate the centre
        origin_x = math.floor(self.width/2)
        origin_y = math.floor(self.depth/2)
        #Use a slight bit of extra offset for even cones
        if self.width % 2 == 0:
            origin_x -= 0.5
        if self.depth % 2 == 0:
            origin_y -= 0.5
        
        #Mark everything inside the cone as filled
        #Formula for cones is: (x**2 / a**2) + (y**2 / b**2) = ((h -z )**2) / h**2
        #Where (x, y, z) is the coordinate of the voxel. a is the width, b is the depth, h is the height
        for z in range(self.height):
            right = ((self.height - z)**2) / self.height**2
            for x in range(math.ceil(self.width/2)):
                for y in range(math.ceil(self.depth/2)):
                    left = ((origin_x - x)**2 / (self.width/2)**2) + ((origin_y - y )**2 / (self.depth/2)**2)
                    if left <= right:
                        self.shape[x][y][z] = FILLED
                        self.shape[self.width-x-1][y][z] = FILLED
                        self.shape[x][self.depth-y-1][z] = FILLED
                        self.shape[self.width-x-1][self.depth-y-1][z] = FILLED 