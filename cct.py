#!/usr/bin/env python3
import argparse
import re
from crochetdiagram import SVG_BASE, Symbol


version = '0.0.2α'
ABOUT = f"""
Crochetable Cyclic Tag (v.{version})
Generates crochetable computational cyclic-tag patterns.
"""


DEFAULT_ROW1 = '[Any sequence of sc / dc stitched onto an appropriately sized foundation chain.]'

STD    = "std"
DEC_SS = "dec-ss"
INC_SC = "inc-sc"
INC_DC = "inc-dc"

VSTD    = "(std) work 1 sc into each dc, 1 dc into each sc until end of row; turn."
VDEC_SS = "(dec-ss) 1 ss, then proceed as in the standard row until end of row; turn."
VINC_SC = "(inc-sc) prepare to proceed as in the std row, if the first st would be sc, skip this and the following std row. Otherwise 1st st is dc: proceed as std row until end of row, then inc 1 extra sc into last st; turn."
VINC_DC = "(inc-dc) prepare to proceed as in the std row, if the first st would be sc, skip this and the following std row. Otherwise 1st st is dc: proceed as std row until end of row, then inc 1 extra dc into last st; turn."

CCT = { ';': DEC_SS,
        '0': INC_SC,
        '1': INC_DC}

VCCT = { STD:    VSTD,
         DEC_SS: VDEC_SS,
         INC_SC: VINC_SC,
         INC_DC: VINC_DC}

DC = 'Ŧ'
SC = '+'
SS = '•'
CH = 'ᴑ'  # U+1D11


def bct_to_ct(s):
    """Takes a bct sequence of {0, 1} (str) and converts it to CT symbols {;, 0, 1}."""
    s = s.replace(' ', '')
    output = ''
    l = len(s)
    i = 0
    while i < l:
        if s[i] == '0':
            output += ';'
            i += 1
        elif s[i] == '1':
            output += s[i+1]
            i += 2
    return output


def ct_to_cct(program, data=DEFAULT_ROW1, title=None, description=None):
    title = title or 'Untitled'
    output = [f'# {title}']
    if description:
        for line in description.split('\n'):
            output.append(f'> {line}')
    output += [f'1. {data}', f'2. {STD}']
    for i, s in enumerate(program):
        output.append('%s. %s' % (2 * i + 3, CCT[s]))
        output.append('%s. %s' % (2 * i + 4, STD))
    output.append('Repeat from Row 3.')
    return '\n'.join(output)


class CrochetableCT:
    LIMIT = 250
    def __init__(self, base_row, pattern):
        """
        base_row: str, made up of crochet stitch symbols.
        pattern: str, the program, consisting of the CT program symbols: {0, 1, ;}
          https://esolangs.org/wiki/Bitwise_Cyclic_Tag#The_language_CT
        """
        self.base_row = base_row
        # pattern in CT
        self.pattern = pattern
        self.width = len(self.base_row)

    def evaluate(self, limit=LIMIT):
        """Evaluate the instructions on base_row."""
        self.crochet(limit)
        last = min(limit, len(self.piece) - 1)
        return '\n'.join([row.rjust(len(self.piece[last])) for row in self.piece[last::-1]])

    def std(self, s):
        tmp = '#'
        return s.replace(DC, tmp).replace(SC, DC).replace(tmp, SC).replace(SS, ' ')

    def dec_ss(self, s):
        return self.std(s.strip()[:-1]) + SS  + ' ' * s.count(' ')

    def inc_sc(self, s):
        return (SC if s.strip()[-1] == SC else '') + self.std(s)

    def inc_dc(self, s):
        return (DC if s.strip()[-1] == SC else '') + self.std(s)

    def chain(self, s, rs=True):
        return s + ('8' if s[-1] == DC else 'o')

    def core_stitches(self, s):
        return s.strip().replace('8', '').replace('o', '')

    def describe(self, verbose=False):
        """Describe the instructions."""
        return ct_to_cct(self.pattern, self.base_row, verbose)

    def crochet(self, stop=LIMIT):
        """
        Evaluates the pattern from base_row.
        Performed on init.
        Populates self.piece
        returns None
        """
        self.piece = [CH * len(self.base_row), self.base_row, self.std(self.base_row)]
        instructions = {';': self.dec_ss, '0': self.inc_sc, '1': self.inc_dc}
        row = 0
        while row < stop and self.piece[-1].strip():
            cmd = self.pattern[row % len(self.pattern)]
            #print("CMD: %d -- %s" % (row, cmd))
            new = instructions[cmd](self.piece[-1])
            # don't add duplicate rows if there is no change
            if len(self.core_stitches(self.std(new))) != len(self.core_stitches(self.piece[-1].strip())):
                self.piece.append(new)
                self.piece.append(self.std(self.piece[-1]))
                self.width = max(self.width, len(self.piece[-1]))
            row += 1


