# Dragon curve is a fractal curve created recursively with a simple pattern
# It is a finite space filling curve

# An option is given to create a terdragon curve, that uses a different
# pattern, and creates three segments for each existing segment
# This is another form of space filling curve
#

# This script offers the possibilty to create animated gif to
# show the construction of the fractal curve.
# This gif is created with convert program from imagemagick

#
# Level | # points    | # line segments
#--------------------------------------
# 0     | 2           | 1
# 1     | 3           | 2
# 2     | 5           | 4
# 3     | 9           | 8
# .     | .           | .
# n     | 2**(n+1)+1  | 2**(n+1)

import numpy as np


# Creates a rotation matrix from angle
rot = lambda x: np.matrix([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])

# Define transformation pattern for dragon curve
f1 = lambda x, y: 1 / np.sqrt(2) * rot(+ np.pi / 4) * np.matrix([[x], [y]])
f2 = lambda x, y: 1 / np.sqrt(2) * rot(- np.pi / 4) * np.matrix([[x], [y]])

# Define transformation pattern for Terdragon
ft1 = lambda x, y: 1 / np.sqrt(3) * rot(+ 1 * np.pi / 6) * np.matrix([[x], [y]])
ft2 = lambda x, y: 1 / np.sqrt(3) * rot(- 1 * np.pi / 6) * np.matrix([[x], [y]])


def rotVec(angle, x, y):
    '''
    returns rotated input vectors x and y from angle
    '''
    res = np.dot(rot(angle), np.vstack([np.asarray(x), np.asarray(y)]))
    return np.asarray(res)[0].tolist(), np.asarray(res)[1].tolist()


def rotVecAsNp(angle, x, y):
    res = np.dot(rot(angle), np.vstack([np.asarray(x), np.asarray(y)]))
    return np.asarray(res)[0], np.asarray(res)[1]


def dragon_curve(level=3):
    x, y = [0, 1], [0, 0]
    res = {0: [x,y]}
    for j in range(level):
        x_new, y_new = [], []
        for i in range(len(x) - 1):
            dx, dy = x[i+1] - x[i], y[i+1] - y[i]
            f = f2 if i%2 else f1
            d = f(dx, dy)
            x_new.extend([x[i], x[i] + d[0, 0]])
            y_new.extend([y[i], y[i] + d[1, 0]])
        x_new.append(x[-1])
        y_new.append(y[-1])
        x, y = x_new, y_new
        assert(len(x) == (2**(j + 1) + 1))
        assert(len(y) == (2**(j + 1) + 1))
        res[j + 1] = [x, y]
    return res


def dragon_ter_curve(level=3):
    '''
    level recursion level
    '''
    x, y = [0, 1], [0, 0]
    res = {0: [x,y]}
    for j in range(level):
        x_new, y_new = [], []
        for i in range(len(x) - 1):
            dx, dy = x[i + 1] - x[i], y[i + 1] - y[i]
            d1, d2 = ft1(dx, dy), ft2(dx, dy)
            x_new.extend([x[i], x[i] + d1[0, 0], x[i] + d2[0, 0]])
            y_new.extend([y[i], y[i] + d1[1, 0], y[i] + d2[1, 0]])
        x_new.append(x[-1])
        y_new.append(y[-1])
        x, y = x_new, y_new
        res[j + 1] = [x, y]
    return res



def dragon_curve_plot(level=15, **kwargs):
    tile = kwargs.get('tile', False)
    plotTerDragon = kwargs.get('plotTerDragon', False)
    showAllLevel = kwargs.get('showAllLevel', False)
    filename = kwargs.get('filename', None)
    grid = kwargs.get('grid', False)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    if plotTerDragon:
        res = dragon_ter_curve(level=level)
    else:
        res = dragon_curve(level=level)
    if showAllLevel:
        for k in res:
            ax.plot(res[k][0], res[k][1], linewidth=0.5, color='k')
    else:
        if tile:
            x, y = np.asarray(res[level][0]), np.asarray(res[level][1])
            if plotTerDragon:
                for i in range(3):
                    xr, yr = rotVecAsNp(i * np.pi / 3, x, y)
                    for k in range(-2, 2):
                        for k2 in range(-2, 3):
                            xoff, yoff = rotVecAsNp(i * np.pi / 3, k + k2 * -0.5, k2 * np.sqrt(3)/2)
                            ax.plot(xoff + xr, yoff + yr, linewidth=0.5, color='C' + str(i))
            else:
                for i in range(4):
                    xr, yr = rotVecAsNp(np.pi / 2 * i, x, y)
                    for k in range(-2, 2):
                        for k2 in range(-2, 2):
                            xoff, yoff = rotVecAsNp(i * np.pi / 2, 2 * k + k2 * 0, 2 * k2)
                            ax.plot(xoff + xr, yoff + yr, linewidth=0.5, color='C' + str(i))
                            xoff, yoff = rotVecAsNp(i * np.pi / 2, 2 * k + 1 + k2 * 0, 2 * k2 + 1)
                            ax.plot(xoff + xr, yoff + yr, linewidth=0.5, color='C' + str(i))
        else:
            ax.plot(res[level][0], res[level][1], linewidth=0.5, color='k')

    plt.axis('equal')
    if grid:
        plt.grid(True)
    else:
        plt.axis('off')
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def create_animated_gif(maxRecursionLevel=7, filename='dragon_curve.gif', **kwargs):
    plotTerDragon = kwargs.get('plotTerDragon', False)
    tile = kwargs.get('tile', False)
    grid = kwargs.get('grid', False)
    import subprocess
    generateLevel = lambda x: list(range(x)) + [x - i - 2 for i in range(x - 1)]
    cmd = 'convert -antialias -density 100 -delay 120 '
    for level in generateLevel(maxRecursionLevel + 1):
        cfilename = filename + '_' + '{0:03d}'.format(level) + '.png'
        cmd += cfilename + ' '
        dragon_curve_plot(level=level, plotTerDragon=plotTerDragon, showAllLevel=False, filename=cfilename, tile=tile, grid=grid)
    cmd += filename
    print(cmd)
    subprocess.check_output(cmd.split(' '))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate a dragon curve')
    pa = parser.add_argument
    pa('level', type=int, help='number of recursion level. Reasonnable value is 15')
    pa('-t', '--ter', action='store_true', help='boolean used to create a terdragon')
    pa('--tile', action='store_true', help='boolean used to create a tiling of the generated curve')
    pa('-a', '--all', action='store_true', help='boolean used to display all levels (disable when tiling)')
    pa('-o', '--output', default=None, help='name of the generated file. If not provided, result will display on screen')
    pa('-g', '--grid', action='store_true', help='boolean used to display grid')
    args = parser.parse_args()
    if args.output and args.output.lower().endswith('gif'):
        create_animated_gif(maxRecursionLevel=args.level, plotTerDragon=args.ter, filename=args.output, grid=args.grid, tile=args.tile)
    else:
        dragon_curve_plot(args.level, plotTerDragon=args.ter, showAllLevel=args.all, filename=args.output, grid=args.grid, tile=args.tile)


if __name__=='__main__':
    main()
