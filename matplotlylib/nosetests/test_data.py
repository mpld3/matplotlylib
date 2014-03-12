from . nose_tools import run_fig, compare_dict
from . data.data import *
import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec
import numbers


def test_line_data():
    fig, ax = plt.subplots()
    ax.plot(D['x1'], D['y1'])
    renderer = run_fig(fig)
    for xi, xf in zip(renderer.data[0]['x'], D['x1']):
        check = (xi == xf)
        assert check, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
        if not check: break


def test_lines_data():
    fig, ax = plt.subplots()
    ax.plot(D['x1'], D['y1'])
    ax.plot(D['x2'], D['y2'])
    renderer = run_fig(fig)
    for xi, xf in zip(renderer.data[0]['x'], D['x1']):
        assert xi == xf, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
    for xi, xf in zip(renderer.data[1]['x'], D['x2']):
        assert xi == xf, str(renderer.data[1]['x']) + ' is not ' + str(D['x2'])


# def test_bar_data():
#     fig, ax = plt.subplots()
#     ax.bar(D['x1'], D['y1'])
#     renderer = run_fig(fig)
#     for xi, xf in zip(renderer.data[0]['x'], D['x1']):
#         assert xi == xf, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
#
#
# def test_bars_data():
#     fig, ax = plt.subplots()
#     ax.bar(D['x1'], D['y1'])
#     ax.barh(D['x2'], D['y2'])
#     renderer = run_fig(fig)
#     for xi, xf in zip(renderer.data[0]['x'], D['x1']):
#         assert xi == xf, str(renderer.data[0]['x']) + ' is not ' + str(D['x1'])
#     for xi, xf in zip(renderer.data[1]['x'], D['x2']):
#         assert xi == xf, str(renderer.data[1]['x']) + ' is not ' + str(D['x2'])