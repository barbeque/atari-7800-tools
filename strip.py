"""
Remove the ATARI7800 header from an *.a78 file,
writing it out as a *.bin file instead so you can
burn it to an EPROM.

Based on http://7800.8bitdev.org/index.php/A78_Header_Specification

Needs Python 3.6+
"""

import os, sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <a78 rom file to strip>")
    sys.exit(1)

binary = []
with open(sys.argv[1], 'rb') as f:
    binary = bytes(f.read())

assert(len(binary) > 0)

def has_header(rom):
    # hacky and slow way to find a sub-array, but who cares
    needle = "ATARI7800"
    j = 0
    for i in range(len(rom)):
        if j == 0:
            # looking for the start
            if chr(rom[i]) == needle[0]:
                j += 1
        else:
            if j >= len(needle):
                return True # found it all
            else:
                if chr(rom[i]) != needle[j]:
                    j = 0
                else:
                    j += 1
    return False # exhausted

is_a78_rom = has_header(binary)
print("Has header? ", is_a78_rom)

# Sure, we could look for it, but let's just hardcode it and call
# it a day
HEADER_LENGTH = 0x80

if is_a78_rom:
    print(f"Removing header of {HEADER_LENGTH} bytes")
    binary2 = binary[HEADER_LENGTH:]
    assert(len(binary2) == len(binary) - HEADER_LENGTH)
    binary = binary2
else:
    print("No header detected, output binary has no changes.")

filename = os.path.basename(sys.argv[1])
filename = filename.replace('.a78', '.bin')

with open(filename, 'wb') as f:
    f.write(binary)
