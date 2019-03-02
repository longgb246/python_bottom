# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/28
"""  
Usage Of 'client_script' : 
"""

import os
import pandas as pd

from pyspark.sql import SparkSession

print('Test Path')
print(__file__)

t_path = os.path.abspath(os.path.dirname(__file__))
spark = SparkSession.builder.enableHiveSupport().getOrCreate()
sp1 = spark.sql('select * from app.app_saas_sfs_model_input limit 1000')
df1 = sp1.toPandas()

print(df1)
# raise Exception(df1)
df1.to_csv('test1.csv', encoding='utf8')