class Instructions(CrochetableCT):
    LIMIT = 250
    def __init__(self, source):
        self.source = source.split('\n')
        self.title = None
        self.description = ''
        self.pattern = []
        for line in self.source:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#') and not self.title:
                self.title = line[1:]
            elif line.startswith('>'):
                self.description += line[1:]
            else:
                self.pattern.append(line)

    def evaluate(self, data, limit=LIMIT):
        instructions = {'std': self.std, 'dec-ss': self.dec_ss, 'inc-sc': self.inc_sc, 'inc-dc': self.inc_dc}
        data = data.replace('0', SC).replace('1', DC)
        width = len(data)
        piece = [CH * width, data, self.std(data)]
        row = 0
        pattern = self.pattern[2:]
        count = len(pattern)
        while len(piece) < limit and piece[-1].strip():
            cmd = pattern[row % count].split(' ')[1]
            row += 1
            try:
                new = instructions[cmd](piece[-1])
            except KeyError as e:
                continue
            # don't add duplicate rows if there is no change
            if len(self.core_stitches(self.std(new))) != len(self.core_stitches(piece[-1].strip())):
                piece.append(new)
                piece.append(self.std(piece[-1]))
                width = max(width, len(piece[-1]))
        self.piece = piece
        return self.piece

    def show_piece(self, limit=LIMIT):
        last = min(limit, len(self.piece) -1)
        return '\n'.join([row.rjust(len(self.piece[last])) for row in self.piece[last::-1]])

    def svg_piece(self, limit=LIMIT):
        smap = {DC: 'double', SC: 'single', SS: 'slipstitch', CH: 'chain'}
        PAGEY_OFFSET = 1080
        PAGEX_OFFSET = 770
        last = min(limit, len(self.piece) -1)
        width = len(self.piece[last])
        output = ''
        for y, row in enumerate([row.rjust(width) for row in self.piece]):
            for x, sym in enumerate(row):
                if sym != ' ':
                    alt = y % 2
                    dh = sym == DC
                    offset = (1 - alt) * (-6.5 if dh else 6.5)
                    output += Symbol('%s_%s' % (x, y), smap[sym], (x * 10 - width * 10 + PAGEX_OFFSET, -y * 15 + offset + PAGEY_OFFSET), 0, alt).symbol
        return SVG_BASE.replace('{CONTENT}', output)

    def std(self, s):
        tmp = '#'
        return s.replace(DC, tmp).replace(SC, DC).replace(tmp, SC).replace(SS, ' ')

    def raw(self):
        return '\n'.join(self.source)

    def verbose(self):
        verbose = self.raw()
        verbose = re.sub(r'\n([0-9]+)\.', r'\n**Row \1**', verbose)
        for k in VCCT.keys():
            verbose = verbose.replace(k, VCCT[k])
        # Force line breaks in markdown
        verbose = verbose.replace('\n', '  \n')
        return verbose


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=ABOUT, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('infile', help='CCT source file to process', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('--svg', '-s', help='Pattern symbol instructions as SVG to STDOUT', action='store_true')
    parser.add_argument('--title', '-t', help='Title')
    parser.add_argument('--describe', help='Description')
    parser.add_argument('--input', '-i', help='Row 1 input (instructions or symbols)')
    parser.add_argument('--ct', help='Convert CT {0, 1, ;} source into CCT')
    parser.add_argument('--bct', help='Convert Bitwise Cyclic Tag {0, 1} source into CCT')
    parser.add_argument('--limit', '-l', help='Limit output evaluation to this many output rows.', type=int, default=Instructions.LIMIT)
    parser.add_argument('--verbose', '-v', help='Verbose instruction output (Markdown)', action='store_true')
    parser.add_argument('--debug', '-d', help='Turn on debug output', action='store_true')
    args = parser.parse_args()

    source = None
    kwargs = {}
    if args.title:
        kwargs['title'] = args.title
    if args.describe:
        kwargs['description'] = args.describe
    if args.input:
        kwargs['data'] = args.input
    if args.ct:
        source = ct_to_cct(args.ct, **kwargs)
    elif args.bct:
        source = ct_to_cct(bct_to_ct(args.bct), **kwargs)

    if args.infile:
        source = args.infile.read()

    if source:
        cct = Instructions(source)
        if args.verbose:
            print(cct.verbose())
        elif not args.infile:
            print(cct.raw())
        elif args.svg:
            # Evaluate to SVG -> STDOUT
            cct.evaluate(args.input, limit=args.limit)
            print(cct.svg_piece(limit=args.limit))
        else:
            # Evaluate to Unicode -> STDOUT
            cct.evaluate(args.input, limit=args.limit)
            print(cct.show_piece(limit=args.limit))
        if args.debug:
            print('TITLE:', cct.title)
            print('FIRST:', cct.pattern[0])
            print(cct.source)
            print(cct.pattern)
            print(cct.raw())
            print('VERBOSE:', cct.verbose())
