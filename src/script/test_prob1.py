# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/10/4
  Usage   :
"""

from __future__ import print_function


def prob_1():
    a = 1

    def test():
        print(a)
        # a = 2

    test()


def prob_2():
    import fileinput, re

    # Matches fields enclosed in square brackets:
    field_pat = re.compile(r'\[(.+?)\]')
    # We'll collect variables in this:
    scope = {}

    # This is used in re.sub:
    def replacement(match):
        code = match.group(1)
        try:
            # If the field can be evaluated, return it:
            return str(eval(code, scope))
        except SyntaxError:
            # Otherwise, execute the assignment in the same scope ... exec code in scope
            rep_exec = code.split('=')
            scope.update({rep_exec[0].strip(): rep_exec[1].strip()})
            # ... and return an empty string:
            return ''

    # Get all the text as a single string:
    # (There are other ways of doing this; see Chapter 11)
    lines = []
    for line in fileinput.input():
        lines.append(line)
    text = ''.join(lines)
    # Substitute all the occurrences of the field pattern:
    x = []
    print(field_pat.sub(replacement, text))


# dataset 包，用于连接数据库的
def prob_3():
    import dataset
    from pandas.io.sql import read_sql
    from pandas.io.sql import to_sql
    import statsmodels.api as sm

    # 创建数据库连接
    db = dataset.connect('sqlite:///:memory:')
    # 创建books表
    table = db["books"]
    # 添加数据,在调用insert时会自动添加表模式
    table.insert(dict(title="Numpy Beginner's guide", author='Ivan Idris'))
    table.insert(dict(title="Numpy Cookbook", author='Ivan Idris'))
    table.insert(dict(title="Learning Numpy", author='Ivan Idris'))
    # 使用pandas的read_sql查询数据
    print(read_sql('SELECT * FROM books', db.executable.raw_connection()))

    # 加载数据
    data_loader = sm.datasets.sunspots.load_pandas()
    df = data_loader.data
    to_sql(df, "sunspots", db.executable.raw_connection())
    table = db['sunspots']

    # 查询前5条数据
    for row in table.find(_limit=5):
        print(row)
    print("Table", db.tables)


if __name__ == '__main__':
    prob_2()
    pass
