# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/11/19
  Usage   :
"""

from __future__ import print_function


class Test(dict):
    def __missing__(self, key):
        """为 dict 类的魔法方法，当 key 的 value 缺失时候，返回值 """
        print('__missing__')
        return

    def __getitem__(self, key):
        """使用 x.__getitem__(y) <==> x[y]，表示可以用 x[y] 进行索引 """
        print('__getitem__ : ', key)
        return dict.__getitem__(self, key)

    def get(self, key):
        """使用 get 方法得到 value """
        print('get : ', key)
        return dict.get(self, key)

    def __len__(self):
        """支持 len(对象) 的长度作用 """
        return 1


class Test2(object):
    def __init__(self, data=None):
        self.data = data or []

    def __missing__(self, key):
        """为 dict 类的魔法方法，当 key 的 value 缺失时候，返回值，故此处不起作用 """
        # print('__missing__')
        return

    def __getitem__(self, key):
        """使用 x.__getitem__(y) <==> x[y]，表示可以用 x[y] 进行索引 """
        # print('__getitem__ : ')
        return self._get_by_index(key)

    def __len__(self):
        """支持 len(对象) 的长度作用 """
        return 2

    def __iter__(self):
        """返回一个可迭代的对象，同时需要配合 next 方法使用，作用于 for i in 对象 的使用中 """
        self._iter_index = 0
        return self

    def next(self):
        """__iter__ 传入的对象，注意别出现死循环 """
        if self._iter_index >= len(self.data):
            raise StopIteration
        else:
            value = self.data[self._iter_index]
            self._iter_index += 1
            return value

    def _get_by_index(self, index):
        assert isinstance(index, int), ValueError('Index must be integer. Your index : {0}'.format(index))
        assert (index < len(self.data)) and (index >= 0), IndexError('list index out of range.')
        return self.data[index]


def test_script():
    # dict 的继承
    tt = Test()
    tt['f'] = 12
    print(tt['f'])
    print(tt['e'])
    print(tt.get('c'))
    print('f' in tt)

    # object 的继承
    tt2 = Test2([3, 4, 4])
    tt2['f'] = 12
    print(tt2['f'])  # 使用 __getitem__ 就可以这么做。不走 __missing__
    print(tt2[2])  # 越界问题
    print(len(tt2))
    for i in tt2:
        print(i)
    pass


if __name__ == '__main__':
    test_script()
