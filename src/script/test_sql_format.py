# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/10/6
  Usage   : From https://github.com/sethelliott/sql_format
"""

from __future__ import print_function
import re
import pprint

ALL_KEYWORDS = [
    'left hash join', 'hash join', 'left join', 'inner join', 'outer join', 'right join',
    'order by', 'group by', 'where', 'select', 'from', 'having', 'on', 'using', 'join',
    'distinct', 'as', '(', ')', 'sum', 'max', 'min'
]
WRAP_KEYWORDS = [
    'left hash join', 'hash join', 'left join', 'inner join', 'outer join',
    'where', 'group by', 'order by', 'select', 'from', 'having', 'join'
]
FUNCTIONS = ['sum', 'min', 'max']
INDENTED_KEYWORDS = ['on']


def clean_sql():
    """Open the test file and sanitize it by stripping whitepace and lower-casing it."""

    file_in = open('test_sql.sql')
    raw_sql = file_in.read()
    file_in.close()
    raw_sql = raw_sql.replace('\n', ' ')

    # sanitized_sql = re.sub(r'\s+', ' ', raw_sql, flags=re.UNICODE)
    # lower_sql = sanitized_sql.lower()
    # return lower_sql
    return raw_sql


def find_keywords(sql, keywords):
    """Find all the keywords in `sql`.

    :param sql: The sql string being manipulated.
    :param keywords: A list of all the keywords being found in sql.
    :return: A dictionary with keys of sql keywords and values of two element lists with the starting and ending indexes of the keywords.
    """
    keyword_positions = []
    for n in range(len(sql)):
        for kw in keywords:
            if sql[n:n + len(kw)].lower() == kw.lower():
                keyword_positions.append([sql[n:n + len(kw)], n, n + len(kw)])

    to_delete = []
    for kw1 in keyword_positions:
        for kw2 in keyword_positions:
            if (kw1[0].lower() in kw2[0].lower()) & (len(kw1[0]) < len(kw2[0])) & (kw1[1] >= kw2[1]) & (kw2[2] <= kw2[2]):
                to_delete.append(kw1)

    for n in to_delete:
        if n in keyword_positions:
            keyword_positions.remove(n)
    return keyword_positions


def line_keywords(sql, keyword_spots, wrap_keywords):
    """Stick all the keywords in keyword_list on a new line.

    :param sql: The sql string being manipulated.
    :param keyword_spots: A dictionary of keywords in sql.
    :param wrap_keywords: A list of keywords that should be placed on a new line.
    :return: An updated sql string that has line breaks before and after keywords.
    """
    for i in keyword_spots:
        if i[0] in wrap_keywords:
            sql = sql.replace(i[0], '\n' + i[0] + '\n')
    sql = sql.replace('\n ', '\n')
    sql = sql.replace(' \n', '\n')
    sql = sql.replace('\n\n', '\n')
    if sql[0] == '\n':
        sql = sql.replace(sql, sql[1:len(sql)])
    return sql


def indent_keywords(sql, keyword_spots, keyword_list):
    """Indent keywords.
    Args:
      sql: The sql string being manipulated.
      keyword_spots: A dictionary of keywords in sql.
      keyword_list: A list of keywords that should be indented.
    Returns:
      An updated sql string that has items in keyword_list indented.
    """
    for i in keyword_spots:
        if i[0] in keyword_list:
            sql = sql.replace(i[0], '\n  ' + i[0])
    sql = sql.replace('\n  \n  ', '\n  ')
    return sql


def indent_lists(sql, keyword_spots, keyword_list):
    """Indent stuff after top level keywords.
    Args:
      sql: The sql string being manipulated.
      keyword_spots: A dictionary of keywords in sql.
      keyword_list: A list of keywords that should be indented.
    Returns:
      An updated sql string with items in the select list indented.
    """

    for i in keyword_spots:
        if i[0] in keyword_list:
            sql = sql.replace(i[0] + '\n', i[0] + '\n ')
    sql = sql.replace(',', ',\n ')
    return sql


def format_functions(sql, keyword_list):
    """Clean up whitespace around function names.
    Args:
      sql: The sql string being manipulated.
      keyword_list: A list of function names.
    Returns:
      An updated sql string with function spacing corrected.
    """

    for i in keyword_list:
        sql = re.sub(i + r'\(\s+', i + '(', sql, flags=re.UNICODE)

    for i in keyword_list:
        sql = re.sub(r'\s+\)', ')', sql, flags=re.UNICODE)

    return sql


def format_subquery(sql, keyword_spots, keyword_list):
    """Indent subqueries.
    Parentheses go on a new line and are indented two spaces from the block
    above. The query is indented an additional two spaces inside the
    parentheses.
    Args:
      sql: The sql string being manipulated.
      keyword_spots: A dictionary of keywords in sql.
      keyword_list: A list of keywords that should be indented.
    Returns:
      An updated sql string with items in the select list indented.
    """
    for n in range(len(keyword_spots)):
        if (keyword_spots[n][0] == '(') and (
                keyword_spots[n - 1][0] not in keyword_list):
            open_paren_loc = keyword_spots[n][1]

            for x in range(open_paren_loc, len(sql)):
                if sql[x] == ')':
                    close_paren_loc = x

    sub_query = sql[open_paren_loc:close_paren_loc + 1]
    new_sub_query = sub_query
    new_sub_query = new_sub_query.replace('\n', '\n    ')
    new_sub_query = new_sub_query.replace('(', '(')
    new_sub_query = new_sub_query.replace(')', '\n  )')

    sql = sql.replace(sub_query, new_sub_query)

    return sql


def upper_keywords(sql, keyword_list):
    """Upper case all the keywords.
    Args:
      sql: The sql string being manipulated.
      keyword_list: A dictionary of all the keywords in sql.
    Returns:
      An updated sql string with all of the keywords capitalized.
    """
    for i in keyword_list:
        sql = sql.replace(i[0], i[0].upper())
    return sql


def add_semicolon(sql):
    """If the query doesn't already end in a semicolon, add one.
    Args:
      sql: The sql string being manipulated.
    Returns:
      An updated sql string with a semicolon as the last character.
    """
    if sql[-1] != ';':
        sql += ';'
    return sql


def main():
    """Run all the little guys above to do the needful.
    """
    output = clean_sql()
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    pprint.pprint(keyword_locations)
    exit()
    output = line_keywords(output, keyword_locations, WRAP_KEYWORDS)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = indent_keywords(output, keyword_locations, INDENTED_KEYWORDS)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = indent_lists(output, keyword_locations, TOP_LEVEL_KEYWORDS)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = format_subquery(output, keyword_locations, FUNCTIONS)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = format_functions(output, FUNCTIONS)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = upper_keywords(output, keyword_locations)
    print(output, '\n\n')
    keyword_locations = find_keywords(output, ALL_KEYWORDS)
    output = add_semicolon(output)
    print(output, '\n\n')

    # new_sql = open('new_sql.sql', 'w')
    # new_sql.write(output)
    # new_sql.close()

    # print(output)


if __name__ == '__main__':
    main()
