from random import choice

from PyQt5.QtGui import *

DARK_MODE = 'Dark mode'
LIGHT_MODE = 'Light mode'

LAYOUT_WITH_WEIGHT = ['layout_drl', 'layout_fruchterman_reingold']

COLOR_SPECTRUM = [QBrush(QColor(c)) for c in [
    '#ff0000', '#fe0000', '#fe0100', '#fe0200', '#fd0401', '#fd0601', '#fc0802', '#fb0c03', '#fa0f04', '#f91305',
    '#f81806', '#f71d07', '#f62208', '#f4280a', '#f22e0c', '#f1340d', '#ef3b0f', '#ed4211', '#eb4913', '#e85016',
    '#e65818', '#e45f1a', '#e1671d', '#df6f1f', '#dc7722', '#d97f25', '#d68728', '#d38f2b', '#d0972e', '#cd9f31',
    '#caa634', '#c7ae37', '#c3b53b', '#c0bc3e', '#bcc342', '#b9ca45', '#b5d049', '#b2d64c', '#aedc50', '#aae154',
    '#a6e658', '#a3eb5b', '#9fef5f', '#9bf263', '#97f667', '#93f86b', '#8ffa6f', '#8bfc73', '#87fd77', '#83fe7b',
    '#7fff7f', '#7bfe83', '#77fd87', '#73fc8b', '#6ffa8f', '#6bf893', '#67f697', '#63f29b', '#5fef9f', '#5beba3',
    '#58e6a6', '#54e1aa', '#50dcae', '#4cd6b2', '#49d0b5', '#45cab9', '#42c3bc', '#3ebcc0', '#3bb5c3', '#37aec7',
    '#34a6ca', '#319fcd', '#2e97d0', '#2b8fd3', '#2887d6', '#257fd9', '#2277dc', '#1f6fdf', '#1d67e1', '#1a5fe4',
    '#1858e6', '#1650e8', '#1349eb', '#1142ed', '#0f3bef', '#0d34f1', '#0c2ef2', '#0a28f4', '#0822f6', '#071df7',
    '#0618f8', '#0513f9', '#040ffa', '#030cfb', '#0208fc', '#0106fd', '#0104fd', '#0002fe', '#0001fe', '#0000fe'
]]


def randomColor():
    return QBrush(QColor(choice(range(0, 256)), choice(range(0, 256)), choice(range(0, 256))))


def arrayToSpectrum(arr):
    minValue = min(arr)
    arr = [v - minValue for v in arr]
    maxValue = max(arr)
    return [COLOR_SPECTRUM[min(99, int(v / maxValue * 100))] for v in arr]
