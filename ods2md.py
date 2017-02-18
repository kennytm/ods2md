#!/usr/bin/env python3

# Copyright 2015, 2017 Kenny Chan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import ezodf
import sys
import unicodedata

# Ref: http://stackoverflow.com/a/31666966/224671
DISPLAY_WIDTH = {
    'A': 1,
    'F': 2,
    'H': 1,
    'N': 1,
    'Na': 1,
    'W': 2,
}

def display_text(cell):
    v = cell.value
    if isinstance(v, float):
        return '{:g}'.format(v)
    elif v is None:
        return ''
    else:
        return str(v)

def display_len(s):
    return sum(DISPLAY_WIDTH[unicodedata.east_asian_width(c)] for c in s)

def main(odf_path, out_file):
    ods = ezodf.opendoc(odf_path)

    for sheet in ods.sheets:
        column_widths = [max(display_len(display_text(cell)) for cell in column) for column in sheet.columns()]
        if not any(column_widths):
            continue

        print('##', sheet.name, file=out_file)
        printed_header = False

        for row in sheet.rows():
            contents = [display_text(cell) for cell in row]
            if not any(contents):
                continue

            print('|', end='', file=out_file)
            for m, content in enumerate(contents):
                column_width = column_widths[m]
                if not column_width:
                    continue
                disp_len = column_width + len(content) - display_len(content)
                print(' {0:<{1}}'.format(content, disp_len), end=' |', file=out_file)
            print(file=out_file)

            if not printed_header:
                printed_header = True
                print('|', end='', file=out_file)
                for w in column_widths:
                    if w:
                        print(':', '-' * (w+1), '|', sep='', end='', file=out_file)
                print(file=out_file)

if __name__ == '__main__':
    main(sys.argv[1], sys.stdout)
