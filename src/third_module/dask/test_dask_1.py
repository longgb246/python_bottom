# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/14
"""  
Usage Of 'test_dask_1' : 
"""

# ipc
#### jdvl start -m /data0/spark:/data0/spark:ro -m /data0/cmo_ipc:/data0/cmo_ipc:rw -i bdp-docker.jd.com:5000/wise_mart_cmo_ipc -o='--net=host' -I bash
# bca
#### jdvl start -m /data0/mart_bca:/data0/mart_bca:rw -i bdp-docker.jd.com:5000/wise_mart_bca:latest -o='--net=host' -I bash

# 单机使用调研


# --------- da.array ---------
import dask.array as da
from dask.distributed import Client, progress

client = Client(processes=False, threads_per_worker=4,
                n_workers=1, memory_limit='2GB')

x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = x + x.T
z = y[::2, 5000:].mean(axis=1)

# --------- dask 调度 ---------
import dask.multiprocessing
# from dask.distributed import Client

# dask.config.set(scheduler='synchronous')  # overwrite default with single-threaded scheduler
# dask.config.set(scheduler='threads')  # overwrite default with threaded scheduler
# dask.config.set(scheduler='processes')  # overwrite default with multiprocessing scheduler

# client = Client()
## or
# client = Client(processes=False)

# --------- dask 延迟 ---------
import dask


def delay_exm1():
    def inc(x):
        return x + 1

    def double(x):
        return x + 2

    def add(x, y):
        return x + y

    data = [1, 2, 3, 4, 5]

    output = []
    for x in data:
        a = dask.delayed(inc)(x)  # a = inc(x)
        b = dask.delayed(double)(x)  # b = double(x)
        c = dask.delayed(add)(a, b)  # c = add(a, b)
        output.append(c)

    total = dask.delayed(sum)(output)  # total = sum(output)
    total.vizualize()
    total.compute()


def delay_exm2():
    @dask.delayed
    def inc(x):
        return x + 1

    @dask.delayed
    def double(x):
        return x + 2

    @dask.delayed
    def add(x, y):
        return x + y

    data = [1, 2, 3, 4, 5]

    output = []
    for x in data:
        a = inc(x)
        b = double(x)
        c = add(a, b)
        output.append(c)

    total = dask.delayed(sum)(output)
    total.compute()


def delay_exm3():
    def inc(x, y):
        return x + 1

    def double(x, y):
        return x + 2

    lazy_results = []
    for a in [1, 2]:
        for b in [3, 4]:
            if a < b:
                c = dask.delayed(inc)(a, b)  # add lazy task
            else:
                c = dask.delayed(double)(a, b)  # add lazy task
            lazy_results.append(c)

    results = dask.compute(*lazy_results)  # compute all in parallel
    print(results)
