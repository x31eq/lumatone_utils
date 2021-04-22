#!/usr/bin/env python3

"""
Extract a color scheme from a Lumatone mapping file
"""

import argparse, sys

KEYS_PER_SECTION = 56

parser = argparse.ArgumentParser(
        description='Extract color scheme from a Lumatone .ltn mapping')
parser.add_argument('-p', '--period', type=int, nargs='?', default=128,
                    help='number of steps to a period/octave')
parser.add_argument('-t', '--tonic', type=int, nargs='?', default=0,
                    help='MIDI reference pitch')
parser.add_argument('-o', '--output', nargs='?',
                    help='file to write the scheme to')
parser.add_argument('input_filename')
args = parser.parse_args()

input_filename = args.input_filename

pitches = [0] * KEYS_PER_SECTION
colors = ['000000'] * KEYS_PER_SECTION

with open(args.input_filename) as ltn:
    for line in ltn:
        if line.startswith('Key_') and line.count('=') == 1:
            key, pitch = line[4:].strip().split('=')
            pitches[int(key)] = (int(pitch) - args.tonic) % args.period
        elif line.startswith('Col_') and line.count('=') == 1:
            key, color = line[4:].strip().split('=')
            if color != '000000':
                colors[int(key)] = color

scheme = ['000000'] * args.period
for pitch, color in zip(pitches, colors):
    scheme[pitch] = color

if args.output:
    with open(args.output, 'w') as result:
        for pitch, color in enumerate(scheme):
            result.write("{}\n".format(color))
else:
    for pitch, color in enumerate(scheme):
        sys.stdout.write("{}\n".format(color))
