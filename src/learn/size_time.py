# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/11/9
  Usage   :
"""

import os
import time


def file_num2size(num_size, h=True):
    """文件大小数值变为 MB 的显示

    :param num_size: 文件大小
    :param h: 是否 human 显示
    :return: {'value': 数值，'measure': 单位，'str': 字串, 'org_size': 原始大小}
    """
    measure_list = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    fsize = num_size

    i = 0
    while (fsize >= 1) and (i < len(measure_list)) and h:
        if fsize < 1024:
            break
        else:
            fsize = fsize / 1024.0
            i += 1

    i = min(i, len(measure_list) - 1)
    fsize = round(fsize, 2) if not isinstance(fsize, int) else fsize
    res_info = {'value': fsize,
                'measure': measure_list[i],
                'str': str(fsize) + measure_list[i],
                'org_size': num_size}
    return res_info


def get_file_size(filePath, h=True):
    """获取文件的大小

    :param filePath: 文件路径
    :param h: 是否human可读
    :return: {'value': 数值，'measure': 单位，'str': 字串}
    """
    # filePath = unicode(filePath, 'utf8')
    org_fsize = os.path.getsize(filePath)
    res_info = file_num2size(org_fsize, h=h)
    return res_info


def timestamp2time(timestamp):
    """把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12"""
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_file_createtime(filePath):
    """获取文件的创建时间"""
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getctime(filePath)
    return timestamp2time(t)


def get_file_modifytime(filePath):
    """获取文件的修改时间"""
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getmtime(filePath)
    return timestamp2time(t)


def get_file_accesstime(filePath):
    """获取文件的访问时间"""
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getatime(filePath)
    return timestamp2time(t)
