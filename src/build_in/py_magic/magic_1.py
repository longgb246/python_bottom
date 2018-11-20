# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/11/19
  Usage   :
"""

from __future__ import print_function
import copy

try:
    from thread import get_ident
except ImportError:
    from _thread import get_ident


def recursive_repr(fillvalue='...'):
    """Decorator to make a repr function return fillvalue for a recursive call"""

    def decorating_function(user_function):
        repr_running = set()

        def wrapper(self):
            key = id(self), get_ident()
            if key in repr_running:
                return fillvalue
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
            return result

        # Can't use functools.wraps() here because of bootstrap issues
        wrapper.__module__ = getattr(user_function, '__module__')
        wrapper.__doc__ = getattr(user_function, '__doc__')
        wrapper.__name__ = getattr(user_function, '__name__')
        return wrapper

    return decorating_function


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
        self._data = data or []

    def __missing__(self, key):
        """为 dict 类的魔法方法，当 key 的 value 缺失时候，返回值，故此处不起作用 """
        # print('__missing__')
        return

    def __setitem__(self, key, value):
        """使用 x.__setitem__(y) <==> x[y] = 1，表示可以用 x[y] 进行赋值 """
        index = self._find_index(key)
        if index == -1:
            self._data.append({key: value})
        else:
            self._data[index] = {key: value}

    def __getitem__(self, key):
        """使用 x.__getitem__(y) <==> x[y]，表示可以用 x[y] 进行索引 """
        # print('__getitem__ : ')
        index = self._find_index(key)
        assert index >= 0, 'key is error : {0}'.format(key)
        return self._data[index]

    def _find_index(self, key):
        if isinstance(key, (unicode, str)):
            for index, each in enumerate(self._data):
                if isinstance(each, dict) and (key in each):
                    return index
            return -1
        elif isinstance(key, int):
            assert (key < len(self._data)) and (key >= 0), IndexError('list index out of range.')
            return key
        else:
            raise ValueError('key is error !')

    def __delitem__(self, key):
        try:
            del self._data[0][key]
        except KeyError:
            raise KeyError('Key not found in the first mapping: {!r}'.format(key))

    def __len__(self):
        """支持 len(对象) 的长度作用 """
        return 2

    def __iter__(self):
        """返回一个可迭代的对象，同时需要配合 next 方法使用，作用于 for i in 对象 的使用中 """
        self._iter_index = 0
        return self

    def next(self):
        """__iter__ 传入的对象，注意别出现死循环 """
        if self._iter_index >= len(self._data):
            raise StopIteration
        else:
            value = self._data[self._iter_index]
            self._iter_index += 1
            return value

    def __reversed__(self):
        """当使用 reversed(对象) 函数翻转对象时调用 """
        return self._data[::-1]

    def __contains__(self, item):
        """当使用in，not in 对象的时候 调用(not in 是在in完成后再取反,实际上还是in操作) 仅仅返回 True|False """
        print('__contains__', item)
        return item in self._data

    @recursive_repr()
    def __str__(self):
        """用于 print """
        # print('__str__')
        return '{0.__class__.__name__}({1})'.format(self, str(self._data))

    # def __repr__(self):
    #     """用于交互环境直接输出该对象，当没有 __str__ 函数的时候，print 也调用它 """
    #     # print('__repr__')
    #     return self._data

    __repr__ = __str__  # 可以这么统一

    def copy(self):
        return self.__class__(self._data)  # 复制该类

    __copy__ = copy

    # def __copy__(self):
    #     """copy.copy 的接口 """
    #     return 1

    # def __deepcopy__(self, memodict={}):
    #     """copy.deepcopy 的接口 """
    #     return 2

    # @property
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        assert isinstance(value, list), ValueError('data must be list.')
        self._data = value

    def append(self, data):
        self._data.append(data)


# __bool__:

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
    tt2['f'] = 23  # __setitem__
    print(tt2['f'])  # __getitem__: 使用 __getitem__ 就可以这么做。不走 __missing__
    print(tt2[2])  # __getitem__: 越界问题
    print(len(tt2))  # __len__
    for i in tt2:  # __iter__ + next
        print(i)
    print(33 in tt2)  # __contains__:
    print(tt2)
    t_copy = copy.copy(tt2)
    t_deepcopy = copy.deepcopy(tt2)
    t_copy.data = [12, 3, 4]  # @property
    tt2.append([3])
    print(tt2['e'])
    pass


if __name__ == '__main__':
    test_script()
