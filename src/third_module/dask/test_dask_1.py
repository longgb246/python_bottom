# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/14
"""  
Usage Of 'test_dask_1' : 
"""

# ipc
#### xxxvl start -m /data0/spark:/data0/spark:ro -m /data0/cmo_ipc:/data0/cmo_ipc:rw -i bdp-docker.xxx.com:5000/wise_mart_cmo_ipc -o='--net=host' -I bash
# bca
#### xxxvl start -m /data0/mart_bca:/data0/mart_bca:rw -i bdp-docker.xxx.com:5000/wise_mart_bca:latest -o='--net=host' -I bash

# 单机使用调研
from __future__ import print_function
import itertools
import warnings
import numpy as np
from scipy import stats
from datetime import date, timedelta

# --------- dask 调度 ---------
import dask
import dask.multiprocessing
import dask.array as da
from dask.distributed import Client, progress
import dask.bag as db
import dask.dataframe as dd


# from dask.distributed import Client

# dask.config.set(scheduler='synchronous')  # overwrite default with single-threaded scheduler
# dask.config.set(scheduler='threads')  # overwrite default with threaded scheduler
# dask.config.set(scheduler='processes')  # overwrite default with multiprocessing scheduler

# client = Client()
## or
# client = Client(processes=False)

# ------------------------------------
# --- dask 延迟
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


# 启动仪表板的Dask客户端
# Dashboard : http://localhost:8787/status
client = Client(processes=False, threads_per_worker=4, n_workers=1, memory_limit='2GB')


def test_da_array():
    x = da.random.random((10000, 10000), chunks=(1000, 1000))
    y = x + x.T
    z = y[::2, 5000:].mean(axis=1)
    z.compute()

    # 在内存中保留数据
    y = y.persist()
    # %time y[0, 0].compute()
    y[0, 0].compute()
    # %time y.sum().compute()
    y.sum().compute()

    # reshape
    arr0 = da.from_array(np.zeros((3, 4)), chunks=(1, 2))
    # arr0.compute()
    arr1 = da.from_array(np.ones((3, 4)), chunks=(1, 2))
    data = [arr0, arr1]
    x = da.stack(data, axis=0)
    x.compute()
    print(da.stack(data, axis=1).shape)
    x = da.concatenate(data, axis=0)
    x.compute()
    x = da.block(data)
    x.compute()

    ### API
    # https://docs.dask.org/en/latest/array-api.html
    ### chunks
    # Chunk sizes between 10MB-1GB are common
    # rechunk
    # -1: no chunking along this dimension
    # None: no change to the chunking along this dimension (useful for rechunk)
    # "auto": allow the chunking in this dimension to accomodate ideal chunk sizes
    x = x.rechunk(1000)
    x = x.rechunk((50, 1000))
    x = x.rechunk({0: 50, 1: 1000})
    x = x.rechunk({0: -1, 1: 'auto', 2: 'auto'})
    x = x.rechunk('auto')
    dask.array.ones((10000, 10000), chunks=(-1, 'auto'))

    # import skimage.io
    # imread = dask.delayed(skimage.io.imread, pure=True)  # Lazy version of imread

    x = da.sum(np.ones(5))
    x.compute()

    # Automatic dask arrays
    x = da.ones(10, chunks=(5,))
    y = np.ones(10)
    z = x + y
    print(z)

    # small amount of data
    x = da.arange(6, chunks=3)
    y = x ** 2
    np.array(y)
    y.compute()

    # user-defined functions on Dask arrays whenever they are constructed
    # If the plugin function returns None, then the input Dask array will be returned without change. If the plugin function returns something else, then that value will be the result of the constructor.
    def f(x):
        print('x.nbytes : ', x.nbytes)

    with dask.config.set(array_plugins=[f]):
        x = da.ones((10, 1), chunks=(5, 1))
        y = x.dot(x.T)

    # Automatically compute
    with dask.config.set(array_plugins=[lambda x: x.compute()]):
        x = da.arange(5, chunks=2)
    print(x)

    # [learn] itertools.product / np.prod / np.roll
    def warn_on_large_chunks(x):
        shapes = list(itertools.product(*x.chunks))
        nbytes = [x.dtype.itemsize * np.prod(shape) for shape in shapes]
        if any(nb > 1e9 for nb in nbytes):
            warnings.warn("Array contains very large chunks")

    # combine plugins
    with dask.config.set(array_plugins=[warn_on_large_chunks, lambda x: x.compute()]):
        print(y)


def test_overlap_computation():
    x = np.array([1, 1, 2, 3, 3, 3, 2, 1, 1])
    x = da.from_array(x, chunks=5)

    def derivative(x):
        return x - np.roll(x, 1)

    y = x.map_overlap(derivative, depth=1, boundary=0)
    y.compute()

    x = np.arange(16).reshape((4, 4))
    d = da.from_array(x, chunks=(2, 2))
    d.map_overlap(lambda x: x + x.size, depth=1).compute()

    func = lambda x: x + 20
    depth = {0: 1, 1: 1}
    boundary = {0: 'reflect', 1: 'none'}
    d.map_overlap(func, depth, boundary).compute()

    x = np.arange(64).reshape((8, 8))
    d = da.from_array(x, chunks=(4, 4))
    print(d.chunks)
    d.compute()
    g = da.overlap.overlap(d, depth={0: 2, 1: 1}, boundary={0: 100, 1: 'reflect'})
    print(g.chunks)
    print(np.array(g))


def test_internal_design():
    x = da.arange(0, 15, chunks=(5,))
    print(x.name)
    print(x.dask)
    print(x.chunks)
    print(x.dtype)
    x.compute()
    pass


