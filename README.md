# Dragon Curve

This repository contains elements to create
[dragon curves](https://en.wikipedia.org/wiki/Dragon_curve),
that recursive space filling curves.

Two implementations are available:

- a HTML/Javascript one implemented in [index.html](index.html).
  Result can be seen [here](https://gjacquenot.github.io/DragonCurve)
- a Python one implemented in [dragon_curve.py](dragon_curve.py).

Here are some command line examples that can be used to
create the images presented below

    python dragon_curve.py --help
    python dragon_curve.py 15 -o dragon_curve_15.gif
    python dragon_curve.py 10 --tile -o dragon_curve_10_tile.gif
    python dragon_curve.py 10 -t -o dragon_curve_ter_10.gif
    python dragon_curve.py  9 -t --tile -o dragon_curve_ter_9_tile.gif


![Alt text](https://upload.wikimedia.org/wikipedia/commons/3/3e/Dragon_curve_15.gif)

![Alt text](https://upload.wikimedia.org/wikipedia/commons/d/d9/Dragon_curve_10_tile.gif)

![Alt text](https://upload.wikimedia.org/wikipedia/commons/4/4b/Dragon_curve_ter_10.gif)

![Alt text](https://upload.wikimedia.org/wikipedia/commons/e/e4/Dragon_curve_ter_9_tile.gif)
