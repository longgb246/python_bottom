# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/10/16
  Usage   :
"""

from __future__ import print_function
import sys
import platform

# ----- Necessary -----
# Get the run system platform
sys_platform = 'mac' if any(list(map(lambda x: x in platform.system().lower(), ('darwin', 'os2', 'os', 'mac')))) else \
    'win' if any(list(map(lambda x: x in platform.system().lower(), ('win32', 'cygwin', 'win')))) else 'other'
# Get the run python version
py_ver = sys.version_info[0]

# python2 reload sys to set utf8
if py_ver == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
# python3 set long and unicode
if py_ver == 3:
    long = int
    unicode = int

# ----- Matplotlib -----
if sys_platform == 'win':
    from pylab import mpl

    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
elif sys_platform == 'mac':
    import matplotlib

    matplotlib.use('TkAgg')

if __name__ == '__main__':
    print()
    print('platform.system().lower() : ', platform.system().lower())
    print('sys_platform : ', sys_platform)
    print('py_version : {}.x'.format(py_ver))
