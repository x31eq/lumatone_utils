#!/usr/bin/env python3

import sys

for filename in sys.argv[1:]:
    with open(filename) as input_file:
        output_filename = filename.replace('.ltn', '_dim.ltn')
        with open(output_filename, 'w', newline=('\r\n')) as output_file:
            for line in input_file:
                if line.startswith('Col_'):
                    prefix, color = line.strip().split('=')
                    prefix += '='
                    if len(color) > 6:
                        # Don't know why this is
                        prefix += color[:-6]
                    color = ('00000' + color)[-6:]
                    red = int(color[:2], 16)
                    green = int(color[2:4], 16)
                    blue = int(color[4:], 16)
                    new_color = '{:02X}{:02X}{:02X}'.format(
                        red // 2, green // 2, blue // 2)
                    line = prefix + new_color + '\n'
                output_file.write(line)
