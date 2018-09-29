# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/9/29
  Usage   :
"""


class TtDir(object):
    attr2 = 'attr2'

    def __init__(self):
        self.attr1 = 'attr1'


tt_dir = TtDir()


class TtDir2(object):
    attr2 = 'attr2'

    def __init__(self):
        self.attr1 = 'attr1'

    def __dir__(self):
        return [self.attr1, self.attr2]


tt_dir2 = TtDir2()
