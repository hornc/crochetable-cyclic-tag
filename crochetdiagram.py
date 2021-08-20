
SVG_BASE = """<?xml version="1.0" encoding="UTF-8"?>
<svg
  xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  width="210mm" height="297mm" style="overflow:visible">
  {CONTENT}
</svg>"""


class Crochet:
    base_style = "opacity:1;fill:none;fill-opacity:1;stroke:%s;stroke-width:0.8;stroke-opacity:1"
    main_style = base_style % '#000000'
    alt_style = base_style % '#a8a8a8'

    double = """
<g id="{ID}"
   transform="translate({POS})">
  <path
     id="{ID}-a"
     d="M 3,7 V 25"
     style="{STYLE}" />
  <path
     id="{ID}-b"
     d="M 0,7 6,7"
     style="{STYLE}" />
  <path
     id="{ID}-c"
     d="M 0.4,11.5 5.6,14.5"
     style="{STYLE}" />
</g>"""

    single = """
<g id="{ID}" transform="translate({POS})">
    <path
       style="{STYLE}"
       d="M 0,9 6,9"
       id="{ID}-a" />
    <path
       style="{STYLE}"
       d="m 3,6 v 6"
       id="{ID}-b" />
  </g>"""

    slipstitch = """
<g id="{ID}" transform="translate({POS}) scale(1.5)">
<circle
       style="{STYLE}"
       id="{ID}"
       cx="2"
       cy="6"
       r="0.4" /></g>"""

    chain = """
<g id="{ID}" transform="translate({POS})">
<ellipse
       style="{STYLE}"
       id="{ID}-a"
       cy="-3"
       cx="9"
       rx="1.1874059"
       ry="2.577101"
       transform="rotate(90)" /></g>"""


class Symbol(Crochet):
    def __init__(self, name, stitch, position=(0, 0), rotation=0, direction=1):
        self.symbol = getattr(Crochet, stitch)
        self.symbol = self.symbol.replace('{POS}', '%s,%s' % position)
        self.symbol = self.symbol.replace('{POSX}', str(position[0]))
        self.symbol = self.symbol.replace('{POSY}', str(position[1]))
        self.symbol = self.symbol.replace('{STYLE}', [Crochet.alt_style, Crochet.main_style][direction])
        self.symbol = self.symbol.replace('{ID}', name)
