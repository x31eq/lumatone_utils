#!/usr/bin/env python3

"""
Extract a color scheme from a Lumatone mapping file
"""

import argparse, sys

N_BOARDS = 5
KEYS_PER_BOARD = 56

parser = argparse.ArgumentParser(
        description='Extract the color scheme from a Lumatone .ltn mapping')
parser.add_argument('-p', '--period', type=int, nargs='?', default=128,
                    help='number of steps to a period/octave')
parser.add_argument('-t', '--tonic', type=int, nargs='?', default=0,
                    help='MIDI reference pitch')
parser.add_argument('-g', '--gap', type=int, nargs='?', default=0,
                    help='Notes to offset from one channel to another')
parser.add_argument('-o', '--output', nargs='?',
                    help='file to write the scheme to')
parser.add_argument('input_filename')
args = parser.parse_args()

pitches = [[0] * KEYS_PER_BOARD for _ in range(N_BOARDS)]
channels = [[0] * KEYS_PER_BOARD for _ in range(N_BOARDS)]
colors = [[None] * KEYS_PER_BOARD for _ in range(N_BOARDS)]

board = 0
with open(args.input_filename) as ltn:
    for line in ltn:
        if line.startswith('[Board'):
            board = int(line[6])
        elif line.startswith('Key_') and line.count('=') == 1:
            key, pitch = line[4:].strip().split('=')
            pitches[board][int(key)] = int(pitch)
        elif line.startswith('Col_') and line.count('=') == 1:
            key, color = line[4:].strip().split('=')
            if color != '000000':
                colors[board][int(key)] = color
        elif line.startswith('Chan_') and line.count('=') == 1:
            key, channel = line[5:].strip().split('=')
            channel = int(channel)
            if channel:
                channels[board][int(key)] = channel

scheme = [None] * args.period
for board, keyspecs in enumerate(zip(pitches, channels, colors)):
    for pitch, channel, color in zip(*keyspecs):
        if channel and color:
            relative_pitch = (pitch + channel * args.gap) - args.tonic
            relative_pitch %= args.period
            old_color = scheme[relative_pitch]
            if old_color and old_color != color:
                sys.stderr.write(
                        "Inconsistent color board {}, channel {}, pitch {}, "
                        "relative pitch {}, color {}, old color {}\n"
                                .format(board, channel, pitch, relative_pitch,
                                    color, old_color))
            else:
                scheme[relative_pitch] = color

if args.output:
    with open(args.output, 'w') as result:
        for pitch, color in enumerate(scheme):
            result.write("{}\n".format(color or '000000'))
else:
    for pitch, color in enumerate(scheme):
        sys.stdout.write("{}\n".format(color or '000000'))
