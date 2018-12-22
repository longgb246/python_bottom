# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/19
"""  
Usage Of 'learn_g1' : 
"""

from __future__ import print_function
import json
import uuid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def test_vars_dir():
    class A(object):
        def __init__(self):
            self.b = 'c'
            self.a = None

        def self_method(self):
            self.m = None

        def __repr__(self):
            print('vars : ', vars(self))
            print('dir : ', dir(self))
            return str(self.__class__) + ' : ' + json.dumps(vars(self), sort_keys=True, indent=4)

    obj = A()
    print(obj)
    print(vars(obj))
    print(dir(obj))
    obj.self_method()
    print(obj)
    print(vars(obj))
    print(dir(obj))


def test_uuid():
    print(uuid.uuid4().hex)


def test_plt_cmap_rain_colors():
    NUM_COLORS = 20
    cm = plt.get_cmap('gist_rainbow')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.0 * i / NUM_COLORS) for i in range(NUM_COLORS)])
    for i in range(NUM_COLORS):
        ax.plot(np.arange(10) * (i + 1))

    # https://matplotlib.org/gallery/color/colormap_reference.html#sphx-glr-gallery-color-colormap-reference-py
    m = [23, 23, 42, 53, 56, 32, 40, 34, 60, 30]
    NUM_COLORS = len(m) + 10
    cm_cmp = 'Paired'  # Pastel1  gist_rainbow  Paired  tab20c
    cm = plt.get_cmap(cm_cmp)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    colors = [cm(1.0 * i / NUM_COLORS) for i in range(NUM_COLORS)][5:]
    ax.bar(range(len(m)), m, color=colors)
