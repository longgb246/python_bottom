# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/9/29
  Usage   : 内置函数
"""

from __future__ import print_function
import pprint


# compile
# format
# frozenset 类
# iter
# memoryview 类，创建的“内存视图”对象
# next
# slice
# super


# [知识点] staticmethod [知识点] classmethod
# staticmethod : 不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
# classmethod : 也不需要self参数，但第一个参数需要是表示自身类的cls参数。
def test_classmethod():
    class A(object):
        bar = 1

        @staticmethod
        def foo():
            print('foo')

        @staticmethod
        def static_foo():
            print('static_foo')
            print(A.bar)

        @classmethod
        def class_foo(cls):
            print('class_foo')
            print(cls.bar)
            cls().foo()

    A.static_foo()
    A.class_foo()


# [知识点] complex 复数
def test_complex():
    print(complex('1+2j'))
    # complex('1 + 2j')  # 是错误的
    z = complex('1+2j')
    print(z.real)
    print(z.imag)


# [知识点] delattr [知识点] hasattr [知识点] setattr [知识点] getattr
# 跟属性有关的函数
def test_hasattr():
    a = 'string'
    print(hasattr(a, 'format'))


# [知识点] dir
# 列出 module、class 的属性，可以通过 __dir__ 来更改函数的返回值
def test_dir():
    import test_dir as t1_module1
    import test_dir.test_dir as t1_module2
    from test_dir.test_dir import TtDir, TtDir2, tt_dir, tt_dir2

    print('t1_module1 : ', dir(t1_module1))
    print('t1_module2 : ', dir(t1_module2))
    print('t1_class : ', dir(TtDir))
    print('t1_class : ', dir(TtDir2))

    attr_list = [t1_module1, t1_module2, TtDir, TtDir2, tt_dir, tt_dir2]
    attr_list_name = ['t1_module1', 't1_module2', 'TtDir', 'TtDir2', 'tt_dir', 'tt_dir2']
    for i, each in enumerate(attr_list):
        tmp_list = dir(each)
        print('\n\n', attr_list_name[i], ' type : ', type(each))
        for each_attr in tmp_list:
            print('\t', each_attr, ' : ', getattr(each, each_attr))


# [知识点] enumerate (sequence, start=0)
def test_enumerate():
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    print(list(enumerate(seasons)))
    print(list(enumerate(seasons, start=1)))


# [知识点] eval(expression[, globals[, locals]]) [知识点] execfile [知识点] exec [知识点] ast.literal_eval()
# eval : 执行表达式， execfile : 执行文件， exec : 执行语句， ast.literal_eval : 检查表达式，当其为有效的python对象时候，进行转换
def test_eval():
    a = 1
    b = 2

    def local_var():
        a = 3
        b = 4
        print("eval('a+b') : ", eval('a+b'))
        print("eval('a+b', globals()) : ", eval('a+b', globals()))
        print("eval('a+b', globals(), locals()) : ", eval('a+b', globals(), locals()))
        print("eval('a+b', {'a': 8, 'b': 9}) : ", eval('a+b', {'a': 8, 'b': 9}))
        print("eval('a+b', {'a': 8, 'b': 9}, {'c': 1, 'b': 2}) : ", eval('a+b', {'a': 8, 'b': 9}, {'c': 1, 'b': 2}))

    local_var()
    func = eval('lambda x: 1.0 / (1 + c*((x - k) / f))', dict({'k': 1, 'f': 2.0}, c=3))
    func(2)


# [知识点] file [知识点] open
# file 和 open 有一样的效果，但是推荐使用 open，file 用于 type 类型的检查
def test_file():
    with open('__init__.py') as f:
        print(f.read())
    with file('__init__.py') as f:
        print(f.read())
        print(isinstance(f, file))


# [知识点] filter
# filter(function, iterable) 等价于 [item for item in iterable if function(item)]
def test_filter():
    tt = [3, 4, 5, 6, 7, 8]
    print(filter(lambda x: x > 5, tt))
    print([y for y in tt if y > 5])


# [知识点] globals [知识点] locals 全局变量与局部变量
def test_globals():
    print(globals())
    print(locals())


# [知识点] input [知识点] raw_input
# input 等价于 eval(raw_input(prompt))
def test_input():
    a = input()
    print(a)
    b = raw_input()
    print(b)


# [知识点] isinstance [知识点] issubclass 可以是自身的子类
def test_isinstance():
    isinstance(3, int)
    issubclass(int, float)


# [知识点] max [知识点] min
# max(iterable [,key]) / max(arg1,arg2,*args [,key])
# key 与 sort 的 key 作用相同，将传入比较的对象进行 key 函数的处理后再进行比较
def test_max():
    # 正常比较大小
    a = [-7, -9, 4, 5, -6, 7]
    print('正常比较大小 : ', max(a))
    # 使用 abs 后比较大小
    print('使用 abs 后比较大小 : ', max(a, key=lambda x: abs(x)))
    # 指定比较的数据
    b = [[-7, 8], [-9, 7], [4, 3], [5, 4], [-6, 6], [7, 5]]
    print('使用第 0 个数据比较 : ', max(b, key=lambda x: x[0]))
    print('使用第 1 个数据比较 : ', max(b, key=lambda x: x[1]))
    # 比较其他类型数据
    prices = {'A': 3, 'B': 6, 'C': 9, 'E': 1}
    print('比较 dict 的数据 : ', max(prices.items(), key=lambda x: x[1]))
    # 同样，对于 max(arg1,arg2,*args [,key]) 也可以使用 key
    max(2, 3, -8, 5, key=lambda x: abs(x))
    max(2, 3, -8, 5, key=lambda x: abs(x))
    max([2, 3], [3, 3, 4], [-8, 9], [3, 5], key=lambda x: x[0])
    max([2, 3], [3, 3, 4], [-8, 9], [3, 5], key=lambda x: x[1])


# [知识点] property
# 1、使用函数的方法；2、使用修饰器方法；当使用了修饰器后，自动有了setter（写属性）、deleter（删属性）可用，当不用时，为只读
def test_property():
    class C(object):
        def __init__(self):
            self._x = None

        def getx(self):
            return self._x

        def setx(self, value):
            self._x = value

        def delx(self):
            del self._x

        x = property(getx, setx, delx, "I'm the 'x' property.")
        # property([fget[, fset[, fdel[, doc]]]])

    c = C()
    c.x = 1
    print(c.x)
    del c.x

    # voltage 为只读属性，不能设值，也不能删除
    class Parrot(object):
        def __init__(self):
            self._voltage = 100000

        @property
        def voltage(self):
            """Get the current voltage."""
            return self._voltage

    parrot = Parrot()
    # parrot.voltage = 1  # 不可设值
    # del parrot.voltage  # 不可删除
    print(parrot.voltage)

    class C2(object):
        def __init__(self):
            self._x = 100000

        @property
        def x(self):
            """I'm the 'x' property."""
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

        @x.deleter
        def x(self):
            del self._x

    c = C2()
    c.x = 1
    print(c.x)
    del c.x


