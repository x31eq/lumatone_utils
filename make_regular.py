#!/usr/bin/env python3

import argparse, sys

ROWS = [
        (4, 0, 2),
        (4, 1, 5),
        (3, 2, 6),
        (3, 3, 6),
        (2, 4, 6),
        (2, 5, 6),
        (1, 6, 6),
        (1, 7, 6),
        (0, 8, 6),
        (1, 9, 5),
        (3, 10, 2),
        ]

# A diatonic scale takes you to the same note on the next board!
BOARD_GAP = 5, 2

parser = argparse.ArgumentParser(
        description='Generate a Lumatone mapping with a regular layout')
parser.add_argument('-t', '--tone', type=int, nargs='?', default=2,
                    help='Number of steps to a bosanquet whole tone')
parser.add_argument('-l', '--limma', type=int, nargs='?', default=0,
                    help='Number of steps to a bosanquet limma (diatonic semitone)')
parser.add_argument('-o', '--output', nargs='?',
                    help='file to write the generated mapping to')
args = parser.parse_args()


coords_of_key = []
key_at = {}
key = 0

for tone, limma, length in ROWS:
    for i in range(length):
        coords_of_key.append((tone + i, limma))
        key_at[tone + i, limma] = key + i
    key += length

tone_gap, limma_gap = BOARD_GAP
note_gap = tone_gap * args.tone + limma_gap * args.limma
for board in range(5):
    print("[Board{}]".format(board))
    tone_gap, limma_gap = BOARD_GAP
    initial = 8 + board * note_gap
    for key, (tone, limma) in enumerate(coords_of_key):
        note = initial + tone * args.tone + limma * args.limma
        print("Key_{}={}".format(key, note))
        print("Chan_{}=1".format(key))
        print("Col_{}=000000".format(key))

print("""\
AfterTouchActive=1
LightOnKeyStrokes=1
InvertFootController=0
ExprCtrlSensivity=0
VelocityIntrvlTbl=1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63 64 66 67 68 70 71 72 73 74 76 77 79 81 82 84 86 88 90 92 94 96 98 101 104 107 111 115 119 124 129 134 140 146 152 159 170 171 175 180 185 190 195 200 205 210 215 220 225 230 235 240 245 250 255 260 265 270 275 280 285 290 295 300 305 310
NoteOnOffVelocityCrvTbl=1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 63 64 65 66 68 69 70 72 73 74 76 77 79 80 82 84 85 87 88 90 92 94 96 97 99 101 103 105 108 110 112 114 117 119 121 124 127 
FaderConfig=1 2 2 2 3 3 3 4 4 4 5 5 6 6 6 7 7 7 8 8 9 9 9 10 10 10 11 11 12 12 12 13 13 14 14 14 15 15 16 16 17 17 17 18 18 19 19 20 20 20 21 21 22 22 23 23 24 24 25 25 26 26 27 27 28 28 29 29 30 31 31 32 32 33 33 34 35 35 36 37 37 38 39 39 40 41 41 42 43 44 45 45 46 47 48 49 50 51 52 53 55 56 57 59 62 65 68 71 74 77 79 82 85 88 91 94 97 99 102 105 108 111 114 117 119 122 125 127
afterTouchConfig=0 2 3 5 6 8 9 10 12 13 14 16 17 18 20 21 22 24 25 26 27 28 30 31 32 33 34 36 37 38 39 40 41 43 44 45 46 47 48 49 50 51 52 53 54 55 57 58 59 60 61 62 63 64 65 66 67 68 69 70 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 85 86 87 88 89 90 91 92 92 93 94 95 96 97 98 99 99 100 101 102 103 104 104 105 106 107 108 109 110 111 112 112 113 114 115 116 116 117 118 119 120 120 121 122 123 123 124 125 126 126 127 0
LumaTouchConfig=0 1 2 2 3 3 3 4 4 4 5 5 5 6 6 7 7 7 8 8 8 9 9 10 10 10 11 11 11 12 12 13 13 13 14 14 15 15 15 16 16 17 17 18 18 18 19 19 20 20 21 21 22 22 22 23 23 24 24 25 25 26 26 27 27 28 28 29 29 30 30 31 32 32 33 33 34 34 35 36 36 37 37 38 39 39 40 41 41 42 43 43 44 45 46 47 47 48 49 50 51 52 53 53 54 56 57 58 60 61 63 65 68 70 73 75 78 81 84 87 90 94 98 102 107 113 121 127""")
