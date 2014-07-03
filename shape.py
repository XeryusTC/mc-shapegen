'''
Created on 19 Aug 2013

@author: xeryus
'''
EMPTY, FILLED, HOLLOW = range(3)

class Shape:
    def __init__(self, width, depth, height):
        self.width = width
        self.depth = depth
        self.height = height

        # Create the 3D shape
        self.shape = []
        for x in range(self.width):
            plane = []
            for y in range(self.depth):
                line = []
                for z in range(self.height):
                    line.append(EMPTY)
                plane.append(line)
            self.shape.append(plane)

    def generate(self):
        raise NotImplementedError()

    def hollow(self):
        for x in range(self.width):
            for y in range(self.depth):
                for z in range(self.height):
                    if not self.borders_empty(x, y, z):
                        self.shape[x][y][z] = HOLLOW

    def borders_empty(self, x, y, z):
        # Borders should always be filled
        if not 0 < x < self.width -1:
            return True
        if not 0 < y < self.depth -1:
            return True
        if z in (0, self.height -1):
            return True
        #Check all directly bordering voxels
        pattern = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1))
        if z != 0: # Add the layer under the current one if it exists
            pattern = pattern + ((0, 0, -1),)

        for d in pattern:
            if self.shape[x+d[0]][y+d[1]][z+d[2]] == EMPTY:
                return True
        return False

    def count_blocks(self, start, end):
        count = 0
        for z in range(end-start):
            for x in range(self.width):
                for y in range(self.depth):
                    if self.shape[x][y][start+z] == FILLED:
                        count += 1
        return count
