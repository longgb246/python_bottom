# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/9/29
  Usage   :
"""

from __future__ import print_function
import pprint


# compile
# format
# frozenset 是一个类


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


# [知识点] delattr [知识点] hasattr [知识点] setattr [知识点] getattr
# 跟属性有关的函数


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


def pass_t():
    pass

# pass
