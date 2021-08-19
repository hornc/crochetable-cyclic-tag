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

### Evaluate
Evaluate CCT to crochet pattern symbols (Unicode to STDOUT):

    ./cct.py examples/collatz.cct

Evaluate CCT to SVG crochet pattern:

    ./cct.py --svg examples/collatz.cct

