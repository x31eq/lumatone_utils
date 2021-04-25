#!/usr/bin/env python3

"""
Apply a color scheme to a Lumatone mapping file
"""

import argparse, sys

N_BOARDS = 5
KEYS_PER_BOARD = 56

parser = argparse.ArgumentParser(
        description='Apply a color scheme to a Lumatone .ltn mapping')
parser.add_argument('-t', '--tonic', type=int, nargs='?', default=0,
                    help='MIDI reference pitch')
parser.add_argument('-g', '--gap', type=int, nargs='?', default=0,
                    help='Notes to offset from one channel to another')
parser.add_argument('-i', '--input', nargs='?',
                    help='file to read the color scheme from')
parser.add_argument('-o', '--output', nargs='?',
                    help='file to write the altered mapping to')
parser.add_argument('mapping_filename')
args = parser.parse_args()

if args.input:
    with open(args.input) as scheme_file:
        scheme = list(filter(None,
            (line.strip() for line in scheme_file)))
else:
    scheme = list(filter(None, (line.strip() for line in sys.stdin)))

period = len(scheme)

if args.mapping_filename:
    with open(args.mapping_filename) as mapping:
        lines = list(filter(None, (line.strip() for line in mapping)))
else:
    lines = list(filter(None,
        (line.strip() for line in sys.stdin)))

pitches = [[0] * KEYS_PER_BOARD for _ in range(N_BOARDS)]
channels = [[0] * KEYS_PER_BOARD for _ in range(N_BOARDS)]

board = 0
for line in lines:
    if line.startswith('[Board'):
        board = int(line[6])
    elif line.startswith('Key_') and line.count('=') == 1:
        key, pitch = line[4:].strip().split('=')
        pitches[board][int(key)] = int(pitch)
    elif line.startswith('Chan_') and line.count('=') == 1:
        key, channel = line[5:].strip().split('=')
        channel = int(channel)
        if channel:
            channels[board][int(key)] = channel

board = 0
output = open(args.output, 'w') if args.output else sys.stdout
for line in lines:
    if line.startswith('[Board'):
        board = int(line[6])
    if line.startswith('Col_') and line.count('=') == 1:
        key, _color = line[4:].strip().split('=')
        key = int(key)
        channel = channels[board][key] - 1
        pitch = pitches[board][key] + (channel * args.gap)
        color = scheme[(pitch - args.tonic) % period]
        line = "Col_{}={}".format(key, color)
    output.write(line + '\n')
