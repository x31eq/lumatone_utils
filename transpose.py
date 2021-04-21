#!/usr/bin/env python3

import sys

transpose_level = int(sys.argv[1])

for filename in sys.argv[2:]:
    with open(filename) as input_file:
        output_filename = 'transposed_' + filename
        with open(output_filename, 'w', newline=('\r\n')) as output_file:
            for line in input_file:
                if line.startswith('Key_'):
                    prefix, pitch = line.strip().split('=')
                    pitch = int(pitch) + transpose_level
                    line = '{}={}\n'.format(prefix, pitch)
                output_file.write(line)
