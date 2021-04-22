#!/usr/bin/env python3

"""
Extract a color scheme from a Lumatone mapping file
"""

import sys

KEYS_PER_SECTION = 56

input_filename = sys.argv[1]

pitches = [0] * 56
colors = ['000000'] * 56

with open(input_filename) as ltn:
    for line in ltn:
        if line.startswith('Key_') and line.count('=') == 1:
            key, pitch = line[4:].strip().split('=')
            pitches[int(key)] = int(pitch)
        elif line.startswith('Col_') and line.count('=') == 1:
            key, color = line[4:].strip().split('=')
            colors[int(key)] = color

for pitch, color in zip(pitches, colors):
    sys.stdout.write("{}={}\n".format(pitch, color))
