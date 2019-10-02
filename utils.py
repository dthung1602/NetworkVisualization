from math import *
from random import choice

from PyQt5.QtGui import *

DARK_MODE = 'Dark mode'
LIGHT_MODE = 'Light mode'
GEO_MODE = 'Geo mode'

LAYOUT_WITH_WEIGHT = ['layout_drl', 'layout_fruchterman_reingold']


def randomColor():
    return QBrush(QColor(choice(range(0, 256)), choice(range(0, 256)), choice(range(0, 256))))


def arrayToSpectrum(arr):
    def g(i):
        return 255 * (i + 1) / 2.0

    def f(start, stop, N):
        interval = (stop - start) / N
        for i in range(N):
            coefficient = start + interval * i
            yield int(g(sin(coefficient * pi)))

    uniqueValues = set(arr)
    n = len(uniqueValues)
    RED = f(0.5, 1.5, n)
    GREEN = f(1.5, 3.5, n)
    BLUE = f(1.5, 2.5, n)
    RGBs = [('#%02x%02x%02x' % rgb) for rgb in zip(RED, GREEN, BLUE)]

    temp = sorted(uniqueValues, reverse=True)
    dictColor = {central: color for central, color in zip(temp, RGBs)}
    return [QBrush(QColor(dictColor[i])) for i in arr]
