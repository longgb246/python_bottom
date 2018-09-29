# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/9/29
  Usage   :
"""

# python test.py --input data.txt --output result.csv --chr 2
# python test_argparse.py --input data.txt --output result.csv --chr 2

from __future__ import print_function
import argparse
import pandas as pd

data = pd.DataFrame([[60, 235, 'W'], [235, 418, 'W'], [54, 500, 'W'], [-1, 43, 'C'], [79, 262, 'C'],
                     [262, 437, 'C'], [459, 500, 'C']], columns=['start', 'end', 'strand'])

parser = argparse.ArgumentParser(description='test')

parser.add_argument('--input', metavar='data.txt', help='input file - data.txt')
parser.add_argument('--output', metavar='result.csv', help='output file - result.csv')
parser.add_argument('--chr', metavar='2', help='chr value - 2')

config = parser.parse_args()
config_dict = config.__dict__
chr_v = config_dict.get('chr')
data['chr'] = chr_v

print(data)

# parser.add_argument('script_file',
#                     metavar='run_file.py zip_file.zip setting.yaml',
#                     nargs='+', help='script_run.py ${run_file} ${zip_file} ${setting.yaml}')
# config = parser.parse_args()
# nargs = len(config.script_file)
# run_file = config.script_file[0]
# zip_file_name = config.script_file[1] if nargs >= 2 else 'src.zip'
# setting_path = config.script_file[2] if nargs >= 3 else 'setting.yaml'
# other_args = config.script_file[3:]
