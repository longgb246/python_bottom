# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2019/2/28
"""  
Usage Of 'j_forecast.py' :
"""

from __future__ import print_function

_flag_parse = True
try:
    from dateutil.parser import parse
except:
    _flag_parse = False

from jpype import *

import os
import re
import logging

logging.basicConfig(format='[ %(asctime)s ] ( %(levelname)s ) - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %a',
                    level=logging.DEBUG)


class PyJava(object):
    """With Function:

    with PyJava(jar_path):
        # 计算数据
        start_date = jDate('2019-02-15 10:00:00')  # 计算开始日期
        days = jDouble(3.5)  # 持续时长
        cr = jDouble(0.95)  # cr 值
        forecast_result = ForecastResultUtils.parseForecastResultFromString(str(mock_data))
        print('mean : ', ForecastResultUtils.getCumMean(forecast_result, start_date, days, 'normal'))
        print('quantile : ', ForecastResultUtils.getCumQuantile(forecast_result, start_date, days, cr, 'normal'))
    """

    def __init__(self, jar_path=[], jvm_path=''):
        # java10 : /Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home/lib/jli/libjli.dylib
        # java8 : /Library/Java/JavaVirtualMachines/jdk1.8.0_201.jdk/Contents/Home/jre/lib/server/libjvm.dylib

        # startJVM(getDefaultJVMPath(), "-ea")
        # startJVM(path, '-Djava.class.path=/Users/longguangbin/Work/java/ipc_forecast.jar')
        # java.lang.System.out.println("hello world!")

        start_jvm(jar_path, jvm_path)

    def __enter__(self):
        pass

    def __exit__(self, *exc_info):
        close_jvm()


def get_jar_path(jar_path=[]):
    """Get the path of jars.

    :param jar_path: ['/Users/longguangbin/Work/java/learn_test-1.0-SNAPSHOT.jar']
    """
    if jar_path:
        jar_path_arg = '-Djava.class.path={jar_path}'.format(jar_path=';'.join(jar_path))
    else:
        jar_path_arg = '-ea'
    return jar_path_arg


def get_jvm_path(jvm_path=''):
    """Get the jvm path. """
    if jvm_path:
        return jvm_path
    else:
        return getDefaultJVMPath()


def find_latest_jar():
    """Find latest ipc_forecast.*?jar """
    jars = []
    re_module = 'ipc_forecast.*?jar'
    for each in os.listdir('.'):
        if re.findall(re_module, each):
            jars.append(each)

    jar_file = sorted(jars)[-1]  # 最新版 jar 包
    return jar_file


def start_jvm(jar_path=[], jvm_path=''):
    """Start jvm to run java. """

    if not jar_path:
        # jar_path = ['./{jar_file}'.format(jar_file=find_latest_jar())]
        jar_path = ['./ipc_forecast_4py.jar']

    jar_url = get_jar_path(jar_path)
    jvm_url = get_jvm_path(jvm_path)

    logging.info('Start Java Virtual Machines : {jvm_url} {jar_url}\n'.format(jvm_url=jvm_url, jar_url=jar_url))

    startJVM(jvm_url, jar_url)

    global j2list
    j2list = java.util.Arrays.asList


def close_jvm():
    """Close the jvm. """
    shutdownJVM()


def jDate(date):
    """Transform python date string to Java Date object. """
    if _flag_parse:
        date = parse(date).strftime('%Y-%m-%d %H:%M:%S')
    sdf = java.text.SimpleDateFormat
    try:
        j_date = sdf('yyyy-MM-dd HH:mm:ss').parse(date)
    except:
        raise ValueError('Date Format must be : %Y-%m-%d %H:%M:%S\n'
                         'Your Input date is : {date}'.format(date=date))
    return j_date


def jDouble(num):
    """Transform python float to Java Double object. """
    return java.lang.Double(float(num))


def jList(arr):
    """Transform python list to Java ArrayList object. """
    for i, each in enumerate(arr):
        try:
            arr[i] = j2list(each)
        except:
            arr[i] = jList(each)
    return j2list(arr)


def getForecastResult(package=''):
    if package:
        return JClass(package)
    else:
        return JClass('com.jd.y.ipc.demand.ForecastResult')


def getForecastResultUtils(package=''):
    if package:
        return JClass(package)
    else:
        return JClass('com.jd.y.ipc.demand.ForecastResultUtils')


def main():
    # path = '/Library/Java/JavaVirtualMachines/jdk1.8.0_201.jdk/Contents/Home/jre/lib/server/libjvm.dylib'

    # jar 包的位置
    jar_path = ['/Users/longguangbin/Work/java/learn_test-1.0-SNAPSHOT.jar']
    start_jvm(jar_path)

    # mock 数据
    mock_data = {"forecast_date": "2019-02-15",
                 "forecast_dist_name": "Gaussian",
                 "forecast_horizon": 91,
                 "forecast_interval_len": 1,
                 "forecast_interval_unit": "day",
                 "forecast_period_type": "1",
                 "forecast_result_list": [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0],
                                          [1.0, 2.0], [1.0, 2.0], [1.0, 4.0],
                                          [1.0, 1.0], [0.0, 4.0], [0.0, 1.0]],
                 "forecast_result_baseline_list": [[0.0, 1.0], [1.0, 1.0], [1.0, 1.0],
                                                   [1.0, 2.0], [1.0, 2.0], [1.0, 4.0],
                                                   [1.0, 1.0], [0.0, 4.0], [0.0, 1.0]]}

    ForecastResultUtils = getForecastResultUtils()

    # 计算数据
    start_date = jDate('2019-02-15 10:00:00')  # 计算开始日期
    days = jDouble(3.5)  # 持续时长
    cr = jDouble(0.95)  # cr 值

    forecast_result = ForecastResultUtils.parseForecastResultFromString(str(mock_data))

    print(forecast_result.getForecastDate())
    print(forecast_result.getForecastResultList())
    print(forecast_result.getForecastDistName())
    print(start_date)
    print(days)
    print(cr)
    print()

    print('mean : ', ForecastResultUtils.getCumMean(forecast_result, start_date, days, 'normal'))
    print('quantile : ', ForecastResultUtils.getCumQuantile(forecast_result, start_date, days, cr, 'normal'))

    close_jvm()


if __name__ == '__main__':
    main()
