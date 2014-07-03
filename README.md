Minecraft Shape Generator
===========

Generates complex three dimensional voxel shapes so they can be build in Minecraft. Currently only cones and spheres are supported, these shapes are always watertight, meaning that if the shape were to be filled with water that none of it would flow out.

The output of the program is an image file that shows the shape split into layers with the first layer being the bottom layer and every subsequent layer being on top of the previous layer. It shows the previous layer relative to the current layer so it easier to identify their relation.

Requirements
============

The following are needed to run this software: python 3.2.3 or higher and Pillow 2.4.0 or higher. It might be possible to run with older versions but it is currently untested.

Usage
=====

Command line options
--------------------
There are two required positional options:

1. `shape` The shape that is generated, currently this can either be 'cone' or 'sphere'
2. `output` Where the output is stored. This is an image of any format that is supported by Pillow (PNG is recommended).

The following options are optional, most have a long name and a short name:
* `--width` `-x` The width of the shape to be generated, usually the x coordinate in Minecraft. This is the diameter in the x direction. Default is 5.
* `--height` `-y` The height of the shape to be generated, usually the y coordinate in Minecraft. This is the diameter in the y direction for spheres and the height for cones. Default is 7.
* `--depth` `-z` The depth of the shape to be generated, usually the z coordinate in Minecraft. This is the diameter in the z direction. Default is 5.
* `--start` `--begin` `-s` The first layer of the shape to draw. Default is 0.
* `--end` `--last` `-l` The last layer of the shape to draw. Default is the same as height, the last layer.
* `--voxel` The size in pixels that a voxel is drawn in the output image. Mainly has an impact on image size. Default is 10.
* `--hollow` `-o` Removes voxels inside the sphere to make it hollow but still makes sure that it is water tight. Lowers the block count and can make it easier to read the shape. Defaults to fill the shape.
* `--hint` Turns the display of the hint in the output off. The hint shows the previous layer relative to the current one.
* `--flip` `-f` Flips the shape on its side by exchanging the z and y axis.
