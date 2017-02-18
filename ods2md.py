#!/usr/bin/env python3

import ezodf
import sys
import html
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

def main(odf_path):
    ods = ezodf.opendoc(odf_path)

    for sheet in ods.sheets:
        print('##', sheet.name)

        column_widths = [max(display_len(display_text(cell)) for cell in column) for column in sheet.columns()]
        # begin omit empty trailing columns (part 1 of 2)
        while column_widths[-1] == 0:
            column_widths.pop()
        # end omit empty trailing columns (part 1 of 2)

        for n, row in enumerate(sheet.rows()):
            # begin omit empty rows
            row_content = ''
            for m, cell in enumerate(row):
                content = display_text(cell)
                row_content += content
            if row_content == '':
                continue
            # end omit empty rows
            print('|', end=' ')
            # begin omit empty trailing columns (part 2 of 2)
            del row[len(column_widths):]
            # end omit empty trailing columns (part 2 of 2)
            for m, cell in enumerate(row):
                content = display_text(cell)
                disp_len = column_widths[m] + len(content) - display_len(content)
                print('{0:<{1}}'.format(content, disp_len), end=' | ')
            print()

            if n == 0:
                print('|', end='')
                for w in column_widths:
                    print(':', '-' * (w+1), '|', sep='', end='')
                print()

if __name__ == '__main__':
    main(sys.argv[1])
