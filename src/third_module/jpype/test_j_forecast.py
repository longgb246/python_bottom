# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2019/3/2
"""  
Usage Of 'test_j_forecast.py' :
"""

from __future__ import print_function
import unittest

from unittest import TestCase

# from j_forecast import *
import j_forecast as jf


class TestJForecast(TestCase):

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('------------ Test Start ------------')

    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('------------ Test End   ------------')

    @classmethod
    def tearDownClass(cls):
        # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('============ [ Test End ] ============\n')

    @classmethod
    def setUpClass(cls):
        # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('============ [ Test Start ] ============\n')

    def test_jpype(self):
        # 启动 java 虚拟机
        jf.start_jvm()

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

        ForecastResultUtils = jf.getForecastResultUtils()

        # 计算数据
        start_date = jf.xxxate('2019-02-15 10:00:00')  # 计算开始日期
        days = jf.xxxouble(3.5)  # 持续时长
        cr = jf.xxxouble(0.95)  # cr 值

        forecast_result = ForecastResultUtils.parseForecastResultFromString(str(mock_data))

        print('[ forecastResult Args ]')
        print('forecastDistName : ', forecast_result.getForecastDistName())
        print('forecastDate : ', forecast_result.getForecastDate())
        print('forecastResultList : {0}\n'.format(forecast_result.getForecastResultList()))

        print('[ calculate Args ]')
        print('start_date : ', start_date)
        print('days : ', days)
        print('cr : {0}\n'.format(cr))

        print('[ calculate Result ]')
        print('mean : ', ForecastResultUtils.getCumMean(forecast_result, start_date, days, 'normal'))
        print('quantile : ', ForecastResultUtils.getCumQuantile(forecast_result, start_date, days, cr, 'normal'))

        jf.close_jvm()

    def test_a(self):
        print('test2')


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