def test_stats():
    def mode(x):
        return stats.mode(x)[0][0]

    x = da.random.beta(1, 1, size=(1000,), chunks=10)
    lazy_results = []
    for func in [stats.kurtosis, stats.skew, mode]:
        lazy_results.append(dask.delayed(func)(x))
    dask.compute(*lazy_results)


# bag
def test_bag():
    b = db.from_sequence([1, 2, 3, 4, 5, 6], npartitions=2)
    b.compute()
    # b = db.read_text('myfile.txt')
    # b = db.read_text('myfile.*.txt.gz')
    b = db.read_text('myfile.*.csv').str.strip().str.split(',')

    # to_textfiles
    # 将dask Bag写入磁盘，每个分区一个文件名，每个元素一行。
    def name(i):
        return str(date(2015, 1, 1) + i * timedelta(days=1))

    b.to_textfiles('/path/to/data/*.json.gz', name_function=name)

    b = db.from_sequence([{'name': 'Alice', 'balance': 100},
                          {'name': 'Bob', 'balance': 200},
                          {'name': 'Charlie', 'balance': 300}],
                         npartitions=2)
    df = b.to_dataframe()
    df.head()
    pass


# DataFrame
def test_dataframe():
    df = dd.read_csv('2014-*.csv')
    df.head()
    df2 = df[df.y == 'a'].x + 1
    df2.compute()
    pass


def test_feature():
    def inc(x):
        return x + 1

    def add(x, y):
        return x + y

    a = client.submit(inc, 10)  # calls inc(10) in background thread or process
    b = client.submit(inc, 20)  # calls inc(20) in background thread or process
    a.result()  # blocks until task completes and data arrives
    c = client.submit(add, a, b)  # calls add on the results of a and b
    futures = client.map(inc, range(1000))


def test_sklearn():
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    from sklearn.linear_model import SGDClassifier, LogisticRegressionCV
    from sklearn.model_selection import GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    from sklearn.externals import joblib
    from sklearn.datasets import make_classification, load_digits, fetch_20newsgroups

    from dask_ml.wrappers import ParallelPostFit

    categories = [
        'alt.atheism',
        'talk.religion.misc',
    ]

    print("Loading 20 newsgroups dataset for categories:")
    print(categories)

    data = fetch_20newsgroups(subset='train', categories=categories)
    print("%d documents" % len(data.filenames))
    print("%d categories" % len(data.target_names))
    print()

    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(max_iter=1000)),
    ])

    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        # 'vect__max_features': (None, 5000, 10000, 50000),
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        # 'tfidf__use_idf': (True, False),
        # 'tfidf__norm': ('l1', 'l2'),
        # 'clf__alpha': (0.00001, 0.000001),
        # 'clf__penalty': ('l2', 'elasticnet'),
        # 'clf__n_iter': (10, 50, 80),
    }

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, cv=3, refit=False, iid=False)
    grid_search.fit(data.data, data.target)

    with joblib.parallel_backend('dask'):
        grid_search.fit(data.data, data.target)

    X, y = load_digits(return_X_y=True)
    svc = ParallelPostFit(SVC(random_state=0, gamma='scale'))

    param_grid = {
        # use estimator__param instead of param
        'estimator__C': [0.01, 1.0, 10],
    }

    grid_search = GridSearchCV(svc, param_grid, iid=False, cv=3)
    grid_search.fit(X, y)

    big_X = da.concatenate([
        da.from_array(X, chunks=X.shape)
        for _ in range(10)
    ])
    predicted = grid_search.predict(big_X)

    #
    X_train, y_train = make_classification(
        n_features=2, n_redundant=0, n_informative=2,
        random_state=1, n_clusters_per_class=1, n_samples=1000)

    N = 100
    X_large = da.concatenate([da.from_array(X_train, chunks=X_train.shape)
                              for _ in range(N)])
    y_large = da.concatenate([da.from_array(y_train, chunks=y_train.shape)
                              for _ in range(N)])
    clf = ParallelPostFit(LogisticRegressionCV(cv=3))
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_large)
    clf.score(X_large, y_large)

    # est.partial_fit(X_train_1, y_train_1)

    # from tpot import TPOTClassifier
    pass


def print_and_return(string):
    print(string)
    return string


def format_str(count, val, nwords):
    return ('word list has {0} occurrences of {1}, '
            'out of {2} words').format(count, val, nwords)


dsk = {'words': 'apple orange apple pear orange pear pear',
       'nwords': (len, (str.split, 'words')),
       'val1': 'orange',
       'val2': 'apple',
       'val3': 'pear',
       'count1': (str.count, 'words', 'val1'),
       'count2': (str.count, 'words', 'val2'),
       'count3': (str.count, 'words', 'val3'),
       'out1': (format_str, 'count1', 'val1', 'nwords'),
       'out2': (format_str, 'count2', 'val2', 'nwords'),
       'out3': (format_str, 'count3', 'val3', 'nwords'),
       'print1': (print_and_return, 'out1'),
       'print2': (print_and_return, 'out2'),
       'print3': (print_and_return, 'out3')}

dask.visualize(dsk, filename='/Users/longguangbin/Work/temp/dask2.pdf')

from dask.threaded import get
from dask.optimization import cull
from dask.optimization import inline

outputs = ['print1', 'print2']
results = get(dsk, outputs)

dsk1, dependencies = cull(dsk, outputs)

dsk2 = inline(dsk1, dependencies=dependencies)
results = get(dsk2, outputs)

# https://docs.dask.org/en/latest/optimize.html

