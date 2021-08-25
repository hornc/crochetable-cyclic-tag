# Crochetable Cyclic Tag

A tool for generating and evaluating Turing-complete crochet patterns based on Emil Post's [tag system](https://en.wikipedia.org/wiki/Tag_system) computational model, and the esoteric programming language [Bitwise Cyclic Tag](https://esolangs.org/wiki/Bitwise_Cyclic_Tag).


## Usage examples

Help:

    ./cct.py -h

### Convert
Convert BCT to CCT:

    ./cct.py --bct "10 11 10 10 10 11 0 11 10 10 0 11 10 10 11 10 10 11 10 10 0 0 0 0" -t "Collatz Sequence"

Convert CT to CCT:

    ./cct.py --ct "010001;100;100100100;;;;" -t "Collatz Sequence"

Convert CCT to human followable crochet instructions for computaion-by-crochet (`--verbose`):

    ./cct.py examples/collatz.cct --verbose

### Evaluate
Evaluate CCT to crochet pattern symbols (Unicode to STDOUT):

    ./cct.py examples/collatz.cct

Evaluate CCT to SVG crochet pattern:

    ./cct.py --svg examples/collatz.cct

## Output example

### CCT code
[simple-triangle.cct](examples/simple-triangle.cct):

```
# Simple decreasing triangle swatch
1. [Any sequence of sc / dc stitched onto an appropriately sized foundation chain.]
2. std
3. dec-ss
4. std
Repeat from Row 3.
```
Produced with `./cct.py --ct ";" --title "Simple decreasing triangle swatch"`

### Verbose instructions

    ./cct.py examples/simple-triangle.cct --verbose

#### Simple decreasing triangle swatch  
**Row 1** [Any sequence of sc / dc stitched onto an appropriately sized foundation chain.]  
**Row 2** (std) work 1 sc into each dc, 1 dc into each sc until end of row; turn.  
**Row 3** (dec-ss) 1 ss, then proceed as in the standard row until end of row; turn.  
**Row 4** (std) work 1 sc into each dc, 1 dc into each sc until end of row; turn.  
Repeat from Row 3. 

### Evaluation of input
`0`: single crochet, `1`: double crochet (US crochet terminology)


    ./cct.py examples/simple-triangle.cct -i 111111

```
•     
+     
Ŧ•    
++    
ŦŦ•   
+++   
ŦŦŦ•  
++++  
ŦŦŦŦ• 
+++++ 
ŦŦŦŦŦ•
++++++
ŦŦŦŦŦŦ
ᴑᴑᴑᴑᴑᴑ
```

A different input produces different output:

    ./cct.py examples/simple-triangle.cct -i 1011101

```
•      
+      
Ŧ•     
+Ŧ     
Ŧ+•    
+Ŧ+    
Ŧ+Ŧ•   
+Ŧ++   
Ŧ+ŦŦ•  
+Ŧ+++  
Ŧ+ŦŦŦ• 
+Ŧ+++Ŧ 
Ŧ+ŦŦŦ+•
+Ŧ+++Ŧ+
Ŧ+ŦŦŦ+Ŧ
ᴑᴑᴑᴑᴑᴑᴑ
```

### SVG output

    ./cct.py examples/simple-triangle.cct -i 1011101 --svg

![SVG example](examples/output/simple-triangle.svg)
