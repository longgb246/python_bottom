# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2019/2/28
"""  
Usage Of 'test_jpype.py' : 
"""

from __future__ import print_function
from jpype import *


class PyJava(object):

    def __init__(self, jvm_path=''):

        if jvm_path == '':
            print(getDefaultJVMPath())
            startJVM(getDefaultJVMPath(), "-ea")
        else:
            print(getDefaultJVMPath())
            print(jvm_path)

    def __enter__(self):
        pass

    def __exit__(self, *exc_info):
        print('Over')


# # jvmPath = '/Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home/lib/jli/libjli.dylib'
# print(getDefaultJVMPath())
# startJVM(getDefaultJVMPath(), "-ea")
# java.lang.System.out.println("hello world!")
# shutdownJVM()


# with PyJava('a'):
path = '/Library/Java/JavaVirtualMachines/jdk1.8.0_201.jdk/Contents/Home/jre/lib/server/libjvm.dylib'
# startJVM(path, '-Djava.class.path=/Users/longguangbin/Work/java/ipc_forecast.jar')
startJVM(getDefaultJVMPath(), '-Djava.class.path=/Users/longguangbin/Work/java/learn_test.jar')
# startJVM(getDefaultJVMPath(), '-Djava.class.path=/Users/longguangbin/Work/java/ipc_forecast.jar')
# startJVM(path, '-Djava.class.path=/Users/longguangbin/Work/java/hanlp-1.7.2.jar')


java.lang.System.out.println("hello world!")
# ProductDemand = JClass('scripts.distribution.ProductDemand')
# ForecastResult = JClass('scripts.distribution.ForecastResult')
# ForecastResult = JClass('com.jd.y.ipc.demand.ForecastResult')
# ForecastResultUtils = JClass('com.jd.y.ipc.demand.ForecastResultUtils')
# ForecastResult = JClass('com.jd.y.ipc.demand.ForecastResult') ForecastResultUtils
# HanLP = JClass('com.hankcs.hanlp.HanLP')
# product_demand = ProductDemand()

# forecast_result = ForecastResult()
# forecast_result.setForecastHorizon(3)
# print(forecast_result.getForecastHorizon())

HelloWorld = JClass('learn.chapter1.HelloWorld')
hello_world = HelloWorld()
hello_world.main()

print('yes')
