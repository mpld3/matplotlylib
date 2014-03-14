from . nose_tools import run_fig
from . data.data import *
import matplotlib.pyplot as plt


def test_line_data():
    fig, ax = plt.subplots()
    ax.plot(D['x1'], D['y1'])
    renderer = run_fig(fig)
    for xi, xf, yi, yf in zip(renderer.data[0]['x'], D['x1'],
                              renderer.data[0]['y'], D['y1']):
        assert xi == xf, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
        assert yi == yf, str(renderer.data[0]['y']) + ' is not ' + str(D['y1'])


def test_lines_data():
    fig, ax = plt.subplots()
    ax.plot(D['x1'], D['y1'])
    ax.plot(D['x2'], D['y2'])
    renderer = run_fig(fig)
    for xi, xf, yi, yf in zip(renderer.data[0]['x'], D['x1'],
                              renderer.data[0]['y'], D['y1']):
        assert xi == xf, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
        assert yi == yf, str(renderer.data[0]['y']) + ' is not ' + str(D['y1'])
    for xi, xf, yi, yf in zip(renderer.data[1]['x'], D['x2'],
                              renderer.data[1]['y'], D['y2']):
        assert xi == xf, str(renderer.data[1]['x']) + ' is not ' + str(D['x2'])
        assert yi == yf, str(renderer.data[0]['y']) + ' is not ' + str(D['y2'])


def test_bar_data():
    fig, ax = plt.subplots()
    ax.bar(D['x1'], D['y1'])
    renderer = run_fig(fig)
    for yi, yf in zip(renderer.data[0]['y'], D['y1']):
        assert yi == yf, str(renderer.data[0]['y']) + ' is not ' + str(D['y1'])


def test_bars_data():
    fig, ax = plt.subplots()
    ax.bar(D['x1'], D['y1'], color='r')
    ax.barh(D['x2'], D['y2'], color='b')
    renderer = run_fig(fig)
    for yi, yf in zip(renderer.data[0]['y'], D['y1']):
        assert yi == yf, str(renderer.data[0]['y']) + ' is not ' + str(D['y1'])
    for yi, yf in zip(renderer.data[1]['y'], D['y2']):
        assert yi == yf, str(renderer.data[1]['y']) + ' is not ' + str(D['y2'])