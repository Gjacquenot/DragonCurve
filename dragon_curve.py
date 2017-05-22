# Dragon curve is a fractal curve created recursively with a simple pattern
# It is a finite space filling curve

# An option is given to create a terdragon curve, that uses a different
# pattern, and creates three segments for each existing segment
# This is another form of space filling curve
#

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


rot = lambda x: np.matrix([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])
f1 = lambda x, y: 1 / np.sqrt(2) * rot(+ np.pi / 4) * np.matrix([[x], [y]])
f2 = lambda x, y: 1 / np.sqrt(2) * rot(- np.pi / 4) * np.matrix([[x], [y]])

ft1 = lambda x, y: 1 / np.sqrt(3) * rot(+ 1 * np.pi / 6) * np.matrix([[x], [y]])
ft2 = lambda x, y: 1 / np.sqrt(3) * rot(- 1 * np.pi / 6) * np.matrix([[x], [y]])


def rotVec(angle, x, y):
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
    x, y = [0, 1], [0, 0]
    res = {0: [x,y]}
    for j in range(level):
        x_new, y_new = [], []
        for i in range(len(x) - 1):
            dx, dy = x[i + 1] - x[i], y[i + 1] - y[i]
            d1 = ft1(dx, dy)
            d2 = ft2(dx, dy)
            x_new.extend([x[i], x[i] + d1[0, 0], x[i] + d2[0, 0]])
            y_new.extend([y[i], y[i] + d1[1, 0], y[i] + d2[1, 0]])
        x_new.append(x[-1])
        y_new.append(y[-1])
        x, y = x_new, y_new
        res[j + 1] = [x, y]
    return res



def demo(level=15, plotTerDragon=False, showAllLevel=False, filename=None):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    if plotTerDragon:
        res = dragon_ter_curve(level=level)
    else:
        res = dragon_curve(level=level)
    if showAllLevel:
        for k in res:
            ax.plot(res[k][0], res[k][1])
    else:
        x, y = np.asarray(res[level][0]), np.asarray(res[level][1])
        for i in range(4):
            xr,yr = rotVecAsNp(np.pi/2*i,x,y)
            for k in range(-2,2):
                for k2 in range(-2,2):
                    xoff,yoff = rotVecAsNp(i * np.pi / 2, 2* k + k2 * 0, 2* k2)
                    ax.plot(xoff+xr, yoff+yr, linewidth=0.5, color = 'C' + str(i))
                    xoff,yoff = rotVecAsNp(i * np.pi / 2, 2* k + 1 + k2 * 0, 2* k2+1)
                    ax.plot(xoff+xr, yoff+yr, linewidth=0.5, color = 'C' + str(i))

    plt.grid(True)
    plt.axis('equal')
    plt.show()
    if filename:
        plt.savefig(filename)


def demo2(level=15):
    res = dragon_curve(level=level)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    x, y = np.asarray(res[level][0]), np.asarray(res[level][1])
    ax.plot(x,y, linewidth=0.5)
    # ax.plot(x+0.5,y+0.5, linewidth=0.5)
    # xr,yr = rotVec(np.pi / 2 + np.pi / 4, x, y)
    # ax.plot(xr,yr)
    # ax.plot(x+1,y)
    # ax.plot(x-1,y)
    # ax.plot(x,y+2/3)
    plt.axis('equal')
    plt.show()


def demo3(level=15):
    res = dragon_ter_curve(level=level)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    x, y = np.asarray(res[level][0]), np.asarray(res[level][1])
    ax.plot(x+1, y, linewidth=0.5, color='C'+str(0))
    for i in range(3):
        xr,yr = rotVecAsNp(i * np.pi / 3, x, y)
        # ax.plot(xr, yr, linewidth=0.5, color='C'+str(i))
        for k in range(-2, 2):
            for k2 in range(-2, 3):
            #xoff,yoff = rotVecAsNp(i * np.pi / 3, k * -0.5, k * np.sqrt(3)/2)
            #ax.plot(xoff+xr, yoff+yr, linewidth=0.5, color = 'C' + str(i))
                xoff,yoff = rotVecAsNp(i * np.pi / 3, k + k2 * -0.5, k2 * np.sqrt(3)/2)
                ax.plot(xoff+xr, yoff+yr, linewidth=1, color = 'C' + str(i))
    plt.grid(True)
    plt.axis('equal')
    plt.show()

#demo()
#demo2()


def create_animated_gif(maxRecursionLevel=7, mfilename='draggon_curve'):
    generateLevel = lambda x:list(range(x))+[x-i-2 for i in range(x-1)]
    cmd = 'convert -antialias -density 100 -delay 60 '
    for level in generateLevel(maxRecursionLevel + 1):
        cmd += mfilename + '_' + '{0:03d}'.format(level) + '.png '
    cmd += mfilename + '.gif'


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a dragon curve')
    parser.add_argument('level', type=int,help='number of recursion level. Reasonnable value is 15')
    parser.add_argument('-a','--all', action='store_true', help='boolean used to display all levels')
    parser.add_argument('-t','--ter', action='store_true', help='boolea used to create a terdragon')
    args = parser.parse_args()
    demo(args.level, plotTerDragon=args.ter, showAllLevel=args.all)
    # demo3(level=args.level)
