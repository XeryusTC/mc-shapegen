#!/usr/bin/python3

import sys, math
import argparse
import export

def main(argv):
    parser = argparse.ArgumentParser(description='Voxel shape generator')
    parser.add_argument('shape', help='The shape to generate (options: cone, sphere)')
    parser.add_argument('output', help='File to write the resulting image to')
    parser.add_argument('-x', '--width', type=int, default=5, help='The width of the cone')
    parser.add_argument('-z', '--depth', type=int, default=5, help='The depth of the cone')
    parser.add_argument('-y', '--height', type=int, default=7, help='The height of the cone')
    parser.add_argument('-s', '--start', '--begin', type=int, metavar='S', default=0, help='The first layer of the output (default: 0)')
    parser.add_argument('-l', '--end', '--last', type=int, metavar='E', default=None, help='The last layer of the output (default: HEIGHT)')
    parser.add_argument('--voxel', type=int, help='The size of one voxel in the image')
    parser.add_argument('-o', '--hollow', action='store_true', default=False, help='Make the cone hollow')
    parser.add_argument('--hint', action='store_false', default=True, help='Turn of the display of hints in the image')
    parser.add_argument('-f', '--flip', action='store_true', default=False, help='Flip the shape onto its side')
    args = vars(parser.parse_args(argv))

    # Do some sanity checking
    if args['shape'] == 'cone':
        import cone
        to_generate = cone.Cone
    elif args['shape'] == 'sphere':
        import sphere
        to_generate = sphere.Sphere
    else:
        print('Wrong shape argument, see --help for usage')
        exit(1)
    if args['voxel'] is not None:
        export.IMAGE_VOXEL_SIZE = args['voxel']

    print ("Generating ", args['shape'], "...", sep='')
    s = to_generate(args['width'], args['depth'], args['height'])
    s.generate()
    if args['hollow']:
        s.hollow()

    if args['flip']:
        import flip
        s = flip.Flip(s)

    # This sanity checking is done here because it is influenced by flipping
    start_layer = args['start'] if args['start'] > 0 else 0
    end_layer = s.height if args['end'] == None else args['end']
    if start_layer == s.height:
        start_layer = s.height-1
    if end_layer > s.height:
        end_layer = s.height
    # this is last, if the start is the same as top then the end should be top+1 so there is still output
    if end_layer <= start_layer:
        end_layer = start_layer +1

    print("Number of blocks needed:", s.count_blocks(start_layer, end_layer))

    print("Exporting to ", args['output'], "...", sep='')
    image = export.ExportToImage()
    image.image(s, start_layer, end_layer)
    image.write(args['output'], args['hint'])
    print('Done!')

if __name__ == "__main__":
    main(sys.argv[1:])