# [知识点] reduce
# reduce(function, iterable[, initializer]), initializer 是设值初始化用的
def test_reduce():
    # reduce 等价于下面函数
    def reducex(func, iterable, initializer=None):
        it = iter(iterable)
        if initializer is None:
            try:
                initializer = next(it)
            except StopIteration:
                raise TypeError('reduce() of empty sequence with no initial value')
        accum_value = initializer
        for x in it:
            accum_value = func(accum_value, x)
        return accum_value

    print(reduce(lambda x, y: x + y, [1, 2, 3, 4, 5], 3))
    print(reducex(lambda x, y: x + y, [1, 2, 3, 4, 5]))


# [知识点] repr 原始字符串
# __repr__ 能够设置 repr 函数的返回值
def test_repr():
    a = 'Enter\nContent'
    print(a)
    print(repr(a))


# [知识点] reversed 反转
def test_reversed():
    a = [2, 3, 4, 5]
    print(a[::-1])
    print(list(reversed(a)))


# [知识点] sorted 排序函数
def test_sorted():
    def cmp_tt(x, y):
        # 比较规则
        return x - y

    a = [['a1', 2], ['a2', 3], ['a3', 5], ['a4', 6], ['a5', 64]]
    print(sorted(a, cmp=cmp_tt, key=lambda x: x[1], reverse=True))


# [知识点] type 动态创建类
def test_type():
    # 判断类型
    print(type('3'))
    # 传入 3 个参数，动态创建类
    X = type('X', (object,), dict(a=1))
    x = X()
    print(x.a)
    print(type(x))

    class X2(object):
        a = 1

    x2 = X2()
    print(type(x2))


# [知识点] vars 返回有 __dict__ 属性的 __dict__ 值
def test_vars():
    vars()  # 不传参数的时候，就和 locals() 一样
    pass


# [知识点] __import__ importlib.import_module()
# 不全，对于 module 的动态引用
def test__import__():
    pass


def pass_t():
    pass

# pass
