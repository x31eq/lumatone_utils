#!/usr/bin/env python3

"""
Make a color scheme for a generated scale
"""

import argparse, sys, xml.etree.ElementTree

parser = argparse.ArgumentParser(
        description='Generate a color scheme')

parser.add_argument('-o', '--output', nargs='?',
                    help='file to write the altered mapping to')
parser.add_argument('palette',
                    help='Lumatone palette file the colors come from')
parser.add_argument('generator',
                    help="Generator as n/d")
parser.add_argument('scheme', type=int, nargs='+',
                    help="Colors by generator as indexes into the palette")

args = parser.parse_args()

tree = xml.etree.ElementTree.parse(args.palette)
palette = [swatch.attrib['Colour'][-6:]
            for swatch in tree.getroot().findall('Swatch')]
colours = args.scheme

generator, period = map(int, args.generator.split('/'))

scheme = ['000000'] * period
for note in range(period):
    index = (generator * note) % period
    color = colours[note] if note < len(colours) else colours[period - note]
    scheme[index] = palette[color]

output = open(args.output, 'w') if args.output else sys.stdout
for color in scheme:
    output.write(color + '\n')
